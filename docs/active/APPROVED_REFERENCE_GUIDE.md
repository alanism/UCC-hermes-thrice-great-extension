# Approved Reference Guide

Status: ACTIVE FOR PLANNING. It authorizes planning and test design only; Stage 4 readiness must pass before runtime implementation.

## Product definition

Hermes Thrice Great is an installable UCC profile distribution for a pinned Hermes release. It supplies reusable profile guidance, UCC skills, deterministic educational-evidence processing, and local approval/ledger controls through supported Hermes extension points.

It is not Hermes source, a general learning-content generator, a live Discord bot, or a multi-family SaaS system.

## Naming

- Product/distribution: Hermes Thrice Great / UCC.
- Plugin: `hermes-thrice-great`.
- Default installed profile: `ucc`.
- Optional personal installed profile: `thoth`.
- Code and contracts must not assume any one profile name.

## MVP correctness

The MVP is correct only when it can, offline and with synthetic data:

1. Install into a temporary Hermes home through native profile-distribution mechanics.
2. Leave stock Hermes behavior unchanged.
3. Load packaged UCC skills with no broken references.
4. Validate versioned SMC, receipt, pairing, proposal, brief, approval-event, and ledger contracts.
5. Reject semantic inconsistencies that JSON Schema alone cannot express.
6. Pair CALM/PRESSURE sessions only when form, skill distribution, timing, completion, integrity, and minimum evidence rules permit comparison.
7. Produce deterministic diagnosis facts and an evidence-labeled parent brief.
8. Create a proposal that cannot become scheduled, active, or done without a valid parent approval event.
9. Prevent an AI actor from approving its own proposal.
10. Write ledger records atomically inside a private configured data root.
11. Operate with web, messaging, and unrestricted terminal/filesystem capabilities disabled by default.
12. Produce task receipts and preserve ACDF claim/state history.

## Contract doctrine

- Schemas identify shape; semantic validators enforce cross-field invariants.
- Every durable artifact carries `schema_version`, a stable ID, provenance, and timestamps.
- Durable learner identifiers are pseudonymous. Display names are optional presentation data and are not required in the ledger.
- Input contracts are never changed in place after release. Breaking changes require a new major contract version and migration task.
- Receipt quality/integrity status is distinct from cryptographic or storage integrity.

## Pressure comparison doctrine

Pressure delta is not computed unless the pairing validator proves comparability. The denominator, timeout treatment, partial-session policy, degraded-data policy, minimum evidence, form match, skill-distribution tolerance, timestamp order, summary/event consistency, and mode/timer-tier consistency are binding contract rules defined in Phase 3.

## Approval doctrine

Task or campaign status is not approval evidence. Approval is a separate append-only event tied to a proposal revision. A valid parent event must name its actor, action, revision, idempotency key, provenance, and source evidence. AI actors cannot emit an approving action.

Approval idempotency keys are globally unique within the configured ledger namespace. Repeating an identical canonical event is an idempotent success. Reusing a key with any different proposal, revision, actor, action, or provenance is a conflict. An event for revision R1 never authorizes R2.

## Privacy doctrine

Real educational data is local/private by default and never enters fixtures, logs, Git, live adapters, or outbound model calls without explicit authorization. Local does not mean unrestricted: paths must be canonicalized safely, writes atomic, secrets redacted, retention/deletion defined, and agent tools restricted by enforceable Hermes configuration or sandboxing.

Gate PR1 proves only that the distribution installs correctly. It is not a safe-to-operate declaration. No learner profile, real data, or semi-real data may be used until SEC1 passes. `SOUL.md` instructions never substitute for enforceable tool and filesystem restrictions.

## Non-goals

- Editing Hermes internals.
- Live Discord or Campaign OS writeback.
- Autonomous educational decisions.
- Clinical inference or mastery overclaim.
- Full learning-engine integrations.
- Multi-user identity/authentication or cloud synchronization.
- Branding before the synthetic weekly dry run passes.

## Open recon decisions

- Reproducible binding of Hermes package `0.16.0` to the executing editable checkout at the candidate HEAD; the banner's `upstream` label is remote-drift metadata, not runtime identity.
- Exact plugin/profile distribution-owned path behavior.
- Restricted Hermes toolset keys for the pinned version.
- Whether the deterministic core remains plugin-internal or becomes a separately packaged Python library. Prefer plugin-internal until reuse is proven.
- Whether optional mock adapters are inside F1 scope. This must be decided before any adapter RED test is authored.
