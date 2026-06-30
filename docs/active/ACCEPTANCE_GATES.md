# Acceptance Gates

All gates are binary. A documented unknown is a FAIL until its recon task closes it.

## P0 — Planning authority

- Active plan, task board, graph, reference guide, gates, and topology decision exist.
- `authority.json` points to them and its hashes validate.
- No implementation is authorized by this gate.
- Pre-A1 execution requires the narrow human declaration in `BOOTSTRAP_PROTOCOL.md`; absent that declaration, even bootstrap tasks remain unauthorized.

## H1 — Hermes pin and native extension recon

- An automated identity probe proves the invoked executable, imported `hermes_cli`, editable-install source, exact checkout HEAD, and version metadata. The banner's fetched `origin/main` label is recorded separately as drift, not runtime identity.
- Any ambiguous executable/import path or unprovable checkout identity produces FAIL and human escalation; a plausible written explanation cannot pass.
- Exact Hermes package version and executing commit are pinned.
- Native profile distribution, skills, plugin, CLI command, and custom distribution-owned paths are characterized on Windows.
- An allowlisted builder generates `dist/hermes-thrice-great-profile/`; the generated inventory contains only policy-approved paths and no governance/private paths.
- Pinned Hermes installs the generated staging tree successfully. Any attempt to use the repository root is rejected by the project's acceptance tooling.
- Stock offline smoke commands pass.
- No Hermes internal edit is proposed.

## A1 — ACDF authority machinery

- `.agent/claims/` and `.agent/state.log` exist.
- Claims are JSON and include every required field plus the active plan hash.
- Authority, task-board synchronization, archive hygiene, and state transitions have machine checks.
- `.agentignore` blinds archive paths.

## C1 — Versioned contract design

- SMC, assessment receipt, receipt pairing, generator brief, proposal/task card, parent brief, approval event, and ledger entry contracts are specified.
- Each contract has an owner, version, compatibility rule, ID rule, and migration rule.
- Semantic invariants are listed separately from JSON Schema constraints.
- No unresolved field-level ambiguity remains.

## R4 — Stage 4 execution readiness

- `READINESS_REPORT.md` is PASS.
- Sandbox/tool restrictions, privacy defaults, dependency/runtime matrix, Windows commands, synthetic fixture policy, deterministic test strategy, stock smoke, and isolated profile install dry run pass.
- A native-Windows pytest/filesystem canary records long-path, drive-case, reserved-name, and junction/reparse behavior and proves either supported behavior or safe fail-closed handling.
- The mutation harness kills a known behavior-changing mutant, does not falsely kill a no-op/equivalent control, and reports setup/crash/timeout as `ERROR`.
- Active plan hash is current; claim and state machinery is operational.
- Zero unresolved critical risks.
- This is the first gate that can authorize test creation; production implementation remains test-gated.

## T1 — Red harness captured

- Every implementation behavior has a separate failing test task and captured expected failure.
- Failures are caused by missing behavior, not broken fixtures or environment.
- Negative-fixture and mutation strategies exist for semantic validation, pairing, approval, path containment, reference integrity, and atomic ledger writes.
- Each mutation probe inherits the Stage 4 meta-probe contract: killable mutant `KILLED`, no-op/equivalent control `SURVIVED` or `SKIPPED`, infrastructure failure `ERROR`.

## S1 — Native skill packaging

- Every skill lives in the format proven by H1.
- Every declared reference exists or was explicitly removed with rationale.
- Frontmatter parses and names are unique.
- Native Hermes discovery/load smoke passes.
- Reference-integrity mutations are detected.

## PR1 — Reusable profile

- Local distribution install into an isolated temporary Hermes home passes.
- `ucc` loads `SOUL.md`, restricted `config.yaml`, packaged skills, and the plugin.
- The same distribution installs under `thoth` without code/content changes.
- Stock Hermes smoke remains unchanged.
- PR1 proves installability only. Learner/semi-real data execution is forbidden until SEC1 passes.

## SEC1 — Privacy and sandbox

- Web and messaging are disabled by default.
- Terminal/filesystem access is sandboxed or restricted by enforceable configuration.
- Path checks resist traversal, symlinks, Windows junctions/reparse points, and case/normalization tricks.
- Logs redact secrets and omit raw learner payloads.
- Durable records are pseudonymous; retention/delete behavior works.
- Generated learner data is outside Git or mechanically ignored by a human-owned ignore rule.

## U1 — Deterministic core

- Schema and semantic validators pass positive cases and reject negative cases.
- Pressure delta only computes after valid pairing.
- Diagnosis facts, proposal, brief data, approval enforcement, and ledger writes are deterministic.
- Approval cannot be forged by an AI actor or replayed across revisions.
- Atomic-write fault mutations leave the prior ledger intact.

## E1 — Synthetic weekly dry run

- A complete synthetic SMC → receipts → pairing → diagnosis → parent brief → proposal → approval wait → approved transition → ledger flow passes offline.
- Re-running with identical input produces identical semantic output except declared volatile envelope fields.
- No network, live model, Discord, or Campaign OS action occurs.

## I1 — EXCLUDED from this release

- C3.8 set `I1_MOCK_ADAPTERS = EXCLUDE`; this gate is not in the F1 dependency chain.
- Mock adapters consume only approved output contracts.
- They are disabled by default and make no network calls.
- Adapter failures cannot corrupt the ledger or bypass approval.

## B1 — Branding and aliases

- Branding is profile/distribution-driven.
- `ucc`, `hermes-thrice-great`, and optional `thoth` installs behave equivalently.
- No stock Hermes identity is changed.

## F1 — Final production distribution acceptance

- Gates H1 through E1 and required governance gates pass.
- Every DONE task has a receipt and matching state-log event.
- Compatibility matrix and readiness report are current.
- Critical risk count is zero.
- Final acceptance command set passes from a clean temporary environment.

Final checklist:

1. Repository topology is explicit.
2. Hermes version and commit are pinned.
3. ACDF authority passes machine validation.
4. Machine-readable claims and `.agent/state.log` are active.
5. Stock Hermes offline smoke passes.
6. UCC profile smoke passes.
7. Skills use native Hermes packaging.
8. Broken skill references are repaired or explicitly removed.
9. Contracts are versioned.
10. Expected failing tests were captured before implementation.
11. Receipt semantic validation accepts positive and rejects negative cases.
12. Pressure delta computes only for semantically valid paired sessions.
13. A valid parent approval event is required before activation.
14. Privacy and containment tests pass.
15. Local ledger writes are atomic and idempotent.
16. Synthetic weekly dry run and repeatability checks pass.
17. No live Discord, network, or model action occurs without explicit opt-in.
18. Every DONE task has a receipt and matching state event.
19. Generated learner outputs are mechanically ineligible for accidental commit.
20. Unresolved critical risks equal zero.
