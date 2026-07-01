# Final Acceptance Report

Date: 2026-07-01

Task: F12.2

Result: **PASS — clean-room production distribution proof for synthetic offline workflows**

## Acceptance results

| Requirement | Result | Evidence |
|---|---|---|
| Generated staging payload is the only install source | PASS | Allowlist builder and T4.8 distribution contract; repository-root source rejected before Hermes invocation. |
| Public `ucc` install | PASS | Fresh native-Windows temporary Hermes root and installed-resource CLI lane. |
| `hermes-thrice-great` public alias | PASS | Semantic payload and doctor output equal to `ucc`. |
| Optional `thoth` alias | PASS, local-only | Equivalent payload/doctor behavior; absent from default public identity. |
| Stock Hermes before/after | PASS | Version, profile list, help, Git HEAD, and clean status unchanged. |
| `hermes ucc doctor` | PASS | Installed identity, resource manifest, registry schema, and compact deny-all restrictions verified. |
| Valid installed synthetic validation | PASS | Exit zero; deterministic canonical hash; zero ledger commits. |
| `invalid_totals` adversarial case | PASS | Nonzero exit; stable `RECEIPT_TOTAL_INCONSISTENT`; zero commits. |
| Explicit valid/adversarial fixtures | PASS | Valid week exits zero; adversarial week exits nonzero with `APPROVAL_REQUIRED`. |
| Seven-stage dry run | PASS | Ordered stages end in one isolated temporary ledger commit. |
| Approval separation | PASS | `approval_wait` precedes `approval_applied`; missing approval never commits. |
| Repeatability | PASS | Two runs produce byte-identical canonical output and equal ledger hashes without mutating fixtures. |
| Ledger safety | PASS | Atomicity, replay idempotency, changed-payload conflict, injected-write-fault preservation, and isolation pass. |
| Network and model containment | PASS | Socket sentinel recorded zero attempts; machine envelopes report zero model calls. |
| Privacy/public/governance boundary | PASS | Private-data staging, public-skill boundary, authority, claim-state, and archive lanes pass. |
| Optional adapters | EXCLUDED | C3.8 keeps T4.11, I10.1, I10.2, and Phase 10 outside F1. |

## Test evidence

- Deterministic, privacy, governance, distribution, branding, and installed CLI suite: 232 passed in 47.93 seconds.
- Pinned-Hermes dependency/restriction canaries: four passed in 5.56 seconds.
- Focused installed CLI, aliases, weekly proof, and distribution lane: 24 passed in 33.49 seconds.
- An initial all-in-one invocation produced 238 passes and three interpreter-selection errors because the repository test venv does not contain Hermes runtime packages. Re-running those runtime canaries with repository pytest plus pinned Hermes site-packages passed; no product assertion failed.

## Final command set

After the generated-payload install and guarded installed-config activation documented in `INSTALL.md`:

```text
hermes ucc doctor
hermes ucc validate --synthetic
hermes ucc validate --synthetic --case invalid_totals
hermes ucc validate --fixture valid/week.json
hermes ucc validate --fixture adversarial/week-cases.json
hermes ucc dry-run --synthetic
```

## Release scope

This release is a production distribution proof for synthetic offline workflows. It may be shared with technical evaluators after F1 reconciliation. It makes no claim of readiness for real or semi-real learner data, live messaging, Campaign OS, external adapters, AI tutoring, cloud operation, network-dependent operation, or detection of cheating, AI writing, or ghostwriting. Hermes remains stock and unmodified.

Critical risks: **0**.

F12.3 reconciliation remains required before F1 is declared.
