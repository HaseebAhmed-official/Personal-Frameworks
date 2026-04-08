---
name: fw
description: >
  Quick launcher for the Context & Workflow Management Framework. Presents a menu of all
  framework maintenance actions and runs the user's choice. Use this skill whenever the user
  types /fw, says "framework menu", "run framework", "maintenance menu", or wants quick
  access to framework tools without remembering individual skill names.
---

# Framework Quick Launcher

Present this menu and wait for the user to pick an option:

```
  Framework Tools
  ───────────────────────────
  1) Memory Cleanup    — scan for stale/duplicate/orphaned memories
  2) Framework Status  — health check all components
  3) Session Review    — analyze session and suggest reusable artifacts
  4) Full Audit        — run all three in sequence
  ───────────────────────────
  Pick a number (1-4):
```

Then execute based on their choice:

- **1** → Invoke the `memory-cleanup` skill
- **2** → Invoke the `framework-status` skill
- **3** → Invoke the `session-review` skill
- **4** → Run all three in order: framework-status first (quick health check), then memory-cleanup (audit memories), then session-review (analyze work done). Separate each with a brief divider line so the output is easy to scan.

If the user passes an argument directly (e.g., `/fw 2` or `/fw status`), skip the menu and go straight to that action. Accept both numbers and keywords: "cleanup"/"memory" → 1, "status"/"health" → 2, "review"/"session" → 3, "all"/"audit"/"full" → 4.
