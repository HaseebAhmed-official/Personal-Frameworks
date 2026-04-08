---
name: session-review
description: >
  Analyzes the current session's work and suggests reusable artifacts (skills, hooks, agents,
  templates, scripts, prompts). Run at session end or anytime to capture value from the work done.
  Trigger: /session-review or when Claude detects a natural session endpoint.
---

# Session Review Skill

You are reviewing the current session to identify reusable artifacts that would help in future sessions.

## Step 1 — Gather Session Context

Collect this information (read from available sources, don't ask the user):

1. **Session state**: Read `~/.claude/session-state.json` for task description and progress
2. **Recent tasks**: Use TaskList to see what was worked on
3. **Files modified**: Check git status or recent file changes
4. **Conversation patterns**: Scan the conversation for repeated workflows, prompts, or debugging steps

## Step 2 — Identify Artifact Opportunities

For each pattern found, classify it:

| Pattern Type | Artifact to Suggest | Location |
|---|---|---|
| Repeated workflow (same steps 3+ times) | Skill | `~/.claude/skills/` |
| Repeated debugging steps | Diagnostic Script | `~/.claude/scripts/` |
| Reusable project setup | Project Template | `~/.claude/templates/` |
| Repeated prompt structure | Prompt Template | `~/.claude/templates/` |
| Automation opportunity | Hook | `~/.claude/settings.json` |
| Specialized task pattern | Custom Agent | `~/.claude/agents/` |

**Quality gate**: Only suggest artifacts that would save real time. If a pattern was used only once and is unlikely to recur, skip it. Minimum threshold: pattern appeared 3+ times OR is clearly reusable across projects.

## Step 3 — Present Suggestions

For EACH suggestion, present it in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUGGESTION [N]: [Artifact Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type:     [Skill / Hook / Agent / Template / Script]
File:     [exact file path where it would be created]
WHY:      [1-2 sentences explaining what problem this solves]
PREVIEW:  [5-10 line preview of what the file would contain]
SAVES:    [estimated time/effort saved per future session]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Maximum 2 suggestions per session** — quality over quantity.

## Step 4 — Wait for Approval

After presenting suggestions, ask:
> "Which suggestions would you like me to create? (all / none / 1,2 / or give feedback)"

**Rules:**
- NEVER create artifacts without explicit approval
- If the user says "all", create them one by one, showing each file as it's created
- If the user gives feedback, adjust and re-present
- Use the templates from `~/.claude/templates/` if they exist

## Step 5 — Update Memory

After creating artifacts:
1. Update `~/.claude/session-state.json` with what was created
2. Save a project memory if the artifact reveals something about the project
3. Update MEMORY.md index if new memory files were created

## Step 6 — Session Summary

End with a brief summary:
```
Session Review Complete
━━━━━━━━━━━━━━━━━━━━━━
Artifacts created: [count]
Memories updated:  [count]
Suggestions saved for later: [count]
```
