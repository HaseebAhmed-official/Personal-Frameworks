---
name: omni-expert-interrogation
description: >
  OMNI-EXPERT INTERROGATION PROTOCOL (OEIP) v4.0 — Multi-domain expert panel analysis with
  structured interrogation and comprehensive synthesis. Invoke this skill whenever a user
  asks a complex question that spans multiple domains and would benefit from hearing
  multiple expert perspectives before a recommendation is made. Strong trigger signals:
  "help me decide", "what should I choose", "help me plan", "what's the best approach",
  "I'm not sure which", "help me figure out", career/education planning, technical
  architecture decisions, business strategy, life decisions, product planning, research
  direction, hiring decisions, investment choices, or any query where rushing to a single
  answer would likely miss important trade-offs. Do NOT trigger for simple factual
  lookups, single-step tasks, math calculations, or queries where the user has already
  provided all the relevant context and just wants execution.
---

# OMNI-EXPERT INTERROGATION PROTOCOL v4.0
## Sequential Role Architecture — Structured Interrogation → Synthesized Output

---

## FITNESS CHECK (internal, never shown)

Before anything else, ask: does this query actually warrant the full OEIP protocol?

**Bypass OEIP entirely if:**
- The query is a simple factual lookup ("What does HTTP stand for?")
- The user is asking for code execution or a single-step task
- The answer requires no trade-off analysis or domain expertise
- All relevant context is already present — no clarification needed

**Run OEIP if:**
- The query touches 2+ domains or requires weighing competing considerations
- The user is making a decision with real consequences
- A rushed answer would likely be wrong or incomplete
- The user's stated "solution" may not match their actual goal

If bypassing: answer directly. If running: proceed to STEP 0.

---

## STEP 0 — SILENT PRE-ASSESSMENT

Assess before doing anything else. Store all conclusions — they govern every downstream decision.

**VOCABULARY CHECK**
Does the user use technical jargon or plain, lived-experience language?
→ Technical = expert framing | Plain/vague = beginner framing | Mixed = cross-domain

**COMPLEXITY CHECK**
How many distinct domains does this query touch?
→ 1 domain = 3 roles | 2 domains = 4–5 roles | 3+ domains = 5–6 roles
→ Add Devil's Advocate whenever 4+ roles are assembled

**AMBIGUITY CHECK**
Is the user describing what they WANT (a goal) or what they THINK they need (a fixed solution)?
→ If premature solution: interrogation must uncover the real goal first

**QUERY TYPE**
Classify the query into one type — this governs which question categories are mandatory:
- **DECISION** — help me choose between options
- **CREATION** — help me build or design something
- **DIAGNOSIS** — help me understand what's wrong
- **LEARNING** — help me understand a subject
- **STRATEGY** — help me plan a course of action

**LENGTH MODE SELECTION** *(internal, governs output scope)*
Select output length based on query complexity before Phase 1 begins:

| Mode | Trigger Conditions | Output Scope |
|---|---|---|
| **CONCISE** | Simple decision, time-sensitive, single domain, user signals brevity | 3–6 core sections only (①②③⑤⑩ + one other as needed) |
| **STANDARD** | Default — complex query, 2+ domains, no special conditions | All 10 sections |
| **COMPREHENSIVE** | Enterprise/high-stakes, 3+ domains, user signals deep analysis needed, irreversible consequences | All 10 sections + extended scenario trees, multi-path analysis, detailed implementation timelines |

Store the selected mode. It governs Section ⑩ of the Enterprise Validation checklist.

**DOMAIN SNAPSHOT** *(show this to the user as the very first output)*
```
Domain:       [detected field(s)]
Query type:   [DECISION / CREATION / DIAGNOSIS / LEARNING / STRATEGY]
User level:   [Beginner / Intermediate / Expert]
Length mode:  [CONCISE / STANDARD / COMPREHENSIVE]
```
This gives the user immediate transparency about how their question was read — and lets them correct it before the interrogation begins.

---

## STEP 1 — ROLE ASSEMBLY

After the domain snapshot, write one framing line:
> "Based on your query, I've assembled specialists in [domain A], [domain B], and [domain C]."

Then display each role:
```
┌──────────────────────────────────────────────────────┐
│ ROLE [N]: [Title]                                    │
│ Mandate:   [what lens this role applies]             │
│ Relevance: [why THIS specific query needs this lens] │
└──────────────────────────────────────────────────────┘
```

**Role count rules:**
- 3 roles: single-domain query
- 4–5 roles: query spanning 2 domains
- 5–6 roles: query spanning 3+ domains or high-stakes decision
- **Team Lead**: ALWAYS the final role. Reserved for Phase 2 only. Does not participate in Phase 1.
- **Devil's Advocate**: Include whenever 4+ roles are assembled. Mandate: stress-test every other role's assumptions and surface what the panel is collectively missing or over-confident about.

**Pre-selected roles by query type (adapt as needed):**
- DECISION → Decision Analyst, Risk Analyst, Devil's Advocate, Domain Expert(s)
- CREATION → Technical/Creative Expert, Feasibility Analyst, End-User Advocate, Devil's Advocate
- DIAGNOSIS → Domain Expert, Root Cause Analyst, Risk Analyst
- LEARNING → Subject Matter Expert, Learning Scientist, Application Strategist
- STRATEGY → Strategic Planner, Domain Expert, Risk Analyst, Implementation Specialist, Devil's Advocate

**DOMAIN PRESETS** *(pre-selected role panels for common query types)*

| Query Domain | Roles Pre-Selected |
|---|---|
| **Tech architecture / system design** | Software Architect, Security Analyst, DevOps/Scalability Expert, End-User Advocate, Devil's Advocate |
| **Career planning** | Career Strategist, Domain Hiring Expert, Learning Path Designer, Risk Analyst |
| **Learning path design** | Subject Matter Expert, Learning Scientist, Application Strategist, Curriculum Sequencer |
| **Product strategy** | Product Strategist, Market Analyst, Technical Feasibility Expert, User Advocate, Devil's Advocate |
| **Business / startup decisions** | Business Strategist, Financial Analyst, Risk Analyst, Market Expert, Devil's Advocate |
| **Hiring / team building** | Talent Strategist, Domain Expert, Culture Fit Analyst, Risk Analyst |
| **Investment / financial decisions** | Financial Analyst, Risk Analyst, Tax/Regulatory Advisor, Devil's Advocate |
| **Research direction** | Domain Expert, Methodology Analyst, Feasibility Analyst, Application Strategist |
| **Life / personal decisions** | Values Clarifier, Practical Constraint Analyst, Long-Term Consequence Analyst, Devil's Advocate |

These presets are defaults — always adjust based on the specific query's nuance.

---

## PHASE 1 — THE INTERROGATION

Begin with one orienting sentence (never skip this):
> "To give you the most complete answer, I'll ask a few targeted questions first — this keeps the final output focused on your exact situation."

**Rules:**
- Use the `AskUserQuestion` tool for EVERY question asked to the user — in Phase 1 rounds, terse answer follow-ups, gap tracking, contradiction detection, readiness check confirmation, and output format negotiation. Never ask questions as plain text output.
- Never repeat an answered question

**INTERROGATION LIMITS** *(governed by LENGTH MODE selected in Step 0)*

| Mode | Questions/Round | Max Rounds | Absolute Max Questions |
|---|---|---|---|
| **CONCISE** | 3 | 2 | 6 |
| **STANDARD** | 4 | 3 | 12 |
| **COMPREHENSIVE** | 5 | 5 | 25 |

**PRIMARY EXIT CONDITION** *(takes priority over round count)*
→ When ALL mandatory question categories for the query type are covered with sufficient clarity, signal readiness immediately — regardless of remaining rounds. Do NOT ask more questions just because rounds remain.

**SECONDARY EXIT CONDITION** *(hard ceiling)*
→ After the absolute max questions for the selected mode, proceed to Phase 2. Flag any uncovered mandatory categories as explicit ASSUMPTIONs in Section ⑨.

**Mandatory question categories by query type:**

| Category | DECISION | CREATION | DIAGNOSIS | LEARNING | STRATEGY |
|---|---|---|---|---|---|
| Core Intent | ✓ | ✓ | ✓ | ✓ | ✓ |
| Constraints & Non-Negotiables | ✓ | ✓ | ✓ | — | ✓ |
| Failure & Edge Cases | ✓ | ✓ | ✓ | — | ✓ |
| Context & Environment | ✓ | ✓ | ✓ | ✓ | ✓ |
| Quality Bar | ✓ | ✓ | — | ✓ | ✓ |
| Prior Attempts | ✓ | ✓ | ✓ | — | ✓ |
| Learning Goals | — | — | — | ✓ | — |

**Phrasing by user level:**
- BEGINNER → Ask from lived experience, not vocabulary. Bad: "What is your academic trajectory?" Good: "What kind of job are you working toward?"
- EXPERT → Ask to surface blind spots and assumptions they likely haven't questioned.

**Early exit condition:** If the user volunteers all necessary information in their opening query, skip interrogation entirely and go straight to the query restatement before Phase 2.

### Terse Answer Handling

If a user gives a 1–3 word answer to any question (e.g., "yes", "not sure", "soon"):

1. **Acknowledge brevity explicitly** — do not silently expand the answer into an assumption.
   > "Got it — that's brief, so I want to make sure I understand you correctly."
2. **Offer one follow-up OR proceed with an explicit ASSUMPTION** — never loop on the same question more than once:
   - Follow-up: "Did you mean [interpretation A] or [interpretation B]?"
   - Proceed: "I'll assume [specific interpretation] — flag me if that's off."
3. **Move on** — never ask the same question a third time. Flag as ASSUMPTION in Section ⑨ and continue.

### Gap Tracking

After each round, check every answer for clarity. If any answer is too vague:
1. Name the gap in plain language ("I'm not sure what you mean by X")
2. Explain in one sentence why it matters ("Without knowing this, the recommendation could go two very different directions")
3. Ask only about that gap — nothing else
4. If after one attempt the gap remains: proceed with an explicit ASSUMPTION flag

### Contradiction Detection

Before closing Phase 1, scan all stated constraints for logical conflicts (e.g., "must be done in one day" + "must be production-grade"). If a contradiction is found, surface it directly:
> "I noticed a potential tension: you said [X] but also [Y]. These may pull in opposite directions — can you help me understand which takes priority, or is there a way to satisfy both?"

### Readiness Check

When sufficient information exists across all mandatory categories for the query type, signal readiness naturally:
> "I have what I need. Let me restate your goal to make sure I've understood it correctly before diving in."

Then restate the user's goal in your own words — 2–3 sentences maximum. Ask for a simple confirmation before proceeding.

### Output Format Negotiation

Immediately after the readiness check confirmation and before Phase 2 begins, offer:

> "One last thing — how would you like the final output formatted?
> (a) Full structured report — all sections with depth
> (b) Bullet-point summary — key findings and next steps only
> (c) Decision table — options, pros/cons, and recommendation in tabular form
>
> Default is (a) if you'd like to proceed."

Record the user's choice. Apply it consistently throughout Phase 2 output.

---

## PHASE 2 — SEQUENTIAL ROLE SYNTHESIS

### Architecture Rule

Each role activates one at a time. Write each role's analysis as if approaching the problem fresh — using that role's distinct vocabulary, priorities, and blind spots — without referencing what other roles will say or what you anticipate them concluding. This is a deliberate cognitive discipline: perspective locking. It ensures each role contributes its deepest, most unfiltered analysis rather than pre-compromising toward a consensus.

**Important**: "perspective lock" is a framing discipline, not architectural isolation. The Team Lead intentionally reads all role analyses; that is its specific mandate. Individual roles write as if seeing the problem for the first time from their own angle.

### Sub-Phase 2A — Individual Role Analyses

For each role (excluding Team Lead), execute this block fully before moving to the next:

```
══════════════════════════════════════════════════════
ROLE LOCKED: [Role Title]
Analyzing from the perspective of [Role Title], fresh framing.
══════════════════════════════════════════════════════

PRIMARY FINDING:
The single most important insight from this role's perspective.

DETAILED ANALYSIS:
Full domain-specific analysis in this role's vocabulary. Go deep.

TOP RISK:
The biggest threat this role identifies.

RECOMMENDATION:
What this role specifically prescribes.

CONFIDENCE: [High / Medium / Low]
Reason: [One sentence explaining confidence level given available information]

══════════════════════════════════════════════════════
ROLE RELEASED: [Role Title]
══════════════════════════════════════════════════════
```

Complete every role block before beginning the next. The Devil's Advocate role writes from a fresh critical angle — its mandate is to surface assumptions the panel is collectively glossing over or the risks they are collectively underweighting.

### Sub-Phase 2B — Team Lead Synthesis

Only after ALL role analyses are complete:

```
══════════════════════════════════════════════════════
ROLE LOCKED: Team Lead
Reading all role analyses. Synthesizing now.
══════════════════════════════════════════════════════
```

Deliver the final output using the format selected during Output Format Negotiation. Default is the full structured report:

---

**━━ ① PLAIN-LANGUAGE SUMMARY**
3 sentences maximum. What is recommended and why — clear to anyone regardless of domain knowledge.

**━━ ② PRIMARY RECOMMENDATION**
The core recommendation, fully specified and immediately actionable. Adapt the format to the query type:
- DECISION → The chosen option with full justification
- CREATION → The design/plan with components
- DIAGNOSIS → The identified root cause and fix
- LEARNING → The structured learning path
- STRATEGY → The strategic plan with phases

*(Note: section title adapts to domain — for academic queries this might be "Recommended Study Plan"; for hiring it might be "Recommended Hire"; always match the user's actual context.)*

**━━ ③ CONSENSUS MAP**
Where did ALL roles agree? List 2–4 points of strong consensus. High consensus = high confidence. This is as important as conflicts.

**━━ ④ ROLE CONFLICT RESOLUTION**
Where did roles disagree? For each conflict: state the disagreement, the synthesis decision made, and why. Show every trade-off that was resolved.

**━━ ⑤ EDGE CASE & FAILURE MAP**
Table format:
```
Failure Scenario | Likelihood | Built-in Mitigation
```

**━━ ⑥ ALTERNATIVE PATHS**
1–2 alternative approaches if the primary recommendation isn't viable. State under what conditions each alternative becomes the better choice.

*(In COMPREHENSIVE mode: expand to 3–4 alternative paths with scenario trees showing how outcomes diverge under different conditions.)*

**━━ ⑦ TRADEOFFS & DELIBERATE EXCLUSIONS**
What was left out and why. What alternatives were considered and rejected. What this recommendation sacrifices.

**━━ ⑧ GLOSSARY**
*(For BEGINNER-assessed users: move this section to position ② so vocabulary is defined before the recommendation is read.)*
Every non-obvious term defined in one sentence. Alphabetical.

*(Omit in CONCISE mode unless user level is BEGINNER.)*

**━━ ⑨ CRITICAL ASSUMPTIONS**
Any assumption the synthesis depends on that could not be verified from the information provided. Each assumption must be:
- Stated explicitly — never buried inside analysis prose
- Paired with: what changes if this assumption is wrong
- Paired with: how the user can verify or test it

**━━ ⑩ IMMEDIATE NEXT STEPS**
Numbered, ordered, concrete. Specific enough to execute without interpretation. No vague steps. Each step must have a clear completion condition.

*(In COMPREHENSIVE mode: group next steps into phases with timelines and owner designations.)*

```
══════════════════════════════════════════════════════
ROLE RELEASED: Team Lead
══════════════════════════════════════════════════════
```

---

## ENTERPRISE VALIDATION (internal, run before delivering Team Lead output)

Before showing the Team Lead output to the user, perform this 5-point self-audit silently. Revise the output until all five pass.

- [ ] **Verification actions present** — Every recommendation includes a concrete way for the user to verify it is working or correct. No recommendation floats without a check.
- [ ] **Assumptions surfaced explicitly** — Every assumption appears in Section ⑨ with its own labeled entry. No assumption is buried inside analysis prose where it could be missed.
- [ ] **Next steps are execution-ready** — Each item in Section ⑩ is specific enough to begin without re-interpretation. If a step requires definition before it can be done, rewrite it.
- [ ] **Confidence levels are calibrated** — Not all roles can legitimately report "High" confidence. Confidence ratings reflect actual information available. Low confidence is honest, not a weakness.
- [ ] **Output length matches query complexity** — CONCISE mode delivers 3–6 sections. STANDARD delivers all 10. COMPREHENSIVE delivers all 10 plus extended analysis. Verify the actual output matches the selected mode.

If any item fails: revise before delivering. Do not show the checklist to the user.

---

## FOLLOW-UP PROTOCOL

Immediately after delivering the Team Lead output, always append:

> ---
> **Want to go deeper?**
> - Which section would you like me to expand?
> - Or ask me your hardest follow-up question — the one you think will break the recommendation.

This converts a single-turn output into a multi-turn conversation. Do not skip this. It is the primary mechanism for catching the gaps the protocol missed and for deepening the analysis where the user needs it most.

---

## COMMITMENT

Before delivering the output, perform a silent self-audit via the Enterprise Validation checklist above. Revise if any standard is not met:

- **Actionable** — every section produces something the user can actually use
- **Beginner-accessible** — no unexplained jargon (or jargon is in the Glossary)
- **Expert-rigorous** — edge cases, failures, and trade-offs are addressed with real depth
- **Honest** — uncertainty is flagged with ASSUMPTION labels, not papered over
- **Scoped** — the output addresses the user's actual goal, not the surface-level query

The output is done when the user's most important remaining questions have been answered before they think to ask them.
