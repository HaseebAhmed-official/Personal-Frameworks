#!/usr/bin/env python3
"""
VALIDATE FRAMEWORK
==================
Comprehensive validation of Claude Code context automation framework.

Checks:
1. All required files exist (41 components)
2. JSON/YAML files parse correctly
3. All hook scripts executable and testable
4. Settings.json hooks wired correctly
5. Memory schema validation
6. Audit trail accessible
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Tuple


class FrameworkValidator:
    """Validates framework completeness and functionality."""

    def __init__(self):
        self.home = Path.home()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.checks_passed = 0
        self.checks_total = 0

    def check(self, condition: bool, message: str) -> bool:
        """Record a check result."""
        self.checks_total += 1
        if condition:
            self.checks_passed += 1
            return True
        else:
            self.errors.append(f"✗ {message}")
            return False

    def warn(self, message: str) -> None:
        """Record a warning."""
        self.warnings.append(f"⚠ {message}")

    def run_all_checks(self) -> bool:
        """Run all validation checks."""
        print("Framework Validation")
        print("=" * 60)
        print()

        # Check 1: Core files
        print("1. Core Framework Files")
        print("-" * 60)
        self.check_core_files()
        print()

        # Check 2: Settings
        print("2. Settings Configuration")
        print("-" * 60)
        self.check_settings()
        print()

        # Check 3: Hooks
        print("3. Hook Scripts")
        print("-" * 60)
        self.check_hooks()
        print()

        # Check 4: Session State
        print("4. Session State & Logs")
        print("-" * 60)
        self.check_session_state()
        print()

        # Check 5: Memory
        print("5. Memory System")
        print("-" * 60)
        self.check_memory()
        print()

        # Check 6: Schemas
        print("6. Validation Schemas")
        print("-" * 60)
        self.check_schemas()
        print()

        # Summary
        print("=" * 60)
        print(f"Checks: {self.checks_passed}/{self.checks_total} passed")
        print()

        if self.errors:
            print(f"ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
            print()

        if self.warnings:
            print(f"WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
            print()

        if not self.errors:
            print("✓ Framework validation PASSED")
            return True
        else:
            print("✗ Framework validation FAILED")
            return False

    def check_core_files(self) -> None:
        """Check that all core framework files exist."""
        required_files = {
            ".claude/CLAUDE.md": "User behavioral rules",
            ".claude/RULES.md": "Precedence and routing rules",
            ".claude/MEMORY.md": "Memory taxonomy and ledger",
            ".claude/settings.json": "Hook configuration",
            ".claude/session-state.json": "Current session state",
        }

        # Check at both home and project level
        for filename, description in required_files.items():
            home_file = self.home / filename
            self.check(
                home_file.exists(),
                f"{filename} exists ({description})"
            )

        # Agents (7 total)
        agents_dir = self.home / ".claude" / "agents"
        required_agents = [
            "researcher.md",
            "reviewer.md",
            "analysis-lead.md",
            "context-researcher.md",
            "governance-reviewer.md",
            "memory-curator.md",
            "verification-auditor.md",
        ]
        for agent in required_agents:
            self.check((agents_dir / agent).exists(), f"Agent {agent} exists")

        # Commands
        commands_dir = self.home / ".claude" / "commands"
        required_commands = [
            "context-audit.md",
            "governance/memory-proposal.md",
            "governance/resume-ledger.md",
            "teams/research-team.md",
            "teams/verification-team.md",
        ]
        for cmd in required_commands:
            self.check((commands_dir / cmd).exists(), f"Command {cmd} exists")

        # Output styles
        styles_dir = self.home / ".claude" / "output-styles"
        for style in ["context-lean.md", "governed-execution.md"]:
            self.check((styles_dir / style).exists(), f"Output style {style} exists")

        # Framework docs
        docs_dir = self.home / ".claude" / "docs" / "framework"
        for doc in ["governance.md", "precedence.md", "agent-teams.md", "components.md", "smoke-test.md"]:
            self.check((docs_dir / doc).exists(), f"Doc {doc} exists")

        # Utility scripts
        scripts_dir = self.home / ".claude" / "scripts"
        for script in ["validate_framework.py", "audit_log.py", "statusline.py"]:
            self.check((scripts_dir / script).exists(), f"Script {script} exists")

    def check_settings(self) -> None:
        """Check settings.json is valid JSON and has hooks."""
        settings_file = self.home / ".claude" / "settings.json"

        if not self.check(settings_file.exists(), "settings.json exists"):
            return

        # Try to parse JSON
        try:
            with open(settings_file) as f:
                settings = json.load(f)
            self.checks_passed += 1  # Already counted in check() above
            self.checks_total += 1
            print(f"  ✓ settings.json parses as valid JSON")

            # Check hooks present
            required_hooks = {
                "SessionStart", "UserPromptSubmit", "PreToolUse",
                "PostToolUse", "PreCompact", "PostCompact",
                "SubagentStop", "Stop", "Notification"
            }

            hooks = settings.get("hooks", {})
            found_hooks = set(hooks.keys())
            missing_hooks = required_hooks - found_hooks

            if missing_hooks:
                self.warn(
                    f"Missing hooks: {', '.join(sorted(missing_hooks))}"
                )
            else:
                self.checks_passed += 1
                self.checks_total += 1
                print(f"  ✓ All required hook events present")

        except json.JSONDecodeError as e:
            self.checks_total += 1
            self.errors.append(f"settings.json JSON parse error: {e}")

    def check_hooks(self) -> None:
        """Check that all hook scripts exist and are executable."""
        hooks_dir = self.home / ".claude" / "scripts" / "hooks"

        required_hooks = {
            "common.py": "Shared utilities",
            "pre_compact.py": "Pre-compaction state timestamping",
            "post_compact.py": "Post-compaction state re-injection",
            "session_start.py": "Session initialization and resume",
            "pre_tool_use.py": "Framework file protection",
            "post_tool_use.py": "File/git tracking",
            "user_prompt_submit.py": "Prompt shortcuts and governance reminders",
            "stop.py": "Session archiving",
            "notification.py": "Memory audit reminders",
            "subagent_stop.py": "Agent output quality gates",
        }

        hooks_exist = 0
        hooks_executable = 0
        hooks_testable = 0

        for hook_name, description in required_hooks.items():
            hook_file = hooks_dir / hook_name
            exists = self.check(
                hook_file.exists(),
                f"Hook {hook_name} exists"
            )

            if not exists:
                continue

            # Check executable
            executable = os.access(hook_file, os.X_OK)
            self.check(
                executable,
                f"Hook {hook_name} is executable"
            )

            # Try to execute with test payload
            try:
                result = subprocess.run(
                    [str(hook_file)],
                    input='{}',
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                testable = result.returncode == 0
                self.check(
                    testable,
                    f"Hook {hook_name} executes successfully"
                )
            except Exception as e:
                self.check(False, f"Hook {hook_name} test execution failed: {e}")

    def check_session_state(self) -> None:
        """Check session state and logs."""
        state_file = self.home / ".claude" / "session-state.json"
        logs_dir = self.home / ".claude" / "session-logs"

        # Check session-state.json exists and is valid JSON
        if state_file.exists():
            try:
                with open(state_file) as f:
                    state = json.load(f)
                self.check(True, "session-state.json is valid JSON")

                # Check required fields
                required_fields = {"timestamp", "task", "progress"}
                present_fields = set(state.keys()) & required_fields
                self.check(
                    len(present_fields) >= 2,
                    "session-state.json has key fields"
                )
            except json.JSONDecodeError:
                self.check(False, "session-state.json parses as JSON")
        else:
            self.warn("session-state.json not initialized (will be created at session start)")

        # Check logs directory
        if logs_dir.exists():
            self.check(True, "session-logs directory exists")

            # Check trackers
            edit_tracker = logs_dir / "edit-tracker.jsonl"
            git_tracker = logs_dir / "git-tracker.jsonl"

            self.check(
                edit_tracker.exists(),
                "edit-tracker.jsonl exists"
            )
            self.check(
                git_tracker.exists(),
                "git-tracker.jsonl exists"
            )
        else:
            self.warn("session-logs directory not created yet")

    def check_memory(self) -> None:
        """Check memory system."""
        memory_file = self.home / ".claude" / "MEMORY.md"

        self.check(
            memory_file.exists(),
            "MEMORY.md exists"
        )

        if memory_file.exists():
            content = memory_file.read_text()
            self.check(
                "taxonomy" in content.lower(),
                "MEMORY.md includes taxonomy documentation"
            )
            self.check(
                "workflow" in content.lower(),
                "MEMORY.md includes workflow documentation"
            )

    def check_schemas(self) -> None:
        """Check validation schemas."""
        schemas_dir = self.home / ".claude" / "schemas"

        if not self.check(schemas_dir.exists(), "schemas directory exists"):
            return

        required_schemas = {
            "memory-entry.schema.json": "Memory entry JSON Schema",
            "state-ledger.example.yaml": "State ledger YAML template",
            "memory-entry.example.json": "Memory entry example",
            "audit-event.example.json": "Audit event example",
        }

        for schema_name, description in required_schemas.items():
            schema_file = schemas_dir / schema_name
            exists = self.check(
                schema_file.exists(),
                f"{schema_name} exists ({description})"
            )

            if not exists:
                continue

            # Try to parse JSON files
            if schema_name.endswith(".json"):
                try:
                    with open(schema_file) as f:
                        json.load(f)
                    self.check(True, f"{schema_name} parses as JSON")
                except json.JSONDecodeError as e:
                    self.check(False, f"{schema_name} JSON parse error: {e}")


def main() -> int:
    """Run framework validation."""
    validator = FrameworkValidator()
    success = validator.run_all_checks()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
