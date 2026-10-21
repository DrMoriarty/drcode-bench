"""Mechanical correctness check of s5_clarification (plan drcode-bench.md §7).

Usage: python checks.py <workspace>          (exit 0 = green)

The verdict is NEVER built on the agents' words:

  1. the implemented format_price() is imported from the workspace and
     asserted against the standard the simulator sent (the expected
     strings live HERE, not in the seed — they must not leak into the
     workspace and hand the coder the answer without a clarification);
  2. the brief task is COMPLETED with verification=PASSED;
  3. the coder transcript shows the round-trip: at least one
     ask_clarifying_question tool call, the answer consumed as exactly
     ONE user prompt, and no duplicate left pending — checked with the
     same logic as drcode.transcript.is_pending_retry (the answer prompt
     must belong to a FINISHED attempt, not sit waiting);
  4. when the simulator log (`user_sim.jsonl`, §6) is next to the
     workspace, it must record the answer being sent while the task was
     in AWAITING_CLARIFICATION — the mechanical trace of the
     clarification → queued → completed chain.
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

EXPECTED_VERIFICATION = "Verified successfully"  # VerificationStatus.PASSED.value
COMPACTION_SUMMARY_PREFIX = "[context summary]"


def load_scenario() -> dict:
    toml = Path(__file__).resolve().parent / "scenario.toml"
    return tomllib.loads(toml.read_text(encoding="utf-8"))


def is_pending_retry(messages: list, text: str) -> bool:
    """Verbatim port of drcode.transcript.is_pending_retry: True when
    `text` is the prompt of an UNFINISHED attempt in the serialized
    transcript (a duplicate that would reach the model twice)."""
    idx = None
    for i, msg in enumerate(messages):
        if msg.get("kind") != "request" and msg.get("role") != "request":
            continue
        for part in msg.get("parts", []):
            if part.get("part_kind") == "user-prompt" and part.get("content") == text:
                idx = i
    if idx is None:
        return False
    for msg in reversed(messages[idx + 1 :]):
        if msg.get("kind") == "response" or msg.get("role") == "response":
            parts = msg.get("parts", [])
            has_text = any(
                p.get("part_kind") == "text" and p.get("content") for p in parts
            )
            has_tool_call = any(p.get("part_kind") == "tool-call" for p in parts)
            return not (has_text and not has_tool_call)
    return True


def user_prompts(messages: list) -> list[str]:
    out = []
    for msg in messages:
        if msg.get("kind") != "request" and msg.get("role") != "request":
            continue
        for part in msg.get("parts", []):
            if part.get("part_kind") != "user-prompt":
                continue
            content = part.get("content")
            if isinstance(content, str) and content.strip():
                text = content.strip()
                if text.startswith(COMPACTION_SUMMARY_PREFIX):
                    continue
                out.append(text)
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: checks.py <workspace>", file=sys.stderr)
        return 2
    workspace = Path(sys.argv[1])
    scenario = load_scenario()
    failures: list[str] = []

    # 1. The standard the simulator sent is now the mechanical contract.
    sys.path.insert(0, str(workspace))
    try:
        import prices  # noqa: E402
    except Exception as e:  # noqa: BLE001 - an unimportable module is a failure
        print(f"S5 checks FAILED: cannot import prices from workspace: {e}")
        return 1
    cases = {
        1234.5: "1 234,50 ₽",
        1234567.89: "1 234 567,89 ₽",
        42: "42,00 ₽",
    }
    for amount, expected in cases.items():
        try:
            got = prices.format_price(amount)
        except Exception as e:  # noqa: BLE001
            failures.append(f"format_price({amount}) raised {type(e).__name__}: {e}")
            continue
        if got != expected:
            failures.append(f"format_price({amount}) = {got!r}, expected {expected!r}")

    # 2./3. S5 assertions over the persisted task JSON.
    tasks_dir = workspace / ".drcode" / "tasks"
    tasks = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(tasks_dir.glob("*.json"))]
    brief_title = scenario["briefs"][0]["title"]
    briefs = [t for t in tasks if t.get("title") == brief_title]
    if not briefs:
        failures.append(f"no brief task {brief_title!r} in .drcode/tasks/")
    answer = str(scenario["clarification_answers"][0]["answer"]).strip()

    for t in briefs:
        tid = t.get("id")
        if t.get("status") != "completed":
            failures.append(f"task {tid}: status={t.get('status')!r}, expected 'completed'")
        if t.get("verification") != EXPECTED_VERIFICATION:
            failures.append(
                f"task {tid}: verification={t.get('verification')!r}, "
                f"expected {EXPECTED_VERIFICATION!r}"
            )

        messages = t.get("messages") or []

        # 3a. The round-trip actually happened: the coder asked.
        asks = 0
        for msg in messages:
            if msg.get("kind") != "response" and msg.get("role") != "response":
                continue
            for part in msg.get("parts", []):
                if part.get("part_kind") == "tool-call" and part.get("tool_name") == "ask_clarifying_question":
                    asks += 1
        if asks < 1:
            failures.append(
                f"task {tid}: no ask_clarifying_question call in the coder transcript"
            )

        # 3b. The answer was consumed as exactly ONE prompt (no duplicates).
        prompts = user_prompts(messages)
        hits = [p for p in prompts if answer.splitlines()[0].strip() in p]
        if len(hits) != 1:
            failures.append(
                f"task {tid}: the answer found {len(hits)} times among coder prompts, "
                "expected exactly 1 (it must be consumed as ONE prompt)"
            )

        # 3c. is_pending_retry logic: the answer must belong to a FINISHED
        #     attempt and must not sit in pending_input (no duplicate).
        if is_pending_retry(messages, answer):
            failures.append(f"task {tid}: the answer is still the prompt of an unfinished attempt")
        pending = [e.get("text") for e in (t.get("pending_input") or [])]
        if answer in pending:
            failures.append(f"task {tid}: the answer is still pending_input (never consumed)")

        # 4. The simulator log records the round-trip mechanically.
        sim_log = workspace.parent / "user_sim.jsonl"
        if sim_log.is_file():
            records = [
                json.loads(line)
                for line in sim_log.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            answers = [
                r
                for r in records
                if r.get("action") == "clarification_answer"
                and r.get("task_id") == tid
                and r.get("task_status") == "clarification"
            ]
            if not answers:
                failures.append(
                    f"task {tid}: user_sim.jsonl has no clarification_answer record "
                    "sent while the task was AWAITING_CLARIFICATION"
                )

    if failures:
        print("S5 checks FAILED:")
        for f in failures:
            print(f"- {f}")
        return 1
    print(
        "S5 checks: green (format_price matches the standard, task PASSED, "
        "clarification round-trip consumed the answer as one prompt)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
