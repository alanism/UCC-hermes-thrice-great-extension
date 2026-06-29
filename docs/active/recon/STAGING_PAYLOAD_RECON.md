# Generated Staging Payload Recon

Task: H1.3A

Date: 2026-06-30 local / 2026-06-29 UTC

## Architecture result

PASS. The repository remains the source, governance, and control repository. Hermes receives only the generated tree at `dist/hermes-thrice-great-profile/`; the repository root is never an install source.

## Builder characterization

The staging builder is deny-by-default. It copies only:

- `distribution.yaml`
- `SOUL.md`
- `config.yaml`
- `.env.EXAMPLE`
- `skills/**`
- `plugins/hermes-thrice-great/**`
- `schemas/**`
- `benchmarks/**`

It creates `dist/hermes-thrice-great-profile.inventory.json` as a sibling sidecar containing the path and SHA-256 digest of every copied file. The sidecar is never installed. A fresh temporary tree replaces the prior output, so stale output cannot survive a rebuild. Source/output overlap, path escape, symlinks, and Windows reparse points are rejected.

## Test evidence

Three tests passed:

1. the full allowlist copied and representative governance, private, local, and non-allowlisted files did not;
2. a stale private file injected into output disappeared on rebuild;
3. an output nested under the source was rejected with `SOURCE_OUTPUT_OVERLAP`.

The generated synthetic payload was installed through pinned Hermes 0.16.0's local profile distribution API into an isolated temporary Hermes home. All allowlisted fixture files were present after install. Representative forbidden paths (`.git`, `.agent`, `ACDF-v7`, `docs`, receipts, authority files, `.env`, `auth.json`, `local`, `memories`, caches, logs, virtual environments, and `node_modules`) were absent.

No Hermes source, network service, model, messaging system, learner data, or UCC product behavior was used or changed.

## Conclusion

The staging tree resolves the H1.3 direct-repository payload incompatibility without patching Hermes. H1 may proceed to native skill/plugin/profile-name characterization.
