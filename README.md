# Hermes Thrice Great

Hermes Thrice Great is a deterministic UCC evidence engine delivered as a profile distribution for stock Hermes Agent. This release proves synthetic, offline workflows on native Windows with `hermes-agent==0.16.0`.

## What this release does

- validates versioned UCC contracts and synthetic assessment evidence;
- separates proposals from authorized adult approval events;
- runs a deterministic seven-stage weekly workflow;
- writes an atomic, idempotent ledger inside isolated synthetic dry runs;
- packages a deliberately generic public skill set; and
- exposes installed-profile `doctor`, `validate`, and `dry-run` commands.

It does not use a model or network to establish facts, approval, or ledger state. It does not detect cheating, AI writing, or ghostwriting.

## Distribution boundary

The repository is the source, governance, and build-control tree. It is never installed as a Hermes profile.

The only installable input is the generated allowlisted payload:

```text
dist/hermes-thrice-great-profile/
```

Build and install instructions are in [INSTALL.md](INSTALL.md). Operational verification and recovery procedures are in [the owner runbook](docs/active/OWNER_RUNBOOK.md).

The public/default profile name is `ucc`. `hermes-thrice-great` is an equivalent public alias. `thoth` is optional, non-default, and local-only.

## Release scope

This is a production distribution proof for synthetic offline workflows. It is not evidence of readiness for real or semi-real learner data, live messaging, Campaign OS, external adapters, AI tutoring, or network-dependent operation. Hermes itself remains stock and pinned; this repository is a profile/plugin distribution, not a Hermes fork.

Hermes Thrice Great F1 is a technical evaluator release for synthetic offline workflows. It proves install, doctor, validation, adversarial validation, explicit fixture validation, seven-stage dry-run, approval separation, deterministic outputs, atomic local ledger behavior, zero model calls, and zero network calls in the proven CLI path. It is not authorized for real learner data, family deployment, or school deployment.

Final acceptance is **F1 PASS** at repository commit `693de12b9a2c954f3ed3546e167b0f6ebcfdde90`, with zero critical risks. Stock Hermes remains pinned to `hermes-agent==0.16.0` at commit `2a5dc0ef3df433a36abed9ee544ea067d807c438`. T4.11, I10.1, I10.2, and Phase 10 remain excluded.

## Evaluator Quickstart

Build and install only the generated staging payload by following [INSTALL.md](INSTALL.md). Never install the repository root.

```powershell
python .\scripts\build_profile_staging.py --source (Get-Location).Path --output .\dist\hermes-thrice-great-profile
python -m pytest -q tests\red\t4_8\test_distribution_red.py -k repository_root_install
hermes ucc doctor
hermes ucc validate --synthetic
hermes ucc validate --synthetic --case invalid_totals
hermes ucc validate --fixture valid/week.json
hermes ucc validate --fixture adversarial/week-cases.json
hermes ucc dry-run --synthetic
```

The pytest command verifies the repository-root rejection policy; it does not install anything. The two adversarial validation commands must exit nonzero with stable issue codes. Use only the bundled labeled synthetic fixtures—never real or semi-real learner data.

## Companion Resources

### UCC Assessment Lab

[UCC Assessment Lab](https://ucc-assessment-test-notebook-598682781761.asia-southeast1.run.app/)

After installing Hermes Thrice Great, technical evaluators may use the UCC Assessment Lab web app to generate or review assessment-style workflows outside the local Hermes distribution.

This Assessment Lab link is an external web app and is not part of the F1 synthetic-offline Hermes Thrice Great proof. Using it requires internet access. Do not upload real learner data unless a future real-data release explicitly authorizes that workflow.

Share this link manually through the family’s or evaluator’s chosen communication channel. Automated messaging adapters are not included in this release.

Future adapter releases may automate link delivery after separate privacy, messaging, and network gates pass.

## Optional Curriculum DLC / Benchmark Packs

[California Common Core Curriculum + Singapore MoE Curriculum DLC](https://drive.google.com/file/d/1GBaPp2mE3vfUhX-yk9H8S4ZUZdN2CzpG/view?usp=sharing)

This DLC package contains optional benchmark/curriculum modules for California Common Core and Singapore Ministry of Education curriculum alignment.

The DLC is a companion curriculum/benchmark pack. It is not hardcoded into the Hermes Thrice Great core. The F1 release proves the deterministic synthetic-offline evidence engine, not real learner deployment or full curriculum planning.

## GitHub Repository

- Public display name: **Hermes Thrice Great extension**
- Repository slug: `hermes-thrice-great-extension`
- Suggested description: “Technical synthetic-offline evaluation release of Hermes Thrice Great, the deterministic evidence engine for UnCommon Core.”

This repository is for technical evaluation of the synthetic offline distribution. Do not use real learner data.

The repository must remain private unless the human explicitly authorizes a public GitHub release. Publication and connection instructions are in [the release-sharing guide](docs/active/RELEASE_SHARING.md).

## License

See [LICENSE](LICENSE).
