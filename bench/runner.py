"""The matrix runner (plan drcode-bench.md §8, stage 5 of §12).

    bench run --scenario <id|all> --matrix matrix.toml --parallel N --repeats K

A full sweep = N_scenarios × N_combos × K runs; every run is ONE
subprocess (`python -m bench.run_one <scenario> <combo> <run_dir>`) — the
isolation unit of the whole benchmark (§2): its own XDG_CONFIG_HOME, its
own scrubbed DRCODE_* environment, clean imports, no shared files and no
shared event loop. `--parallel` bounds the number of concurrent
subprocesses (provider rate limits; VRAM/slots for local gateways).

Infrastructure retries are kept STRICTLY apart from substantive failures
(§8/§13): a subprocess that died before the app started (run_one exit
code 2, no result.json, pre-flight/config failure) is an INFRASTRUCTURE
failure — the runner re-validates the configuration (matrix + scenario
parse, the exact "check the config first" order of §8) and repeats the
run in a fresh run_dir, up to `max_infra_retries` times. A substantive
failure (timeout, red checks.py, failed settle — a run that produced a
verdict) is just a data point: it lands in the report and is never
retried.

Artifacts: every attempt leaves its own `runs/<run_id>/` (result.json,
metrics.json, model_log.jsonl, user_sim.jsonl, stdout/stderr logs);
`runs/runner-summary.json` records the job plan and the retry history;
the report (§10) is regenerated over the whole runs dir at the end.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .matrix import (
    MatrixError,
    check_research_override_assigned,
    get_combo,
    load_matrix,
)
from .scenario import Scenario, ScenarioError, load_scenario

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_ROOT = PROJECT_ROOT / "scenarios"

# Reasons run_one writes into result.json for failures that happened
# BEFORE the application could do any work (§4): pre-flight, app boot,
# config readiness. A provider unreachable at start surfaces here too —
# these are the infrastructure failures §8 retries.
INFRA_REASON_PREFIXES = (
    "pre-flight failed",
    "DrCodeApp failed to start",
    "drcode config is not ready",
)

# Extra wall-clock grace on top of the scenario's own soft timeout: the
# subprocess must terminate itself (wait_settle enforces the scenario
# timeout); if it did not, the harness kills it and treats the attempt as
# infrastructure (the harness, not the model, failed).
GRACE_SECONDS = 900.0

MAX_INFRA_RETRIES = 2
INFRA_BACKOFF_S = 5.0


class RunnerError(RuntimeError):
    """The sweep cannot even be planned (broken matrix or scenario)."""


def format_duration(seconds: float) -> str:
    """Human-readable duration: days, hours, minutes, seconds — leading
    zero components are omitted (`45 s`, `1 m 30 s`, `2 h 5 s`,
    `1 d 0 h 0 m 1 s` keeps interior zeros; `< 1 s` → `0 s`)."""
    total = int(seconds)
    days, rem = divmod(total, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    parts: list[str] = []
    for value, unit in ((days, "d"), (hours, "h"), (minutes, "m"), (secs, "s")):
        if value or parts:
            parts.append(f"{value} {unit}")
    return " ".join(parts) if parts else "0 s"


def warn_missing_api_keys(matrix_path: Path) -> None:
    """§8: `api_key = "env:NAME"` is substituted from the HOST environment
    when the catalog is generated; a variable missing at planning time
    means the provider will run without a key — warn loudly now instead of
    failing (or worse, silently degrading) inside every subprocess."""
    providers, combos = load_matrix(matrix_path)
    for combo in combos:
        seen: set[str] = set()
        for role, ref in combo.roles().items():
            provider_name = ref.partition("/")[0]
            if provider_name in seen:
                continue
            seen.add(provider_name)
            raw = providers[provider_name].api_key
            if raw.startswith("env:") and not os.environ.get(raw[4:]):
                print(
                    f"warning: {matrix_path}: provider '{provider_name}' "
                    f"(combo '{combo.name}', role {role}) uses "
                    f"api_key = {raw!r}, but the variable is not set — "
                    "the provider will run without a key",
                    file=sys.stderr,
                )


# --- planning ------------------------------------------------------------------


def discover_scenarios(scenarios_root: Path) -> list[str]:
    """Every `scenarios/<id>/` with a scenario.toml, sorted (§7)."""
    return sorted(p.parent.name for p in Path(scenarios_root).glob("*/scenario.toml"))


def slug(text: str) -> str:
    """Filesystem-safe form of a scenario/combo name (combo names may
    contain `/` — `strong-coder/cheap-tester`)."""
    return re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-") or "unnamed"


@dataclass
class Job:
    """One (scenario, combo, repeat) unit of the sweep."""

    scenario: str
    combo: str
    repeat: int
    timeout_seconds: float
    use_proxy: bool = False  # §9: force the proxy for scenarios without [proxy]

    def run_id(self, stamp: str, attempt: int) -> str:
        base = f"{stamp}-{slug(self.scenario)}-{slug(self.combo)}-rep{self.repeat}"
        return base if attempt == 0 else f"{base}-try{attempt + 1}"


@dataclass
class JobOutcome:
    """What the runner remembers about one job (→ runner-summary.json)."""

    scenario: str
    combo: str
    repeat: int
    run_dirs: list[str] = field(default_factory=list)
    ok: bool | None = None  # None = no verdict (infrastructure unresolved)
    reason: str = ""
    infra_attempts: int = 0  # extra attempts beyond the first
    infra_errors: list[str] = field(default_factory=list)
    content_failure: bool = False

    @property
    def final_run_dir(self) -> str | None:
        return self.run_dirs[-1] if self.run_dirs else None


def plan_jobs(
    matrix_path: Path,
    scenarios_root: Path,
    scenario_filter: str,
    combo_filter: str,
    repeats: int,
    *,
    use_proxy: bool = False,
) -> tuple[list[Job], list[Scenario], list[str]]:
    """Expand the sweep into jobs; validates the matrix and every scenario
    up front (a typo must fail the planning, not burn run slots). Returns
    (jobs, loaded scenarios, combo names)."""
    try:
        _, combos = load_matrix(matrix_path)
    except MatrixError as e:
        raise RunnerError(f"matrix: {e}") from None
    if combo_filter:
        combos = [c for c in combos if c.name == combo_filter]
        if not combos:
            raise RunnerError(f"no combo named '{combo_filter}' in {matrix_path}")
    if not combos:
        raise RunnerError(f"{matrix_path}: no [[combo]] entries")

    if scenario_filter in ("all", ""):
        scenario_ids = discover_scenarios(scenarios_root)
        if not scenario_ids:
            raise RunnerError(f"no scenarios under {scenarios_root}")
    else:
        scenario_ids = [scenario_filter]

    scenarios: list[Scenario] = []
    for sid in scenario_ids:
        try:
            scenarios.append(load_scenario(scenarios_root / sid))
        except ScenarioError as e:
            raise RunnerError(f"scenario '{sid}': {e}") from None

    # A `[context] research` cap (§1.2) on a combo that assigns no research
    # role would silently never apply (the role falls back to coding) —
    # the planning knows BOTH sides, so it fails loudly here instead of
    # burning run slots on a run whose scenario factor never fired. The
    # scenario load cannot do this check (it does not know the combo).
    for sc in scenarios:
        for combo in combos:
            try:
                check_research_override_assigned(
                    combo, sc.max_context_overrides, f"scenario '{sc.id}'"
                )
            except MatrixError as e:
                raise RunnerError(str(e)) from None

    jobs = [
        Job(
            scenario=sc.id,
            combo=combo.name,
            repeat=repeat,
            timeout_seconds=sc.timeout_seconds,
            # §9: the scenario's own [proxy] section always wins; the
            # runner flag forces a fault-free proxy everywhere else.
            use_proxy=use_proxy or sc.proxy is not None,
        )
        for sc in scenarios
        for combo in combos
        for repeat in range(repeats)
    ]
    return jobs, scenarios, [c.name for c in combos]


# --- execution -----------------------------------------------------------------


def read_result(run_dir: Path) -> dict[str, Any] | None:
    path = run_dir / "result.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def is_infrastructure_failure(result: dict[str, Any] | None) -> bool:
    """A run that produced NO verdict or died before the app could do any
    work (§8). A substantive failure — the run settled/timeout out with a
    verdict, checks.py ran — is a data point, never an infra failure."""
    if result is None:
        return True
    if result.get("ok") is True:
        return False
    reason = str(result.get("reason") or "")
    return any(reason.startswith(prefix) for prefix in INFRA_REASON_PREFIXES)


def _revalidate_config(matrix_path: Path, job: Job) -> None:
    """§8: on an infrastructure failure, check the config FIRST, then
    repeat. Re-parses the matrix and the scenario — a persistent config
    error fails fast instead of burning retries."""
    get_combo(matrix_path, job.combo)
    load_matrix(matrix_path)


class Runner:
    """The parallel orchestrator over (scenario × combo × repeats)."""

    def __init__(
        self,
        matrix_path: Path,
        runs_dir: Path,
        *,
        parallel: int = 1,
        max_infra_retries: int = MAX_INFRA_RETRIES,
        verbose: bool = True,
    ) -> None:
        self.matrix_path = Path(matrix_path)
        self.runs_dir = Path(runs_dir)
        self.parallel = max(1, int(parallel))
        self.max_infra_retries = max(0, int(max_infra_retries))
        self.verbose = verbose
        self._print_lock = __import__("threading").Lock()

    def _log(self, message: str) -> None:
        if not self.verbose:
            return
        with self._print_lock:
            print(message, flush=True)

    # -- one attempt ---------------------------------------------------------

    def _attempt(self, job: Job, run_dir: Path) -> tuple[int, dict[str, Any] | None, float]:
        """One `bench.run_one` subprocess; returns (exit code, result.json
        or None, wall seconds). stdout/stderr land in the run dir (§10)."""
        run_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            sys.executable,
            "-m",
            "bench.run_one",
            job.scenario,
            job.combo,
            str(run_dir),
            "--matrix",
            str(self.matrix_path),
        ]
        if job.use_proxy:
            cmd.append("--use-proxy")
        started = time.monotonic()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(PROJECT_ROOT),
                timeout=job.timeout_seconds + GRACE_SECONDS,
                check=False,
            )
            rc, out, err = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as e:
            rc = 124
            out = (
                e.stdout.decode("utf-8", "replace")
                if isinstance(e.stdout, bytes)
                else (e.stdout or "")
            )
            err = (
                e.stderr.decode("utf-8", "replace")
                if isinstance(e.stderr, bytes)
                else (e.stderr or "")
            )
            err += f"\n[runner] subprocess killed after {job.timeout_seconds + GRACE_SECONDS:.0f} s"
        elapsed = time.monotonic() - started
        (run_dir / "stdout.log").write_text(out or "", encoding="utf-8")
        (run_dir / "stderr.log").write_text(err or "", encoding="utf-8")
        return rc, read_result(run_dir), elapsed

    # -- one job (with infra retries) -----------------------------------------

    def run_job(self, job: Job) -> JobOutcome:
        outcome = JobOutcome(scenario=job.scenario, combo=job.combo, repeat=job.repeat)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        for attempt in range(self.max_infra_retries + 1):
            run_dir = self.runs_dir / job.run_id(stamp, attempt)
            outcome.run_dirs.append(str(run_dir))
            self._log(
                f"[run] {job.scenario} × {job.combo} × rep{job.repeat}"
                + (f" (infra retry {attempt})" if attempt else "")
                + f" → {run_dir.name}"
            )
            rc, result, _elapsed = self._attempt(job, run_dir)
            if result is not None and result.get("ok") is True:
                outcome.ok = True
                outcome.reason = str(result.get("reason") or "ok")
                break
            if result is not None and not is_infrastructure_failure(result):
                # Substantive failure (§8/§13): a data point, NOT retried.
                outcome.ok = False
                outcome.content_failure = True
                outcome.reason = str(result.get("reason") or "failed")
                break
            # Infrastructure failure: re-check the config, then retry.
            detail = (
                f"exit code {rc}, no result.json"
                if result is None
                else f"exit code {rc}: {result.get('reason')}"
            )
            outcome.infra_errors.append(f"{run_dir.name}: {detail}")
            outcome.infra_attempts = attempt + 1
            if attempt < self.max_infra_retries:
                try:
                    _revalidate_config(self.matrix_path, job)
                except (MatrixError, ScenarioError) as e:
                    outcome.reason = f"config re-validation failed after infra failure: {e}"
                    break
                time.sleep(INFRA_BACKOFF_S)
        else:
            outcome.reason = outcome.reason or (
                "infrastructure failure after "
                f"{self.max_infra_retries + 1} attempts: {'; '.join(outcome.infra_errors)}"
            )
        if outcome.ok is None and not outcome.reason:
            outcome.reason = "no verdict produced"
        return outcome

    # -- the sweep --------------------------------------------------------------

    def run(self, jobs: list[Job]) -> list[JobOutcome]:
        warn_missing_api_keys(self.matrix_path)
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        outcomes: list[JobOutcome] = []
        started = time.monotonic()
        with ThreadPoolExecutor(max_workers=self.parallel) as pool:
            futures = [(job, pool.submit(self.run_job, job)) for job in jobs]
            for job, future in futures:
                outcome = future.result()
                outcomes.append(outcome)
                status = (
                    "OK"
                    if outcome.ok
                    else ("DATA-POINT (failed)" if outcome.ok is False else "INFRA-UNRESOLVED")
                )
                self._log(
                    f"[done] {job.scenario} × {job.combo} × rep{job.repeat}: {status}"
                    + (f" — {outcome.reason}" if outcome.reason and not outcome.ok else "")
                )
        self._log(f"[sweep] {len(jobs)} job(s) in {format_duration(time.monotonic() - started)}")
        self.write_summary(outcomes)
        return outcomes

    def write_summary(self, outcomes: list[JobOutcome]) -> Path:
        payload = {
            "schema": "runner-summary/v1",
            "matrix": str(self.matrix_path),
            "parallel": self.parallel,
            "max_infra_retries": self.max_infra_retries,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "jobs": [o.__dict__ for o in outcomes],
            "totals": {
                "jobs": len(outcomes),
                "ok": sum(1 for o in outcomes if o.ok is True),
                "content_failures": sum(1 for o in outcomes if o.ok is False),
                "infra_unresolved": sum(1 for o in outcomes if o.ok is None),
                "infra_retries": sum(o.infra_attempts for o in outcomes if o.ok is not None),
            },
        }
        out = self.runs_dir / "runner-summary.json"
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return out


def run_sweep(
    matrix_path: Path,
    scenarios_root: Path,
    runs_dir: Path,
    *,
    scenario_filter: str = "all",
    combo_filter: str = "",
    repeats: int = 3,
    parallel: int = 1,
    make_report: bool = True,
    use_proxy: bool = False,
) -> tuple[list[JobOutcome], Path | None]:
    """Plan + execute the sweep, then regenerate the report (§10).
    Returns (outcomes, report path or None)."""
    jobs, _, _ = plan_jobs(
        matrix_path,
        scenarios_root,
        scenario_filter,
        combo_filter,
        repeats,
        use_proxy=use_proxy,
    )
    runner = Runner(matrix_path, runs_dir, parallel=parallel)
    outcomes = runner.run(jobs)
    report_path: Path | None = None
    if make_report:
        from .report import generate_report

        report_path = generate_report(runs_dir)
    return outcomes, report_path
