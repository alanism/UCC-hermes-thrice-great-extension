---
name: thoth_ucc_workflows
description: "Core analysis workflows for UnCommon Core ontology, pedagogy alignment, mastery architecture, product specification, assessment telemetry, and app review."
version: 1.7.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ucc, workflow, analysis, thoth]
    related_skills: [ucc_ontology_mapper, pedagogy_alignment_audit, mastery_ledger_contract, assessment_app_reviewer, feynman_explanation_gate, school_model_canvas_interpreter, parent_progress_brief, ghostwriting_integrity_gate, builder_prompt_spec]
---

# Thoth UCC Workflows

## Overview

Core analysis workflows for UnCommon Core ontology, pedagogy alignment, mastery architecture, product specification, assessment telemetry, and app review.

This skill imports the 9 specialist skills below. Use the specialist skill when you need a tight, focused output. Use this workflow skill when you need the full structured analysis from scratch.

---

## Parent Coaching Protocol

Use when [Parent Name] (the parent) asks for advice, judgment, or a plan about [Learner Name] in Discord or this chat. This replaces the Default Analysis Workflow for this specific trigger.

### When to Use

| [Parent Name] says... | Mode |
|---|---|
| "How should I coach [Learner Name] on X?" | **Coaching protocol** — questions first |
| "I'm stuck on Y with [Learner Name]" | **Coaching protocol** — questions first |
| "[Learner Name] is struggling with Z, what should I do?" | **Coaching protocol** — questions first |
| "Build me a spec / interpret this data / fix this file" | **Default workflow** — direct analysis |
| "Just tell me" or "What advice do you have" | **Direct answer** — switch immediately |

### The Question Loop (Coaching Habit)

Ask **one question at a time**. Wait for the answer. Do not stack.

```
1. Open:    "What's on your mind about [topic] right now?"
2. Check:   "Is there anything else on your mind about this?"
3. Focus:   "So what's the real challenge here for you?"
4. Deepen:  "And what else is the real challenge here for you?"
5. Land:    "So... what's the real challenge here for you?"
```

### Discipline Rules

- **One question at a time.** Never stack. Never add a second question while the first is unanswered.
- **Silence after each question.** Let [Parent Name] speak. Do not fill the gap with analysis, reframing, or suggestions.
- **No prescribing while the loop is open.** The goal is to surface *his* real challenge, not for Thoth to guess it.
- **Release valve.** If [Parent Name] says "Just tell me" or "What advice do you have" or "that's it", **break the loop** and give a direct, specific answer. He chooses when coaching is done.
- **Outcome.** When [Parent Name] names the real challenge (usually on the 3rd or 5th question), he owns the next step. Thoth's job shifts from diagnosing the child to helping the parent clarify what *he* needs to decide.

### Post-Coaching Direct Answer Shape

Once the loop releases, use:

1. Restate the real challenge [Parent Name] named
2. Offer 2-3 concrete options (not one prescription)
3. Name the tradeoff [Parent Name] needs to decide
4. Offer to materialize (1-pager, schedule, ledger entry) if useful

This hybrid — coach to clarity, then answer — is the pattern. Not pure coaching, not pure answering. Coaching first, answer when asked.

---

## Default UCC Analysis Workflow

Use for any UCC feature, app, lesson, assessment, or product concept (NOT for parent coaching requests — see Parent Coaching Protocol above).

1. **Identify the learning object**
   - App, Lesson, Assessment, Ledger entry, Parent report, Student activity, Product workflow

2. **Identify the target function**
   - Practice, Mastery, Transfer, Retention, Assessment, Parent coaching, Curriculum planning, Student reflection

3. **Identify the cognitive mechanism**
   - Prediction-error, Retrieval, Spacing, Interleaving, Structured variation, CPA progression, Feynman explanation, Socratic questioning, Pressure testing, Metacognitive reflection

4. **Identify the evidence**
   - What does the student do? What does the system measure? What proves progress? What remains unknown?

5. **Identify the ledger location**
   - Skill graph node, Error pattern, Mastery signal, Transfer signal, Retention schedule, Parent action item, Student reflection artifact

6. **Output the result**
   - Ontology classification, Pedagogy alignment, Telemetry requirements, Risks, Next 3 actions

---

## UCC Ontology Mapping Workflow

Use when converting vague product ideas into the UCC knowledge graph.

1. **Define the entity type**
   - Student, Skill, Standard, Problem schema, Misconception, Hint, Evidence item, Session, Assessment, Receipt, Parent intervention, Artifact

2. **Define relationships**
   - requires, demonstrates, predicts, remediates, transfers_to, retains, weakens_under_pressure, supported_by, generated_from, visible_to_parent

3. **Define required fields**
   - Stable ID, Human-readable label, Domain, Grade band, Evidence type, Source, Timestamp, Confidence or status, Parent-facing explanation

4. **Define forbidden ambiguity**
   - No orphaned skills, No unlabeled evidence, No mastery without proof, No LLM-only grading for deterministic skills, No parent dashboard claims without trace

5. **Output**
   - Entity table, Relationship map, Required fields, Open questions, Acceptance criteria

---

## Pedagogy Alignment Audit

Use when reviewing a UCC feature or app.

1. State the feature's intended learning purpose
2. Map the feature to UCC principles
3. Identify which learning function it supports
4. Check whether feedback is immediate and useful
5. Check whether difficulty is calibrated
6. Check whether errors become diagnosis, not punishment
7. Check whether the parent receives an actionable signal
8. Check whether the student must think, explain, or transfer
9. Flag drift
10. Recommend fixes

**Output**: Aligned elements, Misaligned elements, Missing evidence, False mastery risks, Ghostwriting risks, Required revisions

---

## Mastery OS Design Workflow

Use when designing or revising mastery architecture.

1. **Separate the five functions**
   - Practice: is the student acquiring the skill?
   - Mastery: can the student execute reliably?
   - Transfer: can the student generalize?
   - Retention: will it survive without rehearsal?
   - Assessment: what is the current ceiling?

2. **Define gates**
   - Practice completion, Mastery threshold, Transfer task, Retention interval, Pressure check

3. **Define error taxonomy**
   - Conceptual error, Procedural error, Representation error, Attention error, Language error, Transfer error, Pressure error

4. **Define telemetry**
   - Accuracy, Latency, Hint usage, Attempt count, Error type, Difficulty band, Pressure mode, Explanation quality, Retention interval

5. **Output**
   - Mastery ledger contract, Advancement rule, Retention rule, Parent-facing summary, QA checklist

---

## Assessment Test Review Workflow

Use for STAR-style UCC assessment apps.

1. **Identify the domain**
   - Algebra readiness, Fractions, Measurement and data, Base-10 and place value, Geometry and spatial reasoning, Reading or writing

2. **Identify the adaptive ladder**
   - Difficulty levels, Hidden grade bands, Advancement rules, Recalibration rules

3. **Identify cognitive pillars**
   - Crystallized, Fluidity, Augmented, Pressure

4. **Validate telemetry**
   - Schema name, Hidden grade level, Response latency, Correctness, Hint usage, Frame selection, Timer condition, Export completeness

5. **Check parent usefulness**
   - Can a parent see strength? Can a parent see weakness? Can a parent know what to do next? Can the result be reconstructed later?

6. **Output**
   - Assessment purpose, Evidence captured, Missing evidence, Drift risks, Required fixes

---

## Design Sprint / Implementation Deliverable Review

Use when a design sprint, prototype, or implementation deliverable (schemas, contracts, tests, code, fixtures) needs to be reconciled against the UCC Master Reference for alignment, gaps, risks, and integration requirements. The deliverable may be on disk, in a repo, or passed as context — the methodology is the same.

1. **Survey the directory structure**
   - README, design specs, process docs, contracts, schemas, source code, test harness, fixtures, scripts, configs
   - Categorize each artifact: infrastructure, design, contract, test, fixture, code, config

2. **Read the canonical reference document**
   - UCC-Master-Reference.md (or equivalent) is the specification layer the deliverable claims to implement
   - Pay special attention to Trust Boundary (§I.6), evidence language (§III.9), and the receipt integrity model (§I.4) — these are the most frequently violated constraints

3. **Map artifacts to reference sections**
   - Build an alignment table: Reference § → Implementation artifact → Alignment verdict
   - Verdicts: ✅ (exact match), ⚠️ (partial or mismatched framing), ❌ (conflict), ➕ (additive — not specified but doesn't conflict)

4. **Identify gaps and drift**
   - What does the Master Reference require that the deliverable doesn't address? (e.g. pressure delta computation, paired-session enforcement, reading domain coverage)
   - What does the deliverable implement that the Master Reference doesn't specify? Is it additive (compatible) or conflicting?
   - What does the deliverable explicitly scope out? Is that scope-out honest or a gap?

5. **Assess integration risk**
   - Does the deliverable break the Hermes/Thoth/Discord workflow? (channel discipline, file exchange paths, claim labels)
   - Does it violate the Trust Boundary (§I.6)?
   - Does it assume infrastructure that doesn't exist yet?
   - Does it use terminology or schemas that could conflict with other UCC apps?

6. **Produce structured verdict using Thoth's default output shape**
   - **Bottom line** — one-sentence verdict
   - **System diagnosis** — what the deliverable is, what it implements well, what it's missing
   - **Ontology mapping table** — Reference § → Artifact with alignment labels
   - **Risks** — ordered by severity, each with a suggested fix
   - **Next 3 actions** — prioritized integration steps

**Reference:** `references/ucc-sprint-fable-analysis.md` contains a worked example applied to the ucc-sprint-fable deliverable (55 fixtures, 250 assertions, 5-state integrity model, probabilistic fallback).

**Pitfalls:**
- Do not treat a sprint deliverable as independent of the Master Reference — if it conflicts, the Master Reference governs (§I.6 override rule)
- Do not assume a passing test suite means full alignment — test coverage may miss Trust Boundary, evidence language, or paired-session rules
- Do not treat missing features as conflicts — a sprint that scopes out reading domain isn't wrong, but the gap must be documented for the integration plan
- **Degraded/void check:** If the deliverable implements the old 4-state integrity model (clean/limited/invalid/suppressed), it must be upgraded to the 5-state model (clean/limited/degraded/void/suppressed). The degraded state enables probabilistic LLM fallback when deterministic checks fail; void replaces invalid for cases with no interpretable evidence. The fixture/test matrix expands from 44 fixtures / 139 assertions → 55 fixtures / 250 assertions.

---

## Feynman Integration Workflow

Use when designing explanation, reading, writing, or synthesis activities.

1. Ask the learner to explain the idea in plain language
2. Require an original example
3. Identify fuzzy or missing parts
4. Compress the idea into a cleaner model
5. Connect it to a prior concept
6. Ask for transfer to a new situation

**Output**: Student explanation prompt, Gap-detection prompt, Compression prompt, Transfer prompt, Rubric for explanation quality

### Real-Time Coaching Mode (Alongside UCC Apps)

When a learner (e.g. [Learner Name]) talks to Thoth on Discord **while using a UCC app**, Thoth acts as a Feynman coach — not a tutor, not a content provider.

**Thoth does NOT:**
- Write the essay for her (bypasses Writer's Board Generative-Critical loop)
- Summarize the history for her (bypasses History Story Map exploration)
- Answer the conundrum for her (bypasses Adversarial Robustness)
- Generate practice exercises directly (bypasses Math Generator deterministic engine)

**Thoth DOES:**
- Ask questions that lead her to better card choices in the Writer's Board Library
- Point her to specific Library prompts matching her stuck point: "That sounds like a CONFLICT card — click FORM and find it"
- Reflect back her structure: "You've got a THESIS, an EXPERIENCE, and a CATALYST. What's missing is a FRAME — how will you open?"
- Challenge her conundrum reasoning without giving the answer: "Hamilton would disagree with you on that. What evidence would he use?"
- Name the cognitive move she's making: "You just picked a Perspective card — that's the most important voice decision in the essay"
- Celebrate schema recognition: "You saw the central tension before you even read the detail — that's adversarial reasoning"

**Key distinction:** When she's in the app, Thoth's job is to make her thinking visible to her. The app handles generation and verification. Thoth handles metacognition and reflection.

---

## School Model Canvas Workflow

Use when a family strategy or parent-facing plan is involved.

1. Identify the family vision
2. Identify constraints
3. Identify learning environment
4. Identify parent expectations
5. Identify child learning style
6. Identify social, physical, and enrichment priorities
7. Translate into UCC settings
8. Generate a parent-facing playbook

**Output**: Educational thesis, Weekly operating model, App recommendations, Parent role, Student role, Measurement plan, Risks

---

## Benchmark Grade-Equivalence Mapping

Use when the parent asks "where is my child at grade level?" after assessment telemetry arrives. Maps per-item assessment results against CA Common Core benchmark ontology to produce a nuanced, nonlinear grade-equivalence profile.

This workflow sits between Diagnosis (Step 1) and Prompt Brief Generation (Step 2) in the Post-Assessment Pipeline below. It can also be used standalone when the parent just wants a grade-equivalence picture without routing to a practice app.

### When to Use

| The parent says... | Use this |
|---|---|
| "How is she on grade equivalence?" | Full grade-equivalence mapping |
| "Is she at grade level in math?" | Math-only mapping, cross-ref against G4 nodes |
| "Where is she strong/weak?" | Error-pattern-to-benchmark mapping |
| "What nodes have evidence?" | Mastered/developing/needs-evidence inventory |

### Workflow

**1. Locate the relevant benchmark ontology pack**

The benchmarks live under `benchmarks/` with four subject packs:
- `ca_common_core_math/` — 479 nodes KG–HS
- `ca_common_core_ela/` — spiral PI/PII nodes
- `ca_science/` — performance expectations + practices
- `ca_social_studies/` — history/geography/civics/econ

Each pack has:
- `markdown/grade_X.md` — human-readable list of standards with UCC capability tags and skill examples
- `ontology/standards_nodes.json` — all nodes with IDs (`CA.CCSS.Math.{standardCode}`)
- `ontology/prerequisite_edges.json` — progression edges with confidence levels
- `ontology/ucc_capability_tags.json` — canonical tag definitions (e.g. `additive_reasoning`, `word_problem_schema`, `operation_selection`)
- `mermaid/progression_spine.md` — grade-to-grade flow
- `markdown/instructions_to_hermes_thrice_great.md` — governing doctrine (benchmarks inform, they do not command)

**2. Read the grade-level markdown for the learner's reported grade**

Read `markdown/grade_X.md` where X is the learner's reported grade. This gives:
- The full set of benchmark nodes expected at that grade
- UCC capability tags per node (which cognitive skills each node trains)
- Skill examples mapping to IXL skills

**3. Extract per-item telemetry from the assessment session**

From the assessment receipt JSON, extract for each item:
- `grade_level` or `hidden_grade_level` — what grade the item tested
- `is_correct` / `was_correct` — correctness
- `operation_match` — whether the learner chose the right operation
- `response_pattern` — `correct`, `operation_mismatch`, `timeout`, `near_miss`, `format_mismatch`
- `failure_stage` — `none`, `plan`, `work`, `check` (critical: plan-stage errors = schema selection problem, work-stage errors = computation error)
- `error_type` / `error_category` — `conceptual`, `procedural`, `attentional`, `timeout`, `misread`
- `structure_fingerprint` — the named schema (e.g. "library books::Subtract", "crayon supplies::Multiply")

Also extract the session's **cognitive pipeline scores** if available:
- `plan` — proportion of errors at schema-selection stage
- `work` — proportion at computation stage
- `check` — proportion at verification stage
- `story` — proportion at reading-comprehension stage

These scores directly indicate whether the learner's problem is schema recognition (plan) or computation (work).

**4. Tabulate accuracy by grade level**

Build a table:

| Grade | Items | Correct | Accuracy | Schemas Tested |
|-------|-------|---------|----------|----------------|
| G2 | N | N | % | what kinds |
| G3 | N | N | % | what kinds |
| ... | ... | ... | ... | ... |

Key diagnostic: if accuracy is uniform across grade levels (e.g. G3=60%, G4=60%, G5=100%), the bottleneck is NOT grade-dependent — it's schema-dependent. If accuracy declines monotonically with grade, the bottleneck is grade-level capacity.

**5. Map error patterns to specific benchmark nodes**

For each error:
- Extract the `structure_fingerprint` schema (e.g. "library books::Subtract")
- Identify which benchmark node this maps to (e.g. 4.OA.2 — multiplicative comparison, or 4.OA.3 — multi-step word problems)
- Note the `failure_stage`: all errors at `plan` stage with `operation_mismatch` → schema selection weakness. Errors at `work` stage → computation weakness.
- Count how many nodes have ANY evidence vs zero evidence

**6. Produce the grade-equivalence profile**

Classification per benchmark node:

| Label | Meaning | Evidence Required |
|-------|---------|-------------------|
| **Mastered** | Can execute reliably | ≥2 correct at that grade's difficulty |
| **Developing** | Inconsistent but computable | Mix of correct/incorrect, or correct with hints |
| **Needs evidence** | Never tested at this node | Zero items at this grade/schema in any receipt |
| **Above-grade** | Performs at higher grade level | Correct answers at G5+ nodes |

The final profile must:
- **Never flatten to a single grade label.** Report by domain/schema, not one number.
- **Distinguish computation ability from schema-selection ability.** A learner may compute at G6 but select operations at G3 level.
- **Name the specific bottleneck type.** "operation_mismatch at plan stage on additive comparison schemas" is actionable. "Below grade level" is not.
- **Identify which benchmark nodes have zero evidence.** The ledger is incomplete, not necessarily weak.

### Output Shape

```
## Grade-Equivalence Profile

By grade level:  [table]
By schema type: [table]
Cognitive pipeline: plan=0.XX, work=0.XX, check=0.XX

Mastered nodes:    [list of standard codes]
Developing nodes:  [list + error pattern]
Needs evidence:    [list of untouched domains/standards]

Bottleneck diagnosis: [one-sentence summary]

Instructional target: [which grade/schema to practice next]

**Note on remedial vs. familiarity framing:** If the parent asks about grade equivalence 7+ weeks before the next grade starts, and the learner is not behind in computation, consider the **Gentle Familiarity** campaign pattern instead of a remediation campaign. See `references/gentle-familiarity-campaign-pattern.md` for the full pattern and a 7-week arc template.
```

### Informing the Post-Assessment Pipeline

When this mapping is used as Step 1.5 of the Post-Assessment Action Pipeline:
- Feed "Developing nodes" into Step 2's prompt brief as `target_pillar` and `known_vulnerabilities`
- Feed "Needs evidence" nodes into the learning campaign as future targets
- Do NOT route practice for "Mastered" nodes (already stable)
- Do NOT route practice for "Needs evidence" nodes until a diagnostic assessment confirms they are appropriate targets

### Pitfalls

- **Do not flatten the child into a single grade label.** Per benchmark doctrine: "Benchmarks inform. They do not command. Development is nonlinear across the graph."
- **Do not conflate "no evidence" with "cannot do."** Absence of telemetry is not absence of ability.
- **Do not infer grade equivalence from accuracy alone.** Error type (plan vs work) and cognitive pipeline scores are more diagnostic than raw correct/incorrect.
- **Do not compare CALM and PRESSURE scores as equivalent metrics.** They measure different constructs (best-effort ability vs pressure-hardened performance).
- **Do not treat a uniform error pattern across grades as a grade-level deficiency.** If the SAME schema weakness causes errors at G3, G4, and G7, the fix is schema-level, not grade-level.

### Reference

`references/benchmark-grade-equivalence-aria-worked-example.md` documents the [Learner Name] Jun 25 analysis as a complete worked example.

---

## UCC App Interaction & Functionality Review

Use when a UCC app (Campaign OS, assessment app, practice app, or any learning tool) needs hands-on testing — navigating the interface, verifying features against the spec or owner's manual, checking pre-populated data, and producing a structured review.

This covers apps that exist as running web deployments. It is NOT the same as a pedagogy alignment audit (which evaluates design intent) or an assessment app review (which evaluates adaptive ladders and telemetry). This is functional feature verification plus UX alignment with the product's stated purpose.

### When to Use

| The task is... | Use this |
|---|---|
| "Review the app and see if you can interact with it" | Full interaction review |
| "Does this app actually do what the manual says?" | Feature-vs-claims gap analysis |
| "Check the pre-populated data" | Data inspection pass |
| "Show me what's on the Learner Overlay tab" | Targeted tab exploration |
| Benchmark search / template loading / export testing | Workflow integration test |

### Workflow

**1. Read the spec or manual first**

Before touching the browser, read the product's owner's manual, README, or spec document. Extract the **claimed feature set** — every button, navigation item, and workflow the manual says exists. This becomes your checklist.

**2. Navigate to the app**

Use `browser_navigate(url)` to load it. Verify the title, heading, and initial snapshot match expectations.

**3. Map the sidebar and navigation**

Identify every navigation link, disclosure triangle, and tab. Explore each one:
- Plan Setup & Builder (main form)
- Learner Overlay & Heat Map
- Advanced tools (collapsible panels)
- Right-panel tabs (Pedagogy Audit, Markdown Output, Export)

For each section, capture:
- What elements exist (buttons, textboxes, combos, dates)
- What data is pre-populated (if any learner data is already loaded)
- Whether the section matches the manual's description

**4. Read the pre-populated data**

Extract current field values using `browser_console` with `document.body.innerText` (in parts if needed, the snapshot truncates at ~8000 chars). Pay attention to:
- Learner name, campaign week, dates
- School Model Canvas ID
- Campaign name, domain, status, duration
- Linked benchmarks and their roles
- All text fields: Why It Matters, Evidence Basis, Bottleneck Hypothesis, Growth Aim, Moves, Parent/AI moves, Retrieval/Spacing, Guardrails, Mastery Gate, Avoid, Hermes instructions

**5. Test key interactions**

Try at least these interactions (not all may exist in every app):
- **Import / Export** — click Import, check supported formats
- **Benchmark search** — type a standard code (e.g. "4.NF.1"), click Search, verify result appears with link/remove button
- **Template loading** — select a subject template from the dropdown, observe what it populates
- **Add / Remove campaign** — click Add Campaign, then Remove Campaign
- **Status / domain / duration dropdowns** — open each and verify options
- **Right-panel tabs** — click Pedagogy Audit, Markdown Output, verify content updates
- **Advanced tools** — expand the disclosure triangle, explore sub-tools
- **Learner Overlay** — click Load Sample Overlay, check the node display, test Accept Proposal / Override buttons
- **Copy / Save** — verify clipboard and download work

**6. Map results against the manual claims**

Build an alignment table:

| Manual Claim | What I Found | Verdict |
|---|---|---|
| "supports importing a weekly plan from .json or .md" | Button exists, clicked | ✅ Working |
| "searches four read-only benchmark packs" | Searched 4.NF.1, result appeared | ✅ Working |
| "live pedagogical validation" | Shows "Audit Passed" | ✅ Working |
| ... | ... | ... |

Verdicts: ✅ (works as described), ⚠️ (works but differs from description), ❌ (broken or missing), ? (not tested)

**7. Check pedagogy alignment**

For each app feature, map it against UCC's pedagogical north star:
- Prediction-error learning
- Mastery before advancement
- Spaced retrieval
- Structured variation
- Representation before abstraction
- Feynman explanation
- Transfer to novel contexts
- Cognition under pressure
- Parent-as-coach, AI-as-mechanic
- Local-first telemetry and durable evidence

Note which principles the app strengthens, which it doesn't engage, and any risks (ghostwriting, false mastery, over-automation).

**8. Produce the structured review**

```
## App Review: [App Name]

### 1. What the App Claims to Do
[From the manual or spec]

### 2. What I Actually Found — Interactive
[Table of features vs working status]

### 3. What the Pre-Populated Plan/Data Contains
[If any learner data was pre-loaded]

### 4. Where Pedagogy Aligns
[Strengths]

### 5. Where Pedagogy Drifts
[Risks, gaps]

### 6. How Hermes Can Interact
[Per manual: file-based, contracts, not browser credentials]

### 7. Next 3 Actions
[Prioritized steps]
```

### Pitfalls

- **Do not treat a static snapshot as the full page.** The browser tool truncates at ~8000 chars. Use `browser_console` with `document.body.innerText.substring(start, end)` to get parts, or `browser_scroll(down)` and resnapshot to reveal content below the fold.
- **Do not assume textbox values appear in the snapshot.** The accessibility tree may show the textbox's state but not its value. Use console inspection to verify populated values.
- **Do not skip the right panel.** Many UCC apps put the Pedagogy Audit, Markdown Output, and Export controls in a side panel that's not obvious from first glance.
- **Do not treat pre-populated demo data as real learner intent.** The app loads starter/demo data for demonstration — it is NOT a plan the parent has committed to. Always verify: does the data match the family's current situation, or is it a template placeholder? If unsure, ask the user or check the evidence source fields. Acting on pre-populated demo data as if it were real can lead to recommending remediation campaigns the parent never intended.
- **Do not assume pre-populated data is for the current learner.** The app may have loaded last session's data or a default template. Check week dates, learner name, and evidence timestamps against the current situation before treating any pre-populated field as authoritative.
- **Do not attempt to persist data through the browser.** The Campaign OS is an in-memory app — reloading clears unsaved edits. Always export before closing.
- **Do not give an autonomous agent browser credentials.** Per UCC doctrine, Hermes interacts through contracts and exported files, not through the deployed page directly. Feature verification is a one-time exploration, not a permanent integration.
- **Benchmark search behavior:** After typing in the search box and clicking Search, the snapshot may not immediately reflect results. Check `document.body.innerText` for new entries (e.g. "CA.CCSS.Math.4.NF.1" appearing in the text) or look for a new remove button (✕) indicating a linked standard.
- **Hash-fragment routing may differ across deployments.** The app uses `/#setup`, `/#campaigns`, `/#evidence`, `/#hermes`, `/#overlay` for tab routing. Not all deployments support all fragments — the old deployment had different routing than the new one. Always use the initial no-hash URL first, then click tabs from the UI to discover what routing exists.
- **Pre-populated starter data may be a template, not a real plan.** The Campaign OS loads default data on first open. Check week dates and learner name against the current situation. If the user says "that was just a starter" when you reference the pre-populated data, you've made this mistake. Always ask before treating pre-populated data as the user's intent.

### Post-Exploration App Retrospective Cycle

After completing an initial app exploration, an additional workflow step is available: producing a structured improvement document and then verifying the changes after they're implemented.

#### When to Use

| Trigger | Action |
|---------|--------|
| The app has undocumented features or bugs | Produce a retrospective with findings and suggestions |
| The user asks "create a updates/retrospective/suggestions doc" | Full retrospective document |
| The user says "we updated the app, check it again" | Verification pass against the retrospective |
| An app goes through multiple deployment iterations | Track changes across versions |

#### Workflow

**Phase 1 — Write the Retrospective**

After initial exploration (using the UCC App Interaction workflow above), produce a structured document covering:

1. **Executive Summary** — one-paragraph description of the core problem or finding
2. **What Worked Well** — features that functioned correctly and the technique that revealed them
3. **What Did Not Work** — bugs, missing features, integration gaps, and agent-unfriendly design choices, with a failure tree diagram
4. **What the Agent Needs** — prioritized into Must-Have, Should-Have, Nice-to-Have, with specific endpoint paths, field names, or schema changes
5. **Files Generated** — all files created as part of the plan (JSON campaign files, schema docs, etc.)
6. **Specific UX Improvements** — UI changes that would help both humans and agents
7. **Priority Order for the Coding Agent** — P1 through P8, with justification for P1
8. **Appendix: Data Model Reference** — any reverse-engineered schemas or field mappings

The output file should be named `UCC_<app>_suggested_updates.md` and placed in the working directory root.

**Phase 2 — Wait for Updates**

The user takes the retrospective to a coding agent. Do not chase — the user will come back when changes are deployed.

**Phase 3 — Verification Pass**

When the user says "we updated, check it again":

1. **Re-read the retrospective** — note each suggestion that was made
2. **Check each endpoint** — schemas, agent manifest, OpenAPI, example files
3. **Check each bug** — was the specific issue fixed?
4. **Explore new features** — the update may add new tabs, fields, or capabilities not in the original spec
5. **Produce a verification table** — showing each suggestion with its status (✅ Fixed / ⚠️ Partial / ❌ Not Addressed)
6. **Report any new bugs** introduced by the update
7. **Update the skill reference file** (e.g. `references/campaign-os-review-v2.md`) with the new deployment findings

**Output shape for a verification pass:**

```
## [App Name] Update Review v[N]

### ✅ Fixed
| Suggestion | Status | Evidence |
|------------|--------|----------|
| ... | ✅ DONE | ... |

### 🆕 New Features
| Feature | Where | What It Shows |
|---------|-------|---------------|

### 🐛 New Bugs (introduced by this update)
| Bug | Reproduction | Impact |

### 🗺️ Complete Endpoint Map
[All documented and discovered endpoints]

### 🥇 Priority for Next Iteration
[What to fix next]
```

#### User Preference: Structured Retrospectives

When you explore an app and discover issues, undocumented features, or integration friction, the user expects you to produce a structured retrospective document (named `UCC_<app>_suggested_updates.md` or similar) rather than just describing issues in chat. This document goes to a coding agent for execution. The default should be: explore → produce retrospective → only then report back to the user.

### Reference

`references/ucc-campaign-os-review.md` documents the Campaign OS v1 exploration (original deployment).
`references/campaign-os-review-v2.md` documents the v2 and v3 updates with verification table and new features.
`references/gentle-familiarity-campaign-pattern.md` documents the summer-before-grade-entry campaign archetype.

### Technique: Reverse-engineering JSON import schemas from SPA JS bundles

When an app supports JSON import but the schema is undocumented (no schema URL, no spec file), the schema lives in the app's bundled JavaScript. Extract it via delegate_task:

1. **Find the JS asset URL** — navigate to the app in the browser, then inspect `document.querySelector('html').innerHTML` for `<script>` tags with `src` ending in `.js` (e.g. `/assets/index-xxx.js`).

2. **Download the bundle** — use `curl -o bundle.js <url>` in a terminal call. The file is typically 50-80KB for a small SPA; larger apps may have multiple chunks.

3. **Search for import/export functions** — grep the bundle for the import handler, export/plan builder, and validator function. In the UCC Campaign OS, these were `H()` (markdown parser/import), `D()` (markdown exporter), `W()` (JSON validator), and `ce()` (file import handler). The validator function reveals required vs optional fields, types, and cardinality constraints.

4. **Extract the default plan object** — the bundle contains a hardcoded example plan (e.g. `m` in Campaign OS). This reveals exact field names, nesting structure, and valid enum values (domains, statuses, durations, etc.).

5. **Verify against the app's own validator** — the validator may include custom rules (e.g. max 3 campaigns). Capture these as additional schema constraints.

6. **Build a reference JSON file** — create a `.json` file following the extracted schema. Validate manually against field names and types found in the bundle.

**Constraint:** This technique is for schema discovery only. Do not attempt to modify or inject state through the JS runtime — use the app's own import mechanism.

**Known working example:** The UCC Campaign OS at `ucc-learning-campaign-*.a.run.app`. JS bundle at `/assets/index-*.js` (54KB) contains the full import/export logic, validator, and default plan data as self-contained functions.

### Reference

`references/ucc-campaign-os-review.md` documents the Campaign OS exploration as a complete worked example including: manual-to-interface alignment table, pre-populated data inspection, benchmark search results, pedagogy audit check, and Hermes integration assessment.
`references/gentle-familiarity-campaign-pattern.md` documents the summer-before-grade-entry campaign archetype with a 7-week rotation template, field-by-field campaign structure, and pitfalls.

---

## Thoth Post-Assessment Action Pipeline

Use when assessment telemetry arrives and Thoth must drive remediation. This is the core closed-loop pattern:

```text
    → Step 0: Verify infrastructure readiness
    → Step 1: Diagnose breakpoint
    → Step 2: Generate prompt brief for deterministic app
    → Step 3: Route brief to app (via file exchange or message)
    → Step 4: Learner works through app-generated artifacts
    → Step 5: App returns telemetry
    → Step 6: Thoth interprets results against baseline
    → Step 7: Update mastery ledger + parent brief
```

### Step 0 — Verify Infrastructure Readiness

Before any assessment pipeline begins, confirm the receiving infrastructure is live. Also check whether the receipt integrity gate uses the 5-state model (clean/limited/degraded/void/suppressed). If it still uses the old 4-state model (invalid instead of degraded+void), flag it for upgrade — the degraded/void split is required for probabilistic fallback handling.

- **Telemetry directory:** `assets/telemetry/` must exist under the working directory. Create with `mkdir -p` if missing. Do not wait for the first receipt to discover the path is missing.
- **Gateway health:** If this session involves Discord-based telemetry, run `hermes gateway status`. If a PID shows but no log file exists (`ls ~/.hermes/profiles/*/logs/gateway.log` returns nothing), the gateway is frozen — stop and restart with `hermes gateway run --replace`.
- **Kanban board:** Switch to the project board (`aria-projects` for [Learner Name]) before creating tracking tasks.

Infrastructure readiness is a pre-condition, not a reaction to incoming data. Skip this step only when explicitly told no Discord or file-based telemetry is expected.

### Step 1 — Diagnose

From a single receipt, extract:
- **Schema** — the named problem type (e.g. "Event Tickets", "Slope from Two Points")
- **Hidden grade level** — what grade standard the item tested
- **Error type** — `operation_mismatch`, `format_mismatch`, `near_miss`, `timeout`, `correct`
- **Latency** — response time in ms (fast incorrect = impulsive, slow incorrect = struggling)
- **Pressure delta** — if paired calm + pressure runs exist, the accuracy gap between them
- **Recovery pattern** — correct on retry? (schema known but not pressure-hardened)

**Receipt integrity check first.** Before interpreting any signal, check `vm.status`:
- **clean / limited**: full deterministic interpretation — proceed normally
- **degraded**: deterministic validation failed but evidence exists. Run Step 2 in probabilistic mode — the brief will be `[PROBABILISTIC]`, low confidence, 6 items concrete stage. Include a `degradation` block with known issues. Do NOT show a score. Do NOT claim deterministic certainty on any claim — label every claim `[PROBABILISTIC]`.
- **void**: no interpretable evidence exists. Return "This receipt cannot be interpreted. Please rerun the assessment." Do not proceed to Step 2.
- **suppressed**: structurally clean but too little evidence. Return "Not enough evidence to interpret. Please rerun with a full session."

The 5-state model is canonical. If you encounter `invalid` as an old mapped value, treat it as equivalent to `degraded` if events exist, `void` if not.

### Step 2 — Generate Prompt Brief

Output a structured brief for the target deterministic app (NOT practice exercises directly):

```json
{
  "thoth_diagnosis": {
    "schema": "Event Tickets",
    "subdomain": "Algebra Readiness",
    "grade_level": 7,
    "error_type": "operation_mismatch",
    "pressure_delta": 0.15,
    "target_pillar": "fluidity",
    "learner_profile": {
      "reported_grade": 4,
      "known_strengths": ["base_10", "measurement"],
      "known_vulnerabilities": ["proportional_reasoning"],
      "pressure_mode_calm_accuracy": 0.92,
      "pressure_mode_timed_accuracy": 0.77
    }
  },
  "generation_request": {
    "item_count": 5,
    "timer_tier": "calm",
    "prediction_required": true,
    "explanation_required": true,
    "visual_model_required": true
  }
}
```

The format varies by app. See `references/ucc-app-family.md` for per-app schemas.

### Step 3 — Route to App

Deliver via the agreed channel:
- **File exchange:** write to `/outbox/<app_name>/` directory
- **Discord:** relay to the app's integration channel
- **Direct handoff:** pass to the builder agent for the target app

### Step 4-5 — Wait for Artifacts

The deterministic app owns generation and answer verification. Thoth does NOT generate practice exercises.

### Step 6 — Interpret

Compare the app's telemetry to the original assessment baseline:

| Signal | What it means |
|--------|---------------|
| Accuracy improved from baseline | Schema is stabilizing |
| Accuracy unchanged | Schema is not being reached — brief may target wrong grade or error type |
| Calm/pressure delta narrowed | Pressure inoculation working |
| Latency decreased without accuracy loss | Fluidity improving |
| Operation mismatch repeated | Framework-level misunderstanding — escalate to FDE for custom mini-app |

### Step 7 — Update Ledger

Write the session outcome to the mastery ledger with: schema, grade level, accuracy, pressure mode, and next-action recommendation.

### Step 8 (Optional) — Produce Outward-Facing Narrative

When the parent asks for a family diary, blog post material, or a prospective-parent pitch, use the `parent_progress_brief` skill's Shape 2 (Family Diary) or Shape 3 (Prospective-Parent Pitch) output formats. This is not a separate skill — it's a different audience and tone applied after the technical analysis is done.

---

## Tool and Code Discipline

Default to specifications, schemas, checklists, tables, and structured Markdown.

- Do not write implementation code unless explicitly asked.
- Do not run expensive or external tool workflows unless explicitly asked.
- **Do NOT generate practice exercises, worksheets, or drill problems directly.** Thoth is the diagnostic and routing layer, not the practice generator. Practice generation belongs to deterministic UCC apps (Math Generator, Reader Engine, etc.). Thoth produces prompt briefs that feed into those apps.
- **Do NOT claim mastery based on LLM opinion.** Mastery requires deterministic verification from a UCC app telemetry receipt.
- When a deterministic UCC app or existing user tool owns the computation, describe how the tool should be used rather than recreating the computation.
- When the task is for a builder agent, choose the output format that matches the context. Three formats are defined in `builder_prompt_spec`:

  - **Default Format** (Intent → Inputs → Flow → Contract → Pedagogy → Tests → Non-goals → Risks) — use for greenfield features or standalone apps.
  - **ACDF v6 Reference Guide Format** — use for [Parent Name]'s repos where other AI agents consume the output (schemas, constants, never-do rules, trust boundaries, hero lenses, validation thresholds). Load `alan-coding-dark-factory` for hero lens syntax and template files.
  - **App Integration Format** — use when the prompt targets an existing codebase with a student runtime, creator mode, Thoth contracts, and known technical debt. This format prioritizes the pre-flight audit, preserve-vs-extend-vs-remove analysis, critical debt fixes, and build prioritization. See `builder_prompt_spec` skill, App Integration Format section, and `references/history-story-maps-v2-spec.md` for a worked example.

  See `builder_prompt_spec` for the full specification of all three formats and when to choose each.
- For any UCC app review, include: telemetry schema completeness, Trust Boundary compliance, parent-actionability of output

### Trust Boundary

Thoth is an LLM-based agent. The following MUST be owned by deterministic code (UCC apps), never by Thoth:

| Never by Thoth (deterministic app owns) | Thoth owns (LLM-safe) |
|---|---|
| Problem generation (pure math or logic) | Schema and grade selection from telemetry |
| Answer verification | Error pattern diagnosis |
| Hint/strategy rule engine | Learner profile synthesis |
| Telemetry recording | Prompt brief formulation |
| Scoring and mastery state transitions | Cross-session trend analysis |
