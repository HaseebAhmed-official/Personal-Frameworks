# Claude Context Automation Framework

Merged Claude Code context automation framework.

## Install

### Global layer
```bash
cp -r global/. ~/.claude/
```

### Project layer
```bash
cp project-level/CLAUDE.md project-level/RULES.md project-level/MEMORY.md ./
cp -r project-level/.claude/ ./.claude/
```

## What it does
- Auto-maintains session state across compactions
- Tracks all file edits and git commits to JSONL logs
- Enforces governance gates (memory approval, framework file protection)
- 7 specialized agents, 5 commands, 10 Python hooks, 76-point validation
