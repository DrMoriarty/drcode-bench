"""Report aggregation: runs/ → report.md (plan drcode-bench.md, §10).

    python -m bench report runs/        # → runs/report.md

One section per (scenario, combo) pair; today a pair has a single run
(no matrix/repeats yet — §12 stage 5), but the aggregation is already
built around medians/min/max over repeats: a pair with one run shows the
same table shape with spread columns that collapse to the single value.

The per-run table links the artifacts of every run (metrics.json,
result.json, the run dir) so each run stays reproducibly dissectible.
"""

from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .metrics import MetricsError, extract_run_metrics

SCHEMA = "report/v1"


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
    (§10: recorder per-role prompt/completion sums, medians over runs)."""
    per_run: dict[str, list[tuple[int, int]]] = {}
    for m in runs:
        log = _model_log(m)
        for role, e in (log.get("per_role") or {}).items():
            per_run.setdefault(role, []).append(
                (int(e.get("input_tokens") or 0), int(e.get("output_tokens") or 0))
            )
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
    (requests, latency p50/p95, tokens per role — §10); verdicts list all
    outcomes seen across the repeats (a pair is only as good as its worst
    repeat)."""
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for m in runs:
        key = (m.get("scenario") or "?", m.get("combo") or "?")
        groups.setdefault(key, []).append(m)

    pairs = []
    for (scenario, combo), group in sorted(groups.items()):
        wall = _agg([m.get("wall_time_s", {}).get("settle") for m in group])
        compactions = _agg(
            [(m.get("totals") or {}).get("n_compactions") for m in group]
        )
        rounds = _agg([(m.get("totals") or {}).get("n_testing_rounds") for m in group])
        round_trips = _agg([len(m.get("bug_round_trips") or []) for m in group])
        sim_interventions = _agg(
            [(m.get("user_sim") or {}).get("interventions") for m in group]
        )
        tokens = _agg(
            [
                ((m.get("totals") or {}).get("usage") or {}).get("output_tokens")
                for m in group
            ]
        )
        requests = _agg([_model_log(m).get("requests") for m in group])
        latency_p50 = _agg([_model_log(m).get("latency_ms_p50") for m in group])
        latency_p95 = _agg([_model_log(m).get("latency_ms_p95") for m in group])
        pairs.append(
            {
                "scenario": scenario,
                "combo": combo,
                "runs": [m.get("run_id") for m in group],
                "verdicts": sorted({m.get("verdict") or "unknown" for m in group}),
                "wall_time_s": wall,
                "compactions": compactions,
                "testing_rounds": rounds,
                "bug_round_trips": round_trips,
                "sim_interventions": sim_interventions,
                "output_tokens": tokens,
                "model_requests": requests,
                "latency_ms_p50": latency_p50,
                "latency_ms_p95": latency_p95,
                "tokens_by_role": _tokens_by_role(group),
                "stability": sorted(
                    {_stability_flags(m) for m in group} - {"clean"}
                )
                or ["clean"],
            }
        )
    return pairs


def _pair_rows(pairs: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| scenario | combo | runs | verdicts | wall-time (median, s) | "
        "compactions (med) | testing rounds (med) | bug round-trips (med) | "
        "sim interventions (med) | output tokens (med) | "
        "model requests (med) | latency p50/p95 (med, s) | "
        "tokens by role (med, prompt/compl.) | stability |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for p in pairs:
        wall = p["wall_time_s"]
        wall_str = _fmt(wall["median"], " s")
        if wall["n"] > 1 and wall["min"] != wall["max"]:
            wall_str += f" [{_fmt(wall['min'])}…{_fmt(wall['max'])}]"
        lat_p50 = p["latency_ms_p50"]
        lat_str = (
            f"{_fmt(lat_p50['median'] / 1000 if lat_p50['median'] is not None else None)} / "
            f"{_fmt(p['latency_ms_p95']['median'] / 1000 if p['latency_ms_p95']['median'] is not None else None)}"
        )
        tokens_by_role = "; ".join(
            f"{role}: {_fmt(v['input_tokens_median'])}/{_fmt(v['output_tokens_median'])}"
            for role, v in p["tokens_by_role"].items()
        )
        lines.append(
            f"| {p['scenario']} | {p['combo']} | {wall['n']} "
            f"| {', '.join(p['verdicts'])} "
            f"| {wall_str} "
            f"| {_fmt(p['compactions']['median'])} "
            f"| {_fmt(p['testing_rounds']['median'])} "
            f"| {_fmt(p['bug_round_trips']['median'])} "
            f"| {_fmt(p['sim_interventions']['median'])} "
            f"| {_fmt(p['output_tokens']['median'])} "
            f"| {_fmt(p['model_requests']['median'])} "
            f"| {lat_str} "
            f"| {tokens_by_role or '—'} "
            f"| {', '.join(p['stability'])} |"
        )
    return lines


def _run_rows(runs: list[dict[str, Any]], runs_dir: Path) -> list[str]:
    lines = [
        "| run | scenario | combo | verdict | wall-time | checks | compactions "
        "(ok/started/failed) | testing rounds | sim interventions | tasks | stability | artifacts |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for m in runs:
        run_id = m.get("run_id") or "?"
        rel = f"{Path(runs_dir.name) / run_id}" if runs_dir.name else run_id
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
        verdicts = "/".join(
            f"{t.get('kind')}:{t.get('verification') or t.get('status')}" for t in tasks
        ) or "—"
        lines.append(
            f"| [{run_id}]({rel}/) | {_fmt(m.get('scenario'))} | {_fmt(m.get('combo'))} "
            f"| {_fmt(m.get('verdict'))} | {_fmt(m.get('wall_time_s', {}).get('settle'), ' s')} "
            f"| {checks_str} | {comp_str} "
            f"| {_fmt(comp.get('n_testing_rounds'))} | {sim_str} | {verdicts} "
            f"| {_stability_flags(m)} "
            f"| [metrics]({rel}/metrics.json) · [result]({rel}/result.json) |"
        )
    return lines


def _run_details(runs: list[dict[str, Any]], runs_dir: Path) -> list[str]:
    """Per-run dissection blocks: phase timings, compaction savings,
    bug round-trips — everything needed to read a run without rerunning."""
    lines: list[str] = []
    for m in runs:
        run_id = m.get("run_id") or "?"
        rel = f"{Path(runs_dir.name) / run_id}" if runs_dir.name else run_id
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
        comp_failed = (m.get("totals", {}).get("stability", {}) or {}).get(
            "compaction_failed"
        ) or 0
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
        ttc = m.get("tester_threshold_from_coding")
        if ttc is not None:
            flag = (
                "as expected (§1.2/§13)"
                if ttc
                else "REGRESSION — threshold came from the tester model"
            )
            lines.append(
                f"Tester compaction threshold source: {'coding' if ttc else 'NOT coding'} "
                f"model config — {flag}."
            )
            lines.append("")
        savings = [
            s
            for t in m.get("tasks") or []
            for s in (t.get("compaction_savings") or [])
        ]
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


def generate_report(runs_dir: Path, out: Path | None = None) -> Path:
    """Scan `runs_dir`, extract missing metrics, write the markdown report.
    Returns the path of the written report (default: `<runs_dir>/report.md`)."""
    runs_dir = Path(runs_dir)
    out = out or (runs_dir / "report.md")

    run_dirs = discover_runs(runs_dir)
    runs = [load_run(d) for d in run_dirs]
    pairs = aggregate_pairs(runs)

    lines = [
        "# drcode-bench report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}  ",
        f"Runs dir: `{runs_dir}` · runs: {len(runs)} · pairs: {len(pairs)}",
        "",
        "## Summary (scenario × combo)",
        "",
        "Medians over the repeats of each pair; a single run is a repeat count of 1.",
        "",
        *_pair_rows(pairs),
        "",
        "## Runs",
        "",
        *_run_rows(runs, runs_dir),
        "",
        "## Run details",
        "",
        *_run_details(runs, runs_dir),
    ]
    report = "\n".join(lines).rstrip() + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    return out


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
