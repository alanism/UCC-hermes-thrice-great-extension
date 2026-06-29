# Sample ELA Learner Heat Map

> **Fictional sample only — not real learner data.** This is an ad hoc diagnostic example, not core app UI.

```mermaid
flowchart LR
  A["3.PI.3.6<br/>Reading closely"] --> B["4.PI.4.6<br/>Reading closely"]
  B --> C["4.PI.4.10<br/>Writing texts"]
  B --> D["5.PI.5.7<br/>Evaluating support"]
  D --> E["6.PI.6.7<br/>Argument and evidence"]
  E --> F["7.PI.7.3<br/>Claims and negotiation"]
  F --> G["8.PI.8.10<br/>Writing with evidence"]

  classDef mastered fill:#d6f5d6,stroke:#2e7d32,color:#111
  classDef learning fill:#fff4cc,stroke:#b8860b,color:#111
  classDef weak fill:#ffd6d6,stroke:#b71c1c,color:#111
  classDef noEvidence fill:#eeeeee,stroke:#777,color:#111
  classDef advanced fill:#dbeafe,stroke:#1d4ed8,color:#111

  class A mastered
  class B mastered
  class C learning
  class D learning
  class E weak
  class F noEvidence
  class G advanced
```

**Legend:** green = mastered; yellow = learning; red = foundational-repair candidate; gray = needs evidence; blue = advanced. Status must come from actual overlay evidence.
