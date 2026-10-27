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
  from `result.json`), plus the non-verdict `checks_metrics` facts
  parsed from checks.py stdout (`S9 metric: report_committed=...` —
  measured commit discipline, s9);
- model traffic from the recorder (`model_log.jsonl`, §5): requests per
  role, per-request latency (p50/p95 per role and overall), tokens per
  role (prompt/completion) — and the cross-check of the recorder's
  billing against the `usage` of the serialized ModelResponses of the
  task transcripts (`usage_cross_check` in metrics.json: unmatched
  transcript responses are always unexplained; unmatched recorder
  entries are expected to be compaction-agent requests, whose responses
  drcode does not persist, §1.5);
- testing rounds (`len(tester_messages)`) and bug round-trips (tasks
  with kind=bug and their activation times);
- user-simulator interventions (§6, `user_sim.jsonl`): what the
  simulator did and which scenario failures it recorded;
- stability: "compaction failed" / "tester failed" / network retries /
  exclusion events / `unfinished` / pending clarification.

Runnable standalone for debugging a single run:

    python -m bench.metrics runs/<run_id>
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
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
_NET_RETRY_RE = re.compile(r"^Network error \((?P<err>[^)]*)\): (?P<who>tester )?retry (?P<n>\d+)/")
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
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


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


def user_prompt_contents(msg: dict[str, Any]) -> list[str]:
    """ALL string user-prompt contents of a serialized request. A request
    can carry MORE than one: after a compaction + continuation turn the
    persisted transcript merges the original brief and the synthetic
    summary prompt into a single request (observed on-disk shape), so
    summary detection must scan every part, not just the first."""
    if not _is_request(msg):
        return []
    out = []
    for part in msg.get("parts", []):
        if isinstance(part, dict) and part.get("part_kind") == "user-prompt":
            content = part.get("content")
            if isinstance(content, str):
                out.append(content)
    return out


def is_summary_message(msg: dict[str, Any]) -> bool:
    """True when the request carries the synthetic compaction-summary
    prompt (any user-prompt part — see `user_prompt_contents`)."""
    return any(c.startswith(COMPACTION_SUMMARY_PREFIX) for c in user_prompt_contents(msg))


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
        for needle, (phase, _kind) in _FILL_KINDS.items():
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
        # A request can carry several user-prompt parts (the persisted
        # transcript merges the original brief and the summary prompt into
        # one request after a compaction + continuation turn) — walk the
        # parts in order.
        if _is_request(msg):
            for content in user_prompt_contents(msg):
                if content.startswith(COMPACTION_SUMMARY_PREFIX):
                    summary_body = content[len(COMPACTION_SUMMARY_PREFIX) :].strip()
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
                        "pre_tokens_est": (last_usage["context_tokens"] if last_usage else None),
                        "post_tokens_est": None,
                        "saved_tokens_est": None,
                        "trigger_pct": trigger,
                    }
                else:
                    prompts_before += 1
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


# --- tester compaction threshold source (§1.2/§13, scenario S4) ------------


def read_context_limits(run_dir: Path) -> dict[str, int]:
    """Effective max_context_tokens per role for a run dir (best effort,
    §1.2): `result.json.resolved_context_tokens` when the harness recorded
    it, otherwise reconstructed from the generated configs the way
    `providers.resolve` reads them (project `models` refs → catalog
    entry). Empty dict = unknown."""
    run_dir = Path(run_dir)

    result: dict[str, Any] = {}
    result_path = run_dir / "result.json"
    if result_path.is_file():
        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            result = {}
    recorded = result.get("resolved_context_tokens")
    if isinstance(recorded, dict) and recorded:
        return {str(k): int(v) for k, v in recorded.items() if isinstance(v, (int, float))}

    # Fallback: parse the generated configs. The state dir lives in the
    # workspace (or its diagnostics copy for failed runs).
    for state_dir in (
        run_dir / "workspace" / ".drcode",
        run_dir / "diagnostics" / "drcode-state",
    ):
        project_file = state_dir / "drcode.json"
        catalog_file = run_dir / "config-home" / "drcode" / "models.json"
        if not project_file.is_file() or not catalog_file.is_file():
            continue
        try:
            project = json.loads(project_file.read_text(encoding="utf-8"))
            catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        entries: dict[tuple[str, str], int] = {}
        providers_by_name: dict[str, str] = {}
        for p in catalog.get("providers") or []:
            providers_by_name[p.get("name")] = p.get("base_url", "")
            for m in p.get("models") or []:
                entries[(p.get("name"), m.get("id"))] = int(m.get("max_context_tokens") or 0)
        refs = project.get("models") or {}
        limits: dict[str, int] = {}
        for role, ref in refs.items():
            provider_name, _, model_id = str(ref).partition("/")
            ctx = entries.get((provider_name, model_id))
            if ctx:
                limits[role] = ctx
        if limits:
            return limits
    return {}


def _round_tokens_before_summary(rnd: list[dict[str, Any]]) -> int | None:
    """Context size (input tokens) the tester had accumulated right before
    the round's summary message: the last completed response before it.

    Only works when the pre-compaction tail of the round survived in the
    persisted transcript; the common mid-round path REPLACES the round
    with prompt + summary + continuation (the pre-compaction responses are
    gone) — then the recorder log is the token source
    (`_recorder_tokens_before`)."""
    last: int | None = None
    for msg in rnd:
        if is_summary_message(msg):
            break
        if _is_response(msg):
            usage = usage_of(msg)
            if usage:
                last = usage["input_tokens"]
    return last


def _recorder_tokens_before(
    entries: list[dict[str, Any]],
    tester_tag: str | None,
    at: datetime | None,
    *,
    window_s: float = 300.0,
) -> int | None:
    """Largest reported input_tokens among the tester's recorder entries in
    the window before `at` — the context size the tester had accumulated
    when the compaction gate fired (the recorder logs every request with
    the history it carried, §5)."""
    if not entries or not tester_tag or at is None:
        return None
    t = at.timestamp()
    best = 0
    for rec in entries:
        if rec.get("role") != tester_tag or rec.get("error"):
            continue
        usage = rec.get("usage")
        if not isinstance(usage, dict):
            continue
        tokens = int(usage.get("input_tokens") or 0)
        if not tokens:
            continue
        rec_t = rec.get("ts")
        rec_t = float(rec_t) if isinstance(rec_t, (int, float)) else None
        if rec_t is None or not (t - window_s <= rec_t <= t + 5):
            continue
        best = max(best, tokens)
    return best or None


def _tester_role_tag(run_dir: Path) -> str | None:
    """The recorder role tag of the tester agent (`f"{model}@{base_url}"`,
    §5), reconstructed from the generated configs. None when the configs
    are unreadable."""
    for state_dir in (
        run_dir / "workspace" / ".drcode",
        run_dir / "diagnostics" / "drcode-state",
    ):
        project_file = state_dir / "drcode.json"
        catalog_file = run_dir / "config-home" / "drcode" / "models.json"
        if not project_file.is_file() or not catalog_file.is_file():
            continue
        try:
            project = json.loads(project_file.read_text(encoding="utf-8"))
            catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        ref = (project.get("models") or {}).get("tester")
        if not ref:
            return None
        provider_name, _, model_id = str(ref).partition("/")
        for p in catalog.get("providers") or []:
            if p.get("name") == provider_name:
                return f"{model_id}@{p.get('base_url', '')}"
    return None


def analyze_tester_threshold(
    raw_task: dict[str, Any],
    limits: dict[str, int],
    *,
    log_entries: list[dict[str, Any]] | None = None,
    tester_tag: str | None = None,
) -> dict[str, Any] | None:
    """Which model's context limit drove the tester's compactions (§1.2/§13).

    drcode ≥ 0.5.0 resolves models per role: the tester's mid-round
    compaction threshold is computed from the TESTER model's config
    (`_fill_over_threshold(..., AgentRole.TESTER)` uses the tester role) —
    the benchmark must verify that behavior, not assume it. From the
    artifacts the denominator is recoverable indirectly: a round that was
    compacted at trigger_pct with a pre-compaction token estimate T implies
    an effective limit T / pct * 100 — nearest to the tester limit means the
    threshold indeed came from the tester model, nearest to the coding
    limit would mean drcode regressed to the pre-0.5.0 behavior (threshold
    from the coding config). The token estimate comes from the round
    transcript when its pre-compaction tail survived, otherwise from the
    recorder log (§5).

    When coding and tester limits COINCIDE the classification is moot —
    it is reported as 'tester' (no regression possible). `raw_task` is
    the unparsed task JSON. None = no tester-phase compaction to classify."""
    events = parse_events(raw_task.get("events") or [])
    tester_starts = [e for e in events.compactions if e.phase == "tester" and e.kind == "start"]
    if not tester_starts:
        return None
    coding = limits.get("coding")
    tester = limits.get("tester")
    # The expected denominator is the tester's own limit; only coinciding
    # limits make the two sources indistinguishable (no regression possible).
    moot = coding is not None and tester is not None and tester == coding

    observations: list[dict[str, Any]] = []
    sources: set[str] = set()
    classified = False
    for i, rnd in enumerate(raw_task.get("tester_messages") or []):
        summary = next((m for m in rnd if is_summary_message(m)), None)
        if summary is None:
            continue
        tokens = _round_tokens_before_summary(rnd)
        summary_at = message_time(summary)
        trigger = next(
            (
                e.trigger_pct
                for e in reversed(tester_starts)
                if e.trigger_pct is not None
                and summary_at is not None
                and e.at is not None
                and e.at <= summary_at
            ),
            None,
        )
        if tokens is None:
            # The mid-round compaction replaced the round in place: the
            # pre-compaction responses are gone from the transcript —
            # take the context size from the recorder log (§5).
            start_at = next(
                (
                    e.at
                    for e in reversed(tester_starts)
                    if trigger is not None and e.trigger_pct == trigger
                ),
                None,
            )
            tokens = _recorder_tokens_before(log_entries or [], tester_tag, start_at)
        implied = round(tokens * 100 / trigger) if tokens and trigger else None
        source = "unknown"
        if moot:
            source = "tester"  # thresholds coincide — no regression possible
            classified = True
        elif implied is not None and coding is not None and tester is not None:
            classified = True
            source = "tester" if abs(implied - tester) <= abs(implied - coding) else "coding"
        sources.add(source)
        observations.append(
            {
                "round": i,
                "trigger_pct": trigger,
                "pre_tokens_est": tokens,
                "implied_max_context_tokens": implied,
                "source": source,
            }
        )
    if not observations:
        # Compaction started but never produced a summary (failed): the
        # source cannot be classified from transcripts — events only.
        for e in tester_starts:
            tokens = _recorder_tokens_before(log_entries or [], tester_tag, e.at)
            implied = round(tokens * 100 / e.trigger_pct) if tokens and e.trigger_pct else None
            source = "unknown"
            if moot:
                source, classified = "tester", True
            elif implied is not None and coding and tester and tester != coding:
                classified = True
                source = "tester" if abs(implied - tester) <= abs(implied - coding) else "coding"
            sources.add(source)
            observations.append(
                {
                    "round": None,
                    "trigger_pct": e.trigger_pct,
                    "pre_tokens_est": tokens,
                    "implied_max_context_tokens": implied,
                    "source": source,
                }
            )
    if "tester" in sources or "mixed" in sources:
        source = "tester" if sources == {"tester"} else "mixed"
    elif "coding" in sources:
        source = "coding"
    else:
        source = "unknown"
    return {
        "coding_max_context_tokens": coding,
        "tester_max_context_tokens": tester,
        "source": source,
        "classified": classified,
        "observations": observations,
        "remark": (
            "drcode ≥ 0.5.0 computes the tester compaction threshold from "
            "the TESTER model's config (per-role resolution, §1.2) — "
            "'tester' is the expected classification; 'coding' would be a "
            "regression."
        ),
    }


def analyze_task(
    task: dict[str, Any],
    *,
    context_limits: dict[str, int] | None = None,
    log_entries: list[dict[str, Any]] | None = None,
    tester_tag: str | None = None,
) -> dict[str, Any]:
    """Full per-task metrics block (see the module docstring).

    `context_limits` (effective max_context_tokens per role, §1.2) enables
    the tester-threshold-source classification (`analyze_tester_threshold`)
    — without it that block reports the raw observations only; the
    recorder log backs the token estimate when the mid-round compaction
    replaced the round transcript in place."""
    events = parse_events(task.get("events") or [])
    messages = task.get("messages") or []
    coder_fill_events = [e for e in events.compactions if e.kind == "start"]

    n_summaries = sum(1 for m in messages if is_summary_message(m)) + sum(
        1 for rnd in task.get("tester_messages") or [] for m in rnd if is_summary_message(m)
    )
    tester_threshold = analyze_tester_threshold(
        task,
        context_limits or {},
        log_entries=log_entries,
        tester_tag=tester_tag,
    )

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
            "coder": sum(1 for e in events.compactions if e.phase == "coder" and e.kind == "start"),
            "tester": sum(
                1 for e in events.compactions if e.phase == "tester" and e.kind == "start"
            ),
        },
        # Degradation signal (§10): a summary did not stick — the context
        # filled up again and drcode had to compact a second time. One
        # summary per transcript is the healthy shape; more is the
        # "deterioration after summary" the report must surface.
        "n_summaries_in_transcript": n_summaries,
        "repeat_compaction": n_summaries > 1,
        # Trigger kinds (§1.2): mid-run = pause → sanitized_messages →
        # summary → continuation turn; turn_boundary = the between-turns
        # gate. S3's checks assert at least one of them happened.
        "mid_run_pause": any(
            e.kind == "start" and "pausing the run" in e.detail for e in events.compactions
        ),
        "turn_boundary_pause": any(
            e.kind == "start" and "pausing the agent" in e.detail for e in events.compactions
        ),
        "tester_threshold": tester_threshold,
        "events": [e.as_dict() for e in events.compactions],
    }
    n_prompts = sum(
        1
        for m in messages
        for c in user_prompt_contents(m)
        if not c.startswith(COMPACTION_SUMMARY_PREFIX)
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
            "context_tokens_final": (final_usage["context_tokens"] if final_usage else None),
        },
        "usage": usage_total(messages),
        "testing": analyze_testing(task),
        "stability": stability,
        "stability_events": events.as_dict(),
    }


# --- coder/tester activity diagnostics (§7 S6, passive) --------------------


def _ts_interval(messages: list[dict[str, Any]]):
    """(start, end) over the timestamps of one transcript; None without
    any stamps."""
    stamps = [t for m in messages if (t := message_time(m))]
    if not stamps:
        return None
    return (min(stamps), max(stamps))


def analyze_gate(
    raw_tasks: list[dict[str, Any]],
    log_entries: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Coder/tester activity diagnostics (§2/§7 S6): the recorded
    intersections of coder and tester in-flight activity.

    NOT a gate verdict: the strict reading of «no development while
    testing is in flight» false-bites by construction in multi-task
    runs — with several tasks queued (a bug report from a FAILED
    verdict, neighbouring briefs) drcode legitimately develops one task
    while the tester verifies another. Overlap facts stay in `overlaps`
    as passive diagnostics; the verdict classifies only whether testing
    happened at all.

    Two independent sources:

    - transcripts (always available): a coder message timestamp strictly
      INSIDE a tester round's [start, end] interval — a span-vs-span
      comparison would false-bite, because one task's coder transcript
      legitimately spans the gaps where its own failed testing round ran
      before a follow-up;
    - the recorder log (§5, when the roles are distinguishable by model
      tag): per-request intervals [ts − latency, ts] of coder-tag vs
      tester-tag entries. Tags are mapped to roles by matching recorder
      entries against persisted transcript responses (same token pair,
      §10 cross-check); unmatched entries (the compaction agent's,
      §1.5) never vote and never count.

    verdict: "ok" | "no-testing" | "unknown".
    """
    tester_rounds: list[tuple[str, tuple[datetime, datetime]]] = []
    coder_points: list[tuple[str, datetime]] = []
    for raw in raw_tasks:
        label = f"{raw.get('kind')}:{raw.get('title')}"
        for i, rnd in enumerate(raw.get("tester_messages") or []):
            iv = _ts_interval(rnd)
            if iv:
                tester_rounds.append((f"{label} round {i}", iv))
        for msg in raw.get("messages") or []:
            ts = message_time(msg)
            if ts:
                coder_points.append((label, ts))

    overlaps: list[dict[str, Any]] = []
    for tlabel, (start, end) in tester_rounds:
        for clabel, ts in coder_points:
            if start < ts < end:
                overlaps.append(
                    {
                        "source": "transcripts",
                        "coder": clabel,
                        "tester": tlabel,
                        "at": dt_or(ts),
                        "detail": (
                            f"coder message at {dt_or(ts)} inside tester "
                            f"interval {dt_or(start)}…{dt_or(end)}"
                        ),
                    }
                )

    recorder_checked = False
    if log_entries and tester_rounds:
        # Tag → role votes: a recorder entry matched to a persisted
        # transcript response (same token pair) inherits that response's
        # source (coder/tester, see transcript_responses).
        responses: list[tuple[str, datetime | None, int, int]] = []
        for raw in raw_tasks:
            for r in transcript_responses(raw):
                responses.append(
                    (r["source"], parse_ts(r["ts"]), r["input_tokens"], r["output_tokens"])
                )
        votes: dict[str, set[str]] = {}
        matched: set[int] = set()
        for i, rec in enumerate(log_entries):
            if rec.get("error"):
                continue
            usage = rec.get("usage")
            if not isinstance(usage, dict):
                continue
            in_toks = int(usage.get("input_tokens") or 0)
            out_toks = int(usage.get("output_tokens") or 0)
            if not in_toks and not out_toks:
                continue
            rec_t = rec.get("ts")
            rec_dt = (
                datetime.fromtimestamp(rec_t, tz=UTC)
                if isinstance(rec_t, (int, float))
                else parse_ts(rec_t)
            )
            for source, resp_t, r_in, r_out in responses:
                if r_in != in_toks or r_out != out_toks:
                    continue
                if (
                    rec_dt is not None
                    and resp_t is not None
                    and abs((rec_dt - resp_t).total_seconds()) > 60.0
                ):
                    continue
                matched.add(i)
                tag = str(rec.get("role") or "")
                if tag:
                    votes.setdefault(tag, set()).add(source)
                break
        role_of = {t: next(iter(r)) for t, r in votes.items() if len(r) == 1}
        coder_tags = {t for t, r in role_of.items() if r == "coder"}
        tester_tags = {t for t, r in role_of.items() if r == "tester"}
        if coder_tags and tester_tags:
            recorder_checked = True
            coder_iv: list[tuple[str, tuple[datetime, datetime]]] = []
            tester_iv: list[tuple[str, tuple[datetime, datetime]]] = []
            for i, rec in enumerate(log_entries):
                if i not in matched or rec.get("error"):
                    continue  # compaction traffic (§1.5) has no phase of its own
                tag = str(rec.get("role") or "")
                ts, latency = rec.get("ts"), rec.get("latency_ms")
                if not isinstance(ts, (int, float)) or not isinstance(latency, (int, float)):
                    continue
                end = datetime.fromtimestamp(ts, tz=UTC)
                iv = (datetime.fromtimestamp(ts - latency / 1000.0, tz=UTC), end)
                if tag in coder_tags:
                    coder_iv.append((tag, iv))
                elif tag in tester_tags:
                    tester_iv.append((tag, iv))
            for clabel, (c0, c1) in coder_iv:
                for tlabel, (t0, t1) in tester_iv:
                    start, end = max(c0, t0), min(c1, t1)
                    if end > start:
                        overlaps.append(
                            {
                                "source": "recorder",
                                "coder": clabel,
                                "tester": tlabel,
                                "at": dt_or(start),
                                "detail": (
                                    f"recorder request intervals overlap by "
                                    f"{(end - start).total_seconds() * 1000:.0f} ms "
                                    f"({dt_or(start)}…{dt_or(end)})"
                                ),
                            }
                        )

    if tester_rounds:
        verdict = "ok"
    elif raw_tasks:
        verdict = "no-testing"
    else:
        verdict = "unknown"
    return {
        "verdict": verdict,
        "sources": (["transcripts", "recorder"] if recorder_checked else ["transcripts"]),
        "n_tester_rounds": len(tester_rounds),
        "n_coder_messages": len(coder_points),
        "overlaps": overlaps,
        "remark": (
            "overlaps are PASSIVE diagnostics (§2/§7 S6): in multi-task "
            "runs the coder legitimately works on other tasks while the "
            "tester verifies one — they never affect the verdict; the "
            "recorder source applies only when the roles are "
            "distinguishable by model tag"
        ),
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


def _percentile(values: list[float], pct: float) -> float | None:
    """Linear-interpolated percentile of a non-empty list (None otherwise)."""
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return round(ordered[0], 1)
    k = (len(ordered) - 1) * (pct / 100.0)
    lo, hi = int(k), min(int(k) + 1, len(ordered) - 1)
    frac = k - lo
    return round(ordered[lo] + (ordered[hi] - ordered[lo]) * frac, 1)


def read_model_log_entries(run_dir: Path) -> list[dict[str, Any]]:
    """Raw records of `model_log.jsonl` (recorder §5), corrupt lines
    skipped. Missing file → empty list (a run predating the recorder)."""
    path = run_dir / "model_log.jsonl"
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out


def _load_model_log(
    run_dir: Path, entries: list[dict[str, Any]] | None = None
) -> dict[str, Any] | None:
    """Aggregate `model_log.jsonl` (recorder §5) when present: per-role
    request counts (one HTTP request = one line), latency (per-role and
    overall p50/p95, §10) and tokens per role. Missing file → None (a
    run without the recorder stays unrecorded)."""
    if entries is None:
        entries = read_model_log_entries(run_dir)
    if not entries:
        return None
    per_role: dict[str, dict[str, Any]] = {}
    all_latencies: list[float] = []
    for rec in entries:
        role = str(rec.get("role") or "unknown")
        entry = per_role.setdefault(
            role,
            {
                "requests": 0,
                "latency_ms_total": 0,
                "latency_ms_max": 0,
                "latencies_ms": [],
                **EMPTY_USAGE,
            },
        )
        entry["requests"] += 1
        latency = rec.get("latency_ms")
        if isinstance(latency, (int, float)):
            entry["latency_ms_total"] += int(latency)
            entry["latency_ms_max"] = max(entry["latency_ms_max"], int(latency))
            entry["latencies_ms"].append(float(latency))
            all_latencies.append(float(latency))
        usage = rec.get("usage")
        if isinstance(usage, dict):
            for key in (
                "input_tokens",
                "output_tokens",
                "cache_read_tokens",
                "cache_write_tokens",
            ):
                entry[key] = entry.get(key, 0) + int(usage.get(key) or 0)
    for entry in per_role.values():
        latencies = entry.pop("latencies_ms")
        entry["latency_ms_p50"] = _percentile(latencies, 50)
        entry["latency_ms_p95"] = _percentile(latencies, 95)
    return {
        "file": "model_log.jsonl",
        "per_role": per_role,
        "requests": sum(e["requests"] for e in per_role.values()),
        "latency_ms_p50": _percentile(all_latencies, 50),
        "latency_ms_p95": _percentile(all_latencies, 95),
    }


# --- proxy log (§9/§10) ------------------------------------------------------


def read_proxy_log_entries(run_dir: Path) -> list[dict[str, Any]]:
    """Raw records of `proxy_log.jsonl` (§9 proxy), corrupt lines skipped.
    Missing file → empty list (a run without the proxy)."""
    path = run_dir / "proxy_log.jsonl"
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out


def _watchdog_aggregate(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Stall-watchdog events (§9, `[proxy.watchdog]`) over the proxy log:
    aborts of silent upstream attempts, the transparent retries that
    followed, and their outcomes. Present when the watchdog FIRED at
    least once (an active-but-silent watchdog is marked in result.json
    via `result.proxy_watchdog`, not here)."""
    triggers = retries = saved = exhausted = 0
    phases: dict[str, int] = {}
    for rec in entries:
        wd = rec.get("watchdog")
        if not isinstance(wd, dict):
            continue
        triggers += len(wd.get("events") or [])
        retries += max(int(wd.get("attempts", 1)) - 1, 0)
        if wd.get("saved"):
            saved += 1
        elif wd.get("events"):
            exhausted += 1
        for ev in wd.get("events") or []:
            phase = str(ev.get("phase") or "unknown")
            phases[phase] = phases.get(phase, 0) + 1
    if not triggers and not retries:
        return None
    return {
        "triggers": triggers,
        "retries": retries,
        "saved": saved,
        "exhausted": exhausted,
        "abort_phases": phases,
        "remark": (
            "proxy-side stall watchdog was active: aborted silences are masked tail "
            "latency — do not mix with clean measurements (result.proxy_watchdog "
            "marks the run even when nothing fired)"
        ),
    }


def analyze_proxy(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Aggregate `proxy_log.jsonl` (§9/§10): per-model request counts and
    latency p50/p95 (the proxy measures the SAME wall-time the recorder
    does — request received → response complete — as an INDEPENDENT
    source), the injected fault script replay and the upstream errors.

    The faulted requests are excluded from the latency percentiles: a 429
    answered locally is not the provider's latency."""
    if not entries:
        return None
    per_model: dict[str, dict[str, Any]] = {}
    faults: dict[str, int] = {}
    clean_latencies: list[float] = []
    errors = 0
    for rec in entries:
        model = str(rec.get("model") or "unknown")
        entry = per_model.setdefault(model, {"requests": 0, "faulted": 0, "latencies_ms": []})
        entry["requests"] += 1
        fault = rec.get("fault")
        if fault:
            kind = str(fault.get("kind") or "unknown")
            faults[kind] = faults.get(kind, 0) + 1
            entry["faulted"] += 1
            continue  # a locally-answered fault says nothing about latency
        if rec.get("error") or rec.get("status") in (502, 500):
            errors += 1
            continue
        latency = rec.get("latency_ms")
        if isinstance(latency, (int, float)):
            entry["latencies_ms"].append(float(latency))
            clean_latencies.append(float(latency))
    for entry in per_model.values():
        latencies = entry.pop("latencies_ms")
        entry["latency_ms_p50"] = _percentile(latencies, 50)
        entry["latency_ms_p95"] = _percentile(latencies, 95)
    return {
        "file": "proxy_log.jsonl",
        "requests": len(entries),
        "errors": errors,
        "faults_injected": sum(faults.values()),
        "faults": faults,
        "watchdog": _watchdog_aggregate(entries),
        "per_model": per_model,
        "latency_ms_p50": _percentile(clean_latencies, 50),
        "latency_ms_p95": _percentile(clean_latencies, 95),
    }


def latency_cross_check(
    recorder_entries: list[dict[str, Any]],
    proxy_entries: list[dict[str, Any]],
    *,
    tolerance_s: float = 30.0,
) -> dict[str, Any] | None:
    """Сверка двух источников латентности (§9/§10), available only when
    the run went through the proxy AND kept the §5 recorder enabled.

    The proxy measures request-received → response-complete; the recorder
    measures request-started → usage-final. The SAME HTTP request is on
    both sides: the recorder logs one line per successful model request,
    the proxy relays it and logs its own line. Matching pairs nearest
    completion timestamps within `tolerance_s` (both stamps are written
    when the response is done — the two clocks are the same host's);
    latency deltas over the matched pairs bound the instrumentation
    overhead itself."""
    if not recorder_entries or not proxy_entries:
        return None

    ok_proxy = [
        rec
        for rec in proxy_entries
        if not rec.get("fault") and not rec.get("error") and rec.get("status") == 200
    ]
    ok_rec = [rec for rec in recorder_entries if not rec.get("error")]

    used = [False] * len(ok_proxy)
    deltas: list[float] = []
    for rec in ok_rec:
        rec_t = rec.get("ts")
        if not isinstance(rec_t, (int, float)):
            continue
        rec_lat = rec.get("latency_ms")
        if not isinstance(rec_lat, (int, float)):
            continue
        best_i, best_dt = None, None
        for i, proxy_rec in enumerate(ok_proxy):
            if used[i]:
                continue
            p_t = proxy_rec.get("ts")
            if not isinstance(p_t, (int, float)):
                continue
            dt = abs(p_t - rec_t)
            if dt > tolerance_s:
                continue
            if best_dt is None or dt < best_dt:
                best_i, best_dt = i, dt
        if best_i is not None:
            used[best_i] = True
            p_lat = ok_proxy[best_i].get("latency_ms")
            if isinstance(p_lat, (int, float)):
                deltas.append(float(p_lat) - float(rec_lat))
    if not deltas:
        return {
            "tolerance_s": tolerance_s,
            "recorder_requests": len(ok_rec),
            "proxy_requests": len(ok_proxy),
            "matched": 0,
            "remark": (
                "no recorder↔proxy pairs matched — the two sources stayed inconsistent for this run"
            ),
        }
    return {
        "tolerance_s": tolerance_s,
        "recorder_requests": len(ok_rec),
        "proxy_requests": len(ok_proxy),
        "matched": len(deltas),
        "delta_ms_p50": _percentile(deltas, 50),
        "delta_ms_max": round(max(abs(d) for d in deltas), 1),
        "remark": (
            "proxy latency − recorder latency over matched requests; a "
            "small positive delta is the proxy's own overhead"
        ),
    }


# --- user simulator log (§6/§10) --------------------------------------------

# Actions of bench/user_sim.py that actually mutated task state through
# the public TaskManager API — the report's "вмешательств симулятора".
# Kept as a literal (not imported from bench.user_sim) so this module
# stays import-free: it must keep working on any snapshot without
# pulling drcode into the process.
USER_SIM_INTERVENTION_ACTIONS = ("clarification_answer", "followup", "stuck_nudge")


def read_user_sim_entries(run_dir: Path) -> list[dict[str, Any]]:
    """Raw records of `user_sim.jsonl` (simulator §6), corrupt lines
    skipped. Missing file → empty list (a run without the simulator)."""
    path = run_dir / "user_sim.jsonl"
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out


def analyze_user_sim(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate the simulator log (§6/§10): how many interventions were
    made (and of which kind) and which scenario failures it recorded —
    the report must be able to tell "the model is dumb" from "the
    simulator intervened"."""
    by_action: dict[str, int] = {}
    for rec in entries:
        action = str(rec.get("action") or "unknown")
        by_action[action] = by_action.get(action, 0) + 1
    interventions = sum(by_action.get(a, 0) for a in USER_SIM_INTERVENTION_ACTIONS)
    failures = [
        str((rec.get("detail") or {}).get("reason") or rec.get("detail") or "unknown")
        for rec in entries
        if rec.get("action") == "failure"
    ]
    return {
        "file": "user_sim.jsonl",
        "records": len(entries),
        "interventions": interventions,
        "by_action": by_action,
        "failures": failures,
    }


# --- recorder ↔ transcript cross-check (§10) -------------------------------


def transcript_responses(task: dict[str, Any]) -> list[dict[str, Any]]:
    """Every completed model response persisted for one task, with the
    source transcript it came from: the coder transcript (`messages`)
    and each tester round (`tester_messages`). The compaction agent's
    responses are NOT persisted (§1.5) — that asymmetry is exactly what
    the cross-check below accounts for."""
    out: list[dict[str, Any]] = []
    for source, groups in (
        ("coder", [task.get("messages") or []]),
        ("tester", task.get("tester_messages") or []),
    ):
        for group in groups:
            for msg in group:
                if not _is_response(msg):
                    continue
                usage = usage_of(msg)
                if usage is None:
                    continue  # an attempt that never completed
                out.append(
                    {
                        "source": source,
                        "ts": dt_or(message_time(msg)),
                        "input_tokens": usage["input_tokens"],
                        "output_tokens": usage["output_tokens"],
                    }
                )
    return out


def cross_check_usage(
    responses: list[dict[str, Any]],
    entries: list[dict[str, Any]],
    *,
    n_compactions_started: int = 0,
    tolerance_s: float = 60.0,
) -> dict[str, Any]:
    """Сверка (§10): every token the recorder billed must be either a
    transcript response or a compaction-agent request (whose response
    is never persisted, §1.5); every transcript response must have been
    billed by the recorder.

    Matching pairs a transcript response with a recorder entry by equal
    (input_tokens, output_tokens) and |Δt| ≤ tolerance_s — the same
    ModelResponse object is on both sides, so the token pairs coincide
    exactly and the timestamps are milliseconds apart. Unmatched
    recorder entries are expected to be compaction requests (their
    count vs `n_compactions_started` is reported); anything beyond
    that — or ANY unmatched transcript response — is an unexplained
    discrepancy the metrics consumer must see.
    """
    used = [False] * len(entries)
    unmatched_transcript: list[dict[str, Any]] = []
    matched = 0

    def rec_ts(rec: dict[str, Any]) -> float | None:
        raw = rec.get("ts")
        if isinstance(raw, (int, float)):
            return float(raw)
        dt = parse_ts(raw)
        return dt.timestamp() if dt else None

    for resp in sorted(responses, key=lambda r: r["ts"] or ""):
        resp_ts = parse_ts(resp["ts"])
        best_i, best_dt = None, None
        for i, rec in enumerate(entries):
            if used[i] or rec.get("error"):
                continue
            usage = rec.get("usage")
            if not isinstance(usage, dict):
                continue
            if (
                int(usage.get("input_tokens") or 0) != resp["input_tokens"]
                or int(usage.get("output_tokens") or 0) != resp["output_tokens"]
            ):
                continue
            rec_t = rec_ts(rec)
            if resp_ts is None or rec_t is None:
                best_i, best_dt = i, 0.0  # token pair alone, stamps missing
                break
            dt = abs(rec_t - resp_ts.timestamp())
            if dt > tolerance_s:
                continue
            if best_dt is None or dt < best_dt:
                best_i, best_dt = i, dt
        if best_i is not None:
            used[best_i] = True
            matched += 1
        else:
            unmatched_transcript.append(resp)

    unmatched_recorder: dict[str, dict[str, int]] = {}
    for i, rec in enumerate(entries):
        if used[i] or rec.get("error"):
            continue
        role = str(rec.get("role") or "unknown")
        acc = unmatched_recorder.setdefault(
            role, {"requests": 0, "input_tokens": 0, "output_tokens": 0}
        )
        acc["requests"] += 1
        usage = rec.get("usage")
        if isinstance(usage, dict):
            acc["input_tokens"] += int(usage.get("input_tokens") or 0)
            acc["output_tokens"] += int(usage.get("output_tokens") or 0)
    errored = sum(1 for rec in entries if rec.get("error"))

    tokens_transcript = {
        "input_tokens": sum(r["input_tokens"] for r in responses),
        "output_tokens": sum(r["output_tokens"] for r in responses),
    }
    tokens_recorder = {
        "input_tokens": sum(
            int(rec.get("usage", {}).get("input_tokens") or 0)
            for rec in entries
            if not rec.get("error") and isinstance(rec.get("usage"), dict)
        ),
        "output_tokens": sum(
            int(rec.get("usage", {}).get("output_tokens") or 0)
            for rec in entries
            if not rec.get("error") and isinstance(rec.get("usage"), dict)
        ),
    }
    n_unmatched_recorder = sum(a["requests"] for a in unmatched_recorder.values())
    unexplained_transcript = len(unmatched_transcript)
    # Compaction requests have no transcript counterpart; a failed
    # compaction (no persisted summary either) can leave several.
    unexplained_recorder = max(0, n_unmatched_recorder - n_compactions_started)

    return {
        "tolerance_s": tolerance_s,
        "transcript_responses": len(responses),
        "recorder_entries": len(entries),
        "recorder_errored": errored,
        "matched": matched,
        "unmatched_transcript": unmatched_transcript,
        "unmatched_recorder": unmatched_recorder,
        "n_unmatched_recorder": n_unmatched_recorder,
        "n_compactions_started": n_compactions_started,
        "tokens": {
            "transcript": tokens_transcript,
            "recorder": tokens_recorder,
            "delta_input": tokens_recorder["input_tokens"] - tokens_transcript["input_tokens"],
            "delta_output": tokens_recorder["output_tokens"] - tokens_transcript["output_tokens"],
        },
        "unexplained": unexplained_transcript > 0 or unexplained_recorder > 0,
        "explanation": (
            "compaction-agent responses are not persisted (§1.5), and "
            "mid-run/mid-round compaction REMOVES the pre-compaction "
            "responses from the transcript — unmatched recorder entries ≈ "
            "compaction requests + responses compacted away"
        ),
    }


def _verdict(result: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
    """Overall verdict of the run: the harness verdict (settle + checks.py)
    plus the tester's own label — 'green' only when everything agrees."""
    if not result:
        return "unknown"
    ok = bool(result.get("ok"))
    checks = result.get("checks_ok")
    verified = all(t.get("verification") in (None, "Verified successfully") for t in tasks)
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
    raw_tasks: list[dict[str, Any]] = []
    context_limits = read_context_limits(run_dir)
    log_entries = read_model_log_entries(run_dir)
    tester_tag = _tester_role_tag(run_dir) if context_limits else None
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
            raw_tasks.append(raw)
            tasks.append(
                analyze_task(
                    raw,
                    context_limits=context_limits,
                    log_entries=log_entries,
                    tester_tag=tester_tag,
                )
            )

    # Simulator §6 (§10): interventions and scenario failures of the user
    # simulator — None for runs that predate the simulator.
    user_sim_entries = read_user_sim_entries(run_dir)
    user_sim = analyze_user_sim(user_sim_entries) if user_sim_entries else None

    totals = {
        "n_tasks": len(tasks),
        "n_bug_tasks": sum(1 for t in tasks if t["kind"] == "bug"),
        "n_testing_rounds": sum(t["testing"]["n_rounds"] for t in tasks),
        "n_compactions": sum(t["compactions"]["n_succeeded"] for t in tasks),
        "n_compactions_started": sum(t["compactions"]["n_started"] for t in tasks),
        # Repeat compaction (§10: degradation after summary) and the
        # compaction-failed state (§1.2: never fatal — gate off, run
        # continues uncompressed; the report must surface both).
        "n_repeat_compactions": sum(1 for t in tasks if t["compactions"]["repeat_compaction"]),
        "n_summaries": sum(t["compactions"]["n_summaries_in_transcript"] for t in tasks),
        "usage": _sum_usage(tasks),
        "stability": {
            "compaction_failed": sum(t["stability"]["compaction_failed"] for t in tasks),
            "tester_failed": sum(t["stability"]["tester_failed"] for t in tasks),
            "network_retries": sum(t["stability"]["network_retries"] for t in tasks),
            "unfinished": sum(1 for t in tasks if t["stability"]["unfinished"]),
            "pending_clarification": sum(
                1 for t in tasks if t["stability"]["pending_clarification"]
            ),
            "excluded_from_queue": sum(t["stability"]["excluded_from_queue"] for t in tasks),
        },
        "user_sim_interventions": user_sim["interventions"] if user_sim else 0,
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

    # Tester-threshold source (§1.2, S4): since drcode 0.5.0 the tester's
    # compaction threshold comes from the TESTER model's config (per-role
    # resolution) — verified here, not assumed. False = a threshold computed
    # from the coding model's config (a regression). None = no tester
    # compaction to classify (or only unclassified observations).
    tester_sources = [
        t["compactions"]["tester_threshold"] for t in tasks if t["compactions"]["tester_threshold"]
    ]
    if not tester_sources:
        tester_threshold_from_tester: bool | None = None
    elif any(s["source"] in ("coding", "mixed") for s in tester_sources):
        tester_threshold_from_tester = False
    elif any(s["source"] == "tester" for s in tester_sources):
        tester_threshold_from_tester = True
    else:
        tester_threshold_from_tester = None  # only unclassified observations

    # Coder/tester activity diagnostics (§7 S6, passive): overlap facts
    # never gate the verdict — in multi-task runs they are legitimate.
    gate = analyze_gate(raw_tasks, log_entries)

    # Recorder §5 (§10): per-role requests/latency/tokens, plus the
    # cross-check of the recorder's billing against the usage persisted
    # in the task transcripts (compaction responses are not persisted —
    # §1.5 — so unmatched recorder entries ≈ compaction requests).
    model_log = _load_model_log(run_dir, log_entries)
    usage_cross_check: dict[str, Any] | None = None
    if log_entries:
        usage_cross_check = cross_check_usage(
            [r for raw in raw_tasks for r in transcript_responses(raw)],
            log_entries,
            n_compactions_started=totals["n_compactions_started"],
        )

    # Proxy §9 (§10): the alternative per-request latency source plus the
    # replay of the injected fault script; when the recorder was enabled
    # too, the two latency sources are cross-checked against each other.
    proxy_entries = read_proxy_log_entries(run_dir)
    proxy = analyze_proxy(proxy_entries)
    latency_check: dict[str, Any] | None = None
    if log_entries and proxy_entries:
        latency_check = latency_cross_check(log_entries, proxy_entries)

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
            # Non-verdict facts from checks.py stdout (`S9 metric:
            # report_committed=true`, bench/run_one.CHECKS_METRIC_RE):
            # e.g. s9's commit discipline is measured, not gated — the
            # report renders it as its own `report_committed` column.
            "checks_metrics": result.get("checks_metrics") or {},
            "settle_elapsed_s": result.get("settle_elapsed_s"),
            "started_at": result.get("started_at"),
            "finished_at": result.get("finished_at"),
            "resolved_roles": result.get("resolved_roles") or {},
            # §9 stall watchdog: config + counters when the mode was
            # active for this run (None = clean run, no masking).
            "proxy_watchdog": result.get("proxy_watchdog"),
        },
        "wall_time_s": {
            "settle": result.get("settle_elapsed_s"),
            "run": seconds_between(
                parse_ts(result.get("started_at")), parse_ts(result.get("finished_at"))
            ),
        },
        "totals": totals,
        "bug_round_trips": bug_round_trips,
        "gate": gate,
        "context_limits": context_limits or None,
        "tester_threshold_from_tester": tester_threshold_from_tester,
        "tasks": tasks,
        "model_log": model_log,
        "proxy": proxy,
        "latency_cross_check": latency_check,
        "user_sim": user_sim,
        "usage_cross_check": usage_cross_check,
    }
    if write:
        out = run_dir / "metrics.json"
        out.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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
