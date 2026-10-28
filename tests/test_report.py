"""Tests of bench.report: runs/ → report.md (§10). Synthetic metrics only —
aggregation and rendering are checked without any real runs.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from bench.report import (
    _md_to_html,
    _natural_key,
    _tokens_by_role,
    aggregate_pairs,
    discover_runs,
    generate_report,
)

THIN = "\u202f"  # thousands separator used by the summary cells


def make_model_log(per_role: dict[str, dict]) -> dict:
    filled = {tag: {"latency_ms_total": 0, **e} for tag, e in per_role.items()}
    return {"per_role": filled, "requests": sum(e["requests"] for e in filled.values())}


def make_metrics(run_id: str, scenario: str, combo: str, **overrides) -> dict:
    metrics = {
        "schema": "metrics/v1",
        "run_id": run_id,
        "scenario": scenario,
        "combo": combo,
        "verdict": "green",
        "wall_time_s": {"settle": 100.0, "run": 120.0},
        "totals": {
            "n_tasks": 1,
            "n_bug_tasks": 0,
            "n_testing_rounds": 1,
            "n_compactions": 2,
            "n_compactions_started": 2,
            "usage": {
                "requests": 5,
                "input_tokens": 1000,
                "output_tokens": 200,
                "cache_read_tokens": 0,
                "cache_write_tokens": 0,
            },
            "stability": {
                "compaction_failed": 0,
                "tester_failed": 0,
                "network_retries": 0,
                "unfinished": 0,
                "pending_clarification": 0,
                "excluded_from_queue": 0,
            },
        },
        "bug_round_trips": [],
        "tasks": [
            {
                "id": "t1",
                "title": "Task one",
                "kind": "feature",
                "status": "completed",
                "verification": "Verified successfully",
                "phases": {"dev_s": 80.0, "testing_s": 20.0, "total_s": 100.0},
                "compactions": {"n_started": 2, "n_succeeded": 2, "n_failed": 0},
                "compaction_savings": [
                    {
                        "at": "2025-06-01T10:01:10+00:00",
                        "trigger_pct": 75,
                        "pre_tokens_est": 1550,
                        "post_tokens_est": 310,
                        "saved_tokens_est": 1240,
                        "summary_chars": 300,
                        "prompts_kept": 2,
                    }
                ],
                "testing": {"n_rounds": 1, "rounds": []},
                "usage": {},
                "stability": {},
                "stability_events": {},
            }
        ],
        "model_log": None,
    }
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(metrics.get(key), dict):
            metrics[key].update(value)
        else:
            metrics[key] = value
    return metrics


def _write_run(runs_dir: Path, metrics: dict, result: dict | None = None) -> Path:
    run_dir = runs_dir / metrics["run_id"]
    run_dir.mkdir(parents=True)
    (run_dir / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
    (run_dir / "result.json").write_text(
        json.dumps(result or {"ok": True, "checks_ok": True}), encoding="utf-8"
    )
    return run_dir


def test_discover_runs_ignores_stray_dirs(tmp_path: Path) -> None:
    _write_run(tmp_path, make_metrics("r1", "s1", "c1"))
    (tmp_path / "not-a-run").mkdir()
    (tmp_path / "loose.json").write_text("{}")
    assert [p.name for p in discover_runs(tmp_path)] == ["r1"]
    assert discover_runs(tmp_path / "missing") == []


def test_natural_key_orders_scenarios() -> None:
    """Digit runs compare as integers (s9 < s10 < s13); the text fallback
    keeps s2a < s2b — lexicographic order puts '0' before '_' and gets
    both wrong."""
    names = [
        "s10_research_facts",
        "s1_happy",
        "s2a_bug_followup",
        "s2b_bug_report",
        "s9_research_count",
        "s13_research_feature",
    ]
    assert sorted(names, key=_natural_key) == [
        "s1_happy",
        "s2a_bug_followup",
        "s2b_bug_report",
        "s9_research_count",
        "s10_research_facts",
        "s13_research_feature",
    ]


def test_report_rows_natural_scenario_order(tmp_path: Path) -> None:
    """Regression: s10 must not precede s1 in the report tables. The
    Summary and scenario-winner rows go in natural scenario order (the
    Runs / Run details tables inherit the same ordering from
    generate_report)."""
    _write_run(tmp_path, make_metrics("r-b", "s10_x", "combo-a"))
    _write_run(tmp_path, make_metrics("r-a", "s1_y", "combo-a"))
    text = generate_report(tmp_path).read_text(encoding="utf-8")

    summary = text.split("## Summary", 1)[1].split("## Scenario winners", 1)[0]
    assert summary.index("| s1_y ") < summary.index("| s10_x ")

    winners = text.split("## Scenario winners", 1)[1].split("## Runs", 1)[0]
    assert winners.index("| s1_y ") < winners.index("| s10_x ")


def test_aggregate_pairs_single_run_per_pair() -> None:
    runs = [
        make_metrics("r1", "s1_happy", "combo-a"),
        make_metrics("r2", "s3_compaction", "combo-b", verdict="failed"),
    ]
    pairs = aggregate_pairs(runs)
    assert len(pairs) == 2
    first = pairs[0]
    assert (first["scenario"], first["combo"]) == ("s1_happy", "combo-a")
    assert first["wall_time_s"]["n"] == 1
    assert first["wall_time_s"]["median"] == 100.0
    assert first["verdicts"] == ["green"]


def test_aggregate_pairs_medians_over_repeats() -> None:
    """§10/§12.5 shape: several repeats of one pair → medians + spread."""
    runs = [
        make_metrics("r1", "s1", "c1", wall_time_s={"settle": 100.0, "run": 120.0}),
        make_metrics("r2", "s1", "c1", wall_time_s={"settle": 200.0, "run": 220.0}),
        make_metrics("r3", "s1", "c1", wall_time_s={"settle": 300.0, "run": 320.0}),
    ]
    runs[1]["verdict"] = "failed"  # one bad repeat → both verdicts listed
    pairs = aggregate_pairs(runs)
    (pair,) = pairs
    assert pair["runs"] == ["r1", "r2", "r3"]
    assert pair["wall_time_s"]["median"] == 200.0
    assert pair["wall_time_s"]["min"] == 100.0
    assert pair["wall_time_s"]["max"] == 300.0
    assert pair["verdicts"] == ["failed", "green"]


def test_generate_report_writes_markdown(tmp_path: Path) -> None:
    _write_run(tmp_path / "runs", make_metrics("r1", "s1_happy", "combo-a"))
    out = generate_report(tmp_path / "runs")
    assert out == tmp_path / "runs" / "report.md"
    text = out.read_text(encoding="utf-8")
    assert "# drcode-bench report" in text
    assert "s1_happy" in text and "combo-a" in text
    assert "r1" in text
    # Links to the run artifacts (§10: reproducibly dissectible), relative
    # to the report's own directory (runs/report.md).
    assert "(r1/metrics.json)" in text
    assert "(r1/result.json)" in text
    assert "green" in text
    # Compaction savings table is rendered.
    assert "1550" in text and "1240" in text


def test_report_shows_sim_interventions_and_round_trips(tmp_path: Path) -> None:
    """§6/§10: the report must be able to tell "the model is dumb" from
    "the simulator intervened" — a dedicated column + per-run details."""
    metrics = make_metrics(
        "r1",
        "s2a",
        "c1",
        user_sim={
            "file": "user_sim.jsonl",
            "records": 3,
            "interventions": 2,
            "by_action": {"followup": 2},
            "failures": [],
        },
    )
    metrics["bug_round_trips"] = [{"id": "b1", "title": "bug", "activated_at": "x"}]
    _write_run(tmp_path / "runs", metrics)
    out = generate_report(tmp_path / "runs")
    text = out.read_text(encoding="utf-8")
    assert "sim interventions" in text
    assert "bug round-trips" in text
    assert "User-simulator interventions: 2" in text


def test_generate_report_out_option(tmp_path: Path) -> None:
    _write_run(tmp_path / "runs", make_metrics("r1", "s1_happy", "combo-a"))
    out = generate_report(tmp_path / "runs", out=tmp_path / "elsewhere" / "report.md")
    assert out.is_file()
    assert not (tmp_path / "runs" / "report.md").exists()


def test_generate_report_reextracts_missing_metrics(tmp_path: Path) -> None:
    """A run with only result.json (extraction skipped) still gets in."""
    run_dir = tmp_path / "runs" / "r1"
    (run_dir / "workspace" / ".drcode" / "tasks").mkdir(parents=True)
    (run_dir / "result.json").write_text(
        json.dumps({"scenario": "s1", "combo": "c1", "ok": True}), encoding="utf-8"
    )
    generate_report(tmp_path / "runs")
    assert (run_dir / "metrics.json").is_file()


def test_report_marks_compaction_failed_state(tmp_path: Path) -> None:
    """§1.2/§10: 'compaction failed' is never fatal in drcode (the gate is
    disabled, the run continues uncompressed) — the report must surface
    that state explicitly, plus repeat compactions (degradation)."""
    metrics = make_metrics(
        "r-compfail",
        "s3_compaction_coder",
        "combo-a",
        **{
            "totals": {
                "n_tasks": 1,
                "n_compactions": 0,
                "n_compactions_started": 1,
                "n_repeat_compactions": 1,
                "n_testing_rounds": 1,
                "usage": {},
                "stability": {"compaction_failed": 2},
            },
        },
    )
    _write_run(tmp_path, metrics)
    out = generate_report(tmp_path)
    report = out.read_text(encoding="utf-8")
    assert "COMPACTION FAILED ×2" in report
    assert "_compaction_failed" in report
    assert "UNCOMPRESSED" in report
    assert "Repeat compaction" in report


def test_report_marks_tester_threshold_source(tmp_path: Path) -> None:
    """§1.2 (S4): the tester-threshold-source remark is rendered — and
    a 'coding' classification (the pre-0.5.0 behavior) is named a
    REGRESSION."""
    ok = make_metrics("r-ttc-ok", "s4_compaction_tester", "combo-a")
    ok["tester_threshold_from_tester"] = True
    _write_run(tmp_path, ok)
    reg = make_metrics("r-ttc-reg", "s4_compaction_tester", "combo-a")
    reg["tester_threshold_from_tester"] = False
    _write_run(tmp_path, reg)
    out = generate_report(tmp_path)
    report = out.read_text(encoding="utf-8")
    assert "Tester compaction threshold source: tester" in report
    assert "REGRESSION" in report


def test_summary_links_to_representative_run(tmp_path: Path) -> None:
    """DoD of stage 5, narrowed: the summary row carries a SINGLE link —
    the run count cell — pointing to the artifacts of the pair's
    runs/<run_id>/ (the median-wall repeat); the rest of the cells stay
    plain text (they would all repeat the same target otherwise)."""
    for i, wall in enumerate((100.0, 200.0, 300.0), start=1):
        _write_run(
            tmp_path / "runs",
            make_metrics(f"r{i}", "s1", "c1", wall_time_s={"settle": wall, "run": wall}),
        )
    out = generate_report(tmp_path / "runs")
    text = out.read_text(encoding="utf-8")
    # Links are relative to the report's own directory
    # (runs/report.md → runs/<run_id>/).
    assert "[3](r2/)" in text
    # Exactly one link in the whole summary table (the Runs table below
    # has its own per-run links, so count within the summary rows only).
    summary_rows = _summary_rows(text, "s1")
    assert len(summary_rows) == 1
    assert summary_rows[0].count("](r2/)") == 1


def test_summary_gate_legacy_overlap_normalized(tmp_path: Path) -> None:
    """§7 S6: the run table carries the gate verdict; a legacy `OVERLAP`
    artifact (pre-retirement) renders as `ok` — overlaps are passive
    diagnostics now — and the overlap facts surface as a passive
    Diagnostic block in Run details, never as a GATE VIOLATION."""
    m = make_metrics("r-gate", "s6_queue_priority", "c1")
    m["gate"] = {"verdict": "OVERLAP", "overlaps": [{"detail": "x"}]}
    _write_run(tmp_path, m)
    out = generate_report(tmp_path)
    text = out.read_text(encoding="utf-8")
    assert "gate" in text
    assert "OVERLAP" not in text
    assert "GATE VIOLATION" not in text
    assert "Diagnostic (§7 S6, passive)" in text


def test_generate_report_html(tmp_path: Path) -> None:
    """Optional HTML rendering (§10): same content, table tags, links kept."""
    _write_run(tmp_path / "runs", make_metrics("r1", "s1_happy", "combo-a"))
    out = generate_report(tmp_path / "runs", html=True)
    html_path = out.with_suffix(".html")
    assert html_path.is_file()
    text = html_path.read_text(encoding="utf-8")
    assert "<table>" in text and "</html>" in text
    assert '<a href="r1/">' in text


def _summary_rows(text: str, scenario: str) -> list[str]:
    """Summary-table rows of one scenario — scoped to the Summary section
    (the scenario-winner table below also has `| <scenario> |` rows)."""
    summary = text.split("## Summary", 1)[1].split("## Scenario winners", 1)[0]
    return [line for line in summary.splitlines() if line.startswith(f"| {scenario} ")]


def test_summary_wall_time_whole_seconds_with_spread(tmp_path: Path) -> None:
    """Summary wall-time is rounded to whole seconds, the unit lives in
    the column header, and the spread over the repeats goes into
    parentheses (`23 (19–26)`) instead of `23.1 s · 19.1…26.1`."""
    for i, wall in enumerate((19.07, 23.1, 26.4), start=1):
        _write_run(
            tmp_path / "runs",
            make_metrics(f"r{i}", "s1", "c1", wall_time_s={"settle": wall, "run": wall}),
        )
    out = generate_report(tmp_path / "runs")
    text = out.read_text(encoding="utf-8")
    assert "wall-time (median, s)" in text
    (row,) = _summary_rows(text, "s1")
    assert "| 23 (19–26) |" in row
    assert "· 19" not in row  # old `median · min…max` shape is gone
    assert ".1 s" not in row


def test_summary_single_run_wall_time_no_spread(tmp_path: Path) -> None:
    """A repeat count of 1 → plain whole seconds, no parentheses."""
    _write_run(tmp_path / "runs", make_metrics("r1", "s1", "c1"))
    out = generate_report(tmp_path / "runs")
    (row,) = _summary_rows(out.read_text(encoding="utf-8"), "s1")
    assert "| 100 |" in row


def test_summary_output_tokens_thousands_separator(tmp_path: Path) -> None:
    """Output tokens carry thin-space digit separators (1316 → `1 316`)."""
    _write_run(
        tmp_path,
        make_metrics("r1", "s1", "c1", totals={"usage": {"output_tokens": 1316}}),
    )
    out = generate_report(tmp_path)
    (row,) = _summary_rows(out.read_text(encoding="utf-8"), "s1")
    assert f"| 1{THIN}316 |" in row


def test_summary_tokens_spread_with_separators(tmp_path: Path) -> None:
    """Spread over repeats keeps the separators: `1 316 (1 009–1 664)`."""
    for i, tok in enumerate((1009, 1316, 1664), start=1):
        _write_run(
            tmp_path / "runs",
            make_metrics(f"r{i}", "s1", "c1", totals={"usage": {"output_tokens": tok}}),
        )
    out = generate_report(tmp_path / "runs")
    (row,) = _summary_rows(out.read_text(encoding="utf-8"), "s1")
    assert f"| 1{THIN}316 (1{THIN}009–1{THIN}664) |" in row


def test_summary_has_no_latency_column(tmp_path: Path) -> None:
    """Latency p50/p95 is dropped from the summary table (it stays in the
    run details per-role table) — no data loss, one column less to read."""
    _write_run(tmp_path / "runs", make_metrics("r1", "s1", "c1"))
    out = generate_report(tmp_path / "runs")
    text = out.read_text(encoding="utf-8")
    assert "latency p50/p95" not in text
    pairs = aggregate_pairs([make_metrics("r1", "s1", "c1")])
    assert "latency_ms_p50" not in pairs[0]
    assert "latency_ms_p95" not in pairs[0]


def test_tokens_by_role_strips_endpoint_and_merges_replicas() -> None:
    """Recorder tags are `model@base_url`; the endpoint part is stripped
    and same-model entries are SUMMED within each run — the s7 proxy
    gives each replica an ephemeral port, which must not fragment one
    model into several rows."""
    runs = [
        make_metrics(
            "r1",
            "s7",
            "c1",
            model_log=make_model_log(
                {
                    "coder@http://127.0.0.1:1111/p/copilot": {
                        "requests": 2,
                        "input_tokens": 100,
                        "output_tokens": 10,
                    },
                    "coder@http://127.0.0.1:2222/p/copilot": {
                        "requests": 3,
                        "input_tokens": 200,
                        "output_tokens": 20,
                    },
                    "tester@http://real.host/v1": {
                        "requests": 1,
                        "input_tokens": 50,
                        "output_tokens": 5,
                    },
                }
            ),
        ),
        make_metrics(
            "r2",
            "s7",
            "c1",
            model_log=make_model_log(
                {
                    "coder@http://127.0.0.1:3333/p/copilot": {
                        "requests": 1,
                        "input_tokens": 10,
                        "output_tokens": 1,
                    },
                    "tester@http://real.host/v1": {
                        "requests": 1,
                        "input_tokens": 70,
                        "output_tokens": 9,
                    },
                }
            ),
        ),
    ]
    roles = _tokens_by_role(runs)
    # run1 coder = 100+200=300, run2 coder = 10 → median 155; same-model
    # replicas summed per run, median taken over RUNS, not replicas.
    assert roles["coder"]["n_runs"] == 2
    assert roles["coder"]["input_tokens_median"] == 155.0
    assert roles["coder"]["output_tokens_median"] == 15.5
    assert roles["tester"]["n_runs"] == 2
    assert set(roles) == {"coder", "tester"}


def test_summary_tokens_by_role_clean_names_and_thousands(tmp_path: Path) -> None:
    """The summary tokens-by-role cell shows bare model names with
    separator-formatted numbers; full `model@base_url` stays in the run
    details table."""
    _write_run(
        tmp_path,
        make_metrics(
            "r1",
            "s7",
            "c1",
            model_log=make_model_log(
                {
                    "coder@http://127.0.0.1:1111/p/copilot": {
                        "requests": 2,
                        "input_tokens": 39334,
                        "output_tokens": 1316,
                    },
                }
            ),
        ),
    )
    out = generate_report(tmp_path)
    text = out.read_text(encoding="utf-8")
    (row,) = _summary_rows(text, "s7")
    assert f"coder: 39{THIN}334/1{THIN}316" in row
    assert "@" not in row
    # Run details keep the full tag (§10: reproducibly dissectible).
    assert "coder@http://127.0.0.1:1111/p/copilot" in text


def test_run_rows_wall_time_one_decimal(tmp_path: Path) -> None:
    """Per-run wall-time keeps one decimal (`19.1 s`), not full float spam."""
    _write_run(
        tmp_path, make_metrics("r1", "s1", "c1", wall_time_s={"settle": 19.0744, "run": 19.0744})
    )
    out = generate_report(tmp_path)
    text = out.read_text(encoding="utf-8")
    assert "| 19.1 s |" in text
    assert "19.0744" not in text


def test_html_spread_on_second_line(tmp_path: Path) -> None:
    """HTML summary cells split the spread onto a small gray second line
    (`<br>` + span.spread); right-aligned numeric cells get class=num."""
    for i, wall in enumerate((19.07, 23.1, 26.4), start=1):
        _write_run(
            tmp_path / "runs",
            make_metrics(
                f"r{i}",
                "s1",
                "c1",
                wall_time_s={"settle": wall, "run": wall},
                totals={"usage": {"output_tokens": 1000 + i}},
            ),
        )
    out = generate_report(tmp_path / "runs", html=True)
    text = out.with_suffix(".html").read_text(encoding="utf-8")
    assert ".spread{color:#777;font-size:0.85em;}" in text
    assert "td.num{text-align:right;}" in text
    assert '<span class="spread">19–26</span>' in text
    # The spread marker itself never leaks into the HTML.
    assert "<br><span" in text


def test_html_plain_cells_not_transformed(tmp_path: Path) -> None:
    """Non-numeric cells (combos, verdicts, prose with parentheses) must
    stay untouched by the spread rendering; the combo cell carries the
    ◉ Pareto marker (a lone green pair is trivially non-dominated)."""
    _write_run(tmp_path, make_metrics("r1", "s1", "c1"))
    out = generate_report(tmp_path, html=True)
    text = out.with_suffix(".html").read_text(encoding="utf-8")
    assert '<span class="spread">' not in text
    assert "<td>green</td>" in text
    assert "<td>◉ c1</td>" in text


def test_report_has_glossary_section(tmp_path: Path) -> None:
    """§10: the terse gate/stability codes of the tables are spelled out
    in a Glossary section at the end of the markdown report."""
    _write_run(tmp_path, make_metrics("r1", "s1", "c1"))
    text = generate_report(tmp_path).read_text(encoding="utf-8")
    assert "## Glossary" in text
    assert "gate `ok`" in text
    assert "OVERLAP" not in text
    assert "stability `faults×N`" in text
    assert "stability `compact-fail×N`" in text
    assert "stability `net-retry×N`" in text
    assert "stability `stuck-clarif`" in text
    assert "stability `clean`" in text
    # The section comes after Run details (it explains their codes).
    assert text.index("## Run details") < text.index("## Glossary")


def test_html_glossary_tooltips(tmp_path: Path) -> None:
    """Gate/stability cells of the summary and runs tables get
    `<abbr title=...>` hover tooltips (the `label×N` counted form
    included); other columns stay plain."""
    m = make_metrics("r1", "s1", "c1")
    m["totals"]["stability"]["network_retries"] = 3
    m["gate"] = {"verdict": "ok"}
    _write_run(tmp_path, m)
    _write_run(tmp_path, make_metrics("r2", "s1", "c1"))  # clean stability
    out = generate_report(tmp_path, html=True)
    text = out.with_suffix(".html").read_text(encoding="utf-8")
    # Gate cell (both tables: summary + per-run) and the counted
    # stability form are wrapped; the tooltip text is the definition.
    assert '<abbr title="the coder/tester activity check' in text
    assert ">ok</abbr>" in text
    assert ">net-retry×3</abbr>" in text
    assert ">clean</abbr>" in text
    # Non-glossary cells are untouched by the tooltip pass.
    assert "<td>green</td>" in text
    assert "<td>◉ c1</td>" in text


def test_html_summary_scenario_clusters(tmp_path: Path) -> None:
    """Summary-table rows group into scenario clusters: the first row of
    each new scenario carries the `scenario-start` class (bold top
    border), coexisting with the verdict colouring; the very first data
    row does not (nothing above it to separate from), rows inside a
    cluster don't, and the per-run table is not clustered."""
    _write_run(tmp_path, make_metrics("r-s1-c1", "s1", "c1"))
    _write_run(tmp_path, make_metrics("r-s1-c2", "s1", "c2"))
    fail = make_metrics("r-s2-c1", "s2", "c1")
    fail["verdict"] = "failed"
    _write_run(tmp_path, fail)
    _write_run(tmp_path, make_metrics("r-s2-c2", "s2", "c2"))
    text = generate_report(tmp_path, html=True).with_suffix(".html").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.startswith("<tr")]
    summary_rows = rows[1:5]
    assert summary_rows[0].startswith('<tr class="verdict-ok">')  # s1/c1: top of the table
    assert summary_rows[1].startswith('<tr class="verdict-ok">')  # s1/c2: same cluster
    assert summary_rows[2].startswith(
        '<tr class="verdict-fail scenario-start">'
    )  # s2/c1: new cluster
    assert summary_rows[3].startswith('<tr class="verdict-ok">')  # s2/c2: same cluster
    # The runs table (one row per run) has no scenario clustering.
    assert not any("scenario-start" in ln for ln in rows[5:])


def test_summary_verdicts_markdown_only_html_dropped(tmp_path: Path) -> None:
    """The Summary `verdicts` column stays in the markdown report but is
    hidden in the HTML rendering — there the row background (verdict-ok/
    fail/mixed, derived from the ORIGINAL verdict cells before the drop)
    and the `pass rate` column already carry the outcome; the per-run
    table keeps its own `verdict` column in both renderings."""
    _write_run(tmp_path, make_metrics("r-m1", "s1", "c1"))  # mixed pair
    mixed = make_metrics("r-m2", "s1", "c1")
    mixed["verdict"] = "failed"
    _write_run(tmp_path, mixed)
    _write_run(tmp_path, make_metrics("r-ok", "s2", "c1"))
    fail = make_metrics("r-fail", "s2", "c2")
    fail["verdict"] = "failed"
    _write_run(tmp_path, fail)
    md_path = generate_report(tmp_path, html=True)
    md = md_path.read_text(encoding="utf-8")
    html = md_path.with_suffix(".html").read_text(encoding="utf-8")
    # Markdown keeps the column.
    summary = md.split("## Summary", 1)[1].split("## Scenario winners", 1)[0]
    assert "| scenario | combo | runs | verdicts | pass rate |" in summary
    assert "| failed, green |" in summary
    # HTML summary drops it — but the runs table keeps its `verdict`.
    assert "<th>verdicts</th>" not in html
    assert "<th>verdict</th>" in html
    # Row colouring survives the drop (computed before the column is cut):
    # the three SUMMARY data rows carry all three verdict classes.
    trs = [ln for ln in html.splitlines() if ln.startswith("<tr")]
    summary_rows = trs[1:4]
    assert 'class="verdict-mixed"' in summary_rows[0]
    assert 'class="verdict-ok' in summary_rows[1]  # + scenario-start (new cluster)
    assert 'class="verdict-fail' in summary_rows[2]


def test_summary_compactions_column_removed(tmp_path: Path) -> None:
    """The `compactions (med)` column is gone from the Summary table in
    both renderings (the compaction facts stay in the per-run table and
    Run details)."""
    _write_run(tmp_path, make_metrics("r1", "s1", "c1"))
    md_path = generate_report(tmp_path, html=True)
    md = md_path.read_text(encoding="utf-8")
    html = md_path.with_suffix(".html").read_text(encoding="utf-8")
    assert "compactions (med)" not in md
    assert "<th>compactions (med)</th>" not in html
    # The per-run table keeps its own compactions column.
    assert "compactions (ok/started/failed)" in md


def test_commit_codes_in_gate_cell_and_glossary(tmp_path: Path) -> None:
    """The measured report_committed (s9) rides in the summary `gate`
    cell as a terse commit-yes/no/mixed code — nothing is appended when
    no run of the pair measured the metric — spelled out in the Glossary
    and given `<abbr>` tooltips in HTML; the Summary preamble no longer
    explains the metric (that text moved to the glossary entries)."""
    committed = make_metrics("r-yes", "s9", "c1")
    committed["result"] = {
        "ok": True,
        "checks_ok": True,
        "checks_metrics": {"report_committed": True},
    }
    _write_run(tmp_path, committed)
    not_committed = make_metrics("r-no", "s9", "c2")
    not_committed["result"] = {
        "ok": True,
        "checks_ok": True,
        "checks_metrics": {"report_committed": False},
    }
    _write_run(tmp_path, not_committed)
    for rid in ("r-m1", "r-m2"):  # disagreeing repeats → mixed
        mixed = make_metrics(rid, "s9", "c3")
        mixed["result"] = {
            "ok": True,
            "checks_ok": True,
            "checks_metrics": {"report_committed": rid == "r-m1"},
        }
        _write_run(tmp_path, mixed)
    _write_run(tmp_path, make_metrics("r-none", "s1", "c1"))  # no metric at all
    md_path = generate_report(tmp_path, html=True)
    md = md_path.read_text(encoding="utf-8")
    html = md_path.with_suffix(".html").read_text(encoding="utf-8")

    def row(scenario: str, combo: str) -> str:
        (found,) = [ln for ln in _summary_rows(md, scenario) if f" {combo} |" in ln]
        return found

    assert "n/a, commit-yes" in row("s9", "c1")
    assert "n/a, commit-no" in row("s9", "c2")
    assert "n/a, commit-mixed" in row("s9", "c3")
    # s1 never measured the metric → bare gate cell, nothing appended.
    (plain,) = _summary_rows(md, "s1")
    assert "commit-" not in plain
    # The glossary spells the codes out under the gate column.
    assert "gate `commit-yes`" in md
    assert "gate `commit-no`" in md
    assert "gate `commit-mixed`" in md
    assert "not a verdict gate" in md
    # ... and the Summary preamble no longer does (moved to the glossary).
    preamble = md.split("## Summary", 1)[1].split("| scenario |", 1)[0]
    assert "report_committed" not in preamble
    # HTML: tooltips cover the new gate codes.
    assert ">commit-yes</abbr>" in html
    assert ">commit-no</abbr>" in html
    assert ">commit-mixed</abbr>" in html


def test_html_indented_block_line_terminates_paragraph() -> None:
    """A non-blank line indented before `#`/`- `/`|` misses the unstripped
    outer dispatch but the stripped paragraph exclusion — the fallback
    branch must still consume it or `_md_to_html` spins forever (real
    trigger: indented comments inside multi-line pytest output embedded
    in a run's failure reason)."""
    md = "\n".join(
        [
            "some reason text:",
            "        # RED in the seed: the bug brief's scope.",
            "    - indented list item",
            "    | indented | table |",
            "tail line",
        ]
    )
    html = _md_to_html(md)  # must terminate
    assert "# RED in the seed" in html
    assert "<li>indented list item</li>" in html
    assert "<th>indented</th>" in html
    assert "<th>table</th>" in html


def test_html_legacy_overlap_verdict_normalized(tmp_path: Path) -> None:
    """A legacy `OVERLAP` gate verdict (pre-retirement artifacts) renders
    as `ok` in HTML — tooltip included, no warning mark, no trace of the
    retired code."""
    m = make_metrics("r1", "s6_queue_priority", "c1")
    m["gate"] = {"verdict": "OVERLAP", "overlaps": [{"detail": "x"}]}
    _write_run(tmp_path, m)
    out = generate_report(tmp_path, html=True)
    text = out.with_suffix(".html").read_text(encoding="utf-8")
    assert ">ok</abbr>" in text
    assert "OVERLAP" not in text


# -- quality ranking: cost $, score = α·t_norm + β·m_norm, Pareto (§10) --------------

PRICED_MATRIX = """\
[providers.fake-a]
base_url = "http://fake-a.local:9000/v1"

[providers.fake-a.models.model-a]
price_input = 1.0
price_output = 1.0

[providers.fake-a.models.model-b]
price_input = 3.0
price_output = 3.0

[providers.fake-a.models.model-free]

[providers.fake-a.models.model-zero]
price_input = 0.0
price_output = 0.0

[[combo]]
name   = "zero-priced"
coding = "fake-a/model-zero"
tester = "fake-a/model-zero"
compaction = "fake-a/model-zero"

[[combo]]
name   = "priced"
coding = "fake-a/model-a"
tester = "fake-a/model-a"
compaction = "fake-a/model-a"

[[combo]]
name   = "pricey"
coding = "fake-a/model-b"
tester = "fake-a/model-b"
compaction = "fake-a/model-b"

[[combo]]
name   = "unpriced"
coding = "fake-a/model-free"
tester = "fake-a/model-free"
compaction = "fake-a/model-free"

[[combo]]
name   = "fast"
coding = "fake-a/model-a"
tester = "fake-a/model-a"
compaction = "fake-a/model-a"

[[combo]]
name   = "cheap"
coding = "fake-a/model-a"
tester = "fake-a/model-a"
compaction = "fake-a/model-a"

[[combo]]
name   = "slow"
coding = "fake-a/model-a"
tester = "fake-a/model-a"
compaction = "fake-a/model-a"

[[combo]]
name   = "ufast"
coding = "fake-a/model-free"
tester = "fake-a/model-free"
compaction = "fake-a/model-free"

[[combo]]
name   = "uslow"
coding = "fake-a/model-free"
tester = "fake-a/model-free"
compaction = "fake-a/model-free"

[[combo]]
name   = "mixed"
coding = "fake-a/model-a"
tester = "fake-a/model-a"
compaction = "fake-a/model-a"

[[combo]]
name   = "tie-1"
coding = "fake-a/model-a"
tester = "fake-a/model-a"
compaction = "fake-a/model-a"

[[combo]]
name   = "tie-2"
coding = "fake-a/model-a"
tester = "fake-a/model-a"
compaction = "fake-a/model-a"
"""


@pytest.fixture
def pricing(tmp_path: Path):  # -> Pricing
    from bench.report import load_pricing

    path = tmp_path / "matrix.toml"
    path.write_text(PRICED_MATRIX, encoding="utf-8")
    return load_pricing(path)


def _traffic(model: str, inp: int, out: int) -> dict:
    return make_model_log(
        {
            f"{model}@http://fake-a.local:9000/v1": {
                "requests": 1,
                "input_tokens": inp,
                "output_tokens": out,
            }
        }
    )


def _pairs_by_combo(runs: list[dict], pricing=None, time_weight: float = 0.0) -> dict:
    pairs = aggregate_pairs(runs, pricing, time_weight)
    return {p["combo"]: p for p in pairs}


def test_cost_aggregation_priced_and_unpriced(pricing) -> None:
    """cost $ = Σ per-role input·price_in + output·price_out, median over
    the repeats. An unpriced model (in the combo or only in the traffic)
    → no cost at all; a combo unknown to `--matrix` → no cost either."""
    runs = [
        make_metrics("r1", "s1", "priced", model_log=_traffic("model-a", 2_000_000, 1_000_000)),
        make_metrics("r2", "s1", "priced", model_log=_traffic("model-a", 1_000_000, 1_000_000)),
        make_metrics("r3", "s1", "unpriced", model_log=_traffic("model-free", 1_000_000, 0)),
        # combo 'ghost' is not in the matrix → eligibility fails
        make_metrics("r4", "s1", "ghost", model_log=_traffic("model-a", 1_000_000, 0)),
    ]
    pairs = _pairs_by_combo(runs, pricing)
    # priced: (2·1+1·1 + 1·1+1·1) / 2 → median 2.5, spread 2…3
    assert pairs["priced"]["cost_usd"] == {"n": 2, "median": 2.5, "min": 2.0, "max": 3.0}
    assert pairs["unpriced"]["cost_usd"]["median"] is None
    assert pairs["ghost"]["cost_usd"]["median"] is None
    # pass_rate: share of green repeats
    assert pairs["priced"]["pass_rate"] == 1.0
    runs[1]["verdict"] = "failed"
    assert _pairs_by_combo(runs, pricing)["priced"]["pass_rate"] == 0.5


def test_cost_column_and_unpriced_dash(tmp_path: Path, pricing) -> None:
    """Summary table: cost/score cells render via the spread helper; an
    unpriced pair renders `—` and stays in the table."""
    _write_run(
        tmp_path,
        make_metrics("r1", "s1", "priced", model_log=_traffic("model-a", 1_000_000, 1_000_000)),
    )
    _write_run(
        tmp_path,
        make_metrics("r2", "s1", "unpriced", model_log=_traffic("model-free", 1_000_000, 0)),
    )
    text = generate_report(tmp_path, pricing=pricing).read_text(encoding="utf-8")
    summary = text.split("## Summary", 1)[1].split("## Scenario winners", 1)[0]
    (priced_row,) = [r for r in summary.splitlines() if "| ◉ priced " in r]
    (unpriced_row,) = [r for r in summary.splitlines() if "unpriced " in r]
    assert "| $2 | 1 |" in priced_row  # single run → median only, no spread
    assert "| 100% | — | — |" in unpriced_row
    # the scenario-winner view keeps both, with the t_norm/m_norm factors
    assert "t_norm" in text and "m_norm" in text


def test_subdollar_cost_not_rounded_to_zero(pricing) -> None:
    """Sub-dollar costs survive aggregation: `cost_usd` is aggregated raw
    (rounding happens only at render time, `_dollar`), and the score of a
    small-but-nonzero-cost scenario stays computable. Regression: the old
    `round(x, 1)` collapsed a ~$0.0106 run to 0.0, rendering `$0` in the
    cost column and disabling the score's `m_min` guard (`—` everywhere)."""
    # model-a at $1/$1 per 1M: (10 000 + 600)/1e6 = $0.0106 per repeat
    runs = [
        make_metrics("r1", "s9", "priced", model_log=_traffic("model-a", 10_000, 600)),
        make_metrics("r2", "s9", "priced", model_log=_traffic("model-a", 20_000, 600)),
    ]
    cost = _pairs_by_combo(runs, pricing)["priced"]["cost_usd"]
    assert cost["n"] == 2
    assert cost["median"] == pytest.approx(0.0156)
    assert cost["min"] == pytest.approx(0.0106)
    assert cost["max"] == pytest.approx(0.0206)
    # score divides by the RAW best median (this pair's own median here);
    # with α = 0 the median of the per-repeat scores is the m_norm = 1.0
    # (min/max are the per-repeat ratios 0.0106/0.0156 and 0.0206/0.0156,
    # displayed at the score column's 1-decimal granularity)
    scores = _pairs_by_combo(runs, pricing)["priced"]["quality_score"]
    assert scores["median"] is not None
    assert scores["median"] == pytest.approx(1.0)
    assert scores["min"] == pytest.approx(round(0.0106 / 0.0156, 1))
    assert scores["max"] == pytest.approx(round(0.0206 / 0.0156, 1))


def test_subdollar_cost_renders_and_scores(tmp_path: Path, pricing) -> None:
    """Rendered summary: a ~$0.0106 run shows `$0.0106` (not `$0`) and the
    single-pair scenario's score cell is `1`, not `—`."""
    _write_run(
        tmp_path,
        make_metrics("r1", "s9", "priced", model_log=_traffic("model-a", 10_000, 600)),
    )
    text = generate_report(tmp_path, pricing=pricing).read_text(encoding="utf-8")
    summary = text.split("## Summary", 1)[1].split("## Scenario winners", 1)[0]
    (row,) = [r for r in summary.splitlines() if "| ◉ priced " in r]
    assert "| $0.0106 | 1 |" in row


def test_zero_cost_score_not_disabled(pricing) -> None:
    """A priced-at-$0 model yields cost 0.0 — real data (free/local), not
    'unknown': the pair keeps m_norm and a score (money term pinned at the
    optimum 1.0), while an unpriced pair still renders `—`."""
    runs = [
        make_metrics(
            "r1", "s8", "zero-priced", model_log=_traffic("model-zero", 1_000_000, 1_000_000)
        ),
        make_metrics("r2", "s8", "unpriced", model_log=_traffic("model-free", 1_000_000, 0)),
    ]
    pairs = _pairs_by_combo(runs, pricing)
    assert pairs["zero-priced"]["cost_usd"]["median"] == 0.0
    assert pairs["zero-priced"]["m_norm"] == 1.0
    assert pairs["zero-priced"]["quality_score"]["median"] == 1.0
    assert pairs["unpriced"]["cost_usd"]["median"] is None
    assert pairs["unpriced"]["quality_score"]["median"] is None


def test_pareto_frontier(pricing) -> None:
    """Frontier over (median wall-time, median cost $) among GREEN pairs:
    fast/cheap both non-dominated, a slow+expensive pair is dominated, an
    unpriced pair is eligible on the time axis only, a non-green pair is
    never on the frontier."""
    runs = [
        make_metrics(
            "r-fast",
            "s2",
            "fast",
            wall_time_s={"settle": 100.0},
            model_log=_traffic("model-a", 4_000_000, 1_000_000),
        ),
        make_metrics(
            "r-cheap",
            "s2",
            "cheap",
            wall_time_s={"settle": 200.0},
            model_log=_traffic("model-a", 1_500_000, 500_000),
        ),
        make_metrics(
            "r-slow",
            "s2",
            "slow",
            wall_time_s={"settle": 300.0},
            model_log=_traffic("model-a", 6_000_000, 0),
        ),
        make_metrics(
            "r-ufast",
            "s2",
            "ufast",
            wall_time_s={"settle": 50.0},
            model_log=_traffic("model-free", 1_000_000, 0),
        ),
        make_metrics(
            "r-uslow",
            "s2",
            "uslow",
            wall_time_s={"settle": 150.0},
            model_log=_traffic("model-free", 1_000_000, 0),
        ),
        make_metrics(
            "r-fail",
            "s2",
            "priced",
            verdict="failed",
            wall_time_s={"settle": 10.0},
            model_log=_traffic("model-a", 500_000, 0),
        ),
    ]
    pairs = _pairs_by_combo(runs, pricing)
    assert pairs["fast"]["pareto"] and pairs["cheap"]["pareto"]
    assert not pairs["slow"]["pareto"]  # dominated by `fast` on both axes
    assert pairs["ufast"]["pareto"]  # nothing priced is faster
    assert not pairs["uslow"]["pareto"]  # `fast` (t=100) is strictly faster
    assert not pairs["priced"]["pareto"]  # not green → never on the frontier


def test_ranking_outcome_beats_pass_rate_beats_cost(tmp_path: Path, pricing) -> None:
    """Lexicographic ranking in the scenario-winner table: outcome class
    first, then pass rate, then cost; full ties keep the combo order."""
    runs = [
        make_metrics(
            "r-m1",
            "s1",
            "mixed",
            verdict="green",
            model_log=_traffic("model-a", 1_000_000, 1_000_000),
        ),
        make_metrics(
            "r-m2",
            "s1",
            "mixed",
            verdict="failed",
            model_log=_traffic("model-a", 1_000_000, 1_000_000),
        ),
        make_metrics("r-b", "s1", "pricey", model_log=_traffic("model-b", 1_000_000, 1_000_000)),
        make_metrics("r-c", "s1", "priced", model_log=_traffic("model-a", 1_000_000, 1_000_000)),
        make_metrics("r-d", "s1", "tie-1", model_log=_traffic("model-a", 1_000_000, 1_000_000)),
        make_metrics("r-e", "s1", "tie-2", model_log=_traffic("model-a", 1_000_000, 1_000_000)),
    ]
    _write_run(tmp_path, runs[0])
    for m in runs[1:]:
        _write_run(tmp_path, m)
    text = generate_report(tmp_path, pricing=pricing).read_text(encoding="utf-8")
    winners = text.split("## Scenario winners", 1)[1].split("## Runs", 1)[0]
    order = [
        line.split("|")[3].strip() for line in winners.splitlines() if line.startswith("| s1 |")
    ]
    assert order == ["priced", "tie-1", "tie-2", "pricey", "mixed"]


def test_score_money_only_default_and_time_weight(pricing) -> None:
    """α = 0 (default): score = m_norm only. A non-zero --time-weight
    mixes in the normalized wall-time and can flip the winner."""
    runs = [
        make_metrics(
            "r-f",
            "s3",
            "fast",
            wall_time_s={"settle": 100.0},
            model_log=_traffic("model-a", 4_000_000, 1_000_000),
        ),
        make_metrics(
            "r-c",
            "s3",
            "cheap",
            wall_time_s={"settle": 200.0},
            model_log=_traffic("model-a", 1_500_000, 500_000),
        ),
    ]
    # costs: fast = 5.0, cheap = 2.0 → m_min = 2, t_min = 100
    money = _pairs_by_combo(runs, pricing)
    assert money["cheap"]["quality_score"]["median"] == 1.0
    assert money["fast"]["quality_score"]["median"] == 2.5
    assert money["cheap"]["m_norm"] == 1.0 and money["cheap"]["t_norm"] == 2.0
    assert money["fast"]["m_norm"] == 2.5 and money["fast"]["t_norm"] == 1.0
    # α = 0.5: cheap = 0.5·2 + 1 = 2, fast = 0.5·1 + 2.5 = 3 → cheap still wins
    half = _pairs_by_combo(runs, pricing, time_weight=0.5)
    assert half["cheap"]["quality_score"]["median"] == 2.0
    assert half["fast"]["quality_score"]["median"] == 3.0
    # α = 2: cheap = 2·2 + 1 = 5, fast = 2·1 + 2.5 = 4.5 → fast wins
    timed = _pairs_by_combo(runs, pricing, time_weight=2.0)
    assert timed["fast"]["quality_score"]["median"] < timed["cheap"]["quality_score"]["median"]


def test_score_baseline_is_green_only(pricing) -> None:
    """A failed pair dies early — it is fast and cheap — and must NOT
    become the scenario's normalization baseline (§10: the score is
    computed over the GREEN repeats). Green pairs keep their norms and
    scores against the green-only baseline; a failed pair renders `—`;
    a scenario with no green pair has no baseline at all; and a FAILED
    free pair must not trip the m_min == 0 branch either."""
    runs = [
        # s5: failed pair is fastest AND cheapest — it must not set the baseline
        make_metrics(
            "r-fail",
            "s5",
            "priced",
            verdict="failed",
            wall_time_s={"settle": 10.0},
            model_log=_traffic("model-a", 500_000, 0),
        ),
        make_metrics(
            "r-cheap",
            "s5",
            "cheap",
            wall_time_s={"settle": 200.0},
            model_log=_traffic("model-a", 1_500_000, 500_000),
        ),
        make_metrics(
            "r-fast",
            "s5",
            "fast",
            wall_time_s={"settle": 100.0},
            model_log=_traffic("model-a", 4_000_000, 1_000_000),
        ),
        # s6: no green pair → no meaningful baseline
        make_metrics(
            "r-f1",
            "s6",
            "pricey",
            verdict="failed",
            wall_time_s={"settle": 5.0},
            model_log=_traffic("model-b", 100_000, 0),
        ),
        # s7: a FAILED zero-cost pair must not activate the m_min == 0
        # branch for the green pairs
        make_metrics(
            "r-zfail",
            "s7",
            "zero-priced",
            verdict="failed",
            wall_time_s={"settle": 10.0},
            model_log=_traffic("model-zero", 500_000, 0),
        ),
        make_metrics(
            "r-zgreen",
            "s7",
            "slow",
            wall_time_s={"settle": 100.0},
            model_log=_traffic("model-a", 2_000_000, 0),
        ),
    ]
    pairs = _pairs_by_combo(runs, pricing)
    cheap, fast, failed = pairs["cheap"], pairs["fast"], pairs["priced"]
    # baseline: green-only → t_min = 100, m_min = 2.0 (the failed pair's
    # 10 s / $0.5 would have set both and scored itself 1.0)
    assert cheap["quality_score"]["median"] == 1.0
    assert fast["quality_score"]["median"] == 2.5
    assert cheap["t_norm"] == 2.0 and cheap["m_norm"] == 1.0
    assert fast["t_norm"] == 1.0 and fast["m_norm"] == 2.5
    # the failed pair gets no score, but its norms still display against
    # the same green baseline
    assert failed["quality_score"]["median"] is None
    assert failed["t_norm"] == 0.1 and failed["m_norm"] == 0.25
    # no green pair in s6 → everything `—`
    assert pairs["pricey"]["quality_score"]["median"] is None
    assert pairs["pricey"]["t_norm"] is None and pairs["pricey"]["m_norm"] is None
    # s7: the green pair is the baseline (m_min = 2.0), score 1.0; the
    # failed free pair shows no score and m_norm 0 against it
    assert pairs["slow"]["quality_score"]["median"] == 1.0
    assert pairs["zero-priced"]["quality_score"]["median"] is None
    assert pairs["zero-priced"]["m_norm"] == 0.0


def test_html_spread_for_cost_and_score(tmp_path: Path, pricing) -> None:
    """Cost and score cells carry `$` prefixes / decimals — the HTML
    rendering still splits their spread onto the second line."""
    _write_run(
        tmp_path,
        make_metrics("r1", "s1", "priced", model_log=_traffic("model-a", 1_000_000, 1_000_000)),
    )
    _write_run(
        tmp_path,
        make_metrics("r2", "s1", "priced", model_log=_traffic("model-a", 2_000_000, 1_000_000)),
    )
    text = (
        generate_report(tmp_path, pricing=pricing, html=True)
        .with_suffix(".html")
        .read_text(encoding="utf-8")
    )
    # costs 2.0 / 3.0 → median $2.5, spread $2–$3; α=0 scores are the
    # per-repeat costs over the scenario's best pair median (2.5):
    # 0.8 / 1.2 → median 1, spread 0.8–1.2
    assert '<span class="spread">$2–$3</span>' in text
    assert '<span class="spread">0.8–1.2</span>' in text


def test_glossary_explains_ranking(tmp_path: Path, pricing) -> None:
    """The ◉ Pareto marker and the ordinal-score caveat are spelled out
    in the Glossary section."""
    _write_run(
        tmp_path,
        make_metrics("r1", "s1", "priced", model_log=_traffic("model-a", 1_000_000, 1_000_000)),
    )
    text = generate_report(tmp_path, pricing=pricing).read_text(encoding="utf-8")
    assert "combo `◉`" in text
    assert "Pareto frontier" in text
    assert "RANKING, not a ratio" in text


def test_cli_report_matrix_and_time_weight(tmp_path: Path) -> None:
    """`--matrix` / `--time-weight` wiring: parsed into the report call;
    a priced run shows the $ column, a bad matrix is a planning error."""
    from bench import cli

    args = cli.build_parser().parse_args(
        ["report", "runs", "--matrix", "m.toml", "--time-weight", "0.5"]
    )
    assert (args.matrix, args.time_weight) == ("m.toml", 0.5)

    matrix = tmp_path / "matrix.toml"
    matrix.write_text(PRICED_MATRIX, encoding="utf-8")
    _write_run(
        tmp_path / "runs",
        make_metrics("r1", "s1", "priced", model_log=_traffic("model-a", 1_000_000, 1_000_000)),
    )
    rc = cli.main(["report", str(tmp_path / "runs"), "--matrix", str(matrix)])
    assert rc == 0
    text = (tmp_path / "runs" / "report.md").read_text(encoding="utf-8")
    assert "$2" in text and "Scenario winners" in text
    # a matrix path that does not parse → planning error, exit code 2
    assert (
        cli.main(["report", str(tmp_path / "runs"), "--matrix", str(tmp_path / "nope.toml")]) == 2
    )
