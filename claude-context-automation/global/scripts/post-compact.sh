#!/usr/bin/env bash
# ============================================================
# POST-COMPACT HOOK — Fires AFTER context compaction
# ============================================================
# WHY: After compaction, Claude loses detailed context. This
#      script re-injects a summary so Claude knows what it was
#      doing. The output of this script appears in the conversation.
#
# HOW: Reads session-state.json (maintained by Claude via CLAUDE.md
#      rules) and outputs a formatted summary that Claude sees
#      immediately after compaction completes.
# ============================================================

STATE_FILE="$HOME/.claude/session-state.json"

if [ -f "$STATE_FILE" ]; then
    python3 -c "
import json, sys
try:
    with open('$STATE_FILE', 'r') as f:
        state = json.load(f)

    task = state.get('task', 'Unknown task')
    progress = state.get('progress', 'No progress recorded')
    decisions = state.get('decisions', [])
    next_steps = state.get('next_steps', [])
    active_files = state.get('active_files', [])
    plan_file = state.get('plan_file', '')

    print('--- SESSION STATE RESTORED AFTER COMPACTION ---')
    print(f'Task: {task}')
    print(f'Progress: {progress}')

    if decisions:
        print(f'Key decisions: {\"; \".join(decisions[:5])}')

    if active_files:
        print(f'Active files: {\", \".join(active_files[:8])}')

    if next_steps:
        print(f'Next steps: {\"; \".join(next_steps[:5])}')

    if plan_file:
        print(f'Full plan: {plan_file}')

    print('--- END STATE ---')
    print('Continue from where you left off. Update session-state.json as you make progress.')
except Exception as e:
    print(f'[PostCompact] Could not restore state: {e}')
" 2>/dev/null
else
    echo "[PostCompact] No session state found. Ask the user what they were working on."
fi

exit 0
