#!/usr/bin/env node
'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const PACK_ROOT = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(PACK_ROOT, '..', '..');
const SOURCE_FOLDER = path.join(PROJECT_ROOT, 'California Common Core Math Standards by Grade');
const GRADES = ['KG', '1', '2', '3', '4', '5', '6', '7', '8', 'HS'];
const MERMAID_FILES = [
  'progression_spine.md',
  'operations_algebraic_thinking.md',
  'word_problem_schema_chain.md',
  'fractions_to_ratios_to_functions.md',
  'ratios_to_linear_functions.md',
  'geometry_progression.md',
  'data_statistics_progression.md',
  'sample_learner_heatmap.md',
];

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
  readJson('ontology/learner_overlay_schema.json');

  const nodes = standards && Array.isArray(standards.nodes) ? standards.nodes : [];
  const edges = prerequisites && Array.isArray(prerequisites.edges) ? prerequisites.edges : [];
  const tagIds = new Set(capabilities && Array.isArray(capabilities.tags) ? capabilities.tags.map((tag) => tag.id) : []);
  check(nodes.length > 0, 'standards_nodes.json has no nodes');
  check(edges.length > 0, 'prerequisite_edges.json has no edges');

  for (const grade of GRADES) {
    check(nodes.some((node) => node.grade === grade), `No parsed node for grade ${grade}`);
  }

  const requiredFields = ['id', 'grade', 'standardCode', 'standardText', 'domainCode', 'domainName', 'sourceFile'];
  const ids = new Set();
  for (const node of nodes) {
    for (const field of requiredFields) check(Boolean(node[field]), `Node ${node.id || '(unknown)'} missing ${field}`);
    check(!ids.has(node.id), `Duplicate node ID: ${node.id}`);
    ids.add(node.id);
    for (const tag of node.uccCapabilityTags || []) check(tagIds.has(tag), `Node ${node.id} references undefined capability tag ${tag}`);
  }

  for (const edge of edges) {
    check(['official_progression', 'prerequisite_for'].includes(edge.relationship), `Invalid relationship on edge ${edge.from} -> ${edge.to}`);
    check(['low', 'medium', 'high'].includes(edge.confidence), `Invalid confidence on edge ${edge.from} -> ${edge.to}`);
    if (!ids.has(edge.from) || !ids.has(edge.to)) warnings.push(`Edge references an unparsed node: ${edge.from} -> ${edge.to}`);
  }

  if (manifest && Array.isArray(manifest.source_files)) {
    for (const source of manifest.source_files) {
      const original = path.join(SOURCE_FOLDER, source.filename);
      const copied = path.join(PACK_ROOT, 'raw', source.filename);
      check(fs.existsSync(original), `Missing original source file ${source.filename}`);
      check(fs.existsSync(copied), `Missing raw copy ${source.filename}`);
      if (fs.existsSync(original) && fs.existsSync(copied)) {
        check(sha256(original) === sha256(copied), `Raw copy differs from source: ${source.filename}`);
        check(sha256(original) === source.sha256, `Manifest hash differs from source: ${source.filename}`);
      }
    }
  }

  for (const filename of MERMAID_FILES) {
    const filePath = path.join(PACK_ROOT, 'mermaid', filename);
    check(fs.existsSync(filePath), `Missing Mermaid file ${filename}`);
    if (fs.existsSync(filePath)) check(fs.readFileSync(filePath, 'utf8').includes('```mermaid'), `${filename} has no Mermaid code block`);
  }

  const instructions = path.join(PACK_ROOT, 'markdown', 'instructions_to_hermes_thrice_great.md');
  check(fs.existsSync(instructions), 'Missing instructions_to_hermes_thrice_great.md');
  if (fs.existsSync(instructions)) {
    check(fs.readFileSync(instructions, 'utf8').includes('Benchmarks inform. They do not command.'), 'Hermes instructions omit the governing doctrine');
  }

  for (const warning of warnings) console.warn(`WARNING: ${warning}`);
  if (errors.length) {
    for (const error of errors) console.error(`ERROR: ${error}`);
    console.error(`Validation failed with ${errors.length} error(s) and ${warnings.length} warning(s).`);
    process.exitCode = 1;
    return;
  }
  console.log(`Validation passed: ${nodes.length} nodes, ${edges.length} edges, ${MERMAID_FILES.length} Mermaid files, ${warnings.length} warnings.`);
}

main();

