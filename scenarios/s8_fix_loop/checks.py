"""Mechanical correctness check of s8_fix_loop (plan drcode-bench.md §7;
upstream drcode 18b48f9 — the tester fix loop).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. pytest is run in the workspace by the harness itself — the second
     development round must have left the seed contract green;
  2. the brief task must show the fix loop in its persisted JSON:
     COMPLETED with verification=PASSED, at least 2 testing rounds and at
     least 2 development rounds (two user prompts: the brief + the
     tester's fix-loop report consumed as the task's next input);
  3. the requeue event is in `events` with the exact wording of
     TaskManager.requeue_failed_fix (drcode 18b48f9): "testing failed —
     returned for another development round (round 2/3)" — the counter is
     incremented before the event is composed and the number names the
     UPCOMING development round (the brief is round 1), so "2" is the
     persisted proof that `fix_rounds` reached 1 at the requeue; the final
     JSON necessarily reads `fix_rounds == 0`, because the PASSED verdict
     resets the counter (set_verification, task_manager.py) — asserting 1
     on the completed task would contradict drcode's reset-on-success;
  4. zero user interventions: `user_sim.jsonl` (next to the workspace, in
     the run dir) — when present — contains no simulator action at all
     (only its "start" record): the loop closed internally.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value
MIN_TESTING_ROUNDS = 2
MIN_DEV_ROUNDS = 2
# drcode default (src/drcode/settings.py, Settings.max_dev_rounds) — the
# denominator requeue_failed_fix puts into the event text.
MAX_DEV_ROUNDS = 3
# Exact wording of TaskManager.requeue_failed_fix (drcode 18b48f9). The
# counter is incremented BEFORE the event is composed, and the number is
# the UPCOMING development round: the brief itself is round 1, so the
# FIRST fix-loop requeue reads "round 2/3" — the persisted proof that
# fix_rounds reached 1. (The final JSON reads fix_rounds == 0: the PASSED
# verdict resets the counter, set_verification — asserting 1 on the
# completed task would contradict drcode's reset-on-success.)
REQUEUE_EVENT = (
    f"testing failed — returned for another development round (round 2/{MAX_DEV_ROUNDS})"
)
COMPACTION_SUMMARY_PREFIX = "[context summary]"


def load_scenario() -> dict:
    toml = Path(__file__).resolve().parent / "scenario.toml"
    return tomllib.loads(toml.read_text(encoding="utf-8"))


def user_prompts(messages: list) -> list[str]:
    """Verbatim user prompts of a serialized coder transcript (the same
    extraction drcode.transcript.all_user_prompts uses, inlined so this
    check stays dependency-free). Each prompt is one development round's
    input: the brief, then the tester's fix-loop report."""
    out = []
    for msg in messages:
        if msg.get("kind") != "request" and msg.get("role") != "request":
            continue
        for part in msg.get("parts", []):
            if part.get("part_kind") != "user-prompt":
                continue
            content = part.get("content")
            if isinstance(content, str) and content.strip():
                text = content.strip()
                if text.startswith(COMPACTION_SUMMARY_PREFIX):
                    continue
                out.append(text)
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    scenario = load_scenario()
    failures: list[str] = []

    # 1. The seed contract: pytest is green in the workspace after the
    #    second development round repaired the regression.
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

    # 2./3. Fix-loop assertions over the persisted task JSON.
    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(tasks_dir.glob("*.json"))]
    brief_titles = [b["title"] for b in scenario.get("briefs", [])]
    briefs = [t for t in tasks if t.get("title") in brief_titles]
    if not briefs:
        failures.append(f"no brief task among {brief_titles} in .drcode/tasks/")

    for t in briefs:
        tid = t.get("id")
        if t.get("status") != "completed":
            failures.append(f"task {tid}: status={t.get('status')!r}, expected 'completed'")
        if t.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"task {tid}: verification={t.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r}"
            )

        # The fix loop really fired: the requeue event with the exact
        # wording of requeue_failed_fix — "round 2/3", the persisted proof
        # that fix_rounds was 1 when the task returned to development.
        events = [str(e.get("text", "")) for e in t.get("events") or []]
        requeues = [e for e in events if e == REQUEUE_EVENT]
        if len(requeues) != 1:
            failures.append(
                f"task {tid}: fix-loop requeue event found {len(requeues)} times in "
                f"events, expected exactly 1 (event: {REQUEUE_EVENT!r})"
            )
        # Reset-on-success: the PASSED verdict zeroes fix_rounds before
        # COMPLETED (set_verification) — a non-zero value here would mean
        # the final verdict was NOT a pass.
        if t.get("fix_rounds") != 0:
            failures.append(
                f"task {tid}: fix_rounds={t.get('fix_rounds')!r}, expected 0 "
                "(the final PASSED verdict resets the counter)"
            )

        rounds = len(t.get("tester_messages") or [])
        if rounds < MIN_TESTING_ROUNDS:
            failures.append(
                f"task {tid}: {rounds} testing rounds, expected >= {MIN_TESTING_ROUNDS} "
                "(the round after the fix-loop requeue is missing)"
            )
        dev_rounds = len(user_prompts(t.get("messages") or []))
        if dev_rounds < MIN_DEV_ROUNDS:
            failures.append(
                f"task {tid}: {dev_rounds} development rounds (user prompts), "
                f"expected >= {MIN_DEV_ROUNDS} (the tester's report must reach "
                "the coder as the task's next input)"
            )

    # 4. Zero user interventions (when the artifact is next to the
    #    workspace): the loop must have closed without the simulator.
    user_sim = workspace.parent / "user_sim.jsonl"
    if user_sim.is_file():
        actions = []
        for line in user_sim.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                actions.append(str(rec.get("action")))
        interventions = [a for a in actions if a != "start"]
        if interventions:
            failures.append(
                f"user_sim.jsonl contains non-start actions {interventions} — "
                "the fix loop must close WITHOUT user interventions"
            )

    if failures:
        print("S8 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S8 checks: green (pytest passed, brief task PASSED after the fix "
        f"loop: requeue event '{REQUEUE_EVENT}', "
        f">= {MIN_TESTING_ROUNDS} testing / >= {MIN_DEV_ROUNDS} development "
        "rounds, zero user interventions)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
