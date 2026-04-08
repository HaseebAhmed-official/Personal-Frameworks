#!/usr/bin/env python3
"""
POST-COMPACT HOOK
=================
Fires AFTER context auto-compaction.

After compaction, Claude loses detailed context. This hook re-injects a summary
of the session state so Claude knows what it was doing and can resume work.

The output of this hook appears directly in the conversation.
"""

from common import load_payload, emit, read_session_state


def main() -> int:
    """Re-inject session state summary after compaction."""
    # Load payload (not needed, but consume it)
    _payload = load_payload()

    # Read session state
    state = read_session_state()

    # Build summary message
    lines = []
    lines.append('--- SESSION STATE RESTORED AFTER COMPACTION ---')

    task = state.get('task', 'Unknown task')
    lines.append(f'Task: {task}')

    progress = state.get('progress', 'No progress recorded')
    lines.append(f'Progress: {progress}')

    decisions = state.get('decisions', [])
    if decisions:
        decision_str = '; '.join(str(d) for d in decisions[:5])
        lines.append(f'Key decisions: {decision_str}')

    active_files = state.get('active_files', [])
    if active_files:
        files_str = ', '.join(str(f) for f in active_files[:8])
        lines.append(f'Active files: {files_str}')

    next_steps = state.get('next_steps', [])
    if next_steps:
        steps_str = '; '.join(str(s) for s in next_steps[:5])
        lines.append(f'Next steps: {steps_str}')

    plan_file = state.get('plan_file', '')
    if plan_file:
        lines.append(f'Full plan: {plan_file}')

    lines.append('--- END STATE ---')
    lines.append('Continue from where you left off. Update session-state.json as you make progress.')

    # Emit as system message that appears in conversation
    message = '\n'.join(lines)
    return emit({
        'continue': True,
        'systemMessage': message
    })


if __name__ == '__main__':
    raise SystemExit(main())
