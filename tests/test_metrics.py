"""Unit tests of bench.metrics on synthetic task JSON fixtures (§10) —
no real runs, no models, no drcode app: the fixtures mirror the structure
drcode persists (`<workspace>/.drcode/tasks/<id>.json`, see drcode's
storage.py/models.py and the transcript serialization of pydantic-ai).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from bench.metrics import (
    COMPACTION_SUMMARY_PREFIX,
    analyze_task,
    classify_event,
    extract_run_metrics,
    find_tasks_dir,
    parse_ts,
    seconds_between,
)


def request_msg(content: str, at: str) -> dict:
    """Serialized ModelRequest with a user prompt (pydantic-ai 2.x shape)."""
    return {
        "parts": [{"content": content, "part_kind": "user-prompt", "timestamp": at}],
        "timestamp": at,
        "kind": "request",
    }


def response_msg(at: str, *, inp: int = 0, out: int = 0, cache: int = 0) -> dict:
    """Serialized ModelResponse with usage."""
    return {
        "parts": [{"content": "done", "part_kind": "text"}],
        "timestamp": at,
        "kind": "response",
        "usage": {
            "input_tokens": inp,
            "output_tokens": out,
            "cache_read_tokens": cache,
            "cache_write_tokens": 0,
        },
    }


def summary_msg(summary: str, at: str) -> dict:
    """The synthetic compaction-summary request."""
    return request_msg(f"{COMPACTION_SUMMARY_PREFIX}\n\n{summary}", at)


def make_task() -> dict:
    """A synthetic feature task with the full compaction + stability story:
    one coder compaction (turn boundary), a tester compaction, a network
    retry, a tester failure, two testing rounds."""
    return {
        "id": "a1b2c3d4",
        "title": "Make the test green",
        "kind": "feature",
        "status": "completed",
        "verification": "Verified successfully",
        "created_at": "2025-06-01T10:00:00+00:00",
        "updated_at": "2025-06-01T10:05:00+00:00",
        "activated_at": "2025-06-01T10:00:10+00:00",
        "completed_at": "2025-06-01T10:05:00+00:00",
        "unfinished": False,
        "clarification": None,
        "events": [
            {
                "at": "2025-06-01T10:01:05+00:00",
                "kind": "system",
                "text": "Context fill 75% — pausing the agent and compacting history…",
            },
            {
                "at": "2025-06-01T10:01:10+00:00",
                "kind": "system",
                "text": "Context compacted: history summarized, original task "
                "prompt(s) kept verbatim.",
            },
            {
                "at": "2025-06-01T10:02:30+00:00",
                "kind": "system",
                "text": "Network error (APIConnectionError): retry 1/4 in 2 s",
            },
            {
                "at": "2025-06-01T10:03:30+00:00",
                "kind": "system",
                "text": "Context fill 80% — compacting the testing round…",
            },
            {
                "at": "2025-06-01T10:03:35+00:00",
                "kind": "system",
                "text": "Context compacted: testing round summarized, original "
                "prompt kept verbatim.",
            },
            {
                "at": "2025-06-01T10:04:00+00:00",
                "kind": "system",
                "text": "tester failed: UnexpectedModelBehavior: boom",
            },
        ],
        "messages": [
            request_msg("Fix the shout() function.", "2025-06-01T10:00:12+00:00"),
            response_msg("2025-06-01T10:00:20+00:00", inp=900, out=100),
            request_msg("Also add error handling.", "2025-06-01T10:00:50+00:00"),
            response_msg("2025-06-01T10:01:00+00:00", inp=1400, out=150, cache=50),
            # Compaction: history replaced by the summary (75% fill).
            summary_msg("The task is to fix shout().", "2025-06-01T10:01:10+00:00"),
            response_msg("2025-06-01T10:01:30+00:00", inp=250, out=60),
            response_msg("2025-06-01T10:02:00+00:00", inp=300, out=70),
        ],
        "tester_messages": [
            [
                request_msg("Test the task.", "2025-06-01T10:02:20+00:00"),
                response_msg("2025-06-01T10:02:25+00:00", inp=200, out=30),
            ],
            [
                request_msg("Re-test after the fix.", "2025-06-01T10:03:20+00:00"),
                response_msg("2025-06-01T10:03:25+00:00", inp=210, out=25),
                # Tester compaction rewrote the round in place.
                summary_msg("Re-testing in progress.", "2025-06-01T10:03:35+00:00"),
                response_msg("2025-06-01T10:03:45+00:00", inp=120, out=20),
            ],
        ],
        "pending_input": [],
        "queue_head": False,
        "queue_seq": 0,
        "github_issue": None,
    }


def test_prefix_matches_drcode_source() -> None:
    """The hardcoded prefix must be the one drcode actually writes."""
    from drcode.transcript import COMPACTION_SUMMARY_PREFIX as DRCODE_PREFIX

    assert COMPACTION_SUMMARY_PREFIX == DRCODE_PREFIX


def test_parse_ts_handles_z_and_naive() -> None:
    assert parse_ts("2025-06-01T10:00:00Z").tzinfo is not None
    assert parse_ts("2025-06-01T10:00:00").tzinfo is not None  # assumed UTC
    assert parse_ts(None) is None
    assert parse_ts("garbage") is None


def test_seconds_between_rejects_inverted() -> None:
    a = parse_ts("2025-06-01T10:00:00Z")
    b = parse_ts("2025-06-01T10:01:00Z")
    assert seconds_between(a, b) == 60.0
    assert seconds_between(b, a) is None
    assert seconds_between(None, b) is None


def test_classify_event_all_pipeline_variants() -> None:
    cases = [
        (
            "Context fill 64% — pausing the agent and compacting history…",
            "start",
            "coder",
            64,
        ),
        (
            "Context fill 71% — pausing the run to compact history…",
            "start",
            "coder",
            71,
        ),
        ("Context fill 77% — compacting the testing round…", "start", "tester", 77),
        (
            "Context fill 88% — pausing the tester round to compact history…",
            "start",
            "tester",
            88,
        ),
        (
            "Context compacted: history summarized, original task prompt(s) "
            "kept verbatim.",
            "succeeded",
            "coder",
            None,
        ),
        (
            "Context compacted: testing round summarized, original prompt kept "
            "verbatim.",
            "succeeded",
            "tester",
            None,
        ),
        ("compaction failed: TimeoutError: boom", "failed", "unknown", None),
    ]
    for text, kind, phase, pct in cases:
        ev = classify_event(text)
        assert ev is not None, text
        assert ev.kind == kind, text
        assert ev.phase == phase, text
        assert ev.trigger_pct == pct, text
    # Unrelated events are not compaction events.
    assert classify_event("Network error (TimeoutError): retry 1/4 in 2 s") is None
    assert classify_event("tester failed: X: y") is None


def test_analyze_task_phases() -> None:
    m = analyze_task(make_task())
    ph = m["phases"]
    assert ph["created_at"] == "2025-06-01T10:00:00+00:00"
    assert ph["activated_at"] == "2025-06-01T10:00:10+00:00"
    assert ph["completed_at"] == "2025-06-01T10:05:00+00:00"
    # dev_end = last message of the coder transcript (10:02:00),
    # testing_end = last message of the last tester round (10:03:45).
    assert ph["dev_end"] == "2025-06-01T10:02:00+00:00"
    assert ph["testing_end"] == "2025-06-01T10:03:45+00:00"
    assert ph["queue_wait_s"] == 10.0
    assert ph["dev_s"] == 110.0
    assert ph["testing_s"] == 105.0
    assert ph["total_s"] == 300.0


def test_analyze_task_compaction_counts() -> None:
    m = analyze_task(make_task())
    comp = m["compactions"]
    assert comp["n_started"] == 2  # coder + tester
    assert comp["n_succeeded"] == 2
    assert comp["n_failed"] == 0
    assert comp["by_phase"] == {"coder": 1, "tester": 1}  # starts per phase
    kinds = [(e["kind"], e["phase"]) for e in comp["events"]]
    assert ("start", "coder") in kinds
    assert ("succeeded", "coder") in kinds
    assert ("start", "tester") in kinds
    assert ("succeeded", "tester") in kinds


def test_analyze_task_compaction_savings() -> None:
    m = analyze_task(make_task())
    savings = m["compaction_savings"]
    assert len(savings) == 1  # tester rounds are counted per task only via
    # messages; the coder summary is the one inside `messages`
    s = savings[0]
    assert s["at"] == "2025-06-01T10:01:10+00:00"
    assert s["summary_chars"] == len("The task is to fix shout().")
    assert s["prompts_kept"] == 2  # both original prompts stay verbatim
    # pre = last response before the summary (1400+150), post = first after (250+60)
    assert s["pre_tokens_est"] == 1550
    assert s["post_tokens_est"] == 310
    assert s["saved_tokens_est"] == 1240
    assert s["trigger_pct"] == 75


def test_analyze_task_usage() -> None:
    m = analyze_task(make_task())
    usage = m["usage"]
    assert usage["requests"] == 4
    assert usage["input_tokens"] == 900 + 1400 + 250 + 300
    assert usage["output_tokens"] == 100 + 150 + 60 + 70
    assert usage["cache_read_tokens"] == 50
    assert m["transcript"]["n_user_prompts"] == 2
    assert m["transcript"]["context_tokens_final"] == 370


def test_analyze_task_testing_rounds() -> None:
    m = analyze_task(make_task())
    testing = m["testing"]
    assert testing["n_rounds"] == 2
    assert [r["n_messages"] for r in testing["rounds"]] == [2, 4]
    assert [r["has_summary"] for r in testing["rounds"]] == [False, True]
    assert testing["rounds"][0]["usage"]["requests"] == 1


def test_analyze_task_stability() -> None:
    m = analyze_task(make_task())
    st = m["stability"]
    assert st["compaction_failed"] == 0
    assert st["tester_failed"] == 1
    assert st["network_retries"] == 1
    assert st["unfinished"] is False
    assert st["pending_clarification"] is False
    events = m["stability_events"]
    assert events["network_retries"][0]["who"] == "coder"
    assert events["network_retries"][0]["attempt"] == 1
    assert events["tester_failed"], "the tester failure must be captured"


def test_analyze_task_unfinished_and_clarification() -> None:
    task = make_task()
    task["unfinished"] = True
    task["clarification"] = {"question": "Which branch?", "options": []}
    task["verification"] = None
    task["status"] = "clarification"
    m = analyze_task(task)
    assert m["stability"]["unfinished"] is True
    assert m["stability"]["pending_clarification"] is True


def test_analyze_task_compaction_failed_event() -> None:
    task = make_task()
    task["events"].append(
        {
            "at": "2025-06-01T10:01:12+00:00",
            "kind": "system",
            "text": "compaction failed: APITimeoutError: summarizer timed out",
        }
    )
    m = analyze_task(task)
    assert m["compactions"]["n_failed"] == 1
    assert m["stability"]["compaction_failed"] == 1
    assert m["stability_events"]["compaction_failed"][0]["text"].startswith(
        "compaction failed:"
    )


def test_bug_round_trips_captured() -> None:
    task = make_task()
    task["kind"] = "bug"
    task["activated_at"] = "2025-06-01T10:06:00+00:00"
    m = analyze_task(task)
    assert m["kind"] == "bug"


# --- run-level extraction --------------------------------------------------


def _write_run(run_dir: Path, tasks: list[dict], result: dict) -> Path:
    tasks_dir = run_dir / "workspace" / ".drcode" / "tasks"
    tasks_dir.mkdir(parents=True)
    for t in tasks:
        (tasks_dir / f"{t['id']}.json").write_text(
            json.dumps(t), encoding="utf-8"
        )
    (run_dir / "result.json").write_text(json.dumps(result), encoding="utf-8")
    return run_dir


RESULT = {
    "scenario": "s1_happy",
    "combo": "test-combo",
    "ok": True,
    "reason": "",
    "timed_out": False,
    "checks_ok": True,
    "settle_elapsed_s": 321.0,
    "started_at": "2025-06-01T10:00:00",
    "finished_at": "2025-06-01T10:05:30",
    "resolved_roles": {"coding": "p/m", "tester": "p/m", "compaction": "p/m"},
}


def test_find_tasks_dir_prefers_workspace(tmp_path: Path) -> None:
    assert find_tasks_dir(tmp_path) is None
    live = _write_run(tmp_path / "run-live", [make_task()], RESULT)
    assert find_tasks_dir(live) == live / "workspace" / ".drcode" / "tasks"
    # A failed run: only the diagnostics snapshot exists.
    diag = tmp_path / "run-diag" / "diagnostics" / "drcode-state" / "tasks"
    diag.mkdir(parents=True)
    (diag / "t.json").write_text(json.dumps(make_task()), encoding="utf-8")
    assert find_tasks_dir(tmp_path / "run-diag") == diag


def test_extract_run_metrics_end_to_end(tmp_path: Path) -> None:
    run_dir = _write_run(tmp_path / "r1", [make_task()], RESULT)
    metrics = extract_run_metrics(run_dir)

    assert (run_dir / "metrics.json").is_file()
    assert metrics["schema"] == "metrics/v1"
    assert metrics["run_id"] == "r1"
    assert metrics["scenario"] == "s1_happy"
    assert metrics["combo"] == "test-combo"
    assert metrics["verdict"] == "green"  # ok + checks + PASSED verification
    assert metrics["wall_time_s"]["settle"] == 321.0
    assert metrics["wall_time_s"]["run"] == 330.0

    totals = metrics["totals"]
    assert totals["n_tasks"] == 1
    assert totals["n_testing_rounds"] == 2
    assert totals["n_compactions"] == 2
    assert totals["usage"]["requests"] == 7  # 4 coder + 3 tester responses
    assert totals["stability"]["tester_failed"] == 1

    # metrics.json round-trips to the same structure.
    restored = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert restored == metrics


def test_extract_run_metrics_failed_run_verdict(tmp_path: Path) -> None:
    result = dict(RESULT, ok=False, checks_ok=False, reason="timeout")
    run_dir = _write_run(tmp_path / "r2", [make_task()], result)
    metrics = extract_run_metrics(run_dir)
    assert metrics["verdict"] == "failed"


def test_extract_run_metrics_no_tasks_dir(tmp_path: Path) -> None:
    run_dir = tmp_path / "empty"
    run_dir.mkdir()
    (run_dir / "result.json").write_text(json.dumps(RESULT), encoding="utf-8")
    metrics = extract_run_metrics(run_dir, write=False)
    assert metrics["totals"]["n_tasks"] == 0
    assert metrics["verdict"] == "green"  # harness verdict, no tasks parsed
    with pytest.raises(Exception):
        extract_run_metrics(tmp_path / "missing")


def test_extract_run_metrics_corrupt_task_skipped(tmp_path: Path) -> None:
    run_dir = _write_run(tmp_path / "r3", [make_task()], RESULT)
    tasks_dir = run_dir / "workspace" / ".drcode" / "tasks"
    (tasks_dir / "broken.json").write_text("{not json", encoding="utf-8")
    (tasks_dir / "old.json.bak").write_text("{}", encoding="utf-8")
    metrics = extract_run_metrics(run_dir)
    assert metrics["totals"]["n_tasks"] == 1


def test_extract_run_metrics_model_log(tmp_path: Path) -> None:
    run_dir = _write_run(tmp_path / "r4", [make_task()], RESULT)
    (run_dir / "model_log.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "role": "coding",
                        "latency_ms": 1200,
                        "usage": {"input_tokens": 100, "output_tokens": 10},
                    }
                ),
                json.dumps(
                    {
                        "role": "compaction",
                        "latency_ms": 800,
                        "usage": {"input_tokens": 50, "output_tokens": 5},
                    }
                ),
                "not json",
            ]
        ),
        encoding="utf-8",
    )
    metrics = extract_run_metrics(run_dir)
    log = metrics["model_log"]
    assert log is not None
    assert log["per_role"]["coding"]["requests"] == 1
    assert log["per_role"]["coding"]["latency_ms_total"] == 1200
    assert log["per_role"]["compaction"]["input_tokens"] == 50
