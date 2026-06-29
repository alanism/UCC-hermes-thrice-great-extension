# Hermes Compatibility Matrix

Status: CANDIDATE PIN — Gate H1 must reproduce the executing checkout identity and native extension behavior before implementation.

| Dimension | MVP candidate | Evidence / required proof |
|---|---|---|
| Hermes package | `hermes-agent==0.16.0` | `python -m pip show hermes-agent` on 2026-06-30. |
| Installed source checkout | `2a5dc0ef3df433a36abed9ee544ea067d807c438` | `git -C <installed-hermes> rev-parse HEAD`. |
| Executing code identity | editable checkout at `HEAD 2a5dc0ef3df433a36abed9ee544ea067d807c438` | `where.exe hermes`, `hermes_cli.__file__`, package `direct_url.json`, and Git HEAD all resolve to the same checkout. |
| Banner `upstream` label | fetched `origin/main`; observed first as `ccc92c52`, later `b963d323` | Pinned-source `banner.py` proves this label reads `origin/main`; it is drift information, not executing-code identity. |
| Python | `3.11.15`; supported floor to be confirmed from pinned `pyproject.toml` | Local observation plus recon. |
| Primary OS | Native Windows 10 build `26200` | Local observation. |
| Secondary OS | Linux/macOS compatibility is desired, not an MVP gate | CI decision deferred. |
| Profile mechanism | `distribution.yaml`, `config.yaml`, `SOUL.md`, `hermes profile install` | Confirmed in installed Hermes docs and code. |
| Skill format | `skills/<category-or-slug>/<slug>/SKILL.md` or distribution-local `skills/<slug>/SKILL.md` | Exact discovery behavior must be characterized by H2. |
| Plugin format | `plugin.yaml` plus Python `register(ctx)` | Confirmed in installed Hermes plugin docs. |
| Profile plugin delivery | Proposed explicit `distribution_owned: [plugins/hermes-thrice-great, ...]` | Must be proven by an isolated install test before use. |
| Stock offline smoke | `hermes --version`; `hermes profile list`; `hermes --help` | Must pass without model/network calls. |
| UCC offline smoke | Target public contract: `python scripts/run_ucc_smoke.py --offline` | Script is future work; must install into a temporary `HERMES_HOME`. |
| Update policy | Pinned for the MVP | Drift reported only; no phase-start updates. |

## Known incompatibilities and unknowns

1. The candidate checkout is 1,983 commits behind the fetched `origin/main`; this is deliberate pinning, not permission to update during the MVP.
2. Package version `0.16.0` does not by itself identify post-release commits; H1 must bind package metadata and exact HEAD together.
3. This repository has no `distribution.yaml`, `SOUL.md`, `config.yaml`, or plugin yet.
4. Current skill files are flat and named `*.SKILL.md`; Hermes expects `SKILL.md` inside skill directories.
5. Profile-distribution copying of the custom `plugins/hermes-thrice-great/`, root `schemas/`, and root `benchmarks/` paths must be tested.
6. The exact restricted toolset configuration keys must be read from the pinned Hermes config schema; prose instructions in `SOUL.md` are not a security boundary.

Gate H1 converts the candidate pin into the binding pin only after an automated identity probe reproduces executable path, import path, editable-install source, exact HEAD, version metadata, and stock smoke in an isolated environment. `origin/main` need not equal HEAD. Any ambiguous executable/import path or unprovable checkout identity requires human escalation and H1 FAIL; prose explanation alone cannot pass.
