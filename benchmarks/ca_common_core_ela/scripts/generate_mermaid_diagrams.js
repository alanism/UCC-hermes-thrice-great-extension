#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const OUTPUT_FOLDER = path.resolve(__dirname, '..', 'mermaid');

const diagrams = {
  'progression_spine.md': `# California Common Core ELA Progression Spine

This broad grade-equivalence map shows recurring ELA emphases. It is reference terrain, not a mandatory learning schedule.

\`\`\`mermaid
flowchart TD
  G1["Grade 1: Foundational comprehension, opinions, vocabulary, sentence cohesion"]
  G2["Grade 2: Cause/effect, compare/contrast, topic sentences, descriptive detail"]
  G3["Grade 3: Main idea, inference, text structures, opinion support, roots/affixes"]
  G4["Grade 4: Text evidence, point of view, figurative language, organization, transitions"]
  G5["Grade 5: Multi-text comparison, formal tone, stronger support, plagiarism awareness"]
  G6["Grade 6: Claims, evidence, counterclaims, logical fallacies, bias, academic vocabulary"]
  G7["Grade 7: Thesis, rhetoric, media bias, argument structure, literary/informational analysis"]
  G8["Grade 8: Stronger argument, citations, active/passive voice, rhetoric, text comparison"]
  G9["Grade 9: Rhetorical analysis, claims/evidence, tone, audience, text development"]
  G10["Grade 10: Advanced argument, evidence analysis, rhetoric, formal style, research"]
  G11["Grade 11: Nuanced rhetoric, synthesis, precision, independent analysis"]
  G12["Grade 12: College/career communication, mature argument, research conventions"]
  G1 --> G2 --> G3 --> G4 --> G5 --> G6 --> G7 --> G8 --> G9 --> G10 --> G11 --> G12
\`\`\`

**Legend:** Arrows show grade-reference order only. ELA development spirals and may be uneven across strands.
`,

  'reading_comprehension_progression.md': `# Reading Comprehension Progression

Comprehension revisits the same moves with increasingly complex texts, independence, and analysis through Grades 1–12.

\`\`\`mermaid
flowchart LR
  A["Grades 1–2<br/>Main topic and key details"] --> B["Grades 2–3<br/>Cause/effect and sequence"]
  B --> C["Grades 3–4<br/>Inference and theme"]
  C --> D["Grades 4–5<br/>Point of view and text structure"]
  D --> E["Grades 5–6<br/>Multi-text comparison and evidence"]
  E --> F["Grades 6–8<br/>Argument tracing and informational analysis"]
  F --> G["Grades 9–10<br/>Rhetorical and literary analysis"]
  G --> H["Grades 11–12<br/>Synthesis, uncertainty, and nuanced interpretation"]
\`\`\`

**Legend:** Each node is a recurring emphasis, not a mastery checkpoint that must precede every later node.
`,

  'vocabulary_language_progression.md': `# Vocabulary and Language Progression

Word knowledge grows through repeated encounters with morphology, context, nuance, and discipline-specific language.

\`\`\`mermaid
flowchart LR
  A["Grades 1–2<br/>Categories, synonyms, antonyms"] --> B["Grades 2–3<br/>Multiple meanings and context"]
  B --> C["Grades 3–4<br/>Prefixes and suffixes"]
  C --> D["Grades 4–6<br/>Greek and Latin roots"]
  D --> E["Grades 6–8<br/>Connotation and denotation"]
  E --> F["Grades 8–10<br/>Context, tone, and precise usage"]
  F --> G["Grades 11–12<br/>Academic, technical, and etymological vocabulary"]
\`\`\`

**Legend:** Vocabulary strands support comprehension, writing, and argument in parallel.
`,

  'writing_structure_progression.md': `# Writing Structure Progression

Writing develops by revisiting organization and craft with greater scope, control, audience awareness, and revision.

\`\`\`mermaid
flowchart LR
  A["Grades 1–2<br/>Sentence order"] --> B["Grades 2–3<br/>Topic sentence and details"]
  B --> C["Grades 3–4<br/>Paragraph organization"]
  C --> D["Grades 4–6<br/>Transitions and cohesion"]
  D --> E["Grades 6–8<br/>Varied sentences and claim structure"]
  E --> F["Grades 8–10<br/>Formal style and evidence integration"]
  F --> G["Grades 11–12<br/>Sustained revision, precision, and disciplinary style"]
\`\`\`

**Legend:** Writing artifacts provide evidence; benchmark nodes only locate the terrain.
`,

  'argument_evidence_progression.md': `# Argument and Evidence Progression

This UCC-critical strand connects literacy to judgment, History Story Maps, and conundrum reasoning.

\`\`\`mermaid
flowchart LR
  A["Grades 1–2<br/>Opinion + reason"] --> B["Grades 2–3<br/>Fact versus opinion"]
  B --> C["Grades 3–5<br/>Supporting details"]
  C --> D["Grades 4–6<br/>Claim + textual evidence"]
  D --> E["Grades 6–8<br/>Counterclaim and argument tracing"]
  E --> F["Grades 7–9<br/>Logical fallacy and source bias"]
  F --> G["Grades 8–10<br/>Rhetorical appeals and evidence connection"]
  G --> H["Grades 11–12<br/>Evidence quality, synthesis, uncertainty, and judgment"]
\`\`\`

**Legend:** Arrows show a useful diagnostic spiral. A later argument challenge may call for evidence on an earlier move, not an assumption of deficiency.
`,

  'speaking_listening_collaboration.md': `# Speaking, Listening, and Collaboration

Collaboration moves between listening, exchanging ideas, negotiating opinions, and formal communication.

\`\`\`mermaid
flowchart LR
  A["Grades 1–2<br/>Collaborative conversation"] --> B["Grades 2–4<br/>Exchanging and clarifying ideas"]
  B --> C["Grades 3–6<br/>Written interaction"]
  C --> D["Grades 5–8<br/>Opinion negotiation and persuasion"]
  D --> E["Grades 7–10<br/>Formal presentation"]
  E --> F["Grades 11–12<br/>Audience-aware persuasion and response"]
\`\`\`

**Legend:** Speaking, listening, and writing can develop at different rates and should be evidenced separately.
`,

  'research_media_literacy_progression.md': `# Research and Media Literacy Progression

Research and media judgment grow from recognizing purpose to evaluating, citing, and synthesizing sources.

\`\`\`mermaid
flowchart LR
  A["Grades 1–3<br/>Text purpose"] --> B["Grades 3–5<br/>Source relevance"]
  B --> C["Grades 5–6<br/>Plagiarism awareness"]
  C --> D["Grades 6–8<br/>Bias, headlines, and persuasive choices"]
  D --> E["Grades 8–10<br/>Citations and MLA conventions"]
  E --> F["Grades 9–11<br/>Rhetorical media analysis"]
  F --> G["Grades 11–12<br/>Source synthesis and disciplinary research"]
\`\`\`

**Legend:** Source-evaluation evidence belongs in receipts and artifacts; this graph is a terrain map.
`,

  'sample_learner_heatmap.md': `# Sample ELA Learner Heat Map

> **Fictional sample only — not real learner data.** This is an ad hoc diagnostic example, not core app UI.

\`\`\`mermaid
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
\`\`\`

**Legend:** green = mastered; yellow = learning; red = foundational-repair candidate; gray = needs evidence; blue = advanced. Status must come from actual overlay evidence.
`,
};

function main() {
  fs.mkdirSync(OUTPUT_FOLDER, { recursive: true });
  for (const [filename, contents] of Object.entries(diagrams).sort(([a], [b]) => a.localeCompare(b))) {
    fs.writeFileSync(path.join(OUTPUT_FOLDER, filename), contents.endsWith('\n') ? contents : `${contents}\n`, 'utf8');
  }
  console.log(`Generated ${Object.keys(diagrams).length} ELA Mermaid documents.`);
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(`ELA diagram generation failed: ${error.message}`);
    process.exitCode = 1;
  }
}

