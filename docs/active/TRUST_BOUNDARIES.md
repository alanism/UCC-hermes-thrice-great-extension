# Trust Boundaries

## B1 — Upstream Hermes

Hermes is an external pinned runtime. Only documented public profile, distribution, skill, plugin, CLI, and configuration surfaces may be used. Its source is read-only evidence.

## B2 — Distribution content

The source/control repository is not an install payload. Only the generated allowlisted staging tree under `dist/hermes-thrice-great-profile/` crosses into Hermes profile installation. `distribution.yaml`, `SOUL.md`, `config.yaml`, packaged skills, plugin code, selected schemas, and selected benchmark assets are staging-owned. Governance, claims, receipts, Git metadata, source docs, learner data, and secrets must never cross this boundary. Install/update behavior must never overwrite Hermes user-owned memories, sessions, credentials, logs, or `local/` customizations.

## B3 — Plugin boundary

The plugin receives untrusted contract inputs. Shape validation and semantic validation occur before diagnosis, approval, ledger, or adapter behavior. The plugin may not infer trust from filenames or caller identity.

## B4 — Sensitive learner data

Real learner data belongs under an explicitly configured private data root outside the repository. Durable IDs are pseudonymous. Raw payloads are forbidden in logs, test fixtures, receipts about build execution, and source control.

## B5 — Parent authority

A parent approval event is authority only when it satisfies schema, actor, proposal revision, provenance, and idempotency checks. Model text, task status, Discord messages, and profile identity are not approval.

An idempotency key binds globally within the ledger namespace to one canonical event payload. Identical replay is safe; changed-payload or cross-revision reuse is a conflict. Revision R1 authority never transfers to R2.

## B6 — Filesystem

All paths are untrusted until canonicalized. Containment must account for `..`, absolute paths, drive letters, UNC paths, case folding, symlinks, junctions/reparse points, and target replacement between check and write. Writes use same-directory temporary files, flush, and atomic replace.

## B7 — Model and network

The deterministic MVP requires no model or network call. Hermes chat/model access is a separate optional surface. No learner payload may be sent outbound without explicit policy and run-level opt-in. Discord and Campaign OS are mocked only in MVP.

## B8 — Build agents

Agents may read current authority and execute only a claimed task. They may not edit authority, harness rules, archive, or human-owned ignore/security configuration from an implementation claim.

PR1 crosses only the installation boundary. SEC1 must pass before crossing the sensitive-data boundary; until then, profile tests use isolated temporary homes and synthetic install fixtures only.

## Lethal-trifecta control

Private data access, external exposure, and exfiltration-capable tools must never be simultaneously enabled. The UCC profile defaults to local private data plus disabled external tools. Any future live adapter requires a separate threat model and human approval.
