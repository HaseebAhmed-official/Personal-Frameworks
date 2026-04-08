# Context & Workflow Management Framework

## Complete Hierarchical Workflow Reference

```
Version:  1.0.0
Updated:  2026-04-06
Location: ~/.claude/FRAMEWORK-WORKFLOW.md
```

---

## Table of Contents

- [1. Architecture Overview](#1-architecture-overview)
- [2. Directory Map](#2-directory-map)
- [3. Lifecycle Workflow](#3-lifecycle-workflow)
- [4. Hooks](#4-hooks-8-scripts)
- [5. Skills](#5-skills-5-commands)
- [6. Agents](#6-agents-3-specialists)
- [7. Templates](#7-templates-5-boilerplates)
- [8. Storage Locations](#8-storage-locations-what-gets-saved-where)
- [9. Plugin](#9-plugin-self-contained-backup)
- [10. Keybindings](#10-keybindings)
- [11. Shortcuts](#11-prompt-shortcuts)
- [12. OEIP Constraints](#12-oeip-constraints)
- [13. CLAUDE.md Rules](#13-claudemd-rules-what-claude-is-told)
- [14. Known Limitations](#14-known-limitations)
- [15. Common Tasks](#15-common-tasks-quick-reference)

---

## 1. Architecture Overview

```
                    ┌─────────────────────────────────────┐
                    │         YOU (the user)               │
                    └──────────────┬──────────────────────┘
                                   │
                                   │ Opens Claude Code
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        CLAUDE CODE SESSION                           │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────────┐ │
│  │  CLAUDE.md   │  │ settings.json│  │   session-state.json       │ │
│  │  (Rules)     │  │ (Hook Wiring)│  │   (Session Brain)          │ │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬───────────────┘ │
│         │                  │                        │                 │
│         ▼                  ▼                        ▼                 │
│  Claude follows     8 hooks fire              State preserved        │
│  the rules          automatically             across compactions     │
│                                                                      │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌────────────────────┐    │
│  │ Skills  │  │ Agents  │  │ Templates│  │ Session Logs       │    │
│  │ /fw     │  │researcher│ │ 5 files  │  │ archives + trackers│    │
│  │ /sr     │  │reviewer │  │          │  │                    │    │
│  │ /fs     │  │analysis │  │          │  │                    │    │
│  │ /mc     │  │-lead    │  │          │  │                    │    │
│  └─────────┘  └─────────┘  └──────────┘  └────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### How it works in one sentence

> Hooks automate the boring stuff. Skills give you commands. Agents do heavy work.
> CLAUDE.md tells Claude how to behave. Everything is stored under `~/.claude/`.

---

## 2. Directory Map

```
~/.claude/                                    ← ROOT (everything lives here)
│
├── settings.json                             ← Hook wiring + permissions + plugins
├── CLAUDE.md                                 ← Rules Claude follows every session
├── session-state.json                        ← Current session brain (task, progress, decisions)
├── keybindings.json                          ← Keyboard shortcuts
├── FRAMEWORK-WORKFLOW.md                     ← THIS FILE (you are reading it)
│
├── scripts/                                  ← 8 hook scripts (fire automatically)
│   ├── pre-compact.sh                        ← Saves timestamp before compaction
│   ├── post-compact.sh                       ← Restores state after compaction
│   ├── session-start.sh                      ← Detects previous session on startup
│   ├── session-end.sh                        ← Archives state when session closes
│   ├── post-edit-log.sh                      ← Logs every file edit
│   ├── post-git-log.sh                       ← Logs every git commit
│   ├── memory-cleanup-reminder.sh            ← Reminds if audit is >7 days old
│   └── prompt-shortcuts.sh                   ← Expands !fw → /fw, !mc → /memory-cleanup
│
├── skills/                                   ← 5 skills (you invoke with /name)
│   ├── fw/SKILL.md                           ← Framework launcher menu (/fw)
│   ├── session-review/SKILL.md               ← Suggest reusable artifacts (/session-review)
│   ├── framework-status/SKILL.md             ← Health check diagnostic (/framework-status)
│   ├── memory-cleanup/SKILL.md               ← Memory audit + cleanup (/memory-cleanup)
│   └── omni-expert-interrogation/SKILL.md    ← Multi-expert analysis (/omni-expert-interrogation)
│
├── agents/                                   ← 3 agents (you ask Claude to spawn them)
│   ├── researcher.md                         ← Research agent (model: haiku, read-only)
│   ├── reviewer.md                           ← Code review agent (model: opus, read-only)
│   └── analysis-lead.md                      ← Team coordinator (model: opus, spawns others)
│
├── templates/                                ← 5 boilerplate templates
│   ├── skill-template.md                     ← For creating new skills
│   ├── agent-template.md                     ← For creating new agents
│   ├── hook-template.json                    ← For creating new hooks
│   ├── script-template.sh                    ← For creating new scripts
│   └── prompt-template.md                    ← For creating prompt templates
│
├── session-logs/                             ← All tracking data lives here
│   ├── edit-tracker.jsonl                    ← Every file edit (capped at 500)
│   ├── git-tracker.jsonl                     ← Every git commit (capped at 200)
│   ├── .last-memory-audit                    ← Timestamp of last /memory-cleanup run
│   ├── 2026-04-02-09-08.json                ← Session archive (one per session end)
│   ├── 2026-04-02-09-10.json                ← ...
│   └── ... (54 archives and growing)
│
├── plans/                                    ← Architecture and implementation plans
│   ├── magical-growing-hellman.md            ← Framework build plan (main)
│   └── ... (11 total plans)
│
├── projects/                                 ← Per-project memories
│   └── {project-hash}/memory/
│       ├── MEMORY.md                         ← Index of all memories
│       ├── user_profile.md                   ← Who you are
│       ├── feedback_interaction_style.md     ← How you like to work
│       ├── project_framework_goal.md         ← What you're building
│       ├── oeip_framework_analysis.md        ← Research summary
│       └── feedback_skill_creation.md        ← Skill creation preferences
│
└── plugins/local/context-framework/          ← PLUGIN (backup copy of everything)
    ├── .claude-plugin/plugin.json            ← Plugin metadata
    ├── .mcp.json                             ← MCP server config
    ├── hooks/hooks.json                      ← Mirror of settings.json hooks
    ├── scripts/                              ← Copy of all 8 scripts + MCP tools script
    ├── skills/                               ← Copy of all skills (folder/SKILL.md format)
    └── agents/                               ← Copy of all 3 agents
```

---

## 3. Lifecycle Workflow

### 3A. Session Start

```
You type: claude
         │
         ▼
┌────────────────────────────────────────────────────┐
│  NOTIFICATION HOOK FIRES (automatically)           │
│                                                    │
│  ┌─ session-start.sh ──────────────────────────┐   │
│  │  Checks: Does session-state.json exist?     │   │
│  │                                              │   │
│  │  YES + Fresh (<24h) ──► "Previous session   │   │
│  │                          found. Resume?"     │   │
│  │                                              │   │
│  │  YES + Stale (>24h) ──► "Previous session   │   │
│  │                          found (>24h old)"   │   │
│  │                                              │   │
│  │  NO ──────────────────► (silent, nothing)    │   │
│  └──────────────────────────────────────────────┘   │
│                                                    │
│  ┌─ memory-cleanup-reminder.sh ─────────────────┐  │
│  │  Checks: Is .last-memory-audit >7 days old?  │  │
│  │                                               │  │
│  │  YES ──► "Memory cleanup is overdue.         │  │
│  │           Run /memory-cleanup or /fw 1"       │  │
│  │                                               │  │
│  │  NO ───► (silent)                             │  │
│  └───────────────────────────────────────────────┘  │
│                                                    │
│  WHERE OUTPUT GOES: Into Claude's context.         │
│  Claude reads it and should mention it to you.     │
│  You do NOT see the raw script output on screen.   │
└────────────────────────────────────────────────────┘
```

### 3B. During Session — Normal Work

```
You work with Claude (coding, debugging, planning, etc.)
         │
         ├──── You edit a file ──────────────────────────────────────────┐
         │                                                               │
         │     ┌─ POST-TOOL-USE HOOK fires (matcher: Edit|Write) ──────┐│
         │     │  post-edit-log.sh                                      ││
         │     │  1. Reads stdin JSON: {"tool_name":"Edit",             ││
         │     │     "tool_input":{"file_path":"/path/file.py"}}        ││
         │     │  2. Extracts tool name + file path (jq, fallback grep) ││
         │     │  3. Appends to edit-tracker.jsonl                      ││
         │     │  4. Trims to 500 entries if over cap                   ││
         │     │  Runs: async (does not block Claude)                   ││
         │     │  You see: NOTHING (silent background logging)          ││
         │     └────────────────────────────────────────────────────────┘│
         │                                                               │
         ├──── Claude runs a bash command ───────────────────────────────┤
         │                                                               │
         │     ┌─ POST-TOOL-USE HOOK fires (matcher: Bash) ────────────┐│
         │     │  post-git-log.sh                                       ││
         │     │  1. Reads stdin JSON: {"tool_name":"Bash",             ││
         │     │     "tool_input":{"command":"git commit -m ..."}}      ││
         │     │  2. Checks: Does command contain "git commit"?         ││
         │     │     NO  ──► exit immediately (ignore non-commit cmds)  ││
         │     │     YES ──► extract hash, message, branch              ││
         │     │  3. Appends to git-tracker.jsonl                       ││
         │     │  4. Trims to 200 entries if over cap                   ││
         │     │  Runs: async (does not block Claude)                   ││
         │     │  You see: NOTHING (silent background logging)          ││
         │     └────────────────────────────────────────────────────────┘│
         │                                                               │
         ├──── You type a message ──────────────────────────────────────┤
         │                                                               │
         │     ┌─ USER-PROMPT-SUBMIT HOOK fires ────────────────────────┐
         │     │  prompt-shortcuts.sh                                    │
         │     │  1. Reads stdin JSON: {"message":{"content":"!fw 2"}}  │
         │     │  2. Matches against shortcut table:                     │
         │     │     !fw [arg]  ──► {"message": "/fw [arg]"}            │
         │     │     !mc        ──► {"message": "/memory-cleanup"}      │
         │     │     !fs        ──► {"message": "/framework-status"}    │
         │     │     !sr        ──► {"message": "/session-review"}      │
         │     │     (anything else) ──► no output (pass through)       │
         │     │  3. If matched, Claude receives the expanded command   │
         │     │  Runs: synchronous (transforms BEFORE Claude sees it)  │
         │     │  You see: Your !fw becomes /fw automatically           │
         │     └────────────────────────────────────────────────────────┘
         │
         ├──── Claude follows CLAUDE.md rules ──────────────────────────┐
         │     (These are NOT automated — they depend on Claude)         │
         │                                                               │
         │     At key moments, Claude SHOULD:                            │
         │     • Update session-state.json with current task/progress    │
         │     • Save memories when learning about you                   │
         │     • Delegate to sub-agents for heavy work                   │
         │     • Suggest artifacts when a pattern repeats 3+ times       │
         │     • Use tasks to track progress                             │
         │                                                               │
         │     IMPORTANT: These are rules, not guarantees.               │
         │     Claude may not always follow them perfectly.              │
         └───────────────────────────────────────────────────────────────┘
```

### 3C. During Session — Context Compaction

```
Context window fills up (~90%)
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  STEP 1: PRE-COMPACT HOOK fires                      │
│                                                      │
│  pre-compact.sh                                      │
│  1. Reads session-state.json                         │
│  2. Adds "last_compaction" timestamp                 │
│  3. Increments "compaction_count" by 1               │
│  4. Writes back to session-state.json                │
│                                                      │
│  You see: Status line "Saving session state..."      │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  STEP 2: COMPACTION HAPPENS                          │
│                                                      │
│  Claude Code compresses your entire conversation     │
│  into a short summary. All detailed messages are     │
│  gone. Only the summary remains.                     │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  STEP 3: POST-COMPACT HOOK fires                     │
│                                                      │
│  post-compact.sh                                     │
│  1. Reads session-state.json                         │
│  2. Outputs formatted summary:                       │
│                                                      │
│  --- SESSION STATE RESTORED AFTER COMPACTION ---     │
│  Task: Building user login system in Flask           │
│  Progress: JWT done, Redis sessions pending          │
│  Key decisions: JWT tokens; bcrypt; Redis            │
│  Active files: app/auth.py, app/models/user.py      │
│  Full plan: ~/.claude/plans/...                      │
│  --- END STATE ---                                   │
│  Continue from where you left off.                   │
│                                                      │
│  WHERE OUTPUT GOES: Into Claude's context.           │
│  Claude reads it and continues your work.            │
│  You see: Status line "Restoring session state..."   │
│  You also see: The grey text output briefly.         │
│                                                      │
│  CRITICAL DEPENDENCY: This only works well if        │
│  Claude updated session-state.json BEFORE the        │
│  compaction. If the state is stale, the restored     │
│  info will be old.                                   │
└──────────────────────────────────────────────────────┘
```

### 3D. Session End

```
You type: exit  (or press Ctrl+C, or close terminal)
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  STOP HOOK fires                                     │
│                                                      │
│  session-end.sh                                      │
│  1. Checks: Does session-state.json exist?           │
│  2. YES ──► Copies to session-logs/ as:              │
│             2026-04-06-11-45.json                    │
│     (timestamped archive — permanent record)         │
│  3. session-state.json is NOT deleted                │
│     (it stays for the next session-start to find)    │
│                                                      │
│  Runs: async                                         │
│  You see: NOTHING (runs as you exit)                 │
└──────────────────────────────────────────────────────┘
```

### 3E. Full Lifecycle Diagram

```
SESSION START                    DURING SESSION                     SESSION END
─────────────                    ──────────────                     ───────────

Notification hook                PostToolUse hooks (silent)         Stop hook
  │                                │                                  │
  ├─ session-start.sh              ├─ post-edit-log.sh (Edit/Write)   └─ session-end.sh
  │  "Resume previous?"            │  → edit-tracker.jsonl               → archives to
  │                                │                                       session-logs/
  └─ memory-cleanup-reminder.sh    ├─ post-git-log.sh (Bash)
     "Audit overdue?"              │  → git-tracker.jsonl
                                   │
                                   UserPromptSubmit hook
                                   │
                                   └─ prompt-shortcuts.sh
                                      !fw → /fw

                                   Compaction (when context fills)
                                   │
                                   ├─ pre-compact.sh (timestamps)
                                   └─ post-compact.sh (restores state)

                                   Claude behavior (CLAUDE.md rules)
                                   │
                                   ├─ Updates session-state.json
                                   ├─ Saves memories
                                   ├─ Delegates to agents
                                   └─ Suggests artifacts (3+ patterns)
```

---

## 4. Hooks (8 Scripts)

### 4A. Hook Wiring in settings.json

| Event | Script | Trigger | Mode | Timeout |
|---|---|---|---|---|
| `PreCompact` | `pre-compact.sh` | Auto-compaction starts | sync | 2s |
| `PostCompact` | `post-compact.sh` | Auto-compaction finishes | sync | 2s |
| `Notification` | `session-start.sh` | Session begins | sync | 2s |
| `Notification` | `memory-cleanup-reminder.sh` | Session begins | async | 2s |
| `PostToolUse` (Edit\|Write) | `post-edit-log.sh` | Claude edits/writes a file | async | 2s |
| `PostToolUse` (Bash) | `post-git-log.sh` | Claude runs a bash command | async | 2s |
| `UserPromptSubmit` | `prompt-shortcuts.sh` | User types a message | sync | 2s |
| `Stop` | `session-end.sh` | Session ends | async | 2s |

### 4B. Sync vs Async Explained

| Mode | Meaning | Used For |
|---|---|---|
| **sync** | Claude WAITS for the script to finish before continuing | Compaction hooks (must save/restore state before Claude proceeds), Shortcuts (must transform input before Claude reads it) |
| **async** | Script runs in BACKGROUND, Claude does not wait | Edit/git logging (non-blocking), Session end (runs as you exit), Memory reminder (nice-to-have, not critical) |

### 4C. What Each Hook Script Does

#### `pre-compact.sh`

```
Location:   ~/.claude/scripts/pre-compact.sh
Fires when: Context window is about to be compacted
What it does:
  1. Reads ~/.claude/session-state.json
  2. Adds "last_compaction" = current UTC timestamp
  3. Increments "compaction_count" by 1
  4. Writes back to the same file
Output:     NOTHING (silent — must not block compaction)
Depends on: python3
```

#### `post-compact.sh`

```
Location:   ~/.claude/scripts/post-compact.sh
Fires when: Context compaction just finished
What it does:
  1. Reads ~/.claude/session-state.json
  2. Extracts: task, progress, decisions, active_files, next_steps, plan_file
  3. Outputs formatted summary to stdout
Output:     "--- SESSION STATE RESTORED AFTER COMPACTION ---"
            Task, Progress, Key decisions, Active files, Full plan
            "--- END STATE ---"
Where output goes: Into Claude's conversation context
Depends on: python3, session-state.json being up-to-date
```

#### `session-start.sh`

```
Location:   ~/.claude/scripts/session-start.sh
Fires when: New session starts (Notification event)
What it does:
  1. Checks if session-state.json exists
  2. If yes, reads timestamp and checks age
  3. If <24h old: outputs task/progress summary
  4. If >24h old: outputs summary + stale warning
  5. If file missing: outputs nothing
Output:     "--- PREVIOUS SESSION STATE FOUND ---" + task details
Where output goes: Into Claude's context (Claude should tell you about it)
Depends on: python3
```

#### `session-end.sh`

```
Location:   ~/.claude/scripts/session-end.sh
Fires when: Session closes (Stop event)
What it does:
  1. Copies session-state.json to session-logs/
  2. Filename: YYYY-MM-DD-HH-MM.json
  3. Does NOT delete session-state.json (it persists for next session)
Output:     NOTHING (runs as you exit)
Creates:    ~/.claude/session-logs/YYYY-MM-DD-HH-MM.json
```

#### `post-edit-log.sh`

```
Location:   ~/.claude/scripts/post-edit-log.sh
Fires when: Claude uses Edit or Write tool
Input:      JSON from stdin: {"tool_name":"Edit","tool_input":{"file_path":"/path/file"}}
What it does:
  1. Reads JSON from stdin
  2. Extracts tool_name and file_path (jq primary, grep fallback)
  3. Appends JSONL entry: {"ts":"...","tool":"Edit","file":"/path","project":"/cwd"}
  4. Trims log to 500 entries if over cap
Output:     NOTHING (silent background logging)
Creates:    ~/.claude/session-logs/edit-tracker.jsonl
Depends on: jq (with grep fallback)
```

#### `post-git-log.sh`

```
Location:   ~/.claude/scripts/post-git-log.sh
Fires when: Claude uses Bash tool
Input:      JSON from stdin: {"tool_name":"Bash","tool_input":{"command":"git commit -m ..."}}
What it does:
  1. Reads JSON from stdin
  2. Extracts command string
  3. Checks: Does command contain "git commit"?
     NO  → exits immediately (ignores non-commit commands)
     YES → extracts hash, message, branch from git log
  4. Appends JSONL entry
  5. Trims log to 200 entries if over cap
Output:     NOTHING (silent background logging)
Creates:    ~/.claude/session-logs/git-tracker.jsonl
Depends on: jq (with grep fallback), git
```

#### `memory-cleanup-reminder.sh`

```
Location:   ~/.claude/scripts/memory-cleanup-reminder.sh
Fires when: New session starts (Notification event, async)
What it does:
  1. Reads ~/.claude/session-logs/.last-memory-audit
  2. Compares timestamp to current time
  3. If >7 days old: outputs reminder
  4. If recent or file missing: outputs nothing
Output:     "Memory cleanup is overdue (N days since last audit)."
Where output goes: Into Claude's context
```

#### `prompt-shortcuts.sh`

```
Location:   ~/.claude/scripts/prompt-shortcuts.sh
Fires when: User types any message (UserPromptSubmit event)
Input:      JSON from stdin: {"message":{"content":"!fw 2"}}
What it does:
  1. Reads user's message from stdin JSON
  2. Checks against shortcut table:

     !fw [arg]  → {"message": "/fw [arg]"}
     !mc        → {"message": "/memory-cleanup"}
     !fs        → {"message": "/framework-status"}
     !sr        → {"message": "/session-review"}
     (anything else) → no output (message passes through unchanged)

  3. If matched: outputs JSON that replaces the user's message
Output:     JSON rewrite instruction OR nothing
Effect:     Claude receives "/fw 2" instead of "!fw 2"
```

---

## 5. Skills (5 Commands)

Skills are invoked by typing `/skill-name` in the chat. Each skill is a markdown file that tells Claude exactly what to do.

**IMPORTANT:** Skills must be in `folder/SKILL.md` format to be discovered by Claude Code.

### 5A. Skill Reference Table

| Command | Name | Location | What It Does |
|---|---|---|---|
| `/fw` | Framework Launcher | `~/.claude/skills/fw/SKILL.md` | Menu to access all other skills (1=cleanup, 2=status, 3=review, 4=all) |
| `/session-review` | Session Review | `~/.claude/skills/session-review/SKILL.md` | Analyzes session, suggests reusable artifacts (max 2 per session) |
| `/framework-status` | Framework Status | `~/.claude/skills/framework-status/SKILL.md` | Health check of all 10 framework components |
| `/memory-cleanup` | Memory Cleanup | `~/.claude/skills/memory-cleanup/SKILL.md` | Audits memories: stale, duplicate, orphaned, missing from index |
| `/omni-expert-interrogation` | OEIP | `~/.claude/skills/omni-expert-interrogation/SKILL.md` | Multi-domain expert panel analysis |

### 5B. Skill Details

#### `/fw` — Framework Launcher

```
Quick access to all framework maintenance tools.

Menu:
  1) Memory Cleanup    → runs /memory-cleanup
  2) Framework Status  → runs /framework-status
  3) Session Review    → runs /session-review
  4) Full Audit        → runs all three in sequence

Accepts arguments: /fw 2  or  /fw status
Accepts keywords:  cleanup, status, review, audit, all
Shortcut:          Type !fw instead of /fw
```

#### `/session-review` — Artifact Suggestion Engine

```
Analyzes your session and suggests reusable things to create.

6-step process:
  Step 1: Gathers session context (state, tasks, files, patterns)
  Step 2: Identifies artifact opportunities using this table:

          Pattern (3+ repeats)          → Suggests
          ─────────────────────────────────────────
          Same workflow                 → Skill
          Same debugging steps          → Diagnostic Script
          Same project setup            → Project Template
          Same prompt structure         → Prompt Template
          Automation opportunity         → Hook
          Specialized task              → Custom Agent

  Step 3: Presents max 2 suggestions with:
          - Type (Skill/Hook/Agent/Template/Script)
          - Exact file path
          - WHY it helps
          - Preview of contents
          - Estimated time saved

  Step 4: Waits for your approval (never creates without asking)
  Step 5: Creates approved artifacts using templates
  Step 6: Shows summary

Shortcut: Type !sr
Constraint: Maximum 2 suggestions per session
Threshold: Pattern must appear 3+ times to qualify
```

#### `/framework-status` — Health Diagnostic

```
Runs 10 checks on the framework:

  1.  Hook Scripts     — all 8 exist and are executable?
  2.  Settings Hooks   — all 8 events wired correctly?
  3.  Session State    — exists, fresh, valid JSON?
  4.  Memory System    — count, index integrity, stale check
  5.  Session Logs     — count, recent entries
  6.  CLAUDE.md Rules  — all required sections present?
  7.  PostToolUse      — edit/git trackers working?
  8.  Custom Agents    — 3 agents with correct models?
  9.  Skills           — all skills discovered?
  10. Templates        — all 5 templates present?

Output format:
  ╔══════════════════════════════════════╗
  ║  FRAMEWORK STATUS                    ║
  ║  Hook Scripts:   [OK/WARN/ERROR]    ║
  ║  ...                                 ║
  ║  Overall: [HEALTHY / NEEDS ATTENTION]║
  ╚══════════════════════════════════════╝

Shortcut: Type !fs
```

#### `/memory-cleanup` — Memory Audit

```
6-step memory hygiene process:

  Step 1: Discovers all memory directories across projects
  Step 2: Builds inventory table (file, type, age, indexed?)
  Step 3: Flags issues:
          Critical — files not in MEMORY.md (won't load)
          Critical — MEMORY.md entries pointing to deleted files
          Warning  — files older than 30 days (likely stale)
          Warning  — projects with 50+ memory files (cap exceeded)
          Info     — similar file names (possible duplicates)
  Step 4: Presents report with specific fix actions
  Step 5: Waits for your approval, acts on each one
  Step 6: Updates .last-memory-audit timestamp

Shortcut:      Type !mc
Auto-reminder: session-start warns if >7 days since last audit
Cap:           Max 50 memory entries per project
Stale:         >30 days = flagged for review
```

---

## 6. Agents (3 Specialists)

Agents are NOT automatic. You ask Claude to use them, or Claude decides to use them based on CLAUDE.md rules.

### 6A. Agent Reference Table

| Agent | Model | Cost | File | Role |
|---|---|---|---|---|
| `researcher` | haiku | Cheap + fast | `~/.claude/agents/researcher.md` | Read-only research across web, code, docs |
| `reviewer` | opus | Smart + thorough | `~/.claude/agents/reviewer.md` | Code review for bugs, security, performance |
| `analysis-lead` | opus | Coordinator | `~/.claude/agents/analysis-lead.md` | Spawns researcher + reviewer in parallel |

### 6B. How to Use Each Agent

#### Researcher Agent

```
Model:        haiku (fast, cheap)
Capabilities: WebSearch, WebFetch, Glob, Grep, Read
Constraints:  Read-only (cannot edit files)
               Report must be under 500 words
               Must cite sources
               Must include confidence level

When to use:
  - "Spawn a researcher to find how Redis sessions work in Flask"
  - "Use the researcher agent to explore the API endpoints in this project"
  - "Research agent: what are the best practices for JWT token rotation?"

Output format:
  ### Question
  ### Key Findings (with sources)
  ### Confidence (High/Medium/Low)
  ### Recommendations
```

#### Reviewer Agent

```
Model:        opus (smart, thorough)
Capabilities: Read, Glob, Grep (code analysis)
Constraints:  Read-only (cannot edit files — provides feedback only)
               Focuses on: correctness → security → performance → style
               Must reference specific file:line numbers
               No unnecessary nitpicks

When to use:
  - "Spawn the reviewer agent to check auth.py for security issues"
  - "Use the reviewer to review my last 3 commits"
  - "Reviewer agent: analyze this pull request for bugs"

Output format:
  ### Summary
  ### Critical Issues (must fix)
  ### Warnings (should fix)
  ### Suggestions (nice to have)
  ### Verdict: APPROVE / REQUEST CHANGES / NEEDS DISCUSSION
```

#### Analysis Lead Agent

```
Model:        opus (coordinator)
Capabilities: Spawns researcher + reviewer as teammates
Constraints:  Does NOT research or review itself
               Maximum 4 teammates per analysis
               Must spawn teammates in parallel (same message)
               Synthesizes findings into one report

When to use:
  - "Run an analysis-lead to review this entire codebase"
  - "Spawn analysis-lead: check security, performance, and documentation"
  - "Coordinate a full analysis of the authentication module"

How it works:
  1. Reads your request
  2. Breaks into 2-4 independent subtasks
  3. Spawns researcher + reviewer simultaneously
  4. Waits for both to report back
  5. Combines findings into one unified report

Output format:
  ### Analysis Report: [Topic]
  **Team:** [who did what]
  #### Key Findings (with source agent)
  #### Conflicts or Uncertainties
  #### Recommendations
  #### Confidence Level
```

### 6C. When Claude Uses Agents Automatically (CLAUDE.md Rules)

```
CLAUDE.md tells Claude to prefer agents for:

  Research/exploration tasks      → spawn researcher (haiku — saves money)
  Planning/architecture tasks     → spawn Plan sub-agent
  Multi-faceted analysis          → spawn analysis-lead or parallel agents
  Reading many files              → offload to sub-agent (keeps main context clean)
  Heavy/verbose output            → offload to sub-agent

These are RULES, not guarantees. Claude may or may not follow them
depending on the situation and model behavior.
```

---

## 7. Templates (5 Boilerplates)

Templates are used by `/session-review` when creating new artifacts, or manually when you want to create something new.

| Template | Location | Used For |
|---|---|---|
| `skill-template.md` | `~/.claude/templates/skill-template.md` | Creating new `/skill-name` commands |
| `agent-template.md` | `~/.claude/templates/agent-template.md` | Creating new agent definitions |
| `hook-template.json` | `~/.claude/templates/hook-template.json` | Adding new hook events to settings.json |
| `script-template.sh` | `~/.claude/templates/script-template.sh` | Creating new hook scripts |
| `prompt-template.md` | `~/.claude/templates/prompt-template.md` | Saving reusable prompt structures |

---

## 8. Storage Locations — What Gets Saved Where

### 8A. Files That Change Every Session

| File | Updated By | What It Contains | When It Changes |
|---|---|---|---|
| `~/.claude/session-state.json` | Claude (CLAUDE.md rules) + pre-compact.sh | Current task, progress, decisions, next steps | During session (should be frequent) |
| `~/.claude/session-logs/edit-tracker.jsonl` | post-edit-log.sh (auto) | Every file Claude edited: timestamp, tool, path | Every Edit/Write tool use |
| `~/.claude/session-logs/git-tracker.jsonl` | post-git-log.sh (auto) | Every git commit: timestamp, hash, message, branch | Every "git commit" command |

### 8B. Files Created Per Session

| File | Created By | What It Contains |
|---|---|---|
| `~/.claude/session-logs/YYYY-MM-DD-HH-MM.json` | session-end.sh (auto) | Snapshot of session-state.json at session close |

### 8C. Files That Change Occasionally

| File | Updated By | What It Contains | When It Changes |
|---|---|---|---|
| `~/.claude/projects/*/memory/*.md` | Claude (auto at breakpoints) | User prefs, project decisions, feedback | When Claude learns something about you |
| `~/.claude/projects/*/memory/MEMORY.md` | Claude (auto) | Index of all memory files | When memories are added/removed |
| `~/.claude/session-logs/.last-memory-audit` | /memory-cleanup skill | Timestamp of last audit | When you run /memory-cleanup |

### 8D. Files That Rarely Change

| File | What It Contains | When To Edit |
|---|---|---|
| `~/.claude/settings.json` | Hook wiring, permissions, plugin config | When adding new hooks |
| `~/.claude/CLAUDE.md` | Rules Claude follows | When changing framework behavior |
| `~/.claude/keybindings.json` | Keyboard shortcuts | When adding/changing shortcuts |
| `~/.claude/scripts/*.sh` | Hook script logic | When fixing bugs or adding features |
| `~/.claude/skills/*/SKILL.md` | Skill definitions | When improving a skill |
| `~/.claude/agents/*.md` | Agent definitions | When changing agent behavior |

### 8E. How to Inspect Everything

```bash
# See current session state
cat ~/.claude/session-state.json | python3 -m json.tool

# See last 10 file edits
tail -10 ~/.claude/session-logs/edit-tracker.jsonl | jq .

# See all git commits tracked
cat ~/.claude/session-logs/git-tracker.jsonl | jq .

# See how many session archives exist
ls ~/.claude/session-logs/*.json | wc -l

# See latest session archive
ls -t ~/.claude/session-logs/*.json | head -1 | xargs cat | python3 -m json.tool

# See all memories for current project
find ~/.claude/projects -name "*.md" -path "*/memory/*" -not -name "MEMORY.md"

# See memory index
cat ~/.claude/projects/*/memory/MEMORY.md

# See when last memory audit happened
cat ~/.claude/session-logs/.last-memory-audit

# Check if all scripts are executable
ls -la ~/.claude/scripts/*.sh
```

---

## 9. Plugin (Self-Contained Backup)

```
Location: ~/.claude/plugins/local/context-framework/
Enabled:  "context-framework@local": true  in settings.json
```

### 9A. Plugin Structure

```
~/.claude/plugins/local/context-framework/
├── .claude-plugin/
│   └── plugin.json              ← name: "context-framework", version: "1.0.0"
├── .mcp.json                    ← MCP server config (4 tools)
├── hooks/
│   └── hooks.json               ← Mirror of settings.json hooks section
├── scripts/
│   ├── pre-compact.sh           ← Copy of ~/.claude/scripts/
│   ├── post-compact.sh
│   ├── session-start.sh
│   ├── session-end.sh
│   ├── post-edit-log.sh
│   ├── post-git-log.sh
│   ├── memory-cleanup-reminder.sh
│   ├── prompt-shortcuts.sh
│   └── mcp-framework-tools.sh   ← MCP server (EXTRA — not in main scripts)
├── skills/                       ← Copy of ~/.claude/skills/
│   ├── fw/SKILL.md
│   ├── session-review/SKILL.md
│   ├── framework-status/SKILL.md
│   └── memory-cleanup/SKILL.md
└── agents/                       ← Copy of ~/.claude/agents/
    ├── researcher.md
    ├── reviewer.md
    └── analysis-lead.md
```

### 9B. MCP Server Tools

The plugin provides 4 MCP tools via `mcp-framework-tools.sh`:

| Tool | What It Returns |
|---|---|
| `session_log_stats` | Count of session logs, most recent, oldest |
| `memory_stats` | Memory file counts per project |
| `recent_edits` | Last N entries from edit-tracker.jsonl |
| `recent_commits` | Last N entries from git-tracker.jsonl |

### 9C. Plugin vs Main Framework

```
MAIN FRAMEWORK (active)              PLUGIN (backup)
─────────────────────                ───────────────
~/.claude/scripts/                   plugins/.../scripts/
~/.claude/skills/                    plugins/.../skills/
~/.claude/agents/                    plugins/.../agents/
~/.claude/settings.json hooks       plugins/.../hooks/hooks.json

Both are active simultaneously.
Plugin is NOT auto-synced.
If you edit a script in ~/.claude/scripts/, manually copy it to the plugin too.
```

---

## 10. Keybindings

Custom keybindings added by the framework in `~/.claude/keybindings.json`:

| Shortcut | Context | Action | Description |
|---|---|---|---|
| `Ctrl+Shift+F` | Global | `app:globalSearch` | Search across all files |
| `Ctrl+Shift+P` | Global | `app:quickOpen` | Quick open file/command |
| `Ctrl+X Ctrl+K` | Chat | `chat:killAgents` | Kill all running agents |

**Note:** Keybindings CANNOT trigger skills directly. That's why prompt shortcuts (`!fw`, `!mc`, etc.) exist as a workaround.

---

## 11. Prompt Shortcuts

Type these instead of full slash commands:

| You Type | Claude Receives | Skill Invoked |
|---|---|---|
| `!fw` | `/fw` | Framework launcher menu |
| `!fw 1` | `/fw 1` | Jump to Memory Cleanup |
| `!fw 2` | `/fw 2` | Jump to Framework Status |
| `!fw 3` | `/fw 3` | Jump to Session Review |
| `!fw 4` | `/fw 4` | Run Full Audit (all three) |
| `!mc` | `/memory-cleanup` | Memory audit |
| `!fs` | `/framework-status` | Health check |
| `!sr` | `/session-review` | Artifact suggestion |

These are handled by `prompt-shortcuts.sh` via the UserPromptSubmit hook.
The transformation happens BEFORE Claude sees your message.

---

## 12. OEIP Constraints

These are the hard rules the framework must follow (verified by Level 4 compliance tests):

| Constraint | Value | Where Enforced |
|---|---|---|
| Hook timeout | 2 seconds max | `settings.json` → every hook has `"timeout": 2` |
| Pattern threshold | 3+ repetitions | `CLAUDE.md` + `session-review/SKILL.md` |
| Suggestions per session | Max 2 | `session-review/SKILL.md` |
| Memory entries per project | Max 50 | `CLAUDE.md` + `memory-cleanup/SKILL.md` |
| Memory stale threshold | 30 days | `memory-cleanup/SKILL.md` |
| Memory audit reminder | 7 days | `memory-cleanup-reminder.sh` |
| MEMORY.md index | Max 200 lines | `CLAUDE.md` |
| Script error behavior | Exit 0 (fail-silent) | All scripts use `exit 0` and `try/except` |
| Script execution time | Under 2 seconds | All scripts tested at <300ms |
| Agent models | researcher=haiku, reviewer=opus, analysis-lead=opus | Agent `.md` frontmatter |
| Edit tracker cap | 500 entries | `post-edit-log.sh` |
| Git tracker cap | 200 entries | `post-git-log.sh` |

---

## 13. CLAUDE.md Rules — What Claude Is Told

The `~/.claude/CLAUDE.md` file contains 4 main rule sections that Claude reads at session start:

### Rule 1: Context Window Optimization

```
Claude is told to:
  - Delegate research/exploration → spawn researcher agent (haiku)
  - Delegate planning → spawn Plan sub-agent
  - Delegate multi-faceted analysis → use parallel agents or analysis-lead
  - Use Glob/Grep for file searches (not Read entire files)
  - Offload heavy/verbose tasks to sub-agents
```

### Rule 2: Track Progress With Tasks

```
Claude is told to:
  - Use TaskCreate for work items
  - Update tasks as they complete
  - This creates visible progress that survives compaction
```

### Rule 3: Maintain Session State

```
Claude is told to write to session-state.json:
  - After completing a significant task
  - After making a key decision
  - Before suggesting /compact
  - When conversation reaches 15+ exchanges

Format: {"timestamp","project_dir","task","progress","decisions","active_files","next_steps"}
```

### Rule 4: Post-Compaction Recovery

```
Claude is told to:
  - Read the state summary injected by post-compact.sh
  - Acknowledge it and continue from where it left off
  - NOT re-ask the user what they were working on
```

### Memory Management Rules

```
Claude is told to:
  - Auto-save memories at natural breakpoints
  - Check for duplicates before creating
  - Update stale memories instead of creating new ones
  - Keep MEMORY.md under 200 lines
  - Cap at 50 entries per project
```

### Reusable Component Detection Rules

```
Claude is told to watch for:
  - Same workflow 3+ times → suggest SKILL
  - Same debugging steps → suggest DIAGNOSTIC SCRIPT
  - Same project setup → suggest PROJECT TEMPLATE
  - Same prompt structure → suggest PROMPT TEMPLATE
  - Automation opportunity → suggest HOOK

Protocol: Describe what + why + preview → wait for approval → NEVER auto-create
```

### Tiered Approval System

```
AUTO (silent):        Memory saves, session state, session logs, task tracking
DESCRIBE & ASK:       New skills, hooks, agents, templates, scripts
EXPLICIT REQUEST ONLY: settings.json changes, CLAUDE.md changes, plugin installs
```

---

## 14. Known Limitations

### 14A. Session State Depends on Claude's Behavior

```
PROBLEM:  session-state.json is updated by Claude following CLAUDE.md rules,
          NOT by an automated hook. Claude may not always update it.
IMPACT:   If state is stale when compaction happens, post-compact restores old info.
WORKAROUND: You can tell Claude: "Update the session state now"
            or check with: cat ~/.claude/session-state.json
```

### 14B. Hook Output is Invisible to You

```
PROBLEM:  session-start.sh and memory-cleanup-reminder.sh output goes into
          Claude's context, not your terminal screen. You never see it directly.
IMPACT:   You don't see the "resume previous session?" prompt — Claude does.
          Whether Claude acts on it depends on model behavior.
WORKAROUND: If Claude doesn't mention your previous session, just tell it:
            "Read ~/.claude/session-state.json and continue where I left off"
```

### 14C. Plugin is Not Auto-Synced

```
PROBLEM:  The plugin at plugins/local/context-framework/ is a manual copy.
          Editing ~/.claude/scripts/foo.sh does NOT update the plugin copy.
IMPACT:   Plugin may become outdated if you make changes.
WORKAROUND: After editing any framework file, copy it to the plugin too:
            cp ~/.claude/scripts/foo.sh ~/.claude/plugins/local/context-framework/scripts/
```

### 14D. Skills Must Use folder/SKILL.md Format

```
PROBLEM:  Claude Code only discovers skills in ~/.claude/skills/name/SKILL.md format.
          Single files like skills/name.md are NOT discovered.
IMPACT:   If you create a skill as a single file, /skill-name won't work.
WORKAROUND: Always create skills as:
            mkdir -p ~/.claude/skills/my-skill/
            Then put the content in ~/.claude/skills/my-skill/SKILL.md
```

### 14E. Shortcuts Only Work for Defined Aliases

```
PROBLEM:  Only 4 shortcuts are defined: !fw, !mc, !fs, !sr
          Any other !command passes through unchanged.
IMPACT:   New skills don't automatically get shortcuts.
WORKAROUND: Edit ~/.claude/scripts/prompt-shortcuts.sh to add new cases.
```

---

## 15. Common Tasks — Quick Reference

### Check framework health
```
Type: /fw 2   or   !fs   or   /framework-status
```

### Audit memories
```
Type: /fw 1   or   !mc   or   /memory-cleanup
```

### Review session for reusable artifacts
```
Type: /fw 3   or   !sr   or   /session-review
```

### Run full audit (all three)
```
Type: /fw 4
```

### See what Claude has been editing
```bash
tail -20 ~/.claude/session-logs/edit-tracker.jsonl | jq .
```

### See git commits Claude made
```bash
cat ~/.claude/session-logs/git-tracker.jsonl | jq .
```

### See current session state
```bash
cat ~/.claude/session-state.json | python3 -m json.tool
```

### See session history
```bash
ls -lt ~/.claude/session-logs/*.json | head -10
```

### Force Claude to update session state
```
Tell Claude: "Update session-state.json with our current progress"
```

### Resume previous session in new session
```
Tell Claude: "Read ~/.claude/session-state.json and continue where I left off"
```

### Spawn a research agent
```
Tell Claude: "Spawn a researcher agent to investigate [topic]"
```

### Spawn a code reviewer
```
Tell Claude: "Spawn the reviewer agent to check [file/PR] for issues"
```

### Spawn a full analysis team
```
Tell Claude: "Run an analysis-lead to review [codebase/module] for security, performance, and quality"
```

### Create a new skill
```
1. mkdir -p ~/.claude/skills/my-skill/
2. Copy ~/.claude/templates/skill-template.md to ~/.claude/skills/my-skill/SKILL.md
3. Edit the SKILL.md with your skill's logic
4. Restart Claude Code session for it to be discovered
```

### Create a new agent
```
1. Copy ~/.claude/templates/agent-template.md to ~/.claude/agents/my-agent.md
2. Set the model (haiku for cheap/fast, opus for smart)
3. Define the agent's role, capabilities, and constraints
4. Available immediately — tell Claude to "spawn my-agent"
```

### Add a new hook
```
1. Create script in ~/.claude/scripts/my-hook.sh
2. Make executable: chmod +x ~/.claude/scripts/my-hook.sh
3. Add to ~/.claude/settings.json under the appropriate event
4. Use ~/.claude/templates/hook-template.json as reference
```

### Add a new prompt shortcut
```
1. Edit ~/.claude/scripts/prompt-shortcuts.sh
2. Add a new case in the case/esac block:
   "!xx")
       echo '{"message": "/my-skill"}'
       ;;
3. Works immediately in next message
```

---

*This document is your single source of truth for the entire framework.*
*Keep it updated when you make changes.*
