# C3.1 Contract Inventory

Status: COMPLETE INVENTORY; dispositions feed C3.2–C3.7

## Existing schema disposition

| Existing artifact | Identity / consumers | Finding | Disposition |
|---|---|---|---|
| `assessment-event.schema.json` | `$id: ucc.assessment_event.v1`; referenced by canonical receipt through registry-style ID | Useful item telemetry, but no assessment-form identity, failure stage, or per-event timestamp; `timer_tier` duplicates session mode. | REVISE and absorb as `$defs.event` in `assessment_receipt` v2. Preserve adapter mapping. |
| `canonical-receipt.schema.json` | `$id: ucc.receipt.v1`; intended durable assessment receipt | Missing `receipt_id`, `paired_run_id`, and `assessment_form_id`; requires display name; summary semantics are under-specified. | SUPERSEDE with `assessment_receipt.schema.json` v2; retain read adapter only. |
| `receipt-integrity.schema.json` | `$id: ucc.receipt_integrity.v1`; referenced by canonical receipt | Five useful quality states, but issue-code vocabulary and status interaction are undefined. | REVISE as receipt v2 integrity `$defs`; stable issue codes defined by C3.3. |
| `assessment-to-generator-brief.schema.json` | `$id: ucc.assessment_to_generator_brief.v1`; no file consumer found | Uses `receipt_id` that v1 receipt does not provide; carries display name and free-form modeled interpretation. | REVISE after pairing contract; source only validated receipt/pair IDs and deterministic diagnosis facts. |
| `receipt.schema.json` | no `$id`; consumed by weekly plan | Generic evidence record collides semantically with assessment receipt and lacks durable identity/provenance. | DEPRECATE. Weekly plan migrates to typed evidence references or ledger entry IDs. |
| `hermes_task_card.schema.json` | no `$id`; cited by macro/meso/micro doc | Status conflates workflow with authority; owner includes AI/Hermes; no proposal revision or approval link. | SUPERSEDE with versioned proposal/task-card contract separated from approval events. |
| `learner_overlay.schema.json` | no `$id`; no direct file consumer found | Requires learner name and embeds mutable history; incompatible with pseudonymous durable keys. | DEFER outside the Phase 3 core; future adapter must use pseudonymous learner ID and ledger refs. |
| `learning_campaign.schema.json` | no `$id`; consumed by weekly plan | Useful campaign hypothesis fields; `status: active` has no approval authority and evidence/SMC links are strings. | DEFER and later revise to reference locked proposal, SMC revision, and ledger evidence IDs. |
| `weekly_campaign_plan.schema.json` | no `$id`; docs and assessment-review export reference it | Requires learner name and consumes deprecated generic receipts; schedule tasks are untyped strings. | DEFER and later revise after proposal/approval/ledger lock. |
| `benchmark_alignment.schema.json` | no `$id`; consumed by learning campaign | Correctly treats standards as reference terrain but uses camelCase and free strings. | INCLUDE AS REFERENCE CANDIDATE; version in a later campaign-contract task. |

All ten JSON files parse successfully and use JSON Schema draft-07. Five lack `$id`. Naming mixes camelCase and snake_case. Relative filename `$ref` values and non-URI identifiers require a registry and cannot be release authority as-is.

## Missing production contracts

| Required contract | Current evidence | Phase 3 owner |
|---|---|---|
| Normalized SMC | Markdown template; DOCX intent; SMC interpreter skill | C3.2 |
| Assessment receipt v2 | canonical receipt/event/integrity v1; live reviewer skill | C3.3 |
| Receipt pairing | prose paired-session rules only | C3.4 |
| Task proposal | legacy task card and campaign schema | C3.5 |
| Approval event and transition result | doctrine only; no schema | C3.5 |
| Parent brief | live parent-progress skill; no durable structure | C3.6 |
| Ledger entry/envelope | mastery-ledger skill and privacy doctrine; no schema | C3.6 |
| Contract registry/migration records | policy prose only | C3.7 |

## Identifier audit

| Entity | Existing state | Required decision |
|---|---|---|
| SMC | filename/date or `schoolModelCanvasId`; no revision identity | `smc_id` plus monotonically increasing `revision`; amendment authority and source hash. |
| Receipt | v1 has session ID but no receipt ID | `receipt_id`, `session_id`, optional `paired_run_id`, required `assessment_form_id`. |
| Event | free string event ID | Receipt-scoped uniqueness and ordered item index. |
| Pair | absent | `paired_run_id` and two explicit receipt IDs. |
| Proposal | card/campaign IDs only | `proposal_id` plus positive integer revision and canonical payload hash. |
| Approval | absent | `approval_event_id` plus ledger-namespace-global `idempotency_key`. |
| Brief | brief ID exists only on generator brief | Dedicated `parent_brief_id`, source record IDs, contract version. |
| Ledger | absent | `ledger_entry_id`, namespace, subject ID, event time, recorded time, payload hash, previous-entry hash where applicable. |
| Learner | mixed `student_id`, `learnerId`, names | Canonical pseudonymous `learner_id`; display name optional presentation-only. |

## Reference and consumer contradictions

1. Generator brief requires `receipt_id`, but canonical receipt v1 has none.
2. Canonical receipt uses registry-style `$ref` IDs while weekly/campaign schemas use relative filenames; no registry resolves both models.
3. Generic `receipt.schema.json` and canonical assessment receipt use the same word for different evidence strength.
4. Receipt `assessment.mode` and event `timer_tier` can contradict.
5. Receipt summary totals, events, completion status, score status, and integrity status have no cross-field enforcement.
6. Legacy task/campaign status can become `active` without a separate approval event.
7. Required learner/display names in receipt, weekly plan, overlay, and generator brief conflict with privacy authority.
8. CALM/PRESSURE prose assumes comparable forms and skills but has no form ID, sample floor, timeout denominator, or degradation rule.
9. Parent-progress skill includes internal, public-blog, and prospective-sales shapes in one source; only the internal evidence brief belongs in the core durable contract.
10. Production assessment-review skill infers mode from duration when absent. The locked receipt must require explicit mode; inference belongs only in a declared legacy adapter.
11. Production workflow text still names ghostwriting risk. Public/default contracts must use AI role clarity, process evidence, student thinking evidence, mastery evidence, valid evidence claim, and false mastery risk.
12. Legacy docs claim live Discord/cloud operations. Those are optional future adapters, not core contracts.

## Production doctrine applied

- UCC does not police AI use and does not detect cheating, ghostwriting, or AI-written text.
- AI assistance is allowed when its role is explicit.
- A useful AI-assisted artifact is not automatically valid mastery evidence.
- Mastery claims require recorded student thinking/process evidence under declared conditions.
- Missing evidence produces `insufficient_evidence` or false-mastery-risk findings, never misconduct labels.
- `ghostwriting_integrity_gate` is excluded from public/default release unless separately re-approved.

## Migration consumers

| Consumer | Impact |
|---|---|
| Assessment Lab exporters | Emit receipt v2 directly or pass through a versioned v1 adapter. |
| Assessment reviewer skill | Stop duration-based mode inference for v2; consume stable issue codes and pair result. |
| Generator brief | Consume validated IDs and deterministic facts; never raw unvalidated receipts. |
| Weekly plan/campaign schemas | Replace generic receipt objects and status-as-approval with references. |
| Parent brief renderer | Consume structured brief data only; public/testimonial prose is a separate presentation concern. |
| Mastery ledger | Append validated evidence/decision records with pseudonymous keys. |
| Hermes plugin | Resolve contracts through registry; reject unsupported major versions. |
| Native release skills | Reference locked contract names and issue codes after deliberate genericization. |
| Synthetic fixtures/RED harness | Cover every semantic contradiction above without learner data. |

## Phase 3 lock criteria

C1 cannot pass until C3.2–C3.6 define every field and semantic rule, C3.7 freezes registry/migration behavior with explicit human approval, and C3.8 records the separate optional-adapter scope decision. No runtime implementation is implied by this inventory.
