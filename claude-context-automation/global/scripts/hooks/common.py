#!/usr/bin/env python3
"""
Shared utilities for all Claude Code framework hooks.

This module provides common functions for:
- JSON payload I/O between Claude Code harness and hooks
- File operations (reading/writing session state, logs)
- Date/time utilities
- Error handling with fail-safe defaults
"""

import json
import sys
import os
from typing import Any, Dict, Optional
from datetime import datetime, timezone
from pathlib import Path


def load_payload() -> Dict[str, Any]:
    """Load JSON payload from stdin (sent by Claude Code harness).

    Returns:
        dict: Parsed JSON payload, or empty dict if parsing fails
    """
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError, EOFError):
        return {}


def emit(payload: Dict[str, Any]) -> int:
    """Emit JSON response to stdout (read by Claude Code harness).

    Args:
        payload: Dictionary to send back to harness

    Returns:
        int: Exit code (always 0 to never block Claude Code)
    """
    try:
        sys.stdout.write(json.dumps(payload))
        sys.stdout.flush()
    except Exception:
        pass  # Never fail — hooks must be fail-safe
    return 0


def get_home_dir() -> Path:
    """Get user's home directory.

    Returns:
        Path: Home directory path
    """
    return Path.home()


def get_session_state_file() -> Path:
    """Get path to session-state.json.

    Returns:
        Path: Full path to session-state.json
    """
    return get_home_dir() / ".claude" / "session-state.json"


def get_session_logs_dir() -> Path:
    """Get path to session-logs directory.

    Returns:
        Path: Full path to session-logs directory
    """
    return get_home_dir() / ".claude" / "session-logs"


def read_session_state() -> Dict[str, Any]:
    """Read current session-state.json.

    Returns:
        dict: Parsed session state, or empty dict if file missing/invalid
    """
    state_file = get_session_state_file()
    if not state_file.exists():
        return {}

    try:
        with open(state_file, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def write_session_state(state: Dict[str, Any]) -> bool:
    """Write session-state.json atomically.

    Args:
        state: Dictionary to write

    Returns:
        bool: True if successful, False otherwise
    """
    state_file = get_session_state_file()
    try:
        # Ensure directory exists
        state_file.parent.mkdir(parents=True, exist_ok=True)

        # Write atomically to temp file then rename
        temp_file = state_file.with_suffix('.json.tmp')
        with open(temp_file, 'w') as f:
            json.dump(state, f, indent=2)
        temp_file.replace(state_file)
        return True
    except Exception:
        return False


def append_to_log(log_file: Path, entry: Dict[str, Any]) -> bool:
    """Append JSON entry to JSONL log file.

    Args:
        log_file: Path to JSONL file
        entry: Dictionary to append as JSON line

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        return True
    except Exception:
        return False


def trim_log_file(log_file: Path, max_lines: int) -> bool:
    """Keep only last N lines of JSONL log file.

    Args:
        log_file: Path to JSONL file
        max_lines: Maximum number of lines to keep

    Returns:
        bool: True if successful or file didn't need trimming
    """
    try:
        if not log_file.exists():
            return True

        with open(log_file, 'r') as f:
            lines = f.readlines()

        if len(lines) <= max_lines:
            return True

        # Keep last max_lines entries
        with open(log_file, 'w') as f:
            f.writelines(lines[-max_lines:])
        return True
    except Exception:
        return False


def get_current_time_iso() -> str:
    """Get current UTC time in ISO 8601 format.

    Returns:
        str: Timestamp like "2026-04-08T12:34:56Z"
    """
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def extract_file_path(tool_input: Any) -> Optional[str]:
    """Extract file_path from tool input (handles multiple field names).

    Args:
        tool_input: Tool input dict from payload

    Returns:
        str: File path, or None if not found
    """
    if not isinstance(tool_input, dict):
        return None

    # Try multiple field name variations
    for key in ('file_path', 'path', 'paths'):
        value = tool_input.get(key)
        if isinstance(value, str):
            return value
        elif isinstance(value, list) and value:
            return str(value[0])

    return None


def extract_command(tool_input: Any) -> Optional[str]:
    """Extract bash command from tool input.

    Args:
        tool_input: Tool input dict from payload

    Returns:
        str: Command string, or None if not found
    """
    if not isinstance(tool_input, dict):
        return None

    value = tool_input.get('command')
    return str(value) if value else None
