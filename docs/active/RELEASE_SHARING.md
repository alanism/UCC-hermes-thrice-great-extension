# Release Sharing and GitHub Preparation

Status: private GitHub repository created and connected for accepted-branch publication

## Repository identity

- Display name: **Hermes Thrice Great extension**
- Slug: `hermes-thrice-great-extension`
- Description: **Technical synthetic-offline evaluation release of Hermes Thrice Great, the deterministic evidence engine for UnCommon Core.**
- Initial visibility: **private**
- Created repository: `https://github.com/alanism/hermes-thrice-great-extension`

This repository is for technical evaluation of the synthetic offline distribution. Do not use real learner data.

## GitHub CLI procedure

First confirm that no remote is configured:

```powershell
git remote -v
gh auth status
```

If no remote exists and authentication is unambiguous, create the private repository and push the current branch:

```powershell
gh repo create hermes-thrice-great-extension --private --source . --remote origin --push
```

If `origin` already exists, stop. Do not overwrite or retarget it without human confirmation. Do not use `--public`. Public visibility requires the exact human authorization `PUBLIC GITHUB RELEASE AUTHORIZED`.

## Manual procedure

If GitHub CLI or authentication is unavailable:

1. Create a private GitHub repository named `hermes-thrice-great-extension`.
2. Add that repository as the local `origin` remote.
3. Push the current branch.
4. Reconfirm the synthetic-offline release scope before considering any visibility change.

## Sharing boundary

Private sharing is limited to technical evaluators using labeled synthetic fixtures. The external Assessment Lab and curriculum DLC links are companions only, require internet access, and are outside the F1 proof. No automated messaging, adapters, real learner data, or network-dependent Hermes core behavior is included.
