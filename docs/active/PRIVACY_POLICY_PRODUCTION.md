# Production Distribution Privacy Policy

Data tier: sensitive local educational data.

## Defaults

- Synthetic fixtures only in repository and CI.
- Real data root is explicit, private, outside Git, and denied when unset.
- Durable learner IDs are pseudonymous; display names are optional and excluded from ledger keys.
- Web, messaging, live adapters, and autonomous outbound model use are disabled.
- Terminal/filesystem capabilities use the strongest pinned-Hermes restriction proven on native Windows; profile prose is not enforcement.
- Logs contain issue codes, record IDs, and counts—not raw prompts, responses, names, answers, secrets, or receipt bodies.

## Storage

- Canonical JSON encoding and atomic same-volume replacement.
- Restrictive OS permissions where supported; inability to verify permissions is a warning or failure according to the threat model.
- Path containment resolves Windows drive/UNC semantics, symlinks, junctions, and reparse points.
- Retention duration is configured; delete is explicit, audited, and idempotent.
- Backups and encryption-at-rest are deployment responsibilities documented before real data use. Real-data mode remains blocked until that deployment decision is recorded.

## Outbound data

The deterministic production core sends nothing outbound. Any future model/Discord/Campaign OS flow requires a separate opt-in, minimized payload contract, destination allow-list, audit receipt, and revocation path.

## Source control

Generated learner outputs, temporary Hermes homes, `.env`, credentials, local ledgers, and dry-run outputs are forbidden from commits. The human-owned Git ignore/hook policy must be installed before real-data mode. Agent tests must also scan the staged-file set for forbidden patterns.

## Incident response

Stop processing, preserve non-sensitive audit metadata, disable adapters, rotate exposed credentials, quarantine affected files, and require human review before resumption. Never copy raw learner data into an issue or build receipt.
