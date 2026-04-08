#!/usr/bin/env python3
"""
SESSION START HOOK
==================
Fires when a new Claude Code session starts.

This hook:
1. Checks for previous session state and offers resume if recent (<24h)
2. Emits framework context requirements (load CLAUDE.md, RULES.md, MEMORY.md)
3. Sets the tone for session governance and state management
"""

from common import load_payload, emit, read_session_state, get_current_time_iso
from datetime import datetime, timezone, timedelta


def is_recent_state(state: dict) -> bool:
    """Check if session state is recent (less than 24 hours old).

    Args:
        state: Session state dict

    Returns:
        bool: True if timestamp is within 24 hours
    """
    timestamp_str = state.get('timestamp')
    if not timestamp_str:
        return False

    try:
        # Parse ISO timestamp
        state_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        age = now - state_time

        return age < timedelta(hours=24)
    except Exception:
        return False


def main() -> int:
    """Load framework context and detect previous session."""
    # Load payload (not needed)
    _payload = load_payload()

    # Read session state
    state = read_session_state()

    messages = []

    # === Part 1: Check for previous session ===
    if state:
        if is_recent_state(state):
            # Recent session — offer resume
            task = state.get('task', 'Unknown task')
            progress = state.get('progress', 'No progress')
            messages.append(
                f'**Previous session detected** (active <24h ago):\n'
                f'- Task: {task}\n'
                f'- Progress: {progress}\n\n'
                f'Resume this session? (Or start fresh.)'
            )
        else:
            # Stale session — warn but don't resume
            messages.append(
                '**Previous session state found but is stale (>24h ago). '
                'Use `/governance:resume-ledger` if you want to review what was happening.**'
            )

    # === Part 2: Framework context requirements ===
    messages.append(
        '\n**Framework Context Required**\n'
        'Before major work, load these artifacts:\n'
        '- `@CLAUDE.md` — behavioral rules and operating principles\n'
        '- `@RULES.md` — precedence hierarchy and routing decisions\n'
        '- `@MEMORY.md` — memory taxonomy and ledger template\n'
        '- `@docs/framework/` — governance, agent teams, components\n\n'
        '**Session Operating Principles**:\n'
        '1. Keep main thread compact — delegate heavy work to subagents\n'
        '2. Maintain session-state.json during work (auto-updated at milestones)\n'
        '3. Get explicit approval before: durable memory, framework edits, reusable components, agent teams\n'
        '4. Use `/context-audit` to check context health and routing\n'
        '5. Run validation: `python3 ~/.claude/scripts/validate_framework.py`'
    )

    # Emit as system message
    full_message = '\n'.join(messages)
    return emit({
        'continue': True,
        'systemMessage': full_message
    })


if __name__ == '__main__':
    raise SystemExit(main())
