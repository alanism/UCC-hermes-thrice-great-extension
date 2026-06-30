# School Model Canvas Contract

Status: SPECIFICATION LOCKED BY C3.7; SCHEMA/VALIDATOR TEST-GATED

Contract name: `ucc.smc`

Initial major version: `1`

## Purpose and authority

The School Model Canvas is a parent-controlled educational constitution and decision filter. It records declared values, preferences, constraints, and context. It is not a lesson plan, diagnosis, learner label, mastery record, or approval for a specific campaign.

Only a `parent_guardian` actor may create an active initial revision or authorize an active amendment. Hermes, a model, a plugin, a skill, a tutor, or a learning coach may propose a change but cannot activate it.

## Durable envelope

Every normalized SMC document has these required fields:

| Field | Type | Rule |
|---|---|---|
| `contract_version` | string | Exact semantic version; initial value `ucc.smc.v1.0.0`. |
| `smc_id` | string | Stable pseudonymous ID, `smc_<ULID>`; unchanged across revisions. |
| `revision` | integer | Starts at 1 and increments by exactly 1. |
| `lifecycle_status` | enum | `draft`, `active`, or `superseded`. Only one active revision per `smc_id`. |
| `learner_id` | string | Pseudonymous durable ID; never a display name. |
| `display_name` | string or null | Optional local presentation data; excluded from keys, hashes used for identity, logs, and ledger linkage. |
| `created_at` | UTC timestamp | Time this revision record was created; injected clock. |
| `effective_at` | UTC timestamp or null | Required for `active`; null for draft. |
| `source` | object | `format`, `source_hash`, and optional local source label. No absolute private path in durable output. |
| `authorship` | object | `actor_type`, pseudonymous `actor_id`, and `authored_at`; active revision requires `actor_type: parent_guardian`. |
| `supersedes_revision` | integer or null | Null only for revision 1; otherwise exactly `revision - 1`. |
| `amendment_decision` | object or null | Required for active revision >1; defined below. |
| `canvas` | object | All normalized template sections and fields. |

Timestamps, ULIDs, hashes, learner IDs, actor IDs, issue objects, and references use the common contract-version policy. Contract validation never generates IDs or clocks; callers inject them.

## Missing, unknown, and empty values

Every field mapped from the Markdown template must be present in normalized JSON.

- `null` means unknown, not supplied, or intentionally unanswered.
- `[]` means the parent explicitly declared none for a list field.
- Missing property means malformed normalization and is rejected.
- Empty or whitespace-only strings are rejected; normalizers convert untouched placeholders to `null`.
- An unrecognized heading, label, duplicate field, or duplicate section is rejected rather than silently discarded.
- `other` enum values require a non-empty adjacent `other_label`.
- Drafts may contain null values. Activation requires the critical values listed below.

This distinction prevents “unknown” from being interpreted as “no constraint.”

## Canvas structure

All section objects are required. Unless noted otherwise, scalar values are non-empty string or null; list values are unique non-empty strings or null.

### `learner_context`

| Field | Type / vocabulary |
|---|---|
| `age_years` | integer 0–120 or null |
| `grade_stage` | string or null; presentation context, not a capability claim |
| `schooling_context` | `hybrid`, `homeschool`, `public_school`, `private_school`, `other`, or null |
| `schooling_context_other_label` | string or null |
| `exported_date` | local calendar date or null; provenance only, never revision order |

### `educational_vision`

- `vision`: non-empty string or null.

### `teaching_approach`

| Field | Vocabulary |
|---|---|
| `style` | `collaborative`, `directive`, `mixed`, `other`, or null |
| `pacing` | `linear`, `cyclic`, `interest_driven`, `mixed`, `other`, or null |
| `evaluation_methods` | array drawn from `demonstration`, `testing`, `portfolio`, `observation`, `project`, `other`, or null |
| `other_labels` | string array or null; required when an `other` value is selected |

### `learning_preferences`

| Field | Vocabulary |
|---|---|
| `modalities` | array of `hands_on`, `visual`, `auditory`, `reading`, `mixed`, `other`, or null |
| `environments` | array of `ambient`, `structured`, `social`, `independent`, `mixed`, `other`, or null |
| `scope` | `deep_dive`, `broad_exposure`, `mixed`, `other`, or null |
| `other_labels` | string array or null |

Preferences are parent-declared context, not fixed learner traits or diagnoses.

### `communication_authority`

| Field | Vocabulary |
|---|---|
| `communication_mode` | `discussion`, `instruction`, `learner_led`, `mixed`, `other`, or null |
| `adult_role` | `mentor_apprentice`, `guide`, `director`, `mixed`, `other`, or null |
| `other_labels` | string array or null |

### `physical_activity`

- `frequency`: string or null.
- `activity_types`: array or null.
- `goals`: array or null.

### `socializing`

- `peer_interaction`: string or null.
- `group_learning_enabled`: boolean or null.
- `group_learning_notes`: string or null; required when enabled is true.
- `community_involvement`: array or null.

### `technology`

- `available_devices`: array or null.
- `screen_time_policy`: string or null.
- `digital_literacy_goals`: array or null.

### `enrichment`

- `extracurriculars`: array or null.
- `special_interests`: array or null.
- `field_experiences`: array or null.

### `confidence_building`

- `strategies`: array or null.
- `known_challenges`: array or null.
- `support_resources`: array or null.

These fields describe declared support context. They cannot be converted into clinical or misconduct labels.

### `family_values`

- `educational_philosophies`: array or null.
- `cultural_religious_considerations`: array or null.
- `long_term_vision`: string or null.

This section is sensitive local data and is never emitted to logs or outbound adapters by default.

### `learning_environment`

- `learning_spaces`: array or null.
- `distractions_and_mitigations`: array or null.
- `schedule_flexibility`: `strict`, `mostly_structured`, `mixed`, `mostly_fluid`, `fluid`, `other`, or null.
- `schedule_flexibility_other_label`: string or null.

### `resources_budget`

- `curriculum_materials`: array or null.
- `budget_note`: string or null.
- `support_network`: array or null.

Budget and support-network content is sensitive local data.

### `guardian_expectations`

- `weekly_time_commitment`: string or null.
- `co_learning`: `yes`, `no`, `sometimes`, `unknown`, or null.
- `adaptability`: string or null.

## Activation requirements

An SMC revision cannot become active unless all of these are non-null:

- `learner_id`;
- `educational_vision.vision`;
- `teaching_approach.style`;
- `teaching_approach.pacing`;
- `teaching_approach.evaluation_methods` with at least one item;
- `communication_authority.communication_mode`;
- `communication_authority.adult_role`;
- `authorship` by `parent_guardian`;
- `effective_at`.

Other null fields are allowed and remain explicitly unknown. They must not be filled by inference.

## Markdown normalization

Input is UTF-8 Markdown based on `templates/SMC-TEMPLATE.md`.

1. Normalize line endings to LF and Unicode to NFC.
2. The title supplies optional `display_name`; placeholder `[Learner Name]` becomes null.
3. Match section headings and labels by Unicode-normalized, trimmed, case-folded text after collapsing internal whitespace.
4. Accept the exact template labels and the aliases listed in the mapping table below; no fuzzy matching.
5. Strip surrounding Markdown emphasis from labels, not from values.
6. Convert untouched bracket placeholders to null.
7. Split list-like values only on explicit Markdown list items or semicolons; commas remain part of text unless the field vocabulary is enum-based.
8. Preserve value text after trimming; do not rewrite beliefs, challenges, goals, or support descriptions.
9. Produce a SHA-256 `source_hash` over the normalized Markdown bytes.
10. Return deterministic ordered issues and no normalized document when a blocking issue exists.

### Template mapping

| Markdown source | JSON path |
|---|---|
| Title learner name | `display_name` |
| `Age` | `canvas.learner_context.age_years` |
| `Grade/Stage` | `canvas.learner_context.grade_stage` |
| `Schooling Context` | `canvas.learner_context.schooling_context` |
| `Exported Date` | `canvas.learner_context.exported_date` |
| Educational Vision body | `canvas.educational_vision.vision` |
| Teaching Approach / `Style` | `canvas.teaching_approach.style` |
| Teaching Approach / `Pacing` | `canvas.teaching_approach.pacing` |
| Teaching Approach / `Evaluation` | `canvas.teaching_approach.evaluation_methods` |
| Child's Learning Style / `Modality` | `canvas.learning_preferences.modalities` |
| Child's Learning Style / `Environment` | `canvas.learning_preferences.environments` |
| Child's Learning Style / `Scope` | `canvas.learning_preferences.scope` |
| Communication & Authority / `Mode` | `canvas.communication_authority.communication_mode` |
| Communication & Authority / `Role` | `canvas.communication_authority.adult_role` |
| Physical Activity / `Frequency` | `canvas.physical_activity.frequency` |
| Physical Activity / `Types` | `canvas.physical_activity.activity_types` |
| Physical Activity / `Goals` | `canvas.physical_activity.goals` |
| Socializing / `Peer Interaction` | `canvas.socializing.peer_interaction` |
| Socializing / `Group Learning` | `canvas.socializing.group_learning_enabled`, plus notes |
| Socializing / `Community Involvement` | `canvas.socializing.community_involvement` |
| Technology / `Devices` | `canvas.technology.available_devices` |
| Technology / `Screen Time Policy` | `canvas.technology.screen_time_policy` |
| Technology / `Digital Literacy Goals` | `canvas.technology.digital_literacy_goals` |
| Enrichment / `Extracurriculars` | `canvas.enrichment.extracurriculars` |
| Enrichment / `Special Interests` | `canvas.enrichment.special_interests` |
| Enrichment / `Field Trips / Experiences` | `canvas.enrichment.field_experiences` |
| Confidence Building / `Strategies` | `canvas.confidence_building.strategies` |
| Confidence Building / `Challenges` | `canvas.confidence_building.known_challenges` |
| Confidence Building / `Support` | `canvas.confidence_building.support_resources` |
| Family Beliefs & Values / `Educational Philosophy` | `canvas.family_values.educational_philosophies` |
| Family Beliefs & Values / `Cultural / Religious Considerations` | `canvas.family_values.cultural_religious_considerations` |
| Family Beliefs & Values / `Long-Term Vision` | `canvas.family_values.long_term_vision` |
| Environment / `Learning Space` | `canvas.learning_environment.learning_spaces` |
| Environment / `Distractions` | `canvas.learning_environment.distractions_and_mitigations` |
| Environment / `Schedule Flexibility` | `canvas.learning_environment.schedule_flexibility` |
| Resources & Budget / `Curriculum / Materials` | `canvas.resources_budget.curriculum_materials` |
| Resources & Budget / `Budget` | `canvas.resources_budget.budget_note` |
| Resources & Budget / `Support Network` | `canvas.resources_budget.support_network` |
| Parent / Guardian Expectations / `Weekly Time Commitment` | `canvas.guardian_expectations.weekly_time_commitment` |
| Parent / Guardian Expectations / `Your Own Learning` | `canvas.guardian_expectations.co_learning` |
| Parent / Guardian Expectations / `Flexibility` | `canvas.guardian_expectations.adaptability` |

No template field is dropped.

## Amendment protocol

Revisions are append-only. Existing active JSON is never edited in place.

An amendment proposal is non-authoritative and contains:

- `proposal_id`;
- `smc_id` and `base_revision`;
- JSON Patch operations restricted to `/canvas/**` and optional `/display_name`;
- rationale;
- evidence references, if any;
- proposer actor type and ID;
- `created_at`.

An AI or Hermes proposer is permitted. Activation is not.

For revision >1, `amendment_decision` requires:

- `decision_event_id`;
- `actor_type: parent_guardian`;
- pseudonymous `actor_id`;
- `action: approve_smc_amendment`;
- `proposal_id` and exact `base_revision`;
- `decided_at`;
- canonical proposed-patch hash.

The decision must validate under the locked approval-event contract. A stale base revision, changed patch hash, AI actor, replay conflict, or absent decision blocks activation. The previous active revision becomes superseded only after the new revision is durably recorded.

## Stable issue codes

| Code | Severity | Meaning |
|---|---|---|
| `SMC_UNKNOWN_SECTION` | blocking | Heading is not in the template mapping. |
| `SMC_UNKNOWN_FIELD` | blocking | Label is not recognized in its section. |
| `SMC_DUPLICATE_SECTION` | blocking | A mapped section appears more than once. |
| `SMC_DUPLICATE_FIELD` | blocking | A mapped field appears more than once. |
| `SMC_INVALID_VALUE` | blocking | Value violates type/vocabulary rules. |
| `SMC_REQUIRED_VALUE_MISSING` | blocking for activation | Critical field is null. |
| `SMC_PLACEHOLDER_NORMALIZED` | warning | Untouched placeholder became null. |
| `SMC_STALE_BASE_REVISION` | blocking | Amendment does not target current active revision. |
| `SMC_AMENDMENT_AUTHORITY_INVALID` | blocking | Activating actor/action is not valid parent authority. |
| `SMC_AMENDMENT_HASH_MISMATCH` | blocking | Approved patch differs from applied patch. |

Issues sort by JSON path, then code.

## Acceptance criteria

1. Every field in the current Markdown template maps exactly once.
2. Unknown, missing, null, empty, and explicit-none values remain distinguishable.
3. Two equivalent Markdown inputs normalize to byte-identical canonical semantic payloads.
4. No learner display name participates in identity or durable linkage.
5. No preference becomes a diagnosis or mastery claim.
6. Only parent authority can activate revision 1 or an amendment.
7. AI proposals cannot mutate an active SMC.
8. Stale revision and changed-patch approval mutations are rejected.
9. Raw sensitive SMC values never appear in logs or build receipts.
