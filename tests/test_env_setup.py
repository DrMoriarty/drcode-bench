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
    check_settings_roundtrip,
    prepare_run,
    project_settings,
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

    # settings.json: the FULL pin contract (`project_settings`, "testing"
    # shape — the tester verifies without committing, research keeps
    # git_commit_docs). Guarded by exact equality: dropping a pin here
    # must fail the test, not silently fall back to a drcode default.
    settings = json.loads(paths.settings_file.read_text(encoding="utf-8"))
    assert settings == {
        "task_finalization": "testing",
        "verification": "tester",
        "git_policy": {"tester": "off", "research": "push"},
        "max_dev_rounds": 3,
        "stall_nudge": "never",
        "completed_retention": "never",
        "task_isolation": "off",
        "parallel_tasks": 1,
        "worktree_removal": "on_delete",
        "github_enabled": False,
        "keep_awake": False,
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
    # testing_commit shape: the tester commits and pushes (to the LOCAL
    # bare remote only), research keeps git_commit_docs.
    assert settings["verification"] == "tester"
    assert settings["git_policy"] == {"tester": "push", "research": "push"}


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


# -- settings.json pin contract (full ProjectSettings coverage) -------------------


def test_settings_pins_cover_every_project_settings_field() -> None:
    """Audit guard: EVERY field of drcode's ProjectSettings is either
    pinned in `project_settings()` or on the deliberate UI-only exemption
    list (preferences that cannot affect a headless run). A new or
    previously unpinned behavioral field in drcode must surface HERE —
    forcing an explicit pin-or-exempt decision — never silently fall back
    to a drcode default."""
    from drcode.settings import ProjectSettings

    pinned: set[str] = set()
    for finalization in ("testing", "testing_commit"):
        pinned |= set(project_settings(finalization))
    exempt = {
        # UI-only preferences, no effect on a headless run.
        "esc_abort",
        "isolation_start_branch",
        "github_token",
        "github_repo",
        "github_sync_interval",
        "notifications_enabled",
        "ntfy_topic",
        "voice_api_url",
        "voice_api_key",
        "voice_asr_model",
        "voice_tts_model",
        "voice_tts_voice",
        "voice_tts_completed",
        "voice_tts_tester_failed",
        "voice_tts_queue_empty",
        "voice_language",
    }
    fields = set(ProjectSettings.model_fields)
    unaudited = fields - pinned - exempt
    assert not unaudited, (
        f"unaudited ProjectSettings fields: {sorted(unaudited)} — pin them "
        "in bench.env_setup.project_settings or exempt them as UI-only here"
    )


def test_settings_roundtrip_and_loud_failure(scenario_dir, combo, matrix_file, tmp_path):
    """The generated pins must survive drcode's own ProjectSettingsStore —
    whose load() silently falls back to the ALL-DEFAULTS ProjectSettings
    on an unknown key or a ValidationError. A key renamed/migrated in
    drcode must therefore fail the pre-flight LOUDLY, never silently
    un-pin the run's configuration."""
    run_dir = tmp_path / "runs" / "rt"
    paths = prepare_run(scenario_dir, combo, run_dir, matrix_path=matrix_file)

    # Happy path: every pin round-trips (also part of the pre-flight).
    check_settings_roundtrip(paths.workspace)
    verify_resolution(paths.workspace, paths.config_home, combo, matrix_path=matrix_file)

    settings_path = paths.settings_file
    raw = json.loads(settings_path.read_text(encoding="utf-8"))

    # A key drcode no longer knows (e.g. renamed upstream): the store
    # ignores it and uses the default — the round-trip check must catch it.
    renamed = dict(raw)
    renamed["stall_nudge_renamed"] = renamed.pop("stall_nudge")
    settings_path.write_text(json.dumps(renamed), encoding="utf-8")
    with pytest.raises(EnvSetupError, match="stall_nudge"):
        verify_resolution(paths.workspace, paths.config_home, combo, matrix_path=matrix_file)

    # A value whose shape drcode migrated (ValidationError → all-defaults
    # fallback): the loaded value no longer equals the pin — loud failure.
    drifted = dict(raw)
    drifted["git_policy"] = {"tester": "banana", "research": "push"}
    settings_path.write_text(json.dumps(drifted), encoding="utf-8")
    with pytest.raises(EnvSetupError, match="git_policy"):
        verify_resolution(paths.workspace, paths.config_home, combo, matrix_path=matrix_file)


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


# -- optional research role --------------------------------------------------------

RESEARCH_MATRIX = """\
[providers.fake-a]
base_url = "http://fake-a.local:9000/v1"
api_key  = ""

[providers.fake-a.models.big-coder]
max_context_tokens = 32768

[providers.fake-a.models.researcher]
max_context_tokens = 65536

[providers.fake-b]
base_url = "http://fake-b.local:9001/v1"
api_key  = ""

[providers.fake-b.models.small-8b]
max_context_tokens = 8192

[[combo]]
name       = "with-research"
coding     = "fake-a/big-coder"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b"
research   = "fake-a/researcher"
research_max_context_tokens = 4000

[[combo]]
name       = "without-research"
coding     = "fake-a/big-coder"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b"

[[combo]]
name       = "research-conflict"
coding     = "fake-a/big-coder"
tester     = "fake-b/small-8b"
compaction = "fake-b/small-8b"
research   = "fake-a/big-coder"
research_max_context_tokens = 2048
"""


@pytest.fixture
def research_matrix_file(tmp_path: Path) -> Path:
    path = tmp_path / "matrix.toml"
    path.write_text(RESEARCH_MATRIX, encoding="utf-8")
    return path


def _research_combo(matrix_file: Path, name: str) -> Combo:
    _, combos = load_matrix(matrix_file)
    return next(c for c in combos if c.name == name)


def test_prepare_run_without_research_writes_no_slot(
    scenario_dir: Path, research_matrix_file: Path, tmp_path: Path
) -> None:
    """Backwards compatibility: a combo without research generates a
    drcode.json with NO "research" key — drcode's own resolve_effective
    falls back to coding, the generated files are byte-identical to the
    pre-research format."""
    combo = _research_combo(research_matrix_file, "without-research")
    paths = prepare_run(
        scenario_dir, combo, tmp_path / "runs" / "r0", matrix_path=research_matrix_file
    )
    project = json.loads(paths.project_config.read_text(encoding="utf-8"))
    assert project["models"] == {
        "coding": "fake-a/big-coder",
        "tester": "fake-b/small-8b",
        "compaction": "fake-b/small-8b",
    }
    assert "research" not in project["models"]


def test_prepare_run_writes_research_slot(
    scenario_dir: Path, research_matrix_file: Path, tmp_path: Path
) -> None:
    combo = _research_combo(research_matrix_file, "with-research")
    paths = prepare_run(
        scenario_dir, combo, tmp_path / "runs" / "r1", matrix_path=research_matrix_file
    )
    project = json.loads(paths.project_config.read_text(encoding="utf-8"))
    assert project["models"]["research"] == "fake-a/researcher"


def test_verify_resolution_covers_assigned_research(
    scenario_dir: Path, research_matrix_file: Path, tmp_path: Path
) -> None:
    """Pre-flight: an assigned research role resolves into ITS ref (and its
    combo override), never into the coding fallback; an unassigned one is
    simply absent from the resolved map."""
    combo = _research_combo(research_matrix_file, "with-research")
    paths = prepare_run(
        scenario_dir, combo, tmp_path / "runs" / "pf1", matrix_path=research_matrix_file
    )
    resolved = verify_resolution(
        paths.workspace, paths.config_home, combo, matrix_path=research_matrix_file
    )
    assert resolved == {
        "coding": "fake-a/big-coder",
        "tester": "fake-b/small-8b",
        "compaction": "fake-b/small-8b",
        "research": "fake-a/researcher",
    }

    combo0 = _research_combo(research_matrix_file, "without-research")
    paths0 = prepare_run(
        scenario_dir, combo0, tmp_path / "runs" / "pf0", matrix_path=research_matrix_file
    )
    resolved0 = verify_resolution(
        paths0.workspace, paths0.config_home, combo0, matrix_path=research_matrix_file
    )
    assert "research" not in resolved0


def test_verify_resolution_catches_lost_research_slot(
    scenario_dir: Path, research_matrix_file: Path, tmp_path: Path
) -> None:
    """The research role resolving into the CODING model (the fallback)
    while the combo assigns research = a pre-flight failure with a hint:
    the generated drcode.json must carry the "research" key."""
    combo = _research_combo(research_matrix_file, "with-research")
    paths = prepare_run(
        scenario_dir, combo, tmp_path / "runs" / "pf2", matrix_path=research_matrix_file
    )
    # Sabotage: drop the research slot from the generated drcode.json —
    # resolve() then returns "not set" and resolve_effective (inside the
    # app) would silently run research tasks on the coding model.
    project = json.loads(paths.project_config.read_text(encoding="utf-8"))
    del project["models"]["research"]
    paths.project_config.write_text(json.dumps(project), encoding="utf-8")

    with pytest.raises(EnvSetupError, match=r"role 'research'.*fall back to coding"):
        verify_resolution(
            paths.workspace, paths.config_home, combo, matrix_path=research_matrix_file
        )


def test_research_conflict_goes_to_ctx_clone(
    scenario_dir: Path, research_matrix_file: Path, tmp_path: Path
) -> None:
    """coding and research reference the SAME provider model with different
    research_max_context_tokens: the research role gets a
    `<provider>--ctx<N>` clone (its own small context), coding keeps the
    original provider patched to its own override — the §1.2 conflict
    mechanism treats research like any other role."""
    from bench.env_setup import materialize_providers

    combo = _research_combo(research_matrix_file, "research-conflict")
    providers, _ = load_matrix(research_matrix_file)
    materialized, refs = materialize_providers(combo, providers)
    # coding (first in role order) keeps the original provider; research
    # (last) is re-pointed at the ctx clone.
    assert refs["coding"] == ("fake-a", "big-coder")
    clone_name = refs["research"][0]
    assert clone_name.startswith("fake-a--ctx")
    clone = materialized[clone_name]
    assert clone.base_url == providers["fake-a"].base_url
    assert clone.model("big-coder").max_context_tokens == 2048
    assert materialized["fake-a"].model("big-coder").max_context_tokens == 32768

    # End-to-end through the generated files + the real drcode resolution.
    paths = prepare_run(
        scenario_dir, combo, tmp_path / "runs" / "pf3", matrix_path=research_matrix_file
    )
    project = json.loads(paths.project_config.read_text(encoding="utf-8"))
    assert project["models"]["coding"] == "fake-a/big-coder"
    assert project["models"]["research"] == f"{clone_name}/big-coder"
    resolved = verify_resolution(
        paths.workspace, paths.config_home, combo, matrix_path=research_matrix_file
    )
    assert resolved["research"] == f"{clone_name}/big-coder"
    assert resolved["coding"] == "fake-a/big-coder"


def test_run_preflight_subprocess_roundtrips_research(
    scenario_dir: Path, research_matrix_file: Path, tmp_path: Path
) -> None:
    """The subprocess pre-flight serializes the optional research role and
    reconstructs the Combo on the other side of the pipe."""
    combo = _research_combo(research_matrix_file, "with-research")
    paths = prepare_run(
        scenario_dir, combo, tmp_path / "runs" / "pf4", matrix_path=research_matrix_file
    )
    resolved = run_preflight_subprocess(paths, combo, matrix_path=research_matrix_file)
    assert resolved["research"] == "fake-a/researcher"
    assert resolved["coding"] == "fake-a/big-coder"


# -- scenario `[context]` caps (plan §1.2): scenario > combo > catalog -----------

CONTEXT_SCENARIO_TOML = """\
id = "ctx_scenario"
timeout = 1

[context]
coding = 1500

[[briefs]]
title = "t"
kind = "feature"
text = "do nothing"
"""


@pytest.fixture
def context_scenario_dir(tmp_path: Path) -> Path:
    """A minimal scenario whose scenario.toml carries a [context] section."""
    scenario = tmp_path / "scenarios" / "ctx_scenario"
    seed = scenario / "seed"
    seed.mkdir(parents=True)
    (seed / "main.py").write_text(SEED_MAIN, encoding="utf-8")
    (scenario / "scenario.toml").write_text(CONTEXT_SCENARIO_TOML, encoding="utf-8")
    return scenario


def _write_scenario_toml(scenario_dir: Path, body: str) -> None:
    (scenario_dir / "scenario.toml").write_text(body, encoding="utf-8")


@pytest.mark.parametrize(
    ("body", "match"),
    [
        ("[context]\nwat = 3000\n", "unknown role"),
        ("[context]\ncoding = 0\n", "must be > 0"),
        ("[context]\ncoding = -5\n", "must be > 0"),
        ("[context]\ncoding = '3000'\n", "must be an integer"),
        ("[context]\ncoding = true\n", "must be an integer"),
        ("[context]\ncoding = 3.5\n", "must be an integer"),
    ],
)
def test_scenario_context_rejects_bad_values(scenario_dir: Path, body: str, match: str) -> None:
    """A typo'd [context] fails the scenario load loudly (the
    KNOWN_SETTLE_KEYS principle), never a silent no-op."""
    from bench.scenario import ScenarioError, load_scenario

    base = (
        'id = "x"\n'
        "timeout = 1\n"
        "\n[[briefs]]\n"
        'title = "t"\n'
        'kind = "feature"\n'
        'text = "do nothing"\n'
        "\n"
    )
    _write_scenario_toml(scenario_dir, base + body)
    with pytest.raises(ScenarioError, match=match):
        load_scenario(scenario_dir)


def test_scenario_context_parses_overrides(scenario_dir: Path) -> None:
    from bench.scenario import load_scenario

    _write_scenario_toml(
        scenario_dir,
        'id = "x"\ntimeout = 1\n\n[context]\ncoding = 3000\ntester = 4000\n'
        '\n[[briefs]]\ntitle = "t"\nkind = "feature"\ntext = "do nothing"\n',
    )
    sc = load_scenario(scenario_dir)
    assert sc.max_context_overrides == (("coding", 3000), ("tester", 4000))
    assert sc.max_context_override("coding") == 3000
    assert sc.max_context_override("compaction") is None


def test_effective_max_context_priority_scenario_beats_combo(
    override_matrix_file: Path,
) -> None:
    """Priority (§1.2): scenario `[context]` → combo override → catalog."""
    from bench.matrix import effective_max_context, max_context_source

    providers, combos = load_matrix(override_matrix_file)
    small = next(c for c in combos if c.name == "small-coding-ctx")
    # small-coding-ctx: coding_max_context_tokens = 3000, catalog 32768.
    assert effective_max_context(small, providers, "coding") == 3000
    assert max_context_source(small, "coding") == "combo"
    # The scenario cap wins over BOTH.
    assert (
        effective_max_context(small, providers, "coding", scenario_overrides=(("coding", 1500),))
        == 1500
    )
    assert max_context_source(small, "coding", (("coding", 1500),)) == "scenario"
    # An uncapped role falls through to the catalog value.
    assert effective_max_context(small, providers, "tester") == 8192
    assert max_context_source(small, "tester") == "catalog"


def test_prepare_run_writes_scenario_override_into_catalog(
    override_matrix_file: Path, context_scenario_dir: Path, tmp_path: Path
) -> None:
    """The scenario `[context]` cap travels into the generated catalog entry
    (the layer providers.resolve reads the role's context from)."""
    from bench.scenario import load_scenario

    _, combos = load_matrix(override_matrix_file)
    small = next(c for c in combos if c.name == "small-coding-ctx")
    scenario = load_scenario(context_scenario_dir)
    paths = prepare_run(
        context_scenario_dir,
        small,
        tmp_path / "runs" / "sctx",
        matrix_path=override_matrix_file,
        scenario_overrides=scenario.max_context_overrides,
    )
    catalog = json.loads(paths.models_catalog.read_text(encoding="utf-8"))
    fake_a = next(p for p in catalog["providers"] if p["name"] == "fake-a")
    assert next(m for m in fake_a["models"] if m["id"] == "big-coder")["max_context_tokens"] == 1500


def test_verify_resolution_preflight_roundtrips_scenario_overrides(
    override_matrix_file: Path, context_scenario_dir: Path, tmp_path: Path
) -> None:
    """The pre-flight (in-process AND subprocess forms) validates the
    scenario cap end-to-end: resolve() must return the scenario's small
    context, and the subprocess spec carries the scenario section."""
    from bench.scenario import load_scenario

    _, combos = load_matrix(override_matrix_file)
    small = next(c for c in combos if c.name == "small-coding-ctx")
    scenario = load_scenario(context_scenario_dir)
    paths = prepare_run(
        context_scenario_dir,
        small,
        tmp_path / "runs" / "pfctx",
        matrix_path=override_matrix_file,
        scenario_overrides=scenario.max_context_overrides,
    )
    resolved = verify_resolution(
        paths.workspace,
        paths.config_home,
        small,
        matrix_path=override_matrix_file,
        scenario_overrides=scenario.max_context_overrides,
    )
    assert resolved["coding"] == "fake-a/big-coder"
    via_subprocess = run_preflight_subprocess(
        paths,
        small,
        matrix_path=override_matrix_file,
        scenario_overrides=scenario.max_context_overrides,
    )
    assert via_subprocess == resolved


def test_materialize_scenario_override_conflict_gets_ctx_clone(
    override_matrix_file: Path, tmp_path: Path
) -> None:
    """A scenario cap conflicting with another role's value on the SAME
    model gets the `<provider>--ctx<N>` clone — the §1.2 conflict machinery
    is reused as-is, only the cap source changes."""
    from bench.env_setup import materialize_providers

    providers, combos = load_matrix(override_matrix_file)
    conflict = next(c for c in combos if c.name == "conflicting-overrides")
    # Combo: coding=2000, compaction=5000 (same fake-b/small-8b); the
    # scenario re-caps coding at 1500 — compaction keeps its 5000 clone.
    materialized, refs = materialize_providers(
        conflict, providers, scenario_overrides=(("coding", 1500),)
    )
    assert refs["coding"] == ("fake-b", "small-8b")
    assert materialized["fake-b"].model("small-8b").max_context_tokens == 1500
    clone_name = refs["compaction"][0]
    assert clone_name.startswith("fake-b--ctx")
    assert materialized[clone_name].model("small-8b").max_context_tokens == 5000


def test_check_research_override_assigned(tmp_path: Path) -> None:
    """`[context] research` on a combo without a research role would
    silently never apply — a loud MatrixError naming both sides."""
    from bench.matrix import MatrixError, check_research_override_assigned

    matrix = tmp_path / "matrix.toml"
    matrix.write_text(RESEARCH_MATRIX, encoding="utf-8")
    _providers, combos = load_matrix(matrix)
    without = next(c for c in combos if c.name == "without-research")
    with_research = next(c for c in combos if c.name == "with-research")
    check_research_override_assigned(with_research, (("research", 2048),), "scenario 'x'")
    with pytest.raises(MatrixError, match="assigns no 'research' role"):
        check_research_override_assigned(without, (("research", 2048),), "scenario 'x'")
