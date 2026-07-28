# Textbook Creation Workflow

> How we turn a NotebookLM expert notebook into a 12-chapter interactive textbook with weekly delivery
> Covers: Math Council (Lockhart), STEM Heroes (Feynman), Parenting, Writing
> Last updated: 2026-07-06

---

## Value Proposition

```mermaid
graph LR
    A[NotebookLM Expert] --> B[Role Card]
    A --> C[12-Chapter Outline]
    C --> D[Weekly Chapter Drops]
    D --> E[Written Chapter<br/>~1,500 words]
    D --> F[Interactive Prompt<br/>AI Studio ready]
    E --> G[Complete Textbook<br/>12 weeks]
    F --> H[Interactive Explainer<br/>three.js + d3.js]
```

**One sentence:** Turn any world-class thinker's body of work into a structured, chapter-by-chapter interactive textbook — delivered one piece per week, with zero ongoing effort after setup.

### Why This Exists

| Problem | Solution |
|---------|----------|
| AI-generated content is shallow and generic | Each chapter is grounded in a specific thinker's actual source material from NotebookLM |
| Building a full textbook is overwhelming | 12 weeks, one chapter at a time, automated delivery |
| Kids need more than text — they need to play | Every chapter includes a prompt for an interactive 3D explainer |
| Each thinker's voice gets lost in generic tutoring | Role cards, lens files, and textbook maintain distinct pedagogical identity |
| Textbook creation is manual and fragile | Cron-driven, tracker-based, self-healing auth — set and forget |

---

## Jobs To Be Done (For Me / Alan)

```mermaid
graph TD
    JTBD["When I identify a world-class thinker<br/>I want to turn their knowledge into a<br/>structured teaching resource<br/>so that Aria and other kids can learn<br/>in that thinker's authentic voice"]

    JTBD --> J1["Capture their essence"]
    J1 --> J1a["Extract role card from NotebookLM"]
    J1a --> J1b["File: Learning_Coach_Heros/{Group}/{Thinker}_{Domain}_lens.md"]

    JTBD --> J2["Design the learning arc"]
    J2 --> J2a["12-chapter textbook outline from NotebookLM"]
    J2a --> J2b["Chapter → guiding question → key concepts → signature puzzle → check"]

    JTBD --> J3["Automate the delivery"]
    J3 --> J3a["Set _chapter_tracker.txt to 2"]
    J3a --> J3b["Create cron: one chapter per week"]
    J3b --> J3c["Every Monday or Friday at 6AM, a new chapter appears"]

    JTBD --> J4["Include the interactive layer"]
    J4 --> J4a["Each chapter generates an AI Studio prompt"]
    J4a --> J4b["Kid builds a 3D explainer from it"]
    J4a --> J4c["three.js + d3.js, no build tools"]

    JTBD --> J5["Keep it findable"]
    J5 --> J5a["Textbook folder in Learning_Coach_Heros/{Group}/{Thinker}_Textbook/"]
    J5a --> J5b["Outline + chapters + supplements + tracker"]
```

---

## Workflow Steps

```mermaid
flowchart TB
    START([Identify a thinker]) --> A[Search NotebookLM<br/>for existing notebook]
    A --> B{Notebook exists?}
    B -- No --> C[Create notebook<br/>add sources]
    B -- Yes --> D[Set context & query]

    D --> E[Step 1: Role Card]
    E --> E1["Ask 9 questions + council question"]
    E1 --> E2["Write {Thinker}_{Domain}_lens.md<br/>in Learning_Coach_Heros/{Group}/"]

    D --> F[Step 2: 12-Chapter Outline]
    F --> F1["Ask for 12-chapter outline<br/>in thinker's voice"]
    F1 --> F2["Write {Thinker}_12_Chapter_Textbook_Outline.md"]

    F --> G[Step 3: Textbook Folder]
    G --> G1["mkdir -p {Group}/{Thinker}_Textbook/"]
    G1 --> G2["Move outline into folder"]
    G1 --> G3["Write _chapter_tracker.txt = 2"]

    G --> H[Step 4: Write Chapter 1]
    H --> H1["Ask NotebookLM for<br/>20 questions + 3 quotes<br/>for Chapter 1"]
    H1 --> H2["Write Chapter_01_Title.md<br/>~1,500 words in thinker's voice"]
    H1 --> H3["Write Chapter_01_Supplement_Interactive_Prompt.md"]

    G --> I[Step 5: Set Cron]
    I --> I1{Feynman runs Monday<br/>Lockhart runs Friday}
    I1 --> I2["Create cron job:<br/>day + time + notebook<br/>+ workdir + skills"]
    I2 --> I3["Verify next_run_at"]

    H --> J[Step 6: Next Monday/Friday 6AM]
    J --> J1["Cron fires"]
    J1 --> J2["Read tracker → find chapter N"]
    J2 --> J3["Auth NotebookLM"]
    J3 --> J4["Get 20 questions + 3 quotes"]
    J4 --> J5["Write Chapter_N.md"]
    J4 --> J6["Write Chapter_N_Supplement.md"]
    J5 --> J7["Increment tracker"]
    J6 --> J7

    J7 --> K{Chapter N = 12?}
    K -- No --> J
    K -- Yes --> L[Done! 12 chapters complete]

    style L fill:#4a4,color:#fff
    style START fill:#66b,color:#fff
    style A fill:#66b,color:#fff
    style I fill:#fa3,color:#fff
```

---

## File Naming Convention

Every thinker textbook follows this exact structure:

```
Learning_Coach_Heros/
└── {Group}/
    └── {Thinker}_Textbook/
        ├── {Thinker}_12_Chapter_Textbook_Outline.md          # The full arc — written once
        ├── _chapter_tracker.txt                               # Current chapter number (integer)
        ├── Chapter_01_{Title}.md                              # Written chapter, ~1,500 words
        ├── Chapter_01_Supplement_Interactive_Prompt.md        # AI Studio prompt for 3D explainer
        ├── Chapter_02_{Title}.md                              # (cron delivers weekly)
        ├── Chapter_02_Supplement_Interactive_Prompt.md
        └── ...                                                # Through Chapter 12
```

### Current Real Examples

| Thinker | Group Folder | Textbook Path |
|---------|-------------|---------------|
| Feynman | STEM_Heroes/ | `Learning_Coach_Heros/STEM_Heroes/Feynman_Textbook/` |
| Lockhart | Math_Council/ | `Learning_Coach_Heros/Math_Council/Lockhart_Textbook/` |

### Naming Rules

| File | Convention | Example |
|------|-----------|---------|
| Outline | `{Thinker}_12_Chapter_Textbook_Outline.md` | `Feynman_12_Chapter_Textbook_Outline.md` |
| Tracker | `_chapter_tracker.txt` (always this name) | Contains integer `2` meaning "chapter 2 is next" |
| Chapter | `Chapter_{NN}_{ShortTitle}.md` | `Chapter_01_Atoms_in_Motion.md` |
| Supplement | `Chapter_{NN}_Supplement_Interactive_Prompt.md` | `Chapter_01_Supplement_Interactive_Prompt.md` |

---

## Cron Configuration

```mermaid
flowchart LR
    subgraph Monday 6AM
        FEYNMAN[feynman-textbook-monday]
    end
    subgraph Friday 6AM
        LOCKHART[lockhart-textbook-friday]
    end

    FEYNMAN --> FDIR[workdir: STEM_Heroes/Feynman_Textbook/]
    FEYNMAN --> FSKILL[skills: notebooklm]
    FEYNMAN --> FSCHED[cron: 0 6 * * 1]

    LOCKHART --> LDIR[workdir: Math_Council/Lockhart_Textbook/]
    LOCKHART --> LSKILL[skills: notebooklm]
    LOCKHART --> LSCHED[cron: 0 6 * * 5]
```

### Creating a New Cron

```bash
cronjob action=create \
  name="{thinker}-textbook-{day}" \
  schedule="0 6 * * {1=Mon,5=Fri}" \
  skills='["notebooklm"]' \
  workdir="/path/to/Learning_Coach_Heros/{Group}/{Thinker}_Textbook/"
```

The cron prompt must be self-contained (it runs with no conversation history) and must handle NotebookLM auth expiry by checking and logging in.

---

## The 12-Chapter Arc Pattern

Every textbook follows this progression:

```mermaid
graph LR
    C01[Ch 1<br/>Concrete] --> C02[Ch 2<br/>Patterns] --> C03[Ch 3<br/>Scaling] --> C04[Ch 4<br/>Inversions] --> C05[Ch 5<br/>Space] --> C06[Ch 6<br/>Stories]
    C06 --> C07[Ch 7<br/>Balance] --> C08[Ch 8<br/>Proof] --> C09[Ch 9<br/>Limits] --> C10[Ch 10<br/>3D] --> C11[Ch 11<br/>Infinity] --> C12[Ch 12<br/>Freedom]
```

| Phase | Chapters | What happens |
|-------|----------|-------------|
| **Foundation** | 1–4 | Concrete, tangible ideas (atoms, counting, grouping, fractions) |
| **Construction** | 5–8 | Building tools (geometry, equations, proof) |
| **Frontiers** | 9–12 | Abstract, surprising ideas (irrationals, infinity, complex numbers) |

Each chapter has the same internal structure:

```mermaid
flowchart LR
    Q[Guiding Question] --> C[Key Concepts<br/>3-5 ideas]
    C --> S[Signature Demo/Puzzle]
    S --> L[Thinker's Check]
    L --> E[8 Chapter Questions]
    E --> Q2[Source Quotes]
```

---

## What Each Chapter File Contains

```
# Chapter N: Title
> From: *Book Title*

--- [ hook ] ---
Opens with the Guiding Mystery or Question — the thing that makes you lean in.

--- [ body ] ---
3-5 key concepts explained in the thinker's voice using their signature
metaphors, analogies, and storytelling devices.

--- [ signature ] ---
The Signature Puzzle or Demonstration — the one thing that makes the
concept click. Described vividly enough to do at home.

--- [ check ] ---
The {Thinker} Check — a question the reader should be able to answer
in simple language to prove real understanding.

--- [ questions ] ---
8 Chapter Questions drawn from the NotebookLM 20 Socratic questions.

--- [ quotes ] ---
3 Source Quotes with attribution.

--- [ word count ] ---
~1,200-1,500 words total — about 6 pages.
```

---

## What Each Supplement Prompt Contains

```
# Chapter N Supplement: Interactive HTML Explainer
> Level: 9-year-old
> Tech: three.js + d3.js
> Prompt for: Google AI Studio

--- [ The Prompt ] ---
A single markdown code block labeled "## The Prompt" containing:

- DESIGN PHILOSOPHY (thinker's voice)
- 4-6 SCENES with specific interactions
- THREE.JS REQUIREMENTS (CDN, OrbitControls, lighting)
- D3.JS REQUIREMENTS (visualizations)
- UI/UX REQUIREMENTS (nav, character, responsiveness)
- THE 3 QUOTES to display at key moments

--- [ How to Use ] ---
Copy the prompt, paste into AI Studio, generate the HTML, save alongside chapter.

--- [ Learning Objectives Table ] ---
| Scene | Concept | Thinker's Metaphor |

--- [ Tech Stack Notes ] ---
CDN URLs for three.js, OrbitControls, d3.js
```

---

## Quick Start Checklist

When adding a new thinker:

- [ ] Find or create the NotebookLM notebook
- [ ] Ask 9 role-card questions → write `{Thinker}_{Domain}_lens.md` to `Learning_Coach_Heros/{Group}/`
- [ ] Ask 12-chapter outline → write `{Thinker}_12_Chapter_Textbook_Outline.md`
- [ ] Create `Learning_Coach_Heros/{Group}/{Thinker}_Textbook/` folder
- [ ] Move outline into folder
- [ ] Write `_chapter_tracker.txt = 2`
- [ ] Ask 20 questions + 3 quotes for Chapter 1
- [ ] Write `Chapter_01_Title.md`
- [ ] Write `Chapter_01_Supplement_Interactive_Prompt.md`
- [ ] Create cron job (Monday or Friday 6AM) with workdir pointing to the textbook folder
- [ ] Verify first cron fires at `next_run_at`

---

## Current Textbook Status

| Thinker | Group | Phase | Cron | Chapters Written | Next Chapter | Completion |
|---------|-------|-------|------|------------------|-------------|------------|
| **Feynman** | STEM_Heroes/ | Active | Mon 6AM | Ch 1 done | Ch 2 (July 13) | 1/12 |
| **Lockhart** | Math_Council/ | Active | Fri 6AM | Ch 1 done | Ch 2 (July 10) | 1/12 |
| Oakley | Math_Council/ | Not started | — | — | — | 0/12 |
| Loh | Math_Council/ | Not started | — | — | — | 0/12 |
| Zeitz | Math_Council/ | Not started | — | — | — | 0/12 |
| Feynman (full) | STEM_Heroes/ | Active | Mon 6AM | — | — | 1/12 |
| Lewin | STEM_Heroes/ | Not started | — | — | — | 0/12 |
| Mazur | STEM_Heroes/ | Not started | — | — | — | 0/12 |
| Veritasium | STEM_Heroes/ | Not started | — | — | — | 0/12 |
| 3Blue1Brown | STEM_Heroes/ | Not started | — | — | — | 0/12 |
| Mark Rober | STEM_Heroes/ | Not started | — | — | — | 0/12 |
