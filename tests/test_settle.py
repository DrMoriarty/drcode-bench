"""Tests of settle detection and failure diagnostics (bench.settle, §4)."""

from __future__ import annotations

import asyncio
import json
from datetime import UTC
from pathlib import Path
from types import SimpleNamespace

from bench.scenario import Scenario
from bench.settle import (
    SettleError,
    dead_task_blocker,
    dump_diagnostics,
    settle_blocker,
    wait_settle,
)
from drcode.models import Task, TaskEvent, TaskStatus, VerificationStatus


def make_scenario(**settle) -> Scenario:
    return Scenario(
        id="sX",
        dir=Path("."),
        briefs=(),
        timeout_min=1,
        settle=dict(settle),
    )


class FakePilot:
    def __init__(self) -> None:
        self.pauses = 0

    async def pause(self, delay: float = 0.0) -> None:
        self.pauses += 1
        await asyncio.sleep(0)


def make_app(*tasks: Task, agent_running: bool = False, tester_running: bool = False):
    manager = SimpleNamespace(
        all_tasks=lambda: list(tasks),
        queued=lambda: [t for t in tasks if t.status is TaskStatus.QUEUED],
    )
    return SimpleNamespace(
        manager=manager, agent_running=agent_running, tester_running=tester_running
    )


def completed(verification: VerificationStatus | None = None) -> Task:
    return Task(
        title="t",
        status=TaskStatus.COMPLETED,
        verification=verification,
    )


def test_settled_when_everything_is_done() -> None:
    task = completed(VerificationStatus.PASSED)
    app = make_app(task)
    scenario = make_scenario(verification="passed")
    assert settle_blocker(app, scenario, [task]) is None


def test_active_task_blocks() -> None:
    task = Task(title="t", status=TaskStatus.ACTIVE)
    app = make_app(task)
    blocker = settle_blocker(app, make_scenario(), [task])
    assert blocker is not None and "ACTIVE".lower() in blocker


def test_testing_task_blocks() -> None:
    task = Task(title="t", status=TaskStatus.TESTING)
    app = make_app(task)
    assert settle_blocker(app, make_scenario(), [task])


def test_running_flags_block() -> None:
    task = completed(VerificationStatus.PASSED)
    assert settle_blocker(make_app(task, agent_running=True), make_scenario(), [task])
    assert settle_blocker(make_app(task, tester_running=True), make_scenario(), [task])


def test_queued_task_blocks() -> None:
    task = completed(VerificationStatus.PASSED)
    queued = Task(title="q")
    app = make_app(task, queued)
    blocker = settle_blocker(app, make_scenario(), [task])
    assert blocker is not None and "queue not empty" in blocker


def test_uncompleted_target_blocks() -> None:
    # All statuses benign, but the target task itself is still QUEUED with
    # pending input — not COMPLETED → no settle. (A QUEUED task also makes
    # the queue non-empty; use a task hidden from queued() to isolate.)
    target = Task(title="t", status=TaskStatus.QUEUED)
    app = make_app(target)
    blocker = settle_blocker(app, make_scenario(), [target])
    assert blocker is not None


def test_verification_expectation_fails_on_failed_label() -> None:
    task = completed(VerificationStatus.FAILED)
    app = make_app(task)
    blocker = settle_blocker(app, make_scenario(verification="passed"), [task])
    assert blocker is not None and "expected PASSED" in blocker


async def test_wait_settle_success_polls_pilot() -> None:
    # Start unsettled, complete the task after two polls.
    task = Task(title="t", status=TaskStatus.ACTIVE)
    app = make_app(task)
    pilot = FakePilot()

    async def finish_soon() -> None:
        await asyncio.sleep(0.03)
        task.status = TaskStatus.COMPLETED
        task.verification = VerificationStatus.PASSED

    asyncio.get_running_loop().create_task(finish_soon())
    result = await wait_settle(
        app,
        make_scenario(verification="passed"),
        pilot,
        timeout=5.0,
        targets=[task],
        poll_seconds=0.01,
    )
    assert result.ok and not result.timed_out
    assert pilot.pauses > 0


async def test_wait_settle_timeout_is_failure_not_exception() -> None:
    task = Task(title="stuck", status=TaskStatus.ACTIVE)
    app = make_app(task)
    scenario = make_scenario()
    result = await wait_settle(
        app, scenario, FakePilot(), timeout=0.05, targets=[task], poll_seconds=0.01
    )
    assert not result.ok and result.timed_out
    assert "timeout" in result.reason and "stuck" in result.reason


async def test_wait_settle_extra_blocker_hard_failure() -> None:
    """§6: a simulator-recorded scenario failure (e.g. an unanswered
    clarification) is a HARD failure — settle stops immediately instead
    of burning the scenario timeout."""
    task = completed(VerificationStatus.PASSED)
    app = make_app(task)
    result = await wait_settle(
        app,
        make_scenario(verification="passed"),
        FakePilot(),
        timeout=5.0,
        targets=[task],
        poll_seconds=0.01,
        extra_blocker=lambda: "no answer for the clarifying question",
    )
    assert not result.ok and not result.timed_out
    assert "no answer" in result.reason


async def test_wait_settle_extra_blocker_none_is_no_objection() -> None:
    task = completed(VerificationStatus.PASSED)
    app = make_app(task)
    result = await wait_settle(
        app,
        make_scenario(verification="passed"),
        FakePilot(),
        timeout=5.0,
        targets=[task],
        poll_seconds=0.01,
        extra_blocker=lambda: None,
    )
    assert result.ok and not result.timed_out


async def test_wait_settle_broken_app_is_error() -> None:
    app = SimpleNamespace(manager=None)
    try:
        await wait_settle(app, make_scenario(), FakePilot(), timeout=0.05, poll_seconds=0.01)
    except SettleError as e:
        assert "settle check crashed" in str(e)
    else:
        raise AssertionError("expected SettleError")


# -- dead tasks: deterministic context overflow (hard settle blocker) --------------

# The real event pair drcode emits on a deterministic context overflow
# (pipeline_agent_run: the raw error first, then the manual-intervention
# diagnosis; the task goes back to the queue forever).
_OVERFLOW_ERROR_EVENT = (
    "ModelContextWindowExceededError: status_code: 400, model_name: x5, "
    "body: {'detail': 'Error code: 400 - requested token count exceeds the "
    "model's maximum context length of 262144 tokens'}"
)
_HTTP_OVERFLOW_ERROR_EVENT = (
    "ModelHTTPError: status_code: 400, body: {'message': "
    '"context_length_exceeded: reduce the length of the input"}'
)
_TRANSIENT_ERROR_EVENT = (
    "ModelHTTPError: status_code: 429, body: {'message': 'rate limit exceeded, retry later'}"
)
_DEAD_TASK_MARKER_EVENT = (
    "The transcript exceeds the model's context window: the model rejects "
    "it deterministically on every attempt, retrying cannot help. The task "
    "needs manual intervention — delete it, or shrink its transcript "
    "(e.g. mechanical compaction)."
)


def task_with_events(*texts: str) -> Task:
    t = Task(title="dead")
    t.events = [TaskEvent(text=text) for text in texts]
    return t


def test_dead_task_blocker_fires_on_pair() -> None:
    task = task_with_events("working…", _OVERFLOW_ERROR_EVENT, _DEAD_TASK_MARKER_EVENT)
    reason = dead_task_blocker([task])
    assert reason is not None and "dead" in reason and "context" in reason


def test_dead_task_blocker_accepts_http_overflow_variant() -> None:
    # Some gateways surface the 400 as a plain ModelHTTPError — the pair
    # must still be recognized via the overflow markers (usage.py list).
    task = task_with_events(_HTTP_OVERFLOW_ERROR_EVENT, _DEAD_TASK_MARKER_EVENT)
    assert dead_task_blocker([task]) is not None


def test_dead_task_blocker_requires_error_before_marker() -> None:
    # Marker alone (e.g. reworded upstream text) is not enough — fail only
    # on the «overflow error + subsequent manual-intervention» pair.
    assert dead_task_blocker([task_with_events(_DEAD_TASK_MARKER_EVENT)]) is None


def test_dead_task_blocker_ignores_transient_errors() -> None:
    # 429s / network errors are retried by design — never terminal.
    task = task_with_events(_TRANSIENT_ERROR_EVENT, _DEAD_TASK_MARKER_EVENT)
    assert dead_task_blocker([task]) is None


def test_dead_task_blocker_ignores_benign_tasks() -> None:
    ok = completed(VerificationStatus.PASSED)
    assert dead_task_blocker([ok]) is None


async def test_wait_settle_dead_task_is_immediate_hard_failure() -> None:
    """A dead task keeps the queue non-empty (soft blocker) forever —
    settle must fail the run immediately instead of burning the timeout
    (S4/incredible-four: 3 × 45 min on runs decided in ~2 minutes)."""
    dead = task_with_events(_OVERFLOW_ERROR_EVENT, _DEAD_TASK_MARKER_EVENT)
    target = completed(VerificationStatus.PASSED)
    app = make_app(target, dead)
    result = await wait_settle(
        app,
        make_scenario(verification="passed"),
        FakePilot(),
        timeout=30.0,
        targets=[target],
        poll_seconds=0.01,
    )
    assert not result.ok and not result.timed_out
    assert "dead" in result.reason and "manual intervention" in result.reason
    assert result.elapsed_s < 5.0  # did not wait for the 30 s timeout


async def test_wait_settle_settled_ok_beats_dead_task_marker() -> None:
    # Defensive ordering: the hard blocker is evaluated only when the soft
    # criterion does not hold — a task that somehow settled with the pair
    # in its history must not flip a green run.
    task = task_with_events(_OVERFLOW_ERROR_EVENT, _DEAD_TASK_MARKER_EVENT)
    task.status = TaskStatus.COMPLETED
    task.verification = VerificationStatus.PASSED
    app = make_app(task)
    result = await wait_settle(
        app,
        make_scenario(verification="passed"),
        FakePilot(),
        timeout=1.0,
        targets=[task],
        poll_seconds=0.01,
    )
    assert result.ok and not result.timed_out


# -- dump_diagnostics -------------------------------------------------------------


def test_dump_diagnostics_full(tmp_path: Path) -> None:
    from datetime import datetime

    state = tmp_path / "workspace" / ".drcode" / "tasks"
    state.mkdir(parents=True)
    (state / "abc123.json").write_text(
        json.dumps(
            {
                "id": "abc123",
                "title": "feature task",
                "kind": "feature",
                "status": "active",
                "verification": None,
                "unfinished": True,
                "clarification": {"question": "что именно?"},
                "events": [
                    {"at": datetime.now(UTC).isoformat(), "text": f"e{i}"} for i in range(50)
                ],
                "tester_messages": [[], []],
                "messages": [1, 2, 3],
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "model_log.jsonl").write_text(
        "\n".join(f'{{"i": {i}}}' for i in range(500)) + "\n", encoding="utf-8"
    )

    diag = dump_diagnostics(tmp_path)
    assert (diag / "drcode-state" / "tasks" / "abc123.json").is_file()
    report = json.loads((diag / "diagnostics.json").read_text(encoding="utf-8"))
    (task,) = report["tasks"]
    assert task["id"] == "abc123"
    assert task["unfinished"] is True
    assert task["clarification"] == {"question": "что именно?"}
    assert len(task["last_events"]) == 30  # tail only
    assert task["n_testing_rounds"] == 2
    assert report["logs"]["model_log.jsonl"]["n_lines"] == 500
    assert len(report["logs"]["model_log.jsonl"]["tail"]) == 200


def test_dump_diagnostics_on_empty_run(tmp_path: Path) -> None:
    """A run that died before anything was written must not crash."""
    diag = dump_diagnostics(tmp_path / "never_existed")
    report = json.loads((diag / "diagnostics.json").read_text(encoding="utf-8"))
    assert report["state_dir_found"] is False
    assert report["tasks"] == []
