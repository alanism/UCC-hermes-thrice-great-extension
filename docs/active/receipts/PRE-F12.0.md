# Receipt: PRE-F12.0

Agent: `codex-pref12-cli-01`

ACDF task ID: `F12.0` (machine-safe normalization of the human authorization label `PRE-F12.0`)

Completed: `2026-07-01T05:21:21Z`

## Result

PASS. Installed `hermes ucc` commands now verify the installed profile, load canonical-hashed synthetic resources from the allowlisted plugin payload, run deterministic validation, reject adversarial cases with nonzero exits and stable issues, and execute the real seven-stage weekly orchestrator.

## Installed CLI behavior

- `hermes ucc doctor` verifies distribution identity, registry schema, resource-manifest hashes, and deny-all configuration.
- `hermes ucc validate --synthetic` validates the installed canonical week without a ledger commit.
- `hermes ucc validate --fixture <resource-relative-path>` accepts a contained installed valid fixture and rejects an installed adversarial fixture.
- `hermes ucc validate --synthetic --case <case_id>` rejects all five authorized adversarial cases with stable issue codes.
- `hermes ucc dry-run --synthetic` executes all seven stages and makes exactly one isolated temporary ledger commit.
- `hermes ucc dry-run --synthetic --case <case_id>` fails closed with zero committed entries.

Outputs are deterministic machine-readable JSON with command, status, synthetic set, case, issues, stages, canonical hash, ledger hash, commit count, and zero network/model counts. They contain no local paths or learner payload values.

## Evidence

- Focused source and installed-profile CLI lane: two passed in 12.79 seconds.
- Installed-resource proof covers valid/adversarial synthetic and explicit fixtures, real dry-run telemetry, missing-approval rejection, and socket sentinel zero.
- Full deterministic/privacy/public-boundary regression lane: 198 passed in 26.64 seconds.
- Full distribution/root-rejection/stock-smoke lane: 17 passed in 13.88 seconds.
- SEC1 restriction canary: two passed in 5.93 seconds.
- Stock Hermes remains clean at `2a5dc0ef3df433a36abed9ee544ea067d807c438`.

No real learner data, live model, network, messaging, adapter, Phase 10 behavior, or Hermes source change occurred.

## Next task

F12.1 is unblocked after final governance checks and a clean commit.
