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
- ``fake-compaction`` — returns a plain-text summary (no tools);
- ``s2a-coder`` / ``s2a-tester`` — the S2a loop: the coder fixes only the
  in-scope function, the tester fails the first round and files a bug
  report, the follow-up/bug prompt triggers the full fix;
- ``s2b-coder`` / ``s2b-tester`` — the S2b loop: the coder fixes div /
  implements export_api / fixes the bug-report task, the tester fails the
  first round and files the bug report (queue priority is exercised);
- ``s5-coder`` / ``s5-tester`` — the S5 round-trip: the coder asks the
  clarifying question instead of guessing and implements from the answer;
  the tester imports the module and stamps PASSED;
- ``s3-coder`` — the S3 loop: reads glossary modules one by one, then
  fixes kappa.WEIGHT (the reported usage is inflated per request, so
  drcode's mid-run compaction gate really trips);
- ``s4-coder`` — the S4 coder: fixes report.py in one run_bash;
- ``s4-tester`` — the S4 tester: reads the 4.5k-line listing in whole
  100-line `sed -n 'A,Bp'` chunks (inflated usage → mid-round tester
  compaction; resumes from the summary's read-through marker), then
  stamps PASSED;
- ``s8-coder`` / ``s8-tester`` — the S8 fix loop: the coder's round-1
  edit of pad() breaks the dependent test_row by design, the tester
  stamps set_verification(success=False, retry_here=True), the report
  requeues the task into development, round 2 repairs the regression
  and the tester stamps PASSED;
- ``fake-research`` — the optional 4th combo role: a research model with
  its own transcript (plain analysis text, no tools). The e2e combos
  assign it so the whole 4th-role plumbing (matrix → drcode.json
  "research" key → pre-flight → drcode's own role selection) runs for
  real; scenarios never queue kind=research briefs (plan §7), so the
  script fires only if the pipeline ever routes research work its way.
- ``s9-research`` — the S9 scripted research agent: computes the metric
  from seed/data/orders.csv with run_bash (python one-liner — a
  legitimate tool use, the brief leaves the path free), writes
  docs/report.md with write_file ("total: <number>" — the pinned format
  checks.py parses) and commits it via git_commit_docs (the research.md
  mandate for documentation assignments — s9 MEASURES that discipline as
  the `S9 metric: report_committed=` line instead of gating on it).
- ``s10-research`` — the S10 scripted research agent (variant V2):
  enumerates the seed with glob_files, then ONE grep_search over the
  alternation of the three planted-fact identifiers (orphan constant,
  duplicated "def balance", the deprecated flag), composes
  docs/findings.md FROM THE GREP OUTPUT ITSELF (paths and symbols are
  parsed out of the tool results — nothing about the facts is
  hardcoded in the script; a drifted seed produces a findings.md that
  checks.py rejects) and commits it via git_commit_docs.
- ``s11-research`` — the S11 scripted research agent (variant V3): ONE
  grep_search over the '@route(...' / '^def ' alternation, pairing
  each @route("METHOD /path") entry with the def entry that follows it
  (the seed's decorator-over-def contract), renders the markdown table
  (method | path | handler) in docs/routes.md FROM THE GREP OUTPUT
  ITSELF and commits it via git_commit_docs.
- ``s12-agent`` / ``s12-tester`` — the S12 loop (research variant V4):
  ONE model id serves BOTH the research and the coding role (the S2b
  precedent of alternating transcripts on one model). The research
  transcript reads dispatch/pricing.py, files the ONE bug report via
  create_bug_report (the brief's explicit authorization) with the
  description composed FROM THE READ OUTPUT ITSELF (the defective
  function name and the docstring example are parsed out of the tool
  result — a drifted seed produces a report that checks.py rejects);
  the spawned kind=bug task comes back to the SAME model id as the
  coding transcript (its prompt is the report's description, which
  names the function) and fixes the defect with one targeted run_bash;
  the tester runs full pytest and stamps PASSED.
- ``s13-agent`` / ``s13-tester`` — the S13 loop (research variant V5,
  the compound research → planning → coding → testing chain): ONE model
  id serves BOTH the research and the coding role (the S12 precedent).
  The research transcript greps the deprecated ``math.floor`` token
  across the telemetry package, files the ONE feature request via
  create_feature_request (the brief's explicit authorization) with the
  description composed FROM THE GREP OUTPUT ITSELF (the change-site
  paths are parsed out of the tool result — a drifted seed produces a
  partial plan that checks.py rejects); the spawned kind=feature task
  comes back to the SAME model id as the coding transcript (its prompt
  is the request description, whose bullet list names every site) and
  replaces the deprecated pattern in every listed file with one
  targeted run_bash; the tester runs full pytest and stamps PASSED.

The gateway implements just enough of the OpenAI protocol for pydantic-ai:

- GET  /v1/models                  → the scripted model ids;
- POST /v1/chat/completions        → SSE stream (or a JSON body when the
  client does not ask for streaming), finishing with a usage chunk so the
  recorder and the transcripts carry real token usage to cross-check.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import re
import sys

FIX_CMD = "printf 'def shout(text):\\n    return text.upper() + \"!\"\\n' > string_utils.py"

MODELS = (
    "fake-coder",
    "fake-tester",
    "fake-compaction",
    "fake-research",
    "s2a-coder",
    "s2a-tester",
    "s2b-coder",
    "s2b-tester",
    "s5-coder",
    "s5-tester",
    "s3-coder",
    "s4-coder",
    "s4-tester",
    "s7-coder",
    "s7-tester",
    "s8-coder",
    "s8-tester",
    "s9-research",
    "s10-research",
    "s11-research",
    "s12-agent",
    "s12-tester",
    "s13-agent",
    "s13-tester",
)


# -- stall rules for the §9 stall-watchdog tests (bench/proxy.py) -----------------
# A rule makes /chat/completions requests for one model go SILENT — no bytes —
# for `stall_s` seconds, either before anything is written (mode="pre": the
# proxy's watchdog aborts during the header wait) or after the response head
# and the first body piece (mode="mid": the watchdog aborts mid-relay).
# `requests` limits how many requests the rule applies to (None = every one),
# counted per model: a {"requests": 1, "stall_s": 5} rule stalls the FIRST
# request only, so a proxy-side watchdog retry arrives at an instantly
# responding upstream. The sleeping handler polls the socket every 50 ms and
# gives up as soon as the client (the aborting proxy) disconnects.
STALL_RULES: dict[str, dict] = {}
_stall_seen: dict[str, int] = {}


def clear_stall_rules() -> None:
    """Reset the module-level stall state (tests start a fresh gateway
    per case, but the module dict outlives individual servers)."""
    STALL_RULES.clear()
    _stall_seen.clear()


def _stall_rule_for(model: str) -> dict | None:
    """The stall rule for this request (the request is counted even when
    its rule's `requests` budget is already spent), or None."""
    rule = STALL_RULES.get(model)
    if rule is None:
        return None
    _stall_seen[model] = _stall_seen.get(model, 0) + 1
    limit = rule.get("requests")
    if limit is not None and _stall_seen[model] > int(limit):
        return None
    return rule


async def _stall_silence(seconds: float, writer: asyncio.StreamWriter) -> bool:
    """Stay silent for `seconds`; True = the client disconnected meanwhile
    (the proxy's watchdog abort closed the socket) — give up."""
    deadline = asyncio.get_event_loop().time() + seconds
    while asyncio.get_event_loop().time() < deadline:
        await asyncio.sleep(0.05)
        if writer.is_closing():
            return True
    return writer.is_closing()


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
    """Summary for any compaction role. For the S4 tester's listing reads
    the summary embeds a 'read-through-line=NNNN' marker: the rendered
    history shows the tool results (blocks '[tool result for run_bash]'),
    and the marker records the last listing line they showed — the S4
    tester resumes reading from it (the marker survives the map-reduce
    form too: reduce sees the markers inside the map summaries). The
    marker is parsed ONLY from tool-result blocks, never from the whole
    request: the brief quotes the file's last line ('entry 004500…'), and
    a whole-text scan would always read progress 4500 from the quote."""
    request_text = json.dumps(messages, ensure_ascii=False)
    best = 0
    for match in re.finditer(r"read-through-line=(\d+)", request_text):
        best = max(best, int(match.group(1)))
    for segment in request_text.split("[tool result for run_bash]")[1:]:
        for match in re.finditer(r"entry (\d{6}):", segment.split("\\n\\n[")[0]):
            best = max(best, int(match.group(1)))
    if best:
        return {
            "text": (
                "Задача: починить format_report (разделитель записей); правка "
                f"внесена. Листинг data/listing.txt прочитан по строку {best} "
                f"из 4500 включительно (read-through-line={best}); чтение "
                "продолжить со следующей строки."
            )
        }
    return {"text": "Задача: сделать shout() корректной; правка внесена, тесты зелёные."}


def _research_script(messages: list[dict]) -> dict:
    """Research role (optional 4th combo role): a plain-text analysis —
    the research load profile reads and summarizes, no tools, no code
    edits; deliberately DISTINCT from _coder_script so a research
    transcript is recognizable in model_log/metrics as its own model."""
    return {
        "text": (
            "Анализ: изменение затрагивает shout() в string_utils.py; "
            "существующие вызовы совместимы, риск регрессии минимальный."
        )
    }


# -- helpers for the scenario scripts -------------------------------------------


def _last_user_prompt(messages: list[dict]) -> str:
    """Content of the LAST user message (the current prompt of the run)."""
    for m in reversed(messages):
        if m.get("role") == "user":
            return str(m.get("content") or "")
    return ""


def _after_own_tool_call(messages: list[dict]) -> bool:
    """True when the LAST message is a tool result — i.e. this request is
    the continuation right after the tool call THIS script just made, so
    the only thing left is to end the turn with a text. (Checking `any`
    tool message instead would misfire on the history of later rounds:
    earlier rounds legitimately keep their tool calls in the transcript.)"""
    return bool(messages) and messages[-1].get("role") == "tool"


def _called(messages: list[dict], tool_name: str) -> bool:
    """True when the assistant already called `tool_name` in this run."""
    return any(
        (tc.get("function") or {}).get("name") == tool_name
        for m in messages
        if m.get("role") == "assistant"
        for tc in (m.get("tool_calls") or [])
    )


def _last_tool_output(messages: list[dict]) -> str:
    for m in reversed(messages):
        if m.get("role") == "tool":
            return str(m.get("content") or "")
    return ""


def _last_bash_output(messages: list[dict]) -> str:
    """Output of the LAST run_bash tool call. Tool results carry no tool
    name, but run_bash always prefixes its output with 'exit=N' while
    verdict/bug-report tools don't — so the prefix filter survives any
    number of set_verification/create_bug_report calls made after the
    pytest run (deciding green/red from _last_tool_output alone would
    misread 'Verification label set: …' as a red pytest and loop on
    create_bug_report forever)."""
    for m in reversed(messages):
        if m.get("role") == "tool":
            content = str(m.get("content") or "")
            if content.startswith("exit="):
                return content
    return ""


def _call(tool_name: str, args: dict, call_id: str = "call_1") -> dict:
    return {
        "tool_calls": [
            {
                "id": call_id,
                "name": tool_name,
                "arguments": json.dumps(args, ensure_ascii=False),
            }
        ]
    }


def _run_bash(command: str, call_id: str = "call_bash") -> dict:
    return _call("run_bash", {"command": command}, call_id)


def _bash_end_run(text: str = "Готово.") -> dict:
    return {"text": text}


# -- S2a: seeded bug → FAILED → follow-up → full fix -----------------------------

# calc.py with ONLY div() fixed (the in-scope part of the first brief).
S2A_FIX_DIV = (
    "printf 'def div(a, b):\\n"
    "    if b == 0:\\n"
    '        raise ValueError("zero divisor")\\n'
    "    return a / b\\n"
    "\\n"
    "def pct(a, b):\\n"
    "    return a / b\\n"
    "' > calc.py"
)
# calc.py fully fixed: the follow-up extends the scope to pct().
S2A_FIX_ALL = (
    "printf 'def div(a, b):\\n"
    "    if b == 0:\\n"
    '        raise ValueError("zero divisor")\\n'
    "    return a / b\\n"
    "\\n"
    "def pct(a, b):\\n"
    "    return a / b * 100\\n"
    "' > calc.py"
)


def _s2a_coder_script(messages: list[dict]) -> dict:
    if _after_own_tool_call(messages):
        return _bash_end_run("Правка внесена.")
    prompt = _last_user_prompt(messages)
    # The follow-up (FAILED + лог ошибки) and the tester's bug-report
    # description both extend the scope to pct(); both fixes are
    # idempotent, so the order of the two tasks does not matter.
    if "FAILED" in prompt or "test_pct" in prompt:
        return _run_bash(S2A_FIX_ALL, "call_fix_all")
    return _run_bash(S2A_FIX_DIV, "call_fix_div")


def _bugfix_tester_script(messages: list[dict]) -> dict:
    """Tester for S2a/S2b: run pytest; on red — set_verification(False,
    retry_here=False) then create_bug_report (the tester.md order); on
    green — PASSED. retry_here=False is semantic, not a workaround
    (drcode ≥ 0.5.0 defaults a bare success=False to retry_here=True,
    which requeues the task into its own dev loop instead of finalizing
    FAILED): the red test_pct is NOT caused by this task's changes (the
    coder only touched div), so the failure belongs to the user — the
    finalizing verdict that the scenario's verification_failed follow-up
    waits for."""
    if not any(m.get("role") == "tool" for m in messages):
        return _run_bash("python3 -m pytest -q", "call_pytest")
    out = _last_bash_output(messages)
    # run_bash prefixes its output with "exit=N"; anything but a green
    # exit=0 (pytest summary "N failed") is a failed check.
    if " failed" in out or not out.startswith("exit=0"):
        if not _called(messages, "set_verification"):
            return _call(
                "set_verification",
                {"success": False, "retry_here": False},
                "call_verdict",
            )
        if not _called(messages, "create_bug_report"):
            return _call(
                "create_bug_report",
                {
                    "title": "Починить pct(): test_pct падает",
                    "description": (
                        "Лог ошибки: python -m pytest -q завершается с exit=1 — "
                        "падает test_pct (pct(50, 200) вернула 0.25, ожидалось 25.0). "
                        "Исправьте pct() в calc.py, чтобы полный pytest был зелёным."
                    ),
                },
                "call_bug",
            )
        return _bash_end_run("Задача помечена FAILED, bug-report создан.")
    if not _called(messages, "set_verification"):
        return _call("set_verification", {"success": True}, "call_verdict")
    return _bash_end_run("Тесты зелёные, задача verified.")


def _s2b_tester_script(messages: list[dict]) -> dict:
    """Tester for S2b: full pytest, but the seed's out-of-scope failures
    (pct() broken, export_api() not implemented — other tasks' scope, see
    the first brief's ТЕСТИРОВЩИКУ clause) must NOT fail this task: the
    FIRST brief's tester files ONE bug report via create_bug_report and
    stamps PASSED; the bug task's own tester passes once its in-scope
    part (pct) is fixed — the remaining red is export_api, the second
    brief's scope. The bug task is told so in its description (the only
    prompt difference from the first brief). Deciding green/red from the
    last run_bash output keeps the verdict stable after set_verification."""
    if not any(m.get("role") == "tool" for m in messages):
        return _run_bash("python3 -m pytest -q", "call_pytest")
    out = _last_bash_output(messages)
    green = out.startswith("exit=0") and " failed" not in out
    first_brief = "Исправьте ТОЛЬКО div()" in _last_user_prompt(messages)
    if green or not first_brief:
        # Green suite — or every red is outside THIS task's scope.
        if not _called(messages, "set_verification"):
            return _call("set_verification", {"success": True}, "call_verdict")
        return _bash_end_run("Проверки в объёме задачи зелёные, задача verified.")
    # First brief, red suite: file the ONE bug report, then stamp PASSED.
    if not _called(messages, "create_bug_report"):
        return _call(
            "create_bug_report",
            {
                "title": "Починить pct(): test_pct падает",
                "description": (
                    "Лог ошибки: python -m pytest -q завершается с exit=1 — "
                    "падает test_pct (pct(50, 200) вернула 0.25, ожидалось 25.0). "
                    "Исправьте pct() в calc.py, чтобы полный pytest был зелёным. "
                    "ТЕСТИРОВЩИКУ: если pytest красный только из-за export_api() "
                    "(ещё не реализована, вне объёма) — set_verification(True)."
                ),
            },
            "call_bug",
        )
    if not _called(messages, "set_verification"):
        return _call("set_verification", {"success": True}, "call_verdict")
    return _bash_end_run("Bug-report создан, задача verified.")


# -- S2b coder scripts (see _s2b_tester_script for the tester side) --------------

# calc.py: div fixed (the first brief's scope).
S2B_FIX_DIV = S2A_FIX_DIV
# calc.py: the bug report's scope — pct() fixed on top of div().
S2B_FIX_PCT = S2A_FIX_ALL
# calc.py: the second brief — export_api() on top of the fully fixed file.
S2B_WRITE_FINAL = (
    "printf 'def div(a, b):\\n"
    "    if b == 0:\\n"
    '        raise ValueError("zero divisor")\\n'
    "    return a / b\\n"
    "\\n"
    "def pct(a, b):\\n"
    "    return a / b * 100\\n"
    "\\n"
    "def export_api():\\n"
    '    return ["div", "pct"]\\n'
    "' > calc.py"
)


def _s2b_coder_script(messages: list[dict]) -> dict:
    if _after_own_tool_call(messages):
        return _bash_end_run("Правка внесена.")
    prompt = _last_user_prompt(messages)
    if "функцию export_api" in prompt:
        return _run_bash(S2B_WRITE_FINAL, "call_export")
    if "test_pct" in prompt or "FAILED" in prompt:
        return _run_bash(S2B_FIX_PCT, "call_fix_pct")
    return _run_bash(S2B_FIX_DIV, "call_fix_div")


# -- S5: clarification round-trip -------------------------------------------------

# prices.py implementing the standard the simulator's answer states.
S5_IMPLEMENT = (
    'printf \'def format_price(amount, currency="RUB"):\\n'
    '    symbol = "₽" if currency == "RUB" else currency\\n'
    '    body = f"{amount:,.2f}"\\n'
    '    body = body.replace(",", " ").replace(".", ",")\\n'
    '    return f"{body} {symbol}"\\n'
    "' > prices.py"
)


def _s5_coder_script(messages: list[dict]) -> dict:
    if _after_own_tool_call(messages):
        return _bash_end_run("Реализовано по стандарту из ответа.")
    prompt = _last_user_prompt(messages)
    if "Стандарт оформления цен" in prompt and not _called(messages, "run_bash"):
        return _run_bash(S5_IMPLEMENT, "call_impl")
    if "Стандарт оформления цен" in prompt:
        return _bash_end_run("Реализовано по стандарту из ответа.")
    return _call(
        "ask_clarifying_question",
        {
            "question": (
                "Какой именно стандарт оформления цен использовать? "
                "Формат (разделители, знаки, символ валюты) в репозитории не описан."
            ),
            "options": [],
        },
        "call_ask",
    )


def _s5_tester_script(messages: list[dict]) -> dict:
    """Tester for S5: no tests in the seed — run the module as the build
    check and stamp PASSED (tester.md: no tests → try to build/import)."""
    if _called(messages, "set_verification"):
        return _bash_end_run("Модуль импортируется, задача verified.")
    if not any(m.get("role") == "tool" for m in messages):
        return _run_bash(
            'python3 -c "import prices; print(prices.format_price(1234.5))"',
            "call_import",
        )
    return _call("set_verification", {"success": True}, "call_verdict")


# -- S3: coder compaction on a small context (§7 S3) ------------------------------

# glossary/ modules the scripted coder walks through with read_file —
# enough requests for the INFLATED usage (see _usage_for) to cross the
# compaction threshold mid-run.
S3_READ_ORDER = [
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "zeta",
]
S3_FIX_KAPPA = (
    "python3 -c \"import pathlib; p=pathlib.Path('glossary/kappa.py'); "
    "p.write_text(p.read_text().replace('WEIGHT = 13', 'WEIGHT = 42'))\""
)


def _read_paths(messages: list[dict]) -> list[str]:
    out = []
    for m in messages:
        if m.get("role") != "assistant":
            continue
        for tc in m.get("tool_calls") or []:
            fn = tc.get("function") or {}
            if fn.get("name") == "read_file":
                with contextlib.suppress(json.JSONDecodeError):
                    out.append(str((json.loads(fn.get("arguments") or "{}")).get("path")))
    return out


def _s3_coder_script(messages: list[dict]) -> dict:
    """Coder for S3: read glossary modules one by one (each request
    reports inflated usage — the mid-run gate trips), then fix
    lambda.WEIGHT via run_bash and end the turn."""
    if _called(messages, "run_bash"):
        return _bash_end_run("WEIGHT термина kappa изменён на 42, тесты зелёные.")
    prompt_all = "\n".join(str(m.get("content") or "") for m in messages if m.get("role") == "user")
    # After the mid-run compaction the read history is summarized away —
    # the continuation turn goes straight to the fix.
    if "[context summary]" in prompt_all:
        return _run_bash(S3_FIX_KAPPA, "call_fix")
    reads = _read_paths(messages)
    for name in S3_READ_ORDER:
        if f"glossary/{name}.py" not in reads:
            return _call("read_file", {"path": f"glossary/{name}.py"}, f"call_read_{name}")
    return _run_bash(S3_FIX_KAPPA, "call_fix")


# -- S4: tester compaction on fat run_bash output (§7 S4) -------------------------

# report.py with the correct separator (the S4 coder's one-shot fix).
S4_FIX_REPORT = (
    "printf 'def format_report(items):\\n    return \"\\\\n\\\\n\".join(items)\\n' > report.py"
)
# The tester reads the 4.5k-line listing in WHOLE chunks of 100 lines
# (`sed -n 'A,Bp'` without pipes — the brief bans head/tail/grep filters;
# 100 × ~44 chars ≈ 4.4 KiB, safely under drcode's 10 KiB run_bash cap, so
# every portion is shown whole). The INFLATED usage crosses the threshold
# mid-round, so the tester compaction fires; the compaction rewrites the
# round in place — the pre-compaction reads are gone from the model view —
# and the fake compaction summary carries a read-through marker the tester
# resumes from (see _compaction_script / _s4_progress_in_summary).
S4_LISTING_LINES = 4500
S4_CHUNK_LINES = 100
# The mid-round trip point: usage(t) = 300 + 2200·t (t = tool results in
# view) crosses 80% × 30000 = 24000 at t = 11 → the compaction fires after
# the 12th read result of a cycle (the live reading lags one boundary
# behind) — 12 × 100 = 1200 lines per compaction cycle, the last cycle
# (reads 37..45, lines 3601..4500) stays under the threshold, so its reads
# SURVIVE in the transcript and checks.py can verify the shown coverage.
S4_USAGE_PER_TOOL = 2200


def _s4_shown_entries(messages: list[dict]) -> list[int]:
    """Listing line numbers shown in the tool results of the CURRENT model
    view (after a compaction the view is a summary — the pre-compaction
    reads are gone, so this deliberately restarts at the summary's marker)."""
    nums: list[int] = []
    for m in messages:
        if m.get("role") != "tool":
            continue
        for match in re.finditer(r"^entry (\d{6}):", str(m.get("content") or ""), re.MULTILINE):
            nums.append(int(match.group(1)))
    return nums


def _s4_progress_in_summary(messages: list[dict]) -> int:
    """Reading progress recorded by the fake compaction summary (0 when no
    summary is in the view): the 'read-through-line=NNNN' marker embedded
    by _compaction_script."""
    best = 0
    for m in messages:
        if m.get("role") != "user":
            continue
        for match in re.finditer(r"read-through-line=(\d+)", str(m.get("content") or "")):
            best = max(best, int(match.group(1)))
    return best


def _s4_coder_script(messages: list[dict]) -> dict:
    """Coder for S4: one run_bash fixing report.py, then end."""
    if _called(messages, "run_bash"):
        return _bash_end_run("format_report исправлен, pytest зелёный.")
    return _run_bash(S4_FIX_REPORT, "call_fix")


def _s4_tester_script(messages: list[dict]) -> dict:
    """Tester for S4: reads the full listing in whole 100-line chunks of
    `sed -n 'A,Bp'` (the brief's acceptance requirement, no pipes), then
    stamps PASSED. Resumes from the max line shown in the CURRENT view —
    after the mid-round compaction that view is a summary, so the resume
    point comes from the summary's read-through marker (compaction erases
    the pre-summary reads from the view; without the marker the script
    would restart from line 1 and re-cross the inflated threshold forever,
    compacting in a loop)."""
    if _called(messages, "set_verification"):
        return _bash_end_run("Листинг проверен полностью, задача verified.")
    shown = _s4_shown_entries(messages)
    progress = max(max(shown, default=0), _s4_progress_in_summary(messages))
    if progress >= S4_LISTING_LINES:
        return _call("set_verification", {"success": True}, "call_verdict")
    start = progress + 1
    end = min(start + S4_CHUNK_LINES - 1, S4_LISTING_LINES)
    return _run_bash(f"sed -n '{start},{end}p' data/listing.txt", f"call_cat_{start}")


# -- S7: fault injection (the proxy sits between drcode and THIS gateway) --------

# formatter.py with the correct bullet prefix (the S7 coder's fix).
S7_FIX = (
    "printf 'def bullet_list(items):\n"
    '    return "\\\\n".join("- " + item for item in items)\n'
    "' > formatter.py"
)
S7_READS = ["formatter.py", "test_formatter.py"]


def _s7_coder_script(messages: list[dict]) -> dict:
    """Coder for S7: reads BOTH seed files one by one (the brief demands
    it), then fixes bullet_list via run_bash and ends the turn — several
    requests before the turn completes, so the fault script's drops hit
    MID-DEVELOPMENT.

    Deliberately does NOT use _after_own_tool_call: a fault-injected run
    RESUMES a dropped attempt whose history legitimately ends with a tool
    result that is not this script's own call — the decision must come
    from what the history already contains (stateless across retries)."""
    if _called(messages, "run_bash"):
        return _bash_end_run("bullet_list исправлен, pytest зелёный.")
    reads = _read_paths(messages)
    for name in S7_READS:
        if name not in reads:
            return _call("read_file", {"path": name}, f"call_read_{name.replace('.', '_')}")
    return _run_bash(S7_FIX, "call_fix")


# -- S8: the tester fix loop (retry_here=True, upstream drcode 18b48f9) -----------

# fmt.py with ONLY pad() gaining truncation (the S8 brief's scope — the
# brief names no other function): the change BY DESIGN breaks test_row,
# which consumes pad() through row() with a name longer than the column.
# test_pad (short strings only) stays green — the change is invisible to
# its own pinned contract.
S8_FIX_PAD = (
    "printf 'def pad(text, width):\n"
    "    return text[:width].ljust(width)\n"
    "\\n"
    "def row(name, value, width=12):\n"
    '    return f"{pad(name, width)}: {value}"\n'
    "' > fmt.py"
)
# fmt.py after the fix-loop round: the regression from the tester's report
# is repaired (row() keeps long names whole) while pad() keeps its new
# truncation — the full suite is green again.
S8_FIX_ALL = (
    "printf 'def pad(text, width):\n"
    "    return text[:width].ljust(width)\n"
    "\\n"
    "def row(name, value, width=12):\n"
    '    return f"{pad(name, max(width, len(name)))}: {value}"\n'
    "' > fmt.py"
)

S8_RETRY_REPORT = (
    "Лог ошибки: python3 -m pytest -q завершается с exit=1 — падает test_row: "
    "row('configuration', 42) вернула 'configuratio: 42', ожидалось "
    "'configuration: 42'. Сбой вызван изменениями самой этой задачи: до правки "
    "pad() тест был зелёным. Исправьте регрессию: имя в row() не должно "
    "обрезаться новым pad() (верните строке её прежний контракт), новое "
    "поведение pad() (обрезка длинных строк) сохраните, чтобы полный pytest "
    "был зелёным."
)


def _s8_coder_script(messages: list[dict]) -> dict:
    """Coder for S8: round 1 changes ONLY pad() (the brief's scope) — by
    design that breaks test_row, which comes back to this very transcript
    as the tester's fix-loop report; round 2 repairs the regression
    (row() pads with spaces itself) keeping the new dot padding of pad()."""
    if _after_own_tool_call(messages):
        return _bash_end_run("Правка внесена.")
    prompt = _last_user_prompt(messages)
    # The fix-loop report (queued as the task's next input) names the
    # broken test — the round-2 repair is keyed on it. The brief does not
    # contain the literal, so round 1 stays scoped to pad().
    if "test_row" in prompt:
        return _run_bash(S8_FIX_ALL, "call_fix_regression")
    return _run_bash(S8_FIX_PAD, "call_fix_pad")


def _s8_tester_script(messages: list[dict]) -> dict:
    """Tester for S8: full pytest; a red suite is a failure caused by THIS
    task's own changes (the round-1 pad() edit broke the dependent
    test_row) → set_verification(success=False, retry_here=True) with the
    failure report — the fix loop requeues the task into development. A
    green suite → PASSED. retry_here=True is semantic, not a workaround:
    the regression belongs to the task, the report must reach the coder
    through requeue_failed_fix's pending_input."""
    if not any(m.get("role") == "tool" for m in messages):
        return _run_bash("python3 -m pytest -q", "call_pytest")
    out = _last_bash_output(messages)
    if " failed" in out or not out.startswith("exit=0"):
        if not _called(messages, "set_verification"):
            return _call(
                "set_verification",
                {
                    "success": False,
                    "retry_here": True,
                    "report": S8_RETRY_REPORT,
                },
                "call_verdict",
            )
        return _bash_end_run("Вердикт выставлен: возврат в разработку.")
    if not _called(messages, "set_verification"):
        return _call("set_verification", {"success": True}, "call_verdict")
    return _bash_end_run("Тесты зелёные, задача verified.")


# -- S9: research task over the CSV seed (docs/report.md, commit measured) --------

# The metric computation is a legitimate tool use (the brief leaves the
# path free): one python one-liner over data/orders.csv prints the sum of
# `amount` over `status == "completed"` — the run_bash output carries the
# number for the next step's write_file.
S9_COUNT_CMD = (
    'python3 -c "import csv; '
    "print(sum(int(r['amount']) for r in "
    "csv.DictReader(open('data/orders.csv')) "
    "if r['status'] == 'completed'))\""
)


def _s9_research_script(messages: list[dict]) -> dict:
    """Research agent for S9: compute the metric with run_bash, write
    docs/report.md with write_file (tracked into task.edited_files), commit
    it with git_commit_docs (the research.md mandate for documentation
    assignments — s9 measures the discipline via report_committed instead
    of failing the run on a missing commit), end the turn. Stateless
    decisions from the history: the computed number is parsed from the
    LAST run_bash output ('exit=0' line first, the printed sum last)."""
    if _called(messages, "git_commit_docs"):
        return _bash_end_run("Готово: отчёт записан в docs/report.md и закоммичен.")
    if _called(messages, "write_file"):
        return _call("git_commit_docs", {"message": "Add revenue report"}, "call_commit")
    if _called(messages, "run_bash"):
        out = _last_bash_output(messages)
        total = out.removeprefix("exit=0").strip().splitlines()[-1].strip()
        return _call(
            "write_file",
            {"path": "docs/report.md", "content": f"total: {total}\n"},
            "call_report",
        )
    return _run_bash(S9_COUNT_CMD, "call_count")


# -- S10: research over the planted facts (docs/findings.md + git_commit_docs) ----

# The grep alternation covering ALL THREE planted facts (orphan constant,
# duplicated function name, deprecated flag) — one search, like a real
# research pass; the paths/symbols for findings.md are parsed out of the
# tool RESULTS, never hardcoded here.
S10_FACT_PATTERN = "PARCEL_VOLUME_LIMIT_L|def balance|DETAILED_LEDGER"


def _tool_entries(messages: list[dict]) -> list[str]:
    """Flat list of the run's tool-result entries.

    A list return (grep_search / glob_files) reaches the gateway as the
    JSON array produced by ToolReturnPart.model_response_str(); a str
    return (run_bash etc.) arrives verbatim. Both shapes collapse into
    one list of strings here."""
    out: list[str] = []
    for m in messages:
        if m.get("role") != "tool":
            continue
        content = str(m.get("content") or "")
        try:
            val = json.loads(content)
        except json.JSONDecodeError:
            val = [content]
        if isinstance(val, list):
            out.extend(str(item) for item in val)
        else:
            out.append(str(val))
    return out


def _grep_hits(entries: list[str], needle: str) -> list[tuple[str, str]]:
    """(path, line text) pairs of grep entries 'path:line: text' whose
    text or path contains `needle`."""
    hits: list[tuple[str, str]] = []
    for entry in entries:
        path, lineno, text = entry.split(":", 2) if entry.count(":") >= 2 else ("", "", "")
        if path.endswith(".py") and lineno.isdigit() and needle in text:
            hits.append((path, text.strip()))
    return hits


def _s10_findings(messages: list[dict]) -> str:
    """Compose docs/findings.md from the ACTUAL tool outputs: the
    orphan/duplicate/flag facts come from the grep results the seed
    produced — exactly the reading-based path the brief demands."""
    entries = _tool_entries(messages)
    orphan = _grep_hits(entries, "PARCEL_VOLUME_LIMIT_L")
    dup = _grep_hits(entries, "def balance")
    flag = _grep_hits(entries, "DETAILED_LEDGER")

    lines = ["# Результаты исследования", ""]
    lines += ["## 1. Неиспользуемая константа", ""]
    for path, text in orphan:
        name = text.partition("=")[0].strip()
        lines.append(f"- `{path}` — `{name}` (единственное вхождение — определение)")
    lines += ["", "## 2. Функции с одинаковым именем в разных модулях", ""]
    for path, text in dup:
        name = text.partition("(")[0].removeprefix("def").strip()
        lines.append(f"- `{path}` — `{name}`")
    lines += ["", "## 3. Использование флага DETAILED_LEDGER", ""]
    for path, text in flag:
        role = "определение" if text.startswith("DETAILED_LEDGER") else "использование"
        lines.append(f"- `{path}` — {role}")
    return "\n".join(lines) + "\n"


def _s10_research_script(messages: list[dict]) -> dict:
    """Research agent for S10 (variant V2): glob the seed layout, grep
    the three fact identifiers in one alternation, write findings.md
    composed from the grep results, commit via git_commit_docs (the
    research.md mandate for documentation assignments). Stateless
    decisions from the history, like the other scenario scripts."""
    if _called(messages, "git_commit_docs"):
        return _bash_end_run("Готово: findings.md записан в docs/ и закоммичен.")
    if _called(messages, "write_file"):
        return _call("git_commit_docs", {"message": "Add code research findings"}, "call_commit")
    if _called(messages, "grep_search"):
        return _call(
            "write_file",
            {"path": "docs/findings.md", "content": _s10_findings(messages)},
            "call_report",
        )
    if _called(messages, "glob_files"):
        return _call(
            "grep_search",
            {"pattern": S10_FACT_PATTERN, "include": "*.py"},
            "call_grep",
        )
    return _call("glob_files", {"pattern": "**/*.py"}, "call_glob")


# -- S11: research over the route table (docs/routes.md + git_commit_docs) --------

# One grep covers BOTH sides of the seed's decorator-over-def pairs: every
# '@route("METHOD /path")' line arrives immediately before its 'def <name>'
# line in the results (grep walks files top-down), so the route table for
# docs/routes.md is parsed out of the TOOL RESULTS — nothing about the
# routes is hardcoded in the script; a drifted seed produces a table that
# checks.py rejects.
S11_ROUTE_PATTERN = r"@route\(|^def "


def _s11_table(messages: list[dict]) -> str:
    """Compose docs/routes.md from the ACTUAL grep output: every
    '@route("METHOD /path")' entry is paired with the next 'def <name>'
    entry — the decorator-over-def contract the brief describes. Rendered
    as the markdown table the brief pins (method | path | handler)."""
    routes: list[tuple[str, str, str]] = []
    pending: tuple[str, str] | None = None
    for entry in _tool_entries(messages):
        path, lineno, text = entry.split(":", 2) if entry.count(":") >= 2 else ("", "", "")
        if not (path.endswith(".py") and lineno.isdigit()):
            continue
        text = text.strip()
        match = re.match(r'@route\("(\w+) ([^"]+)"\)', text)
        if match:
            pending = (match.group(1), match.group(2))
            continue
        if pending and text.startswith("def "):
            handler = text[4:].split("(", 1)[0].strip()
            routes.append((*pending, handler))
            pending = None
    lines = ["| method | path | handler |", "| --- | --- | --- |"]
    lines += [f"| {method} | {route_path} | {handler} |" for method, route_path, handler in routes]
    return "\n".join(lines) + "\n"


def _s11_research_script(messages: list[dict]) -> dict:
    """Research agent for S11 (variant V3): ONE grep over the
    decorator/def alternation, pair each @route(...) line with the def
    line that follows it, write the markdown table composed from the
    grep results, commit via git_commit_docs (the research.md mandate
    for documentation assignments). Stateless decisions from the
    history, like the other scenario scripts."""
    if _called(messages, "git_commit_docs"):
        return _bash_end_run("Готово: таблица маршрутов записана в docs/routes.md и закоммичена.")
    if _called(messages, "write_file"):
        return _call("git_commit_docs", {"message": "Add API route table"}, "call_commit")
    if _called(messages, "grep_search"):
        return _call(
            "write_file",
            {"path": "docs/routes.md", "content": _s11_table(messages)},
            "call_report",
        )
    return _call(
        "grep_search",
        {"pattern": S11_ROUTE_PATTERN, "include": "*.py"},
        "call_grep",
    )


# -- S12: research files a bug report; the spawned bug runs the full pipeline -----

S12_PRICING_PATH = "dispatch/pricing.py"
# The defective function: the brief names only the module — the name in the
# report must come from the agent's own reading (parsed out of the read_file
# result, see _s12_bug_report). The CODING phase of the same model id keys on
# it appearing in the spawned bug's prompt (the report description); the
# research brief must NOT contain it.
S12_FUNCTION = "batches_needed"

# The coder's fix for the spawned bug: keep the whole file, replace the
# remainder-dropping return with the ceiling division (a targeted in-place
# replace, like the S3 kappa fix — the rest of the module stays untouched).
S12_FIX_CMD = (
    "python3 -c \"import pathlib; p=pathlib.Path('dispatch/pricing.py'); "
    "p.write_text(p.read_text().replace("
    "'return items // per_batch', "
    "'return -(-items // per_batch)'))\""
)


def _s12_bug_report(source: str) -> dict:
    """Compose the bug report from the ACTUAL read output: the function
    name and the docstring's example call are parsed out of the file the
    research agent read — exactly the reading-based path the brief demands.
    A drifted seed (renamed function, changed example) yields a report that
    checks.py rejects instead of silently passing."""
    match = re.search(r"(\w+)\((\d+),\s*(\d+)\)\s*==\s*(\d+)", source)
    name = match.group(1) if match else S12_FUNCTION
    items = int(match.group(2)) if match else 0
    per_batch = int(match.group(3)) if match else 0
    expected = int(match.group(4)) if match else 0
    actual = items // per_batch
    description = (
        f"Логическая ошибка в {S12_PRICING_PATH}, функция {name}: результат "
        f"{items} // {per_batch} отбрасывает остаток — неполная партия не "
        f"учитывается, хотя контракт (докстринг) требует обратного. "
        f"Проявление: {name}({items}, {per_batch}) возвращает {actual}, "
        f"по контракту должно быть {expected}. Исправьте {name} в "
        f"{S12_PRICING_PATH}: последняя неполная партия должна считаться, "
        "полный pytest должен остаться зелёным."
    )
    return {"title": f"Починить {name}(): теряется неполная партия", "description": description}


def _s12_agent_script(messages: list[dict]) -> dict:
    """The S12 agent — ONE model id for BOTH the research and the coding
    role (the S2b precedent of alternating transcripts on one model; the
    transcripts never mix: each task has its own). Research phase: read
    dispatch/pricing.py, file the ONE bug report via create_bug_report
    (the brief's explicit authorization), end the turn. Coding phase (the
    spawned bug's prompt IS the report description, which names the
    defective function): fix it with one targeted run_bash, end the turn.
    Stateless decisions from the history, like the other scenario scripts."""
    prompt = _last_user_prompt(messages)
    if S12_FUNCTION in prompt:
        # Coding phase on the spawned bug task.
        if _called(messages, "run_bash"):
            return _bash_end_run("Дефект исправлен, pytest зелёный.")
        return _run_bash(S12_FIX_CMD, "call_fix")
    # Research phase (the brief names the module, never the function).
    if _called(messages, "create_bug_report"):
        return _bash_end_run("Багрепорт заведён, задача исследования завершена.")
    if _called(messages, "read_file"):
        return _call("create_bug_report", _s12_bug_report(_last_tool_output(messages)), "call_bug")
    return _call("read_file", {"path": S12_PRICING_PATH}, "call_read")


def _s12_tester_script(messages: list[dict]) -> dict:
    """Tester for S12: full pytest on the spawned bug task; green → PASSED.
    The seed suite is green by design and the scripted fix keeps it so;
    the harness's checks.py re-runs pytest regardless of the verdict."""
    if not any(m.get("role") == "tool" for m in messages):
        return _run_bash("python3 -m pytest -q", "call_pytest")
    if not _called(messages, "set_verification"):
        return _call("set_verification", {"success": True}, "call_verdict")
    return _bash_end_run("Тесты зелёные, задача verified.")


# -- S13: research plans the refactor (create_feature_request); the spawned
# feature runs the full pipeline -------------------------------------------

# The package and the deprecated pattern the brief names; the canonical
# site list (5 telemetry modules) is NOT hardcoded here — the paths are
# parsed out of the grep results (see _s13_feature_request), so a drifted
# seed produces a plan that checks.py rejects instead of silently passing.
S13_PACKAGE = "telemetry"
S13_TOKEN = "math.floor"

# The uniform pattern line of the seed (identical in all five modules, so
# ONE targeted in-place replace covers every site — like the S3 kappa fix).
S13_OLD = "math.floor(sum(readings) / window_s)"
S13_NEW = "sum(readings) // window_s"

S13_FIX_CMD = (
    'python3 -c "import pathlib; '
    "[p.write_text(p.read_text().replace("
    f"'{S13_OLD}', "
    f"'{S13_NEW}')) "
    f"for p in pathlib.Path('{S13_PACKAGE}').glob('*.py')]\""
)


def _s13_feature_request(grep_output: str) -> dict:
    """Compose the feature request from the ACTUAL grep output: the site
    paths are parsed out of the tool result — exactly the reading-based
    path the brief demands (the canonical list of ALL places). A drifted
    seed yields an incomplete plan that checks.py rejects."""
    paths = sorted(set(re.findall(rf"{S13_PACKAGE}/[a-z_]+\.py", grep_output)))
    bullets = "\n".join(f"- {p}" for p in paths)
    description = (
        f"Перевести пакет {S13_PACKAGE} на целочисленное деление: заменить "
        f"конструкцию {S13_TOKEN}(...) на оператор // во всех местах, где "
        "она используется. Полный список файлов для изменения:\n"
        f"{bullets}\n"
        f"В каждом перечисленном файле заменить {S13_OLD} на {S13_NEW}; "
        "полный pytest должен остаться зелёным."
    )
    return {
        "title": f"Перевести {S13_PACKAGE} на целочисленное деление",
        "description": description,
    }


def _s13_agent_script(messages: list[dict]) -> dict:
    """The S13 agent — ONE model id for BOTH the research and the coding
    role (the S12 precedent of alternating transcripts on one model; the
    transcripts never mix: each task has its own). Research phase: grep
    the deprecated token across the package, file the ONE feature
    request via create_feature_request (the brief's explicit
    authorization) with the site list composed FROM THE GREP OUTPUT,
    end the turn. Coding phase (the spawned feature's prompt IS the
    request description, whose bullet list carries '- telemetry/'):
    apply the replacement in every listed file with one targeted
    run_bash, end the turn. Stateless decisions from the history, like
    the other scenario scripts."""
    prompt = _last_user_prompt(messages)
    # Coding phase discriminator: the request's bullet list ("-
    # telemetry/cpu.py") — the research brief names the package but never
    # as a bullet, so the phase split cannot misfire either way.
    if f"- {S13_PACKAGE}/" in prompt:
        if _called(messages, "run_bash"):
            return _bash_end_run("Замена выполнена во всех файлах, pytest зелёный.")
        return _run_bash(S13_FIX_CMD, "call_fix")
    # Research phase (the brief names the pattern, never the paths).
    if _called(messages, "create_feature_request"):
        return _bash_end_run("Задача на доработку составлена, исследование завершено.")
    if _called(messages, "grep_search"):
        return _call(
            "create_feature_request",
            _s13_feature_request(_last_tool_output(messages)),
            "call_request",
        )
    return _call(
        "grep_search",
        {"pattern": S13_TOKEN, "include": f"{S13_PACKAGE}/*.py"},
        "call_grep",
    )


def _s13_tester_script(messages: list[dict]) -> dict:
    """Tester for S13: full pytest on the spawned feature task; green →
    PASSED. The seed suite is green by design and the scripted
    replacement (behavior-preserving) keeps it so; the harness's
    checks.py re-runs pytest regardless of the verdict."""
    if not any(m.get("role") == "tool" for m in messages):
        return _run_bash("python3 -m pytest -q", "call_pytest")
    if not _called(messages, "set_verification"):
        return _call("set_verification", {"success": True}, "call_verdict")
    return _bash_end_run("Тесты зелёные, задача verified.")


SCRIPTS = {
    "fake-coder": _coder_script,
    "fake-tester": _tester_script,
    "fake-compaction": _compaction_script,
    "fake-research": _research_script,
    "s2a-coder": _s2a_coder_script,
    "s2a-tester": _bugfix_tester_script,
    "s2b-coder": _s2b_coder_script,
    "s2b-tester": _s2b_tester_script,
    "s5-coder": _s5_coder_script,
    "s5-tester": _s5_tester_script,
    "s3-coder": _s3_coder_script,
    "s4-coder": _s4_coder_script,
    "s4-tester": _s4_tester_script,
    "s7-coder": _s7_coder_script,
    "s7-tester": _tester_script,
    "s8-coder": _s8_coder_script,
    "s8-tester": _s8_tester_script,
    "s9-research": _s9_research_script,
    "s10-research": _s10_research_script,
    "s11-research": _s11_research_script,
    "s12-agent": _s12_agent_script,
    "s12-tester": _s12_tester_script,
    "s13-agent": _s13_agent_script,
    "s13-tester": _s13_tester_script,
}

# Fixed usage the gateway reports for every completion — small but
# non-zero, so recorder totals and transcript usage are cross-checkable.
USAGE = {"prompt_tokens": 120, "completion_tokens": 24, "total_tokens": 144}

# S3/S4: the gateway INFLATES the reported usage of these models so the
# compaction gates of drcode really trip in the e2e runs (plan §1.2). The
# caps come from the scenario's `[context]` section (9000 for the S3
# coding role, 30000 for the S4 tester role), so the inflation is tuned
# to THAT window (threshold = 80% of the cap, hard limit = 97%):
# - s3-coder: usage(n) = 300 + 1300·n crosses 80% × 9000 = 7200 at
#   n = 6 (8100) — the mid-run/turn-boundary gate trips there, right at
#   the end of the 6-module S3_READ_ORDER walk — and stays under the
#   hard limit 8730;
# - s4-tester: usage(n) = 300 + 2200·n crosses 80% × 30000 = 24000 at
#   n = 11 (24500) — the mid-round gate trips there (the live reading lags
#   one tool boundary behind, so the compaction fires after the 12th read
#   result of a cycle) — and stays under the hard limit 29100. The trip
#   point is tuned to the chunking in S4_CHUNK_LINES (100 lines/read,
#   1200 lines per compaction cycle): the final cycle (reads 37..45) never
#   re-crosses the threshold, so its reads survive the round rewrite and
#   checks.py can verify the shown listing coverage.
# In both cases the post-compaction continuation turn carries NO tool
# results (the history is a summary), so it reports the bare base —
# back under the threshold, and the compacted run settles instead of
# looping pause→compact forever. The read_file budget guard reads the
# same numbers, so at the trip point a further read is refused (a neutral
# tool result — the gate handles the window).
INFLATED_USAGE = {"s3-coder": (300, 1300), "s4-tester": (300, S4_USAGE_PER_TOOL)}


def _usage_for(model: str, messages: list[dict]) -> dict:
    spec = INFLATED_USAGE.get(model)
    if spec is None:
        return USAGE
    base, per_tool = spec
    n_tools = sum(1 for m in messages if m.get("role") == "tool")
    prompt = base + per_tool * n_tools
    return {
        "prompt_tokens": prompt,
        "completion_tokens": 24,
        "total_tokens": prompt + 24,
    }


def _sse(data: dict) -> bytes:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n".encode()


def _chat_stream(body: dict) -> bytes:
    """OpenAI-style SSE stream for one scripted completion."""
    model = body.get("model", "fake-coder")
    messages = body.get("messages", [])
    script = SCRIPTS.get(model, _coder_script)(messages)
    out = b""
    first = {
        "id": "chatcmpl-fixture",
        "object": "chat.completion.chunk",
        "created": 0,
        "model": model,
    }
    if "text" in script:
        out += _sse(
            first | {"choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}}]}
        )
        out += _sse(first | {"choices": [{"index": 0, "delta": {"content": script["text"]}}]})
        out += _sse(first | {"choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]})
    else:
        call = script["tool_calls"][0]
        out += _sse(
            first | {"choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}}]}
        )
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
    out += _sse(
        {
            "id": "chatcmpl-fixture",
            "object": "chat.completion.chunk",
            "created": 0,
            "model": model,
            "choices": [],
            "usage": _usage_for(model, messages),
        }
    )
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
        "usage": _usage_for(model, messages),
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
        _method, _, path = request_line.decode().partition(" ")
        path = path.split(" ")[0] if " " in path else path

        if path.endswith("/models") or path.endswith("/running"):
            payload = json.dumps({"data": [{"id": m} for m in MODELS]}).encode()
            head = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n"
        elif path.endswith("/chat/completions"):
            body = json.loads(body_raw or b"{}")
            rule = _stall_rule_for(str(body.get("model") or ""))
            if body.get("stream"):
                head = (
                    b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\n"
                    b"Connection: close\r\n\r\n"
                )
                if rule and rule.get("mode") == "mid":
                    # Headers + the FIRST SSE chunk, then silence: the
                    # watchdog abort lands mid-relay (not retryable).
                    stream = _chat_stream(body)
                    writer.write(head + stream.split(b"\n\n")[0] + b"\n\n")
                    await writer.drain()
                    if await _stall_silence(float(rule["stall_s"]), writer):
                        return
                    writer.write(stream)
                    await writer.drain()
                    return
                if rule and await _stall_silence(float(rule["stall_s"]), writer):
                    return
                writer.write(head + _chat_stream(body))
                await writer.drain()
                return
            payload = _chat_json(body)
            head = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n"
            if rule and rule.get("mode") == "mid":
                # Headers + a partial JSON body (the promised
                # Content-Length is unmet), then silence.
                writer.write(
                    head + f"Content-Length: {len(payload)}\r\n\r\n".encode() + payload[:10]
                )
                await writer.drain()
                if await _stall_silence(float(rule["stall_s"]), writer):
                    return
                writer.write(payload[10:])
                await writer.drain()
                return
            if rule and await _stall_silence(float(rule["stall_s"]), writer):
                return
        else:
            payload = b'{"error": "not found"}'
            head = (
                b"HTTP/1.1 404 Not Found\r\nContent-Type: application/json\r\nConnection: close\r\n"
            )
        writer.write(head + f"Content-Length: {len(payload)}\r\n\r\n".encode() + payload)
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
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(serve(int(sys.argv[1]) if len(sys.argv) > 1 else 8917))
