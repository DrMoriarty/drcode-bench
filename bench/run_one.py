"""One benchmark run = one subprocess (plan drcode-bench.md, §4).

    python -m bench.run_one <scenario> <combo> <run_dir> [--matrix PATH]

Inside this process:

    1. the run tree is prepared (bench.env_setup.prepare_run, §3): the
       seed of the scenario is copied into `workspace/`, the combo's
       models.json / drcode.json / settings.json are generated;
    2. the process environment is sanitized IN PLACE and BEFORE drcode is
       imported (drcode.config binds XDG_CONFIG_HOME at import time; the
       repo `.env` of drcode leaks through pydantic-settings — only a
       fresh process with a scrubbed environment gives clean layered
       config, plan §2/§13): XDG_CONFIG_HOME → <run_dir>/config-home,
       every DRCODE_* variable stripped;
    3. a real `DrCodeApp` runs headless via textual `run_test()` in a
       plain asyncio loop (no pytest — same path as drcode's
       tests/test_network_app.py, but with real models and minutes
       instead of seconds);
    4. the scenario briefs are queued through `app.manager.create`
       (kinds feature/bug only, §7) and the pipeline is kicked exactly
       like the TUI's own submit action does;
    5. `viewed_id` is NEVER touched: opening a task renders the whole
       transcript and would put render overhead into the measurements
       (plan §4/§13);
    6. `bench.settle.wait_settle` polls the settle criterion; on failure
       `dump_diagnostics` snapshots the run, `checks.py` of the scenario
       runs afterwards and everything lands in `<run_dir>/result.json`.

Exit code: 0 = settled (+ green checks.py when the scenario has one),
1 = failed.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from .env_setup import EnvSetupError, prepare_run, subprocess_env
from .matrix import MatrixError, get_combo, load_matrix
from .scenario import Scenario, ScenarioError, load_scenario

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = PROJECT_ROOT / "matrix.toml"
SCENARIOS_ROOT = PROJECT_ROOT / "scenarios"

APP_SIZE = (120, 40)  # plan §4: run_test size only affects the layout


class RunError(RuntimeError):
    """The run could not even start (infrastructure failure)."""


@dataclass
class RunReport:
    """What lands in `<run_dir>/result.json` (§10 consumes it later)."""

    scenario: str
    combo: str
    run_dir: str
    started_at: str
    finished_at: str = ""
    ok: bool = False
    reason: str = ""
    timed_out: bool = False
    settle_elapsed_s: float = 0.0
    checks_ok: bool | None = None  # None = scenario has no checks.py
    checks_output: str = ""
    resolved_roles: dict[str, str] = field(default_factory=dict)
    tasks: list[dict[str, object]] = field(default_factory=list)

    def dump(self, run_dir: Path) -> Path:
        out = run_dir / "result.json"
        out.write_text(
            json.dumps(self.__dict__, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return out


def _sanitize_own_environ(config_home: Path) -> None:
    """Scrub THIS process's environment before drcode is imported (§3/§13):
    XDG_CONFIG_HOME at import time decides the user-level config dir for
    the whole run, and any inherited DRCODE_* variable (or the repo .env
    leak of drcode via pydantic-settings) would override the per-role
    model selection for ALL roles."""
    clean = subprocess_env(config_home)
    for key in list(os.environ):
        if key not in clean:
            del os.environ[key]
    os.environ.update(clean)


def _kick_pipeline(app) -> None:
    """Start the pipeline for the just-created briefs.

    `TaskManager.create` only queues a task; promotion happens in
    `_advance`, which in the live TUI is called by the submit action. The
    harness must not fork the pipeline (plan §2) — it uses the very same
    entry point, scheduled on the app's own loop.
    """
    app.call_later(app._advance)


def run_checks(scenario: Scenario, workspace: Path) -> tuple[bool | None, str]:
    """Run the scenario's mechanical correctness check (§7): the verdict
    is never built on the agents' words. `checks.py <workspace>` exit 0 =
    green. No checks.py → None (nothing to assert mechanically)."""
    checks = scenario.checks_file
    if not checks.is_file():
        return None, ""
    result = subprocess.run(
        [sys.executable, str(checks), str(workspace)],
        capture_output=True,
        text=True,
        cwd=str(workspace),
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def _task_summaries(manager) -> list[dict[str, object]]:
    out = []
    for t in manager.all_tasks():
        out.append(
            {
                "id": t.id,
                "title": t.title,
                "kind": t.kind.value,
                "status": t.status.value,
                "verification": t.verification.value if t.verification else None,
                "unfinished": t.unfinished,
                "n_testing_rounds": len(t.tester_messages),
                "created_at": t.created_at.isoformat(),
                "activated_at": t.activated_at.isoformat() if t.activated_at else None,
                "completed_at": t.completed_at.isoformat() if t.completed_at else None,
            }
        )
    return out


async def run_benchmark(
    scenario: Scenario, combo_name: str, run_dir: Path, matrix_path: Path
) -> RunReport:
    """The §4 skeleton: prepare → headless DrCodeApp → briefs → settle."""
    combo = get_combo(matrix_path, combo_name)
    report = RunReport(
        scenario=scenario.id,
        combo=combo.name,
        run_dir=str(run_dir),
        started_at=time.strftime("%Y-%m-%dT%H:%M:%S"),
    )

    # 1. Run tree (§3): seed copy, models.json, drcode.json, settings.json
    #    (stall_nudge=never, completed_retention=never), git init.
    paths = prepare_run(
        scenario.dir, combo, run_dir, matrix_path=matrix_path, exists_ok=True
    )
    # 2. Env hygiene BEFORE drcode is imported anywhere (see docstring).
    _sanitize_own_environ(paths.config_home)

    # drcode imports happen only now — with the sanitized environment.
    from drcode.tui.app import DrCodeApp

    from .settle import dump_diagnostics, wait_settle

    try:
        # 3. Pre-flight (§3 end): the generated config must resolve each
        #    role to the combo's model before any application code runs.
        from .env_setup import verify_resolution

        report.resolved_roles = verify_resolution(
            paths.workspace, paths.config_home, combo, matrix_path=matrix_path
        )
    except EnvSetupError as e:
        report.reason = f"pre-flight failed: {e}"
        report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        report.dump(run_dir)
        return report

    # §5 hook: the recording wrapper around build_model, when the module
    # has arrived (plan stage 3). Absent → the run proceeds unrecorded.
    try:
        from .recording import install_recorder  # noqa: F401  (stage 3)
    except ImportError:
        install_recorder = None
    if install_recorder is not None:
        install_recorder(run_dir / "model_log.jsonl")

    try:
        app = DrCodeApp(paths.workspace)
    except Exception as e:  # noqa: BLE001 - a broken app is a failed run
        report.reason = f"DrCodeApp failed to start: {type(e).__name__}: {e}"
        report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        dump_diagnostics(run_dir)
        report.dump(run_dir)
        return report

    if not app.config.is_ready:
        report.reason = (
            "drcode config is not ready (no model resolvable) — check "
            f"{paths.project_config} and {paths.models_catalog}"
        )
        report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        report.dump(run_dir)
        return report

    targets = []
    settled_ok = False
    try:
        async with app.run_test(size=APP_SIZE) as pilot:
            await pilot.pause()
            # 4. Queue the briefs (§4). NOT kind research — §7. created
            #    AFTER mount on purpose: with an empty manager the app's
            #    on_mount takes the "new task" form instead of opening a
            #    task, so viewed_id stays None and no transcript is ever
            #    rendered into the measurements (§4/§13).
            for brief in scenario.briefs:
                targets.append(
                    app.manager.create(brief.title, brief.text, kind=brief.task_kind())
                )
            _kick_pipeline(app)
            await pilot.pause()

            # 5. Settle detection (§4). The user simulator (§6, stage 3)
            #    will run as a sibling asyncio task here.
            result = await wait_settle(
                app, scenario, pilot, timeout=scenario.timeout_seconds, targets=targets
            )
            settled_ok = result.ok
            report.reason = result.reason
            report.timed_out = result.timed_out
            report.settle_elapsed_s = result.elapsed_s
    except Exception as e:  # noqa: BLE001 - any crash is a failed run
        report.reason = f"app crashed: {type(e).__name__}: {e}"

    report.tasks = _task_summaries(app.manager)
    report.checks_ok, report.checks_output = run_checks(scenario, paths.workspace)

    if settled_ok and report.checks_ok is False:
        report.reason = f"settled but checks.py failed:\n{report.checks_output}"

    report.ok = settled_ok and report.checks_ok is not False
    report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")

    if not report.ok:
        dump_diagnostics(run_dir)  # §4: dissect without repeating the run
    report.dump(run_dir)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bench.run_one",
        description="One benchmark run: headless DrCodeApp + settle detection (§4).",
    )
    parser.add_argument("scenario", help="scenario id (folder under scenarios/)")
    parser.add_argument("combo", help="combo name from matrix.toml (empty = first)")
    parser.add_argument("run_dir", help="directory for this run's artifacts")
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX), help="path to matrix.toml")
    args = parser.parse_args(argv)

    try:
        scenario = load_scenario(SCENARIOS_ROOT / args.scenario)
        matrix_path = Path(args.matrix)
        if args.combo:
            get_combo(matrix_path, args.combo)  # validate early
        else:
            _, combos = load_matrix(matrix_path)
            if not combos:
                raise MatrixError(f"{matrix_path}: no [[combo]] entries")
    except (ScenarioError, MatrixError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    run_dir = Path(args.run_dir)
    try:
        report = asyncio.run(run_benchmark(scenario, args.combo, run_dir, matrix_path))
    except (EnvSetupError, RunError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(f"run:      {report.run_dir}")
    print(f"scenario: {report.scenario}  combo: {report.combo}")
    print(f"result:   {'OK' if report.ok else 'FAILED'} — {report.reason}")
    for t in report.tasks:
        print(
            f"  [{t['status']}] {t['title']} "
            f"(verification={t['verification']}, rounds={t['n_testing_rounds']})"
        )
    if report.checks_ok is not None:
        print(f"checks.py: {'green' if report.checks_ok else 'RED'}")
    if not report.ok:
        print(f"diagnostics: {run_dir / 'diagnostics'}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
