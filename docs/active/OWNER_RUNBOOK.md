# Owner Runbook: Synthetic Offline Distribution

Status: final handoff candidate

## Supported boundary

Hermes Thrice Great is supported here only as an installed, synthetic, offline profile distribution on native Windows. The source repository builds the payload but is never itself an install source. Stock Hermes is pinned to `hermes-agent==0.16.0` and acceptance commit `2a5dc0ef3df433a36abed9ee544ea067d807c438`.

No real or semi-real learner data is authorized. No live model, socket, Discord, messaging, Campaign OS, external adapter, or Phase 10 behavior is authorized.

## Clean install procedure

1. Start PowerShell in the repository root.
2. Set `$Repo` and `$Staging` and run the staging builder shown in `INSTALL.md`.
3. Confirm the staging root contains `distribution.yaml`, `SOUL.md`, `config.yaml`, `.env.EXAMPLE`, `skills/`, and `plugins/hermes-thrice-great/`, with no governance or private paths.
4. Set `HERMES_HOME` to a new empty temporary directory.
5. Install the staging root as `ucc`; never install `$Repo`.
6. Apply the guarded activation replacement from `INSTALL.md` to the installed copy of `config.yaml`. This changes only `plugins.enabled` and preserves the delivered deny-all restrictions. Do not run `hermes plugins enable` for this release: Hermes 0.16.0 expands the YAML serialization and the release doctor intentionally verifies the compact restriction form.
7. Point `HERMES_HOME` at `<temporary-root>\profiles\ucc`. Hermes 0.16.0 registers plugin subcommands from the active home before parsing `-p`, so this activation is required for `hermes ucc`.
8. Remove `HERMES_SAFE_MODE` after installation. Safe mode suppresses all plugin loading; runtime containment instead comes from the installed deny-all tool configuration and offline sentinel.
9. Run the command set below.

## Acceptance command set

```powershell
hermes --version
hermes profile list
hermes ucc doctor
hermes ucc validate --synthetic
hermes ucc validate --synthetic --case invalid_totals
hermes ucc validate --fixture valid/week.json
hermes ucc validate --fixture adversarial/week-cases.json
hermes ucc dry-run --synthetic
```

Expected behavior:

| Command | Expected result |
|---|---|
| `doctor` | exit 0; distribution, resource manifest, registry schema, and deny-all configuration pass |
| valid synthetic validation | exit 0; no ledger commit |
| `invalid_totals` | nonzero; `RECEIPT_TOTAL_INCONSISTENT`; zero commits |
| explicit valid fixture | exit 0 |
| explicit adversarial fixture | nonzero; `APPROVAL_REQUIRED`; zero commits |
| synthetic dry run | exit 0; seven ordered stages; one isolated temporary commit |

Every JSON result must report `network_attempts: 0` and `model_calls: 0`. Repeated valid runs must produce identical canonical hashes and bytes. Approval must remain a distinct wait-then-apply transition.

## Troubleshooting

- `ucc` command missing: confirm the guarded activation replacement was applied to the installed profile, not the repository.
- `DISTRIBUTION_*` or resource hash failure: rebuild the staging payload from a clean source checkout; do not repair generated output manually.
- Unexpected issue code: stop and retain only synthetic command output for diagnosis.
- Socket or model attempt: stop immediately; the release boundary has been violated.
- Dirty stock Hermes checkout: stop; do not repair or update Hermes as part of this distribution.
- Failed ledger write: confirm the prior ledger remains valid and no partial staged file became committed.

## Recovery and rollback

Discard the isolated Hermes home and generated staging tree, then regenerate from the pinned repository commit. Generated implementation and install state are disposable; do not hand-edit them. User-owned or learner-containing homes are outside this release and must not be used for recovery testing.

## Shareability

After F1 passes, the allowlisted generated distribution may be shared with technical evaluators for synthetic offline evaluation. It must carry the scope statement from `README.md` and must not be represented as real-learner-data ready.

The Assessment Lab and curriculum DLC documented in `README.md` are external companion resources, not installed distribution components or F1 evidence. Share either link manually through the family’s or evaluator’s chosen communication channel. Automated messaging adapters are not included in this release. Never upload or route real learner data through either companion resource under this authorization.
