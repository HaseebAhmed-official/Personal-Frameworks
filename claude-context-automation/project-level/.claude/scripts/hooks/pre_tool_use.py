#!/usr/bin/env python3
from common import emit, load_payload


FRAMEWORK_FILES = {
    "CLAUDE.md",
    "RULES.md",
    "MEMORY.md",
    ".claude/settings.json",
}


def main() -> int:
    payload = load_payload()
    tool_name = payload.get("toolName", "")
    tool_input = payload.get("toolInput", {})
    paths = []

    if isinstance(tool_input, dict):
        for key in ("file_path", "path", "paths"):
            value = tool_input.get(key)
            if isinstance(value, str):
                paths.append(value)
            elif isinstance(value, list):
                paths.extend(str(item) for item in value)

    touched = [p for p in paths if any(p.endswith(name) for name in FRAMEWORK_FILES)]
    if touched and tool_name in {"Write", "Edit", "MultiEdit"}:
        return emit(
            {
                "continue": True,
                "systemMessage": (
                    "You are editing framework-governed files. Confirm the user explicitly approved "
                    "this category of change and keep the update minimal and auditable."
                ),
            }
        )

    return emit({"continue": True})


if __name__ == "__main__":
    raise SystemExit(main())
