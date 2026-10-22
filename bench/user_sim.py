"""User simulator (plan drcode-bench.md, §6).

An asyncio task in the SAME event loop as the headless `DrCodeApp`. It
polls `app.manager` every 0.5–1 s and performs everything a human sitting
at the TUI would do — strictly through the PUBLIC `TaskManager` API (the
very same calls the TUI itself makes: `manager.send`, nothing else; no
`set_hold`, no `delete`, no direct field writes — §6 p.4):

1. **Auto-answer clarification.** A task in AWAITING_CLARIFICATION with
   `task.clarification` gets its answer from `scenario.clarification_answers`
   (match by question substring when `match` is set, otherwise by order)
   and `manager.send(task_id, answer)`. No answer found → the scenario
   FAILS (the task would hang forever waiting for a human).
2. **Follow-up comments** on the scenario schedule (`scenario.followups`):
   condition = the tester stamped FAILED / elapsed time / a task event
   containing a needle. Main case: the tester set FAILED → the simulator
   sends "вот лог ошибки, исправь" with the scenario-defined text.
3. **Stuck protection.** A task ACTIVE with `agent_running=False` and
   `unfinished=False` for longer than N seconds is the "active, nothing
   running" state a live TUI would leave for the human. The simulator
   nudges with a comment ONCE, and if the state persists for another N
   seconds, records a scenario failure.
4. **Never** touches HOLD or deletions (§6 p.4): scenarios don't use them.

Every action is appended to `runs/<run_id>/user_sim.jsonl` (what, when,
which task, which status the task was in) — without this log a report
cannot tell "the model is dumb" from "the simulator intervened" (§6).

Pipeline kicks: `TaskManager.send` only mutates state; promotion is up to
the caller — exactly like the TUI, which advances the pipeline after a
send (drcode/tui/actions.py `_submit_user_text`). The simulator mirrors
that: `app.call_later(app._advance)` for queued/clarification/completed
tasks, and `app.call_later(app.run_agent, task_id)` for a nudge to an
ACTIVE task (the TUI's own "comment to a running task" path).
"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from drcode.models import Task, TaskStatus, VerificationStatus

POLL_SECONDS = 0.75  # §6: polling every 0.5–1 s is enough
STUCK_AFTER_S = 120.0  # "active, nothing running" tolerated this long

# Text for the stuck-protection nudge (§6 p.3). A scenario that wants a
# different text can schedule an ordinary followup instead.
NUDGE_TEXT = (
    "[simulator nudge] Задача активна, но агент ничего не делает. "
    "Продолжай работу над задачей: доделай оставшееся и заверши ход; "
    "если что-то мешает — объясни или задай уточняющий вопрос."
)

# Actions that actually mutated task state through TaskManager (the
# "вмешательства симулятора" column of the report, §10).
INTERVENTION_ACTIONS = ("clarification_answer", "followup", "stuck_nudge")


class UserSimulator:
    """One simulator instance per run; `run()` is the asyncio task body."""

    def __init__(
        self,
        app: Any,
        scenario: Any,
        targets: list[Task],
        log_path: Path,
        *,
        poll_seconds: float = POLL_SECONDS,
        stuck_after_s: float = STUCK_AFTER_S,
        nudge_text: str = NUDGE_TEXT,
    ) -> None:
        self.app = app
        self.scenario = scenario
        self.targets = list(targets)
        self.log_path = Path(log_path)
        self.poll_seconds = poll_seconds
        self.stuck_after_s = stuck_after_s
        self.nudge_text = nudge_text

        self.actions = 0  # every send() performed (interventions, §6/§10)
        self.failures: list[str] = []  # scenario-level failures (§6: hard)
        self._started = time.monotonic()
        self._fired_followups: set[tuple[int, str]] = set()
        self._answers_consumed = 0  # order-based clarification answers
        self._stuck_since: dict[str, float] = {}
        self._nudged: set[str] = set()
        self._logged_failures: set[str] = set()

    # -- run loop -------------------------------------------------------------

    async def run(self) -> None:
        """Poll `app.manager` until cancelled (§4: `sim.cancel()` after
        settle). A crashing tick must never take the run down: it is
        logged as an `error` record and the loop continues."""
        self._log("start", detail={"scenario": self.scenario.id})
        while True:
            try:
                self._tick()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self._log("error", detail={"error": f"{type(e).__name__}: {e}"})
            await asyncio.sleep(self.poll_seconds)

    def failure_reason(self) -> str | None:
        """First recorded scenario failure (a settle-blocker, §6: "ответ
        не найден → провал сценария"). None = nothing to object."""
        return self.failures[0] if self.failures else None

    # -- per-tick handlers ------------------------------------------------------

    def _tick(self) -> None:
        tasks = self.app.manager.all_tasks()
        self._answer_clarifications(tasks)
        self._fire_due_followups()
        self._watch_stuck(tasks)

    # 1. clarification auto-answer (§6 p.1)

    def _answer_clarifications(self, tasks: list[Task]) -> None:
        for task in tasks:
            if task.status is not TaskStatus.AWAITING_CLARIFICATION or task.clarification is None:
                continue
            question = task.clarification.question
            answer = self._find_answer(question)
            if answer is None:
                self._fail(
                    f"task '{task.title}' ({task.id}) awaits clarification "
                    f"but no scenario answer matches: {question!r}"
                )
                continue
            self._send(
                task,
                answer,
                action="clarification_answer",
                detail={"question": question[:200]},
            )

    def _find_answer(self, question: str) -> str | None:
        """Answer lookup (§6): `match`ed answers win (substring of the
        question, case-insensitive); when the scenario defines matchless
        answers they are consumed in declaration order. Matched answers
        that do NOT fit the question are never guessed with."""
        answers = self.scenario.clarification_answers
        matched = [a for a in answers if a.match and a.match.lower() in question.lower()]
        if matched:
            return matched[0].answer
        pool = [a for a in answers if not a.match]
        if self._answers_consumed < len(pool):
            answer = pool[self._answers_consumed]
            self._answers_consumed += 1
            return answer.answer
        return None

    # 2. follow-up comments (§6 p.2)

    def _fire_due_followups(self) -> None:
        for idx, followup in enumerate(self.scenario.followups):
            for task in self._resolve_followup_tasks(followup):
                key = (idx, task.id)
                if key in self._fired_followups:
                    continue
                if not self._followup_due(followup, task):
                    continue
                self._fired_followups.add(key)
                self._send(
                    task,
                    followup.text,
                    action="followup",
                    detail={
                        "when": followup.when,
                        "followup_index": idx,
                    },
                )

    def _resolve_followup_tasks(self, followup: Any) -> list[Task]:
        selector = (followup.task or "last").strip()
        if selector == "all":
            return list(self.targets)
        if selector == "last":
            return [self.targets[-1]] if self.targets else []
        return [t for t in self.targets if selector == t.title or selector in t.title]

    def _followup_due(self, followup: Any, task: Task) -> bool:
        when = followup.when
        if when == "verification_failed":
            return (
                task.status is TaskStatus.COMPLETED
                and task.verification is VerificationStatus.FAILED
            )
        if when == "elapsed":
            assert followup.after_minutes is not None
            return (time.monotonic() - self._started) >= followup.after_minutes * 60.0
        if when.startswith("event:"):
            needle = when.partition(":")[2].strip().lower()
            if not needle:
                return False
            return any(needle in str(ev.text).lower() for ev in task.events)
        return False  # validated away by the loader; never fire on unknown

    # 3. stuck protection (§6 p.3)

    def _watch_stuck(self, tasks: list[Task]) -> None:
        now = time.monotonic()
        agent_running = bool(getattr(self.app, "agent_running", False))
        for task in tasks:
            stuck = task.status is TaskStatus.ACTIVE and not agent_running and not task.unfinished
            if not stuck:
                self._stuck_since.pop(task.id, None)
                continue
            since = self._stuck_since.setdefault(task.id, now)
            if now - since < self.stuck_after_s:
                continue
            if task.id not in self._nudged:
                # Nudge once (the TUI's own path for a comment to an active
                # task: send() + run_agent), then give the model another
                # window before declaring the scenario failed.
                self._nudged.add(task.id)
                self._stuck_since[task.id] = now
                self._send(
                    task,
                    self.nudge_text,
                    action="stuck_nudge",
                    detail={"stuck_for_s": round(now - since, 1)},
                )
            else:
                self._fail(
                    f"task '{task.title}' ({task.id}) is ACTIVE with nothing "
                    f"running for {round(now - since, 1)} s even after a nudge"
                )

    # -- mutation + logging -----------------------------------------------------

    def _send(self, task: Task, text: str, *, action: str, detail: Any) -> None:
        """The ONLY mutation the simulator performs (§6): the public
        `TaskManager.send`, the same call the TUI's submit path makes —
        then the pipeline kick, mirroring `_submit_user_text`."""
        status_before = task.status.value
        self.app.manager.send(task.id, text)
        self.actions += 1
        self._log(
            action,
            task=task,
            task_status=status_before,  # §6: the status the action met
            detail={
                "status_before": status_before,
                "text": text,
                **(detail if isinstance(detail, dict) else {"detail": detail}),
            },
        )
        self._kick(task)

    def _kick(self, task: Task) -> None:
        """Schedule the pipeline advance like the TUI does after a send:
        a comment to an ACTIVE task restarts that task's agent run
        (`run_agent`, the TUI's was_active path); everything else goes
        through the single `_advance` gate."""
        app = self.app
        if task.status is TaskStatus.ACTIVE and not getattr(app, "agent_running", False):
            app.call_later(app.run_agent, task.id)
        else:
            app.call_later(app._advance)

    def _fail(self, message: str) -> None:
        """Record a scenario failure once (dedup): surfaced through
        `failure_reason()` as a settle-blocker (§6: провал сценария)."""
        if message not in self.failures:
            self.failures.append(message)
        if message not in self._logged_failures:
            self._logged_failures.add(message)
            self._log("failure", detail={"reason": message})

    def _log(
        self,
        action: str,
        task: Task | None = None,
        detail: Any = None,
        task_status: str | None = None,
    ) -> None:
        record: dict[str, Any] = {
            "ts": round(time.time(), 3),
            "at": datetime.now(UTC).isoformat(timespec="milliseconds"),
            "action": action,
            "task_id": task.id if task else None,
            "task_title": task.title if task else None,
            "task_status": task_status or (task.status.value if task else None),
            "detail": detail,
        }
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


async def run_user_simulator(
    app: Any,
    scenario: Any,
    targets: list[Task],
    log_path: Path,
    **kwargs: Any,
) -> tuple[UserSimulator, asyncio.Task[None]]:
    """Convenience wrapper (§4 skeleton): create the simulator and run it
    as an asyncio task. Returns the running task's handle tuple
    (simulator, asyncio.Task)."""
    sim = UserSimulator(app, scenario, targets, log_path, **kwargs)
    return sim, asyncio.create_task(sim.run(), name="bench-user-sim")
