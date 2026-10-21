"""CLI of drcode-bench (plan §8, §11).

Stage 1 (§12.1): `run` and `report` are stubs — they validate their
arguments, show the resolved combo/scenario and say clearly what is not
implemented yet. The orchestrator (`bench/run_one.py`) arrives at stage 2.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .env_setup import EnvSetupError
from .matrix import MatrixError, get_combo, load_matrix

DEFAULT_MATRIX = Path(__file__).resolve().parents[1] / "matrix.toml"


def _cmd_run(args: argparse.Namespace) -> int:
    """`bench run` — orchestrator stub (§4)."""
    try:
        combo = get_combo(Path(args.matrix), args.combo)
        providers, combos = load_matrix(Path(args.matrix))
    except MatrixError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(f"matrix:   {args.matrix}")
    print(f"combo:    {combo.name}")
    for role in ("coding", "tester", "compaction"):
        ref = combo.ref(role)
        base_url = providers[ref.partition("/")[0]].base_url
        print(f"  {role:10} {ref}  ({base_url})")
    print(f"scenario: {args.scenario}")
    print(f"repeats:  {args.repeats}, parallel: {args.parallel}")
    if args.combo and not any(c.name == args.combo for c in combos):
        print(
            f"note: combo '{args.combo}' is not defined in {args.matrix}",
            file=sys.stderr,
        )
    print(
        "\nnot implemented yet: the run orchestrator (bench/run_one.py — "
        "headless DrCodeApp, settle detection, metrics extraction) is stage 2 "
        "of the plan (drcode-bench.md §12.2). Environment preparation itself "
        "already works: see bench/env_setup.py and its tests."
    )
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    """`bench report` — aggregation stub (§10)."""
    runs_dir = Path(args.runs_dir)
    print(f"runs dir: {runs_dir.resolve()}")
    if not runs_dir.is_dir():
        print("note: the directory does not exist yet — no runs recorded.")
    print(
        "\nnot implemented yet: report aggregation (metrics.json → report.md, "
        "drcode-bench.md §10) arrives with the first real runs. The metric "
        "sources are described in the plan: task JSON in .drcode/tasks/, "
        "model_log.jsonl (recorder), user_sim.jsonl."
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bench",
        description="Benchmark harness for the full drcode agent loop "
        "(coding → testing → compaction) with a model per role.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="run scenarios × combos (stub)")
    run.add_argument("--scenario", required=True, help="scenario id, or 'all'")
    run.add_argument("--matrix", default=str(DEFAULT_MATRIX), help="path to matrix.toml")
    run.add_argument("--combo", default="", help="combo name (empty = first)")
    run.add_argument("--parallel", type=int, default=1, help="max concurrent runs")
    run.add_argument("--repeats", type=int, default=3, help="repeats per pair")
    run.set_defaults(func=_cmd_run)

    report = sub.add_parser("report", help="aggregate runs into a report (stub)")
    report.add_argument("runs_dir", nargs="?", default="runs", help="runs directory")
    report.set_defaults(func=_cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except EnvSetupError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
