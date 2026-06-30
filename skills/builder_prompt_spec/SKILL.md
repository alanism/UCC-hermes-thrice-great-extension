---
name: builder_prompt_spec
description: "Turn UCC product intent into a builder-ready prompt for Gemini, Claude, Codex, or another coding agent."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ucc, builder, prompt, spec, product]
    related_skills: [pedagogy_alignment_audit, mastery_ledger_contract]
---

# Builder Prompt Spec

## Overview

Turn UCC product intent into a builder-ready prompt for Gemini, Claude, Codex, or another coding agent.

Do not use this skill to write production code directly.

## Pre-Flight Checks (Before Writing)

**Check these before drafting.** Skipping them produces prompts that contradict existing contracts or miss known debt:

1. **UCC App Contract** — Check the supplied, repository-local app contract. It defines what Hermes Thrice Great sends to the app and what the app must return. Every builder prompt must be consistent with that contract.

2. **CTO / Technical Review** — If a `docs/CTO_REVIEW_PACKET.md` or similar audit exists, read it. It lists known debt (DEBT-01, DEBT-02…), architecture constraints, and V2 proposals. Your prompt must fix critical/high debts or explain why they're deferred.

3. **Existing Codebase Scan** — Before proposing new architecture, check what already exists:
   - Student runtime (untouchable)
   - Creator/authoring code
   - Published artifact schemas and serializers
   - Existing Zod validators, types, and compiler pipelines

4. **Existing Integration Documents** — Repository-local contracts and owner documentation define offline routing and telemetry parsing. Read only the documents supplied with the target project.

When targeting a **V1.5 → V2 upgrade**, always create a table of preserved vs. extended vs. removed code (see App Integration format below).

## Procedure

1. State product intent
2. Define inputs
3. Define user flow
4. Define data contract
5. Define pedagogical constraints
6. Define acceptance tests
7. Define non-goals
8. Define risk checks
9. **If targeting an existing codebase**: add a preserve-vs-extend-vs-remove table mapping every file/directory to one of: untouched, refactor, extend, replace, or new

## Output Format

Choose the format that matches the context:

- **Default Format** — use for greenfield features or standalone apps
- **ACDF Reference Guide Format** — use for repositories where other agents consume the output.
- **App Integration Format** — use when the prompt targets an existing codebase with a learner runtime, creator mode, or established UCC contract.

### Default Format

- **Intent**: one-paragraph description of what the app/feature does
- **Inputs**: all data the feature receives
- **User flow**: step-by-step interaction sequence
- **Data contract**: schema for inputs, outputs, and persisted state
- **Pedagogy constraints**: non-negotiable learning design rules
- **Acceptance tests**: how to verify the feature works correctly
- **Non-goals**: explicitly excluded scope
- **Risks**: pedagogical, technical, evidence-validity, and privacy risks

### Dark Factory Reference Guide Format (for [Parent Name]'s Projects)

When producing builder prompts for agent-governed repositories, use the active repository ACDF reference-guide format. Do not assume an external private skill or profile exists.

Every section is required:

| Section | What it contains |
|---------|-----------------|
| **Product Outcome** | Who is this for, and what gets better if it works? |
| **Target User / Operator** | Who interacts with the system? |
| **System Scope** | What is in scope? |
| **Non-Goals** | What is explicitly out of scope? |
| **Schemas** | Every data object with fields, types, constraints, defaults |
| **Constants** | Every named constant with value and unit |
| **State Model** | Every UI state, persistence state, and transition |
| **Data Flow** | Direction of data movement, sources, transforms, sinks |
| **Calculation Rules** | Every formula, threshold, rounding rule, edge case |
| **AI / Model Output Contract** | What the AI generates, structure, validation, failure handling |
| **UX States** | Loading, empty, success, error, partial, offline |
| **Failure States** | Timeout, network loss, invalid input, empty response, provider 429 |
| **Security Boundaries** | Untrusted inputs, privileged actions, data that cannot leak |
| **Design Rules** | Voice, color, typography, spacing — with wrong examples |
| **Never-Do Rules** | What the system must never do |
| **Trust Boundary** | Which parts are deterministic vs LLM-generated |
| **Hero Lenses** | Agent behavior controls from the ACDF hero table |
| **Validation Proof** | What tests, screenshots, exports prove it works |

Append these to the prompt:

```text
Hero Lens:
[L] Lopopolo + [W] Willison

Agent Behavior:
- Make changes mechanically verifiable.
- Run declared tests before marking done.
- Touch only allowed files.

Evidence Required:
- Test command output
- Files touched list
- Validation note
```

### App Integration Format (for Existing Codebase Upgrades)

Use this when the prompt targets an existing codebase that has a learner runtime, creator mode, UCC contracts, and known technical debt. This format prioritizes telling the coding agent what **not** to touch and what **must** be fixed.

| Section | What it contains |
|---------|-----------------|
| **Core Context** | What the existing system does, what the UCC workflow enables, and known debt being addressed |
| **System Architecture** | Diagram + key decisions about how headless API relates to existing visual UI |
| **Hermes Thrice Great ↔ App Contract** | Full offline input/output schemas — what the UCC workflow supplies and what the app returns. Include a generic synthetic example. |
| **Internal Compilation Pipeline** | Flow from brief input through validation to artifact output. Note which pipeline stages are deterministic vs AI-powered |
| **Critical Debt Fix** | Exact specification for any DEBT-0x being fixed (schema changes, code location, fallback behavior, acceptance criteria) |
| **Data Flow & File Protocol** | Contained relative paths, CLI syntax, in-process API, and offline file exchange |
| **Existing Code: Preserve vs Extend vs Remove** | Table mapping every file/directory to untouched, refactor, extend, replace, or new |
| **Implementation Phases** | Phased plan with day estimates, prioritized |
| **Success Criteria** | Functional criteria + non-functional criteria (latency, determinism, isolation) + integration test scenarios |
| **Non-Goals** | Explicitly excluded scope |
| **Appendices** | Type definitions, reference file paths, telemetry schemas, any sub-schemas (e.g., ConundrumPayload) |

When writing the **Critical Debt Fix** section, always include:
- The exact symptom
- The file(s) to modify
- An implementation sketch (pseudocode or code diff)
- 4-6 acceptance criteria in a table

When writing the **Existing Code** table, organize by:
- **Preserve as-is** (student runtime, styling, data files, deployment config)
- **Extend** (add files to, not replace)
- **Remove / de-prioritize** (with reason)

**Build Priority table** — add a priority table for complex builds:

| Priority | Component | Why |
|----------|-----------|-----|
| **P0** | Core schema + validation | Foundation for everything else |
| **P0** | Deterministic in-process entry point | Core of the offline UCC integration |
| **P0** | Critical debt fix | Blocking bug |
| **P1** | Supporting infrastructure | Needed for integration |
| **P2** | Polish / tooling | Nice-to-have |
| **P3** | Human UI improvements | Lower priority |

Use only repository-local, public examples supplied with the target project. Do not assume a private profile reference or messaging integration exists.
