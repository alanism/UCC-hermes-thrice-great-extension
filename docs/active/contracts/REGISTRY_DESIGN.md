# Contract Registry Design

Status: C3.7 SPECIFICATION LOCKED; IMPLEMENTATION BACKLOG

## Registry artifact

The future generated registry is canonical local JSON, validated offline and included in the allowlisted staging payload only when required by the plugin. It contains no network URL resolution and no private data.

Registry contract identity: `ucc.contract_registry.v1.0.0`

Registry `$id`: `urn:ucc:contract:contract-registry:1.0.0`

## Registry record

Each exact contract release record contains:

- `contract_name`;
- `wire_version`;
- `major`, `minor`, `patch` integers;
- schema `$id` URN;
- staged relative schema path;
- schema SHA-256;
- specification path and SHA-256;
- semantic validator entry point and source SHA-256;
- canonicalization ID;
- semantic projection ID/hash, if display fields are excluded;
- stable issue-code namespace;
- positive, negative, compatibility, and mutation fixture-set paths/hashes;
- compatible reader/writer version ranges as explicit exact lists/rules;
- lifecycle status: `planned`, `experimental`, `locked`, `deprecated`, or `retired`;
- replacement wire version when deprecated;
- migration adapter IDs;
- release approval event/receipt reference.

Duplicate name+wire-version, duplicate `$id`, duplicate staged path, missing hash, relative `$id/$ref`, or path escape invalidates the registry.

## Resolution

1. Read document `contract_version`.
2. Find exactly one registry record by wire version.
3. Require supported/allowed lifecycle status.
4. Resolve schema only from the registry's contained local staged path.
5. Verify schema bytes against registry hash before use.
6. Resolve every `$ref` URN through the same immutable registry snapshot.
7. Verify semantic validator and projection hashes.
8. Run shape then semantic validation.

Unknown records and hashes fail closed. No filesystem search, filename guess, package import scan, or network fetch is a resolution strategy.

## Locked specification registry

| Contract family | Locked wire version | Specification | Schema state | Semantic validator state |
|---|---|---|---|---|
| SMC | `ucc.smc.v1.0.0` | `SMC_CONTRACT.md` | planned U8.1 | planned after RED |
| Assessment receipt | `ucc.assessment_receipt.v2.0.0` | `RECEIPT_CONTRACT.md` | planned U8.1 | planned U8.2 |
| Receipt pairing | `ucc.receipt_pairing.v1.0.0` | `PAIRING_CONTRACT.md` | planned U8.1 | planned U8.3 |
| Task proposal | `ucc.task_proposal.v1.0.0` | `APPROVAL_CONTRACT.md` | planned U8.1 | planned U8.4/U8.5 |
| Approval event | `ucc.approval_event.v1.0.0` | `APPROVAL_CONTRACT.md` | planned U8.1 | planned U8.5 |
| Approval transition | `ucc.approval_transition.v1.0.0` | `APPROVAL_CONTRACT.md` | planned U8.1 | planned U8.5 |
| Parent brief | `ucc.parent_brief.v1.0.0` | `BRIEF_LEDGER_CONTRACT.md` | planned U8.1 | planned U8.4 |
| Ledger entry | `ucc.ledger_entry.v1.0.0` | `BRIEF_LEDGER_CONTRACT.md` | planned U8.1 | planned U8.6 |
| Ledger file | `ucc.ledger_file.v1.0.0` | `BRIEF_LEDGER_CONTRACT.md` | planned U8.1 | planned U8.6 |

“Locked” here freezes field semantics for RED test authoring. It does not falsely claim that schemas or validators already exist.

## Migration registry

Initial planned adapters:

| Adapter ID | Source | Target | Loss policy |
|---|---|---|---|
| `adapt.smc_markdown.v1` | current SMC Markdown template | `ucc.smc.v1.0.0` | Placeholders -> null; unknown/duplicate fields block. |
| `adapt.assessment_receipt_v1.v2` | `ucc.receipt.v1` family | `ucc.assessment_receipt.v2.0.0` | External form identity required; no invented thinking/mastery evidence. |
| `adapt.generic_receipt.v1` | unversioned `receipt.schema.json` | typed evidence/ledger reference | Insufficient identity blocks durable conversion unless supplied by trusted migration context. |
| `adapt.task_card.v1` | unversioned Hermes task card | `ucc.task_proposal.v1.0.0` | Always draft/awaiting decision; status never approval. |

Every adapter is deterministic, idempotent by source hash+adapter version, and produces a migration receipt. No adapter writes runtime state directly.

## Issue codes

- `REGISTRY_SCHEMA_INVALID`
- `REGISTRY_DUPLICATE_VERSION`
- `REGISTRY_DUPLICATE_ID`
- `REGISTRY_PATH_INVALID`
- `REGISTRY_HASH_MISMATCH`
- `REGISTRY_REF_UNRESOLVED`
- `REGISTRY_VERSION_UNSUPPORTED`
- `REGISTRY_LIFECYCLE_UNUSABLE`
- `REGISTRY_VALIDATOR_MISMATCH`
- `REGISTRY_FIXTURE_HASH_MISMATCH`
- `MIGRATION_ADAPTER_UNAVAILABLE`
- `MIGRATION_REQUIRED_TRUTH_MISSING`
- `MIGRATION_LOSS_UNDECLARED`
- `MIGRATION_OUTPUT_INVALID`

Issues contain contract IDs, versions, hashes, and contained relative paths only.

## RED readiness

T4.1 must prove missing registry/schemas fail for the expected reason, then cover duplicate IDs/versions, relative refs, hash mutation, path escape, unsupported versions, and missing validator/fixture hashes. Tests cannot be authored until R4.5 passes.
