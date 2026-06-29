# Pinned Hermes Stock Offline Smoke

Status: H1 PASS

Date: 2026-06-30 local / 2026-06-29 UTC

## Bound runtime

- Package: `hermes-agent==0.16.0`
- Executing checkout: `C:\Users\alani\AppData\Local\hermes\hermes-agent`
- Executing HEAD: `2a5dc0ef3df433a36abed9ee544ea067d807c438`
- Python: `3.11.15`
- Platform: native Windows 10 build 26200

## Smoke contract

Run each command with a newly created temporary `HERMES_HOME` and project-plugin discovery disabled:

```powershell
hermes --version
hermes profile list
hermes --help
```

Pass requires exit code 0 for every command, no model or gateway start, no credential prompt, no network operation, and cleanup limited to the probe's own temporary home.

The pinned `--version` path checks update drift synchronously. Because the executing code is a local Git checkout, `hermes_cli.banner.check_for_updates()` compares existing local `HEAD` and `origin/main` references; it does not fetch. The other two commands are local parser/profile operations. If a future install lacks the local checkout, its version path may fall through to PyPI and is not approved as an offline smoke until separately contained.

## Observed result

| Command | Exit | Key observation |
|---|---:|---|
| `hermes --version` | 0 | v0.16.0; project path matches pin; Python 3.11.15 |
| `hermes profile list` | 0 | isolated default profile listed; no gateway |
| `hermes --help` | 0 | stock parser/help rendered |

After smoke, executing HEAD remained `2a5dc0ef3df433a36abed9ee544ea067d807c438` and the checkout remained clean.

## Drift report

The existing local `origin/main` reference was `d2ce2c852d919b43a17f5966095d969ff8fa7407` at H1.5, 2,010 commits ahead of the executing pin. This differs from earlier observations and proves why the banner label is volatile. No fetch, pull, update, checkout, merge, vendoring, or source edit was performed.

## Future acceptance use

R4 and later acceptance must rerun this contract before and after profile/plugin installation. A changed package version, checkout HEAD, import path, executable path, dirty Hermes worktree, nonzero command, or attempted network fallback is FAIL.
