#!/bin/bash
# Memory Cleanup Reminder — Checks if memory audit is overdue
# Triggered at session start. If last audit was >7 days ago, reminds user.
# Lightweight: just checks a timestamp file, no scanning.

MARKER_FILE="$HOME/.claude/session-logs/.last-memory-audit"
REMINDER_DAYS=7

# If marker doesn't exist, create it (first run — don't nag immediately)
if [ ! -f "$MARKER_FILE" ]; then
    date -u +"%Y-%m-%dT%H:%M:%SZ" > "$MARKER_FILE"
    exit 0
fi

# Check age of last audit
LAST_AUDIT=$(cat "$MARKER_FILE" 2>/dev/null)
LAST_EPOCH=$(date -d "$LAST_AUDIT" +%s 2>/dev/null || echo 0)
NOW_EPOCH=$(date +%s)
DIFF_DAYS=$(( (NOW_EPOCH - LAST_EPOCH) / 86400 ))

if [ "$DIFF_DAYS" -ge "$REMINDER_DAYS" ]; then
    echo ""
    echo "  Memory cleanup is overdue ($DIFF_DAYS days since last audit)."
    echo "  Run /memory-cleanup or /fw 1 to audit your memories."
    echo ""
fi

exit 0
