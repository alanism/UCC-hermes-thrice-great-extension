# Mutation Outcome Contract

Status: R4.4 PASS

Every mutation probe runs a known-green baseline before its mutant. Outcomes are mutually exclusive:

- `KILLED`: baseline exits 0 and the mutant causes pytest exit 1 (ordinary test failure).
- `SURVIVED`: baseline and mutant both exit 0.
- `SKIPPED`: a future probe may use this only when it records a deterministic equivalence or applicability reason without executing a mutant.
- `ERROR`: baseline failure, pytest collection/usage failure, process crash, timeout, or any exit other than 0/1.

An `ERROR` never counts as a killed mutant and fails the mutation gate. A `SURVIVED` behavior-changing mutant also fails its task gate. An explicitly equivalent/no-op control must be `SURVIVED` or `SKIPPED`.

## Meta-canaries

`scripts/run_mutation_checks.py --self-test` proves:

- behavior-changing arithmetic mutant → `KILLED`;
- no-op/equivalent environment mutant → `SURVIVED`;
- abrupt process exit 70 → `ERROR`;
- missing pytest target/setup failure → `ERROR`;
- subprocess timeout → `ERROR`.

`--all` currently runs this registered meta-canary set. Later task-specific probes may be added only after their corresponding Phase 4 RED task and must preserve this classifier contract.
