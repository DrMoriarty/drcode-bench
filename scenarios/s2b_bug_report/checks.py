"""Mechanical correctness check of s2b_bug_report (plan drcode-bench.md §7).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. pytest is green in the workspace — the tester's bug report was really
     fixed and the second brief was really implemented;
  2. exactly ONE task has kind=bug and it is NOT one of the briefs — it is
     the tester's own create_bug_report;
  3. the bug task is COMPLETED with verification=PASSED — it went through
     its own testing round;
  4. the bug task was ACTIVATED before the other queued briefs
     (by activated_at): bugs sort to the head of TaskManager.queued(),
     so the tester's report must jump ahead of the second brief even
     though the briefs were created first;
  5. every task is COMPLETED at the end.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value


def load_scenario() -> dict:
    toml = Path(__file__).resolve().parent / "scenario.toml"
    return tomllib.loads(toml.read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    scenario = load_scenario()
    failures: list[str] = []

    # 1. The seed contract: the whole suite is green at the end.
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

    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(tasks_dir.glob("*.json"))]
    brief_titles = [b["title"] for b in scenario.get("briefs", [])]
    briefs = [t for t in tasks if t.get("title") in brief_titles]
    if len(briefs) != len(brief_titles):
        failures.append(
            f"expected {len(brief_titles)} brief tasks in .drcode/tasks/, found {len(briefs)}"
        )

    # 2. Exactly one kind=bug task, and it is the tester's report (not a brief).
    #    Even when the count is off, checks 3/4 still run on the best
    #    candidate for the tester's report (title outside the briefs; among
    #    several — the earliest created), so one checks.py run reports ALL
    #    violations instead of stopping at the count failure.
    bugs = [t for t in tasks if t.get("kind") == "bug"]
    if len(bugs) != 1:
        failures.append(
            f"expected exactly 1 kind=bug task (the tester's report), found {len(bugs)}"
        )
    candidates = [t for t in bugs if t.get("title") not in brief_titles]
    if candidates:
        bug = min(candidates, key=lambda t: str(t.get("created_at") or ""))
    elif bugs:
        bug = min(bugs, key=lambda t: str(t.get("created_at") or ""))
    else:
        bug = None
    if len(bugs) == 1 and bug is not None and bug.get("title") in brief_titles:
        failures.append("the kind=bug task is a brief — expected the tester's own report")

    # 5. Everything COMPLETED.
    for t in tasks:
        if t.get("status") != "completed":
            failures.append(
                f"task {t.get('id')} ({t.get('title')!r}): status={t.get('status')!r}, expected 'completed'"
            )

    if bug is not None:
        # 3. The bug task passed its own testing round.
        if bug.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"bug task {bug.get('id')}: verification={bug.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r} (it must pass testing)"
            )
        if not bug.get("tester_messages"):
            failures.append(f"bug task {bug.get('id')}: no testing rounds at all")
        # 4. Queue priority: the bug task was activated BEFORE every other
        #    queued brief (by activated_at), even though the briefs were
        #    created earlier. The ONLY exception is the earliest-activated
        #    brief — the one that was in development when the tester filed
        #    the report (its testing produced the bug task).
        bug_activated = bug.get("activated_at")
        if not bug_activated:
            failures.append("bug task has no activated_at (was never activated)")
        else:
            started = sorted(
                (t for t in briefs if t.get("activated_at")),
                key=lambda t: t["activated_at"],
            )
            for other in started[1:]:
                if other["activated_at"] < bug_activated:
                    failures.append(
                        f"queue priority broken: brief {other.get('title')!r} was activated "
                        f"({other['activated_at']}) BEFORE the bug report ({bug_activated})"
                    )

    if failures:
        print("S2b checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S2b checks: green (pytest passed, tester's bug report completed+PASSED "
        "and activated before the queued briefs)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
