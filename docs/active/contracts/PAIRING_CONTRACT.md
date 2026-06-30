# Receipt Pairing and Pressure-Delta Contract

Status: SPECIFICATION LOCKED BY C3.7; SCHEMA/EVALUATOR TEST-GATED

Contract name: `ucc.receipt_pairing`

Initial major version: `1`

## Purpose

A pair result determines whether one CALM receipt and one PRESSURE receipt are comparable enough for a pressure-condition contrast. It does not diagnose a learner, establish mastery, or convert incomplete evidence into certainty.

The evaluator is deterministic and fail-closed. Thresholds are never guessed: every evaluation references an immutable registered pairing policy. Missing policy or form metadata makes the pair incomparable.

## Inputs

Exactly two semantically validated `ucc.assessment_receipt.v2.0.0` documents plus:

- one immutable form-comparison manifest per form revision;
- one immutable `pairing_policy`;
- a registry snapshot ID/hash;
- injected evaluator version and clock for the audit envelope.

Both receipts must carry the same non-null `paired_run_id`. More or fewer than two receipts for one run ID is invalid.

## Pair result envelope

| Field | Rule |
|---|---|
| `contract_version` | `ucc.receipt_pairing.v1.0.0`. |
| `pair_result_id` | `pres_<ULID>`; injected. |
| `paired_run_id` | Exact shared run ID from inputs. |
| `learner_id` | Exact shared pseudonymous learner ID. |
| `calm_receipt_id` | Receipt whose explicit mode is CALM. |
| `pressure_receipt_id` | Receipt whose explicit mode is PRESSURE. |
| `pairing_policy_id` | Immutable policy identity. |
| `registry_snapshot_sha256` | Registry/form/policy snapshot used. |
| `status` | `valid`, `valid_limited`, `insufficient_evidence`, `incomparable`, or `void`. |
| `comparability` | Deterministic checks and metrics below. |
| `metrics` | Present only for `valid` or `valid_limited`. |
| `issues` | Stable sorted issues with safe IDs/counts only. |
| `canonical_input_sha256` | Hash of ordered receipt hashes plus policy/registry hashes. |

## Pairing policy

The policy is immutable and contains explicit values for:

- `pairing_policy_id` and version;
- `minimum_answered_per_mode` (positive integer);
- `minimum_presented_per_mode` (positive integer, not below answered minimum);
- `minimum_answered_per_skill_per_mode` (object mapping every form skill ID to a positive integer; no missing or extra keys);
- `minimum_engagement_rate` in `[0,1]`;
- `maximum_pair_window_seconds` (positive integer);
- `maximum_presented_count_difference_ratio` in `[0,1]`;
- `maximum_skill_distribution_tvd` in `[0,1]`;
- `allowed_quality_statuses`, limited to `clean` and optionally `limited`;
- `pairing_nonblocking_warning_codes` for any allowed limited receipts;
- `allow_exact_form_reuse` boolean;
- `allow_registered_equivalent_forms` boolean;
- `required_ai_role_match` boolean, true in the initial production policy;
- `rounding_mode: half_even` and `decimal_places: 4`.

There is deliberately no undocumented global sample default. A form/policy author must choose and version the evidence floor. A missing, mutable, or contradictory policy yields `PAIR_POLICY_INVALID` and no metrics.

## Identity and mode checks

A candidate pair requires:

1. exactly one CALM receipt and one PRESSURE receipt;
2. same `paired_run_id`, `learner_id`, domain, and contract major;
3. distinct receipt IDs and session IDs;
4. both source payload hashes known and stable;
5. CALM completes before PRESSURE starts; sessions cannot overlap;
6. elapsed seconds from CALM completion to PRESSURE start not above policy maximum;
7. each receipt quality allowed by policy;
8. both completion statuses exactly `completed`.

Partial, aborted, expired, degraded, void, or suppressed receipts may be reported together for audit but cannot produce a pressure delta. Partial/aborted/expired evidence yields `insufficient_evidence`; degraded/void/suppressed input yields `void`.

## Form compatibility

Forms are compatible only by one of two explicit routes.

### Exact form

- same `assessment_form_id`;
- same `assessment_form_version`;
- policy `allow_exact_form_reuse` is true.

### Registered equivalent forms

- policy `allow_registered_equivalent_forms` is true;
- both immutable form manifests declare the same non-empty `comparison_family_id`;
- each manifest explicitly names the other form revision as pairing-compatible;
- same domain and exact same skill-ID set;
- presented-count difference ratio is within policy;
- skill-distribution total variation distance is within policy;
- level/difficulty bands are declared equivalent by the registry.

No title, filename, duration, or coincidental skill overlap establishes equivalence.

Presented-count difference ratio:

```text
abs(calm_items_presented - pressure_items_presented)
---------------------------------------------------
max(calm_items_presented, pressure_items_presented)
```

Skill distribution uses presented-event shares. For every skill in the common skill set:

```text
p_mode(skill) = presented events for skill / all presented events in mode
TVD = 0.5 * sum(abs(p_calm(skill) - p_pressure(skill)))
```

The forms fail comparison when `TVD` exceeds policy. Skill IDs absent from either side are not tolerated; that is a skill-set mismatch, not a small distribution difference.

## Minimum evidence

Each mode independently must satisfy:

- items presented at or above policy floor;
- items answered at or above policy floor;
- engagement rate at or above policy floor;
- per-skill answered counts at or above policy floor;
- no unresolved form item;
- no duplicate/reordered event;
- complete session;
- allowed quality and warning codes only.

Failure produces `insufficient_evidence` and no delta. The evaluator never scales a partial sample up to the minimum.

If `required_ai_role_match` is true, the two receipts' sorted session AI-role sets must match. Different AI support conditions are useful observations but confound a pressure-only comparison and produce `PAIR_AI_ROLE_MISMATCH`.

## Metrics and denominators

Metrics are computed only for `valid` or `valid_limited`.

### Answered-item contrast

```text
calm_accuracy_answered = calm.correct / calm.items_answered
pressure_accuracy_answered = pressure.correct / pressure.items_answered
pressure_delta_answered = calm_accuracy_answered - pressure_accuracy_answered
```

This measures correctness among answered items and excludes timeouts/skips.

### Canonical pressure delta

```text
calm_performance_presented = calm.correct / calm.items_presented
pressure_performance_presented = pressure.correct / pressure.items_presented
pressure_delta = calm_performance_presented - pressure_performance_presented
```

The canonical `pressure_delta` uses presented items so pressure-related timeouts and skips cannot disappear from the denominator. Positive means CALM performance was higher; negative means PRESSURE performance was higher. It is a coaching signal, not a clinical diagnosis.

### Access metrics

```text
calm_timeout_rate = calm.timeouts / calm.items_presented
pressure_timeout_rate = pressure.timeouts / pressure.items_presented
timeout_rate_delta = pressure_timeout_rate - calm_timeout_rate

calm_skip_rate = calm.skipped / calm.items_presented
pressure_skip_rate = pressure.skipped / pressure.items_presented
skip_rate_delta = pressure_skip_rate - calm_skip_rate

response_time_ratio = pressure.average_response_time_ms
                      / calm.average_response_time_ms
```

`response_time_ratio` is null when either average is null or CALM average is zero.

### Per-skill metrics

For each skill, compute the same presented-item performance delta only when both modes meet the per-skill answered floor. Skills below the floor are listed in `insufficient_skill_ids` and receive no delta.

All ratios and deltas use decimal arithmetic and half-even rounding to the policy decimal places. Calculations use unrounded inputs and round once at output.

## Pair status

| Status | Rule |
|---|---|
| `valid` | Every compatibility/minimum check passes and both receipts are clean. |
| `valid_limited` | Checks pass; at least one receipt is limited only by policy-allowed warning codes. Limitations propagate. |
| `insufficient_evidence` | Identity/forms are comparable, but samples, completion, engagement, or per-skill floors fail. |
| `incomparable` | Identity, mode, order, form, skill, policy, timing, or AI-role comparison fails. |
| `void` | Any input is degraded/void/suppressed or has an untrusted canonical hash. |

No metrics appear for the last three statuses.

## Stable issue codes

| Code | Status class | Condition |
|---|---|---|
| `PAIR_COUNT_INVALID` | incomparable | Run ID does not bind exactly two receipts. |
| `PAIR_RUN_ID_MISMATCH` | incomparable | Non-null run IDs differ. |
| `PAIR_MODE_SET_INVALID` | incomparable | Not exactly one CALM and one PRESSURE. |
| `PAIR_LEARNER_MISMATCH` | incomparable | Learner IDs differ. |
| `PAIR_DOMAIN_MISMATCH` | incomparable | Domains differ. |
| `PAIR_RECEIPT_ID_COLLISION` | incomparable | Receipt/session identity collides. |
| `PAIR_ORDER_INVALID` | incomparable | CALM is not completed before PRESSURE begins. |
| `PAIR_WINDOW_EXCEEDED` | incomparable | Policy time window exceeded. |
| `PAIR_POLICY_INVALID` | incomparable | Policy absent, mutable, or internally inconsistent. |
| `PAIR_FORM_MISMATCH` | incomparable | Neither exact nor registered-equivalent route passes. |
| `PAIR_SKILL_SET_MISMATCH` | incomparable | Skill sets differ. |
| `PAIR_SKILL_DISTRIBUTION_EXCEEDED` | incomparable | TVD exceeds policy. |
| `PAIR_ITEM_COUNT_TOLERANCE_EXCEEDED` | incomparable | Presented-count ratio exceeds policy. |
| `PAIR_AI_ROLE_MISMATCH` | incomparable | Declared support condition differs under required matching. |
| `PAIR_PARTIAL_SESSION` | insufficient | Either completion status is not completed. |
| `PAIR_MINIMUM_PRESENTED_NOT_MET` | insufficient | Presented floor fails. |
| `PAIR_MINIMUM_ANSWERED_NOT_MET` | insufficient | Answered floor fails. |
| `PAIR_MINIMUM_SKILL_EVIDENCE_NOT_MET` | insufficient | Per-skill floor fails. |
| `PAIR_MINIMUM_ENGAGEMENT_NOT_MET` | insufficient | Engagement floor fails. |
| `PAIR_RECEIPT_WARNING_NOT_ALLOWED` | insufficient | Limited warning is not policy-allowed. |
| `PAIR_INPUT_QUALITY_UNUSABLE` | void | Input is degraded, void, or suppressed. |

Issues sort by code, then receipt ID, then skill ID. They contain no raw answers or learner names.

## Interpretation boundary

Allowed deterministic statements:

- the measured deltas and rates;
- whether the pair met its registered comparability policy;
- which evidence floor failed;
- that performance differed under the two declared conditions.

Forbidden conclusions from a pair alone:

- mastery or lack of mastery;
- anxiety, disability, attention disorder, or other clinical state;
- cheating, ghostwriting, AI misuse, or motivation;
- a causal claim that pressure alone produced the difference.

## Acceptance criteria

1. Reversing modes/order, changing learner/form/skill identity, or reusing a run ID with extra receipts fails.
2. Exact and equivalent-form routes are independently testable.
3. Skill TVD and item-count tolerance have fixed formulas and policy values.
4. Partial/degraded/void/suppressed receipts never produce deltas.
5. Missing sample policy never falls back to an assumed threshold.
6. Timeouts/skips affect canonical presented-item delta and remain separately visible.
7. Answered-item and presented-item metrics cannot be confused by name.
8. Identical inputs and registry/policy snapshot produce byte-identical semantic results.
9. Pairing produces evidence comparison, not diagnosis or mastery.
