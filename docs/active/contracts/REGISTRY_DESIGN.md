# Contract Registry Wire Contract

Status: C3.7A MACHINE-TESTABLE CONTRACT LOCK; IMPLEMENTATION BACKLOG

Registry contract identity: `ucc.contract_registry.v1.0.0`

Registry `$id`: `urn:ucc:contract:contract-registry:1.0.0`

The registry is a deterministic local manifest. It never resolves a network URL, searches the filesystem, guesses a filename, scans imports, or reads private data.

## 1. Closed top-level envelope

The JSON document contains exactly one root member named `ucc_contract_registry`. Its value is a registry envelope with these fields:

| Field | Type | Required | Rule |
|---|---|---|---|
| `registry_schema_version` | string | yes | Exactly `ucc.contract_registry.v1.0.0`. |
| `registry_id` | string | yes | `reg_` plus an uppercase 26-character Crockford ULID. |
| `generated_at` | string | yes | RFC 3339 UTC with milliseconds; injected clock. |
| `approved_at` | string | yes | Same timestamp format; not earlier than `generated_at`; injected/fixed. |
| `canonicalization_id` | string | yes | Exactly `rfc8785-jcs-v1`. |
| `families` | object | yes | Exactly the five family keys listed below for registry schema v1. |
| `extensions` | object | no | Namespaced inert extension values; rules below. |

Unknown root members or registry-envelope members are invalid. Missing and null are distinct; none of the required envelope fields is nullable.

The exact v1 family keys are:

- `smc`;
- `assessment_receipt`;
- `receipt_pairing`;
- `proposal_approval`;
- `parent_brief_ledger`.

Adding a family key requires a compatible registry-schema minor release. Removing or changing a family meaning requires a registry-schema major release.

## 2. Family object

Each `families.<key>` value is a closed object:

| Field | Type | Required | Rule |
|---|---|---|---|
| `family_id` | string | yes | Must exactly equal its containing family key. |
| `versions` | array | yes | Non-empty; version records sorted by contract name then semantic version; no duplicate `version`. |
| `extensions` | object | no | Namespaced and resolution-inert. |

The only permitted family-object members are `family_id`, `versions`, and `extensions`.

## 3. Version record

Every member of `versions` is a closed object with exactly these required fields plus optional `extensions`:

| Field | Type | Nullable | Rule |
|---|---|---|---|
| `version` | string | no | Exact wire version `ucc.<contract_name>.v<major>.<minor>.<patch>`. |
| `lifecycle_state` | string | no | One of the five lifecycle values below. |
| `schema_ref` | object or null | yes | `null` only for `draft`; required otherwise. |
| `contract_ref` | object | no | Normative contract artifact reference. |
| `canonical_hash` | string or null | yes | `null` only for `draft`; otherwise exact lowercase SHA-256 of the version resolution projection. |
| `semantic_validator_ref` | object or null | yes | Required for `active`; null permitted for `draft`/`locked` while implementation is test-gated. |
| `semantic_projection_ref` | object or null | yes | Registered display-field projection, or null when no projection applies. |
| `introduced_at` | string | no | Injected/fixed RFC 3339 UTC milliseconds. |
| `replaces` | string or null | yes | Exact earlier wire version in the same family, or null. |
| `compatible_with` | object | no | Explicit reader/writer rules; prose is invalid. |
| `migration` | object | no | Explicit migration requirement and adapter list. |
| `fixture_sets` | array | no | Exact fixture-set objects. Locked/active records require all four purposes. |
| `approval_ref` | object or null | yes | `null` only for `draft`; required otherwise. |
| `extensions` | object | yes | Optional, namespaced, resolution-inert. |

Unknown version members are `REGISTRY_UNKNOWN_FIELD`. A non-draft record missing `schema_ref`, `canonical_hash`, or `approval_ref` is invalid even when its lifecycle is non-resolvable.

### Schema reference

`schema_ref` is null or a closed object with all fields required:

```json
{
  "schema_id": "urn:ucc:contract:smc:1.0.0",
  "path": "schemas/smc.schema.json",
  "artifact_sha256": "64 lowercase hexadecimal characters"
}
```

`schema_id` is an absolute registered `urn:ucc:contract:` URN. `path` is a normalized forward-slash relative path contained by the staging root: no drive, UNC form, leading slash, empty segment, `.` or `..`. Unknown members are rejected.

### Contract artifact reference

`contract_ref` is a closed object:

| Field | Type | Required | Rule |
|---|---|---|---|
| `path` | string | yes | Contained normalized relative path. |
| `media_type` | string | yes | `application/json` or `text/markdown`. |
| `artifact_sha256` | string | yes | SHA-256 of exact artifact bytes. Markdown bytes are UTF-8 with repository line endings normalized to LF before hashing. |
| `canonical_excerpt` | object or null | yes | Optional normative Markdown excerpt; null when the whole artifact is normative. |

A non-null `canonical_excerpt` is exactly:

```json
{
  "selector": "stable section heading or fragment identifier",
  "excerpt_sha256": "64 lowercase hexadecimal characters"
}
```

The excerpt hash is SHA-256 over UTF-8 NFC text with LF line endings and one terminal LF. It supplements and never replaces `artifact_sha256`.

### Semantic validator and projection references

A non-null `semantic_validator_ref` contains exactly `validator_version`, `entry_point`, `source_path`, and `source_sha256`. `entry_point` is a dotted local import path plus callable name; `source_path` is a contained relative Python path. An `active` record must have this reference. A `locked` record may keep it null only for `purpose: test` or `contract_lock_validation`; it cannot be activated until populated and hash-verified.

A non-null `semantic_projection_ref` contains exactly `projection_id`, `source_path`, and `source_sha256`. It is required when any display-only field is excluded from semantic hashing and null otherwise. Unknown members are rejected.

## 4. Lifecycle and resolution

Lifecycle values are exactly:

- `draft`;
- `locked`;
- `active`;
- `deprecated`;
- `retired`.

Unknown values are invalid with `REGISTRY_LIFECYCLE_UNKNOWN`.

| State | Normal runtime resolution | Contract/test resolution |
|---|---|---|
| `active` | allowed | allowed |
| `locked` | denied | allowed only when request sets `allow_locked: true` and `purpose` is `test` or `contract_lock_validation` |
| `draft` | denied | denied |
| `deprecated` | denied | denied; caller may receive replacement metadata only |
| `retired` | denied | denied |

There is at most one `active` version for one exact contract name and major version. Locked records do not become active implicitly. Deprecated/retired records remain hash-verifiable audit records but are never returned as resolvable contracts.

## 5. Compatibility rules

`compatible_with` is a closed object with three required members:

```json
{
  "readers": [
    {
      "consumer_version": "ucc.smc.v1.0.0",
      "accepted_versions": ["ucc.smc.v1.0.0"]
    }
  ],
  "writers": [
    {
      "producer_version": "ucc.smc.v1.0.0",
      "emitted_version": "ucc.smc.v1.0.0"
    }
  ],
  "unknown_version_behavior": "reject"
}
```

Rules:

- `readers` and `writers` are arrays; draft records may use empty arrays.
- Each reader object contains exactly `consumer_version` and a sorted, unique, non-empty `accepted_versions` array of exact wire versions.
- Each writer object contains exactly `producer_version` and `emitted_version`, both exact wire versions.
- `unknown_version_behavior` is exactly `reject`.
- Prose strings, ranges, wildcards, inequalities, implied SemVer compatibility, and network negotiation are invalid.
- Locked/active records must include a self-reader and self-writer rule.

## 6. Migration object

`migration` is a closed object:

```json
{
  "required": false,
  "adapters": []
}
```

When adapters exist, each is a closed object with:

| Field | Type | Rule |
|---|---|---|
| `adapter_id` | string | Stable non-empty ID. |
| `adapter_version` | string | Exact semantic version. |
| `source_version` | string | Exact registered wire version. |
| `target_version` | string | Exact registered wire version. |
| `implementation_ref` | artifact reference or null | Null only while target is `draft` or `locked`; active migration requires a verified local artifact. |
| `loss_policy` | string | `lossless`, `declared_loss`, or `blocking`. |

If `replaces` is non-null, `migration.required` is true and exactly one adapter must map that replaced version to the current version. Other adapters may exist but `(adapter_id, adapter_version)` is unique registry-wide. A migration is never automatic: resolution returns `MIGRATION_REQUIRED` with the exact adapter identity; an explicit migration request verifies source/target versions and adapter hash before execution.

## 7. Fixture-set representation

Every fixture-set object is closed and contains exactly:

```json
{
  "fixture_set_id": "smc-v1-positive",
  "path": "fixtures/contracts/smc/v1/positive",
  "purpose": "positive",
  "expected_hash": "64 lowercase hexadecimal characters",
  "coverage_labels": ["shape", "canonicalization"]
}
```

Rules:

- `fixture_set_id` is non-empty and unique registry-wide.
- `path` uses the contained relative-path rule.
- `purpose` is exactly `positive`, `negative`, `compatibility`, or `mutation`.
- `expected_hash` is SHA-256 over a canonical fixture manifest, not a directory enumeration supplied by the operating system.
- `coverage_labels` is a sorted, unique, non-empty array of stable lowercase tokens matching `^[a-z0-9][a-z0-9_-]*$`.
- Locked/active versions contain exactly one fixture set for each of the four purposes. Draft may use zero or more; deprecated/retired retain their last valid sets.

The canonical fixture manifest is an array sorted by relative path. Each item is `{"path": <relative path>, "sha256": <exact file-byte hash>}`. `expected_hash` is SHA-256 over RFC 8785 canonical JSON bytes of that array.

## 8. Approval reference

`approval_ref` is null or a closed object:

```json
{
  "actor_role": "contract_authority",
  "approval_event_id": null,
  "decision_id": "dec_01J00000000000000000000000",
  "timestamp": "2026-06-30T00:00:00.000Z",
  "source_document": "docs/active/contracts/LOCK_AUDIT.md",
  "scope": {
    "family_id": "smc",
    "version": "ucc.smc.v1.0.0",
    "decision": "contract_lock"
  }
}
```

Rules:

- `actor_role` is `contract_authority` or `product_owner`.
- Exactly one of `approval_event_id` and `decision_id` is non-null. IDs use their documented prefix plus ULID.
- `timestamp` uses the common injected/fixed timestamp convention.
- `source_document` is a contained repository-relative Markdown path.
- `scope` contains exactly `family_id`, `version`, and `decision`; decision is `contract_lock`, `activate`, `deprecate`, or `retire`.
- Scope family/version must equal the containing record.

## 9. Extensions

Any closed registry object may include the single optional member `extensions`. It is an object whose keys match a reverse-domain namespace pattern such as `org.example.feature`; values are I-JSON values. Unnamespaced keys are invalid.

Extensions are included in the external full-registry snapshot hash but are removed from the deterministic resolution projection. Resolvers do not branch, select, approve, migrate, or alter compatibility based on extensions. Promoting extension meaning into resolution requires a registry-schema version change.

## 10. Canonical JSON and hashes

All JSON obeys I-JSON and `rfc8785-jcs-v1`. Duplicate keys, NaN, Infinity, invalid Unicode, and non-interoperable numbers are invalid.

Three hash layers are distinct:

1. `artifact_sha256` hashes exact referenced bytes under the artifact-specific rule.
2. Version `canonical_hash` hashes RFC 8785 bytes of this exact projection:

```json
{
  "version": "<version>",
  "schema_id": "<schema_ref.schema_id>",
  "schema_artifact_sha256": "<schema_ref.artifact_sha256>",
  "contract_artifact_sha256": "<contract_ref.artifact_sha256>",
  "canonical_excerpt_sha256": "<contract_ref.canonical_excerpt.excerpt_sha256 or null>",
  "semantic_validator_sha256": "<semantic_validator_ref.source_sha256 or null>",
  "semantic_projection_sha256": "<semantic_projection_ref.source_sha256 or null>",
  "canonicalization_id": "<top-level canonicalization_id>"
}
```

3. The registry snapshot hash is external to avoid self-reference: SHA-256 over RFC 8785 bytes of the complete root JSON, including extensions. Callers supply the expected snapshot hash and resolution fails if it differs.

Lowercase 64-hex is mandatory. No field contains a `sha256:` prefix.

## 11. Deterministic resolution and version behavior

Resolution inputs are `registry JSON`, expected snapshot hash, `family_id`, exact `version`, `purpose`, and `allow_locked`.

The resolver:

1. rejects JSON/schema/unknown-field errors;
2. verifies the external registry snapshot hash;
3. finds the exact family key and requires `family_id` equality;
4. finds exactly one record by exact wire version;
5. validates lifecycle eligibility for the request;
6. verifies `schema_ref`, contract artifact, canonical excerpt when present, and version `canonical_hash`;
7. verifies approval scope and fixture-set hashes;
8. applies only explicit compatibility rules;
9. returns immutable local references and hashes.

Unknown contract/version, unknown major/minor/patch, absent record, or absent explicit compatibility fails closed. Filename guesses and “latest” selection are forbidden. Deprecated records may name `replaces` only as history; callers use an explicit active target and registered adapter. Adapters never fabricate identity, evidence, approval, mastery, form metadata, or other missing truth.

## 12. Stable validation issue codes

Issues sort by JSON Pointer path, code, then stable family/version/fixture ID. They contain paths, IDs, versions, and hashes only.

| Code | Condition |
|---|---|
| `REGISTRY_SCHEMA_INVALID` | Root/type/required-field violation. |
| `REGISTRY_UNKNOWN_FIELD` | Member outside the closed shape and `extensions`. |
| `REGISTRY_EXTENSION_NAMESPACE_INVALID` | Extension key is not namespaced. |
| `REGISTRY_FAMILY_ID_MISSING` | Family object lacks `family_id`. |
| `REGISTRY_FAMILY_ID_MISMATCH` | Family ID differs from containing key. |
| `REGISTRY_FAMILY_UNKNOWN` | Family key unsupported by this registry schema version. |
| `REGISTRY_DUPLICATE_VERSION` | Duplicate exact version in a family. |
| `REGISTRY_DUPLICATE_ID` | Duplicate registry, adapter, fixture, approval, or schema ID where uniqueness is required. |
| `REGISTRY_PATH_INVALID` | Absolute, escaping, or non-normalized path. |
| `REGISTRY_HASH_MISMATCH` | External snapshot or artifact hash mismatch. |
| `REGISTRY_CANONICAL_HASH_MISMATCH` | Version projection does not match `canonical_hash`. |
| `REGISTRY_REF_UNRESOLVED` | Local schema/contract/excerpt reference is missing. |
| `REGISTRY_VERSION_UNSUPPORTED` | Exact family/version record is absent. |
| `REGISTRY_LIFECYCLE_UNKNOWN` | Lifecycle value is outside the five-value enum. |
| `REGISTRY_LIFECYCLE_UNUSABLE` | Known lifecycle is not resolvable for the request. |
| `REGISTRY_COMPATIBILITY_INVALID` | Compatibility is prose, wildcard/range based, malformed, or incomplete. |
| `REGISTRY_FIXTURE_SET_INVALID` | Fixture set is malformed, incomplete, duplicated, or missing a required purpose. |
| `REGISTRY_FIXTURE_HASH_MISMATCH` | Canonical fixture manifest hash differs. |
| `REGISTRY_APPROVAL_REF_INVALID` | Actor, ID choice, timestamp, source, or scope is missing/mismatched. |
| `REGISTRY_VALIDATOR_MISMATCH` | Registered semantic validator identity/hash differs when one is introduced by a registry-schema minor. |
| `MIGRATION_ADAPTER_UNAVAILABLE` | Required exact adapter is absent or non-executable. |
| `MIGRATION_REQUIRED` | Exact version exists but explicit migration is required before target use. |
| `MIGRATION_REQUIRED_TRUTH_MISSING` | Migration would need invented truth. |
| `MIGRATION_LOSS_UNDECLARED` | Observed loss contradicts adapter loss policy. |
| `MIGRATION_OUTPUT_INVALID` | Target output fails registered validation. |

## 13. Complete positive example

This is a complete wire-valid registry example. Artifact and fixture hashes denote a synthetic artifact map supplied by T4.1; it is not a production release inventory. Draft records demonstrate required fields with explicitly permitted null/empty values.

```json
{
  "ucc_contract_registry": {
    "registry_schema_version": "ucc.contract_registry.v1.0.0",
    "registry_id": "reg_01J00000000000000000000000",
    "generated_at": "2026-06-30T00:00:00.000Z",
    "approved_at": "2026-06-30T00:00:00.000Z",
    "canonicalization_id": "rfc8785-jcs-v1",
    "families": {
      "smc": {
        "family_id": "smc",
        "versions": [{
          "version": "ucc.smc.v1.0.0",
          "lifecycle_state": "locked",
          "schema_ref": {"schema_id": "urn:ucc:contract:smc:1.0.0", "path": "schemas/smc.schema.json", "artifact_sha256": "1111111111111111111111111111111111111111111111111111111111111111"},
          "contract_ref": {"path": "docs/active/contracts/SMC_CONTRACT.md", "media_type": "text/markdown", "artifact_sha256": "2222222222222222222222222222222222222222222222222222222222222222", "canonical_excerpt": null},
          "canonical_hash": "1c42944213233e21a915e549b6ebbc2c96a67094b3ab1ae1a8be185cdbaa97a4",
          "semantic_validator_ref": null,
          "semantic_projection_ref": null,
          "introduced_at": "2026-06-30T00:00:00.000Z",
          "replaces": null,
          "compatible_with": {"readers": [{"consumer_version": "ucc.smc.v1.0.0", "accepted_versions": ["ucc.smc.v1.0.0"]}], "writers": [{"producer_version": "ucc.smc.v1.0.0", "emitted_version": "ucc.smc.v1.0.0"}], "unknown_version_behavior": "reject"},
          "migration": {"required": false, "adapters": []},
          "fixture_sets": [
            {"fixture_set_id": "smc-v1-compatibility", "path": "fixtures/contracts/smc/v1/compatibility", "purpose": "compatibility", "expected_hash": "4444444444444444444444444444444444444444444444444444444444444444", "coverage_labels": ["exact_version"]},
            {"fixture_set_id": "smc-v1-mutation", "path": "fixtures/contracts/smc/v1/mutation", "purpose": "mutation", "expected_hash": "5555555555555555555555555555555555555555555555555555555555555555", "coverage_labels": ["hash_mutation"]},
            {"fixture_set_id": "smc-v1-negative", "path": "fixtures/contracts/smc/v1/negative", "purpose": "negative", "expected_hash": "6666666666666666666666666666666666666666666666666666666666666666", "coverage_labels": ["closed_shape"]},
            {"fixture_set_id": "smc-v1-positive", "path": "fixtures/contracts/smc/v1/positive", "purpose": "positive", "expected_hash": "7777777777777777777777777777777777777777777777777777777777777777", "coverage_labels": ["canonicalization", "shape"]}
          ],
          "approval_ref": {"actor_role": "contract_authority", "approval_event_id": null, "decision_id": "dec_01J00000000000000000000000", "timestamp": "2026-06-30T00:00:00.000Z", "source_document": "docs/active/contracts/LOCK_AUDIT.md", "scope": {"family_id": "smc", "version": "ucc.smc.v1.0.0", "decision": "contract_lock"}}
        }]
      },
      "assessment_receipt": {
        "family_id": "assessment_receipt",
        "versions": [{"version": "ucc.assessment_receipt.v2.0.0", "lifecycle_state": "draft", "schema_ref": null, "contract_ref": {"path": "docs/active/contracts/RECEIPT_CONTRACT.md", "media_type": "text/markdown", "artifact_sha256": "8888888888888888888888888888888888888888888888888888888888888888", "canonical_excerpt": null}, "canonical_hash": null, "semantic_validator_ref": null, "semantic_projection_ref": null, "introduced_at": "2026-06-30T00:00:00.000Z", "replaces": null, "compatible_with": {"readers": [], "writers": [], "unknown_version_behavior": "reject"}, "migration": {"required": false, "adapters": []}, "fixture_sets": [], "approval_ref": null}
        ]
      },
      "receipt_pairing": {
        "family_id": "receipt_pairing",
        "versions": [{"version": "ucc.receipt_pairing.v1.0.0", "lifecycle_state": "draft", "schema_ref": null, "contract_ref": {"path": "docs/active/contracts/PAIRING_CONTRACT.md", "media_type": "text/markdown", "artifact_sha256": "9999999999999999999999999999999999999999999999999999999999999999", "canonical_excerpt": null}, "canonical_hash": null, "semantic_validator_ref": null, "semantic_projection_ref": null, "introduced_at": "2026-06-30T00:00:00.000Z", "replaces": null, "compatible_with": {"readers": [], "writers": [], "unknown_version_behavior": "reject"}, "migration": {"required": false, "adapters": []}, "fixture_sets": [], "approval_ref": null}]
      },
      "proposal_approval": {
        "family_id": "proposal_approval",
        "versions": [{"version": "ucc.task_proposal.v1.0.0", "lifecycle_state": "draft", "schema_ref": null, "contract_ref": {"path": "docs/active/contracts/APPROVAL_CONTRACT.md", "media_type": "text/markdown", "artifact_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "canonical_excerpt": null}, "canonical_hash": null, "semantic_validator_ref": null, "semantic_projection_ref": null, "introduced_at": "2026-06-30T00:00:00.000Z", "replaces": null, "compatible_with": {"readers": [], "writers": [], "unknown_version_behavior": "reject"}, "migration": {"required": false, "adapters": []}, "fixture_sets": [], "approval_ref": null}]
      },
      "parent_brief_ledger": {
        "family_id": "parent_brief_ledger",
        "versions": [{"version": "ucc.parent_brief.v1.0.0", "lifecycle_state": "draft", "schema_ref": null, "contract_ref": {"path": "docs/active/contracts/BRIEF_LEDGER_CONTRACT.md", "media_type": "text/markdown", "artifact_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "canonical_excerpt": null}, "canonical_hash": null, "semantic_validator_ref": null, "semantic_projection_ref": null, "introduced_at": "2026-06-30T00:00:00.000Z", "replaces": null, "compatible_with": {"readers": [], "writers": [], "unknown_version_behavior": "reject"}, "migration": {"required": false, "adapters": []}, "fixture_sets": [], "approval_ref": null}]
      }
    }
  }
}
```

## 14. Negative examples for T4.1

Each example is an RFC 6902-style mutation applied independently to the positive example. T4.1 fixtures must materialize the resulting complete JSON document and assert the exact primary issue code.

| Fixture ID | Mutation | Primary issue |
|---|---|---|
| `registry-missing-family-id` | `remove /ucc_contract_registry/families/smc/family_id` | `REGISTRY_FAMILY_ID_MISSING` |
| `registry-unknown-lifecycle` | `replace /ucc_contract_registry/families/smc/versions/0/lifecycle_state` with `"experimental"` | `REGISTRY_LIFECYCLE_UNKNOWN` |
| `registry-active-missing-schema-ref` | replace lifecycle with `active`; remove `schema_ref` | `REGISTRY_SCHEMA_INVALID` |
| `registry-active-missing-canonical-hash` | replace lifecycle with `active`; remove `canonical_hash` | `REGISTRY_SCHEMA_INVALID` |
| `registry-compatibility-prose` | replace `compatible_with` with `"same major versions are compatible"` | `REGISTRY_COMPATIBILITY_INVALID` |
| `registry-fixture-missing-hash` | remove `/ucc_contract_registry/families/smc/versions/0/fixture_sets/0/expected_hash` | `REGISTRY_FIXTURE_SET_INVALID` |
| `registry-approval-missing-actor` | remove `approval_ref.actor_role` | `REGISTRY_APPROVAL_REF_INVALID` |
| `registry-approval-missing-scope` | remove `approval_ref.scope` | `REGISTRY_APPROVAL_REF_INVALID` |

For multiple simultaneous faults, issues are all returned in deterministic sort order. The “primary issue” above is the first issue for that single-mutation fixture, not an early-exit license.

## 15. Locked specification inventory

The registry schema can hold these exact contract versions; the example above is intentionally smaller than the eventual production inventory:

| Contract | Locked wire version |
|---|---|
| SMC | `ucc.smc.v1.0.0` |
| Assessment receipt | `ucc.assessment_receipt.v2.0.0` |
| Receipt pairing | `ucc.receipt_pairing.v1.0.0` |
| Task proposal | `ucc.task_proposal.v1.0.0` |
| Approval event | `ucc.approval_event.v1.0.0` |
| Approval transition | `ucc.approval_transition.v1.0.0` |
| Parent brief | `ucc.parent_brief.v1.0.0` |
| Ledger entry | `ucc.ledger_entry.v1.0.0` |
| Ledger file | `ucc.ledger_file.v1.0.0` |

“Locked” freezes field semantics for RED authoring. It does not claim schemas, registry code, validators, migrations, or product behavior exist.
