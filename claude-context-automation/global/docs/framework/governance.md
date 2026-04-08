# Governance Contract

## Approval Matrix
Explicit user approval is required for:
- durable memory writes
- edits to framework policy files
- creating or modifying hooks
- creating or modifying subagents
- creating or modifying custom commands
- creating or modifying output styles
- launching agent teams
- enabling or widening MCP integrations

Autonomous actions allowed:
- read-only analysis
- targeted context loading
- use of existing subagents for bounded tasks
- transient state updates

## Trust Boundaries
### Hooks
- Enforce deterministic checks
- Must fail closed for sensitive policy violations

### MCP
- Allowlisted servers only
- No durable memory writes from MCP-triggered automation

### Custom Commands
- Prefer prompt-only workflows
- Shell-backed commands must remain minimal and reviewable

### SDK and CI
- Use bounded turns and structured output
- Record audit-friendly logs
- Do not bypass approval gates for memory or reusable component creation

## Transcript Governance
- Treat resume state and transcripts as sensitive operational artifacts
- Do not treat transcript summaries as durable memory unless explicitly approved
- Redact or avoid secret-bearing context before broad sharing

## Observability
Track:
- compact frequency
- resume success
- delegation count
- agent team launches
- pending approvals
- hook failures
- context pressure
- cost spikes
