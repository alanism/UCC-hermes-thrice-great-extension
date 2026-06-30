# Contract Version Policy

Status: C3.7 PRODUCTION CONTRACT LOCK

## Wire version and schema identity

Every durable document carries exact semantic version form:

`ucc.<contract_name>.v<major>.<minor>.<patch>`

Example: `ucc.assessment_receipt.v2.0.0`.

Every released JSON Schema uses the absolute, non-network URN:

`urn:ucc:contract:<contract-name>:<major>.<minor>.<patch>`

Example: `urn:ucc:contract:assessment-receipt:2.0.0`.

Released `$ref` values use registered URNs only. Relative filename references and remote resolution are forbidden in the production distribution. The local registry resolves URNs to allowlisted staged schema files.

## Registry wire authority

C3.7A locks the exact registry JSON envelope, closed nested objects, compatibility rules, lifecycle resolution, fixture manifests, approval references, migrations, and three-layer hashing in `docs/active/contracts/REGISTRY_DESIGN.md`. That wire contract is normative wherever this policy previously referred generically to a “registry record.”

Registry lifecycle values are exactly `draft`, `locked`, `active`, `deprecated`, and `retired`. Normal runtime resolution accepts only `active`; `locked` is accepted only by an explicit test/contract-lock request. No SemVer range, prose compatibility rule, unknown field, or implicit “latest” behavior is permitted.

## Common scalar and reference conventions

- Timestamps are exact RFC 3339 UTC strings with millisecond precision: `YYYY-MM-DDTHH:MM:SS.sssZ`. Offsets, missing milliseconds, and leap seconds are rejected.
- Prefixed IDs use an uppercase 26-character Crockford Base32 ULID after the documented lowercase prefix. Ambiguous characters `I`, `L`, `O`, and `U` are forbidden.
- Durable learner IDs use `lrn_<ULID>`; actor IDs use `act_<ULID>`.
- Fields named `*_sha256` contain exactly 64 lowercase hexadecimal characters with no `sha256:` prefix.
- Nullable means explicit JSON null. Missing, null, empty string, and empty array remain distinct according to each contract.
- All issue objects contain `code`, RFC 6901 JSON Pointer `path`, and optional safe scalar/list metadata. Raw private content is forbidden.
- A typed record reference contains `contract_version`, `record_id`, `canonical_payload_sha256`, `quality_or_status`, and `resolution_state` (`resolved`, `missing`, or `hash_mismatch`). Absolute paths are forbidden.

Contract specifications inherit these conventions unless they explicitly narrow them. A conflicting local convention is a contract defect, not an override.

## Change classes

- Patch: descriptions, annotations, or validator defect correction that does not change the accepted/rejected document set or semantic output.
- Minor: backward-compatible optional field/enum addition with explicit unknown behavior and no changed meaning for existing documents.
- Major: required-field, type, identity, enum removal, canonicalization, authority, denominator, status, interpretation, or compatibility change.

Any change that alters stable issue codes or semantic output for an existing valid payload is major unless the prior behavior was provably a validator defect and the migration/compatibility review explicitly approves a patch/minor correction.

Released schema and semantic-validator artifacts are immutable. Every release gets a new registry record, URN, content hash, fixture-set hash, and validator hash. Source convenience filenames may point to the current development version but are not distributable identity.

## Compatibility

- Readers accept exact registered versions by default.
- A reader may accept a newer patch/minor only when the registry record explicitly names that reader version as compatible and the fixture compatibility suite passes.
- Unsupported major, unknown minor, unknown contract, unknown canonicalization, or missing registry record fails with a stable actionable issue.
- No reader silently removes fields, fills missing truth, coerces unknown enums, or downgrades quality.
- Writers emit one exact registered version and never negotiate dynamically through a network service.

## Canonical JSON

Canonicalization ID: `rfc8785-jcs-v1`.

- Input must satisfy I-JSON constraints; duplicate object keys, NaN, Infinity, invalid Unicode, and out-of-range interoperable numbers are rejected.
- Contract decimals are computed using decimal arithmetic and serialized according to RFC 8785 after contract rounding.
- Strings are valid Unicode; fields requiring NFC enforce it semantically before canonicalization.
- Canonical hashes use SHA-256 over canonical UTF-8 bytes.
- Display-only fields explicitly excluded by a contract are removed before semantic hashing through a registered projection; exclusion is never ad hoc.

A future canonicalization change is a contract major change.

## Schema and semantic validation

Shape validity is necessary but not sufficient. Registry records declare a schema and semantic validator. Validators return deterministic issues sorted by contract-defined path/code/ID order.

Semantic validation covers at minimum:

- identifier uniqueness and binding;
- timestamp/event order;
- receipt totals, mode/timer and quality derivation;
- pairing policy, form/skill comparability and evidence floors;
- SMC revision/amendment authority;
- proposal revision/payload hash;
- approval actor/action/provenance/idempotency;
- brief source/claim linkage;
- ledger sequence/hash/linkage/idempotency/retention.

Approval idempotency remains globally unique within one ledger namespace. Exact canonical replay is success without duplicate append; any changed semantic field or cross-revision reuse is `IDEMPOTENCY_CONFLICT`.

## Production schema backlog

Schema implementation occurs only after Phase 4 RED tasks and U8.1 authorization.

| Planned source file | Initial wire version | Initial `$id` |
|---|---|---|
| `schemas/smc.schema.json` | `ucc.smc.v1.0.0` | `urn:ucc:contract:smc:1.0.0` |
| `schemas/assessment_receipt.schema.json` | `ucc.assessment_receipt.v2.0.0` | `urn:ucc:contract:assessment-receipt:2.0.0` |
| `schemas/receipt_pairing.schema.json` | `ucc.receipt_pairing.v1.0.0` | `urn:ucc:contract:receipt-pairing:1.0.0` |
| `schemas/task_proposal.schema.json` | `ucc.task_proposal.v1.0.0` | `urn:ucc:contract:task-proposal:1.0.0` |
| `schemas/approval_event.schema.json` | `ucc.approval_event.v1.0.0` | `urn:ucc:contract:approval-event:1.0.0` |
| `schemas/approval_transition.schema.json` | `ucc.approval_transition.v1.0.0` | `urn:ucc:contract:approval-transition:1.0.0` |
| `schemas/parent_brief.schema.json` | `ucc.parent_brief.v1.0.0` | `urn:ucc:contract:parent-brief:1.0.0` |
| `schemas/ledger_entry.schema.json` | `ucc.ledger_entry.v1.0.0` | `urn:ucc:contract:ledger-entry:1.0.0` |
| `schemas/ledger_file.schema.json` | `ucc.ledger_file.v1.0.0` | `urn:ucc:contract:ledger-file:1.0.0` |

Revision backlogs:

- generator brief v2 consumes only validated receipt/pair IDs and deterministic facts;
- legacy task card migrates only to draft/awaiting-decision proposal;
- weekly plan/campaign schemas migrate after approval/ledger implementation;
- benchmark alignment receives a stable version when campaign contracts are claimed.

## Migration rule

Every migration is an explicit registered adapter with source/target versions, adapter version/hash, deterministic issue set, fixture set, and loss classification. The result records source bytes SHA-256, target semantic SHA-256, adapter identity, warnings, and fields not representable.

Adapters never fabricate form identity, student-thinking evidence, parent approval, mastery, provenance, or missing SMC values. When required truth is unavailable, output is null/degraded/void/draft as defined by the target contract or migration fails.

## Human lock authority

The human owner explicitly authorized progression through Phase 3 contract lock on 2026-06-30 under the production doctrine in the C3 build prompt. That authorization applies to the contract specifications and registry/migration design, not runtime implementation, live integrations, learner data, or the unresolved optional-adapter scope decision in C3.8.
