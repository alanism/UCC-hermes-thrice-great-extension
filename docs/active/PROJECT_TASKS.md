# Project Tasks

Status values: `TODO`, `IN_PROGRESS <agent> <UTC timestamp>`, `BLOCKED <reason>`, `FAILED <reason>`, `DONE <agent> <UTC timestamp>`.

All tasks begin `TODO`. Before any source/test/config change, create `.agent/claims/<task-id>.<agent-id>.json`, copy the active plan hash, change the board status, and append matching events to `.agent/state.log`. Receipt path is exactly `docs/active/receipts/<task-id>.md`. No claim, no code.

Global forbidden scope unless a row explicitly allows it: installed/upstream Hermes source, `docs/archive/**`, real learner data, secrets, live model/network/Discord/Campaign OS actions, unrelated files, and human-owned harness/security rules. Implementation claims also forbid `docs/active/authority.json`, `BUILD_PLAN.md`, and `PROJECT_TASKS.md`.

This is the sole active master queue. Only the earliest dependency-ready TODO within the current human-authorized milestone is claimable. Later TODO rows are backlog, not implicit authorization. Conditional tasks are never claimable unless their named scope decision is active.

Before A1, T0.*, H1.*, and A2.* may run only under a dated human declaration in `BOOTSTRAP_PROTOCOL.md` and still require manual JSON claims, state events, allowed-file checks, and receipts. No such declaration currently exists.

## Phase 0 — Repo state and topology

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| T0.1 | Record repository state, runtime versions, existing paths, and invalid prior-plan paths. | None | `docs/active/TOPOLOGY_DECISION.md` | Distribution | PowerShell inventory and Git/Hermes status captured. | `T0.1.md` | P0 |
| T0.2 | Confirm independent profile/plugin distribution and reject source-fork assumptions. | T0.1 | `docs/active/TOPOLOGY_DECISION.md`, `architecture.mmd` | Topology | Decision names update and rollback workflows. | `T0.2.md` | P0 |

## Phase 1 — Hermes compatibility and recon

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| H1.1 | Prove executing Hermes identity and select exact package/HEAD pin. | T0.2 | `docs/active/HERMES_COMPATIBILITY_MATRIX.md`, `docs/active/recon/**`, temporary probe output | Upstream Hermes | Automated probe resolves executable, import file, editable `direct_url.json`, exact HEAD, version metadata, and `origin/main` separately. Ambiguity is FAIL plus human escalation; prose cannot pass. | `H1.1.md` | H1 |
| H1.2 | Characterize local profile-distribution install/update in a temporary Hermes home. | H1.1 | `docs/active/recon/**` | Profile distribution | Manual isolated install transcript; no persistent profile or network action. | `H1.2.md` | H1 |
| H1.3 | Characterize custom distribution-owned plugin/schema/benchmark paths. | H1.2 | `docs/active/recon/**`, temporary OS directory | Distribution/plugin | Installed inventory proves exact copy/update behavior. | `H1.3.md` | H1 |
| H1.3A | Adopt and prove generated allowlisted staging payload after H1.3 copy-scope finding. | H1.3 | governance docs, staging builder/test, ignored `dist/**`, recon evidence | Packaging boundary | RED/GREEN allowlist tests; forbidden-path scan; pinned Hermes installs only generated staging tree. | `H1.3A.md` | H1 |
| H1.4 | Characterize skill discovery, plugin enablement/CLI API, arbitrary profile names, and restricted config keys. | H1.3A | `docs/active/recon/**` | Profile/skills/plugin | Pinned-source citations and offline command evidence. | `H1.4.md` | H1 |
| H1.5 | Finalize matrix and stock offline smoke definition; report upstream drift without updating. | H1.3, H1.4 | `HERMES_COMPATIBILITY_MATRIX.md`, `docs/active/UPSTREAM_SMOKE_TEST.md` | Compatibility | Stock smoke passes; exact pin and known incompatibilities are explicit. | `H1.5.md` | H1 |

## Phase 2 — ACDF authority machinery

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| A2.1 | Human-authorized Git initialization and planning baseline commit. | T0.2 | Git metadata only | Authority | Branch, commit, and rollback reference recorded; no source rewrite. | `A2.1.md` | A1 |
| A2.2 | Write failing tests for authority hashes, exactly-one-active-plan, and archive hygiene. | A2.1 | `tests/governance/**` | Authority | Focused pytest RED for missing checker behavior. | `A2.2.md` | A1 |
| A2.3 | Implement minimum cross-platform authority/archive checker. | A2.2 | `scripts/validate_authority.py`, `scripts/check_archive_hygiene.py` | Authority | Focused tests GREEN; malformed hash mutation fails. | `A2.3.md` | A1 |
| A2.4 | Initialize archive policy, `.agentignore`, claims directory, state log, and source manifest. | A2.3 | `docs/archive/**`, `.agentignore`, `.agent/**`, `docs/active/sources.manifest.json` | Authority | Checker reports valid structure; no implementation claim active. | `A2.4.md` | A1 |
| A2.5 | Write failing tests for claim schema, active-plan hash, task sync, and all required state events. | A2.4 | `tests/governance/**` | Claims | Focused pytest RED for missing synchronization. | `A2.5.md` | A1 |
| A2.6 | Implement minimum claim/state/task synchronization checker. | A2.5 | `scripts/check_claim_state.py`, `.agent/claim.schema.json` | Claims | Focused tests GREEN; stale-plan and collision mutations fail. | `A2.6.md` | A1 |
| A2.7 | Rehash and activate authority; classify obsolete root README/INSTALL claims. | A2.6 | `docs/active/authority.json`, `ARCHIVE_HYGIENE_CHECK.md`, `BUILD_LEDGER.md` | Authority | All governance scripts PASS; classification recorded without editing root docs. | `A2.7.md` | A1 |

## Phase 3 — Contract design

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| C3.1 | Inventory current schemas, IDs, references, contradictions, and migration consumers. | H1.5, A2.7 | `docs/active/contracts/**` | Contracts | Complete include/revise/deprecate table. | `C3.1.md` | C1 |
| C3.2 | Specify normalized SMC contract and Markdown normalization/amendment rules. | C3.1 | `docs/active/contracts/SMC_CONTRACT.md` | SMC | Every template field mapped; unknown/missing behavior defined. | `C3.2.md` | C1 |
| C3.3 | Specify assessment receipt and semantic validation rules. | C3.1 | `docs/active/contracts/RECEIPT_CONTRACT.md` | Receipt | IDs, totals, timestamps, modes, quality states, and issue codes complete. | `C3.3.md` | C1 |
| C3.4 | Specify pairing and pressure-delta policy. | C3.3 | `docs/active/contracts/PAIRING_CONTRACT.md` | Pairing | Form/skill tolerance, denominators, timeout/partial/degraded/minimum evidence rules complete. | `C3.4.md` | C1 |
| C3.5 | Specify proposal, append-only approval event, and transition evaluator. | C3.1 | `docs/active/contracts/APPROVAL_CONTRACT.md` | Approval | Actor/action/revision/provenance complete; key globally binds canonical event; identical replay succeeds; changed payload or R1→R2 key reuse conflicts. | `C3.5.md` | C1 |
| C3.5A | Amend proposal/approval contract with exact machine-testable wire format for proposal evidence references, SMC references, authorship, and empty-evidence rationale. | C3.5 | `docs/active/PROJECT_TASKS.md`, `docs/active/contracts/APPROVAL_CONTRACT.md`, `docs/active/contracts/LOCK_AUDIT.md` if needed, `docs/active/BUILD_LEDGER.md`, `docs/active/receipts/C3.5A.md`, `.agent/claims/**`, `.agent/state.log`, `docs/active/authority.json` for required rehash | Contracts / approval | Exact proposal/event envelopes and nested shapes, evidence/SMC/authorship/rationale, revision/hash/actor/replay/conflict rules, issue codes, and positive/negative examples sufficient for T4.4. | `C3.5A.md` | C1 |
| C3.6 | Specify parent brief and atomic ledger contracts. | C3.2, C3.3, C3.5 | `docs/active/contracts/BRIEF_LEDGER_CONTRACT.md` | Brief/ledger | Canonical JSON, clock/ID, linkage, retention, replay, and fault behavior complete. | `C3.6.md` | C1 |
| C3.6A | Amend parent brief/ledger contract with exact machine-testable ledger wire and file format. | C3.6 | `docs/active/PROJECT_TASKS.md`, `docs/active/contracts/BRIEF_LEDGER_CONTRACT.md`, `docs/active/contracts/LOCK_AUDIT.md` if needed, `docs/active/BUILD_LEDGER.md`, `docs/active/receipts/C3.6A.md`, `.agent/claims/**`, `.agent/state.log`, `docs/active/authority.json` for required rehash | Contracts / ledger | Exact ledger and entry envelopes, nested types, payload/source/approval/brief references, hash projections, IDs, ordering, replay/conflict, atomic faults, retention/deletion/tombstones, unknown fields, issue codes, and positive/negative examples sufficient for T4.5. | `C3.6A.md` | C1 |
| C3.7 | Approve registry/version/migration design and schema backlog. | C3.2, C3.4, C3.5, C3.6 | `CONTRACT_VERSION_POLICY.md`, `docs/active/contracts/REGISTRY_DESIGN.md` | Contracts | Zero unresolved field ambiguity; human approval recorded. | `C3.7.md` | C1 |
| C3.7A | Amend registry/versioning contract with exact machine-testable registry wire format. | C3.7 | `docs/active/PROJECT_TASKS.md`, `docs/active/contracts/REGISTRY_DESIGN.md`, `docs/active/contracts/CONTRACT_VERSION_POLICY.md` if needed, `docs/active/contracts/LOCK_AUDIT.md` if needed, `docs/active/BUILD_LEDGER.md`, `docs/active/receipts/C3.7A.md`, `.agent/claims/**`, `.agent/state.log`, `docs/active/authority.json` for required rehash | Contracts / registry | Exact envelope, nested types, compatibility, fixtures/hashes, approval reference, lifecycle/resolution, canonicalization, unknown fields, migration/version resolution, issue codes, and positive/negative examples sufficient for T4.1. | `C3.7A.md` | C1 |
| C3.8 | Decide whether `I1_MOCK_ADAPTERS` is inside production F1 scope. | C3.7 | `docs/active/PRODUCTION_SCOPE_DECISION.md`, `authority.json` via human authority update | Scope | **EXCLUDE** selected; T4.11 and Phase 10 are not claimable; F1 excludes I1. | `C3.8.md` | C1 |

## Stage 4 — Execution readiness

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| R4.0 | Run native-Windows pytest/filesystem host canary. | H1.5, A2.7 | `tests/canary/**`, `scripts/run_host_canary.py`, temporary OS directory | Host runtime | Trivial pytest plus >260 path, drive-case, reserved-name, junction/reparse probes record supported or deterministic fail-closed behavior; infrastructure errors are distinct. | `R4.0.md` | R4 |
| R4.1 | Pin Python/development dependencies and Windows runtime matrix. | H1.5, C3.8, R4.0 | future packaging manifest, lockfile, `HERMES_COMPATIBILITY_MATRIX.md` | Runtime | Clean environment resolves exact dependencies; host-canary constraints recorded; human approves harness changes. | `R4.1.md` | R4 |
| R4.2 | Select and manually prove the enforceable Hermes sandbox/tool restriction baseline. | H1.5, R4.0 | `docs/active/SECURITY_BASELINE.md`, temporary Hermes home | Trust boundary | Disabled tools and containment behavior observed offline. | `R4.2.md` | R4 |
| R4.3 | Install human-owned ignore/hook policy for generated private data. | A2.7 | `.gitignore`, human-owned hook config | Privacy | Staged forbidden synthetic sentinel is rejected; no real data used. | `R4.3.md` | R4 |
| R4.4 | Write and prove mutation-runner meta-canaries. | R4.1 | `tests/mutation_canary/**`, `scripts/run_mutation_checks.py` | Test harness | Behavior-changing mutant is KILLED; no-op/equivalent control is SURVIVED/SKIPPED; crash/setup/timeout is ERROR. | `R4.4.md` | R4 |
| R4.5 | Execute full Stage 4 checklist and write readiness result. | R4.2, R4.3, R4.4 | `READINESS_REPORT.md`, `ARCHIVE_HYGIENE_CHECK.md` | Readiness | Every checklist row PASS and critical risks zero. | `R4.5.md` | R4 |

## Phase 4 — RED tests and fixtures

All rows permit only `tests/**` and `fixtures/**` named by the task. Production/plugin/profile/schema implementation is forbidden.

| ID | Task | Depends | Graph scope | Required RED evidence | Receipt | Gate |
|---|---|---|---|---|---|---|
| T4.1 | Write schema-registry and contract-version tests. | R4.5 | Contracts | Fails because new schemas/registry do not exist. | `T4.1.md` | T1 |
| T4.2 | Write receipt semantic-validator positive/negative tests and mutation probe. | R4.5, C3.3 | Receipt | Fails for missing semantic validator, not malformed fixtures; probe obeys mutation meta-contract. | `T4.2.md` | T1 |
| T4.3 | Write pairing/pressure policy tests and mutations. | T4.2, C3.4 | Pairing | Fails for missing pairing evaluator. | `T4.3.md` | T1 |
| T4.4 | Write approval actor/revision/replay/transition tests and mutations. | R4.5, C3.5 | Approval | Fails for missing evaluator; includes same-key changed-payload and R1→R2 cross-revision conflict cases. | `T4.4.md` | T1 |
| T4.5 | Write atomic ledger/idempotency/fault-injection tests and mutations. | R4.5, C3.6 | Ledger | Fails for missing ledger implementation; probe obeys mutation meta-contract. | `T4.5.md` | T1 |
| T4.6 | Write Windows traversal/reparse/redaction/retention/commit-eligibility tests. | R4.5, R4.2 | Privacy | Fails for missing guards, not unsupported host behavior; uses R4.0 capability result. | `T4.6.md` | T1 |
| T4.7 | Write skill layout/frontmatter/reference/native-discovery tests and mutation. | R4.5, H1.4 | Skills | Fails against current flat skills and missing references; probe obeys mutation meta-contract. | `T4.7.md` | T1 |
| T4.8 | Write isolated distribution install, plugin delivery, arbitrary-name, and stock-smoke tests. | R4.5, H1.3 | Profile | Fails because distribution/profile/plugin files do not exist. | `T4.8.md` | T1 |
| T4.9 | Write deterministic diagnosis/brief/proposal/plugin-command tests. | R4.5, C3.6 | Core | Fails because core plugin does not exist. | `T4.9.md` | T1 |
| T4.10 | Write offline synthetic-week and repeatability tests. | T4.2, T4.3, T4.4, T4.5, T4.9 | E2E | Fails because orchestrator is missing. | `T4.10.md` | T1 |
| T4.11 | **EXCLUDED / NOT CLAIMABLE** — mock-adapter isolation/fault tests. | C3.8=EXCLUDE | Adapters | No task or receipt in this release; excluded from T1/F1. | none | excluded |
| T4.12 | Write branding/install-name equivalence and stock-identity tests. | T4.8 | Branding | Fails because distribution presentation is absent. | `T4.12.md` | T1 |

## Phase 5 — Skill packaging GREEN

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| S5.1 | Move flat skills into H1-proven native directories with minimum frontmatter fixes. | T4.7 | `skills/**` | Skills | Packaging tests move from expected RED toward GREEN; content diff reviewed. | `S5.1.md` | S1 |
| S5.2 | Repair, supply, or explicitly remove every broken skill reference. | S5.1 | `skills/**` | Skills | Reference test GREEN; provenance/rationale for each change. | `S5.2.md` | S1 |
| S5.3 | Run native discovery/load and reference mutation gate. | S5.2 | tests/receipts only | Skills | Native Hermes load passes and renamed/deleted reference mutation is killed. | `S5.3.md` | S1 |

## Phase 6 — Profile distribution GREEN

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| P6.1 | Add minimum profile payload sources and generate the staging tree. | T4.8, S5.3 | named profile sources, staging builder inputs, ignored `dist/**` | Profile | Isolated staging-tree install tests GREEN; repo-root install rejected; no secret or hardcoded `thoth`. | `P6.1.md` | PR1 |
| P6.2 | Add minimum plugin manifest/skeleton and proven distribution-owned paths. | P6.1, T4.8 | `plugins/hermes-thrice-great/**`, `distribution.yaml` | Plugin | Plugin discovered but performs no untested core behavior; delivery test GREEN. | `P6.2.md` | PR1 |
| P6.3 | Prove installs as `ucc` and `thoth`, config isolation, update preservation, and stock smoke. | P6.2 | tests/receipts only | Profile | Alias equivalence/install lifecycle tests GREEN in temporary homes with synthetic install fixtures only; stock smoke unchanged; output warns PR1 is not safe-to-operate. | `P6.3.md` | PR1 |

## Phase 7 — Privacy and sandbox GREEN

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| SEC7.1 | Implement minimum enforceable disabled-tool/sandbox profile configuration. | P6.3, T4.6 | `config.yaml`, distribution docs | Tool boundary | Disabled web/messaging/nonessential tool tests GREEN. | `SEC7.1.md` | SEC1 |
| SEC7.2 | Implement path containment and log redaction guards. | SEC7.1, T4.6 | plugin privacy modules | Filesystem/privacy | Native Windows adversarial tests GREEN; path mutations killed. | `SEC7.2.md` | SEC1 |
| SEC7.3 | Implement pseudonymous record, retention/delete, and staged-output guards. | SEC7.2, R4.3 | plugin privacy modules, validation scripts | Data lifecycle | Retention/delete and commit-eligibility tests GREEN. | `SEC7.3.md` | SEC1 |

## Phase 8 — Deterministic core GREEN

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| U8.1 | Implement versioned schemas and registry. | T4.1, C3.7 | named `schemas/*.json`, registry | Contracts | T4.1 GREEN; positive/negative schema fixtures pass. | `U8.1.md` | U1 |
| U8.2 | Implement semantic receipt validator with stable issue codes. | U8.1, T4.2 | plugin validator modules | Receipt | T4.2 GREEN; totals/timestamp/mode mutations killed. | `U8.2.md` | U1 |
| U8.3 | Implement pairing evaluator and gated pressure delta. | U8.2, T4.3 | plugin pairing modules | Pairing | T4.3 GREEN; form/skill/sample mutations killed. | `U8.3.md` | U1 |
| U8.4 | Implement deterministic diagnosis facts, parent brief, and proposal. | U8.3, T4.9 | plugin core/templates | Diagnosis/brief | Deterministic focused tests GREEN; no model call. | `U8.4.md` | U1 |
| U8.5 | Implement approval-event validation and transition evaluator. | U8.4, T4.4 | plugin approval modules | Approval | T4.4 GREEN; AI/wrong-revision/replay mutations killed. | `U8.5.md` | U1 |
| U8.6 | Implement atomic, idempotent local ledger. | U8.5, T4.5, SEC7.3 | plugin ledger modules | Ledger | T4.5 GREEN; injected write faults preserve prior state. | `U8.6.md` | U1 |
| U8.7 | Register offline UCC CLI/tool surface through native plugin API. | U8.2, U8.6, P6.2 | plugin registration/CLI modules | Plugin | Offline doctor/validate/dry-run commands pass; stock smoke passes. | `U8.7.md` | U1 |

## Phase 9 — Synthetic weekly dry run

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| E9.1 | Complete valid and adversarial synthetic week fixture sets. | U8.7, T4.10 | `fixtures/synthetic/**` | E2E | Fixture validator passes; synthetic labels and no real identifiers. | `E9.1.md` | E1 |
| E9.2 | Implement minimum offline weekly orchestrator. | E9.1 | plugin orchestration modules | E2E | T4.10 valid flow GREEN; invalid flows fail with expected codes. | `E9.2.md` | E1 |
| E9.3 | Prove repeatability, zero-network operation, approval wait/approve flow, and ledger safety. | E9.2 | tests/receipts only | E2E | Two canonical runs equal; network sentinel sees zero attempts. | `E9.3.md` | E1 |

## Phase 10 — EXCLUDED / NOT CLAIMABLE for this release

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| I10.1 | **EXCLUDED / NOT CLAIMABLE** — mock Discord and Campaign OS adapters. | C3.8=EXCLUDE | none | Adapters | No implementation in this release. | none | excluded |
| I10.2 | **EXCLUDED / NOT CLAIMABLE** — adapter fault proof. | C3.8=EXCLUDE | none | Adapters | No implementation in this release. | none | excluded |

## Phase 11 — Branding and aliases

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| B11.1 | Add distribution/profile-driven Hermes Thrice Great presentation. | E9.3, T4.12 | `SOUL.md`, `distribution.yaml`, plugin presentation files | Branding | Branding tests GREEN; no upstream files touched. | `B11.1.md` | B1 |
| B11.2 | Prove `ucc`, `hermes-thrice-great`, and optional `thoth` semantic equivalence. | B11.1 | tests/receipts only | Aliases | Canonical smoke outputs equivalent; stock identity unchanged. | `B11.2.md` | B1 |

## Phase 12 — Handoff and learning

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| F12.0 | **PRE-F12.0 amendment:** integrate installed `hermes ucc` CLI commands with deterministic validation, installed synthetic resources, and offline weekly orchestration. | U8.7, E9.3, B11.2 | plugin CLI/orchestration/resources, tests, governance bookkeeping | CLI / installed resources / synthetic orchestrator | Installed valid fixtures pass; adversarial cases fail with stable issues; real seven-stage dry-run; zero socket/model calls. | `PRE-F12.0.md` | F1 precondition |
| F12.1 | Update owner/install/runbook documentation to match the proven distribution. | E9.3, B11.2, F12.0 | `README.md`, `INSTALL.md`, `docs/**` excluding authority | Handoff | Commands replay successfully on clean Windows environment. | `F12.1.md` | F1 |
| F12.2 | Run clean-room final acceptance and finalize readiness/risk/compatibility reports. | F12.1 | reports and receipts only | Acceptance | Final command set PASS; critical risks zero; I1 excluded by C3.8. | `F12.2.md` | F1 |
| F12.3 | Finalize build ledger, learning cards, and post-release upstream drift task. | F12.2 | `BUILD_LEDGER.md`, `learning_cards.md`, compatibility report | Learning | Every DONE task/receipt/state event reconciles; no upstream update performed. | `F12.3.md` | F1 |

## Phase 13 — Post-F1 release sharing

| ID | Task | Depends | Allowed files | Graph scope | Validation / evidence | Receipt | Gate |
|---|---|---|---|---|---|---|---|
| REL13.1 | Update README/INSTALL sharing guidance with external companion-resource links and prepare GitHub repository publication instructions. | F12.3 | `README.md`, `INSTALL.md`, `docs/active/OWNER_RUNBOOK.md`, `.gitignore`, release/share notes, governance bookkeeping | Release sharing / documentation / GitHub publication preparation | Synthetic-offline scope, external-resource boundaries, repository slug, evaluator quickstart, and private-publication safety are explicit and mechanically checked. | `REL13.1.md` | post-F1 sharing |

## Claim JSON minimum

```json
{
  "task_id": "U8.2",
  "agent_id": "agent-id",
  "claimed_at": "2026-06-30T00:00:00Z",
  "active_plan_hash": "sha256:...",
  "allowed_files": ["plugins/hermes-thrice-great/core/validation/**"],
  "forbidden_files": ["docs/archive/**", "docs/active/BUILD_PLAN.md", "docs/active/PROJECT_TASKS.md", "docs/active/authority.json"],
  "status": "IN_PROGRESS"
}
```

Required state events: `CLAIM_CREATED`, `TASK_IN_PROGRESS`, `TASK_BLOCKED`, `TASK_FAILED`, `TASK_DONE`, `DRIFT_PAUSE`. A task may emit only the events relevant to its actual lifecycle, but the checker must support and test all six.
