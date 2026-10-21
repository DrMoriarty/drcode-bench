"""Mechanical correctness check of s2a_bug_followup (plan drcode-bench.md §7).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. pytest is run in the workspace by the harness itself — the follow-up
     round must have left the seed contract green;
  2. the brief task must show the S2a path in its persisted JSON:
     COMPLETED, verification=PASSED, at least 2 testing rounds (the first
     round failed, the follow-up round passed);
  3. the follow-up comment must be visible in the CODER transcript as
     exactly ONE user prompt — no duplicates (the send()/is_pending_retry
     dedupe of drcode must have swallowed any double-send).
"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value
MIN_ROUNDS = 2
COMPACTION_SUMMARY_PREFIX = "[context summary]"


def load_scenario() -> dict:
    toml = Path(__file__).resolve().parent / "scenario.toml"
    return tomllib.loads(toml.read_text(encoding="utf-8"))


def user_prompts(messages: list) -> list[str]:
    """Verbatim user prompts of a serialized coder transcript (the same
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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    scenario = load_scenario()
    failures: list[str] = []

    # 1. The seed contract: pytest is green in the workspace after the
    #    follow-up round.
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

    # 2./3. S2a assertions over the persisted task JSON.
    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(tasks_dir.glob("*.json"))]
    brief_titles = [b["title"] for b in scenario.get("briefs", [])]
    briefs = [t for t in tasks if t.get("title") in brief_titles]
    if not briefs:
        failures.append(f"no brief task among {brief_titles} in .drcode/tasks/")

    followup_marker = str(scenario["followups"][0]["text"]).strip().splitlines()[0].strip()

    for t in briefs:
        tid = t.get("id")
        if t.get("status") != "completed":
            failures.append(f"task {tid}: status={t.get('status')!r}, expected 'completed'")
        if t.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"task {tid}: verification={t.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r}"
            )
        rounds = len(t.get("tester_messages") or [])
        if rounds < MIN_ROUNDS:
            failures.append(
                f"task {tid}: {rounds} testing rounds, expected >= {MIN_ROUNDS} "
                "(the follow-up round is missing)"
            )

        # 3. The follow-up reached the coder as exactly ONE prompt.
        prompts = user_prompts(t.get("messages") or [])
        hits = [p for p in prompts if followup_marker in p]
        if len(hits) != 1:
            failures.append(
                f"task {tid}: follow-up marker found {len(hits)} times in the coder "
                f"transcript prompts, expected exactly 1 (marker: {followup_marker!r})"
            )

    if failures:
        print("S2a checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S2a checks: green (pytest passed, brief task PASSED with "
        f">= {MIN_ROUNDS} rounds, follow-up seen once as one prompt)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
