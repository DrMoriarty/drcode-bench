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
- ``s4-tester`` — the S4 tester: reads the 25k-line listing in chunks
  (inflated usage → mid-round tester compaction), then stamps PASSED;
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
  mandate for documentation assignments).

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
)


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
# The tester reads the 25k-line listing in chunks (each run_bash result is
# capped at 10 KiB by drcode); the INFLATED usage crosses the threshold
# mid-round, so the tester compaction fires.
S4_CAT_COMMANDS = [
    "head -n 9000 data/listing.txt",
    "sed -n '9001,18000p' data/listing.txt",
    "tail -n 7000 data/listing.txt",
]


def _bash_calls(messages: list[dict]) -> int:
    return sum(
        1
        for m in messages
        if m.get("role") == "assistant"
        for tc in (m.get("tool_calls") or [])
        if (tc.get("function") or {}).get("name") == "run_bash"
    )


def _s4_coder_script(messages: list[dict]) -> dict:
    """Coder for S4: one run_bash fixing report.py, then end."""
    if _called(messages, "run_bash"):
        return _bash_end_run("format_report исправлен, pytest зелёный.")
    return _run_bash(S4_FIX_REPORT, "call_fix")


def _s4_tester_script(messages: list[dict]) -> dict:
    """Tester for S4: reads the full listing in chunks (the brief's
    acceptance requirement), then stamps PASSED. After the mid-round
    compaction the chunk history is a summary — the continuation goes
    straight to the verdict."""
    if _called(messages, "set_verification"):
        return _bash_end_run("Листинг проверен полностью, задача verified.")
    prompt_all = "\n".join(str(m.get("content") or "") for m in messages if m.get("role") == "user")
    if "[context summary]" in prompt_all:
        return _call("set_verification", {"success": True}, "call_verdict")
    n = _bash_calls(messages)
    if n < len(S4_CAT_COMMANDS):
        return _run_bash(S4_CAT_COMMANDS[n], f"call_cat_{n}")
    return _call("set_verification", {"success": True}, "call_verdict")


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


# -- S9: research task over the CSV seed (docs/report.md + git_commit_docs) -------

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
    assignments), end the turn. Stateless decisions from the history: the
    computed number is parsed from the LAST run_bash output ('exit=0' line
    first, the printed sum last)."""
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
}

# Fixed usage the gateway reports for every completion — small but
# non-zero, so recorder totals and transcript usage are cross-checkable.
USAGE = {"prompt_tokens": 120, "completion_tokens": 24, "total_tokens": 144}

# S3/S4: the gateway INFLATES the reported usage of these models so the
# compaction gates of drcode really trip in the e2e runs (plan §1.2): the
# prompt_tokens grow with every tool result in the history, crossing 80%
# of the matrix's max_context_tokens (100000 → 80000) after a few reads /
# fat run_bash outputs. The read_file budget guard uses the same numbers,
# so the scripted models stop reading right before the guard would refuse.
INFLATED_BASE = 9000
INFLATION_PER_TOOL_RESULT = {"s3-coder": 13000, "s4-tester": 26000}


def _usage_for(model: str, messages: list[dict]) -> dict:
    per_tool = INFLATION_PER_TOOL_RESULT.get(model)
    if per_tool is None:
        return USAGE
    n_tools = sum(1 for m in messages if m.get("role") == "tool")
    prompt = INFLATED_BASE + per_tool * n_tools
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
