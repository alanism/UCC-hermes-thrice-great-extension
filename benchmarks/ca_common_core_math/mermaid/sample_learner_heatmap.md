# Sample Learner Heat Map

> **Fictional sample only — not real learner data.** This demonstrates an ad hoc diagnostic overlay and is not core app UI.

```mermaid
flowchart LR
  A["1.OA.1"] --> B["2.OA.1"] --> C["3.OA.3"]
  C --> D["4.OA.2"]
  C --> E["4.OA.3"]
  D --> F["5.OA.2"]
  E --> F

  classDef mastered fill:#d6f5d6,stroke:#2e7d32,color:#111
  classDef learning fill:#fff4cc,stroke:#b8860b,color:#111
  classDef weak fill:#ffd6d6,stroke:#b71c1c,color:#111
  classDef noEvidence fill:#eeeeee,stroke:#777,color:#111
  classDef advanced fill:#dbeafe,stroke:#1d4ed8,color:#111

  class A mastered
  class B weak
  class C learning
  class D noEvidence
  class E noEvidence
  class F advanced
```

**Legend:** green = mastered; yellow = learning; red = weak/foundational repair candidate; gray = needs evidence; blue = advanced. Status must come from overlay evidence, never from this sample.
