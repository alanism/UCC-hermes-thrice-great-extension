# Sample Science Learner Heat Map

> **Fictional sample only — not real learner data.** This is an ad hoc diagnostic artifact, not core app UI.

```mermaid
flowchart LR
  A["3-PS2-1<br/>Forces investigation"] --> B["4-LS1-1<br/>Structure/function argument"]
  B --> C["5-LS2-1<br/>Matter movement in ecosystems"]
  C --> D["MS-LS1-1<br/>Cells evidence"]
  A --> E["MS-PS2-2<br/>Force/mass/motion investigation"]
  D --> F["HS-LS1-1<br/>DNA/protein explanation"]

  classDef mastered fill:#d6f5d6,stroke:#2e7d32,color:#111
  classDef learning fill:#fff4cc,stroke:#b8860b,color:#111
  classDef weak fill:#ffd6d6,stroke:#b71c1c,color:#111
  classDef noEvidence fill:#eeeeee,stroke:#777,color:#111
  classDef advanced fill:#dbeafe,stroke:#1d4ed8,color:#111

  class A mastered
  class B learning
  class C learning
  class D weak
  class E noEvidence
  class F advanced
```

**Legend:** green = mastered; yellow = learning; red = foundational-repair candidate; gray = needs evidence; blue = advanced. Use only actual overlay evidence for real learners.
