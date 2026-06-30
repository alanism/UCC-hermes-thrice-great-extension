# Parent Brief and Atomic Ledger Contract

Status: C3.6 PROPOSED LOCK

Contracts:

- `ucc.parent_brief.v1`
- `ucc.ledger_entry.v1`
- `ucc.ledger_file.v1`

## Parent brief purpose

The core parent brief is a deterministic, evidence-labeled explanation for the configured parent/guardian. It separates observed facts, calculations, interpretations, limitations, and proposed next actions. It is not a public testimonial, sales artifact, diagnosis, mastery shortcut, or model-authored narrative.

Public blog/chronicle and prospective-parent pitch shapes in the legacy `parent_progress_brief` skill are presentation products outside the core durable contract.

## Parent brief envelope

| Field | Rule |
|---|---|
| `contract_version` | `ucc.parent_brief.v1`. |
| `parent_brief_id` | `pbrf_<ULID>`; injected. |
| `learner_id` | Pseudonymous durable ID. |
| `display_name` | Optional local presentation field; excluded from identity/logging. |
| `brief_type` | `assessment`, `weekly`, or `decision_support`. |
| `period_start`, `period_end` | UTC timestamps; start <= end. |
| `created_at` | Injected UTC timestamp. |
| `smc_ref` | Active SMC ID/revision/hash used for alignment. |
| `source_refs` | Sorted typed refs to accepted receipts, pair results, ledger entries, and/or proposals. |
| `source_set_sha256` | Canonical hash of ordered source IDs and payload hashes. |
| `sections` | Structured content below. |
| `limitations` | Stable issue codes and safe explanations. |
| `render_profile_id` | Immutable deterministic template identity. |
| `semantic_payload_sha256` | Canonical hash excluding display name and `created_at`. |

Every source ref carries contract name/version, record ID, canonical payload hash, quality/status, and local resolution state. Unresolved or unusable source evidence cannot be silently summarized.

## Evidence labels

Every substantive brief statement is a structured claim:

| Label | Meaning |
|---|---|
| `measured` | Direct validated receipt/event observation. |
| `calculated` | Deterministic calculation with named formula/policy. |
| `modeled` | Deterministic rule-based interpretation; not raw fact. |
| `forecast` | Proposed expectation or future possibility. |
| `noted` | Parent/coach observation with explicit human provenance. |

Claim object fields:

- `claim_id` (`clm_<ULID>`, injected or deterministically derived by registered policy);
- `label` from the table;
- `claim_code` stable vocabulary;
- `text_key` plus structured interpolation values for deterministic rendering;
- `source_refs` non-empty except forecast proposals;
- `confidence`: `direct`, `bounded`, or `tentative`;
- `valid_evidence_claim`: `practice`, `familiarity`, `performance`, `mastery_candidate`, `mastery_established`, or `insufficient_evidence`;
- `ai_role_summary`;
- `process_evidence_status`;
- `student_thinking_evidence_status`;
- `mastery_policy_id` and supporting ledger entry ID only when claim is `mastery_established`.

`mastery_established` is forbidden unless an accepted ledger entry records that decision under a locked mastery policy. A receipt or pair result alone can provide at most `mastery_candidate`.

## Brief sections

All section keys are required; arrays may be empty with an explicit limitation.

1. `executive_summary`: up to three evidence-labeled claims.
2. `demonstrated_strengths`: measured/calculated claims with source evidence.
3. `attention_areas`: evidence gaps or observed difficulty; never fixed learner labels.
4. `condition_comparison`: pair metrics and policy status, if a valid pair exists.
5. `ai_role_clarity`: what AI did and what student evidence remains independently attributable.
6. `process_and_thinking_evidence`: referenced process/student-thinking evidence status.
7. `mastery_evidence`: established, candidate, insufficient, or not assessed; source/policy required.
8. `false_mastery_risks`: stable reasons a stronger claim is not valid; no conduct accusation.
9. `proposed_next_actions`: forecast claims linked to proposal drafts, never active work.
10. `questions_for_parent`: deterministic decision prompts.

The terms “weakness,” “cheating,” “ghostwriting,” and AI-writing detection are not contract labels. Rendering uses neutral evidence language.

## Brief semantic rules

- Source learner IDs must all match the brief learner ID.
- Period bounds must cover every included source event time.
- Void/suppressed evidence contributes only audit existence and limitations.
- Degraded evidence can support measured facts explicitly allowed by its quality result, never pair/mastery claims.
- Limited evidence propagates its issue codes to the claim and limitations.
- Conflicting sources are shown as a conflict; the renderer cannot choose one silently.
- No clinical or causal interpretation is produced from pressure delta.
- Recommendations are proposals and remain unapproved.
- The deterministic core renders only registered text keys/templates. Optional model prose, if ever approved, is a separate non-authoritative presentation layer and cannot modify facts or decisions.

Stable brief issues include:

- `BRIEF_SOURCE_UNRESOLVED`;
- `BRIEF_SOURCE_HASH_MISMATCH`;
- `BRIEF_LEARNER_MISMATCH`;
- `BRIEF_PERIOD_INVALID`;
- `BRIEF_SOURCE_QUALITY_UNUSABLE`;
- `BRIEF_SOURCE_LIMITATION_PROPAGATED`;
- `BRIEF_CLAIM_SOURCE_MISSING`;
- `BRIEF_CLAIM_LABEL_INVALID`;
- `BRIEF_MASTERY_AUTHORITY_MISSING`;
- `BRIEF_CONFLICT_UNRESOLVED`;
- `BRIEF_TEMPLATE_UNSUPPORTED`.

## Ledger role

The ledger is a private local append-only logical history of accepted evidence, comparisons, briefs, proposals, approval decisions, transitions, and later mastery decisions. Normal writes never edit or delete an existing semantic entry. Corrections append a new entry referencing the prior entry.

Privacy-authorized deletion is the sole exception to physical append-only storage and follows the controlled tombstone/compaction protocol below.

## Ledger file

One configured namespace uses one canonical JSON file under an explicit private data root outside Git.

Ledger file envelope:

| Field | Rule |
|---|---|
| `contract_version` | `ucc.ledger_file.v1`. |
| `ledger_namespace` | Stable configured local namespace. |
| `created_at` | Injected creation timestamp. |
| `retention_policy_id` | Immutable policy identity. |
| `entry_count` | Exact entries length. |
| `head_sequence` | 0 for empty, otherwise final sequence. |
| `head_entry_chain_sha256` | Null for empty, otherwise final chain hash. |
| `entries` | Ordered ledger entry array. |

The configured file path is not part of semantic identity and is never stored in build receipts or logs.

## Ledger entry

| Field | Rule |
|---|---|
| `contract_version` | `ucc.ledger_entry.v1`. |
| `ledger_entry_id` | `ldgr_<ULID>`; globally unique in namespace. |
| `write_idempotency_key` | Namespace-global opaque key. |
| `sequence` | Previous head + 1, starting at 1. |
| `previous_entry_chain_sha256` | Null at sequence 1; otherwise exact prior chain hash. |
| `entry_type` | `evidence`, `pair_result`, `parent_brief`, `proposal`, `approval_event`, `approval_transition`, `mastery_decision`, `correction`, or `deletion_tombstone`. |
| `learner_id` | Pseudonymous ID or null for namespace/system event. |
| `occurred_at` | Domain event time from source, not write time. |
| `recorded_at` | Injected local commit time. |
| `source_refs` | Sorted typed record refs/hashes. |
| `payload_contract` | Contract name/version of embedded or referenced payload. |
| `payload` | Canonical semantic payload or content-addressed local reference. |
| `payload_sha256` | Hash of canonical payload. |
| `semantic_sha256` | Hash excluding sequence, previous chain, recorded time, and physical path. |
| `entry_chain_sha256` | Hash of the complete entry excluding this field, including recorded time and previous chain. |

`source_refs` and `payload` cannot contain absolute paths, secrets, display names as keys, or unvalidated raw model output.

### Linkage rules

- Evidence entry references accepted receipt ID/hash.
- Pair entry references both receipt IDs/hashes and pairing policy/registry hash.
- Brief entry references brief ID/hash and its source-set hash.
- Proposal entry references exact proposal ID/revision/hash and SMC ref.
- Approval entry references accepted approval event plus proposal revision/hash.
- Transition entry references approval event and prior/next state result.
- Mastery decision references the locked mastery policy plus sufficient ledger evidence; no receipt alone establishes it.
- Correction references exactly one prior entry and describes replacement semantics without altering the prior bytes.
- Tombstone references deleted entry IDs and hashes but contains no deleted learner payload.

## Canonical JSON and clocks

- UTF-8, NFC strings, LF, sorted object keys, no insignificant whitespace.
- Integers remain integers; decimal policy is contract-specific; NaN/Infinity forbidden.
- Arrays preserve semantic order unless their field declares sorted uniqueness.
- UTC timestamps use RFC 3339 `Z` with millisecond precision.
- IDs and clocks are injected dependencies.
- `semantic_sha256` provides repeatable cross-run comparison.
- `entry_chain_sha256` provides storage-history integrity and includes injected storage envelope values.

The registry design in C3.7 freezes the canonicalization algorithm/version.

## Write idempotency

The first accepted `write_idempotency_key` binds to `semantic_sha256` within the namespace.

- Identical key and semantic hash returns the existing entry without append.
- Same key and different semantic hash returns `LEDGER_IDEMPOTENCY_CONFLICT`.
- Duplicate payload under a new key is allowed only when the entry type contract allows repeated observations; it is never silently deduplicated.

Approval-event idempotency is validated before ledger write and remains independently enforceable.

## Atomic commit protocol

Normal append rewrites the complete ledger file atomically:

1. Resolve and verify configured data root, ledger path, and lock path remain contained on one volume; reject links, junctions, and reparse points.
2. Acquire an exclusive namespace lock with bounded timeout and recorded owner token.
3. Read the current ledger once; validate schema, entry count, sequence, chain, hashes, and idempotency index.
4. Build the next complete ledger in memory and validate it before I/O.
5. Create a unique temporary file in the ledger file's same directory with exclusive creation.
6. Write canonical bytes, flush userspace buffers, and `fsync`/`FlushFileBuffers` the temporary file.
7. Recheck lock ownership and unchanged prior ledger hash.
8. Replace the ledger atomically with the same-volume platform operation.
9. Flush the containing directory where supported; record an explicit durability warning where the platform cannot do so.
10. Reopen and read back the ledger; verify complete file hash, new head, chain, and target entry.
11. Release lock and emit a commit receipt only after readback passes.

The implementation may not report success before step 10.

### Fault behavior

| Fault point | Required outcome |
|---|---|
| Before/during temp write or temp flush | Prior ledger remains byte-identical; temp is safely removed/quarantined. |
| Lock lost or prior hash changed before replace | Abort; prior ledger remains; return conflict. |
| Replace fails | Prior ledger remains; no success receipt. |
| Crash after successful replace before directory flush/readback | Recovery sees either complete old or complete new ledger, never partial; rerun uses idempotency key. Return state is unknown until recovery/readback. |
| Readback/hash fails | Return `LEDGER_COMMIT_UNKNOWN`; quarantine writes; never claim rollback without evidence. |

No best-effort in-place append is permitted.

## Recovery

On open:

1. reject path escapes/reparse points;
2. inspect ledger and same-directory temp candidates;
3. validate complete hashes/chains before considering any file;
4. prefer the valid ledger at configured path;
5. never auto-promote a temp candidate over a valid ledger;
6. require explicit recovery command/human confirmation if configured ledger is invalid and a valid temp exists;
7. rerun uncertain operations with the same idempotency key.

## Retention and deletion

Retention policy specifies entry-type durations, legal/owner holds, and deletion authorization. No implicit default deletion period exists.

An authorized deletion request contains request ID, parent/owner actor ID, namespace, target learner/entry IDs, policy ID, requested time, and idempotency key. Deletion:

1. validates authority and scope;
2. builds a new ledger omitting targeted payload entries;
3. appends a `deletion_tombstone` containing only request ID, target entry IDs, prior hashes, reason code, and deletion time;
4. atomically commits the rewritten ledger through the same protocol;
5. returns the existing tombstone on identical replay;
6. conflicts on changed scope under the same key.

This is controlled privacy compaction, not historical mutation disguised as a normal append. Backups and synced copies require the deployment retention/delete contract; deletion is not claimed complete for copies the system cannot control.

## Ledger issue codes

| Code | Meaning |
|---|---|
| `LEDGER_PATH_INVALID` | Root/path containment or reparse check failed. |
| `LEDGER_LOCK_TIMEOUT` | Exclusive lock unavailable. |
| `LEDGER_LOCK_LOST` | Lock ownership changed before replace. |
| `LEDGER_SCHEMA_INVALID` | File or entry shape invalid. |
| `LEDGER_COUNT_MISMATCH` | Header count/head disagrees with entries. |
| `LEDGER_SEQUENCE_INVALID` | Sequence not contiguous. |
| `LEDGER_CHAIN_INVALID` | Previous/head chain hash invalid. |
| `LEDGER_PAYLOAD_HASH_MISMATCH` | Payload hash invalid. |
| `LEDGER_IDEMPOTENCY_CONFLICT` | Key already binds different semantic hash. |
| `LEDGER_CONCURRENT_MODIFICATION` | Prior ledger hash changed under lock. |
| `LEDGER_TEMP_WRITE_FAILED` | Temp creation/write/flush failed. |
| `LEDGER_REPLACE_FAILED` | Atomic replacement failed. |
| `LEDGER_COMMIT_UNKNOWN` | Replace may have occurred but durable readback not proven. |
| `LEDGER_READBACK_FAILED` | New complete state could not be verified. |
| `LEDGER_DURABILITY_WARNING` | Directory flush unsupported after otherwise verified commit. |
| `LEDGER_DELETE_AUTHORITY_INVALID` | Deletion actor/scope invalid. |
| `LEDGER_RETENTION_POLICY_MISSING` | Required retention policy unavailable. |

Issues/logs contain safe paths only as configured aliases, never absolute private paths or payload content.

## Acceptance criteria

1. Brief facts, calculations, modeled interpretations, forecasts, and human notes remain distinguishable.
2. AI role and student/process evidence determine valid claim strength without policing AI use.
3. Parent brief mastery language requires an accepted ledger mastery decision.
4. Brief limitations propagate receipt/pair quality deterministically.
5. Entry IDs, event time, recorded time, semantic hash, chain hash, and linkage have one meaning.
6. Exact write replay is idempotent; changed-payload key reuse conflicts.
7. Fault injection at every commit stage preserves a complete prior or new ledger and never falsely reports success.
8. Corrections append; ordinary writes never mutate prior entries.
9. Privacy deletion is authorized, idempotent, atomically compacted, and tombstoned without retaining deleted content.
10. Real data, private paths, names, answers, and evidence bodies never enter build/test logs or Git.
