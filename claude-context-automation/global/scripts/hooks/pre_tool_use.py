#!/usr/bin/env python3
"""
PRE TOOL USE HOOK
=================
Fires BEFORE any tool execution (Read, Write, Edit, Bash, etc.)

This hook:
1. Detects attempts to edit framework governance files
2. Requires confirmation that the user explicitly approved the change
3. Prevents accidental corruption of CLAUDE.md, RULES.md, MEMORY.md, settings.json
"""

from common import load_payload, emit


FRAMEWORK_FILES = {
    'CLAUDE.md',
    'RULES.md',
    'MEMORY.md',
    '.claude/settings.json',
    '.claude/settings.local.json',
}


def extract_tool_info(payload: dict) -> tuple:
    """Extract tool name and file paths from payload.

    Args:
        payload: Hook payload from harness

    Returns:
        tuple: (tool_name, list_of_paths)
    """
    tool_name = payload.get('toolName', '')
    tool_input = payload.get('toolInput', {})

    paths = []

    if isinstance(tool_input, dict):
        for key in ('file_path', 'path', 'paths'):
            value = tool_input.get(key)
            if isinstance(value, str):
                paths.append(value)
            elif isinstance(value, list):
                paths.extend(str(item) for item in value)

    return tool_name, paths


def is_framework_file(path: str) -> bool:
    """Check if path refers to a framework governance file.

    Args:
        path: File path

    Returns:
        bool: True if path ends with a framework file name
    """
    for framework_file in FRAMEWORK_FILES:
        if path.endswith(framework_file):
            return True
    return False


def main() -> int:
    """Intercept framework file edits and require confirmation."""
    payload = load_payload()

    tool_name, paths = extract_tool_info(payload)

    # Check if any touched file is a framework file
    touched_framework_files = [p for p in paths if is_framework_file(p)]

    # Only gate Write/Edit/MultiEdit tools
    if touched_framework_files and tool_name in ('Write', 'Edit', 'MultiEdit'):
        return emit({
            'continue': True,
            'systemMessage': (
                f'**Framework File Edit Gate**: You are about to edit governance files: '
                f'{", ".join(touched_framework_files)}.\n\n'
                f'**Requirement**: Confirm that the user explicitly approved this change. '
                f'Keep the update minimal and auditable. Document the reason.'
            )
        })

    # All other operations pass through
    return emit({'continue': True})


if __name__ == '__main__':
    raise SystemExit(main())
