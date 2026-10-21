"""End-to-end runs of the interactive scenarios S2a/S2b/S5 (plan §7, stage
3 of §12) — on the local scripted gateway (tests/fake_gateway.py), i.e. on
the REAL pipeline (headless DrCodeApp, real OpenAIChatModel SSE streaming)
with a LOCAL model, no external network.

What each e2e run proves (the DoD of the stage):

- the run settles by itself, the user simulator (§6) intervenes exactly
  where the scenario needs it, and everything lands in user_sim.jsonl +
  metrics.json;
- each scenario's checks.py is green on the produced workspace.
"""

from __future__ import annotations

import dataclasses
import json
import os
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

MATRIX_TEMPLATE = """
[providers.fake]
base_url = "http://127.0.0.1:{port}/v1"
api_key  = ""

[providers.fake.models.fake-compaction]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.fake-coder]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.fake-tester]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s2a-coder]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s2a-tester]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s2b-coder]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s2b-tester]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s5-coder]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s5-tester]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s3-coder]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s4-coder]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s4-tester]
max_context_tokens = 100000
max_tokens = 8192

[[combo]]
name       = "{combo}"
coding     = "fake/{coder}"
tester     = "fake/{tester}"
compaction = "fake/fake-compaction"
"""

COMBOS = {
    "s2a_bug_followup": ("s2a-coder", "s2a-tester"),
    "s2b_bug_report": ("s2b-coder", "s2b-tester"),
    "s5_clarification": ("s5-coder", "s5-tester"),
    # S3/S4: the compaction lives on the CODER side (S3) / the TESTER side
    # (S4); the inflated gateway usage (fake_gateway._usage_for) trips the
    # real gates of drcode on the 100000-token context.
    "s3_compaction_coder": ("s3-coder", "fake-tester"),
    "s4_compaction_tester": ("s4-coder", "s4-tester"),
}


@pytest.fixture
def env_guard():
    saved = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(saved)


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


async def _run_scenario(tmp_path: Path, monkeypatch, scenario_id: str):
    from tests.fake_gateway import start

    server = await start(0)
    port = server.sockets[0].getsockname()[1]
    try:
        coder, tester = COMBOS[scenario_id]
        combo = f"{scenario_id}-roles"
        matrix_path = tmp_path / "matrix.toml"
        matrix_path.write_text(
            MATRIX_TEMPLATE.format(port=port, combo=combo, coder=coder, tester=tester),
            encoding="utf-8",
        )

        # In-process isolation (see tests/test_recording.py): drcode.config
        # binds the user config dir at import time.
        import drcode.config as dconfig

        run_dir = tmp_path / "runs" / scenario_id
        config_home = run_dir / "config-home" / "drcode"
        config_home.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(dconfig, "_USER_CONFIG_DIR", config_home)
        monkeypatch.setattr(dconfig, "USER_CONFIG_FILE", config_home / "drcode.json")

        from bench.run_one import run_benchmark
        from bench.scenario import load_scenario_by_id

        scenario = load_scenario_by_id(REPO / "scenarios", scenario_id)
        # Shrink the 45-minute soft limit: a scripted run settles in seconds;
        # a hung run must fail the test in minutes, not hours.
        scenario = dataclasses.replace(scenario, timeout_min=3)
        return await run_benchmark(scenario, combo, run_dir, matrix_path)
    finally:
        server.close()
        await server.wait_closed()


async def test_s2a_bug_followup_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    report = await _run_scenario(tmp_path, monkeypatch, "s2a_bug_followup")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = [t for t in report.tasks if t["title"].startswith("Почините div()")]
    assert brief["status"] == "completed"
    assert brief["verification"] == "Verified successfully"
    assert brief["n_testing_rounds"] >= 2  # FAILED round + follow-up round

    # §6: every simulator intervention is on the record.
    assert (run_dir / "user_sim.jsonl").is_file()
    records = read_jsonl(run_dir / "user_sim.jsonl")
    followups = [r for r in records if r["action"] == "followup"]
    assert followups, "the simulator must have sent the follow-up"
    assert followups[0]["task_status"] == "completed"  # met the FAILED verdict
    assert "FAILED" in followups[0]["detail"]["text"]

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["totals"]["n_testing_rounds"] >= 2
    assert metrics["user_sim"]["interventions"] >= 1
    assert not metrics["user_sim"]["failures"]


async def test_s2b_bug_report_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    report = await _run_scenario(tmp_path, monkeypatch, "s2b_bug_report")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True

    bugs = [t for t in report.tasks if t["kind"] == "bug"]
    assert len(bugs) == 1, "the tester must have filed exactly one bug report"
    (bug,) = bugs
    assert bug["status"] == "completed"
    assert bug["verification"] == "Verified successfully"  # passed its testing
    assert bug["activated_at"]

    # Queue priority: the bug task ran before the second brief.
    scenario_tasks = {t["title"]: t for t in report.tasks}
    brief_b = scenario_tasks["Реализуйте export_api()"]
    brief_a = scenario_tasks["Почините div() (ValueError вместо ZeroDivisionError)"]
    assert brief_a["activated_at"] < bug["activated_at"] < brief_b["activated_at"]

    # §6: no scenario followups/answers here — the simulator intervened 0 times.
    records = read_jsonl(run_dir / "user_sim.jsonl")
    assert not [r for r in records if r["action"] in ("followup", "clarification_answer")]

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["totals"]["n_bug_tasks"] == 1
    assert metrics["totals"]["n_testing_rounds"] >= 3  # A, the bug task, B
    assert not (metrics["user_sim"] or {}).get("failures", [])


async def test_s5_clarification_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    report = await _run_scenario(tmp_path, monkeypatch, "s5_clarification")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = report.tasks
    assert brief["status"] == "completed"
    assert brief["verification"] == "Verified successfully"

    # The full round-trip is on the simulator's record: answered while the
    # task was AWAITING_CLARIFICATION, exactly once.
    records = read_jsonl(run_dir / "user_sim.jsonl")
    answers = [r for r in records if r["action"] == "clarification_answer"]
    assert len(answers) == 1
    assert answers[0]["task_status"] == "clarification"

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["user_sim"]["interventions"] == 1
    assert not metrics["user_sim"]["failures"]
    (task,) = metrics["tasks"]
    # The answer was consumed as ONE prompt (§7 S5: no duplicates).
    assert task["transcript"]["n_user_prompts"] == 2  # brief + answer


async def test_s3_compaction_coder_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S3 (plan §7, stage 4): the coder's compaction on a context the
    gateway keeps near-full — real mid-run/turn-boundary gate, real
    summary, real continuation turn; checks.py green; metrics carry the
    compaction block."""
    report = await _run_scenario(tmp_path, monkeypatch, "s3_compaction_coder")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = report.tasks
    assert brief["status"] == "completed"
    assert brief["verification"] == "Verified successfully"

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    (task,) = metrics["tasks"]
    comp = task["compactions"]
    # §7 S3 assertions: the compaction really happened...
    assert comp["n_succeeded"] >= 1
    assert comp["n_started"] >= 1
    # ...at a REAL gate of drcode (mid-run pause or turn boundary), not by
    # our own doing:
    assert comp["mid_run_pause"] or comp["turn_boundary_pause"]
    # The summary reached the coder transcript, the original prompt
    # survived verbatim (§1.4):
    assert comp["n_summaries_in_transcript"] >= 1
    assert task["transcript"]["n_user_prompts"] >= 1
    assert not comp["repeat_compaction"]

    # The harness recorded the effective per-role context limits (§1.2).
    assert report.resolved_context_tokens["coding"] == 100000

    # §10: the report generation must not choke on compaction artifacts.
    from bench.report import generate_report

    generate_report(run_dir.parent)


async def test_s4_compaction_tester_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S4 (plan §7, stage 4): the tester's mid-round compaction — the
    round is rewritten in place (summary in tester_messages[-1]), the
    verdict is set, checks.py green. The threshold-source classification
    (§1.2/§13: coding model's config) is exercised with equal limits —
    'coding' classification, no regression flag."""
    report = await _run_scenario(tmp_path, monkeypatch, "s4_compaction_tester")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = report.tasks
    assert brief["status"] == "completed"
    assert brief["verification"] == "Verified successfully"
    assert brief["n_testing_rounds"] == 1

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    (task,) = metrics["tasks"]
    comp = task["compactions"]
    # §7 S4 assertions: a compaction inside the testing round...
    assert comp["by_phase"]["tester"] >= 1
    assert comp["n_succeeded"] >= 1
    # ...the last round was rewritten with the summary in place:
    assert comp["n_summaries_in_transcript"] >= 1
    rounds = task["testing"]["rounds"]
    assert rounds[-1]["has_summary"] is True
    # §1.2/§13: the threshold-source block exists and does NOT flag a
    # regression (limits are equal here — classification is moot but must
    # not say 'tester').
    threshold = comp["tester_threshold"]
    assert threshold is not None
    assert threshold["source"] in ("coding", "unknown")
    assert metrics["tester_threshold_from_coding"] is not False

    # §10: the report must render the run (incl. the threshold remark).
    from bench.report import generate_report

    generate_report(run_dir.parent)
