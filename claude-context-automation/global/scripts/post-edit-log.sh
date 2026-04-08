#!/bin/bash
# Post-Edit Log — Tracks file edits made during the session
# Triggered by PostToolUse hook after Edit/Write tools
# Keeps a lightweight log of what files were changed and when
# Hook system passes JSON via stdin with tool_name, tool_input, etc.

LOG_DIR="$HOME/.claude/session-logs"
LOG_FILE="$LOG_DIR/edit-tracker.jsonl"

mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
PROJECT_DIR=$(pwd)

# Read hook input from stdin (JSON with tool_name, tool_input fields)
HOOK_INPUT=$(cat 2>/dev/null)

# Extract tool name and file path from stdin JSON
if command -v jq &>/dev/null && [ -n "$HOOK_INPUT" ]; then
    TOOL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_name // .toolName // "unknown"' 2>/dev/null)
    FILE_PATH=$(echo "$HOOK_INPUT" | jq -r '.tool_input.file_path // .tool_input.path // "unknown"' 2>/dev/null)
else
    # Fallback: try env vars, then default to unknown
    TOOL_NAME="${CLAUDE_TOOL_NAME:-unknown}"
    if [ -n "$HOOK_INPUT" ]; then
        FILE_PATH=$(echo "$HOOK_INPUT" | grep -oP '"file_path"\s*:\s*"[^"]*"' | head -1 | grep -oP ':\s*"\K[^"]+')
    fi
    [ -z "$FILE_PATH" ] && FILE_PATH="unknown"
fi

# Append to JSONL log (one line per edit, stays small)
echo "{\"ts\":\"$TIMESTAMP\",\"tool\":\"$TOOL_NAME\",\"file\":\"$FILE_PATH\",\"project\":\"$PROJECT_DIR\"}" >> "$LOG_FILE"

# Keep log from growing forever — retain last 500 entries
if [ -f "$LOG_FILE" ]; then
    LINE_COUNT=$(wc -l < "$LOG_FILE")
    if [ "$LINE_COUNT" -gt 500 ]; then
        tail -n 500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
    fi
fi

exit 0
