#!/usr/bin/env node
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const PACK_ROOT = path.resolve(__dirname, '..');
const standards = JSON.parse(fs.readFileSync(path.join(PACK_ROOT, 'ontology', 'standards_nodes.json'), 'utf8'));
const nodeIds = new Set(standards.nodes.map((node) => node.id));
const expected = ['CA.SS.1.1.1.1', 'CA.SS.2.2.2.1', 'CA.SS.3.3.4.1', 'CA.SS.4.4.5.1', 'CA.SS.5.5.5.1', 'CA.SS.6.6.2.1', 'CA.SS.7.7.8.1', 'CA.SS.8.8.2.2', 'CA.SS.HS.12.1.1'];
for (const id of expected) assert(nodeIds.has(id), `Expected parsed node ${id}`);
for (const filename of ['historical_reasoning_progression.md', 'source_analysis_progression.md', 'story_map_conundrum_alignment.md']) {
  const contents = fs.readFileSync(path.join(PACK_ROOT, 'mermaid', filename), 'utf8');
  assert(contents.includes('```mermaid'), `${filename} should contain Mermaid`);
}
const instructions = fs.readFileSync(path.join(PACK_ROOT, 'markdown', 'instructions_to_hermes_thrice_great.md'), 'utf8');
assert(instructions.includes('Benchmarks inform. They do not command.'), 'Hermes instructions should contain governing doctrine');
assert(!standards.nodes.some((node) => ['Math', 'ELA', 'Science'].includes(node.subject)), 'Social Studies nodes must contain no other subject');
assert(nodeIds.has('CA.SS.7.7.10.1') && nodeIds.has('CA.SS.8.8.10.1'), 'Approved normalization nodes should exist');
assert(!standards.nodes.some((node) => /^RH\./.test(node.standardCode)), 'Appended RH.6-8 standards should remain out of scope');
console.log(`Social Studies smoke test passed for ${expected.length} important standards and core documentation.`);

