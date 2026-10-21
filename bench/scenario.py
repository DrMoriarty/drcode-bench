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
    kind  = "feature"           # ONLY "feature"/"bug" — research never
                                # passes the tester (plan §7 rules)

    [settle]                    # scenario-specific part of the settle
                                # criterion (§4); see bench/settle.py
    verification = "passed"

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

# Plan §7 rule: research tasks skip the tester entirely, so they can never
# exercise the coding → testing loop the benchmark exists to measure.
ALLOWED_KINDS = ("feature", "bug")

# The settle keys bench/settle.py knows how to evaluate. A scenario may not
# invent new ones silently — a typo'd key would otherwise just be ignored
# and the run would settle green without the intended assertion.
KNOWN_SETTLE_KEYS = ("verification",)


class ScenarioError(ValueError):
    """Invalid scenario definition."""


@dataclass(frozen=True)
class Brief:
    """One task the harness queues via `TaskManager.create` (§4)."""

    title: str
    text: str
    kind: str  # "feature" | "bug" (validated against ALLOWED_KINDS)

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
    substring when `match` is given, otherwise by order."""

    match: str | None
    answer: str


@dataclass(frozen=True)
class Scenario:
    id: str
    dir: Path
    briefs: tuple[Brief, ...]
    timeout_min: float  # soft limit, MINUTES (plan §4)
    settle: dict[str, object] = field(default_factory=dict)
    followups: tuple[Followup, ...] = ()
    clarification_answers: tuple[ClarificationAnswer, ...] = ()

    @property
    def timeout_seconds(self) -> float:
        return self.timeout_min * 60.0

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
                f"briefs[{i}]: kind {kind!r} not allowed — use one of "
                f"{ALLOWED_KINDS} (research never passes the tester, plan §7)"
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
        raise ScenarioError(
            f"[settle]: unknown key(s) {unknown} — known: {KNOWN_SETTLE_KEYS}"
        )
    verification = settle.get("verification")
    if verification is not None and verification not in ("passed", "any"):
        raise ScenarioError(
            f"[settle] verification must be 'passed' or 'any', got {verification!r}"
        )
    return settle


def _parse_followups(data: dict) -> tuple[Followup, ...]:
    out = []
    for i, f in enumerate(data.get("followups") or []):
        when = str(f.get("when", "elapsed"))
        if when not in ("verification_failed", "elapsed", "event") and not when.startswith(
            "event:"
        ):
            raise ScenarioError(f"followups[{i}]: unsupported when={when!r}")
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
        match = a.get("match")
        out.append(
            ClarificationAnswer(
                match=str(match).strip() if match else None, answer=answer
            )
        )
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

    return Scenario(
        id=sid,
        dir=scenario_toml.parent,
        briefs=_parse_briefs(data),
        timeout_min=timeout,
        settle=_parse_settle(data),
        followups=_parse_followups(data),
        clarification_answers=_parse_clarification_answers(data),
    )


def load_scenario_by_id(scenarios_root: Path, scenario_id: str) -> Scenario:
    """Resolve `scenarios/<id>/`; also accepts 'all' is NOT handled here —
    the orchestrator expands it before calling."""
    return load_scenario(scenarios_root / scenario_id)
