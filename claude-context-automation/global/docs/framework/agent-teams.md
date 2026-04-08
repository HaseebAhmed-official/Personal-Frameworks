# Agent Teams Contract

Agent teams are a native Claude Code feature and an experimental framework default for tasks that benefit from direct teammate-to-teammate communication.

## When To Use
- Parallel research with distinct lenses
- Competing-hypothesis debugging
- Cross-layer work with separable ownership
- Review tasks where multiple criteria should be evaluated independently

## When Not To Use
- Sequential tasks
- Same-file edits
- Small tasks where coordination cost dominates
- Work that can be handled by one subagent returning a concise result

## Conservative Defaults
- 1 lead
- 3 active teammates by default
- 1 verifier at most
- 5 to 6 tasks per teammate when using the shared task list
- Collapse back to a single session if cost grows too quickly, task boundaries blur, or teammates repeatedly block each other

## Standard Team Patterns
### Research Team
- Roles: lead, researcher, architect, skeptic
- Use for: exploration, tradeoffs, discovery

### Planning Team
- Roles: lead, planner, feasibility reviewer, verifier
- Use for: design and rollout plans

### Build Team
- Roles: lead, implementation worker A, implementation worker B, verifier
- Use for: independent file ownership and parallel execution

### Memory Curation Team
- Roles: lead, memory curator, governance reviewer
- Use for: reviewing persistence candidates and contradictions

## Required Handoff Schema
Every teammate output should include:
- task
- assumptions
- findings
- file ownership or scope
- open risks
- recommended next action

## Quality Gates
Use hooks and lead review to enforce:
- no completion without clear findings
- no teammate cleanup from a non-lead session
- no shared-file ownership collisions
