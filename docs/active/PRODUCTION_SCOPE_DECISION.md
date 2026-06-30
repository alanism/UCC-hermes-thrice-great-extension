# Production Optional-Adapter Scope Decision

Status: DECIDED — EXCLUDE

Task: C3.8

## Human decision

`I1_MOCK_ADAPTERS = EXCLUDE`

Received from the human owner on 2026-06-30.

### Applied consequences

- T4.11 remains unclaimed and is excluded from T1/F1.
- Phase 10 remains out of the production acceptance dependency chain.
- Core contracts still prohibit live network/messaging integrations.
- Future mock/live adapter work requires a separately authorized scope revision.

### Rejected alternative: INCLUDE

- T4.11 becomes claimable only after R4.5.
- Phase 10 becomes required for F1 after the offline synthetic core passes E1.
- Work remains deterministic, synthetic, captured locally, and zero-network.
- Inclusion does not authorize live Discord, Campaign OS, messaging, model, or network actions.

The decision is explicit and was not inferred from the separate prohibition on live integrations.
