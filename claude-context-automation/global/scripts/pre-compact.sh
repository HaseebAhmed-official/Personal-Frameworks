#!/usr/bin/env bash
# ============================================================
# PRE-COMPACT HOOK — Fires BEFORE context auto-compaction
# ============================================================
# WHY: When context fills up, Claude auto-compacts (compresses)
#      old messages. This can lose important state. This script
#      marks the timestamp so PostCompact knows state is fresh.
#
# HOW: Reads stdin (JSON event data from Claude Code), timestamps
#      the existing session-state.json so we know when compaction
#      happened. The REAL state saving happens via CLAUDE.md rules
#      that instruct Claude to write session-state.json during work.
#
# CONSTRAINT: Must run in <2 seconds to not block compaction.
# ============================================================

STATE_FILE="$HOME/.claude/session-state.json"

# If session state exists, add compaction timestamp
if [ -f "$STATE_FILE" ]; then
    # Use python3 for reliable JSON manipulation (fast, <1 sec)
    python3 -c "
import json, sys
from datetime import datetime, timezone
try:
    with open('$STATE_FILE', 'r') as f:
        state = json.load(f)
    state['last_compaction'] = datetime.now(timezone.utc).isoformat()
    state['compaction_count'] = state.get('compaction_count', 0) + 1
    with open('$STATE_FILE', 'w') as f:
        json.dump(state, f, indent=2)
except Exception:
    pass  # Never block compaction
" 2>/dev/null
fi

# Output nothing — PreCompact should be silent and fast
exit 0
