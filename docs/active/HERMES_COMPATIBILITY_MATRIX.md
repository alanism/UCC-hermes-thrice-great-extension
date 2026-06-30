# Hermes Compatibility Matrix

Status: **H1 PASS** — exact executing identity, staged profile delivery, native extensions, arbitrary names, restricted config keys, and stock offline smoke are proven.

| Dimension | Production pin / candidate | Evidence / required proof |
|---|---|---|
| Hermes package | `hermes-agent==0.16.0` | `python -m pip show hermes-agent` on 2026-06-30. |
| Installed source checkout | `2a5dc0ef3df433a36abed9ee544ea067d807c438` | `git -C <installed-hermes> rev-parse HEAD`. |
| Executing code identity | editable checkout at `HEAD 2a5dc0ef3df433a36abed9ee544ea067d807c438` | `where.exe hermes`, `hermes_cli.__file__`, package `direct_url.json`, and Git HEAD all resolve to the same checkout. |
| Banner `upstream` label | volatile local `origin/main`; latest H1 observation `d2ce2c85` | Pinned-source `banner.py` proves this label reads the existing local `origin/main`; it is drift information, not executing-code identity. No H1 probe fetched. |
| Python | `3.11.15`; supported floor to be confirmed from pinned `pyproject.toml` | Local observation plus recon. |
| Primary OS | Native Windows 10 build `26200` | Local observation. |
| Secondary OS | Linux/macOS compatibility is desired, not a current production acceptance gate | CI decision deferred. |
| Profile mechanism | `distribution.yaml`, `config.yaml`, `SOUL.md`, `hermes profile install` | Confirmed in installed Hermes docs and code. |
| Skill format | distribution-local `skills/<slug>/SKILL.md`; nested `SKILL.md` discovery supported | H1.4 native discovery and Windows frontmatter/platform probe passed. |
| Plugin format | `plugins/<name>/plugin.yaml` plus Python `register(ctx)` | H1.4 opt-in user-plugin load and CLI/slash-command registration passed. |
| Profile payload delivery | Generated allowlisted `dist/hermes-thrice-great-profile/`; never repository root | H1.3 proved pinned Hermes copies all non-user-excluded source entries regardless of `distribution_owned`; staging is mandatory. |
| Stock offline smoke | `hermes --version`; `hermes profile list`; `hermes --help` | H1.5: all exit 0 in isolated `HERMES_HOME`; no model/network action. |
| UCC offline smoke | Target public contract: `python scripts/run_ucc_smoke.py --offline` | Script is future work; must install into a temporary `HERMES_HOME`. |
| Update policy | Pinned for this production distribution release | Drift reported only; no phase-start updates. |

## Known incompatibilities and unknowns

1. The candidate checkout was 2,004 commits behind the existing local `origin/main` ref at H1.1 and 2,010 behind the later local `d2ce2c85` ref at H1.5. This is deliberate release pinning, not permission to update during the production build.
2. Package version `0.16.0` does not by itself identify post-release commits; H1 must bind package metadata and exact HEAD together.
3. This repository has no `distribution.yaml`, `SOUL.md`, `config.yaml`, or plugin yet.
4. Current skill files are flat and named `*.SKILL.md`; Hermes expects `SKILL.md` inside skill directories.
5. Custom plugin/schema/benchmark paths copy correctly, but the pinned installer does not enforce `distribution_owned` as an allowlist. The project staging builder must enforce the boundary before install.
6. The characterized keys are `plugins.enabled`, `plugins.disabled`, and `agent.disabled_toolsets`. The sufficient restricted-toolset baseline remains an R4.2 proof obligation; prose instructions in `SOUL.md` are not a security boundary.

Gate H1 binds `hermes-agent==0.16.0` executing from clean checkout `2a5dc0ef3df433a36abed9ee544ea067d807c438`. `origin/main` need not equal HEAD and is not part of executing identity. Any future ambiguous executable/import path, dirty checkout, changed HEAD, or unprovable identity requires human escalation and H1 FAIL; prose explanation alone cannot pass.
