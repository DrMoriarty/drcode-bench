"""Report aggregation: runs/ → report.md (plan drcode-bench.md, §10).

    python -m bench report runs/           # → runs/report.md
    python -m bench report runs/ --html    # + report.html

The summary table is combo × scenario (§10): rows — median wall-time,
median/sum tokens per role, verdict, number of compactions — with the
spread over the repeats (min…max). Every cell would otherwise repeat the
same link, so only the run count points to the pair's representative run
(`runs/<run_id>/`, the median-wall repeat).

The per-run table links the artifacts of every run (metrics.json,
result.json, the run dir) so each run stays reproducibly dissectible.

The terse codes of the gate/stability columns are spelled out in a
Glossary section (§10) and as `<abbr title=...>` hover tooltips in the
HTML rendering.
"""

from __future__ import annotations

import json
import re
import statistics
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .metrics import MetricsError, extract_run_metrics

SCHEMA = "report/v1"

# §10: the terse codes of the `gate` and `stability` columns, spelled out
# both in the report's Glossary section (`_glossary_lines`) and as hover
# tooltips in the HTML rendering (`_glossary_abbr`). Keys match the cell
# labels; the counted `label×N` form (`net-retry×3`) is matched by the
# label prefix.
GLOSSARY: dict[str, str] = {
    "ok": (
        "the gate 'no development while testing is in flight' held: coder "
        "and tester activity intervals never overlapped (verified from "
        "transcripts and model_log.jsonl)"
    ),
    "OVERLAP": (
        "gate violation: coder and tester activity overlapped (see the "
        "per-run GATE VIOLATION block in Run details)"
    ),
    "faults": (
        "faults injected by the proxy fault script (s7 [proxy] runs / "
        "--use-proxy); the retries they caused appear alongside as net-retry"
    ),
    "compact-fail": (
        "compaction failed: drcode does not abort — it disables the "
        "compaction gate (`_compaction_failed`) and continues with the "
        "UNCOMPRESSED history (summaries may be missing from transcripts)"
    ),
    "tester-fail": "tester failures",
    "net-retry": "drcode retried a failed model request",
    "unfinished": "task not finished by the end of the run",
    "stuck-clarif": "task left pending clarification",
    "excluded": "task excluded from the queue",
    "clean": "none of the above",
}

# Which column each glossary term belongs to (for the Glossary section).
_GLOSSARY_COLUMN: dict[str, str] = {
    "ok": "gate",
    "OVERLAP": "gate",
    **{t: "stability" for t in GLOSSARY if t not in ("ok", "OVERLAP")},
}

# Terms always carrying a count in the cells — shown in the glossary with
# the `label×N` form (`faults×N`); the others appear bare at count 1.
_GLOSSARY_COUNTED = frozenset({"faults", "compact-fail", "tester-fail", "net-retry"})


def _glossary_lines() -> list[str]:
    """The '## Glossary' section: one line per terse code, in column order."""
    lines = [
        "## Glossary",
        "",
        "Meaning of the codes in the `gate` and `stability` columns:",
        "",
    ]
    for term, definition in GLOSSARY.items():
        label = f"{term}×N" if term in _GLOSSARY_COUNTED else term
        lines.append(f"- {_GLOSSARY_COLUMN[term]} `{label}` — {definition}")
    return lines


# Longest-first alternation so no term shadows a prefix of another; the
# lookarounds keep whole-label matching (a term must not light up inside
# a longer word, but `net-retry×3` and `OVERLAP ⚠` must match).
_GLOSSARY_TERM_RE = re.compile(
    rf"(?<![\w-])({'|'.join(re.escape(t) for t in sorted(GLOSSARY, key=len, reverse=True))})"
    r"(×\d+)?(?![\w-])"
)


def _glossary_abbr(rendered: str) -> str:
    """Wrap the known gate/stability terms of an already-rendered cell in
    `<abbr title=...>` hover tooltips (§10: the codes are always
    interpretable, not only in the Glossary section). The visible text
    keeps its `_md_inline` escaping (the terms are plain words, so
    escaping is a no-op on them); the `title` attribute is escaped
    separately."""
    import html as _html

    def _repl(m: re.Match[str]) -> str:
        term = m.group(1)
        title = _html.escape(GLOSSARY[term], quote=True)
        return f'<abbr title="{title}">{m.group(0)}</abbr>'

    return _GLOSSARY_TERM_RE.sub(_repl, rendered)


def _fmt(value: Any, suffix: str = "") -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:g}{suffix}"
    return f"{value}{suffix}"


def discover_runs(runs_dir: Path) -> list[Path]:
    """Run directories = subdirs of runs_dir holding result.json and/or
    metrics.json (sorted for a stable report)."""
    if not runs_dir.is_dir():
        return []
    out = []
    for path in sorted(p for p in runs_dir.iterdir() if p.is_dir()):
        if (path / "result.json").is_file() or (path / "metrics.json").is_file():
            out.append(path)
    return out


def load_run(run_dir: Path) -> dict[str, Any]:
    """Metrics of one run: reuse metrics.json when fresh enough, extract
    otherwise (extraction is idempotent and cheap — reading local JSON)."""
    metrics_file = run_dir / "metrics.json"
    if metrics_file.is_file():
        try:
            return json.loads(metrics_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass  # corrupted — re-extract below
    try:
        return extract_run_metrics(run_dir)
    except MetricsError as e:
        return {
            "schema": "metrics/v1",
            "run_id": run_dir.name,
            "scenario": None,
            "combo": None,
            "verdict": "unknown",
            "totals": {},
            "wall_time_s": {},
            "tasks": [],
            "error": str(e),
        }


def _stability_flags(metrics: dict[str, Any]) -> str:
    """Compact stability signature of a run, e.g. `compact-fail×2 net×3`."""
    st = (metrics.get("totals") or {}).get("stability") or {}
    parts = []
    # §9: the injected fault script of a proxy run belongs in the same
    # signature — the retries it caused are visible right next to it.
    proxy_faults = ((metrics.get("proxy") or {}).get("faults_injected")) or 0
    if proxy_faults:
        parts.append(f"faults×{proxy_faults}")
    for key, label in (
        ("compaction_failed", "compact-fail"),
        ("tester_failed", "tester-fail"),
        ("network_retries", "net-retry"),
        ("unfinished", "unfinished"),
        ("pending_clarification", "stuck-clarif"),
        ("excluded_from_queue", "excluded"),
    ):
        n = st.get(key) or 0
        if n:
            parts.append(f"{label}×{n}" if n > 1 else label)
    return ", ".join(parts) if parts else "clean"


def _model_log(m: dict[str, Any]) -> dict[str, Any]:
    return m.get("model_log") or {}


def _tokens_by_role(runs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Per-role token totals aggregated over the repeats of a pair
    (§10: recorder per-role prompt/completion sums, medians over runs).

    Recorder role tags are `model@base_url` (bench/recording.py); the
    `@base_url` part is stripped and entries of the same model are
    SUMMED within each run before the median — the s7 proxy gives each
    replica a distinct ephemeral port, which would otherwise fragment
    one model into several rows."""
    per_run: dict[str, list[tuple[int, int]]] = {}
    for m in runs:
        # Sum same-model entries within the run (replicas differ only in
        # the ephemeral base_url port), then collect one pair per run.
        sums: dict[str, tuple[int, int]] = {}
        for role, e in (_model_log(m).get("per_role") or {}).items():
            model = role.split("@", 1)[0].strip() or role
            prev = sums.get(model, (0, 0))
            sums[model] = (
                prev[0] + int(e.get("input_tokens") or 0),
                prev[1] + int(e.get("output_tokens") or 0),
            )
        for model, pair in sums.items():
            per_run.setdefault(model, []).append(pair)
    out: dict[str, dict[str, Any]] = {}
    for role, values in per_run.items():
        inputs = [v[0] for v in values]
        outputs = [v[1] for v in values]
        out[role] = {
            "n_runs": len(values),
            "input_tokens_median": round(statistics.median(inputs), 1),
            "output_tokens_median": round(statistics.median(outputs), 1),
        }
    return out


def _agg(values: list[float | int | None]) -> dict[str, Any]:
    """Spread-aware aggregate of one metric over the repeats of a pair
    (§10: medians/разброс; a single run is a repeat count of 1)."""
    known = [float(v) for v in values if v is not None]
    if not known:
        return {"n": len(values), "median": None, "min": None, "max": None}
    return {
        "n": len(values),
        "median": round(statistics.median(known), 1),
        "min": round(min(known), 1),
        "max": round(max(known), 1),
    }


def aggregate_pairs(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group runs by (scenario, combo) and aggregate the report metrics.

    Shape is repeat-ready: every pair carries `_agg` blocks for wall-time,
    compactions, testing rounds and the recorder's model traffic
    (requests, tokens per role — §10; latency p50/p95 stays per run in
    the run details); verdicts list all
    outcomes seen across the repeats (a pair is only as good as its worst
    repeat). `repr_run` is the median-wall repeat — the run whose
    artifacts the summary table links to."""
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for m in runs:
        key = (m.get("scenario") or "?", m.get("combo") or "?")
        groups.setdefault(key, []).append(m)

    pairs = []
    for (scenario, combo), group in sorted(groups.items()):
        wall = _agg([m.get("wall_time_s", {}).get("settle") for m in group])
        compactions = _agg([(m.get("totals") or {}).get("n_compactions") for m in group])
        rounds = _agg([(m.get("totals") or {}).get("n_testing_rounds") for m in group])
        round_trips = _agg([len(m.get("bug_round_trips") or []) for m in group])
        sim_interventions = _agg([(m.get("user_sim") or {}).get("interventions") for m in group])
        tokens = _agg(
            [((m.get("totals") or {}).get("usage") or {}).get("output_tokens") for m in group]
        )
        requests = _agg([_model_log(m).get("requests") for m in group])
        pairs.append(
            {
                "scenario": scenario,
                "combo": combo,
                "runs": [m.get("run_id") for m in group],
                "repr_run": _representative_run(group, wall),
                "verdicts": sorted({m.get("verdict") or "unknown" for m in group}),
                "wall_time_s": wall,
                "compactions": compactions,
                "testing_rounds": rounds,
                "bug_round_trips": round_trips,
                "sim_interventions": sim_interventions,
                "output_tokens": tokens,
                "model_requests": requests,
                "tokens_by_role": _tokens_by_role(group),
                "gate": sorted({((m.get("gate") or {}).get("verdict") or "n/a") for m in group}),
                "stability": sorted({_stability_flags(m) for m in group} - {"clean"}) or ["clean"],
            }
        )
    return pairs


def _representative_run(group: list[dict[str, Any]], wall: dict[str, Any]) -> str | None:
    """The run whose artifacts the summary table links to: the median-wall
    repeat (the first run when the median is not a member / single run)."""
    median = wall.get("median")
    for m in group:
        if median is not None and m.get("wall_time_s", {}).get("settle") == median:
            return m.get("run_id")
    return group[0].get("run_id") if group else None


def _run_count_cell(p: dict[str, Any]) -> str:
    """The summary table's single link per row: the run count points to
    the artifacts of the pair's representative run (§10/DoD:
    runs/<run_id>/ is one click away from the aggregate figures)."""
    run_id = p.get("repr_run")
    if not run_id:
        return str(p["wall_time_s"]["n"])
    # The report always lives inside runs_dir itself (runs/report.md), so
    # the link is relative to the report's own directory — no `runs/`
    # prefix (that would resolve to runs/runs/<run_id>/ in a browser).
    return f"[{p['wall_time_s']['n']}]({run_id}/)"


def _thousands(value: Any) -> str:
    """Integer with thin-space thousands separators (1316 → `1 316`);
    `—` for missing values."""
    if value is None:
        return "—"
    return f"{int(value):,}".replace(",", "\u202f")


def _sec_whole(value: Any) -> str:
    """Whole seconds, unit omitted (it lives in the column header)."""
    return "—" if value is None else str(round(float(value)))


def _sec_1dec(value: Any) -> str:
    """Wall-time with one decimal, unit attached (per-run rows)."""
    return "—" if value is None else f"{float(value):.1f} s"


def _with_spread(agg: dict[str, Any], fmt: Callable[[Any], str] = _fmt) -> str:
    """A summary-table cell: the median, with the min–max spread over the
    repeats in parentheses when it exists (`23 (19–26)`). The unit lives
    in the column header, not in the cell; in the HTML rendering the
    spread moves to a second line of the cell (see `_md_to_html`)."""
    text = fmt(agg["median"])
    if agg["n"] > 1 and agg["min"] != agg["max"]:
        text += f" ({fmt(agg['min'])}–{fmt(agg['max'])})"
    return text


def _pair_rows(pairs: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| scenario | combo | runs | verdicts | wall-time (median, s) | "
        "compactions (med) | testing rounds (med) | bug round-trips (med) | "
        "sim interventions (med) | output tokens (med) | "
        "model requests (med) | tokens by role (med, prompt/compl.) | gate | stability |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for p in pairs:
        tokens_by_role = "; ".join(
            f"{role}: {_thousands(v['input_tokens_median'])}/{_thousands(v['output_tokens_median'])}"
            for role, v in p["tokens_by_role"].items()
        )
        lines.append(
            f"| {p['scenario']} | {p['combo']} | {_run_count_cell(p)} "
            f"| {', '.join(p['verdicts'])} "
            f"| {_with_spread(p['wall_time_s'], _sec_whole)} "
            f"| {_with_spread(p['compactions'])} "
            f"| {_fmt(p['testing_rounds']['median'])} "
            f"| {_fmt(p['bug_round_trips']['median'])} "
            f"| {_fmt(p['sim_interventions']['median'])} "
            f"| {_with_spread(p['output_tokens'], _thousands)} "
            f"| {_fmt(p['model_requests']['median'])} "
            f"| {tokens_by_role or '—'} "
            f"| {', '.join(p['gate'])} "
            f"| {', '.join(p['stability'])} |"
        )
    return lines


def _run_rows(runs: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| run | scenario | combo | verdict | wall-time | checks | compactions "
        "(ok/started/failed) | testing rounds | sim interventions | tasks | gate | stability | artifacts |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for m in runs:
        run_id = m.get("run_id") or "?"
        rel = run_id  # report sits in runs_dir → links relative to it
        checks = m.get("result", {}).get("checks_ok")
        checks_str = {True: "green", False: "RED", None: "n/a"}.get(
            checks if checks is None else bool(checks), "n/a"
        )
        comp = m.get("totals", {})
        comp_str = (
            f"{_fmt(comp.get('n_compactions'))}/{_fmt(comp.get('n_compactions_started'))}"
            f"/{_fmt(comp.get('stability', {}).get('compaction_failed'))}"
        )
        sim = m.get("user_sim") or {}
        sim_str = _fmt(sim.get("interventions"))
        if sim.get("failures"):
            sim_str += " ⚠"
        tasks = m.get("tasks") or []
        verdicts = (
            "/".join(f"{t.get('kind')}:{t.get('verification') or t.get('status')}" for t in tasks)
            or "—"
        )
        gate = (m.get("gate") or {}).get("verdict") or "n/a"
        if gate == "OVERLAP":
            gate += " ⚠"
        lines.append(
            f"| [{run_id}]({rel}/) | {_fmt(m.get('scenario'))} | {_fmt(m.get('combo'))} "
            f"| {_fmt(m.get('verdict'))} | {_sec_1dec(m.get('wall_time_s', {}).get('settle'))} "
            f"| {checks_str} | {comp_str} "
            f"| {_fmt(comp.get('n_testing_rounds'))} | {sim_str} | {verdicts} "
            f"| {gate} "
            f"| {_stability_flags(m)} "
            f"| [metrics]({rel}/metrics.json) · [result]({rel}/result.json) |"
        )
    return lines


def _run_details(runs: list[dict[str, Any]]) -> list[str]:
    """Per-run dissection blocks: phase timings, compaction savings,
    bug round-trips — everything needed to read a run without rerunning."""
    lines: list[str] = []
    for m in runs:
        run_id = m.get("run_id") or "?"
        rel = run_id  # report sits in runs_dir → links relative to it
        lines.append(f"### {run_id} — {_fmt(m.get('scenario'))} × {_fmt(m.get('combo'))}\n")
        reason = m.get("result", {}).get("reason")
        if reason:
            lines.append(f"Reason: `{reason}`\n")
        lines.append("| task | kind | status | verification | dev s | testing s | total s |")
        lines.append("|---|---|---|---|---|---|---|")
        for t in m.get("tasks") or []:
            ph = t.get("phases", {})
            lines.append(
                f"| {t.get('title')} | {t.get('kind')} | {t.get('status')} "
                f"| {_fmt(t.get('verification'))} "
                f"| {_fmt(ph.get('dev_s'))} | {_fmt(ph.get('testing_s'))} "
                f"| {_fmt(ph.get('total_s'))} |"
            )
        lines.append("")
        # Compaction health of the run (§1.2/§10): "compaction failed" is
        # never fatal in drcode — the gate is disabled (`_compaction_failed`)
        # and the run continues UNCOMPRESSED — but the benchmark must
        # recognize and surface that state, plus repeat compactions (the
        # summary did not stick → degradation signal).
        comp_failed = (m.get("totals", {}).get("stability", {}) or {}).get("compaction_failed") or 0
        if comp_failed:
            lines.append(
                f"⚠ COMPACTION FAILED ×{comp_failed}: drcode disabled the "
                "compaction gate (`_compaction_failed`) and the run "
                "continued with the UNCOMPRESSED history — summaries may "
                "be missing from the transcripts.\n"
            )
        if (m.get("totals") or {}).get("n_repeat_compactions"):
            lines.append(
                "⚠ Repeat compaction (§10): a context was compacted more "
                "than once — degradation after the summary.\n"
            )
        # The development/testing gate (§7 S6): coder and tester must never
        # be in flight at the same time — verified from the transcripts
        # and, when the recorder separates the roles, from model_log.jsonl.
        gate = m.get("gate")
        if gate and gate.get("verdict") == "OVERLAP":
            lines.append(
                "⚠ GATE VIOLATION: coder and tester activity overlapped — "
                "the pipeline gate 'no development while testing is in "
                "flight' did not hold.\n"
            )
            for o in gate.get("overlaps") or []:
                lines.append(f"- {o}")
            lines.append("")
        ttt = m.get("tester_threshold_from_tester")
        if ttt is not None:
            flag = (
                "as expected (drcode ≥ 0.5.0: per-role config, §1.2)"
                if ttt
                else "REGRESSION — threshold came from the coding model"
            )
            lines.append(
                f"Tester compaction threshold source: {'tester' if ttt else 'NOT tester'} "
                f"model config — {flag}."
            )
            lines.append("")
        savings = [s for t in m.get("tasks") or [] for s in (t.get("compaction_savings") or [])]
        if savings:
            lines.append("Compaction savings (token estimates from response usage):\n")
            lines.append(
                "| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |"
            )
            lines.append("|---|---|---|---|---|---|---|")
            for s in savings:
                lines.append(
                    f"| {_fmt(s.get('at'))} | {_fmt(s.get('trigger_pct'))} "
                    f"| {_fmt(s.get('pre_tokens_est'))} | {_fmt(s.get('post_tokens_est'))} "
                    f"| {_fmt(s.get('saved_tokens_est'))} | {_fmt(s.get('summary_chars'))} "
                    f"| {_fmt(s.get('prompts_kept'))} |"
                )
            lines.append("")
        if m.get("bug_round_trips"):
            lines.append("Bug round-trips:\n")
            for b in m["bug_round_trips"]:
                lines.append(f"- `{b['id']}` {b['title']} (activated {b['activated_at']})")
            lines.append("")
        sim = m.get("user_sim")
        if sim:
            by_action = ", ".join(
                f"{action}: {n}" for action, n in sorted(sim.get("by_action", {}).items())
            )
            lines.append(
                f"User-simulator interventions: {sim.get('interventions', 0)} "
                f"({by_action or 'none'})"
            )
            for failure in sim.get("failures") or []:
                lines.append(f"- SIM FAILURE: {failure}")
            lines.append("")
        model_log = m.get("model_log")
        if model_log:
            lines.append("Model usage per role (recorder):\n")
            lines.append(
                "| role | requests | latency total s | latency p50 s | latency p95 s "
                "| input tok | output tok |"
            )
            lines.append("|---|---|---|---|---|---|---|")
            for role, e in model_log.get("per_role", {}).items():
                lines.append(
                    f"| {role} | {e['requests']} "
                    f"| {_fmt(e['latency_ms_total'] / 1000)} "
                    f"| {_fmt((e.get('latency_ms_p50') or 0) / 1000)} "
                    f"| {_fmt((e.get('latency_ms_p95') or 0) / 1000)} "
                    f"| {e.get('input_tokens', 0)} | {e.get('output_tokens', 0)} |"
                )
            lines.append("")
            lines.append(
                f"Overall: {model_log.get('requests', 0)} model requests, "
                f"latency p50 {_fmt((model_log.get('latency_ms_p50') or 0) / 1000, ' s')} / "
                f"p95 {_fmt((model_log.get('latency_ms_p95') or 0) / 1000, ' s')}."
            )
            cross = m.get("usage_cross_check")
            if cross:
                flag = (
                    "UNEXPLAINED DISCREPANCIES"
                    if cross.get("unexplained")
                    else "no unexplained discrepancies"
                )
                lines.append(
                    f"Recorder ↔ transcript cross-check: {cross['matched']}/"
                    f"{cross['transcript_responses']} transcript responses matched, "
                    f"{cross['n_unmatched_recorder']} unmatched recorder entries "
                    f"(compaction requests, §1.5) — {flag}."
                )
            lines.append("")
        lines.append(f"Artifacts: `{rel}/`\n")
    return lines


def generate_report(runs_dir: Path, out: Path | None = None, *, html: bool = False) -> Path:
    """Scan `runs_dir`, extract missing metrics, write the markdown report
    (and, with `html=True`, an HTML rendering next to it).
    Returns the path of the written markdown report
    (default: `<runs_dir>/report.md`)."""
    runs_dir = Path(runs_dir)
    out = out or (runs_dir / "report.md")

    run_dirs = discover_runs(runs_dir)
    runs = [load_run(d) for d in run_dirs]
    pairs = aggregate_pairs(runs)

    lines = [
        "# drcode-bench report",
        "",
        f"Generated: {datetime.now(UTC).isoformat(timespec='seconds')}  ",
        f"Runs dir: `{runs_dir}` · runs: {len(runs)} · pairs: {len(pairs)}",
        "",
        "## Summary (scenario × combo)",
        "",
        "Medians over the repeats of each pair; a single run is a repeat count of 1. "
        "The run count links to the artifacts of the pair's median-wall run.",
        "",
        *_pair_rows(pairs),
        "",
        "## Runs",
        "",
        *_run_rows(runs),
        "",
        "## Run details",
        "",
        *_run_details(runs),
        "",
        # §10: the terse gate/stability codes of the tables above, spelled
        # out at the end of the report.
        *_glossary_lines(),
    ]
    report = "\n".join(lines).rstrip() + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    if html:
        html_path = out.with_suffix(".html")
        html_path.write_text(_md_to_html(report), encoding="utf-8")
    return out


# --- minimal markdown → HTML rendering (no extra dependencies) -----------------


def _md_inline(text: str) -> str:
    """Inline markdown: escape, `code`, **bold**, [text](url)."""
    import html as _html
    import re as _re

    text = _html.escape(text, quote=False)
    text = _re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>',
        text,
    )
    text = _re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = _re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def _verdict_row_class(cell: str) -> str | None:
    """CSS class for a table row, derived from the text of its verdict
    cell: green-only → `verdict-ok`, failed-only → `verdict-fail`,
    a mix of both (one combo with correct and failed repeats) →
    `verdict-mixed`; anything else (`settled-but-flagged`, `unknown`,
    missing column) stays uncoloured.
    Summary-table verdict cells carry no markdown links (only the run
    count cell does), but the stripping keeps the helper safe either
    way."""
    stripped = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell)
    verdicts = {v.strip() for v in stripped.split(",")}
    has_ok = "green" in verdicts
    has_fail = "failed" in verdicts
    if has_ok and has_fail:
        return "verdict-mixed"
    if has_fail:
        return "verdict-fail"
    if has_ok:
        return "verdict-ok"
    return None


# Summary-table spread cells (`23 (19–26)`, thousands separated by
# thin spaces) — rendered in HTML as the median on the first line and
# the min–max spread on a small gray second line.
_SPREAD_CELL_RE = re.compile(r"^(\d[\d\u202f ]*) \((\d[\d\u202f ]*–\d[\d\u202f ]+)\)$")
_PLAIN_NUMBER_RE = re.compile(r"^\d+([\u202f ]\d+)*$")


def _render_cell(cell: str, *, summary: bool, glossary: bool = False) -> str:
    """One table cell → HTML: inline markdown, plus (summary tables only)
    the two-line spread layout and right alignment for numeric cells, plus
    (gate/stability cells only) `<abbr>` hover tooltips from GLOSSARY."""
    rendered = _md_inline(cell)
    if summary:
        m = _SPREAD_CELL_RE.match(cell)
        if m:
            return (
                f'{_md_inline(m.group(1))}<br><span class="spread">{_md_inline(m.group(2))}</span>'
            )
        if _PLAIN_NUMBER_RE.match(cell):
            return f'<span class="num">{rendered}</span>'
    return _glossary_abbr(rendered) if glossary else rendered


def _md_to_html(md: str) -> str:
    """A small renderer for the report's own markdown subset: headings,
    paragraphs, `- ` lists and pipe tables. Enough for report.html without
    pulling in a markdown dependency."""
    out: list[str] = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8">',
        "<title>drcode-bench report</title>",
        "<style>",
        "body{font-family:system-ui,sans-serif;margin:2rem;max-width:160rem;}",
        "table{border-collapse:collapse;margin:1rem 0;}",
        "th,td{border:1px solid #bbb;padding:4px 10px;text-align:left;vertical-align:top;}",
        "th{background:#f4f4f4;}",
        "code{background:#f4f4f4;padding:0 4px;}",
        # Glossary hover tooltips (§10): make the <abbr> cells visibly
        # hoverable (dotted underline + help cursor).
        "abbr{cursor:help;text-decoration:underline dotted;}",
        # Summary-table spread cells: median on the first line, the
        # min–max spread on a small gray second line; numeric cells
        # right-aligned.
        ".spread{color:#777;font-size:0.85em;}",
        "td.num{text-align:right;}",
        # Verdict colouring (§10): pale green — all repeats green, pale red —
        # all repeats failed, pale yellow — a summary row mixing both.
        "tr.verdict-ok{background:#d9ead3;}",
        "tr.verdict-fail{background:#f4cccc;}",
        "tr.verdict-mixed{background:#fff2cc;}",
        "h1,h2,h3{margin-top:1.6rem;}",
        "</style></head><body>",
    ]
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("### "):
            out.append(f"<h3>{_md_inline(line[4:])}</h3>")
            i += 1
        elif line.startswith("## "):
            out.append(f"<h2>{_md_inline(line[3:])}</h2>")
            i += 1
        elif line.startswith("# "):
            out.append(f"<h1>{_md_inline(line[2:])}</h1>")
            i += 1
        elif line.lstrip().startswith("|"):
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") and c for c in cells):
                    rows.append(cells)
                i += 1
            out.append("<table>")
            verdict_col: int | None = None
            # The two-line spread layout is a summary-table feature —
            # recognized by its wall-time header (the runs/dissection
            # tables have no spread cells to transform).
            is_summary = any(c == "wall-time (median, s)" for c in rows[0])
            # Tooltip hook: gate/stability columns of the summary/runs
            # tables get GLOSSARY hover tooltips on their terse codes
            # (the dissection tables have no such columns).
            glossary_cols = {
                c for c, cell in enumerate(rows[0]) if cell.lower() in ("gate", "stability")
            }
            for r, row in enumerate(rows):
                tag = "th" if r == 0 else "td"
                if r == 0:
                    # Colouring hook: locate the verdict column of the
                    # summary/runs tables (the dissection tables have none).
                    for c, cell in enumerate(row):
                        if cell.lower() in ("verdict", "verdicts"):
                            verdict_col = c
                            break
                cls = ""
                if r > 0 and verdict_col is not None and verdict_col < len(row):
                    row_cls = _verdict_row_class(row[verdict_col])
                    if row_cls:
                        cls = f' class="{row_cls}"'
                body = "".join(
                    f"<{tag}>{_render_cell(cell, summary=is_summary and r > 0, glossary=r > 0 and ci in glossary_cols)}</{tag}>"
                    for ci, cell in enumerate(row)
                )
                out.append(f"<tr{cls}>{body}</tr>")
            out.append("</table>")
        elif line.lstrip().startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                out.append(f"<li>{_md_inline(lines[i].lstrip()[2:])}</li>")
                i += 1
            out.append("</ul>")
        else:
            paragraph: list[str] = []
            while (
                i < len(lines)
                and lines[i].strip()
                and not lines[i].lstrip().startswith(("|", "- ", "# "))
            ):
                paragraph.append(_md_inline(lines[i]))
                i += 1
            if not paragraph:
                # An indented `#`/`- `/`|` line misses the unstripped
                # outer dispatch but the stripped exclusion above, so
                # the loop body never ran — emit it raw or `i` never
                # advances and the outer loop spins forever.
                paragraph.append(lines[i])
                i += 1
            out.append("<p>" + "<br>".join(paragraph) + "</p>")
    out.append("</body></html>")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    runs_dir = Path(args[0]) if args else Path("runs")
    if not runs_dir.is_dir():
        print(f"error: runs directory not found: {runs_dir}", file=sys.stderr)
        return 2
    out = generate_report(runs_dir)
    print(f"report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
