# Word-Problem Schema Chain

This diagnostic chain helps Hermes test whether a current-grade word-problem issue may depend on an earlier schema. It is not a diagnosis by itself.

```mermaid
flowchart LR
  A["1.OA.1<br/>Add/subtract situations"] --> B["2.OA.1<br/>One/two-step additive problems"]
  B --> C["3.OA.3<br/>Multiply/divide situations"]
  C --> D["4.OA.2<br/>Multiplicative comparison"]
  C --> E["4.OA.3<br/>Multi-step four-operation problems"]
  D --> F["5.OA.2<br/>Write and interpret expressions"]
  E --> F
  F --> G["6.RP.3<br/>Ratio/rate problems"]
  G --> H["7.RP.2<br/>Proportional relationships"]
  H --> I["8.EE.5<br/>Slope as unit rate"]
  I --> J["HS modeling<br/>Context → model → interpretation"]
```

**Legend:** Arrows mean “inspect as a possible dependency,” not “must be mastered in this order.”
