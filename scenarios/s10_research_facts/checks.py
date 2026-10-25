"""Mechanical correctness check of s10_research_facts (plan §7; the
research scenario, variant V2 — facts found by reading the code).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. docs/findings.md exists and answers ALL THREE planted facts by
     their CODE identifiers: per fact, the file path AND the symbol
     name must appear as case-insensitive substrings. The seed is
     built so the identifiers are unambiguous (grep yields no false
     matches, see scenario.toml) — the agent must quote them verbatim,
     a paraphrase of names is impossible; three facts at once guard
     against "one lucky grep line".
  2. The facts themselves are RECOMPUTED from the workspace source
     (the seed is the single source of truth — nothing is hardcoded
     twice, the same contract as s9): the orphan constant really has
     exactly one occurrence in *.py (its own definition), the
     duplicated name really has exactly two definitions, the flag
     really has exactly one definition and one usage file (three
     occurrences: definition, import, condition). The
     research agent cannot edit source (drcode research.md write
     limit) — a drifted seed fails here loudly instead of passing.
  3. The task JSON in <workspace>/.drcode/tasks/ shows the research
     contract: EXACTLY ONE task kind=research, status=completed, ZERO
     testing rounds (research skips the tester, plan §7) and no
     verification label (research ends with mark_done — there is
     nothing to verify).
  4. The stricter git check: `git log -- docs/findings.md` is
     non-empty, i.e. the research agent's mandatory git_commit_docs
     really committed the findings (the workspace is a git repo with
     a seed commit, bench/env_setup.py; the brief told the agent to
     create the file with write_file so it lands in
     task.edited_files and is committable). If git itself is
     unavailable the check is skipped — a report committed by no
     means is caught by (3)'s event trail in the diagnostics instead.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

# Per fact: (description, required needles) — file path AND symbol name,
# matched as case-insensitive substrings over docs/findings.md.
FACT_NEEDLES: list[tuple[str, tuple[str, ...]]] = [
    (
        "orphan constant",
        ("parcel_volume_limit_l", "rates.py"),
    ),
    (
        "functions with the same name in different modules",
        ("totals.py", "summary.py", "balance"),
    ),
    (
        "deprecated flag usage",
        ("detailed_ledger", "render.py"),
    ),
]

ORPHAN = "PARCEL_VOLUME_LIMIT_L"
DUP_DEF_RE = re.compile(r"^def balance\b", re.MULTILINE)
FLAG = "DETAILED_LEDGER"
FLAG_DEF_RE = re.compile(r"^DETAILED_LEDGER\s*=", re.MULTILINE)


def _py_sources(workspace: Path) -> list[Path]:
    return [p for p in workspace.rglob("*.py") if ".drcode" not in p.parts]


def _seed_facts(workspace: Path) -> tuple[int, int, int, int] | None:
    """Recompute the planted facts from the workspace source:
    (orphan occurrences, duplicate definitions, flag occurrences,
    flag definitions). None when the source tree itself is broken."""
    orphan = dup = flag = flag_def = 0
    for p in _py_sources(workspace):
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            return None
        orphan += text.count(ORPHAN)
        dup += len(DUP_DEF_RE.findall(text))
        flag += text.count(FLAG)
        flag_def += len(FLAG_DEF_RE.findall(text))
    return orphan, dup, flag, flag_def


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    failures: list[str] = []

    # 2 (first: a drifted seed invalidates everything below).
    facts = _seed_facts(workspace)
    if facts is None or not any(facts):
        print(f"S10 checks FAILED:\n- seed source unreadable in {workspace}")
        return 1
    orphan, dup, flag, flag_def = facts
    if orphan != 1:
        failures.append(
            f"seed drift: {ORPHAN} occurs {orphan}x in *.py, expected exactly 1 "
            "(its own definition — a second occurrence would mean the constant "
            "is no longer an orphan)"
        )
    if dup != 2:
        failures.append(
            f"seed drift: 'def balance' found {dup}x, expected exactly 2 "
            "(one definition per module)"
        )
    if flag_def != 1:
        failures.append(f"seed drift: {FLAG} defined {flag_def}x, expected exactly 1")
    if flag != 3:
        failures.append(
            f"seed drift: {FLAG} occurs {flag}x in *.py, expected exactly 3 "
            "(definition + two references at the single usage site: "
            "the import line and the condition)"
        )

    # 1. docs/findings.md: every fact answered by its code identifiers.
    findings = workspace / "docs" / "findings.md"
    if not findings.is_file():
        failures.append("docs/findings.md is missing in the workspace")
    else:
        lowered = findings.read_text(encoding="utf-8").lower()
        for description, needles in FACT_NEEDLES:
            missing = [n for n in needles if n not in lowered]
            if missing:
                failures.append(
                    f"docs/findings.md does not answer the fact "
                    f"({description}): missing identifier(s) {missing} "
                    "(file path AND symbol name must appear verbatim, "
                    "case-insensitive)"
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

    # 4. The stricter git check: git_commit_docs committed the findings.
    if findings.is_file():
        git_run = subprocess.run(
            ["git", "log", "--", "docs/findings.md"],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=False,
        )
        if git_run.returncode != 0:
            print(f"S10 checks: git log skipped ({git_run.stderr.strip()})")
        elif not git_run.stdout.strip():
            failures.append(
                "git log -- docs/findings.md is empty — the findings were not "
                "committed by git_commit_docs (the documentation assignment "
                "must end with the agent committing its own changes)"
            )

    if failures:
        print("S10 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S10 checks: green (docs/findings.md names all three planted facts "
        "by file+symbol, seed facts recomputed from source: orphan "
        f"{ORPHAN}=1x, def balance=2x, {FLAG}=def+1 usage file, research task "
        "COMPLETED with 0 testing rounds, findings committed)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
