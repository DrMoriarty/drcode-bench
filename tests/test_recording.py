"""Tests of the recording wrapper around `agent_model.build_model` (§5).

Covered:

- `RecordingModel` logs exactly one JSONL line per model request, with
  role tag, model_name, latency, n_history, usage and ts — for both the
  non-streaming and the STREAMING path (the streaming path must stay
  streaming: deltas flow through untouched, the record lands when the
  consumer leaves the stream context);
- `install_recorder` monkeypatches `drcode.agent_model.build_model`
  (coder/tester AND compaction agents are wrapped — the compaction
  usage is the whole point of the recorder, §1.5);
- the role-tag limitation (§5): two roles on the same model share one
  tag — documented behavior, asserted here so it cannot silently change;
- `bench.metrics._load_model_log` percentiles and
  `bench.metrics.cross_check_usage` (recorder ↔ transcript сверка, §10),
  including the "compaction requests have no transcript counterpart"
  rule;
- an end-to-end S1 run against the local fake OpenAI gateway
  (tests/fake_gateway.py): the real `OpenAIChatModel` streaming path
  through the recorder, real `bench.run_one`, real metrics extraction.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest
from drcode import agent_model
from pydantic_ai import Agent
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.usage import RequestUsage

from bench.metrics import cross_check_usage, extract_run_metrics, transcript_responses
from bench.recording import JsonlSink, RecordingModel, install_recorder, usage_dict

REPO = Path(__file__).resolve().parents[1]


def _text_response(text: str, usage: RequestUsage | None = None):
    from pydantic_ai.messages import ModelResponse, TextPart

    # FunctionModel (pydantic-ai 2.x) requires a usage object on the
    # response; a zero-usage response is normalized by the model itself.
    return ModelResponse(parts=[TextPart(content=text)], usage=usage or RequestUsage())


def _read_log(log: Path) -> list[dict]:
    return [json.loads(line) for line in log.read_text().splitlines() if line.strip()]


def test_usage_dict_handles_field_and_method(tmp_path: Path) -> None:
    resp = _text_response("x", RequestUsage(input_tokens=10, output_tokens=2))
    assert usage_dict(resp) == {
        "input_tokens": 10,
        "output_tokens": 2,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
    }
    assert usage_dict(_text_response("x", None)) is None


def test_request_path_logs_one_line_per_request(tmp_path: Path) -> None:
    log = tmp_path / "model_log.jsonl"
    calls: list[int] = []

    def fn(messages, info):
        calls.append(1)
        return _text_response("hi", RequestUsage(input_tokens=7, output_tokens=3))

    sink = JsonlSink(log)
    model = RecordingModel(FunctionModel(fn), "coder@http://gw/v1", sink)
    agent = Agent(model)
    first = asyncio.run(agent.run("hello"))
    asyncio.run(agent.run("again", message_history=first.all_messages()))

    records = _read_log(log)
    assert len(records) == 2
    rec = records[0]
    assert rec["role"] == "coder@http://gw/v1"
    assert rec["streamed"] is False
    assert rec["n_history"] == 1  # fresh run: single user message
    assert rec["usage"] == {"input_tokens": 7, "output_tokens": 3, "cache_read_tokens": 0, "cache_write_tokens": 0}
    assert rec["latency_ms"] >= 0
    assert isinstance(rec["ts"], float)
    assert records[1]["n_history"] == 3  # request+response of the first run


def test_stream_path_stays_streaming_and_logs_final_usage(tmp_path: Path) -> None:
    """§5/§13: deltas reach the consumer unchanged; the log line carries
    the final usage and lands only after the stream is exhausted."""
    log = tmp_path / "model_log.jsonl"
    deltas_seen: list[str] = []

    async def stream_fn(messages, info):
        yield "a"
        yield "b"
        yield "c"

    def fn(messages, info):
        return _text_response("abc", RequestUsage(input_tokens=11, output_tokens=3))

    model = RecordingModel(
        FunctionModel(fn, stream_function=stream_fn), "tester@http://gw/v1", JsonlSink(log)
    )
    agent = Agent(model)

    async def consume() -> str:
        async with agent.run_stream("stream me") as result:
            chunks = []
            async for chunk in result.stream_output(debounce_by=None):
                chunks.append(chunk)
                deltas_seen.append(chunk)
            return await result.get_output()

    output = asyncio.run(consume())
    assert output == "abc"
    # Real deltas, not one blob: the text arrives in pieces and a final
    # full-output event closes the stream.
    assert deltas_seen[:3] == ["a", "ab", "abc"]

    (record,) = _read_log(log)
    assert record["streamed"] is True
    # FunctionModel estimates stream usage from the deltas (the exact
    # real-usage passthrough is covered by the gateway e2e test below,
    # where OpenAIChatModel reports the provider's usage chunk).
    assert record["usage"] is not None
    assert record["usage"]["output_tokens"] == 3


def test_request_error_is_logged_with_error_field(tmp_path: Path) -> None:
    log = tmp_path / "model_log.jsonl"

    def fn(messages, info):
        raise RuntimeError("gateway down")

    model = RecordingModel(FunctionModel(fn), "coder@http://gw/v1", JsonlSink(log))
    agent = Agent(model)
    with pytest.raises(RuntimeError):
        asyncio.run(agent.run("boom"))

    (record,) = _read_log(log)
    assert "RuntimeError" in record["error"]
    assert record["usage"] is None
    assert record["streamed"] is False


def test_same_model_two_roles_share_one_tag(tmp_path: Path) -> None:
    """Documented limitation (§5): the tag is model+base_url, not the role —
    two roles on the same model produce identical tags. Locked by a test
    so nobody mistakes it for a bug (and for the matrix to avoid)."""
    log = tmp_path / "model_log.jsonl"
    for tag in ("same@http://gw/v1", "same@http://gw/v1"):
        model = RecordingModel(
            FunctionModel(lambda m, i: _text_response("ok")), tag, JsonlSink(log)
        )
        asyncio.run(Agent(model).run("x"))
    records = _read_log(log)
    assert [r["role"] for r in records] == ["same@http://gw/v1", "same@http://gw/v1"]


def test_install_recorder_wraps_build_model_including_compaction(tmp_path: Path) -> None:
    """§5/§1.5: after install_recorder, EVERY agent built through
    `agent_model.build_model` — coder, tester and the compaction
    summarizer — is recorded. The compaction agent's usage is nowhere on
    drcode's disk, the recorder is the only witness."""
    log = tmp_path / "model_log.jsonl"

    def fake_builder(config):
        return FunctionModel(lambda m, i: _text_response("summary"))

    original = agent_model.build_model
    agent_model.build_model = fake_builder
    try:
        install_recorder(log)
        assert agent_model.build_model is not fake_builder  # patched

        from drcode.compaction import build_compaction_agent
        from drcode.config import Config

        config = Config(model="summarizer", base_url="http://gw/v1")
        compaction_agent = build_compaction_agent(config)
        asyncio.run(compaction_agent.run("compact this"))
    finally:
        agent_model.build_model = original

    records = _read_log(log)
    assert len(records) == 1
    assert records[0]["role"] == "summarizer@http://gw/v1"
    assert records[0]["model_name"].startswith("function:")


def test_load_model_log_percentiles(tmp_path: Path) -> None:
    lines = []
    for i, latency in enumerate([100, 200, 300, 400, 1000]):
        lines.append(
            json.dumps(
                {
                    "role": "m@u",
                    "model_name": "m",
                    "streamed": True,
                    "latency_ms": latency,
                    "n_history": i,
                    "usage": {"input_tokens": 10, "output_tokens": 1},
                    "ts": 1000.0 + i,
                }
            )
        )
    (tmp_path / "model_log.jsonl").write_text("\n".join(lines) + "\n")
    metrics = extract_run_metrics(tmp_path)
    log = metrics["model_log"]
    assert log["requests"] == 5
    entry = log["per_role"]["m@u"]
    assert entry["requests"] == 5
    assert entry["latency_ms_p50"] == 300
    assert entry["latency_ms_p95"] == 880  # linear interpolation between 400 and 1000
    assert log["latency_ms_p50"] == 300
    assert entry["input_tokens"] == 50


def test_cross_check_usage_matches_and_flags() -> None:
    responses = [
        {"source": "coder", "ts": "2025-01-01T00:00:00+00:00", "input_tokens": 100, "output_tokens": 10},
        {"source": "tester", "ts": "2025-01-01T00:00:05+00:00", "input_tokens": 50, "output_tokens": 5},
    ]
    entries = [
        {"role": "m@u", "ts": 1735689600.1, "usage": {"input_tokens": 100, "output_tokens": 10}},
        {"role": "m@u", "ts": 1735689605.1, "usage": {"input_tokens": 50, "output_tokens": 5}},
        # A compaction request: no transcript counterpart, expected.
        {"role": "m@u", "ts": 1735689606.0, "usage": {"input_tokens": 30, "output_tokens": 40}},
    ]
    cross = cross_check_usage(responses, entries, n_compactions_started=1)
    assert cross["matched"] == 2
    assert cross["unmatched_transcript"] == []
    assert cross["n_unmatched_recorder"] == 1
    assert cross["unexplained"] is False
    assert cross["tokens"]["delta_input"] == 30
    assert cross["tokens"]["delta_output"] == 40


def test_cross_check_usage_flags_unexplained() -> None:
    responses = [
        {"source": "coder", "ts": "2025-01-01T00:00:00+00:00", "input_tokens": 100, "output_tokens": 10},
    ]
    # Recorder billed nothing like that response and compaction explains none.
    entries = [
        {"role": "m@u", "ts": 1735689600.1, "usage": {"input_tokens": 999, "output_tokens": 999}},
    ]
    cross = cross_check_usage(responses, entries, n_compactions_started=0)
    assert cross["matched"] == 0
    assert len(cross["unmatched_transcript"]) == 1
    assert cross["n_unmatched_recorder"] == 1
    assert cross["unexplained"] is True


def test_transcript_responses_covers_coder_and_tester() -> None:
    task = {
        "messages": [
            {"kind": "request", "parts": []},
            {"kind": "response", "usage": {"input_tokens": 10, "output_tokens": 2},
             "timestamp": "2025-01-01T00:00:00+00:00", "parts": []},
        ],
        "tester_messages": [
            [
                {"kind": "response", "usage": {"input_tokens": 20, "output_tokens": 4},
                 "timestamp": "2025-01-01T00:00:09+00:00", "parts": []},
            ]
        ],
    }
    out = transcript_responses(task)
    assert [(r["source"], r["input_tokens"]) for r in out] == [("coder", 10), ("tester", 20)]


@pytest.mark.asyncio
async def test_end_to_end_s1_on_fake_gateway(tmp_path: Path, monkeypatch) -> None:
    """DoD of §5: an S1 run against a local model leaves model_log.jsonl
    with one record per request (real OpenAIChatModel SSE streaming),
    and metrics.json cross-checks recorder vs transcripts."""
    from tests.fake_gateway import start

    server = await start(0)
    port = server.sockets[0].getsockname()[1]
    matrix_path = tmp_path / "matrix.toml"
    matrix_path.write_text(
        f"""
[providers.fake]
base_url = "http://127.0.0.1:{port}/v1"
api_key  = ""

[providers.fake.models.fake-coder]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.fake-tester]
max_context_tokens = 100000
max_tokens = 8192

[providers.fake.models.fake-compaction]
max_context_tokens = 100000
max_tokens = 8192

[[combo]]
name       = "fixture-roles"
coding     = "fake/fake-coder"
tester     = "fake/fake-tester"
compaction = "fake/fake-compaction"
""",
        encoding="utf-8",
    )

    from bench.run_one import run_benchmark
    from bench.scenario import load_scenario_by_id

    # In-process isolation (env_setup._isolated_user_config does the same
    # for the pre-flight): drcode.config binds the user config dir at
    # import time — a real subprocess would sanitize the env before the
    # import, a pytest process must patch the binding instead, else the
    # developer's real user catalog resolves the roles.
    import drcode.config as dconfig

    run_dir = tmp_path / "runs" / "s1"
    config_home = run_dir / "config-home" / "drcode"
    config_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(dconfig, "_USER_CONFIG_DIR", config_home)
    monkeypatch.setattr(dconfig, "USER_CONFIG_FILE", config_home / "drcode.json")

    scenario = load_scenario_by_id(REPO / "scenarios", "s1_happy")
    try:
        report = await run_benchmark(scenario, "fixture-roles", run_dir, matrix_path)
        assert report.ok, report.reason

        records = _read_log(run_dir / "model_log.jsonl")
        assert records, "recorder wrote nothing"
        assert all(r["streamed"] is True for r in records)  # streaming preserved
        roles = {r["role"] for r in records}
        assert any("fake-coder" in r for r in roles)
        assert any("fake-tester" in r for r in roles)

        metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
        cross = metrics["usage_cross_check"]
        assert cross["matched"] == cross["transcript_responses"]
        assert cross["unexplained"] is False
        assert metrics["model_log"]["latency_ms_p50"] is not None
        for role, entry in metrics["model_log"]["per_role"].items():
            assert entry["latency_ms_p50"] is not None
            assert entry["input_tokens"] > 0
    finally:
        server.close()
        await server.wait_closed()
