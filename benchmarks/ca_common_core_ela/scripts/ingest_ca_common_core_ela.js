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
const GRADES = Array.from({ length: 12 }, (_, index) => String(index + 1));

const TAGS = [
  ['collaborative_discussion', 'Collaborative discussion', 'Exchanging information and ideas orally or in writing with others.'],
  ['reading_comprehension', 'Reading comprehension', 'Understanding literary, informational, and multimedia texts.'],
  ['close_reading', 'Close reading', 'Reading closely to determine explicit and implicit meaning.'],
  ['main_idea', 'Main idea', 'Identifying central ideas and key details.'],
  ['theme', 'Theme', 'Identifying themes in literary texts.'],
  ['inference', 'Inference', 'Drawing conclusions from textual evidence.'],
  ['point_of_view', 'Point of view', 'Identifying and comparing narrator, speaker, author perspective, and bias.'],
  ['text_structure', 'Text structure', 'Understanding sequence, cause/effect, compare/contrast, problem/solution, and organization.'],
  ['vocabulary_morphology', 'Vocabulary and morphology', 'Prefixes, suffixes, roots, word relationships, connotation, denotation, and context clues.'],
  ['figurative_language', 'Figurative language', 'Simile, metaphor, allusion, personification, and rhetorical effect.'],
  ['writing_structure', 'Writing structure', 'Topic sentences, organization, transitions, sentence ordering, and paragraph structure.'],
  ['argument_claim_evidence', 'Argument, claim, and evidence', 'Claims, reasons, evidence, counterclaims, argument tracing, and support.'],
  ['rhetoric_media_literacy', 'Rhetoric and media literacy', 'Purpose, audience, tone, bias, appeals, rhetoric, and persuasive strategies.'],
  ['language_conventions', 'Language conventions', 'Grammar, usage, mechanics, sentence construction, punctuation, and frequently confused words.'],
  ['research_citation', 'Research and citation', 'Sources, plagiarism, citations, works cited, and evidence use.'],
  ['oral_presentation', 'Oral presentation', 'Presenting information and ideas formally in academic contexts.'],
  ['explanation_reconstruction', 'Explanation and reconstruction', 'Explaining, summarizing, paraphrasing, and reconstructing meaning in the learner\'s own words.'],
].map(([id, label, description]) => ({ id, label, description }));

const TAG_RULES = [
  ['collaborative_discussion', /collaborative|conversation|discussion|interacting|exchanging information/i],
  ['reading_comprehension', /reading closely|literary|informational texts|multimedia|passage|\btext\b/i],
  ['close_reading', /reading closely|explicitly|implicitly|\bclose\b/i],
  ['main_idea', /main idea|central idea|key details|supporting details/i],
  ['theme', /theme|myths|fables|folktales|short stories/i],
  ['inference', /infer|inference|draw conclusions|predict/i],
  ['point_of_view', /point of view|narrator|speaker|perspective|bias/i],
  ['text_structure', /text structure|sequence|order of events|cause|effect|compare|contrast|problem|solution|organization/i],
  ['vocabulary_morphology', /vocabulary|prefix|suffix|root|Greek|Latin|synonym|antonym|homophone|multiple-meaning|connotation|denotation|context/i],
  ['figurative_language', /simile|metaphor|allusion|personification|figure of speech|figurative/i],
  ['writing_structure', /writing|topic sentence|concluding sentence|transition|paragraph|organize|sentence order|revise|varied sentences/i],
  ['argument_claim_evidence', /claim|evidence|counterclaim|opinion|reason|argument|supporting details|logical fallac/i],
  ['rhetoric_media_literacy', /rhetoric|ethos|pathos|logos|persuasive|author's purpose|audience|tone|formal|bias|headline|media/i],
  ['language_conventions', /grammar|verb|noun|adjective|adverb|preposition|modal|homophone|frequently confused|punctuation|capitalization|sentence/i],
  ['research_citation', /source|citation|plagiarism|Works Cited|MLA|in-text citation|relevant sources/i],
  ['oral_presentation', /oral presentation|presenting information|formal oral/i],
  ['explanation_reconstruction', /summarize|paraphrase|explain|describe|determine|analyze|evaluate/i],
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
  const match = filename.match(/California Common Core ELA Grade (\d+)\.txt$/i);
  if (!match) throw new Error(`Cannot detect ELA grade from filename: ${filename}`);
  return match[1];
}

function sourceFiles() {
  if (!fs.existsSync(SOURCE_FOLDER)) throw new Error(`Source folder does not exist: ${SOURCE_FOLDER}`);
  const files = fs.readdirSync(SOURCE_FOLDER)
    .filter((name) => /^California Common Core ELA Grade \d+\.txt$/i.test(name))
    .sort((a, b) => Number(gradeFromFilename(a)) - Number(gradeFromFilename(b)) || a.localeCompare(b));
  const found = new Set(files.map(gradeFromFilename));
  const missing = GRADES.filter((grade) => !found.has(grade));
  if (missing.length) throw new Error(`Missing ELA source grade files: ${missing.join(', ')}`);
  return files;
}

function copyRawFiles(files) {
  for (const filename of files) {
    const source = path.join(SOURCE_FOLDER, filename);
    const target = path.join(RAW_FOLDER, filename);
    if (!fs.existsSync(target) || sha256(source) !== sha256(target)) fs.copyFileSync(source, target);
  }
}

function parseStrand(line) {
  const match = line.match(/^((?:PI|PII)\.\d+(?:-\d+)?)\s+(.+)$/);
  return match ? { strandCode: match[1], strandName: match[2].trim() } : null;
}

function parseSubStrand(line) {
  const match = line.match(/^((?:PI|PII)\.\d+(?:-\d+)?\.[A-Z])\s+(.+)$/);
  return match ? { subStrandCode: match[1], subStrandName: match[2].trim() } : null;
}

function parseStandard(line) {
  const match = line.match(/^((?:PI|PII)\.\d+(?:-\d+)?\.\d+(?:\.[a-z])?)\s+(.+)$/);
  return match ? { standardCode: match[1], standardText: match[2].trim() } : null;
}

function isSkillExample(line) {
  return /\([^\n()]*\)$/.test(line);
}

function uniqueSorted(values) {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b));
}

function tagsFor(node) {
  const text = [node.standardText, ...node.skillExamples].join(' ');
  return TAG_RULES.filter(([, rule]) => rule.test(text)).map(([tag]) => tag).sort();
}

function progressionTagsFor(node) {
  const tags = new Set([`grade${node.grade}_core`]);
  if (node.subStrandCode.endsWith('.A')) tags.add(node.strandCode.startsWith('PII') ? 'cohesive_texts' : 'collaborative_interaction');
  if (node.subStrandCode.endsWith('.B')) tags.add(node.strandCode.startsWith('PII') ? 'expanding_enriching_ideas' : 'interpretive_reading');
  if (node.subStrandCode.endsWith('.C')) tags.add(node.strandCode.startsWith('PII') ? 'connecting_condensing_ideas' : 'productive_language');
  return [...tags].sort();
}

function parseFile(filename) {
  const grade = gradeFromFilename(filename);
  const lines = fs.readFileSync(path.join(SOURCE_FOLDER, filename), 'utf8').replace(/\r\n/g, '\n').split('\n');
  const nodes = [];
  let strand = null;
  let subStrand = null;
  let current = null;
  let inSpecifiedOntologySection = false;

  for (const originalLine of lines) {
    const line = originalLine.trim();
    if (!line) continue;

    const nextStrand = parseStrand(line);
    if (nextStrand) {
      strand = nextStrand;
      subStrand = null;
      current = null;
      inSpecifiedOntologySection = true;
      continue;
    }

    const nextSubStrand = parseSubStrand(line);
    if (nextSubStrand) {
      if (!strand) throw new Error(`${filename}: sub-strand ${nextSubStrand.subStrandCode} appears before a strand`);
      subStrand = nextSubStrand;
      current = null;
      continue;
    }

    const standard = parseStandard(line);
    if (standard) {
      if (!strand || !subStrand) throw new Error(`${filename}: standard ${standard.standardCode} appears before strand metadata`);
      current = {
        id: `CA.CCSS.ELA.${grade}.${standard.standardCode}`,
        system: 'CA Common Core',
        subject: 'ELA',
        grade,
        strandCode: strand.strandCode,
        strandName: strand.strandName,
        subStrandCode: subStrand.subStrandCode,
        subStrandName: subStrand.subStrandName,
        standardCode: standard.standardCode,
        standardText: standard.standardText,
        skillExamples: [],
        uccCapabilityTags: [],
        progressionTags: [],
        sourceFile: filename,
      };
      nodes.push(current);
      continue;
    }

    // The approved ontology schema covers PI/PII only. Stop before PIII/L/RF/RI/RL/W sections.
    if (/^(?:PIII|L|RF|RI|RL|W)\.\d+(?:-\d+)?(?:\s|\.|$)/.test(line)) {
      inSpecifiedOntologySection = false;
      current = null;
      continue;
    }

    if (inSpecifiedOntologySection && current && isSkillExample(line)) current.skillExamples.push(line);
  }

  for (const node of nodes) {
    node.skillExamples = uniqueSorted(node.skillExamples);
    node.uccCapabilityTags = tagsFor(node);
    node.progressionTags = progressionTagsFor(node);
  }
  return nodes;
}

function standardParts(node) {
  const match = node.standardCode.match(/^(PII?)\.[^.]+\.(\d+)(?:\.([a-z]))?$/);
  return match ? { family: match[1], number: Number(match[2]), nested: match[3] || '' } : { family: '', number: 999, nested: '' };
}

function compareNodes(a, b) {
  const gradeDifference = Number(a.grade) - Number(b.grade);
  if (gradeDifference) return gradeDifference;
  const familyDifference = standardParts(a).family.localeCompare(standardParts(b).family);
  if (familyDifference) return familyDifference;
  const pa = standardParts(a);
  const pb = standardParts(b);
  return pa.number - pb.number || pa.nested.localeCompare(pb.nested) || a.standardCode.localeCompare(b.standardCode);
}

function addEdge(edges, nodeIds, fromNode, toNode, relationship, confidence, reason) {
  if (!fromNode || !toNode || fromNode.id === toNode.id || !nodeIds.has(fromNode.id) || !nodeIds.has(toNode.id)) return;
  const key = `${fromNode.id}|${toNode.id}|${relationship}`;
  if (!edges.has(key)) edges.set(key, { from: fromNode.id, to: toNode.id, relationship, confidence, reason });
}

function buildEdges(nodes) {
  const nodeIds = new Set(nodes.map((node) => node.id));
  const edges = new Map();
  const findNode = (grade, family, number) => nodes.find((node) => {
    const parts = standardParts(node);
    return node.grade === String(grade) && parts.family === family && parts.number === number && !parts.nested;
  });

  for (let grade = 1; grade < 12; grade += 1) {
    for (const family of ['PI', 'PII']) {
      for (let number = 1; number <= (family === 'PI' ? 12 : 7); number += 1) {
        addEdge(
          edges,
          nodeIds,
          findNode(grade, family, number),
          findNode(grade + 1, family, number),
          'spiral_progression',
          'medium',
          `The same ${family} capability reappears with later-grade texts, language demands, and independence; this is a spiral reference, not a rigid prerequisite.`,
        );
      }
    }
  }

  for (let grade = 1; grade <= 12; grade += 1) {
    const links = [
      ['PII', 1, 'PI', 6, 'supports', 'Text-structure knowledge supports close reading and reconstruction of meaning.'],
      ['PI', 8, 'PI', 6, 'supports', 'Vocabulary and language-resource analysis supports reading comprehension.'],
      ['PI', 6, 'PI', 7, 'supports', 'Close reading supports evaluating how ideas and arguments are developed.'],
      ['PI', 7, 'PI', 11, 'supports', 'Evaluating support in texts informs the learner\'s own argument and evidence choices.'],
      ['PII', 2, 'PI', 10, 'supports', 'Cohesion supports organized literary and informational writing.'],
      ['PI', 3, 'PI', 11, 'future_dependency', 'Negotiating opinions develops toward justifying and evaluating arguments.'],
    ];
    for (const [fromFamily, fromNumber, toFamily, toNumber, relationship, reason] of links) {
      addEdge(edges, nodeIds, findNode(grade, fromFamily, fromNumber), findNode(grade, toFamily, toNumber), relationship, relationship === 'supports' ? 'medium' : 'low', reason);
    }
  }

  return [...edges.values()].sort((a, b) => a.from.localeCompare(b.from) || a.to.localeCompare(b.to) || a.relationship.localeCompare(b.relationship));
}

function generatedAt(files) {
  const latest = Math.max(...files.map((filename) => fs.statSync(path.join(SOURCE_FOLDER, filename)).mtimeMs));
  return new Date(latest).toISOString();
}

function gradeMarkdown(grade, nodes) {
  const gradeNodes = nodes.filter((node) => node.grade === grade);
  const strands = new Map();
  for (const node of gradeNodes) {
    if (!strands.has(node.strandCode)) strands.set(node.strandCode, { name: node.strandName, subStrands: new Map() });
    const subStrands = strands.get(node.strandCode).subStrands;
    if (!subStrands.has(node.subStrandCode)) subStrands.set(node.subStrandCode, { name: node.subStrandName, nodes: [] });
    subStrands.get(node.subStrandCode).nodes.push(node);
  }
  const lines = [
    `# California Common Core ELA — Grade ${grade}`,
    '',
    '> Reference benchmark only. Benchmarks inform. They do not command.',
    '',
    `This grade-equivalence view contains ${gradeNodes.length} PI/PII benchmark nodes. ELA capabilities spiral across grades; this page is reference terrain rather than a fixed learning path.`,
    '',
  ];
  for (const [strandCode, strand] of strands) {
    lines.push(`## ${strandCode}: ${strand.name}`, '');
    for (const [subStrandCode, subStrand] of strand.subStrands) {
      lines.push(`### ${subStrandCode}: ${subStrand.name}`, '');
      for (const node of subStrand.nodes) {
        lines.push(`#### ${node.standardCode}`, '', node.standardText, '', `**UCC capability tags:** ${node.uccCapabilityTags.length ? node.uccCapabilityTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '');
        if (node.skillExamples.length) lines.push('**Skill examples:**', '', ...node.skillExamples.map((example) => `- ${example}`), '');
      }
    }
  }
  lines.push('## Related diagrams', '', '- [Reading comprehension progression](../mermaid/reading_comprehension_progression.md)', '- [Argument and evidence progression](../mermaid/argument_evidence_progression.md)', '- [Sample learner heat map](../mermaid/sample_learner_heatmap.md)', '');
  return lines.join('\n');
}

function ontologyMarkdown(nodes, edges) {
  return `# California Common Core ELA Benchmark Ontology

> **Benchmarks inform. They do not command.**

## What this pack is

This pack is a reference benchmark layer for UnCommon Core / Hermes Thrice Great. It converts the supplied California ELA PI/PII sections into ${nodes.length} grade-qualified nodes and ${edges.length} transparent, editable relationships. It offers grade-equivalence terrain, capability tags, and visual maps.

## What this pack is not

It is not UCC's curriculum authority, a fixed grade staircase, or evidence that a learner can perform a capability. The School Model Canvas remains the macro educational authority. Learning Campaigns remain the active plan.

## Extraction scope

The source files contain a PI/PII English-language-development ontology followed by other ELA standard families. This schema extracts the explicitly specified PI and PII strands, sub-strands, standards, and trailing skill examples. It preserves all raw files unchanged. IDs include source grade, so shared 9–10 and 11–12 band codes remain collision-safe.

## Spiraling strands and edge meanings

ELA develops through overlapping comprehension, vocabulary, writing, argument, language, speaking/listening, research, media-literacy, and style strands. \`spiral_progression\` links a recurring capability across grades without claiming strict order. \`supports\` describes a useful cross-strand contribution. \`prerequisite_for\` and \`future_dependency\` are editable hypotheses, never learner diagnoses. \`parallel_strand\` identifies capabilities that may develop alongside one another.

## Evidence and planning

Reader Engine receipts can map comprehension, vocabulary, explanation, and evidence use to nodes. Writer's White Board artifacts can map organization, claims, evidence, conventions, revision, and style. Quiz receipts and parent observations add evidence but do not change the benchmark's reference-only role. Learning Campaign Builder should consult the School Model Canvas and receipts before selecting benchmark-aligned targets.

## Learner overlays and heat maps

The overlay schema stores learner status separately from the benchmark. Missing data means \`no_evidence\`, not inability. Hermes may join overlay entries to node IDs and render an ad hoc Mermaid diagnostic; these heat maps are not core app UI or permanent learner labels.

## Commands

\`\`\`bash
node benchmarks/ca_common_core_ela/scripts/ingest_ca_common_core_ela.js
node benchmarks/ca_common_core_ela/scripts/generate_mermaid_diagrams.js
node benchmarks/ca_common_core_ela/scripts/validate_benchmark_pack.js
node benchmarks/ca_common_core_ela/tests/benchmark_pack_smoke_test.js
\`\`\`
`;
}

function hermesInstructions() {
  return `# Instructions to Hermes Thrice Great — ELA Benchmark Pack

## Governing doctrine

**Benchmarks inform. They do not command.**

This benchmark pack is reference terrain, not curriculum authority. SchoolModelCanvas.md is the mission. Learning Campaigns are the active plan. Reader Engine receipts, writing artifacts, quiz receipts, parent observations, and campaign outcomes are evidence. Hermes interprets and orchestrates. The parent is the final decision-maker.

\`\`\`mermaid
flowchart TD
  SMC["SchoolModelCanvas.md<br/>Family educational constitution"]
  LC["Learning Campaigns<br/>Active weekly/monthly priorities"]
  Reader["Reader Engine Receipts<br/>Highlights, quizzes, comprehension, explanations"]
  Writer["Writing Artifacts<br/>Drafts, outlines, claims, evidence"]
  Benchmarks["CA Common Core ELA Benchmark Pack<br/>Reference terrain map"]
  Hermes["Hermes Thrice Great<br/>Interpretation + orchestration"]
  Parent["Parent Coach<br/>Final judgment"]
  Plan["Next Move / Weekly Plan"]
  Heatmap["Ad hoc Mermaid ELA Heat Map<br/>Optional diagnostic artifact"]
  SMC --> Hermes
  LC --> Hermes
  Reader --> Hermes
  Writer --> Hermes
  Benchmarks --> Hermes
  Hermes --> Parent
  Parent --> Plan
  Hermes --> Heatmap
\`\`\`

## Interpretation order

1. Begin with the School Model Canvas and active Learning Campaign.
2. Read receipts and artifacts; distinguish demonstrated evidence from impressions.
3. Map evidence to one or more capability strands and benchmark nodes.
4. Use edges as diagnostic hypotheses, remembering that ELA spirals rather than marching in a single sequence.
5. Recommend the smallest evidence-producing next move for parent judgment.

Treat ELA as overlapping strands: reading comprehension; vocabulary and morphology; literary analysis; informational-text analysis; writing structure; argument, claim, and evidence; research and citation; rhetoric and media literacy; speaking/listening/collaboration; and language conventions.

Prefer language such as **needs evidence**, **currently developing**, **foundational repair**, **current-grade target**, **future dependency**, **benchmark-aligned**, **strength area**, **stretch area**, and **maintenance area**. Do not reduce the learner to comparative grade labels or use demeaning ability labels.

## Evidence-to-campaign example

- **Evidence:** Recent Reader Engine work shows Aria can identify main idea but needs more support connecting evidence to an explanation.
- **Benchmark lens:** This maps to the Grade 3–6 chain: main idea → inference → supporting details → claim/evidence → argument tracing.
- **Interpretation:** Treat this as an explanation-and-evidence campaign, not a generic reading weakness.
- **Recommended campaign:** Evidence Before Opinion.
- **Parent move:** Ask, “What sentence in the text proves that?”

## Heat-map guardrails

Generate Mermaid heat maps only as ad hoc diagnostics, never as core app UI or permanent identity labels. Use real overlay data, show evidence strength, and render unobserved nodes as \`no_evidence\`. A weekly artifact may be named \`aria_ela_heatmap_weekXX.md\`. The included sample is fictional and must never be presented as learner evidence.

\`\`\`mermaid
flowchart LR
  E["Receipts and artifacts"] --> O["Learner overlay"]
  B["ELA terrain map"] --> O
  O --> Q{"Enough evidence?"}
  Q -->|"yes"| C["Campaign recommendation"]
  Q -->|"no"| N["Needs evidence"]
  C --> P["Parent judgment"]
\`\`\`
`;
}

function main() {
  ensureDirectories();
  const files = sourceFiles();
  copyRawFiles(files);
  const nodes = files.flatMap(parseFile).sort(compareNodes);
  const edges = buildEdges(nodes);
  const timestamp = generatedAt(files);
  const nodeIds = new Set(nodes.map((node) => node.id));
  if (nodeIds.size !== nodes.length) throw new Error('Duplicate ELA node IDs were generated');

  writeJson(path.join(ONTOLOGY_FOLDER, 'standards_nodes.json'), {
    schema_version: 'ca_common_core_ela_nodes.v1',
    benchmark_system: 'California Common Core ELA',
    role: 'reference_only',
    generated_at: timestamp,
    source_folder: SOURCE_FOLDER,
    nodes,
  });
  writeJson(path.join(ONTOLOGY_FOLDER, 'prerequisite_edges.json'), {
    schema_version: 'ca_common_core_ela_edges.v1',
    benchmark_system: 'California Common Core ELA',
    role: 'reference_only',
    generated_at: timestamp,
    edges,
  });
  writeJson(path.join(ONTOLOGY_FOLDER, 'ucc_capability_tags.json'), {
    schema_version: 'ucc_ela_capability_tags.v1',
    tags: TAGS,
  });
  writeJson(path.join(ONTOLOGY_FOLDER, 'learner_overlay_schema.json'), {
    schema_version: 'learner_benchmark_overlay.v1',
    description: 'A learner-specific overlay that marks benchmark ELA standards as mastered, learning, weak, no_evidence, advanced, or not_applicable.',
    node_status_values: ['mastered', 'learning', 'weak', 'no_evidence', 'advanced', 'not_applicable'],
    evidence_strength_values: ['low', 'medium', 'high'],
    example: {
      learnerId: 'aria',
      benchmarkSystem: 'CA Common Core ELA',
      generatedAt: '2026-06-27',
      nodes: [{
        standardId: 'CA.CCSS.ELA.4.PI.4.6',
        status: 'learning',
        evidenceStrength: 'medium',
        latestEvidenceDate: '2026-06-22',
        evidenceSources: ['reader_engine_receipt_2026_06_22'],
        notes: 'Can identify main idea with support, but inference and evidence explanation need more observation.',
      }],
    },
  });

  const countsByGrade = Object.fromEntries(GRADES.map((grade) => [grade, nodes.filter((node) => node.grade === grade).length]));
  writeJson(path.join(ONTOLOGY_FOLDER, 'manifest.json'), {
    schema_version: 'ca_common_core_ela_manifest.v1',
    benchmark_system: 'California Common Core ELA',
    role: 'reference_only',
    generated_at: timestamp,
    source_folder: SOURCE_FOLDER,
    source_files: files.map((filename) => ({ filename, grade: gradeFromFilename(filename), sha256: sha256(path.join(SOURCE_FOLDER, filename)) })),
    extraction_scope: 'PI and PII strands defined by the approved implementation specification',
    counts: { nodes: nodes.length, edges: edges.length, nodes_by_grade: countsByGrade },
    generation: {
      ingest: 'node benchmarks/ca_common_core_ela/scripts/ingest_ca_common_core_ela.js',
      diagrams: 'node benchmarks/ca_common_core_ela/scripts/generate_mermaid_diagrams.js',
      validate: 'node benchmarks/ca_common_core_ela/scripts/validate_benchmark_pack.js',
      smoke_test: 'node benchmarks/ca_common_core_ela/tests/benchmark_pack_smoke_test.js',
    },
  });

  writeText(path.join(MARKDOWN_FOLDER, 'ca_common_core_ela_ontology.md'), ontologyMarkdown(nodes, edges));
  for (const grade of GRADES) writeText(path.join(MARKDOWN_FOLDER, `grade_${grade}.md`), gradeMarkdown(grade, nodes));
  writeText(path.join(MARKDOWN_FOLDER, 'instructions_to_hermes_thrice_great.md'), hermesInstructions());
  console.log(`Ingested ${files.length} ELA source files into ${nodes.length} nodes and ${edges.length} edges.`);
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(`ELA ingest failed: ${error.message}`);
    process.exitCode = 1;
  }
}
