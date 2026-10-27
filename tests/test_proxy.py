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
import time
from pathlib import Path

import httpx
import pytest
from bench.matrix import load_matrix
from bench.proxy import (
    FaultEngine,
    FaultProxy,
    FaultSpec,
    ProxyError,
    WatchdogSpec,
    apply_proxy_base,
    parse_faults,
    parse_watchdog,
)
from tests.fake_gateway import STALL_RULES, clear_stall_rules
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
            t0 = time.monotonic()
            r = await client.post(f"{base}/p/fake/chat/completions", json=body)
            elapsed = time.monotonic() - t0
            assert r.status_code == 200
            assert elapsed >= 0.4, "the delay fault must stall the request"
    finally:
        await proxy.stop()
        server.close()
        await server.wait_closed()


# --- stall watchdog (§9, opt-in [proxy.watchdog]) -----------------------------------


@pytest.fixture(autouse=True)
def _clean_stall_rules():
    clear_stall_rules()
    yield
    clear_stall_rules()


def test_watchdog_spec_parsing_and_validation() -> None:
    assert parse_watchdog(None) is None
    wd = parse_watchdog({})
    assert wd == WatchdogSpec(stall_timeout_s=45.0, retries=1)
    assert parse_watchdog({"stall_timeout_s": 30, "retries": 2}) == WatchdogSpec(30.0, 2)
    with pytest.raises(ProxyError):
        parse_watchdog({"stall_timeout_s": 0})
    with pytest.raises(ProxyError):
        parse_watchdog({"retries": -1})
    with pytest.raises(ProxyError):
        WatchdogSpec(stall_timeout_s=-5)
    # Config travels into result.json provenance.
    assert WatchdogSpec(30.0, 2).as_dict() == {"stall_timeout_s": 30.0, "retries": 2}


async def test_watchdog_aborts_stall_and_retry_succeeds(tmp_path: Path) -> None:
    """The S4 tail case: the upstream goes silent long past the watchdog
    budget on the FIRST attempt; the proxy aborts, retries ONCE — the
    retry hits an instantly responding upstream and the client sees one
    normal answer."""
    server = await start_gateway(0)
    gport = server.sockets[0].getsockname()[1]
    STALL_RULES["fake-compaction"] = {"stall_s": 5.0, "requests": 1, "mode": "pre"}
    log_path = tmp_path / "proxy_log.jsonl"
    proxy = FaultProxy(
        {"fake": f"http://127.0.0.1:{gport}/v1"},
        watchdog=WatchdogSpec(stall_timeout_s=0.3, retries=1),
        log_path=log_path,
    )
    base = await proxy.start()
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            t0 = time.monotonic()
            r = await client.post(
                f"{base}/p/fake/chat/completions",
                json={
                    "model": "fake-compaction",
                    "messages": [{"role": "user", "content": "p"}],
                },
            )
            elapsed = time.monotonic() - t0
            assert r.status_code == 200
            payload = r.json()
            assert payload["choices"][0]["message"]["content"]
            assert elapsed < 5.0, "the stalled upstream must be aborted, not waited out"
    finally:
        await proxy.stop()
        server.close()
        await server.wait_closed()

    from tests.fake_gateway import _stall_seen

    assert _stall_seen["fake-compaction"] == 2, "exactly one proxy-side retry"
    entries = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert len(entries) == 1, "drcode sees ONE request — the retry stays inside the proxy"
    wd = entries[0]["watchdog"]
    assert wd["saved"] is True
    assert wd["attempts"] == 2
    assert [ev["phase"] for ev in wd["events"]] == ["headers"]
    assert proxy.stats.watchdog_triggers == 1
    assert proxy.stats.watchdog_retries == 1
    assert proxy.stats.watchdog_saved == 1
    assert proxy.stats.watchdog_exhausted == 0


async def test_watchdog_exhausts_budget_and_reports_502(tmp_path: Path) -> None:
    """An upstream silent on EVERY attempt: exactly one retry, then the
    failure surfaces as-is (a clean 502) — no infinite retry loop."""
    server = await start_gateway(0)
    gport = server.sockets[0].getsockname()[1]
    STALL_RULES["fake-coder"] = {"stall_s": 5.0, "requests": None, "mode": "pre"}
    log_path = tmp_path / "proxy_log.jsonl"
    proxy = FaultProxy(
        {"fake": f"http://127.0.0.1:{gport}/v1"},
        watchdog=WatchdogSpec(stall_timeout_s=0.3, retries=1),
        log_path=log_path,
    )
    base = await proxy.start()
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                f"{base}/p/fake/chat/completions",
                json={"model": "fake-coder", "messages": [{"role": "user", "content": "p"}]},
            )
            assert r.status_code == 502
            assert r.json()["error"]["type"] == "bench_stall_watchdog"
    finally:
        await proxy.stop()
        server.close()
        await server.wait_closed()

    from tests.fake_gateway import _stall_seen

    assert _stall_seen["fake-coder"] == 2, "the initial attempt plus ONE retry, no more"
    entries = [json.loads(line) for line in log_path.read_text().splitlines()]
    wd = entries[0]["watchdog"]
    assert wd["saved"] is False
    assert wd["attempts"] == 2
    assert len(wd["events"]) == 2
    assert entries[0]["status"] == 502
    assert proxy.stats.watchdog_exhausted == 1


async def test_watchdog_does_not_touch_a_flowing_stream(tmp_path: Path) -> None:
    """Streaming responses with chunks arriving are never aborted — the
    watchdog counts SILENCE, not total duration."""
    server = await start_gateway(0)
    gport = server.sockets[0].getsockname()[1]
    log_path = tmp_path / "proxy_log.jsonl"
    proxy = FaultProxy(
        {"fake": f"http://127.0.0.1:{gport}/v1"},
        watchdog=WatchdogSpec(stall_timeout_s=0.2, retries=1),
        log_path=log_path,
    )
    base = await proxy.start()
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                f"{base}/p/fake/chat/completions",
                json={
                    "model": "fake-coder",
                    "messages": [{"role": "user", "content": "p"}],
                    "stream": True,
                },
            )
            assert r.status_code == 200
            assert "data: [DONE]" in r.text
    finally:
        await proxy.stop()
        server.close()
        await server.wait_closed()

    entries = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert all("watchdog" not in e for e in entries)
    assert proxy.stats.watchdog_triggers == 0


async def test_watchdog_midstream_abort_is_not_retryable(tmp_path: Path) -> None:
    """A stall AFTER body bytes reached the client: the status line is
    already on the wire, so no transparent retry is possible — the
    watchdog logs the abort and the client sees the truncated stream
    (the same break an unlatched `drop` produces)."""
    server = await start_gateway(0)
    gport = server.sockets[0].getsockname()[1]
    STALL_RULES["fake-coder"] = {"stall_s": 5.0, "requests": None, "mode": "mid"}
    log_path = tmp_path / "proxy_log.jsonl"
    proxy = FaultProxy(
        {"fake": f"http://127.0.0.1:{gport}/v1"},
        watchdog=WatchdogSpec(stall_timeout_s=0.3, retries=1),
        log_path=log_path,
    )
    base = await proxy.start()
    try:
        # httpx re-frames the relayed SSE as chunked; uvicorn closes the
        # connection mid-body on the abort → an incomplete chunked read
        # while the (partial) body is being consumed.
        async with (
            httpx.AsyncClient(timeout=15.0) as client,
            client.stream(
                "POST",
                f"{base}/p/fake/chat/completions",
                json={
                    "model": "fake-coder",
                    "messages": [{"role": "user", "content": "p"}],
                    "stream": True,
                },
            ) as r,
        ):
            assert r.status_code == 200
            received: list[str] = []
            with pytest.raises(httpx.RemoteProtocolError):
                async for chunk in r.aiter_text():
                    received.append(chunk)
            text = "".join(received)
            assert "chatcmpl-fixture" in text, "the first chunk did reach the client"
            assert "[DONE]" not in text, "the stream stays truncated"
    finally:
        await proxy.stop()
        server.close()
        await server.wait_closed()

    from tests.fake_gateway import _stall_seen

    assert _stall_seen["fake-coder"] == 1, "a mid-stream stall is never retried"
    entries = [json.loads(line) for line in log_path.read_text().splitlines()]
    wd = entries[0]["watchdog"]
    assert wd["saved"] is False
    assert wd["attempts"] == 1
    assert wd["events"][0]["phase"] == "mid-stream"
    assert "not retryable" in entries[0]["error"]
    assert proxy.stats.watchdog_exhausted == 1


async def test_watchdog_retry_passes_through_the_fault_stream(tmp_path: Path) -> None:
    """Determinism (§9): the watchdog retry is a real request through the
    proxy stream — it ADVANCES the fault rules' nth counters (and can
    fire one). Here the drop rule's nth=2 fires on the RETRY, before it
    reaches the upstream (the gateway never sees a second request)."""
    server = await start_gateway(0)
    gport = server.sockets[0].getsockname()[1]
    STALL_RULES["fake-coder"] = {"stall_s": 5.0, "requests": 1, "mode": "pre"}
    log_path = tmp_path / "proxy_log.jsonl"
    proxy = FaultProxy(
        {"fake": f"http://127.0.0.1:{gport}/v1"},
        (FaultSpec("drop", 2, "chat/completions"),),
        watchdog=WatchdogSpec(stall_timeout_s=0.3, retries=1),
        log_path=log_path,
    )
    base = await proxy.start()
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            with pytest.raises(httpx.RemoteProtocolError):
                await client.post(
                    f"{base}/p/fake/chat/completions",
                    json={"model": "fake-coder", "messages": [{"role": "user", "content": "p"}]},
                )
    finally:
        await proxy.stop()
        server.close()
        await server.wait_closed()

    from tests.fake_gateway import _stall_seen

    assert _stall_seen["fake-coder"] == 1, "the retry was faulted before the upstream"
    entries = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert entries[0]["fault"]["kind"] == "drop"
    assert entries[0]["fault"]["on_watchdog_retry"] is True
    wd = entries[0]["watchdog"]
    assert wd["saved"] is False
    assert wd["attempts"] == 2
    assert [ev["phase"] for ev in wd["events"]] == ["headers"]


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
    # drcode ≥ 0.5: drcode.json carries no provider fields — the proxy
    # routing lives entirely in the catalog; the project file holds only
    # the per-role refs (which must point at the same providers).
    assert "base_url" not in project
    assert set(project["models"].values()) == {
        "fake/fake-coder",
        "fake/fake-tester",
    }
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
