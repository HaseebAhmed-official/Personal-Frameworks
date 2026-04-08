#!/usr/bin/env python3
"""
PRE-COMPACT HOOK
================
Fires BEFORE context auto-compaction.

When context fills up, Claude Code auto-compacts (compresses) old messages.
This hook marks the current timestamp so we know when compaction happened,
enabling post-compact recovery to work properly.

The actual state saving happens via CLAUDE.md rules that instruct Claude
to write session-state.json during work.
"""

from common import load_payload, emit, read_session_state, write_session_state, get_current_time_iso


def main() -> int:
    """Timestamp session state before compaction."""
    # Load payload from harness (we don't actually need it for this hook)
    _payload = load_payload()

    # Read existing session state
    state = read_session_state()

    # Add compaction timestamp
    state['last_compaction'] = get_current_time_iso()
    state['compaction_count'] = state.get('compaction_count', 0) + 1

    # Write back
    write_session_state(state)

    # Emit success response with no special message (silent hook)
    return emit({'continue': True})


if __name__ == '__main__':
    raise SystemExit(main())
