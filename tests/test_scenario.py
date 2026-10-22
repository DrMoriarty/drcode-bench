"""Tests of the scenario loader (bench.scenario, plan §7)."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest
from bench.scenario import (
    Scenario,
    ScenarioError,
    load_scenario,
    load_scenario_by_id,
)

REPO_SCENARIOS = Path(__file__).resolve().parents[1] / "scenarios"


def _write_scenario(tmp_path: Path, body: str) -> Scenario:
    d = tmp_path / "sX"
    d.mkdir()
    (d / "scenario.toml").write_text(textwrap.dedent(body), encoding="utf-8")
    return load_scenario(d)


def test_loads_repo_s1_happy() -> None:
    s = load_scenario_by_id(REPO_SCENARIOS, "s1_happy")
    assert s.id == "s1_happy"
    assert s.briefs and len(s.briefs) == 1
    assert s.briefs[0].kind == "feature"
    assert s.timeout_min > 0
    assert s.settle == {"verification": "passed"}
    assert (s.seed_dir / "string_utils.py").is_file()
    assert s.checks_file.is_file()


def test_kinds_restricted_to_feature_bug(tmp_path: Path) -> None:
    with pytest.raises(ScenarioError, match="research"):
        _write_scenario(
            tmp_path,
            """
            timeout = 10
            [[briefs]]
            title = "t"
            text = "do"
            kind = "research"
            """,
        )


def test_timeout_required(tmp_path: Path) -> None:
    with pytest.raises(ScenarioError, match="timeout"):
        _write_scenario(
            tmp_path,
            """
            [[briefs]]
            title = "t"
            text = "do"
            """,
        )


def test_unknown_settle_key_rejected(tmp_path: Path) -> None:
    with pytest.raises(ScenarioError, match="unknown key"):
        _write_scenario(
            tmp_path,
            """
            timeout = 10
            [[briefs]]
            title = "t"
            text = "do"
            [settle]
            verificatoin = "passed"
            """,
        )


def test_settle_ok_passed(tmp_path: Path) -> None:
    from drcode.models import Task, VerificationStatus

    s = _write_scenario(
        tmp_path,
        """
        timeout = 10
        [[briefs]]
        title = "t"
        text = "do"
        [settle]
        verification = "passed"
        """,
    )
    from drcode.models import TaskStatus

    ok_task = Task(title="t", status=TaskStatus.COMPLETED, verification=VerificationStatus.PASSED)
    bad_task = Task(title="t", status=TaskStatus.COMPLETED, verification=VerificationStatus.FAILED)
    assert s.settle_ok([ok_task]) is None
    assert "expected PASSED" in (s.settle_ok([bad_task]) or "")


def test_followups_and_answers_parsed(tmp_path: Path) -> None:
    s = _write_scenario(
        tmp_path,
        """
        timeout = 10
        [[briefs]]
        title = "t"
        text = "do"
        kind = "bug"

        [[followups]]
        task = "t"
        when = "verification_failed"
        text = "вот лог ошибки, исправь"

        [[clarification_answers]]
        match = "какой формат"
        answer = "JSON"
        """,
    )
    assert s.followups[0].when == "verification_failed"
    assert s.clarification_answers[0].answer == "JSON"
