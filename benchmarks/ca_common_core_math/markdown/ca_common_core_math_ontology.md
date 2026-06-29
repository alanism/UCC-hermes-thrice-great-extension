# California Common Core Math Benchmark Ontology

> **Benchmarks inform. They do not command.**

## What this pack is

This pack is a reference benchmark layer for UnCommon Core / Hermes Thrice Great. It turns the supplied California Common Core Math text into 479 standards nodes and 193 transparent, editable progression or prerequisite edges. It provides grade-equivalence terrain, capability tags, and visual maps.

## What this pack is not

It is not UCC's curriculum authority, a prescription that a learner move linearly, or proof of mastery. The School Model Canvas remains the macro educational authority. Assessment receipts remain the evidence layer. Learning Campaigns remain the active plan.

## From source text to ontology

Each detected domain, cluster, standard, skill example, and checkpoint is preserved on a deterministic node ID of the form `CA.CCSS.Math.{standardCode}`. Repeated high-school standards are merged by ID; their skill examples and checkpoints are deduplicated. Keyword rules assign readable UCC capability tags. The raw files are copied unchanged into `raw/`.

## Edge meanings

- `official_progression` preserves nearby grade sequence within a California domain family. Confidence is `medium`; it is a navigation aid, not an official claim that one individual standard is the sole prerequisite for another.
- `prerequisite_for` is an editable inference based on named math progressions. Its `low`, `medium`, or `high` confidence reports heuristic strength.

## Using the pack

Hermes should begin with receipts, then use nodes and edges to locate a current-grade target, foundational repair, future dependency, or area that needs evidence. Learning Campaign Builder may select benchmark-aligned targets after consulting the School Model Canvas and current evidence; it must not substitute the grade map for learner-specific judgment.

## Learner overlays and heat maps

The overlay schema stores learner-specific status and evidence strength separately from the reference ontology. A heat map joins overlay records to node IDs and may render an ad hoc Mermaid diagnostic. Missing overlay data means `no_evidence`, not inability. Heat maps are diagnostic artifacts, not core app UI and not permanent labels.

## Nonlinear development

California's grade sequence is retained because it is useful reference terrain. A learner may nevertheless show advanced evidence in one branch, foundational repair in another, and no evidence elsewhere. Plans should follow dependencies and receipts rather than forcing the learner through a single age-graded path.

## Commands

```bash
node benchmarks/ca_common_core_math/scripts/ingest_ca_common_core_math.js
node benchmarks/ca_common_core_math/scripts/generate_mermaid_diagrams.js
node benchmarks/ca_common_core_math/scripts/validate_benchmark_pack.js
node benchmarks/ca_common_core_math/tests/benchmark_pack_smoke_test.js
```
