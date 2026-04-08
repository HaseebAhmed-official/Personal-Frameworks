#!/usr/bin/env python3
from common import emit


if __name__ == "__main__":
    raise SystemExit(
        emit(
            {
                "continue": True,
                "systemMessage": (
                    "Subagent outputs must stay concise and include findings, risks, and recommended next action."
                ),
            }
        )
    )
