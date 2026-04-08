---
name: framework-status
description: >
  Diagnostic skill that validates all framework components are installed and working correctly.
  Checks hook scripts, memory system, session state, settings, and reports any issues.
  Trigger: /framework-status or when something seems wrong with the framework.
---

# Framework Status Diagnostic

You are running a health check on the Context & Workflow Management Framework.
Check every component and report status clearly.

## Run These Checks

### 1. Hook Scripts
For each script in `~/.claude/scripts/`, verify:
- File exists
- File is executable (`-x` permission)
- File runs without error (execute with `bash <script> 2>&1; echo "exit:$?"`)

Expected scripts:
- `pre-compact.sh` — saves state before compaction
- `post-compact.sh` — restores state after compaction
- `session-start.sh` — offers resume on new session
- `session-end.sh` — archives session on exit

### 2. Settings.json Hooks
Read `~/.claude/settings.json` and verify hooks section contains:
- PreCompact hook pointing to pre-compact.sh
- PostCompact hook pointing to post-compact.sh
- Notification hook pointing to session-start.sh (or SessionStart if available)
- Stop hook pointing to session-end.sh

### 3. Session State
Check `~/.claude/session-state.json`:
- Exists? If yes, show last update timestamp and task
- Is it fresh (<24 hours)? Mark stale if older
- Valid JSON? Flag if corrupted

### 4. Memory System
Check the project memory directory:
- Count memory files
- List them with their types (user/feedback/project/reference)
- Check MEMORY.md exists and is under 200 lines
- Flag any memories older than 30 days as potentially stale

### 5. Session Logs
Check `~/.claude/session-logs/`:
- Count total session logs
- Show most recent 3 with dates
- Flag if >50 logs (suggest cleanup)

### 6. CLAUDE.md Framework Rules
Read `~/.claude/CLAUDE.md` and verify it contains:
- "Context & Workflow Management Framework" section
- Sub-agent delegation rules
- Memory management rules
- Tiered approval system
- Pattern detection rules

### 7. PostToolUse Hooks (Phase 3)
Check `~/.claude/settings.json` for PostToolUse entries:
- Edit/Write hook → `post-edit-log.sh` exists and is executable
- Bash hook → `post-git-log.sh` exists and is executable
- Check `~/.claude/session-logs/edit-tracker.jsonl` — exists? how many entries?
- Check `~/.claude/session-logs/git-tracker.jsonl` — exists? how many entries?

### 8. Custom Sub-agents (Phase 3)
Check `~/.claude/agents/`:
- `researcher.md` exists with valid frontmatter (model: haiku)
- `reviewer.md` exists with valid frontmatter (model: opus)
- Flag any agent files without frontmatter

### 9. Skills
List all skills in `~/.claude/skills/`:
- Show name and description from frontmatter
- Flag any without frontmatter
- Note which skills support scheduling (/schedule or /loop)

### 10. Templates
Check `~/.claude/templates/`:
- List available templates
- Flag if directory is empty (Phase 2 not complete)

## Output Format

```
╔══════════════════════════════════════════════════╗
║  FRAMEWORK STATUS                                ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  Hook Scripts:     [OK/WARN/ERROR] [details]    ║
║  Settings Hooks:   [OK/WARN/ERROR] [details]    ║
║  Session State:    [OK/STALE/MISSING] [details] ║
║  Memory System:    [OK/WARN] [N files]          ║
║  Session Logs:     [OK/WARN] [N logs]           ║
║  CLAUDE.md Rules:  [OK/INCOMPLETE] [details]    ║
║  PostToolUse:      [OK/WARN/MISSING] [details]  ║
║  Custom Agents:    [OK/WARN/MISSING] [details]  ║
║  Skills:           [N installed]                 ║
║  Templates:        [N available]                 ║
║                                                  ║
╠══════════════════════════════════════════════════╣
║  Overall: [HEALTHY / NEEDS ATTENTION / BROKEN]  ║
╚══════════════════════════════════════════════════╝
```

If any component is WARN or ERROR, explain:
1. What's wrong (in plain language)
2. How to fix it (specific command or action)
3. Impact if not fixed (what breaks)
