# Hermes Thrice Great

Hermes Thrice Great is a deterministic UCC evidence engine delivered as a profile distribution for stock Hermes Agent. This release proves synthetic, offline workflows on native Windows with `hermes-agent==0.16.0`.

---

## Getting Started

Hermes Thrice Great is an **extension for the Hermes desktop app** — the harness that runs the underlying AI model and lets it act instead of just chat. Install the harness first. This repository only runs on top of it.

1. **Install the Hermes desktop app:** [https://hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com)
2. **Clone this repository** — either manually, or by telling the agent in chat:
   ```
   gh repo clone alanism/hermes-thrice-great-extension .
   ```
3. **Build and install the profile payload.** The repository itself is never installed directly — follow `INSTALL.md` to build the allowlisted `dist/hermes-thrice-great-profile/` payload and install *that*. See **Distribution Boundary** below for why.
4. **Technical evaluators** proving the F1 synthetic-offline release specifically should use the **Evaluator Quickstart** section below instead — it covers the full validation and dry-run proof path end to end.

---

## Project Vision (Context, Not a Claim About This Release)

Hermes Thrice Great is the profile/plugin distribution for UnCommon Core's broader education system: a council of expert teaching "lenses" — each one distilled from a real thinker's actual philosophy (math, STEM, parenting, writing, movement & sports) — plus a chapter-a-week textbook factory and a three-layer context system that keeps every recommendation tied to what a specific family actually believes, not a generic default.

That context system has a name:

- **Macro** — the family's own charter: pace, style, values, constraints. Written once, referenced every time.
- **Meso** — curriculum benchmark packs (California Common Core, Singapore MOE, IB PYP) as structured, versioned data — a reference point, never a driver.
- **Micro** — what's true about a specific learner right now: assessment telemetry, current interests, issue areas, and the specific lens the moment calls for.

Hermes Agent is the harness — the runtime that lets an underlying AI model act instead of just chat. Hermes Thrice Great is a profile extension bolted onto that harness, adding the UCC domain: contracts, lenses, and evidence workflows.

**This vision is the long-term roadmap for the project.** It is not a description of what the F1 release proves. F1 is a synthetic, offline, model-free evidence engine only — see **Release Scope** below for the exact, current boundary. Nothing in this section is authorized functionality until a corresponding release explicitly says so.

---

## What This Release (F1) Does

- Validates versioned UCC contracts and synthetic assessment evidence
- Separates proposals from authorized adult approval events
- Runs a deterministic seven-stage weekly workflow
- Writes an atomic, idempotent ledger inside isolated synthetic dry runs
- Packages a deliberately generic public skill set
- Exposes installed-profile `doctor`, `validate`, and `dry-run` commands

## What This Release Does Not Do

- Does not use a model or network to establish facts, approval, or ledger state
- Does not detect cheating, AI writing, or ghostwriting
- Is not evidence of readiness for real or semi-real learner data, live messaging, Campaign OS, external adapters, AI tutoring, or network-dependent operation

Stock Hermes remains stock and pinned. This repository is a profile/plugin distribution, not a Hermes fork.

---

## Distribution Boundary

The repository is the source, governance, and build-control tree. **It is never installed as a Hermes profile.**

The only installable input is the generated allowlisted payload:

```
dist/hermes-thrice-great-profile/
```

Build and install instructions are in `INSTALL.md`. Operational verification and recovery procedures are in the owner runbook.

The public/default profile name is `ucc`. `hermes-thrice-great` is an equivalent public alias. `thoth` is optional, non-default, and local-only.

---

## Release Scope

This is a production distribution proof for synthetic offline workflows. It is **not** evidence of readiness for real or semi-real learner data, live messaging, Campaign OS, external adapters, AI tutoring, or network-dependent operation. Hermes itself remains stock and pinned; this repository is a profile/plugin distribution, not a Hermes fork.

Hermes Thrice Great F1 is a technical evaluator release for synthetic offline workflows. It proves install, doctor, validation, adversarial validation, explicit fixture validation, seven-stage dry-run, approval separation, deterministic outputs, atomic local ledger behavior, zero model calls, and zero network calls in the proven CLI path. **It is not authorized for real learner data, family deployment, or school deployment.**

Final acceptance is **F1 PASS** at repository commit `693de12b9a2c954f3ed3546e167b0f6ebcfdde90`, with zero critical risks. Stock Hermes remains pinned to `hermes-agent==0.16.0` at commit `2a5dc0ef3df433a36abed9ee544ea067d807c438`. T4.11, I10.1, I10.2, and Phase 10 remain excluded.

---

## Evaluator Quickstart

Build and install only the generated staging payload by following `INSTALL.md`. **Never install the repository root.**

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

The pytest command verifies the repository-root rejection policy; it does not install anything. The two adversarial validation commands must exit nonzero with stable issue codes. Use only the bundled labeled synthetic fixtures — never real or semi-real learner data.

---

## Companion Resources

These are external web apps. **Neither is part of the F1 synthetic-offline Hermes Thrice Great proof.** Using either requires internet access. Do not upload real learner data unless a future real-data release explicitly authorizes that workflow. Share links manually through the family's or evaluator's chosen communication channel — automated messaging adapters are not included in this release. Future adapter releases may automate link delivery after separate privacy, messaging, and network gates pass.

### UCC Assessment Lab (Micro layer)
[UCC Assessment Lab](https://ucc-assessment-test-notebook-598682781761.asia-southeast1.run.app/)

After installing Hermes Thrice Great, technical evaluators may use the UCC Assessment Lab web app to generate or review assessment-style workflows outside the local Hermes distribution. This is the source of Micro-layer telemetry referenced in the Project Vision above.

### UCC School Model Canvas (Macro layer)
[UCC School Model Canvas](https://ucc-school-model-canvas-notebook-wbg25ukt3a-uc.a.run.app/)

A family charter notebook — pace, style, values, and constraints — used as the Macro-layer guardrail referenced in the Project Vision above.

---

## Optional DLCs

### NotebookLM Bridge — Textbook Factory (Meso ↔ Micro)

Connect Hermes to **Google NotebookLM / Gemini Notebook** via [`notebooklm-mcp-cli`](https://github.com/jacob-bd/gemini-notebook-mcp-cli) (forked to [`alanism/gemini-notebook-mcp-cli`](https://github.com/alanism/gemini-notebook-mcp-cli)).

> The same bridge we use locally (`~/projects/gemini-notebook-mcp-cli` @ `0.9.4`, 43 tools, `nlm` + `notebooklm-mcp`). Powers `coach-cards/workflows/_textbook_workflow.md` — role card → 12-chapter outline → weekly cron delivery.

**Quick connect:** `uv tool install notebooklm-mcp-cli && nlm login && nlm setup add <client>` — full guide at [`integrations/notebooklm/README.md`](integrations/notebooklm/README.md) (includes `mcp.json.example` + `setup.sh`). Not part of F1 offline proof — opt-in only.

### Curriculum DLC / Benchmark Packs

**California Common Core Curriculum + Singapore MoE Curriculum DLC + IB PYP**

This DLC package contains optional benchmark/curriculum modules for California Common Core and Singapore Ministry of Education curriculum alignment. This is the Meso layer referenced in the Project Vision above — supplied as structured, versioned reference data, not as a hardcoded default.

The DLC is a companion curriculum/benchmark pack. It is not hardcoded into the Hermes Thrice Great core. The F1 release proves the deterministic synthetic-offline evidence engine, not real learner deployment or full curriculum planning.
https://drive.google.com/file/d/1knnGa3MIwTtDLo1RaZVF2hfGinHujC7q/view?usp=drive_link

Learning Coach Heros:  https://drive.google.com/file/d/1knnGa3MIwTtDLo1RaZVF2hfGinHujC7q/view?usp=sharing

---

## GitHub Repository

- **Public display name:** Hermes Thrice Great extension
- **Repository slug:** `hermes-thrice-great-extension`
- **Suggested description:** "Technical synthetic-offline evaluation release of Hermes Thrice Great, the deterministic evidence engine for UnCommon Core."

This repository is for technical evaluation of the synthetic offline distribution. Do not use real learner data.

The repository must remain private unless the human explicitly authorizes a public GitHub release. Publication and connection instructions are in the release-sharing guide.

---

## Links

| Resource | Link | Notes |
|---|---|---|
| Hermes desktop app (harness) | [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com) | Install this first — see Getting Started |
| This repository | [github.com/alanism/hermes-thrice-great-extension](https://github.com/alanism/hermes-thrice-great-extension) | Source, governance, and build-control tree only — never installed directly |
| Project home / website | [landing-page-vj-wbg25ukt3a-as.a.run.app/hermes](https://landing-page-vj-wbg25ukt3a-as.a.run.app/hermes) | Project overview |
| UCC Assessment Lab (Micro layer) | [ucc-assessment-test-notebook-598682781761.asia-southeast1.run.app](https://ucc-assessment-test-notebook-598682781761.asia-southeast1.run.app/) | External web app — see Companion Resources |
| UCC School Model Canvas (Macro layer) | [ucc-school-model-canvas-notebook-wbg25ukt3a-uc.a.run.app](https://ucc-school-model-canvas-notebook-wbg25ukt3a-uc.a.run.app/) | External web app — see Companion Resources |
| NotebookLM Bridge (fork) | [github.com/alanism/gemini-notebook-mcp-cli](https://github.com/alanism/gemini-notebook-mcp-cli) | Fork of jacob-bd/gemini-notebook-mcp-cli — 43 tools, opt-in DLC (not F1) |
| NotebookLM setup guide | [integrations/notebooklm/README.md](integrations/notebooklm/README.md) | Local mirror of `~/projects/gemini-notebook-mcp-cli` @ 0.9.4 |
| Live lens demo — Feynman chapter | [atoms-in-motion-598682781761.asia-southeast1.run.app](https://atoms-in-motion-598682781761.asia-southeast1.run.app/) | Standalone demo, unrelated to the F1 proof |
| Live lens demo — Lockhart chapter | [the-jungle-and-the-stones-598682781761.asia-southeast1.run.app](https://the-jungle-and-the-stones-598682781761.asia-southeast1.run.app/) | Standalone demo, unrelated to the F1 proof |

---

## License



## License

See [LICENSE](LICENSE).
