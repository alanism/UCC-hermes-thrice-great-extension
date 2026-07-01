# Hermes Thrice Great

Hermes Thrice Great is a deterministic UCC evidence engine delivered as a profile distribution for stock Hermes Agent. This release proves synthetic, offline workflows on native Windows with `hermes-agent==0.16.0`.

## What this release does

- validates versioned UCC contracts and synthetic assessment evidence;
- separates proposals from authorized adult approval events;
- runs a deterministic seven-stage weekly workflow;
- writes an atomic, idempotent ledger inside isolated synthetic dry runs;
- packages a deliberately generic public skill set; and
- exposes installed-profile `doctor`, `validate`, and `dry-run` commands.

It does not use a model or network to establish facts, approval, or ledger state. It does not detect cheating, AI writing, or ghostwriting.

## Distribution boundary

The repository is the source, governance, and build-control tree. It is never installed as a Hermes profile.

The only installable input is the generated allowlisted payload:

```text
dist/hermes-thrice-great-profile/
```

Build and install instructions are in [INSTALL.md](INSTALL.md). Operational verification and recovery procedures are in [the owner runbook](docs/active/OWNER_RUNBOOK.md).

The public/default profile name is `ucc`. `hermes-thrice-great` is an equivalent public alias. `thoth` is optional, non-default, and local-only.

## Release scope

This is a production distribution proof for synthetic offline workflows. It is not evidence of readiness for real or semi-real learner data, live messaging, Campaign OS, external adapters, AI tutoring, or network-dependent operation. Hermes itself remains stock and pinned; this repository is a profile/plugin distribution, not a Hermes fork.

## License

See [LICENSE](LICENSE).
