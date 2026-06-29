# Hermes Executing Identity Probe

Date: 2026-06-30 local / 2026-06-29 UTC

Task: H1.1

Network policy: local-only. No fetch, update, installer, model, gateway, or remote command was invoked.

## Result

PASS. The invoked Hermes command, Python interpreter, imported `hermes_cli`, editable package metadata, and Git checkout all resolve to the same local source tree.

## Binding candidate

- Package: `hermes-agent==0.16.0`
- Executing checkout: `2a5dc0ef3df433a36abed9ee544ea067d807c438`
- Branch: `main`
- Checkout state: clean
- Python: `C:\Users\alani\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe` (`3.11.15` observed by T0.1)
- Release metadata: `2026.6.5`
- Nearest ancestor tag: `v2026.6.5`
- Exact tag at HEAD: none

The binding identity is the tuple `(package version, exact checkout commit)`, not the package version alone.

## Path proof

| Evidence | Value | Result |
|---|---|---|
| Executable | `C:\Users\alani\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe` | Under checkout |
| Interpreter | `C:\Users\alani\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe` | Under checkout |
| Imported module | `C:\Users\alani\AppData\Local\hermes\hermes-agent\hermes_cli\__init__.py` | Under checkout |
| Distribution `direct_url.json` | `file:///C:/Users/alani/AppData/Local/hermes/hermes-agent` | Exact checkout match |
| Editable flag | `true` | Confirmed |
| Module/distribution/pyproject version | `0.16.0` / `0.16.0` / `0.16.0` | Consistent |

## Drift evidence

At probe time, the existing local `origin/main` ref was `f171842f0de73171031ce4f62a4fcfc7adc397d8`; executing HEAD was 2,004 commits behind and zero ahead. No fetch was performed by this task. The remote-tracking ref is volatile drift evidence and is not runtime identity.

## Falsifiable pass rule

H1.1 passes only while all are true:

1. resolved `hermes.exe` is inside the candidate checkout;
2. `hermes_cli.__file__` is inside the same checkout;
3. package direct URL exactly names the same checkout and is editable;
4. module, distribution, and `pyproject.toml` versions agree;
5. exact Git HEAD is recorded and the checkout is clean;
6. `origin/main` is reported separately and never substituted for HEAD.

Any future mismatch is H1 FAIL plus human escalation. A prose explanation alone cannot pass.
