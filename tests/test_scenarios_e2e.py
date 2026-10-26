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

import csv
import dataclasses
import json
import os
import re
import subprocess
import sys
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

# The optional 4th combo role (research): its OWN model id — the gateway
# scripts per model id, so a research transcript would be distinguishable
# from the coder's. Scenarios never queue kind=research briefs (plan §7),
# so the model is pre-flighted and resolved but never called — exactly the
# "assigned, wired, idle" contract the research role has in drcode.
[providers.fake.models.fake-research]
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
# The CATALOG context is big on purpose: the small limit (5000) must reach
# the coding ROLE via the scenario's [context] section — not via the
# catalog entry (§1.2, scenario → combo → catalog priority).
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s4-coder]
max_context_tokens = 100000
max_tokens = 8192

# Same for the S4 tester: the catalog entry stays big; the scenario's
# [context] cap (6000) is what both tester gates must divide by.
[providers.fake.models.s4-tester]
max_context_tokens = 1000000
max_tokens = 8192

[providers.fake.models.s7-coder]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s7-tester]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s8-coder]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s8-tester]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s9-research]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s10-research]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s11-research]
max_context_tokens = 100000
max_tokens = 8192

# S12: ONE scripted model id serves BOTH the research and the coding role
# (the S2b precedent of alternating transcripts on one model — there the
# coder serves two different tasks). The transcripts never mix: each task
# carries its own, and the script keys the phase off the prompt/history.
[providers.fake.models.s12-agent]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s12-tester]
max_context_tokens = 100000
max_tokens = 8192

# S13: ONE scripted model id serves BOTH the research and the coding role
# (the S12 precedent): the research transcript greps the deprecated token
# and files the feature request with the site plan, the spawned feature's
# coding transcript alternates on the same id; the tester keeps its own id
# (pytest + verdict).
[providers.fake.models.s13-agent]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.s13-tester]
max_context_tokens = 100000
max_tokens = 8192

[[combo]]
name       = "{combo}"
coding     = "fake/{coder}"
tester     = "fake/{tester}"
compaction = "fake/fake-compaction"
research   = "fake/{research}"
{extra}"""

# Per-role max_context_tokens overrides appended to the generated combo —
# DEPRECATED source (§1.2): the working path is the scenario's [context]
# section. S4 keeps a COMBO override (50000) on purpose: the scenario's
# [context] tester = 6000 must WIN over it, so the e2e proves the
# scenario → combo priority on the real pipeline (a regression to
# combo-wins would resolve tester to 50000 and fail the assertions
# below).
COMBO_EXTRA_TOML = {
    "s4_compaction_tester": "tester_max_context_tokens = 50000",
}

COMBOS = {
    "s2a_bug_followup": ("s2a-coder", "s2a-tester"),
    "s2b_bug_report": ("s2b-coder", "s2b-tester"),
    "s5_clarification": ("s5-coder", "s5-tester"),
    # S3/S4: the compaction lives on the CODER side (S3) / the TESTER side
    # (S4); the inflated gateway usage (fake_gateway._usage_for) trips the
    # real gates of drcode (both on the scenario's [context] caps — 5000
    # for the S3 coding role, 6000 for the S4 tester role).
    "s3_compaction_coder": ("s3-coder", "fake-tester"),
    "s4_compaction_tester": ("s4-coder", "s4-tester"),
    "s7_fault_injection": ("s7-coder", "s7-tester"),
    # S8: the fix loop lives inside ONE task (coder → tester → same coder);
    # no compaction pressure is needed — the loop is context-independent.
    "s8_fix_loop": ("s8-coder", "s8-tester"),
    # S9: a kind=research brief — the coding/tester roles are assigned but
    # never called (research skips the tester, plan §7); the research role
    # serves the only task on its OWN scripted model.
    "s9_research_count": ("fake-coder", "fake-tester"),
    # S10: same shape — the research role serves the only task; the
    # coding/tester scripts stay idle for the whole run.
    "s10_research_facts": ("fake-coder", "fake-tester"),
    # S11: same shape — the route-table research lives entirely on the
    # research role's own scripted model.
    "s11_research_routes": ("fake-coder", "fake-tester"),
    # S12: the research and the coding role SHARE one scripted model id —
    # the research transcript reads the seed and files the bug report, the
    # spawned bug's coding transcript alternates on the same id (S2b
    # precedent); the tester keeps its own id (pytest + verdict).
    "s12_research_bug_report": ("s12-agent", "s12-tester"),
    # S13: same shared-id shape — the research transcript plans the
    # refactor into a create_feature_request, the spawned feature's
    # coding transcript alternates on the same id; the tester keeps its
    # own id (pytest + verdict).
    "s13_research_feature": ("s13-agent", "s13-tester"),
}

# The research model of each combo (defaults to the idle 4th-role model;
# S9 gives the research role its own scripted agent so the research
# transcript is distinguishable from the coder's in model_log.jsonl).
RESEARCH_MODELS = {
    "s9_research_count": "s9-research",
    "s10_research_facts": "s10-research",
    "s11_research_routes": "s11-research",
    # S12: the research role runs on the SAME scripted model id as the
    # coding role — the alternation under test.
    "s12_research_bug_report": "s12-agent",
    # S13: same shared-id shape — research and coding alternate on one id.
    "s13_research_feature": "s13-agent",
}


def _research_model(scenario_id: str) -> str:
    return RESEARCH_MODELS.get(scenario_id, "fake-research")


@pytest.fixture
def env_guard():
    saved = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(saved)


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
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
            MATRIX_TEMPLATE.format(
                port=port,
                combo=combo,
                coder=coder,
                tester=tester,
                research=_research_model(scenario_id),
                extra=COMBO_EXTRA_TOML.get(scenario_id, ""),
            ),
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
    # The optional 4th combo role traveled the whole pipeline: the
    # pre-flight resolved research into its OWN model (not the coding
    # fallback) and its context limit is on the record.
    assert report.resolved_roles.get("research") == "fake/fake-research"
    assert report.resolved_context_tokens.get("research") == 100000
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
    compaction block. The small context comes from the scenario's
    `[context]` section (§1.2) — the catalog entry of s3-coder stays big
    on purpose, so the run proves the scenario → catalog priority too."""
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

    # The harness recorded the effective per-role context limits (§1.2)
    # and WHERE each limit came from: the coding role runs on the
    # scenario's [context] cap (5000, catalog entry 100000 untouched).
    assert report.resolved_context_tokens["coding"] == 5000
    assert report.resolved_context_sources["coding"] == "scenario"
    assert report.resolved_context_sources["tester"] == "catalog"

    # §10: the report generation must not choke on compaction artifacts.
    from bench.report import generate_report

    generate_report(run_dir.parent)


async def test_s4_compaction_tester_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S4 (plan §7, stage 4): the tester's mid-round compaction — the
    round is rewritten in place (summary in tester_messages[-1]), the
    verdict is set, checks.py green. The small context reaches the TESTER
    role via the scenario's `[context]` cap (§1.2), which must WIN over
    the combo's per-role override (50000 — see COMBO_EXTRA_TOML): the
    mid-round gate divides by the tester model's resolved
    max_context_tokens (drcode ≥ 0.5.0), and the threshold-source
    classification (§1.2) must name 'tester' — a 'coding' source would be
    a regression."""
    report = await _run_scenario(tmp_path, monkeypatch, "s4_compaction_tester")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = report.tasks
    assert brief["status"] == "completed"
    assert brief["verification"] == "Verified successfully"
    assert brief["n_testing_rounds"] == 1

    # §1.2: the small limit landed on the tester ROLE via the scenario's
    # [context] cap — 6000, beating BOTH the combo's 50000 override and
    # the s4-tester catalog entry (1000000) — while coding keeps its
    # untouched catalog limit — the two roles must resolve DIFFERENT
    # contexts now that the resume path reads the tester config too
    # (upstream 5129872).
    assert report.resolved_context_tokens["coding"] == 100000
    assert report.resolved_context_tokens["tester"] == 6000
    assert report.resolved_context_sources["tester"] == "scenario"
    assert report.resolved_context_sources["coding"] == "catalog"

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
    # §1.2: the threshold-source block exists and names the tester model's
    # config (limits are equal here — classification is moot, but it must
    # not flag a regression).
    threshold = comp["tester_threshold"]
    assert threshold is not None
    assert threshold["source"] == "tester"
    assert threshold["classified"] is True
    assert metrics["tester_threshold_from_tester"] is True

    # §10: the report must render the run (incl. the threshold remark).
    from bench.report import generate_report

    generate_report(run_dir.parent)


async def test_s7_fault_injection_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S7 (plan §9, stage 6 of §12): the run goes through the local
    fault-injecting proxy (the generated catalog points at it, the proxy
    forwards to the scripted gateway) — two 429s and one connection drop
    are injected on the REAL HTTP layer, without touching drcode. The run
    must survive: network retries in the task events (within the
    NETWORK_RETRIES budget), the interrupted attempt resumed
    (unfinished-resume, the brief not re-sent), final success, and the
    proxy log in the artifacts + metrics (with the recorder latency
    cross-check, since both sources are enabled here)."""
    report = await _run_scenario(tmp_path, monkeypatch, "s7_fault_injection")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = report.tasks
    assert brief["status"] == "completed"
    assert brief["verification"] == "Verified successfully"

    # §9: the run went through the proxy and the fault script fired.
    assert report.proxy_base, "the run must report the proxy base URL"
    proxy_log = run_dir / "proxy_log.jsonl"
    assert proxy_log.is_file()
    proxy_entries = read_jsonl(proxy_log)
    faults = [e["fault"]["kind"] for e in proxy_entries if e.get("fault")]
    # The script: three 429s (the first two are absorbed by the openai
    # SDK's own max_retries=2 — the third reaches drcode) + two
    # connection drops mid-development (the SDK never retries an
    # interrupted stream).
    assert faults == ["http_429", "http_429", "http_429", "drop", "drop"], faults
    # The 429s never reached the gateway; the drops were answered with a
    # truncated 200 (a transport break, not an HTTP error status); the
    # rest were forwarded and answered 200.
    forwarded = [e for e in proxy_entries if not e.get("fault")]
    assert forwarded and all(e["status"] == 200 for e in forwarded)
    assert all(e["status"] in (429, 200) for e in proxy_entries if e.get("fault"))
    # Every proxied request carries a latency measurement (§9: exact
    # timings are the proxy's second job).
    assert all(isinstance(e["latency_ms"], int) for e in proxy_entries)

    # §7 S7: the retries are in the task events, the budget was honored,
    # and the interrupted attempt resumed.
    raw_task = json.loads(
        next((run_dir / "workspace" / ".drcode" / "tasks").glob("*.json")).read_text(
            encoding="utf-8"
        )
    )
    retry_events = [
        str(e.get("text", ""))
        for e in raw_task.get("events") or []
        if str(e.get("text", "")).startswith("Network error (")
    ]
    assert len(retry_events) == 3, retry_events
    # One ModelHTTPError (the surfaced 429) + two connection drops.
    assert any("ModelHTTPError" in e or "RateLimit" in e for e in retry_events)
    assert retry_events.count(next(e for e in retry_events if "ModelConnectionError" in e)) == 2
    # unfinished-resume: the brief was consumed exactly once — the retry
    # resumed the attempt instead of re-sending the prompt.
    prompts = [
        part["content"]
        for msg in raw_task.get("messages") or []
        for part in msg.get("parts") or []
        if isinstance(part, dict)
        and part.get("part_kind") == "user-prompt"
        and "bullet_list" in str(part.get("content"))
        and "Исправьте" in str(part.get("content"))
    ]
    assert len(prompts) == 1
    # The persisted task ended clean: the unfinished flag was cleared by
    # the resuming continuation turn.
    assert raw_task.get("unfinished") is False

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    # §10: the proxy is an aggregated latency/fault source in metrics.json.
    proxy_block = metrics["proxy"]
    assert proxy_block["faults"] == {"http_429": 3, "drop": 2}
    assert proxy_block["latency_ms_p50"] is not None
    # The stability totals see the same retries the checks asserted.
    assert metrics["totals"]["stability"]["network_retries"] == 3
    # Both latency sources were on: the cross-check must match pairs.
    latency_check = metrics["latency_cross_check"]
    assert latency_check is not None
    assert latency_check["matched"] >= 3
    assert metrics["model_log"] is not None

    # §10: the report generation must not choke on the proxy artifacts.
    from bench.report import generate_report

    generate_report(run_dir.parent)


async def test_s8_fix_loop_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S8 (upstream drcode 18b48f9): the tester fix loop — the coder's
    round-1 change breaks the dependent test_row BY DESIGN (the full seed
    suite is green before the change, unlike s2a), the tester attributes
    the failure to the task's own changes and stamps
    set_verification(success=False, retry_here=True); drcode requeues the
    task into development (fix_rounds=1 of max_dev_rounds=3), the tester's
    report reaches the same coder transcript as the next input, round 2
    repairs the regression and the tester stamps PASSED — with ZERO user
    interventions (the loop closes internally, no follow-ups)."""
    report = await _run_scenario(tmp_path, monkeypatch, "s8_fix_loop")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = report.tasks
    assert brief["status"] == "completed"
    assert brief["verification"] == "Verified successfully"
    assert brief["n_testing_rounds"] >= 2  # FAILED round + post-fix-loop round

    # The fix loop left its mark in the persisted task JSON: the requeue
    # event of requeue_failed_fix with fix_rounds=1 of the cap 3 (the
    # counter is incremented before the event is composed and the number
    # names the UPCOMING development round — the brief is round 1).
    raw_task = json.loads(
        next((run_dir / "workspace" / ".drcode" / "tasks").glob("*.json")).read_text(
            encoding="utf-8"
        )
    )
    events = [str(e.get("text", "")) for e in raw_task.get("events") or []]
    assert "testing failed — returned for another development round (round 2/3)" in events, events
    # Reset-on-success: the final PASSED verdict zeroed the counter.
    assert raw_task.get("fix_rounds") == 0
    # The report was consumed as ONE new prompt (no duplicates).
    prompts = [
        part["content"]
        for msg in raw_task.get("messages") or []
        for part in msg.get("parts") or []
        if isinstance(part, dict)
        and part.get("part_kind") == "user-prompt"
        and "test_row" in str(part.get("content"))
    ]
    assert len(prompts) == 1, prompts

    # §6: the contract of S8 is ZERO interventions — the simulator only
    # wrote its start record.
    records = read_jsonl(run_dir / "user_sim.jsonl")
    assert records, "the simulator must at least log its start"
    assert not [r for r in records if r["action"] != "start"]

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["totals"]["n_testing_rounds"] >= 2
    assert metrics["user_sim"]["interventions"] == 0
    assert not metrics["user_sim"]["failures"]


async def test_s9_research_count_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S9 (variant V1 research): a kind=research brief — the agent computes
    a metric from the seed CSV (the path is free; the scripted agent uses
    run_bash + python, a legitimate tool use), writes docs/report.md in the
    pinned format (one line exactly "total: <number>", parsed by the
    anchored regex in checks.py) and commits it via git_commit_docs.
    Research skips the tester entirely (plan §7): no verification label,
    zero testing rounds, zero user interventions; checks.py recomputes the
    reference from the seed CSV itself, so nothing is hardcoded twice."""
    report = await _run_scenario(tmp_path, monkeypatch, "s9_research_count")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = report.tasks
    assert brief["kind"] == "research"
    assert brief["status"] == "completed"
    # Research ends with mark_done: no tester, no verification label.
    assert brief["verification"] is None
    assert brief["n_testing_rounds"] == 0

    # The research role SERVED the task: pre-flight resolved it into its
    # OWN model (not the coding fallback), and the recorder log carries
    # the research traffic under the distinct model tag.
    assert report.resolved_roles.get("research") == "fake/s9-research"
    log_records = read_jsonl(run_dir / "model_log.jsonl")
    assert any("s9-research@" in str(r.get("role")) for r in log_records)
    assert not any("fake-coder@" in str(r.get("role")) for r in log_records)

    # The report is on disk in the pinned format and in the git history
    # (git_commit_docs committed the agent's own write_file edit).
    report_md = (run_dir / "workspace" / "docs" / "report.md").read_text(encoding="utf-8")
    match = re.search(r"^total: (\d+)$", report_md, re.MULTILINE)
    assert match, report_md
    # The number is recomputed from the seed here too — the same contract
    # checks.py enforces (no double-hardcoded reference).
    with (run_dir / "workspace" / "data" / "orders.csv").open(encoding="utf-8", newline="") as f:
        reference = sum(
            int(row["amount"]) for row in csv.DictReader(f) if row["status"] == "completed"
        )
    assert int(match.group(1)) == reference
    git_log = subprocess.run(
        ["git", "log", "--", "docs/report.md"],
        cwd=run_dir / "workspace",
        capture_output=True,
        text=True,
        check=False,
    )
    assert git_log.returncode == 0 and git_log.stdout.strip(), git_log.stderr

    # §6: the research loop closes without any user intervention.
    records = read_jsonl(run_dir / "user_sim.jsonl")
    assert records, "the simulator must at least log its start"
    assert not [r for r in records if r["action"] != "start"]

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["totals"]["n_testing_rounds"] == 0
    assert metrics["user_sim"]["interventions"] == 0
    assert not metrics["user_sim"]["failures"]


async def test_s10_research_facts_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S10 (variant V2 research): the agent finds the THREE planted seed
    facts by reading/grepping the code (orphan constant, a function name
    defined in two modules, the deprecated flag's usage sites) and
    documents them in docs/findings.md. The scripted research agent
    composes the findings from its OWN grep output — the identifiers
    checks.py needles on come from the seed through the tool results,
    not from the script. Research skips the tester entirely (plan §7):
    no verification label, zero testing rounds, zero user interventions."""
    report = await _run_scenario(tmp_path, monkeypatch, "s10_research_facts")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = report.tasks
    assert brief["kind"] == "research"
    assert brief["status"] == "completed"
    # Research ends with mark_done: no tester, no verification label.
    assert brief["verification"] is None
    assert brief["n_testing_rounds"] == 0

    # The research role SERVED the task on its OWN scripted model.
    assert report.resolved_roles.get("research") == "fake/s10-research"
    log_records = read_jsonl(run_dir / "model_log.jsonl")
    assert any("s10-research@" in str(r.get("role")) for r in log_records)
    assert not any("fake-coder@" in str(r.get("role")) for r in log_records)

    # findings.md on disk answers all three facts by code identifiers
    # (file path AND symbol name) — the same needles checks.py enforces;
    # three facts at once rule out "one lucky grep line".
    findings = (run_dir / "workspace" / "docs" / "findings.md").read_text(encoding="utf-8")
    lowered = findings.lower()
    for needle in (
        "parcel_volume_limit_l",
        "rates.py",
        "totals.py",
        "summary.py",
        "balance",
        "detailed_ledger",
        "render.py",
    ):
        assert needle in lowered, findings

    # The findings are in the git history (git_commit_docs committed the
    # agent's own write_file edit).
    git_log = subprocess.run(
        ["git", "log", "--", "docs/findings.md"],
        cwd=run_dir / "workspace",
        capture_output=True,
        text=True,
        check=False,
    )
    assert git_log.returncode == 0 and git_log.stdout.strip(), git_log.stderr

    # §6: the research loop closes without any user intervention.
    records = read_jsonl(run_dir / "user_sim.jsonl")
    assert records, "the simulator must at least log its start"
    assert not [r for r in records if r["action"] != "start"]

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["totals"]["n_testing_rounds"] == 0
    assert metrics["user_sim"]["interventions"] == 0
    assert not metrics["user_sim"]["failures"]


async def test_s11_research_routes_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S11 (variant V3 research): the agent extracts the route table of the
    seed mini-router src/api/ (each endpoint is a '@route("METHOD /path")'
    decorator directly above its 'def handle_*' handler) and documents it
    as a markdown table in docs/routes.md (method | path | handler, one
    row per route). The scripted research agent pairs the decorator/def
    lines out of its OWN grep output — the table checks.py validates comes
    from the seed through the tool results, not from the script. Markdown
    tables are the most fragile research output, so the e2e asserts the
    reference triples the same lenient way checks.py does (a line carrying
    method AND path AND handler, not a strict table grid). Research skips
    the tester entirely (plan §7): no verification label, zero testing
    rounds, zero user interventions."""
    report = await _run_scenario(tmp_path, monkeypatch, "s11_research_routes")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (brief,) = report.tasks
    assert brief["kind"] == "research"
    assert brief["status"] == "completed"
    # Research ends with mark_done: no tester, no verification label.
    assert brief["verification"] is None
    assert brief["n_testing_rounds"] == 0

    # The research role SERVED the task on its OWN scripted model.
    assert report.resolved_roles.get("research") == "fake/s11-research"
    log_records = read_jsonl(run_dir / "model_log.jsonl")
    assert any("s11-research@" in str(r.get("role")) for r in log_records)
    assert not any("fake-coder@" in str(r.get("role")) for r in log_records)

    # routes.md on disk answers EVERY reference route — the reference is
    # recomputed from the workspace seed by the same decorator parsing
    # checks.py enforces (no double-hardcoded reference); each triple must
    # be carried by a single line (lenient row parse, like checks.py).
    workspace = run_dir / "workspace"
    routes_md = (workspace / "docs" / "routes.md").read_text(encoding="utf-8")
    decorator_re = re.compile(r'@route\("([A-Z]+)\s+([^"]+)"\)\s*\ndef\s+(\w+)')
    reference = {
        triple
        for path in (workspace / "src" / "api").rglob("*.py")
        for triple in decorator_re.findall(path.read_text(encoding="utf-8"))
    }
    assert len(reference) == 5, reference
    lowered_lines = [line.lower() for line in routes_md.splitlines()]
    for method, route_path, handler in reference:
        assert any(
            method.lower() in line and route_path.lower() in line and handler.lower() in line
            for line in lowered_lines
        ), (routes_md, (method, route_path, handler))

    # The table is in the git history (git_commit_docs committed the
    # agent's own write_file edit).
    git_log = subprocess.run(
        ["git", "log", "--", "docs/routes.md"],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    assert git_log.returncode == 0 and git_log.stdout.strip(), git_log.stderr

    # §6: the research loop closes without any user intervention.
    records = read_jsonl(run_dir / "user_sim.jsonl")
    assert records, "the simulator must at least log its start"
    assert not [r for r in records if r["action"] != "start"]

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["totals"]["n_testing_rounds"] == 0
    assert metrics["user_sim"]["interventions"] == 0
    assert not metrics["user_sim"]["failures"]


async def test_s12_research_bug_report_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S12 (research variant V4): the research agent finds the LATENT defect
    by reading (the seed suite is GREEN — pytest cannot reveal the defect,
    unlike s2a) and files the bug report via create_bug_report under the
    brief's explicit authorization; the spawned kind=bug task
    (origin="system" via TaskManager.create) runs the FULL coding → testing
    pipeline and passes. ONE scripted model id alternates the research and
    the coding transcripts (the S2b precedent). Research skips the tester
    (plan §7): no verification label, zero testing rounds, zero user
    interventions; the default settle criterion holds the run until the
    spawned bug is developed AND tested (the queue must drain)."""
    report = await _run_scenario(tmp_path, monkeypatch, "s12_research_bug_report")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True

    # The research target: COMPLETED, no tester involvement.
    (brief,) = [t for t in report.tasks if t["kind"] == "research"]
    assert brief["status"] == "completed"
    assert brief["verification"] is None
    assert brief["n_testing_rounds"] == 0

    # The spawned bug: exactly one, COMPLETED and PASSED — the FULL pipeline.
    bugs = [t for t in report.tasks if t["kind"] == "bug"]
    assert len(bugs) == 1, "the research agent must have filed exactly one bug report"
    (bug,) = bugs
    assert bug["status"] == "completed"
    assert bug["verification"] == "Verified successfully"
    assert bug["n_testing_rounds"] >= 1

    # ONE model id served both roles: the research role resolved to the
    # same scripted model as the coding role.
    assert report.resolved_roles.get("coding") == "fake/s12-agent"
    assert report.resolved_roles.get("research") == "fake/s12-agent"
    log_records = read_jsonl(run_dir / "model_log.jsonl")
    assert any("s12-agent@" in str(r.get("role")) for r in log_records)
    assert any("s12-tester@" in str(r.get("role")) for r in log_records)

    # The persisted task JSON: the research → bug chain is mechanical.
    raw = [
        json.loads(f.read_text(encoding="utf-8"))
        for f in sorted((run_dir / "workspace" / ".drcode" / "tasks").glob("*.json"))
    ]
    (research_raw,) = [t for t in raw if t["kind"] == "research"]
    (bug_raw,) = [t for t in raw if t["kind"] == "bug"]

    # Exactly ONE create_bug_report call in the research transcript; the
    # description (composed by the script FROM the read_file output) cites
    # the code identifiers — file path AND function name.
    calls = [
        part
        for msg in research_raw.get("messages") or []
        for part in (msg.get("parts") or [])
        if isinstance(part, dict)
        and part.get("part_kind") == "tool-call"
        and part.get("tool_name") == "create_bug_report"
    ]
    assert len(calls) == 1
    args = json.loads(calls[0]["args"])
    assert "dispatch/pricing.py" in args["description"]
    assert "batches_needed" in args["description"]
    assert args["title"] == bug_raw["title"]

    # The report description became the bug task's first (and only) prompt.
    bug_prompts = [
        part["content"]
        for msg in bug_raw.get("messages") or []
        for part in (msg.get("parts") or [])
        if isinstance(part, dict)
        and part.get("part_kind") == "user-prompt"
        and isinstance(part.get("content"), str)
    ]
    assert len(bug_prompts) == 1
    assert bug_prompts[0].strip() == args["description"].strip()

    # The coder's fix landed in the seed module: the remainder case now
    # counts the incomplete batch, and the full suite is green on disk.
    pricing = (run_dir / "workspace" / "dispatch" / "pricing.py").read_text(encoding="utf-8")
    assert "-(-items // per_batch)" in pricing
    pytest_run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=run_dir / "workspace",
        capture_output=True,
        text=True,
        check=False,
    )
    assert pytest_run.returncode == 0, pytest_run.stdout + pytest_run.stderr

    # §6: no followups/clarifications — the loop closes without the user.
    records = read_jsonl(run_dir / "user_sim.jsonl")
    assert records, "the simulator must at least log its start"
    assert not [r for r in records if r["action"] != "start"]

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["totals"]["n_bug_tasks"] == 1
    assert metrics["totals"]["n_testing_rounds"] >= 1
    assert metrics["user_sim"]["interventions"] == 0
    assert not metrics["user_sim"]["failures"]


async def test_s13_research_feature_end_to_end(tmp_path: Path, monkeypatch, env_guard) -> None:
    """S13 (research variant V5, the heaviest one): the COMPOUND
    research → planning → coding → testing chain. The research agent
    composes the refactor PLAN into a create_feature_request whose
    description lists ALL change sites (the seed's canonical list is
    exactly 5 telemetry modules carrying the deprecated math.floor
    token); the spawned kind=feature task (origin="system" via
    TaskManager.create, the TAIL of the queue — unlike the S12 bug)
    runs the FULL coding → testing pipeline and passes. ONE scripted
    model id alternates the research and the coding transcripts (the
    S12 precedent). The default settle criterion holds the run until
    the spawned feature is developed AND tested (the queue must
    drain); the plan's completeness and the actual implementation are
    asserted mechanically from the task JSON and the workspace."""
    report = await _run_scenario(tmp_path, monkeypatch, "s13_research_feature")
    run_dir = Path(report.run_dir)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True

    # The research target: COMPLETED, no tester involvement.
    (brief,) = [t for t in report.tasks if t["kind"] == "research"]
    assert brief["status"] == "completed"
    assert brief["verification"] is None
    assert brief["n_testing_rounds"] == 0

    # The spawned feature: exactly one, COMPLETED and PASSED — the FULL
    # pipeline, after the research task activated it from the queue tail.
    features = [t for t in report.tasks if t["kind"] == "feature"]
    assert len(features) == 1, "the research agent must have filed exactly one feature request"
    (feature,) = features
    assert feature["status"] == "completed"
    assert feature["verification"] == "Verified successfully"
    assert feature["n_testing_rounds"] >= 1
    assert brief["activated_at"] < feature["activated_at"]

    # ONE model id served both roles: the research role resolved to the
    # same scripted model as the coding role.
    assert report.resolved_roles.get("coding") == "fake/s13-agent"
    assert report.resolved_roles.get("research") == "fake/s13-agent"
    log_records = read_jsonl(run_dir / "model_log.jsonl")
    assert any("s13-agent@" in str(r.get("role")) for r in log_records)
    assert any("s13-tester@" in str(r.get("role")) for r in log_records)

    # The canonical change-site list of the seed (5 telemetry modules).
    seed = REPO / "scenarios" / "s13_research_feature" / "seed"
    sites = sorted(
        p.relative_to(seed).as_posix()
        for p in seed.rglob("*.py")
        if "math.floor" in p.read_text(encoding="utf-8")
    )
    assert len(sites) == 5

    # The persisted task JSON: the research → feature chain is mechanical.
    raw = [
        json.loads(f.read_text(encoding="utf-8"))
        for f in sorted((run_dir / "workspace" / ".drcode" / "tasks").glob("*.json"))
    ]
    (research_raw,) = [t for t in raw if t["kind"] == "research"]
    (feature_raw,) = [t for t in raw if t["kind"] == "feature"]

    # Exactly ONE create_feature_request call in the research transcript;
    # the description (composed by the script FROM the grep output) lists
    # EVERY canonical path — the compound planning step under test.
    calls = [
        part
        for msg in research_raw.get("messages") or []
        for part in (msg.get("parts") or [])
        if isinstance(part, dict)
        and part.get("part_kind") == "tool-call"
        and part.get("tool_name") == "create_feature_request"
    ]
    assert len(calls) == 1
    args = json.loads(calls[0]["args"])
    for site in sites:
        assert site in args["description"].lower()
    assert args["title"] == feature_raw["title"]

    # The request description became the feature task's first prompt.
    feature_prompts = [
        part["content"]
        for msg in feature_raw.get("messages") or []
        for part in (msg.get("parts") or [])
        if isinstance(part, dict)
        and part.get("part_kind") == "user-prompt"
        and isinstance(part.get("content"), str)
    ]
    assert feature_prompts[0].strip() == args["description"].strip()

    # The compound chain closed on disk: the deprecated token is gone
    # from every listed site, and the full suite is green in the workspace.
    for site in sites:
        assert "math.floor" not in (run_dir / "workspace" / site).read_text(encoding="utf-8")
    pytest_run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=run_dir / "workspace",
        capture_output=True,
        text=True,
        check=False,
    )
    assert pytest_run.returncode == 0, pytest_run.stdout + pytest_run.stderr

    # §6: no followups/clarifications — the loop closes without the user.
    records = read_jsonl(run_dir / "user_sim.jsonl")
    assert records, "the simulator must at least log its start"
    assert not [r for r in records if r["action"] != "start"]

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["totals"]["n_testing_rounds"] >= 1
    assert metrics["user_sim"]["interventions"] == 0
    assert not metrics["user_sim"]["failures"]


async def test_s1_through_use_proxy_flag(tmp_path: Path, monkeypatch, env_guard) -> None:
    """§9: `--use-proxy` forces the proxy for a scenario WITHOUT a
    [proxy] section — a fault-free recording proxy (the §5-recorder
    alternative): the run goes through it untouched, the log lands in
    the artifacts and the metrics carry both latency sources with the
    cross-check."""
    from tests.fake_gateway import start

    server = await start(0)
    port = server.sockets[0].getsockname()[1]
    try:
        combo = "s1-proxy-roles"
        matrix_path = tmp_path / "matrix.toml"
        matrix_path.write_text(
            MATRIX_TEMPLATE.format(
                port=port,
                combo=combo,
                coder="fake-coder",
                tester="fake-tester",
                research=_research_model("s1_happy"),
                extra="",
            ),
            encoding="utf-8",
        )

        import drcode.config as dconfig

        run_dir = tmp_path / "runs" / "s1_happy"
        config_home = run_dir / "config-home" / "drcode"
        config_home.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(dconfig, "_USER_CONFIG_DIR", config_home)
        monkeypatch.setattr(dconfig, "USER_CONFIG_FILE", config_home / "drcode.json")

        from bench.run_one import run_benchmark
        from bench.scenario import load_scenario_by_id

        scenario = load_scenario_by_id(REPO / "scenarios", "s1_happy")
        assert scenario.proxy is None  # no [proxy] section — forced by the flag
        scenario = dataclasses.replace(scenario, timeout_min=3)
        report = await run_benchmark(scenario, combo, run_dir, matrix_path, use_proxy=True)
    finally:
        server.close()
        await server.wait_closed()

    assert report.ok, report.reason
    assert report.proxy_base
    proxy_entries = read_jsonl(run_dir / "proxy_log.jsonl")
    assert proxy_entries
    assert not any(e.get("fault") for e in proxy_entries)  # fault-free mode
    # The catalog pointed at the proxy, the gateway saw the traffic.
    assert all(e["status"] == 200 for e in proxy_entries)

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["proxy"]["requests"] == len(proxy_entries)
    assert metrics["proxy"]["faults_injected"] == 0
    # Both latency sources on → the cross-check matched the pairs.
    assert metrics["latency_cross_check"]["matched"] >= 1
