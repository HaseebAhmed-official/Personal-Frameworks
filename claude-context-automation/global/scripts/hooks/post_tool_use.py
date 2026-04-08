#!/usr/bin/env python3
"""
POST TOOL USE HOOK
==================
Fires AFTER Claude Code tools: Edit, Write, MultiEdit, Bash

This hook:
1. Tracks file edits to edit-tracker.jsonl (for all Write/Edit/MultiEdit)
2. Tracks git commits to git-tracker.jsonl (for git commit commands in Bash)
3. Reminds Claude to refresh session state after mutations
"""

import json
import subprocess
import os
from pathlib import Path
from common import (
    load_payload, emit, append_to_log, trim_log_file,
    get_session_logs_dir, get_current_time_iso, extract_file_path,
    extract_command
)


def log_file_edit(tool_name: str, file_path: str) -> bool:
    """Log file edit to edit-tracker.jsonl.

    Args:
        tool_name: Edit, Write, or MultiEdit
        file_path: Path to file that was edited

    Returns:
        bool: True if successful
    """
    log_dir = get_session_logs_dir()
    log_file = log_dir / 'edit-tracker.jsonl'

    entry = {
        'ts': get_current_time_iso(),
        'tool': tool_name,
        'file': file_path,
        'project': os.getcwd()
    }

    if append_to_log(log_file, entry):
        # Keep last 500 entries
        trim_log_file(log_file, 500)
        return True

    return False


def log_git_commit() -> bool:
    """Log git commit to git-tracker.jsonl.

    Calls `git log -1` to get latest commit info.

    Returns:
        bool: True if successfully logged commit
    """
    log_dir = get_session_logs_dir()
    log_file = log_dir / 'git-tracker.jsonl'

    try:
        # Get latest commit info
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%h%n%s%n%(refname:short)'],
            capture_output=True, text=True, timeout=2
        )

        if result.returncode != 0:
            return False

        lines = result.stdout.strip().split('\n')
        if len(lines) < 3:
            return False

        commit_hash, commit_msg, branch = lines[0], lines[1], lines[2]

        entry = {
            'ts': get_current_time_iso(),
            'hash': commit_hash,
            'msg': commit_msg,
            'branch': branch,
            'project': os.getcwd()
        }

        if append_to_log(log_file, entry):
            # Keep last 200 entries
            trim_log_file(log_file, 200)
            return True

    except Exception:
        pass

    return False


def main() -> int:
    """Track file edits and git commits."""
    payload = load_payload()

    tool_name = payload.get('toolName', '')
    tool_input = payload.get('toolInput', {})

    # Track file edits for Write/Edit/MultiEdit
    if tool_name in ('Write', 'Edit', 'MultiEdit'):
        file_path = extract_file_path(tool_input)
        if file_path:
            log_file_edit(tool_name, file_path)

    # Track git commits (only if Bash tool executed a git commit command)
    if tool_name == 'Bash':
        command = extract_command(tool_input)
        if command and 'git commit' in command:
            log_git_commit()

    # Remind Claude to refresh state ledger after mutations
    message = (
        '**State Ledger Update**: After writing/editing, refresh session-state.json with:\n'
        '- decisions made\n'
        '- files affected\n'
        '- risks introduced\n'
        '- next action'
    )

    return emit({
        'continue': True,
        'systemMessage': message
    })


if __name__ == '__main__':
    raise SystemExit(main())
