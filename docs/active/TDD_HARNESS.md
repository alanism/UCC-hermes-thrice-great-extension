# TDD Harness

## Mandatory loop

For every behavior:

1. Claim the test task.
2. Add the smallest contract/security test or negative fixture.
3. Run it and record RED with the expected failure reason.
4. Complete the test task; claim the linked implementation task.
5. Implement the minimum behavior.
6. Run the focused test and record GREEN.
7. Run the impacted suite.
8. Run the declared mutation/negative check.
9. Write a receipt and update `.agent/state.log`.

A test that passes before implementation is invalid unless it is explicitly a characterization test. An environment or syntax failure is not RED.

## Guard the guards

Before Phase 4, the mutation runner must prove three distinct outcomes:

1. A known behavior-changing canary mutant is detected as `KILLED`.
2. A no-op/equivalent control is `SURVIVED` or explicitly `SKIPPED`, never falsely reported killed.
3. Setup failure, crash, timeout, or non-execution is `ERROR`, never counted as killed.

Any runner that cannot distinguish these outcomes blocks R4. Phase-specific probes must reuse this outcome model and carry a meta-test.

## Planned test layers

- `tests/characterization/`: pinned Hermes distribution/profile/plugin behavior.
- `tests/contracts/`: schema registry and semantic rules.
- `tests/security/`: tool restrictions, path containment, logging, commit eligibility.
- `tests/skills/`: frontmatter, native discovery, reference integrity.
- `tests/profiles/`: isolated install and arbitrary installed names.
- `tests/plugin/`: deterministic core and approval/ledger enforcement.
- `tests/e2e/`: offline synthetic week.

## Required mutation/negative gates

| Target | Required killed fault |
|---|---|
| Semantic receipt validator | Accept mismatched totals or reversed timestamps. |
| Pressure pairing | Ignore form/skill mismatch or minimum sample. |
| Approval enforcement | Permit AI approval, wrong revision, or replay. |
| Path containment | Accept traversal, alternate drive/UNC, symlink, or junction escape. |
| Skill references | Remove or rename a referenced file without detection. |
| Ledger atomicity | Fault between temporary write and replace without preserving prior record. |

Use deterministic project scripts for required mutations unless a pinned mutation framework is approved in the dependency matrix.

## Timing

Focused feedback must remain under 60 seconds. If a focused suite exceeds 60 seconds, stop feature work and split/optimize the harness before continuing. Full acceptance may exceed 60 seconds but must emit only failures and a final summary.

## Windows commands

```powershell
python -m pytest tests/contracts/test_receipt_semantics.py -q
python scripts/run_mutation_checks.py --target receipt-semantics
python scripts/run_acceptance.py --offline
```

Scripts must be cross-platform Python. Bash-only command chains are not acceptance authority.

Before these suites are authored, the Stage 4 host canary must run a trivial pytest test and filesystem probes for paths beyond 260 characters, drive-letter case normalization, Windows reserved names, and junction/reparse behavior. Unsupported host behavior is acceptable only when the product and harness prove a deterministic fail-closed path.
