# Macro-Meso-Micro Loop

> How the **Hermes Thrice Great** agent (individual name: **Thoth**) orchestrates a family's learning system across three layers — constitution, campaign, and evidence — connected through a private Discord server.

---

## 1. The Three-Layer Architecture

```mermaid
flowchart TD
    subgraph "MACRO — School Model Canvas"
        M1["Educational constitution"]
        M2["Values: mentor/apprentice, agency, demonstration"]
        M3["Frequency: reviewed quarterly, changed only by parent"]
        M4["File: UCC-SMC-<learner>-<date>.md"]
    end

    subgraph "MESO — Learning Campaign OS"
        E1["Weekly campaign plans"]
        E2["CA Common Core benchmark anchoring"]
        E3["Grade-level equivalence mapping"]
        E4["5-step workflow: Setup → Campaigns → Evidence → Hermes → Overlay"]
        E5["Files: weekly-plans/aria-wkXX-*.json"]
    end

    subgraph "MICRO — Assessment Lab Telemetry"
        I1["CALM mode: untimed, deliberate"]
        I2["PRESSURE mode: timed, cognition-under-pressure"]
        I3["Structured receipts with item-level evidence"]
        I4["Error taxonomy: operation_mismatch, timeout, conceptual"]
        I5["Files: assets/telemetry/YYYY-MM-DD-*-CALM.txt"]
    end

    subgraph "COMMS — Discord"
        D1["#parent-agent: briefs, diagnoses, evidence-labeled summaries"]
        D2["#student-tasks: one clear task for the learner"]
        D3["#tutor-student: Socratic help (free response)"]
        D4["#receipts: telemetry uploads + status"]
        D5["#weekly-plan: the week's campaign plan"]
        D6["#admin-support: system health, troubleshooting"]
    end

    M1 -->|"constitution constrains"| E1
    E1 -->|"plan defines moves"| I1
    I1 -->|"telemetry informs"| E1
    E1 -->|"plan delivered via"| D5
    I1 -->|"receipts uploaded to"| D4
    M1 -->|"values shape"| D2
```

**Macro** = the constitution. Changes rarely. Set by the parent.

**Meso** = the campaign. Changes weekly. Designed by the agent, approved by the parent.

**Micro** = the evidence. Changes daily. Produced by the learner, interpreted by the agent.

**Comms** = the connective tissue. Every layer communicates through Discord channels.

---

## 2. The Core Loop

```mermaid
flowchart LR
    subgraph "Week N"
        A["SMC: constitution"] --> B["Campaign OS: build plan"]
        B --> C["Discord: deliver to parent + learner"]
        C --> D["Assessment Lab: CALM + PRESSURE"]
        D --> E["Telemetry: structured receipt"]
        E --> F["Discord: receipt uploaded to #receipts"]
        F --> G["Thoth: diagnose + adjust"]
        G --> B
    end

    subgraph "Outputs"
        H["SMC update (quarterly)"]
        I["Campaign JSON (weekly)"]
        J["Kanban task (per campaign)"]
        K["Parent brief (per assessment)"]
    end

    G --> H
    G --> I
    G --> J
    G --> K
```

Each week: plan → execute → assess → diagnose → adjust. The loop runs at the speed of one week.

---

## 3. File System Layout

```
Aria-EdTech/
│
├── UCC-SMC-Aria-2026-06-07.md          ← MACRO: the constitution
│
├── weekly-plans/                        ← MESO: campaign plans
│   ├── aria-wk01-fractions-decimals.json
│   ├── aria-wk02-weathering-erosion.json
│   ├── aria-wk03-california-geography.json
│   ├── aria-wk04-ela-opinion-text.json
│   ├── aria-wk05-multi-digit-multiplication.json
│   ├── aria-wk06-energy-waves.json
│   └── aria-wk07-wrapup-catchup.json
│
├── assets/telemetry/                    ← MICRO: assessment evidence
│   ├── 2026-06-25-algebra-readiness-aria-CALM.txt
│   └── 2026-06-25-algebra-readiness-aria-PRESSURE.txt
│
├── benchmarks/                          ← CA Common Core reference terrain
│   ├── ca_common_core_math/
│   ├── ca_common_core_ela/
│   ├── ca_science/
│   └── ca_social_studies/
│       ├── ontology/standards_nodes.json
│       ├── ontology/prerequisite_edges.json
│       └── markdown/grade_4.md
│
├── ucc-sprint-fable/                    ← App source + schemas
│   └── schemas/
│       ├── weekly_campaign_plan.schema.json
│       ├── receipt.schema.json
│       └── hermes_task_card.schema.json
│
├── UCC_learning_campaign_suggested_updates.md
│
└── docs/
    ├── runbook.md
    └── owners_manual.md
```

---

## 4. How the School Model Canvas Works (Macro)

```mermaid
flowchart TD
    subgraph "What the SMC Contains"
        S1["Teaching approach: collaborative, mentor/apprentice"]
        S2["Pacing: cyclic, with pre-grade transition periods"]
        S3["Measurement: demonstration over completion"]
        S4["Confidence: competence builds confidence + moonshots"]
        S5["Family beliefs: agency, experimental, internal motivation"]
        S6["Environment: hands-on, ambient, deep-dive"]
        S7["Tech: pure tool, balanced, AI as tutor"]
    end

    subgraph "How the Agent Uses It"
        T1["Pre-flight check before every kanban task"]
        T2["Phase detection: skill-building vs familiarity vs break"]
        T3["Campaign field: schoolModelCanvasAlignment"]
        T4["Filter: reject any action that conflicts with values"]
    end

    subgraph "How the Parent Updates It"
        P1["Reviewed quarterly or when values shift"]
        P2["One-line amendments for seasonal strategy"]
        P3["Exported date tracks freshness"]
    end

    S1 --> T1
    S2 --> T2
    S3 --> T3
    S4 --> T4
    P1 --> S1
    P2 --> S2
```

**The SMC is not a plan. It is a decision filter.** Every campaign, every kanban task, every assessment mode is checked against it before execution.

---

## 5. How the Learning Campaign OS Works (Meso)

```mermaid
flowchart LR
    subgraph "5-Step App Workflow"
        A["01 Setup"] --> B["02 Campaigns"]
        B --> C["03 Evidence"]
        C --> D["04 Hermes"]
        D --> E["05 Overlay"]
    end

    subgraph "What Each Step Does"
        F["Set learner, dates, canvas ID, theme, receipts"]
        G["Choose 1–3 campaigns, edit fields, link benchmarks"]
        H["Review source context, campaign reasoning, audit"]
        I["Parent dialogue cards + receipt buttons"]
        J["Delivery preview + parent override + mermaid heatmap"]
    end

    A --> F
    B --> G
    C --> H
    D --> I
    E --> J
```

### California Common Core Anchoring

```mermaid
flowchart LR
    subgraph "Benchmark Packs (Reference Only)"
        B1["Math — 479 nodes, 193 edges, KG–HS"]
        B2["ELA — spiraling PI/PII capabilities"]
        B3["Science — 17 performance expectations at G4"]
        B4["Social Studies — historical reasoning + civic judgment"]
    end

    subgraph "How the Agent Uses Them"
        U1["Search by standard code: 4.NF.1"]
        U2["Link to campaign: benchmarkAlignment.relatedStandards"]
        U3["Set role: reference_only / diagnostic_map / reentry_readiness"]
        U4["Interpret in parent language: not a score, not a label"]
    end

    subgraph "Grade-Equivalence Mapping"
        G1["Raw telemetry → grade level by item"]
        G2["Example: 10/16 correct, max difficulty G6"]
        G3["Conclusion: schema selection at G3–G4, computation at G5+"]
        G4["Translated to campaign: exposure, not remediation"]
    end

    B1 --> U1
    U2 --> G1
    G3 --> G4
```

**Benchmarks inform. They do not command.** The packs are reference terrain — they tell the agent which grade-level concepts exist, but the SMC decides whether and how to pursue them.

---

## 6. How the Assessment Lab Works (Micro)

```mermaid
flowchart TD
    subgraph "Dual-Mode Assessment"
        A["CALM mode (10 min)"]
        B["PRESSURE mode (5 min)"]
        A -->|"untimed, deliberate"| C["Item-level telemetry"]
        B -->|"timed, cognition-under-pressure"| C
    end

    subgraph "What the Receipt Contains"
        C --> D["session_seed, mode, duration"]
        C --> E["16 items with grade_level, is_correct, response_time_ms"]
        C --> F["error_type: conceptual / procedural / attentional / timeout"]
        C --> G["response_pattern: correct / operation_mismatch / timeout"]
        C --> H["failure_stage: plan / work / check"]
        C --> I["cognitive_pipeline_scores: story, plan, work, check"]
    end

    subgraph "How the Agent Diagnoses"
        D --> J["Extract accuracy, max difficulty, error distribution"]
        E --> J
        F --> K["Cluster errors by type"]
        G --> K
        H --> L["Identify failure stage (plan vs work)"]
        I --> L
        J --> M["Example diagnosis: all errors are operation_mismatch at plan stage"]
        K --> M
        L --> M
        M --> N["Conclusion: schema recognition, not computation"]
        N --> O["Campaign adjustment: exposure over remediation"]
    end

    subgraph "Pressure Delta"
        P["CALM accuracy − PRESSURE accuracy = pressure fragility"]
        P --> Q["0.625 − 0.667 = −0.042 → stable under pressure"]
        P --> R["High delta → build calm mastery before adding time pressure"]
    end
```

**The pressure delta is the single most informative metric.** A large gap between CALM and PRESSURE accuracy means the learner knows the material but can't access it under time stress. A zero or negative gap means the bottleneck is elsewhere (in Aria's case: schema selection, not pressure).

---

## 7. The Full Weekly Workflow

```mermaid
flowchart TD
    %% Phase 1: Plan
    A["Sunday: Agent reads SMC"] --> B["Agent checks current phase"]
    B --> C["Agent builds campaign JSON"]
    C --> D["Parent imports into Campaign OS app"]
    D --> E["Pedagogy audit passes"]
    E --> F["Plan delivered to #weekly-plan"]

    %% Phase 2: Execute
    F --> G["Tuesday: Parent delivers tiny move"]
    G --> H["Parent logs outcome in Hermes tab"]
    H --> I{"Button pressed?"}
    I -->|"Skipped"| J["Kanban: blocked — didn't come up"]
    I -->|"Said it"| K["Kanban: comment — parent delivered"]
    I -->|"She noticed"| L["Kanban: 80% toward done"]
    I -->|"She asked"| M["Kanban: mastery gate met"]

    %% Phase 3: Assess
    J --> N["Thursday: CALM assessment"]
    K --> N
    L --> N
    M --> N
    N --> O["Receipt uploaded to #receipts"]
    O --> P["Agent diagnoses telemetry"]

    %% Phase 4: Adjust
    P --> Q{"Week complete?"}
    Q -->|"Yes"| R["Agent writes end-of-week brief"]
    Q -->|"No"| G
    R --> S["Parent reviews brief"]
    S --> T{"Campaign goals met?"}
    T -->|"Yes"| U["Close campaign. Start next."]
    T -->|"No"| V["Adjust hypothesis. Extend or pivot."]
    U --> A
    V --> A
```

---

## 8. How Thoth (the Agent) Fits

```mermaid
flowchart LR
    subgraph "Thoth's Tools"
        T1["Read/write files in Aria-EdTech/"]
        T2["Interact with Campaign OS app (browser)"]
        T3["Kanban board (aria-projects)"]
        T4["Discord (send + receive via gateway)"]
        T5["Benchmark ontologies (search + reference)"]
        T6["Schema validation (JSON Schema draft-07)"]
    end

    subgraph "What Thoth Cannot Do"
        X1["Change the SMC — parent only"]
        X2["Approve own proposals — parent reviews"]
        X3["Declare a child 'behind' — no score labels"]
        X4["Write to the public app — local companion only"]
        X5["Access learner data outside synced directory"]
    end

    subgraph "Outputs Thoth Produces"
        Y1["Weekly campaign JSON → app"]
        Y2["Kanban tasks → board"]
        Y3["Assessment diagnoses → #parent-agent"]
        Y4["Campaign briefs → #weekly-plan"]
        Y5["SMC amendment suggestions → parent"]
    end

    T1 --> Y1
    T2 --> Y1
    T3 --> Y2
    T4 --> Y3
    T4 --> Y4
    T5 --> Y1
    T6 --> Y1
```

**Thoth is an orchestrator and interpreter — not the final authority.** The parent reviews, accepts, rejects, or overrides every proposal. The agent's power is in pattern recognition (spotting the operation_mismatch cluster across 16 items) and translation (turning 500 lines of telemetry JSON into a one-sentence campaign hypothesis).

---

## 9. Communication Through Discord

```mermaid
flowchart TD
    subgraph "Channel Architecture"
        C1["#parent-agent"]
        C2["#student-tasks"]
        C3["#tutor-student"]
        C4["#receipts"]
        C5["#weekly-plan"]
        C6["#admin-support"]
    end

    subgraph "Message Types"
        M1["Diagnosis briefs with M/C/Mod/F/N labels"]
        M2["One clear task, short + kind"]
        M3["Socratic questions, never answers"]
        M4["Status confirmations + next steps"]
        M5["Structured weekly plan"]
        M6["System health reports"]
    end

    subgraph "Flow"
        F1["Thoth → #parent-agent: 'CALM 0.625, all errors operation_mismatch'"]
        F2["Thoth → #student-tasks: 'Try pointing at a price tag today'"]
        F3["Aria → #tutor-student: 'I don't get this problem'"]
        F4["Thoth → #tutor-student: 'What kind of problem is this — total, groups, or comparison?'"]
        F5["Parent → #receipts: telemetry file upload"]
        F6["Thoth → #weekly-plan: full campaign plan link"]
    end

    C1 --> M1
    C2 --> M2
    C3 --> M3
    C4 --> M4
    C5 --> M5
    C6 --> M6

    M1 --> F1
    M2 --> F2
    M3 --> F3
    M3 --> F4
    M4 --> F5
    M5 --> F6
```

### Channel Roles

| Channel | Speaker → Listener | Tone | @mention Required? |
|---------|-------------------|------|-------------------|
| #parent-agent | Thoth → Parent | Evidence-labeled, calm, unsentimental | Yes |
| #student-tasks | Thoth → Learner | Short, warm, one task at a time | Yes |
| #tutor-student | Learner ↔ Thoth | Socratic, questions-only | No (free response) |
| #receipts | Any → Thoth | Status + next step | No (free response) |
| #weekly-plan | Thoth → All | Structured plan format | Yes |
| #admin-support | Thoth → Parent | Technical, tables | Yes |

---

## 10. Summary: What a New Family Needs to Replicate

To set up their own Hermes Thrice Great agent with the same system:

| Component | What They Need | Provided By |
|-----------|---------------|-------------|
| **Agent** | Hermes-compatible AI runtime | Hermes Agent (open source) |
| **Agent identity** | Name their agent (e.g., Thoth) | They choose |
| **SMC** | `UCC-SMC-<learner>-<date>.md` | Template from UCC |
| **Campaign OS** | Deployed app + optional local companion | UCC deployment (Cloud Run) |
| **Benchmarks** | CA Common Core packs (or their state's) | UCC provides CA packs; they can swap |
| **Assessment Lab** | UCC assessment app or their own | UCC provides or they build |
| **Discord** | Private server with channel structure | They create; we document role mapping |
| **Kanban** | Hermes kanban board | Built into Hermes CLI |
| **File store** | Local or synced directory (OneDrive, etc.) | They choose |

### Minimal File Set to Start

```
<learner>-edtech/
├── UCC-SMC-<learner>-<date>.md           ← Must create first
├── weekly-plans/                          ← Agent creates weekly
├── assets/telemetry/                      ← Assessment receipts land here
├── benchmarks/                            ← Provided by UCC
└── docs/
    ├── owners_manual.md
    └── runbook.md
```

---

## 11. Quick Reference: The Loop in One Diagram

```mermaid
flowchart TD
    MACRO["MACRO: School Model Canvas"] -->|"constitution"| MESO
    subgraph MESO["MESO: Campaign OS (weekly)"]
        PLAN["Build campaign JSON"] --> APP["Import to app"]
        APP --> DELIVER["Deliver via Discord"]
        DELIVER --> EXECUTE["Parent + learner execute"]
    end
    EXECUTE -->|"telemetry"| MICRO
    subgraph MICRO["MICRO: Assessment Lab"]
        CALM["CALM round (10 min)"] --> RECEIPT["Structured receipt"]
        PRESSURE["PRESSURE round (5 min)"] --> RECEIPT
        RECEIPT --> DIAGNOSE["Agent diagnoses"]
    end
    DIAGNOSE -->|"adjustment"| PLAN
    DIAGNOSE -->|"brief"| PARENT_BRIEF["#parent-agent brief"]
    DIAGNOSE -->|"kanban"| KANBAN["Kanban task update"]
    
    MACRO -.->|"pre-flight check"| KANBAN
```

**Three layers, one loop, one week at a time.**
