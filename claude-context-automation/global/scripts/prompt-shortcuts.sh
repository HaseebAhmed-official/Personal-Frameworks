#!/bin/bash
# Prompt Shortcuts — Expands short aliases into full skill invocations
# Triggered by UserPromptSubmit hook. Reads the user's prompt from stdin.
# If it matches a shortcut, outputs a JSON response that rewrites the prompt.
#
# Why: Keybindings can't trigger skills. This gives the same speed —
# type "!fw" instead of "/fw", "!mc" instead of "/memory-cleanup", etc.
# The "!" prefix avoids conflicts with slash commands.

# Read hook input from stdin
HOOK_INPUT=$(cat 2>/dev/null)

# Extract the user's prompt text
if command -v jq &>/dev/null && [ -n "$HOOK_INPUT" ]; then
    PROMPT=$(echo "$HOOK_INPUT" | jq -r '.message.content // .prompt // ""' 2>/dev/null)
else
    PROMPT=""
fi

# Trim whitespace
PROMPT=$(echo "$PROMPT" | xargs 2>/dev/null)

# Match shortcuts and rewrite
case "$PROMPT" in
    "!fw"|"!fw "*)
        # Extract argument after !fw (e.g., "!fw 2" → "2")
        ARG="${PROMPT#!fw}"
        ARG=$(echo "$ARG" | xargs 2>/dev/null)
        if [ -n "$ARG" ]; then
            echo "{\"message\": \"/fw $ARG\"}"
        else
            echo "{\"message\": \"/fw\"}"
        fi
        ;;
    "!mc")
        echo "{\"message\": \"/memory-cleanup\"}"
        ;;
    "!fs")
        echo "{\"message\": \"/framework-status\"}"
        ;;
    "!sr")
        echo "{\"message\": \"/session-review\"}"
        ;;
esac

exit 0
