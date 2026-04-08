#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict


def load_payload() -> Dict[str, Any]:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def emit(payload: Dict[str, Any]) -> int:
    sys.stdout.write(json.dumps(payload))
    return 0
