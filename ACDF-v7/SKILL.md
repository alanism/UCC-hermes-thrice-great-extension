---
name: ACDF v7.0 — Alanism Coding Dark Factory
description: Operating methodology for AI-agentic software builds. Load this file first, always. Load files under parts/ on demand per the routing table below — do not load all parts into context at once.
---

# ACDF v7.0 — How to Read This

flowchart TD
    A[ACDF v7.0] --> B[What This Document Is]
    A --> C[Who It Is For]
    A --> D[What Problems It Solves]
    A --> E[How It Is Structured]
    A --> F[How To Use It]
    B --> B1[Standalone operating methodology]
    B --> B2[Governance layer above AI coding tools]
    B --> B3[Lifecycle system from objective to production handoff]
    B --> B4[Not tied to any single model, IDE, or agent]
    C --> C1[Solo developer / technical founder]
    C --> C2[Engineer on an existing team]
    C --> C3[AI coding agent receiving repo context]
    C --> C4[Business function builder / domain expert]
    D --> D1[Specification problem]
    D --> D2[Authority problem]
    D --> D3[Structure problem]
    D --> D4[Recency problem]
    D --> D5[Context-cost problem]
    D --> D6[Execution-drift problem]
    F --> F1[Read the active graph first]
    F --> F2[Read authority.json second]
    F --> F3[Read acceptance gates third]
    F --> F4[Read task board fourth]
    F --> F5[Execute only against current authority]

flowchart LR
    A[Raw Sources] --> B[Source Manifest]
    B --> C[Canonical Mermaid Graph]
    C --> D[Approved Reference Guide]
    D --> E[Build Plan]
    E --> F[Adversarial Review]
    F --> G[Authority Capsule]
    G --> H[Task Board]
    H --> I[Agent Execution]
    I --> J[Receipts]
    J --> K[Learning Cards]
    K --> C
    B -. freshness check .-> G
    C -. graph hash .-> G
    J -. implementation proof .-> G

flowchart TD
    A[Agent Receives Context] --> B{Is docs/active/authority.json present?}
    B -->|No| X[Stop: no current authority]
    B -->|Yes| C[Load authority.json]
    C --> D{Does authority.json name current graph?}
    D -->|No| X
    D -->|Yes| E[Load architecture.mmd]
    E --> F{Does task cite current acceptance gates?}
    F -->|No| Y[Stop: task is underspecified]
    F -->|Yes| G[Claim task]
    G --> H[Implement minimal safe diff]
    H --> I[Run tests / checks / screenshots]
    I --> J[Write receipt]
    J --> K{Did implementation change graph?}
    K -->|No| L[Mark task complete]
    K -->|Yes| M[Classify graph delta]
    M --> N{Approved delta?}
    N -->|Yes| O[Update graph + authority hash]
    N -->|No| P[Pause for human approval]

flowchart TD
    A[ACDF v7 Failure Equation] --> B[Undefined Specification]
    A --> C[Stale Authority]
    A --> D[Unstructured Context]
    A --> E[Stale Sources]
    A --> F[Unverified Execution]
    B --> G[Agent guesses]
    C --> H[Agent follows old plan]
    D --> I[Agent burns context and drifts]
    E --> J[Agent implements obsolete truth]
    F --> K[Agent claims done without proof]
    G --> L[Rework]
    H --> L
    I --> L
    J --> L
    K --> L
    L --> M[ACDF v7 Countermeasure]
    M --> N[Reference Guide]
    M --> O[Authority Engine]
    M --> P[Mermaid Graph]
    M --> Q[Source Manifest]
    M --> R[Receipts]

---

## The Doctrine (load-bearing, keep in working memory)

A model may propose.
A graph must locate.
A manifest must date.
An authority file must bind.
A receipt must prove.

**Economic Doctrine:** Structure substitutes for scale. A well-specified task given to a cheap or free-tier model reliably outperforms an underspecified task given to an expensive frontier model.

**Where ACDF sits:** ACDF is for the cost-and-time-constrained solo builder or small team doing agentic code engineering (greenfield or legacy), as an alternative to the tokenmaxxing agent-loop ("long-running goals" / OODA loop) meta — not a replacement for it, and not aimed at vibe coding.

**The Ten No's** (full detail in `parts/03-plan-and-attack.md`): no TBD schemas, no implicit constants, no undefined thresholds, no vague edge cases, no hidden retry behavior, no unstated trust boundary, no unclear UX state, no ambiguous authority rule, no model output without contract, no phase requiring agent judgment about correctness.

---

## File Structure (diagram-first)

Every file under `parts/` is structured as: a **Diagram Map** (all Mermaid flowcharts for that file, grouped by chapter, near the top) followed by a **Narrative** section (all prose, in original order, with section headings intact for cross-reference).

This means an agent can read just the Diagram Map of a part file to get the structural shape of that Part's content — gates, doctrines, decision trees, hero-lens activation conditions — at a fraction of the token cost of the full file. Read the Narrative section only when the diagram alone doesn't resolve the question (e.g., exact PASS/FAIL wording for a gate, or the prose justification behind a doctrine).

For routing decisions ("which part do I need?"), the Diagram Map alone is usually sufficient. For implementation detail (writing a specific file, citing exact gate language), read the matching Narrative section.

---

## Routing Table — load on demand, not all at once

| When you are doing... | Load |
|---|---|
| Starting fresh: understanding the method, the failure equation, the six engines, hero lenses overview, economic rationale | `parts/01-orientation.md` |
| Stage 0-1: synthesizing sources, NotebookLM reference-guide loop, building the Approved Reference Guide | `parts/02-build-the-truth.md` |
| Stage 2-3: build plan, indexed task board, determinism map, adversarial review council, AI Credit Arbitrage, risk register | `parts/03-plan-and-attack.md` |
| Stage 4-8 (any): authority capsule, claims/collision control, drift pause protocol, graph delta classification, Auto-Approve Mode, **and** any specific stage runbook (0-8) | `parts/04-authority-and-stages.md` |
| Project archetype is data pipeline / AI-LLM app / frontend / creative / native-mobile / takeover-fork / Web3 — OR reusing a pattern (Level 5 Harness, Structured Output Compiler, Build Ledger, etc.) | `parts/05-overlays-and-patterns.md` |
| Choosing a governance mode (solo/standard/heavy/enterprise), or need the glossary / example repo structures / domain-expert Stage 0-1 guidance | `parts/06-governance-and-reference.md` |
| Asked specifically about ACDF's history, the UCC case study, external convergence, or the hero-lens activation hypothesis — NOT needed for execution | `parts/07-provenance.md` (optional, skip by default) |

**First-time setup for a new project:** load this file + `parts/01-orientation.md` + `parts/02-build-the-truth.md`, then proceed to Stage 0.

**Mid-build (authority.json already exists):** load this file + `parts/04-authority-and-stages.md` (for the relevant stage) + whichever of `02`/`03`/`05`/`06` the current task actually requires. Do not preload files you don't need for the current task — that is the Structure Problem this method exists to avoid.

---

## Part Index

| Part | Covers | File |
|---|---|---|
| I — Orientation | Core thesis, failure equation, six engines, v7 operating model, structure-first doctrine, hero lenses intro, economic doctrine | `parts/01-orientation.md` |
| II — Build the Truth | Source synthesis, NotebookLM SME loop, nine-question reference guide loop, approved reference guide | `parts/02-build-the-truth.md` |
| III — Turn Truth into Plan | Build plan, Plan Mode, indexed task board, determinism mapping, the Ten No's, gate design | `parts/03-plan-and-attack.md` |
| IV — Attack the Plan | Adversarial review, frontier model council, independence control, AI Credit Arbitrage, risk register | `parts/03-plan-and-attack.md` |
| V — Authority and Task Control | Truth layers, authority capsule, claims/collision, drift pause, graph delta classification, Auto-Approve Mode | `parts/04-authority-and-stages.md` |
| VI — The 0-8 Stage Workflow | Stage runbooks 0 through 8 | `parts/04-authority-and-stages.md` |
| VIII — Archetype Overlays | Frontend, creative/product, native/mobile, takeover/fork, Web3/protocol | `parts/05-overlays-and-patterns.md` |
| IX — Reusable Patterns | Level 5 Harness, Structured Output Compiler, Creative/Product Reference Guide pattern, AI App Failure Checklist, Build Ledger | `parts/05-overlays-and-patterns.md` |
| X — Governance Modes | Solo/standard/heavy/enterprise, orchestration bridge | `parts/06-governance-and-reference.md` |
| Appendix A-C | Glossary, example repo structures, domain-expert guidance | `parts/06-governance-and-reference.md` |
| Appendix D-E | External convergence, hero lens hypothesis, UCC case study (provenance — optional) | `parts/07-provenance.md` |

**Note:** Part VII (Agent Roles and Collaboration Protocol) and Part XII (Quick Reference and Templates) are referenced in this index but do not yet exist as written content in v7 — this is a known gap, not a packaging omission.
