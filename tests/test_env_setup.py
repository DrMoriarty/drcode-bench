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
    providers, combos = load_matrix(matrix_file)
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
            scenario_dir, combo, tmp_path / "r3", matrix_path=matrix_file,
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


def test_verify_resolution_returns_expected_models(
    scenario_dir, combo, matrix_file, tmp_path
):
    """Pre-flight (§3 end): resolve() for every role returns the expected
    provider/model — against the generated config files only."""
    run_dir = tmp_path / "runs" / "pf"
    paths = prepare_run(scenario_dir, combo, run_dir, matrix_path=matrix_file)

    resolved = verify_resolution(
        paths.workspace, paths.config_home, combo, matrix_path=matrix_file
    )
    assert resolved == {
        "coding": "fake-a/big-coder",
        "tester": "fake-b/small-8b",
        "compaction": "fake-b/small-8b",
    }


def test_verify_resolution_detects_mismatch(
    scenario_dir, combo, matrix_file, tmp_path
):
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
        verify_resolution(
            paths.workspace, paths.config_home, combo, matrix_path=matrix_file
        )


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
    resolved = verify_resolution(
        paths.workspace, paths.config_home, combo, matrix_path=matrix_file
    )
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
