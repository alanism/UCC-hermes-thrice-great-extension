# Hermes Profile Staging Payload Policy

Status: BINDING PRODUCTION DISTRIBUTION ARCHITECTURE

Install source: `dist/hermes-thrice-great-profile/`

The repository root is source/governance/control state and must never be passed to `hermes profile install`.

## Allowlist

Only these relative paths may appear in the generated staging root:

- `distribution.yaml`
- `SOUL.md`
- `config.yaml`
- `.env.EXAMPLE`
- `skills/**`
- `plugins/hermes-thrice-great/**`
- `schemas/**` when selected by the plugin manifest/build configuration
- `benchmarks/**` when selected by the plugin manifest/build configuration
- a minimal Hermes-required metadata file explicitly added to this policy

The builder is deny-by-default. A source path's existence does not authorize copying it.

## Explicit exclusions

The builder must reject or omit all non-allowlisted content, including:

- `.git/**`, `.agent/**`
- `ACDF-v7/**`
- `docs/**`, including active/archive authority, receipts, ledgers, and reviews
- source planning documents
- `.env`, `auth.json`, credentials, keys, tokens, and secrets
- `local/**`, `memories/**`, `sessions/**`, `logs/**`
- real or semi-real learner data
- caches, temporary files, outputs, virtual environments, databases, and `node_modules/**`
- reparse points, symlinks, junctions, or any path escaping the source root
- anything not explicitly allowlisted

## Build invariants

1. Build into a fresh staging tree; stale files cannot survive rebuild.
2. Canonicalize source and destination paths before copying.
3. Reject source/destination overlap and path escape.
4. Reject symlinks/reparse points in selected payload paths.
5. Emit a sorted file inventory and content hashes as a sibling sidecar outside the install payload.
6. Validate `distribution.yaml` at the staging root before install.
7. Run a forbidden-path scan before any Hermes install probe.
8. `dist/` remains Git-ignored; generated payload is evidence, not source authority.

## Publication

The production build uses the local generated staging tree. A dedicated release repository or branch may later publish the same allowlisted payload after acceptance; it is not required for the current build sequence.
