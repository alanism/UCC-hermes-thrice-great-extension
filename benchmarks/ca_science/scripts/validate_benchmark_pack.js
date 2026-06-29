#!/usr/bin/env node
'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const PACK_ROOT = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(PACK_ROOT, '..', '..');
const SOURCE_FOLDER = path.join(PROJECT_ROOT, 'California Common Core Math Standards by Grade');
const GRADES = ['1', '2', '3', '4', '5', '6', '7', '8', 'HS'];
const MERMAID_FILES = [
  'progression_spine.md',
  'life_science_progression.md',
  'physical_science_progression.md',
  'earth_space_science_progression.md',
  'engineering_design_progression.md',
  'scientific_practices_progression.md',
  'matter_energy_systems_progression.md',
  'evidence_argument_modeling_progression.md',
  'sample_learner_heatmap.md',
];
const PHENOMENON_TAGS = new Set(['life_science', 'cells_genetics', 'matter_chemistry', 'forces_motion', 'energy_waves', 'earth_systems', 'space_systems', 'human_impacts_engineering']);
const errors = [];
const warnings = [];

function check(condition, message) {
  if (!condition) errors.push(message);
}

function readJson(relativePath) {
  const filePath = path.join(PACK_ROOT, relativePath);
  check(fs.existsSync(filePath), `Missing ${relativePath}`);
  if (!fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    errors.push(`Invalid JSON in ${relativePath}: ${error.message}`);
    return null;
  }
}

function sha256(filePath) {
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function main() {
  for (const folder of ['raw', 'ontology', 'markdown', 'mermaid', 'scripts', 'tests']) {
    check(fs.existsSync(path.join(PACK_ROOT, folder)), `Missing output folder: ${folder}`);
  }

  const manifest = readJson('ontology/manifest.json');
  const standards = readJson('ontology/standards_nodes.json');
  const prerequisites = readJson('ontology/prerequisite_edges.json');
  const capabilities = readJson('ontology/ucc_capability_tags.json');
  const practices = readJson('ontology/science_practices.json');
  const concepts = readJson('ontology/crosscutting_concepts.json');
  readJson('ontology/learner_overlay_schema.json');

  const nodes = standards && Array.isArray(standards.nodes) ? standards.nodes : [];
  const edges = prerequisites && Array.isArray(prerequisites.edges) ? prerequisites.edges : [];
  const practiceIds = new Set(practices && Array.isArray(practices.practices) ? practices.practices.map((item) => item.id) : []);
  const conceptIds = new Set(concepts && Array.isArray(concepts.concepts) ? concepts.concepts.map((item) => item.id) : []);
  const capabilityIds = new Set(capabilities && Array.isArray(capabilities.tags) ? capabilities.tags.map((item) => item.id) : []);
  check(nodes.length > 0, 'standards_nodes.json has no nodes');
  check(edges.length > 0, 'prerequisite_edges.json has no edges');

  const sourceFiles = manifest && Array.isArray(manifest.source_files) ? manifest.source_files : [];
  for (const grade of GRADES) {
    const source = sourceFiles.find((entry) => entry.grade === grade);
    check(Boolean(source), `Manifest has no Science source for grade ${grade}`);
    check(nodes.some((node) => node.grade === grade), `No parsed node for Science grade ${grade}`);
    if (source) check(nodes.some((node) => node.sourceFile === source.filename), `No parsed node from ${source.filename}`);
    check(fs.existsSync(path.join(PACK_ROOT, 'markdown', `grade_${grade}.md`)), `Missing grade_${grade}.md`);
  }

  const requiredFields = ['id', 'grade', 'standardCode', 'standardText', 'disciplineCode', 'disciplineName', 'topic', 'sourceFile'];
  const ids = new Set();
  for (const node of nodes) {
    for (const field of requiredFields) check(Boolean(node[field]), `Node ${node.id || '(unknown)'} missing ${field}`);
    check(!ids.has(node.id), `Duplicate node ID: ${node.id}`);
    ids.add(node.id);
    check(node.subject === 'Science', `Non-Science subject found on ${node.id}`);
    check(/^California Common Core Science Grade (?:[1-8]|HS)\.txt$/i.test(node.sourceFile), `Non-Science source on ${node.id}: ${node.sourceFile}`);
    check(['LS', 'PS', 'ESS', 'ETS'].includes(node.disciplineCode), `Invalid discipline on ${node.id}`);
    for (const tag of node.sciencePracticeTags || []) check(practiceIds.has(tag), `Node ${node.id} references undefined practice ${tag}`);
    for (const tag of node.crosscuttingConceptTags || []) check(conceptIds.has(tag), `Node ${node.id} references undefined concept ${tag}`);
    for (const tag of node.phenomenonTags || []) check(PHENOMENON_TAGS.has(tag), `Node ${node.id} references undefined phenomenon ${tag}`);
    for (const tag of node.uccCapabilityTags || []) check(capabilityIds.has(tag), `Node ${node.id} references undefined capability ${tag}`);
  }

  const allowedRelationships = new Set(['spiral_progression', 'conceptual_progression', 'practice_progression', 'supports', 'future_dependency', 'parallel_practice', 'engineering_design_reuse']);
  for (const edge of edges) {
    check(allowedRelationships.has(edge.relationship), `Invalid relationship on ${edge.from} -> ${edge.to}`);
    check(['low', 'medium', 'high'].includes(edge.confidence), `Invalid confidence on ${edge.from} -> ${edge.to}`);
    if (!ids.has(edge.from) || !ids.has(edge.to)) warnings.push(`Edge references an unparsed node: ${edge.from} -> ${edge.to}`);
  }

  for (const source of sourceFiles) {
    check(/^California Common Core Science Grade (?:[1-8]|HS)\.txt$/i.test(source.filename), `Manifest contains a non-Science source: ${source.filename}`);
    const original = path.join(SOURCE_FOLDER, source.filename);
    const copied = path.join(PACK_ROOT, 'raw', source.filename);
    check(fs.existsSync(original), `Missing source file ${source.filename}`);
    check(fs.existsSync(copied), `Missing raw copy ${source.filename}`);
    if (fs.existsSync(original) && fs.existsSync(copied)) {
      check(sha256(original) === sha256(copied), `Raw copy differs from source: ${source.filename}`);
      check(sha256(original) === source.sha256, `Manifest hash differs from source: ${source.filename}`);
    }
  }
  if (fs.existsSync(path.join(PACK_ROOT, 'raw'))) {
    for (const filename of fs.readdirSync(path.join(PACK_ROOT, 'raw'))) {
      check(/^California Common Core Science Grade (?:[1-8]|HS)\.txt$/i.test(filename), `Science raw folder contains non-Science file: ${filename}`);
    }
  }

  for (const filename of MERMAID_FILES) {
    const filePath = path.join(PACK_ROOT, 'mermaid', filename);
    check(fs.existsSync(filePath), `Missing Mermaid file ${filename}`);
    if (fs.existsSync(filePath)) check(fs.readFileSync(filePath, 'utf8').includes('```mermaid'), `${filename} has no Mermaid code block`);
  }

  const instructions = path.join(PACK_ROOT, 'markdown', 'instructions_to_hermes_thrice_great.md');
  check(fs.existsSync(instructions), 'Missing instructions_to_hermes_thrice_great.md');
  if (fs.existsSync(instructions)) check(fs.readFileSync(instructions, 'utf8').includes('Benchmarks inform. They do not command.'), 'Hermes instructions omit the governing doctrine');

  for (const warning of warnings) console.warn(`WARNING: ${warning}`);
  if (errors.length) {
    for (const error of errors) console.error(`ERROR: ${error}`);
    console.error(`Science validation failed with ${errors.length} error(s) and ${warnings.length} warning(s).`);
    process.exitCode = 1;
    return;
  }
  console.log(`Science validation passed: ${nodes.length} nodes, ${edges.length} edges, ${MERMAID_FILES.length} Mermaid files, ${warnings.length} warnings.`);
}

main();

