# California Common Core ELA Benchmark Ontology

> **Benchmarks inform. They do not command.**

## What this pack is

This pack is a reference benchmark layer for UnCommon Core / Hermes Thrice Great. It converts the supplied California ELA PI/PII sections into 228 grade-qualified nodes and 281 transparent, editable relationships. It offers grade-equivalence terrain, capability tags, and visual maps.

## What this pack is not

It is not UCC's curriculum authority, a fixed grade staircase, or evidence that a learner can perform a capability. The School Model Canvas remains the macro educational authority. Learning Campaigns remain the active plan.

## Extraction scope

The source files contain a PI/PII English-language-development ontology followed by other ELA standard families. This schema extracts the explicitly specified PI and PII strands, sub-strands, standards, and trailing skill examples. It preserves all raw files unchanged. IDs include source grade, so shared 9–10 and 11–12 band codes remain collision-safe.

## Spiraling strands and edge meanings

ELA develops through overlapping comprehension, vocabulary, writing, argument, language, speaking/listening, research, media-literacy, and style strands. `spiral_progression` links a recurring capability across grades without claiming strict order. `supports` describes a useful cross-strand contribution. `prerequisite_for` and `future_dependency` are editable hypotheses, never learner diagnoses. `parallel_strand` identifies capabilities that may develop alongside one another.

## Evidence and planning

Reader Engine receipts can map comprehension, vocabulary, explanation, and evidence use to nodes. Writer's White Board artifacts can map organization, claims, evidence, conventions, revision, and style. Quiz receipts and parent observations add evidence but do not change the benchmark's reference-only role. Learning Campaign Builder should consult the School Model Canvas and receipts before selecting benchmark-aligned targets.

## Learner overlays and heat maps

The overlay schema stores learner status separately from the benchmark. Missing data means `no_evidence`, not inability. Hermes may join overlay entries to node IDs and render an ad hoc Mermaid diagnostic; these heat maps are not core app UI or permanent learner labels.

## Commands

```bash
node benchmarks/ca_common_core_ela/scripts/ingest_ca_common_core_ela.js
node benchmarks/ca_common_core_ela/scripts/generate_mermaid_diagrams.js
node benchmarks/ca_common_core_ela/scripts/validate_benchmark_pack.js
node benchmarks/ca_common_core_ela/tests/benchmark_pack_smoke_test.js
```
