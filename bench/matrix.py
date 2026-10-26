"""Parsing of `matrix.toml` (plan §8): providers + per-role combos.

The format mirrors the user-level catalog of drcode (`Provider`/`ModelEntry`
in `drcode/src/drcode/providers.py`): each provider has a `base_url`, an
`api_key` and a table of models keyed by model id. API keys support
host-env substitution: `api_key = "env:NAME"` is resolved from `os.environ`
when the combo is materialized — the key value never has to live in the
file itself.

A model table key is normally the wire name too; an optional `model` field
turns the key into a local alias for a real provider model (`ModelSpec`,
§8) — materialized into a virtual provider by `env_setup.materialize_providers`.

A combo assigns a `"<provider>/<model-id>"` reference to each of the
three REQUIRED agent roles drcode knows about (`AgentRole`): coding,
tester, compaction. The fourth role, research, is OPTIONAL
(`research = "provider/model"`): when a combo does not assign it, the
research role is absent from the generated selection and drcode itself
falls back to the coding model (`providers.resolve_effective`) — every
pre-research matrix.toml stays valid.

Per-role `max_context_tokens` overrides of a combo
(`<role>_max_context_tokens`) are DEPRECATED: the "small context"
compaction pressure is scenario knowledge now — a `[context]` section in
scenario.toml (bench.scenario) — and it WINS over the combo's overrides
(priority: scenario → combo → catalog). The combo-level mechanism is
kept for backwards compatibility; matrix.toml no longer uses it.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROLES = ("coding", "tester", "compaction")
# Roles a combo MAY additionally assign; absent = drcode's own fallback.
OPTIONAL_ROLES = ("research",)


class MatrixError(ValueError):
    """Invalid or inconsistent matrix.toml."""


@dataclass(frozen=True)
class ModelSpec:
    """One model of a provider, as written in matrix.toml.

    `model` (optional, §8) is the REAL model name at the provider; the
    table key (`id`) then acts only as a local alias — e.g. one provider
    model described twice with different context caps
    (`[models.qwen3-8b-small-ctx]` with `model = "qwen3-8b"`). Empty
    (default) means the table key IS the wire name, as before — drcode
    sends the catalog id to the provider verbatim, so an alias entry is
    materialized into a virtual provider by
    `env_setup.materialize_providers` (§1.2 mechanism reuse).

    The alias mechanism is UNUSED by the repo's matrix.toml now: the
    compaction pressure lives in the scenario's `[context]` section, which
    needs no second catalog entry. Kept (with tests) as a generic
    capability of the matrix parser.

    `price_input` / `price_output` (optional, $ per 1M tokens) feed the
    report's quality ranking (§10: cost = α·t_norm + β·m_norm). A model
    missing EITHER price has NO price — the report renders its money axis
    as "—" and keeps the pair out of money-based ranking. Both fields
    absent (the default) keeps every existing matrix.toml valid.
    """

    provider: str
    id: str
    max_context_tokens: int = 200_000
    max_tokens: int | None = None
    compaction_threshold: int | None = None
    model: str = ""
    price_input: float | None = None
    price_output: float | None = None

    @property
    def is_priced(self) -> bool:
        """True when BOTH prices are set (a half-priced model is unpriced)."""
        return self.price_input is not None and self.price_output is not None

    @property
    def wire_name(self) -> str:
        """The model name the provider actually receives in API requests:
        the explicit `model` when set, otherwise the catalog id itself."""
        return self.model or self.id

    @property
    def is_alias(self) -> bool:
        """True when the table key is only a local alias (`model` set and
        different from `id`)."""
        return bool(self.model) and self.model != self.id


@dataclass(frozen=True)
class ProviderSpec:
    """One OpenAI-compatible endpoint from matrix.toml."""

    name: str
    base_url: str
    api_key: str = ""
    models: dict[str, ModelSpec] = None  # type: ignore[assignment]

    def model(self, model_id: str) -> ModelSpec:
        try:
            return self.models[model_id]
        except KeyError:
            raise MatrixError(
                f"provider '{self.name}' has no model '{model_id}' "
                f"(known: {', '.join(sorted(self.models))})"
            ) from None


@dataclass(frozen=True)
class Combo:
    """One matrix combination: role → provider/model reference.

    `max_context_overrides` carries the per-role `max_context_tokens`
    overrides of the combo (plan §1.2/§8): compaction scenarios need a SMALL
    context on the compacted role (S3 → the coding model's mid-run gate,
    S4 → the tester model's mid-round gate — since drcode 0.5.0 both gates
    read the role's own resolved config), and the override must be written
    into the catalog entry (models.json) — the layer `providers.resolve`
    reads a role's connection and context from — so that the run does not
    have to depend on `DRCODE_MAX_CONTEXT_TOKENS` env (which subprocess
    hygiene strips anyway, §13; the flat-config fallback itself is gone in
    0.5.0). TOML form, flat per role:

        [[combo]]
        name     = "..."
        coding   = "provider-a/model"
        research = "provider-a/researcher"   # optional
        coding_max_context_tokens = 3000

    DEPRECATED: the compaction pressure is scenario knowledge now — the
    `[context]` section of scenario.toml (bench.scenario), which WINS over
    the combo's overrides (`effective_max_context` priority scenario →
    combo → catalog). Keep this mechanism only for backwards compatibility.
    """

    name: str
    coding: str
    tester: str
    compaction: str
    research: str | None = None
    max_context_overrides: tuple[tuple[str, int], ...] = ()

    def ref(self, role: str) -> str:
        value = getattr(self, role)
        if value is None:
            raise MatrixError(f"combo '{self.name}': optional role '{role}' is not assigned")
        return value

    def roles(self) -> dict[str, str]:
        """The combo's assigned roles in a deterministic order: the three
        required roles in ROLES order, then every assigned optional role —
        research last (the ctx-conflict resolution of env_setup keeps the
        original provider for the first role of a group, so the required
        roles must keep priority over research)."""
        roles = {role: self.ref(role) for role in ROLES}
        for role in OPTIONAL_ROLES:
            value = getattr(self, role)
            if value is not None:
                roles[role] = value
        return roles

    def max_context_override(self, role: str) -> int | None:
        """The combo's `max_context_tokens` override for a role (None =
        keep the model's catalog value)."""
        for r, value in self.max_context_overrides:
            if r == role:
                return value
        return None


def _resolve_api_key(value: str) -> str:
    """Substitute `env:NAME` api_keys from the host environment."""
    if value.startswith("env:"):
        var = value[4:]
        return os.environ.get(var, "")
    return value


def parse_ref(ref: str, context: str) -> tuple[str, str]:
    """Split `"<provider>/<model-id>"` (exactly one `/`: drcode ≥ 0.5
    forbids `/` in provider names and model ids — `ModelEntry`/`Provider`
    validators — so a second `/` in a ref is a matrix error, not a model
    id with a slash)."""
    provider, sep, model = ref.partition("/")
    if not sep or not provider or not model:
        raise MatrixError(f"invalid model reference {ref!r} ({context})")
    if "/" in model:
        raise MatrixError(
            f"invalid model reference {ref!r} ({context}): '/' is not "
            "allowed in model ids (drcode reference format)"
        )
    return provider, model


def _parse_max_context_overrides(
    raw: dict, *, combo_name: str, assigned: tuple[str, ...]
) -> tuple[tuple[str, int], ...]:
    """Per-role `max_context_tokens` overrides of a combo entry: flat TOML
    keys `<role>_max_context_tokens` (§1.2: the small context goes to the
    compacted role — S3 → coding, S4 → tester; since drcode 0.5.0 each
    compaction gate reads its own role's resolved config). An override on
    an unassigned optional role would silently never apply (the role
    falls back to coding and reads coding's resolved config), so it is an
    error instead.

    DEPRECATED: the scenario's `[context]` section (bench.scenario) is the
    working path — it wins over these combo overrides; kept for backwards
    compatibility with existing matrices."""
    out: list[tuple[str, int]] = []
    for role in (*ROLES, *OPTIONAL_ROLES):
        value = raw.get(f"{role}_max_context_tokens")
        if value is None:
            continue
        if role not in assigned:
            raise MatrixError(
                f"combo '{combo_name}': {role}_max_context_tokens is set, "
                f"but the combo assigns no '{role}' role"
            )
        value = int(value)
        if value <= 0:
            raise MatrixError(f"combo '{combo_name}': {role}_max_context_tokens must be > 0")
        out.append((role, value))
    return tuple(out)


def max_context_source(
    combo: Combo, role: str, scenario_overrides: tuple[tuple[str, int], ...] = ()
) -> str:
    """Where the role's max_context_tokens comes from: `"scenario"` (the
    `[context]` section of scenario.toml), `"combo"` (a deprecated
    `<role>_max_context_tokens` combo key) or `"catalog"` (the model's own
    value). Same priority `effective_max_context` resolves with."""
    if any(r == role for r, _ in scenario_overrides):
        return "scenario"
    if combo.max_context_override(role) is not None:
        return "combo"
    return "catalog"


def effective_max_context(
    combo: Combo,
    providers: dict[str, ProviderSpec],
    role: str,
    scenario_overrides: tuple[tuple[str, int], ...] = (),
) -> int:
    """The max_context_tokens the role will actually run with, by priority
    (§1.2): the scenario's `[context]` cap → the combo's (deprecated)
    per-role override → the catalog value of the referenced model."""
    for r, value in scenario_overrides:
        if r == role:
            return value
    override = combo.max_context_override(role)
    if override is not None:
        return override
    provider_name, model_id = parse_ref(combo.ref(role), f"combo '{combo.name}' role {role}")
    return providers[provider_name].model(model_id).max_context_tokens


def check_research_override_assigned(
    combo: Combo, scenario_overrides: tuple[tuple[str, int], ...], where: str
) -> None:
    """A `[context] research` cap on a combo that assigns no research role
    would silently never apply (the role falls back to coding and reads
    coding's resolved config) — a loud error instead, at the point that
    knows BOTH sides: the planning (`bench.runner.plan_jobs`) and the
    single-run entry (`bench.run_one.main`). The scenario load itself
    CANNOT do this check — it does not know the combo."""
    if not any(role == "research" for role, _ in scenario_overrides):
        return
    if combo.research is None:
        raise MatrixError(
            f"{where}: [context] research is set, but combo '{combo.name}' "
            "assigns no 'research' role — the cap would silently never "
            "apply (the role falls back to coding); assign research in the "
            "combo or drop the cap"
        )


def _parse_price(value: object, where: str) -> float | None:
    """Optional per-model price ($ per 1M tokens): absent = no price,
    present = a non-negative number (a negative or non-numeric price is
    a loud matrix error, not a silently unpriced model)."""
    if value is None:
        return None
    try:
        price = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        raise MatrixError(f"{where}: not a number: {value!r}") from None
    if price < 0:
        raise MatrixError(f"{where}: must be >= 0, got {price}")
    return price


def load_matrix(path: Path) -> tuple[dict[str, ProviderSpec], list[Combo]]:
    """Parse matrix.toml → (providers by name, combos)."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise MatrixError(f"matrix file not found: {path}") from None
    except tomllib.TOMLDecodeError as e:
        raise MatrixError(f"{path}: {e}") from None

    providers: dict[str, ProviderSpec] = {}
    for name, raw in (data.get("providers") or {}).items():
        # drcode ≥ 0.5 rejects "/" in provider names and model ids
        # (`ModelEntry`/`Provider` validators); catch it here with a
        # readable message instead of a pydantic ValidationError at
        # catalog load time (or a silently dropped ref, `_parse_ref`).
        if "/" in name:
            raise MatrixError(f"{path}: provider name '{name}' must not contain '/'")
        models: dict[str, ModelSpec] = {}
        for model_id, mraw in (raw.get("models") or {}).items():
            if "/" in model_id:
                raise MatrixError(f"{path}: model id '{name}/{model_id}' must not contain '/'")
            # Optional `model` field (§8): the real wire name behind a
            # local alias. Same reference format rules as the table key:
            # non-empty, no '/' (drcode `ModelEntry.id` validator).
            wire = mraw.get("model")
            if wire is not None:
                wire = str(wire)
                if not wire:
                    raise MatrixError(
                        f"{path}: model '{name}/{model_id}': 'model' must not be empty"
                    )
                if "/" in wire:
                    raise MatrixError(
                        f"{path}: model '{name}/{model_id}': wire name '{wire}' must "
                        "not contain '/' (drcode reference format)"
                    )
            models[model_id] = ModelSpec(
                provider=name,
                id=model_id,
                max_context_tokens=int(mraw.get("max_context_tokens", 200_000)),
                max_tokens=mraw.get("max_tokens"),
                compaction_threshold=mraw.get("compaction_threshold"),
                model=wire or "",
                price_input=_parse_price(
                    mraw.get("price_input"), f"{path}: model '{name}/{model_id}': price_input"
                ),
                price_output=_parse_price(
                    mraw.get("price_output"), f"{path}: model '{name}/{model_id}': price_output"
                ),
            )
        providers[name] = ProviderSpec(
            name=name,
            base_url=str(raw.get("base_url", "")),
            api_key=str(raw.get("api_key", "")),
            models=models,
        )

    combos: list[Combo] = []
    for i, raw in enumerate(data.get("combo") or []):
        missing = [r for r in ROLES if r not in raw]
        if missing:
            raise MatrixError(f"combo #{i}: missing roles: {', '.join(missing)}")
        name = str(raw.get("name", f"combo-{i}"))
        # Optional roles (research): assigned only when present in the TOML
        # — the missing-role check above stays on the required three.
        assigned = tuple(r for r in (*ROLES, *OPTIONAL_ROLES) if raw.get(r) is not None)
        combo = Combo(
            name=name,
            coding=str(raw["coding"]),
            tester=str(raw["tester"]),
            compaction=str(raw["compaction"]),
            research=str(raw["research"]) if raw.get("research") is not None else None,
            max_context_overrides=_parse_max_context_overrides(
                raw, combo_name=name, assigned=assigned
            ),
        )
        # Every referenced model must exist in the matrix.
        for role, ref in combo.roles().items():
            provider_name, model_id = parse_ref(ref, f"combo '{combo.name}' role {role}")
            if provider_name not in providers:
                raise MatrixError(
                    f"combo '{combo.name}' role {role}: unknown provider '{provider_name}'"
                )
            providers[provider_name].model(model_id)
        combos.append(combo)

    return providers, combos


def get_combo(path: Path, name: str) -> Combo:
    """Find one combo by name; empty name = the first combo."""
    _, combos = load_matrix(path)
    if not combos:
        raise MatrixError(f"{path}: no [[combo]] entries")
    if not name:
        return combos[0]
    for combo in combos:
        if combo.name == name:
            return combo
    known = ", ".join(c.name for c in combos)
    raise MatrixError(f"{path}: no combo named '{name}' (known: {known})")


def combo_api_key(providers: dict[str, ProviderSpec], ref: str) -> str:
    """Resolved api_key (env-substituted) of the provider behind `ref`."""
    provider_name, _ = parse_ref(ref, "api_key lookup")
    return _resolve_api_key(providers[provider_name].api_key)
