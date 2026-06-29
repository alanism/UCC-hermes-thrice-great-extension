# Adversarial Review Disposition

Date: 2026-06-30
Status: incorporated into planning authority; runtime implementation remains unauthorized.

## Inputs

| Review | SHA-256 | Disposition summary |
|---|---|---|
| Review A | `ee08bec2b72268949021190636c3fa5a4a493a1cf547034bcf223e77a84315a0` | Direction endorsed; milestone execution and H1-first sequencing accepted. |
| Review B | `1e9012a78d44da0500478e3d54fda81f802a37d3a08653eabf014500a3a8ce2d` | Six concrete findings evaluated; all underlying risks accepted, with two technical corrections. |
| Review C | `59a807cb7982471c854f50dcb6642fa51d296693fa615f0c237793af1b5d7e95` | Proposed hotfixes evaluated; falsifiable gates adopted where technically sound. |

## Accepted changes

1. H1 now requires executable/import/editable-install/ref/commit evidence and human escalation when the executing checkout cannot be proven.
2. Stage 4 gains a native-Windows filesystem/pytest canary before RED tests.
3. Stage 4 gains mutation-harness self-tests: a killable mutant must be `KILLED`, a no-op/equivalent control must not be reported killed, and infrastructure failure must be `ERROR`.
4. Approval idempotency explicitly rejects reuse of one key across proposal revisions or changed approval payloads.
5. PR1 means installable, not safe for learner data. SEC1 is mandatory before any learner-profile or semi-real-data execution.
6. Mock-adapter RED tests are conditional on an explicit pre-T1 MVP scope decision.
7. Execution is milestone-bounded and one dependency-ready task at a time. A second active task board is rejected because ACDF requires one authoritative queue.

## Corrected recommendations

### Hermes commit evidence

The apparent `2a5dc0ef` versus `ccc92c52` split was not a path collision. Read-only inspection proved:

- `hermes.exe` resolves under the local editable installation.
- `hermes_cli.__file__` resolves inside `C:\Users\alani\AppData\Local\hermes\hermes-agent`.
- package `direct_url.json` points to that editable checkout.
- executing checkout `HEAD` is `2a5dc0ef3df433a36abed9ee544ea067d807c438`.
- the banner's `upstream` value is computed from `origin/main`, not the executing commit.
- after fetch drift, `origin/main` was `b963d323...` and 1,983 commits ahead of HEAD.

Therefore `git name-rev --tags <banner-upstream>` is not a valid runtime identity test. H1 still must pin the executing HEAD and release metadata, but an untagged upstream tip does not imply an unrecoverable installation.

### Mutation meta-probe

A deliberately incorrect, behavior-changing mutant must be detected as `KILLED`, not `SURVIVED`. To guard against false kills, the harness must also run an equivalent/no-op control that remains `SURVIVED` or is explicitly `SKIPPED`, and must classify setup/crash/timeouts as `ERROR`, never `KILLED`.

### Approval idempotency

Composite uniqueness on `(idempotency_key, proposal_revision)` would allow the same key to be reused on a new revision, contradicting the requested cross-revision rejection. The adopted rule is:

- `idempotency_key` is globally unique within the configured ledger namespace.
- Repeating the same key with the identical canonical approval payload is idempotent success.
- Reusing the key with a different proposal ID, revision, actor, action, or provenance is `IDEMPOTENCY_CONFLICT`.
- Approval for revision R1 never authorizes R2, regardless of key.

### Windows canary

The canary tests paths beyond 260 characters, case behavior, reserved device names, and junction/reparse behavior. A host lacking long-path or link privileges is not automatically unusable: the product may pass by rejecting the unsupported operation safely. Readiness fails only if the harness cannot exercise or prove fail-closed behavior for the intended deployment mode.

## Unchanged conclusions

- H1 remains the first substantive blocker.
- Git initialization remains human-authorized.
- Stage 4 remains FAIL.
- No T0/H1 execution task was claimed or completed by this review pass.
- No runtime/profile/schema implementation is authorized.
