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

const HISTORICAL_SKILLS = [
  ['chronology', 'Chronology', 'Ordering events, creating timelines, and relating events across time.'],
  ['spatial_thinking', 'Spatial thinking', 'Using maps, regions, location, movement, and geography to explain history.'],
  ['source_analysis', 'Source analysis', 'Using primary and secondary sources, documents, artifacts, and media.'],
  ['point_of_view', 'Point of view', 'Identifying perspective, context, author position, and competing interpretations.'],
  ['cause_effect', 'Cause and effect', 'Explaining short-term and long-term causes, consequences, and correlations.'],
  ['continuity_change', 'Continuity and change', 'Identifying what changed, what persisted, and why.'],
  ['historical_context', 'Historical context', 'Placing people and events in time, place, and social conditions.'],
  ['interpretation', 'Historical interpretation', 'Recognizing that interpretations can differ and change with new evidence.'],
  ['evidence_argument', 'Evidence and argument', 'Making claims, supporting them with evidence, and evaluating claims.'],
].map(([id, label, description]) => ({ id, label, description }));

const CIVIC_TAGS = [
  ['citizenship', 'Citizenship', 'Rights, responsibilities, participation, public virtue, civic life.'],
  ['rules_laws', 'Rules and laws', 'Why societies make rules and laws and how laws are enforced.'],
  ['democracy', 'Democracy', 'Direct democracy, representative democracy, elections, consent of the governed.'],
  ['constitutional_reasoning', 'Constitutional reasoning', 'Constitutional structure, rights, amendments, limits, and interpretation.'],
  ['branches_of_government', 'Branches of government', 'Legislative, executive, judicial functions and checks and balances.'],
  ['federalism', 'Federalism', 'Local, state, federal, tribal powers and relationships.'],
  ['rights_obligations', 'Rights and obligations', 'Civil liberties, civil rights, duties, reciprocity, and civic responsibilities.'],
  ['civil_society', 'Civil society', 'Voluntary associations, media, organizations, religion, public participation.'],
  ['political_systems', 'Political systems', 'Democracy, monarchy, authoritarianism, totalitarianism, socialism, communism, fascism.'],
  ['media_public_opinion', 'Media and public opinion', 'Free press, media influence, public agenda, campaigns, political communication.'],
].map(([id, label, description]) => ({ id, label, description }));

const GEO_ECON_TAGS = [
  ['maps_location', 'Maps and location', 'Maps, grids, latitude/longitude, regions, landmarks, spatial orientation.'],
  ['physical_geography', 'Physical geography', 'Landforms, climate, water, resources, environment, regions.'],
  ['human_geography', 'Human geography', 'Settlements, cities, migration, population, culture, land use.'],
  ['migration_movement', 'Migration and movement', 'Movement of people, goods, ideas, religions, empires, refugees, and diasporas.'],
  ['trade_exchange', 'Trade and exchange', 'Trade routes, markets, goods, cultural diffusion, commerce.'],
  ['scarcity_resources', 'Scarcity and resources', 'Resource limits, production, consumption, land, water, labor, incentives.'],
  ['economic_systems', 'Economic systems', 'Agriculture, industry, capitalism, labor, taxes, public goods, government services.'],
  ['technology_infrastructure', 'Technology and infrastructure', 'Transportation, communications, agriculture, railroads, water systems, industry.'],
].map(([id, label, description]) => ({ id, label, description }));

const UCC_TAGS = [
  ['historical_reasoning', 'Historical reasoning', 'Using time, context, evidence, cause/effect, and continuity/change to explain the past.'],
  ['source_evidence_reasoning', 'Source and evidence reasoning', 'Interpreting sources, assessing credibility, distinguishing fact/opinion, supporting claims.'],
  ['geographic_reasoning', 'Geographic reasoning', 'Using maps, regions, places, movement, and spatial relationships to explain human activity.'],
  ['civic_judgment', 'Civic judgment', 'Reasoning about rights, laws, institutions, citizenship, democracy, and public life.'],
  ['economic_reasoning', 'Economic reasoning', 'Reasoning about resources, production, consumption, trade, incentives, and systems.'],
  ['perspective_taking', 'Perspective-taking', 'Understanding different actors, interests, identities, and points of view.'],
  ['cause_effect_reasoning', 'Cause/effect reasoning', 'Explaining short-term and long-term causes, effects, and unintended consequences.'],
  ['continuity_change_reasoning', 'Continuity/change reasoning', 'Identifying persistence, transformation, reform, rupture, and historical patterns.'],
  ['conundrum_reasoning', 'Conundrum reasoning', 'Reasoning through tradeoffs, dilemmas, competing values, and judgment under uncertainty.'],
  ['narrative_reconstruction', 'Narrative reconstruction', 'Reconstructing events, actors, motives, decisions, and consequences into coherent explanations.'],
  ['map_story_reasoning', 'Map-story reasoning', 'Connecting geography, movement, place, conflict, and historical sequence.'],
].map(([id, label, description]) => ({ id, label, description }));

const HISTORICAL_RULES = [
  ['chronology', /timeline|time line|chronolog|sequence|period|era|BCE|CE|before|after/i],
  ['spatial_thinking', /map|region|location|spatial|geography|migration|expansion|route|settlement|border|territory/i],
  ['source_analysis', /source|primary|secondary|document|artifact|photograph|interview|credibility|evidence/i],
  ['point_of_view', /point of view|perspective|author|context|interpretation|bias|opinion/i],
  ['cause_effect', /cause|effect|consequence|impact|led to|resulted|influence|because/i],
  ['continuity_change', /continuity|change|transformation|evolution|development|growth|decline|rise|fall/i],
  ['historical_context', /context|time and place|conditions|social|political|economic|religious|cultural/i],
  ['interpretation', /interpret|analyze|evaluate|explain|compare|contrast/i],
  ['evidence_argument', /claim|argument|defend|evidence|support|evaluate/i],
];

const CIVIC_RULES = [
  ['citizenship', /citizen|citizenship|civic|public virtue|participation|voting|volunteer/i],
  ['rules_laws', /rule|law|constitution|legal|court|rights|responsibilities/i],
  ['democracy', /democracy|representative|direct democracy|election|consent of the governed/i],
  ['constitutional_reasoning', /Constitution|Bill of Rights|amendment|Declaration of Independence|Federalist|constitutional/i],
  ['branches_of_government', /legislative|executive|judicial|branches|checks and balances|separation of powers/i],
  ['federalism', /federal|state|local|tribal|sovereign|federalism/i],
  ['rights_obligations', /rights|obligations|responsibilities|civil liberties|civil rights|freedom/i],
  ['civil_society', /civil society|religion|media|association|public opinion|press/i],
  ['political_systems', /monarchy|authoritarian|totalitarian|communism|socialism|fascism|political systems/i],
  ['media_public_opinion', /media|press|campaign|poll|advertising|public opinion/i],
];

const GEO_ECON_RULES = [
  ['maps_location', /map|grid|latitude|longitude|coordinate|capital|continent|ocean|river|mountain|region/i],
  ['physical_geography', /landform|climate|water|vegetation|natural environment|resources|physical geography/i],
  ['human_geography', /community|settlement|city|town|population|migration|immigration|culture|land use/i],
  ['migration_movement', /migration|immigration|movement|diaspora|route|expansion|dispersion|exploration/i],
  ['trade_exchange', /trade|commerce|market|merchant|exchange|Silk Road|goods|routes/i],
  ['scarcity_resources', /scarcity|resources|production|consumption|land|water|labor|incentive|supply|demand/i],
  ['economic_systems', /economy|economic|agriculture|industry|capitalism|tax|labor|business|public goods/i],
  ['technology_infrastructure', /technology|infrastructure|transportation|railroad|water system|communications|industry|irrigation/i],
];

const STORY_RULES = [
  ['people', /people|leader|hero|biograph|individual|group|society|class|family/i],
  ['places', /place|region|city|state|country|river|mountain|route|map|geography/i],
  ['pressures', /conflict|competition|war|crisis|problem|obstacle|tension|threat/i],
  ['choices', /decision|choose|choice|policy|law|act|solution|response/i],
  ['consequences', /effect|consequence|impact|result|aftermath|legacy|influence/i],
  ['perspectives', /compare|contrast|point of view|perspective|different|debate|controversy/i],
  ['conundrum', /rights|slavery|conflict|tradeoff|obligation|freedom|justice|moral|ethical/i],
  ['institutions', /government|institution|empire|state|law|constitution|church|court/i],
];

function ensureDirectories() {
  for (const folder of [RAW_FOLDER, ONTOLOGY_FOLDER, MARKDOWN_FOLDER]) fs.mkdirSync(folder, { recursive: true });
}
function writeJson(filePath, value) { fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8'); }
function writeText(filePath, value) { fs.writeFileSync(filePath, value.endsWith('\n') ? value : `${value}\n`, 'utf8'); }
function sha256(filePath) { return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex'); }

function gradeFromFilename(filename) {
  const match = filename.match(/California Common Core Social Studies Grade ([1-8]|HS)\.txt$/i);
  if (!match) throw new Error(`Cannot detect Social Studies grade from filename: ${filename}`);
  return match[1].toUpperCase();
}
function gradeIndex(grade) { return GRADES.indexOf(String(grade)); }
function sourceFiles() {
  if (!fs.existsSync(SOURCE_FOLDER)) throw new Error(`Source folder does not exist: ${SOURCE_FOLDER}`);
  const files = fs.readdirSync(SOURCE_FOLDER).filter((name) => /^California Common Core Social Studies Grade (?:[1-8]|HS)\.txt$/i.test(name)).sort((a, b) => gradeIndex(gradeFromFilename(a)) - gradeIndex(gradeFromFilename(b)) || a.localeCompare(b));
  const found = new Set(files.map(gradeFromFilename));
  const missing = GRADES.filter((grade) => !found.has(grade));
  if (missing.length) throw new Error(`Missing Social Studies source grade files: ${missing.join(', ')}`);
  return files;
}
function copyRawFiles(files) {
  for (const filename of files) {
    const source = path.join(SOURCE_FOLDER, filename);
    const target = path.join(RAW_FOLDER, filename);
    if (!fs.existsSync(target) || sha256(source) !== sha256(target)) fs.copyFileSync(source, target);
  }
}
function isSkillExample(line) { return /\([^\n()]*\)$/.test(line); }
function uniqueSorted(values) { return [...new Set(values)].sort((a, b) => a.localeCompare(b)); }
function tagsFromRules(text, rules) { return rules.filter(([, rule]) => rule.test(text)).map(([tag]) => tag).sort(); }

function applyTags(node) {
  const text = [node.courseTheme, node.strandOrUnit, node.clusterText, node.standardText, ...node.skillExamples].filter(Boolean).join(' ');
  node.historicalReasoningTags = tagsFromRules(text, HISTORICAL_RULES);
  node.civicReasoningTags = tagsFromRules(text, CIVIC_RULES);
  node.geographyEconomicsTags = tagsFromRules(text, GEO_ECON_RULES);
  node.storyMapTags = tagsFromRules(text, STORY_RULES);
  const historical = new Set(node.historicalReasoningTags);
  const civic = new Set(node.civicReasoningTags);
  const geo = new Set(node.geographyEconomicsTags);
  const story = new Set(node.storyMapTags);
  const ucc = new Set();
  if (historical.size) ucc.add('historical_reasoning');
  if (historical.has('source_analysis') || historical.has('evidence_argument')) ucc.add('source_evidence_reasoning');
  if (historical.has('spatial_thinking') || geo.has('maps_location')) ucc.add('geographic_reasoning');
  if (civic.size) ucc.add('civic_judgment');
  if (geo.has('economic_systems') || geo.has('scarcity_resources') || geo.has('trade_exchange')) ucc.add('economic_reasoning');
  if (historical.has('point_of_view') || story.has('perspectives')) ucc.add('perspective_taking');
  if (historical.has('cause_effect')) ucc.add('cause_effect_reasoning');
  if (historical.has('continuity_change')) ucc.add('continuity_change_reasoning');
  if (story.has('conundrum')) ucc.add('conundrum_reasoning');
  if (story.has('people') || story.has('choices') || story.has('consequences')) ucc.add('narrative_reconstruction');
  if (story.has('places') || geo.has('maps_location')) ucc.add('map_story_reasoning');
  node.uccCapabilityTags = [...ucc].sort();
  node.progressionTags = uniqueSorted([`grade${node.grade}_core`, ...node.uccCapabilityTags.map((tag) => `${tag}_progression`)]);
}

function makeNode({ grade, filename, theme, strand, cluster, substandardNumber, standardText, analysisSkillCode = null }) {
  const standardCode = analysisSkillCode ? `ANALYSIS.${analysisSkillCode}` : substandardNumber ? `${cluster.code}.${substandardNumber}` : cluster.code;
  return {
    id: `CA.SS.${grade}.${standardCode}`,
    system: 'California Social Studies',
    subject: 'Social Studies',
    grade,
    courseTheme: theme,
    strandOrUnit: strand || theme,
    clusterCode: analysisSkillCode ? null : cluster.code,
    sourceClusterCode: !analysisSkillCode && cluster.sourceCode !== cluster.code ? cluster.sourceCode : null,
    clusterText: analysisSkillCode ? null : cluster.text,
    substandardNumber: substandardNumber || null,
    analysisSkillCode,
    standardCode,
    standardText,
    skillExamples: [],
    historicalReasoningTags: [],
    civicReasoningTags: [],
    geographyEconomicsTags: [],
    uccCapabilityTags: [],
    storyMapTags: [],
    progressionTags: [],
    skillCoverage: 'no_skills_listed',
    sourceFile: filename,
  };
}

function parseFile(filename) {
  const grade = gradeFromFilename(filename);
  const lines = fs.readFileSync(path.join(SOURCE_FOLDER, filename), 'utf8').replace(/\r\n/g, '\n').split('\n');
  const nodes = [];
  const rawClusterCounts = new Map();
  let theme = '';
  let strand = '';
  let cluster = null;
  let current = null;
  let analysisMode = false;
  let analysisSection = null;

  function finalizeCluster() {
    if (cluster && cluster.substandardCount === 0) {
      const node = makeNode({ grade, filename, theme, strand, cluster, standardText: cluster.text });
      node.skillExamples = uniqueSorted(cluster.skillExamples);
      node.skillCoverage = cluster.noIxl ? 'no_ixl_skills_available' : node.skillExamples.length ? 'skills_available' : 'no_skills_listed';
      nodes.push(node);
    }
    cluster = null;
    current = null;
  }

  function normalizedClusterCode(sourceCode) {
    const count = rawClusterCounts.get(sourceCode) || 0;
    rawClusterCounts.set(sourceCode, count + 1);
    if (grade === '7' && sourceCode === '7.1' && count === 1) return '7.10';
    if (grade === '8' && sourceCode === '8.1' && count === 1) return '8.10';
    return sourceCode;
  }

  for (const originalLine of lines) {
    const line = originalLine.trim();
    if (!line) continue;
    if (/^RH\.6-8\s+Reading$/.test(line)) {
      finalizeCluster();
      break;
    }
    if (line === 'Historical and Social Sciences Analysis Skills') {
      finalizeCluster();
      analysisMode = true;
      analysisSection = null;
      theme = line;
      strand = line;
      continue;
    }
    if (analysisMode && ['Chronological and Spatial Thinking', 'Research, Evidence, and Point of View', 'Historical Interpretation'].includes(line)) {
      analysisSection = {
        code: line === 'Chronological and Spatial Thinking' ? 'CST' : line === 'Research, Evidence, and Point of View' ? 'REPV' : 'HI',
        name: line,
      };
      strand = line;
      current = null;
      continue;
    }
    const numbered = line.match(/^(\d+)\s+(.+)$/);
    if (analysisMode && analysisSection && numbered) {
      current = makeNode({ grade, filename, theme, strand, cluster: null, substandardNumber: numbered[1], standardText: numbered[2].trim(), analysisSkillCode: `${analysisSection.code}.${numbered[1]}` });
      nodes.push(current);
      continue;
    }
    if (analysisMode && current && isSkillExample(line)) {
      current.skillExamples.push(line);
      current.skillCoverage = 'skills_available';
      continue;
    }
    if (analysisMode) {
      analysisMode = false;
      analysisSection = null;
      theme = line;
      strand = line;
      current = null;
      continue;
    }

    const clusterMatch = line.match(/^(\d+\.\d+)\s+(.+)$/);
    if (clusterMatch) {
      finalizeCluster();
      const sourceCode = clusterMatch[1];
      cluster = { sourceCode, code: normalizedClusterCode(sourceCode), text: clusterMatch[2].trim(), substandardCount: 0, skillExamples: [], noIxl: false };
      continue;
    }
    if (cluster && cluster.substandardCount === 0 && /^[a-z]/.test(line)) {
      cluster.text = `${cluster.text}${line}`;
      continue;
    }
    if (cluster && numbered) {
      current = makeNode({ grade, filename, theme, strand, cluster, substandardNumber: numbered[1], standardText: numbered[2].trim() });
      cluster.substandardCount += 1;
      nodes.push(current);
      continue;
    }
    if (/^Skills covering this topic are not currently available on IXL\.$/.test(line)) {
      if (current) current.skillCoverage = 'no_ixl_skills_available';
      else if (cluster) cluster.noIxl = true;
      continue;
    }
    if (isSkillExample(line)) {
      if (current) {
        current.skillExamples.push(line);
        current.skillCoverage = 'skills_available';
      } else if (cluster) {
        cluster.skillExamples.push(line);
      }
      continue;
    }
    finalizeCluster();
    theme = line;
    strand = line;
  }
  finalizeCluster();
  for (const node of nodes) {
    node.skillExamples = uniqueSorted(node.skillExamples);
    applyTags(node);
  }
  return nodes;
}

function mergeNodes(nodes) {
  const byId = new Map();
  for (const node of nodes) {
    const existing = byId.get(node.id);
    if (!existing) { byId.set(node.id, node); continue; }
    if (existing.standardText !== node.standardText || existing.clusterText !== node.clusterText) throw new Error(`Conflicting repeated Social Studies node: ${node.id}`);
    existing.skillExamples = uniqueSorted([...existing.skillExamples, ...node.skillExamples]);
    if (node.skillCoverage === 'no_ixl_skills_available') existing.skillCoverage = node.skillCoverage;
    else if (existing.skillExamples.length) existing.skillCoverage = 'skills_available';
  }
  const merged = [...byId.values()];
  for (const node of merged) applyTags(node);
  return merged.sort((a, b) => gradeIndex(a.grade) - gradeIndex(b.grade) || a.standardCode.localeCompare(b.standardCode, undefined, { numeric: true }));
}

function addEdge(edges, nodeIds, from, to, relationship, confidence, reason) {
  if (!nodeIds.has(from) || !nodeIds.has(to) || from === to) return;
  const key = `${from}|${to}|${relationship}`;
  if (!edges.has(key)) edges.set(key, { from, to, relationship, confidence, reason });
}
function buildEdges(nodes) {
  const ids = new Set(nodes.map((node) => node.id));
  const edges = new Map();
  for (const section of ['CST', 'REPV', 'HI']) {
    const max = section === 'CST' ? 3 : section === 'REPV' ? 5 : 6;
    for (let number = 1; number <= max; number += 1) {
      addEdge(edges, ids, `CA.SS.6.ANALYSIS.${section}.${number}`, `CA.SS.7.ANALYSIS.${section}.${number}`, 'skill_progression', 'medium', 'The same historical-analysis skill is revisited with different content and increasing independence.');
      addEdge(edges, ids, `CA.SS.7.ANALYSIS.${section}.${number}`, `CA.SS.8.ANALYSIS.${section}.${number}`, 'skill_progression', 'medium', 'The same historical-analysis skill is revisited with different content and increasing independence.');
    }
  }
  const curated = [
    ['CA.SS.1.1.1.1', 'CA.SS.3.3.4.1', 'civic_progression', 'Early rule-making and citizenship support later reasoning about laws, constitutions, and civic consequences.'],
    ['CA.SS.2.2.2.1', 'CA.SS.4.4.1.1', 'geography_progression', 'Simple grid location supports later latitude/longitude and regional reasoning.'],
    ['CA.SS.3.3.4.4', 'CA.SS.4.4.5.1', 'civic_progression', 'Understanding government branches supports analysis of local, state, and federal responsibilities.'],
    ['CA.SS.5.5.5.1', 'CA.SS.8.8.1.2', 'historical_progression', 'Grade 5 causes of the American Revolution support Grade 8 analysis of revolutionary ideals and constitutional democracy.'],
    ['CA.SS.5.5.7.1', 'CA.SS.8.8.2.2', 'civic_progression', 'Founding-era constitutional development supports later comparison of the Articles and Constitution.'],
    ['CA.SS.8.8.2.2', 'CA.SS.HS.12.1.1', 'future_dependency', 'Constitutional structure in Grade 8 supports high-school analysis of democratic principles and political thought.'],
    ['CA.SS.8.ANALYSIS.REPV.4', 'CA.SS.8.8.2.2', 'source_analysis_progression', 'Credibility and source analysis support evidence-based constitutional interpretation.'],
    ['CA.SS.5.5.5.1', 'CA.SS.8.8.2.2', 'story_map_dependency', 'A Founding-era Story Map can connect pressures and choices in revolution to constitutional consequences.'],
  ];
  for (const [from, to, relationship, reason] of curated) addEdge(edges, ids, from, to, relationship, relationship === 'future_dependency' ? 'low' : 'high', reason);
  return [...edges.values()].sort((a, b) => a.from.localeCompare(b.from) || a.to.localeCompare(b.to) || a.relationship.localeCompare(b.relationship));
}

function generatedAt(files) {
  const latest = Math.max(...files.map((filename) => fs.statSync(path.join(SOURCE_FOLDER, filename)).mtimeMs));
  return new Date(latest).toISOString();
}

function gradeMarkdown(grade, nodes) {
  const gradeNodes = nodes.filter((node) => node.grade === grade);
  const units = new Map();
  for (const node of gradeNodes) {
    const unit = node.strandOrUnit || node.courseTheme;
    if (!units.has(unit)) units.set(unit, []);
    units.get(unit).push(node);
  }
  const lines = [`# California Social Studies — Grade ${grade}`, '', '> Reference benchmark only. Benchmarks inform. They do not command.', '', `This grade/course view contains ${gradeNodes.length} benchmark nodes. Content and reasoning evidence may develop nonlinearly across history, civics, geography, economics, sources, and Story Maps.`, ''];
  for (const [unit, unitNodes] of units) {
    lines.push(`## ${unit}`, '');
    for (const node of unitNodes) {
      lines.push(`### ${node.standardCode}`, '', node.clusterText && node.substandardNumber ? `**Cluster ${node.clusterCode}:** ${node.clusterText}` : '', node.standardText, '', `**Historical reasoning:** ${node.historicalReasoningTags.length ? node.historicalReasoningTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '', `**Civic reasoning:** ${node.civicReasoningTags.length ? node.civicReasoningTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '', `**Geography/economics:** ${node.geographyEconomicsTags.length ? node.geographyEconomicsTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '', `**UCC capabilities:** ${node.uccCapabilityTags.length ? node.uccCapabilityTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '', `**Story Map tags:** ${node.storyMapTags.length ? node.storyMapTags.map((tag) => `\`${tag}\``).join(', ') : 'Needs manual tagging.'}`, '', `**Skill coverage:** \`${node.skillCoverage}\``, '');
      if (node.sourceClusterCode) lines.push(`**Normalized source code:** ${node.sourceClusterCode} → ${node.clusterCode}`, '');
      if (node.skillExamples.length) lines.push('**Skill examples:**', '', ...node.skillExamples.map((example) => `- ${example}`), '');
    }
  }
  lines.push('## Related diagrams', '', '- [Historical reasoning progression](../mermaid/historical_reasoning_progression.md)', '- [Story Map and conundrum alignment](../mermaid/story_map_conundrum_alignment.md)', '- [Sample learner heat map](../mermaid/sample_learner_heatmap.md)', '');
  return lines.filter((line) => line !== '').join('\n\n');
}

function ontologyMarkdown(nodes, edges) {
  return `# California Social Studies Benchmark Ontology

> **Benchmarks inform. They do not command.**

## Purpose and limits

This pack is reference terrain for UnCommon Core / Hermes Thrice Great. It converts California Social Studies clusters, substandards, and Grades 6–8 analysis skills into ${nodes.length} nodes and ${edges.length} transparent relationships. It is not curriculum authority, a memorized timeline, or proof of learner capability. The School Model Canvas remains the macro authority; Learning Campaigns remain the active plan; receipts and artifacts remain evidence.

## Extraction and normalization

Nodes preserve course theme, cluster text, substandard text, skill examples, and source file. Analysis skills use deterministic \`ANALYSIS.CST/REPV/HI\` codes. Exact duplicated HS content is merged. With explicit approval, the second source occurrences of \`7.1\` and \`8.1\` are normalized to \`7.10\` and \`8.10\`; raw files remain unchanged and every affected node records its source cluster code. The parser stops before appended \`RH.6-8\` literacy standards because they are outside this approved ontology schema.

## Five lenses and edge meanings

The ontology exposes content, historical reasoning, civic judgment, geography/economics, and UCC History Story Map lenses. Edge types describe historical, skill, civic, geography, economic, source-analysis, Story Map, parallel-theme, or future-dependency relationships. All are editable diagnostic hypotheses rather than rigid prerequisites.

## Evidence and Story Maps

History Story Map receipts may map people, places, pressures, choices, consequences, perspectives, and conundrums to benchmark nodes. Reader Engine receipts, writing artifacts, source analyses, discussion notes, and parent observations should record content and reasoning separately. Learning Campaign Builder should begin with mission and evidence, then use this pack to choose an evidence-producing historical question or conundrum.

Learner overlays remain separate from the benchmark. \`no_evidence\` means unobserved, not inability. Mermaid heat maps are ad hoc diagnostics, not core app UI or permanent labels.

## Commands

\`\`\`bash
node benchmarks/ca_social_studies/scripts/ingest_ca_social_studies.js
node benchmarks/ca_social_studies/scripts/generate_mermaid_diagrams.js
node benchmarks/ca_social_studies/scripts/validate_benchmark_pack.js
node benchmarks/ca_social_studies/tests/benchmark_pack_smoke_test.js
\`\`\`
`;
}

function hermesInstructions() {
  return `# Instructions to Hermes Thrice Great — Social Studies Benchmark Pack

## Governing doctrine

**Benchmarks inform. They do not command.**

This pack is a terrain map, not curriculum authority. SchoolModelCanvas.md is the mission. Learning Campaigns are the active plan. History Story Map receipts, Reader Engine receipts, writing artifacts, discussion notes, source analyses, and parent observations are evidence. Hermes interprets and orchestrates. The parent is the final decision-maker.

\`\`\`mermaid
flowchart TD
  SMC["SchoolModelCanvas.md<br/>Family educational constitution"]
  LC["Learning Campaigns<br/>Active weekly/monthly priorities"]
  StoryMaps["History Story Map Receipts<br/>Topics, perspectives, places, conundrums"]
  Reader["Reader Engine Receipts<br/>Sources, highlights, explanations"]
  Writing["Writing Artifacts<br/>Claims, evidence, reflection"]
  Benchmarks["CA Social Studies Benchmark Pack<br/>History + civics + geography + economics"]
  Hermes["Hermes Thrice Great<br/>Interpretation + orchestration"]
  Parent["Parent Coach<br/>Final judgment"]
  Plan["Next Move / Weekly Plan"]
  Heatmap["Ad hoc Mermaid Social Studies Heat Map<br/>Optional diagnostic artifact"]
  SMC --> Hermes
  LC --> Hermes
  StoryMaps --> Hermes
  Reader --> Hermes
  Writing --> Hermes
  Benchmarks --> Hermes
  Hermes --> Parent
  Parent --> Plan
  Hermes --> Heatmap
\`\`\`

Track content knowledge separately from chronology/spatial reasoning, source analysis/evidence, perspective-taking, cause/effect, continuity/change, civic judgment, geography/economics, narrative reconstruction, conundrum reasoning, and Story Map transfer.

Use this order:

1. Read the School Model Canvas and active Learning Campaign.
2. Inspect receipts and artifacts; name demonstrated content and reasoning separately.
3. Map a Story Map's actors, places, pressures, choices, consequences, perspectives, and conundrums to nodes.
4. Treat graph edges as diagnostic hypotheses, never as a rigid grade schedule.
5. Recommend the smallest source-rich next move for parent judgment.

Prefer **needs evidence**, **currently developing**, **foundational repair**, **current-grade target**, **future dependency**, **benchmark-aligned**, **strength area**, **stretch area**, **maintenance area**, **source-analysis gap**, **perspective-taking gap**, and **civic-judgment campaign**. Do not reduce the learner to comparative grade labels or demeaning history-ability labels.

## Example interpretation

- **Evidence:** Aria can retell the Patriot viewpoint but needs more support comparing Loyalist, enslaved, Indigenous, and British perspectives.
- **Benchmark lens:** Grade 5 Revolution, Grade 8 constitutional democracy, and point-of-view/source-analysis skills.
- **Interpretation:** Treat this as a perspective-taking and source-evidence campaign, not a generic history weakness.
- **Recommended campaign:** Evidence Before Opinion.
- **Parent move:** Ask, “Whose perspective is missing, and what source would help us understand it?”

## Heat-map guardrails

Generate heat maps only as ad hoc diagnostic artifacts. Use actual overlay evidence, distinguish content from reasoning, and render unobserved nodes as \`no_evidence\`. A weekly artifact may be named \`aria_social_studies_heatmap_weekXX.md\`. The included sample is fictional.

\`\`\`mermaid
flowchart LR
  R["Receipts + Story Maps"] --> C["Content overlay"]
  R --> S["Reasoning-skill overlay"]
  B["Benchmark terrain"] --> C
  B --> S
  C --> N["Next source-rich conundrum"]
  S --> N
  N --> P["Parent judgment"]
\`\`\`
`;
}

function storyMapSchema() {
  return {
    schema_version: 'story_map_alignment.v1',
    description: 'Schema for mapping Social Studies standards to UCC History Story Maps.',
    fields: {
      storyMapTopic: 'string', benchmarkSystem: 'California Social Studies', relatedStandards: ['string'], timePeriod: 'string', places: ['string'], actors: ['string'], perspectives: ['string'], conundrums: ['string'], historicalReasoningTags: ['string'], civicReasoningTags: ['string'], geographyEconomicsTags: ['string'], uccCapabilityTags: ['string'], evidenceSources: ['string'], interpretation: 'string',
    },
    example: {
      storyMapTopic: 'Founding Fathers / American Revolution', benchmarkSystem: 'California Social Studies', relatedStandards: ['CA.SS.5.5.5.1', 'CA.SS.8.8.1.2', 'CA.SS.8.8.2.2', 'CA.SS.HS.12.1.3'], timePeriod: '1763–1789', places: ['Boston', 'Philadelphia', 'Virginia', 'London'], actors: ['Patriots', 'Loyalists', 'enslaved people', 'Indigenous nations', 'British officials', 'colonial merchants'], perspectives: ['colonist', 'loyalist', 'enslaved person', 'Indigenous nation', 'British official'], conundrums: ['Liberty for whom?', 'When is rebellion justified?', 'How should power be limited?'], historicalReasoningTags: ['cause_effect', 'source_analysis', 'point_of_view'], civicReasoningTags: ['constitutional_reasoning', 'democracy', 'rights_obligations'], geographyEconomicsTags: [], uccCapabilityTags: ['historical_reasoning', 'civic_judgment', 'conundrum_reasoning'], evidenceSources: ['history_story_map_receipt'], interpretation: 'This story map aligns to American Revolution and constitutional democracy benchmarks while emphasizing civic judgment and perspective-taking.',
    },
  };
}

function main() {
  ensureDirectories();
  const files = sourceFiles();
  copyRawFiles(files);
  const nodes = mergeNodes(files.flatMap(parseFile));
  const edges = buildEdges(nodes);
  const timestamp = generatedAt(files);
  writeJson(path.join(ONTOLOGY_FOLDER, 'standards_nodes.json'), { schema_version: 'ca_social_studies_nodes.v1', benchmark_system: 'California Social Studies', role: 'reference_only', generated_at: timestamp, source_folder: SOURCE_FOLDER, nodes });
  writeJson(path.join(ONTOLOGY_FOLDER, 'prerequisite_edges.json'), { schema_version: 'ca_social_studies_edges.v1', benchmark_system: 'California Social Studies', role: 'reference_only', generated_at: timestamp, edges });
  writeJson(path.join(ONTOLOGY_FOLDER, 'historical_reasoning_skills.json'), { schema_version: 'historical_reasoning_skills.v1', skills: HISTORICAL_SKILLS });
  writeJson(path.join(ONTOLOGY_FOLDER, 'civic_reasoning_tags.json'), { schema_version: 'civic_reasoning_tags.v1', tags: CIVIC_TAGS });
  writeJson(path.join(ONTOLOGY_FOLDER, 'geography_economics_tags.json'), { schema_version: 'geography_economics_tags.v1', tags: GEO_ECON_TAGS });
  writeJson(path.join(ONTOLOGY_FOLDER, 'ucc_capability_tags.json'), { schema_version: 'ucc_social_studies_capability_tags.v1', tags: UCC_TAGS });
  writeJson(path.join(ONTOLOGY_FOLDER, 'story_map_alignment_schema.json'), storyMapSchema());
  writeJson(path.join(ONTOLOGY_FOLDER, 'learner_overlay_schema.json'), {
    schema_version: 'learner_benchmark_overlay.v1', description: 'A learner-specific overlay that marks Social Studies standards, reasoning skills, and story-map capabilities as mastered, learning, weak, no_evidence, advanced, or not_applicable.', node_status_values: ['mastered', 'learning', 'weak', 'no_evidence', 'advanced', 'not_applicable'], evidence_strength_values: ['low', 'medium', 'high'], example: { learnerId: 'aria', benchmarkSystem: 'California Social Studies', generatedAt: '2026-06-27', nodes: [{ standardId: 'CA.SS.5.5.5.1', status: 'learning', evidenceStrength: 'medium', latestEvidenceDate: '2026-06-22', evidenceSources: ['history_story_map_receipt_founding_fathers'], notes: 'Can identify taxes and protest as causes, but needs stronger source-based explanation of competing perspectives.' }], skillOverlay: [{ uccCapabilityTag: 'source_evidence_reasoning', status: 'learning', evidenceStrength: 'medium', notes: 'Uses evidence when prompted; needs to cite source before opinion.' }, { uccCapabilityTag: 'perspective_taking', status: 'learning', evidenceStrength: 'medium', notes: 'Can compare Patriot and Loyalist views with support.' }] },
  });
  const countsByGrade = Object.fromEntries(GRADES.map((grade) => [grade, nodes.filter((node) => node.grade === grade).length]));
  writeJson(path.join(ONTOLOGY_FOLDER, 'manifest.json'), {
    schema_version: 'ca_social_studies_manifest.v1', benchmark_system: 'California Social Studies', role: 'reference_only', generated_at: timestamp, source_folder: SOURCE_FOLDER, source_files: files.map((filename) => ({ filename, grade: gradeFromFilename(filename), sha256: sha256(path.join(SOURCE_FOLDER, filename)) })), source_normalizations: [{ grade: '7', source_cluster_code: '7.1', normalized_cluster_code: '7.10', occurrence: 2, reason: 'Sequence-supported source typo between 7.9 and 7.11; user approved intuitive normalization.' }, { grade: '8', source_cluster_code: '8.1', normalized_cluster_code: '8.10', occurrence: 2, reason: 'Sequence-supported source typo between 8.9 and 8.11; user approved intuitive normalization.' }], extraction_scope: 'California Social Studies clusters/substandards plus Grades 6–8 Historical and Social Sciences Analysis Skills; appended RH.6-8 standards excluded by specification.', counts: { nodes: nodes.length, edges: edges.length, nodes_by_grade: countsByGrade }, generation: { ingest: 'node benchmarks/ca_social_studies/scripts/ingest_ca_social_studies.js', diagrams: 'node benchmarks/ca_social_studies/scripts/generate_mermaid_diagrams.js', validate: 'node benchmarks/ca_social_studies/scripts/validate_benchmark_pack.js', smoke_test: 'node benchmarks/ca_social_studies/tests/benchmark_pack_smoke_test.js' },
  });
  writeText(path.join(MARKDOWN_FOLDER, 'ca_social_studies_ontology.md'), ontologyMarkdown(nodes, edges));
  for (const grade of GRADES) writeText(path.join(MARKDOWN_FOLDER, `grade_${grade}.md`), gradeMarkdown(grade, nodes));
  writeText(path.join(MARKDOWN_FOLDER, 'instructions_to_hermes_thrice_great.md'), hermesInstructions());
  console.log(`Ingested ${files.length} Social Studies source files into ${nodes.length} nodes and ${edges.length} edges.`);
}

if (require.main === module) {
  try { main(); } catch (error) { console.error(`Social Studies ingest failed: ${error.message}`); process.exitCode = 1; }
}

