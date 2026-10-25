"""Mechanical correctness check of s12_research_bug_report (plan §7; the
research scenario, variant V4 — the defect FOUND BY READING becomes a
task that runs the FULL coding → testing pipeline).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. pytest is run in the workspace by the harness itself: the seed
     suite was green BEFORE the run (the latent defect is outside the
     tests' coverage — that is the scenario's premise) and the coder's
     fix of the spawned bug must have kept it green;
  2. the seed linkage: dispatch/pricing.py exists in the workspace and
     still defines batches_needed — the needles below are tied to the
     seed the brief pointed at, so a drifted seed fails here loudly;
  3. the task JSON in <workspace>/.drcode/tasks/ shows BOTH contracts:
     - EXACTLY ONE task kind=research (the brief): COMPLETED, ZERO
       testing rounds, no verification label (research ends with
       mark_done, plan §7);
     - EXACTLY ONE task kind=bug that is NOT one of the briefs. A
       kind=bug task of non-brief origin can only be the
       origin="system" product of the research agent's
       create_bug_report tool: the harness queues the briefs and the
       user simulator (§6) only comments on existing tasks — neither
       creates bug tasks. The tool call itself is proven in (4);
     - the bug task is COMPLETED with verification=PASSED and at least
       one testing round — the FULL pipeline ran on the spawned bug;
  4. the research → bug chain is mechanical, not circumstantial: the
     research transcript contains EXACTLY ONE create_bug_report tool
     call, its arguments match the bug task's title/description, and
     the description carries the code identifiers — the defective
     module's file path AND the defective function name (case-
     insensitive substrings; the agent quotes identifiers verbatim, a
     paraphrase is impossible).
"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value
COMPACTION_SUMMARY_PREFIX = "[context summary]"

# The defective module/function of the seed (the brief names only the
# module — the function name must come from the agent's own reading).
DEFECT_MODULE = "dispatch/pricing.py"
DEFECT_FUNCTION = "batches_needed"


def load_scenario() -> dict:
    toml = Path(__file__).resolve().parent / "scenario.toml"
    return tomllib.loads(toml.read_text(encoding="utf-8"))


def user_prompts(messages: list) -> list[str]:
    """Verbatim user prompts of a serialized transcript (the same
    extraction drcode.transcript.all_user_prompts uses, inlined so this
    check stays dependency-free)."""
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


def tool_calls(messages: list) -> list[tuple[str, dict]]:
    """(tool_name, arguments) of every tool call in a serialized
    transcript. `args` arrives as the JSON string pydantic-ai persists
    (a dict is tolerated for symmetry)."""
    out = []
    for msg in messages:
        if msg.get("kind") == "request" or msg.get("role") == "request":
            continue
        for part in msg.get("parts", []):
            if part.get("part_kind") != "tool-call":
                continue
            raw = part.get("args")
            if isinstance(raw, str):
                try:
                    args = json.loads(raw)
                except json.JSONDecodeError:
                    args = {}
            elif isinstance(raw, dict):
                args = raw
            else:
                args = {}
            out.append((str(part.get("tool_name")), args))
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    scenario = load_scenario()
    failures: list[str] = []

    # 1. The seed contract holds after the fix: pytest is green in the
    #    workspace.
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

    # 2. Seed linkage: the defective module is where the brief pointed
    #    and still defines the defective function (a drifted seed
    #    invalidates the needles below).
    pricing = workspace / "dispatch" / "pricing.py"
    if not pricing.is_file():
        failures.append(f"seed drift: {DEFECT_MODULE} is missing in the workspace")
    elif f"def {DEFECT_FUNCTION}" not in pricing.read_text(encoding="utf-8"):
        failures.append(f"seed drift: def {DEFECT_FUNCTION} not found in {DEFECT_MODULE}")

    # 3. The task contracts over the persisted task JSON.
    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(tasks_dir.glob("*.json"))]
    brief_titles = [b["title"] for b in scenario.get("briefs", [])]

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

    # The spawned bug: kind=bug, NOT a brief (the briefs are research) —
    # hence created by the research agent's create_bug_report tool
    # (origin="system", see the docstring).
    bugs = [t for t in tasks if t.get("kind") == "bug" and t.get("title") not in brief_titles]
    if len(bugs) != 1:
        failures.append(
            f"expected exactly 1 non-brief task with kind=bug "
            f"(the research agent's create_bug_report product), found {len(bugs)}"
        )
    bug_description = ""
    for t in bugs:
        tid = t.get("id")
        if t.get("status") != "completed":
            failures.append(f"bug task {tid}: status={t.get('status')!r}, expected 'completed'")
        if t.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"bug task {tid}: verification={t.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r} (the spawned bug must pass testing)"
            )
        rounds = len(t.get("tester_messages") or [])
        if rounds < 1:
            failures.append(
                f"bug task {tid}: {rounds} testing rounds, expected >= 1 "
                "(the spawned bug must run the FULL coding → testing pipeline)"
            )
        prompts = user_prompts(t.get("messages") or [])
        if not prompts:
            failures.append(f"bug task {tid}: no user prompts in the coder transcript")
            continue
        # The task description (the report text) is the bug task's first
        # prompt — the needles go against IT, not the coder's later work.
        bug_description = prompts[0]
        lowered = bug_description.lower()
        for needle in (DEFECT_MODULE, DEFECT_FUNCTION):
            if needle not in lowered:
                failures.append(
                    f"bug task {tid}: description does not name the defect's code "
                    f"identifiers — {needle!r} missing; the report must cite the "
                    "file path AND the function name verbatim"
                )

    # 4. The research → bug chain: the research transcript filed the
    #    report itself, exactly once, with the matching text.
    if research:
        calls = [
            args
            for name, args in tool_calls(research[0].get("messages") or [])
            if name == "create_bug_report"
        ]
        if len(calls) != 1:
            failures.append(
                f"research transcript: create_bug_report called {len(calls)} times, "
                "expected exactly 1 (the brief authorizes ONE report for the ONE "
                "latent defect)"
            )
        elif bugs:
            args = calls[0]
            # create() strips the message text; compare the same way.
            if str(args.get("title", "")).strip() != bugs[0].get("title"):
                failures.append(
                    "research transcript: create_bug_report title "
                    f"{args.get('title')!r} does not match the bug task title "
                    f"{bugs[0].get('title')!r}"
                )
            if str(args.get("description", "")).strip() != bug_description:
                failures.append(
                    "research transcript: create_bug_report description does not "
                    "match the bug task's first prompt — the bug task was not "
                    "created from THIS tool call"
                )

    if failures:
        print("S12 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S12 checks: green (pytest passed, research task COMPLETED with 0 testing "
        "rounds, its create_bug_report spawned the kind=bug task that completed "
        "PASSED with a testing round; description names "
        f"{DEFECT_MODULE} / {DEFECT_FUNCTION})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
