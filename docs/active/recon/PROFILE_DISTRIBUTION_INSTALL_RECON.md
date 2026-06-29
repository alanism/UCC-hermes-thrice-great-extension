# Native Profile Distribution Install Recon

Task: H1.2

Date: 2026-06-30 local / 2026-06-29 UTC

## Result

PASS. Hermes 0.16.0 can install and update a synthetic distribution entirely from a local directory through `hermes_cli.profile_distribution`, under an isolated temporary `HERMES_HOME`, without invoking the network-capable top-level CLI.

## Proven behavior

- `distribution.yaml` is required at the source root.
- `hermes_requires: ">=0.16.0"` accepts the pinned runtime.
- Install-name override changes the installed manifest name (`probe-one`).
- The target remained under the isolated temporary Hermes home.
- `SOUL.md`, `config.yaml`, and `skills/probe-skill/SKILL.md` were copied.
- Standard user-owned directories were bootstrapped.
- The installed manifest recorded the local source path.
- Update restored a tampered distribution-owned `SOUL.md`.
- Update preserved a user-modified `config.yaml` by default.
- Update preserved a synthetic file under user-owned `memories/`.
- `describe_distribution()` returned the installed override name.

## Safety method

- Synthetic files only.
- No aliases, credentials, model calls, gateways, network calls, or Git operations in the Hermes checkout.
- Hermes venv Python ran with `-B`.
- Temporary files were ignored by repository Git policy and removed after the probe.

## Windows harness lesson

The first attempt used PowerShell variable `$home`; PowerShell variable names are case-insensitive and `$HOME` is read-only, so the assignment failed and the synthetic target defaulted to `C:\Users\alani\profiles\probe-one`. The exact synthetic manifest and path were verified, no reparse points were present, and only that probe directory was removed. The probe was rerun successfully using `$probeHome`.

This is a concrete input for the later native-Windows canary and must not be hidden as a clean first-pass result.
