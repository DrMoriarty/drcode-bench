"""Tests of bench.report: runs/ → report.md (§10). Synthetic metrics only —
aggregation and rendering are checked without any real runs.
"""

from __future__ import annotations

import json
from pathlib import Path

from bench.report import (
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
    summary_rows = [line for line in text.splitlines() if line.startswith("| s1 ")]
    assert len(summary_rows) == 1
    assert summary_rows[0].count("](r2/)") == 1


def test_summary_shows_gate_verdict(tmp_path: Path) -> None:
    """§7 S6: the run table carries the gate verdict; an overlap is
    flagged in the run details."""
    m = make_metrics("r-gate", "s6_queue_priority", "c1")
    m["gate"] = {"verdict": "OVERLAP", "overlaps": [{"detail": "x"}]}
    _write_run(tmp_path, m)
    out = generate_report(tmp_path)
    text = out.read_text(encoding="utf-8")
    assert "gate" in text
    assert "OVERLAP" in text
    assert "GATE VIOLATION" in text


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
    return [line for line in text.splitlines() if line.startswith(f"| {scenario} ")]


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
    stay untouched by the spread rendering."""
    _write_run(tmp_path, make_metrics("r1", "s1", "c1"))
    out = generate_report(tmp_path, html=True)
    text = out.with_suffix(".html").read_text(encoding="utf-8")
    assert '<span class="spread">' not in text
    assert "<td>green</td>" in text
    assert "<td>c1</td>" in text
