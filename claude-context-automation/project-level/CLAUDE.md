# Context Orchestration Contract

This project installs a Claude Code framework for context management, delegation, memory curation, and governance.

Load and follow these artifacts before major work:
- `@RULES.md`
- `@MEMORY.md`
- `@docs/framework/precedence.md`
- `@docs/framework/agent-teams.md`
- `@docs/framework/governance.md`
- `@docs/framework/components.md`
- `@docs/framework/smoke-test.md`

## Session Priorities
1. Preserve state and recoverability.
2. Keep the main context compact and decision-focused.
3. Improve quality through controlled delegation.
4. Respect approval, security, and governance constraints.

## Mandatory Operating Behavior
- Keep the main thread limited to goals, accepted decisions, blockers, approvals, and next actions.
- Use `TodoWrite` for active task tracking instead of carrying large working sets in conversation.
- Prefer targeted context with `@file`, `@directory`, and `@mcp:resource` over dumping raw content.
- Validate reusable component changes with `python3 .claude/scripts/validate_framework.py` after edits.
- Prefer a single session for sequential or tightly coupled work.
- Use subagents for bounded tasks where only the result needs to return.
- Use agent teams only when parallel work and teammate-to-teammate communication materially improve the result.
- Treat agent teams as experimental and get explicit user approval before creating one.
- Never persist durable memory automatically.
- Never create or modify reusable framework components without explicit user approval.

## Required Approval Gates
Get explicit user approval before:
- saving durable memory
- editing `CLAUDE.md`, `RULES.md`, `MEMORY.md`, or `.claude/settings.json`
- creating or changing hooks, subagents, custom commands, or output styles
- enabling new MCP servers or external integrations
- launching an agent team

## State Ledger Requirement
Before compact, resume, stop, or handoff, capture:
- goal
- constraints
- accepted decisions
- blockers
- next action
- pending approvals
- persistence candidates

Use `MEMORY.md` and the contracts in `docs/framework/` as the source of truth for storage classes and precedence.
