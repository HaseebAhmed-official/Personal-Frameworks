#!/usr/bin/env python3
from common import emit


MESSAGE = (
    "Project framework active. Load CLAUDE.md, RULES.md, MEMORY.md, and docs/framework/*. "
    "Keep the main thread compact. Use TodoWrite for active work. "
    "Get explicit approval before durable memory writes, framework edits, reusable component creation, or agent team launch."
)


if __name__ == "__main__":
    raise SystemExit(emit({"continue": True, "systemMessage": MESSAGE}))
