# Final Risk Report

Date: 2026-07-01

Unresolved critical risks: **0**

| ID | Level | Status | Rationale / control |
|---|---|---|---|
| R-F12-01 | Scope boundary | Controlled | Real and semi-real learner data are not authorized. This is a release exclusion, not an accepted data risk. |
| R-F12-02 | Low | Controlled | Hermes 0.16.0 plugin activation requires a guarded installed-config token replacement so compact deny-all serialization remains doctor-verifiable. The exact Windows procedure replayed successfully. |
| R-F12-03 | Low | Controlled | The pinned Hermes checkout trails the existing local upstream ref. Executing identity remains bound to the tested commit; no update occurred. Post-release drift review is human-gated. |
| R-F12-04 | Scope boundary | Deferred | Linux and macOS are not acceptance platforms for this release. Native Windows is the only proven host. |
| R-F12-05 | Scope boundary | Excluded | Discord, messaging, Campaign OS, external adapters, Phase 10, and live network/model operation are outside F1. |

No listed item permits broader operation than the release scope. Any move toward learner data, networking, adapters, another OS, or a different Hermes revision requires a new gated acceptance cycle.
