# Phase Gate Table

| Phase | Entry | Exit | Implementation allowed? |
|---|---|---|---|
| 0 Repo state/topology | User decision Option B | P0 | Documentation only |
| 1 Hermes compatibility | P0 | H1 | Recon scripts/tests only after claim |
| 2 ACDF repair | P0 | A1 | Governance scripts only |
| 3 Contract design | H1, A1 | C1 | Schemas remain backlog; no runtime code |
| Stage 4 readiness | H1, A1, C1 | R4 | Host/mutation canaries and governance utilities only; then authorizes test creation |
| 4 TDD harness | R4 | T1 | Tests/fixtures only; capture RED |
| 5 Skill packaging | T1 | S1 | Minimum packaging changes after RED |
| 6 Native profile | T1, S1 | PR1 | Minimum distribution/profile files after RED; temporary synthetic install only, not safe for learner data |
| 7 Privacy/sandbox | T1, PR1 | SEC1 | Minimum config/guards after RED |
| 8 Deterministic core | C1, T1, PR1, SEC1 | U1 | Yes, one test-gated behavior at a time |
| 9 Synthetic week | U1 | E1 | E2E fixtures/runner only |
| 10 Mock adapters | E1 plus Phase 3 INCLUDE decision | I1 | Conditional MVP extension; no RED task when excluded |
| 11 Branding/aliases | E1 | B1 | Presentation only |
| 12 Handoff/learning | E1, I1 if included, B1 | F1 | Docs and release evidence |

Every phase also requires a current authority hash, valid claim, matching task status, and no critical-source staleness.
