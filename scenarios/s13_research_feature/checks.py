"""Mechanical correctness check of s13_research_feature (plan §7; the
research scenario, variant V5 and the HEAVIEST one: the compound
research → planning → coding → testing chain).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. pytest is run in the workspace by the harness itself: the seed
     suite was green BEFORE the run and the replacement (a
     behavior-preserving refactor, readings are non-negative) must
     keep it green;
  2. the REFERENCE change-site list is RECOMPUTED from the scenario's
     own seed directory (NOT from the workspace — the coder has
     already touched the workspace copy, so it can no longer serve as
     the source of truth): every file carrying the deprecated token
     must be one of the telemetry modules, exactly one occurrence per
     file (no stray docstring/comment mentions). A drifted seed fails
     here loudly instead of passing — and it pins the «canonical list
     is exactly N and unambiguous» premise the whole scenario rests on;
  3. the task JSON in <workspace>/.drcode/tasks/ shows BOTH contracts:
     - EXACTLY ONE task kind=research (the brief): COMPLETED, ZERO
       testing rounds, no verification label (research ends with
       mark_done, plan §7);
     - EXACTLY ONE task kind=feature that is NOT one of the briefs. A
       kind=feature task of non-brief origin can only be the
       origin="system" product of the research agent's
       create_feature_request tool (TaskManager.create — the tool is
       the only non-user source of kind=feature tasks; the harness
       queues the briefs, the user simulator (§6) only comments on
       existing tasks): COMPLETED with verification=PASSED and at
       least one testing round — the FULL pipeline ran on the spawned
       feature;
  4. the PLAN is complete: the spawned feature's description (its
     first prompt — the research agent's create_feature_request
     description) contains EVERY expected path as a case-insensitive
     substring. A partial list fails: the plan's point is «all N
     places», not «some places»;
  5. the research → feature chain is mechanical, not circumstantial:
     the research transcript contains EXACTLY ONE create_feature_request
     tool call, and its title/description match the spawned task
     (the description became the task's first prompt);
  6. the compound chain closed: every expected file in the workspace
     no longer carries the deprecated token — the coder actually
     implemented the plan the research agent composed (pytest-green
     alone would pass an inert run, because the replacement is
     behavior-preserving; this check is what makes the implementation
     observable).
"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value
COMPACTION_SUMMARY_PREFIX = "[context summary]"

# The deprecated pattern (the brief names it) and the package the seed
# scopes it to; the canonical change-site list is derived from the seed.
DEPRECATED_TOKEN = "math.floor"
PACKAGE = "telemetry"
EXPECTED_SITE_COUNT = 5  # the N the scenario.toml header promises

SEED_DIR = Path(__file__).resolve().parent / "seed"


def load_scenario() -> dict:
    toml = Path(__file__).resolve().parent / "scenario.toml"
    return tomllib.loads(toml.read_text(encoding="utf-8"))


def reference_sites() -> list[str]:
    """Paths (repo-root-relative, /-separated) of the seed files that
    carry the deprecated token — the canonical list the plan must
    reproduce. The workspace cannot serve as the source (the coder has
    already edited it), so the reference comes from the scenario's own
    untouched seed."""
    return sorted(
        p.relative_to(SEED_DIR).as_posix()
        for p in SEED_DIR.rglob("*.py")
        if DEPRECATED_TOKEN in p.read_text(encoding="utf-8")
    )


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

    # 2. Seed drift guard: the reference list from the untouched seed
    #    must be exactly the N telemetry modules, one token occurrence
    #    per file (a docstring mentioning the token would make the
    #    «grep the token» discovery ambiguous — a sixth place).
    sites = reference_sites()
    if len(sites) != EXPECTED_SITE_COUNT:
        failures.append(
            f"seed drift: {DEPRECATED_TOKEN} appears in {len(sites)} seed files, "
            f"expected exactly {EXPECTED_SITE_COUNT}: {sites}"
        )
    for site in sites:
        if not site.startswith(f"{PACKAGE}/"):
            failures.append(f"seed drift: {site} is outside the {PACKAGE}/ package")
        if SEED_DIR.joinpath(site).read_text(encoding="utf-8").count(DEPRECATED_TOKEN) != 1:
            failures.append(
                f"seed drift: {site} carries {DEPRECATED_TOKEN} more than once — "
                "the canonical site list would be ambiguous"
            )

    # 1. The seed contract holds after the implementation: pytest is
    #    green in the workspace.
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

    # The spawned feature: kind=feature, NOT a brief (the briefs are
    # research) — hence created by the research agent's
    # create_feature_request tool (origin="system", see the docstring).
    features = [t for t in tasks if t.get("kind") == "feature" and t.get("title") not in brief_titles]
    if len(features) != 1:
        failures.append(
            f"expected exactly 1 non-brief task with kind=feature "
            f"(the research agent's create_feature_request product), found {len(features)}"
        )
    feature_description = ""
    for t in features:
        tid = t.get("id")
        if t.get("status") != "completed":
            failures.append(f"feature task {tid}: status={t.get('status')!r}, expected 'completed'")
        if t.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"feature task {tid}: verification={t.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r} (the spawned feature must pass testing)"
            )
        rounds = len(t.get("tester_messages") or [])
        if rounds < 1:
            failures.append(
                f"feature task {tid}: {rounds} testing rounds, expected >= 1 "
                "(the spawned feature must run the FULL coding → testing pipeline)"
            )
        prompts = user_prompts(t.get("messages") or [])
        if not prompts:
            failures.append(f"feature task {tid}: no user prompts in the coder transcript")
            continue
        # The plan (the request text) is the feature task's first prompt
        # — the path needles go against IT, not the coder's later work.
        feature_description = prompts[0]
        lowered = feature_description.lower()
        # 4. The plan is complete: EVERY canonical path is named. A
        #    partial list fails even if the rest of the run is green.
        for site in sites:
            if site.lower() not in lowered:
                failures.append(
                    f"feature task {tid}: the plan does not name the change site "
                    f"{site!r} — the list must cover ALL {len(sites)} places "
                    "(paths from the repository root, case-insensitive substring)"
                )

    # 5. The research → feature chain: the research transcript filed the
    #    request itself, exactly once, with the matching text.
    if research:
        calls = [
            args
            for name, args in tool_calls(research[0].get("messages") or [])
            if name == "create_feature_request"
        ]
        if len(calls) != 1:
            failures.append(
                f"research transcript: create_feature_request called {len(calls)} times, "
                "expected exactly 1 (the brief authorizes ONE request for the "
                "ONE refactor)"
            )
        elif features:
            args = calls[0]
            # create() strips the message text; compare the same way.
            if str(args.get("title", "")).strip() != features[0].get("title"):
                failures.append(
                    "research transcript: create_feature_request title "
                    f"{args.get('title')!r} does not match the feature task title "
                    f"{features[0].get('title')!r}"
                )
            if str(args.get("description", "")).strip() != feature_description:
                failures.append(
                    "research transcript: create_feature_request description does "
                    "not match the feature task's first prompt — the feature task "
                    "was not created from THIS tool call"
                )

    # 6. The compound chain closed: the deprecated token is gone from
    #    every canonical site in the workspace. pytest-green alone would
    #    pass an inert run — the replacement is behavior-preserving, so
    #    the implementation itself must be observable on disk.
    for site in sites:
        ws_file = workspace / site
        if not ws_file.is_file():
            failures.append(f"workspace drift: {site} is missing")
        elif DEPRECATED_TOKEN in ws_file.read_text(encoding="utf-8"):
            failures.append(
                f"workspace: {site} still carries {DEPRECATED_TOKEN} — the spawned "
                "feature was not implemented (the plan's sites must all be migrated)"
            )

    if failures:
        print("S13 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S13 checks: green (pytest passed, research task COMPLETED with 0 testing "
        "rounds, its create_feature_request plan named all "
        f"{len(sites)} change sites, the spawned kind=feature task completed "
        "PASSED with a testing round and the deprecated token is gone from every "
        "listed file)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
