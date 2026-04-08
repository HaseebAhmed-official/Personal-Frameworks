#!/usr/bin/env python3
from common import emit, load_payload


def build_message(prompt: str) -> str:
    base = (
        "Apply the context-orchestration framework. Prefer targeted context, summarize exploration, "
        "and keep only decisions, blockers, approvals, and next action in the main thread."
    )
    lower = prompt.lower()
    if "agent team" in lower or "agent teams" in lower:
        base += " Agent teams are experimental and require explicit user approval before creation."
    if "memory" in lower or "remember" in lower:
        base += " Durable memory can be proposed, but not written automatically."
    return base


if __name__ == "__main__":
    payload = load_payload()
    prompt = payload.get("prompt", "")
    raise SystemExit(emit({"continue": True, "systemMessage": build_message(prompt)}))
