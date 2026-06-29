# Archive Hygiene Check

Date:
Active plan hash:
Overall: PASS / FAIL

- [ ] `docs/active/` exists.
- [ ] Exactly one active `BUILD_PLAN.md` exists.
- [ ] Exactly one active `PROJECT_TASKS.md` exists.
- [ ] `authority.json` names and hashes every binding artifact.
- [ ] `docs/archive/` exists or is explicitly declared empty.
- [ ] Root contains no competing build plan or task board.
- [ ] `.agentignore` excludes `docs/archive/` and generated private-data paths.
- [ ] `.agent/claims/` exists.
- [ ] `.agent/state.log` exists.
- [ ] Superseded artifacts are listed by `authority.json`.
- [ ] Attached/chat-only plans are not treated as authority.

Failures:
