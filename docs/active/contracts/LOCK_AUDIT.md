# C3.7A Registry Wire Lock Audit

Status: PASS

Date: 2026-06-30

## Gap repaired

The prior C3.7 registry design fixed registry semantics but did not fix the exact top-level envelope or several nested representations. T4.1 therefore could not distinguish a valid fixture from an agent-invented wire format. C3.7A repairs only that gap; it does not change receipt, pairing, approval, brief, ledger, privacy, or product behavior.

## Machine-testable decisions

- root is exactly `ucc_contract_registry`;
- registry schema/version/ID/clock/canonicalization fields are exact and closed;
- five family keys and key-to-`family_id` equality are exact;
- version fields, nullable states, and unknown-field rejection are exact;
- schema, Markdown contract, validator, and projection references have exact shapes;
- compatibility is explicit exact-version reader/writer objects, never prose/ranges;
- migration objects and explicit adapter selection are exact;
- fixture-set IDs, purposes, paths, canonical manifests, hashes, and coverage labels are exact;
- approval actor, mutually exclusive event/decision ID, clock, source, and scope are exact;
- lifecycle states and request-dependent resolution are exact;
- artifact, version-projection, and external registry snapshot hashes are distinct;
- extension namespacing and resolution-inert behavior are exact;
- deterministic resolution order and stable issue codes are fixed.

## Example audit

The positive example is valid JSON, contains all five v1 families, uses a valid registry/decision ULID, and carries a recomputed SMC version projection hash. Draft records demonstrate the only permitted null/empty states without claiming implementation exists.

Eight independent negative mutations cover missing/mismatched identity, unknown lifecycle, missing active references/hashes, prose compatibility, missing fixture hash, and incomplete approval actor/scope. Each names its deterministic primary issue code.

## T4.1 readiness

T4.1 may now materialize the documented positive example plus its synthetic artifact map, then apply the documented negative mutations. A failure caused by absent registry/schema implementation is distinguishable from malformed fixtures or unresolved contract interpretation.

No schema, validator, registry runtime, fixture file, test, plugin, or product behavior was implemented by C3.7A.
