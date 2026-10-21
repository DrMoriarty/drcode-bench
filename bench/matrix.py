"""Parsing of `matrix.toml` (plan §8): providers + per-role combos.

The format mirrors the user-level catalog of drcode (`Provider`/`ModelEntry`
in `drcode/providers.py`, see `models.json.example` of drcode): each
provider has a `base_url`, an `api_key` and a table of models keyed by
model id. API keys support host-env substitution: `api_key = "env:NAME"`
is resolved from `os.environ` when the combo is materialized — the key
value never has to live in the file itself.

A combo assigns a `"<provider>/<model-id>"` reference to each of the
three agent roles drcode knows about (`AgentRole`): coding, tester,
compaction.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROLES = ("coding", "tester", "compaction")


class MatrixError(ValueError):
    """Invalid or inconsistent matrix.toml."""


@dataclass(frozen=True)
class ModelSpec:
    """One model of a provider, as written in matrix.toml."""

    provider: str
    id: str
    max_context_tokens: int = 200_000
    max_tokens: int | None = None
    compaction_threshold: int | None = None


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
    """One matrix combination: role → provider/model reference."""

    name: str
    coding: str
    tester: str
    compaction: str

    def ref(self, role: str) -> str:
        return getattr(self, role)

    def roles(self) -> dict[str, str]:
        return {role: self.ref(role) for role in ROLES}


def _resolve_api_key(value: str) -> str:
    """Substitute `env:NAME` api_keys from the host environment."""
    if value.startswith("env:"):
        var = value[4:]
        return os.environ.get(var, "")
    return value


def parse_ref(ref: str, context: str) -> tuple[str, str]:
    """Split `"<provider>/<model-id>"` (model ids may contain `/`)."""
    provider, sep, model = ref.partition("/")
    if not sep or not provider or not model:
        raise MatrixError(f"invalid model reference {ref!r} ({context})")
    return provider, model


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
        models: dict[str, ModelSpec] = {}
        for model_id, mraw in (raw.get("models") or {}).items():
            models[model_id] = ModelSpec(
                provider=name,
                id=model_id,
                max_context_tokens=int(mraw.get("max_context_tokens", 200_000)),
                max_tokens=mraw.get("max_tokens"),
                compaction_threshold=mraw.get("compaction_threshold"),
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
        combo = Combo(
            name=str(raw.get("name", f"combo-{i}")),
            coding=str(raw["coding"]),
            tester=str(raw["tester"]),
            compaction=str(raw["compaction"]),
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
