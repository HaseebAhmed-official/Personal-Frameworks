#!/usr/bin/env python3
"""
NOTIFICATION HOOK
=================
Fires for framework events and periodic checks.

This hook:
1. Reminds user if memory audit is overdue (>7 days)
2. Checks for pending approvals
3. Monitors context pressure
"""

from pathlib import Path
from datetime import datetime, timezone, timedelta
from common import load_payload, emit, get_home_dir, get_current_time_iso


def get_audit_marker_file() -> Path:
    """Get path to last-memory-audit marker file.

    Returns:
        Path: ~/.claude/session-logs/.last-memory-audit
    """
    return get_home_dir() / '.claude' / 'session-logs' / '.last-memory-audit'


def check_memory_audit_overdue() -> bool:
    """Check if memory audit is overdue (>7 days).

    Returns:
        bool: True if overdue, False if recent
    """
    marker = get_audit_marker_file()

    if not marker.exists():
        # First run — create marker but don't nag yet
        try:
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text(get_current_time_iso())
        except Exception:
            pass
        return False

    try:
        timestamp_str = marker.read_text().strip()
        audit_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        age = now - audit_time

        return age > timedelta(days=7)
    except Exception:
        return False


def main() -> int:
    """Check framework health and emit reminders."""
    payload = load_payload()

    reminders = []

    # Check memory audit status
    if check_memory_audit_overdue():
        reminders.append(
            '⚠️ **Memory Audit Overdue**: Last audit was >7 days ago. '
            'Run `/memory-cleanup` to clean up stale/duplicate entries.'
        )

    # Could add more checks here in future:
    # - Pending approvals
    # - Context pressure warnings
    # - Framework validation failures

    if reminders:
        message = '\n\n'.join(reminders)
        return emit({
            'continue': True,
            'systemMessage': message
        })

    return emit({'continue': True})


if __name__ == '__main__':
    raise SystemExit(main())
