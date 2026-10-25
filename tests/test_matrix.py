"""Tests of bench/matrix parsing: the optional `model` field (§8) that
turns a model table key into a local alias for a real provider model."""

from __future__ import annotations

from pathlib import Path

import pytest
from bench.matrix import ROLES, MatrixError, load_matrix

ALIAS_MATRIX = """\
[providers.fake-b]
base_url = "http://fake-b.local:9001/v1"
api_key  = ""

[providers.fake-b.models.qwen3-8b]
max_context_tokens = 8192
max_tokens = 2048

[providers.fake-b.models.qwen3-8b-small-ctx]
model = "qwen3-8b"
max_context_tokens = 4096
max_tokens = 4096

[[combo]]
name       = "alias-combo"
coding     = "fake-b/qwen3-8b-small-ctx"
tester     = "fake-b/qwen3-8b"
compaction = "fake-b/qwen3-8b"
"""


@pytest.fixture
def alias_matrix_file(tmp_path: Path) -> Path:
    path = tmp_path / "matrix.toml"
    path.write_text(ALIAS_MATRIX, encoding="utf-8")
    return path


def test_model_spec_defaults_to_table_key(alias_matrix_file: Path) -> None:
    """No `model` field: the table key IS the wire name (backwards
    compatible with every existing matrix.toml)."""
    providers, _ = load_matrix(alias_matrix_file)
    plain = providers["fake-b"].model("qwen3-8b")
    assert plain.model == ""
    assert plain.wire_name == "qwen3-8b"
    assert not plain.is_alias


def test_model_spec_parses_alias(alias_matrix_file: Path) -> None:
    """`model` field: the table key is a local alias, `wire_name` is the
    real name the provider receives; caps come from the alias entry."""
    providers, combos = load_matrix(alias_matrix_file)
    alias = providers["fake-b"].model("qwen3-8b-small-ctx")
    assert alias.model == "qwen3-8b"
    assert alias.id == "qwen3-8b-small-ctx"
    assert alias.wire_name == "qwen3-8b"
    assert alias.is_alias
    assert alias.max_context_tokens == 4096
    # The combo keeps referencing the alias.
    assert combos[0].coding == "fake-b/qwen3-8b-small-ctx"


@pytest.mark.parametrize(
    ("snippet", "match"),
    [
        ('model = ""', "must not be empty"),
        ('model = "ns/other"', "must not contain '/'"),
    ],
)
def test_model_field_validation(tmp_path: Path, snippet: str, match: str) -> None:
    matrix = f"""\
[providers.fake-b]
base_url = "http://fake-b.local:9001/v1"

[providers.fake-b.models.alias-x]
{snippet}
max_context_tokens = 4096

[[combo]]
name   = "c"
coding = "fake-b/alias-x"
tester = "fake-b/alias-x"
compaction = "fake-b/alias-x"
"""
    path = tmp_path / "matrix.toml"
    path.write_text(matrix, encoding="utf-8")
    with pytest.raises(MatrixError, match=match):
        load_matrix(path)


def test_model_equal_to_key_is_not_alias(tmp_path: Path) -> None:
    """`model` explicitly equal to the table key: legal, but not an alias
    (no virtualization needed — the id is already the wire name)."""
    matrix = """\
[providers.fake-b]
base_url = "http://fake-b.local:9001/v1"

[providers.fake-b.models.m1]
model = "m1"
max_context_tokens = 4096

[[combo]]
name   = "c"
coding = "fake-b/m1"
tester = "fake-b/m1"
compaction = "fake-b/m1"
"""
    path = tmp_path / "matrix.toml"
    path.write_text(matrix, encoding="utf-8")
    providers, _ = load_matrix(path)
    spec = providers["fake-b"].model("m1")
    assert spec.wire_name == "m1"
    assert not spec.is_alias


# -- optional research role --------------------------------------------------------

RESEARCH_MATRIX = """\
[providers.fake-a]
base_url = "http://fake-a.local:9000/v1"

[providers.fake-a.models.big-coder]
max_context_tokens = 32768

[providers.fake-a.models.researcher]
max_context_tokens = 65536

[providers.fake-b]
base_url = "http://fake-b.local:9001/v1"

[providers.fake-b.models.small-8b]
max_context_tokens = 8192

[[combo]]
name       = "with-research"
coding     = "fake-a/big-coder"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b"
research   = "fake-a/researcher"

[[combo]]
name       = "without-research"
coding     = "fake-a/big-coder"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b"
"""


@pytest.fixture
def research_matrix_file(tmp_path: Path) -> Path:
    path = tmp_path / "matrix.toml"
    path.write_text(RESEARCH_MATRIX, encoding="utf-8")
    return path


def test_research_role_is_optional(research_matrix_file: Path) -> None:
    """A combo WITHOUT research parses exactly as before (backwards
    compatibility): `research` is None, `roles()` carries only the three
    required roles — drcode's own coding fallback covers research."""
    _, combos = load_matrix(research_matrix_file)
    without = next(c for c in combos if c.name == "without-research")
    assert without.research is None
    assert without.roles() == {role: without.ref(role) for role in ROLES}
    assert "research" not in without.roles()


def test_research_role_parses(research_matrix_file: Path) -> None:
    """`research = "provider/model"`: parsed like any other role, present
    in `roles()` (after the required three), absent from the missing-roles
    check when not given."""
    _, combos = load_matrix(research_matrix_file)
    with_research = next(c for c in combos if c.name == "with-research")
    assert with_research.research == "fake-a/researcher"
    roles = with_research.roles()
    assert roles["research"] == "fake-a/researcher"
    assert list(roles) == ["coding", "tester", "compaction", "research"]


def test_research_ref_validation(research_matrix_file: Path, tmp_path: Path) -> None:
    """A research ref is validated like every other role: unknown provider
    or unknown model is a matrix error."""
    matrix = RESEARCH_MATRIX.replace(
        'research   = "fake-a/researcher"', 'research   = "fake-a/no-such-model"'
    )
    path = tmp_path / "matrix.toml"
    path.write_text(matrix, encoding="utf-8")
    with pytest.raises(MatrixError, match="no model 'no-such-model'"):
        load_matrix(path)

    matrix = RESEARCH_MATRIX.replace(
        'research   = "fake-a/researcher"', 'research   = "no-provider/researcher"'
    )
    path.write_text(matrix, encoding="utf-8")
    with pytest.raises(MatrixError, match="unknown provider 'no-provider'"):
        load_matrix(path)


def test_research_max_context_override_parses(tmp_path: Path) -> None:
    """`research_max_context_tokens = N` rides the existing per-role
    override mechanism."""
    matrix = RESEARCH_MATRIX.replace(
        'research   = "fake-a/researcher"',
        'research   = "fake-a/researcher"\nresearch_max_context_tokens = 4000',
    )
    path = tmp_path / "matrix.toml"
    path.write_text(matrix, encoding="utf-8")
    _, combos = load_matrix(path)
    with_research = next(c for c in combos if c.name == "with-research")
    assert with_research.max_context_override("research") == 4000


def test_research_override_without_role_is_an_error(tmp_path: Path) -> None:
    """An override on an unassigned optional role would silently never
    apply (research falls back to coding and reads coding's resolved
    config) — reject it at parse time instead."""
    matrix = RESEARCH_MATRIX.replace(
        '[[combo]]\nname       = "without-research"',
        '[[combo]]\nname       = "without-research"\nresearch_max_context_tokens = 4000',
    )
    path = tmp_path / "matrix.toml"
    path.write_text(matrix, encoding="utf-8")
    with pytest.raises(MatrixError, match="assigns no 'research' role"):
        load_matrix(path)
