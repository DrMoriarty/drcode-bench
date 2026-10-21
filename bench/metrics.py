"""Metric extraction from a finished run (plan drcode-bench.md, §10).

The single source of truth for every figure here is the on-disk state of
drcode itself: `<workspace>/.drcode/tasks/<id>.json` (structure defined by
`drcode/src/drcode/storage.py` + `drcode/src/drcode/models.py`) and — when
the recording wrapper (§5) has arrived — `model_log.jsonl`. drcode is NOT
imported: task files are parsed as plain JSON so the extraction works on
any snapshot (a live run tree, a diagnostics copy) without pulling the
app into the process.

What is extracted per run (into `runs/<run_id>/metrics.json`):

- wall-time of the phases: created → activated → end of development →
  end of testing → completed (task fields + message timestamps);
- compactions: how many, on which phase (coder/tester), when, at what
  context fill — from the task `events`;
- compaction savings: the transcript before/after the summary message
  (`COMPACTION_SUMMARY_PREFIX`); the exact pre-compaction length is not
  recoverable from the final transcript (the history is replaced in
  place), so it is estimated from the token usage of the last response
  before the summary vs the first response after it;
- correctness: `verification` + the harness verdict (checks.py result
  from `result.json`);
- testing rounds (`len(tester_messages)`) and bug round-trips (tasks
  with kind=bug and their activation times);
- stability: "compaction failed" / "tester failed" / network retries /
  exclusion events / `unfinished` / pending clarification.

Runnable standalone for debugging a single run:

    python -m bench.metrics runs/<run_id>
"""

from __future__ import annotations

import json
import re
import statistics
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Marker of the synthetic user message carrying the compaction summary
# (drcode/src/drcode/transcript.py). Hardcoded to keep this module
# import-free; asserted against the drcode source in the tests.
COMPACTION_SUMMARY_PREFIX = "[context summary]"

SCHEMA = "metrics/v1"

# --- event text patterns (exact strings emitted by drcode's pipeline) ----

# "Context fill {pct}% — pausing the agent and compacting history…"
# "Context fill {pct}% — pausing the run to compact history…"
# "Context fill {pct}% — compacting the testing round…"
# "Context fill {pct}% — pausing the tester round to compact history…"
_FILL_RE = re.compile(r"^Context fill (\d+)% — (.+)$")
# Compaction failure (coder and tester alike): "compaction failed: Type: msg"
_COMPACTION_FAILED_RE = re.compile(r"^compaction failed:")
# "Network error (Type): retry 1/4 in 2 s" / "...: tester retry 1/4 in 2 s"
_NET_RETRY_RE = re.compile(
    r"^Network error \((?P<err>[^)]*)\): (?P<who>tester )?retry (?P<n>\d+)/"
)
_TESTER_FAILED_RE = re.compile(r"^tester failed:")
# "Task failed and was excluded from development for the rest of the session…"
_EXCLUDED_RE = re.compile(r"^Task failed and was excluded")

# Classification of a "Context fill N% — <rest>" event.
_FILL_KINDS = {
    "pausing the agent and compacting history": ("coder", "turn_boundary"),
    "pausing the run to compact history": ("coder", "mid_run"),
    "compacting the testing round": ("tester", "round"),
    "pausing the tester round to compact history": ("tester", "mid_round"),
}
_COMPACTION_SUCCESS_KINDS = {
    "history summarized": "coder",
    "testing round summarized": "tester",
}


class MetricsError(RuntimeError):
    """Metrics cannot be extracted (no run artifacts at all)."""


# --- small parsing helpers ------------------------------------------------


def parse_ts(raw: Any) -> datetime | None:
    """ISO timestamp string (or datetime) → aware UTC datetime, None on
    anything unparsable/missing. Naive stamps are assumed UTC (drcode
    persists aware datetimes; legacy snapshots may not carry the offset)."""
    if raw is None:
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


def dt_or(raw: Any) -> str | None:
    """Timestamp → normalized ISO string (stable form for metrics.json)."""
    dt = parse_ts(raw)
    return dt.isoformat() if dt else None


def seconds_between(a: datetime | None, b: datetime | None) -> float | None:
    """b - a in seconds (rounded to 0.1), None when either side is missing
    or inverted (a > b — a phase that never happened must not show up as
    a negative duration)."""
    if a is None or b is None:
        return None
    delta = (b - a).total_seconds()
    if delta < 0:
        return None
    return round(delta, 1)


def _is_request(msg: dict[str, Any]) -> bool:
    return msg.get("kind") == "request" or msg.get("role") == "request"


def _is_response(msg: dict[str, Any]) -> bool:
    return msg.get("kind") == "response" or msg.get("role") == "response"


def message_time(msg: dict[str, Any]) -> datetime | None:
    """Timestamp of a serialized ModelMessage: the top-level `timestamp`
    (pydantic-ai 2.x puts it on both ModelRequest and ModelResponse), with
    the per-part stamps of legacy transcripts as the fallback."""
    dt = parse_ts(msg.get("timestamp"))
    if dt:
        return dt
    stamps = [
        d
        for part in msg.get("parts", [])
        if isinstance(part, dict) and (d := parse_ts(part.get("timestamp")))
    ]
    return max(stamps) if stamps else None


def user_prompt_content(msg: dict[str, Any]) -> str | None:
    if not _is_request(msg):
        return None
    for part in msg.get("parts", []):
        if isinstance(part, dict) and part.get("part_kind") == "user-prompt":
            content = part.get("content")
            if isinstance(content, str):
                return content
    return None


def is_summary_message(msg: dict[str, Any]) -> bool:
    content = user_prompt_content(msg)
    return content is not None and content.startswith(COMPACTION_SUMMARY_PREFIX)


def usage_of(msg: dict[str, Any]) -> dict[str, int] | None:
    """Token usage of a serialized ModelResponse (None when absent/zero —
    empty usage means the request never completed)."""
    usage = msg.get("usage")
    if not isinstance(usage, dict):
        return None
    out = {
        "input_tokens": int(usage.get("input_tokens") or 0),
        "output_tokens": int(usage.get("output_tokens") or 0),
        "cache_read_tokens": int(usage.get("cache_read_tokens") or 0),
        "cache_write_tokens": int(usage.get("cache_write_tokens") or 0),
    }
    if not any(out.values()):
        return None
    out["context_tokens"] = out["input_tokens"] + out["output_tokens"]
    return out


def add_usage(acc: dict[str, int], usage: dict[str, int] | None) -> None:
    if usage is None:
        return
    for key in (
        "input_tokens",
        "output_tokens",
        "cache_read_tokens",
        "cache_write_tokens",
    ):
        acc[key] = acc.get(key, 0) + usage[key]


EMPTY_USAGE = {
    "requests": 0,
    "input_tokens": 0,
    "output_tokens": 0,
    "cache_read_tokens": 0,
    "cache_write_tokens": 0,
}


def usage_total(messages: list[dict[str, Any]]) -> dict[str, int]:
    """Aggregate token usage over all responses of a transcript."""
    acc = dict(EMPTY_USAGE)
    for msg in messages:
        if not _is_response(msg):
            continue
        acc["requests"] += 1
        add_usage(acc, usage_of(msg))
    return acc


# --- events ---------------------------------------------------------------


@dataclass
class CompactionEvent:
    """One compaction-related event of a task."""

    at: datetime | None
    kind: str  # "start" | "succeeded" | "failed"
    phase: str  # "coder" | "tester" | "unknown"
    trigger_pct: int | None = None
    detail: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "at": dt_or(self.at),
            "kind": self.kind,
            "phase": self.phase,
            "trigger_pct": self.trigger_pct,
            "detail": self.detail,
        }


def classify_event(text: str) -> CompactionEvent | None:
    """Map an event text onto the compaction taxonomy (None = unrelated)."""
    m = _FILL_RE.match(text)
    if m:
        rest = m.group(2).strip().rstrip("…").strip()
        for needle, (phase, kind) in _FILL_KINDS.items():
            if needle in rest:
                return CompactionEvent(None, "start", phase, int(m.group(1)), rest)
        return CompactionEvent(None, "fill_report", "unknown", int(m.group(1)), rest)
    if _COMPACTION_FAILED_RE.match(text):
        return CompactionEvent(None, "failed", "unknown", None, text)
    for needle, phase in _COMPACTION_SUCCESS_KINDS.items():
        if needle in text:
            return CompactionEvent(None, "succeeded", phase, None, text)
    return None


@dataclass
class TaskEvents:
    """Compaction/stability events parsed from one task's event list."""

    compactions: list[CompactionEvent] = field(default_factory=list)
    compaction_failed: list[dict[str, Any]] = field(default_factory=list)
    tester_failed: list[dict[str, Any]] = field(default_factory=list)
    network_retries: list[dict[str, Any]] = field(default_factory=list)
    excluded: list[dict[str, Any]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "compactions": [e.as_dict() for e in self.compactions],
            "compaction_failed": self.compaction_failed,
            "tester_failed": self.tester_failed,
            "network_retries": self.network_retries,
            "excluded": self.excluded,
        }


def parse_events(events: list[dict[str, Any]]) -> TaskEvents:
    out = TaskEvents()
    for ev in events:
        at = parse_ts(ev.get("at"))
        text = str(ev.get("text", ""))
        compaction = classify_event(text)
        if compaction is not None:
            compaction.at = at
            out.compactions.append(compaction)
        if _COMPACTION_FAILED_RE.match(text):
            out.compaction_failed.append({"at": dt_or(at), "text": text})
        if _TESTER_FAILED_RE.match(text):
            out.tester_failed.append({"at": dt_or(at), "text": text})
        m = _NET_RETRY_RE.match(text)
        if m:
            out.network_retries.append(
                {
                    "at": dt_or(at),
                    "who": "tester" if m.group("who") else "coder",
                    "attempt": int(m.group("n")),
                    "error": m.group("err"),
                    "text": text,
                }
            )
        if _EXCLUDED_RE.match(text):
            out.excluded.append({"at": dt_or(at), "text": text})
    return out


# --- per-task analysis ----------------------------------------------------


def _last_message_time(messages: list[dict[str, Any]]) -> datetime | None:
    for msg in reversed(messages):
        dt = message_time(msg)
        if dt:
            return dt
    return None


def analyze_phases(task: dict[str, Any]) -> dict[str, Any]:
    """Wall-time of the phases (§10): постановка → активация → конец
    девелопмента → конец testing → completed.

    created/activated/completed come from the task fields; the end of
    development is the last timestamp of the coder transcript, the end of
    testing — of the last tester round (approximate: persisted message
    stamps are the finest wall-clock drcode keeps on disk, plan §1.5)."""
    created = parse_ts(task.get("created_at"))
    activated = parse_ts(task.get("activated_at"))
    completed = parse_ts(task.get("completed_at"))

    coder_messages = task.get("messages") or []
    tester_rounds = task.get("tester_messages") or []
    dev_end = _last_message_time(coder_messages)
    testing_end = _last_message_time(tester_rounds[-1]) if tester_rounds else None

    return {
        "created_at": dt_or(created),
        "activated_at": dt_or(activated),
        "dev_end": dt_or(dev_end),
        "testing_end": dt_or(testing_end),
        "completed_at": dt_or(completed),
        "queue_wait_s": seconds_between(created, activated),
        "dev_s": seconds_between(activated, dev_end),
        "testing_s": seconds_between(dev_end, testing_end),
        "active_to_done_s": seconds_between(activated, completed),
        "total_s": seconds_between(created, completed),
    }


def analyze_compaction_savings(
    messages: list[dict[str, Any]],
    fill_events: list[CompactionEvent],
) -> list[dict[str, Any]]:
    """Компакционная экономия (§10): what each summary replaced.

    The final transcript keeps only the original user prompts (verbatim)
    plus the synthetic summary request — the summarized history is gone.
    The best on-disk estimate of the before/after size is the token usage
    the model itself reported: the last completed response BEFORE the
    summary reports the context fill that triggered the compaction, the
    first response AFTER it reports the compacted context."""
    savings: list[dict[str, Any]] = []
    last_usage: dict[str, int] | None = None
    pending: dict[str, Any] | None = None
    prompts_before = 0
    for msg in messages:
        if is_summary_message(msg):
            body = user_prompt_content(msg) or ""
            summary_body = body[len(COMPACTION_SUMMARY_PREFIX) :].strip()
            trigger = None
            summary_at = message_time(msg)
            for ev in fill_events:
                if ev.kind != "start":
                    continue
                if summary_at is None or ev.at is None or ev.at <= summary_at:
                    trigger = ev.trigger_pct
            pending = {
                "at": dt_or(summary_at),
                "summary_chars": len(summary_body),
                "prompts_kept": prompts_before,
                "pre_tokens_est": last_usage["context_tokens"] if last_usage else None,
                "post_tokens_est": None,
                "saved_tokens_est": None,
                "trigger_pct": trigger,
            }
            continue
        if pending is not None and _is_response(msg):
            usage = usage_of(msg)
            if usage:
                pending["post_tokens_est"] = usage["context_tokens"]
                if pending["pre_tokens_est"] is not None:
                    pending["saved_tokens_est"] = max(
                        0, pending["pre_tokens_est"] - usage["context_tokens"]
                    )
                savings.append(pending)
                pending = None
        if _is_request(msg) and user_prompt_content(msg) is not None:
            prompts_before += 1
        if _is_response(msg):
            last_usage = usage_of(msg) or last_usage
    # A summary as the very last message (compacted right before the run
    # ended) has no post-compaction response to measure against.
    if pending is not None:
        savings.append(pending)
    return savings


def analyze_testing(task: dict[str, Any]) -> dict[str, Any]:
    """Testing rounds: one transcript per round; a compaction rewrites the
    last round in place, which shows up as a summary message inside it."""
    rounds = []
    for i, rnd in enumerate(task.get("tester_messages") or []):
        rounds.append(
            {
                "index": i,
                "n_messages": len(rnd),
                "has_summary": any(is_summary_message(m) for m in rnd),
                "usage": usage_total(rnd),
            }
        )
    return {"n_rounds": len(rounds), "rounds": rounds}


def analyze_task(task: dict[str, Any]) -> dict[str, Any]:
    """Full per-task metrics block (see the module docstring)."""
    events = parse_events(task.get("events") or [])
    messages = task.get("messages") or []
    coder_fill_events = [e for e in events.compactions if e.kind == "start"]

    stability = {
        "compaction_failed": len(events.compaction_failed),
        "tester_failed": len(events.tester_failed),
        "network_retries": len(events.network_retries),
        "excluded_from_queue": len(events.excluded),
        "unfinished": bool(task.get("unfinished")),
        "pending_clarification": task.get("clarification") is not None,
    }
    compactions = {
        "n_started": sum(1 for e in events.compactions if e.kind == "start"),
        "n_succeeded": sum(1 for e in events.compactions if e.kind == "succeeded"),
        "n_failed": len(events.compaction_failed),
        "by_phase": {
            "coder": sum(
                1 for e in events.compactions if e.phase == "coder" and e.kind == "start"
            ),
            "tester": sum(
                1
                for e in events.compactions
                if e.phase == "tester" and e.kind == "start"
            ),
        },
        "events": [e.as_dict() for e in events.compactions],
    }
    n_prompts = sum(
        1
        for m in messages
        if _is_request(m)
        and (c := user_prompt_content(m)) is not None
        and not c.startswith(COMPACTION_SUMMARY_PREFIX)
    )
    final_usage = next(
        (u for m in reversed(messages) if _is_response(m) and (u := usage_of(m))),
        None,
    )
    return {
        "id": task.get("id"),
        "title": task.get("title"),
        "kind": task.get("kind"),
        "status": task.get("status"),
        "verification": task.get("verification"),
        "phases": analyze_phases(task),
        "compactions": compactions,
        "compaction_savings": analyze_compaction_savings(messages, coder_fill_events),
        "transcript": {
            "n_messages": len(messages),
            "n_user_prompts": n_prompts,
            "context_tokens_final": (
                final_usage["context_tokens"] if final_usage else None
            ),
        },
        "usage": usage_total(messages),
        "testing": analyze_testing(task),
        "stability": stability,
        "stability_events": events.as_dict(),
    }


# --- run-level extraction -------------------------------------------------


def find_tasks_dir(run_dir: Path) -> Path | None:
    """Locate the task JSONs of a run: the live run tree first
    (`<run_dir>/workspace/.drcode/tasks/`), the failure-diagnostics copy
    (`<run_dir>/diagnostics/drcode-state/tasks/`) second — a run that
    never settled still has its state snapshotted (§4)."""
    for candidate in (
        run_dir / "workspace" / ".drcode" / "tasks",
        run_dir / "diagnostics" / "drcode-state" / "tasks",
    ):
        if candidate.is_dir() and any(candidate.glob("*.json")):
            return candidate
    return None


def _load_model_log(run_dir: Path) -> dict[str, Any] | None:
    """Aggregate `model_log.jsonl` (recorder §5) when present: per-role
    request counts, latency and tokens. Missing file → None (the recorder
    arrives at plan stage 2; runs without it stay unrecorded)."""
    path = run_dir / "model_log.jsonl"
    if not path.is_file():
        return None
    per_role: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        role = str(rec.get("role") or "unknown")
        entry = per_role.setdefault(
            role,
            {"requests": 0, "latency_ms_total": 0, "latency_ms_max": 0, **EMPTY_USAGE},
        )
        entry["requests"] += 1
        latency = rec.get("latency_ms")
        if isinstance(latency, (int, float)):
            entry["latency_ms_total"] += int(latency)
            entry["latency_ms_max"] = max(entry["latency_ms_max"], int(latency))
        usage = rec.get("usage")
        if isinstance(usage, dict):
            for key in (
                "input_tokens",
                "output_tokens",
                "cache_read_tokens",
                "cache_write_tokens",
            ):
                entry[key] = entry.get(key, 0) + int(usage.get(key) or 0)
    return {"file": path.name, "per_role": per_role} if per_role else None


def _verdict(result: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    """Overall verdict of the run: the harness verdict (settle + checks.py)
    plus the tester's own label — 'green' only when everything agrees."""
    if not result:
        return "unknown"
    ok = bool(result.get("ok"))
    checks = result.get("checks_ok")
    verified = all(
        t.get("verification") in (None, "Verified successfully") for t in tasks
    )
    if ok and checks is not False and verified:
        return "green"
    if ok:
        return "settled-but-flagged"
    return "failed"


def _sum_usage(tasks: list[dict[str, Any]]) -> dict[str, int]:
    acc = dict(EMPTY_USAGE)
    for t in tasks:
        for key in acc:
            acc[key] += t["usage"].get(key, 0)
        for rnd in t["testing"]["rounds"]:
            for key in acc:
                acc[key] += rnd["usage"].get(key, 0)
    return acc


def extract_run_metrics(run_dir: Path, *, write: bool = True) -> dict[str, Any]:
    """Full metric extraction for one run directory → metrics dict (and
    `metrics.json` inside it, unless `write=False`)."""
    run_dir = Path(run_dir)
    result: dict[str, Any] = {}
    result_path = run_dir / "result.json"
    if result_path.is_file():
        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            result = {}

    tasks_dir = find_tasks_dir(run_dir)
    if tasks_dir is None and not result and not run_dir.is_dir():
        raise MetricsError(f"no run artifacts in {run_dir}")

    tasks: list[dict[str, Any]] = []
    if tasks_dir is not None:
        for path in sorted(tasks_dir.glob("*.json")):
            if path.name.endswith(".bak"):
                continue
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if not isinstance(raw, dict) or "title" not in raw:
                continue  # not a task file
            tasks.append(analyze_task(raw))

    totals = {
        "n_tasks": len(tasks),
        "n_bug_tasks": sum(1 for t in tasks if t["kind"] == "bug"),
        "n_testing_rounds": sum(t["testing"]["n_rounds"] for t in tasks),
        "n_compactions": sum(t["compactions"]["n_succeeded"] for t in tasks),
        "n_compactions_started": sum(t["compactions"]["n_started"] for t in tasks),
        "usage": _sum_usage(tasks),
        "stability": {
            "compaction_failed": sum(t["stability"]["compaction_failed"] for t in tasks),
            "tester_failed": sum(t["stability"]["tester_failed"] for t in tasks),
            "network_retries": sum(t["stability"]["network_retries"] for t in tasks),
            "unfinished": sum(1 for t in tasks if t["stability"]["unfinished"]),
            "pending_clarification": sum(
                1 for t in tasks if t["stability"]["pending_clarification"]
            ),
            "excluded_from_queue": sum(
                t["stability"]["excluded_from_queue"] for t in tasks
            ),
        },
    }
    # Bug round-trips (§10): bug tasks with their activation stamps.
    bug_round_trips = [
        {
            "id": t["id"],
            "title": t["title"],
            "activated_at": t["phases"]["activated_at"],
        }
        for t in tasks
        if t["kind"] == "bug"
    ]

    metrics: dict[str, Any] = {
        "schema": SCHEMA,
        "run_id": run_dir.name,
        "scenario": result.get("scenario"),
        "combo": result.get("combo"),
        "verdict": _verdict(result, tasks),
        "result": {
            "ok": result.get("ok"),
            "reason": result.get("reason", ""),
            "timed_out": result.get("timed_out"),
            "checks_ok": result.get("checks_ok"),
            "settle_elapsed_s": result.get("settle_elapsed_s"),
            "started_at": result.get("started_at"),
            "finished_at": result.get("finished_at"),
            "resolved_roles": result.get("resolved_roles") or {},
        },
        "wall_time_s": {
            "settle": result.get("settle_elapsed_s"),
            "run": seconds_between(
                parse_ts(result.get("started_at")), parse_ts(result.get("finished_at"))
            ),
        },
        "totals": totals,
        "bug_round_trips": bug_round_trips,
        "tasks": tasks,
        "model_log": _load_model_log(run_dir),
    }
    if write:
        out = run_dir / "metrics.json"
        out.write_text(
            json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return metrics


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: python -m bench.metrics <run_dir>", file=sys.stderr)
        return 2
    try:
        metrics = extract_run_metrics(Path(args[0]))
    except MetricsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
