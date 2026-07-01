# Learning Cards

These cards record empirical agent/harness failures. They are constraints for future work, not retrospective polish.

## LC-001 — PowerShell `$HOME` collision recurred

- Observed: H1 install recon and again during F12.1 replay.
- Failure: PowerShell variable names are case-insensitive; assigning `$home` attempts to overwrite read-only `$HOME`.
- Control: use descriptive names such as `$HermesRoot`, `$ProfileRoot`, and `$InstalledProfile`; never use `$home` in Windows harnesses.
- Evidence: both failures occurred before a Hermes action; isolated temporary roots were safely removed.
- Retry date: 2027-01-01. Verify whether current agent generation avoids the collision unaided.

## LC-002 — Plugin command discovery precedes `-p` selection

- Observed: F12.1 native CLI replay.
- Failure: `hermes -p ucc ucc doctor` cannot parse because Hermes 0.16.0 registers plugin subcommands from the initial active home before processing profile selection.
- Control: activate the installed profile directory through `HERMES_HOME`, then invoke `hermes ucc ...`.
- Retry date: on any Hermes revision review and no later than 2027-01-01.

## LC-003 — Safe mode suppresses the delivered plugin

- Observed: F12.1 clean install replay.
- Failure: leaving `HERMES_SAFE_MODE=1` active after installation suppresses all plugin loading, including the locally installed UCC plugin.
- Control: use safe mode for installation; remove it only after direct profile activation while deny-all config and socket sentinel remain enforced.
- Retry date: on any Hermes revision review.

## LC-004 — Native enablement changes YAML serialization

- Observed: F12.1 clean install replay.
- Failure: `hermes plugins enable` expands `config.yaml`; the current release doctor verifies compact deny-all restriction tokens and then fails.
- Control: use the guarded single-token installed-config activation in `INSTALL.md`. Long-term work may replace textual doctor checks with semantic YAML validation, but that is a separately authorized product change.
- Retry date: 2027-01-01 or the next CLI hardening authorization.

## LC-005 — Runtime canaries require composed test/runtime environments

- Observed: F12.2 all-in-one pytest invocation.
- Failure: repository pytest lacks Hermes/PyYAML; pinned Hermes venv lacks pytest. Three canaries errored while 238 other tests passed.
- Control: run normal tests in the repository venv, then run Hermes canaries with repository pytest and pinned Hermes `site-packages` on `PYTHONPATH`.
- Retry date: when dependency topology changes and no later than 2027-01-01.

## LC-006 — PowerShell native-output capture is not a JSON contract

- Observed: F12.1 replay after product command exits passed.
- Failure: PowerShell capture formatting made the final captured element unsuitable for `ConvertFrom-Json`, despite successful command exit checks and silent socket sentinel.
- Control: validate process exit independently and parse machine JSON through the Python subprocess acceptance lane.
- Retry date: 2027-01-01.
