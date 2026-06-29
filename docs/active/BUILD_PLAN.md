# Hermes Thrice Great — Replacement Implementation Build Plan

Status: ACTIVE PLAN; planning only. Runtime implementation is forbidden until Gate R4 passes.

## Executive summary

Hermes Thrice Great will remain an independent UCC source/governance repository for a pinned Hermes runtime. It will generate an allowlisted profile payload under `dist/hermes-thrice-great-profile/` using Hermes-native `distribution.yaml`, `SOUL.md`, profile configuration, skill directories, and plugin extension points. The repository root is never installed. It will not vendor or patch Hermes.

The MVP proves an offline, deterministic learning-evidence loop with synthetic data: normalized SMC → semantically valid CALM/PRESSURE receipts → valid pairing → diagnosis facts → parent brief → proposal → parent approval event → atomic local ledger. Branding and optional mock adapters come after that proof.

## Repository truth

- Current folder: UCC documentation, contracts, skills, templates, benchmark packs, and ACDF v7 material.
- Git: absent.
- Hermes source: absent from this repository.
- Locally installed Hermes: package 0.16.0 on Python 3.11.15, native Windows. The banner's `upstream` hash was proven to be fetched `origin/main`, while executing code resolves to editable checkout HEAD `2a5dc0ef...`; H1 must reproduce and bind that identity before implementation.
- Current contracts are useful source material, not yet an internally consistent runtime contract set.
- Current skills require native packaging and reference repair.

## Bootstrap control

Early recon and governance machinery precede Gate A1's automated claim checker. `BOOTSTRAP_PROTOCOL.md` defines the only permitted bridge: explicit human authorization, manual JSON claims/state events, planning/recon/governance scope only, one task at a time, and automatic expiration at A1. No declaration is currently present, so no execution task is authorized.

## Planned runtime structure

Source files are created only by test-gated tasks. The install surface is generated:

```text
distribution.yaml
SOUL.md
config.yaml
skills/<slug>/SKILL.md
plugins/hermes-thrice-great/
  plugin.yaml
  __init__.py
  core/
schemas/
benchmarks/
tests/
scripts/
dist/hermes-thrice-great-profile/   # generated, ignored, sole install payload
```

`ucc` is the default installed profile. `thoth` is an optional local install name, never a hardcoded dependency.

## Phase 0 — Repo inspection and topology decision

Objective: establish facts and select the distribution topology.

Completed planning evidence:

- Repository contents and Git absence inspected.
- Native Hermes availability inspected.
- Option B selected in `TOPOLOGY_DECISION.md`.
- Invalid old-plan assumptions recorded.

Exit: Gate P0.

## Phase 1 — Hermes compatibility pinning and extension recon

Objective: convert the observed Hermes installation into a reproducible, binding compatibility pin.

Tasks:

1. Run an automated identity probe that resolves `hermes.exe`, imported `hermes_cli`, package `direct_url.json`, exact checkout HEAD, version metadata, and fetched `origin/main` separately. A written theory cannot pass; ambiguous execution/import paths require human escalation.
2. Record the exact release/tag/commit and Python constraint.
3. Characterize local `hermes profile install <path> --name <name>` in a temporary `HERMES_HOME`.
4. Characterize custom `distribution_owned` paths for plugin, schemas, and benchmarks.
5. Prove the project allowlist builder excludes every non-approved source/control path and install only its generated staging tree.
6. Characterize skill discovery, plugin enablement, CLI registration, profile naming, and restricted config keys.
7. Capture stock offline smoke behavior.

No upstream update or source edit is permitted. Upstream drift is reported only.

Exit: H1.

## Phase 2 — ACDF authority machinery repair

Objective: make authority and task control executable rather than ceremonial.

Tasks:

1. Initialize Git through a human-authorized repository operation and record the planning baseline.
2. Create/validate `authority.json`, source manifest, hashes, archive policy, `.agentignore`, `.agent/claims/`, and `.agent/state.log`.
3. Implement cross-platform authority, task/claim synchronization, receipt, and archive-hygiene checkers—each test-first.
4. Classify obsolete root README/INSTALL claims; update them only in a later claimed documentation task.
5. Require state events for claim creation, task start, block, fail, completion, and drift pause.

Exit: A1.

## Phase 3 — Contract versioning and semantic validation design

Objective: remove every field-level ambiguity before runtime code.

Contract decisions:

- Normalize Markdown SMC into a versioned JSON contract; define required versus optional fields and amendment authority.
- Replace/adapter-version the assessment receipt with `receipt_id`, `session_id`, `paired_run_id`, and `assessment_form_id`.
- Define pairing policy: form match, skill-distribution tolerance, denominators, timeouts, partial/degraded sessions, minimum evidence, timestamp order, totals, and timer-tier consistency.
- Separate task proposal from append-only approval authority.
- Define canonical ledger entry and parent brief output.
- Define ID, clock, canonical JSON, provenance, idempotency, and migration rules.
- Bind each approval idempotency key globally within the ledger namespace to one canonical proposal/revision/actor/action/provenance tuple; identical replay succeeds, changed-tuple or cross-revision reuse conflicts.
- Decide whether `I1_MOCK_ADAPTERS` is inside the MVP before adapter RED tests can be authored.

Planned schemas are backlog only in this planning turn:

- `schemas/smc.schema.json`
- `schemas/assessment_receipt.schema.json`
- `schemas/receipt_pairing.schema.json`
- `schemas/approval_event.schema.json`
- `schemas/ledger_entry.schema.json`
- `schemas/parent_brief.schema.json`

Exit: C1.

## Stage 4 — Execution readiness

This gate occurs before Phase 4 test creation and long before Phase 8 runtime implementation.

Required proof:

- sandbox/tool restriction selected and tested;
- archive/authority/claim machinery valid;
- plan hash stable;
- dependency/runtime matrix locked;
- local-only fixture and privacy policies enforceable;
- Windows command set works;
- native-Windows pytest/filesystem canary records long-path, drive-case, reserved-name, and junction/reparse behavior and proves supported or fail-closed behavior;
- mutation meta-probe kills a known behavior-changing mutant, preserves a no-op/equivalent control, and reports infrastructure failure as ERROR;
- stock Hermes smoke and isolated distribution install dry run pass;
- deterministic/mutation strategy ready;
- critical risk count zero.

Exit: R4. A partial pass is FAIL.

## Phase 4 — TDD harness, fixtures, and failing tests

Objective: create RED evidence before behavior.

Create synthetic fixtures and separate failing tests for:

- schema registry and contract versions;
- semantic receipt invariants;
- pressure pairing and delta gating;
- approval actor/revision/idempotency enforcement;
- ledger atomicity and replay;
- privacy path containment/redaction/retention;
- skill packaging/reference integrity;
- profile install under arbitrary names;
- deterministic parent brief and weekly dry run.

Each RED receipt must name the expected missing behavior. Mutation probes inherit the Stage 4 meta-probe outcome contract and must themselves be tested. Mock-adapter RED tests run only when the Phase 3 scope decision includes `I1_MOCK_ADAPTERS`.

Exit: T1.

## Phase 5 — Hermes-native skill packaging

Objective: minimally transform flat skills after the packaging tests are RED.

- Move each skill to the exact H1-proven directory layout.
- Rename only where required by native discovery.
- Move/create required references with provenance, or remove broken references explicitly.
- Preserve content unless a reference/frontmatter defect requires a surgical fix.
- Prove native Hermes discovery/load and kill reference-integrity mutations.

Exit: S1.

## Phase 6 — Native reusable profile creation

Objective: make this repository installable as a Hermes profile distribution.

- Add `distribution.yaml`, `SOUL.md`, and restricted `config.yaml` only after profile tests are RED.
- Deliver the plugin and data through the H1-proven generated staging tree; direct repository-root install is forbidden.
- Install into temporary homes as `ucc` and `thoth`; compare semantic behavior.
- Keep credentials in `.env.EXAMPLE`/documented local setup only; no secrets committed.
- Prove stock Hermes remains unchanged.

PR1 proves installability only. Until SEC1 passes, the installed distribution may be exercised only in isolated temporary homes with synthetic installation fixtures; no learner profile, real data, or semi-real data may be used.

Exit: PR1.

## Phase 7 — Privacy and sandbox configuration

Objective: make safe local behavior the enforced default.

- Disable web, messaging, live adapters, and nonessential tools.
- Select the strongest usable Windows sandbox/restricted backend supported by the pin.
- Implement tested path containment, redaction, pseudonymous records, retention/delete, and commit-eligibility checks.
- Require explicit local/private marking before real-data mode.
- Human owner installs/reviews Git ignore and hook rules; agents verify them but do not weaken the harness.

Exit: SEC1.

## Phase 8 — Deterministic UCC core plugin/package

Objective: implement only behavior already represented by RED tests.

Order:

1. Contract registry and JSON Schema validation.
2. Semantic receipt validation.
3. CALM/PRESSURE pairing decision.
4. Pressure delta and diagnosis facts.
5. Deterministic parent brief and proposal.
6. Approval-event validation and transition evaluator.
7. Atomic local ledger.
8. Offline plugin CLI/tool surface.

Every substep follows RED → minimum GREEN → impacted suite → mutation gate. No model call participates in facts or approval.

Exit: U1.

## Phase 9 — Synthetic weekly dry run

Objective: prove the complete offline loop and rejection paths.

Run one valid week plus adversarial weeks containing mismatched forms, weak samples, partial/degraded sessions, AI approval, wrong revision, replay, traversal, and interrupted writes. Compare canonical outputs across two identical runs.

Exit: E1.

## Phase 10 — Optional mock Discord and Campaign OS adapters

Objective: prove integration contracts without live services.

Adapters consume approved contracts, capture outputs locally, remain disabled, and cannot mutate approval or ledger state on failure. This phase executes only if the Phase 3 scope decision includes `I1_MOCK_ADAPTERS`; otherwise its conditional RED and implementation tasks remain unclaimed and F1 excludes I1.

Exit: I1.

## Phase 11 — Branding and profile aliases

Objective: apply product naming without contaminating stock Hermes or coupling code to `thoth`.

Branding lives in distribution/profile/plugin presentation files. Install-name equivalence and stock smoke must pass.

Exit: B1.

## Phase 12 — Handoff, readiness, and learning cards

Objective: prove operability and preserve empirical lessons.

- Run clean-room acceptance on native Windows.
- Finalize runbook, owner manual deltas, compatibility matrix, build ledger, readiness report, risk register, receipts, and learning cards.
- Record upstream drift and open a separate post-MVP compatibility task; do not update during acceptance.

Exit: F1.

## Upstream lifecycle after MVP

For each candidate Hermes upgrade: create a compatibility branch/task, update the matrix, run stock characterization, isolated distribution install, full UCC acceptance, and migration/rollback rehearsal. Promote only after a human decision. Never merge upstream source into this repository.

## Execution milestones

Only one dependency-ready task is claimable at a time; a later TODO is not claimable merely because it appears on the master board.

1. Authority and compatibility: Phases 0–2.
2. Contracts and RED harness: Phases 3–4.
3. Skills and profile install: Phases 5–6.
4. Privacy and deterministic core: Phases 7–8.
5. Synthetic week and optional post-proof surfaces: Phases 9–12.

`PROJECT_TASKS.md` remains the sole active queue. Creating a second active milestone board would reintroduce authority ambiguity.

## Risk register

| ID | Severity | Risk | Required closure |
|---|---|---|---|
| R-01 | Critical | Package version alone does not identify the editable checkout; banner drift metadata could be mistaken for runtime identity. | H1 automated identity probe pins executable/import source and exact HEAD. |
| R-02 | Critical | Approval could be inferred from status/model text. | Separate schema plus actor/revision/idempotency tests. |
| R-03 | Critical | Private learner data could coexist with outbound tools. | SEC1 lethal-trifecta enforcement. |
| R-04 | High | JSON Schema accepts semantically inconsistent receipts. | Semantic validator and mutation gate. |
| R-05 | High | Invalid pairs produce misleading pressure delta. | Versioned pairing policy and negative fixtures. |
| R-06 | High | Windows junction/symlink escape bypasses containment. | Native-Windows adversarial path tests. |
| R-07 | High | Profile distribution omits plugin/data paths. | H1 isolated install characterization. |
| R-08 | High | Flat skills/broken references silently fail discovery. | S1 packaging/reference gate. |
| R-09 | High | Generated learner data becomes commit-eligible. | Human-owned ignore/hook plus staged-file test. |
| R-10 | Medium | Governance artifacts exist but are not synchronized. | A1 machine checks and state log. |
| R-11 | Medium | Deterministic output hides volatile timestamps/IDs. | Injected clock/ID and canonical comparison. |
| R-12 | Medium | Focused test loop exceeds 60 seconds. | Stop and split harness. |
| R-13 | High | Mutation infrastructure failure is misclassified as a killed mutant. | Stage 4 killable/no-op/error meta-canaries. |
| R-14 | High | One approval key is reused across revisions or altered payloads. | Globally bound key plus cross-revision conflict tests. |
| R-15 | Medium | Installable PR1 profile is mistaken for safe-to-operate profile. | Hard SEC1 interlock before learner/semi-real execution. |

## Stop conditions

Stop immediately if:

1. Authority hash, task status, or claim state disagrees.
2. A task lacks RED evidence required by its implementation dependency.
3. The exact Hermes pin or extension behavior is uncertain.
4. Work requires a Hermes internal edit.
5. A critical source is stale or a contract field is ambiguous.
6. Real learner data would enter tests, logs, Git, model context, or network traffic.
7. Sandbox/tool restrictions cannot be mechanically verified.
8. Parent approval actor/revision semantics are unclear.
9. An implementation task needs a forbidden file or harness change.
10. A focused test loop exceeds 60 seconds.
11. Stock Hermes smoke regresses.
12. Any critical risk is open at a phase exit.

## Final acceptance command set

The eventual cross-platform entry point is:

```powershell
python scripts/validate_authority.py
python scripts/check_archive_hygiene.py
python scripts/check_skill_references.py
python scripts/run_mutation_checks.py --all
python -m pytest -q
python scripts/run_acceptance.py --offline --hermes-command hermes
```

`run_acceptance.py` must create an isolated temporary Hermes home, run stock smoke, install the distribution as `ucc` and `thoth`, run UCC smoke and the synthetic week twice, compare canonical outputs, verify zero network attempts, and remove only its own temporary directory.

MVP acceptance requires all 20 conditions in `ACCEPTANCE_GATES.md`, zero critical risks, receipts for every DONE task, and no live model/Discord/Campaign OS action.
