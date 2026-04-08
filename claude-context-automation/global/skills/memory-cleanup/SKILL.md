---
name: memory-cleanup
description: >
  Weekly memory hygiene — scans all project memory directories for stale, duplicate, or orphaned
  entries and suggests cleanup actions. Use this skill whenever the user mentions memory cleanup,
  memory maintenance, stale memories, memory hygiene, or wants to audit their memory files.
  Also triggers when memory count is high, MEMORY.md seems out of sync, or the user says
  "clean up memories", "check my memories", "memory audit", or "too many memories".
  Designed to run via /schedule or /loop for automated weekly maintenance.
---

# Memory Cleanup

You are performing a memory hygiene audit. Your job is to scan memory directories, find problems,
and present a clear report with suggested actions. You never delete or modify anything without
explicit user confirmation.

## Why This Matters

Memory files accumulate over time. Without periodic cleanup:
- Stale memories give outdated advice (e.g., a project decision that was reversed)
- Duplicate entries waste context window tokens when loaded
- Orphaned index entries (in MEMORY.md) point to files that no longer exist
- Missing index entries mean useful memories never get loaded
- Too many memories (50+) make the index hard to scan and slow to load

## How to Run the Audit

Follow these steps in order. Use Glob and Grep to scan — don't read every file in full unless needed.

### Step 1: Discover All Memory Directories

```bash
find ~/.claude/projects/*/memory/ -name "*.md" -not -name "MEMORY.md" 2>/dev/null
```

Group results by project directory. Report how many projects have memories and total file count.

### Step 2: For Each Project, Build an Inventory

For each memory directory found:

1. **List all .md files** (excluding MEMORY.md) with their modification dates
2. **Read the frontmatter** of each file to extract: name, description, type
3. **Read MEMORY.md** to get the index entries

Present as a table:

| File | Type | Last Modified | In Index? | Age (days) |
|------|------|---------------|-----------|------------|

### Step 3: Flag Issues

Check for these problems and categorize by severity:

**Critical (index broken):**
- Files that exist but aren't listed in MEMORY.md (missing from index — they'll never load)
- MEMORY.md entries that point to files that don't exist (orphaned references)

**Warning (likely stale):**
- Memory files older than 30 days — they may reflect outdated decisions or context
- Projects with more than 50 memory files (cap exceeded)

**Info (possible duplicates):**
- Files with very similar names (e.g., `feedback_testing.md` and `feedback_test_approach.md`)
- Files with similar descriptions in their frontmatter (use judgment — similar topics aren't always duplicates)

### Step 4: Present the Report

Structure your report like this:

```
## Memory Audit Report — [date]

### Summary
- X projects scanned
- Y total memory files
- Z issues found (N critical, N warnings, N info)

### Critical Issues
[List each with file path and what's wrong]

### Warnings
[List each with file path, age, and why it might be stale]

### Possible Duplicates
[List pairs with their descriptions so user can judge]

### Suggested Actions
For each issue, suggest a specific action:
- "Add [file] to MEMORY.md index" (for missing entries)
- "Remove line N from MEMORY.md — file no longer exists" (for orphans)
- "Review [file] — last updated 45 days ago, may be outdated" (for stale)
- "Consider merging [file1] and [file2] — similar topics" (for duplicates)
```

### Step 5: Act on User Decisions

After presenting the report, wait for the user to tell you which actions to take.
For each action the user approves:
- **Adding to index:** Edit MEMORY.md to add the entry
- **Removing orphans:** Edit MEMORY.md to remove the broken line
- **Deleting stale files:** Delete the file AND remove its MEMORY.md entry
- **Merging duplicates:** Combine content into one file, delete the other, update MEMORY.md

Never batch-delete. Confirm each destructive action individually.

### Step 6: Update Audit Timestamp

After completing the audit (whether or not any actions were taken), update the marker file
so the session-start reminder knows the audit was done:

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ" > ~/.claude/session-logs/.last-memory-audit
```

## Automated Reminders

A SessionStart hook automatically checks if the last memory audit was more than 7 days ago.
If overdue, it reminds the user to run `/memory-cleanup` or `/fw 1`. No manual scheduling needed.

For long sessions, you can also use:
- `/loop 7d /memory-cleanup` — run every 7 days during the session

When running on a schedule (unattended), generate the report and save it to
`~/.claude/session-logs/memory-audit-[date].md` for the user to review later.
Only suggest actions — never auto-execute when running unattended.
