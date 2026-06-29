# Topology Decision

Status: SELECTED FOR PLANNING; implementation blocked until Gate H1 confirms the exact Hermes pin.

## Repository-state finding

- This folder is not a Git repository. `git rev-parse --is-inside-work-tree` fails.
- It contains UCC assets, not Hermes source: `schemas/` (11 JSON schemas), `skills/` (11 flat `*.SKILL.md` files plus `.gitkeep`), `templates/`, `benchmarks/` (four California subject packs), `docs/`, `discord/`, `cron/`, and `ACDF-v7/`.
- The School Model Canvas template is `templates/SMC-TEMPLATE.md`.
- Hermes source is not vendored here and Hermes is not declared as a dependency here.
- A separate native-Windows Hermes installation exists at `C:\Users\alani\AppData\Local\hermes\hermes-agent`. Observed package version: `0.16.0`; Python: `3.11.15`.
- The prior source-fork plan incorrectly assumed a pristine Hermes checkout, a usable baseline tag, `ucc/` copies, `docs/source/`, `docs/dark-factory/`, custom `identity.md` / `system_prompt.md`, and an upstream-edit workflow. Those assumptions are removed.
- Existing flat skills are not in native Hermes `skills/<slug>/SKILL.md` layout. Several reference files named by skills are absent.
- Existing SMC, receipt, task-card, and approval concepts do not yet form a versioned, semantically enforceable runtime contract.

## Compared options

| Option | Fit | Decision |
|---|---|---|
| True Hermes source fork | Carries upstream merge burden and conflicts with zero-touch doctrine. | Rejected. |
| Independent Hermes profile/plugin distribution | Matches current Hermes `distribution.yaml`, profile, skill, and plugin extension points. | Selected. |
| Package-only wrapper | Useful for the deterministic core but insufficient alone for profile, skills, and install lifecycle. | Component only. |
| Temporary local recon clone | Appropriate for compatibility inspection only. | Allowed as read-only evidence source. |

## Selected topology

This repository becomes the installable **Hermes Thrice Great** profile distribution. It is not a copy of Hermes.

Planned distribution-owned runtime surface:

```text
distribution.yaml
SOUL.md
config.yaml
skills/<skill-slug>/SKILL.md
plugins/hermes-thrice-great/
schemas/
benchmarks/
```

The default install name is `ucc`. A user may install the same distribution as `hermes-thrice-great` or a personal alias such as `thoth`:

```powershell
hermes profile install . --name ucc
hermes profile install . --name thoth
```

The profile name is installation state, not product identity. No runtime module may require the literal name `thoth`.

## Upstream policy

- Pin one Hermes release and source commit for the MVP.
- Do not vendor Hermes or modify its source.
- Phase starts may fetch/report upstream drift but must not merge or update Hermes.
- Upstream upgrades occur only in separately claimed compatibility tasks after MVP acceptance.
- A direct Hermes modification requires a human-approved exception and a new topology decision.

## Rollback

Uninstall or disable the `ucc` profile/plugin. Stock Hermes remains independently installed and unchanged.
