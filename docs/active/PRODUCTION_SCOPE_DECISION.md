# Production Optional-Adapter Scope Decision

Status: PENDING HUMAN DECISION

Task: C3.8

## Decision required

Choose exactly one value for `I1_MOCK_ADAPTERS`:

### EXCLUDE

- T4.11 remains unclaimed and is excluded from T1/F1.
- Phase 10 remains out of the production acceptance dependency chain.
- Core contracts still prohibit live network/messaging integrations.
- Future mock/live adapter work requires a separately authorized scope revision.

### INCLUDE

- T4.11 becomes claimable only after R4.5.
- Phase 10 becomes required for F1 after the offline synthetic core passes E1.
- Work remains deterministic, synthetic, captured locally, and zero-network.
- Inclusion does not authorize live Discord, Campaign OS, messaging, model, or network actions.

## Recommendation

EXCLUDE is the narrower production-core path and avoids making nonessential adapter simulation a release blocker. INCLUDE is appropriate only if adapter-boundary fault behavior must be part of this release's acceptance evidence.

## Required human response

Reply with `I1_MOCK_ADAPTERS = INCLUDE` or `I1_MOCK_ADAPTERS = EXCLUDE`.

No default is inferred from silence or from the prohibition on live integrations.
