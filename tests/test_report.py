"""Tests of bench.report: runs/ → report.md (§10). Synthetic metrics only —
aggregation and rendering are checked without any real runs.
"""

from __future__ import annotations

import json
from pathlib import Path

from bench.report import aggregate_pairs, discover_runs, generate_report


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
    # Links to the run artifacts (§10: reproducibly dissectible).
    assert "(runs/r1/metrics.json)" in text
    assert "(runs/r1/result.json)" in text
    assert "green" in text
    # Compaction savings table is rendered.
    assert "1550" in text and "1240" in text


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
