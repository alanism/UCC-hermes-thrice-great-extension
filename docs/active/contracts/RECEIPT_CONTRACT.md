# Assessment Receipt and Semantic Validation Contract

Status: SPECIFICATION LOCKED BY C3.7; SCHEMA/VALIDATOR TEST-GATED

Contract name: `ucc.assessment_receipt`

Initial production major version: `2`

## Purpose

An assessment receipt is a local, durable record of what occurred in one assessment session. It preserves observed performance, conditions, AI role, process evidence, and student-thinking evidence. It is not itself a mastery decision, diagnosis, clinical label, or misconduct judgment.

Receipt v2 supersedes `ucc.receipt.v1`, `ucc.assessment_event.v1`, and `ucc.receipt_integrity.v1` as the canonical write format. Those v1 contracts remain read-only migration inputs.

## Canonical receipt envelope

| Field | Type | Rule |
|---|---|---|
| `contract_version` | string | `ucc.assessment_receipt.v2.0.0`. |
| `receipt_id` | string | `rcpt_<ULID>`; globally unique in the configured ledger namespace. |
| `session_id` | string | `sess_<ULID>`; identifies one execution. |
| `paired_run_id` | string or null | `pair_<ULID>` only when the session was intentionally scheduled as part of a pair. Pair validity is decided separately. |
| `assessment_form_id` | string | Stable form identity; required and never inferred from title. |
| `assessment_form_version` | positive integer | Exact immutable form revision. |
| `learner_id` | string | Pseudonymous durable learner ID. |
| `display_name` | string or null | Optional local presentation field; never used in IDs, hashes, logs, pairing, or ledger keys. |
| `source` | object | `app_id`, `app_version`, `device_session_id` or null, and `generated_at`. |
| `assessment` | object | Domain, name, explicit mode, declared skill scope, level context, and timer policy. |
| `session` | object | Start/end timestamps and completion status. |
| `events` | array | Ordered presented-item events; at least one unless completion is `aborted_before_start`. |
| `summary` | object | Deterministic totals derived from events. |
| `evidence_context` | object | Session AI role and evidence-reference summary. |
| `quality` | object | Deterministic semantic-validation result and stable issues. |

All timestamps, IDs, hashes, issues, and references use the common contract-version policy. Writers inject clocks and IDs. Validators never invent missing values.

## Assessment object

Required fields:

| Field | Type / rule |
|---|---|
| `domain` | `math` or `reading` for v2. New domains require a compatible minor or new major decision. |
| `name` | non-empty display label; not identity. |
| `mode` | exactly `calm` or `pressure`; mandatory, never inferred from duration. |
| `skill_ids` | non-empty, sorted, unique stable skill IDs represented by the form. |
| `reported_grade_or_level` | string or null; context only, not evidence. |
| `timer_policy` | object below. |

Timer policy:

| Field | CALM | PRESSURE |
|---|---|---|
| `timer_visible` | must be false | must be true |
| `time_limit_seconds` | null | positive integer |
| `timeout_behavior` | `none` | `per_item`, `session_deadline`, or `both` |
| `policy_id` | stable non-empty policy identifier | stable non-empty policy identifier |

Legacy duration-based mode inference is allowed only inside a named v1 adapter and produces warning `RECEIPT_LEGACY_MODE_INFERRED`. It is forbidden for v2 input.

## Session object

Required fields:

- `started_at`;
- `completed_at` or null;
- `completion_status`: `completed`, `partial`, `aborted`, `expired`, or `aborted_before_start`;
- `termination_reason`: non-empty string or null.

Rules:

- `completed` requires non-null `completed_at` and every presented event resolved.
- `partial`, `aborted`, and `expired` require non-null `completed_at` and a termination reason.
- `aborted_before_start` requires null `completed_at` and zero events.
- No event timestamp may precede `started_at` or follow non-null `completed_at`.
- `source.generated_at` must be at or after non-null `completed_at`, or at/after `started_at` for `aborted_before_start`.

## Event object

Every event has:

| Field | Type / rule |
|---|---|
| `event_id` | `evt_<ULID>`; unique within and across receipts. |
| `item_index` | positive integer, unique and contiguous from 1 in event order. |
| `form_item_id` | stable item ID from the immutable assessment form revision. |
| `skill_id` | one of `assessment.skill_ids`. |
| `skill_label` | optional presentation label. |
| `grade_or_level` | string or null; item context only. |
| `prompt_type` | `multiple_choice`, `numeric`, `free_response`, or `visual_model`. |
| `presented_at` | UTC timestamp. |
| `resolved_at` | UTC timestamp at or after `presented_at`. |
| `response_status` | `answered`, `timeout`, or `skipped`. |
| `response_time_ms` | nonnegative integer measured by a monotonic timer. |
| `answer` | string or null; sensitive local data. |
| `correct_answer` | string or null; sensitive local form data. |
| `is_correct` | boolean for `answered`; null otherwise. |
| `difficulty_before` | integer or null. |
| `difficulty_after` | integer or null. |
| `error_type` | `conceptual`, `procedural`, `attention_signal`, `operation_mismatch`, `other`, `none`, or null. |
| `error_type_other_label` | non-empty string only when `error_type` is `other`; otherwise null. |
| `failure_stage` | `plan`, `work`, `check`, `response`, `unknown`, `none`, or null. |
| `representation_stage` | `concrete`, `pictorial`, `abstract`, `unknown`, or null. |
| `evidence_intent` | `practice`, `familiarity`, `performance_check`, or `mastery_check`. |
| `independence` | `independent`, `scaffolded`, `collaborative`, or `unknown`. |
| `ai_role` | object below. |
| `process_evidence_refs` | sorted unique local artifact IDs; may be empty. |
| `student_thinking_evidence_refs` | sorted unique local artifact IDs; may be empty. |

AI role object:

- `role`: `none`, `instructions_only`, `socratic_prompt`, `strategy_prompt`, `explanation_before_attempt`, `explanation_after_attempt`, `answer_generation`, `composition_assistance`, or `other`;
- `disclosed`: boolean;
- `description`: required only for `other`.

AI assistance is not prohibited and is not treated as cheating. It changes what evidence claim is valid.
The resulting distinction is a false mastery risk check, not an AI-use or conduct check.

For `mastery_check`, all of these are required:

- `response_status: answered`;
- `independence: independent`;
- non-empty `student_thinking_evidence_refs`;
- non-empty `process_evidence_refs` for free-response, numeric multi-step, and visual-model prompts;
- `ai_role.role` limited to `none`, `instructions_only`, or `explanation_after_attempt`.

If these are absent, the event remains useful session evidence but is not mastery-eligible and emits `RECEIPT_FALSE_MASTERY_RISK`. The validator does not accuse or classify the learner.

## Summary object and denominators

Required fields:

- `items_presented`;
- `items_answered`;
- `correct`;
- `incorrect`;
- `timeouts`;
- `skipped`;
- `accuracy_answered`;
- `engagement_rate`;
- `average_response_time_ms`;
- `max_grade_or_level_reached`.

Exact derivation:

```text
items_presented = len(events)
items_answered = count(response_status == answered)
correct = count(answered and is_correct == true)
incorrect = count(answered and is_correct == false)
timeouts = count(response_status == timeout)
skipped = count(response_status == skipped)
items_answered = correct + incorrect
items_presented = items_answered + timeouts + skipped
accuracy_answered = correct / items_answered, or null when items_answered == 0
engagement_rate = (items_answered + timeouts) / items_presented,
                  or null when items_presented == 0
average_response_time_ms = arithmetic mean response_time_ms for answered events,
                           rounded half-even to an integer, or null when none
```

Decimal ratios are canonical numbers rounded half-even to four decimal places. Timeout and skipped events never enter the accuracy denominator. Pairing may define a second presented-item metric but cannot relabel it as `accuracy_answered`.

`max_grade_or_level_reached` is string or null and must be selected from answered events by the immutable form's declared level order. Lexical sorting is forbidden.

## Evidence context

Required fields:

- `session_ai_roles`: sorted unique roles observed in events;
- `process_evidence_count`;
- `student_thinking_evidence_count`;
- `mastery_check_event_count`;
- `mastery_eligible_event_count`;
- `valid_evidence_claim`: `practice_only`, `familiarity_only`, `performance_evidence`, `mastery_candidate_evidence`, or `insufficient_evidence`;
- `false_mastery_risk`: boolean;
- `false_mastery_reason_codes`: sorted unique issue codes.

This object is deterministically derived. `mastery_candidate_evidence` means the receipt may be evaluated with other evidence under the future ledger mastery policy; it does not mean mastery is established.

## Quality model

`quality` contains `status`, `blocking_issues`, and `warnings`. Each issue has `code`, `path`, and safe metadata containing IDs/counts only. Human prose is rendered from issue codes outside the canonical payload.

| Status | Meaning | Permitted downstream use |
|---|---|---|
| `clean` | No blocking issues or warnings. | Full observed-fact use; may enter pairing/mastery-candidate evaluation. |
| `limited` | Valid and interpretable with warnings that narrow claims. | Observed facts and explicitly allowed calculations; limited reasons propagate. |
| `degraded` | Partially interpretable due to declared missing/inconsistent non-core evidence. | Raw observed facts only; no pairing delta or mastery candidate. |
| `void` | Core identity, chronology, totals, or event truth cannot be trusted. | Provenance/audit only; no learning inference. |
| `suppressed` | Human/privacy policy intentionally withholds evidence. | Existence/audit metadata only; no learning inference. |

Derivation precedence: `suppressed` by explicit parent/privacy control; otherwise any void-class issue -> `void`; otherwise any degraded-class issue -> `degraded`; otherwise any warning -> `limited`; otherwise `clean`.

A producer cannot self-upgrade quality. The semantic validator recomputes it.

## Stable semantic issue codes

### Void-class blocking issues

| Code | Condition |
|---|---|
| `RECEIPT_ID_DUPLICATE` | Receipt ID already binds a different canonical payload. |
| `RECEIPT_SESSION_ID_DUPLICATE` | Session ID already binds a different receipt. |
| `RECEIPT_FORM_ID_MISSING` | Form identity/version is absent. |
| `RECEIPT_TIMESTAMP_ORDER_INVALID` | Session/source/event chronology is impossible. |
| `RECEIPT_EVENT_ID_DUPLICATE` | Event ID repeats or binds different content. |
| `RECEIPT_EVENT_ORDER_INVALID` | Item indexes are duplicate, non-contiguous, or out of order. |
| `RECEIPT_TOTAL_MISMATCH` | Summary totals do not exactly derive from events. |
| `RECEIPT_ANSWER_STATE_INVALID` | Answer/correctness fields contradict response status. |
| `RECEIPT_COMPLETION_STATE_INVALID` | Completion status contradicts timestamps/events. |
| `RECEIPT_MODE_TIMER_MISMATCH` | Explicit mode contradicts timer policy. |
| `RECEIPT_SKILL_SCOPE_MISMATCH` | Event skill is outside declared form skill scope. |

### Degraded-class issues

| Code | Condition |
|---|---|
| `RECEIPT_FORM_ITEM_UNKNOWN` | Event item is not resolvable in the stated form revision. |
| `RECEIPT_LEVEL_ORDER_UNKNOWN` | Max level cannot be deterministically derived. |
| `RECEIPT_PROCESS_EVIDENCE_UNRESOLVED` | Referenced process artifact cannot be resolved locally. |
| `RECEIPT_THINKING_EVIDENCE_UNRESOLVED` | Referenced student-thinking artifact cannot be resolved locally. |
| `RECEIPT_SOURCE_VERSION_UNSUPPORTED` | Source version has no declared adapter/compatibility rule. |

### Limited warnings

| Code | Condition |
|---|---|
| `RECEIPT_PARTIAL_SESSION` | Completion is partial/aborted/expired but remaining facts are coherent. |
| `RECEIPT_NO_ANSWERED_ITEMS` | No accuracy denominator exists. |
| `RECEIPT_AI_ROLE_UNDISCLOSED` | AI role is not `none` and disclosure is false. |
| `RECEIPT_FALSE_MASTERY_RISK` | Mastery intent lacks required independent thinking/process evidence. |
| `RECEIPT_LEGACY_MODE_INFERRED` | A named legacy adapter inferred mode; impossible on native v2. |
| `RECEIPT_PAIR_DECLARED_NOT_VALIDATED` | `paired_run_id` exists but no valid pair result is linked yet. |

Schema/type failures use `RECEIPT_SCHEMA_INVALID` and the receipt is rejected before semantic quality classification.

Issues sort by JSON path, code, then stable ID. No issue includes raw answers, names, prompts, or private artifact content.

## Validation result

The validator returns a separate result envelope:

- `validator_contract_version`;
- `validator_version`;
- `receipt_id`;
- `canonical_payload_sha256`;
- `quality`;
- `validated_at` in a volatile audit envelope;
- `accepted_for_storage`;
- `accepted_for_pairing`;
- `accepted_for_mastery_candidate_evaluation`.

Canonical payload hashing excludes `validated_at` and display-only fields. The registry policy freezes exact canonicalization.

## Legacy v1 adapter

The v1 adapter must:

1. preserve source bytes/hash and record `source_contract_version`;
2. require injected `receipt_id` when absent;
3. map `student.student_id` to `learner_id` and treat display name as optional presentation data;
4. require external `assessment_form_id` and version or emit void;
5. map assessment mode directly when present; only the explicitly named duration adapter may infer it with warning;
6. map events without fabricating thinking/process evidence;
7. recompute all totals and quality;
8. never promote v1 evidence to mastery-eligible merely because it was correct.

## Acceptance criteria

1. IDs, timestamps, modes, timers, totals, event states, quality states, and issue codes have one meaning.
2. Reordered/duplicated events, reversed timestamps, mismatched totals, and mode/timer mutations fail deterministically.
3. Timeout and skipped denominators cannot inflate or deflate answered accuracy.
4. AI-assisted output remains usable with explicit role, while unsupported mastery claims are blocked.
5. No cheating, ghostwriting, or AI-writing detector exists.
6. Raw names, answers, prompts, and evidence bodies never enter logs/issues.
7. Void/degraded/limited evidence cannot be silently upgraded downstream.
8. Same semantic input, injected IDs/clocks, form registry, and validator version produce byte-identical canonical semantic output.
