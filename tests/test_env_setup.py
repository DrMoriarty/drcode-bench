"""Tests of bench/env_setup (stage 1 DoD): generation of models.json /
drcode.json / settings.json, environment sanitization, git plumbing and
the pre-flight check — drcode.providers.resolve() must return the expected
model for every role.

A tiny in-repo matrix (tmp_path) plays the role of a fake provider
catalog — no network, no real models: resolve() only reads the generated
files.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from bench.env_setup import (
    EnvSetupError,
    RunPaths,
    prepare_run,
    run_preflight_subprocess,
    subprocess_env,
    verify_resolution,
)
from bench.matrix import Combo, load_matrix

MATRIX = """\
[providers.fake-a]
base_url = "http://fake-a.local:9000/v1"
api_key  = "env:FAKE_A_KEY"

[providers.fake-a.models.big-coder]
max_context_tokens = 32768
max_tokens = 4096

[providers.fake-b]
base_url = "http://fake-b.local:9001/v1"
api_key  = ""

[providers.fake-b.models.small-8b]
max_context_tokens = 8192
max_tokens = 2048

[[combo]]
name       = "combo-1"
coding     = "fake-a/big-coder"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b"

[[combo]]
name       = "single-model"
coding     = "fake-a/big-coder"
tester     = "fake-a/big-coder"
compaction = "fake-a/big-coder"
"""

SEED_MAIN = "def add(a, b):\n    return a + b\n"
SEED_TEST = """\
def test_add():
    assert add(2, 2) == 4
"""


@pytest.fixture
def matrix_file(tmp_path: Path) -> Path:
    path = tmp_path / "matrix.toml"
    path.write_text(MATRIX, encoding="utf-8")
    return path


@pytest.fixture
def scenario_dir(tmp_path: Path) -> Path:
    """A minimal scenario: seed with a couple of files + AGENTS.md."""
    scenario = tmp_path / "scenarios" / "s1_happy"
    seed = scenario / "seed"
    seed.mkdir(parents=True)
    (seed / "main.py").write_text(SEED_MAIN, encoding="utf-8")
    (seed / "test_main.py").write_text(SEED_TEST, encoding="utf-8")
    (scenario / "AGENTS.md").write_text("# agents rules\n", encoding="utf-8")
    return scenario


@pytest.fixture
def combo(matrix_file: Path) -> Combo:
    _providers, combos = load_matrix(matrix_file)
    assert combos, "matrix fixture must define combos"
    return combos[0]


def test_prepare_run_tree(scenario_dir, combo, matrix_file, tmp_path, monkeypatch):
    monkeypatch.setenv("FAKE_A_KEY", "sk-host-secret")
    run_dir = tmp_path / "runs" / "r1"
    paths = prepare_run(scenario_dir, combo, run_dir, matrix_path=matrix_file)

    assert isinstance(paths, RunPaths)
    # workspace: seed copied + AGENTS.md + own .gitignore
    assert (paths.workspace / "main.py").read_text(encoding="utf-8") == SEED_MAIN
    assert (paths.workspace / "test_main.py").is_file()
    assert (paths.workspace / "AGENTS.md").read_text(encoding="utf-8") == "# agents rules\n"
    assert (paths.workspace / ".gitignore").read_text(encoding="utf-8") == ".drcode/\n"

    # config-home/drcode/models.json: providers of the combo only, env:KEY resolved
    catalog = json.loads(paths.models_catalog.read_text(encoding="utf-8"))
    provider_names = sorted(p["name"] for p in catalog["providers"])
    assert provider_names == ["fake-a", "fake-b"]
    fake_a = next(p for p in catalog["providers"] if p["name"] == "fake-a")
    assert fake_a["base_url"] == "http://fake-a.local:9000/v1"
    assert fake_a["api_key"] == "sk-host-secret"
    big_coder = next(m for m in fake_a["models"] if m["id"] == "big-coder")
    assert big_coder["max_context_tokens"] == 32768
    assert catalog["defaults"] == {}

    # drcode.json: flat layer (empty) + per-role models selection
    project = json.loads(paths.project_config.read_text(encoding="utf-8"))
    assert project["models"] == {
        "coding": "fake-a/big-coder",
        "tester": "fake-b/small-8b",
        "compaction": "fake-b/small-8b",
    }

    # settings.json: benchmark hygiene values
    settings = json.loads(paths.settings_file.read_text(encoding="utf-8"))
    assert settings == {
        "task_finalization": "testing",
        "stall_nudge": "never",
        "completed_retention": "never",
    }

    # no remote for plain "testing"
    assert paths.remote is None

    # git: workspace is a repo with a seed commit; .drcode/ is NOT committed
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=paths.workspace, capture_output=True, text=True, check=True
        ).stdout

    assert git("rev-parse", "--is-inside-work-tree").strip() == "true"
    committed = git("ls-files").split()
    assert "main.py" in committed
    assert not any(name.startswith(".drcode") for name in committed)


def test_prepare_run_testing_commit_local_remote(scenario_dir, combo, matrix_file, tmp_path):
    run_dir = tmp_path / "runs" / "r2"
    paths = prepare_run(
        scenario_dir,
        combo,
        run_dir,
        matrix_path=matrix_file,
        task_finalization="testing_commit",
    )
    # Local bare remote inside the run tree — never GitHub.
    assert paths.remote is not None and paths.remote.is_dir()
    assert (paths.remote / "HEAD").is_file()
    assert "github" not in str(paths.remote)
    remotes = subprocess.run(
        ["git", "remote", "-v"], cwd=paths.workspace, capture_output=True, text=True, check=True
    ).stdout
    assert str(paths.remote) in remotes

    settings = json.loads(paths.settings_file.read_text(encoding="utf-8"))
    assert settings["task_finalization"] == "testing_commit"


def test_prepare_run_rejects_bad_finalization(scenario_dir, combo, matrix_file, tmp_path):
    with pytest.raises(EnvSetupError, match="task_finalization"):
        prepare_run(
            scenario_dir,
            combo,
            tmp_path / "r3",
            matrix_path=matrix_file,
            task_finalization="none",
        )


def test_prepare_run_rejects_existing_dir(scenario_dir, combo, matrix_file, tmp_path):
    run_dir = tmp_path / "runs" / "dup"
    run_dir.mkdir(parents=True)
    with pytest.raises(EnvSetupError, match="already exists"):
        prepare_run(scenario_dir, combo, run_dir, matrix_path=matrix_file)


def test_subprocess_env_strips_drcode_and_pins_xdg(tmp_path):
    os.environ["DRCODE_MODEL"] = "leak-model"
    os.environ["DRCODE_BASE_URL"] = "http://leak.local/v1"
    os.environ["DRCODE_SOMETHING_ELSE"] = "1"
    try:
        env = subprocess_env(tmp_path / "config-home", home=tmp_path / "home")
        assert not [k for k in env if k.startswith("DRCODE_")]
        assert env["XDG_CONFIG_HOME"] == str(tmp_path / "config-home")
        assert env["HOME"] == str(tmp_path / "home")
    finally:
        for key in ("DRCODE_MODEL", "DRCODE_BASE_URL", "DRCODE_SOMETHING_ELSE"):
            del os.environ[key]


def test_verify_resolution_returns_expected_models(scenario_dir, combo, matrix_file, tmp_path):
    """Pre-flight (§3 end): resolve() for every role returns the expected
    provider/model — against the generated config files only."""
    run_dir = tmp_path / "runs" / "pf"
    paths = prepare_run(scenario_dir, combo, run_dir, matrix_path=matrix_file)

    resolved = verify_resolution(paths.workspace, paths.config_home, combo, matrix_path=matrix_file)
    assert resolved == {
        "coding": "fake-a/big-coder",
        "tester": "fake-b/small-8b",
        "compaction": "fake-b/small-8b",
    }


def test_verify_resolution_detects_mismatch(scenario_dir, combo, matrix_file, tmp_path):
    run_dir = tmp_path / "runs" / "pf2"
    paths = prepare_run(scenario_dir, combo, run_dir, matrix_path=matrix_file)
    # Sabotage the catalog: remove the provider the tester points at —
    # resolve() must fall through (dangling ref), and the pre-flight must
    # catch it instead of silently running the wrong model.
    catalog_path = paths.models_catalog
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog["providers"] = [p for p in catalog["providers"] if p["name"] != "fake-b"]
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")

    with pytest.raises(EnvSetupError, match="pre-flight failed for role 'tester'"):
        verify_resolution(paths.workspace, paths.config_home, combo, matrix_path=matrix_file)


def test_verify_resolution_env_override_is_not_honored(
    scenario_dir, combo, matrix_file, tmp_path, monkeypatch
):
    """DRCODE_MODEL in the environment must NOT leak into the pre-flight:
    verify_resolution clears DRCODE_* exactly like the run subprocess env
    (otherwise env would win for all roles, §1.1/§13)."""
    monkeypatch.setenv("DRCODE_MODEL", "host-override")
    monkeypatch.setenv("DRCODE_BASE_URL", "http://host-override.local/v1")
    run_dir = tmp_path / "runs" / "pf3"
    paths = prepare_run(scenario_dir, combo, run_dir, matrix_path=matrix_file)
    resolved = verify_resolution(paths.workspace, paths.config_home, combo, matrix_path=matrix_file)
    assert resolved["coding"] == "fake-a/big-coder"


def test_run_preflight_subprocess(scenario_dir, combo, matrix_file, tmp_path):
    """The subprocess form: fresh interpreter + sanitized env reproduces the
    import-time XDG_CONFIG_HOME binding of the real run."""
    run_dir = tmp_path / "runs" / "pf4"
    paths = prepare_run(scenario_dir, combo, run_dir, matrix_path=matrix_file)
    resolved = run_preflight_subprocess(paths, combo, matrix_path=matrix_file)
    assert resolved == {
        "coding": "fake-a/big-coder",
        "tester": "fake-b/small-8b",
        "compaction": "fake-b/small-8b",
    }
    assert sys.prefix  # sanity: tests run inside the bench venv


# -- per-role max_context_tokens overrides (plan §1.2, stage 4) ------------------

OVERRIDE_MATRIX = """\
[providers.fake-a]
base_url = "http://fake-a.local:9000/v1"
api_key  = ""

[providers.fake-a.models.big-coder]
max_context_tokens = 32768
max_tokens = 4096

[providers.fake-b]
base_url = "http://fake-b.local:9001/v1"
api_key  = ""

[providers.fake-b.models.small-8b]
max_context_tokens = 8192
max_tokens = 2048

[[combo]]
name       = "small-coding-ctx"
coding     = "fake-a/big-coder"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b"
coding_max_context_tokens = 3000

[[combo]]
name       = "conflicting-overrides"
coding     = "fake-b/small-8b"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b"
coding_max_context_tokens = 2000
compaction_max_context_tokens = 5000
"""


@pytest.fixture
def override_matrix_file(tmp_path: Path) -> Path:
    path = tmp_path / "matrix.toml"
    path.write_text(OVERRIDE_MATRIX, encoding="utf-8")
    return path


def test_matrix_parses_max_context_overrides(override_matrix_file: Path) -> None:
    _, combos = load_matrix(override_matrix_file)
    small, conflict = combos
    assert small.max_context_override("coding") == 3000
    assert small.max_context_override("tester") is None
    assert conflict.max_context_override("coding") == 2000
    assert conflict.max_context_override("compaction") == 5000


def test_materialize_patches_catalog_entry_in_place(
    override_matrix_file: Path, tmp_path: Path
) -> None:
    """No conflict (distinct models): the override lands on the referenced
    catalog entry — the layer that beats the flat config for the role."""
    from bench.env_setup import materialize_providers

    providers, _ = load_matrix(override_matrix_file)
    small = load_matrix(override_matrix_file)[1][0]
    materialized, refs = materialize_providers(small, providers)
    assert refs["coding"] == ("fake-a", "big-coder")
    assert materialized["fake-a"].model("big-coder").max_context_tokens == 3000
    # Untouched roles keep their values.
    assert materialized["fake-b"].model("small-8b").max_context_tokens == 8192


def test_materialize_resolves_conflict_with_virtual_provider(
    override_matrix_file: Path,
) -> None:
    """Same model referenced by roles needing different contexts: the first
    role in ROLES order keeps the original provider (patched), the others
    get `<name>--ctx<N>` clones with identical base_url."""
    from bench.env_setup import materialize_providers

    providers, combos = load_matrix(override_matrix_file)
    conflict = combos[1]
    materialized, refs = materialize_providers(conflict, providers)
    # The first role in ROLES order (coding, ctx 2000) keeps the original
    # provider, patched.
    assert refs["coding"] == ("fake-b", "small-8b")
    assert materialized["fake-b"].model("small-8b").max_context_tokens == 2000
    clone_name = refs["compaction"][0]
    assert clone_name.startswith("fake-b--ctx")
    clone = materialized[clone_name]
    assert clone.base_url == providers["fake-b"].base_url
    assert clone.model("small-8b").max_context_tokens == 5000
    # The tester (no override → catalog 8192 ≠ kept 2000) gets its own
    # clone with the catalog value.
    tester_clone = materialized[refs["tester"][0]]
    assert tester_clone.model("small-8b").max_context_tokens == 8192


def test_prepare_run_writes_override_into_catalog(
    override_matrix_file: Path, scenario_dir: Path, tmp_path: Path
) -> None:
    _, combos = load_matrix(override_matrix_file)
    small = next(c for c in combos if c.name == "small-coding-ctx")
    paths = prepare_run(
        scenario_dir, small, tmp_path / "runs" / "ovr", matrix_path=override_matrix_file
    )
    catalog = json.loads(paths.models_catalog.read_text(encoding="utf-8"))
    fake_a = next(p for p in catalog["providers"] if p["name"] == "fake-a")
    assert next(m for m in fake_a["models"] if m["id"] == "big-coder")["max_context_tokens"] == 3000
    project = json.loads(paths.project_config.read_text(encoding="utf-8"))
    assert project["models"]["coding"] == "fake-a/big-coder"


def test_verify_resolution_asserts_context_override(
    override_matrix_file: Path, scenario_dir: Path, tmp_path: Path
) -> None:
    """The pre-flight must catch a run where the small context did NOT
    reach the role — the compaction scenarios would silently run with the
    big window otherwise."""
    _, combos = load_matrix(override_matrix_file)
    small = next(c for c in combos if c.name == "small-coding-ctx")
    paths = prepare_run(
        scenario_dir, small, tmp_path / "runs" / "pf", matrix_path=override_matrix_file
    )
    resolved = verify_resolution(
        paths.workspace, paths.config_home, small, matrix_path=override_matrix_file
    )
    assert resolved["coding"] == "fake-a/big-coder"

    # Sabotage: restore the big context in the generated catalog — the
    # pre-flight must fail.
    catalog = json.loads(paths.models_catalog.read_text(encoding="utf-8"))
    for p in catalog["providers"]:
        for m in p["models"]:
            if m["id"] == "big-coder":
                m["max_context_tokens"] = 32768
    paths.models_catalog.write_text(json.dumps(catalog), encoding="utf-8")
    with pytest.raises(EnvSetupError, match="max_context_tokens"):
        verify_resolution(
            paths.workspace, paths.config_home, small, matrix_path=override_matrix_file
        )


# -- alias entries (`model` field, plan §8) ---------------------------------------

ALIAS_MATRIX = """\
[providers.fake-b]
base_url = "http://fake-b.local:9001/v1"
api_key  = "env:FAKE_B_KEY"

[providers.fake-b.models.small-8b]
max_context_tokens = 8192
max_tokens = 2048

[providers.fake-b.models.small-8b-tiny-ctx]
model = "small-8b"
max_context_tokens = 4096
max_tokens = 4096

[[combo]]
name       = "alias-coding"
coding     = "fake-b/small-8b-tiny-ctx"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b"

[[combo]]
name       = "shared-alias"
coding     = "fake-b/small-8b-tiny-ctx"
tester     = "fake-b/small-8b-tiny-ctx"
compaction = "fake-b/small-8b"

[[combo]]
name       = "alias-with-override"
coding     = "fake-b/small-8b-tiny-ctx"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b-tiny-ctx"
compaction_max_context_tokens = 1000
"""


@pytest.fixture
def alias_matrix_file(tmp_path: Path) -> Path:
    path = tmp_path / "matrix.toml"
    path.write_text(ALIAS_MATRIX, encoding="utf-8")
    return path


@pytest.fixture
def alias_combo(alias_matrix_file: Path) -> Combo:
    _providers, combos = load_matrix(alias_matrix_file)
    return next(c for c in combos if c.name == "alias-coding")


def test_materialize_alias_becomes_virtual_provider(alias_matrix_file: Path, monkeypatch) -> None:
    """An alias entry (§8) is materialized into a virtual provider
    `<provider>--<alias>`: same base_url/api_key, a single entry keyed by
    the REAL wire name with the alias's caps; the role ref is rewritten."""
    from bench.env_setup import materialize_providers

    monkeypatch.setenv("FAKE_B_KEY", "sk-b")
    providers, combos = load_matrix(alias_matrix_file)
    combo = next(c for c in combos if c.name == "alias-coding")
    materialized, refs = materialize_providers(combo, providers)

    vname = "fake-b--small-8b-tiny-ctx"
    assert refs["coding"] == (vname, "small-8b")
    # Non-alias roles keep their refs.
    assert refs["tester"] == ("fake-b", "small-8b")

    virtual = materialized[vname]
    assert virtual.base_url == providers["fake-b"].base_url
    assert virtual.api_key == "env:FAKE_B_KEY"  # resolved later, in build_catalog
    assert list(virtual.models) == ["small-8b"]
    entry = virtual.model("small-8b")
    assert entry.max_context_tokens == 4096
    assert entry.max_tokens == 4096

    # The original provider no longer carries the alias entry — the
    # catalog contains only names the provider actually serves.
    assert "small-8b-tiny-ctx" not in materialized["fake-b"].models
    assert "small-8b" in materialized["fake-b"].models


def test_materialize_shared_alias_reuses_one_virtual_provider(
    alias_matrix_file: Path,
) -> None:
    """Roles sharing an alias share one virtual provider — no clones."""
    from bench.env_setup import materialize_providers

    providers, combos = load_matrix(alias_matrix_file)
    combo = next(c for c in combos if c.name == "shared-alias")
    materialized, refs = materialize_providers(combo, providers)
    vname = "fake-b--small-8b-tiny-ctx"
    assert refs["coding"] == refs["tester"] == (vname, "small-8b")
    assert refs["compaction"] == ("fake-b", "small-8b")
    assert sum(1 for name in materialized if name.startswith("fake-b--")) == 1


def test_materialize_alias_with_ctx_override(alias_matrix_file: Path) -> None:
    """A combo ctx override on top of an alias: the virtual provider's
    entry is patched (no conflict) or cloned (conflict) — exactly like the
    §1.2 mechanism on a plain entry."""
    from bench.env_setup import materialize_providers

    providers, combos = load_matrix(alias_matrix_file)
    combo = next(c for c in combos if c.name == "alias-with-override")
    materialized, refs = materialize_providers(combo, providers)
    vname = "fake-b--small-8b-tiny-ctx"
    # coding keeps the alias's catalog ctx (4096) on the virtual provider…
    assert refs["coding"] == (vname, "small-8b")
    assert materialized[vname].model("small-8b").max_context_tokens == 4096
    # …compaction (override 1000) gets a ctx-clone of the virtual provider.
    clone_name = refs["compaction"][0]
    assert clone_name.startswith(vname + "--ctx")
    assert materialized[clone_name].model("small-8b").max_context_tokens == 1000
    assert materialized[clone_name].base_url == providers["fake-b"].base_url


def test_prepare_run_catalog_carries_only_wire_names(
    alias_matrix_file: Path, scenario_dir: Path, tmp_path: Path, monkeypatch
) -> None:
    """Generated models.json / drcode.json: only real wire names — the
    provider never sees an alias in an API request."""
    monkeypatch.setenv("FAKE_B_KEY", "sk-b")
    _providers, combos = load_matrix(alias_matrix_file)
    combo = next(c for c in combos if c.name == "alias-coding")
    paths = prepare_run(
        scenario_dir, combo, tmp_path / "runs" / "al", matrix_path=alias_matrix_file
    )

    catalog = json.loads(paths.models_catalog.read_text(encoding="utf-8"))
    names = sorted(p["name"] for p in catalog["providers"])
    assert names == ["fake-b", "fake-b--small-8b-tiny-ctx"]
    virtual = next(p for p in catalog["providers"] if p["name"].startswith("fake-b--"))
    assert [m["id"] for m in virtual["models"]] == ["small-8b"]
    assert virtual["models"][0]["max_context_tokens"] == 4096
    assert virtual["api_key"] == "sk-b"

    project = json.loads(paths.project_config.read_text(encoding="utf-8"))
    assert project["models"]["coding"] == "fake-b--small-8b-tiny-ctx/small-8b"
    assert project["models"]["tester"] == "fake-b/small-8b"


def test_verify_resolution_with_alias(
    alias_matrix_file: Path, scenario_dir: Path, tmp_path: Path, monkeypatch
) -> None:
    """Pre-flight resolves the rewritten ref and reports the real wire
    name — what recorder/model_log will show."""
    monkeypatch.setenv("FAKE_B_KEY", "sk-b")
    _providers, combos = load_matrix(alias_matrix_file)
    combo = next(c for c in combos if c.name == "alias-coding")
    paths = prepare_run(
        scenario_dir, combo, tmp_path / "runs" / "pfal", matrix_path=alias_matrix_file
    )
    resolved = verify_resolution(
        paths.workspace, paths.config_home, combo, matrix_path=alias_matrix_file
    )
    assert resolved == {
        "coding": "fake-b--small-8b-tiny-ctx/small-8b",
        "tester": "fake-b/small-8b",
        "compaction": "fake-b/small-8b",
    }
