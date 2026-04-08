# Reusable Components Contract

Every reusable framework component must declare:
- owner
- scope
- version
- change approval path
- inheritance rule
- override rule
- rollout status

## Component Categories
### Rule packs
- Files: `CLAUDE.md`, `RULES.md`, imported rule packs
- Scope: project or shared

### Memory ledgers
- Files: `MEMORY.md`, approved structured memory files
- Scope: project, user, or enterprise

### Agents
- Files: `.claude/agents/*.md`
- Scope: project or user

### Agent team templates
- Files: `.claude/commands/teams/*.md`, `docs/framework/agent-teams.md`
- Scope: project or shared

### Hook bundles
- Files: `.claude/scripts/hooks/*.py`, `.claude/settings.json`
- Scope: project or enterprise-managed

### Custom commands
- Files: `.claude/commands/**/*.md`
- Scope: project or user

### Output styles
- Files: `.claude/output-styles/*.md`
- Scope: project or user

### Schemas and audit artifacts
- Files: `.claude/schemas/*`, `.claude/logs/*`
- Scope: project

## Ownership Defaults
- Project maintainer owns project-level components.
- User owns personal local overrides.
- Enterprise admins own managed settings and global policy.

## Versioning Rule
- Start every reusable component set at `v1`.
- Bump the version when behavior, scope, or approval semantics change.
