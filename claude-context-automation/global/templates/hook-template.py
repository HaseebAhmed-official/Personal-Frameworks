#!/usr/bin/env python3
"""
HOOK NAME
=========
TRIGGER EVENT: (SessionStart | UserPromptSubmit | PreToolUse | PostToolUse |
                PreCompact | PostCompact | SubagentStop | Stop | Notification)

WHY:
  What problem this hook solves and why automation is better than manual.

HOW:
  High-level description of the hook's logic.

WHEN:
  Which trigger event fires this hook and under what conditions.
"""

import sys
sys.path.insert(0, '/root/.claude/scripts/hooks')  # Ensure common.py is importable
from common import load_payload, emit


def main() -> int:
    """Main hook entry point."""
    # Load the payload from Claude Code harness
    payload = load_payload()

    # ── Your logic here ──────────────────────────────────────
    # Example: extract tool name
    # tool_name = payload.get("toolName", "")
    # tool_input = payload.get("toolInput", {})

    # Example: emit a system message
    # return emit({
    #     "continue": True,
    #     "systemMessage": "Your message here"
    # })

    # Example: rewrite a prompt
    # return emit({"message": "Rewritten prompt"})

    # ── Always emit continue to avoid blocking Claude Code ───
    return emit({"continue": True})


if __name__ == "__main__":
    raise SystemExit(main())
