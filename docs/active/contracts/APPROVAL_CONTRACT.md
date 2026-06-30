# Parent Proposal and Approval Wire Contract

Status: C3.5A MACHINE-TESTABLE CONTRACT LOCK; SCHEMA/EVALUATOR TEST-GATED

Contracts:

- `ucc.task_proposal.v1.0.0`;
- `ucc.approval_event.v1.0.0`;
- `ucc.approval_transition.v1.0.0`.

## 1. Authority boundary

A proposal requests a future action. It is never approval by itself. AI and system processes may author, render, validate, or produce evidence for a proposal; they cannot approve learner-state or execution transitions. Only a valid `ucc_parent_approval_event` from a configured `parent`, `guardian`, or `authorized_adult` can authorize the exact current proposal revision and hash.

The six-value `proposal_status` enum includes `approved` and `rejected`, but those two values are evaluator-derived read projections only. Proposal authors may write only `draft` or `ready_for_parent`; revision control may derive `superseded`, and clock/policy evaluation may derive `expired`. A submitted proposal carrying author-asserted `approved` or `rejected` is invalid.

## 2. Closed proposal envelope

The root JSON object contains exactly one member, `ucc_parent_proposal`. Its value is a closed object with these required fields and one optional `extensions` member:

| Field | Type | Rule |
|---|---|---|
| `contract_version` | string | Exactly `ucc.task_proposal.v1.0.0`. |
| `proposal_id` | string | `prop_` plus uppercase 26-character Crockford ULID. |
| `proposal_revision` | positive integer | Starts at 1 and increases exactly by 1. |
| `supersedes_revision` | integer or null | Null for R1; otherwise `proposal_revision - 1`. |
| `proposal_type` | string | `task`, `campaign`, or `smc_amendment`. |
| `learner_id` | string or null | Pseudonymous `lrn_<ULID>`; null only for non-learner-specific proposal. |
| `created_at` | string | Injected RFC 3339 UTC milliseconds. |
| `authorship` | object | Exact authorship object below. |
| `smc_ref` | object or null | Required for learner-specific task/campaign and every SMC amendment. |
| `expected_evidence` | array | Exact evidence references below; sorted by `evidence_ref_id`. |
| `empty_evidence_rationale` | object or null | Required exactly when `expected_evidence` is empty. |
| `proposal_payload` | object | Exact requested-action payload below. |
| `proposal_status` | string | `draft`, `ready_for_parent`, `superseded`, `approved`, `rejected`, or `expired`. |
| `canonical_hash` | string | Lowercase SHA-256 of the canonical proposal projection. |
| `extensions` | object | Optional namespaced resolution-inert values. |

Unknown root or proposal members are `PROPOSAL_UNKNOWN_FIELD`.

## 3. Exact SMC reference

`smc_ref` is null or contains exactly:

```json
{
  "smc_id": "smc_01J00000000000000000000000",
  "smc_version": "ucc.smc.v1.0.0",
  "canonical_hash": "64 lowercase hexadecimal characters",
  "source_path": "local/contracts/smc-active.json",
  "approved_at": "2026-06-30T00:00:00.000Z"
}
```

`source_path` is a normalized contained relative path: no drive, UNC, leading slash, `.` or `..`. The referenced SMC must be active, hash-matched, and approved no later than proposal creation. Unknown members are rejected.

## 4. Exact authorship representation

`authorship` contains exactly:

| Field | Type | Rule |
|---|---|---|
| `proposal_author` | object | `actor_role` and `actor_id`. |
| `evidence_producers` | array | Sorted by `producer_id`; may be empty only with empty expected evidence. |
| `rendered_by` | object or null | Rendering process identity. |
| `validated_by` | object or null | Validation process identity. |

`proposal_author` is:

```json
{"actor_role": "ai", "actor_id": "act_01J00000000000000000000001"}
```

Author roles are `parent`, `guardian`, `authorized_adult`, `learning_coach`, `ai`, or `system`.

Each evidence producer contains exactly `producer_role`, `producer_id`, and `evidence_ref_ids`. Producer roles are `parent`, `guardian`, `authorized_adult`, `learning_coach`, `learner`, `ai`, or `system`. Evidence IDs are sorted, unique, and must exist in `expected_evidence`.

`rendered_by` and `validated_by` each contain exactly `process_id` and `process_version`; both are non-empty strings. They record process provenance, not authority.

No `approval_actor`, `approved_by`, approval key, or decision is permitted inside `authorship`. Conflation yields `PROPOSAL_AUTHORSHIP_CONFLATED`.

## 5. Exact expected-evidence representation

`expected_evidence` is an array of closed objects. Each contains exactly:

| Field | Type | Rule |
|---|---|---|
| `evidence_ref_id` | string | `eref_<ULID>`; unique and sorted. |
| `evidence_type` | string | `assessment_receipt`, `receipt_pairing`, `ledger_entry`, `process_artifact`, or `student_thinking_artifact`. |
| `source_receipt_id` | string or null | `rcpt_<ULID>` only for assessment-receipt evidence. |
| `source_pairing_id` | string or null | `pres_<ULID>` only for receipt-pairing evidence. |
| `required` | boolean | Whether approval requires the reference. |
| `claim_supported` | string | `practice`, `familiarity`, `performance`, or `mastery_candidate`; never mastery established. |
| `quality_state` | string | `clean`, `limited`, `degraded`, `void`, or `suppressed`. |

For `assessment_receipt`, `source_receipt_id` is non-null and `source_pairing_id` null. For `receipt_pairing`, the inverse applies. For all other types both source fields are null. `void` or `suppressed` evidence cannot be required and cannot support a claim. `degraded` evidence may support observed facts only, never `mastery_candidate`.

## 6. Empty-evidence rationale

`empty_evidence_rationale` is null when evidence is non-empty. When evidence is empty it contains exactly:

```json
{
  "reason_code": "administrative_only",
  "human_readable_reason": "Synthetic administrative proposal; no learner evidence required.",
  "allowed_claim_scope": "administrative_only"
}
```

`reason_code` is `administrative_only`, `no_prior_evidence`, or `smc_amendment_context`. `allowed_claim_scope` is `administrative_only`, `practice_only`, `planning_only`, or `none`.

An empty-evidence proposal cannot request or authorize `mastery_candidate` or `mastery_state`, cannot change a mastery ledger state, and cannot claim evidence exists. Violation is `PROPOSAL_EMPTY_EVIDENCE_SCOPE_INVALID`.

## 7. Exact proposal payload

`proposal_payload` is closed and contains exactly:

| Field | Type | Rule |
|---|---|---|
| `title` | string | Non-empty presentation text. |
| `objective` | string | Non-empty requested outcome. |
| `rationale` | string | Non-empty; not authority. |
| `requested_claim_scope` | string | `administrative`, `practice`, `familiarity`, `performance`, `mastery_candidate`, or `mastery_state`. |
| `requested_actions` | array | Non-empty ordered action objects. |
| `start_not_before` | string or null | UTC milliseconds. |
| `complete_not_after` | string or null | UTC milliseconds; not before start. |
| `risk_flags` | array | Sorted unique stable strings. |
| `data_access` | array | Sorted unique local contract/artifact type codes; never paths. |
| `external_effects` | array | Must be empty in this production distribution. |
| `stop_conditions` | array | Non-empty closed stop-condition objects. |
| `parent_summary` | string | Non-empty local presentation text. |

Each requested action contains exactly `action_id`, `action_type`, `owner_role`, `target_ref`, `instructions`, `not_before`, `not_after`, `expected_evidence_codes`, and `requires_parent_presence`.

- `action_id`: `actn_<ULID>`;
- `action_type`: `learning_session`, `assessment_session`, `parent_dialogue`, `evidence_review`, `artifact_creation`, or `smc_amendment`;
- `owner_role`: `parent`, `guardian`, `authorized_adult`, `learning_coach`, `learner`, or `system`;
- `target_ref`: null or common typed record reference (`contract_version`, `record_id`, `canonical_payload_sha256`, `quality_or_status`, `resolution_state`);
- `instructions`: non-empty deterministic text, never shell/model commands;
- action timestamps: nullable UTC milliseconds with valid order;
- `expected_evidence_codes`: sorted unique non-empty stable strings;
- `requires_parent_presence`: boolean.

Each stop condition contains exactly `code` and `description`, both non-empty strings. Stop-condition codes are sorted and unique.

## 8. Proposal revision and canonical hash

Revisions are immutable. Any semantic payload, SMC, evidence, authorship, date, risk, data-access, stop-condition, or rationale change creates exactly the next revision. R1 has null `supersedes_revision`; Rn names n-1. Only the highest non-expired revision may be `ready_for_parent`. An older revision is `superseded`.

Proposal `canonical_hash` is SHA-256 over RFC 8785/JCS UTF-8 bytes of the `ucc_parent_proposal` value after recursively removing every `extensions` member plus top-level `canonical_hash` and `proposal_status`. Status is excluded because it is derived control state; revision and all authority-relevant semantic fields remain included.

## 9. Closed approval-event envelope

The root contains exactly `ucc_parent_approval_event`. Its closed value contains:

| Field | Type | Rule |
|---|---|---|
| `contract_version` | string | Exactly `ucc.approval_event.v1.0.0`. |
| `approval_event_id` | string | `appr_<ULID>`; injected, not payload-derived. |
| `approval_key` | string | `idem_<ULID>`; injected and globally unique in namespace. |
| `ledger_namespace` | string | Configured local namespace. |
| `proposal_id` | string | Exact target ID. |
| `proposal_revision` | positive integer | Exact current revision. |
| `proposal_hash` | string | Exact target proposal `canonical_hash`. |
| `proposal_type` | string | Exact target type. |
| `approval_action` | string | `approve`, `reject`, or `request_revision`. |
| `actor` | object | Exact configured human actor below. |
| `decision_at` | string | Injected human-decision timestamp. |
| `scope` | object | Exact proposal/transition scope below. |
| `reason_code` | string or null | Stable non-sensitive code. |
| `reason_note` | string or null | Sensitive local note; never logged. |
| `provenance` | object | Exact capture provenance below. |
| `canonical_hash` | string | Event semantic binding hash. |
| `extensions` | object | Optional namespaced, resolution-inert values. |

Unknown root/event members are `APPROVAL_UNKNOWN_FIELD`.

### Actor

`actor` contains exactly `actor_role` and `actor_id`. Valid roles are exactly `parent`, `guardian`, and `authorized_adult`. `ai`, `system`, `learner`, `unknown`, and every unconfigured role are unauthorized. `actor_id` is a configured `act_<ULID>`.

### Scope

`scope` contains exactly `proposal_id`, `proposal_revision`, `learner_id`, `proposal_type`, and `decision_effect`. Values must equal the proposal/event. `decision_effect` equals `approve`, `reject`, or `request_revision` and must equal `approval_action`.

### Provenance

`provenance` contains exactly `capture_contract_version`, `capture_channel`, `source_event_id`, `source_payload_sha256`, `captured_at`, and `authority_configuration_sha256`.

`capture_channel` is `local_ui`, `local_cli`, `signed_local_file`, or `synthetic_test`. Synthetic capture is valid only in an explicitly synthetic namespace. A live message is never approval authority.

## 10. Approval IDs, hash, and idempotency binding

`approval_event_id` and `approval_key` are injected ULIDs, never truncated content hashes. Exact replay reuses both. New semantic decisions require a new event ID and key.

Event `canonical_hash` is SHA-256 over RFC 8785/JCS bytes of the `ucc_parent_approval_event` value after recursively removing `extensions` and top-level `canonical_hash`.

Within one `ledger_namespace`, the first accepted `approval_key` permanently binds every field in that canonical projection, including event ID, proposal revision/hash, action, actor, decision timestamp, scope, reason null markers, and provenance.

- identical key and identical canonical projection returns the original result with `replayed: true` and appends nothing;
- same key with any changed field is `IDEMPOTENCY_CONFLICT`;
- reusing an R1 key for R2 is `IDEMPOTENCY_CONFLICT`, even if the action/actor match;
- R2 requires a new event ID/key and an event explicitly naming revision 2 and its new proposal hash;
- a new key carrying a conflicting terminal action for an already decided revision is `APPROVAL_DECISION_CONFLICT`.

## 11. Proposal-to-approval validation and transitions

Validation order is schema/version, namespace, exact proposal ID/current revision/type/status/hash, human actor configuration, action, provenance, approval-key binding, prior decision conflict, then transition.

Only `ready_for_parent` is decidable. Rules:

- `approve` derives proposal status `approved` and permits execution `not_started -> scheduled|active`;
- `reject` derives `rejected` and permits no execution;
- `request_revision` derives the current revision `superseded`; a new R+1 proposal starts as `draft` and needs a new approval event;
- `draft`, `superseded`, `expired`, author-asserted `approved`, and author-asserted `rejected` reject decision events;
- approval never permits `completed`; evidence/ledger contracts control completion;
- event delivery order cannot change the first accepted terminal decision.

Revocation is not an approval action in this v1 wire contract. Adding it requires a new contract version and explicit transition rules.

Transition result contains exactly `contract_version`, proposal ID/revision/hash, accepted event ID or null, prior/next proposal status, prior execution state, permitted next execution states, `replayed`, sorted `issues`, canonical input hash, and canonical output hash.

## 12. Stable issue codes

| Code | Condition |
|---|---|
| `PROPOSAL_SCHEMA_INVALID` | Required/type/enum failure. |
| `PROPOSAL_UNKNOWN_FIELD` | Unknown member outside namespaced extensions. |
| `PROPOSAL_REVISION_INVALID` | Revision/supersedes chain invalid. |
| `PROPOSAL_NOT_CURRENT` | Event targets non-highest revision. |
| `PROPOSAL_STATUS_NOT_DECIDABLE` | Status is not evaluator-accepted `ready_for_parent`. |
| `PROPOSAL_HASH_MISMATCH` | Recomputed proposal hash differs. |
| `PROPOSAL_SMC_REF_INVALID` | SMC reference missing, malformed, unapproved, escaping, or hash-mismatched. |
| `PROPOSAL_EVIDENCE_INVALID` | Evidence reference shape/applicability/quality invalid. |
| `PROPOSAL_EMPTY_EVIDENCE_RATIONALE_REQUIRED` | Empty evidence lacks rationale. |
| `PROPOSAL_EMPTY_EVIDENCE_SCOPE_INVALID` | Empty evidence attempts mastery-state authority or mismatched scope. |
| `PROPOSAL_AUTHORSHIP_INVALID` | Authorship role/ID/evidence binding invalid. |
| `PROPOSAL_AUTHORSHIP_CONFLATED` | Proposal authorship contains approval authority. |
| `APPROVAL_SCHEMA_INVALID` | Event required/type/enum failure. |
| `APPROVAL_UNKNOWN_FIELD` | Unknown member outside namespaced extensions. |
| `APPROVAL_NAMESPACE_INVALID` | Namespace missing/unrecognized. |
| `APPROVAL_ACTOR_UNAUTHORIZED` | Actor role/ID is not configured human authority. |
| `APPROVAL_ACTION_INVALID` | Action invalid for proposal type/status. |
| `APPROVAL_SCOPE_MISMATCH` | Scope differs from proposal/event/action. |
| `APPROVAL_PROVENANCE_INVALID` | Capture provenance missing/untrusted/mismatched. |
| `APPROVAL_REVISION_MISMATCH` | Event revision differs from current proposal. |
| `APPROVAL_PROPOSAL_HASH_MISMATCH` | Event `proposal_hash` differs from target. |
| `APPROVAL_SYNTHETIC_NAMESPACE_VIOLATION` | Synthetic capture targets non-synthetic namespace. |
| `IDEMPOTENCY_CONFLICT` | Existing key binding differs, including R1-to-R2 reuse. |
| `APPROVAL_DECISION_CONFLICT` | Different terminal decision already binds revision. |
| `APPROVAL_REQUIRED` | Execution requested without accepted approval. |

Issues sort by JSON Pointer path, code, proposal ID, revision, event ID. They never include proposal prose, evidence bodies, learner names, or reason notes.

## 13. Complete positive proposal example

```json
{
  "ucc_parent_proposal": {
    "contract_version": "ucc.task_proposal.v1.0.0",
    "proposal_id": "prop_01J00000000000000000000010",
    "proposal_revision": 1,
    "supersedes_revision": null,
    "proposal_type": "task",
    "learner_id": "lrn_01J00000000000000000000011",
    "created_at": "2026-06-30T01:00:00.000Z",
    "authorship": {
      "proposal_author": {"actor_role": "ai", "actor_id": "act_01J00000000000000000000012"},
      "evidence_producers": [{"producer_role": "system", "producer_id": "act_01J00000000000000000000013", "evidence_ref_ids": ["eref_01J00000000000000000000014"]}],
      "rendered_by": {"process_id": "synthetic-proposal-renderer", "process_version": "1.0.0"},
      "validated_by": {"process_id": "synthetic-proposal-validator", "process_version": "1.0.0"}
    },
    "smc_ref": {"smc_id": "smc_01J00000000000000000000015", "smc_version": "ucc.smc.v1.0.0", "canonical_hash": "1111111111111111111111111111111111111111111111111111111111111111", "source_path": "local/contracts/smc-active.json", "approved_at": "2026-06-30T00:00:00.000Z"},
    "expected_evidence": [{"evidence_ref_id": "eref_01J00000000000000000000014", "evidence_type": "assessment_receipt", "source_receipt_id": "rcpt_01J00000000000000000000016", "source_pairing_id": null, "required": true, "claim_supported": "performance", "quality_state": "clean"}],
    "empty_evidence_rationale": null,
    "proposal_payload": {
      "title": "Synthetic evidence review",
      "objective": "Review one synthetic performance receipt with the parent.",
      "rationale": "The synthetic receipt is ready for parent review.",
      "requested_claim_scope": "performance",
      "requested_actions": [{"action_id": "actn_01J00000000000000000000017", "action_type": "evidence_review", "owner_role": "parent", "target_ref": {"contract_version": "ucc.assessment_receipt.v2.0.0", "record_id": "rcpt_01J00000000000000000000016", "canonical_payload_sha256": "2222222222222222222222222222222222222222222222222222222222222222", "quality_or_status": "clean", "resolution_state": "resolved"}, "instructions": "Review the synthetic receipt and choose approve, reject, or request revision.", "not_before": null, "not_after": null, "expected_evidence_codes": ["performance_receipt"], "requires_parent_presence": true}],
      "start_not_before": null,
      "complete_not_after": null,
      "risk_flags": [],
      "data_access": ["assessment_receipt"],
      "external_effects": [],
      "stop_conditions": [{"code": "parent_declines", "description": "Stop if the parent declines the review."}],
      "parent_summary": "Review one synthetic performance receipt."
    },
    "proposal_status": "ready_for_parent",
    "canonical_hash": "e33f036cde3b20ac9da9b9cf92f19eff32d214ff1ee412fc40c17b7af3a40500"
  }
}
```

## 14. Complete positive approval-event example

```json
{
  "ucc_parent_approval_event": {
    "contract_version": "ucc.approval_event.v1.0.0",
    "approval_event_id": "appr_01J00000000000000000000018",
    "approval_key": "idem_01J00000000000000000000019",
    "ledger_namespace": "synthetic-test",
    "proposal_id": "prop_01J00000000000000000000010",
    "proposal_revision": 1,
    "proposal_hash": "e33f036cde3b20ac9da9b9cf92f19eff32d214ff1ee412fc40c17b7af3a40500",
    "proposal_type": "task",
    "approval_action": "approve",
    "actor": {"actor_role": "parent", "actor_id": "act_01J0000000000000000000001A"},
    "decision_at": "2026-06-30T01:05:00.000Z",
    "scope": {"proposal_id": "prop_01J00000000000000000000010", "proposal_revision": 1, "learner_id": "lrn_01J00000000000000000000011", "proposal_type": "task", "decision_effect": "approve"},
    "reason_code": "synthetic_parent_approved",
    "reason_note": null,
    "provenance": {"capture_contract_version": "ucc.synthetic_capture.v1.0.0", "capture_channel": "synthetic_test", "source_event_id": "synthetic-source-1", "source_payload_sha256": "3333333333333333333333333333333333333333333333333333333333333333", "captured_at": "2026-06-30T01:05:00.000Z", "authority_configuration_sha256": "4444444444444444444444444444444444444444444444444444444444444444"},
    "canonical_hash": "3e83f9c6de45e98a31e6cc5b7b16f2e0d23394adc1e9ab70062fe5f913685b3c"
  }
}
```

## 15. Negative examples for T4.4

Each mutation is applied independently to the positive examples and materialized as a complete document before evaluation.

| Fixture ID | Mutation | Primary issue |
|---|---|---|
| `proposal-missing-expected-evidence` | remove proposal `expected_evidence` | `PROPOSAL_SCHEMA_INVALID` |
| `proposal-empty-evidence-no-rationale` | set evidence `[]` while rationale remains null | `PROPOSAL_EMPTY_EVIDENCE_RATIONALE_REQUIRED` |
| `proposal-empty-evidence-mastery-state` | set evidence `[]`, add rationale, set requested scope `mastery_state` | `PROPOSAL_EMPTY_EVIDENCE_SCOPE_INVALID` |
| `proposal-missing-smc-ref` | remove `smc_ref` from learner-specific task | `PROPOSAL_SMC_REF_INVALID` |
| `proposal-smc-missing-hash` | remove `smc_ref.canonical_hash` | `PROPOSAL_SMC_REF_INVALID` |
| `approval-ai-actor` | set actor role `ai` | `APPROVAL_ACTOR_UNAUTHORIZED` |
| `approval-system-actor` | set actor role `system` | `APPROVAL_ACTOR_UNAUTHORIZED` |
| `approval-key-changed-payload` | replay same key with changed action/reason/provenance | `IDEMPOTENCY_CONFLICT` |
| `approval-key-r1-to-r2` | replay same key against revision 2/new proposal hash | `IDEMPOTENCY_CONFLICT` |
| `proposal-unknown-field` | add proposal member outside `extensions` | `PROPOSAL_UNKNOWN_FIELD` |
| `proposal-authorship-conflated` | add `authorship.approval_actor` | `PROPOSAL_AUTHORSHIP_CONFLATED` |
| `approval-scope-mismatch` | scope revision/action differs from event | `APPROVAL_SCOPE_MISMATCH` |

## 16. Acceptance criteria

1. Proposal, human decision, derived status, and execution state remain distinct.
2. Evidence, SMC, authorship, empty rationale, payload, and revision fields have exact closed shapes.
3. AI/system authorship never grants approval authority.
4. Approval binds exact ID, revision, proposal hash/type, action, actor, time, scope, and provenance.
5. Identical replay succeeds once; changed payload and R1-to-R2 key reuse conflict.
6. Empty evidence never supports mastery-state approval.
7. Unknown fields fail except namespaced inert extensions.
8. No live message is direct authority and no model participates in decision state.
9. Stable inputs and injected clocks/IDs produce byte-identical canonical results.
