"""Unit tests of the §9 fault-injecting proxy (bench/proxy.py): the
deterministic fault engine, the provider-prefix routing, the fault
semantics on the real HTTP layer (429 / truncated response / delay) and
the catalog rewrite (apply_proxy_base).

The streaming/forwarding path is exercised against tests/fake_gateway.py
— a real HTTP server, no mocks (the proxy is pure HTTP plumbing; mocking
it would prove nothing).
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from bench.matrix import load_matrix
from bench.proxy import (
    FaultEngine,
    FaultProxy,
    FaultSpec,
    ProxyError,
    apply_proxy_base,
    parse_faults,
)
from tests.fake_gateway import start as start_gateway

# --- fault engine ---------------------------------------------------------------


def test_fault_engine_deterministic_by_counter() -> None:
    engine = FaultEngine(
        (
            FaultSpec("http_429", 1, "chat/completions"),
            FaultSpec("http_429", 2, "chat/completions"),
            FaultSpec("drop", 4, "chat/completions"),
        )
    )
    seq = ["chat/completions"] * 6
    fired = [engine.inspect(p) for p in seq]
    assert [f.kind if f else None for f in fired] == [
        "http_429",
        "http_429",
        None,
        "drop",
        None,
        None,
    ]
    # A fresh engine replays the same pattern — reproducibility of the
    # fault script (DoD of §9).
    engine2 = FaultEngine(engine.faults)
    again = [engine2.inspect(p) for p in seq]
    assert [(f.kind if f else None) for f in again] == [f.kind if f else None for f in fired]


def test_fault_engine_scope_and_independent_rules() -> None:
    # The /models probes must not consume the chat/completions counters.
    engine = FaultEngine((FaultSpec("http_429", 2, "chat/completions"),))
    assert engine.inspect("p/fake/models") is None
    assert engine.inspect("p/fake/chat/completions") is None  # cnt=1
    fault = engine.inspect("p/fake/chat/completions")  # cnt=2 → fire
    assert fault is not None and fault.kind == "http_429"


def test_fault_engine_rules_advance_independently() -> None:
    """A fired rule must not freeze the counters of the later rules —
    otherwise the fault pattern would depend on rule ORDER, not on the
    request stream (the bug this test pins)."""
    engine = FaultEngine(
        (FaultSpec("http_429", 1, "chat/completions"), FaultSpec("drop", 2, "chat/completions"))
    )
    fault = engine.inspect("chat/completions")
    assert fault is not None and fault.kind == "http_429"
    fault = engine.inspect("chat/completions")
    assert fault is not None and fault.kind == "drop"
    assert engine.inspect("chat/completions") is None


def test_fault_spec_validation() -> None:
    with pytest.raises(ProxyError):
        FaultSpec("alien", 1)
    with pytest.raises(ProxyError):
        FaultSpec("http_429", 0)
    with pytest.raises(ProxyError):
        FaultSpec("delay", 1)  # delay needs delay_s > 0
    with pytest.raises(ProxyError):
        parse_faults([{"kind": "nope", "nth": 1}])


def test_parse_faults_from_scenario_section() -> None:
    faults = parse_faults(
        [
            {"kind": "http_429", "nth": 1, "scope": "chat/completions"},
            {"kind": "drop", "nth": 4},
            {"kind": "delay", "nth": 5, "delay_s": 2.5},
        ]
    )
    assert [f.kind for f in faults] == ["http_429", "drop", "delay"]
    assert faults[2].delay_s == 2.5


# --- routing ----------------------------------------------------------------------


def test_route_prefix_mapping() -> None:
    app = FaultProxy({"fake": "http://up:8000/v1"}).app
    url, name = app.route("/p/fake/chat/completions")
    assert url == "http://up:8000/v1/chat/completions"
    assert name == "fake"
    # Empty rest (a GET of the base) forwards to the bare upstream.
    assert app.route("/p/fake")[0] == "http://up:8000/v1"
    with pytest.raises(ProxyError):
        app.route("/p/unknown/models")
    with pytest.raises(ProxyError):
        app.route("/no-prefix")


# --- the real HTTP layer (against the scripted gateway) ----------------------------


async def test_proxy_forwards_and_injects_faults(tmp_path: Path) -> None:
    server = await start_gateway(0)
    gport = server.sockets[0].getsockname()[1]
    log_path = tmp_path / "proxy_log.jsonl"
    proxy = FaultProxy(
        {"fake": f"http://127.0.0.1:{gport}/v1"},
        (
            FaultSpec("http_429", 1, "chat/completions"),
            FaultSpec("drop", 2, "chat/completions"),
        ),
        log_path=log_path,
    )
    base = await proxy.start()
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Non-chat path: forwarded untouched.
            r = await client.get(f"{base}/p/fake/models")
            assert r.status_code == 200
            assert "fake-coder" in [m["id"] for m in r.json()["data"]]

            body = {
                "model": "fake-coder",
                "messages": [{"role": "user", "content": "ping"}],
            }
            # 1st chat request: 429 by the fault script — never forwarded.
            r1 = await client.post(f"{base}/p/fake/chat/completions", json=body)
            assert r1.status_code == 429
            assert r1.json()["error"]["type"] == "bench_fault_injection"

            # 2nd: the drop — a truncated response the HTTP stack reports
            # as an incomplete read (a transport break, NOT an HTTP status).
            with pytest.raises(httpx.RemoteProtocolError):
                await client.post(f"{base}/p/fake/chat/completions", json=body)

            # 3rd: passes through — the scripted completion over real SSE.
            r3 = await client.post(f"{base}/p/fake/chat/completions", json={**body, "stream": True})
            assert r3.status_code == 200
            assert "data: [DONE]" in r3.text
    finally:
        await proxy.stop()
        server.close()
        await server.wait_closed()

    # The log (§9/§10): one line per request, faults included.
    entries = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert len(entries) == 4
    faults = [e["fault"]["kind"] for e in entries if e.get("fault")]
    assert faults == ["http_429", "drop"]
    forwarded = [e for e in entries if not e.get("fault")]
    assert {e["status"] for e in forwarded} == {200}
    assert all(isinstance(e["latency_ms"], int) for e in entries)
    assert all(e["provider"] == "fake" for e in entries)
    # The model name is peeked from the request body (per-model latency).
    chat = [e for e in entries if e["model"]]
    assert chat and all(e["model"] == "fake-coder" for e in chat)


async def test_proxy_delay_fault(tmp_path: Path) -> None:
    server = await start_gateway(0)
    gport = server.sockets[0].getsockname()[1]
    proxy = FaultProxy(
        {"fake": f"http://127.0.0.1:{gport}/v1"},
        (FaultSpec("delay", 1, "chat/completions", delay_s=0.4),),
    )
    base = await proxy.start()
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            body = {"model": "fake-coder", "messages": [{"role": "user", "content": "p"}]}
            import time

            t0 = time.monotonic()
            r = await client.post(f"{base}/p/fake/chat/completions", json=body)
            elapsed = time.monotonic() - t0
            assert r.status_code == 200
            assert elapsed >= 0.4, "the delay fault must stall the request"
    finally:
        await proxy.stop()
        server.close()
        await server.wait_closed()


# --- catalog rewrite ---------------------------------------------------------------


def test_apply_proxy_base_rewrites_every_provider() -> None:
    providers, _ = load_matrix(Path(__file__).resolve().parents[1] / "matrix.toml")
    rewritten = apply_proxy_base(providers, "http://127.0.0.1:12345")
    for name, spec in rewritten.items():
        assert spec.base_url == f"http://127.0.0.1:12345/p/{name}"
        assert spec.models is providers[name].models  # untouched otherwise
    # The originals stay intact (the matrix file remains the source of
    # the real endpoints).
    for spec in providers.values():
        assert "/p/" not in spec.base_url


def test_prepare_run_with_proxy_base(tmp_path: Path) -> None:
    """The generated catalog + flat config point at the proxy (§3/§9);
    the pre-flight validates the exact (proxy-routed) resolution."""
    from bench.env_setup import prepare_run, verify_resolution
    from bench.matrix import get_combo

    repo = Path(__file__).resolve().parents[1]
    scenario_dir = repo / "scenarios" / "s1_happy"
    combo = get_combo(repo / "tests" / "fixtures" / "none.toml", "") if False else None
    # A minimal in-test matrix keeps the test independent of matrix.toml.
    matrix = tmp_path / "matrix.toml"
    matrix.write_text(
        """
[providers.fake]
base_url = "http://127.0.0.1:9001/v1"
api_key  = ""

[providers.fake.models.fake-coder]
max_context_tokens = 100000

[providers.fake.models.fake-tester]
max_context_tokens = 100000

[[combo]]
name       = "p"
coding     = "fake/fake-coder"
tester     = "fake/fake-tester"
compaction = "fake/fake-coder"
""",
        encoding="utf-8",
    )
    combo = get_combo(matrix, "p")
    run_dir = tmp_path / "run"
    paths = prepare_run(
        scenario_dir, combo, run_dir, matrix_path=matrix, proxy_base="http://127.0.0.1:12345"
    )
    catalog = json.loads(paths.models_catalog.read_text())
    for provider in catalog["providers"]:
        assert provider["base_url"] == f"http://127.0.0.1:12345/p/{provider['name']}"
    project = json.loads(paths.project_config.read_text())
    assert project["base_url"] == "http://127.0.0.1:12345/p/fake"
    # Pre-flight passes against the proxy-routed config...
    resolved = verify_resolution(
        paths.workspace,
        paths.config_home,
        combo,
        matrix_path=matrix,
        proxy_base="http://127.0.0.1:12345",
    )
    assert set(resolved) == {"coding", "tester", "compaction"}
    # ...and would FAIL against the real endpoints — the two layers must
    # never disagree about where the traffic goes.
    with pytest.raises(Exception, match="pre-flight failed"):
        verify_resolution(paths.workspace, paths.config_home, combo, matrix_path=matrix)


# --- scenario [proxy] section --------------------------------------------------------


def test_scenario_proxy_section_parsed() -> None:
    from bench.scenario import load_scenario

    repo = Path(__file__).resolve().parents[1]
    scenario = load_scenario(repo / "scenarios" / "s7_fault_injection")
    assert scenario.proxy is not None
    assert scenario.proxy.enabled
    assert [f.kind for f in scenario.proxy.faults] == [
        "http_429",
        "http_429",
        "http_429",
        "drop",
        "drop",
    ]
    assert all(f.scope == "chat/completions" for f in scenario.proxy.faults)
    # A scenario without the section has no proxy setup.
    plain = load_scenario(repo / "scenarios" / "s1_happy")
    assert plain.proxy is None


def test_scenario_proxy_faults_require_enabled(tmp_path: Path) -> None:
    from bench.scenario import ScenarioError, load_scenario

    bad = tmp_path / "s_bad"
    (bad / "seed").mkdir(parents=True)
    (bad / "seed" / "x.py").write_text("x = 1\n")
    (bad / "scenario.toml").write_text(
        """
id = "s_bad"
timeout = 1

[[briefs]]
title = "t"
text = "do it"
kind = "feature"

[proxy]
enabled = false

[[proxy.faults]]
kind = "drop"
nth = 1
""",
        encoding="utf-8",
    )
    with pytest.raises(ScenarioError, match="enabled"):
        load_scenario(bad)


def test_scenario_proxy_unknown_fault_kind_rejected(tmp_path: Path) -> None:
    from bench.scenario import ScenarioError, load_scenario

    bad = tmp_path / "s_bad2"
    (bad / "seed").mkdir(parents=True)
    (bad / "seed" / "x.py").write_text("x = 1\n")
    (bad / "scenario.toml").write_text(
        """
id = "s_bad2"
timeout = 1

[[briefs]]
title = "t"
text = "do it"
kind = "feature"

[[proxy.faults]]
kind = "alien_probe"
nth = 1
""",
        encoding="utf-8",
    )
    with pytest.raises(ScenarioError, match="kind"):
        load_scenario(bad)


# The proxy must be startable twice in a row on the same loop (the
# e2e S7 test and real runs both rely on clean startup/shutdown).
async def test_proxy_restart_clean() -> None:
    server = await start_gateway(0)
    gport = server.sockets[0].getsockname()[1]
    for _ in range(2):
        proxy = FaultProxy({"fake": f"http://127.0.0.1:{gport}/v1"})
        base = await proxy.start()
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{base}/p/fake/models")
            assert r.status_code == 200
        await proxy.stop()
    server.close()
    await server.wait_closed()
