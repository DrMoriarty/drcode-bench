"""Preparation of the per-run environment (plan drcode-bench.md, §3).

One run = one isolated tmp tree:

    <run_dir>/
    ├── workspace/            # project root for the agents (seed copy + .drcode/ + .git)
    │   ├── <seed files>
    │   ├── AGENTS.md         # optional
    │   ├── .gitignore        # ".drcode/" (matches drcode's own behavior)
    │   ├── .git/             # init + first commit
    │   └── .drcode/
    │       ├── drcode.json   # per-role "models" selection + non-provider
    │       │                 # settings (compaction_threshold); provider
    │       │                 # fields never live here (drcode ≥ 0.5 moves
    │       │                 # them into the catalog / custom models)
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
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from .matrix import (
    ROLES,
    Combo,
    ProviderSpec,
    _resolve_api_key,
    effective_max_context,
    load_matrix,
    parse_ref,
)

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


def materialize_providers(
    combo: Combo,
    providers: dict[str, ProviderSpec],
) -> tuple[dict[str, ProviderSpec], dict[str, tuple[str, str]]]:
    """Apply the combo's per-role `max_context_tokens` overrides (§1.2) to
    the provider catalog and return the materialized providers plus the
    effective role refs.

    - No override (or an override equal to the catalog value): the role
      keeps its original ref — the happy path of every non-compaction
      combo.
    - An override on a (provider, model) pair NOT shared with a role that
      needs a different value: the catalog entry is patched in place —
      `providers.resolve` copies `max_context_tokens` from the entry into
      the role's config (the catalog entry is the layer that carries the
      role's connection, §1.2).
    - A CONFLICT (same provider+model referenced by roles needing different
      values): the overridden role is re-pointed at a virtual provider
      `<name>--ctx<N>` — same base_url/api_key, single model entry with the
      overridden context. Model ids stay untouched so the run reports the
      model the combo asked for.

    The point of the whole mechanism: compaction scenarios set a SMALL
    context on the compacted role (S3 → coding, S4 → tester — since
    drcode 0.5.0 each compaction gate reads its own role's resolved config)
    WITHOUT touching `DRCODE_*` env (which the run hygiene strips anyway,
    §13) — the override travels in the generated models.json, the catalog
    layer drcode honors per role.
    """
    refs: dict[str, tuple[str, str]] = {}
    wants: dict[tuple[str, str], dict[int, list[str]]] = {}
    for role in ROLES:
        provider_name, model_id = parse_ref(combo.ref(role), f"combo '{combo.name}' role {role}")
        refs[role] = (provider_name, model_id)
        ctx = effective_max_context(combo, providers, role)
        wants.setdefault((provider_name, model_id), {}).setdefault(ctx, []).append(role)

    out = {name: providers[name] for name in providers}
    for (provider_name, model_id), by_ctx in wants.items():
        if len(by_ctx) == 1:
            (ctx, _) = next(iter(by_ctx.items()))
            spec = out[provider_name]
            model = spec.model(model_id)
            if model.max_context_tokens != ctx:
                out[provider_name] = _spec_with_model(spec, model, ctx)
            continue
        # Conflict: the first role group in ROLES order wins the original
        # provider (its entry patched to that group's effective ctx), the
        # other groups get clones and their refs are rewritten.
        kept_ctx = min(by_ctx, key=lambda ctx: min(ROLES.index(r) for r in by_ctx[ctx]))
        spec = out[provider_name]
        model = spec.model(model_id)
        if model.max_context_tokens != kept_ctx:
            out[provider_name] = _spec_with_model(spec, model, kept_ctx)
        for ctx, roles in by_ctx.items():
            if ctx == kept_ctx:
                continue
            clone_name = f"{provider_name}--ctx{ctx}"
            suffix = 2
            while clone_name in out and clone_name != provider_name:
                clone_name = f"{provider_name}--ctx{ctx}-{suffix}"
                suffix += 1
            out[clone_name] = _spec_with_model(spec, spec.model(model_id), ctx, clone_name)
            for role in roles:
                refs[role] = (clone_name, model_id)
    return out, refs


def _spec_with_model(
    spec: ProviderSpec,
    model: object,
    max_context_tokens: int,
    name: str | None = None,
) -> ProviderSpec:
    """A copy of `spec` whose entry for `model.id` carries the given
    max_context_tokens (single-model copy when `name` is given — the
    virtual-provider form)."""
    from dataclasses import replace

    new_model = replace(model, max_context_tokens=max_context_tokens)  # type: ignore[arg-type]
    if name is None:
        models = dict(spec.models)
        models[model.id] = new_model  # type: ignore[index]
        return replace(spec, models=models)
    return replace(spec, name=name, models={model.id: new_model})  # type: ignore[dict-item]


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
    """models.json payload for the combo (format: drcode `UserModelsConfig`
    / `ModelEntry`, see `drcode/src/drcode/providers.py`). api_key =
    "env:NAME" is resolved from the host environment here.

    `providers` must already carry the combo's per-role context overrides
    (`materialize_providers`) — the catalog entry is the layer
    `providers.resolve` reads a role's connection and context from (§1.2)."""
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
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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
    agents_md: Path | None = None,
    proxy_base: str | None = None,
    exists_ok: bool = False,
) -> RunPaths:
    """Create the full run tree for one (scenario, combo) pair and return
    its layout (§3).

    - copies `<scenario_dir>/seed/` into `workspace/` (+ `AGENTS.md` when
      the scenario provides one);
    - generates `config-home/drcode/models.json` from the combo's providers;
    - writes `workspace/.drcode/drcode.json` (the per-role `models`
      selection + non-provider settings) and `workspace/.drcode/settings.json`
      (`stall_nudge="never"`, `completed_retention="never"`,
      `task_finalization="testing"` — or `"testing_commit"` with a LOCAL
      bare remote inside the run tree, never GitHub);
    - git-init's the workspace with a seed commit.

    `task_finalization` must be `"testing"` or `"testing_commit"`.

    `proxy_base` (§9): when set (e.g. `http://127.0.0.1:PORT` — the
    address of the run's fault-injection proxy), EVERY provider base_url
    in the generated catalog AND in the flat config points at
    `<proxy_base>/p/<provider-name>`; the proxy rewrites the prefix back
    to the real upstream (bench.proxy.ProxyApp.route). The pre-flight
    (`verify_resolution`) applies the same rewrite, so it validates the
    exact configuration the run will use.
    """
    scenario_dir = Path(scenario_dir)
    run_dir = Path(run_dir)
    if task_finalization not in FINALIZATION_CHOICES:
        raise EnvSetupError(
            f"task_finalization must be one of {FINALIZATION_CHOICES}, got {task_finalization!r}"
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

    # 2. user-level catalog of this combo, with the per-role
    #    max_context_tokens overrides written INTO the catalog entries
    #    (§1.2: the catalog entry beats the flat config for a role; §13:
    #    never via DRCODE_* env). Conflicting overrides on one model get a
    #    virtual provider clone; `refs` holds the effective role refs.
    used_providers = _providers_for_combo(combo, providers, matrix_path)
    catalog_providers, refs = materialize_providers(combo, used_providers)
    if proxy_base:
        # §9: every base_url the run sees goes through the proxy; the
        # real endpoints stay in the matrix file only.
        from .proxy import apply_proxy_base

        catalog_providers = apply_proxy_base(catalog_providers, proxy_base)
    models_catalog = _write_json(
        user_drcode_dir / "models.json", build_catalog(catalog_providers, combo)
    )

    # 3. project-level per-role selection. Provider fields never live in
    #    drcode.json (json layers stopped carrying them — drcode ≥ 0.5,
    #    `Config._PROVIDER_FIELDS`): every role resolves through its
    #    `models` ref into the generated catalog (providers.resolve). A
    #    legacy flat config here would be silently absorbed (and
    #    rewritten!) by drcode's startup migration `migrate_project_config`
    #    mid-run — so the generated file only carries the per-role refs
    #    plus non-provider settings (`compaction_threshold` still layers
    #    through the ordinary Config json layering).
    coding_provider_name, coding_model_id = refs["coding"]
    coding_model = catalog_providers[coding_provider_name].model(coding_model_id)
    project: dict[str, object] = {"models": {role: f"{p}/{m}" for role, (p, m) in refs.items()}}
    if coding_model.compaction_threshold is not None:
        project["compaction_threshold"] = coding_model.compaction_threshold
    project_config = _write_json(workspace / PROJECT_STATE_DIRNAME / "drcode.json", project)

    # 4. project settings: no watchdog, no retention cleanup, testing
    #    finalization — pushes go to a LOCAL bare remote inside the run
    #    tree only, never to GitHub (§13).
    remote: Path | None = None
    if task_finalization == "testing_commit":
        remote = run_dir / "remote.git"
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
    if task_finalization == "testing_commit" and remote is not None:
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
    saved_env = {k: v for k, v in os.environ.items() if k.startswith("DRCODE_")}
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
    proxy_base: str | None = None,
) -> dict[str, str]:
    """Pre-flight: resolve each role against the generated config and assert
    the expected model AND the expected max_context_tokens (the compaction
    scenarios live or die by the small coding context, §1.2). Returns
    role → "provider/model" as resolved.

    Uses `drcode.providers.resolve()` — the same precedence (env >
    project models > catalog defaults) the run will see;
    the expected refs/values come from `materialize_providers`, i.e. the
    combo's per-role overrides included. With `proxy_base` set (§9) the
    expected base_url is the proxy-routed one — the exact configuration
    the run was generated with (`prepare_run(proxy_base=...)`).
    """
    if providers is None:
        if matrix_path is None:
            matrix_path = Path(__file__).resolve().parents[1] / "matrix.toml"
        providers, _ = load_matrix(matrix_path)

    catalog_providers, refs = materialize_providers(combo, providers)
    if proxy_base:
        from .proxy import apply_proxy_base

        catalog_providers = apply_proxy_base(catalog_providers, proxy_base)

    import drcode.providers as dproviders
    from drcode.config import Config

    with _isolated_user_config(config_home):
        config = Config(project_root=Path(workspace).resolve())
        resolved: dict[str, str] = {}
        for role in ROLES:
            agent_role = dproviders.AgentRole(role)
            eff = dproviders.resolve(config, agent_role)
            provider_name, model_id = refs[role]
            spec = catalog_providers[provider_name]
            model = spec.model(model_id)
            expected_base_url = spec.base_url
            if eff.model != model_id or eff.base_url != expected_base_url:
                raise EnvSetupError(
                    f"pre-flight failed for role '{role}': expected "
                    f"{model_id}@{expected_base_url}, resolved "
                    f"{eff.model}@{eff.base_url}"
                )
            if eff.max_context_tokens != model.max_context_tokens:
                raise EnvSetupError(
                    f"pre-flight failed for role '{role}': resolved "
                    f"max_context_tokens={eff.max_context_tokens}, expected "
                    f"{model.max_context_tokens} (combo override + catalog "
                    "entry must reach the role)"
                )
            resolved[role] = f"{provider_name}/{eff.model}"
    return resolved


def run_preflight_subprocess(
    paths: RunPaths,
    combo: Combo,
    providers: dict[str, ProviderSpec] | None = None,
    matrix_path: Path | None = None,
    proxy_base: str | None = None,
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
                "max_context_overrides": [
                    [role, value] for role, value in combo.max_context_overrides
                ],
            },
            "matrix_path": str(matrix_path) if matrix_path else None,
            "proxy_base": proxy_base,
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
        max_context_overrides=tuple(
            (role, int(value)) for role, value in spec["combo"].get("max_context_overrides") or ()
        ),
    )
    matrix_path = Path(spec["matrix_path"]) if spec.get("matrix_path") else None
    proxy_base = spec.get("proxy_base") or None
    # XDG_CONFIG_HOME of this process IS the run's config-home; drcode.config
    # binds it at import time — exactly like in the real run.
    resolved = verify_resolution(
        Path(spec["workspace"]),
        Path(spec["config_home"]),
        combo,
        matrix_path=matrix_path,
        proxy_base=proxy_base,
    )
    print(json.dumps(resolved))
    return 0


if __name__ == "__main__":
    raise SystemExit(_preflight_main())
