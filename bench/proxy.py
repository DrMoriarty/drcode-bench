"""Fault-injecting forward proxy between the agents and the provider
(plan drcode-bench.md, §9 — the optional last stage, §12 p.6).

A local raw-ASGI HTTP proxy (served by uvicorn) sits where the provider
used to be: the generated models.json / drcode.json point every
provider's base_url at the proxy, and the proxy rewrites each request to
the real upstream, logging exact per-request timings (and, optionally,
the full request bodies) into `runs/<run_dir>/proxy_log.jsonl`.

Routing: the proxy serves ALL providers of the combo on one port — each
provider gets the synthetic base_url `<proxy>/p/<provider-name>` and the
prefix is stripped again on the way out:

    drcode → http://127.0.0.1:PORT/p/fake/v1/chat/completions
    proxy  → <fake.base_url>/v1/chat/completions

Fault injection needs NO drcode changes: the script (deterministic —
matched by the REQUEST COUNTER over the requests passing through the
proxy, optionally narrowed by a path scope) injects on the real HTTP
layer exactly what drcode's network layer must survive:

- `http_429` — an HTTP 429 response (→ pydantic-ai ModelHTTPError(429),
  retryable per drcode.tui.usage._is_retryable_network_error);
- `drop`     — a TRUNCATED response: valid headers with a declared
  Content-Length larger than the body actually sent, then the connection
  is closed (→ httpx.RemoteProtocolError → openai APIConnectionError →
  pydantic-ai ModelConnectionError, also retryable);
- `delay`    — the request is stalled `delay_s` seconds before being
  forwarded (watchdog/timeout pressure, no retry by itself).

The proxy can also replace the §5 recording wrapper when that is
inconvenient (e.g. a packaged binary run): its log carries per-request
latency and upstream status for every agent's traffic. The main mode
remains §5; when both are enabled the two latency sources are
cross-checked in metrics.json (bench.metrics.latency_cross_check).

Determinism: a fault rule fires when the number of requests matching its
scope (counted per rule, 1-based) equals `nth` — a fixed request stream
produces a fixed fault pattern, so a scenario's fault script is
reproducible. drcode's own retries are part of that stream (each retried
request passes the proxy again), which the rules' numbering accounts for.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import ssl
import time
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import httpx

from .recording import JsonlSink

SCHEMA = "proxy-faults/v1"

FAULT_KINDS = ("http_429", "drop", "delay")

# Hop-by-hop headers that must never be relayed (RFC 9110 §7.6.1) — the
# proxy re-frames the response itself (chunked via ASGI when the length
# is unknown), so framing headers from the upstream are always dropped.
_HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "content-length",  # reframed by the proxy / ASGI server
}


class ProxyError(RuntimeError):
    """The proxy cannot be started or the fault script is invalid."""


def upstream_ssl_verify() -> ssl.SSLContext | bool:
    """Trust-store-backed TLS verification for the upstream client — mirrors
    drcode.agent_model._ssl_verify. The corporate CAs drcode trusts are
    missing from certifi, so a default-verify httpx client gets
    CERTIFICATE_VERIFY_FAILED (wrapped in ConnectError → a 502 for every
    request) against the very upstreams drcode reaches fine. Without
    truststore installed, fall back to httpx defaults."""
    try:
        import truststore

        return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    except ImportError:
        return True


# --- fault script ----------------------------------------------------------------


@dataclass(frozen=True)
class FaultSpec:
    """One deterministic fault rule (§9): fires when the number of
    requests matching `scope` equals `nth` (1-based, counted per rule).

    - kind="http_429": the request is answered 429 without forwarding;
    - kind="drop":     the request is answered with a truncated body and
      the connection is closed — a transport-level break for the client;
    - kind="delay":    the request is stalled `delay_s` seconds, then
      forwarded normally.

    `scope` is a substring the request path must contain ("" = every
    request). Point it at "chat/completions" to leave the availability
    probes (GET /models etc.) out of the count.
    """

    kind: str
    nth: int
    scope: str = ""
    delay_s: float = 0.0

    def __post_init__(self) -> None:
        if self.kind not in FAULT_KINDS:
            raise ProxyError(f"fault kind {self.kind!r} not supported — use one of {FAULT_KINDS}")
        if int(self.nth) < 1:
            raise ProxyError(f"fault nth must be >= 1, got {self.nth}")
        if self.kind == "delay" and self.delay_s <= 0:
            raise ProxyError('fault kind="delay" needs delay_s > 0')

    def matches(self, path: str) -> bool:
        return self.scope in path

    def as_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"kind": self.kind, "nth": self.nth}
        if self.scope:
            out["scope"] = self.scope
        if self.kind == "delay":
            out["delay_s"] = self.delay_s
        return out


def parse_faults(raw: list[dict[str, Any]] | None) -> tuple[FaultSpec, ...]:
    """Fault rules from the scenario `[proxy]` TOML section (validated:
    a typo'd kind must fail the scenario load, not silently pass every
    request through)."""
    out = []
    for i, item in enumerate(raw or []):
        try:
            out.append(
                FaultSpec(
                    kind=str(item.get("kind", "")),
                    nth=int(item.get("nth", 0)),
                    scope=str(item.get("scope", "") or ""),
                    delay_s=float(item.get("delay_s", 0.0) or 0.0),
                )
            )
        except (TypeError, ValueError) as e:
            raise ProxyError(f"faults[{i}]: {e}") from None
    return tuple(out)


class FaultEngine:
    """The deterministic fault matcher (§9): per-rule request counters
    over the requests that pass the proxy; a rule fires on the request
    that brings its counter to `nth`.

    Not thread-safe by design: the proxy serves one run's event loop —
    ASGI requests are serialized into coroutines and the check+increment
    pair never awaits between its two steps.
    """

    def __init__(self, faults: tuple[FaultSpec, ...] = ()) -> None:
        self.faults = faults
        self._counters = [0] * len(faults)
        self.fired: list[dict[str, Any]] = []

    def inspect(self, path: str) -> FaultSpec | None:
        """The fault to inject for this request, or None. EVERY matching
        rule's counter advances on every matching request (independently
        of what fires) — the pattern depends only on the request
        sequence. When several rules fire on the same request, the first
        in script order wins."""
        fired_i: int | None = None
        for i, rule in enumerate(self.faults):
            if not rule.matches(path):
                continue
            self._counters[i] += 1
            if fired_i is None and self._counters[i] == rule.nth:
                fired_i = i
        if fired_i is None:
            return None
        rule = self.faults[fired_i]
        self.fired.append(
            {
                "kind": rule.kind,
                "nth": rule.nth,
                "scope": rule.scope,
                "path": path,
                "ts": time.time(),
            }
        )
        return rule

    def fired_summary(self) -> dict[str, int]:
        """Injected faults by kind (for result.json / metrics)."""
        out: dict[str, int] = {}
        for f in self.fired:
            out[f["kind"]] = out.get(f["kind"], 0) + 1
        return out


# --- the ASGI app ------------------------------------------------------------------


@dataclass
class ProxyStats:
    """What one proxy instance observed (→ result.json)."""

    requests: int = 0
    faults_injected: int = 0
    errors: int = 0
    started_at: float = 0.0
    stopped_at: float = 0.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "requests": self.requests,
            "faults_injected": self.faults_injected,
            "errors": self.errors,
            "uptime_s": (
                round(self.stopped_at - self.started_at, 1)
                if self.started_at and self.stopped_at
                else None
            ),
        }


class ProxyApp:
    """Raw ASGI application: prefix-routed forwarding proxy with fault
    injection and JSONL logging.

    One instance per run; the provider→upstream map comes from the
    combo's matrix providers, the fault script from the scenario. Logs
    one line per request into the sink (`runs/<run_id>/proxy_log.jsonl`,
    §10 artifacts) — including the faulted ones (no upstream contact)
    and the failed ones.
    """

    def __init__(
        self,
        upstreams: dict[str, str],
        *,
        faults: tuple[FaultSpec, ...] = (),
        log_path: Path | None = None,
        log_bodies: bool = False,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not upstreams:
            raise ProxyError("proxy needs at least one provider → upstream mapping")
        self.upstreams = dict(upstreams)
        self.engine = FaultEngine(faults)
        self.log_bodies = log_bodies
        self.stats = ProxyStats()
        self.sink = JsonlSink(log_path) if log_path else None
        self._client = client or httpx.AsyncClient(
            # Same trust store drcode uses (see upstream_ssl_verify) — a
            # CA-mismatch must not silently turn the whole run into 502s.
            verify=upstream_ssl_verify(),
            timeout=httpx.Timeout(600.0, connect=15.0),
            # The upstream is local (or trusted); do not follow redirects —
            # relay them, the client decides.
            follow_redirects=False,
        )

    # -- routing --------------------------------------------------------

    def route(self, path: str) -> tuple[str, str]:
        """`/p/<name>/<rest>` → (upstream_url, provider). ProxyError on an
        unknown provider (a config bug must be loud, not a 404 loop)."""
        parts = path.lstrip("/").split("/", 2)
        if len(parts) < 2 or parts[0] != "p" or not parts[1]:
            raise ProxyError(f"proxy path must be /p/<provider>/<rest>, got {path!r}")
        name = parts[1]
        rest = parts[2] if len(parts) > 2 else ""
        base = self.upstreams.get(name)
        if base is None:
            raise ProxyError(f"no upstream for provider {name!r} (known: {sorted(self.upstreams)})")
        url = base.rstrip("/")
        if rest:
            url = f"{url}/{rest}"
        return url, name

    # -- ASGI entry -------------------------------------------------------

    async def __call__(self, scope: dict, receive, send) -> None:
        if scope["type"] != "http":  # pragma: no cover - uvicorn http only
            return
        method = scope["method"].upper()
        path = scope["path"]
        t0 = time.monotonic()

        body = await self._read_body(receive)

        record: dict[str, Any] = {
            "ts": time.time(),
            "method": method,
            "path": path,
            "provider": None,
            "model": None,
            "status": None,
            "latency_ms": None,
            "stream": None,
            "fault": None,
            "error": None,
            "request_bytes": len(body),
        }
        if self.log_bodies:
            record["request_body"] = body.decode("utf-8", "replace")

        # Body peek: the OpenAI payload names the model — one line in the
        # log per (role-)model keeps per-model latency comparable with the
        # recorder's tags (§5). A non-JSON body (probe, garbage) is fine.
        with contextlib.suppress(json.JSONDecodeError):
            record["model"] = json.loads(body or b"{}").get("model") or None

        try:
            upstream_url, provider = self.route(path)
        except ProxyError as e:
            record.update(status=500, error=str(e), latency_ms=self._ms(t0))
            self.stats.errors += 1
            await self._send_json(send, 500, {"error": str(e)})
            self._log(record)
            return
        record["provider"] = provider

        # Fault script (§9): deterministic, per-rule counter over the
        # request stream.
        fault = self.engine.inspect(path)
        if fault is not None:
            record["fault"] = fault.as_dict()
            self.stats.faults_injected += 1
            if fault.kind == "http_429":
                record.update(status=429, latency_ms=self._ms(t0))
                await self._send_json(
                    send,
                    429,
                    {
                        "error": {
                            "message": "rate limited by fault injection",
                            "type": "bench_fault_injection",
                        }
                    },
                    extra_headers=[(b"retry-after", b"1")],
                )
                self._log(record)
                return
            if fault.kind == "drop":
                # Truncated response: headers promise more than is sent,
                # then the connection dies — a transport break for the
                # client (APIConnectionError), not an HTTP error status.
                record.update(
                    status=200,
                    error="connection dropped by fault injection",
                    latency_ms=self._ms(t0),
                )
                self.stats.errors += 1
                await self._send_truncated(send)
                self._log(record)
                return
            if fault.kind == "delay":
                record["fault"] = fault.as_dict() | {"delayed_s": fault.delay_s}
                await asyncio.sleep(fault.delay_s)
                # fall through to the normal forwarding

        await self._forward(scope, method, upstream_url, body, record, send, t0)

    # -- forwarding -------------------------------------------------------

    async def _forward(
        self,
        scope: dict,
        method: str,
        upstream_url: str,
        body: bytes,
        record: dict[str, Any],
        send,
        t0: float,
    ) -> None:
        headers = self._upstream_headers(scope)
        req = self._client.build_request(
            method, upstream_url, content=body or None, headers=headers
        )
        try:
            resp = await self._client.send(req, stream=True)
        except httpx.HTTPError as e:
            # Upstream transport failure is logged and surfaced as 502 —
            # a fault script produces drops, an unreachable upstream is
            # an infrastructure problem the run must SEE as one.
            record.update(
                status=502, error=f"upstream {type(e).__name__}: {e}", latency_ms=self._ms(t0)
            )
            self.stats.errors += 1
            await self._send_json(send, 502, {"error": f"upstream unreachable: {e}"})
            self._log(record)
            return

        resp_headers = [
            (k.lower().encode("latin-1"), v.encode("latin-1"))
            for k, v in resp.headers.items()
            if k.lower() not in _HOP_BY_HOP
        ]
        stream = "text/event-stream" in resp.headers.get("content-type", "")
        record["status"] = resp.status_code
        record["stream"] = stream
        await send(
            {
                "type": "http.response.start",
                "status": resp.status_code,
                "headers": resp_headers,
            }
        )
        sent = 0
        try:
            async for chunk in resp.aiter_raw():
                sent += len(chunk)
                await send({"type": "http.response.body", "body": chunk, "more_body": True})
            await send({"type": "http.response.body", "body": b"", "more_body": False})
        except httpx.HTTPError as e:
            # Died mid-relay: the client sees a truncated response (the
            # same break a `drop` fault produces) — log and give up; the
            # ASGI connection is closed by uvicorn on the early return.
            record["error"] = f"relay interrupted: {type(e).__name__}: {e}"
            self.stats.errors += 1
        finally:
            await resp.aclose()
        record["latency_ms"] = self._ms(t0)
        record["response_bytes"] = sent
        self._log(record)

    # -- helpers ----------------------------------------------------------

    @staticmethod
    def _ms(t0: float) -> int:
        return int((time.monotonic() - t0) * 1000)

    @staticmethod
    async def _read_body(receive) -> bytes:
        chunks = []
        while True:
            msg = await receive()
            if msg["type"] == "http.request":
                chunks.append(msg.get("body", b""))
                if not msg.get("more_body"):
                    break
            elif msg["type"] == "http.disconnect":  # pragma: no cover
                raise asyncio.CancelledError("client disconnected mid-request")
        return b"".join(chunks)

    @staticmethod
    def _upstream_headers(scope: dict) -> dict[str, str]:
        """Relayed request headers minus hop-by-hop and the Host header
        (httpx sets it from the upstream URL)."""
        out = {}
        for k, v in scope.get("headers") or []:
            name = k.decode("latin-1").lower()
            if name in _HOP_BY_HOP or name == "host":
                continue
            out[name] = v.decode("latin-1")
        return out

    @staticmethod
    async def _send_json(
        send, status: int, payload: dict, extra_headers: list[tuple[bytes, bytes]] | None = None
    ) -> None:
        body = json.dumps(payload).encode()
        headers = [
            (b"content-type", b"application/json"),
            (b"content-length", str(len(body)).encode()),
            *(extra_headers or []),
        ]
        await send({"type": "http.response.start", "status": status, "headers": headers})
        await send({"type": "http.response.body", "body": body})

    @staticmethod
    async def _send_truncated(send) -> None:
        """Headers with a Content-Length far beyond the body actually
        sent, then EOF: the client's HTTP stack raises an incomplete-read
        error → a connection-level failure, exactly the `drop` semantics
        of §9."""
        partial = b'{"error": {"message": "tr'
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"content-length", b"9999"),
                ],
            }
        )
        await send({"type": "http.response.body", "body": partial, "more_body": True})
        # No final body event: uvicorn closes the connection with the
        # declared length unmet — the client sees a truncated response.

    def _log(self, record: dict[str, Any]) -> None:
        self.stats.requests += 1
        if self.sink is not None:
            self.sink.write(record)

    async def aclose(self) -> None:
        await self._client.aclose()


# --- server lifecycle ---------------------------------------------------------


class FaultProxy:
    """Lifecycle wrapper: starts the ASGI app on an ephemeral port inside
    the CALLER'S event loop (uvicorn.Server task) and reports the base
    URL the generated catalog must point at (§3/§9)."""

    def __init__(
        self,
        upstreams: dict[str, str],
        faults: tuple[FaultSpec, ...] = (),
        *,
        log_path: Path | None = None,
        log_bodies: bool = False,
    ) -> None:
        self.app = ProxyApp(upstreams, faults=faults, log_path=log_path, log_bodies=log_bodies)
        self.base_url: str | None = None
        self._server: Any = None
        self._task: asyncio.Task | None = None

    async def start(self) -> str:
        import uvicorn

        await self._preflight_upstreams()
        config = uvicorn.Config(
            self.app,
            host="127.0.0.1",
            port=0,  # ephemeral: no collisions between parallel runs
            log_level="warning",
            access_log=False,
            lifespan="off",
        )
        self._server = uvicorn.Server(config)
        self._task = asyncio.create_task(self._server.serve(), name="bench-proxy")
        for _ in range(200):  # ~2 s to bind — the loop is already running
            if self._server.started:
                break
            await asyncio.sleep(0.01)
        if not self._server.started:
            raise ProxyError("proxy server did not start within 2 s")
        sock = self._server.servers[0].sockets[0]
        port = sock.getsockname()[1]
        self.base_url = f"http://127.0.0.1:{port}"
        self.app.stats.started_at = time.time()
        return self.base_url

    async def _preflight_upstreams(self) -> None:
        """Fail the run loudly (ProxyError at prep time) when the proxy
        cannot establish TLS to a real upstream. A trust-store mismatch used
        to surface only as 502s in proxy_log.jsonl and cost a full scenario
        timeout (s7 run 20261023-145721). Only certificate failures are
        fatal here — any other connect problem still shows up per-request
        as a 502 the run can report."""
        for name, base in self.app.upstreams.items():
            try:
                # Any HTTP answer (even 404/401) proves the TLS layer works.
                await self.app._client.get(base, timeout=10.0)
            except httpx.ConnectError as e:
                # Detection by exception type, not message: the truststore
                # backend localizes the message (e.g. Russian macOS text).
                cur: BaseException | None = e
                while cur is not None:
                    if isinstance(cur, ssl.SSLCertVerificationError):
                        raise ProxyError(
                            f"proxy → upstream TLS failure for provider {name!r} ({base}): "
                            f"{e} — trust-store mismatch; install truststore or add the "
                            "corporate CA to the certifi bundle"
                        ) from e
                    cur = cur.__cause__ or cur.__context__

    async def stop(self) -> None:
        if self._server is not None:
            self._server.should_exit = True
        if self._task is not None:
            try:
                await asyncio.wait_for(self._task, timeout=10.0)
            except (TimeoutError, asyncio.CancelledError):
                self._task.cancel()
            except Exception:
                pass  # the run's own result (we are in a finally block)
            self._task = None
        self.app.stats.stopped_at = time.time()
        with contextlib.suppress(Exception):
            await self.app.aclose()

    @property
    def stats(self) -> ProxyStats:
        return self.app.stats

    @property
    def engine(self) -> FaultEngine:
        return self.app.engine


def upstreams_for_providers(providers: dict[str, Any]) -> dict[str, str]:
    """provider name → REAL base_url, from the combo's matrix providers
    (the ones actually referenced — see env_setup._providers_for_combo)."""
    return {name: spec.base_url for name, spec in providers.items()}


def apply_proxy_base(providers: dict[str, Any], proxy_base: str) -> dict[str, Any]:
    """Rewrite every provider's base_url to `<proxy_base>/p/<name>` — the
    catalog/flat-config layer the run sees (§3: the generated models.json
    points at the proxy; the real endpoints stay in the matrix file).

    Works on `bench.matrix.ProviderSpec` values (frozen dataclasses are
    replaced, not mutated)."""
    out = {}
    for name, spec in providers.items():
        out[name] = replace(spec, base_url=f"{proxy_base.rstrip('/')}/p/{name}")
    return out
