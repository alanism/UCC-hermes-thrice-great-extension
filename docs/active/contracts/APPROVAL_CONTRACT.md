# Proposal, Approval Event, and Transition Contract

Status: C3.5 PROPOSED LOCK

Contracts:

- `ucc.task_proposal.v1`
- `ucc.approval_event.v1`
- `ucc.approval_transition.v1`

## Authority boundary

A proposal describes a requested future action. It is never authority by itself. Task/card/campaign status, model text, a skill result, profile identity, a Discord message, or a filename cannot approve anything.

Only a validated append-only approval event from a configured `parent_guardian` actor can authorize the exact current proposal revision and payload hash. AI and Hermes may author proposals; they cannot author parent decision events.

## Task proposal

### Identity and envelope

| Field | Rule |
|---|---|
| `contract_version` | `ucc.task_proposal.v1`. |
| `proposal_id` | `prop_<ULID>`; stable across revisions. |
| `proposal_revision` | Positive integer starting at 1 and incrementing by exactly 1. |
| `supersedes_revision` | Null for revision 1; otherwise exactly previous revision. |
| `proposal_type` | `task`, `campaign`, or `smc_amendment`. |
| `learner_id` | Pseudonymous learner ID or null when proposal is not learner-specific. |
| `created_at` | Injected UTC timestamp. |
| `created_by` | `actor_type` (`parent_guardian`, `learning_coach`, `ai`, or `system`) and pseudonymous actor ID. |
| `smc_ref` | Active `smc_id`, exact revision, and canonical payload hash. Required for learner-specific task/campaign proposals. |
| `source_evidence_refs` | Sorted unique validated receipt/pair/ledger IDs; may be empty only with explicit rationale. |
| `proposal_payload` | Exact requested action below. |
| `proposal_payload_sha256` | Hash of canonical `proposal_payload` plus identity/revision/SMC/evidence refs. |
| `proposal_state` | `draft`, `awaiting_decision`, `withdrawn`, or `superseded`; never `approved`, `active`, or `done`. |

Approval state is deliberately absent from the proposal document. It is derived by the transition evaluator from append-only events.

### Proposal payload

Common required fields:

- `title`;
- `objective`;
- `rationale`;
- `requested_actions`: ordered structured actions, never shell/model text;
- `expected_evidence`: typed evidence requirements and valid-evidence claim;
- `start_not_before` and `complete_not_after`, each UTC timestamp or null;
- `risk_flags`: sorted stable codes;
- `data_access`: declared local contract/artifact types required;
- `external_effects`: empty array in the core production distribution;
- `stop_conditions`;
- `parent_summary`.

`expected_evidence.valid_claim` uses `practice`, `familiarity`, `performance`, or `mastery_candidate`. A proposal cannot promise mastery. AI role, process evidence, and student-thinking evidence requirements must be explicit when mastery-candidate evidence is requested.

For `smc_amendment`, payload also requires `smc_id`, `base_revision`, JSON Patch operations, and canonical patch hash as defined by the SMC contract.

### Revision rules

- Revisions are immutable snapshots; no in-place payload edit.
- Any semantic payload, SMC reference, evidence reference, date window, risk, or stop-condition change creates the next revision and a new hash.
- Approval for revision R1 never transfers to R2.
- A new revision sets the earlier one to derived `superseded`; it does not modify the old record.
- Only the highest existing revision may enter `awaiting_decision`.

## Approval event

Approval events are immutable and append-only.

| Field | Rule |
|---|---|
| `contract_version` | `ucc.approval_event.v1`. |
| `approval_event_id` | `appr_<ULID>`; stable for exact replay. |
| `ledger_namespace` | Configured local namespace; participates in idempotency scope. |
| `idempotency_key` | `idem_<ULID>` or equivalent 128-bit opaque key; globally unique inside namespace. |
| `proposal_id` | Exact target proposal. |
| `proposal_revision` | Exact positive revision. |
| `proposal_payload_sha256` | Must equal stored target revision hash. |
| `proposal_type` | Must equal stored target type. |
| `actor_type` | Must be `parent_guardian` for a valid decision. |
| `actor_id` | Pseudonymous configured parent/guardian authority ID. |
| `action` | `approve`, `approve_smc_amendment`, `reject`, `request_changes`, or `revoke`. |
| `decision_at` | UTC time the human decision was captured. |
| `reason_code` | Optional stable non-sensitive code. |
| `reason_note` | Optional sensitive local note; excluded from logs but included in event hash. |
| `provenance` | Local capture provenance below. |
| `revokes_approval_event_id` | Required only for `revoke`; must reference accepted approval for same proposal revision. |

Action constraints:

- `approve` is valid only for `task` and `campaign`.
- `approve_smc_amendment` is valid only for `smc_amendment` and satisfies the SMC contract action.
- `reject` and `request_changes` are valid for an undecided current revision.
- `revoke` is valid only after an accepted approval action and cannot target rejection/change events.

### Provenance

Required fields:

- `capture_contract_version`;
- `capture_channel`: `local_ui`, `local_cli`, `signed_local_file`, or `synthetic_test`;
- `source_event_id`;
- `source_payload_sha256`;
- `captured_at` UTC;
- `authority_configuration_sha256`.

`synthetic_test` is accepted only in test mode and can never authorize a non-synthetic namespace. Live messaging text is not a capture channel. Any future adapter must convert a human interaction into a separately authenticated local capture event under a future approved contract; the inbound message itself is never approval.

## Canonical idempotency binding

Within one `ledger_namespace`, the first accepted use of `idempotency_key` permanently binds it to the canonical approval semantic payload:

```text
approval_event_id
proposal_id
proposal_revision
proposal_payload_sha256
proposal_type
actor_type
actor_id
action
decision_at
reason_code
reason_note
provenance.capture_contract_version
provenance.capture_channel
provenance.source_event_id
provenance.source_payload_sha256
provenance.captured_at
provenance.authority_configuration_sha256
revokes_approval_event_id
```

The binding hash excludes only storage `recorded_at` and physical file location. It includes null markers and uses registry canonical JSON.

- Exact same key plus byte-identical canonical binding payload returns the original accepted result and does not append a second event.
- Same key plus any changed field returns `IDEMPOTENCY_CONFLICT`.
- Reusing a key from proposal revision R1 for R2 is a conflict even if all other values match.
- A new key with a second incompatible decision for the same revision returns `APPROVAL_DECISION_CONFLICT`.

Idempotency is not composite uniqueness on key+revision. The key alone is unique within the namespace.

## Validation order

The evaluator performs checks in this order and returns all safe deterministic issues applicable at each completed layer:

1. schema and supported contract versions;
2. namespace and authority configuration;
3. proposal identity, current revision, type, state, and payload hash;
4. actor authorization;
5. action/type rules and revocation target;
6. provenance authenticity/allowlist;
7. idempotency-key lookup and canonical binding comparison;
8. existing accepted-decision conflict;
9. transition calculation.

An invalid event is never appended to the authoritative approval stream. It may be preserved in a quarantined audit area containing no raw learner evidence.

## Transition evaluator

Inputs:

- immutable target proposal revision;
- current proposal-control state;
- current execution state;
- ordered accepted approval events for the proposal;
- idempotency binding index;
- authority configuration/registry snapshot.

Derived decision states:

- `awaiting_decision`;
- `approved`;
- `rejected`;
- `changes_requested`;
- `revoked`;
- `withdrawn`;
- `superseded`.

Execution states are separate:

- `not_started`;
- `scheduled`;
- `active`;
- `completed`;
- `cancelled`.

Rules:

1. `approve` or `approve_smc_amendment` on the current awaiting revision derives `approved`.
2. Only derived `approved` permits `not_started -> scheduled` or `not_started -> active`.
3. `reject` derives `rejected`; that revision cannot be approved later.
4. `request_changes` derives `changes_requested`; work requires a new revision and new approval.
5. `revoke` derives `revoked`. If execution is scheduled, it must cancel. If active, result emits `halt_required`; revocation does not erase completed evidence or ledger history.
6. Approval does not permit `completed`; completion requires the later evidence/ledger contract.
7. Withdrawn or superseded proposals reject new approval events.
8. Exact idempotent replay returns the original transition result with `replayed: true` and no state/event duplication.
9. Event arrival order cannot alter the result because the first accepted terminal decision for a revision binds it; conflicting later decisions are rejected.

Transition result fields:

- `contract_version: ucc.approval_transition.v1`;
- proposal ID/revision/hash;
- accepted event ID or null;
- `prior_decision_state` and `next_decision_state`;
- `prior_execution_state` and permitted next execution states;
- `halt_required` and `cancel_required` booleans;
- `replayed` boolean;
- stable issues;
- canonical input/output hashes.

## Stable issue codes

| Code | Meaning |
|---|---|
| `PROPOSAL_SCHEMA_INVALID` | Proposal shape/version invalid. |
| `PROPOSAL_REVISION_INVALID` | Revision chain is missing, duplicated, or non-monotonic. |
| `PROPOSAL_NOT_CURRENT` | Event targets a superseded/non-highest revision. |
| `PROPOSAL_STATE_NOT_DECIDABLE` | Proposal is not awaiting decision. |
| `PROPOSAL_PAYLOAD_HASH_MISMATCH` | Event hash differs from stored revision. |
| `APPROVAL_SCHEMA_INVALID` | Event shape/version invalid. |
| `APPROVAL_NAMESPACE_INVALID` | Namespace is missing/unrecognized. |
| `APPROVAL_ACTOR_UNAUTHORIZED` | Actor is not configured parent/guardian authority. |
| `APPROVAL_ACTION_INVALID` | Action is invalid for proposal type/state. |
| `APPROVAL_PROVENANCE_INVALID` | Capture provenance is missing, untrusted, or mismatched. |
| `APPROVAL_REVOCATION_TARGET_INVALID` | Revoke target is absent or not matching approval. |
| `IDEMPOTENCY_CONFLICT` | Existing key binding differs in any semantic field. |
| `APPROVAL_DECISION_CONFLICT` | A different terminal decision already binds revision. |
| `APPROVAL_REVISION_MISMATCH` | Event revision differs from current proposal revision. |
| `APPROVAL_REQUIRED` | Execution transition requested without accepted approval. |
| `APPROVAL_REVOKED` | Execution is blocked/cancelled/halt-required after revocation. |
| `APPROVAL_SYNTHETIC_NAMESPACE_VIOLATION` | Synthetic provenance targets non-synthetic state. |

Issues contain IDs, revisions, hashes, enums, and codes only; no proposal prose, evidence bodies, learner names, or parent notes.

## Legacy task-card migration

`hermes_task_card.schema.json` is not approval evidence.

- `cardId` maps to migration provenance, not automatically to proposal ID.
- title/evidence/script fields may seed a draft proposal.
- owner `ai`/`hermes` maps to proposal authorship only.
- every legacy status maps to `proposal_state: draft` or `awaiting_decision` plus a migration note.
- `Done / Evidence Captured`, `Today`, or any active-looking status never creates approval or execution authority.
- no legacy record becomes scheduled/active/completed without a new valid parent event and later evidence checks.

## Acceptance criteria

1. Proposal, decision authority, and execution state are distinct artifacts.
2. AI may propose but cannot approve, reject, request changes, or revoke as a parent actor.
3. Approval binds exact proposal ID, revision, type, payload hash, actor, action, and provenance.
4. Identical replay succeeds once; changed payload, changed provenance, or R1-to-R2 key reuse conflicts.
5. Wrong/stale revision and status-only “approval” fail.
6. Revocation has deterministic cancel/halt behavior and never erases history.
7. Synthetic approval cannot escape a synthetic namespace.
8. No live message is direct authority.
9. Stable semantic inputs produce the same transition result independent of event delivery retries.
