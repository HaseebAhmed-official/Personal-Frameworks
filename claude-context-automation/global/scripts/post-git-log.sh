#!/bin/bash
# Post-Git Log — Updates project memory after git commits
# Triggered by PostToolUse hook after Bash tool runs git commit
# Records commit info so future sessions know what was done
# Hook system passes JSON via stdin with tool_name, tool_input, etc.

LOG_DIR="$HOME/.claude/session-logs"
LOG_FILE="$LOG_DIR/git-tracker.jsonl"

mkdir -p "$LOG_DIR"

# Read hook input from stdin (JSON with tool_name, tool_input fields)
HOOK_INPUT=$(cat 2>/dev/null)

# Extract tool name and command from stdin JSON
if command -v jq &>/dev/null && [ -n "$HOOK_INPUT" ]; then
    TOOL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_name // .toolName // "unknown"' 2>/dev/null)
    COMMAND=$(echo "$HOOK_INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null)
else
    # Fallback: try env vars
    TOOL_NAME="${CLAUDE_TOOL_NAME:-unknown}"
    if [ -n "$HOOK_INPUT" ]; then
        COMMAND=$(echo "$HOOK_INPUT" | grep -oP '"command"\s*:\s*"[^"]*"' | head -1 | grep -oP ':\s*"\K[^"]+')
    else
        COMMAND=""
    fi
fi

# Only proceed if this was a git commit command
echo "$COMMAND" | grep -q "git commit" || exit 0

# Check if we're in a git repo
git rev-parse --is-inside-work-tree &>/dev/null || exit 0

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
PROJECT_DIR=$(pwd)

# Get latest commit info
COMMIT_HASH=$(git log -1 --format="%h" 2>/dev/null || echo "unknown")
COMMIT_MSG=$(git log -1 --format="%s" 2>/dev/null || echo "unknown")
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

# Append to JSONL log
echo "{\"ts\":\"$TIMESTAMP\",\"hash\":\"$COMMIT_HASH\",\"msg\":\"$COMMIT_MSG\",\"branch\":\"$BRANCH\",\"project\":\"$PROJECT_DIR\"}" >> "$LOG_FILE"

# Keep last 200 entries
if [ -f "$LOG_FILE" ]; then
    LINE_COUNT=$(wc -l < "$LOG_FILE")
    if [ "$LINE_COUNT" -gt 200 ]; then
        tail -n 200 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
    fi
fi

exit 0
