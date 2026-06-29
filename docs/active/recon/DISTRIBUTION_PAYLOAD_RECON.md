# Distribution Payload Recon

Task: H1.3

Date: 2026-06-30 local / 2026-06-29 UTC

## Characterization result

The intended custom paths work under pinned Hermes 0.16.0:

- `plugins/hermes-thrice-great/` copied and restored on update;
- root `schemas/` copied and restored on update;
- root `benchmarks/` copied and restored on update;
- target `.env`, `auth.json`, and `local/` user files were preserved;
- source `.env`, `auth.json`, `memories/`, and `local/` payloads were excluded.

All tested install/update assertions passed in an isolated temporary Hermes home.

## Critical incompatibility

Pinned `hermes_cli.profile_distribution._copy_dist_payload()` iterates every top-level source entry and copies it unless its name is in `USER_OWNED_EXCLUDE`. The manifest's `distribution_owned` list is parsed and serialized but is not used to filter install payload entries.

Consequences for the current topology:

- A Git-URL install of this repository would copy ACDF sources, `docs/active`, build receipts, source documentation, root files, and all other non-excluded tracked paths into the installed profile.
- A local-directory install would additionally expose `.git/` to the copy loop because local sources are not staged into a Git-clean clone first and `.git` is not in `USER_OWNED_EXCLUDE`.
- `distribution_owned` cannot serve as an allow-list in the pinned version.
- The repository root is therefore not a safe direct profile-distribution payload.

This contradicts the current topology statement that the repository root itself becomes directly installable.

## Resolution options requiring human architecture decision

1. Dedicated distribution-only Git repository containing only approved payload paths.
2. Generated allowlisted staging tree plus a dedicated release branch/repository for Git installs.
3. Full-repository profile copy — rejected as unsafe and operationally noisy.
4. Patch Hermes copy behavior — forbidden by the selected zero-touch topology.

Option 1 is the cleanest product boundary. Option 2 keeps one source repository but adds a governed packaging/release surface. Either changes the current packaging architecture and authority graph.

## Stop condition

The Authority + Compatibility milestone is paused before H1.4 because a required dependency cannot be resolved without a human-approved architecture change.
