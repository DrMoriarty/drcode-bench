"""A minimal local OpenAI-compatible gateway for end-to-end bench runs.

Serves the `bench.run_one` pipeline with a scripted model over real
HTTP + SSE, so §5 (recording) and §10 (metrics) are validated on the
genuine streaming path of `OpenAIChatModel` — no external provider, no
network beyond localhost (plan §3: "прогон не должен зависеть от
внешней сети").

Usage:

    python tests/fake_gateway.py [port]

Served models (scripted per model id, see SCRIPTS):

- ``fake-coder``      — fixes the s1 seed bug via one `run_bash`, then ends;
- ``fake-tester``     — calls `set_verification(success=true)`, then ends;
- ``fake-compaction`` — returns a plain-text summary (no tools).

The gateway implements just enough of the OpenAI protocol for pydantic-ai:

- GET  /v1/models                  → the three model ids;
- POST /v1/chat/completions        → SSE stream (or a JSON body when the
  client does not ask for streaming), finishing with a usage chunk so the
  recorder and the transcripts carry real token usage to cross-check.
"""

from __future__ import annotations

import asyncio
import json
import sys

FIX_CMD = "printf 'def shout(text):\\n    return text.upper() + \"!\"\\n' > string_utils.py"

MODELS = ("fake-coder", "fake-tester", "fake-compaction")


def _coder_script(messages: list[dict]) -> dict:
    """Coder: one run_bash fixing the seed, then a closing text."""
    if any(m.get("role") == "tool" for m in messages):
        return {"text": "Готово: shout() исправлена, pytest зелёный."}
    return {
        "tool_calls": [
            {
                "id": "call_fix",
                "name": "run_bash",
                "arguments": json.dumps({"command": FIX_CMD}),
            }
        ]
    }


def _tester_script(messages: list[dict]) -> dict:
    """Tester: set_verification(success=true) on the first turn, then text."""
    if any(m.get("role") == "tool" for m in messages):
        return {"text": "Тесты зелёные, задача verified."}
    return {
        "tool_calls": [
            {
                "id": "call_verdict",
                "name": "set_verification",
                "arguments": json.dumps({"success": True}),
            }
        ]
    }


def _compaction_script(messages: list[dict]) -> dict:
    return {"text": "Задача: сделать shout() корректной; правка внесена, тесты зелёные."}


SCRIPTS = {
    "fake-coder": _coder_script,
    "fake-tester": _tester_script,
    "fake-compaction": _compaction_script,
}

# Fixed usage the gateway reports for every completion — small but
# non-zero, so recorder totals and transcript usage are cross-checkable.
USAGE = {"prompt_tokens": 120, "completion_tokens": 24, "total_tokens": 144}


def _sse(data: dict) -> bytes:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n".encode()


def _chat_stream(body: dict) -> bytes:
    """OpenAI-style SSE stream for one scripted completion."""
    model = body.get("model", "fake-coder")
    messages = body.get("messages", [])
    script = SCRIPTS.get(model, _coder_script)(messages)
    out = b""
    first = {"id": "chatcmpl-fixture", "object": "chat.completion.chunk", "created": 0, "model": model}
    if "text" in script:
        out += _sse(first | {"choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}}]})
        out += _sse(first | {"choices": [{"index": 0, "delta": {"content": script["text"]}}]})
        out += _sse(first | {"choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]})
    else:
        call = script["tool_calls"][0]
        out += _sse(first | {"choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}}]})
        out += _sse(
            first
            | {
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "tool_calls": [
                                {
                                    "index": 0,
                                    "id": call["id"],
                                    "type": "function",
                                    "function": {
                                        "name": call["name"],
                                        "arguments": call["arguments"],
                                    },
                                }
                            ]
                        },
                    }
                ]
            },
        )
        out += _sse(first | {"choices": [{"index": 0, "delta": {}, "finish_reason": "tool_calls"}]})
    # The usage chunk OpenAI appends when stream_options.include_usage —
    # the final usage the recorder logs for this request.
    out += _sse({"id": "chatcmpl-fixture", "object": "chat.completion.chunk", "created": 0, "model": model, "choices": [], "usage": USAGE})
    out += b"data: [DONE]\n\n"
    return out


def _chat_json(body: dict) -> bytes:
    """Non-streaming variant (a client that did not set stream=true)."""
    model = body.get("model", "fake-coder")
    messages = body.get("messages", [])
    script = SCRIPTS.get(model, _coder_script)(messages)
    message: dict = {"role": "assistant"}
    finish = "stop"
    if "text" in script:
        message["content"] = script["text"]
    else:
        call = script["tool_calls"][0]
        message["tool_calls"] = [
            {
                "id": call["id"],
                "type": "function",
                "function": {"name": call["name"], "arguments": call["arguments"]},
            }
        ]
        finish = "tool_calls"
    payload = {
        "id": "chatcmpl-fixture",
        "object": "chat.completion",
        "created": 0,
        "model": model,
        "choices": [{"index": 0, "message": message, "finish_reason": finish}],
        "usage": USAGE,
    }
    return json.dumps(payload, ensure_ascii=False).encode()


async def _handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        request_line = await reader.readline()
        headers: dict[str, str] = {}
        while True:
            line = await reader.readline()
            if line in (b"\r\n", b"\n", b""):
                break
            name, _, value = line.decode().partition(":")
            headers[name.strip().lower()] = value.strip()
        length = int(headers.get("content-length", "0"))
        body_raw = await reader.readexactly(length) if length else b""
        method, _, path = request_line.decode().partition(" ")
        path = path.split(" ")[0] if " " in path else path

        if path.endswith("/models") or path.endswith("/running"):
            payload = json.dumps({"data": [{"id": m} for m in MODELS]}).encode()
            head = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n"
        elif path.endswith("/chat/completions"):
            body = json.loads(body_raw or b"{}")
            if body.get("stream"):
                head = (
                    b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\n"
                    b"Connection: close\r\n\r\n"
                )
                writer.write(head + _chat_stream(body))
                await writer.drain()
                return
            payload = _chat_json(body)
            head = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n"
        else:
            payload = b'{"error": "not found"}'
            head = b"HTTP/1.1 404 Not Found\r\nContent-Type: application/json\r\nConnection: close\r\n"
        writer.write(
            head
            + f"Content-Length: {len(payload)}\r\n\r\n".encode()
            + payload
        )
        await writer.drain()
    except (asyncio.IncompleteReadError, ConnectionError):
        pass  # a client hangup mid-probe is not a gateway error
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except ConnectionError:
            pass


async def start(port: int = 0):
    """Start the gateway on `port` (0 = ephemeral) and return the server —
    for tests: `server = await start(); port = server.sockets[0].getsockname()[1]`."""
    return await asyncio.start_server(_handle, "127.0.0.1", port)


async def serve(port: int) -> None:
    server = await start(port)
    print(f"fake gateway on http://127.0.0.1:{server.sockets[0].getsockname()[1]}/v1", flush=True)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(serve(int(sys.argv[1]) if len(sys.argv) > 1 else 8917))
    except KeyboardInterrupt:
        pass
