# Parent Brief and Atomic Ledger Contract

Status: SPECIFICATION LOCKED BY C3.7; LEDGER WIRE AMENDED BY C3.6A; SCHEMA/IMPLEMENTATION TEST-GATED

Contracts:

- `ucc.parent_brief.v1.0.0`
- `ucc.ledger_entry.v1.0.0`
- `ucc.ledger_file.v1.0.0`

## 1. Parent brief contract retained

The parent brief is deterministic and evidence-labeled. It separates measured facts, calculations, rule-based interpretations, limitations, and proposed actions. It never turns a proposal into approval and never treats model output as fact, approval, or ledger state.

The brief has injected `parent_brief_id` (`pbrf_<ULID>`), pseudonymous `learner_id`, `brief_revision` (positive integer), UTC period/creation timestamps, exact SMC and source references, structured evidence-labeled sections, limitations, immutable render profile, and a canonical semantic hash. Claims are labeled `measured`, `calculated`, `modeled`, `forecast`, or `noted`; mastery language requires accepted ledger authority under a locked policy. The original C3.6 source/quality/AI-role/mastery/neutral-language rules remain binding.

## 2. Ledger role and closed roots

The ledger is a private local append-only logical history. Normal writes never edit or delete a semantic entry. Privacy deletion is a separately authorized two-event operation followed by atomic compaction.

A ledger document is a JSON object with exactly one member, `ucc_local_ledger`. Each element of `entries` is an object with exactly one member, `ucc_ledger_entry`. Unknown members at either wrapper or inner-object level are rejected unless the inner object explicitly permits `extensions`.

## 3. Exact ledger-file envelope

`ucc_local_ledger` contains exactly these required fields and optional `extensions`:

| Field | Type | Rule |
|---|---|---|
| `ledger_schema_version` | string | Exactly `ucc.ledger_file.v1.0.0`. |
| `ledger_id` | string | Injected `ledg_<ULID>`; immutable. |
| `ledger_namespace` | string | Non-empty configured local namespace; immutable. |
| `created_at` | string | Injected UTC RFC 3339 timestamp with millisecond precision. |
| `retention_policy_ref` | object | Exact shape below. |
| `entry_count` | integer | Non-negative; equals present `entries` length. |
| `head_sequence` | integer | Zero when empty; otherwise greatest logical sequence. |
| `head_entry_hash` | string/null | Null when empty; otherwise canonical hash of greatest-sequence entry. |
| `entries` | array | Entries ordered by strictly increasing `sequence`. |
| `ledger_hash` | string | Lowercase SHA-256 of the ledger projection in section 9. |
| `extensions` | object | Optional namespaced, resolution-inert values. |

`retention_policy_ref` contains exactly `policy_id` (`retp_<ULID>`), `policy_version` (non-empty contract version), and `canonical_hash` (64 lowercase hexadecimal characters).

Before compaction, sequences are contiguous from 1. After authorized compaction, gaps are permitted only when every omitted entry ID/hash is named by a retained tombstone. `head_sequence` is therefore not necessarily `entry_count` after compaction.

## 4. Exact ledger-entry envelope

`ucc_ledger_entry` contains exactly these required fields and optional `extensions`:

| Field | Type | Rule |
|---|---|---|
| `contract_version` | string | Exactly `ucc.ledger_entry.v1.0.0`. |
| `ledger_entry_id` | string | Injected namespace-global `ldgr_<ULID>`; not payload-derived. |
| `idempotency_key` | string | Injected namespace-global `idem_<ULID>`; immutable binding key. |
| `entry_type` | string | Exact enum in section 5. |
| `sequence` | integer | Positive; prior logical head + 1. |
| `occurred_at` | string | Domain-event UTC timestamp, millisecond precision. |
| `recorded_at` | string | Injected commit UTC timestamp, millisecond precision. |
| `previous_entry_hash` | string/null | Null only for sequence 1; otherwise prior logical entry canonical hash. |
| `payload_contract` | object | Exact shape in section 6. |
| `payload` | object | Embedded canonical semantic payload; never null. |
| `source_refs` | array | Sorted unique exact references from section 6. |
| `approval_ref` | object/null | Exact shape in section 7. |
| `parent_brief_ref` | object/null | Exact shape in section 7. |
| `canonical_hash` | string | Lowercase SHA-256 of the entry projection in section 9. |
| `extensions` | object | Optional namespaced, resolution-inert values. |

`recorded_at >= occurred_at`. IDs, key, sequence, and clocks are injected. File paths, display names, secrets, learner answers, and unvalidated model output are forbidden in entry control fields and logs.

## 5. Entry types and reference requirements

Allowed `entry_type` values are exactly:

- `proposal_recorded`;
- `approval_recorded`;
- `learner_state_transition`;
- `parent_brief_recorded`;
- `retention_policy_recorded`;
- `deletion_requested`;
- `tombstone_recorded`.

`approval_recorded` and `learner_state_transition` require non-null `approval_ref`. `parent_brief_recorded` requires non-null `parent_brief_ref`. Other types use null unless their source contract explicitly requires the reference. `learner_state_transition` cannot assert a stronger state than the referenced approval permits. No model call participates in any entry fact, approval, or transition.

## 6. Payload contract and source references

`payload_contract` contains exactly:

| Field | Type | Rule |
|---|---|---|
| `contract_family` | string | Stable registered family ID. |
| `contract_version` | string | Exact payload wire version. |
| `schema_ref` | string | Contained normalized relative path; no drive, UNC, leading slash, `.` or `..`. |
| `canonical_hash` | string | SHA-256 of the JCS payload value. |

Each `source_refs` item contains exactly:

| Field | Type |
|---|---|
| `source_ref_id` | `sref_<ULID>` string |
| `source_type` | exact enum below |
| `source_id` | non-empty stable record ID |
| `source_contract_family` | non-empty stable family ID |
| `source_contract_version` | non-empty exact version |
| `source_hash` | 64 lowercase hexadecimal characters |
| `relationship` | non-empty stable relationship code |

Allowed source types are exactly `smc`, `assessment_receipt`, `receipt_pairing`, `proposal`, `approval_event`, `parent_brief`, `ledger_entry`, and `synthetic_fixture`. References sort by `(source_type, source_id, relationship, source_ref_id)` and duplicates are invalid.

## 7. Approval and parent-brief references

`approval_ref` is null or contains exactly:

- `approval_event_id`: `appr_<ULID>`;
- `proposal_id`: `prop_<ULID>`;
- `proposal_revision`: positive integer;
- `proposal_hash`: 64 lowercase hexadecimal characters;
- `approval_action`: `approve`, `reject`, or `request_revision`;
- `approval_actor_role`: `parent`, `guardian`, or `authorized_adult`;
- `approval_scope`: object containing exactly `proposal_id`, `proposal_revision`, `learner_id`, `proposal_type`, and `decision_effect` as locked by C3.5A.

All duplicate ID/revision/action fields must agree with the accepted approval event.

`parent_brief_ref` is null or contains exactly:

- `parent_brief_id`: `pbrf_<ULID>`;
- `brief_revision`: positive integer;
- `brief_hash`: 64 lowercase hexadecimal characters;
- `rendered_from_proposal_id`: `prop_<ULID>` or null;
- `rendered_from_proposal_revision`: positive integer or null.

The two rendered-from fields are both null or both non-null. The brief hash is its locked semantic payload hash.

## 8. Required, optional, and unknown fields

All fields listed as required remain present even when their value is null. The only optional member is `extensions`. An `extensions` object is closed to keys matching `^[a-z0-9]+(?:[.-][a-z0-9]+)+$`; values must be JSON values. Extensions are recursively removed before hashing and cannot change validation, resolution, ordering, idempotency, transition, retention, or deletion. Any other unknown field is invalid.

## 9. Canonical JSON and exact hash projections

Canonical JSON is RFC 8785/JCS encoded as UTF-8. Strings are valid Unicode, timestamps use UTC `Z` with millisecond precision, NaN/Infinity are forbidden, and no transport delimiter or BOM is hashed.

- `payload_contract.canonical_hash` is SHA-256 of JCS `payload`.
- Entry `canonical_hash` is SHA-256 of the JCS `ucc_ledger_entry` value after recursively removing every `extensions` member and removing top-level `canonical_hash`. It therefore includes IDs, key, type, sequence, both clocks, previous hash, payload contract, payload, source refs, approval ref, and parent-brief ref. It excludes file path, lock data, temp-file name, OS metadata, and transport framing because none are wire members.
- `ledger_hash` is SHA-256 of JCS over exactly: `ledger_schema_version`, `ledger_id`, `ledger_namespace`, `created_at`, `retention_policy_ref`, `entry_count`, `head_sequence`, `head_entry_hash`, and `ordered_entry_hashes` (the present entries' canonical hashes in sequence order). It excludes `entries`, `ledger_hash`, and `extensions` to avoid duplicate payload hashing.
- `previous_entry_hash` is the preceding logical entry's `canonical_hash`, or null for sequence 1. After compaction a missing predecessor is valid only if a retained tombstone proves its ID/hash.

## 10. Identity, order, replay, and conflicts

Within a namespace, `ledger_id`, `ledger_entry_id`, and `idempotency_key` are unique. The first accepted idempotency key permanently binds the complete entry canonical projection except storage-assigned `sequence`, `recorded_at`, `previous_entry_hash`, and `canonical_hash`; those four fields are the recorded result returned on replay.

- Identical replay returns the original entry with `replayed: true` and appends nothing.
- Same key with any changed bound field returns `LEDGER_IDEMPOTENCY_CONFLICT`.
- Reusing an approval key is not a substitute for a ledger idempotency key; approval validation occurs first.
- New writes use `sequence = head_sequence + 1`, `previous_entry_hash = head_entry_hash`, and strictly increasing injected `recorded_at`.
- Same entry ID under a new key is `LEDGER_ENTRY_ID_CONFLICT`.

## 11. Atomic commit and fault outcomes

The writer must resolve a contained non-reparse private root, take an exclusive namespace lock, read and fully validate the current ledger, construct/validate the complete next bytes in memory, and create a unique temp file in the ledger's directory. It writes and flushes the temp file, rechecks lock ownership and the prior ledger hash, performs one same-volume atomic replace, performs the platform durability flush where supported, then reopens and verifies bytes/hash/head before reporting success.

| Injection point | Required result |
|---|---|
| Before temp create | Prior ledger byte-identical; `LEDGER_TEMP_CREATE_FAILED`. |
| During temp write | Prior ledger byte-identical; partial temp is never commit-eligible; `LEDGER_TEMP_WRITE_FAILED`. |
| Temp flush | Prior ledger byte-identical; `LEDGER_TEMP_FLUSH_FAILED`. |
| Lock lost / prior hash changed | No replace; `LEDGER_LOCK_LOST` or `LEDGER_CONCURRENT_MODIFICATION`. |
| Atomic replace | Prior ledger remains valid; no success; `LEDGER_REPLACE_FAILED`. |
| Crash after replace | Recovery observes complete old or complete new bytes, never partial; outcome remains unknown until readback. |
| Readback/hash mismatch | No success; quarantine further writes; `LEDGER_COMMIT_UNKNOWN`. |
| Directory flush unsupported | Verified commit may return `LEDGER_DURABILITY_WARNING`; it is not a false rollback. |

Temps are never auto-promoted over a valid configured ledger. If the configured ledger is invalid and a valid temp exists, recovery requires an explicit human recovery operation.

## 12. Retention, deletion, and tombstones

No implicit retention duration exists. A `retention_policy_recorded` payload contains exactly `retention_policy_id`, `policy_version`, `recorded_by_actor_role`, `effective_at`, `entry_type_rules`, and `hold_codes`. Each rule contains exactly `entry_type` and `retention_days` (positive integer or null). Holds prevent deletion.

A `deletion_requested` payload contains exactly `deletion_request_id`, `target_entry_ids` (non-empty sorted unique ledger-entry IDs), `policy_id`, `reason_code`, `requested_by_actor_role`, `requested_by_actor_id`, `requested_at`, `redaction_scope`, and `request_key`. Authority, scope, policy, holds, targets, and key binding are validated before mutation.

Deletion is exactly:

1. append a validated `deletion_requested` entry;
2. construct a new ledger that omits the targeted entries and appends one `tombstone_recorded` entry;
3. preserve non-target entry IDs, sequences, hashes, and logical predecessor hashes;
4. permit resulting sequence/hash-chain gaps only when the tombstone's retained audit hashes cover them;
5. commit the compacted ledger through the same atomic protocol;
6. return the existing request/tombstone on identical replay, and conflict on changed targets/scope under the same request or ledger key.

No in-place erase, field blanking, or hash rewriting is permitted. Backups/copies are governed separately; deletion is not claimed for an uncontrolled copy.

The `tombstone_recorded` payload contains exactly:

| Field | Type | Rule |
|---|---|---|
| `tombstone_id` | string | Injected `tomb_<ULID>`. |
| `target_entry_id` | string | One `ldgr_<ULID>` target. Multiple targets require one tombstone per target. |
| `reason_code` | string | Stable non-sensitive code. |
| `requested_by_actor_role` | string | `parent`, `guardian`, `authorized_adult`, or configured `data_owner`. |
| `requested_at` | string | Exact deletion-request timestamp. |
| `redaction_scope` | string | `payload_only` or `payload_and_private_refs`. |
| `retained_audit_hashes` | array | Non-empty; exact objects `{target_entry_id, canonical_hash}`, sorted by target ID. |

Tombstones contain no learner ID, answer, evidence body, display name, private path, reason note, or deleted payload.

## 13. Stable ledger issue codes

| Code | Meaning |
|---|---|
| `LEDGER_ROOT_INVALID` | Wrong/multiple top-level envelope members. |
| `LEDGER_SCHEMA_VERSION_UNSUPPORTED` | File or entry version unsupported. |
| `LEDGER_SCHEMA_INVALID` | Required member/type/null rule invalid. |
| `LEDGER_UNKNOWN_FIELD` | Unknown member outside valid extensions. |
| `LEDGER_EXTENSION_INVALID` | Extension namespace/value invalid. |
| `LEDGER_ENTRY_TYPE_INVALID` | Entry type outside exact enum. |
| `LEDGER_COUNT_MISMATCH` | Count differs from present entries. |
| `LEDGER_SEQUENCE_INVALID` | Order, sequence, or uncovered compaction gap invalid. |
| `LEDGER_PREVIOUS_HASH_INVALID` | Previous logical hash missing/mismatched. |
| `LEDGER_PAYLOAD_CONTRACT_INVALID` | Payload contract/ref invalid. |
| `LEDGER_PAYLOAD_HASH_MISMATCH` | Payload canonical hash differs. |
| `LEDGER_SOURCE_REF_INVALID` | Source type/shape/order/hash invalid. |
| `LEDGER_APPROVAL_REF_INVALID` | Required approval reference absent/invalid. |
| `LEDGER_PARENT_BRIEF_REF_INVALID` | Required brief reference absent/invalid. |
| `LEDGER_ENTRY_HASH_MISMATCH` | Entry projection hash differs. |
| `LEDGER_HASH_MISMATCH` | File projection hash differs. |
| `LEDGER_IDEMPOTENCY_CONFLICT` | Existing key binds changed semantics. |
| `LEDGER_ENTRY_ID_CONFLICT` | Entry ID already exists under another key. |
| `LEDGER_PATH_INVALID` | Containment/reparse/same-volume check failed. |
| `LEDGER_LOCK_TIMEOUT` | Exclusive lock unavailable. |
| `LEDGER_LOCK_LOST` | Lock ownership changed. |
| `LEDGER_CONCURRENT_MODIFICATION` | Prior ledger hash changed before replace. |
| `LEDGER_TEMP_CREATE_FAILED` | Same-directory temp creation failed. |
| `LEDGER_TEMP_WRITE_FAILED` | Temp write failed. |
| `LEDGER_TEMP_FLUSH_FAILED` | Temp durable flush failed. |
| `LEDGER_REPLACE_FAILED` | Atomic replace failed. |
| `LEDGER_READBACK_FAILED` | Complete new state could not be reopened. |
| `LEDGER_COMMIT_UNKNOWN` | Replace may have occurred but verification failed. |
| `LEDGER_DURABILITY_WARNING` | Directory flush unsupported after verified replace. |
| `LEDGER_RETENTION_POLICY_MISSING` | Required policy unavailable. |
| `LEDGER_DELETE_AUTHORITY_INVALID` | Deletion actor/scope unauthorized. |
| `LEDGER_DELETE_HOLD_ACTIVE` | Target is protected by a hold. |
| `LEDGER_TOMBSTONE_INVALID` | Tombstone shape/hash/target coverage invalid. |

Issues sort by JSON Pointer path then code then entry ID. Diagnostics never include private payload values or absolute paths.

## 14. Complete positive ledger example

The external synthetic retention-policy artifact intentionally has hash `aaaaaaaa...`; all ledger-owned hashes below recompute exactly under section 9.

```json
{"ucc_local_ledger":{"ledger_schema_version":"ucc.ledger_file.v1.0.0","ledger_id":"ledg_01J00000000000000000000028","ledger_namespace":"synthetic-test","created_at":"2026-06-30T00:59:00.000Z","retention_policy_ref":{"policy_id":"retp_01J00000000000000000000029","policy_version":"ucc.retention_policy.v1.0.0","canonical_hash":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},"entry_count":2,"head_sequence":2,"head_entry_hash":"18c2cb7f376ce2cb224813e32203d27f5c191dd0347c62280a9c64ad19ddf36d","entries":[{"ucc_ledger_entry":{"contract_version":"ucc.ledger_entry.v1.0.0","ledger_entry_id":"ldgr_01J00000000000000000000021","idempotency_key":"idem_01J00000000000000000000022","entry_type":"approval_recorded","sequence":1,"occurred_at":"2026-06-30T01:00:00.000Z","recorded_at":"2026-06-30T01:00:01.000Z","previous_entry_hash":null,"payload_contract":{"contract_family":"proposal_approval","contract_version":"ucc.approval_event.v1.0.0","schema_ref":"schemas/approval-event.v1.schema.json","canonical_hash":"b6c6dbf1f2f43a6856865e9b835b70b08be58deed8081d48def40d9509712a25"},"payload":{"approval_event_id":"appr_01J00000000000000000000018","approval_action":"approve","proposal_id":"prop_01J00000000000000000000010","proposal_revision":1,"proposal_hash":"e33f036cde3b20ac9da9b9cf92f19eff32d214ff1ee412fc40c17b7af3a40500"},"source_refs":[{"source_ref_id":"sref_01J00000000000000000000024","source_type":"approval_event","source_id":"appr_01J00000000000000000000018","source_contract_family":"proposal_approval","source_contract_version":"ucc.approval_event.v1.0.0","source_hash":"3e83f9c6de45e98a31e6cc5b7b16f2e0d23394adc1e9ab70062fe5f913685b3c","relationship":"records"}],"approval_ref":{"approval_event_id":"appr_01J00000000000000000000018","proposal_id":"prop_01J00000000000000000000010","proposal_revision":1,"proposal_hash":"e33f036cde3b20ac9da9b9cf92f19eff32d214ff1ee412fc40c17b7af3a40500","approval_action":"approve","approval_actor_role":"parent","approval_scope":{"proposal_id":"prop_01J00000000000000000000010","proposal_revision":1,"learner_id":"lrn_01J00000000000000000000020","proposal_type":"evidence_review","decision_effect":"approve"}},"parent_brief_ref":null,"canonical_hash":"e2605f3bc21585444d893c984db951b20a30a94b31c5f1731e0bd2ad128eb49a"}},{"ucc_ledger_entry":{"contract_version":"ucc.ledger_entry.v1.0.0","ledger_entry_id":"ldgr_01J00000000000000000000025","idempotency_key":"idem_01J00000000000000000000026","entry_type":"learner_state_transition","sequence":2,"occurred_at":"2026-06-30T01:00:00.000Z","recorded_at":"2026-06-30T01:00:02.000Z","previous_entry_hash":"e2605f3bc21585444d893c984db951b20a30a94b31c5f1731e0bd2ad128eb49a","payload_contract":{"contract_family":"proposal_approval","contract_version":"ucc.learner_state_transition.v1.0.0","schema_ref":"schemas/learner-state-transition.v1.schema.json","canonical_hash":"1595f300e6c7128347e4ccff76f85fb7d0eccbd5ce8b679dfcdb9a51a8bed7d5"},"payload":{"transition_id":"tran_01J00000000000000000000023","learner_id":"lrn_01J00000000000000000000020","prior_state":"candidate","next_state":"approved_performance","effective_at":"2026-06-30T01:00:00.000Z"},"source_refs":[{"source_ref_id":"sref_01J00000000000000000000027","source_type":"ledger_entry","source_id":"ldgr_01J00000000000000000000021","source_contract_family":"parent_brief_ledger","source_contract_version":"ucc.ledger_entry.v1.0.0","source_hash":"e2605f3bc21585444d893c984db951b20a30a94b31c5f1731e0bd2ad128eb49a","relationship":"authorized_by"}],"approval_ref":{"approval_event_id":"appr_01J00000000000000000000018","proposal_id":"prop_01J00000000000000000000010","proposal_revision":1,"proposal_hash":"e33f036cde3b20ac9da9b9cf92f19eff32d214ff1ee412fc40c17b7af3a40500","approval_action":"approve","approval_actor_role":"parent","approval_scope":{"proposal_id":"prop_01J00000000000000000000010","proposal_revision":1,"learner_id":"lrn_01J00000000000000000000020","proposal_type":"evidence_review","decision_effect":"approve"}},"parent_brief_ref":null,"canonical_hash":"18c2cb7f376ce2cb224813e32203d27f5c191dd0347c62280a9c64ad19ddf36d"}}],"ledger_hash":"02b1d4c7573c08cde6694ffd568c363e5346f3976c3786ce8ac41ee87c22e971"}}
```

This is also the complete positive `approval_recorded` and `learner_state_transition` entry example set.

## 15. Complete positive tombstone entry example

This entry follows a valid sequence-3 deletion request whose canonical hash is represented by `bbbb...`. Its payload hash is `9224f1e0...`; its complete entry hash is `1e6861a8...`.

```json
{"ucc_ledger_entry":{"contract_version":"ucc.ledger_entry.v1.0.0","ledger_entry_id":"ldgr_01J00000000000000000000031","idempotency_key":"idem_01J00000000000000000000032","entry_type":"tombstone_recorded","sequence":4,"occurred_at":"2026-06-30T02:00:00.000Z","recorded_at":"2026-06-30T02:00:02.000Z","previous_entry_hash":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","payload_contract":{"contract_family":"parent_brief_ledger","contract_version":"ucc.tombstone.v1.0.0","schema_ref":"schemas/tombstone.v1.schema.json","canonical_hash":"9224f1e06dee784784a3ce8e883138538c33c96d73c8292487f476826e46f72d"},"payload":{"tombstone_id":"tomb_01J00000000000000000000030","target_entry_id":"ldgr_01J00000000000000000000025","reason_code":"owner_deletion_request","requested_by_actor_role":"parent","requested_at":"2026-06-30T02:00:00.000Z","redaction_scope":"payload_and_private_refs","retained_audit_hashes":[{"target_entry_id":"ldgr_01J00000000000000000000025","canonical_hash":"18c2cb7f376ce2cb224813e32203d27f5c191dd0347c62280a9c64ad19ddf36d"}]},"source_refs":[{"source_ref_id":"sref_01J00000000000000000000033","source_type":"ledger_entry","source_id":"ldgr_01J00000000000000000000025","source_contract_family":"parent_brief_ledger","source_contract_version":"ucc.ledger_entry.v1.0.0","source_hash":"18c2cb7f376ce2cb224813e32203d27f5c191dd0347c62280a9c64ad19ddf36d","relationship":"tombstones"}],"approval_ref":null,"parent_brief_ref":null,"canonical_hash":"1e6861a8e677e21a4d1e4f14e9cbfe9b84b04fded9c7d815f97d767aa9ec3b65"}}
```

## 16. Negative examples for T4.5

Apply each mutation independently to a complete positive document and recompute no dependent hash unless the mutation explicitly tests a later semantic rule.

| Fixture ID | Mutation | Primary issue |
|---|---|---|
| `ledger-wrong-root` | rename `ucc_local_ledger` | `LEDGER_ROOT_INVALID` |
| `ledger-version-unknown` | change file version | `LEDGER_SCHEMA_VERSION_UNSUPPORTED` |
| `ledger-count-mismatch` | set `entry_count` to 3 | `LEDGER_COUNT_MISMATCH` |
| `ledger-sequence-duplicate` | duplicate sequence 1 | `LEDGER_SEQUENCE_INVALID` |
| `ledger-previous-hash-wrong` | change entry 2 previous hash | `LEDGER_PREVIOUS_HASH_INVALID` |
| `ledger-payload-hash-wrong` | change payload without contract hash | `LEDGER_PAYLOAD_HASH_MISMATCH` |
| `ledger-entry-hash-wrong` | change `canonical_hash` | `LEDGER_ENTRY_HASH_MISMATCH` |
| `ledger-file-hash-wrong` | change `ledger_hash` | `LEDGER_HASH_MISMATCH` |
| `ledger-entry-type-unknown` | use `assessment` | `LEDGER_ENTRY_TYPE_INVALID` |
| `ledger-source-type-unknown` | use `file` | `LEDGER_SOURCE_REF_INVALID` |
| `ledger-approval-ref-missing` | null approval ref on transition | `LEDGER_APPROVAL_REF_INVALID` |
| `ledger-brief-ref-half-null` | only one rendered-from field null | `LEDGER_PARENT_BRIEF_REF_INVALID` |
| `ledger-unknown-field` | add `debug_path` outside extensions | `LEDGER_UNKNOWN_FIELD` |
| `ledger-extension-unqualified` | add extension key `debug` | `LEDGER_EXTENSION_INVALID` |
| `ledger-idempotency-changed-payload` | replay key with changed payload | `LEDGER_IDEMPOTENCY_CONFLICT` |
| `ledger-entry-id-reused` | new key with existing entry ID | `LEDGER_ENTRY_ID_CONFLICT` |
| `ledger-tombstone-no-request` | tombstone lacks prior deletion request | `LEDGER_TOMBSTONE_INVALID` |
| `ledger-tombstone-private-payload` | tombstone retains learner ID/body | `LEDGER_TOMBSTONE_INVALID` |
| `ledger-compaction-gap-uncovered` | omit entry without tombstone hash | `LEDGER_SEQUENCE_INVALID` |
| `ledger-delete-hold-active` | delete target covered by hold | `LEDGER_DELETE_HOLD_ACTIVE` |

## 17. Acceptance criteria

1. File, entry, payload, source, approval, brief, retention, deletion, and tombstone shapes are closed and machine-testable.
2. All hash projections are exact and recomputable.
3. IDs, ordering, clock injection, replay, and conflict behavior have one meaning.
4. Exact replay appends nothing; changed-payload key reuse conflicts.
5. Every injected write fault preserves a complete old or complete new file and never falsely reports success.
6. Deletion is authorized, two-event, atomically compacted, and audit-preserving without retaining learner-sensitive payload in tombstones.
7. Unknown fields fail except namespaced inert extensions.
8. The examples and mutations are sufficient for T4.5 RED tests to fail only because ledger implementation is absent.
