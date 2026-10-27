"""Scenario loading (plan drcode-bench.md, §7).

One scenario = one folder `scenarios/<id>/`:

    scenarios/s1_happy/
    ├── seed/                  # seed repo: code + tests (copied by env_setup)
    ├── scenario.toml          # briefs, followups, clarification_answers, timeout
    └── checks.py              # mechanical post-run check (run by the harness)

scenario.toml:

    timeout = 45                # soft limit in MINUTES (plan §4: 30–60 min)

    [[briefs]]
    title = "..."
    text  = "..."
    kind  = "feature"           # "feature"/"bug"/"research" — research skips
                                # the tester entirely (plan §7), so a research
                                # brief forbids [settle] verification="passed"

    [settle]                    # scenario-specific part of the settle
                                # criterion (§4); see bench/settle.py
    verification = "passed"

    [context]                   # per-role max_context_tokens caps for THIS
    coding = 3000               # scenario (§1.2) — e.g. force compaction on
                                # the coding model. Beats the combo's own
                                # <role>_max_context_tokens overrides
                                # (deprecated) and the catalog value.

    [[followups]]               # consumed by the user simulator (§6)
    ...

    [[clarification_answers]]   # consumed by the user simulator (§6)
    ...

checks.py contract: executed as `python checks.py <workspace>`; exit 0 =
the scenario's mechanical correctness criterion holds. The verdict is
NEVER built on the agents' own words — the harness runs pytest and the
assertions itself (§7).
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .proxy import ProxyError, WatchdogSpec, parse_faults, parse_watchdog

# Plan §7 rule: research tasks skip the tester entirely (they end with
# mark_done and never get a verification label). They are queueable, but a
# scenario that wants a PASSED settle assertion must not use them.
ALLOWED_KINDS = ("feature", "bug", "research")

# The settle keys bench/settle.py knows how to evaluate. A scenario may not
# invent new ones silently — a typo'd key would otherwise just be ignored
# and the run would settle green without the intended assertion.
KNOWN_SETTLE_KEYS = ("verification",)

# Roles a scenario's `[context]` section may cap. `research` is allowed here
# but NOT validated against the combo at load time — the scenario does not
# know which combo it will run with; that cross-check (a research cap on a
# combo that assigns no research role would silently never apply) happens at
# planning time (bench.runner.plan_jobs) and for single runs in
# bench.run_one.main (bench.matrix.check_research_override_assigned).
CONTEXT_ROLES = ("coding", "tester", "compaction", "research")


class ScenarioError(ValueError):
    """Invalid scenario definition."""


@dataclass(frozen=True)
class Brief:
    """One task the harness queues via `TaskManager.create` (§4)."""

    title: str
    text: str
    kind: str  # "feature" | "bug" | "research" (validated against ALLOWED_KINDS)

    def task_kind(self):
        from drcode.models import TaskKind

        return TaskKind(self.kind)


@dataclass(frozen=True)
class Followup:
    """A user-simulator comment (§6), raw for now — the simulator arrives
    with stage 3; the loader already validates the shape."""

    task: str  # brief title or "all"/"last" — matched by the simulator
    when: str  # "verification_failed" | "elapsed" | "event:<text>"
    after_minutes: float | None  # for when="elapsed"
    text: str


@dataclass(frozen=True)
class ClarificationAnswer:
    """An auto-answer for AWAITING_CLARIFICATION (§6): matched by question
    substring when `match` is given, otherwise by order.

    `match` may be a single substring or a LIST of alternative substrings
    (any-of match): the agent paraphrases the same question run to run
    (s5 hit a paraphrase without the Latin «формат» — only the function
    name format_price), so one narrow needle made the matcher brittle."""

    match: str | list[str] | tuple[str, ...] | None
    answer: str

    @property
    def needles(self) -> tuple[str, ...]:
        """The substrings any of which must appear in the question
        (case-insensitive matching is done by the simulator)."""
        if self.match is None:
            return ()
        if isinstance(self.match, str):
            return (self.match,)
        return tuple(self.match)


@dataclass(frozen=True)
class ProxySpec:
    """The scenario's fault-injection proxy setup (§9): the harness starts
    the proxy BEFORE the run tree is generated and points every provider
    base_url at it (`env_setup.prepare_run(proxy_base=...)`).

        [proxy]
        enabled = true
        log_bodies = false          # full request bodies into proxy_log.jsonl

        [[proxy.faults]]
        kind = "http_429"           # http_429 | drop | delay
        nth = 1                     # 1-based over the requests matching scope
        scope = "chat/completions"  # path substring, "" = every request

        # Optional stall watchdog (§9, opt-in): an upstream silent for
        # `stall_timeout_s` (no headers/body/SSE bytes) is aborted and
        # retried once by the proxy, transparently for drcode. MASKS real
        # provider tail latency — enable only for scenarios where the
        # tail is infrastructure noise (e.g. s4_compaction_tester,
        # s8_fix_loop); the run is then marked in result.json
        # (`proxy_watchdog`) and metrics.json (`proxy.watchdog`).
        [proxy.watchdog]
        stall_timeout_s = 45        # seconds of upstream silence per attempt
        retries = 1                 # proxy-side retries per request
    """

    enabled: bool = True
    log_bodies: bool = False
    faults: tuple = ()  # tuple[FaultSpec, ...] (bench.proxy.FaultSpec)
    watchdog: WatchdogSpec | None = None  # opt-in stall watchdog (§9)


@dataclass(frozen=True)
class Scenario:
    id: str
    dir: Path
    briefs: tuple[Brief, ...]
    timeout_min: float  # soft limit, MINUTES (plan §4)
    settle: dict[str, object] = field(default_factory=dict)
    followups: tuple[Followup, ...] = ()
    clarification_answers: tuple[ClarificationAnswer, ...] = ()
    proxy: ProxySpec | None = None  # §9: fault-injection proxy setup
    # Per-role max_context_tokens caps of the `[context]` section (§1.2):
    # compaction scenarios force a SMALL context on the compacted role
    # (S3 → coding, S4 → tester) as part of the scenario itself — no
    # service combos in matrix.toml needed. Priority over the combo's own
    # (deprecated) per-role overrides and the catalog value.
    max_context_overrides: tuple[tuple[str, int], ...] = ()

    @property
    def timeout_seconds(self) -> float:
        return self.timeout_min * 60.0

    def max_context_override(self, role: str) -> int | None:
        """The scenario's `max_context_tokens` cap for a role (None = the
        scenario does not cap it)."""
        for r, value in self.max_context_overrides:
            if r == role:
                return value
        return None

    @property
    def checks_file(self) -> Path:
        return self.dir / "checks.py"

    @property
    def seed_dir(self) -> Path:
        return self.dir / "seed"

    def settle_ok(self, tasks) -> str | None:
        """Scenario-specific part of the settle criterion (§4): `tasks` are
        the target tasks created from `briefs`. Returns None when the
        scenario's assertions hold, otherwise a human-readable reason."""

        for task in tasks:
            expected = self.settle.get("verification")
            if expected == "passed" and not _verification_passed(task):
                return (
                    f"task '{task.title}' settled with verification="
                    f"{getattr(task.verification, 'value', task.verification)!r}, "
                    f"expected PASSED"
                )
        return None


def _verification_passed(task) -> bool:
    from drcode.models import VerificationStatus

    return task.verification is VerificationStatus.PASSED


def _parse_briefs(data: dict) -> tuple[Brief, ...]:
    raw = data.get("briefs")
    if not raw:
        raise ScenarioError("scenario.toml: [[briefs]] is required (the run has nothing to do)")
    briefs = []
    for i, b in enumerate(raw):
        kind = str(b.get("kind", "feature"))
        if kind not in ALLOWED_KINDS:
            raise ScenarioError(
                f"briefs[{i}]: kind {kind!r} not allowed — use one of {ALLOWED_KINDS}"
            )
        title = str(b.get("title", "")).strip()
        text = str(b.get("text", "")).strip()
        if not text:
            raise ScenarioError(f"briefs[{i}]: text is required")
        briefs.append(Brief(title=title or text.splitlines()[0][:60], text=text, kind=kind))
    return tuple(briefs)


def _parse_settle(data: dict) -> dict[str, object]:
    settle = dict(data.get("settle") or {})
    unknown = [k for k in settle if k not in KNOWN_SETTLE_KEYS]
    if unknown:
        raise ScenarioError(f"[settle]: unknown key(s) {unknown} — known: {KNOWN_SETTLE_KEYS}")
    verification = settle.get("verification")
    if verification is not None and verification not in ("passed", "any"):
        raise ScenarioError(
            f"[settle] verification must be 'passed' or 'any', got {verification!r}"
        )
    return settle


def _check_research_settle(briefs: tuple[Brief, ...], settle: dict[str, object], path) -> None:
    """A research brief can never satisfy settle verification="passed"
    (plan §7): research ends with mark_done and never receives a
    verification label — there is no «verification successfully» for it.
    Mixed scenarios (research + spawned feature/bug tasks) must use
    verification="any" or omit the key; the spawned tasks' PASSED is
    asserted by checks.py on the task JSON."""
    if settle.get("verification") != "passed":
        return
    titles = [b.title for b in briefs if b.kind == "research"]
    if titles:
        raise ScenarioError(
            f"{path}: [settle] verification='passed' is impossible with "
            f"research brief(s) {titles} — research never passes the tester "
            "(plan §7); use verification='any' or omit the key"
        )


def _parse_followups(data: dict) -> tuple[Followup, ...]:
    out = []
    for i, f in enumerate(data.get("followups") or []):
        when = str(f.get("when", "elapsed"))
        if when not in ("verification_failed", "elapsed") and not when.startswith("event:"):
            # Bare "event" is rejected on purpose: without a needle it can
            # never fire, and a silently dead followup is worse than a
            # loud load error (plan §6 p.2: condition = failed verdict /
            # elapsed / event:<needle>).
            raise ScenarioError(
                f"followups[{i}]: unsupported when={when!r} — use "
                "'verification_failed', 'elapsed' or 'event:<needle>'"
            )
        after = f.get("after_minutes")
        if when == "elapsed" and after is None:
            raise ScenarioError(f"followups[{i}]: when='elapsed' needs after_minutes")
        if not str(f.get("text", "")).strip():
            raise ScenarioError(f"followups[{i}]: text is required")
        out.append(
            Followup(
                task=str(f.get("task", "last")),
                when=when,
                after_minutes=float(after) if after is not None else None,
                text=str(f["text"]),
            )
        )
    return tuple(out)


def _parse_clarification_answers(data: dict) -> tuple[ClarificationAnswer, ...]:
    out = []
    for i, a in enumerate(data.get("clarification_answers") or []):
        answer = str(a.get("answer", "")).strip()
        if not answer:
            raise ScenarioError(f"clarification_answers[{i}]: answer is required")
        out.append(ClarificationAnswer(match=_parse_match(a.get("match"), i), answer=answer))
    return tuple(out)


def _parse_match(raw: object, idx: int) -> str | list[str] | tuple[str, ...] | None:
    """`match` is a substring or an array of alternative substrings
    (any-of); anything else is a loud load error, not a silently dead
    matcher."""
    if raw is None:
        return None
    if isinstance(raw, str):
        return raw.strip() or None
    if isinstance(raw, list) and raw and all(isinstance(m, str) for m in raw):
        needles = tuple(str(m).strip() for m in raw if str(m).strip())
        if needles:
            return needles
    raise ScenarioError(
        f"clarification_answers[{idx}]: match must be a substring or a "
        f"non-empty array of substrings, got {raw!r}"
    )


def _parse_proxy(data: dict) -> ProxySpec | None:
    """The optional `[proxy]` section (§9): fault-injection proxy for this
    scenario. Faults are validated here — an unknown fault kind must fail
    the scenario load, not silently pass every request through. Same for
    the optional `[proxy.watchdog]` table (stall watchdog)."""
    raw = data.get("proxy")
    if not raw:
        return None
    if not isinstance(raw, dict):
        raise ScenarioError("[proxy] must be a table")
    try:
        faults = parse_faults(raw.get("faults") or [])
        watchdog = parse_watchdog(raw.get("watchdog"))
    except ProxyError as e:
        raise ScenarioError(f"[proxy]: {e}") from None
    spec = ProxySpec(
        enabled=bool(raw.get("enabled", True)),
        log_bodies=bool(raw.get("log_bodies", False)),
        faults=faults,
        watchdog=watchdog,
    )
    if spec.faults and not spec.enabled:
        raise ScenarioError("[proxy]: faults defined but enabled = false")
    return spec


def _parse_max_context_overrides(data: dict) -> tuple[tuple[str, int], ...]:
    """The optional `[context]` section (§1.2): per-role `max_context_tokens`
    caps for this scenario — the "how to trigger compaction" knowledge lives
    in the scenario itself (the `[proxy]` precedent, §9), not in service
    combos of matrix.toml. Same loud-error principle as KNOWN_SETTLE_KEYS:
    an unknown role or a non-positive/non-integer value fails the scenario
    load instead of being silently ignored. The override travels into
    `env_setup.materialize_providers`, which writes the cap into the
    generated catalog entry of the role's model (§1.2)."""
    raw = data.get("context")
    if not raw:
        return ()
    if not isinstance(raw, dict):
        raise ScenarioError("[context] must be a table of role = max_context_tokens")
    out: list[tuple[str, int]] = []
    for role, value in raw.items():
        if role not in CONTEXT_ROLES:
            raise ScenarioError(f"[context]: unknown role {role!r} — known roles: {CONTEXT_ROLES}")
        # bool is an int subclass in Python — reject it explicitly: a
        # `coding = true` cap is a typo, not a limit.
        if isinstance(value, bool) or not isinstance(value, int):
            raise ScenarioError(f"[context] {role}: must be an integer (tokens), got {value!r}")
        if value <= 0:
            raise ScenarioError(f"[context] {role}: must be > 0, got {value}")
        out.append((role, int(value)))
    return tuple(out)


def load_scenario(path: Path) -> Scenario:
    """Parse `scenarios/<id>/scenario.toml` into a `Scenario`."""
    path = Path(path)
    # Accept either the scenario folder or the toml file itself.
    scenario_toml = path / "scenario.toml" if path.is_dir() else path
    try:
        data = tomllib.loads(scenario_toml.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ScenarioError(f"scenario file not found: {scenario_toml}") from None
    except tomllib.TOMLDecodeError as e:
        raise ScenarioError(f"{scenario_toml}: {e}") from None

    sid = str(data.get("id") or path.name)
    timeout = data.get("timeout")
    if timeout is None:
        raise ScenarioError(f"{scenario_toml}: 'timeout' (minutes) is required")
    timeout = float(timeout)
    if not 0 < timeout <= 24 * 60:
        raise ScenarioError(f"{scenario_toml}: timeout must be in (0, 1440] minutes")

    briefs = _parse_briefs(data)
    settle = _parse_settle(data)
    _check_research_settle(briefs, settle, scenario_toml)

    return Scenario(
        id=sid,
        dir=scenario_toml.parent,
        briefs=briefs,
        timeout_min=timeout,
        settle=settle,
        followups=_parse_followups(data),
        clarification_answers=_parse_clarification_answers(data),
        proxy=_parse_proxy(data),
        max_context_overrides=_parse_max_context_overrides(data),
    )


def load_scenario_by_id(scenarios_root: Path, scenario_id: str) -> Scenario:
    """Resolve `scenarios/<id>/`; also accepts 'all' is NOT handled here —
    the orchestrator expands it before calling."""
    return load_scenario(scenarios_root / scenario_id)
