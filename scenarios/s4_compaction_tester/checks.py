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
   3. the listing must have really been SHOWN to the tester: the
      run_bash tool-returns of the testing rounds are mined for
      'entry NNNNNN: …' lines and the shown range must be contiguous,
      end at the file's last line with its exact text. A verdict built
      on a piped read (`sed -n '1,500p' … | tail -5`: 5 lines per
      500-line portion) leaves huge gaps in the shown range and fails
      here even when the verdict itself was word-perfect.

      NOTE on the pre-compaction reads: drcode's in-place round
      compaction (compaction.py `compacted_messages`) keeps only the
      original prompts verbatim plus the summary — the tool-returns
      summarized away are gone from tester_messages, so the literal
      'lines 1..4500 all shown' is provable only for runs that never
      compacted. Hence: without a summary in any round the shown range
      must START at line 1 (a full uncompacted read always does);
      with a summary, only the surviving suffix is verifiable and the
      start line is not demanded.
"""

from __future__ import annotations

import json
import re
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

# The acceptance target (scenario.toml brief): the seed's data/listing.txt
# is 4500 'entry NNNNNN: …' lines; the last one is pinned verbatim.
LISTING_LINES = 4500
LISTING_LAST_LINE = "epsilon payload-38 checksum=35500"
_ENTRY_RE = re.compile(r"^entry (\d{6}): (.*)$")


def shown_listing_lines(tester_messages: list) -> dict[int, str]:
    """Lines of data/listing.txt actually SHOWN to the tester: the
    'entry NNNNNN: …' lines mined from run_bash tool-returns across all
    testing rounds, in transcript order (line number -> shown text)."""
    shown: dict[int, str] = {}
    for rnd in tester_messages:
        for msg in rnd:
            for part in msg.get("parts") or []:
                if not (
                    isinstance(part, dict)
                    and part.get("part_kind") == "tool-return"
                    and part.get("tool_name") == "run_bash"
                ):
                    continue
                for line in str(part.get("content") or "").splitlines():
                    m = _ENTRY_RE.match(line)
                    if m:
                        shown[int(m.group(1))] = m.group(2)
    return shown


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

        # 3. The reading-coverage check: what the tool-returns really showed.
        shown = shown_listing_lines(rounds)
        if not shown:
            failures.append(
                f"task {tid}: no data/listing.txt lines in the tester's "
                "run_bash tool-returns — the listing was never read (the "
                "brief's acceptance requirement)"
            )
        else:
            lo, hi = min(shown), max(shown)
            gaps = [n for n in range(lo, hi + 1) if n not in shown]
            if gaps:
                preview = ", ".join(f"entry {n:06d}" for n in gaps[:8])
                more = "" if len(gaps) <= 8 else f" … (+{len(gaps) - 8} more)"
                failures.append(
                    f"task {tid}: shown listing range {lo}..{hi} has "
                    f"{len(gaps)} gap(s) — portions were filtered/truncated "
                    f"instead of being shown whole (first gaps: {preview}{more})"
                )
            if hi != LISTING_LINES:
                failures.append(
                    f"task {tid}: the last shown listing line is "
                    f"entry {hi:06d}, expected {LISTING_LINES} — the file's "
                    "tail was never shown"
                )
            elif shown[LISTING_LINES] != LISTING_LAST_LINE:
                failures.append(
                    f"task {tid}: the last listing line drifted: "
                    f"entry {LISTING_LINES:06d}: {shown[LISTING_LINES]!r}, "
                    f"expected {LISTING_LAST_LINE!r}"
                )
            if not any(
                isinstance(p, dict)
                and p.get("part_kind") == "user-prompt"
                and isinstance(p.get("content"), str)
                and p["content"].startswith(COMPACTION_SUMMARY_PREFIX)
                for rnd in rounds
                for msg in rnd
                for p in msg.get("parts") or []
            ) and lo != 1:
                # No compaction anywhere → nothing was summarized away → a
                # full sequential read must start at the very first line.
                failures.append(
                    f"task {tid}: no tester compaction, so no read may have "
                    f"been summarized away, yet the first shown listing line "
                    f"is entry {lo:06d}, not entry 000001 — the reading was "
                    "not sequential from the file start"
                )
            notes.append(
                f"task {tid}: listing lines shown {lo}..{hi} "
                f"({hi - lo + 1} of {LISTING_LINES})"
            )

    if failures:
        print("S4 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print("S4 checks: green (pytest passed, bug COMPLETED/PASSED, "
          "tester mid-round compaction + summary in the last round, "
          "listing shown whole to the tester)")
    for n in notes:
        print(f"- {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
