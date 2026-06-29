#!/usr/bin/env node
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const PACK_ROOT = path.resolve(__dirname, '..');
const rawFolder = path.join(PACK_ROOT, 'raw');
const standards = JSON.parse(fs.readFileSync(path.join(PACK_ROOT, 'ontology', 'standards_nodes.json'), 'utf8'));
const nodeIds = new Set(standards.nodes.map((node) => node.id));
const importantStandards = [
  ['1', '1-LS1-1'],
  ['2', '2-PS1-1'],
  ['3', '3-PS2-1'],
  ['4', '4-LS1-1'],
  ['5', '5-LS2-1'],
  ['6', 'MS-LS1-1'],
  ['7', 'MS-LS2-3'],
  ['8', 'MS-PS2-2'],
  ['HS', 'HS-LS1-1'],
  ['HS', 'HS-PS1-7'],
];

for (const [grade, code] of importantStandards) {
  const filename = `California Common Core Science Grade ${grade}.txt`;
  const rawText = fs.readFileSync(path.join(rawFolder, filename), 'utf8');
  const escaped = code.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  if (new RegExp(`^${escaped}\\s`, 'm').test(rawText)) {
    assert(nodeIds.has(`CA.SCI.${grade}.${code}`), `Expected parsed node CA.SCI.${grade}.${code}`);
  }
}

for (const filename of ['scientific_practices_progression.md', 'evidence_argument_modeling_progression.md']) {
  const contents = fs.readFileSync(path.join(PACK_ROOT, 'mermaid', filename), 'utf8');
  assert(contents.includes('```mermaid'), `${filename} should contain Mermaid`);
}

const instructions = fs.readFileSync(path.join(PACK_ROOT, 'markdown', 'instructions_to_hermes_thrice_great.md'), 'utf8');
assert(instructions.includes('Benchmarks inform. They do not command.'), 'Hermes instructions should contain governing doctrine');
assert(!standards.nodes.some((node) => node.subject === 'Math' || node.subject === 'ELA'), 'Science standards_nodes.json must contain no Math or ELA nodes');

console.log(`Science smoke test passed for ${importantStandards.length} important standards and core documentation.`);

