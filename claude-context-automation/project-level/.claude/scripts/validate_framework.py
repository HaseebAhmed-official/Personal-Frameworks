#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = [
    "CLAUDE.md",
    "RULES.md",
    "MEMORY.md",
    ".claude/settings.json",
    ".claude/agents/context-researcher.md",
    ".claude/agents/verification-auditor.md",
    ".claude/agents/memory-curator.md",
    ".claude/agents/governance-reviewer.md",
    ".claude/commands/context-audit.md",
    ".claude/commands/governance/memory-proposal.md",
    ".claude/commands/governance/resume-ledger.md",
    ".claude/output-styles/context-lean.md",
    ".claude/output-styles/governed-execution.md",
    ".claude/scripts/statusline.py",
    ".claude/scripts/hooks/common.py",
    ".claude/scripts/hooks/session_start.py",
    ".claude/scripts/hooks/user_prompt_submit.py",
    ".claude/scripts/hooks/pre_tool_use.py",
    ".claude/scripts/hooks/post_tool_use.py",
    ".claude/scripts/hooks/pre_compact.py",
    ".claude/scripts/hooks/stop.py",
    ".claude/scripts/hooks/subagent_stop.py",
    ".claude/scripts/hooks/notification.py",
    ".claude/schemas/memory-entry.schema.json",
    ".claude/schemas/memory-entry.example.json",
    ".claude/schemas/state-ledger.example.yaml",
    ".claude/schemas/audit-event.example.json",
    "docs/framework/precedence.md",
    "docs/framework/agent-teams.md",
    "docs/framework/governance.md",
    "docs/framework/components.md",
    "docs/framework/smoke-test.md",
]


def run_json_check(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def run_hook(path: Path, payload: dict) -> str:
    proc = subprocess.run(
        ["python3", str(path)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout.strip()


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    missing = [item for item in REQUIRED_FILES if not (repo / item).exists()]
    assert_true(not missing, f"Missing required files: {missing}")

    run_json_check(repo / ".claude/settings.json")
    run_json_check(repo / ".claude/schemas/memory-entry.schema.json")
    run_json_check(repo / ".claude/schemas/memory-entry.example.json")
    run_json_check(repo / ".claude/schemas/audit-event.example.json")

    status_proc = subprocess.run(
        ["python3", str(repo / ".claude/scripts/statusline.py")],
        input="{}",
        text=True,
        capture_output=True,
        check=True,
    )
    assert_true(bool(status_proc.stdout.strip()), "Status line output is empty")

    session_output = run_hook(repo / ".claude/scripts/hooks/session_start.py", {})
    user_prompt_output = run_hook(
        repo / ".claude/scripts/hooks/user_prompt_submit.py",
        {"prompt": "Create an agent team and remember this"},
    )
    pre_tool_output = run_hook(
        repo / ".claude/scripts/hooks/pre_tool_use.py",
        {"toolName": "Edit", "toolInput": {"file_path": "CLAUDE.md"}},
    )
    stop_output = run_hook(repo / ".claude/scripts/hooks/stop.py", {})
    subagent_output = run_hook(repo / ".claude/scripts/hooks/subagent_stop.py", {})

    parsed_outputs = {}
    for label, raw in [
        ("session_start", session_output),
        ("user_prompt_submit", user_prompt_output),
        ("pre_tool_use", pre_tool_output),
        ("stop", stop_output),
        ("subagent_stop", subagent_output),
    ]:
        parsed = json.loads(raw)
        parsed_outputs[label] = parsed
        assert_true(parsed.get("continue") is True, f"{label} did not continue")

    pre_tool_message = parsed_outputs["pre_tool_use"].get("systemMessage", "").lower()
    user_prompt_message = parsed_outputs["user_prompt_submit"].get("systemMessage", "").lower()

    assert_true("approved" in pre_tool_message or "approval" in pre_tool_message, "PreToolUse reminder missing")
    assert_true("agent teams" in user_prompt_message, "Agent team reminder missing")
    assert_true("memory" in user_prompt_message, "Memory reminder missing")

    print("Framework validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Framework validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
