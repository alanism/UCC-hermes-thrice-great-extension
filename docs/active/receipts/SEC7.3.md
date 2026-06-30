# Receipt: SEC7.3

Agent: `codex-sec7-green-01`

Completed: `2026-06-30T19:32:52Z`

## Result

PASS. The local guard surface now enforces pseudonymous learner IDs, deterministic hold-aware retention decisions, deletion planning without in-place erasure, content-free audit tombstones, and commit ineligibility for private/generated paths.

## Evidence

- Initial focused RED: 10 expected failures because retention, commit-eligibility, and mutation functions did not exist; the synthetic-fixture assertion passed after replacing one non-synthetic profile label.
- Full T4.6 privacy suite: 35 passed in 0.29 seconds.
- Pseudonym guard accepts `lrn_<ULID>` and rejects malformed IDs and direct identity fields.
- Deletion guard fails closed on active holds, requires target/audit binding, returns an atomic three-action plan, and never authorizes in-place erasure.
- Tombstones reject learner IDs and other private payload fields while retaining only audit hashes.
- Commit guard rejects `outputs/`, `learner_data/`, `local/`, secret-shaped files, and all non-synthetic inputs; the human-owned staged-data checker independently matches those decisions.
- Mutation probe: six behavior-changing controls KILLED; equivalent normalization-order control SURVIVED; crash/setup/timeout classified ERROR.
- Actual distribution restriction canary: 2 passed in 6.28 seconds with zero final tools, plugins, MCP servers, or network attempts.

No learner ledger, product deletion engine, model, network, messaging, adapter, or Hermes source behavior was implemented or invoked.

## Gate

SEC1 PASS for local synthetic workflows. This receipt does not authorize real or semi-real learner data.

## Next task

U8.1 is dependency-ready under the task graph but requires its own Phase 8 authorization.
