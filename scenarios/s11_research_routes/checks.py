"""Mechanical correctness check of s11_research_routes (plan §7; the
research scenario, variant V3 — a route table extracted from a seed
mini-router, the hardest output format of the research family to parse).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. The REFERENCE route table is RECOMPUTED from the workspace seed by
     the same decorator parsing the brief describes («@route("METHOD
     /path") directly above its def handler»): every (method, path,
     handler) triple must be unique and there must be 4–6 of them —
     a drifted seed fails here loudly instead of passing (the same
     single-source-of-truth contract as S9/S10; nothing is hardcoded
     twice).
  2. docs/routes.md exists and answers the table with EVERY reference
     triple. Markdown tables are the most fragile output of the whole
     research family, so the parsing is deliberately LENIENT: line by
     line, a route row is any line that carries an HTTP method token
     AND a slash-path token; separators (|-ro_ws) and the header line
     are ignored. A reference triple is answered when SOME route row
     contains all three parts (method as a standalone token, the path,
     the handler); the brief pins the column ORDER, but a row that
     happens to carry them backtick-quoted or pipe-separated still
     counts. EXTRA route rows — a (method, path) pair that is not in
     the reference — bite: the agent must not invent routes.
  3. The task JSON in <workspace>/.drcode/tasks/ shows the research
     contract: EXACTLY ONE task kind=research, status=completed, ZERO
     testing rounds (research skips the tester, plan §7) and no
     verification label (research ends with mark_done — there is
     nothing to verify).
  4. The stricter git check: `git log -- docs/routes.md` is non-empty,
     i.e. the research agent's mandatory git_commit_docs really
     committed the table (the workspace is a git repo with a seed
     commit, bench/env_setup.py; the brief told the agent to create
     the file with write_file so it lands in task.edited_files and is
     committable). If git itself is unavailable the check is skipped —
     a report committed by no means is caught by (3)'s event trail in
     the diagnostics instead.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

# The seed contract: "@route(\"METHOD /path\")" directly above "def name".
ROUTE_DECORATOR_RE = re.compile(r'@route\("([A-Z]+)\s+([^"]+)"\)\s*\ndef\s+(\w+)')
SEED_PACKAGE = "src/api"
ROUTE_COUNT_RANGE = (4, 6)  # the seed size the scenario.toml header promises

HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
_METHOD_TOKEN_RE = re.compile(r"(?<![A-Za-z])(%s)(?![A-Za-z])" % "|".join(HTTP_METHODS))
_DEF_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_SEPARATOR_LINE_RE = re.compile(r"^[\s|:\-]*$")


def seed_routes(workspace: Path) -> set[tuple[str, str, str]]:
    """Extract the reference route table from the seed package — the same
    decorator parsing the brief describes to the agent."""
    routes: set[tuple[str, str, str]] = set()
    for path in sorted((workspace / SEED_PACKAGE).rglob("*.py")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"unreadable seed source {path}: {exc}") from exc
        routes.update(
            (method, path_spec, handler)
            for method, path_spec, handler in ROUTE_DECORATOR_RE.findall(text)
        )
    return routes


def _clean_token(token: str) -> str:
    """Strip the markdown dressing a row may carry: backticks, emphasis,
    trailing punctuation after a pipe cell."""
    return token.strip().strip("`*_").strip().rstrip(",.;:").strip()


def parse_route_rows(text: str) -> list[tuple[str, str, list[str]]]:
    """Lenient line-by-line parse of docs/routes.md: (method, path, tokens)
    for every line that carries both an HTTP method token and a slash-path
    token. Table separators and the header line never match."""
    rows: list[tuple[str, str, list[str]]] = []
    for line in text.splitlines():
        if _SEPARATOR_LINE_RE.match(line):
            continue
        tokens = [t for t in (_clean_token(part) for part in re.split(r"[|\s]+", line)) if t]
        method = next((t.upper() for t in tokens if _METHOD_TOKEN_RE.fullmatch(t)), None)
        route_path = next((t for t in tokens if t.startswith("/")), None)
        if method and route_path:
            rows.append((method, route_path, tokens))
    return rows


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    failures: list[str] = []

    # 1 (first: a drifted seed invalidates everything below).
    seed_pkg = workspace / SEED_PACKAGE
    if not seed_pkg.is_dir():
        print(f"S11 checks FAILED:\n- seed package missing: {seed_pkg}")
        return 1
    try:
        reference = seed_routes(workspace)
    except RuntimeError as exc:
        print(f"S11 checks FAILED:\n- {exc}")
        return 1
    if not ROUTE_COUNT_RANGE[0] <= len(reference) <= ROUTE_COUNT_RANGE[1]:
        failures.append(
            f"seed drift: the decorator parser found {len(reference)} routes in "
            f"{SEED_PACKAGE}/, expected {ROUTE_COUNT_RANGE[0]}–{ROUTE_COUNT_RANGE[1]} "
            "— the seed no longer matches the '@route(...) over def' contract"
        )

    # 2. docs/routes.md: every reference triple answered by one lenient
    #    route row; no extra rows with foreign (method, path) pairs.
    routes_md = workspace / "docs" / "routes.md"
    if not routes_md.is_file():
        failures.append("docs/routes.md is missing in the workspace")
    else:
        rows = parse_route_rows(routes_md.read_text(encoding="utf-8"))
        if not rows:
            failures.append(
                "docs/routes.md contains no parseable route rows: a route row is a "
                "line carrying an HTTP method (GET/POST/...) AND a /path — the brief "
                "pins the columns method | path | handler, one row per route"
            )
        for method, route_path, handler in sorted(reference):
            answered = any(
                m == method and p == route_path and handler in tokens
                for m, p, tokens in rows
            )
            if not answered:
                failures.append(
                    f"docs/routes.md does not answer the route {method} {route_path} "
                    f"-> {handler}: no single row carries all three (method as a "
                    "token, the path verbatim, the handler name)"
                )
        reference_pairs = {(m, p) for m, p, _ in reference}
        for method, route_path, _ in rows:
            if (method, route_path) not in reference_pairs:
                failures.append(
                    f"docs/routes.md has an EXTRA route row {method} {route_path} — "
                    "no such (method, path) pair exists in src/api/"
                )

    # 3. The research contract over the persisted task JSON.
    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(tasks_dir.glob("*.json"))]
    research = [t for t in tasks if t.get("kind") == "research"]
    if len(research) != 1:
        failures.append(
            f"expected exactly 1 task with kind=research in .drcode/tasks/, found {len(research)}"
        )
    for t in research:
        tid = t.get("id")
        if t.get("status") != "completed":
            failures.append(f"task {tid}: status={t.get('status')!r}, expected 'completed'")
        rounds = len(t.get("tester_messages") or [])
        if rounds != 0:
            failures.append(
                f"task {tid}: {rounds} testing rounds, expected 0 "
                "(research tasks skip the tester, plan §7)"
            )
        if t.get("verification") is not None:
            failures.append(
                f"task {tid}: verification={t.get('verification')!r}, expected None "
                "(research ends with mark_done and never gets a verdict label)"
            )

    # 4. The stricter git check: git_commit_docs committed the table.
    if routes_md.is_file():
        git_run = subprocess.run(
            ["git", "log", "--", "docs/routes.md"],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=False,
        )
        if git_run.returncode != 0:
            print(f"S11 checks: git log skipped ({git_run.stderr.strip()})")
        elif not git_run.stdout.strip():
            failures.append(
                "git log -- docs/routes.md is empty — the route table was not "
                "committed by git_commit_docs (the documentation assignment "
                "must end with the agent committing its own changes)"
            )

    if failures:
        print("S11 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S11 checks: green (docs/routes.md answers all "
        f"{len(reference)} seed routes of {SEED_PACKAGE}/ with no extra rows, "
        "research task COMPLETED with 0 testing rounds, table committed)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
