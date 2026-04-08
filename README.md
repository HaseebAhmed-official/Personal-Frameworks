# Personal-Frameworks

A collection of reusable automation frameworks for Claude Code. These frameworks provide structured patterns for session continuity, context management, governance, and team coordination.

## Available Frameworks

| Framework | Description |
|-----------|-------------|
| [claude-context-automation](./claude-context-automation) | Merged context automation framework with session continuity, governance gates, memory taxonomy, and 10 specialized hooks. Combines practical automation (session state, JSONL tracking, skills) with governance (11-level precedence, approval workflows). 85 files, 7,409 lines, 76 validation checks. |

## How Frameworks Are Structured

Each framework consists of two installation layers:

- **`global/`** — Installs to `~/.claude/` (user-level configuration)
  - Global behaviors, hooks, agents, skills, output styles
  - Shared across all projects
  - Single source of truth for user preferences

- **`project-level/`** — Installs to project root + `.claude/` (project-level configuration)
  - Project-specific rules (CLAUDE.md, RULES.md, MEMORY.md)
  - Project agents, commands, output styles
  - Overrides global settings for this project

## Quick Start

1. Choose a framework from the table above
2. Read its README for detailed documentation
3. Follow the installation instructions in that framework's README
4. Run validation if provided to ensure all components are installed correctly

## About This Repository

This repo is maintained by HaseebAhmed-official and contains frameworks developed and validated for Claude Code automation. Each framework is self-contained and can be installed independently.
