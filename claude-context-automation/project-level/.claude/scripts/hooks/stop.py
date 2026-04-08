#!/usr/bin/env python3
from common import emit


if __name__ == "__main__":
    raise SystemExit(
        emit(
            {
                "continue": True,
                "systemMessage": (
                    "Before stopping, ensure the state ledger is clear and durable memory has not been "
                    "written without explicit approval."
                ),
            }
        )
    )
