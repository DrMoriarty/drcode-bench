"""CLI of drcode-bench (plan §8, §11).

`run` is the matrix orchestrator (§8, stage 5 of §12): scenario × combo ×
repeats, one subprocess per run (`bench.run_one`), `--parallel` bounded,
infrastructure retries separated from substantive failures. A SINGLE run
remains available as `python -m bench.run_one <scenario> <combo>
<run_dir>`. `report` aggregates `runs/` into `report.md` (§10, optional
HTML via --html).
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
    """`bench run` — the matrix sweep (§8): plan → parallel subprocesses →
    report. Exit code 0 when every job produced a verdict (a substantive
    failure is a data point, not an error); 1 when infrastructure failures
    stayed unresolved after the retries; 2 on planning errors."""
    from .runner import RunnerError, run_sweep

    try:
        jobs_plan = _describe_plan(args)
    except (MatrixError, RunnerError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(f"matrix:    {args.matrix}")
    print(f"scenarios: {args.scenario}")
    print(f"combos:    {jobs_plan}")
    print(f"repeats:   {args.repeats}, parallel: {args.parallel}")
    print(f"runs dir:  {Path(args.runs_dir).resolve()}")
    print()

    outcomes, report_path = run_sweep(
        Path(args.matrix),
        Path(__file__).resolve().parents[1] / "scenarios",
        Path(args.runs_dir),
        scenario_filter=args.scenario,
        combo_filter=args.combo,
        repeats=args.repeats,
        parallel=args.parallel,
        make_report=not args.no_report,
        use_proxy=args.use_proxy,
    )
    if report_path is not None:
        print(f"report:    {report_path.resolve()}")

    unresolved = [o for o in outcomes if o.ok is None]
    if unresolved:
        for o in unresolved:
            print(
                f"error: {o.scenario} × {o.combo} × rep{o.repeat}: "
                f"infrastructure failure unresolved: {o.reason}",
                file=sys.stderr,
            )
        return 1
    return 0


def _describe_plan(args: argparse.Namespace) -> str:
    """Human-readable summary of the planned sweep (validates early)."""
    from .runner import RunnerError, discover_scenarios

    _, combos = load_matrix(Path(args.matrix))
    if args.combo:
        combos = [c for c in combos if c.name == args.combo]
        if not combos:
            raise MatrixError(f"no combo named '{args.combo}' in {args.matrix}")
    if args.scenario in ("all", ""):
        scenario_ids = discover_scenarios(
            Path(__file__).resolve().parents[1] / "scenarios"
        )
        if not scenario_ids:
            raise RunnerError("no scenarios under scenarios/")
    else:
        scenario_ids = [args.scenario]
    combos_str = ", ".join(c.name for c in combos)
    scenarios_str = ", ".join(scenario_ids)
    total = len(combos) * len(scenario_ids) * args.repeats
    return (
        f"[{combos_str}] × scenarios [{scenarios_str}] × {args.repeats} repeats "
        f"= {total} run(s)"
    )


def _cmd_report(args: argparse.Namespace) -> int:
    """`bench report` — runs/ → report.md (§10), optionally + .html."""
    from .report import generate_report

    runs_dir = Path(args.runs_dir)
    print(f"runs dir: {runs_dir.resolve()}")
    if not runs_dir.is_dir():
        print("note: the directory does not exist yet — no runs recorded.")
        return 0
    out = generate_report(
        runs_dir,
        out=Path(args.out) if args.out else None,
        html=args.html,
    )
    print(f"report:   {out.resolve()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bench",
        description="Benchmark harness for the full drcode agent loop "
        "(coding → testing → compaction) with a model per role.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser(
        "run", help="run the matrix: scenarios × combos × repeats (§8)"
    )
    run.add_argument("--scenario", required=True, help="scenario id, or 'all'")
    run.add_argument("--matrix", default=str(DEFAULT_MATRIX), help="path to matrix.toml")
    run.add_argument("--combo", default="", help="only this combo (empty = all)")
    run.add_argument("--parallel", type=int, default=1, help="max concurrent run subprocesses")
    run.add_argument("--repeats", type=int, default=3, help="repeats per pair (default 3)")
    run.add_argument("--runs-dir", default="runs", help="artifacts directory (default runs/)")
    run.add_argument(
        "--no-report", action="store_true", help="skip the end-of-sweep report"
    )
    run.add_argument(
        "--use-proxy",
        action="store_true",
        help="route every run through the local proxy (§9) — scenarios "
        "with a [proxy] section use their fault script, the rest get a "
        "fault-free recording proxy",
    )
    run.set_defaults(func=_cmd_run)

    report = sub.add_parser(
        "report", help="aggregate runs into report.md (drcode-bench.md §10)"
    )
    report.add_argument("runs_dir", nargs="?", default="runs", help="runs directory")
    report.add_argument(
        "--out", default="", help="output path (default: <runs_dir>/report.md)"
    )
    report.add_argument(
        "--html",
        action="store_true",
        help="also write an HTML version next to the markdown report",
    )
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
