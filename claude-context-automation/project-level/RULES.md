# Framework Rules

## Source Classification
Every reusable component in this framework must be one of:
- Native Claude feature
- Framework convention
- Experimental orchestration pattern
- External integration

Do not blur these categories in documentation or automation.

## Precedence
Follow the precedence model in `docs/framework/precedence.md`.

High-level order:
1. Enterprise managed policy and IAM restrictions
2. Current explicit user approvals or denials
3. Current task request and active command invocation
4. Hook-enforced controls
5. Project `CLAUDE.md` and imported project rules
6. Project `.claude/settings.json`
7. Project `.claude/settings.local.json`
8. User-level memory and settings
9. MCP-provided resources and prompts
10. Transcript-derived summaries and framework ledgers

## Routing Rules
- Stay in the main thread when work is sequential, local, and under control.
- Use targeted `@` references before pasting large context.
- Use a subagent when the task is bounded and only the distilled result needs to return.
- Use an agent team when multiple workers need to coordinate directly or challenge each other.
- Compact before continuing if the thread is carrying too many unresolved branches.
- Resume before acting if the session state is incomplete.

## Agent Team Defaults
- Agent teams are experimental and opt-in.
- Start with 3 teammates unless the task clearly needs more.
- Default maximum active workers: 3
- Default maximum verifier roles: 1
- Default pattern: coordinator + specialists + optional verifier
- Prefer research, review, and competing-hypothesis work before multi-file implementation

## Durable Memory Rules
- `auto-memory` may propose, but never write durable memory on its own.
- Every durable memory entry needs owner, scope, provenance, approval state, and review date.
- Conflicting memory creates a review item instead of an overwrite.

## Safety Rules
- Do not expose secrets or broad sensitive directories through `@directory`.
- Do not use `!` shell commands in custom commands for unreviewed destructive actions.
- Do not let automation surfaces persist durable memory without approval.
