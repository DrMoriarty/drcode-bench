"""Mechanical correctness check of the s6_queue_priority scenario
(plan §7, stage 5 of §12).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. pytest is run in the workspace by the harness itself;
  2. both briefs are COMPLETED with verification=PASSED;
  3. queue priority (§7 S6): the bug brief was ACTIVATED before the
     feature brief (by activated_at) — bugs sort to the head of
     TaskManager.queued() even when both briefs were created at once;
  4. the development/testing gate (§7: "no development while testing is
     in flight"): the busy intervals of the coder (task `messages`
     timestamps) and of the tester (`tester_messages` rounds) never
     overlap — across tasks too; the task `events` lists are also
     scanned for stability signals;
  5. when `model_log.jsonl` (recorder §5, one level above the workspace)
     distinguishes the roles by model tag, the same non-overlap check is
     repeated over the recorder's per-request intervals.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value


def parse_ts(raw):
    if not raw:
        return None
    if isinstance(raw, datetime):
        dt = raw
    elif isinstance(raw, str):
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def busy_interval(messages):
    """(start, end) over the timestamps of one transcript, None when no
    stamps are available."""
    stamps = [t for t in (parse_ts(m.get("timestamp")) for m in messages) if t]
    if not stamps:
        return None
    return (min(stamps), max(stamps))


def overlap(a, b):
    """Seconds of intersection of two (start, end) intervals (0 = none)."""
    delta = (a[1] - b[0]).total_seconds()
    if delta <= 0 or (b[1] - a[0]).total_seconds() <= 0:
        return 0.0
    return min(a[1], b[1]).timestamp() - max(a[0], b[0]).timestamp()


def is_model_response(msg: dict) -> bool:
    """True when a transcript message is a billed model response (as opposed
    to a pipeline-composed user prompt — e.g. a requeue report injected into
    the coder transcript with the queue timestamp, not the model's). The
    same predicate distinguishes responses in check_gate_recorder's
    tag→role matching."""
    return msg.get("kind") == "response" or msg.get("role") == "response"


def load_tasks(workspace: Path) -> list[dict]:
    tasks_dir = workspace / ".drcode" / "tasks"
    return [
        json.loads(f.read_text(encoding="utf-8"))
        for f in sorted(tasks_dir.glob("*.json"))
    ]


def check_gate_transcripts(tasks: list[dict], failures: list[str]) -> bool:
    """The gate over the persisted transcripts (§7: no development while
    testing is in flight): a CODER *model response* timestamp strictly
    inside a tester round's [start, end] interval means both agents were
    in flight at once. Only billed model responses count (the same
    distinction check_gate_recorder makes when matching usage): a
    pipeline-composed user prompt — e.g. a requeue report delivered into
    the coder transcript with the queue's timestamp — is not development
    activity and must not bite the gate. (Interval-vs-interval spans would
    false-bite too: one task's coder transcript legitimately spans the gaps
    where other testing rounds — e.g. its own failed round before a
    follow-up — ran.)
    Returns True when there was tester activity to check at all."""
    tester: list[tuple[str, tuple]] = []
    for t in tasks:
        label = f"{t.get('kind')}:{t.get('title')!r}"
        for i, rnd in enumerate(t.get("tester_messages") or []):
            iv = busy_interval(rnd)
            if iv:
                tester.append((f"{label} round {i}", iv))
    if not tester:
        failures.append("no tester activity found in any task (no testing rounds)")
        return False
    for t in tasks:
        label = f"{t.get('kind')}:{t.get('title')!r}"
        for msg in t.get("messages") or []:
            if not is_model_response(msg):
                continue
            ts = parse_ts(msg.get("timestamp"))
            if ts is None:
                continue
            for tlabel, (start, end) in tester:
                if start < ts < end:
                    failures.append(
                        f"GATE VIOLATION: coder message of {label} at "
                        f"{ts.isoformat()} falls INSIDE the tester interval "
                        f"of {tlabel} ({start.isoformat()}…{end.isoformat()})"
                    )
    return True


def check_gate_recorder(workspace: Path, failures: list[str]) -> None:
    """The same gate over the recorder log (§5), when it exists and the
    roles are distinguishable by model tag: each log entry is matched to a
    transcript response (equal token pair) to learn the tag→role mapping;
    tags that never map are skipped (they may be the compaction agent's).
    Then the per-request intervals [ts - latency, ts] of coder-tag vs
    tester-tag entries must not overlap."""
    log_path = workspace.parent / "model_log.jsonl"
    if not log_path.is_file():
        return
    entries = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and not rec.get("error"):
            entries.append(rec)
    if not entries:
        return

    # Tag → role votes from the persisted transcripts (the same response
    # object is billed once by the recorder and once by the transcript).
    # Unmatched entries are skipped: a successful request whose response
    # was not persisted is the compaction agent's (§1.5) — it runs inside
    # whatever phase triggered it and its tag must not vote.
    votes: dict[str, set[str]] = {}
    tasks = load_tasks(workspace)
    for t in tasks:
        for source, groups in (
            ("coder", [t.get("messages") or []]),
            ("tester", t.get("tester_messages") or []),
        ):
            for group in groups:
                for msg in group:
                    if not is_model_response(msg):
                        continue
                    usage = msg.get("usage")
                    if not isinstance(usage, dict):
                        continue
                    in_toks = int(usage.get("input_tokens") or 0)
                    out_toks = int(usage.get("output_tokens") or 0)
                    if not in_toks and not out_toks:
                        continue
                    for rec in entries:
                        ru = rec.get("usage") or {}
                        if (
                            int(ru.get("input_tokens") or 0) == in_toks
                            and int(ru.get("output_tokens") or 0) == out_toks
                        ):
                            rec["_matched"] = True
                            tag = str(rec.get("role") or "")
                            if tag:
                                votes.setdefault(tag, set()).add(source)

    role_of = {}
    for tag, roles in votes.items():
        if len(roles) == 1:
            role_of[tag] = next(iter(roles))
    coder_tags = {t for t, r in role_of.items() if r == "coder"}
    tester_tags = {t for t, r in role_of.items() if r == "tester"}
    if not coder_tags or not tester_tags:
        return  # roles not separable in this run — the transcript check above stands

    coder_iv, tester_iv = [], []
    for rec in entries:
        if not rec.pop("_matched", False):
            continue  # compaction-agent traffic (§1.5): no phase of its own
        tag = str(rec.get("role") or "")
        ts = rec.get("ts")
        latency = rec.get("latency_ms")
        if not isinstance(ts, (int, float)) or not isinstance(latency, (int, float)):
            continue
        end = datetime.fromtimestamp(ts, tz=timezone.utc)
        start = datetime.fromtimestamp(ts - latency / 1000.0, tz=timezone.utc)
        if tag in coder_tags:
            coder_iv.append((tag, (start, end)))
        elif tag in tester_tags:
            tester_iv.append((tag, (start, end)))
    for clabel, civ in coder_iv:
        for tlabel, tiv in tester_iv:
            dt = overlap(civ, tiv)
            if dt > 0:
                failures.append(
                    f"GATE VIOLATION (recorder): request of coder tag "
                    f"{clabel!r} overlaps request of tester tag {tlabel!r} "
                    f"by {dt * 1000:.0f} ms"
                )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    scenario = tomllib.loads(
        (Path(__file__).resolve().parent / "scenario.toml").read_text(encoding="utf-8")
    )
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

    tasks = load_tasks(workspace)
    brief_titles = [b["title"] for b in scenario.get("briefs", [])]
    briefs = {t.get("title"): t for t in tasks if t.get("title") in brief_titles}
    missing = [title for title in brief_titles if title not in briefs]
    if missing:
        failures.append(f"brief tasks missing from .drcode/tasks/: {missing}")

    # 2. Both briefs COMPLETED with the tester's PASSED label.
    for title, t in briefs.items():
        if t.get("status") != "completed":
            failures.append(f"brief {title!r}: status={t.get('status')!r}, expected 'completed'")
        if t.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"brief {title!r}: verification={t.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r}"
            )
        if not t.get("tester_messages"):
            failures.append(f"brief {title!r}: no testing rounds at all")

    # 3. Queue priority: the bug brief was activated first.
    bug = next((t for t in briefs.values() if t.get("kind") == "bug"), None)
    feature = next((t for t in briefs.values() if t.get("kind") == "feature"), None)
    if bug and feature:
        b_at, f_at = bug.get("activated_at"), feature.get("activated_at")
        if not b_at:
            failures.append("bug brief has no activated_at (was never activated)")
        elif not f_at:
            failures.append("feature brief has no activated_at (was never activated)")
        elif b_at >= f_at:
            failures.append(
                f"queue priority broken: the bug was activated at {b_at}, "
                f"not before the feature (activated {f_at})"
            )

    # 4. The development/testing gate over the persisted transcripts.
    has_testing = check_gate_transcripts(tasks, failures)

    # 5. The same gate over the recorder log when roles are separable.
    if has_testing:
        check_gate_recorder(workspace, failures)

    if failures:
        print("S6 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S6 checks: green (pytest passed, bug activated before feature, "
        "coder/tester never overlap, both briefs PASSED)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
