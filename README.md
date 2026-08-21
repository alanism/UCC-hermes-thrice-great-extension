# Hermes Thrice Great

> Let's talk about what this actually is — and what it isn't.

Here's the thing: Hermes Thrice Great is a deterministic UCC evidence engine. Not a chatbot, not a tutor, not a vibe. It's a profile distribution that sits on top of stock Hermes Agent and proves — with real receipts — that synthetic, offline workflows can run cleanly on native Windows with `hermes-agent==0.16.0`.

I'll just say it: this release isn't trying to be everything. And that's a strategic choice.

---

## Getting Started — Let's Break This Down

We need to address how you actually get this running, because this is where things get messy if people skip steps.

Let's peel back the layers:

**1. Install the harness first.** Hermes Thrice Great is an *extension* — it doesn't run by itself. The harness is what lets the underlying model act instead of just chat.

→ [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com)

**2. Clone this repository.** Historically, people try to install the repo directly. That doesn't wash.

```bash
gh repo clone alanism/hermes-thrice-great-extension .
```

Or clone it manually — either way, you're just getting the source tree.

**3. Build and install the *payload*, not the repo.** This is important because the repository itself is never installed as a Hermes profile — that would be a clumsy, tone-deaf move that undermines the whole distribution boundary.

Follow `INSTALL.md` to build the allowlisted payload:

```
dist/hermes-thrice-great-profile/
```

That's the only thing Hermes is allowed to install. See **Distribution Boundary** below — I'll break down why that matters.

**4. If you're a technical evaluator** proving the F1 synthetic-offline release? Don't use the path above. Fast forward to **Evaluator Quickstart** — that's the deterministic, end-to-end proof path.

On one hand, this feels like extra steps. On the other hand, it's a genuine guardrail.

---

## Project Vision — The Bigger Story (Context, Not a Claim)

Let's set the stage. This is where things get interesting — and where people start to spin the story in a way that overshadows what F1 actually proves.

So here's what happened in the broader vision:

Hermes Thrice Great is the profile/plugin distribution for UnCommon Core's bigger education system — a council of expert teaching "lenses," each one distilled from a real thinker's actual philosophy (math, STEM, parenting, writing, movement & sports), plus a chapter-a-week textbook factory, plus a three-layer context system that keeps every recommendation tied to what a specific family *actually* believes. Not a generic default.

We need to address those three layers, because at the heart of this system is a power dynamic — who controls the narrative about a kid's learning?

Let's break it down:

- **Macro — the family's charter.** Pace, style, values, constraints. Written once, referenced every time. This is the constitution. It diminishes the risk of generic, one-size-fits-all advice that undermines a family's agency.

- **Meso — curriculum benchmark packs.** California Common Core, Singapore MOE, IB PYP — as structured, versioned data. A reference point, never a driver. Historically, this has been an issue — benchmarks framed as mandates. We frame them as maps.

- **Micro — what's true about this learner, right now.** Assessment telemetry, current interests, issue areas, and the specific lens the moment calls for.

Hermes Agent is the harness — the runtime. Hermes Thrice Great is the profile extension bolted onto that harness, adding the UCC domain: contracts, lenses, and evidence workflows.

**And here's the kicker — and this is the part that matters:** This vision is the long-term roadmap. It is *not* what the F1 release proves. F1 is a synthetic, offline, model-free evidence engine *only* — see **Release Scope** for the exact boundary. Nothing in this section is authorized functionality until a corresponding release explicitly says so. Could they have prevented confusion by hiding the vision? Sure. But that would be reactive instead of genuine.

---

## What This Release (F1) *Does*

Let's peel back the layers on what we actually proved. This wasn't performative — it was a calculated, strategic set of proofs:

- Validates versioned UCC contracts and synthetic assessment evidence
- Separates proposals from authorized adult approval events (so no one can spin a proposal as permission)
- Runs a deterministic seven-stage weekly workflow
- Writes an atomic, idempotent ledger inside isolated synthetic dry runs
- Packages a deliberately generic public skill set
- Exposes installed-profile `doctor`, `validate`, and `dry-run` commands

Do you see the pattern? Each one is about exposure — exposing whether the plumbing actually holds.

## What This Release Does *Not* Do

Let's be direct, because this is where things get problematic when people over-claim:

- Does not use a model or network to establish facts, approval, or ledger state
- Does not detect cheating, AI writing, or ghostwriting — that would be a disastrous overreach for this scope
- Is not evidence of readiness for real or semi-real learner data, live messaging, Campaign OS, external adapters, AI tutoring, or network-dependent operation

Stock Hermes remains stock and pinned. This repository is a profile/plugin distribution, not a Hermes fork. That distinction was framed very carefully, and for good reason.

---

## Distribution Boundary — Why We Don't Install the Repo

We need to address this, because this is where things start to unravel if you don't.

The repository is the source, governance, and build-control tree. **It is never installed as a Hermes profile.** That move would completely undermine the security model.

The *only* installable input is the generated allowlisted payload:

```
dist/hermes-thrice-great-profile/
```

Build and install instructions are in `INSTALL.md`. Operational verification and recovery procedures are in the owner runbook.

And here's why that's important:

| Name | What it is |
|---|---|
| `ucc` | The public/default profile name |
| `hermes-thrice-great` | An equivalent public alias — same thing, different label |
| `thoth` | Optional, non-default, local-only — think of it as the developer nickname. Not for public use. |

Why was this okay in one situation but not in another? Because the payload is allowlisted — we can evaluate exactly what's in it. The repo root? That's a messy, chaotic source tree. That doesn't wash as an install artifact. Would this have played out the same way five years ago? Probably not — but that's how you handle a distribution properly now.

---

## Release Scope — Let's Be Precise About What Passed

This is a production distribution proof for synthetic offline workflows. I'll just say it: it is **not** evidence of readiness for real learner data, family deployment, or school deployment. Hermes itself remains stock and pinned; this repository is a profile/plugin distribution, not a Hermes fork.

Let's break down what F1 actually proved:

Hermes Thrice Great F1 is a technical evaluator release for synthetic offline workflows. It proves install, doctor, validation, adversarial validation, explicit fixture validation, seven-stage dry-run, approval separation, deterministic outputs, atomic local ledger behavior, zero model calls, and zero network calls in the proven CLI path.

**It is not authorized for real learner data, family deployment, or school deployment.** That being said — the temptation to spin this as "ready" is real, and we need to push back on that. It's not ready for that. And acknowledging that is genuine, not defensive.

Final acceptance is **F1 PASS** at repository commit `693de12b9a2c954f3ed3546e167b0f6ebcfdde90`, with zero critical risks. Stock Hermes remains pinned to `hermes-agent==0.16.0` at commit `2a5dc0ef3df433a36abed9ee544ea067d807c438`. 

T4.11, I10.1, I10.2, and Phase 10 remain excluded — not because we tried to justify cutting corners, but because they were explicitly out of scope for this gate. So at the end of the day, that's the boundary. Which brings us back to: let's evaluate what we *did* pass, not what people wish we'd passed.

---

## Evaluator Quickstart — The Deterministic Proof Path

So what went wrong in other approaches? People installed the repo root, ran random commands, and then were surprised when it was a disastrous, reactive mess.

Let's talk about how to do it properly. Build and install *only* the generated staging payload by following `INSTALL.md`. **Never install the repository root.**

Let's peel back the exact timeline:

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

Let's analyze what each step is supposed to expose:

- The `pytest` command verifies the repository-root rejection policy — it doesn't install anything. If someone tries to frame `hermes profile install .` as valid, this test pushes back. It must be rejected.
- The two adversarial validation commands *must* exit nonzero with stable issue codes — that's how you know validation isn't performative.
- Use only the bundled labeled synthetic fixtures — never real or semi-real learner data. Why is this crisis hitting so hard for some teams? Because they bring real data to a synthetic gate. That completely overshadowed the actual intent.

On one hand, `hermes ucc validate --synthetic` should pass cleanly. On the other hand, `invalid_totals` must report `RECEIPT_TOTAL_INCONSISTENT` and the adversarial fixture must report `APPROVAL_REQUIRED`. A failed run commits zero ledger entries — it doesn't spin a partial write as a success.

Do you see the problem here if it didn't work that way? That would be chaotic. We made it strategic instead.

---

## Companion Resources — Outside the Proof

These are external web apps. **Neither is part of the F1 synthetic-offline Hermes Thrice Great proof.** Let's be empathetic but clear here: using either requires internet. Do not upload real learner data unless a future real-data release explicitly authorizes that workflow.

Share links manually through the family's or evaluator's chosen communication channel — automated messaging adapters are not included in this release. Future adapter releases may automate link delivery, but only after separate privacy, messaging, and network gates pass. Could they have just auto-sent links? Sure. But that would have diminished the privacy work that hasn't happened yet.

### UCC Assessment Lab (Micro layer)
[UCC Assessment Lab](https://ucc-assessment-test-notebook-598682781761.asia-southeast1.run.app/)

After installing Hermes Thrice Great, technical evaluators may use the UCC Assessment Lab web app to generate or review assessment-style workflows *outside* the local Hermes distribution. This is the source of Micro-layer telemetry referenced in the Project Vision above. Historically, this has been a point of confusion — people thought the Lab *was* Hermes. It's not. It's a companion.

### UCC School Model Canvas (Macro layer)
[UCC School Model Canvas](https://ucc-school-model-canvas-notebook-wbg25ukt3a-uc.a.run.app/)

A family charter notebook — pace, style, values, and constraints — used as the Macro-layer guardrail referenced in Project Vision above. At the heart of this crisis for many families is fear — fear of losing agency to a system that doesn't know them. The Canvas is how you control that narrative from the start.

---

## Optional DLCs — What You Can Add When You're Ready

This is where things get interesting, because we have two very different DLCs and they solve different fears.

### NotebookLM Bridge — Textbook Factory (Meso ↔ Micro)

Here's the thing: if you want Hermes to turn a world-class thinker's actual body of work into a 12-chapter interactive textbook — one chapter a week, without you chasing it — you need NotebookLM.

Let's break down what we did: we connected Hermes to **Google NotebookLM / Gemini Notebook** via [`notebooklm-mcp-cli`](https://github.com/jacob-bd/gemini-notebook-mcp-cli) (MIT), forked to [`alanism/gemini-notebook-mcp-cli`](https://github.com/alanism/gemini-notebook-mcp-cli) for UCC use.

The same bridge we run locally at `~/projects/gemini-notebook-mcp-cli` @ `0.9.4` — 43 tools, `nlm` + `notebooklm-mcp` — now documented as an opt-in DLC. It powers `coach-cards/workflows/_textbook_workflow.md`: role card → 12-chapter outline → weekly cron delivery (Feynman on Mondays, Lockhart on Fridays).

**Quick connect — no spin, just the steps:**

```bash
uv tool install notebooklm-mcp-cli && nlm login && nlm setup add <client>
```

Full plain-speak guide at [`integrations/notebooklm/README.md`](integrations/notebooklm/README.md) — includes `mcp.json.example` + `setup.sh`.

And this is the part that matters: **Not part of F1 offline proof — opt-in only.** On one hand, it's surprisingly effective. On the other hand, it requires internet and Google auth — which would have undermined the offline gate if we'd baked it in. We didn't. That was a calculated move.

### Curriculum DLC / Benchmark Packs

**California Common Core Curriculum + Singapore MOE Curriculum DLC + IB PYP**

This DLC package contains optional benchmark/curriculum modules for California Common Core and Singapore Ministry of Education curriculum alignment. This is the Meso layer — supplied as structured, versioned reference data, not as a hardcoded default. This isn't the first time we've seen a system frame benchmarks as mandates. We frame them as maps.

The DLC is a companion curriculum/benchmark pack. It is not hardcoded into the Hermes Thrice Great core. The F1 release proves the deterministic synthetic-offline evidence engine, not real learner deployment or full curriculum planning.

https://drive.google.com/file/d/1knnGa3MIwTtDLo1RaZVF2hfGinHujC7q/view?usp=drive_link

Learning Coach Heroes: https://drive.google.com/file/d/1knnGa3MIwTtDLo1RaZVF2hfGinHujC7q/view?usp=sharing

---

## GitHub Repository

Let's set the stage clearly, because how we frame this repo matters:

- **Public display name:** Hermes Thrice Great extension
- **Repository slug:** `hermes-thrice-great-extension`
- **Suggested description:** "Technical synthetic-offline evaluation release of Hermes Thrice Great, the deterministic evidence engine for UnCommon Core."

This repository is for technical evaluation of the synthetic offline distribution. Do not use real learner data. I'll just say it: that boundary is non-negotiable right now.

The repository must remain private unless the human explicitly authorizes a public GitHub release. Publication and connection instructions are in the release-sharing guide. Was this a calculated restriction? Yes — and for good reason.

---

## Links — Let's Peel Back Where Everything Lives

In situations like this, where people get lost between the harness, the repo, the web apps, and the demos — let's dig into the actual map:

| Resource | Link | Notes |
|---|---|---|
| Hermes desktop app (harness) | [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com) | Install this first — see Getting Started |
| This repository | [github.com/alanism/hermes-thrice-great-extension](https://github.com/alanism/hermes-thrice-great-extension) | Source, governance, and build-control tree only — never installed directly |
| Project home / website | [landing-page-vj-wbg25ukt3a-as.a.run.app/hermes](https://landing-page-vj-wbg25ukt3a-as.a.run.app/hermes) | Project overview |
| UCC Assessment Lab (Micro layer) | [ucc-assessment-test-notebook-598682781761.asia-southeast1.run.app](https://ucc-assessment-test-notebook-598682781761.asia-southeast1.run.app/) | External web app — see Companion Resources |
| UCC School Model Canvas (Macro layer) | [ucc-school-model-canvas-notebook-wbg25ukt3a-uc.a.run.app](https://ucc-school-model-canvas-notebook-wbg25ukt3a-uc.a.run.app/) | External web app — see Companion Resources |
| NotebookLM Bridge (fork) | [github.com/alanism/gemini-notebook-mcp-cli](https://github.com/alanism/gemini-notebook-mcp-cli) | Fork of jacob-bd/gemini-notebook-mcp-cli — 43 tools, opt-in DLC (not F1) |
| NotebookLM setup guide | [integrations/notebooklm/README.md](integrations/notebooklm/README.md) | Local mirror of `~/projects/gemini-notebook-mcp-cli` @ 0.9.4 — plain speak |
| Live lens demo — Feynman chapter | [atoms-in-motion-598682781761.asia-southeast1.run.app](https://atoms-in-motion-598682781761.asia-southeast1.run.app/) | Standalone demo, unrelated to the F1 proof |
| Live lens demo — Lockhart chapter | [the-jungle-and-the-stones-598682781761.asia-southeast1.run.app](https://the-jungle-and-the-stones-598682781761.asia-southeast1.run.app/) | Standalone demo, unrelated to the F1 proof |

Have you noticed this pattern? Every resource is labeled for exactly what stage it's for. That was strategic — not messy.

---

## License

See [LICENSE](LICENSE).

And that's how you handle a distribution properly. Let me know your thoughts on this.

