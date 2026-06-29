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
const GRADES = ['KG', '1', '2', '3', '4', '5', '6', '7', '8', 'HS'];

const TAGS = [
  ['counting_cardinality', 'Counting and cardinality', 'Number names, count sequence, cardinality, one-to-one correspondence.'],
  ['additive_reasoning', 'Additive reasoning', 'Addition/subtraction situations, composing/decomposing, comparison, unknowns.'],
  ['word_problem_schema', 'Word-problem schema', 'Recognizing what kind of problem is being asked before computing.'],
  ['operation_selection', 'Operation selection', 'Choosing addition, subtraction, multiplication, division, ratio, equation, or model.'],
  ['multiplicative_reasoning', 'Multiplicative reasoning', 'Equal groups, arrays, multiplicative comparison, factors, multiples.'],
  ['place_value_base_ten', 'Place value and base ten', 'Base-ten structure, regrouping, multi-digit operations, decimals.'],
  ['fraction_decimal_reasoning', 'Fraction and decimal reasoning', 'Fractions, decimals, equivalence, operations, magnitude.'],
  ['ratio_proportional_reasoning', 'Ratio and proportional reasoning', 'Ratios, rates, percents, proportional relationships.'],
  ['algebra_expressions_equations', 'Expressions and equations', 'Variables, expressions, equations, inequalities, systems.'],
  ['functions_modeling', 'Functions and modeling', 'Functions, linear relationships, exponential/quadratic models, interpretation.'],
  ['modeling', 'Mathematical modeling', 'Representing a situation mathematically, interpreting results, and revising a model.'],
  ['geometry_spatial_reasoning', 'Geometry and spatial reasoning', 'Shapes, transformations, congruence, similarity, area, volume.'],
  ['measurement_units', 'Measurement and units', 'Length, area, volume, unit conversion, dimensional reasoning.'],
  ['data_statistics_probability', 'Data, statistics, and probability', 'Graphs, data displays, distributions, probability, inference.'],
  ['fluency_automaticity', 'Fluency and automaticity', 'Speed plus correctness; foundational skills becoming automatic.'],
  ['explanation_reasoning', 'Explanation and reasoning', 'Explaining why a method works; justifying steps and conclusions.'],
].map(([id, label, description]) => ({ id, label, description }));

const TAG_RULES = [
  ['counting_cardinality', /count|cardinality|number names|count sequence|one-to-one/i],
  ['additive_reasoning', /addition|subtraction|\badd\b|\bsubtract\b|additive/i],
  ['word_problem_schema', /word problem|real-world|situation|context/i],
  ['operation_selection', /operation|equation|expression|unknown|variable/i],
  ['multiplicative_reasoning', /multiplication|division|equal groups|arrays?|factor|multiple/i],
  ['place_value_base_ten', /place value|base[- ]ten|digit|hundred|thousand|decimal place/i],
  ['fraction_decimal_reasoning', /fraction|decimal/i],
  ['ratio_proportional_reasoning', /\bratios?\b|\brates?\b|\bpercent|proportional/i],
  ['algebra_expressions_equations', /linear|slope|function|graph|y\s*=|equation|system|expression|variable|inequalit/i],
  ['functions_modeling', /function|model|exponential|quadratic/i],
  ['geometry_spatial_reasoning', /shape|geometry|angle|triangle|area|volume|transform|rotation|reflection|translation|congruence|similar|pythagorean/i],
  ['measurement_units', /measure|length|unit|time|money|volume|area|convert/i],
  ['data_statistics_probability', /data|graph|plot|statistics|probability|distribution|scatter/i],
  ['fluency_automaticity', /fluently|from memory|know from memory|automatic/i],
  ['explanation_reasoning', /explain|justify|reason|argument|prove/i],
];

function ensureDirectories() {
  for (const folder of [RAW_FOLDER, ONTOLOGY_FOLDER, MARKDOWN_FOLDER]) {
    fs.mkdirSync(folder, { recursive: true });
  }
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

function sourceFiles() {
  if (!fs.existsSync(SOURCE_FOLDER)) {
    throw new Error(`Source folder does not exist: ${SOURCE_FOLDER}`);
  }
  const files = fs.readdirSync(SOURCE_FOLDER)
    .filter((name) => /\.txt$/i.test(name) && /Grade\s+(KG|[1-8]|HS)\.txt$/i.test(name))
    .sort((a, b) => gradeIndex(gradeFromFilename(a)) - gradeIndex(gradeFromFilename(b)) || a.localeCompare(b));
  const foundGrades = new Set(files.map(gradeFromFilename));
  const missing = GRADES.filter((grade) => !foundGrades.has(grade));
  if (missing.length) throw new Error(`Missing source grade files: ${missing.join(', ')}`);
  return files;
}

function gradeFromFilename(filename) {
  const match = filename.match(/Grade\s+(KG|[1-8]|HS)\.txt$/i);
  if (!match) throw new Error(`Cannot detect grade from filename: ${filename}`);
  return match[1].toUpperCase();
}

function gradeIndex(grade) {
  return GRADES.indexOf(String(grade));
}

function copyRawFiles(files) {
  for (const filename of files) {
    const source = path.join(SOURCE_FOLDER, filename);
    const target = path.join(RAW_FOLDER, filename);
    if (!fs.existsSync(target) || sha256(source) !== sha256(target)) {
      fs.copyFileSync(source, target);
    }
  }
}

function parseDomain(line, grade) {
  const elementary = line.match(/^((?:K|[1-8])\.([A-Z]+))\s+(.+)$/);
  if (elementary && (grade === 'KG' || elementary[1].startsWith(`${grade}.`))) {
    return { domainCode: elementary[2], domainName: elementary[3].trim() };
  }
  const highSchool = line.match(/^([A-Z]+-[A-Z]+)\s+(.+)$/);
  if (grade === 'HS' && highSchool) {
    return { domainCode: highSchool[1], domainName: highSchool[2].trim() };
  }
  return null;
}

function parseStandard(line, grade) {
  const regular = line.match(/^((?:(?:K|[1-8])\.[A-Z]+|[A-Z]+-[A-Z]+)\.\d+(?:\.[a-z])?)\s+(.+)$/);
  if (regular) return { standardCode: regular[1], standardText: regular[2].trim() };
  const practice = grade === 'HS' ? line.match(/^(MP\d+)\s+(.+)$/) : null;
  if (practice) return { standardCode: practice[1], standardText: practice[2].trim(), mathematicalPractice: true };
  return null;
}

function isSkillExample(line) {
  return /\([A-Z0-9]+(?:-[A-Z0-9]+)?\.[A-Z0-9]*\)$|\([A-Z0-9]+\)$/i.test(line);
}

function uniqueSorted(values) {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b));
}

function tagsFor(node) {
  const text = [node.domainName, node.clusterText, node.standardText, ...node.skillExamples].join(' ');
  const tags = new Set();
  for (const [tag, rule] of TAG_RULES) if (rule.test(text)) tags.add(tag);
  if (/word problem|real-world|situation|context/i.test(text)) {
    tags.add('word_problem_schema');
    tags.add('modeling');
  }
  return [...tags].sort();
}

function progressionTagsFor(node) {
  const text = `${node.clusterText} ${node.standardText}`;
  const tags = new Set([`grade${node.grade}_core`, `${node.domainCode.toLowerCase().replace(/[^a-z0-9]+/g, '_')}_progression`]);
  if (/multiplicative comparison/i.test(text)) tags.add('multiplicative_comparison');
  if (/word problem/i.test(text)) tags.add('word_problem_progression');
  if (/fraction|decimal/i.test(text)) tags.add('fractions_progression');
  if (/ratio|rate|percent|proportional/i.test(text)) tags.add('proportional_progression');
  if (/function|linear|slope/i.test(text)) tags.add('functions_progression');
  return [...tags].sort();
}

function parseFile(filename) {
  const grade = gradeFromFilename(filename);
  const lines = fs.readFileSync(path.join(SOURCE_FOLDER, filename), 'utf8').replace(/\r\n/g, '\n').split('\n');
  const parsed = [];
  let domain = null;
  let clusterText = '';
  let current = null;
  let currentIsPractice = false;

  for (const originalLine of lines) {
    const line = originalLine.trim();
    if (!line) continue;

    const nextDomain = parseDomain(line, grade);
    if (nextDomain) {
      domain = nextDomain;
      clusterText = '';
      current = null;
      currentIsPractice = false;
      continue;
    }

    const standard = parseStandard(line, grade);
    if (standard) {
      if (standard.mathematicalPractice) {
        domain = { domainCode: 'MP', domainName: 'Standards for Mathematical Practice' };
        clusterText = 'Mathematical practice.';
      }
      if (!domain) throw new Error(`${filename}: standard ${standard.standardCode} appears before a domain heading`);
      current = {
        id: `CA.CCSS.Math.${standard.standardCode}`,
        system: 'CA Common Core',
        subject: 'Math',
        grade,
        domainCode: domain.domainCode,
        domainName: domain.domainName,
        clusterText,
        standardCode: standard.standardCode,
        standardText: standard.standardText,
        skillExamples: [],
        checkpoints: [],
        uccCapabilityTags: [],
        progressionTags: [],
        sourceFile: filename,
      };
      parsed.push(current);
      currentIsPractice = Boolean(standard.mathematicalPractice);
      continue;
    }

    if (/^Checkpoint(?: opportunity|:)/i.test(line)) {
      if (current) current.checkpoints.push(line);
      continue;
    }

    if (current && isSkillExample(line)) {
      current.skillExamples.push(line);
      continue;
    }

    if (current && currentIsPractice) {
      current.standardText = `${current.standardText} ${line}`;
      currentIsPractice = false;
      continue;
    }

    // HS category labels (for example, "A Algebra") are organizational, not domains.
    if (grade === 'HS' && /^[A-Z]\s+.+/.test(line)) {
      current = null;
      currentIsPractice = false;
      clusterText = '';
      continue;
    }

    // Remaining prose between standards is the cluster heading for the next standard.
    clusterText = line;
    current = null;
    currentIsPractice = false;
  }

  return parsed;
}

function mergeNodes(nodes) {
  const byId = new Map();
  for (const node of nodes) {
    const existing = byId.get(node.id);
    if (!existing) {
      byId.set(node.id, node);
      continue;
    }
    const normalizeRepeatedText = (text) => text.normalize('NFKC').replace(/[–—−]/g, '-').replace(/\s/g, '');
    const existingNormalized = normalizeRepeatedText(existing.standardText);
    const nodeNormalized = normalizeRepeatedText(node.standardText);
    const sameTextIgnoringFormatting = existingNormalized === nodeNormalized;
    const isPrefixVariant = existingNormalized.startsWith(nodeNormalized) || nodeNormalized.startsWith(existingNormalized);
    if ((!sameTextIgnoringFormatting && !isPrefixVariant) || existing.domainCode !== node.domainCode) {
      throw new Error(`Conflicting repeated standard: ${node.standardCode}`);
    }
    if (node.standardText.length > existing.standardText.length) existing.standardText = node.standardText;
    existing.skillExamples.push(...node.skillExamples);
    existing.checkpoints.push(...node.checkpoints);
    if (!existing.clusterText && node.clusterText) existing.clusterText = node.clusterText;
  }
  const merged = [...byId.values()];
  for (const node of merged) {
    node.skillExamples = uniqueSorted(node.skillExamples);
    node.checkpoints = uniqueSorted(node.checkpoints);
    node.uccCapabilityTags = tagsFor(node);
    node.progressionTags = progressionTagsFor(node);
  }
  return merged.sort(compareNodes);
}

function codeParts(code) {
  const number = code.match(/\.(\d+)(?:\.([a-z]))?$/);
  return { number: number ? Number(number[1]) : 999, nested: number && number[2] ? number[2] : '' };
}

function compareNodes(a, b) {
  const gradeDifference = gradeIndex(a.grade) - gradeIndex(b.grade);
  if (gradeDifference) return gradeDifference;
  const domainDifference = a.domainCode.localeCompare(b.domainCode);
  if (domainDifference) return domainDifference;
  const pa = codeParts(a.standardCode);
  const pb = codeParts(b.standardCode);
  return pa.number - pb.number || pa.nested.localeCompare(pb.nested) || a.standardCode.localeCompare(b.standardCode);
}

function addEdge(map, nodeIds, fromCode, toCode, relationship, confidence, reason) {
  const from = `CA.CCSS.Math.${fromCode}`;
  const to = `CA.CCSS.Math.${toCode}`;
  if (!nodeIds.has(from) || !nodeIds.has(to) || from === to) return;
  const key = `${from}|${to}|${relationship}`;
  if (!map.has(key)) map.set(key, { from, to, relationship, confidence, reason });
}

function buildEdges(nodes) {
  const nodeIds = new Set(nodes.map((node) => node.id));
  const edges = new Map();
  const elementary = nodes.filter((node) => node.grade !== 'HS');
  const byDomainGrade = new Map();
  for (const node of elementary) {
    const key = `${node.domainCode}|${node.grade}`;
    if (!byDomainGrade.has(key)) byDomainGrade.set(key, []);
    byDomainGrade.get(key).push(node);
  }
  for (const domainCode of uniqueSorted(elementary.map((node) => node.domainCode))) {
    const progressionGrades = ['KG', '1', '2', '3', '4', '5', '6', '7', '8'];
    for (let index = 0; index < progressionGrades.length - 1; index += 1) {
      const fromGrade = progressionGrades[index];
      const toGrade = progressionGrades[index + 1];
      const fromNodes = byDomainGrade.get(`${domainCode}|${fromGrade}`) || [];
      const toNodes = byDomainGrade.get(`${domainCode}|${toGrade}`) || [];
      for (const fromNode of fromNodes) {
        const fromNumber = codeParts(fromNode.standardCode).number;
        const candidates = toNodes.filter((node) => codeParts(node.standardCode).number === fromNumber);
        if (candidates.length) {
          addEdge(edges, nodeIds, fromNode.standardCode, candidates[0].standardCode, 'official_progression', 'medium', `Preserves the California grade sequence for nearby ${domainCode} standards with the same standard number.`);
        }
      }
    }
  }

  const curated = [
    ['K.OA.2', '1.OA.1', 'high', 'First-grade additive word-problem schemas build on representing addition and subtraction situations.'],
    ['1.OA.1', '2.OA.1', 'high', 'One- and two-step additive word problems extend first-grade situation and unknown-position schemas.'],
    ['2.OA.1', '3.OA.3', 'medium', 'Multiplicative word problems reuse earlier practices for representing situations, unknowns, and equations.'],
    ['2.OA.4', '3.OA.1', 'high', 'Repeated addition and arrays provide a foundation for interpreting products as equal groups.'],
    ['3.OA.3', '4.OA.2', 'high', 'Multiplicative comparison problems depend on multiplication and division situation schemas.'],
    ['3.OA.3', '4.OA.3', 'high', 'Multi-step four-operation problems depend on multiplication and division situation schemas.'],
    ['2.OA.1', '4.OA.3', 'medium', 'Multi-step four-operation word problems depend on earlier one- and two-step additive word-problem schemas.'],
    ['3.NF.3', '4.NF.1', 'high', 'Fraction equivalence in grade 4 extends grade 3 equivalence and comparison concepts.'],
    ['4.NF.4', '5.NF.4', 'high', 'Multiplying fractions in grade 5 extends whole-number-by-fraction multiplication.'],
    ['5.NF.7', '6.RP.1', 'medium', 'Fraction division supports reasoning about ratios and rates with non-whole quantities.'],
    ['6.RP.3', '7.RP.2', 'high', 'Recognizing proportional relationships extends ratio and rate problem solving.'],
    ['7.RP.2', '8.EE.5', 'high', 'Slope in proportional graphs depends on constants of proportionality and unit-rate reasoning.'],
    ['8.EE.5', '8.F.3', 'high', 'Understanding slope and proportional graphs supports interpreting linear functions.'],
    ['8.F.3', 'F-IF.4', 'medium', 'High-school function interpretation extends grade 8 classification and comparison of functions.'],
    ['7.SP.1', '8.SP.1', 'medium', 'Bivariate data analysis extends sampling and statistical reasoning.'],
    ['8.SP.3', 'S-ID.6', 'medium', 'Linear modeling of bivariate data extends informal line-of-best-fit reasoning.'],
    ['8.G.2', 'G-CO.2', 'medium', 'High-school transformation functions extend grade 8 rigid-motion reasoning.'],
  ];
  for (const [from, to, confidence, reason] of curated) {
    addEdge(edges, nodeIds, from, to, 'prerequisite_for', confidence, reason);
  }
  return [...edges.values()].sort((a, b) => a.from.localeCompare(b.from) || a.to.localeCompare(b.to) || a.relationship.localeCompare(b.relationship));
}

function generatedAt(files) {
  const latest = Math.max(...files.map((filename) => fs.statSync(path.join(SOURCE_FOLDER, filename)).mtimeMs));
  return new Date(latest).toISOString();
}

function gradeMarkdown(grade, nodes) {
  const gradeNodes = nodes.filter((node) => node.grade === grade);
  const domains = new Map();
  for (const node of gradeNodes) {
    if (!domains.has(node.domainCode)) domains.set(node.domainCode, { name: node.domainName, nodes: [] });
    domains.get(node.domainCode).nodes.push(node);
  }
  const lines = [
    `# California Common Core Math — Grade ${grade}`,
    '',
    '> Reference benchmark only. Benchmarks inform. They do not command.',
    '',
    `This grade-equivalence view contains ${gradeNodes.length} benchmark nodes across ${domains.size} domains. It is terrain for diagnosis and planning, not a fixed learning path.`,
    '',
  ];
  for (const [domainCode, domain] of [...domains.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    lines.push(`## ${domainCode}: ${domain.name}`, '');
    for (const node of domain.nodes) {
      lines.push(`### ${node.standardCode}`, '', node.clusterText ? `**Cluster:** ${node.clusterText}` : '**Cluster:** Not stated in source.', '', node.standardText, '');
      lines.push(`**UCC capability tags:** ${node.uccCapabilityTags.length ? node.uccCapabilityTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '');
      if (node.skillExamples.length) {
        lines.push('**Skill examples:**', '', ...node.skillExamples.map((example) => `- ${example}`), '');
      }
      if (node.checkpoints.length) {
        lines.push('**Checkpoints:**', '', ...node.checkpoints.map((checkpoint) => `- ${checkpoint}`), '');
      }
    }
  }
  lines.push('## Related diagrams', '', '- [Progression spine](../mermaid/progression_spine.md)', '- [Word-problem schema chain](../mermaid/word_problem_schema_chain.md)', '- [Sample learner heat map](../mermaid/sample_learner_heatmap.md)', '');
  return lines.join('\n');
}

function ontologyMarkdown(nodes, edges) {
  return `# California Common Core Math Benchmark Ontology

> **Benchmarks inform. They do not command.**

## What this pack is

This pack is a reference benchmark layer for UnCommon Core / Hermes Thrice Great. It turns the supplied California Common Core Math text into ${nodes.length} standards nodes and ${edges.length} transparent, editable progression or prerequisite edges. It provides grade-equivalence terrain, capability tags, and visual maps.

## What this pack is not

It is not UCC's curriculum authority, a prescription that a learner move linearly, or proof of mastery. The School Model Canvas remains the macro educational authority. Assessment receipts remain the evidence layer. Learning Campaigns remain the active plan.

## From source text to ontology

Each detected domain, cluster, standard, skill example, and checkpoint is preserved on a deterministic node ID of the form \`CA.CCSS.Math.{standardCode}\`. Repeated high-school standards are merged by ID; their skill examples and checkpoints are deduplicated. Keyword rules assign readable UCC capability tags. The raw files are copied unchanged into \`raw/\`.

## Edge meanings

- \`official_progression\` preserves nearby grade sequence within a California domain family. Confidence is \`medium\`; it is a navigation aid, not an official claim that one individual standard is the sole prerequisite for another.
- \`prerequisite_for\` is an editable inference based on named math progressions. Its \`low\`, \`medium\`, or \`high\` confidence reports heuristic strength.

## Using the pack

Hermes should begin with receipts, then use nodes and edges to locate a current-grade target, foundational repair, future dependency, or area that needs evidence. Learning Campaign Builder may select benchmark-aligned targets after consulting the School Model Canvas and current evidence; it must not substitute the grade map for learner-specific judgment.

## Learner overlays and heat maps

The overlay schema stores learner-specific status and evidence strength separately from the reference ontology. A heat map joins overlay records to node IDs and may render an ad hoc Mermaid diagnostic. Missing overlay data means \`no_evidence\`, not inability. Heat maps are diagnostic artifacts, not core app UI and not permanent labels.

## Nonlinear development

California's grade sequence is retained because it is useful reference terrain. A learner may nevertheless show advanced evidence in one branch, foundational repair in another, and no evidence elsewhere. Plans should follow dependencies and receipts rather than forcing the learner through a single age-graded path.

## Commands

\`\`\`bash
node benchmarks/ca_common_core_math/scripts/ingest_ca_common_core_math.js
node benchmarks/ca_common_core_math/scripts/generate_mermaid_diagrams.js
node benchmarks/ca_common_core_math/scripts/validate_benchmark_pack.js
node benchmarks/ca_common_core_math/tests/benchmark_pack_smoke_test.js
\`\`\`
`;
}

function hermesInstructions() {
  return `# Instructions to Hermes Thrice Great

## Governing doctrine

**Benchmarks inform. They do not command.**

This pack is a reference layer. The School Model Canvas remains the macro educational authority. Assessment receipts remain demonstrated evidence. Learning Campaigns remain the active plan. A benchmark node identifies terrain; it does not decide what a learner must study next.

## Decision order

1. Read the relevant School Model Canvas constraints and aims.
2. Read current assessment receipts and note evidence strength.
3. Map demonstrated evidence and open questions to benchmark nodes.
4. Trace prerequisite edges only as diagnostic hypotheses.
5. Propose or update the Learning Campaign using learner-specific evidence.
6. Record what needs evidence; do not infer incapacity from missing data.

Use language such as **foundational repair**, **current-grade target**, **future dependency**, **needs evidence**, **currently developing**, and **benchmark-aligned**. Never shame the learner or flatten the child into a single grade label. Treat development as nonlinear across the graph.

## Diagnostic graph pattern

\`\`\`mermaid
flowchart LR
  R["Assessment receipts"] --> O["Learner overlay"]
  S["School Model Canvas"] --> C["Learning Campaign"]
  B["Benchmark nodes + editable edges"] --> O
  O --> C
  C --> N["Next evidence-producing activity"]
\`\`\`

When a current-grade problem appears, inspect earlier schema dependencies without assuming they are weak:

\`\`\`mermaid
flowchart LR
  A["Current-grade target"] --> Q{"Enough evidence?"}
  Q -->|"yes"| P["Plan next campaign step"]
  Q -->|"no"| E["Mark needs evidence"]
  Q -->|"dependency signal"| F["Test a foundational prerequisite"]
  F --> R["Create a new receipt"]
\`\`\`

## Learner heat maps

Generate Mermaid heat maps only as ad hoc diagnostic artifacts, never as core app UI or permanent identity labels. Join overlay entries to ontology node IDs, show evidence strength in notes or labels, and render unobserved nodes as \`no_evidence\`. A weekly artifact may be named \`aria_math_heatmap_weekXX.md\`, but only when actual overlay data is supplied. The included sample is fictional and must not be presented as learner evidence.

## Guardrails

- Do not treat California grade order as a mandated learning schedule.
- Do not claim mastery without receipts.
- Do not turn a heuristic edge into a diagnosis without evidence.
- Do not summarize the learner with comparative grade labels.
- Keep inferred prerequisite edges transparent and editable.
- Preserve the distinction between benchmark alignment, active plans, and demonstrated evidence.
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
    schema_version: 'ca_common_core_math_nodes.v1',
    benchmark_system: 'California Common Core Math',
    role: 'reference_only',
    generated_at: timestamp,
    source_folder: SOURCE_FOLDER,
    nodes,
  });
  writeJson(path.join(ONTOLOGY_FOLDER, 'prerequisite_edges.json'), {
    schema_version: 'ca_common_core_math_edges.v1',
    benchmark_system: 'California Common Core Math',
    role: 'reference_only',
    generated_at: timestamp,
    edges,
  });
  writeJson(path.join(ONTOLOGY_FOLDER, 'ucc_capability_tags.json'), {
    schema_version: 'ucc_capability_tags.v1',
    tags: TAGS,
  });
  writeJson(path.join(ONTOLOGY_FOLDER, 'learner_overlay_schema.json'), {
    schema_version: 'learner_benchmark_overlay.v1',
    description: 'A learner-specific overlay that marks benchmark standards as mastered, learning, weak, no_evidence, advanced, or not_applicable.',
    node_status_values: ['mastered', 'learning', 'weak', 'no_evidence', 'advanced', 'not_applicable'],
    evidence_strength_values: ['low', 'medium', 'high'],
    example: {
      learnerId: 'aria',
      benchmarkSystem: 'CA Common Core Math',
      generatedAt: '2026-06-27',
      nodes: [{
        standardId: 'CA.CCSS.Math.2.OA.1',
        status: 'weak',
        evidenceStrength: 'medium',
        latestEvidenceDate: '2026-06-22',
        evidenceSources: ['assessment_lab_math_receipt_2026_06_22'],
        notes: 'Operation/schema selection uncertain in mixed word problems.',
      }],
    },
  });

  const sourceManifest = files.map((filename) => ({ filename, grade: gradeFromFilename(filename), sha256: sha256(path.join(SOURCE_FOLDER, filename)) }));
  const countsByGrade = Object.fromEntries(GRADES.map((grade) => [grade, nodes.filter((node) => node.grade === grade).length]));
  writeJson(path.join(ONTOLOGY_FOLDER, 'manifest.json'), {
    schema_version: 'ca_common_core_math_manifest.v1',
    benchmark_system: 'California Common Core Math',
    role: 'reference_only',
    generated_at: timestamp,
    source_folder: SOURCE_FOLDER,
    source_files: sourceManifest,
    counts: { nodes: nodes.length, edges: edges.length, nodes_by_grade: countsByGrade },
    generation: {
      ingest: 'node benchmarks/ca_common_core_math/scripts/ingest_ca_common_core_math.js',
      diagrams: 'node benchmarks/ca_common_core_math/scripts/generate_mermaid_diagrams.js',
      validate: 'node benchmarks/ca_common_core_math/scripts/validate_benchmark_pack.js',
      smoke_test: 'node benchmarks/ca_common_core_math/tests/benchmark_pack_smoke_test.js',
    },
  });

  writeText(path.join(MARKDOWN_FOLDER, 'ca_common_core_math_ontology.md'), ontologyMarkdown(nodes, edges));
  for (const grade of GRADES) writeText(path.join(MARKDOWN_FOLDER, `grade_${grade}.md`), gradeMarkdown(grade, nodes));
  writeText(path.join(MARKDOWN_FOLDER, 'instructions_to_hermes_thrice_great.md'), hermesInstructions());

  console.log(`Ingested ${files.length} source files into ${nodes.length} nodes and ${edges.length} edges.`);
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(`Ingest failed: ${error.message}`);
    process.exitCode = 1;
  }
}
