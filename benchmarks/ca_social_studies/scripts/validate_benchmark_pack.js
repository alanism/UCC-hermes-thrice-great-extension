#!/usr/bin/env node
'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const PACK_ROOT = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(PACK_ROOT, '..', '..');
const SOURCE_FOLDER = path.join(PROJECT_ROOT, 'California Common Core Math Standards by Grade');
const GRADES = ['1', '2', '3', '4', '5', '6', '7', '8', 'HS'];
const MERMAID_FILES = ['progression_spine.md', 'historical_reasoning_progression.md', 'geography_mapping_progression.md', 'source_analysis_progression.md', 'civic_government_progression.md', 'economics_incentives_progression.md', 'world_history_civilizations_progression.md', 'us_history_constitution_progression.md', 'story_map_conundrum_alignment.md', 'sample_learner_heatmap.md'];
const STORY_TAGS = new Set(['people', 'places', 'pressures', 'choices', 'consequences', 'perspectives', 'conundrum', 'institutions']);
const errors = [];
const warnings = [];
function check(condition, message) { if (!condition) errors.push(message); }
function readJson(relativePath) {
  const filePath = path.join(PACK_ROOT, relativePath);
  check(fs.existsSync(filePath), `Missing ${relativePath}`);
  if (!fs.existsSync(filePath)) return null;
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); } catch (error) { errors.push(`Invalid JSON in ${relativePath}: ${error.message}`); return null; }
}
function sha256(filePath) { return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex'); }

function main() {
  for (const folder of ['raw', 'ontology', 'markdown', 'mermaid', 'scripts', 'tests']) check(fs.existsSync(path.join(PACK_ROOT, folder)), `Missing output folder: ${folder}`);
  const manifest = readJson('ontology/manifest.json');
  const standards = readJson('ontology/standards_nodes.json');
  const prerequisites = readJson('ontology/prerequisite_edges.json');
  const capabilities = readJson('ontology/ucc_capability_tags.json');
  const historical = readJson('ontology/historical_reasoning_skills.json');
  const civic = readJson('ontology/civic_reasoning_tags.json');
  const geoEcon = readJson('ontology/geography_economics_tags.json');
  readJson('ontology/story_map_alignment_schema.json');
  readJson('ontology/learner_overlay_schema.json');
  const nodes = standards && Array.isArray(standards.nodes) ? standards.nodes : [];
  const edges = prerequisites && Array.isArray(prerequisites.edges) ? prerequisites.edges : [];
  const historicalIds = new Set(historical && Array.isArray(historical.skills) ? historical.skills.map((item) => item.id) : []);
  const civicIds = new Set(civic && Array.isArray(civic.tags) ? civic.tags.map((item) => item.id) : []);
  const geoEconIds = new Set(geoEcon && Array.isArray(geoEcon.tags) ? geoEcon.tags.map((item) => item.id) : []);
  const capabilityIds = new Set(capabilities && Array.isArray(capabilities.tags) ? capabilities.tags.map((item) => item.id) : []);
  check(nodes.length > 0, 'standards_nodes.json has no nodes');
  check(edges.length > 0, 'prerequisite_edges.json has no edges');

  const sourceFiles = manifest && Array.isArray(manifest.source_files) ? manifest.source_files : [];
  for (const grade of GRADES) {
    const source = sourceFiles.find((entry) => entry.grade === grade);
    check(Boolean(source), `Manifest has no Social Studies source for grade ${grade}`);
    check(nodes.some((node) => node.grade === grade), `No parsed node for Social Studies grade ${grade}`);
    if (source) check(nodes.some((node) => node.sourceFile === source.filename), `No parsed node from ${source.filename}`);
    check(fs.existsSync(path.join(PACK_ROOT, 'markdown', `grade_${grade}.md`)), `Missing grade_${grade}.md`);
  }

  const ids = new Set();
  for (const node of nodes) {
    for (const field of ['id', 'grade', 'standardCode', 'standardText', 'sourceFile']) check(Boolean(node[field]), `Node ${node.id || '(unknown)'} missing ${field}`);
    check(Boolean(node.clusterCode || node.analysisSkillCode), `Node ${node.id || '(unknown)'} missing clusterCode or analysisSkillCode`);
    check(!ids.has(node.id), `Duplicate node ID: ${node.id}`);
    ids.add(node.id);
    check(node.subject === 'Social Studies', `Wrong subject on ${node.id}`);
    check(/^California Common Core Social Studies Grade (?:[1-8]|HS)\.txt$/i.test(node.sourceFile), `Non-Social-Studies source on ${node.id}`);
    check(!/^RH\./.test(node.standardCode), `Out-of-scope RH node found: ${node.id}`);
    for (const tag of node.historicalReasoningTags || []) check(historicalIds.has(tag), `Node ${node.id} references undefined historical tag ${tag}`);
    for (const tag of node.civicReasoningTags || []) check(civicIds.has(tag), `Node ${node.id} references undefined civic tag ${tag}`);
    for (const tag of node.geographyEconomicsTags || []) check(geoEconIds.has(tag), `Node ${node.id} references undefined geography/economics tag ${tag}`);
    for (const tag of node.uccCapabilityTags || []) check(capabilityIds.has(tag), `Node ${node.id} references undefined capability ${tag}`);
    for (const tag of node.storyMapTags || []) check(STORY_TAGS.has(tag), `Node ${node.id} references undefined Story Map tag ${tag}`);
  }

  const allowedRelationships = new Set(['historical_progression', 'skill_progression', 'civic_progression', 'geography_progression', 'economic_progression', 'source_analysis_progression', 'story_map_dependency', 'parallel_theme', 'future_dependency']);
  for (const edge of edges) {
    check(allowedRelationships.has(edge.relationship), `Invalid relationship on ${edge.from} -> ${edge.to}`);
    check(['low', 'medium', 'high'].includes(edge.confidence), `Invalid confidence on ${edge.from} -> ${edge.to}`);
    if (!ids.has(edge.from) || !ids.has(edge.to)) warnings.push(`Edge references an unparsed node: ${edge.from} -> ${edge.to}`);
  }

  for (const source of sourceFiles) {
    check(/^California Common Core Social Studies Grade (?:[1-8]|HS)\.txt$/i.test(source.filename), `Manifest contains a non-Social-Studies source: ${source.filename}`);
    const original = path.join(SOURCE_FOLDER, source.filename);
    const copied = path.join(PACK_ROOT, 'raw', source.filename);
    check(fs.existsSync(original), `Missing source file ${source.filename}`);
    check(fs.existsSync(copied), `Missing raw copy ${source.filename}`);
    if (fs.existsSync(original) && fs.existsSync(copied)) {
      check(sha256(original) === sha256(copied), `Raw copy differs from source: ${source.filename}`);
      check(sha256(original) === source.sha256, `Manifest hash differs from source: ${source.filename}`);
    }
  }
  if (fs.existsSync(path.join(PACK_ROOT, 'raw'))) for (const filename of fs.readdirSync(path.join(PACK_ROOT, 'raw'))) check(/^California Common Core Social Studies Grade (?:[1-8]|HS)\.txt$/i.test(filename), `Raw folder contains non-Social-Studies file: ${filename}`);
  for (const filename of MERMAID_FILES) {
    const filePath = path.join(PACK_ROOT, 'mermaid', filename);
    check(fs.existsSync(filePath), `Missing Mermaid file ${filename}`);
    if (fs.existsSync(filePath)) check(fs.readFileSync(filePath, 'utf8').includes('```mermaid'), `${filename} has no Mermaid code block`);
  }
  const instructions = path.join(PACK_ROOT, 'markdown', 'instructions_to_hermes_thrice_great.md');
  check(fs.existsSync(instructions), 'Missing instructions_to_hermes_thrice_great.md');
  if (fs.existsSync(instructions)) check(fs.readFileSync(instructions, 'utf8').includes('Benchmarks inform. They do not command.'), 'Hermes instructions omit governing doctrine');
  check(ids.has('CA.SS.7.7.10.1') && ids.has('CA.SS.8.8.10.1'), 'Approved 7.10/8.10 normalizations are missing');

  for (const warning of warnings) console.warn(`WARNING: ${warning}`);
  if (errors.length) {
    for (const error of errors) console.error(`ERROR: ${error}`);
    console.error(`Social Studies validation failed with ${errors.length} error(s) and ${warnings.length} warning(s).`);
    process.exitCode = 1;
    return;
  }
  console.log(`Social Studies validation passed: ${nodes.length} nodes, ${edges.length} edges, ${MERMAID_FILES.length} Mermaid files, ${warnings.length} warnings.`);
}
main();

