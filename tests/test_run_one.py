"""End-to-end smoke test of bench.run_one (plan §4) — WITHOUT real models.

The combo points at a black-hole endpoint (port 1: connection refused
instantly). The run therefore cannot settle: the app boots for real, the
brief is queued and activated, the agent run fails, and `wait_settle`
must time out → `dump_diagnostics` + result.json with ok=false. This
exercises the full plumbing (env prep → headless DrCodeApp → briefs →
settle timeout → diagnostics) in seconds.

The scenario timeout is shortened via dataclasses.replace; the process
environment mutated by run_benchmark is restored afterwards.
"""

from __future__ import annotations

import dataclasses
import json
import os
from pathlib import Path

import pytest

from bench.matrix import load_matrix
from bench.run_one import run_benchmark
from bench.scenario import load_scenario_by_id

REPO = Path(__file__).resolve().parents[1]

MATRIX = """
[providers.blackhole]
base_url = "http://127.0.0.1:1/v1"
api_key = ""

[providers.blackhole.models.stub-model]
max_context_tokens = 100000
max_tokens = 4096

[[combo]]
name = "blackhole"
coding = "blackhole/stub-model"
tester = "blackhole/stub-model"
compaction = "blackhole/stub-model"
"""


@pytest.fixture
def env_guard():
    saved = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(saved)


async def test_run_one_blackhole_times_out_with_diagnostics(
    tmp_path: Path, env_guard
) -> None:
    matrix_path = tmp_path / "matrix.toml"
    matrix_path.write_text(MATRIX, encoding="utf-8")
    _, combos = load_matrix(matrix_path)
    assert combos[0].name == "blackhole"

    scenario = load_scenario_by_id(REPO / "scenarios", "s1_happy")
    # Shrink the 45-minute soft limit to ~5 s for the smoke run.
    scenario = dataclasses.replace(scenario, timeout_min=0.08)

    run_dir = tmp_path / "runs" / "r1"
    report = await run_benchmark(scenario, "blackhole", run_dir, matrix_path)

    assert not report.ok
    assert report.timed_out
    assert report.tasks, "the brief must have been created"
    # The env hygiene ran: no DRCODE_* survived into the run process env.
    assert not [k for k in os.environ if k.startswith("DRCODE_")]
    assert os.environ.get("XDG_CONFIG_HOME") == str(run_dir / "config-home")

    # Artifacts on disk.
    result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
    assert result["ok"] is False
    assert result["timed_out"] is True
    assert result["checks_ok"] is False  # pytest cannot pass on the untouched seed
    assert (run_dir / "diagnostics" / "diagnostics.json").is_file()
    assert (run_dir / "diagnostics" / "drcode-state" / "drcode.json").is_file()
    diag = json.loads(
        (run_dir / "diagnostics" / "diagnostics.json").read_text(encoding="utf-8")
    )
    assert diag["state_dir_found"] is True
    assert diag["tasks"], "task JSONs must be snapshotted"

    # The generated project config carries the flat coding connection
    # (is_ready gate) AND the per-role selection.
    cfg = json.loads(
        (run_dir / "workspace" / ".drcode" / "drcode.json").read_text(encoding="utf-8")
    )
    assert cfg["model"] == "stub-model"
    assert cfg["base_url"] == "http://127.0.0.1:1/v1"
    assert cfg["models"] == {
        "coding": "blackhole/stub-model",
        "tester": "blackhole/stub-model",
        "compaction": "blackhole/stub-model",
    }


async def test_run_one_happy_path_settles_green(
    tmp_path: Path, env_guard, monkeypatch
) -> None:
    """Full S1 cycle with a scripted model (no HTTP at all): the coder
    fixes the seed via run_bash, the tester stamps PASSED — the run must
    settle green and checks.py must pass."""
    from drcode import agent_model
    from pydantic_ai.messages import (
        ModelRequest,
        ModelResponse,
        TextPart,
        ToolCallPart,
        UserPromptPart,
    )
    from pydantic_ai.models.function import AgentInfo, DeltaToolCall, FunctionModel

    def _text_response(text: str) -> ModelResponse:
        return ModelResponse(parts=[TextPart(content=text)])

    def _tool_response(tool: str, args: dict) -> ModelResponse:
        return ModelResponse(
            parts=[ToolCallPart(tool_name=tool, args=args, tool_call_id="c1")]
        )

    def _last_user_text(messages: list) -> str:
        parts = []
        for msg in messages:
            if isinstance(msg, ModelRequest):
                for p in msg.parts:
                    if isinstance(p, UserPromptPart) and isinstance(p.content, str):
                        parts.append(p.content)
        return "\n".join(parts)

    fix_cmd = (
        "printf 'def shout(text):\\n    return text.upper() + \"!\"\\n'"
        " > string_utils.py"
    )
    state = {"steps": [], "calls": []}

    def fn(messages: list, info: AgentInfo) -> ModelResponse:
        state["calls"].append(_last_user_text(messages))
        steps: list = state["steps"]
        assert steps, "scripted model queue is empty"
        return steps.pop(0)

    async def stream_fn(messages: list, info: AgentInfo):
        # Mirror drcode's own ScriptedState.stream_fn: text as str deltas,
        # tool calls as DeltaToolCall (the TUI consumes deltas; a plain
        # dict is not accepted by pydantic-ai's FunctionModel).
        response = fn(messages, info)
        for part in response.parts:
            if isinstance(part, TextPart):
                yield part.content
            elif isinstance(part, ToolCallPart):
                args = part.args if isinstance(part.args, str) else json.dumps(part.args or {})
                yield {
                    0: DeltaToolCall(
                        name=part.tool_name,
                        json_args=args,
                        tool_call_id=part.tool_call_id,
                    )
                }

    monkeypatch.setattr(
        agent_model,
        "build_model",
        lambda cfg: FunctionModel(fn, stream_function=stream_fn),
    )

    matrix_path = tmp_path / "matrix.toml"
    matrix_path.write_text(MATRIX, encoding="utf-8")
    scenario = load_scenario_by_id(REPO / "scenarios", "s1_happy")
    scenario = dataclasses.replace(scenario, timeout_min=0.5)

    state["steps"] = [
        _tool_response("run_bash", {"command": fix_cmd}),  # coder: fix the seed
        _text_response("Fixed shout(); pytest is green."),  # coder: end of run
        _tool_response("set_verification", {"success": True}),  # tester verdict
        _text_response("All tests pass."),  # tester: end of round
    ]

    run_dir = tmp_path / "runs" / "happy"
    report = await run_benchmark(scenario, "blackhole", run_dir, matrix_path)

    assert report.ok, report.reason
    assert not report.timed_out
    assert report.checks_ok is True
    (task,) = report.tasks
    assert task["status"] == "completed"
    assert task["verification"] == "Verified successfully"
    assert task["n_testing_rounds"] == 1
    # The coder saw the brief exactly once, as one prompt (§7 S1: the
    # brief reaches the model verbatim).
    assert "Сделайте тест зелёным" in state["calls"][0] or "pytest" in state["calls"][0]
