"""Mechanical correctness check of the s3_compaction_coder scenario
(plan §7, stage 4 of §12).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:
  1. pytest is run in the workspace by the harness itself;
  2. the persisted task JSON must show that the compaction really
     happened on the small coding context (§1.2: max_context_tokens of
     the CODING model ≈ 5000 from the scenario's [context] section):
       - a "Context compacted" event in `events`;
       - a compaction start event (mid-run pause or turn-boundary gate);
       - a synthetic user prompt with COMPACTION_SUMMARY_PREFIX in
         `messages`;
       - the ORIGINAL user prompt (the brief) kept verbatim;
       - task COMPLETED with verification=PASSED.
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
COMPACTED_NEEDLE = "Context compacted"
START_NEEDLES = (
    "pausing the run to compact history",  # mid-run (§1.2)
    "pausing the agent and compacting history",  # turn boundary
)


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

    # 2. The S3 assertions over the persisted task JSON.
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
            failures.append(f"task {tid}: status={t.get('status')!r}, expected 'completed'")
        if t.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"task {tid}: verification={t.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r}"
            )

        events = [str(e.get("text", "")) for e in t.get("events") or []]
        if not any(COMPACTED_NEEDLE in e for e in events):
            failures.append(
                f"task {tid}: no {COMPACTED_NEEDLE!r} event — compaction did "
                "not happen on the small coding context"
            )
        starts = [e for e in events if any(n in e for n in START_NEEDLES)]
        if not starts:
            failures.append(
                f"task {tid}: no compaction start event (expected one of "
                f"{START_NEEDLES})"
            )
        elif any("pausing the run" in e for e in starts):
            notes.append(
                f"task {tid}: mid-run path taken (pause → sanitized_messages "
                "→ summary → continuation turn, §1.2)"
            )
        else:
            notes.append(f"task {tid}: turn-boundary compaction path taken")

        messages = t.get("messages") or []
        prompts = []
        for msg in messages:
            for part in msg.get("parts") or []:
                if (
                    isinstance(part, dict)
                    and part.get("part_kind") == "user-prompt"
                    and isinstance(part.get("content"), str)
                ):
                    prompts.append(part["content"])
        summaries = [p for p in prompts if p.startswith(COMPACTION_SUMMARY_PREFIX)]
        if not summaries:
            failures.append(
                f"task {tid}: no {COMPACTION_SUMMARY_PREFIX!r} prompt in "
                "`messages` — the summary never reached the transcript"
            )
        original = next(
            (p for p in prompts if "найдите модуль термина" in p and not p.startswith(COMPACTION_SUMMARY_PREFIX)),
            None,
        )
        if original is None:
            failures.append(
                f"task {tid}: the original user prompt did not survive the "
                "compaction verbatim (§1.4)"
            )
        if not (t.get("tester_messages") or []):
            failures.append(f"task {tid}: task completed without any testing round")

    if failures:
        print("S3 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print("S3 checks: green (pytest passed, feature COMPLETED/PASSED, "
          "compaction event + summary prompt + verbatim original prompt)")
    for n in notes:
        print(f"- {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
