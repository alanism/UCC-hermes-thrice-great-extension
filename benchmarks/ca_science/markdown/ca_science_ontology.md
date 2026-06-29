# California Science Benchmark Ontology

> **Benchmarks inform. They do not command.**

## What this pack is

This pack is a reference terrain map for UnCommon Core / Hermes Thrice Great. It converts the supplied California Science / NGSS-style performance expectations into 192 nodes and 129 transparent, editable relationships across discipline, practice, crosscutting-concept, and phenomenon lenses.

## What this pack is not

It is not UCC's curriculum authority, a rigid grade schedule, or proof that a learner can perform a practice. The School Model Canvas remains the macro authority. Learning Campaigns remain the active plan. Receipts and artifacts remain the evidence layer.

## From performance expectations to nodes

Each source performance expectation becomes a grade-qualified deterministic ID. The parser preserves topic, inferred discipline, source grade band, skill examples, and any available discipline section heading. Exact repeated HS standards are merged by ID with examples deduplicated and alternate topics retained. Raw files are copied unchanged.

Performance expectations combine content and action: knowing a topic is not equivalent to planning an investigation, analyzing data, developing a model, or arguing from evidence. Tags therefore expose all four science lenses rather than reducing the pack to a topic list.

## Edge meanings

- `conceptual_progression`: a science idea reappears with greater depth.
- `practice_progression`: a scientific practice reappears with greater independence or rigor.
- `spiral_progression`, `supports`, and `future_dependency`: editable diagnostic hypotheses, not mandated order.
- `parallel_practice`: practices that can develop together.
- `engineering_design_reuse`: the same grade-band design expectation appears in multiple grade files.

## Evidence, planning, and overlays

Science receipts, projects, lab notes, models, explanations, builds, and parent observations may map separately to content and practice tags. Learning Campaign Builder should begin with the School Model Canvas and actual evidence, then use this terrain to choose a phenomenon and an evidence-producing next move. Overlay status lives outside the ontology; `no_evidence` means unobserved, not inability. Mermaid heat maps are ad hoc diagnostics, not core app UI or identity labels.

## Commands

```bash
node benchmarks/ca_science/scripts/ingest_ca_science.js
node benchmarks/ca_science/scripts/generate_mermaid_diagrams.js
node benchmarks/ca_science/scripts/validate_benchmark_pack.js
node benchmarks/ca_science/tests/benchmark_pack_smoke_test.js
```
