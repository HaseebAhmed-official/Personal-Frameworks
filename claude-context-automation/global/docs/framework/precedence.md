# Precedence Contract

This framework uses one precedence model across instructions, configuration, memory, and automation.

## Ordered Precedence
1. Enterprise managed settings and IAM restrictions
2. Explicit user approvals and denials in the active session
3. The active task request and the currently invoked slash/custom command
4. Hook-enforced controls
5. Project `CLAUDE.md` and imported project rule packs
6. Project `.claude/settings.json`
7. Project `.claude/settings.local.json`
8. User `~/.claude/CLAUDE.md` and user settings
9. MCP-provided prompts, tools, and resources
10. Transcript-derived summaries and resume state
11. Framework ledgers such as `MEMORY.md`

## Conflict Rules
- Enterprise policy cannot be overridden downstream.
- Session-specific approval overrides framework defaults for that session only.
- Transcript summaries cannot override durable approved policy or memory.
- Framework conventions refine behavior but cannot contradict native policy or settings.
- If two durable memory items conflict at the same scope, the newer approved item wins provisionally and the older one is marked for review.

## Practical Use
- Treat `settings.local.json` as personal local override only; do not encode shared policy there.
- Use `CLAUDE.md` and imported rule packs for durable shared behavior.
- Use `MEMORY.md` as a ledger and review surface, not as a replacement for project policy.
