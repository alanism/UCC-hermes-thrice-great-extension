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
  '1.OA.1',
  '2.OA.1',
  '3.OA.3',
  '4.OA.2',
  '4.OA.3',
  '6.RP.1',
  '7.RP.2',
  '8.EE.5',
];

const rawText = fs.readdirSync(rawFolder)
  .filter((filename) => /\.txt$/i.test(filename))
  .sort()
  .map((filename) => fs.readFileSync(path.join(rawFolder, filename), 'utf8'))
  .join('\n');

for (const code of importantStandards) {
  const escaped = code.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  if (new RegExp(`^${escaped}\\s`, 'm').test(rawText)) {
    assert(nodeIds.has(`CA.CCSS.Math.${code}`), `Expected parsed node CA.CCSS.Math.${code}`);
  }
}

for (const filename of ['word_problem_schema_chain.md', 'progression_spine.md']) {
  const contents = fs.readFileSync(path.join(PACK_ROOT, 'mermaid', filename), 'utf8');
  assert(contents.includes('```mermaid'), `${filename} should contain Mermaid`);
}

const instructions = fs.readFileSync(path.join(PACK_ROOT, 'markdown', 'instructions_to_hermes_thrice_great.md'), 'utf8');
assert(instructions.includes('Benchmarks inform. They do not command.'), 'Hermes instructions should contain governing doctrine');

console.log(`Smoke test passed for ${importantStandards.length} important standards and core documentation.`);

