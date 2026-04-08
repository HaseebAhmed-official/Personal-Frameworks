# Framework Simulation: A New Session from Start to Finish

This document traces exactly what happens — hook by hook, message by message — when a user opens Claude Code in a project that uses the merged context automation framework.

---

## 1. Session Start

**Trigger:** User opens Claude Code (or runs `claude` in the terminal).

**Hook fires:** `SessionStart` → `python3 ~/.claude/scripts/hooks/session_start.py`

**What the hook does:**

1. Reads `~/.claude/session-state.json`
2. Checks the `timestamp` field against the current time
3. Decision branch:

| State file condition | Hook output |
|---|---|
| File missing / empty | Emits framework-load reminder only |
| Timestamp > 24 hours ago | Emits "stale session" notice (no resume offer) |
| Timestamp ≤ 24 hours ago | Emits full resume block with prior task/decisions/next_action |

**What Claude sees (recent session example):**

```
[SYSTEM] SESSION STATE RESTORED
─────────────────────────────────
task: "Implement merged framework Phase 3 — agents and commands"
progress: "Phase 1 (hooks) ✓  Phase 2 (governance) ✓  Phase 3 in progress"
decisions: ["Use Python for all hooks", "Keep bash hooks' functionality", "Add 7 agents total"]
blockers: []
next_steps: ["Add governance commands", "Add output-styles", "Run validate_framework.py"]
active_files: [".claude/commands/", ".claude/agents/", ".claude/output-styles/"]
─────────────────────────────────
Load: @~/.claude/CLAUDE.md  @~/.claude/RULES.md  @~/.claude/MEMORY.md
      @~/.claude/docs/framework/governance.md
```

**Claude's first visible response:** Picks up the task from next_steps without asking "what were we doing?"

---

## 2. User Types First Message

**Trigger:** User submits a prompt (e.g., "let's keep going on Phase 3").

**Hook fires:** `UserPromptSubmit` → `python3 ~/.claude/scripts/hooks/user_prompt_submit.py`

**Shortcut expansion table:**

| User types | Claude receives |
|---|---|
| `!fw` | `/fw` |
| `!fw 2` | `/fw 2` |
| `!mc` | `/memory-cleanup` |
| `!fs` | `/framework-status` |
| `!sr` | `/session-review` |
| Anything else | Unchanged |

**Governance keyword detection:**

| Keyword in prompt | Injected systemMessage |
|---|---|
| "agent team" | "⚠ Agent teams require explicit approval (RULES.md Level 2). Describe the team and get user sign-off before launching." |
| "remember" / "memory" | "⚠ Durable memory requires explicit approval. Use /governance:memory-proposal to classify the candidate first." |

**What Claude actually receives vs what the user typed:**

- Plain prompt `"let's keep going on Phase 3"` → arrives unchanged, no injection
- Prompt `"!fs"` → arrives as `/framework-status` (shortcut expanded)
- Prompt `"remember this for next time"` → arrives with a governance reminder appended as a system message

---

## 3. Claude Delegates Research to a Subagent

**Trigger:** Claude calls the `Agent` tool to spawn a sub-agent.

**On spawn:** No hook fires. The Agent tool is not intercepted by PreToolUse or PostToolUse.

**The sub-agent runs independently.** It has its own context window, reads files, makes tool calls. None of those tool calls trigger the parent's hooks.

**When the sub-agent finishes:** `SubagentStop` fires → `python3 ~/.claude/scripts/hooks/subagent_stop.py`

**Quality gate logic:**

```
output = payload.get("output", "")
missing = []
if "Findings" not in output and "findings" not in output:
    missing.append("Findings")
if "Risk" not in output and "risk" not in output:
    missing.append("Risks")
if "Next Action" not in output and "next action" not in output:
    missing.append("Recommended Next Action")
```

| Output contains all three | Hook response |
|---|---|
| Yes | `{"continue": True}` — silent pass |
| No | `{"continue": True, "systemMessage": "⚠ Subagent output missing: [Findings / Risks / Next Action]. Ask the agent to restate with those sections."}` |

**Claude sees the quality gate reminder** and can prompt the user or re-query the agent if the output was incomplete.

---

## 4. Claude Edits a File

**Trigger:** Claude calls `Edit`, `Write`, or `MultiEdit`.

**PreToolUse fires first:** `python3 ~/.claude/scripts/hooks/pre_tool_use.py`

**Framework file protection gate:**

```python
FRAMEWORK_FILES = {
    'CLAUDE.md', 'RULES.md', 'MEMORY.md',
    '.claude/settings.json', '.claude/settings.local.json'
}
```

| Target file | Hook response |
|---|---|
| Normal file (e.g., `src/app.py`) | `{"continue": True}` — passes through silently |
| Framework file (e.g., `CLAUDE.md`) | `{"continue": False, "stopReason": "⚠ FRAMEWORK FILE PROTECTION: Editing CLAUDE.md requires explicit user approval (RULES.md Level 1). State what you want to change and why, then wait for the user to approve."}` |

**If passed:** Edit executes.

**PostToolUse fires after:** `python3 ~/.claude/scripts/hooks/post_tool_use.py`

```
toolName = "Edit"
file_path = payload["toolInput"]["file_path"]
→ Appends to ~/.claude/session-logs/edit-tracker.jsonl:
  {"timestamp": "2026-04-08T14:23:11Z", "tool": "Edit", "file": "src/app.py", "session": "..."}
→ Trims to last 500 entries if needed
→ Emits systemMessage: "State ledger reminder: if this edit resolves a decision or blocker, update session-state.json."
```

---

## 5. Claude Runs a Git Commit

**Trigger:** Claude calls `Bash` with a `git commit` command.

**PreToolUse fires:** `python3 ~/.claude/scripts/hooks/pre_tool_use.py`

`git commit` is not a framework file edit → `{"continue": True}` silently.

**The commit executes.**

**PostToolUse fires:** `python3 ~/.claude/scripts/hooks/post_tool_use.py`

```
toolName = "Bash"
command = "git commit -m 'Add governance agents'"
→ Detected: "git commit" in command
→ Runs: git log -1 --format="%H|%s|%ai"
→ Appends to ~/.claude/session-logs/git-tracker.jsonl:
  {"timestamp": "2026-04-08T14:31:00Z", "hash": "a3f9c12", "subject": "Add governance agents", "author_date": "2026-04-08T14:31:00+00:00"}
→ Trims to last 200 entries if needed
```

No system message injection for git commits — tracking is silent.

---

## 6. Context Fills Up → Compaction

**When it happens:** Context window reaches ~83.5% full (the autocompact buffer threshold).

**PreCompact fires:** `python3 ~/.claude/scripts/hooks/pre_compact.py`

```python
state = read_session_state()
state['last_compaction'] = get_current_time_iso()
state['compaction_count'] = state.get('compaction_count', 0) + 1
write_session_state(state)
return emit({'continue': True})
```

The session state is **timestamped** before the conversation is summarized. This snapshot is durable — it will survive the compaction.

**Compaction runs.** The full conversation is summarized into a compressed form. Earlier messages are replaced by a summary block.

**PostCompact fires:** `python3 ~/.claude/scripts/hooks/post_compact.py`

Reads `session-state.json` and emits it as a `systemMessage`:

```
[SYSTEM] SESSION STATE RESTORED after compaction #2
─────────────────────────────────
task: "Add governance agents to ~/.claude/agents/"
progress: "4 of 7 agents written"
decisions: ["Use sonnet model for all governance agents"]
blockers: []
next_steps: ["Write verification-auditor.md", "Run validate_framework.py"]
last_compaction: "2026-04-08T14:45:00Z"
─────────────────────────────────
```

**Claude resumes** with full context of where it was, what was decided, and what to do next — no re-asking the user.

---

## 7. User Asks Claude to Remember Something

**Trigger:** User types "remember that we always use sonnet for governance agents".

**UserPromptSubmit fires:** Detects "remember" keyword.

**Injected systemMessage:**

```
⚠ Durable memory requires explicit user approval (RULES.md Level 2).
Before saving, use /governance:memory-proposal to classify this candidate:
  - Class (enterprise-policy / project-operating / personal-preference / ...)
  - Scope (global / project / session)
  - Sensitivity (public / internal / confidential)
  - Review date
Wait for the user to approve the classified proposal before writing to MEMORY.md.
```

**Claude's behavior:**

1. Does NOT silently write to MEMORY.md
2. Invokes `/governance:memory-proposal` or manually walks through the classification
3. Presents the classified proposal to the user
4. Waits for explicit "yes, save it"
5. Only then writes the entry with all required fields

**What gets written (approved entry):**

```json
{
  "id": "pref-agent-model-2026-04-08",
  "class": "personal-preference",
  "owner": "user",
  "scope": "global",
  "source": "user-stated",
  "provenance": "session e17fc49c",
  "sensitivity": "internal",
  "approval_state": "approved",
  "created_at": "2026-04-08T14:50:00Z",
  "review_at": "2026-07-08T00:00:00Z",
  "content": "Always use sonnet model for governance agents (governance-reviewer, memory-curator, verification-auditor, context-researcher)"
}
```

---

## 8. Session Ends

**Trigger:** User closes Claude Code, or the session ends naturally.

**Stop fires:** `python3 ~/.claude/scripts/hooks/stop.py`

```python
state_file = Path.home() / ".claude" / "session-state.json"
logs_dir = Path.home() / ".claude" / "session-logs"
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
archive_path = logs_dir / f"{timestamp}.json"
shutil.copy2(state_file, archive_path)
```

**Result:** `~/.claude/session-logs/2026-04-08T14-55-00Z.json` — a frozen snapshot of the session's final state.

**Next session:** `session_start.py` finds this file (< 24h old), loads it, and offers a resume block. The cycle begins again.

---

## 9. Full Precedence Resolution Example

**Scenario:** User asks "remember this preference" in the middle of a task. The task requires staying focused. A hook wants to inject a governance reminder. What wins?

**The 11-level hierarchy (RULES.md):**

```
Level 1  — Enterprise policy         (not applicable here)
Level 2  — Explicit approval gates   (memory save requires approval)
Level 3  — Task request              (user's current task: stay focused)
Level 4  — Hooks                     (UserPromptSubmit governance reminder)
Level 5  — Project CLAUDE.md rules   (never auto-save durable memory)
Level 6  — Settings permissions      (allow list)
Level 7  — Local overrides           (none)
Level 8  — UI preferences            (none)
Level 9  — MCP resources             (none)
Level 10 — Conversation transcripts  (prior context)
Level 11 — Framework ledgers         (session-state.json)
```

**Resolution walkthrough:**

1. Hook (Level 4) fires, injects governance reminder — this is allowed, it's advisory not blocking
2. Task request (Level 3) says stay focused → Claude acknowledges but does NOT pivot to memory workflow mid-task
3. Explicit approval gate (Level 2) says memory save requires approval → Claude cannot save without approval even if user said "remember"
4. Project CLAUDE.md (Level 5) reinforces: "never persist durable memory automatically"

**Outcome:** Claude says "Noted — I'll propose this as a memory candidate after we finish the current task. Continuing with [task]." The preference is held in session-state.json (session tier, no approval needed) and formally proposed at task completion.

**Key principle:** Higher level wins when there is a conflict. Advisory hooks (Level 4) never override explicit approval gates (Level 2). Task continuity (Level 3) is respected over convenience automations (Level 4).

---

## 10. Data Flow Diagram

```
User Input
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Claude Code Harness                                         │
│                                                              │
│  UserPromptSubmit                                            │
│  ┌────────────────────────────────────────────────────┐     │
│  │  stdin: {"prompt": "user text", "session_id": ...} │     │
│  │              │                                      │     │
│  │              ▼                                      │     │
│  │  user_prompt_submit.py                              │     │
│  │  ┌─────────────────────────────────────────┐       │     │
│  │  │  load_payload() ← stdin                 │       │     │
│  │  │  expand shortcuts (!fw → /fw)           │       │     │
│  │  │  detect governance keywords             │       │     │
│  │  │  emit({"message": rewritten_prompt})    │       │     │
│  │  │       OR                                │       │     │
│  │  │  emit({"continue": True,                │       │     │
│  │  │        "systemMessage": "⚠ reminder"}) │       │     │
│  │  └────────────────────┬────────────────────┘       │     │
│  │                       │ stdout JSON                  │     │
│  └───────────────────────┼──────────────────────────── ┘     │
│                          │                                    │
│                          ▼                                    │
│                   Harness reads stdout                        │
│                   • "message" → replaces prompt               │
│                   • "systemMessage" → prepended to context    │
│                   • "continue: false" → blocks tool call      │
│                                                               │
│  Tool call pipeline (for every tool):                        │
│                                                               │
│  Claude decides to call Edit("src/app.py", ...)              │
│      │                                                        │
│      ▼                                                        │
│  PreToolUse → pre_tool_use.py                                 │
│      │  checks FRAMEWORK_FILES                                │
│      │  → blocked? emit({"continue": false, "stopReason"})   │
│      │  → allowed? emit({"continue": true})                  │
│      ▼                                                        │
│  Tool executes (Edit runs)                                    │
│      │                                                        │
│      ▼                                                        │
│  PostToolUse → post_tool_use.py                               │
│      │  Edit/Write/MultiEdit → append edit-tracker.jsonl     │
│      │  Bash "git commit" → run git log, append git-tracker  │
│      │  emit({"continue": true, "systemMessage": "..."})     │
│      ▼                                                        │
│  systemMessage injected into Claude's next context turn       │
│                                                               │
│  Compaction pipeline:                                         │
│                                                               │
│  Context ~84% full                                            │
│      ▼                                                        │
│  PreCompact → pre_compact.py                                  │
│      │  timestamps session-state.json                        │
│      ▼                                                        │
│  Compaction summarizes conversation                           │
│      ▼                                                        │
│  PostCompact → post_compact.py                                │
│      │  reads session-state.json                             │
│      │  emit({"continue": true, "systemMessage": "RESTORED"})│
│      ▼                                                        │
│  Claude resumes with full state context                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Persistent files written during session:
  ~/.claude/session-state.json          ← live session recovery doc
  ~/.claude/session-logs/edit-tracker.jsonl   ← every file edit
  ~/.claude/session-logs/git-tracker.jsonl    ← every git commit
  ~/.claude/session-logs/audit-log.jsonl      ← framework events
  ~/.claude/session-logs/YYYY-MM-DDTHH-MM-SSZ.json  ← archived at Stop
```

---

*This simulation covers the full lifecycle of a single session. Each section maps directly to a hook script in `~/.claude/scripts/hooks/`. For the formal governance rules that govern every decision above, see `~/.claude/RULES.md` and `~/.claude/docs/framework/governance.md`.*
