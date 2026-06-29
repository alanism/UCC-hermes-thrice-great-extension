# Contract Version Policy

## Version form

Every durable UCC contract carries a namespaced version such as `ucc.assessment_receipt.v2`. The JSON Schema `$id` is an absolute, stable identifier selected during Phase 3; relative filename references are forbidden in released contracts.

## Change classes

- Patch: descriptions or validator bug fix that does not change accepted documents.
- Minor: backward-compatible optional fields or enum additions with defined unknown handling.
- Major: required-field, semantic, enum-removal, type, identity, or interpretation changes.

Released schemas are immutable. A major change creates a new schema and an explicit migration/adapter. A registry records filename, `$id`, version, status, semantic validator, and fixture sets.

## Required contract backlog

| Planned file | Purpose |
|---|---|
| `schemas/smc.schema.json` | Versioned normalized School Model Canvas. |
| `schemas/assessment_receipt.schema.json` | Durable session/event evidence with `receipt_id`. |
| `schemas/receipt_pairing.schema.json` | `paired_run_id`, form identity, comparison policy, and pair result. |
| `schemas/approval_event.schema.json` | Append-only parent decision authority. |
| `schemas/ledger_entry.schema.json` | Durable append-only evidence/decision record. |
| `schemas/parent_brief.schema.json` | Structured parent-facing output. |
| Revised generator brief | Source IDs and validated pairing provenance. |
| Revised proposal/task card | Proposal revision and activation state separate from approval evidence. |

## Semantic validation

Schema-valid does not mean usable. Semantic validators must check timestamp order, identifier uniqueness, summary/event totals, mode/timer consistency, completion/integrity rules, pairing comparability, proposal revision, approval actor/action, ledger linkage, and idempotency.

Approval `idempotency_key` values are globally unique within one ledger namespace. The first accepted event binds the key to the canonical tuple `(proposal_id, proposal_revision, actor_type, actor_id, action, provenance)`. An identical replay is idempotent success; reuse with any changed tuple member is `IDEMPOTENCY_CONFLICT`. Proposal revision R1 authority cannot transfer to R2.

## Compatibility

Readers must reject unsupported major versions with an actionable issue code. They may accept newer minor versions only when the registry declares compatibility. No reader silently coerces an unknown contract.
