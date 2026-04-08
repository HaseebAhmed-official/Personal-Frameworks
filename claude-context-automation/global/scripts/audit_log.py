#!/usr/bin/env python3
"""
AUDIT LOG
=========
Initialize and append to the framework audit trail.

Creates or appends to ~/.claude/session-logs/audit-log.jsonl.
Each entry records: timestamp, event_type, actor, component, status, details.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone


def get_audit_log_file() -> Path:
    return Path.home() / ".claude" / "session-logs" / "audit-log.jsonl"


def append_event(event_type: str, actor: str, component: str, status: str, details: dict = None) -> Path:
    """Append a single event to the audit log.

    Args:
        event_type: What happened (e.g., 'validation_run', 'memory_write')
        actor: Who caused it (e.g., 'claude-hook', 'user', 'validate_script')
        component: Which component (e.g., 'framework', 'memory', 'session')
        status: Outcome (e.g., 'success', 'failure', 'skipped')
        details: Optional dict with additional context

    Returns:
        Path: Path to audit log file
    """
    log_file = get_audit_log_file()
    log_file.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "event_type": event_type,
        "actor": actor,
        "component": component,
        "status": status,
        "details": details or {}
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return log_file


def seed_validation(checks_passed: int, checks_total: int) -> Path:
    """Record a framework validation run."""
    return append_event(
        event_type="validation_seed",
        actor="validate_script",
        component="framework",
        status="success" if checks_passed == checks_total else "partial",
        details={
            "checks_passed": checks_passed,
            "checks_total": checks_total,
            "pass_rate": f"{checks_passed}/{checks_total}"
        }
    )


if __name__ == "__main__":
    # Default: seed a validation event when called directly
    log_file = append_event(
        event_type="validation_seed",
        actor="local-script",
        component="framework",
        status="success",
        details={"message": "audit log initialized"}
    )
    print(f"Audit log: {log_file}")
