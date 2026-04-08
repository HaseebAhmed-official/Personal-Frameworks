#!/usr/bin/env python3
"""
SUBAGENT STOP HOOK
==================
Fires when a subagent completes and returns output to main thread.

This hook:
1. Reminds Claude to verify agent output quality
2. Enforces output format standards (findings, risks, recommendations)
3. Prevents unbounded context bleed from agents
"""

from common import load_payload, emit


def main() -> int:
    """Quality gate for subagent output."""
    payload = load_payload()

    message = (
        '**Subagent Output Quality Gate**:\n\n'
        'Verify the agent\'s output contains:\n'
        '✓ **Findings**: Clear, concise results (not raw exploration)\n'
        '✓ **Risks**: Known failure modes or assumptions to watch\n'
        '✓ **Recommended Next Action**: What should happen next\n\n'
        'If output is too verbose or missing structure, ask agent to condense and restructure.'
    )

    return emit({
        'continue': True,
        'systemMessage': message
    })


if __name__ == '__main__':
    raise SystemExit(main())
