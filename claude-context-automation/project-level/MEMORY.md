# Memory Ledger

This file is a framework convention, not a native Claude Code primitive.

## Memory Taxonomy
### Enterprise policy memory
- Scope: organization-wide
- Examples: managed settings, IAM restrictions, compliance controls
- Write policy: enterprise-controlled only

### Project operating memory
- Scope: shared repository behavior
- Examples: architecture constraints, approval rules, team workflows
- Write policy: explicit user or maintainer approval

### Personal durable preference memory
- Scope: user-specific durable working preferences
- Examples: preferred communication style, review strictness, default delegation posture
- Write policy: explicit user approval

### Session state memory
- Scope: transient active work
- Examples: current goal, blockers, next action, pending approvals
- Write policy: update during work; do not treat as durable memory by default

### Retrieval/index memory
- Scope: retrieval aids
- Examples: where rules live, which command audits context, which agent is used for verification
- Write policy: explicit approval if durable

### Reflective memory
- Scope: lessons from orchestration or failures
- Examples: patterns that reduced context bloat, common recovery failures
- Write policy: explicit approval

## Entry Schema
Every durable entry should capture:
- `id`
- `class`
- `owner`
- `scope`
- `source`
- `provenance`
- `sensitivity`
- `approval_state`
- `created_at`
- `review_at`
- `supersedes`
- `status`

Allowed `sensitivity` values:
- `low`
- `moderate`
- `high`
- `restricted`

Allowed `approval_state` values:
- `proposed`
- `approved`
- `rejected`
- `expired`

Allowed `status` values:
- `active`
- `superseded`
- `under_review`
- `archived`

## Session Ledger Template
Use this for compact/resume/handoff:

```yaml
goal:
non_goals:
constraints:
decisions:
blockers:
next_action:
relevant_context:
pending_approvals:
persistence_candidates:
risks:
context_pressure:
```

## Current Durable Items
- None yet. The framework is installed, but no durable memory entries have been approved.

## Memory Review Rules
- Proposed entries stay out of default working context until approved.
- Expired or archived entries should not be loaded into active context by default.
- Contradictory active items must be marked `under_review`.
- Shared and enterprise memory require a `review_at` date.
