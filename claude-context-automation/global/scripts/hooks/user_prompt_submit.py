#!/usr/bin/env python3
"""
USER PROMPT SUBMIT HOOK
=======================
Fires when the user submits a message (before Claude processes it).

This hook:
1. Expands prompt shortcuts (!fw, !mc, !fs, !sr → /fw, /memory-cleanup, etc.)
2. Adds governance reminders if user mentions "agent team" or "memory"
3. Provides base framework context reminder
"""

from common import load_payload, emit


def extract_prompt(payload: dict) -> str:
    """Extract user's prompt text from payload.

    Args:
        payload: Hook payload from harness

    Returns:
        str: User's prompt text, or empty string
    """
    # Try multiple field paths
    if isinstance(payload.get('message'), dict):
        return payload['message'].get('content', '').strip()

    if isinstance(payload.get('message'), str):
        return payload['message'].strip()

    return payload.get('prompt', '').strip()


def expand_shortcut(prompt: str) -> str:
    """Expand prompt shortcuts to full commands.

    Args:
        prompt: User's prompt text

    Returns:
        str: Expanded prompt if matched, otherwise original
    """
    prompt = prompt.strip()

    if prompt.startswith('!fw'):
        # Extract argument after !fw (e.g., "!fw 2" → "2")
        arg = prompt[3:].strip()
        return f'/fw {arg}' if arg else '/fw'

    if prompt == '!mc':
        return '/memory-cleanup'

    if prompt == '!fs':
        return '/framework-status'

    if prompt == '!sr':
        return '/session-review'

    return prompt


def main() -> int:
    """Process prompt: expand shortcuts and add reminders."""
    payload = load_payload()
    prompt = extract_prompt(payload)

    if not prompt:
        return emit({'continue': True})

    # === Step 1: Expand shortcuts ===
    expanded_prompt = expand_shortcut(prompt)

    # If prompt was rewritten, emit rewrite
    if expanded_prompt != prompt:
        return emit({'message': expanded_prompt})

    # === Step 2: Add governance reminders based on content ===
    reminders = []

    if 'agent team' in prompt.lower():
        reminders.append(
            '**Agent Teams Note**: Experimental feature. Creating an agent team requires explicit '
            'user approval. Use `/teams:research-team` or `/teams:verification-team` with explicit consent.'
        )

    if 'memory' in prompt.lower() or 'remember' in prompt.lower():
        reminders.append(
            '**Memory Note**: Durable memory cannot be auto-written. Use `/governance:memory-proposal` to '
            'review candidates, then get explicit user approval before writing to MEMORY.md.'
        )

    # === Step 3: Emit response ===
    if reminders:
        reminder_text = '\n\n'.join(reminders)
        return emit({
            'continue': True,
            'systemMessage': reminder_text
        })

    # No special handling needed — continue normally
    return emit({'continue': True})


if __name__ == '__main__':
    raise SystemExit(main())
