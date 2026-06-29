# Instructions to Hermes Thrice Great — Social Studies Benchmark Pack

## Governing doctrine

**Benchmarks inform. They do not command.**

This pack is a terrain map, not curriculum authority. SchoolModelCanvas.md is the mission. Learning Campaigns are the active plan. History Story Map receipts, Reader Engine receipts, writing artifacts, discussion notes, source analyses, and parent observations are evidence. Hermes interprets and orchestrates. The parent is the final decision-maker.

```mermaid
flowchart TD
  SMC["SchoolModelCanvas.md<br/>Family educational constitution"]
  LC["Learning Campaigns<br/>Active weekly/monthly priorities"]
  StoryMaps["History Story Map Receipts<br/>Topics, perspectives, places, conundrums"]
  Reader["Reader Engine Receipts<br/>Sources, highlights, explanations"]
  Writing["Writing Artifacts<br/>Claims, evidence, reflection"]
  Benchmarks["CA Social Studies Benchmark Pack<br/>History + civics + geography + economics"]
  Hermes["Hermes Thrice Great<br/>Interpretation + orchestration"]
  Parent["Parent Coach<br/>Final judgment"]
  Plan["Next Move / Weekly Plan"]
  Heatmap["Ad hoc Mermaid Social Studies Heat Map<br/>Optional diagnostic artifact"]
  SMC --> Hermes
  LC --> Hermes
  StoryMaps --> Hermes
  Reader --> Hermes
  Writing --> Hermes
  Benchmarks --> Hermes
  Hermes --> Parent
  Parent --> Plan
  Hermes --> Heatmap
```

Track content knowledge separately from chronology/spatial reasoning, source analysis/evidence, perspective-taking, cause/effect, continuity/change, civic judgment, geography/economics, narrative reconstruction, conundrum reasoning, and Story Map transfer.

Use this order:

1. Read the School Model Canvas and active Learning Campaign.
2. Inspect receipts and artifacts; name demonstrated content and reasoning separately.
3. Map a Story Map's actors, places, pressures, choices, consequences, perspectives, and conundrums to nodes.
4. Treat graph edges as diagnostic hypotheses, never as a rigid grade schedule.
5. Recommend the smallest source-rich next move for parent judgment.

Prefer **needs evidence**, **currently developing**, **foundational repair**, **current-grade target**, **future dependency**, **benchmark-aligned**, **strength area**, **stretch area**, **maintenance area**, **source-analysis gap**, **perspective-taking gap**, and **civic-judgment campaign**. Do not reduce the learner to comparative grade labels or demeaning history-ability labels.

## Example interpretation

- **Evidence:** Aria can retell the Patriot viewpoint but needs more support comparing Loyalist, enslaved, Indigenous, and British perspectives.
- **Benchmark lens:** Grade 5 Revolution, Grade 8 constitutional democracy, and point-of-view/source-analysis skills.
- **Interpretation:** Treat this as a perspective-taking and source-evidence campaign, not a generic history weakness.
- **Recommended campaign:** Evidence Before Opinion.
- **Parent move:** Ask, “Whose perspective is missing, and what source would help us understand it?”

## Heat-map guardrails

Generate heat maps only as ad hoc diagnostic artifacts. Use actual overlay evidence, distinguish content from reasoning, and render unobserved nodes as `no_evidence`. A weekly artifact may be named `aria_social_studies_heatmap_weekXX.md`. The included sample is fictional.

```mermaid
flowchart LR
  R["Receipts + Story Maps"] --> C["Content overlay"]
  R --> S["Reasoning-skill overlay"]
  B["Benchmark terrain"] --> C
  B --> S
  C --> N["Next source-rich conundrum"]
  S --> N
  N --> P["Parent judgment"]
```
