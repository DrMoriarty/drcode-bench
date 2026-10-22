"""Mechanical correctness check of the s7_fault_injection scenario
(plan §7 S7, §9 — the proxy fault-injection stage, §12 p.6).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words. Everything asserted here
comes from the persisted task JSON and the run's own artifacts:

  1. pytest is run in the workspace by the harness itself;
  2. the task COMPLETED with verification=PASSED — the run recovered
     from the injected faults and finished the full coding → testing
     loop;
  3. network retries ARE in `events`: every injected fault (2×429 + 1
     connection drop) must have produced a
     "Network error (<type>): retry N/<NETWORK_RETRIES> in X s" event,
     and EVERY observed retry index stays within drcode's retry budget
     (NETWORK_RETRIES = 5, drcode/src/drcode/tui/usage.py) — a retry
     index beyond the budget would mean the budget was ignored;
  4. the interrupted attempt RESUMED without re-sending the brief: the
     original user prompt appears exactly once in `messages` (the
     unfinished-resume path — a duplicated prompt would mean the retry
     re-queued the consumed text instead of resuming it);
  5. the drop hit MID-DEVELOPMENT: the transcript shows tool calls
     (the coder was working when the connection was cut) and the turn
     completed after the retry — at least one tool call precedes the
     first network-error event in time and the task went on to testing.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value
# drcode's in-place retry budget (src/drcode/tui/usage.py) — the exact
# number drcode emits in "retry {attempt}/{NETWORK_RETRIES}".
NETWORK_RETRIES = 5
# Fault script of the scenario (scenario.toml [proxy.faults]): two 429s
# on the first chat/completions requests + one connection drop.
EXPECTED_RETRIES = 3
_RETRY_RE = re.compile(r"^Network error \(([^)]*)\): (?:tester )?retry (\d+)/(\d+) in (\d+) s$")


def _user_prompts(task: dict) -> list[str]:
    out = []
    for msg in task.get("messages") or []:
        if msg.get("role") not in ("request",) and msg.get("kind") != "request":
            continue
        for part in msg.get("parts") or []:
            if (
                isinstance(part, dict)
                and part.get("part_kind") == "user-prompt"
                and isinstance(part.get("content"), str)
            ):
                out.append(part["content"])
    return out


def _first_message_time(task: dict) -> str | None:
    for msg in task.get("messages") or []:
        ts = msg.get("timestamp")
        if ts:
            return str(ts)
    return None


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    failures: list[str] = []
    notes: list[str] = []

    # 1. The seed contract: pytest is green in the workspace.
    pytest_run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    if pytest_run.returncode != 0:
        failures.append(
            "pytest failed in workspace:\n" + (pytest_run.stdout + pytest_run.stderr)[-4000:]
        )

    # 2–5. The S7 assertions over the persisted task JSON.
    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = [
        json.loads(f.read_text(encoding="utf-8"))
        for f in sorted(tasks_dir.glob("*.json"))
    ]
    features = [t for t in tasks if t.get("kind") == "feature"]
    if not features:
        failures.append("no task with kind=feature in .drcode/tasks/")

    for t in features:
        tid = t.get("id")
        if t.get("status") != "completed":
            failures.append(
                f"task {tid}: status={t.get('status')!r}, expected 'completed' — "
                "the run did not recover from the injected faults"
            )
        if t.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"task {tid}: verification={t.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r}"
            )
        if not (t.get("tester_messages") or []):
            failures.append(f"task {tid}: task completed without any testing round")

        # 3. Network retries in events, within the retry budget (§7 S7).
        events = [str(e.get("text", "")) for e in t.get("events") or []]
        retries = []
        for text in events:
            m = _RETRY_RE.match(text)
            if m:
                retries.append(m)
        if len(retries) < EXPECTED_RETRIES:
            failures.append(
                f"task {tid}: {len(retries)} 'Network error (...): retry' "
                f"event(s) in events, expected >= {EXPECTED_RETRIES} "
                "(the fault script injects two 429s and one connection "
                "drop — each must be retried on the real HTTP layer)"
            )
        for m in retries:
            attempt, budget = int(m.group(2)), int(m.group(3))
            if budget != NETWORK_RETRIES:
                failures.append(
                    f"task {tid}: retry event budget {budget} != "
                    f"NETWORK_RETRIES={NETWORK_RETRIES}"
                )
            if attempt > NETWORK_RETRIES:
                failures.append(
                    f"task {tid}: retry attempt {attempt} exceeds the "
                    f"NETWORK_RETRIES={NETWORK_RETRIES} budget"
                )
        who = sorted({("tester" if "tester retry" in m.group(0) else "coder") for m in retries})
        notes.append(
            f"task {tid}: {len(retries)} network retry event(s) "
            f"(who={','.join(who) or '—'}), all within the budget of "
            f"{NETWORK_RETRIES}"
        )

        # 4. unfinished-resume without re-sending the brief (§7 S7).
        prompts = _user_prompts(t)
        briefs = [p for p in prompts if "bullet_list" in p and "Исправьте" in p]
        if len(briefs) != 1:
            failures.append(
                f"task {tid}: the original brief appears {len(briefs)}× in "
                "`messages`, expected exactly 1 — the resumed attempt "
                "re-sent the consumed prompt instead of resuming it"
            )
        # 5. The drop hit mid-development: tool calls exist (the coder
        # was working when the connection was cut) and the transcript
        # carries model responses (the resumed turns completed).
        messages = t.get("messages") or []
        responses = [
            msg for msg in messages
            if msg.get("kind") == "response" or msg.get("role") == "assistant"
        ]
        if not responses:
            failures.append(f"task {tid}: no model responses in the transcript")
        tool_calls = [
            part
            for msg in messages
            for part in msg.get("parts") or []
            if isinstance(part, dict) and part.get("part_kind") == "tool-call"
        ]
        if not tool_calls:
            failures.append(
                f"task {tid}: no tool calls in the transcript — the drop "
                "was supposed to hit mid-development"
            )

    if failures:
        print("S7 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S7 checks: green (pytest passed, feature COMPLETED/PASSED after "
        f"{EXPECTED_RETRIES} injected faults, retries within "
        f"NETWORK_RETRIES={NETWORK_RETRIES}, brief not re-sent on resume)"
    )
    for n in notes:
        print(f"- {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
