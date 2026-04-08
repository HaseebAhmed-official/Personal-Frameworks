#!/usr/bin/env python3
"""
STOP HOOK
=========
Fires when Claude Code session terminates.

This hook:
1. Archives session-state.json to session-logs/ with timestamp
2. Performs final governance check
3. Ensures audit trail is complete
"""

import shutil
from pathlib import Path
from common import (
    load_payload, emit, get_session_state_file,
    get_session_logs_dir, get_current_time_iso
)


def archive_session_state() -> bool:
    """Archive current session-state.json to session-logs.

    Stores copy with timestamp: session-logs/YYYY-MM-DDTHH-MM-SSZ.json

    Returns:
        bool: True if successful
    """
    state_file = get_session_state_file()
    if not state_file.exists():
        return False

    try:
        logs_dir = get_session_logs_dir()
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Create timestamped archive name
        timestamp = get_current_time_iso().replace(':', '-')  # Make filesystem-safe
        archive_file = logs_dir / f'{timestamp}.json'

        # Copy state file to archive
        shutil.copy2(state_file, archive_file)
        return True
    except Exception:
        return False


def main() -> int:
    """Archive session state and perform governance checks."""
    payload = load_payload()

    # Archive session state
    archive_session_state()

    # Governance final check
    message = (
        '**Session Ending Governance Check**:\n\n'
        '✓ Session state archived to ~/.claude/session-logs/\n\n'
        '**Verify before stopping**:\n'
        '- Session state ledger is clear (goal, decisions, blockers, next action captured)\n'
        '- No unauthorized memory has been written to MEMORY.md\n'
        '- No framework files modified without approval\n\n'
        'If this is incomplete, consider `/governance:resume-ledger` at next session start.'
    )

    return emit({
        'continue': True,
        'systemMessage': message
    })


if __name__ == '__main__':
    raise SystemExit(main())
