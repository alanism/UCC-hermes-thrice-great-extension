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
  ['1', 'PI.1.6'],
  ['2', 'PI.2.6'],
  ['3', 'PI.3.6'],
  ['4', 'PI.4.6'],
  ['5', 'PI.5.6'],
  ['6', 'PI.6.7'],
  ['7', 'PI.7.3'],
  ['8', 'PI.8.10'],
  ['9', 'PI.9-10.8'],
  ['10', 'PI.9-10.8'],
  ['11', 'PI.11-12.8'],
  ['12', 'PI.11-12.8'],
];

for (const [grade, code] of importantStandards) {
  const filename = `California Common Core ELA Grade ${grade}.txt`;
  const rawText = fs.readFileSync(path.join(rawFolder, filename), 'utf8');
  const escaped = code.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  if (new RegExp(`^${escaped}\\s`, 'm').test(rawText)) {
    assert(nodeIds.has(`CA.CCSS.ELA.${grade}.${code}`), `Expected parsed node CA.CCSS.ELA.${grade}.${code}`);
  }
}

for (const filename of ['argument_evidence_progression.md', 'reading_comprehension_progression.md']) {
  const contents = fs.readFileSync(path.join(PACK_ROOT, 'mermaid', filename), 'utf8');
  assert(contents.includes('```mermaid'), `${filename} should contain Mermaid`);
}

const instructions = fs.readFileSync(path.join(PACK_ROOT, 'markdown', 'instructions_to_hermes_thrice_great.md'), 'utf8');
assert(instructions.includes('Benchmarks inform. They do not command.'), 'Hermes instructions should contain governing doctrine');
assert(!standards.nodes.some((node) => node.subject === 'Math'), 'ELA standards_nodes.json must contain no Math nodes');

console.log(`ELA smoke test passed for ${importantStandards.length} important standards and core documentation.`);

