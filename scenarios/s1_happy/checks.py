"""Mechanical correctness check of the s1_happy scenario (plan §7).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:
  1. pytest is run in the workspace by the harness itself;
  2. the task JSON in <workspace>/.drcode/tasks/ must show the happy
     path actually happened: a COMPLETED feature task with
     verification=PASSED and EXACTLY ONE testing round (S1 assertions).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    failures: list[str] = []

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

    # 2. The S1 assertions over the persisted task JSON.
    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = []
    for f in sorted(tasks_dir.glob("*.json")):
        tasks.append(json.loads(f.read_text(encoding="utf-8")))
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
        rounds = len(t.get("tester_messages") or [])
        if rounds != 1:
            failures.append(f"task {tid}: {rounds} testing rounds, expected exactly 1")

    if failures:
        print("S1 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print("S1 checks: green (pytest passed, feature COMPLETED, PASSED, 1 round)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
