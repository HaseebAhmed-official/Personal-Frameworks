# Global Claude Code Rules

## Framework Contracts

Before major work, load these companion documents:
- `@~/.claude/RULES.md` — Precedence hierarchy, routing decisions, conflict resolution
- `@~/.claude/MEMORY.md` — Memory taxonomy, entry schema, approval workflow
- `@~/.claude/docs/framework/governance.md` — Approval matrix and trust boundaries

**Session priorities:**
1. Preserve state and recoverability
2. Keep main context compact and decision-focused
3. Improve quality through controlled delegation
4. Respect approval, security, and governance constraints

## Context & Workflow Management Framework

This framework automatically manages context window, memory, and reusable artifact generation.
It works globally across ALL projects. The hooks in `~/.claude/settings.json` handle the automation.

### Context Window Optimization

**Rule 1 — Delegate heavy work to sub-agents to keep main context light:**

- Research/exploration tasks → spawn Explore sub-agent (uses Haiku, cheaper + keeps main context clean)
- Planning/architecture tasks → spawn Plan sub-agent
- Multi-faceted analysis → use parallel Agent calls or Agent Teams
- File searches → use Glob/Grep tools directly instead of reading entire files
- When a task involves reading many files or generating verbose output, offload to a sub-agent

**Rule 2 — Track progress with tasks, not memory:**

- Use TaskCreate to track work items within the session
- Update tasks as they complete (TaskUpdate with status: "completed")
- This creates a visible progress record that survives compaction

**Rule 3 — Maintain session-state.json for continuity:**

- Write to `~/.claude/session-state.json` at these moments:
  - After completing a significant task or milestone
  - After making a key decision (architecture choice, approach selection)
  - Before suggesting /compact to the user
  - When detecting the conversation is getting long (15+ exchanges)
- Format: `{"timestamp":"ISO","project_dir":"path","task":"description","progress":"status","decisions":[],"active_files":[],"next_steps":[]}`
- Keep it concise — this is a recovery document, not a transcript

**Rule 4 — After compaction, read the restored state:**

- The PostCompact hook will inject session state into the conversation
- Read it, acknowledge it, and continue from where you left off
- Do NOT re-ask the user what they were working on if state is available

### Memory Management

**Two-tier memory system:**

**Tier 1 — Session state (auto-maintained, no approval needed):**
- `~/.claude/session-state.json` is updated silently at milestones
- Contains: task, progress, decisions, blockers, next_steps, active_files
- Archived automatically at session end to session-logs/

**Tier 2 — Durable memory (REQUIRES explicit user approval):**
- Never auto-write durable entries to MEMORY.md
- Use `/governance:memory-proposal` to identify and classify candidates
- Wait for user to explicitly approve before writing anything durable
- Durable entries require: class, owner, scope, sensitivity, review_at date
- See `~/.claude/MEMORY.md` for the 6-class taxonomy and schema

**Memory hygiene (applies to both tiers):**
- Check existing memories before creating duplicates
- Update stale memories rather than creating new ones
- Keep MEMORY.md index under 200 lines
- Cap at max 50 entries per project (run /memory-cleanup if exceeded)
- Run `/memory-cleanup` when audit overdue (notification reminds after 7 days)

### Reusable Component Detection (Describe First, Ask to Create)

**Watch for these patterns during work:**

- Same workflow repeated 3+ times → suggest a SKILL
- Same debugging steps → suggest a DIAGNOSTIC SCRIPT
- Same project setup → suggest a PROJECT TEMPLATE
- Same prompt structure → suggest a PROMPT TEMPLATE
- Useful automation opportunity → suggest a HOOK

**Protocol when detecting a pattern:**

1. Describe WHAT you'd create (file name, location, purpose)
2. Explain WHY it helps future sessions
3. Show a brief preview of what it would contain
4. Wait for explicit approval before creating
5. NEVER auto-create skills, hooks, agents, templates, or scripts without permission

### Tiered Approval System

| Action                  | Approval Level   | Behavior                                  |
| ----------------------- | ---------------- | ----------------------------------------- |
| Memory saves            | Auto (silent)    | Save without asking                       |
| Session state updates   | Auto (silent)    | Write session-state.json without asking   |
| Session logs            | Auto (silent)    | Archive session summaries automatically   |
| Task tracking           | Auto (silent)    | Create/update tasks without asking        |
| New skills              | Describe & ask   | Explain what and why, wait for permission |
| New hooks               | Describe & ask   | Explain what and why, wait for permission |
| New agents              | Describe & ask   | Explain what and why, wait for permission |
| New templates/scripts   | Describe & ask   | Explain what and why, wait for permission |
| Settings.json changes   | Explicit request | Only modify if user explicitly asks       |
| CLAUDE.md modifications | Explicit request | Only modify if user explicitly asks       |
| Plugin installs         | Explicit request | Only install if user explicitly asks      |

### User Profile (Auto-Loaded Context)

The user is a beginner who relies on Claude Code for terminal operations. They:

- Work on ALL project types (web/software, research, data/AI, mixed)
- Want to understand WHY things work, not just WHAT to do
- Prefer semi-manual control: describe before creating, explain before executing
- Value comprehensive analysis from every angle
- Need explanations in plain language without unexplained jargon
