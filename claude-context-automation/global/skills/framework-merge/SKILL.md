---
name: framework-merge
description: >
  Compares two systems, codebases, configs, or approaches and synthesizes a merged best-of-both form.
  Use this skill whenever the user has two things doing the same job and wants to consolidate, pick one,
  or combine the best parts — even without the word "merge". Strong triggers: "which is better and
  combine them", "synthesize best of both", "take the best parts of X and Y", "we have two versions —
  which should we use", "merge these frameworks", "reconcile these configs", "make one canonical X",
  "consolidate into one", "pick one and deprecate the other", "two engineers wrote competing
  implementations". Also trigger when the user describes two parallel scripts, configs, pipelines,
  patterns, or approaches that overlap and wants a single authoritative one — even if they phrase it as
  "compare" or "which is better" with no explicit mention of merging.
  Trigger on /framework-merge.
---

# Framework Merge Skill

You are about to compare two systems and produce a single, unified best-of-both form. This is a
structured process — don't shortcut the exploration phase or the user will end up with a merge
that misses hidden strengths in one of the systems.

## Step 0 — Identify the two systems

If the user gave you paths, names, or descriptions of both systems, proceed. If only one is clear,
ask: "What are the two things you want me to compare and merge?" Keep it brief — you just need the
two subjects.

## Step 1 — Parallel exploration (spawn two Haiku agents simultaneously)

Spawn **both agents in the same message** so they run in parallel. Each agent explores one system
and returns a structured report. Do not wait for one to finish before spawning the other.

**Agent A prompt template:**
```
Explore [SYSTEM A] thoroughly. Read all relevant files. Return a structured report with exactly
these sections:
1. Architecture overview (how it's organized, key files, entry points)
2. Strengths (what it does well — be specific, cite file paths)
3. Weaknesses (gaps, rough edges, things that are missing or broken)
4. Unique features (things this system has that the other likely doesn't)
5. Key design decisions (the choices that define its character)

Be thorough but concise. This report will be compared against a parallel report for [SYSTEM B].
```

**Agent B prompt:** Same structure, swap system names.

Wait for both to complete before proceeding.

## Step 2 — Build the comparison matrix

Using the two reports, fill in this matrix. Be honest — if one system clearly wins a dimension,
say so. If it's a tie, say tie. If one has a feature the other lacks entirely, mark N/A for the
other.

```
DIMENSION              | SYSTEM A | SYSTEM B | NOTES
-----------------------|----------|----------|--------------------------------
Correctness            |          |          | Does it work reliably?
Maintainability        |          |          | Easy to read, change, extend?
Automation depth       |          |          | How much does it do for you?
Governance / structure |          |          | Rules, precedence, guardrails?
Developer experience   |          |          | Friction to use day-to-day?
Performance            |          |          | Speed, resource use, overhead?
Coverage               |          |          | What use cases does it handle?
Unique value           |          |          | What would be lost if dropped?
```

Add or remove dimensions as relevant to the actual systems being compared.

## Step 3 — Synthesize the merged form

Write a proposed merged design with:

1. **What comes from System A** (and why — tie it to the matrix)
2. **What comes from System B** (and why)
3. **What gets discarded** from each (and why — be direct, not everything deserves to survive)
4. **New pieces needed** that neither system has but the merge requires
5. **The merged structure** — a concrete outline (file tree, component list, or config sketch)

Present this to the user. Do not start implementing until they approve.

## Step 4 — Phased implementation (after approval)

Break the work into phases. Use this default structure, adapting to what the specific merge requires:

- **Phase 1 — Core / foundation**: The parts everything else depends on (shared utilities, base
  configs, data models). Get these right before adding features.
- **Phase 2 — Governance / structure**: Rules, precedence, guardrails, schemas. The skeleton that
  keeps the system coherent at scale.
- **Phase 3 — Features / integrations**: The capabilities users interact with — commands, hooks,
  agents, APIs, UI.
- **Phase 4 — Polish / docs**: Validation scripts, simulation docs, inline comments, README updates.

**After each phase**, spawn a verification-auditor subagent with this prompt:
```
Review the implementation just completed for Phase [N] of [MERGE PROJECT].
Compare what was planned against what was actually built.

Return:
## Findings
[Specific differences between plan and implementation]

## Risks
[Anything that could cause problems in later phases]

## Recommended Next Action
[What should happen before Phase N+1 begins]
```

Do not proceed to the next phase if the auditor flags unresolved risks.

## Step 5 — Final validation

After Phase 4, run whatever validation exists:
- If `validate_framework.py` exists: `python3 validate_framework.py`
- If tests exist: run them
- If neither exists, do a manual checklist pass against the merged design from Step 3

Report the validation result to the user.

## Step 6 — Suggest artifacts for capture

End with: "Would you like me to run `/session-review` to capture any reusable patterns from this
merge as skills, templates, or hooks?" This merge process itself is reusable — if the user says yes,
run the skill.

---

## Notes on judgment calls

- **Don't merge for the sake of merging.** If one system is clearly better across every dimension,
  say so and recommend adopting it wholesale rather than producing a bloated hybrid.
- **Don't average the two systems.** The goal is the best of both, not the middle of both. Be
  willing to discard things even if the user is attached to them.
- **Keep the main thread lean.** Heavy file reading goes to Haiku agents. Planning and decision
  logic stays in the main thread with the user. Verification goes to the auditor.
- **Phase gate strictly.** The temptation is to push through all phases at once. Resist it — the
  auditor exists because merges drift from plans, and catching drift early is far cheaper than
  fixing it after four phases of compounding assumptions.
