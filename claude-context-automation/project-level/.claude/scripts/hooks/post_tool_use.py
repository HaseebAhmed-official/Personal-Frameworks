#!/usr/bin/env python3
from common import emit, load_payload


def main() -> int:
    payload = load_payload()
    tool_name = payload.get("toolName", "")
    if tool_name in {"Write", "Edit", "MultiEdit"}:
        return emit(
            {
                "continue": True,
                "systemMessage": (
                    "A write just occurred. Refresh the state ledger: decisions made, files affected, "
                    "risks introduced, and next action."
                ),
            }
        )
    return emit({"continue": True})


if __name__ == "__main__":
    raise SystemExit(main())
