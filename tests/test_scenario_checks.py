"""Tests of the scenario checks.py contracts (plan drcode-bench.md §7).

Each scenario's mechanical check is run against a SYNTHETIC workspace
(seed + a hand-built `.drcode/tasks/` state) — both green and broken
variants, so the assertions are known to actually bite.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def run_checks(scenario_id: str, workspace: Path) -> subprocess.CompletedProcess:
    checks = REPO / "scenarios" / scenario_id / "checks.py"
    return subprocess.run(
        [sys.executable, str(checks), str(workspace)],
        capture_output=True,
        text=True,
        cwd=str(workspace),
        check=False,
    )


def load_scenario_toml(scenario_id: str) -> dict:
    return tomllib.loads(
        (REPO / "scenarios" / scenario_id / "scenario.toml").read_text(encoding="utf-8")
    )


def make_workspace(tmp_path: Path, scenario_id: str, *, fix: bool) -> Path:
    """A run tree with the seed copied in; `fix` applies the scenario's
    intended final state of the seed code."""
    run_dir = tmp_path / "run"
    workspace = run_dir / "workspace"
    shutil.copytree(REPO / "scenarios" / scenario_id / "seed", workspace)
    (workspace / ".drcode" / "tasks").mkdir(parents=True)
    if fix:
        if scenario_id == "s2a_bug_followup":
            (workspace / "calc.py").write_text(
                "def div(a, b):\n"
                "    if b == 0:\n"
                "        raise ValueError('zero divisor')\n"
                "    return a / b\n\n"
                "def pct(a, b):\n"
                "    return a / b * 100\n",
                encoding="utf-8",
            )
        elif scenario_id == "s3_compaction_coder":
            p = workspace / "glossary" / "kappa.py"
            p.write_text(
                p.read_text(encoding="utf-8").replace("WEIGHT = 13", "WEIGHT = 42"),
                encoding="utf-8",
            )
        elif scenario_id == "s4_compaction_tester":
            (workspace / "report.py").write_text(
                'def format_report(items):\n    return "\\n\\n".join(items)\n',
                encoding="utf-8",
            )
        elif scenario_id == "s2b_bug_report":
            (workspace / "calc.py").write_text(
                "def div(a, b):\n"
                "    if b == 0:\n"
                "        raise ValueError('zero divisor')\n"
                "    return a / b\n\n"
                "def pct(a, b):\n"
                "    return a / b * 100\n\n"
                "def export_api():\n"
                "    return ['div', 'pct']\n",
                encoding="utf-8",
            )
        elif scenario_id == "s5_clarification":
            (workspace / "prices.py").write_text(
                'def format_price(amount, currency="RUB"):\n'
                '    symbol = "₽" if currency == "RUB" else currency\n'
                '    body = f"{amount:,.2f}"\n'
                '    body = body.replace(",", " ").replace(".", ",")\n'
                '    return f"{body} {symbol}"\n',
                encoding="utf-8",
            )
    return run_dir


def request_msg(content: str) -> dict:
    return {
        "kind": "request",
        "timestamp": "2025-06-01T10:00:00+00:00",
        "parts": [{"part_kind": "user-prompt", "content": content}],
    }


def response_msg(parts: list[dict]) -> dict:
    return {
        "kind": "response",
        "timestamp": "2025-06-01T10:00:05+00:00",
        "parts": parts,
    }


def text_part(content: str) -> dict:
    return {"part_kind": "text", "content": content}


def tool_call_part(name: str) -> dict:
    return {"part_kind": "tool-call", "tool_name": name, "args": "{}"}


def write_task(workspace: Path, **fields) -> dict:
    task = {
        "id": fields.get("id", "abc123"),
        "title": fields["title"],
        "kind": fields.get("kind", "feature"),
        "status": fields.get("status", "completed"),
        "verification": fields.get("verification", "Verified successfully"),
        "messages": fields.get("messages", []),
        "tester_messages": fields.get("tester_messages", []),
        "events": fields.get("events", []),
        "pending_input": fields.get("pending_input", []),
        "activated_at": fields.get("activated_at"),
        "created_at": "2025-06-01T10:00:00+00:00",
    }
    path = workspace / ".drcode" / "tasks" / f"{task['id']}.json"
    path.write_text(json.dumps(task, ensure_ascii=False), encoding="utf-8")
    return task


# -- S2a ----------------------------------------------------------------------


def brief_messages(scenario_id: str) -> tuple[str, list[dict]]:
    """(followup marker, coder transcript of the intended S2a flow)."""
    scenario = load_scenario_toml(scenario_id)
    brief_text = scenario["briefs"][0]["text"].strip()
    followup_text = scenario["followups"][0]["text"].strip()
    messages = [
        request_msg(brief_text),
        response_msg([text_part("Исправил div().")]),
        request_msg(followup_text),
        response_msg([text_part("Исправил и pct(), pytest зелёный.")]),
    ]
    return followup_text, messages


def test_s2a_checks_green(tmp_path: Path) -> None:
    run_dir = make_workspace(tmp_path, "s2a_bug_followup", fix=True)
    workspace = run_dir / "workspace"
    _, messages = brief_messages("s2a_bug_followup")
    scenario = load_scenario_toml("s2a_bug_followup")
    write_task(
        workspace,
        title=scenario["briefs"][0]["title"],
        kind="bug",
        messages=messages,
        tester_messages=[[], []],  # two testing rounds
    )
    result = run_checks("s2a_bug_followup", workspace)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda msgs: msgs[:2], id="one-round-only"),
        pytest.param(
            lambda msgs: msgs + [msgs[2], msgs[3]], id="follow-up-seen-twice"
        ),
        pytest.param(lambda msgs: [], id="no-follow-up-at-all"),
    ],
)
def test_s2a_checks_bite(tmp_path: Path, mutate) -> None:
    run_dir = make_workspace(tmp_path, "s2a_bug_followup", fix=True)
    workspace = run_dir / "workspace"
    _, messages = brief_messages("s2a_bug_followup")
    scenario = load_scenario_toml("s2a_bug_followup")
    rounds = 2 if len(mutate(messages)) >= 2 else 1
    write_task(
        workspace,
        title=scenario["briefs"][0]["title"],
        kind="bug",
        messages=mutate(messages),
        tester_messages=[[] for _ in range(rounds)],
    )
    result = run_checks("s2a_bug_followup", workspace)
    assert result.returncode == 1, result.stdout + result.stderr


def test_s2a_checks_red_on_red_pytest(tmp_path: Path) -> None:
    run_dir = make_workspace(tmp_path, "s2a_bug_followup", fix=False)
    workspace = run_dir / "workspace"
    _, messages = brief_messages("s2a_bug_followup")
    scenario = load_scenario_toml("s2a_bug_followup")
    write_task(
        workspace,
        title=scenario["briefs"][0]["title"],
        kind="bug",
        messages=messages,
        tester_messages=[[], []],
    )
    result = run_checks("s2a_bug_followup", workspace)
    assert result.returncode == 1


# -- S2b ----------------------------------------------------------------------


def test_s2b_checks_green(tmp_path: Path) -> None:
    run_dir = make_workspace(tmp_path, "s2b_bug_report", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s2b_bug_report")
    write_task(
        workspace,
        id="briefA",
        title=scenario["briefs"][0]["title"],
        kind="feature",
        activated_at="2025-06-01T10:00:05+00:00",
        tester_messages=[[]],
    )
    write_task(
        workspace,
        id="briefB",
        title=scenario["briefs"][1]["title"],
        kind="feature",
        activated_at="2025-06-01T10:00:20+00:00",
        tester_messages=[[]],
    )
    write_task(
        workspace,
        id="bug1",
        title="Починить pct(): test_pct падает",
        kind="bug",
        activated_at="2025-06-01T10:00:10+00:00",  # before briefB
        tester_messages=[[]],  # passed its own testing round
    )
    result = run_checks("s2b_bug_report", workspace)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "bug_activated",
    ["2025-06-01T10:00:30+00:00"],  # AFTER briefB — queue priority broken
)
def test_s2b_checks_bite_on_queue_priority(tmp_path: Path, bug_activated: str) -> None:
    run_dir = make_workspace(tmp_path, "s2b_bug_report", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s2b_bug_report")
    write_task(
        workspace, id="briefA", title=scenario["briefs"][0]["title"],
        kind="feature", activated_at="2025-06-01T10:00:05+00:00", tester_messages=[[]],
    )
    write_task(
        workspace, id="briefB", title=scenario["briefs"][1]["title"],
        kind="feature", activated_at="2025-06-01T10:00:20+00:00", tester_messages=[[]],
    )
    write_task(
        workspace, id="bug1", title="Починить pct()", kind="bug",
        activated_at=bug_activated, tester_messages=[[]],
    )
    result = run_checks("s2b_bug_report", workspace)
    assert result.returncode == 1
    assert "queue priority" in result.stdout


def test_s2b_checks_bite_on_unverified_bug(tmp_path: Path) -> None:
    run_dir = make_workspace(tmp_path, "s2b_bug_report", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s2b_bug_report")
    write_task(
        workspace, id="briefA", title=scenario["briefs"][0]["title"],
        kind="feature", activated_at="2025-06-01T10:00:05+00:00", tester_messages=[[]],
    )
    write_task(
        workspace, id="briefB", title=scenario["briefs"][1]["title"],
        kind="feature", activated_at="2025-06-01T10:00:20+00:00", tester_messages=[[]],
    )
    write_task(
        workspace, id="bug1", title="Починить pct()", kind="bug",
        activated_at="2025-06-01T10:00:10+00:00",
        verification=None, tester_messages=[],  # never tested
    )
    result = run_checks("s2b_bug_report", workspace)
    assert result.returncode == 1


# -- S5 -----------------------------------------------------------------------


def s5_answer() -> str:
    return load_scenario_toml("s5_clarification")["clarification_answers"][0][
        "answer"
    ].strip()


def s5_messages(*, duplicate_answer: bool = False, answer_pending: bool = False) -> list[dict]:
    scenario = load_scenario_toml("s5_clarification")
    brief_text = scenario["briefs"][0]["text"].strip()
    answer = s5_answer()
    messages = [
        request_msg(brief_text),
        response_msg([tool_call_part("ask_clarifying_question")]),
        request_msg(answer),
    ]
    if answer_pending:
        return messages  # the answer sits at the tail — never consumed
    messages.append(response_msg([text_part("Реализовал по стандарту.")]))
    if duplicate_answer:
        messages.append(request_msg(answer))
        messages.append(response_msg([text_part("Реализовал по стандарту.")]))
    return messages


def test_s5_checks_green(tmp_path: Path) -> None:
    run_dir = make_workspace(tmp_path, "s5_clarification", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s5_clarification")
    task = write_task(
        workspace,
        title=scenario["briefs"][0]["title"],
        kind="feature",
        messages=s5_messages(),
        tester_messages=[[]],
    )
    (run_dir / "user_sim.jsonl").write_text(
        json.dumps(
            {
                "action": "clarification_answer",
                "task_id": task["id"],
                "task_status": "clarification",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    result = run_checks("s5_clarification", workspace)
    assert result.returncode == 0, result.stdout + result.stderr


def test_s5_checks_bite_on_duplicate_answer(tmp_path: Path) -> None:
    run_dir = make_workspace(tmp_path, "s5_clarification", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s5_clarification")
    write_task(
        workspace,
        title=scenario["briefs"][0]["title"],
        kind="feature",
        messages=s5_messages(duplicate_answer=True),
        tester_messages=[[]],
    )
    result = run_checks("s5_clarification", workspace)
    assert result.returncode == 1
    assert "exactly 1" in result.stdout


def test_s5_checks_bite_on_unconsumed_answer(tmp_path: Path) -> None:
    run_dir = make_workspace(tmp_path, "s5_clarification", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s5_clarification")
    write_task(
        workspace,
        title=scenario["briefs"][0]["title"],
        kind="feature",
        messages=s5_messages(answer_pending=True),
        tester_messages=[[]],
    )
    result = run_checks("s5_clarification", workspace)
    assert result.returncode == 1


def test_s5_checks_bite_without_clarification(tmp_path: Path) -> None:
    """The coder never asked — the round-trip assertion must fail even
    though the implementation itself is correct."""
    run_dir = make_workspace(tmp_path, "s5_clarification", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s5_clarification")
    write_task(
        workspace,
        title=scenario["briefs"][0]["title"],
        kind="feature",
        messages=[
            request_msg(scenario["briefs"][0]["text"].strip()),
            response_msg([text_part("Сделал как понял.")]),
        ],
        tester_messages=[[]],
    )
    result = run_checks("s5_clarification", workspace)
    assert result.returncode == 1
    assert "ask_clarifying_question" in result.stdout


# -- S3: coder compaction -------------------------------------------------------


def s3_task_messages(scenario_id: str = "s3_compaction_coder") -> tuple[list[dict], str]:
    """(coder transcript of the intended S3 flow, brief text)."""
    brief = load_scenario_toml(scenario_id)["briefs"][0]["text"].strip()
    merged = {
        "kind": "request",
        "timestamp": "2025-06-01T10:00:20+00:00",
        "parts": [
            {"part_kind": "user-prompt", "content": brief},
            {
                "part_kind": "user-prompt",
                "content": "[context summary]\n\nЗадача: изменить WEIGHT kappa на 42; прочитаны модули каталога.",
            },
        ],
    }
    messages = [
        request_msg(brief),
        response_msg([tool_call_part("read_file")]),
        # The persisted post-compaction shape: the ORIGINAL prompt and the
        # summary prompt live in one merged request (observed on disk).
        merged,
        response_msg([tool_call_part("run_bash")]),
        response_msg([text_part("Готово, pytest зелёный.")]),
    ]
    return messages, brief


def s3_events() -> list[dict]:
    return [
        {"at": "2025-06-01T10:00:10+00:00", "text": "Context fill 87% — pausing the run to compact history…"},
        {"at": "2025-06-01T10:00:11+00:00", "text": "Context fill 87% — pausing the agent and compacting history…"},
        {"at": "2025-06-01T10:00:12+00:00", "text": "Context compacted: history summarized, original task prompt(s) kept verbatim."},
    ]


def test_s3_checks_green(tmp_path: Path) -> None:
    run_dir = make_workspace(tmp_path, "s3_compaction_coder", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s3_compaction_coder")
    messages, _ = s3_task_messages()
    write_task(
        workspace,
        title=scenario["briefs"][0]["title"],
        kind="feature",
        messages=messages,
        events=s3_events(),
        tester_messages=[[]],
    )
    result = run_checks("s3_compaction_coder", workspace)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "mid-run path" in result.stdout


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda t: {**t, "events": []}, id="no-compaction-events"),
        pytest.param(
            lambda t: {
                **t,
                "messages": [
                    m
                    for m in t["messages"]
                    if "[context summary]" not in json.dumps(m, ensure_ascii=False)
                ],
            },
            id="no-summary-in-transcript",
        ),
        pytest.param(
            lambda t: {
                **t,
                # Summary present but the ORIGINAL prompt lost (§1.4 violated).
                "messages": [
                    m for m in t["messages"] if "найдите модуль термина" not in json.dumps(m, ensure_ascii=False)
                ],
            },
            id="original-prompt-lost",
        ),
        pytest.param(lambda t: {**t, "verification": None}, id="no-verdict"),
    ],
)
def test_s3_checks_bite(tmp_path: Path, mutate) -> None:
    run_dir = make_workspace(tmp_path, "s3_compaction_coder", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s3_compaction_coder")
    messages, _ = s3_task_messages()
    task = {
        "id": "abc123",
        "title": scenario["briefs"][0]["title"],
        "kind": "feature",
        "status": "completed",
        "verification": "Verified successfully",
        "messages": messages,
        "tester_messages": [[]],
        "events": s3_events(),
    }
    write_task(workspace, **mutate(task))
    result = run_checks("s3_compaction_coder", workspace)
    assert result.returncode == 1, result.stdout + result.stderr


# -- S4: tester mid-round compaction ---------------------------------------------


def s4_tester_rounds(scenario_id: str = "s4_compaction_tester") -> list[list[dict]]:
    """The intended S4 tester round: chunks of the listing, then the
    mid-round compaction rewrites the round in place (summary inside the
    LAST round), then the verdict."""
    return [
        [
            request_msg("Verify completed task: полный листинг data/listing.txt"),
            response_msg([tool_call_part("run_bash")]),
            request_msg("[context summary]\n\nПрочитан листинг: 25000 строк, entry 025000 в конце."),
            response_msg([tool_call_part("set_verification")]),
            response_msg([text_part("Листинг проверен полностью.")]),
        ]
    ]


def s4_events() -> list[dict]:
    return [
        {"at": "2025-06-01T10:00:20+00:00", "text": "Context fill 87% — pausing the tester round to compact history…"},
        {"at": "2025-06-01T10:00:21+00:00", "text": "Context fill 87% — compacting the testing round…"},
        {"at": "2025-06-01T10:00:22+00:00", "text": "Context compacted: testing round summarized, original prompt kept verbatim."},
    ]


def test_s4_checks_green(tmp_path: Path) -> None:
    run_dir = make_workspace(tmp_path, "s4_compaction_tester", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s4_compaction_tester")
    write_task(
        workspace,
        title=scenario["briefs"][0]["title"],
        kind="bug",
        messages=[
            request_msg(scenario["briefs"][0]["text"].strip()),
            response_msg([text_part("format_report исправлен.")]),
        ],
        events=s4_events(),
        tester_messages=s4_tester_rounds(),
    )
    result = run_checks("s4_compaction_tester", workspace)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda t: {**t, "events": []}, id="no-tester-compaction-events"),
        pytest.param(
            lambda t: {
                **t,
                # Compaction happened in an EARLIER round, not the last one.
                "tester_messages": [
                    s4_tester_rounds()[0],
                    [request_msg("second round"), response_msg([text_part("ok")])],
                ],
            },
            id="summary-not-in-last-round",
        ),
        pytest.param(lambda t: {**t, "verification": None}, id="no-verdict"),
        pytest.param(
            lambda t: {**t, "events": [e for e in t["events"] if "summarized" not in e["text"]]},
            id="compaction-never-succeeded",
        ),
    ],
)
def test_s4_checks_bite(tmp_path: Path, mutate) -> None:
    run_dir = make_workspace(tmp_path, "s4_compaction_tester", fix=True)
    workspace = run_dir / "workspace"
    scenario = load_scenario_toml("s4_compaction_tester")
    task = {
        "id": "bug1",
        "title": scenario["briefs"][0]["title"],
        "kind": "bug",
        "status": "completed",
        "verification": "Verified successfully",
        "messages": [
            request_msg(scenario["briefs"][0]["text"].strip()),
            response_msg([text_part("format_report исправлен.")]),
        ],
        "events": s4_events(),
        "tester_messages": s4_tester_rounds(),
    }
    write_task(workspace, **mutate(task))
    result = run_checks("s4_compaction_tester", workspace)
    assert result.returncode == 1, result.stdout + result.stderr
