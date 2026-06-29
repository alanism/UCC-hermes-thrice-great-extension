#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const OUTPUT_FOLDER = path.resolve(__dirname, '..', 'mermaid');

const diagrams = {
  'progression_spine.md': `# California Science Progression Spine

This broad grade-equivalence view is reference terrain, not a required science schedule.

\`\`\`mermaid
flowchart TD
  G1["Grade 1: Structures, offspring, sky patterns, light/sound, simple engineering"]
  G2["Grade 2: Ecosystems, habitats, Earth changes, matter properties, erosion solutions"]
  G3["Grade 3: Life cycles, traits, adaptations, fossils, weather/climate, forces/magnets"]
  G4["Grade 4: Structure/function, senses, Earth processes, energy, waves, resources"]
  G5["Grade 5: Matter conservation, food energy, Earth systems, stars, gravity, water"]
  G6["Grade 6: Cells, genetics, water cycle, weather/climate, thermal energy, impacts"]
  G7["Grade 7: Ecosystems, matter/energy cycling, plate tectonics, chemistry, thermal processes"]
  G8["Grade 8: Evolution, space systems, forces, waves, natural selection, impacts"]
  HS["High School: Biology, chemistry, physics, Earth systems, engineering, computational models"]
  G1 --> G2 --> G3 --> G4 --> G5 --> G6 --> G7 --> G8 --> HS
\`\`\`

**Legend:** Arrows preserve grade-reference order only. Phenomena, concepts, and practices may develop nonlinearly.
`,
  'life_science_progression.md': `# Life Science Progression

Life-science ideas spiral from observable structures toward cellular, ecological, and evolutionary mechanisms.

\`\`\`mermaid
flowchart LR
  A["Grades 1–2<br/>Plant/animal parts, offspring, habitats"] --> B["Grade 3<br/>Life cycles, traits, adaptations"]
  B --> C["Grade 4<br/>Structure and function"]
  C --> D["Grade 5<br/>Food webs and matter flow"]
  D --> E["Grade 6<br/>Cells and genetics"]
  E --> F["Grades 7–8<br/>Ecosystems, evolution, natural selection"]
  F --> G["High School<br/>Molecular biology, ecology, heredity, evolution"]
\`\`\`

**Legend:** Each transition is a conceptual thread, not a universal prerequisite claim.
`,
  'physical_science_progression.md': `# Physical Science Progression

Physical-science terrain connects observable phenomena to particle, force, wave, and energy models.

\`\`\`mermaid
flowchart LR
  A["Grade 1<br/>Light and sound"] --> B["Grade 2<br/>Materials and properties"]
  B --> C["Grade 3<br/>Forces and magnets"]
  C --> D["Grade 4<br/>Energy and waves"]
  D --> E["Grades 5–6<br/>Particles, matter, temperature"]
  E --> F["Grade 7<br/>Chemical reactions and thermal processes"]
  F --> G["Grade 8<br/>Newtonian forces and wave models"]
  G --> H["High School<br/>Mechanics, waves, energy, chemistry"]
\`\`\`

**Legend:** Content knowledge and modeling/investigation evidence should be tracked separately.
`,
  'earth_space_science_progression.md': `# Earth and Space Science Progression

Earth/space reasoning moves between observable patterns, interacting systems, deep time, and human impacts.

\`\`\`mermaid
flowchart LR
  A["Grade 1<br/>Sun, moon, stars"] --> B["Grade 2<br/>Land, water, erosion"]
  B --> C["Grade 3<br/>Weather and climate"]
  C --> D["Grade 4<br/>Fossils and landscape change"]
  D --> E["Grades 5–6<br/>Earth systems and water cycle"]
  E --> F["Grade 7<br/>Plate tectonics and climate"]
  F --> G["Grade 8<br/>Space systems and geologic time"]
  G --> H["High School<br/>Earth systems, climate, resources, space"]
\`\`\`

**Legend:** System models, evidence, and scale reasoning spiral throughout this thread.
`,
  'engineering_design_progression.md': `# Engineering Design Progression

Engineering expectations are deliberately reusable across grades and phenomena.

\`\`\`mermaid
flowchart LR
  A["Ask questions and define a problem"] --> B["Sketch or model a solution"]
  B --> C["Compare test results"]
  C --> D["Define criteria and constraints"]
  D --> E["Run fair tests"]
  E --> F["Evaluate competing solutions"]
  F --> G["Optimize and refine designs"]
\`\`\`

**Legend:** Design cycles may repeat in any domain; arrows describe iteration rather than age-locked stages.
`,
  'scientific_practices_progression.md': `# Scientific Practices Progression

Scientific practices grow through repeated use with increasing precision, independence, and complexity.

\`\`\`mermaid
flowchart LR
  A["Observe"] --> B["Ask questions"] --> C["Investigate"] --> D["Develop/use models"]
  D --> E["Analyze data"] --> F["Construct explanations"] --> G["Argue from evidence"]
  G --> H["Compute/simulate"] --> I["Design and refine"]
\`\`\`

**Legend:** This is a practice repertoire, not a one-way sequence; investigations often loop among nodes.
`,
  'matter_energy_systems_progression.md': `# Matter, Energy, and Systems Progression

This cross-disciplinary thread links physical and life-science accounts of flows, cycles, and conservation.

\`\`\`mermaid
flowchart LR
  A["Materials"] --> B["Matter states"] --> C["Conservation of matter"]
  C --> D["Food energy"] --> E["Ecosystem matter flow"]
  E --> F["Particles and temperature"] --> G["Chemical reactions"]
  G --> H["HS chemistry and biology energy systems"]
\`\`\`

**Legend:** Track whether evidence concerns vocabulary, system models, quantitative conservation, or explanation.
`,
  'evidence_argument_modeling_progression.md': `# Evidence, Argument, and Modeling Progression

This UCC-critical-thinking thread emphasizes how observations become defensible scientific explanations.

\`\`\`mermaid
flowchart LR
  A["Observation"] --> B["Evidence-based account"] --> C["Data interpretation"]
  C --> D["Model explanation"] --> E["Argument from evidence"]
  E --> F["Claims + evidence + reasoning"] --> G["Computational representation"]
\`\`\`

**Legend:** A content-correct answer does not automatically demonstrate the practice represented by the next node.
`,
  'sample_learner_heatmap.md': `# Sample Science Learner Heat Map

> **Fictional sample only — not real learner data.** This is an ad hoc diagnostic artifact, not core app UI.

\`\`\`mermaid
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
\`\`\`

**Legend:** green = mastered; yellow = learning; red = foundational-repair candidate; gray = needs evidence; blue = advanced. Use only actual overlay evidence for real learners.
`,
};

function main() {
  fs.mkdirSync(OUTPUT_FOLDER, { recursive: true });
  for (const [filename, contents] of Object.entries(diagrams).sort(([a], [b]) => a.localeCompare(b))) {
    fs.writeFileSync(path.join(OUTPUT_FOLDER, filename), contents.endsWith('\n') ? contents : `${contents}\n`, 'utf8');
  }
  console.log(`Generated ${Object.keys(diagrams).length} Science Mermaid documents.`);
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(`Science diagram generation failed: ${error.message}`);
    process.exitCode = 1;
  }
}

