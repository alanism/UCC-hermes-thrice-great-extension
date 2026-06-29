#!/usr/bin/env node
'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const PACK_ROOT = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(PACK_ROOT, '..', '..');
const SOURCE_FOLDER = path.join(PROJECT_ROOT, 'California Common Core Math Standards by Grade');
const RAW_FOLDER = path.join(PACK_ROOT, 'raw');
const ONTOLOGY_FOLDER = path.join(PACK_ROOT, 'ontology');
const MARKDOWN_FOLDER = path.join(PACK_ROOT, 'markdown');
const GRADES = ['1', '2', '3', '4', '5', '6', '7', '8', 'HS'];

const DISCIPLINES = {
  LS: 'Life Science',
  PS: 'Physical Science',
  ESS: 'Earth and Space Science',
  ETS: 'Engineering Design',
};

const SCIENCE_PRACTICES = [
  ['asking_questions', 'Asking questions and defining problems', 'Asking scientific questions or defining engineering problems.'],
  ['developing_models', 'Developing and using models', 'Creating, using, revising, or interpreting models.'],
  ['planning_investigations', 'Planning and carrying out investigations', 'Designing or conducting observations, experiments, or fair tests.'],
  ['analyzing_data', 'Analyzing and interpreting data', 'Using tables, graphs, measurements, patterns, or datasets to reason.'],
  ['math_computational_thinking', 'Using mathematics and computational thinking', 'Using numerical, mathematical, or computational representations.'],
  ['constructing_explanations', 'Constructing explanations', 'Explaining how or why a phenomenon occurs using evidence.'],
  ['designing_solutions', 'Designing solutions', 'Designing, comparing, testing, or improving solutions.'],
  ['argument_from_evidence', 'Engaging in argument from evidence', 'Supporting claims with evidence and reasoning.'],
  ['obtaining_information', 'Obtaining, evaluating, and communicating information', 'Using texts, media, or technical information to explain or evaluate.'],
].map(([id, label, description]) => ({ id, label, description }));

const CROSSCUTTING_CONCEPTS = [
  ['patterns', 'Patterns', 'Observed patterns that organize, classify, or predict phenomena.'],
  ['cause_effect', 'Cause and effect', 'Mechanisms and explanations for why events occur.'],
  ['scale_proportion_quantity', 'Scale, proportion, and quantity', 'Size, time, proportion, quantity, and mathematical scale.'],
  ['systems_system_models', 'Systems and system models', 'Systems, subsystems, boundaries, interactions, and models.'],
  ['energy_matter', 'Energy and matter', 'Flows, cycles, conservation, and transfer of energy and matter.'],
  ['structure_function', 'Structure and function', 'How shape, structure, or organization enables function.'],
  ['stability_change', 'Stability and change', 'Change over time, equilibrium, feedback, and stability.'],
].map(([id, label, description]) => ({ id, label, description }));

const UCC_TAGS = [
  ['scientific_investigation', 'Scientific investigation', 'Planning, observing, measuring, testing, and collecting evidence.'],
  ['model_based_reasoning', 'Model-based reasoning', 'Developing and using models to explain phenomena.'],
  ['evidence_reasoning', 'Evidence reasoning', 'Using evidence to support explanations, claims, and arguments.'],
  ['data_graph_reasoning', 'Data and graph reasoning', 'Reading, creating, and interpreting tables, graphs, maps, and datasets.'],
  ['cause_effect_reasoning', 'Cause and effect reasoning', 'Explaining mechanisms and causal relationships.'],
  ['systems_thinking', 'Systems thinking', 'Understanding components, interactions, feedback loops, and boundaries.'],
  ['structure_function_reasoning', 'Structure and function reasoning', 'Explaining how parts, structures, or forms support function.'],
  ['matter_energy_reasoning', 'Matter and energy reasoning', 'Tracking matter, energy, flows, cycles, and conservation.'],
  ['engineering_design', 'Engineering design', 'Defining problems, constraints, criteria, prototypes, tests, and improvements.'],
  ['scientific_communication', 'Scientific communication', 'Explaining, arguing, presenting, reading, and synthesizing scientific information.'],
  ['phenomenon_explanation', 'Phenomenon explanation', 'Explaining observable real-world phenomena using science ideas.'],
  ['math_in_science', 'Mathematics in science', 'Using math, quantities, computation, ratios, graphs, and models in science.'],
].map(([id, label, description]) => ({ id, label, description }));

const PRACTICE_RULES = [
  ['asking_questions', /ask questions?|evaluate questions?|define.*problem/i],
  ['developing_models', /develop.*models?|use.*models?|model to describe|represent.*model/i],
  ['planning_investigations', /plan.*investigation|conduct.*investigation|carry out|fair test|make observations|measurements/i],
  ['analyzing_data', /analyze.*data|interpret.*data|collect data|observations.*patterns|graph|table|display|map|patterns in data/i],
  ['math_computational_thinking', /mathematical|computational|calculate|quantitative|representations|percent|ratio/i],
  ['constructing_explanations', /construct.*explanation|explain|explanation based on evidence/i],
  ['designing_solutions', /design|solution|prototype|criteria|constraints|test.*device|refine/i],
  ['argument_from_evidence', /argument|claim|support.*evidence|defend.*claim|evaluate.*evidence/i],
  ['obtaining_information', /obtain.*information|gather.*information|communicate|read texts|use media|synthesize/i],
];

const CONCEPT_RULES = [
  ['patterns', /pattern|cycle|predictable|sequence|repeating/i],
  ['cause_effect', /cause|effect|impact|affect|influence|results in|leads to/i],
  ['scale_proportion_quantity', /scale|proportion|quantity|amount|percentage|ratio|distance|relative|size/i],
  ['systems_system_models', /system|subsystem|interacting|feedback|cycle|flow|network/i],
  ['energy_matter', /energy|matter|conservation|transfer|flow|cycling|photosynthesis|respiration|food chain|food web/i],
  ['structure_function', /structure|function|parts|external parts|internal structures|shape|organ|cell parts/i],
  ['stability_change', /change|stability|stable|weathering|erosion|evolution|succession|equilibrium|homeostasis/i],
];

const PHENOMENON_RULES = [
  ['life_science', /plant|animal|organism|offspring|parent|trait|life cycle|ecosystem|food chain|food web|biodiversity|adaptation|evolution|natural selection/i],
  ['cells_genetics', /cell|DNA|gene|protein|genetic|mutation|chromosome|reproduction|mitosis|meiosis/i],
  ['matter_chemistry', /matter|material|solid|liquid|gas|particle|chemical|reaction|atom|molecule|substance/i],
  ['forces_motion', /force|motion|push|pull|magnet|electric|gravity|acceleration|collision|Newton/i],
  ['energy_waves', /energy|heat|thermal|temperature|light|sound|wave|wavelength|amplitude|frequency/i],
  ['earth_systems', /earth|rock|erosion|weathering|fossil|land|water|climate|weather|geosphere|hydrosphere|atmosphere/i],
  ['space_systems', /sun|moon|stars|solar system|planet|gravity|galaxy|universe|season|eclipse/i],
  ['human_impacts_engineering', /human impact|natural resources|environment|hazard|flood|hurricane|erosion|conservation|pollution|engineering design|design solution|prototype/i],
];

function ensureDirectories() {
  for (const folder of [RAW_FOLDER, ONTOLOGY_FOLDER, MARKDOWN_FOLDER]) fs.mkdirSync(folder, { recursive: true });
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function writeText(filePath, value) {
  fs.writeFileSync(filePath, value.endsWith('\n') ? value : `${value}\n`, 'utf8');
}

function sha256(filePath) {
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function gradeFromFilename(filename) {
  const match = filename.match(/California Common Core Science Grade ([1-8]|HS)\.txt$/i);
  if (!match) throw new Error(`Cannot detect Science grade from filename: ${filename}`);
  return match[1].toUpperCase();
}

function gradeIndex(grade) {
  return GRADES.indexOf(String(grade));
}

function sourceFiles() {
  if (!fs.existsSync(SOURCE_FOLDER)) throw new Error(`Source folder does not exist: ${SOURCE_FOLDER}`);
  const files = fs.readdirSync(SOURCE_FOLDER)
    .filter((name) => /^California Common Core Science Grade (?:[1-8]|HS)\.txt$/i.test(name))
    .sort((a, b) => gradeIndex(gradeFromFilename(a)) - gradeIndex(gradeFromFilename(b)) || a.localeCompare(b));
  const found = new Set(files.map(gradeFromFilename));
  const missing = GRADES.filter((grade) => !found.has(grade));
  if (missing.length) throw new Error(`Missing Science source grade files: ${missing.join(', ')}`);
  return files;
}

function copyRawFiles(files) {
  for (const filename of files) {
    const source = path.join(SOURCE_FOLDER, filename);
    const target = path.join(RAW_FOLDER, filename);
    if (!fs.existsSync(target) || sha256(source) !== sha256(target)) fs.copyFileSync(source, target);
  }
}

function parseStandard(line) {
  const match = line.match(/^((?:[1-8]|K-2|3-5|MS|HS)-(LS|PS|ESS|ETS)\d+-\d+)\s+(.+)$/);
  if (!match) return null;
  return { standardCode: match[1], disciplineCode: match[2], standardText: match[3].trim() };
}

function parseDisciplineHeading(line) {
  const match = line.match(/^(LS|PS|ESS|ETS)\s+(.+)$/);
  return match ? { disciplineCode: match[1], heading: line } : null;
}

function isSkillExample(line) {
  return /\([^\n()]*\)$/.test(line);
}

function uniqueSorted(values) {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b));
}

function tagsFromRules(text, rules) {
  return rules.filter(([, rule]) => rule.test(text)).map(([tag]) => tag).sort();
}

function applyTags(node) {
  const text = [node.topic, ...(node.alternateTopics || []), node.standardText, ...node.skillExamples].join(' ');
  node.sciencePracticeTags = tagsFromRules(text, PRACTICE_RULES);
  node.crosscuttingConceptTags = tagsFromRules(text, CONCEPT_RULES);
  node.phenomenonTags = tagsFromRules(text, PHENOMENON_RULES);
  const practices = new Set(node.sciencePracticeTags);
  const concepts = new Set(node.crosscuttingConceptTags);
  const ucc = new Set();
  if (practices.has('planning_investigations')) ucc.add('scientific_investigation');
  if (practices.has('developing_models')) ucc.add('model_based_reasoning');
  if (practices.has('argument_from_evidence') || practices.has('constructing_explanations')) ucc.add('evidence_reasoning');
  if (practices.has('analyzing_data')) ucc.add('data_graph_reasoning');
  if (concepts.has('cause_effect')) ucc.add('cause_effect_reasoning');
  if (concepts.has('systems_system_models')) ucc.add('systems_thinking');
  if (concepts.has('structure_function')) ucc.add('structure_function_reasoning');
  if (concepts.has('energy_matter')) ucc.add('matter_energy_reasoning');
  if (practices.has('designing_solutions')) ucc.add('engineering_design');
  if (practices.has('obtaining_information')) ucc.add('scientific_communication');
  if (practices.has('constructing_explanations')) ucc.add('phenomenon_explanation');
  if (practices.has('math_computational_thinking')) ucc.add('math_in_science');
  node.uccCapabilityTags = [...ucc].sort();
  node.progressionTags = uniqueSorted([`grade${node.grade}_core`, `${node.disciplineCode.toLowerCase()}_progression`, ...node.phenomenonTags.map((tag) => `${tag}_progression`)]);
}

function parseFile(filename) {
  const grade = gradeFromFilename(filename);
  const lines = fs.readFileSync(path.join(SOURCE_FOLDER, filename), 'utf8').replace(/\r\n/g, '\n').split('\n');
  const nodes = [];
  let topic = '';
  let disciplineSectionHeading = '';
  let current = null;

  for (const originalLine of lines) {
    const line = originalLine.trim();
    if (!line) continue;

    const standard = parseStandard(line);
    if (standard) {
      if (!topic) throw new Error(`${filename}: standard ${standard.standardCode} appears before a topic heading`);
      const gradeBand = standard.standardCode.match(/^(.+?)-(?:LS|PS|ESS|ETS)/)[1];
      current = {
        id: `CA.SCI.${grade}.${standard.standardCode}`,
        system: 'California Science',
        subject: 'Science',
        grade,
        gradeBand,
        disciplineCode: standard.disciplineCode,
        disciplineName: DISCIPLINES[standard.disciplineCode],
        disciplineSectionHeading: disciplineSectionHeading || null,
        topic,
        alternateTopics: [],
        standardCode: standard.standardCode,
        standardText: standard.standardText,
        skillExamples: [],
        sciencePracticeTags: [],
        crosscuttingConceptTags: [],
        phenomenonTags: [],
        uccCapabilityTags: [],
        progressionTags: [],
        sourceFile: filename,
      };
      nodes.push(current);
      continue;
    }

    if (current && isSkillExample(line)) {
      current.skillExamples.push(line);
      continue;
    }

    const disciplineHeading = parseDisciplineHeading(line);
    if (disciplineHeading) {
      disciplineSectionHeading = disciplineHeading.heading;
      topic = '';
      current = null;
      continue;
    }

    topic = line;
    current = null;
  }
  return nodes;
}

function mergeNodes(nodes) {
  const byId = new Map();
  for (const node of nodes) {
    const existing = byId.get(node.id);
    if (!existing) {
      byId.set(node.id, node);
      continue;
    }
    if (existing.standardText !== node.standardText || existing.disciplineCode !== node.disciplineCode) {
      throw new Error(`Conflicting repeated Science standard: ${node.standardCode}`);
    }
    existing.skillExamples.push(...node.skillExamples);
    if (existing.topic !== node.topic) existing.alternateTopics.push(node.topic);
  }
  const merged = [...byId.values()];
  for (const node of merged) {
    node.skillExamples = uniqueSorted(node.skillExamples);
    node.alternateTopics = uniqueSorted(node.alternateTopics);
    applyTags(node);
  }
  return merged.sort(compareNodes);
}

function standardKey(code) {
  const match = code.match(/-(LS|PS|ESS|ETS)(\d+)-(\d+)$/);
  return match ? `${match[1]}${match[2]}-${match[3]}` : code;
}

function compareNodes(a, b) {
  return gradeIndex(a.grade) - gradeIndex(b.grade) || a.disciplineCode.localeCompare(b.disciplineCode) || a.standardCode.localeCompare(b.standardCode, undefined, { numeric: true });
}

function addEdge(edges, nodeIds, fromId, toId, relationship, confidence, reason) {
  if (!nodeIds.has(fromId) || !nodeIds.has(toId) || fromId === toId) return;
  const key = `${fromId}|${toId}|${relationship}`;
  if (!edges.has(key)) edges.set(key, { from: fromId, to: toId, relationship, confidence, reason });
}

function buildEdges(nodes) {
  const nodeIds = new Set(nodes.map((node) => node.id));
  const edges = new Map();
  const byKey = new Map();
  for (const node of nodes) {
    const key = standardKey(node.standardCode);
    if (!byKey.has(key)) byKey.set(key, []);
    byKey.get(key).push(node);
  }
  for (const group of byKey.values()) {
    group.sort(compareNodes);
    for (let index = 0; index < group.length - 1; index += 1) {
      const from = group[index];
      const to = group[index + 1];
      const repeatedBandCode = from.standardCode === to.standardCode;
      addEdge(
        edges,
        nodeIds,
        from.id,
        to.id,
        repeatedBandCode && from.disciplineCode === 'ETS' ? 'engineering_design_reuse' : 'conceptual_progression',
        'medium',
        repeatedBandCode
          ? 'The same grade-band performance expectation is intentionally reused in another source grade; evidence may be collected through different phenomena and projects.'
          : `The ${standardKey(from.standardCode)} idea reappears at a later level with greater conceptual or practice demands.`,
      );
    }
  }

  const curated = [
    ['CA.SCI.1.1-LS1-1', 'CA.SCI.4.4-LS1-1', 'conceptual_progression', 'Early observation of external parts supports later structure-function argumentation.'],
    ['CA.SCI.2.2-PS1-1', 'CA.SCI.5.5-PS1-1', 'conceptual_progression', 'Classifying observable material properties supports later particle and conservation reasoning.'],
    ['CA.SCI.3.3-PS2-1', 'CA.SCI.8.MS-PS2-2', 'practice_progression', 'Grade 3 force investigations support middle-school investigation of force, mass, and acceleration.'],
    ['CA.SCI.4.4-PS4-1', 'CA.SCI.8.MS-PS4-1', 'conceptual_progression', 'Elementary wave models support mathematical middle-school wave representations.'],
    ['CA.SCI.5.5-LS2-1', 'CA.SCI.7.MS-LS2-3', 'conceptual_progression', 'Models of matter movement in food webs support middle-school cycling and energy-flow explanations.'],
    ['CA.SCI.6.MS-LS1-1', 'CA.SCI.HS.HS-LS1-1', 'future_dependency', 'Evidence that organisms are cellular supports molecular structure-function explanations in high school.'],
    ['CA.SCI.8.MS-PS2-2', 'CA.SCI.HS.HS-PS2-1', 'practice_progression', 'Middle-school force investigations support high-school quantitative analysis of Newtonian motion.'],
  ];
  for (const [from, to, relationship, reason] of curated) addEdge(edges, nodeIds, from, to, relationship, relationship === 'future_dependency' ? 'low' : 'high', reason);

  return [...edges.values()].sort((a, b) => a.from.localeCompare(b.from) || a.to.localeCompare(b.to) || a.relationship.localeCompare(b.relationship));
}

function generatedAt(files) {
  const latest = Math.max(...files.map((filename) => fs.statSync(path.join(SOURCE_FOLDER, filename)).mtimeMs));
  return new Date(latest).toISOString();
}

function gradeMarkdown(grade, nodes) {
  const gradeNodes = nodes.filter((node) => node.grade === grade);
  const disciplines = new Map();
  for (const node of gradeNodes) {
    if (!disciplines.has(node.disciplineCode)) disciplines.set(node.disciplineCode, { name: node.disciplineName, topics: new Map() });
    const topics = disciplines.get(node.disciplineCode).topics;
    if (!topics.has(node.topic)) topics.set(node.topic, []);
    topics.get(node.topic).push(node);
  }
  const lines = [
    `# California Science — Grade ${grade}`,
    '',
    '> Reference benchmark only. Benchmarks inform. They do not command.',
    '',
    `This view contains ${gradeNodes.length} performance-expectation nodes across ${disciplines.size} discipline areas. Science evidence may be nonlinear across content, practices, crosscutting concepts, and phenomena.`,
    '',
  ];
  for (const [disciplineCode, discipline] of [...disciplines.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    lines.push(`## ${disciplineCode}: ${discipline.name}`, '');
    for (const [topic, topicNodes] of discipline.topics) {
      lines.push(`### ${topic}`, '');
      for (const node of topicNodes) {
        lines.push(`#### ${node.standardCode}`, '', node.standardText, '');
        if (node.alternateTopics.length) lines.push(`**Also appears under:** ${node.alternateTopics.join('; ')}`, '');
        lines.push(`**Science practices:** ${node.sciencePracticeTags.length ? node.sciencePracticeTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '', `**Crosscutting concepts:** ${node.crosscuttingConceptTags.length ? node.crosscuttingConceptTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '', `**Phenomena:** ${node.phenomenonTags.length ? node.phenomenonTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '', `**UCC capabilities:** ${node.uccCapabilityTags.length ? node.uccCapabilityTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '');
        if (node.skillExamples.length) lines.push('**Skill examples:**', '', ...node.skillExamples.map((example) => `- ${example}`), '');
      }
    }
  }
  lines.push('## Related diagrams', '', '- [Scientific practices progression](../mermaid/scientific_practices_progression.md)', '- [Evidence, argument, and modeling progression](../mermaid/evidence_argument_modeling_progression.md)', '- [Sample learner heat map](../mermaid/sample_learner_heatmap.md)', '');
  return lines.join('\n');
}

function ontologyMarkdown(nodes, edges) {
  return `# California Science Benchmark Ontology

> **Benchmarks inform. They do not command.**

## What this pack is

This pack is a reference terrain map for UnCommon Core / Hermes Thrice Great. It converts the supplied California Science / NGSS-style performance expectations into ${nodes.length} nodes and ${edges.length} transparent, editable relationships across discipline, practice, crosscutting-concept, and phenomenon lenses.

## What this pack is not

It is not UCC's curriculum authority, a rigid grade schedule, or proof that a learner can perform a practice. The School Model Canvas remains the macro authority. Learning Campaigns remain the active plan. Receipts and artifacts remain the evidence layer.

## From performance expectations to nodes

Each source performance expectation becomes a grade-qualified deterministic ID. The parser preserves topic, inferred discipline, source grade band, skill examples, and any available discipline section heading. Exact repeated HS standards are merged by ID with examples deduplicated and alternate topics retained. Raw files are copied unchanged.

Performance expectations combine content and action: knowing a topic is not equivalent to planning an investigation, analyzing data, developing a model, or arguing from evidence. Tags therefore expose all four science lenses rather than reducing the pack to a topic list.

## Edge meanings

- \`conceptual_progression\`: a science idea reappears with greater depth.
- \`practice_progression\`: a scientific practice reappears with greater independence or rigor.
- \`spiral_progression\`, \`supports\`, and \`future_dependency\`: editable diagnostic hypotheses, not mandated order.
- \`parallel_practice\`: practices that can develop together.
- \`engineering_design_reuse\`: the same grade-band design expectation appears in multiple grade files.

## Evidence, planning, and overlays

Science receipts, projects, lab notes, models, explanations, builds, and parent observations may map separately to content and practice tags. Learning Campaign Builder should begin with the School Model Canvas and actual evidence, then use this terrain to choose a phenomenon and an evidence-producing next move. Overlay status lives outside the ontology; \`no_evidence\` means unobserved, not inability. Mermaid heat maps are ad hoc diagnostics, not core app UI or identity labels.

## Commands

\`\`\`bash
node benchmarks/ca_science/scripts/ingest_ca_science.js
node benchmarks/ca_science/scripts/generate_mermaid_diagrams.js
node benchmarks/ca_science/scripts/validate_benchmark_pack.js
node benchmarks/ca_science/tests/benchmark_pack_smoke_test.js
\`\`\`
`;
}

function hermesInstructions() {
  return `# Instructions to Hermes Thrice Great — Science Benchmark Pack

## Governing doctrine

**Benchmarks inform. They do not command.**

This pack is reference terrain, not curriculum authority. SchoolModelCanvas.md is the mission. Learning Campaigns are the active plan. Science receipts, project artifacts, lab notes, models, explanations, and parent observations are evidence. Hermes interprets and orchestrates. The parent is the final decision-maker.

\`\`\`mermaid
flowchart TD
  SMC["SchoolModelCanvas.md<br/>Family educational constitution"]
  LC["Learning Campaigns<br/>Active weekly/monthly priorities"]
  Receipts["Science Receipts<br/>Assessments, projects, lab notes, models"]
  Artifacts["Portfolio Artifacts<br/>Diagrams, explanations, builds, observations"]
  Benchmarks["CA Science Benchmark Pack<br/>Phenomena + practices + concepts"]
  Hermes["Hermes Thrice Great<br/>Interpretation + orchestration"]
  Parent["Parent Coach<br/>Final judgment"]
  Plan["Next Move / Weekly Plan"]
  Heatmap["Ad hoc Mermaid Science Heat Map<br/>Optional diagnostic artifact"]
  SMC --> Hermes
  LC --> Hermes
  Receipts --> Hermes
  Artifacts --> Hermes
  Benchmarks --> Hermes
  Hermes --> Parent
  Parent --> Plan
  Hermes --> Heatmap
\`\`\`

## Interpret through overlapping lenses

Track Life Science, Physical Science, Earth and Space Science, Engineering Design, scientific practices, crosscutting concepts, phenomena, and data/model/evidence quality. Separate recall of content from the ability to investigate, model, interpret data, explain mechanisms, argue from evidence, design, communicate precisely, or use mathematics inside science.

Use this order:

1. Read the School Model Canvas and active Learning Campaign.
2. Inspect receipts and artifacts; name what was actually demonstrated.
3. Map content and practice evidence separately to nodes and tags.
4. Use edges as hypotheses for a next diagnostic or project, never as a rigid schedule.
5. Recommend the smallest phenomenon-rich activity that produces useful evidence for parent judgment.

Prefer **needs evidence**, **currently developing**, **foundational repair**, **current-grade target**, **future dependency**, **benchmark-aligned**, **strength area**, **stretch area**, **maintenance area**, **practice gap**, **modeling gap**, and **evidence gap**. Do not reduce the learner to comparative grade labels or demeaning science-ability labels.

## Example interpretation

- **Evidence:** Recent work shows Aria can name plant parts but needs more practice explaining how structure supports function.
- **Benchmark lens:** Grade 1–4 life-science structure/function thread: \`1-LS1-1 → 4-LS1-1\`.
- **Interpretation:** Treat this as a structure-function explanation campaign, not a generic science weakness.
- **Recommended campaign:** Structure Explains Function.
- **Parent move:** Ask, “What job does this part do, and how does its shape help it do that job?”

## Heat-map guardrails

Generate Mermaid heat maps only as ad hoc diagnostics. Join real overlay evidence to node IDs and practice tags; show content and practice status separately. Render unobserved areas as \`no_evidence\`. A weekly artifact may be named \`aria_science_heatmap_weekXX.md\`. The included sample is fictional and must never be presented as learner evidence.

\`\`\`mermaid
flowchart LR
  E["Receipts + artifacts"] --> C["Content overlay"]
  E --> P["Practice overlay"]
  B["Science terrain map"] --> C
  B --> P
  C --> N["Next phenomenon-rich move"]
  P --> N
  N --> J["Parent judgment"]
\`\`\`
`;
}

function main() {
  ensureDirectories();
  const files = sourceFiles();
  copyRawFiles(files);
  const nodes = mergeNodes(files.flatMap(parseFile));
  const edges = buildEdges(nodes);
  const timestamp = generatedAt(files);

  writeJson(path.join(ONTOLOGY_FOLDER, 'standards_nodes.json'), {
    schema_version: 'ca_science_nodes.v1',
    benchmark_system: 'California Science / NGSS-style Performance Expectations',
    role: 'reference_only',
    generated_at: timestamp,
    source_folder: SOURCE_FOLDER,
    nodes,
  });
  writeJson(path.join(ONTOLOGY_FOLDER, 'prerequisite_edges.json'), {
    schema_version: 'ca_science_edges.v1',
    benchmark_system: 'California Science',
    role: 'reference_only',
    generated_at: timestamp,
    edges,
  });
  writeJson(path.join(ONTOLOGY_FOLDER, 'science_practices.json'), { schema_version: 'science_practices.v1', practices: SCIENCE_PRACTICES });
  writeJson(path.join(ONTOLOGY_FOLDER, 'crosscutting_concepts.json'), { schema_version: 'crosscutting_concepts.v1', concepts: CROSSCUTTING_CONCEPTS });
  writeJson(path.join(ONTOLOGY_FOLDER, 'ucc_capability_tags.json'), { schema_version: 'ucc_science_capability_tags.v1', tags: UCC_TAGS });
  writeJson(path.join(ONTOLOGY_FOLDER, 'learner_overlay_schema.json'), {
    schema_version: 'learner_benchmark_overlay.v1',
    description: 'A learner-specific overlay that marks Science standards/practices/concepts as mastered, learning, weak, no_evidence, advanced, or not_applicable.',
    node_status_values: ['mastered', 'learning', 'weak', 'no_evidence', 'advanced', 'not_applicable'],
    evidence_strength_values: ['low', 'medium', 'high'],
    example: {
      learnerId: 'aria',
      benchmarkSystem: 'California Science',
      generatedAt: '2026-06-27',
      nodes: [{
        standardId: 'CA.SCI.4.4-LS1-1',
        status: 'learning',
        evidenceStrength: 'medium',
        latestEvidenceDate: '2026-06-22',
        evidenceSources: ['science_receipt_2026_06_22', 'parent_observation'],
        notes: 'Understands external plant/animal structures but needs stronger explanation of structure-function relationships.',
      }],
      practiceOverlay: [{
        practiceTag: 'developing_models',
        status: 'learning',
        evidenceStrength: 'medium',
        notes: 'Can label diagrams but needs more practice using models to explain mechanisms.',
      }],
    },
  });

  const countsByGrade = Object.fromEntries(GRADES.map((grade) => [grade, nodes.filter((node) => node.grade === grade).length]));
  writeJson(path.join(ONTOLOGY_FOLDER, 'manifest.json'), {
    schema_version: 'ca_science_manifest.v1',
    benchmark_system: 'California Science / NGSS-style Performance Expectations',
    role: 'reference_only',
    generated_at: timestamp,
    source_folder: SOURCE_FOLDER,
    source_files: files.map((filename) => ({ filename, grade: gradeFromFilename(filename), sha256: sha256(path.join(SOURCE_FOLDER, filename)) })),
    counts: { nodes: nodes.length, edges: edges.length, nodes_by_grade: countsByGrade },
    generation: {
      ingest: 'node benchmarks/ca_science/scripts/ingest_ca_science.js',
      diagrams: 'node benchmarks/ca_science/scripts/generate_mermaid_diagrams.js',
      validate: 'node benchmarks/ca_science/scripts/validate_benchmark_pack.js',
      smoke_test: 'node benchmarks/ca_science/tests/benchmark_pack_smoke_test.js',
    },
  });

  writeText(path.join(MARKDOWN_FOLDER, 'ca_science_ontology.md'), ontologyMarkdown(nodes, edges));
  for (const grade of GRADES) writeText(path.join(MARKDOWN_FOLDER, `grade_${grade}.md`), gradeMarkdown(grade, nodes));
  writeText(path.join(MARKDOWN_FOLDER, 'instructions_to_hermes_thrice_great.md'), hermesInstructions());
  console.log(`Ingested ${files.length} Science source files into ${nodes.length} nodes and ${edges.length} edges.`);
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(`Science ingest failed: ${error.message}`);
    process.exitCode = 1;
  }
}
