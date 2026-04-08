# Claude Code Smoke Test

Run these checks inside Claude Code after opening this project.

## 1. Session bootstrap
- Confirm `CLAUDE.md` is loaded.
- Confirm the status line renders.
- Confirm the session start hook message appears.

Expected result:
- The assistant references the context-orchestration framework and approval rules.

## 2. Command discovery
Run:
- `/context-audit`
- `/governance:resume-ledger`
- `/governance:memory-proposal`

Expected result:
- Each command is discoverable and returns structured output.

## 3. Output style switching
Switch to:
- `context-lean`
- `governed-execution`

Expected result:
- Response behavior changes without breaking task continuity.

## 4. Hook behavior
Trigger:
- a normal read-only action
- an edit to a framework file
- a compact event

Expected result:
- read-only work continues normally
- framework-file edits produce a governance reminder
- compact produces the handoff reminder

## 5. Subagent discovery
Use `/agents` and verify these agents are visible:
- `context-researcher`
- `verification-auditor`
- `memory-curator`
- `governance-reviewer`

Expected result:
- Agents are discoverable and their descriptions match the intended roles.

## 6. Agent team flow
Only after explicit approval, run an agent team flow using the research team template.

Expected result:
- the team launches
- roles stay bounded
- outputs return as concise findings
- lead synthesis remains compact

## 7. Resume and compact
- Work for several turns
- compact
- resume
- reconstruct the session with `/governance:resume-ledger`

Expected result:
- goal, constraints, decisions, blockers, next action, and pending approvals survive.

## 8. Validation scripts
From the project root, run:

```bash
python3 .claude/scripts/validate_framework.py
python3 .claude/scripts/audit_log.py
```

Expected result:
- validation passes
- audit log seed file is created or updated under `.claude/logs/`
