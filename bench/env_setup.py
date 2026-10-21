"""Preparation of the per-run environment (plan drcode-bench.md, §3).

One run = one isolated tmp tree:

    <run_dir>/
    ├── workspace/            # project root for the agents (seed copy + .drcode/ + .git)
    │   ├── <seed files>
    │   ├── AGENTS.md         # optional
    │   ├── .gitignore        # ".drcode/" (matches drcode's own behavior)
    │   ├── .git/             # init + first commit
    │   └── .drcode/
    │       ├── drcode.json   # flat layer + per-role "models" selection
    │       └── settings.json # task_finalization / stall_nudge / completed_retention
    ├── config-home/          # becomes XDG_CONFIG_HOME of the run subprocess
    │   └── drcode/
    │       └── models.json   # provider catalog of this combo
    └── remote.git/           # local bare remote (only for testing_commit)

Everything is generated from the model matrix (`bench.matrix`); drcode
sources are never modified. Pushes go ONLY to the local bare remote —
never to GitHub; the run must not depend on the external network.

Subprocess environment hygiene: `subprocess_env()` sets
`XDG_CONFIG_HOME=<config-home>` and strips EVERY `DRCODE_*` variable —
`DRCODE_MODEL`/`DRCODE_BASE_URL` would override the per-role selection
for ALL roles (providers.resolve precedence, plan §1.1/§13).

Pre-flight check (§3 end): `verify_resolution()` loads the generated
config exactly like drcode would and asserts that
`drcode.providers.resolve(config, role)` returns the expected model for
each role — before any application code is started.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from .matrix import Combo, ProviderSpec, ROLES, _resolve_api_key, load_matrix

# `task_finalization` values allowed for a benchmark run. "none" is not
# useful here (the benchmark exists to exercise the tester).
FINALIZATION_CHOICES = ("testing", "testing_commit")

PROJECT_STATE_DIRNAME = ".drcode"  # keep in sync with drcode.config


class EnvSetupError(RuntimeError):
    """Run environment could not be prepared or verified."""


@dataclass(frozen=True)
class RunPaths:
    """Layout of one run's tmp tree (§3)."""

    run_dir: Path
    workspace: Path
    config_home: Path
    models_catalog: Path  # config-home/drcode/models.json
    project_config: Path  # workspace/.drcode/drcode.json
    settings_file: Path  # workspace/.drcode/settings.json
    remote: Path | None  # local bare remote (testing_commit only)

    def subprocess_env(self, *, home: Path | None = None) -> dict[str, str]:
        """Sanitized env for the run subprocess (see `subprocess_env`)."""
        return subprocess_env(self.config_home, home=home)


# -- subprocess environment hygiene (§1.1, §13) --------------------------------


def subprocess_env(config_home: Path, *, home: Path | None = None) -> dict[str, str]:
    """Environment for the run subprocess.

    - `XDG_CONFIG_HOME` points at the run's own config-home (the user-level
      drcode config dir is bound at `drcode.config` import time, so each run
      must be a fresh process with its own XDG_CONFIG_HOME);
    - every `DRCODE_*` variable is stripped: `DRCODE_MODEL`/`DRCODE_BASE_URL`
      win globally for all roles and would silently override the per-role
      selection written into `.drcode/drcode.json`;
    - `HOME` is redirected when requested (full isolation from the host).
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("DRCODE_")}
    env["XDG_CONFIG_HOME"] = str(config_home)
    if home is not None:
        env["HOME"] = str(home)
    return env


# -- config file generation -----------------------------------------------------


def _providers_for_combo(
    combo: Combo,
    providers: dict[str, ProviderSpec] | None,
    matrix_path: Path | None,
) -> dict[str, ProviderSpec]:
    """Providers of the combo: explicit dict, else loaded from matrix.toml.

    Only providers actually referenced by the combo are materialized into
    models.json — the run sees exactly the endpoints of its combination.
    """
    if providers is None:
        if matrix_path is None:
            matrix_path = Path(__file__).resolve().parents[1] / "matrix.toml"
        providers, _ = load_matrix(matrix_path)
    used: set[str] = set()
    for role in ROLES:
        provider_name = combo.ref(role).partition("/")[0]
        if provider_name not in providers:
            raise EnvSetupError(
                f"combo '{combo.name}' role '{role}': unknown provider '{provider_name}'"
            )
        used.add(provider_name)
    return {name: providers[name] for name in sorted(used)}


def build_catalog(
    providers: dict[str, ProviderSpec],
    combo: Combo,
) -> dict[str, object]:
    """models.json payload for the combo (format: drcode `UserModelsConfig`,
    see `models.json.example` of drcode). api_key = "env:NAME" is resolved
    from the host environment here."""
    out_providers = []
    for name in sorted(providers):
        spec = providers[name]
        out_providers.append(
            {
                "name": name,
                "base_url": spec.base_url,
                "api_key": _resolve_api_key(spec.api_key),
                "health_check_url": "",
                "models": [
                    {
                        "id": model.id,
                        "max_context_tokens": model.max_context_tokens,
                        "max_tokens": model.max_tokens,
                        "compaction_threshold": model.compaction_threshold,
                        "context_reported": False,
                    }
                    for model in spec.models.values()
                ],
            }
        )
    # Per-role fallbacks are pinned at the project level (drcode.json
    # "models" key); user-level defaults stay empty so the project layer
    # is the single visible source of the selection.
    return {"providers": out_providers, "defaults": {}}


def _write_json(path: Path, payload: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return path


# -- git plumbing (workspace repo + local bare remote) --------------------------


def _git(*args: str, cwd: Path | None = None) -> None:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise EnvSetupError(f"git {' '.join(args)} failed: {result.stderr.strip()}")


def _git_init_bare(remote: Path) -> None:
    """`git init --bare <remote>` (parent created on demand)."""
    remote.parent.mkdir(parents=True, exist_ok=True)
    _git("init", "--bare", "--initial-branch=main", str(remote))


def _git_init_workspace(workspace: Path, remote: Path | None) -> None:
    """git init + first commit; bare remote added as `origin` when given."""
    # Identity is forced locally: the run must not depend on the host's
    # global git config (or its absence in CI).
    _git("init", "--initial-branch=main", cwd=workspace)
    _git("config", "user.email", "bench@drcode.local", cwd=workspace)
    _git("config", "user.name", "drcode-bench", cwd=workspace)
    _git("config", "commit.gpgsign", "false", cwd=workspace)
    _git("add", "-A", cwd=workspace)
    _git("commit", "-m", "seed", cwd=workspace)
    if remote is not None:
        _git("remote", "add", "origin", str(remote), cwd=workspace)


# -- the tree -------------------------------------------------------------------


def prepare_run(
    scenario_dir: Path,
    combo: Combo,
    run_dir: Path,
    *,
    providers: dict[str, ProviderSpec] | None = None,
    matrix_path: Path | None = None,
    task_finalization: str = "testing",
    flat_config: dict[str, object] | None = None,
    agents_md: Path | None = None,
    exists_ok: bool = False,
) -> RunPaths:
    """Create the full run tree for one (scenario, combo) pair and return
    its layout (§3).

    - copies `<scenario_dir>/seed/` into `workspace/` (+ `AGENTS.md` when
      the scenario provides one);
    - generates `config-home/drcode/models.json` from the combo's providers;
    - writes `workspace/.drcode/drcode.json` (optional flat layer + the
      per-role `models` selection) and `workspace/.drcode/settings.json`
      (`stall_nudge="never"`, `completed_retention="never"`,
      `task_finalization="testing"` — or `"testing_commit"` with a LOCAL
      bare remote inside the run tree, never GitHub);
    - git-init's the workspace with a seed commit.

    `task_finalization` must be `"testing"` or `"testing_commit"`.
    """
    scenario_dir = Path(scenario_dir)
    run_dir = Path(run_dir)
    if task_finalization not in FINALIZATION_CHOICES:
        raise EnvSetupError(
            f"task_finalization must be one of {FINALIZATION_CHOICES}, "
            f"got {task_finalization!r}"
        )
    if run_dir.exists() and not exists_ok:
        raise EnvSetupError(f"run dir already exists: {run_dir}")
    seed = scenario_dir / "seed"
    if not seed.is_dir():
        raise EnvSetupError(f"scenario has no seed/ directory: {scenario_dir}")

    workspace = run_dir / "workspace"
    config_home = run_dir / "config-home"
    user_drcode_dir = config_home / "drcode"

    # 1. workspace: seed copy (+ optional project AGENTS.md for the agents).
    shutil.copytree(seed, workspace)
    agents_md = agents_md or (scenario_dir / "AGENTS.md")
    if agents_md.is_file():
        shutil.copyfile(agents_md, workspace / "AGENTS.md")
    # `.drcode/` holds run-local task storage — never part of the seed commit.
    (workspace / ".gitignore").write_text(".drcode/\n", encoding="utf-8")

    # 2. user-level catalog of this combo.
    used_providers = _providers_for_combo(combo, providers, matrix_path)
    models_catalog = _write_json(
        user_drcode_dir / "models.json", build_catalog(used_providers, combo)
    )

    # 3. project-level per-role selection (+ optional flat layer).
    flat = dict(flat_config) if flat_config else {}
    project_config = _write_json(
        workspace / PROJECT_STATE_DIRNAME / "drcode.json",
        {**flat, "models": combo.roles()},
    )

    # 4. project settings: no watchdog, no retention cleanup, testing
    #    finalization — pushes go to a LOCAL bare remote inside the run
    #    tree only, never to GitHub (§13).
    remote: Path | None = None
    if task_finalization == "testing_commit":
        remote = run_dir / "remote.git"
        _git("init", "--bare", "--initial-branch=main", cwd=run_dir.__class__(".") if False else None) if False else None
    settings_file = _write_json(
        workspace / PROJECT_STATE_DIRNAME / "settings.json",
        {
            "task_finalization": task_finalization,
            "stall_nudge": "never",
            "completed_retention": "never",
        },
    )

    # 5. git: seed commit; bare remote (created before the workspace repo
    #    references it) for testing_commit.
    if task_finalization == "testing_commit":
        _git_init_bare(remote)
        _git_init_workspace(workspace, remote)
    else:
        _git_init_workspace(workspace, None)

    return RunPaths(
        run_dir=run_dir,
        workspace=workspace,
        config_home=config_home,
        models_catalog=models_catalog,
        project_config=project_config,
        settings_file=settings_file,
        remote=remote,
    )


# -- pre-flight check (§3 end) ---------------------------------------------------


@contextmanager
def _isolated_user_config(config_home: Path) -> Iterator[None]:
    """Point `drcode.config` at the run's config-home in-process.

    `drcode.config` binds `_USER_CONFIG_DIR` at import time; tests and the
    pre-flight redirect it here instead of spawning a process. All
    `DRCODE_*` variables are temporarily cleared for the same reason as in
    `subprocess_env` — they would override the per-role selection.
    """
    import drcode.config as dconfig

    saved_dir, saved_file = dconfig._USER_CONFIG_DIR, dconfig.USER_CONFIG_FILE
    saved_env = {
        k: v for k, v in os.environ.items() if k.startswith("DRCODE_")
    }
    for k in saved_env:
        del os.environ[k]
    dconfig._USER_CONFIG_DIR = Path(config_home) / "drcode"
    dconfig.USER_CONFIG_FILE = dconfig._USER_CONFIG_DIR / "drcode.json"
    try:
        yield
    finally:
        dconfig._USER_CONFIG_DIR, dconfig.USER_CONFIG_FILE = saved_dir, saved_file
        os.environ.update(saved_env)


def verify_resolution(
    workspace: Path,
    config_home: Path,
    combo: Combo,
    providers: dict[str, ProviderSpec] | None = None,
    matrix_path: Path | None = None,
) -> dict[str, str]:
    """Pre-flight: resolve each role against the generated config and assert
    the expected model. Returns role → "provider/model" as resolved.

    Uses `drcode.providers.resolve()` — the same precedence (env >
    project models > catalog defaults > flat config) the run will see.
    """
    if providers is None:
        if matrix_path is None:
            matrix_path = Path(__file__).resolve().parents[1] / "matrix.toml"
        providers, _ = load_matrix(matrix_path)

    import drcode.providers as dproviders
    from drcode.config import Config

    with _isolated_user_config(config_home):
        config = Config(project_root=Path(workspace).resolve())
        resolved: dict[str, str] = {}
        for role in ROLES:
            agent_role = dproviders.AgentRole(role)
            eff = dproviders.resolve(config, agent_role)
            ref = combo.ref(role)
            provider_name, model_id = ref.partition("/")[0], ref.partition("/")[2]
            spec = providers[provider_name].model(model_id)
            expected_base_url = providers[provider_name].base_url
            if eff.model != model_id or eff.base_url != expected_base_url:
                raise EnvSetupError(
                    f"pre-flight failed for role '{role}': expected "
                    f"{model_id}@{expected_base_url}, resolved "
                    f"{eff.model}@{eff.base_url}"
                )
            resolved[role] = f"{provider_name}/{eff.model}"
    return resolved


def run_preflight_subprocess(
    paths: RunPaths,
    combo: Combo,
    providers: dict[str, ProviderSpec] | None = None,
    matrix_path: Path | None = None,
) -> dict[str, str]:
    """Pre-flight in a FRESH interpreter with the sanitized env.

    This is the form the real run uses: the run subprocess sees
    XDG_CONFIG_HOME=<config-home> at `drcode.config` import time, so the
    check reproduces the import-time binding exactly (no monkeypatching).
    """
    payload = json.dumps(
        {
            "workspace": str(paths.workspace),
            "config_home": str(paths.config_home),
            "combo": {
                "name": combo.name,
                "coding": combo.coding,
                "tester": combo.tester,
                "compaction": combo.compaction,
            },
            "matrix_path": str(matrix_path) if matrix_path else None,
        }
    )
    result = subprocess.run(
        [sys.executable, "-m", "bench.env_setup"],
        input=payload,
        text=True,
        capture_output=True,
        env=paths.subprocess_env(),
        cwd=str(Path(__file__).resolve().parents[1]),
        check=False,
    )
    if result.returncode != 0:
        raise EnvSetupError(f"pre-flight subprocess failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def _preflight_main() -> int:
    """Entry of `python -m bench.env_setup`: read the job spec from stdin,
    verify resolution with the (already sanitized) process env, print the
    resolved role map as JSON."""
    import sys as _sys

    spec = json.loads(_sys.stdin.read())
    combo = Combo(
        name=spec["combo"]["name"],
        coding=spec["combo"]["coding"],
        tester=spec["combo"]["tester"],
        compaction=spec["combo"]["compaction"],
    )
    matrix_path = Path(spec["matrix_path"]) if spec.get("matrix_path") else None
    # XDG_CONFIG_HOME of this process IS the run's config-home; drcode.config
    # binds it at import time — exactly like in the real run.
    resolved = verify_resolution(
        Path(spec["workspace"]),
        Path(spec["config_home"]),
        combo,
        matrix_path=matrix_path,
    )
    print(json.dumps(resolved))
    return 0


if __name__ == "__main__":
    raise SystemExit(_preflight_main())
