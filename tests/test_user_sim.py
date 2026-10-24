"""Tests of the user simulator (bench.user_sim, plan drcode-bench.md §6).

Unit level: a REAL TaskManager on a tmp project root + a stub app that
records the pipeline kicks — the simulator must mutate task state ONLY
through the public TaskManager API and log every action to
user_sim.jsonl.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
from pathlib import Path

from bench.scenario import ClarificationAnswer, Followup, Scenario
from bench.user_sim import UserSimulator
from drcode.models import TaskEvent, TaskKind, TaskStatus, VerificationStatus
from drcode.task_manager import TaskManager


class FakeApp:
    """The slice of the textual app the simulator touches: the manager,
    the run flags and the pipeline entry points the TUI itself uses."""

    def __init__(self, manager: TaskManager) -> None:
        self.manager = manager
        self.agent_running = False
        self.tester_running = False
        self.kicks: list[tuple[str, tuple]] = []

    def call_later(self, callback, *args) -> bool:
        self.kicks.append((getattr(callback, "__name__", str(callback)), args))
        return True

    def _advance(self) -> None:  # the pipeline gate (kick target)
        pass

    def run_agent(self, task_id: str) -> None:  # active-task kick target
        pass


def make_scenario(**kwargs) -> Scenario:
    return Scenario(id="sX", dir=Path("."), briefs=(), timeout_min=1, **kwargs)


def make_manager(tmp_path: Path) -> TaskManager:
    return TaskManager(tmp_path / "project")


def read_log(log_path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in log_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


async def run_until(sim: UserSimulator, pred, timeout: float = 2.0) -> None:
    """Run the simulator's poll loop until `pred()` holds, then cancel."""
    task = asyncio.create_task(sim.run())
    try:
        async with asyncio.timeout(timeout):
            while not pred():
                await asyncio.sleep(0.01)
    finally:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task


async def test_clarification_answered_by_match(tmp_path: Path) -> None:
    from drcode.models import Clarification

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    task = manager.create("t", "", kind=TaskKind.FEATURE)
    task.status = TaskStatus.AWAITING_CLARIFICATION
    task.clarification = Clarification(question="Какой формат использовать?")
    manager.storage.save(task)

    scenario = make_scenario(
        clarification_answers=(ClarificationAnswer(match="формат", answer="JSON"),)
    )
    log_path = tmp_path / "user_sim.jsonl"
    sim = UserSimulator(app, scenario, [task], log_path)

    await run_until(sim, lambda: app.kicks)

    assert task.status is TaskStatus.QUEUED
    assert task.queue_head is True  # answered clarifications jump the queue
    assert [e.text for e in task.pending_input] == ["JSON"]
    assert task.clarification is None
    assert sim.actions == 1
    assert ("_advance", ()) in app.kicks

    records = read_log(log_path)
    answer = next(r for r in records if r["action"] == "clarification_answer")
    assert answer["task_id"] == task.id
    assert answer["task_status"] == "clarification"  # §6: logged with the status
    assert answer["detail"]["text"] == "JSON"


def test_find_answer_anyof_list_matches_paraphrase(tmp_path: Path) -> None:
    """List `match` = any-of substrings, case-insensitive. The question is
    the real one from run 20261024-130550 (s5, combo
    degradation-weak-compactor): it contains the Latin function name
    format_price and the word «стандарт», but NO Cyrillic «формат» — the
    old single-substring matcher recorded a hard scenario failure here."""
    from bench.user_sim import UserSimulator

    scenario = make_scenario(
        clarification_answers=(
            ClarificationAnswer(
                match=["формат", "стандарт", "оформления цен"],
                answer="Стандарт: 1 234,50 ₽",
            ),
        )
    )
    sim = UserSimulator(object(), scenario, [], tmp_path / "sim.jsonl")

    failing = (
        "Опишите, пожалуйста, корпоративный стандарт оформления цен: как "
        "должна выглядеть строка, которую возвращает format_price(amount, "
        "currency)? Например: какой разделитель тысяч и дробной части, …"
    )
    assert sim._find_answer(failing) == "Стандарт: 1 234,50 ₽"
    assert sim._find_answer("Какой ФОРМАТ использовать?") == "Стандарт: 1 234,50 ₽"
    assert sim._find_answer("Что делать?") is None

    # A single-string match still works (the pre-list shape).
    scenario = make_scenario(
        clarification_answers=(ClarificationAnswer(match="формат", answer="JSON"),)
    )
    sim = UserSimulator(object(), scenario, [], tmp_path / "sim.jsonl")
    assert sim._find_answer("Какой формат?") == "JSON"
    assert sim._find_answer("Какой вид?") is None


async def test_clarification_answered_by_list_match(tmp_path: Path) -> None:
    from drcode.models import Clarification

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    task = manager.create("t", "", kind=TaskKind.FEATURE)
    task.status = TaskStatus.AWAITING_CLARIFICATION
    # Paraphrase without the «формат» needle — only «стандарт» hits.
    task.clarification = Clarification(question="Опишите корпоративный стандарт оформления цен?")
    manager.storage.save(task)

    scenario = make_scenario(
        clarification_answers=(ClarificationAnswer(match=["формат", "стандарт"], answer="JSON"),)
    )
    sim = UserSimulator(app, scenario, [task], tmp_path / "sim.jsonl")
    await run_until(sim, lambda: app.kicks)

    assert task.status is TaskStatus.QUEUED
    assert [e.text for e in task.pending_input] == ["JSON"]


async def test_clarification_waits_for_agent_turn_to_finish(tmp_path: Path) -> None:
    """The answer must not land while the asker's agent run is live:
    send() would requeue the task and cancel the run before it persists
    the ask exchange — the sanitized history then drops the ask entirely
    (s5_clarification check 3a race)."""
    from drcode.models import Clarification

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    task = manager.create("t", "", kind=TaskKind.FEATURE)
    task.status = TaskStatus.AWAITING_CLARIFICATION
    task.clarification = Clarification(question="Какой формат использовать?")
    manager.storage.save(task)

    scenario = make_scenario(
        clarification_answers=(ClarificationAnswer(match="формат", answer="JSON"),)
    )
    sim = UserSimulator(app, scenario, [task], tmp_path / "sim.jsonl")
    app.agent_running = True  # the asker's turn is still winding down

    ran = asyncio.create_task(sim.run())
    try:
        await asyncio.sleep(0.15)  # a couple of polls: nothing sent yet
        assert sim.actions == 0
        assert task.status is TaskStatus.AWAITING_CLARIFICATION
        assert task.pending_input == []

        app.agent_running = False  # the turn finished and persisted
        async with asyncio.timeout(2.0):
            while sim.actions < 1:
                await asyncio.sleep(0.01)
    finally:
        ran.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await ran

    assert task.status is TaskStatus.QUEUED
    assert [e.text for e in task.pending_input] == ["JSON"]


async def test_clarification_answered_by_order(tmp_path: Path) -> None:
    from drcode.models import Clarification, TaskKind

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    tasks = []
    for title in ("a", "b"):
        t = manager.create(title, "", kind=TaskKind.FEATURE)
        t.status = TaskStatus.AWAITING_CLARIFICATION
        t.clarification = Clarification(question=f"Вопрос про {title}?")
        manager.storage.save(t)
        tasks.append(t)

    scenario = make_scenario(
        clarification_answers=(
            ClarificationAnswer(match=None, answer="первый ответ"),
            ClarificationAnswer(match=None, answer="второй ответ"),
        )
    )
    sim = UserSimulator(app, scenario, tasks, tmp_path / "sim.jsonl")
    await run_until(sim, lambda: sim.actions >= 2)

    got = {t.title: t.pending_input[0].text for t in tasks if t.pending_input}
    assert got == {"a": "первый ответ", "b": "второй ответ"}


async def test_clarification_without_answer_fails_scenario(tmp_path: Path) -> None:
    from drcode.models import Clarification, TaskKind

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    task = manager.create("t", "", kind=TaskKind.FEATURE)
    task.status = TaskStatus.AWAITING_CLARIFICATION
    task.clarification = Clarification(question="Что делать?")
    manager.storage.save(task)

    scenario = make_scenario()  # no answers at all
    log_path = tmp_path / "sim.jsonl"
    sim = UserSimulator(app, scenario, [task], log_path)

    await run_until(sim, lambda: sim.failures)

    reason = sim.failure_reason()
    assert reason and "clarification" in reason
    # §6: not answered → the task must stay untouched, still awaiting.
    assert task.status is TaskStatus.AWAITING_CLARIFICATION
    assert not task.pending_input
    records = read_log(log_path)
    assert any(r["action"] == "failure" for r in records)


async def test_followup_on_verification_failed_fires_once(tmp_path: Path) -> None:
    from drcode.models import TaskKind

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    task = manager.create("Починить", "", kind=TaskKind.BUG)
    task.status = TaskStatus.COMPLETED
    task.verification = VerificationStatus.FAILED
    manager.storage.save(task)

    scenario = make_scenario(
        followups=(
            Followup(
                task="Починить",
                when="verification_failed",
                after_minutes=None,
                text="вот лог ошибки, исправь",
            ),
        )
    )
    log_path = tmp_path / "sim.jsonl"
    sim = UserSimulator(app, scenario, [task], log_path)

    await run_until(sim, lambda: app.kicks)
    # The FAILED verdict re-queues the task through the public send().
    assert task.status is TaskStatus.QUEUED
    assert task.verification is None  # the stale label is reset by send()
    assert [e.text for e in task.pending_input] == ["вот лог ошибки, исправь"]
    assert sim.actions == 1

    # Keep polling: the follow-up must not fire a second time.
    n_actions = sim.actions
    await asyncio.sleep(0.05)
    assert sim.actions == n_actions
    follows = [r for r in read_log(log_path) if r["action"] == "followup"]
    assert len(follows) == 1
    assert follows[0]["detail"]["when"] == "verification_failed"


async def test_followup_elapsed_fires_after_delay(tmp_path: Path) -> None:
    from drcode.models import TaskKind

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    task = manager.create("t", "", kind=TaskKind.FEATURE)

    scenario = make_scenario(
        followups=(
            Followup(
                task="all",
                when="elapsed",
                after_minutes=1.0 / 60.0,  # 1 second
                text="подстёгивание по времени",
            ),
        )
    )
    sim = UserSimulator(app, scenario, [task], tmp_path / "sim.jsonl")
    await run_until(sim, lambda: sim.actions >= 1, timeout=5.0)
    assert [e.text for e in task.pending_input] == ["подстёгивание по времени"]


async def test_followup_event_condition(tmp_path: Path) -> None:
    from drcode.models import TaskKind

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    task = manager.create("t", "", kind=TaskKind.FEATURE)
    task.events.append(TaskEvent(text="Network error (Timeout): retry 1/4 in 2 s"))
    manager.storage.save(task)

    scenario = make_scenario(
        followups=(
            Followup(
                task="t",
                when="event:network error",
                after_minutes=None,
                text="сеть моргнула — продолжай",
            ),
        )
    )
    sim = UserSimulator(app, scenario, [task], tmp_path / "sim.jsonl")
    await run_until(sim, lambda: sim.actions >= 1)
    assert [e.text for e in task.pending_input] == ["сеть моргнула — продолжай"]


async def test_stuck_active_task_is_nudged_then_fails(tmp_path: Path) -> None:
    from drcode.models import TaskKind

    manager = make_manager(tmp_path)
    app = FakeApp(manager)  # agent_running stays False — nothing is running
    task = manager.create("t", "", kind=TaskKind.FEATURE)
    task.status = TaskStatus.ACTIVE
    manager.storage.save(task)

    scenario = make_scenario()
    log_path = tmp_path / "sim.jsonl"
    sim = UserSimulator(app, scenario, [task], log_path, poll_seconds=0.01, stuck_after_s=0.05)

    await run_until(sim, lambda: sim.failures, timeout=5.0)

    # First a nudge through the TUI's own active-task path...
    assert [e.text for e in task.pending_input] == [sim.nudge_text]
    assert ("run_agent", (task.id,)) in app.kicks
    # ...then, with nothing still running, a scenario failure.
    reason = sim.failure_reason()
    assert reason and "ACTIVE" in reason
    records = read_log(log_path)
    actions = [r["action"] for r in records]
    assert "stuck_nudge" in actions
    assert "failure" in actions


async def test_active_task_with_running_agent_is_not_stuck(tmp_path: Path) -> None:
    from drcode.models import TaskKind

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    app.agent_running = True
    task = manager.create("t", "", kind=TaskKind.FEATURE)
    task.status = TaskStatus.ACTIVE
    manager.storage.save(task)

    sim = UserSimulator(
        app,
        make_scenario(),
        [task],
        tmp_path / "sim.jsonl",
        poll_seconds=0.01,
        stuck_after_s=0.05,
    )
    await asyncio.sleep(0.2)
    assert sim.actions == 0
    assert not sim.failures
    assert task.status is TaskStatus.ACTIVE and not task.pending_input


async def test_hold_and_unfinished_are_untouched(tmp_path: Path) -> None:
    from drcode.models import TaskKind

    manager = make_manager(tmp_path)
    app = FakeApp(manager)
    held = manager.create("held", "", kind=TaskKind.FEATURE)
    held.status = TaskStatus.HOLD
    paused = manager.create("paused", "", kind=TaskKind.FEATURE)
    paused.status = TaskStatus.ACTIVE
    paused.unfinished = True  # an interrupted attempt — resumable, not stuck
    manager.storage.save(held)
    manager.storage.save(paused)

    sim = UserSimulator(
        app,
        make_scenario(),
        [held, paused],
        tmp_path / "sim.jsonl",
        poll_seconds=0.01,
        stuck_after_s=0.05,
    )
    await asyncio.sleep(0.2)
    assert sim.actions == 0 and not sim.failures
    assert held.status is TaskStatus.HOLD  # §6 p.4: never touched
    assert paused.unfinished is True


def test_analyze_user_sim_interventions(tmp_path: Path) -> None:
    from bench.metrics import analyze_user_sim

    entries = [
        {"action": "start"},
        {"action": "clarification_answer", "task_id": "a"},
        {"action": "followup", "task_id": "a"},
        {"action": "stuck_nudge", "task_id": "b"},
        {"action": "failure", "detail": {"reason": "no answer"}},
    ]
    stats = analyze_user_sim(entries)
    assert stats["interventions"] == 3
    assert stats["by_action"]["clarification_answer"] == 1
    assert stats["failures"] == ["no answer"]


def test_extract_run_metrics_includes_user_sim(tmp_path: Path) -> None:
    from bench.metrics import extract_run_metrics

    run_dir = tmp_path / "r1"
    (run_dir / "workspace" / ".drcode" / "tasks").mkdir(parents=True)
    (run_dir / "result.json").write_text(
        json.dumps({"scenario": "s5", "combo": "c", "ok": True}), encoding="utf-8"
    )
    (run_dir / "user_sim.jsonl").write_text(
        json.dumps({"action": "clarification_answer", "task_id": "a"})
        + "\n"
        + json.dumps({"action": "followup", "task_id": "a"})
        + "\n",
        encoding="utf-8",
    )
    metrics = extract_run_metrics(run_dir)
    assert metrics["user_sim"]["interventions"] == 2
    assert metrics["totals"]["user_sim_interventions"] == 2


def test_extract_run_metrics_without_user_sim(tmp_path: Path) -> None:
    from bench.metrics import extract_run_metrics

    run_dir = tmp_path / "r1"
    (run_dir / "workspace" / ".drcode" / "tasks").mkdir(parents=True)
    metrics = extract_run_metrics(run_dir)
    assert metrics["user_sim"] is None
    assert metrics["totals"]["user_sim_interventions"] == 0
