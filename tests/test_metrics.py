"""Unit tests of bench.metrics on synthetic task JSON fixtures (§10) —
no real runs, no models, no drcode app: the fixtures mirror the structure
drcode persists (`<workspace>/.drcode/tasks/<id>.json`, see drcode's
storage.py/models.py and the transcript serialization of pydantic-ai).
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from bench.metrics import (
    COMPACTION_SUMMARY_PREFIX,
    MetricsError,
    analyze_proxy,
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


def test_analyze_proxy_watchdog_aggregate() -> None:
    """§9 stall watchdog: abort events from proxy_log.jsonl aggregate
    into metrics["proxy"]["watchdog"]; a log without watchdog events
    yields None there (clean run)."""
    entries = [
        {  # aborted once, retry SAVED the request (attempts 2, saved)
            "model": "m",
            "status": 200,
            "latency_ms": 3100,
            "watchdog": {
                "stall_timeout_s": 0.3,
                "retries": 1,
                "attempts": 2,
                "saved": True,
                "events": [{"attempt": 1, "phase": "headers", "stalled_s": 0.3}],
            },
        },
        {  # retry budget exhausted → 502
            "model": "m",
            "status": 502,
            "error": "stall watchdog gave up",
            "watchdog": {
                "stall_timeout_s": 0.3,
                "retries": 1,
                "attempts": 2,
                "saved": False,
                "events": [
                    {"attempt": 1, "phase": "headers", "stalled_s": 0.3},
                    {"attempt": 2, "phase": "headers", "stalled_s": 0.3},
                ],
            },
        },
        {"model": "m", "status": 200, "latency_ms": 500},
    ]
    result = analyze_proxy(entries)
    assert result is not None
    wd = result["watchdog"]
    assert wd is not None
    assert wd["triggers"] == 3
    assert wd["retries"] == 2
    assert wd["saved"] == 1
    assert wd["exhausted"] == 1
    assert wd["abort_phases"] == {"headers": 3}

    clean = analyze_proxy([{"model": "m", "status": 200, "latency_ms": 100}])
    assert clean is not None
    assert clean["watchdog"] is None


def test_prefix_matches_drcode_source() -> None:
    """The hardcoded prefix must be the one drcode actually writes."""
    from drcode.transcript import COMPACTION_SUMMARY_PREFIX as DRCODE_PREFIX

    assert COMPACTION_SUMMARY_PREFIX == DRCODE_PREFIX


def test_parse_ts_handles_z_and_naive() -> None:
    ts_z = parse_ts("2025-06-01T10:00:00Z")
    ts_naive = parse_ts("2025-06-01T10:00:00")
    assert ts_z is not None and ts_z.tzinfo is not None
    assert ts_naive is not None and ts_naive.tzinfo is not None  # assumed UTC
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
            "Context compacted: history summarized, original task prompt(s) kept verbatim.",
            "succeeded",
            "coder",
            None,
        ),
        (
            "Context compacted: testing round summarized, original prompt kept verbatim.",
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
    assert m["stability_events"]["compaction_failed"][0]["text"].startswith("compaction failed:")


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
        (tasks_dir / f"{t['id']}.json").write_text(json.dumps(t), encoding="utf-8")
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
    with pytest.raises(MetricsError):
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


# -- tester compaction threshold source (§1.2/§13, stage 4 / S4) -----------------

from bench.metrics import (  # noqa: E402
    analyze_gate,
    analyze_tester_threshold,
    is_summary_message,
    read_context_limits,
    user_prompt_content,
    user_prompt_contents,
)

T0 = "2024-10-27T05:33:20+00:00"  # epoch 1730000000
T1 = "2024-10-27T05:33:30+00:00"  # +10 s


def _tester_task(events: list[dict], rounds: list[list[dict]]) -> dict:
    return {
        "id": "t1",
        "title": "task",
        "kind": "bug",
        "events": events,
        "tester_messages": rounds,
        "messages": [],
    }


def test_merged_summary_request_is_detected() -> None:
    """After a compaction + continuation turn the persisted request carries
    BOTH the original prompt and the summary as separate user-prompt parts
    (observed on-disk shape) — summary detection must scan all parts."""
    msg = {
        "kind": "request",
        "timestamp": T0,
        "parts": [
            {"part_kind": "user-prompt", "content": "original brief"},
            {"part_kind": "user-prompt", "content": "[context summary]\n\nsummary body"},
        ],
    }
    assert is_summary_message(msg)
    assert user_prompt_contents(msg) == [
        "original brief",
        "[context summary]\n\nsummary body",
    ]
    # drcode's own detector looks only at the FIRST part — the benchmark
    # deliberately diverges (documented in user_prompt_contents).
    assert not (user_prompt_content(msg) or "").startswith(COMPACTION_SUMMARY_PREFIX)


def test_analyze_task_counts_summaries_in_merged_requests() -> None:
    task = {
        "id": "t",
        "title": "task",
        "kind": "feature",
        "events": [],
        "messages": [
            {
                "kind": "request",
                "timestamp": T0,
                "parts": [
                    {"part_kind": "user-prompt", "content": "brief"},
                    {"part_kind": "user-prompt", "content": "[context summary]\n\ns"},
                ],
            },
            response_msg(T1, inp=100, out=10),
        ],
        "tester_messages": [],
    }
    result = analyze_task(task)
    assert result["compactions"]["n_summaries_in_transcript"] == 1
    assert result["compactions"]["repeat_compaction"] is False
    assert result["transcript"]["n_user_prompts"] == 1  # the brief only


def test_analyze_task_repeat_compaction_flagged() -> None:
    """Two summaries in one transcript = the summary did not stick (§10:
    degradation after summary) — the metrics must flag it."""
    task = {
        "id": "t",
        "title": "task",
        "kind": "feature",
        "events": [],
        "messages": [
            request_msg("brief", T0),
            request_msg("[context summary]\n\ns1", T0),
            response_msg(T1, inp=100, out=10),
            request_msg("[context summary]\n\ns2", T1),
            response_msg(T1, inp=100, out=10),
        ],
        "tester_messages": [],
    }
    result = analyze_task(task)
    assert result["compactions"]["n_summaries_in_transcript"] == 2
    assert result["compactions"]["repeat_compaction"] is True


def test_analyze_task_mid_run_vs_turn_boundary() -> None:
    task = {
        "id": "t",
        "title": "task",
        "kind": "feature",
        "events": [
            {"at": T0, "text": "Context fill 85% — pausing the run to compact history…"},
        ],
        "messages": [],
        "tester_messages": [],
    }
    comp = analyze_task(task)["compactions"]
    assert comp["mid_run_pause"] is True
    assert comp["turn_boundary_pause"] is False


def test_tester_threshold_moot_when_limits_equal() -> None:
    """Equal coding/tester limits: no regression is possible — the
    classification must say 'tester' (the expected source), not
    'coding'/'unknown'."""
    task = _tester_task(
        [{"at": T0, "text": "Context fill 87% — pausing the tester round to compact history…"}],
        [
            [
                request_msg("verify", T0),
                request_msg("[context summary]\n\ns", T0),
                response_msg(T1, inp=100, out=10),
            ]
        ],
    )
    result = analyze_tester_threshold(task, {"coding": 100000, "tester": 100000})
    assert result is not None
    assert result["source"] == "tester"
    assert result["classified"] is True


def test_tester_threshold_classifies_tester_from_recorder() -> None:
    """Distinct limits: the pre-compaction tokens come from the recorder
    log (the mid-round compaction replaced the round in place — the
    pre-compaction responses are gone); the implied limit must land on the
    TESTER value (drcode ≥ 0.5.0: per-role gate, §1.2)."""
    task = _tester_task(
        [{"at": T1, "text": "Context fill 87% — compacting the testing round…"}],
        [
            [
                request_msg("verify", T0),
                request_msg("[context summary]\n\ns", T1),
                response_msg(T1, inp=100, out=10),
            ]
        ],
    )
    entries = [
        {
            "role": "tester-model@http://g/v1",
            "ts": 1730007200.0,  # T0 — inside the window before the event
            "usage": {"input_tokens": 87000, "output_tokens": 10},
        },
        {
            "role": "other@x",
            "ts": 1730000000.0,
            "usage": {"input_tokens": 999999, "output_tokens": 10},
        },
    ]
    result = analyze_tester_threshold(
        task,
        {"coding": 500000, "tester": 100000},
        log_entries=entries,
        tester_tag="tester-model@http://g/v1",
    )
    assert result is not None
    assert result["observations"][0]["pre_tokens_est"] == 87000
    assert result["observations"][0]["implied_max_context_tokens"] == 100000
    assert result["source"] == "tester"
    assert result["classified"] is True


def test_tester_threshold_flags_coding_source_as_regression() -> None:
    """The regression case the metrics exist to catch: the implied limit
    matches the CODING model's config, not the tester's own (the pre-0.5.0
    behavior, §1.2)."""
    task = _tester_task(
        [{"at": T1, "text": "Context fill 17% — compacting the testing round…"}],
        [
            [
                request_msg("verify", T0),
                request_msg("[context summary]\n\ns", T1),
                response_msg(T1, inp=100, out=10),
            ]
        ],
    )
    entries = [
        {
            "role": "tester-model@http://g/v1",
            "ts": 1730007200.0,
            "usage": {"input_tokens": 85000, "output_tokens": 10},
        },
    ]
    result = analyze_tester_threshold(
        task,
        {"coding": 500000, "tester": 100000},
        log_entries=entries,
        tester_tag="tester-model@http://g/v1",
    )
    assert result is not None
    assert result["observations"][0]["implied_max_context_tokens"] == 500000
    assert result["source"] == "coding"


def test_tester_threshold_none_without_tester_compaction() -> None:
    task = _tester_task([], [[request_msg("verify", T0)]])
    assert analyze_tester_threshold(task, {"coding": 100000, "tester": 100000}) is None


def test_read_context_limits_prefers_result_json(tmp_path: Path) -> None:
    (tmp_path / "result.json").write_text(
        json.dumps({"resolved_context_tokens": {"coding": 3000, "tester": 131072}}),
        encoding="utf-8",
    )
    assert read_context_limits(tmp_path) == {"coding": 3000, "tester": 131072}


def test_read_context_limits_reconstructed_from_configs(tmp_path: Path) -> None:
    """Fallback: the generated configs are parsed the way providers.resolve
    reads them (project `models` ref → catalog entry; drcode ≥ 0.5 json
    layers carry no provider fields, so refs→catalog is the only path)."""
    state = tmp_path / "workspace" / ".drcode"
    state.mkdir(parents=True)
    catalog_dir = tmp_path / "config-home" / "drcode"
    catalog_dir.mkdir(parents=True)
    (state / "drcode.json").write_text(
        json.dumps(
            {"models": {"coding": "p/small", "tester": "p/big"}},
        ),
        encoding="utf-8",
    )
    (catalog_dir / "models.json").write_text(
        json.dumps(
            {
                "providers": [
                    {
                        "name": "p",
                        "base_url": "http://g/v1",
                        "models": [
                            {"id": "small", "max_context_tokens": 3000},
                            {"id": "big", "max_context_tokens": 131072},
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    assert read_context_limits(tmp_path) == {"coding": 3000, "tester": 131072}


def test_extract_run_metrics_carries_threshold_verdict(tmp_path: Path) -> None:
    """The run-level flag exists in metrics.json and is False on the
    regression shape (the threshold computed from the coding model's
    config — §1.2: the state must be visible in the report)."""
    tasks_dir = tmp_path / "workspace" / ".drcode" / "tasks"
    tasks_dir.mkdir(parents=True)
    task = _tester_task(
        [{"at": T1, "text": "Context fill 85% — compacting the testing round…"}],
        [
            [
                request_msg("verify", T0),
                request_msg("[context summary]\n\ns", T1),
                response_msg(T1, inp=100, out=10),
            ]
        ],
    )
    task.update({"title": "task"})
    (tasks_dir / "t1.json").write_text(json.dumps(task), encoding="utf-8")
    (tmp_path / "result.json").write_text(
        json.dumps(
            {
                "ok": True,
                "resolved_context_tokens": {"coding": 100000, "tester": 500000},
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "model_log.jsonl").write_text(
        json.dumps(
            {
                "role": "tester-model@http://g/v1",
                "ts": 1730007200.0,
                "usage": {"input_tokens": 85000, "output_tokens": 10},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    # The tester's recorder tag is reconstructed from the generated configs.
    state = tmp_path / "workspace" / ".drcode"
    (state / "drcode.json").write_text(
        json.dumps({"models": {"tester": "p/tester-model"}}), encoding="utf-8"
    )
    catalog_dir = tmp_path / "config-home" / "drcode"
    catalog_dir.mkdir(parents=True, exist_ok=True)
    (catalog_dir / "models.json").write_text(
        json.dumps(
            {
                "providers": [
                    {
                        "name": "p",
                        "base_url": "http://g/v1",
                        "models": [{"id": "tester-model", "max_context_tokens": 500000}],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    metrics = extract_run_metrics(tmp_path, write=False)
    assert metrics["tester_threshold_from_tester"] is False
    assert metrics["totals"]["n_summaries"] >= 1


# -- the development/testing gate (§7 S6, stage 5) --------------------------------


def _gate_task(
    kind: str, title: str, coder_stamps: list[str], tester_rounds: list[tuple[str, str]]
) -> dict:
    return {
        "id": title,
        "title": title,
        "kind": kind,
        "messages": [
            {
                "kind": "response",
                "timestamp": ts,
                "parts": [{"part_kind": "text", "content": "x"}],
                "usage": {"input_tokens": 500, "output_tokens": 50},
            }
            for ts in coder_stamps
        ],
        "tester_messages": [
            [
                {"kind": "request", "timestamp": a, "parts": []},
                {
                    "kind": "response",
                    "timestamp": b,
                    "parts": [],
                    "usage": {"input_tokens": 800, "output_tokens": 30},
                },
            ]
            for a, b in tester_rounds
        ],
        "events": [],
    }


def test_analyze_gate_ok_sequential() -> None:
    """Bug dev → bug testing → feature dev → feature testing: never both
    in flight (§7 S6)."""
    tasks = [
        _gate_task(
            "bug",
            "bug",
            ["2025-06-01T10:00:10+00:00", "2025-06-01T10:00:40+00:00"],
            [("2025-06-01T10:00:45+00:00", "2025-06-01T10:01:10+00:00")],
        ),
        _gate_task(
            "feature",
            "feature",
            ["2025-06-01T10:01:30+00:00", "2025-06-01T10:02:00+00:00"],
            [("2025-06-01T10:02:05+00:00", "2025-06-01T10:02:30+00:00")],
        ),
    ]
    gate = analyze_gate(tasks)
    assert gate["verdict"] == "ok"
    assert gate["overlaps"] == []


def test_analyze_gate_records_overlap_passively() -> None:
    """A coder message stamped inside a tester round is recorded as an
    overlap FACT — but the verdict stays "ok": in multi-task runs the
    coder legitimately develops another task while the tester verifies
    one (overlaps are passive diagnostics, §7 S6)."""
    tasks = [
        _gate_task(
            "bug",
            "bug",
            ["2025-06-01T10:00:10+00:00", "2025-06-01T10:00:40+00:00"],
            [("2025-06-01T10:00:45+00:00", "2025-06-01T10:01:10+00:00")],
        ),
        _gate_task(
            "feature",
            "feature",
            ["2025-06-01T10:00:55+00:00"],
            [],
        ),
    ]
    gate = analyze_gate(tasks)
    assert gate["verdict"] == "ok"
    (o,) = gate["overlaps"]
    assert o["source"] == "transcripts"
    assert "feature" in o["coder"] and "bug" in o["tester"]


def test_analyze_gate_no_testing() -> None:
    gate = analyze_gate([_gate_task("feature", "f", ["2025-06-01T10:00:10+00:00"], [])])
    assert gate["verdict"] == "no-testing"


def test_analyze_gate_recorder_overlap_detected() -> None:
    """Recorder-based overlap diagnostics: coder-tag and tester-tag
    request intervals overlap (a passive fact, verdict stays "ok"); the
    compaction entry (unmatched, §1.5) must not affect the verdict."""
    base = 1750000000.0  # 2025-06-15T15:06:40Z
    t0 = datetime.fromtimestamp(base, tz=UTC).isoformat()
    t1 = datetime.fromtimestamp(base + 55, tz=UTC).isoformat()
    t2 = datetime.fromtimestamp(base + 65, tz=UTC).isoformat()
    tasks = [
        _gate_task("bug", "bug", [t0], [(t1, t2)]),
    ]
    log = [
        # the task's real coder response (matches the transcript)
        {
            "role": "c@a",
            "ts": base + 5,
            "latency_ms": 4000,
            "usage": {"input_tokens": 500, "output_tokens": 50},
        },
        # an in-flight coder request OVERLAPPING an in-flight tester request
        {
            "role": "c@a",
            "ts": base + 30,
            "latency_ms": 60000,
            "usage": {"input_tokens": 500, "output_tokens": 50},
        },
        # the tester's round response (matches the transcript)
        {
            "role": "t@b",
            "ts": base + 60,
            "latency_ms": 4000,
            "usage": {"input_tokens": 800, "output_tokens": 30},
        },
        # an in-flight tester request overlapping the coder request above
        {
            "role": "t@b",
            "ts": base + 20,
            "latency_ms": 60000,
            "usage": {"input_tokens": 800, "output_tokens": 30},
        },
        # compaction traffic: unmatched — must be ignored
        {
            "role": "t@b",
            "ts": base + 20,
            "latency_ms": 4000,
            "usage": {"input_tokens": 111, "output_tokens": 22},
        },
    ]
    gate = analyze_gate(tasks, log)
    assert gate["verdict"] == "ok"
    assert any(o["source"] == "recorder" for o in gate["overlaps"])


def test_analyze_gate_recorder_ok_when_sequential() -> None:
    base = 1750000000.0
    t0 = datetime.fromtimestamp(base, tz=UTC).isoformat()
    t1 = datetime.fromtimestamp(base + 55, tz=UTC).isoformat()
    t2 = datetime.fromtimestamp(base + 65, tz=UTC).isoformat()
    tasks = [_gate_task("bug", "bug", [t0], [(t1, t2)])]
    log = [
        {
            "role": "c@a",
            "ts": base + 5,
            "latency_ms": 4000,
            "usage": {"input_tokens": 500, "output_tokens": 50},
        },
        {
            "role": "t@b",
            "ts": base + 60,
            "latency_ms": 4000,
            "usage": {"input_tokens": 800, "output_tokens": 30},
        },
    ]
    gate = analyze_gate(tasks, log)
    assert gate["verdict"] == "ok"
    assert gate["sources"] == ["transcripts", "recorder"]


def test_extract_run_metrics_carries_gate(tmp_path: Path) -> None:
    tasks_dir = tmp_path / "workspace" / ".drcode" / "tasks"
    tasks_dir.mkdir(parents=True)
    (tmp_path / "result.json").write_text(
        json.dumps({"scenario": "s6", "combo": "c", "ok": True}), encoding="utf-8"
    )
    (tasks_dir / "t1.json").write_text(
        json.dumps(
            _gate_task(
                "bug",
                "bug",
                ["2025-06-01T10:00:10+00:00"],
                [("2025-06-01T10:01:00+00:00", "2025-06-01T10:02:00+00:00")],
            )
        ),
        encoding="utf-8",
    )
    metrics = extract_run_metrics(tmp_path, write=False)
    assert metrics["gate"]["verdict"] == "ok"
    assert metrics["gate"]["n_tester_rounds"] == 1
