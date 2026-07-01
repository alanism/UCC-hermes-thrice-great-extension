# Hermes Compatibility Matrix

Status: **F12.2 PASS** — installed synthetic-offline distribution behavior is proven on native Windows.

| Dimension | Locked value | Acceptance evidence |
|---|---|---|
| Hermes package | `hermes-agent==0.16.0` | R4.1 runtime lock and F12.2 canary. |
| Executing checkout | `2a5dc0ef3df433a36abed9ee544ea067d807c438` | Git identity and clean-status checks before/after install. |
| Python | `>=3.11,<3.14`; observed 3.11.15 | Native-Windows harness. |
| Primary OS | Native Windows 10 build 26200 | H1/R4/F12 acceptance host. |
| Secondary OS | Linux/macOS deferred | Not an acceptance platform for this release. |
| Profile mechanism | Local `hermes profile install` from generated staging tree | H1.2, P6, F12.1/F12.2. |
| Install source | `dist/hermes-thrice-great-profile/` only | Deny-by-default builder and root-source rejection contract. |
| Public names | `ucc`; alias `hermes-thrice-great` | Semantically equivalent installed payloads and doctor output. |
| Optional local name | `thoth` | Equivalent, non-default, local-only. |
| Skills | `skills/<slug>/SKILL.md` | Native discovery/load and reference mutation gate pass. |
| Plugin | `plugins/hermes-thrice-great/plugin.yaml` plus Python registration | Native installed discovery and CLI execution pass. |
| Installed commands | `hermes ucc doctor`, `validate`, `dry-run` | Valid/adversarial resources, seven stages, zero sockets/models. |
| Restricted tools | `agent.disabled_toolsets: ["*"]`, empty CLI toolsets/MCP | R4.2 and F12 doctor pass. |
| Test harness | `pytest==9.0.2`, `pytest-asyncio==1.3.0` with exact lock | R4.1 and F12.2 canaries. |
| Update policy | Pinned; no update in this release | Drift is report-only and human-gated. |

## Known compatibility constraints

1. Package version alone is insufficient identity; the exact clean Git commit is binding.
2. The pinned Hermes installer copies more than `distribution_owned`; the project staging builder is the mandatory allowlist boundary.
3. Hermes 0.16.0 discovers plugin command parsers from active `HERMES_HOME` before `-p` selection. Installed plugin commands require direct profile-home activation.
4. Native `hermes plugins enable` expands YAML serialization. This release instead uses the guarded installed-config token replacement in `INSTALL.md`, preserving compact doctor-verifiable deny-all restrictions.
5. Paths beyond 260 characters fail closed on the acceptance host; drive letters are case-insensitive; reserved names and junctions require explicit guards.
6. The existing local upstream ref is ahead of the pinned checkout. This is deliberate pinning, not update authorization.

## Stock compatibility

`hermes --version`, `hermes profile list`, and `hermes --help` remain unchanged before and after isolated distribution installs. Stock Hermes source is unmodified and clean. Any changed executable/import path, dirty checkout, changed HEAD, network attempt, or model call invalidates this matrix and requires a new acceptance cycle.
