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
    6. `bench.recording.install_recorder` monkeypatches
       `drcode.agent_model.build_model` BEFORE the app is created (§5):
       every model request of every agent — coder, tester, compaction —
       is logged with latency and usage into `<run_dir>/model_log.jsonl`;
    7. the user simulator (§6, `bench.user_sim.UserSimulator`) runs as a
       sibling asyncio task in the same loop: it auto-answers
       clarifications, fires the scenario's followups and guards against
       stuck tasks — every intervention lands in
       `<run_dir>/user_sim.jsonl`;
    8. `bench.settle.wait_settle` polls the settle criterion (the
       simulator's scenario failures act as hard settle-blockers); after
       settle the simulator is cancelled, `dump_diagnostics` snapshots a
       failed run, `checks.py` of the scenario runs afterwards and
       everything lands in `<run_dir>/result.json`.

Exit code: 0 = settled (+ green checks.py when the scenario has one),
1 = failed.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

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
    # Effective max_context_tokens per role (combo overrides applied,
    # §1.2): S3/S4 assert the small coding context actually reached the
    # role — the pre-flight (verify_resolution) fails the run otherwise,
    # this record keeps the fact in the artifacts.
    resolved_context_tokens: dict[str, int] = field(default_factory=dict)
    # §9 proxy mode: when the run went through the fault-injection proxy,
    # the artifacts must say so (log path, base address, injected faults).
    proxy_log: str | None = None
    proxy_base: str | None = None
    proxy_faults: dict[str, int] = field(default_factory=dict)
    tasks: list[dict[str, Any]] = field(default_factory=list)
    # User simulator (§6): how many interventions it made and which
    # scenario failures it recorded (report §10 must be able to tell
    # "the model is dumb" from "the simulator intervened").
    user_sim_actions: int = 0
    user_sim_failures: list[str] = field(default_factory=list)

    def dump(self, run_dir: Path) -> Path:
        out = run_dir / "result.json"
        out.parent.mkdir(parents=True, exist_ok=True)
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
    # Resolve both paths to absolute: the child runs with cwd=workspace, so a
    # relative workspace argument would be re-resolved against the workspace
    # itself and fail with FileNotFoundError.
    checks = scenario.checks_file.resolve()
    workspace = workspace.resolve()
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
    scenario: Scenario,
    combo_name: str,
    run_dir: Path,
    matrix_path: Path,
    *,
    use_proxy: bool = False,
) -> RunReport:
    """The §4 skeleton: prepare → headless DrCodeApp → briefs → settle.

    `use_proxy` (§9): force the proxy for a scenario without a `[proxy]`
    section — a fault-free recording proxy (the §5-recorder alternative);
    the scenario's own `[proxy]` section always enables it, with its
    fault script.
    """
    combo = get_combo(matrix_path, combo_name)
    report = RunReport(
        scenario=scenario.id,
        combo=combo.name,
        run_dir=str(run_dir),
        started_at=time.strftime("%Y-%m-%dT%H:%M:%S"),
    )

    # 0. §9: the fault-injection proxy starts BEFORE the run tree is
    #    generated — the catalog's base_urls must point at its ephemeral
    #    port. The proxy lives inside THIS process/loop: one run = one
    #    proxy = one upstream set (no cross-run interference, §2).
    proxy = None
    proxy_spec = scenario.proxy
    if proxy_spec is not None or use_proxy:
        from .proxy import FaultProxy, ProxyError, upstreams_for_providers

        providers, _ = load_matrix(matrix_path)
        used = {ref.partition("/")[0] for ref in combo.roles().values()}
        upstreams = upstreams_for_providers({name: providers[name] for name in sorted(used)})
        proxy = FaultProxy(
            upstreams,
            proxy_spec.faults if proxy_spec else (),
            log_path=run_dir / "proxy_log.jsonl",
            log_bodies=bool(proxy_spec.log_bodies) if proxy_spec else False,
        )
        try:
            proxy_base = await proxy.start()
        except ProxyError as e:
            report.reason = f"pre-flight failed: proxy failed to start: {e}"
            report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")
            report.dump(run_dir)
            return report
        report.proxy_base = proxy_base
        report.proxy_log = str(run_dir / "proxy_log.jsonl")

    # 1..7 — the run itself, with the proxy (if any) stopped in ALL exits.
    try:
        return await _run_with_optional_proxy(scenario, combo, run_dir, matrix_path, report)
    finally:
        if proxy is not None:
            await proxy.stop()
            report.proxy_faults = proxy.engine.fired_summary()


async def _run_with_optional_proxy(
    scenario: Scenario,
    combo,
    run_dir: Path,
    matrix_path: Path,
    report: RunReport,
) -> RunReport:
    """Everything after the proxy is up (§4 skeleton steps 1–7)."""
    # 1. Run tree (§3): seed copy, models.json, drcode.json, settings.json
    #    (stall_nudge=never, completed_retention=never), git init. With a
    #    proxy (§9) every generated base_url points at it.
    paths = prepare_run(
        scenario.dir,
        combo,
        run_dir,
        matrix_path=matrix_path,
        exists_ok=True,
        proxy_base=report.proxy_base,
    )
    # 2. Env hygiene BEFORE drcode is imported anywhere (see docstring).
    _sanitize_own_environ(paths.config_home)

    # drcode imports happen only now — with the sanitized environment.
    from drcode.tui.app import DrCodeApp

    from .settle import dump_diagnostics, wait_settle

    try:
        # 3. Pre-flight (§3 end): the generated config must resolve each
        #    role to the combo's model before any application code runs —
        #    through the proxy when one is up (§9).
        from .env_setup import verify_resolution

        report.resolved_roles = verify_resolution(
            paths.workspace,
            paths.config_home,
            combo,
            matrix_path=matrix_path,
            proxy_base=report.proxy_base,
        )
        from .matrix import effective_max_context, load_matrix

        providers, _ = load_matrix(matrix_path)
        report.resolved_context_tokens = {
            role: effective_max_context(combo, providers, role) for role in combo.roles()
        }
    except EnvSetupError as e:
        report.reason = f"pre-flight failed: {e}"
        report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        report.dump(run_dir)
        return report

    # §5: the recording wrapper around `agent_model.build_model`,
    # installed BEFORE the app exists — every agent (coder, tester,
    # compaction) is observed from its very first HTTP request, and the
    # per-request log lands in `<run_dir>/model_log.jsonl`. The recorder
    # is an observation instrument (§2), but its failure is
    # infrastructure: failing fast here beats burning the scenario
    # timeout on an unrecorded run. (The §9 proxy is an ADDITIONAL
    # observation point: latency cross-check, bench.metrics.)
    from .recording import install_recorder

    install_recorder(run_dir / "model_log.jsonl")

    try:
        app = DrCodeApp(paths.workspace)
    except Exception as e:
        report.reason = f"DrCodeApp failed to start: {type(e).__name__}: {e}"
        report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        dump_diagnostics(run_dir)
        report.dump(run_dir)
        return report

    # drcode ≥ 0.5: json layers no longer carry provider fields, so the
    # flat `Config` is never "ready" by itself — readiness is a PER-ROLE
    # property of the resolution (`providers.resolve` over the project
    # `models` refs and the user catalog). All three roles must resolve;
    # the app's own pipeline gates on the coding role in on_mount.
    from drcode.providers import AgentRole

    not_ready = [role.value for role in AgentRole if not app.resolved_config(role).is_ready]
    if not_ready:
        report.reason = (
            "drcode config is not ready for role(s) "
            f"{', '.join(not_ready)} (no model resolvable) — check "
            f"{paths.project_config} and {paths.models_catalog}"
        )
        report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        report.dump(run_dir)
        return report

    targets = []
    settled_ok = False
    sim = None
    try:
        async with app.run_test(size=APP_SIZE) as pilot:
            await pilot.pause()
            # 4. Queue the briefs (§4) — any allowed kind, including
            #    research (research skips the tester per plan §7). created
            #    AFTER mount on purpose: with an empty manager the app's
            #    on_mount takes the "new task" form instead of opening a
            #    task, so viewed_id stays None and no transcript is ever
            #    rendered into the measurements (§4/§13).
            for brief in scenario.briefs:
                targets.append(app.manager.create(brief.title, brief.text, kind=brief.task_kind()))
            _kick_pipeline(app)
            await pilot.pause()

            # 5. The user simulator (§6): a sibling asyncio task in the
            #    same loop, polling app.manager and mutating ONLY through
            #    the public TaskManager API. Every intervention is
            #    appended to <run_dir>/user_sim.jsonl.
            from .user_sim import UserSimulator

            sim = UserSimulator(app, scenario, targets, run_dir / "user_sim.jsonl")
            sim_task = asyncio.create_task(sim.run(), name="bench-user-sim")
            try:
                # 6. Settle detection (§4). The simulator's scenario
                #    failures (e.g. an unanswered clarification, §6 p.1)
                #    act as hard settle-blockers: a run that can no longer
                #    succeed must not burn the whole scenario timeout.
                result = await wait_settle(
                    app,
                    scenario,
                    pilot,
                    timeout=scenario.timeout_seconds,
                    targets=targets,
                    extra_blocker=sim.failure_reason,
                )
                settled_ok = result.ok
                report.reason = result.reason
                report.timed_out = result.timed_out
                report.settle_elapsed_s = result.elapsed_s
            finally:
                # §4 skeleton: the simulator is cancelled right after
                # settle (or if the settle wait itself crashed).
                sim_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await sim_task
                report.user_sim_actions = sim.actions
                report.user_sim_failures = list(sim.failures)
    except Exception as e:
        report.reason = f"app crashed: {type(e).__name__}: {e}"

    report.tasks = _task_summaries(app.manager)
    report.checks_ok, report.checks_output = run_checks(scenario, paths.workspace)

    if settled_ok and report.checks_ok is False:
        report.reason = f"settled but checks.py failed:\n{report.checks_output}"
    if sim is not None and sim.failures and settled_ok:
        # The simulator recorded scenario failures (§6) even though the
        # pipeline reached a quiet state: the run is still a failure.
        report.reason = f"settled but the user simulator failed: {'; '.join(sim.failures)}"

    report.ok = settled_ok and report.checks_ok is not False and not (sim and sim.failures)
    report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")

    if not report.ok:
        dump_diagnostics(run_dir)  # §4: dissect without repeating the run
    report.dump(run_dir)

    # §10: every run leaves metrics.json behind — extracted automatically
    # right after the run, from the same on-disk state the diagnostics use.
    # Never fatal: a broken extraction must not flip the run's exit code.
    try:
        from .metrics import extract_run_metrics

        extract_run_metrics(run_dir)
    except Exception as e:
        print(f"warning: metrics extraction failed: {e}", file=sys.stderr)

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
    parser.add_argument(
        "--use-proxy",
        action="store_true",
        help="route the run through the local proxy (§9) even when the "
        "scenario has no [proxy] section — a fault-free recording proxy",
    )
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
        report = asyncio.run(
            run_benchmark(scenario, args.combo, run_dir, matrix_path, use_proxy=args.use_proxy)
        )
    except (EnvSetupError, RunError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(f"run:      {report.run_dir}")
    print(f"scenario: {report.scenario}  combo: {report.combo}")
    if report.proxy_base:
        faults = ", ".join(f"{k}×{v}" for k, v in report.proxy_faults.items())
        print(f"proxy:    {report.proxy_base} (faults: {faults or 'none'})")
    if report.resolved_context_tokens:
        ctx = ", ".join(f"{role}={n}" for role, n in sorted(report.resolved_context_tokens.items()))
        print(f"context:  max_context_tokens per role: {ctx}")
    print(f"result:   {'OK' if report.ok else 'FAILED'} — {report.reason}")
    for t in report.tasks:
        print(
            f"  [{t['status']}] {t['title']} "
            f"(verification={t['verification']}, rounds={t['n_testing_rounds']})"
        )
    if report.checks_ok is not None:
        print(f"checks.py: {'green' if report.checks_ok else 'RED'}")
    if report.user_sim_actions or report.user_sim_failures:
        print(f"user sim: {report.user_sim_actions} intervention(s) ({run_dir / 'user_sim.jsonl'})")
        for failure in report.user_sim_failures:
            print(f"  sim failure: {failure}")
    if not report.ok:
        print(f"diagnostics: {run_dir / 'diagnostics'}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
