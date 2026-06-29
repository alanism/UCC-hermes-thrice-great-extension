#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const OUTPUT_FOLDER = path.resolve(__dirname, '..', 'mermaid');

const diagrams = {
  'progression_spine.md': `# California Social Studies Progression Spine

This grade-equivalence view is reference terrain, not a mandated historical sequence.

\`\`\`mermaid
flowchart TD
  G1["Grade 1: Citizenship, maps, symbols, traditions, community, continuity/change"]
  G2["Grade 2: Family history, sources, maps, government, economics, biographies"]
  G3["Grade 3: Local geography, Indigenous communities, local history, government, economy"]
  G4["Grade 4: California geography/history, Gold Rush, immigration, government"]
  G5["Grade 5: Pre-Columbian peoples, exploration, colonization, Revolution"]
  G6["Grade 6: Ancient civilizations, chronology, geography, source analysis"]
  G7["Grade 7: Medieval/early modern world, religions, empires, trade, Renaissance"]
  G8["Grade 8: U.S. founding, Constitution, expansion, slavery, Civil War"]
  HS["High School: Democracy, rights, civil society, branches, courts, elections, media"]
  G1 --> G2 --> G3 --> G4 --> G5 --> G6 --> G7 --> G8 --> HS
\`\`\`

**Legend:** Arrows preserve grade-reference order only; content and reasoning may develop nonlinearly.
`,
  'historical_reasoning_progression.md': `# Historical Reasoning Progression

Historical reasoning develops through recurring work with time, context, causality, continuity, and evidence.

\`\`\`mermaid
flowchart LR
  A["Then and now"] --> B["Timeline and sequence"] --> C["Local history and context"]
  C --> D["Source analysis"] --> E["Cause and effect"] --> F["Continuity and change"]
  F --> G["Competing interpretations"] --> H["Argument from evidence"]
\`\`\`

**Legend:** This is a reasoning repertoire, not a one-way mastery ladder.
`,
  'geography_mapping_progression.md': `# Geography and Mapping Progression

Spatial reasoning links place, movement, environment, settlement, conflict, and exchange.

\`\`\`mermaid
flowchart LR
  A["Community maps"] --> B["Letter-number grids"] --> C["Continents and oceans"]
  C --> D["California regions"] --> E["Exploration routes"] --> F["Ancient civilizations"]
  F --> G["Migration, empires, and trade"] --> H["Global political geography"]
\`\`\`

**Legend:** Map evidence should connect location to historical explanation, not stop at labeling.
`,
  'source_analysis_progression.md': `# Source Analysis Progression

Source work grows from family evidence toward credibility, context, interpretation, and civic/legal analysis.

\`\`\`mermaid
flowchart LR
  A["Artifacts, photos, interviews"] --> B["Primary and secondary sources"]
  B --> C["Fact and opinion"] --> D["Credibility and relevance"]
  D --> E["Point of view and context"] --> F["Competing interpretations"]
  F --> G["Civic and legal source analysis"]
\`\`\`

**Legend:** A retelling is content evidence; sourcing and corroboration are separate reasoning evidence.
`,
  'civic_government_progression.md': `# Civic and Government Progression

Civic reasoning spirals from classroom rules toward constitutional interpretation and participation.

\`\`\`mermaid
flowchart LR
  A["Rules and laws"] --> B["Citizenship"] --> C["Local/state/federal government"]
  C --> D["Constitution and Bill of Rights"] --> E["Federalism and checks/balances"]
  E --> F["Supreme Court and civil rights"] --> G["Democratic participation"]
\`\`\`

**Legend:** Civic judgment requires evidence, competing values, and institutional context.
`,
  'economics_incentives_progression.md': `# Economics and Incentives Progression

Economic reasoning connects choices and resources to institutions and historical consequences.

\`\`\`mermaid
flowchart LR
  A["Producers and consumers"] --> B["Resources, supply, and demand"]
  B --> C["Colonial economies"] --> D["Trade routes and exchange"]
  D --> E["Industrialization"] --> F["Capitalism, labor, taxes, and public goods"]
\`\`\`

**Legend:** Ask who gains, who bears costs, which incentives matter, and what changes over time.
`,
  'world_history_civilizations_progression.md': `# World History and Civilizations Progression

This content map supports comparative questions across civilizations without reducing history to recall.

\`\`\`mermaid
flowchart LR
  A["Ancient river civilizations"] --> B["Judaism, Hinduism, Buddhism, China, Greece, Rome"]
  B --> C["Islam, Medieval Europe, Africa, Japan, Americas"]
  C --> D["Renaissance, Reformation, and Exploration"]
\`\`\`

**Legend:** Compare geography, institutions, beliefs, trade, pressures, choices, and consequences.
`,
  'us_history_constitution_progression.md': `# U.S. History and Constitution Progression

This thread connects colonial pressures to constitutional democracy and unresolved conflicts.

\`\`\`mermaid
flowchart LR
  A["Colonies"] --> B["Revolution"] --> C["Declaration"] --> D["Articles of Confederation"]
  D --> E["Constitution"] --> F["Bill of Rights"] --> G["Early republic"]
  G --> H["Expansion, slavery, and Civil War"] --> I["Constitutional democracy"]
\`\`\`

**Legend:** Use Story Maps to expose actors, omitted perspectives, institutional constraints, and moral tradeoffs.
`,
  'story_map_conundrum_alignment.md': `# Story Map and Conundrum Alignment

This workflow maps benchmark terrain into a UCC History Story Map and an evidence-producing campaign.

\`\`\`mermaid
flowchart TD
  Benchmark["Social Studies Benchmark Node"]
  Topic["Historical Topic"]
  Places["Places / Map Coordinates"]
  Actors["Actors / Perspectives"]
  Pressures["Pressures"]
  Choices["Choices"]
  Consequences["Consequences"]
  Conundrum["Conundrum / Moral Tradeoff"]
  Receipt["Story Map Receipt"]
  Campaign["Learning Campaign"]
  Hermes["Hermes Brief"]
  Benchmark --> Topic
  Topic --> Places
  Topic --> Actors
  Actors --> Pressures
  Pressures --> Choices
  Choices --> Consequences
  Consequences --> Conundrum
  Receipt --> Benchmark
  Receipt --> Campaign
  Benchmark --> Hermes
  Campaign --> Hermes
\`\`\`

**Legend:** Benchmark = terrain; Story Map receipt = evidence; campaign = active plan; parent = final judgment.
`,
  'sample_learner_heatmap.md': `# Sample Social Studies Learner Heat Map

> **Fictional sample only — not real learner data.** This is an ad hoc diagnostic artifact, not core app UI.

\`\`\`mermaid
flowchart LR
  A["1.1 Citizenship"] --> B["2.1 Family history + sources"] --> C["3.4 Rules/laws/government"]
  C --> D["4.5 Local/state/federal government"] --> E["5.5 Revolution causes"]
  E --> F["Grade 6 source analysis"] --> G["8.2 Constitution"] --> H["HS 12.1 Democracy"]

  classDef mastered fill:#d6f5d6,stroke:#2e7d32,color:#111
  classDef learning fill:#fff4cc,stroke:#b8860b,color:#111
  classDef weak fill:#ffd6d6,stroke:#b71c1c,color:#111
  classDef noEvidence fill:#eeeeee,stroke:#777,color:#111
  classDef advanced fill:#dbeafe,stroke:#1d4ed8,color:#111
  class A mastered
  class B learning
  class C mastered
  class D learning
  class E learning
  class F weak
  class G noEvidence
  class H advanced
\`\`\`

**Legend:** green = mastered; yellow = learning; red = foundational-repair candidate; gray = needs evidence; blue = advanced. Real status must come from overlay evidence.
`,
};

function main() {
  fs.mkdirSync(OUTPUT_FOLDER, { recursive: true });
  for (const [filename, contents] of Object.entries(diagrams).sort(([a], [b]) => a.localeCompare(b))) fs.writeFileSync(path.join(OUTPUT_FOLDER, filename), contents.endsWith('\n') ? contents : `${contents}\n`, 'utf8');
  console.log(`Generated ${Object.keys(diagrams).length} Social Studies Mermaid documents.`);
}
if (require.main === module) {
  try { main(); } catch (error) { console.error(`Social Studies diagram generation failed: ${error.message}`); process.exitCode = 1; }
}

