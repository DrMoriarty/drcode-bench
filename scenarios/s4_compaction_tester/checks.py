"""Mechanical correctness check of the s4_compaction_tester scenario
(plan §7, stage 4 of §12).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:
  1. pytest is run in the workspace by the harness itself;
  2. the persisted task JSON must show the mid-round compaction of the
     tester really happened (§1.2, drcode ≥ 0.5.0: the tester's threshold
     is computed from the TESTER model's own config — the source itself is
     classified in metrics.json, `tester_threshold_from_tester`; a
     'coding' source would be a regression to the pre-0.5.0 behavior):
       - a tester-phase compaction start event in `events`
         ("compacting the testing round" / "pausing the tester round…");
       - the success event ("testing round summarized");
       - `tester_messages[-1]` contains a COMPACTION_SUMMARY_PREFIX
         prompt (the round was rewritten in place);
       - a verdict was set (verification is not None) and the task is
         COMPLETED (PASSED — the followup must not have been needed).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value
# drcode/src/drcode/transcript.py (asserted against the source in
# tests/test_metrics.py) — hardcoded to keep this check standalone.
COMPACTION_SUMMARY_PREFIX = "[context summary]"
TESTER_START_NEEDLES = (
    "compacting the testing round",  # mid-round gate
    "pausing the tester round to compact history",
)
TESTER_SUCCESS_NEEDLE = "testing round summarized"


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

    # 2. The S4 assertions over the persisted task JSON.
    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = [
        json.loads(f.read_text(encoding="utf-8"))
        for f in sorted(tasks_dir.glob("*.json"))
    ]
    targets = [t for t in tasks if t.get("kind") == "bug"]
    if not targets:
        failures.append("no task with kind=bug in .drcode/tasks/")
    for t in targets:
        tid = t.get("id")
        if t.get("status") != "completed":
            failures.append(f"task {tid}: status={t.get('status')!r}, expected 'completed'")
        if t.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"task {tid}: verification={t.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r} (verdict must be set "
                "and positive)"
            )

        events = [str(e.get("text", "")) for e in t.get("events") or []]
        starts = [e for e in events if any(n in e for n in TESTER_START_NEEDLES)]
        if not starts:
            failures.append(
                f"task {tid}: no tester-phase compaction start event "
                f"(expected one of {TESTER_START_NEEDLES}) — the testing "
                "round never hit the compaction threshold"
            )
        if not any(TESTER_SUCCESS_NEEDLE in e for e in events):
            failures.append(
                f"task {tid}: no {TESTER_SUCCESS_NEEDLE!r} event — the "
                "tester compaction never succeeded"
            )

        rounds = t.get("tester_messages") or []
        if not rounds:
            failures.append(f"task {tid}: no testing rounds at all")
            continue
        last = rounds[-1]
        last_prompts = [
            part["content"]
            for msg in last
            for part in (msg.get("parts") or [])
            if isinstance(part, dict)
            and part.get("part_kind") == "user-prompt"
            and isinstance(part.get("content"), str)
        ]
        if not any(p.startswith(COMPACTION_SUMMARY_PREFIX) for p in last_prompts):
            failures.append(
                f"task {tid}: tester_messages[-1] contains no "
                f"{COMPACTION_SUMMARY_PREFIX!r} prompt — the last round was "
                "not rewritten by the mid-round compaction"
            )
        # The summarized round must have continued and produced responses
        # after the summary (continuation-turn, §1.2).
        summary_seen = False
        responses_after = 0
        for msg in last:
            for part in msg.get("parts") or []:
                if (
                    isinstance(part, dict)
                    and part.get("part_kind") == "user-prompt"
                    and isinstance(part.get("content"), str)
                    and part["content"].startswith(COMPACTION_SUMMARY_PREFIX)
                ):
                    summary_seen = True
            if summary_seen and msg.get("kind") == "response":
                responses_after += 1
        if summary_seen and responses_after == 0:
            notes.append(
                f"task {tid}: WARNING — no model response after the round "
                "summary (round may have ended right at the compaction)"
            )
        notes.append(
            f"task {tid}: {len(rounds)} testing round(s), summary inside "
            "the last round"
        )

    if failures:
        print("S4 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print("S4 checks: green (pytest passed, bug COMPLETED/PASSED, "
          "tester mid-round compaction + summary in the last round)")
    for n in notes:
        print(f"- {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
