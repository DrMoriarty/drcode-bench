"""Recording wrapper around `agent_model.build_model` (plan drcode-bench.md, §5).

Per-request wall-time and usage of the compaction agent are nowhere on
drcode's disk (§1.5) — the task transcripts keep only the
coder/tester `ModelResponse.usage`, and nothing at all about latency.
The recorder closes that hole WITHOUT touching drcode sources: it
monkeypatches `drcode.agent_model.build_model` in the benchmark process
and wraps every built model, so each real HTTP request to a model is
logged as one JSONL line into `runs/<run_id>/model_log.jsonl`:

    {"role": "qwen3-coder-30b@http://localhost:8080/v1",
     "model_name": "qwen3-coder-30b", "streamed": true,
     "latency_ms": 4210, "n_history": 17,
     "usage": {"input_tokens": 8123, "output_tokens": 210,
               "cache_read_tokens": 0, "cache_write_tokens": 0},
     "ts": 1730000000.123}

`build_model` is called separately per agent (coder, tester,
compaction agent) with the ALREADY-RESOLVED config of the role, so the
tag `f"{config.model}@{config.base_url}"` identifies the agent by its
model selection.

ROLE-IDENTIFICATION LIMITATION (§5): when the SAME model+base_url is
assigned to several roles (the "baseline-single-model" combo, or the
common tester == compaction pairing), the tag is identical for those
roles and the log alone cannot separate coder from tester traffic.
Both would have to be told apart by build-call order (fragile) or by
threading the call site through drcode (a source edit — out of scope).
For matrix combinations with a DISTINCT model per role the tag is
sufficient, and per-request disambiguation inside one run is always
possible via the usage cross-check against the task transcripts
(bench.metrics.cross_check_usage). This is a documented limitation of
the observation tool, not a bug.

STREAMING INVARIANT (§13): `request_stream` stays a real streaming
async context manager yielding the inner StreamedResponse untouched —
the TUI and the watchdog consume deltas, and substituting a
non-streaming request would distort both the timings measured here and
the observed behavior (time-to-first-token, cancellation paths). The
log line for a streamed request is written when the consumer leaves
the stream context (the point where the response — and its final
usage — is complete).

Install once per run, BEFORE the app builds its agents:

    from bench.recording import install_recorder
    install_recorder(run_dir / "model_log.jsonl")
"""

from __future__ import annotations

import json
import threading
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

# The usage keys of the serialized transcripts (bench.metrics.EMPTY_USAGE):
# one vocabulary on both sides of the cross-check. pydantic-ai normalizes
# usage from all providers, so input_tokens already INCLUDES cache
# reads/writes (they must not be added on top — see drcode.transcript).
USAGE_KEYS = ("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens")


def usage_dict(response: Any) -> dict[str, int] | None:
    """Normalized token usage of a ModelResponse / StreamedResponse.

    Handles both shapes of the pydantic-ai API: `response.usage` as a
    field (2.x, a RequestUsage) and as a method (legacy `usage()`).
    None when the response carries no measurable usage (a failed or
    cancelled request) — empty usage must not pollute token sums.
    """
    usage = getattr(response, "usage", None)
    if usage is None:
        return None
    if callable(usage):
        try:
            usage = usage()
        except Exception:
            return None
    out = {key: int(getattr(usage, key, 0) or 0) for key in USAGE_KEYS}
    return out if any(out.values()) else None


class JsonlSink:
    """Append-only JSONL writer, one line per record, process-safe
    against interleaved coroutines via a lock. The file is opened per
    record: negligible at model-request volume, and immune to a crashed
    run leaving a truncated buffer behind."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self._lock = threading.Lock()
        self._n_records = 0

    def write(self, record: dict[str, Any]) -> None:
        line = json.dumps(record, ensure_ascii=False)
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
            self._n_records += 1

    @property
    def n_records(self) -> int:
        return self._n_records


class RecordingModel:
    """Delegating wrapper around a pydantic-ai Model that logs every
    request (§5). Only `request` and `request_stream` are overridden;
    everything else (`model_name`, `base_url`, `profile`, `provider`,
    `system`, `customize_request_parameters`, …) reaches the inner
    model through `__getattr__`, so the wrapper satisfies whatever the
    `pydantic_ai.models.Model` interface — or drcode's pipeline — asks
    of it, including the `_ensure_model_supports_streaming` type-level
    check (our own `request_stream` is defined, the base class's is
    not)."""

    def __init__(self, inner: Any, role_tag: str, sink: JsonlSink) -> None:
        object.__setattr__(self, "_inner", inner)
        object.__setattr__(self, "_role_tag", role_tag)
        object.__setattr__(self, "_sink", sink)

    # -- delegation -----------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        # Only reached for names NOT found normally: forward to the
        # inner model. The explicit __dict__ lookup avoids infinite
        # recursion when the wrapper is not fully initialized yet.
        inner = object.__getattribute__(self, "__dict__").get("_inner")
        if inner is None:
            raise AttributeError(name)
        return getattr(inner, name)

    # -- logging --------------------------------------------------------

    def _log(
        self,
        messages: list[Any],
        t0: float,
        *,
        streamed: bool,
        response: Any = None,
        error: str | None = None,
    ) -> None:
        record: dict[str, Any] = {
            "role": object.__getattribute__(self, "_role_tag"),
            "model_name": getattr(object.__getattribute__(self, "_inner"), "model_name", None),
            "streamed": streamed,
            "latency_ms": int((time.monotonic() - t0) * 1000),
            "n_history": len(messages),
            "usage": usage_dict(response) if response is not None else None,
            "ts": time.time(),
        }
        if error is not None:
            record["error"] = error
        object.__getattribute__(self, "_sink").write(record)

    # -- the two overridden entry points --------------------------------

    async def request(
        self, messages: list[Any], model_settings: Any, model_request_parameters: Any
    ) -> Any:
        """Non-streaming request (pydantic-ai 2.x signature: the request
        carries its resolved ModelRequestParameters, not the legacy
        tools list). One completed HTTP request = one log line."""
        t0 = time.monotonic()
        try:
            resp = await object.__getattribute__(self, "_inner").request(
                messages, model_settings, model_request_parameters
            )
        except BaseException as e:
            self._log(messages, t0, streamed=False, error=f"{type(e).__name__}: {e}")
            raise
        self._log(messages, t0, streamed=False, response=resp)
        return resp

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[Any],
        model_settings: Any,
        model_request_parameters: Any,
        run_context: Any = None,
    ) -> AsyncIterator[Any]:
        """Streaming request, KEPT STREAMING (§5/§13): the inner
        StreamedResponse is yielded untouched — the TUI consumes deltas
        and the watchdog depends on them. The record lands when the
        consumer leaves the stream context: then, and only then, is the
        usage final (it arrives with the last SSE chunk)."""
        t0 = time.monotonic()
        inner = object.__getattribute__(self, "_inner")
        async with inner.request_stream(
            messages, model_settings, model_request_parameters, run_context
        ) as stream:
            try:
                yield stream
            except BaseException as e:
                self._log(messages, t0, streamed=True, error=f"{type(e).__name__}: {e}")
                raise
        self._log(messages, t0, streamed=True, response=stream)


# `pydantic_ai.models.Model` is an ABC and the agent machinery does
# `isinstance(model, Model)` (infer_model) — register the wrapper as a
# virtual subclass so a wrapped model passes everywhere a Model is
# expected, without subclassing (subclassing would pin the interface of
# one pydantic-ai version).
try:  # pragma: no cover - trivial registration
    from pydantic_ai.models import Model as _PydanticModel

    _PydanticModel.register(RecordingModel)
except ImportError:  # pragma: no cover - bench always ships with pydantic-ai
    pass


def install_recorder(log_path: Path) -> list[str]:
    """Monkeypatch `drcode.agent_model.build_model` so every model it
    builds is wrapped in a RecordingModel logging to `log_path`.

    This is an observation instrument of the benchmark process, not an
    edit of drcode sources (§2/§5): drcode keeps calling
    `agent_model.build_model(config)` unchanged — coder, tester and
    compaction agents each get their own call with their own resolved
    config, and each wrapped model carries the tag
    `f"{config.model}@{config.base_url}"`.

    Returns the list of role tags seen at install time (empty — the
    tags accumulate as the app builds its agents).
    """
    from drcode import agent_model  # imported here: after env sanitization

    sink = JsonlSink(log_path)
    original = agent_model.build_model

    def patched(config: Any):
        inner = original(config)
        tag = f"{config.model}@{config.base_url}"
        return RecordingModel(inner, tag, sink)

    agent_model.build_model = patched
    return []
