"""Tests of the matrix runner (bench.runner, plan §8, stage 5 of §12).

The subprocess layer is faked: `bench.runner.subprocess.run` is
monkeypatched to script what `python -m bench.run_one` would do — write
(or not write) `result.json` into the run dir and exit with a code. The
planning, the parallelism bound, the infra/content failure separation,
the retries and the summary are checked without any real models.
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import pytest
from bench.runner import (
    Job,
    JobOutcome,
    Runner,
    RunnerError,
    discover_scenarios,
    is_infrastructure_failure,
    plan_jobs,
    slug,
)

REPO = Path(__file__).resolve().parents[1]

MATRIX = """
[providers.p]
base_url = "http://127.0.0.1:1/v1"
api_key = ""

[providers.p.models.m]
max_context_tokens = 100000
max_tokens = 4096

[[combo]]
name = "combo-a"
coding = "p/m"
tester = "p/m"
compaction = "p/m"

[[combo]]
name = "combo-b"
coding = "p/m"
tester = "p/m"
compaction = "p/m"
"""

SCENARIO_TOML = """
timeout = 1

[[briefs]]
title = "t"
kind = "feature"
text = "do nothing"
"""


@pytest.fixture
def bench_env(tmp_path: Path) -> tuple[Path, Path]:
    matrix = tmp_path / "matrix.toml"
    matrix.write_text(MATRIX, encoding="utf-8")
    scenarios = tmp_path / "scenarios"
    for sid in ("s1_x", "s2_y"):
        d = scenarios / sid
        d.mkdir(parents=True)
        (d / "scenario.toml").write_text(SCENARIO_TOML, encoding="utf-8")
        (d / "seed").mkdir()
        (d / "seed" / "f.txt").write_text("x", encoding="utf-8")
    return matrix, scenarios


def test_discover_scenarios_sorted(bench_env) -> None:
    _, scenarios = bench_env
    assert discover_scenarios(scenarios) == ["s1_x", "s2_y"]


def test_slug_sanitizes_combo_name() -> None:
    assert slug("strong-coder/cheap-tester") == "strong-coder-cheap-tester"
    assert slug("a b/c") == "a-b-c"


def test_plan_jobs_full_sweep(bench_env) -> None:
    matrix, scenarios = bench_env
    jobs, loaded, combos = plan_jobs(matrix, scenarios, "all", "", repeats=3)
    assert [s.id for s in loaded] == ["s1_x", "s2_y"]
    assert combos == ["combo-a", "combo-b"]
    assert len(jobs) == 2 * 2 * 3
    assert {(j.scenario, j.combo, j.repeat) for j in jobs} == {
        (s, c, r) for s in ("s1_x", "s2_y") for c in ("combo-a", "combo-b") for r in range(3)
    }


def test_plan_jobs_scenario_and_combo_filters(bench_env) -> None:
    matrix, scenarios = bench_env
    jobs, _, combos = plan_jobs(matrix, scenarios, "s2_y", "combo-b", repeats=2)
    assert len(jobs) == 2
    assert all(j.scenario == "s2_y" and j.combo == "combo-b" for j in jobs)
    assert combos == ["combo-b"]


def test_plan_jobs_unknown_scenario_fails(bench_env) -> None:
    matrix, scenarios = bench_env
    with pytest.raises(RunnerError):
        plan_jobs(matrix, scenarios, "s9_missing", "", repeats=1)


def test_plan_jobs_unknown_combo_fails(bench_env) -> None:
    matrix, scenarios = bench_env
    with pytest.raises(RunnerError):
        plan_jobs(matrix, scenarios, "all", "nope", repeats=1)


def test_plan_jobs_rejects_research_context_without_research_role(bench_env) -> None:
    """A scenario `[context] research` cap (§1.2) on a combo that assigns no
    research role would silently never apply (the role falls back to
    coding) — the planning knows both sides and fails loudly instead of
    burning run slots."""
    matrix, scenarios = bench_env
    d = scenarios / "s3_ctx"
    d.mkdir(parents=True)
    (d / "scenario.toml").write_text(
        SCENARIO_TOML + "\n[context]\nresearch = 2048\n", encoding="utf-8"
    )
    (d / "seed").mkdir()
    (d / "seed" / "f.txt").write_text("x", encoding="utf-8")
    with pytest.raises(RunnerError, match="assigns no 'research' role"):
        plan_jobs(matrix, scenarios, "s3_ctx", "combo-a", repeats=1)


# -- infra vs content classification ----------------------------------------------


def test_is_infrastructure_failure_classification() -> None:
    assert is_infrastructure_failure(None)  # no verdict at all
    assert is_infrastructure_failure({"ok": False, "reason": "pre-flight failed: x"})
    assert is_infrastructure_failure({"ok": False, "reason": "DrCodeApp failed to start: boom"})
    assert is_infrastructure_failure(
        {"ok": False, "reason": "drcode config is not ready (no model resolvable)"}
    )
    # Substantive failures: a verdict is a data point, never retried.
    assert not is_infrastructure_failure({"ok": True})
    assert not is_infrastructure_failure(
        {"ok": False, "reason": "timeout (45 min): last blocker: ..."}
    )
    assert not is_infrastructure_failure(
        {"ok": False, "reason": "settled but checks.py failed: ..."}
    )
    assert not is_infrastructure_failure({"ok": False, "reason": "app crashed: X"})


# -- job execution with a faked run_one subprocess ---------------------------------


def install_fake(monkeypatch, scripts, timeout_flag: list[str] | None = None):
    """Monkeypatch runner.subprocess.run with the scripted fake."""
    import bench.runner as runner_mod

    calls: list[dict] = []

    def fake_run(cmd, **kwargs):
        scenario, combo, run_dir = cmd[3], cmd[4], Path(cmd[5])
        # rep index from the run dir name (…-rep<k>[-tryN])
        name = run_dir.name
        rep = int(name.split("-rep")[1].split("-")[0])
        key = (scenario, combo, rep)
        calls.append({"key": key, "cmd": cmd, "kwargs": kwargs, "run_dir": run_dir})
        script = scripts[key]
        rc, payload = script.pop(0)
        if rc == 124:
            raise subprocess.TimeoutExpired(cmd, timeout=10, output=b"", stderr=b"")
        if payload is not None:
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "result.json").write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.CompletedProcess(cmd, rc, stdout="out", stderr="err")

    monkeypatch.setattr(runner_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(runner_mod, "INFRA_BACKOFF_S", 0.0)
    return calls


def test_runner_retries_infra_failure_then_succeeds(bench_env, tmp_path, monkeypatch) -> None:
    matrix, scenarios = bench_env
    ok = {"ok": True, "reason": "settled", "checks_ok": True}
    scripts = {
        ("s1_x", "combo-a", 0): [(2, None), (0, ok)],  # infra → retry → ok
        ("s1_x", "combo-b", 0): [(0, {"ok": False, "reason": "timeout"})],  # data point
        ("s2_y", "combo-a", 0): [
            (1, {"ok": False, "reason": "pre-flight failed: x"}),
            (1, {"ok": False, "reason": "pre-flight failed: y"}),
            (0, ok),
        ],
        ("s2_y", "combo-b", 0): [(0, ok)],
    }
    calls = install_fake(monkeypatch, scripts)
    runner = Runner(matrix, tmp_path / "runs", parallel=2, verbose=False)
    jobs, _, _ = plan_jobs(matrix, scenarios, "all", "", repeats=1)
    outcomes = runner.run(jobs)

    by_key = {(o.scenario, o.combo, o.repeat): o for o in outcomes}
    retried = by_key[("s1_x", "combo-a", 0)]
    assert retried.ok is True
    assert retried.infra_attempts == 1
    assert len(retried.run_dirs) == 2
    assert retried.run_dirs[0].endswith("rep0")
    assert retried.run_dirs[1].endswith("rep0-try2")

    content = by_key[("s1_x", "combo-b", 0)]
    assert content.ok is False and content.content_failure
    assert content.infra_attempts == 0 and len(content.run_dirs) == 1

    twice_retried = by_key[("s2_y", "combo-a", 0)]
    assert twice_retried.ok is True and twice_retried.infra_attempts == 2

    # stdout/stderr of every attempt are captured into the run dir (§10).
    for call in calls:
        assert (call["run_dir"] / "stdout.log").read_text() == "out"
        assert (call["run_dir"] / "stderr.log").read_text() == "err"

    summary = json.loads((tmp_path / "runs" / "runner-summary.json").read_text(encoding="utf-8"))
    assert summary["totals"]["jobs"] == 4
    assert summary["totals"]["ok"] == 3
    assert summary["totals"]["content_failures"] == 1
    assert summary["totals"]["infra_unresolved"] == 0
    assert summary["totals"]["infra_retries"] == 3


def test_runner_infra_exhausted_is_unresolved(bench_env, tmp_path, monkeypatch) -> None:
    matrix, scenarios = bench_env
    scripts = {
        ("s1_x", "combo-a", 0): [(2, None), (2, None), (2, None)],
    }
    install_fake(monkeypatch, scripts)
    runner = Runner(matrix, tmp_path / "runs", parallel=1, max_infra_retries=2, verbose=False)
    jobs, _, _ = plan_jobs(matrix, scenarios, "s1_x", "combo-a", repeats=1)
    outcomes = runner.run(jobs)
    (outcome,) = outcomes
    assert outcome.ok is None
    assert outcome.content_failure is False
    assert len(outcome.run_dirs) == 3
    assert "infrastructure failure after 3 attempts" in outcome.reason


def test_runner_timeout_killed_counts_as_infra(bench_env, tmp_path, monkeypatch) -> None:
    matrix, scenarios = bench_env
    ok = {"ok": True, "reason": "settled"}
    scripts = {
        ("s1_x", "combo-a", 0): [(124, None), (0, ok)],
    }
    install_fake(monkeypatch, scripts)
    runner = Runner(matrix, tmp_path / "runs", parallel=1, verbose=False)
    jobs, _, _ = plan_jobs(matrix, scenarios, "s1_x", "combo-a", repeats=1)
    outcomes = runner.run(jobs)
    (outcome,) = outcomes
    assert outcome.ok is True and outcome.infra_attempts == 1


def test_run_sweep_generates_report(bench_env, tmp_path, monkeypatch) -> None:
    matrix, scenarios = bench_env
    ok = {"ok": True, "reason": "settled", "checks_ok": True}
    scripts = {
        (s, c, r): [(0, ok)]
        for s in ("s1_x", "s2_y")
        for c in ("combo-a", "combo-b")
        for r in range(2)
    }
    install_fake(monkeypatch, scripts)
    from bench.runner import run_sweep

    outcomes, report_path = run_sweep(
        matrix,
        scenarios,
        tmp_path / "runs",
        scenario_filter="all",
        repeats=2,
        parallel=3,
    )
    assert len(outcomes) == 8
    assert all(o.ok for o in outcomes)
    assert report_path is not None and report_path.is_file()
    text = report_path.read_text(encoding="utf-8")
    assert "# drcode-bench report" in text
    assert "combo-a" in text and "s1_x" in text


# -- console log: completion order + durations --------------------------------------


def test_done_log_follows_completion_order(bench_env, tmp_path, monkeypatch, capsys) -> None:
    """With parallel > 1 the `[done]` lines must appear in COMPLETION order,
    not submission order: a slow job submitted first must report last, even
    though fast jobs submitted after it finish long before it does."""
    matrix, _ = bench_env
    durations = {"s1_x": 1.0, "s2_y": 0.2}
    # parallel=2: worker slots take s1_x/rep0 (1.0 s) and s2_y/rep0 (0.2 s);
    # the third job (s2_y/rep1) starts when the fast one frees its slot at
    # ~0.2 s and finishes at ~0.4 s — long before the first job at ~1.0 s.
    # Completion order (s2_y0, s2_y1, s1_x0) differs from submission order
    # (s1_x0, s2_y0, s2_y1).
    jobs = [
        Job(scenario=sid, combo="combo-a", repeat=rep, timeout_seconds=10)
        for sid, rep in (("s1_x", 0), ("s2_y", 0), ("s2_y", 1))
    ]

    def fake_attempt(self, job: Job, run_dir: Path):
        time.sleep(durations[job.scenario])
        return 0, {"ok": True, "reason": "settled"}, durations[job.scenario]

    monkeypatch.setattr(Runner, "_attempt", fake_attempt)
    runner = Runner(matrix, tmp_path / "runs", parallel=2, verbose=True)
    outcomes = runner.run(jobs)

    done_lines = [
        line for line in capsys.readouterr().out.splitlines() if line.startswith("[done]")
    ]
    assert len(done_lines) == 3
    completion_order = [line.split()[1] for line in done_lines]
    assert completion_order == ["s2_y", "s2_y", "s1_x"]

    # But outcomes and the summary keep the stable submission order.
    assert [(o.scenario, o.repeat) for o in outcomes] == [(j.scenario, j.repeat) for j in jobs]
    summary = json.loads((tmp_path / "runs" / "runner-summary.json").read_text(encoding="utf-8"))
    assert [(j["scenario"], j["repeat"]) for j in summary["jobs"]] == [
        (j.scenario, j.repeat) for j in jobs
    ]
    assert all(j["elapsed_seconds"] is not None for j in summary["jobs"])


def test_done_log_includes_job_duration(bench_env, tmp_path, monkeypatch, capsys) -> None:
    """Each `[done]` line carries the job's wall-clock duration, formatted
    by format_duration, and the outcome records it for the summary."""
    matrix, _ = bench_env
    job = Job(scenario="s1_x", combo="combo-a", repeat=0, timeout_seconds=10)

    def fake_attempt(self, job: Job, run_dir: Path):
        # The duration must be REAL wall time: run_job measures the job
        # itself (all attempts + backoff), it does not trust _attempt.
        time.sleep(1.05)
        return 0, {"ok": True, "reason": "settled"}, 1.05

    monkeypatch.setattr(Runner, "_attempt", fake_attempt)
    runner = Runner(matrix, tmp_path / "runs", parallel=1, verbose=True)
    (outcome,) = runner.run([job])

    out = capsys.readouterr().out
    done_line = next(line for line in out.splitlines() if line.startswith("[done]"))
    assert "in 1 s" in done_line
    assert outcome.elapsed_seconds == pytest.approx(1.05, abs=0.1)


def test_runs_dir_is_gitignored() -> None:
    """DoD stage 5: run artifacts (runs/) must never be committed."""
    proc = subprocess.run(
        ["git", "check-ignore", "-v", "runs/probe-run"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, "runs/ is not gitignored"
    assert ".gitignore" in proc.stdout


# -- CLI wiring --------------------------------------------------------------------


def test_cli_run_invokes_sweep_and_report(tmp_path, monkeypatch, capsys) -> None:
    import bench.cli as cli
    import bench.runner as runner_mod

    captured: dict = {}

    def fake_sweep(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return (
            [JobOutcome(scenario="s1_happy", combo="c", repeat=0, ok=True, reason="settled")],
            tmp_path / "runs" / "report.md",
        )

    monkeypatch.setattr(runner_mod, "run_sweep", fake_sweep)
    rc = cli.main(
        [
            "run",
            "--scenario",
            "s6_queue_priority",
            "--repeats",
            "2",
            "--parallel",
            "2",
            "--runs-dir",
            str(tmp_path / "runs"),
        ]
    )
    assert rc == 0
    assert captured["kwargs"]["scenario_filter"] == "s6_queue_priority"
    assert captured["kwargs"]["repeats"] == 2
    assert captured["kwargs"]["parallel"] == 2
    out = capsys.readouterr().out
    assert "repeats:   2" in out and "report:" in out


def test_cli_run_unresolved_infra_exit_code(tmp_path, monkeypatch) -> None:
    import bench.cli as cli
    import bench.runner as runner_mod

    def fake_sweep(*args, **kwargs):
        return (
            [
                JobOutcome(
                    scenario="s1_happy",
                    combo="c",
                    repeat=0,
                    ok=None,
                    reason="infrastructure failure after 3 attempts: x",
                )
            ],
            None,
        )

    monkeypatch.setattr(runner_mod, "run_sweep", fake_sweep)
    rc = cli.main(["run", "--scenario", "s1_happy", "--runs-dir", str(tmp_path / "r")])
    assert rc == 1
