# Root Documentation Classification

Status: BINDING UNTIL A CLAIMED DOCUMENTATION REWRITE

Date: 2026-06-30

The root documents are retained unchanged as historical/product-intent sources. They are not installation, runtime, security, or implementation authority.

## `README.md`

Classification: **historical product vision; partially obsolete**.

Retain as intent:

- Hermes Thrice Great is an educational/UCC extension;
- macro, meso, and micro pedagogical scales are product concepts;
- School Model Canvas, campaign, and assessment concepts are source requirements subject to later contract design.

Do not rely on as current fact:

- calling this repository a source-code “fork” of Hermes;
- listing Discord as the implemented primary front end;
- describing current `skills/` content as Python skills;
- implying the depicted repository tree is an implemented runtime.

Current authority is the zero-touch pinned-Hermes profile/plugin topology and generated staging payload in `TOPOLOGY_DECISION.md` and `STAGING_PAYLOAD_POLICY.md`.

## `INSTALL.md`

Classification: **obsolete and unsafe as an installation runbook**.

The following instructions are not approved:

- cloning or installing Hermes from the network;
- `npm install`, ad hoc `pip install`, or updating the pinned runtime;
- cloning this repository into a Hermes skills directory;
- installing the repository root as a profile;
- creating Discord credentials/channels or performing live Discord actions;
- creating a real `.env` with tokens;
- invoking nonexistent `setup.sh`, `setup.py`, `/hermes ping`, or claimed layer-status behavior.

No current user installation guide exists. The only proven development-time install path is: generate `dist/hermes-thrice-great-profile/` with the allowlisted builder, scan it, and install that staging tree into an isolated temporary Hermes home. Product installation documentation is future claimed work after profile implementation and acceptance.

## Precedence

On conflict, `docs/active/authority.json` and its binding artifacts win. Neither root document may be used to bypass dependency gates, privacy controls, the staging boundary, the exact Hermes pin, or the prohibition on live integrations.
