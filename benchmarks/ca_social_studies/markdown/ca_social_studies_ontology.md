# California Social Studies Benchmark Ontology

> **Benchmarks inform. They do not command.**

## Purpose and limits

This pack is reference terrain for UnCommon Core / Hermes Thrice Great. It converts California Social Studies clusters, substandards, and Grades 6–8 analysis skills into 386 nodes and 36 transparent relationships. It is not curriculum authority, a memorized timeline, or proof of learner capability. The School Model Canvas remains the macro authority; Learning Campaigns remain the active plan; receipts and artifacts remain evidence.

## Extraction and normalization

Nodes preserve course theme, cluster text, substandard text, skill examples, and source file. Analysis skills use deterministic `ANALYSIS.CST/REPV/HI` codes. Exact duplicated HS content is merged. With explicit approval, the second source occurrences of `7.1` and `8.1` are normalized to `7.10` and `8.10`; raw files remain unchanged and every affected node records its source cluster code. The parser stops before appended `RH.6-8` literacy standards because they are outside this approved ontology schema.

## Five lenses and edge meanings

The ontology exposes content, historical reasoning, civic judgment, geography/economics, and UCC History Story Map lenses. Edge types describe historical, skill, civic, geography, economic, source-analysis, Story Map, parallel-theme, or future-dependency relationships. All are editable diagnostic hypotheses rather than rigid prerequisites.

## Evidence and Story Maps

History Story Map receipts may map people, places, pressures, choices, consequences, perspectives, and conundrums to benchmark nodes. Reader Engine receipts, writing artifacts, source analyses, discussion notes, and parent observations should record content and reasoning separately. Learning Campaign Builder should begin with mission and evidence, then use this pack to choose an evidence-producing historical question or conundrum.

Learner overlays remain separate from the benchmark. `no_evidence` means unobserved, not inability. Mermaid heat maps are ad hoc diagnostics, not core app UI or permanent labels.

## Commands

```bash
node benchmarks/ca_social_studies/scripts/ingest_ca_social_studies.js
node benchmarks/ca_social_studies/scripts/generate_mermaid_diagrams.js
node benchmarks/ca_social_studies/scripts/validate_benchmark_pack.js
node benchmarks/ca_social_studies/tests/benchmark_pack_smoke_test.js
```
