# Claude Context Automation Framework

A comprehensive automation framework for Claude Code that merges practical session continuity with governance and approval workflows. Built by synthesizing two frameworks: Claude's bash-based global automation layer and Codex's Python-based governance layer.

## What This Framework Does

### 1. Session Continuity & Recovery
Automatically maintains your session state across compactions and interruptions. When you resume within 24 hours, the framework re-injects your previous task, decisions, blockers, and next steps—no need to explain what you were doing.

### 2. Post-Compaction State Recovery
Before summarizing, the pre-compaction hook timestamps your full context. After summarization, the post-compaction hook re-injects that context, preserving all state across Claude's context window compaction.

### 3. Edit & Git Audit Trail
Every file edit is appended to an JSONL audit log (with 500-entry cap) and every git commit to a git tracker (200-entry cap). Enables full traceability of who changed what and when.

### 4. Framework File Protection
Prevents accidental modifications to critical framework files (CLAUDE.md, RULES.md, MEMORY.md, settings.json) without explicit user approval in the current session.

### 5. Governance Gates
Detects keywords like "remember" or "agent team" in your prompts and injects approval-requirement reminders, ensuring intentional governance.

### 6. Subagent Quality Gate
Requires every subagent output to include structured findings, risks, and recommended next actions—enforcing consistency across delegated work.

### 7. Prompt Shortcuts
Quick command aliases that expand to full skill invocations:
- `!fw` → `/fw` (framework menu)
- `!mc` → `/memory-cleanup` (memory hygiene)
- `!fs` → `/framework-status` (validation check)
- `!sr` → `/session-review` (session analysis)

### 8. Two-Tier Memory System
**Session memory** (`session-state.json`) — Auto-updated, no approval needed. Tracks current task, decisions, blockers, pending approvals.

**Durable memory** (`MEMORY.md`) — Persistent across sessions, requires explicit approval. Classified into 6 memory classes (Enterprise, Project Operating, Personal Preference, Session State, Retrieval/Index, Audit Trail).

### 9. 11-Level Precedence Hierarchy
When rules conflict, resolution is deterministic:
1. Enterprise policy (cannot be overridden)
2. Explicit user approval (session-specific)
3. Task request (what you asked for)
4. Hooks (automated behavior)
5. Project CLAUDE.md rules
6. ~/.claude/settings.json
7. ~/.claude/settings.local.json
8. Claude Code UI settings
9. MCP servers (allowlisted)
10. Transcript summaries
11. Framework ledgers (auto-generated)

## Architecture Overview

The framework operates as a two-layer system:

### Global Layer (~/.claude/)
Installs user-level configuration, hooks, agents, skills, and output styles. Shared across all projects. Includes:
- 4 rule documents (CLAUDE.md, RULES.md, MEMORY.md, FRAMEWORK-WORKFLOW.md)
- 10 Python hooks (session start, pre/post tool use, pre/post compact, stop, subagent stop, user prompt submit, notification)
- 7 specialized agents (researcher, reviewer, analysis-lead, verification-auditor, context-researcher, governance-reviewer, memory-curator)
- 6 skills (fw, framework-status, memory-cleanup, session-review, framework-merge, omni-expert-interrogation)
- 5 commands (context-audit, memory-proposal, resume-ledger, research-team, verification-team)
- 2 output styles (context-lean, governed-execution)
- Templates, schemas, keybindings

### Project Layer (./.claude/ + project root)
Installs project-specific configuration and governance. Overrides global settings for this project. Includes:
- 3 rule documents (CLAUDE.md, RULES.md, MEMORY.md)
- 10 Python hooks (same lifecycle events, project-scoped)
- 4 project agents (verification-auditor, context-researcher, governance-reviewer, memory-curator)
- 5 project commands (context-audit, memory-proposal, resume-ledger, research-team, verification-team)
- 2 project output styles (context-lean, governed-execution)
- 4 schemas for validation

Rules, agents, and commands at project level override their global counterparts for that project.

## Hook Reference

| Hook Name | Event | Purpose |
|-----------|-------|---------|
| **session_start.py** | Session begins | Detects prior sessions (<24h old), re-injects task/decisions/blockers |
| **pre_tool_use.py** | Before tool execution | Blocks edits to framework files without approval; validates MCP allowlist |
| **post_tool_use.py** | After tool execution | Appends file edits to edit-tracker.jsonl; git commits to git-tracker.jsonl |
| **pre_compact.py** | Before context summarization | Timestamps session state to enable recovery after compaction |
| **post_compact.py** | After context summarization | Re-injects full session state from backup |
| **user_prompt_submit.py** | Before processing user input | Injects approval reminders for "remember"/"agent team" keywords |
| **stop.py** | Session shutdown | Archives session logs and cleans up ephemeral state |
| **subagent_stop.py** | Subagent shutdown | Enforces Findings + Risks + Recommended Next Action in output |
| **notification.py** | Message delivery | Formats hook notifications for user display |
| **common.py** | All hooks | Shared utilities (logging, JSON I/O, path resolution) |

## Agent Roster

| Agent | Model | Purpose |
|-------|-------|---------|
| **researcher** | haiku | Deep research across web, codebase, and documentation; returns findings without bloating main context |
| **reviewer** | haiku | Code and architecture review; identifies risks and improvement opportunities |
| **analysis-lead** | haiku | Multi-domain expert analysis; coordinates specialized interrogation protocols |
| **verification-auditor** | haiku | Validates framework components and checks compliance with governance rules |
| **context-researcher** | haiku | Explores decision trees and context dependencies; identifies relevant artifacts |
| **governance-reviewer** | haiku | Audits approval workflows and precedence rule application |
| **memory-curator** | haiku | Analyzes memory entries for staleness, duplicates, and governance compliance |

## Skills Reference

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **fw** | `/fw` | Menu launcher for all framework maintenance actions |
| **framework-status** | `/framework-status` | Diagnostic validation—checks all hooks, agents, memory, settings, and reports issues |
| **memory-cleanup** | `/memory-cleanup` | Weekly memory hygiene—scans for stale, duplicate, or orphaned entries |
| **session-review** | `/session-review` | Analyzes work done this session and suggests reusable artifacts (skills, hooks, agents, templates) |
| **framework-merge** | `/framework-merge` | Synthesizes two systems/frameworks into a merged best-of-both form |
| **omni-expert-interrogation** | `/omni-expert-interrogation` | Multi-domain expert panel analysis with structured interrogation and synthesis |

## Installation Instructions

### Prerequisites
- Python 3.8 or later
- Claude Code CLI (installed and authenticated)
- `gh` CLI for git integration (optional but recommended)

### Step 1: Global Layer Installation

Copy the global layer to your user's Claude Code directory:

```bash
cp -r global/. ~/.claude/
```

This installs:
- CLAUDE.md, RULES.md, MEMORY.md, FRAMEWORK-WORKFLOW.md (core documentation)
- scripts/hooks/ (10 Python automation hooks)
- agents/, skills/, commands/, output-styles/, templates/ (reusable components)
- schemas/, keybindings.json, settings.json (configuration)

### Step 2: Project Layer Installation

For each project where you want to use this framework:

```bash
cd /path/to/your/project
cp /path/to/claude-context-automation/project-level/CLAUDE.md ./
cp /path/to/claude-context-automation/project-level/RULES.md ./
cp /path/to/claude-context-automation/project-level/MEMORY.md ./
cp -r /path/to/claude-context-automation/project-level/.claude/ ./
```

This installs:
- CLAUDE.md, RULES.md, MEMORY.md (project-level governance rules)
- .claude/agents/, .claude/commands/, .claude/output-styles/ (project overrides)
- .claude/scripts/hooks/ (project-scoped hook scripts)
- .claude/logs/.gitkeep (log directory)

### Step 3: Verify Installation

Run the validation diagnostic:

```bash
/path/to/claude-context-automation/global/scripts/validate_framework.py
```

This checks:
- All hook scripts are executable and syntactically valid
- settings.json is properly formatted
- All agents, skills, commands are reachable
- Memory files follow the correct schema
- 76 validation points in total

Expected output:
```
Validation complete: 76/76 checks passing
```

### Step 4: Test Session Start

Begin a Claude Code session in your project:

```bash
cd /path/to/your/project
claude
```

The session_start.py hook will:
- Check for prior sessions (<24h old)
- Inject recovered state if found
- Display confirmation that framework is active

## File Structure Overview

```
claude-context-automation/
├── global/                          # Install to ~/.claude/
│   ├── CLAUDE.md                   # Global behavioral rules
│   ├── RULES.md                    # Precedence hierarchy & routing
│   ├── MEMORY.md                   # Memory taxonomy & ledger
│   ├── FRAMEWORK-WORKFLOW.md       # 10-section session lifecycle reference
│   ├── settings.json               # Hook registration and global config
│   ├── keybindings.json            # Keyboard shortcuts for commands
│   ├── statusline.py               # Status display for terminal
│   ├── scripts/
│   │   ├── hooks/                  # 10 Python automation hooks
│   │   │   ├── session_start.py
│   │   │   ├── pre_tool_use.py
│   │   │   ├── post_tool_use.py
│   │   │   ├── pre_compact.py
│   │   │   ├── post_compact.py
│   │   │   ├── user_prompt_submit.py
│   │   │   ├── stop.py
│   │   │   ├── subagent_stop.py
│   │   │   ├── notification.py
│   │   │   └── common.py
│   │   ├── validate_framework.py   # 76-point validation diagnostic
│   │   ├── audit_log.py            # JSONL audit trail utilities
│   │   └── [legacy bash scripts]
│   ├── agents/                     # 7 specialized agents
│   │   ├── researcher.md
│   │   ├── reviewer.md
│   │   ├── analysis-lead.md
│   │   ├── verification-auditor.md
│   │   ├── context-researcher.md
│   │   ├── governance-reviewer.md
│   │   └── memory-curator.md
│   ├── skills/                     # 6 reusable command suites
│   │   ├── fw/
│   │   ├── framework-status/
│   │   ├── memory-cleanup/
│   │   ├── session-review/
│   │   ├── framework-merge/
│   │   └── omni-expert-interrogation/
│   ├── commands/                   # 5 custom commands
│   │   ├── context-audit.md
│   │   ├── governance/
│   │   │   ├── memory-proposal.md
│   │   │   └── resume-ledger.md
│   │   └── teams/
│   │       ├── research-team.md
│   │       └── verification-team.md
│   ├── output-styles/              # 2 response modes
│   │   ├── context-lean.md
│   │   └── governed-execution.md
│   ├── schemas/                    # Validation templates
│   │   ├── memory-entry.schema.json
│   │   ├── state-ledger.example.yaml
│   │   ├── audit-event.example.json
│   │   └── memory-entry.example.json
│   ├── templates/                  # Reusable templates
│   │   ├── agent-template.md
│   │   ├── hook-template.py
│   │   ├── hook-template.json
│   │   ├── prompt-template.md
│   │   ├── script-template.sh
│   │   └── skill-template.md
│   └── docs/
│       ├── framework/
│       │   ├── governance.md       # Approval matrix & trust boundaries
│       │   ├── precedence.md       # 11-level hierarchy explained
│       │   ├── agent-teams.md      # Multi-agent coordination patterns
│       │   ├── components.md       # All framework component types
│       │   └── smoke-test.md       # Post-install validation
│       └── simulation.md           # Session lifecycle reference
│
└── project-level/                  # Install to project root + ./.claude/
    ├── CLAUDE.md                   # Project behavioral rules
    ├── RULES.md                    # Project-specific precedence
    ├── MEMORY.md                   # Project memory ledger
    └── .claude/                    # Project-scoped overrides
        ├── settings.json
        ├── agents/                 # 4 project agents
        ├── commands/               # 5 project commands
        ├── output-styles/          # 2 project output styles
        ├── scripts/hooks/          # 10 project-scoped hooks
        ├── logs/.gitkeep
        └── schemas/                # 4 project schemas
```

## Memory Taxonomy (6 Classes)

Durable memory entries are classified by scope and lifecycle:

| Class | Scope | Owner | Lifecycle | Use Case |
|-------|-------|-------|-----------|----------|
| **Enterprise Policy** | Organization-wide | Enterprise | Annual review | Org-mandated policies, compliance, security |
| **Project Operating** | This project | Project lead | Quarterly review | Shared conventions, architecture decisions |
| **Personal Preference** | User-specific | User | Bi-annual review | Working patterns, tool preferences, optimizations |
| **Session State** | Current session | Claude (ephemeral) | Auto-archived | Current task, active decisions, blockers |
| **Retrieval/Index** | Framework-internal | Framework curator | Auto-expired | Quick reference, navigation, search help |
| **Audit Trail** | All changes | Framework | Permanent | Edit history, commit log, governance compliance |

Write policy: Session state updates automatically without approval. All other classes require explicit user approval via `/governance:memory-proposal`.

## Requirements

- **Python 3.8+** for hook scripts
- **Claude Code CLI** (installed and authenticated) for core functionality
- **gh CLI** (optional) for enhanced git tracking and integration
- **~/.claude/ directory** with write permissions for global installation
- **Project ./.claude/ directory** with write permissions for project installation

## Validation & Smoke Testing

After installation, verify everything is working:

```bash
# Run the diagnostic
python3 ~/.claude/scripts/validate_framework.py

# Or use the framework menu
/fw
→ Select "Validate Installation"

# Or use the shell shortcut
!fs
```

Expected output: `76/76 validation checks passing`

## Key Behaviors in Action

### Session Recovery Example
```
Session 1: You write code, ask Claude for help, make decisions
Compaction happens (automatic)
Session 2: <24h later, same project>
SessionStart hook fires → Re-injects your previous task, decisions, blockers
You see: "Restored prior session context"
→ You continue without explaining what you were doing
```

### Edit Tracking Example
```
You: "Edit the requirements.txt"
Claude: [edits requirements.txt]
PostToolUse hook fires:
  - Appends event to .claude/logs/edit-tracker.jsonl
  - Git hook runs (if enabled) → auto-commits change
  - Audit log now has full traceability
```

### Framework Protection Example
```
You: "Update my global CLAUDE.md with new rules"
PreToolUse hook fires → Detects CLAUDE.md edit attempt
Claude is blocked from editing without explicit approval
Claude responds: "This requires explicit approval. Say: 'I approve editing CLAUDE.md'"
You: "I approve editing CLAUDE.md"
→ Edit proceeds in current session only
```

## Getting Help

- **Framework Status:** `/framework-status` — Diagnoses installation issues
- **Memory Cleanup:** `/memory-cleanup` — Hygiene and maintenance
- **Session Review:** `/session-review` — Captures reusable artifacts
- **Context Audit:** `/context-audit` — Analyzes current context usage
- **Framework Menu:** `/fw` — Launcher for all maintenance actions

## Project Statistics

- **100 files** (scripts, templates, agents, hooks, documentation, schemas)
- **7,409 lines of code**
- **76 validation checks** (all passing)
- **10 Python automation hooks**
- **7 specialized agents**
- **6 reusable skills**
- **11-level governance precedence**
- **6-class memory taxonomy**

## Contributing

This framework is designed to be extended. To add:
- **New hooks:** Copy `templates/hook-template.py`, register in `settings.json`
- **New agents:** Copy `templates/agent-template.md`, save to `~/.claude/agents/`
- **New skills:** Copy `templates/skill-template.md`, create a subdirectory under `skills/`
- **New commands:** Create `.md` file in `commands/`, register in `settings.json`

All customizations can be validated with `validate_framework.py`.

## License

See LICENSE in the repository root.

## Author

HaseebAhmed-official

Built by merging two frameworks:
- **Framework A:** Claude's bash-based global automation framework
- **Framework B:** Codex's Python-based governance framework

Result: A production-grade context automation system for Claude Code with enterprise-level governance, session continuity, and approval workflows.
