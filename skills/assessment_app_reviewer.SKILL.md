---
name: assessment_app_reviewer
description: "Review UCC STAR-style assessment apps, adaptive cognitive ladders, Brain Power scores, telemetry exports, or pressure-mode test design — and interpret raw telemetry receipts into cognitive signals, ceiling detection, error patterns, and pressure vulnerability."
version: 2.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ucc, assessment, review, star, telemetry, diagnosis]
    related_skills: [pedagogy_alignment_audit, mastery_ledger_contract]
linked:
  references:
    - references/telemetry-schema.md
    - references/reverse-engineered-data-model.md
    - references/app-update-verification-example.md
---

# Assessment App Reviewer

## Overview

Review UCC STAR-style assessment apps, adaptive cognitive ladders, Brain Power scores, telemetry exports, or pressure-mode test design.

**Two modes of use:**

1. **App review** — evaluate the assessment design itself (ladder, pillars, telemetry fidelity)
2. **Receipt interpretation** — analyze a real student session's raw telemetry for cognitive signals, error diagnosis, ceiling detection, and pressure vulnerability

Do not use this skill for general UCC product positioning.

---

## Procedure: App Review

Two variants exist. Use **Variant A** for adaptive assessment apps (STAR-style tests with adaptive ladders). Use **Variant B** for non-assessment UCC apps (campaign builder, dashboard, reader engine, companion API).

### Variant A — Assessment Instrument Review

Use when evaluating an assessment *app* or *instrument* (before student data exists).

1. **Identify domain and target grade band**
   - Subject, subdomain, constructs measured, grade band range
2. **Identify adaptive ladder structure**
   - Difficulty levels, hidden grade bands, advancement rules (correct → step up), recalibration rules (incorrect → step down)
   - Does it cap at a max, or keep probing?
   - How many unique schemas per grade band?
3. **Identify measured cognitive pillars**
   - Crystallized, Fluidity, Augmented, Pressure — which are active?
   - Is the pressure mode a separate session or a timer tier within session?
4. **Validate telemetry completeness**
   - See `references/telemetry-schema.md` for the full field inventory
   - Check which fields are populated vs. null vs. missing
   - Check for integrity warnings (duplicate items, pool exhaustion)
5. **Check whether outputs reconstruct student thinking**
   - Can you reproduce what the student knew from the telemetry alone?
   - Or do you need the actual answer string?
6. **Recommend fixes**

### Variant B — Non-Assessment UCC App Review

Use when evaluating a UCC app that is NOT an adaptive assessment (campaign builder, dashboard, learner overlay, companion API). This covers UX, data model, API surface, schema discoverability, and pedagogical alignment of the app design itself.

1. **Identify the app's purpose and claims**
   - What does it claim to do? Read the owner's manual or README first
   - What does it actually do? Navigate and explore every tab/section
   - Map both against the UCC pedagogical north star (mastery, transfer, retention, coaching)
   - Identify discrepancy between claimed and actual behavior

2. **SPA interaction strategy**
   When the app is a single-page application and browser tools are unreliable (snapshot truncation, DOM queries return null, button clicks have no visible effect):
   - Extract the full page text via `browser_console("document.body.innerText")` — this is more reliable than the truncated snapshot
   - Find the JS bundle URL from the page source (look for `<script type="module" src="/assets/index-*.js">`)
   - Download the JS bundle with `curl` and search for field names, validator functions, and default data objects to reverse-engineer the data format
   - **Do not fight the browser form** for complex multi-field data entry. Instead, build importable JSON files that match the app's format and import them
   - For state-changing operations (add campaign, remove campaign, submit override): if the browser click doesn't work after 2 attempts, the app may not allow that operation for the current state (e.g., can't remove the only campaign). Look for guard conditions in the JS bundle
   - Use `web_extract` on known endpoints to probe for schema files, API documentation, and example files

3. **Schema and contract discovery**
   - Check these endpoints in order:
     - `/schemas/weekly_campaign_plan.schema.json` — main plan schema
     - `/openapi.json` — full API documentation
     - `/agent/hermes.json` — agent manifest describing companion API
     - `/examples/weekly-campaign-plan.json` — sample import file
   - If endpoints return the app's HTML page instead of JSON, the schemas don't exist yet — mark as missing
   - For local companion APIs: check `http://127.0.0.1:4174/agent/hermes.json`
   - Document which schemas exist and which are missing

4. **Data model extraction (fallback when schema endpoint missing)**
   If no schema endpoint exists:
   - Download the JS bundle via `curl -s <bundle_url>`
   - Search for the validator function (usually named `W()` or similar, checks required fields)
   - Search for the default/example plan object
   - Extract all enum values (domain, status, duration, directInstructionNeed, etc.)
   - Build a TypeScript interface from the extracted fields
   - Validate by writing a test JSON file and checking it against the validator
   - See `references/reverse-engineered-data-model.md` for an example of the output format

5. **Verify against previous recommendations**
   When the user says the app was updated based on a retro document you previously submitted:
   - Build a systematic checklist from every item in your retro
   - For schema endpoints: use `web_extract` — returns JSON or failure
   - For UI changes: use `browser_navigate` and inspect the DOM for new elements
   - For API changes: check the new JS bundle for endpoint handler functions
   - Report each retro item as ✅ DONE, ⚠️ Partial, or ❌ Still Missing
   - Include one new finding or bug discovered during verification
   - See `references/app-update-verification-example.md` for the output format

6. **Benchmark search verification**
   - Search each benchmark pack (Math, ELA, Science, Social Studies) with a known standard code
   - Verify the search returns relevant results
   - Check that the standard IDs match the format in `standards_nodes.json`
   - Verify linked standards appear correctly in the campaign editor

7. **Recommend fixes**
   - Separate into: P0 (blocks workflow), P1 (saves major agent time), P2 (nice-to-have)
   - Include specific implementation guidance (field IDs to change, endpoints to add)

---

## Procedure: Receipt Interpretation

Use when a raw UCC telemetry receipt arrives (from [Learner Name] or any student). Follow this sequence:

### Step A — Structural Scan

Read the summary block first:

| Field | What to look for |
|-------|-----------------|
| `accuracy` | Ceiling or floor? >= 90% means no ceiling found yet |
| `max_difficulty_reached` | Is this the ladder's top? If yes, ceiling unknown |
| `performance_index` | Internal metric — track change across sessions, not absolute value |
| `integrity_warnings` | If duplicate items exist, treat ceiling claims with skepticism |
| `test_duration_setting_minutes` | 5 min = pressure mode , 10 min = calm mode (infer from this if no explicit flag) |
| `hidden_grade_level` on events | What grade levels did the student actually face? |

### Step B — Adaptive Ladder Trace

Plot the difficulty_before → difficulty_after sequence. Every recalibration down (e.g. 5→4) marks a **wall**. Every recalibration up (e.g. 4→5) marks a **pass**.

Key questions:
- How many walls? What grade level triggered each wall?
- Did the student recover on retry? (Same schema, second attempt = recovery signal)
- Did the ladder plateau? If difficulty stays at max for 5+ items, **ceiling not reached** — test pool exhausted.

### Step C — Error Diagnosis

For every `was_correct: false` event, examine:

| Field | If true | If false |
|-------|---------|----------|
| `operation_match` | Student used right approach, execution error | Student used wrong framework — conceptual gap |
| `response_pattern` | `incorrect` = attempted | `timeout` = froze | `blank` = skipped |
| `response_time_ms` | Fast (< 10s) = guess / impulsive | Slow (> 30s) = struggled, then got wrong |
| `timer_appropriateness` | Was pressure a factor? |

**Combine into a diagnosis:**

| Pattern | Likely meaning |
|---------|---------------|
| Fast incorrect + operation_mismatch | Applied wrong framework — doesn't recognize the schema |
| Slow incorrect + operation_match | Knows the approach but execution breaks down (arithmetic slip, multi-step loss) |
| Timeout + blank | Froze under pressure — not a knowledge gap, a regulation gap |
| Fast correct after error | Recovery signal — learn from mistake, adjust speed |

### Step D — Ceiling Detection

The most common finding in these assessments is **no ceiling found** (test runs out of items before the student fails). Signals:

- Last 3+ items all correct at max difficulty
- Student finished before timer expired
- Item repetition in integrity warnings (pool exhausted)

**Action**: Flag "Ceiling not reached — this test cannot measure this student's upper bound. Need harder items or a different instrument."

### Step E — Schema Stability Analysis

Group events by `schema` name. For each schema, ask:

- Correct on first encounter? If not, a gap exists
- Correct on repeat? If yes, student can learn from exposure
- Consistent response time? Big variance = unreliable knowledge
- Operation match stable? Schema-specific misunderstanding vs general

### Step F — Calm vs Pressure Delta

When a student has BOTH a calm session (10 min) and a pressure session (5 min) on the same subdomain:

| Metric | Calm | Pressure | Delta | Meaning |
|--------|------|----------|-------|---------|
| Accuracy | — | — | > 15% drop | Pressure vulnerability |
| Avg time | — | — | < 50% of calm | Rushing, not adjusting |
| Wall location | — | — | Earlier wall in pressure | Cognitive load degrades performance |
| Error type shift | — | — | operation_mismatch ↑ | Framework degrades under pressure |

**Big delta** = narrow safe zone. Need to strengthen the skill until pressure performance matches calm.
**Small delta** = robust. Student can perform under constraint.

---

## Output Format

### App Review

- **Domain**: subject area and grade band
- **Adaptive ladder**: difficulty levels, hidden grade bands, advancement and recalibration rules
- **Cognitive pillars**: which of Crystallized, Fluidity, Augmented, Pressure are measured
- **Telemetry captured**: what the system records
- **Telemetry missing**: what the system does not record but should
- **Reconstruction quality**: whether outputs can reconstruct what the student knew
- **Required fixes**: specific changes to assessment design

### Receipt Interpretation

- **Session context**: domain, subdomain, duration setting, student reported grade
- **Structural summary**: items, accuracy, max difficulty, ceiling status, integrity warnings
- **Adaptive ladder trace**: walls passed, walls failed, recovery evidence
- **Error diagnosis**: per-error analysis with operation_match + response_time + timer context
- **Schema stability**: which schemas are stable, which are fragile
- **Pressure delta** (if paired data exists): calm vs pressure comparison
- **Diagnostic limits**: what this telemetry CANNOT tell us (missing fields, answer content, etc.)
- **Next actionable question**: what to ask the student or test next

---

## Known Diagnostic Limits

These fields are **not yet populated** in v1.1 receipts (check schema_version before assuming):

- `hints_used` — exists in Performance Index formula but not logged per event
- `started_at` — frequently null
- Student answer content — only correctness is recorded, not what was entered
- Pressure-mode flag — must be inferred from `test_duration_setting_minutes`
- Error subtype taxonomy — only coarse `response_pattern` available

When these are missing, you can flag a domain-level weakness but NOT a specific concept-level diagnosis. Follow up with a Feynman gate or direct questioning.
