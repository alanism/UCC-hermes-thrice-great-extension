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

---

# C3.5A Proposal/Approval Wire Lock Addendum

Status: PASS

The prior C3.5 authority and transition semantics remained sound, but nested proposal fields were not machine-testable enough for a provably valid T4.4 fixture. C3.5A now fixes:

- closed `ucc_parent_proposal` and `ucc_parent_approval_event` envelopes;
- exact proposal, evidence-reference, SMC-reference, authorship, rationale, payload, event actor, scope, and provenance fields/types;
- author-writable versus evaluator-derived proposal statuses;
- exact approval actions and human actor roles;
- proposal/event canonical hash projections;
- injected event/key rules and namespace-global binding;
- identical replay, changed-payload conflict, and R1-to-R2 key conflict;
- namespaced resolution-inert extensions and unknown-field rejection;
- deterministic issue codes and twelve negative mutations.

Both complete positive examples parse as JSON, all prefixed IDs carry 26-character ULIDs, the approval event references the exact proposal hash, and both canonical hashes recompute from their documented projections.

T4.4 may now materialize these examples and mutations without inventing proposal evidence, SMC, authorship, rationale, actor, scope, replay, or conflict semantics. No schema, evaluator, test, fixture file, runtime, or product behavior was implemented by C3.5A.

---

# C3.6A Ledger Wire Lock Addendum

Status: PASS

The prior C3.6 contract fixed ledger intent but left the file root, entry types, nested references, and hash projections too open for valid T4.5 fixtures. C3.6A fixes closed ledger/entry envelopes; exact payload, source, approval, brief, retention, deletion, and tombstone fields; seven entry types; injected identity/order/replay rules; JCS hash projections; atomic fault outcomes; deletion-request-before-tombstone compaction; namespaced inert extensions; stable issue codes; and complete positive/negative examples.

Both JSON example blocks parse. Approval, transition, tombstone, and full-ledger hashes recompute exactly. T4.5 can now distinguish absent implementation from malformed fixtures or prose interpretation. No test, fixture file, schema, ledger runtime, plugin, product behavior, learner data, model, network, messaging, adapter, or Hermes source was created or changed.
