#!/usr/bin/env bash
# ============================================================
# SESSION START HOOK — Fires when a new session begins
# ============================================================
# WHY: When starting a new session, Claude has no memory of the
#      previous session. This script checks for saved state and
#      outputs a resume prompt so Claude can pick up where it
#      left off — eliminating the "re-explain everything" cycle.
#
# HOW: Reads session-state.json. If it exists and is <24 hours
#      old, outputs a resume summary. If stale, notes it.
# ============================================================

STATE_FILE="$HOME/.claude/session-state.json"

if [ -f "$STATE_FILE" ]; then
    python3 -c "
import json, sys
from datetime import datetime, timezone
try:
    with open('$STATE_FILE', 'r') as f:
        state = json.load(f)

    task = state.get('task', 'Unknown task')
    progress = state.get('progress', 'No progress recorded')
    project_dir = state.get('project_dir', '')
    next_steps = state.get('next_steps', [])
    plan_file = state.get('plan_file', '')
    timestamp = state.get('timestamp', '')

    # Check freshness
    stale = False
    if timestamp:
        try:
            saved_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            age_hours = (datetime.now(timezone.utc) - saved_time).total_seconds() / 3600
            stale = age_hours > 24
        except:
            pass

    print('--- PREVIOUS SESSION STATE FOUND ---')
    if stale:
        print('(Note: This state is >24 hours old — may be outdated)')
    print(f'Task: {task}')
    print(f'Progress: {progress}')
    if project_dir:
        print(f'Project: {project_dir}')
    if next_steps:
        print(f'Next steps: {\"; \".join(next_steps[:5])}')
    if plan_file:
        print(f'Full plan: {plan_file}')
    print('--- END STATE ---')
    print('Ask the user: \"I found state from a previous session. Resume this task, or start fresh?\"')
except Exception as e:
    print(f'[SessionStart] Error reading state: {e}')
" 2>/dev/null
fi

exit 0
