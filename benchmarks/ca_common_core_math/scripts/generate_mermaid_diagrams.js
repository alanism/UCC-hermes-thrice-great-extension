#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const OUTPUT_FOLDER = path.resolve(__dirname, '..', 'mermaid');

const diagrams = {
  'progression_spine.md': `# California Common Core Math Progression Spine

This is a broad grade-equivalence reference map, not a required learning schedule.

\`\`\`mermaid
flowchart TD
  KG["KG: Counting, cardinality, early number sense"]
  G1["Grade 1: Add/subtract schemas within 20"]
  G2["Grade 2: One/two-step word problems; fluency within 20"]
  G3["Grade 3: Multiplication/division; arrays; fractions"]
  G4["Grade 4: Multi-step operations; multiplicative comparison; fractions"]
  G5["Grade 5: Expressions; decimals; fraction operations; volume"]
  G6["Grade 6: Ratios; rates; fraction division; rational numbers"]
  G7["Grade 7: Proportional relationships; rational operations; percent"]
  G8["Grade 8: Linear equations; functions; irrational numbers; Pythagorean theorem"]
  HS["High School: Algebra; functions; modeling; geometry; statistics"]
  KG --> G1 --> G2 --> G3 --> G4 --> G5 --> G6 --> G7 --> G8 --> HS
\`\`\`

**Legend:** Arrows preserve the official grade sequence as reference terrain; they do not command an individual learner's path.
`,

  'operations_algebraic_thinking.md': `# Operations and Algebraic Thinking Progression

Selected K–5 nodes show how operation meanings, fluency, schemas, and expressions develop.

\`\`\`mermaid
flowchart TD
  K["K foundations: counting, cardinality, operation situations"]
  K --> OA11["1.OA.1: Add/subtract word-problem schemas"]
  OA11 --> OA16["1.OA.6: Add/subtract fluency within 20"]
  OA11 --> OA21["2.OA.1: One- and two-step word problems"]
  OA16 --> OA22["2.OA.2: Fluency within 20"]
  OA22 --> OA24["2.OA.4: Arrays as repeated addition"]
  OA24 --> OA31["3.OA.1: Interpret products"]
  OA31 --> OA32["3.OA.2: Interpret quotients"]
  OA32 --> OA33["3.OA.3: Multiplication/division word problems"]
  OA33 --> OA37["3.OA.7: Fluency within 100"]
  OA33 --> OA42["4.OA.2: Multiplicative comparison"]
  OA42 --> OA43["4.OA.3: Multi-step problems"]
  OA37 --> OA44["4.OA.4: Factors and multiples"]
  OA43 --> OA51["5.OA.1: Grouping symbols"]
  OA51 --> OA52["5.OA.2: Write and interpret expressions"]
  OA52 --> OA53["5.OA.3: Numerical patterns"]
\`\`\`

**Legend:** Solid arrows are selected progression hypotheses for diagnosis. Consult ontology edges and receipts before using them in a campaign.
`,

  'word_problem_schema_chain.md': `# Word-Problem Schema Chain

This diagnostic chain helps Hermes test whether a current-grade word-problem issue may depend on an earlier schema. It is not a diagnosis by itself.

\`\`\`mermaid
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
\`\`\`

**Legend:** Arrows mean “inspect as a possible dependency,” not “must be mastered in this order.”
`,

  'fractions_to_ratios_to_functions.md': `# Fractions to Ratios to Functions

This map highlights a conceptual route from partitioning to proportional and functional reasoning.

\`\`\`mermaid
flowchart LR
  P["Early partitioning<br/>equal shares and wholes"] --> G3["Grade 3 fractions<br/>number-line magnitude and equivalence"]
  G3 --> G4["Grade 4 fractions<br/>equivalence and operations"]
  G4 --> G5["Grade 5<br/>fraction operations and decimals"]
  G5 --> G6["Grade 6<br/>ratios and rates"]
  G6 --> G7["Grade 7<br/>proportional relationships"]
  G7 --> G8["Grade 8<br/>slope and linear functions"]
  G8 --> HS["High School<br/>functions and modeling"]
\`\`\`

**Legend:** Nodes summarize benchmark terrain; learner evidence may be uneven or nonlinear across the route.
`,

  'ratios_to_linear_functions.md': `# Ratios to Linear Functions

Selected domains connect unit-rate reasoning to slope, equations, and functions.

\`\`\`mermaid
flowchart LR
  RP6["6.RP<br/>Ratios and rates"] --> RP7["7.RP<br/>Proportional relationships"]
  RP7 --> EE8["8.EE<br/>Slope and linear equations"]
  EE8 --> F8["8.F<br/>Functions"]
  F8 --> HSF["HS F-IF / F-LE<br/>Functions and modeling"]
\`\`\`

**Legend:** Domain-level arrows are editable prerequisite hypotheses, not learner labels.
`,

  'geometry_progression.md': `# Geometry Progression

The geometry spine preserves grade-equivalence landmarks while allowing nonlinear evidence.

\`\`\`mermaid
flowchart TD
  K["K: Shapes"] --> G1["Grade 1: Attributes, composition, partitioning"]
  G1 --> G2["Grade 2: Shapes, arrays, area foundations"]
  G2 --> G3["Grade 3: Area, perimeter, partitioned shapes"]
  G3 --> G4["Grade 4: Angles, lines, shape classification"]
  G4 --> G5["Grade 5: Coordinate plane and volume"]
  G5 --> G6["Grade 6: Area, surface area, volume"]
  G6 --> G7["Grade 7: Scale drawings, circles, area, volume"]
  G7 --> G8["Grade 8: Transformations and Pythagorean theorem"]
  G8 --> HS["High School: Congruence, similarity, proof, coordinates, modeling"]
\`\`\`

**Legend:** Each arrow marks neighboring benchmark terrain; use receipts to determine the learner's actual starting point.
`,

  'data_statistics_progression.md': `# Data, Statistics, and Probability Progression

The data spine moves from representations toward inference and modeling.

\`\`\`mermaid
flowchart TD
  G1["Grade 1: Picture/tally/data tables"] --> G2["Grade 2: Line plots and bar graphs"]
  G2 --> G3["Grade 3: Scaled graphs"]
  G3 --> G4["Grade 4: Measurement data and line plots"]
  G4 --> G5["Grade 5: Coordinate graphing"]
  G5 --> G6["Grade 6: Statistical distributions"]
  G6 --> G7["Grade 7: Sampling, probability, statistics"]
  G7 --> G8["Grade 8: Scatter plots and lines of best fit"]
  G8 --> HS["High School: Statistics, probability, inference, modeling"]
\`\`\`

**Legend:** These are broad grade references; not every source grade uses the same domain label.
`,

  'sample_learner_heatmap.md': `# Sample Learner Heat Map

> **Fictional sample only — not real learner data.** This demonstrates an ad hoc diagnostic overlay and is not core app UI.

\`\`\`mermaid
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
\`\`\`

**Legend:** green = mastered; yellow = learning; red = weak/foundational repair candidate; gray = needs evidence; blue = advanced. Status must come from overlay evidence, never from this sample.
`,
};

function main() {
  fs.mkdirSync(OUTPUT_FOLDER, { recursive: true });
  for (const [filename, contents] of Object.entries(diagrams).sort(([a], [b]) => a.localeCompare(b))) {
    fs.writeFileSync(path.join(OUTPUT_FOLDER, filename), contents.endsWith('\n') ? contents : `${contents}\n`, 'utf8');
  }
  console.log(`Generated ${Object.keys(diagrams).length} Mermaid documents.`);
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(`Diagram generation failed: ${error.message}`);
    process.exitCode = 1;
  }
}

