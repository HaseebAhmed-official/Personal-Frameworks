#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    cwd = Path(payload.get("workspace", os.getcwd())).name
    model = payload.get("model", "?")
    output_style = payload.get("outputStyle", "default")
    session_mode = payload.get("permissionMode", "default")
    cost = payload.get("cost", {})
    total_cost = cost.get("totalCostUsd")

    cost_fragment = ""
    if total_cost is not None:
        cost_fragment = f" | ${total_cost:.2f}"

    line = f"{cwd} | {model} | {output_style} | {session_mode}{cost_fragment}"
    sys.stdout.write(line[:140])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
