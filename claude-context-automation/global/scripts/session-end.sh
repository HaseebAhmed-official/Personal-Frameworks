#!/usr/bin/env bash
# ============================================================
# SESSION END (STOP) HOOK — Fires when session ends
# ============================================================
# WHY: Captures final session state and logs a session summary.
#      Even if the user didn't manually save, this ensures state
#      is preserved for the next session.
#
# HOW: Copies current session-state.json to session-logs with
#      a timestamped filename for history. The session-state.json
#      itself persists for the next session's SessionStart hook.
# ============================================================

STATE_FILE="$HOME/.claude/session-state.json"
LOG_DIR="$HOME/.claude/session-logs"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# If state exists, archive it to session logs
if [ -f "$STATE_FILE" ]; then
    TIMESTAMP=$(date +%Y-%m-%d-%H-%M)
    cp "$STATE_FILE" "$LOG_DIR/${TIMESTAMP}.json" 2>/dev/null
fi

exit 0
