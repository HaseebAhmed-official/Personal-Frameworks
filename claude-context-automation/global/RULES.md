# Framework Rules & Precedence

This document defines how the Claude Code context automation framework makes decisions when rules conflict, how components are classified, and how routing works.

## Source Classification

All framework components are classified by source:

| Source | Definition | Binding |
|--------|-----------|---------|
| **Enterprise** | Organization-wide policy | Cannot be overridden |
| **Explicit Approval** | User approval in this session | Overrides framework defaults for this session only |
| **Task Request** | Explicit instruction in prompt | Overrides framework defaults |
| **Hooks** | Automated behaviors in settings.json | Execute at defined lifecycle events |
| **Project Rules** | This project's CLAUDE.md | Shared/versioned rules for the repo |
| **Settings** | ~/.claude/settings.json | User's global defaults |
| **Local Settings** | ~/.claude/settings.local.json | Personal development overrides |
| **User Settings** | Claude Code UI preferences | UI/UX defaults |
| **MCP Servers** | External integrations (allowlisted) | Careful integration points |
| **Transcript Summaries** | AI-generated session summaries | Never override policy |

## Precedence Hierarchy (11 Levels)

When instructions conflict, resolve by this ordering (highest wins):

```
1. Enterprise policy             ← Cannot be overridden
2. Explicit user approval        ← Session-specific consent
3. Task request                  ← What user asked for
4. Hooks (automated behavior)    ← Execution events
5. Project CLAUDE.md rules       ← Repo-level policy
6. ~/.claude/settings.json       ← Global user defaults
7. ~/.claude/settings.local.json ← Local development
8. Claude Code UI settings       ← User preferences
9. MCP servers (allowlisted)     ← External integrations
10. Transcript summaries         ← AI-generated context
11. Framework ledgers            ← Auto-generated records
```

## Conflict Resolution

**Enterprise cannot be overridden** — If enterprise policy exists, it wins unconditionally.

**Session approval overrides framework defaults** — User's explicit "yes" in this session trumps CLAUDE.md/RULES.md.

**Task request trumps generic policy** — Specific instruction in prompt overrides framework defaults.

**Transcripts cannot override policy** — AI summaries are informational, never policy-changing.

## Component Classification

### Rule Packs
- **CLAUDE.md** — Global behavioral rules (user level)
- **RULES.md** — This file; precedence and routing (framework level)
- **MEMORY.md** — Memory taxonomy and ledger (framework level)
- Location: `~/.claude/` or `./.claude/` (project overrides)

### Memory
- **MEMORY.md index** — Ledger of all durable memory entries
- Location: Per-project at `~/.claude/projects/{project}/memory/MEMORY.md`
- Scope: Project-local or user-global
- Write policy: Proposal + approval workflow only

### Agents
- **Agent definitions** — Markdown with YAML frontmatter
- Location: `~/.claude/agents/` or `./.claude/agents/`
- Owned by: User (personal defaults) or project (shared)
- Examples: researcher, reviewer, governance-reviewer, memory-curator

### Agent Teams
- **Team patterns** — Predefined multi-agent configurations
- Pre-built: research-team, verification-team, governance-team
- Requires: Explicit user approval before creation
- Location: Defined in commands; executed by Agent tool

### Hook Bundles
- **Hook scripts** — Automation at lifecycle events
- Location: `~/.claude/scripts/hooks/` (Python scripts)
- Lifecycle: SessionStart, PreToolUse, PostToolUse, PreCompact, PostCompact, Stop, Notification, SubagentStop
- Execution: Configured in settings.json

### Custom Commands
- **Skill definitions** — Invokable via `/command` syntax
- Location: `~/.claude/commands/` or `./.claude/commands/`
- Examples: /fw, /session-review, /memory-cleanup, /context-audit
- Owned by: User (global) or project (shared)

### Output Styles
- **Behavioral modes** — Modify Claude's response format
- Examples: context-lean (concise), governed-execution (formal)
- Location: `~/.claude/output-styles/`
- Scope: Session-wide setting

### Schemas & Audit
- **Validation templates** — JSON Schema, YAML, examples
- Location: `~/.claude/schemas/`
- Used for: Memory entries, state ledgers, audit events
- Enforcement: Schema validation before persistence

## Routing Rules

### When to Stay in Main Thread
- Sequential work on one task
- Single project, single objective
- Context not under pressure
- Collaboration is minimal

### When to Use a Subagent (Single)
- Bounded research task (web search, codebase exploration)
- Deep code review on specific files
- Focused analysis with clear scope
- Need to keep main context light
- Time-bound work (<1 hour)

### When to Use an Agent Team
- Parallel research from multiple angles
- Multi-criteria evaluation (competing lenses)
- Cross-layer work (frontend + backend simultaneously)
- Requires teammate-to-teammate communication
- Needs explicit approval before creation
- Conservative defaults: 1 lead, 3 teammates, 1 verifier

### When to Trigger Compaction
- Unresolved branches accumulate (3+ open threads)
- Context window pressure detected
- Before starting new major work
- When `/context-audit` recommends it

## Durable Memory Rules

### What Can Be Durable Memory

**YES:**
- Project-specific knowledge (API schemas, architecture)
- User preferences and patterns
- Reusable solutions and patterns
- Decision rationales (why we chose X over Y)
- Team/project conventions

**NO:**
- Session state (use session-state.json instead)
- Transcript summaries (informational, don't auto-save)
- Temporary work-in-progress notes
- Speculative ideas not yet validated

### Memory Workflow

1. **Identify** — During work, flag potential memory candidates
2. **Propose** — Run `/governance:memory-proposal` to extract and classify
3. **Review** — User examines proposed entries
4. **Approve** — User explicitly approves or rejects each entry
5. **Write** — Approved entries written to MEMORY.md with metadata
6. **Review Cycle** — Set `review_at` date; curator reminds for re-evaluation

### Memory Schema

Every durable entry must have 10 required fields:
- **id** — Unique identifier (memory-NNNN)
- **class** — One of 6 taxonomy classes
- **owner** — Who can edit (user, project, enterprise)
- **scope** — Visibility (personal, project, organization)
- **source** — Where it came from (transcript, decision, documentation)
- **provenance** — When/where created (session summary link)
- **sensitivity** — Data classification (low, moderate, high, restricted)
- **approval_state** — Workflow state (proposed, approved, rejected, expired)
- **created_at** — ISO 8601 timestamp
- **review_at** — Next review date (triggers audit reminder)

Optional fields:
- **supersedes** — Which previous entries this replaces
- **status** — Current status (active, superseded, under_review, archived)

## Safety Rules

### Secrets & Sensitive Data
- Never write credentials, API keys, tokens to durable memory
- Deny Read access to `.env`, `secrets/`, `credentials.*`
- Deny Bash commands: `curl`, `wget` (use WebFetch/WebSearch)
- Deny destructive: `rm -rf`, `git reset --hard`, `git push --force`

### Framework Files Protection
- CLAUDE.md, RULES.md, MEMORY.md, settings.json require approval before edit
- Pre_tool_use hook intercepts and reminds
- Edits must be minimal and auditable
- Always document reason for framework changes

### Destructive Operations
- Git force-push requires explicit confirmation
- Database migrations require verification
- Deleting durable entries requires approval
- Clearing session state requires confirmation

## Approval Gates (Require Explicit User Approval)

1. **Durable Memory** — No auto-write; must propose + approve
2. **Framework File Edits** — CLAUDE.md, RULES.md, MEMORY.md, settings.json
3. **New Hooks** — Adding/modifying automation in settings.json
4. **Custom Commands** — Creating new /commands
5. **Output Styles** — Changing response behavior
6. **Agent Teams** — Creating research-team, verification-team, or custom teams
7. **MCP Integration** — Enabling new external services
8. **Component Templates** — Creating reusable artifacts

## Autonomous Actions (No Approval Needed)

1. **Read-only analysis** — Exploring code, analyzing patterns
2. **Context loading** — Loading @files, @directories
3. **Existing subagent use** — Spawning researcher, reviewer, etc.
4. **Transient state updates** — Writing session-state.json during work
5. **Tracking** — Appending to edit-tracker.jsonl, git-tracker.jsonl
6. **Reminders** — Emitting governance/state reminders

## Session vs Durable Decision

| Question | Answer | Implication |
|----------|--------|-------------|
| Is this user-specific? | Yes | Personal memory or session-state.json |
| Is this project-wide? | Yes | Project-scoped MEMORY.md entry |
| Will future sessions need this? | Yes | Propose for durable memory |
| Is this temporary work-in-progress? | Yes | Keep in session-state.json only |
| Could this guide decisions for months? | Yes | Propose for durable memory |
| Is this sensitive data? | Yes | Session state only; never durable |

## Known Limitations

1. **Session state depends on Claude** — Framework requests, user discipline required
2. **Hook output invisible to user** — Hooks emit to stdout, may not appear visibly
3. **Plugin not auto-synced** — Manual copy needed after editing framework
4. **Skill format requirements** — Must follow SKILL.md frontmatter structure
5. **Shortcut limitations** — Keybindings cannot trigger skills (workaround: prompt shortcuts)
6. **Team defaults conservative** — 3 teammates max; can be overridden with explicit approval

## Framework Contracts

When following this framework, you agree to:

✓ **Load** CLAUDE.md, RULES.md, MEMORY.md before major work  
✓ **Maintain** session-state.json with goal, decisions, blockers, next_steps  
✓ **Propose** memory, never auto-write  
✓ **Respect** precedence hierarchy for conflict resolution  
✓ **Protect** framework files from unauthorized changes  
✓ **Gate** teams, hooks, commands, and MCP integrations  
✓ **Audit** all meaningful events to logs  
✓ **Document** framework changes with reason and date  

---

**Version:** 1.0  
**Last Updated:** 2026-04-08  
**Scope:** Global user framework (~/.claude/)  
**Ownership:** User
