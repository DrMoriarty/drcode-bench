"""Settle detection and failure diagnostics (plan drcode-bench.md, §4).

Settle criterion (success of a run): no task in ACTIVE/TESTING, every
target task COMPLETED, `tester_running=False`, `agent_running=False`,
the queue is empty — plus the scenario-specific check
(`Scenario.settle_ok`, e.g. "verification=PASSED" for S1).

The scenario timeout is a SOFT limit (default 30–60 min, plan §4): when
it expires the run fails and `dump_diagnostics` snapshots everything
needed to dissect the run without repeating it (a copy of `.drcode/`,
the last events of every task, `unfinished`/`clarification` flags, log
tails).
"""

from __future__ import annotations

import asyncio
import json
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from drcode.models import TaskStatus

if TYPE_CHECKING:  # only for type hints; keeps the module import-light
    from .scenario import Scenario

POLL_SECONDS = 1.0
EVENT_TAIL = 30  # last events per task in the diagnostics snapshot
LOG_TAIL_LINES = 200  # tail of each log file

# §4/§6: a task whose transcript is over the model's context window is DEAD —
# drcode rejects it deterministically on every attempt (the summarizer's
# mechanical trim is chars-estimated and does not guarantee the real window),
# emits the error event followed by the manual-intervention event
# (drcode/src/drcode/tui/pipeline_agent_run.py) and parks the task back in the
# queue forever. Without special handling settle burns the whole scenario
# timeout on "queue not empty" (S4/incredible-four: 3 × 45 min on runs decided
# in the first ~2 minutes). The manual-intervention phrase is emitted ONLY by
# drcode's deterministic-overflow branch — never by model output or scenario
# text — but we still require the overflow-error event to precede it (the
# «pair»), so a reworded drcode message can never fail a run on its own.
DEAD_TASK_MARKER = "needs manual intervention"
_OVERFLOW_ERROR_NAME = "modelcontextwindowexceedederror"
_HTTP_ERROR_NAME = "modelhttperror"
# Same phrasings drcode's own _is_context_overflow_error matches (usage.py).
_HTTP_OVERFLOW_MARKERS = (
    "context length",
    "context_length",
    "context too long",
    "context window",
    "prompt is too long",
    "input is too long",
    "input too long",
    "too many tokens",
    "reduce the length of the input",
    "context overflow",
)


def _is_overflow_error_event(text_lower: str) -> bool:
    """True when an event text looks like the deterministic context-overflow
    model rejection (transient 429s / transport drops never match — those
    must keep retrying)."""
    if _OVERFLOW_ERROR_NAME in text_lower:
        return True
    return _HTTP_ERROR_NAME in text_lower and any(
        marker in text_lower for marker in _HTTP_OVERFLOW_MARKERS
    )


def dead_task_blocker(tasks: list[Any]) -> str | None:
    """Hard (terminal) blocker: a task carrying the «deterministic
    context-overflow error + manual-intervention event» pair. Such a task
    can never leave the queue this session, so waiting for settle is
    pointless — the run fails immediately with this reason."""
    for t in tasks:
        texts = [str(e.text).lower() for e in t.events]
        for i, text in enumerate(texts):
            if DEAD_TASK_MARKER in text and any(
                _is_overflow_error_event(prev) for prev in texts[:i]
            ):
                return (
                    f"task '{t.title}' ({t.id}) is dead: deterministic context "
                    "overflow, manual intervention required"
                )
    return None


class SettleError(RuntimeError):
    """Settle criterion cannot be evaluated (broken harness state)."""


@dataclass(frozen=True)
class SettleResult:
    ok: bool
    reason: str
    elapsed_s: float
    timed_out: bool


def settle_blocker(app: Any, scenario: Scenario, targets: list[Any]) -> str | None:
    """One evaluation of the settle criterion: None = settled, otherwise
    the current reason it is not.

    `targets` are the tasks created from the scenario briefs (the tester
    may have added bug-report tasks on top; those are covered by the
    queue/ACTIVE/TESTING checks and, via `settle.verification`, by the
    scenario check too).
    """
    tasks = app.manager.all_tasks()

    for t in tasks:
        if t.status in (TaskStatus.ACTIVE, TaskStatus.TESTING):
            return f"task '{t.title}' ({t.id}) is {t.status.value}"
    if app.agent_running:
        return "agent_running"
    if app.tester_running:
        return "tester_running"
    queued = app.manager.queued()
    if queued:
        names = ", ".join(f"'{t.title}'" for t in queued[:3])
        return f"queue not empty: {names}"
    for t in targets:
        if t.status is not TaskStatus.COMPLETED:
            return f"target task '{t.title}' ({t.id}) is {t.status.value}"
    return scenario.settle_ok(targets)


async def wait_settle(
    app: Any,
    scenario: Scenario,
    pilot: Any,
    timeout: float,
    *,
    targets: list[Any] | None = None,
    poll_seconds: float = POLL_SECONDS,
    extra_blocker: Any = None,
) -> SettleResult:
    """Poll the settle criterion until it holds or the (soft) timeout of
    the scenario expires (plan §4). The timeout expiring is a FAILURE of
    the run, not an exception — the caller dumps diagnostics and reports.

    `pilot` is the textual Pilot of `run_test()`; polling goes through
    `pilot.pause()` so the app keeps processing its message queue while
    we wait.

    `extra_blocker` (used by the user simulator, §6): a callable returning
    None (no objection) or a failure reason string. A non-None result is a
    HARD scenario failure ("ответ не найден → провал сценария"): settle
    stops immediately with ok=False instead of burning the whole scenario
    timeout on a run that can no longer succeed.

    A dead task (deterministic context overflow, `dead_task_blocker`) is
    the same kind of HARD blocker, detected from the app state itself: the
    moment any task shows the «overflow error + manual intervention» pair,
    the run fails immediately with that reason (the soft blockers — the
    dead task keeps the queue non-empty — would otherwise spin until the
    scenario timeout).
    """
    targets = targets or []
    start = time.monotonic()
    deadline = start + timeout
    reason = "scenario timeout before the first settle check"

    while True:
        if extra_blocker is not None:
            hard = extra_blocker()
            if hard:
                return SettleResult(
                    ok=False,
                    reason=f"scenario failure: {hard}",
                    elapsed_s=time.monotonic() - start,
                    timed_out=False,
                )
        try:
            reason = settle_blocker(app, scenario, targets)
        except Exception as e:
            raise SettleError(f"settle check crashed: {type(e).__name__}: {e}") from e
        if reason is None:
            return SettleResult(
                ok=True,
                reason="settled",
                elapsed_s=time.monotonic() - start,
                timed_out=False,
            )
        # Not settled: before scheduling another poll, check for a terminal
        # state — a dead task never leaves the queue, so a soft reason like
        # "queue not empty" would only burn the scenario timeout.
        hard = dead_task_blocker(app.manager.all_tasks())
        if hard is not None:
            return SettleResult(
                ok=False,
                reason=hard,
                elapsed_s=time.monotonic() - start,
                timed_out=False,
            )
        if time.monotonic() >= deadline:
            return SettleResult(
                ok=False,
                reason=f"timeout ({scenario.timeout_min:g} min): last blocker: {reason}",
                elapsed_s=time.monotonic() - start,
                timed_out=True,
            )
        await asyncio.sleep(poll_seconds)
        # Keep the textual app pumping while we poll (same loop, headless).
        if pilot is not None:
            await pilot.pause(0.0)


# -- failure diagnostics (§4) ----------------------------------------------------


def dump_diagnostics(run_dir: Path) -> Path:
    """Snapshot everything needed to dissect a failed run WITHOUT
    repeating it (plan §4):

    - a full copy of `<workspace>/.drcode/` (tasks, events, configs);
    - `diagnostics.json`: per-task status/verification/unfinished/
      clarification + the last events, plus the tails of the run logs
      (model_log.jsonl, user_sim.jsonl) when present.

    Safe to call on a run that died early: every input is optional.
    Returns the diagnostics directory.
    """
    run_dir = Path(run_dir)
    diag = run_dir / "diagnostics"
    diag.mkdir(parents=True, exist_ok=True)

    state_dir = run_dir / "workspace" / ".drcode"
    state_copy = diag / "drcode-state"
    if state_dir.is_dir() and not state_copy.exists():
        shutil.copytree(state_dir, state_copy)

    report: dict[str, Any] = {
        "run_dir": str(run_dir),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "state_dir_found": state_dir.is_dir(),
        "tasks": [],
        "logs": {},
    }

    if state_dir.is_dir():
        for task_file in sorted((state_dir / "tasks").glob("*.json")):
            try:
                raw = json.loads(task_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as e:
                report["tasks"].append({"file": task_file.name, "error": str(e)})
                continue
            events = raw.get("events") or []
            report["tasks"].append(
                {
                    "id": raw.get("id"),
                    "title": raw.get("title"),
                    "kind": raw.get("kind"),
                    "status": raw.get("status"),
                    "verification": raw.get("verification"),
                    "unfinished": raw.get("unfinished"),
                    "clarification": raw.get("clarification"),
                    "n_events": len(events),
                    "last_events": [
                        {"at": e.get("at"), "text": e.get("text")} for e in events[-EVENT_TAIL:]
                    ],
                    "n_testing_rounds": len(raw.get("tester_messages") or []),
                    "n_messages": len(raw.get("messages") or []),
                }
            )

    for log_name in (
        "model_log.jsonl",
        "proxy_log.jsonl",
        "user_sim.jsonl",
        "stderr.log",
        "stdout.log",
    ):
        log_file = run_dir / log_name
        if not log_file.is_file():
            continue
        try:
            lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as e:
            report["logs"][log_name] = {"error": str(e)}
            continue
        report["logs"][log_name] = {
            "n_lines": len(lines),
            "tail": lines[-LOG_TAIL_LINES:],
        }

    out = diag / "diagnostics.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return diag
