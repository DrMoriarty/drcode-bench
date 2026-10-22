# AGENTS.md

## What this repo is

Benchmark harness for the drcode agent loop (coding → testing → compaction) with a model per role. `drcode/` is a **git submodule used as a path dependency** (`[tool.uv.sources]`) — never edit files under `drcode/` from this repo. Its internals are documented in `drcode/AGENTS.md`.

The full design lives in `drcode-bench.md`; code comments throughout `bench/` cite its sections (`§N`) — when a `§` comment is unclear, cross-reference the plan instead of guessing.

## Setup

```bash
git submodule update --init --recursive   # required: uv sync fails without the submodule
uv sync                                   # Python 3.12 (.python-version), creates .venv
```

The drcode path dependency is installed **non-editable**: after
`git submodule update --remote` a plain `uv sync` does NOT refresh the
installed copy (site-packages keeps the old version — an e2e suite can
look green while actually running against the previous drcode). Always
follow submodule updates with:

```bash
uv sync --reinstall-package drcode
uv run python -c "from importlib.metadata import version; print(version('drcode'))"
```

## Commands

```bash
uv run pytest                                            # whole suite (testpaths=tests, asyncio_mode=auto)
uv run pytest tests/test_runner.py -k gate               # focused run
uv run bench run --scenario all --matrix matrix.toml --parallel 2 --repeats 3
uv run bench run --scenario s6_queue_priority --combo strong-coder/cheap-tester --repeats 1
python -m bench.run_one <scenario> <combo> <run_dir>     # single run (no matrix sweep)
uv run bench report runs/ [--html]                       # → runs/report.md
uv run ruff check . && uv run ruff format --check .      # lint + format gate
uv run pyright                                           # type gate
python tests/fake_gateway.py [port]                      # local scripted OpenAI-compatible gateway
```

No CI/pre-commit exists in this repo, but the repo gates on **ruff + pyright + pytest** (same tooling as the drcode submodule):

```bash
uv run ruff check . && uv run ruff format --check .   # lint + format
uv run pyright                                        # types (basic mode)
```

Ruff/pyright are scoped to `bench/` + `tests/` — the `drcode/` submodule is excluded (it has its own gate; never lint or fix it from this repo). Cyrillic in briefs/docstrings is intentional, hence `RUF001`–`RUF003` are ignored.

## How a run works (non-obvious invariants)

- **One scenario = one subprocess** (`bench/run_one.py`): `drcode.config` binds `XDG_CONFIG_HOME` at import time, and drcode's repo `.env` leaks through pydantic-settings — only a fresh process with a scrubbed env gives clean layered config. The env is sanitized *in place, before* drcode is imported.
- **Never set `DRCODE_MODEL` / `DRCODE_BASE_URL`**: they override the per-role (coding/tester/compaction) model choice for *all* roles. Role selection comes only from `matrix.toml` → generated `models.json` / `.drcode/drcode.json` files.
- The harness runs the **real `DrCodeApp` headless** (textual `run_test()`) — never reimplement or fork the drcode pipeline in bench code.
- The recording wrapper monkeypatches `drcode.agent_model.build_model` *before* app creation; `viewed_id` is never touched (opening a task renders the whole transcript and pollutes timing measurements).
- `bench run` exit codes: 0 = every job got a verdict (a substantive failure is a data point, not an error), 1 = unresolved infrastructure failures, 2 = planning errors.
- Artifacts per run land in `runs/<run_id>/` (gitignored): `result.json`, `metrics.json`, `model_log.jsonl`, `user_sim.jsonl`, a `.drcode/` snapshot. `runs/runner-summary.json` holds scheduler history.

## Matrix & scenarios

- `matrix.toml`: providers + `[[combo]]` with exactly three roles (`coding`/`tester`/`compaction`). `api_key` supports `"env:NAME"` substitution. Combo keys like `coding_max_context_tokens = 3000` become per-model catalog overrides (used to force compaction without env vars).
- Scenario = `scenarios/<id>/` with `seed/` (copied into the run workspace), `scenario.toml` (briefs, followups, clarification_answers, timeout, `[settle]`), and `checks.py` (harness calls `python checks.py <workspace>`; exit 0 = green). Verdicts are always **mechanical** — the harness runs pytest in the workspace itself; never judge by agent words.
- Task kinds in briefs: `feature`/`bug` only — `research` tasks never reach the tester.
- Implemented scenarios: S1, S2a, S2b, S3, S4, S5, S6, S7.
- S7 routes the run through `bench/proxy.py` (§9): a scenario `[proxy]` section enables it with a deterministic fault script (`[[proxy.faults]]`: `http_429`/`drop`/`delay` fired by request counter); `bench run --use-proxy` / `run_one --use-proxy` forces a fault-free recording proxy for any scenario. Proxy log → `runs/<run_id>/proxy_log.jsonl`, aggregated into `metrics.json["proxy"]` (+ `latency_cross_check` against the recorder when both are on). Note: the openai SDK inside drcode retries 429s itself (max_retries=2) — a drcode-visible 429 needs three consecutive 429 faults; connection drops are never SDK-retried.
- Scenario briefs and docs are written in Russian; code and comments in English — keep that split.

## Testing quirks

- `tests/test_scenarios_e2e.py` drives the **real pipeline end-to-end** through `tests/fake_gateway.py` (localhost HTTP/SSE, scripted per model id) — much slower than the unit tests, but no external network. The fake gateway inflates reported usage to genuinely trip drcode's compaction gates.
- In-process runs must monkeypatch `drcode.config._USER_CONFIG_DIR`/`USER_CONFIG_FILE` (config dir is bound at import time) and restore `os.environ` around the test — see `env_guard` and `test_scenarios_e2e.py` for the established pattern.
- The user simulator (`bench/user_sim.py`) is part of correctness, not a test helper: every intervention goes to `user_sim.jsonl`, and its scenario failures are hard settle-blockers.
