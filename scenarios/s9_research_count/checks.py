"""Mechanical correctness check of s9_research_count (plan §7; the first
research scenario — variant V1).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. the reference value is RECOMPUTED from the seed CSV in the
     workspace itself (sum of `amount` over `status == "completed"`) —
     the seed and the check cannot drift apart, nothing is hardcoded
     in two places;
  2. docs/report.md exists and contains the pinned output format: a
     line exactly "total: <number>" (anchored regex ^total: N$ over a
     single line — no currency, no thousand separators, no prose on
     that line), matching the recomputed reference EXACTLY;
  3. the task JSON in <workspace>/.drcode/tasks/ shows the research
     contract: EXACTLY ONE task kind=research, status=completed, ZERO
     testing rounds (research skips the tester, plan §7) and no
     verification label (research ends with mark_done — there is
     nothing to verify);
The verdict is built on checks 1-3 ONLY. The commit discipline of the
research agent (the mandatory git_commit_docs of the drcode research.md
prompt really committed the report) is NOT a verdict condition anymore
— it is a MEASURED metric: this script emits a machine-readable line

    S9 metric: report_committed=true|false

which bench/run_one.py parses out of stdout into result.json
(`checks_metrics`) and the report aggregates into a dedicated
`report_committed` column (§10). The workspace is a git repo with a
seed commit (bench/env_setup.py) and the brief tells the agent to
create the file with write_file so it lands in task.edited_files and
is committable; when git itself is unavailable the metric line is
omitted entirely (the harness reads None — "unknown", not "false").
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

TOTAL_LINE_RE = re.compile(r"^total: (\d+)$", re.MULTILINE)


def expected_total(orders_csv: Path) -> int:
    """Recompute the reference metric from the seed data: the sum of the
    `amount` column over the rows with status == "completed"."""
    with orders_csv.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return sum(int(r["amount"]) for r in rows if r["status"] == "completed")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    failures: list[str] = []

    # 1. Recompute the reference from the seed (the seed is the single
    #    source of truth — never duplicated as a literal here).
    orders_csv = workspace / "data" / "orders.csv"
    if not orders_csv.is_file():
        print(f"S9 checks FAILED:\n- seed data file missing: {orders_csv}")
        return 1
    reference = expected_total(orders_csv)

    # 2. docs/report.md: the pinned "total: N" line, exactly once, and
    #    the number must equal the recomputed reference.
    report = workspace / "docs" / "report.md"
    if not report.is_file():
        failures.append("docs/report.md is missing in the workspace")
    else:
        text = report.read_text(encoding="utf-8")
        totals = TOTAL_LINE_RE.findall(text)
        if len(totals) != 1:
            failures.append(
                f"docs/report.md must contain exactly one line 'total: <number>' "
                f"(anchored regex ^total: N$), found {len(totals)}: {totals!r}"
            )
        elif int(totals[0]) != reference:
            failures.append(
                f"docs/report.md: total={totals[0]}, expected {reference} "
                "(recomputed from data/orders.csv: sum of amount where "
                "status == 'completed')"
            )

    # 3. The research contract over the persisted task JSON.
    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(tasks_dir.glob("*.json"))]
    research = [t for t in tasks if t.get("kind") == "research"]
    if len(research) != 1:
        failures.append(
            f"expected exactly 1 task with kind=research in .drcode/tasks/, found {len(research)}"
        )
    for t in research:
        tid = t.get("id")
        if t.get("status") != "completed":
            failures.append(f"task {tid}: status={t.get('status')!r}, expected 'completed'")
        rounds = len(t.get("tester_messages") or [])
        if rounds != 0:
            failures.append(
                f"task {tid}: {rounds} testing rounds, expected 0 "
                "(research tasks skip the tester, plan §7)"
            )
        if t.get("verification") is not None:
            failures.append(
                f"task {tid}: verification={t.get('verification')!r}, expected None "
                "(research ends with mark_done and never gets a verdict label)"
            )

    # 4. NOT a verdict condition: the commit discipline is measured and
    #    emitted as a machine-readable metric line (see the docstring).
    #    bench/run_one.py parses `S9 metric: key=value` out of stdout —
    #    for any other scenario that means zero changes here.
    if report.is_file():
        git_run = subprocess.run(
            ["git", "log", "--", "docs/report.md"],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=False,
        )
        if git_run.returncode != 0:
            # git itself is unavailable: no metric line at all — the
            # harness reads None ("unknown"), never a false positive.
            print(f"S9 checks: git log skipped ({git_run.stderr.strip()})")
        else:
            committed = bool(git_run.stdout.strip())
            print(f"S9 metric: report_committed={'true' if committed else 'false'}")

    if failures:
        print("S9 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S9 checks: green (docs/report.md carries total: "
        f"{reference} — recomputed from data/orders.csv, research task "
        "COMPLETED with 0 testing rounds)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
