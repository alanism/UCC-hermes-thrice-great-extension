# Production Source Authority

Status: C3.1 inventory decision

## Precedence

1. `docs/active/authority.json` and its binding artifacts govern build execution.
2. Phase 3 locked contracts govern durable runtime truth.
3. The live local `thoth-big-pc` Hermes profile is the canonical operational source for existing UCC skills, subject to privacy review and release genericization.
4. `UCC_systems_document.docx` is canonical product-intent evidence, not a machine contract.
5. Repository schemas, flat skills, templates, manuals, and exports are candidates or historical consumers until explicitly promoted by a locked contract task.

No source may override the pinned Hermes identity, generated-staging boundary, privacy policy, approval doctrine, or machine authority.

## Canonical production skill source

Canonical local path:

`C:\Users\alani\AppData\Local\hermes\profiles\thoth-big-pc\skills\pedagogy\`

The C3.1 inventory inspected file names and contract-relevant skill text only. It did not inspect `memories`, `sessions`, logs, credentials, environment files, learner records, or other private profile state.

Ten profile skills have corresponding flat repository exports. Seven hashes match. Three do not and therefore prove that the repository copy is not automatically canonical:

| Skill | Production profile SHA-256 | Repository export SHA-256 | Decision |
|---|---|---|---|
| `assessment_app_reviewer` | `b29b36159ec1c45e8d6fcbc88f697f64d95d3aad4e5229060f9b5bd79201663e` | `4655f5a5d966b65027e5e4f8ed258d1571a3c7e12beee0132ca6aae8fbc8e19a` | Profile canonical; repo export stale. |
| `builder_prompt_spec` | `3d0509987797025542cb308d387d2dacfd6c9b1058bfa07499181c641f76ae31` | `bbe7b0b50965d47f4aaeb29498e182d6056c6d8b1ba9b7c3c39071a98bf727b5` | Profile canonical; repo export stale. |
| `thoth_ucc_workflows` | `de68598cf778b553dc5d46222df4efd368d06e74f3e5449d40e371f8faeb6553` | `afd6ec478bf782bc6627a15777a2d5698c7ca34ba45b7f60832d464d03d36e61` | Profile canonical; repo export stale. |

Matching hashes establish identity only for the inspected version; they do not authorize packaging. Release skills must be deliberately selected, sanitized, converted to native Hermes layout, reference-checked, and approved by the later skill/release tasks.

Special cases:

- `aria_workflow` exists in the production profile and is local/private by default. It is excluded from public/default distribution.
- `parent_workflow` exists only as a repository flat skill. It is a deliberate sanitized release candidate, not dead code and not production authority.
- `ghostwriting_integrity_gate` exists in both places with matching content. It is excluded from public/default distribution and deprecated as a release contract. Its useful concepts are renamed to AI role clarity, process evidence, student thinking evidence, mastery evidence, valid evidence claim, and false mastery risk.

## Product-intent source

`UCC_systems_document.docx` contains 422 paragraphs and 69 tables. Its contract-relevant intent includes:

- SMC as a parent-controlled educational constitution;
- local learning receipts as the evidence unit;
- CALM and PRESSURE as different assessment conditions;
- pressure delta as a coaching signal, not a diagnosis;
- parent-controlled sharing and local storage;
- Hermes as an evidence reader, campaign proposer, and parent briefer;
- no agent self-approval;
- evidence of thinking before mastery claims.

Claims that Hermes is a source fork, that Discord is the required production channel, or that live integrations are already part of the distributable runtime are superseded by active topology and trust-boundary authority.

The DOCX renderer could not run because LibreOffice is not installed. Structural extraction through the bundled document runtime succeeded; no DOCX edit was made.

## Repository source classifications

| Source | Classification | Use |
|---|---|---|
| `templates/SMC-TEMPLATE.md` | Candidate normalization source | C3.2 maps every field into the versioned SMC contract. |
| `templates/telemetry/example-receipt.json` | Synthetic legacy example | Migration fixture candidate only; never production evidence. |
| `templates/campaigns/example-weekly-plan.json` | Synthetic legacy example | Consumer/migration analysis only. |
| `schemas/*.json` | Mixed legacy contract candidates | Include, revise, deprecate, or defer per `CONTRACT_INVENTORY.md`. |
| `docs/macro-meso-micro-loop.md` | Architecture/intention evidence | Useful consumer map; contains learner-specific filenames that must not become release defaults. |
| `docs/owners_manual.md` | Historical/operator narrative | Ghostwriting-policing and live-channel language is non-authoritative. |
| `docs/runbook.md`, `docs/REPLICATING.md` | Stale operational exports | Cloud/live/network commands are forbidden and not contract authority. |
| `benchmarks/**` | Reference terrain | Standards inform; they do not command or prove mastery. |
| `dist/hermes-thrice-great-profile/` | Generated output | Never source authority; never committed. |

## Release boundary

Contract work may describe skill packaging and staging requirements, but C3 does not copy or package production-profile skills. The repository root remains non-installable. Only the later approved source selection may feed the allowlisted staging builder.
