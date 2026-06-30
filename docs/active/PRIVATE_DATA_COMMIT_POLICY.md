# Private-Data Commit Policy

Status: R4.3 enforced

The repository uses two independent Git controls:

1. `.gitignore` excludes secrets, local environment files, runtime databases, generated output, local/profile state, caches, logs, and private learner-data roots.
2. `.githooks/pre-commit` invokes `scripts/check_staged_private_data.py` against the actual staged-file set. This rejects forbidden paths even if a caller force-adds an ignored file.

The repository-local hook path must remain `core.hooksPath=.githooks`. The checker treats Windows path spelling and case variants equivalently. Public `.env.EXAMPLE`/`.env.template` files and explicitly synthetic contract fixtures outside private roots remain eligible.

## Forbidden commit roots

`outputs/`, `data/`, `learner_data/`, `private/`, `local/`, `sessions/`, `memories/`, `workspace/`, `logs/`, and generated `dist/` are forbidden. Profile secrets/runtime state, `.env`, authentication/credential files, private keys, and runtime databases are also rejected.

## Verification rule

R4.3 uses only synthetic sentinels and a separate temporary Git index initialized from `HEAD`. The real index must remain unchanged. The proof must demonstrate all three outcomes:

- ordinary `git add` refuses the ignored sentinel;
- forced staging into the temporary index succeeds, proving the hook is not tautological;
- the staged-path checker and installed pre-commit hook reject that temporary index.

Changing or bypassing these controls requires explicit human authorization. Agents may strengthen the policy only inside a specifically authorized governance task; implementation claims may not edit it.
