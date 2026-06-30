---
name: parent_progress_brief
description: "Convert UCC telemetry, assessment results, or ledger entries into a clear parent-facing explanation of how a child is doing — for the parent of the child, for prospective parents evaluating the system, or for a public blog post."
version: 1.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ucc, parent, progress, brief, telemetry, blog, narrative, pitch]
    related_skills: [school_model_canvas_interpreter, mastery_ledger_contract]
---

# Parent Progress Brief

## Overview

Convert UCC telemetry, assessment results, or ledger entries into a clear parent-facing explanation of how a child is doing.

Three distinct output shapes:

1. **Progress Brief** (internal) — for the parent of the specific child. Strengths, weaknesses, next actions.
2. **Family Diary / Weekly Chronicle** (public-facing) — for blog posts or social media. Chronological narrative of what happened, what the system revealed, what the parent did.
3. **Prospective-Parent Pitch** (persuasive) — for demos, testimonials, or marketing. Shows what the system saw, what the parent did, and what changed. Designed to be compelling to a parent evaluating whether to adopt.

Do not use this skill for technical architecture or product specs.

---

## Shape 1: Progress Brief (Internal / Current Parent)

### Procedure

1. Summarize current status
2. Separate strength, weakness, and uncertainty
3. Explain evidence in plain language
4. Recommend next work
5. Identify what to watch
6. Keep the parent action-oriented

### Output Format

- **Bottom line**: one-sentence status summary
- **Strengths**: what the child does well, with evidence
- **Weaknesses**: where the child struggles, with evidence
- **Evidence**: the telemetry that supports these claims
- **This week's work**: recommended focus areas
- **Parent move**: one action the parent can take this week
- **Watch item**: what to monitor for signs of progress or regression

---

## Shape 2: Family Diary / Weekly Chronicle (Public-Facing / Blog)

**When to use:** The parent asks for a "diary of what we did this week" or "something for my blog post." The audience is other parents or a personal audience, not the system.

### Procedure

1. **Scan the week.** Check kanban board completed tasks, saved telemetry receipts, coaching conversations, and cron nudge records. Note gaps (days with no system activity).
2. **Lead with the narrative arc.** What was the most significant learning event this week? Open with that. The diary is a story, not a log.
3. **Anchor each day with what happened chronologically**, but compress quiet days into a single line.
4. **For assessment days, show the contrast:** what the surface score says vs what the telemetry actually revealed. This is the core insight that makes the diary worth reading.
5. **Show the parent-in-the-loop.** When the parent coached between rounds (Feynman dialogue, conversation, practice), document that explicitly. The reader needs to see that the system doesn't replace the parent — it equips the parent.
6. **End with a "what this demonstrates" section** — the system sees X, the parent did Y, the outcome was Z. This readers a reason to care.

### Output Format

- **Day-by-day narrative** — chronological, compress quiet days
- **Key assessment breakdown** — what the numbers say vs what the errors reveal
- **Parent coaching moment** — what the parent did between rounds
- **Diagnosis correction** (if applicable) — system learned something that changed the plan
- **How Hermes Thrice Great worked** — for transparency, show the loop: receipt → deterministic analysis → proposal → parent decision → validation
- **What a prospective parent should take from this** — optional closing section if the brief doubles as a marketing testimonial

**Pitfall:** Don't just log raw events. Every event needs interpretation — not "she scored 62%" but "she scored 62%, and every error was the same type, which revealed something the score alone couldn't."

**Pitfall:** Don't write the blog post for the parent. Write raw material they can pull from — tables, insights, the narrative arc. They'll do the final edit.

---

## Shape 3: Prospective-Parent Pitch (Persuasive / Testimonial)

**When to use:** The parent asks for "insights that would be insightful for a parent thinking about adopting our system." The audience is a prospect evaluating UCC. The goal is persuasion through evidence.

### Procedure

1. **Start with what a conventional system would say** (a single score, a grade, a vague "needs practice"). This establishes the contrast.
2. **Show what the telemetry actually revealed** — the error pattern, the failure stage, the hidden diagnosis. Use a table.
3. **Show the diagnosis correction** (if applicable). Systems that learn from data and revise their model of the child are more trustworthy than systems that lock in a first impression.
4. **Show the parent's role.** The system gave a specific coaching script. The parent ran it. The child retested. This is the parent-as-coach model in action — the most persuasive thing to another parent.
5. **Show the outcome.** Did performance change? Did the diagnosis hold or shift? Use the pressure delta as a concrete metric.
6. **End with the contrast table:** What a conventional system gives (score) vs what UCC gives (diagnosis + script + validation loop).

### Output Format

| Section | Content |
|---------|---------|
| **Surface reading** | What a grade or score would say |
| **Real diagnosis** | What telemetry revealed (error pattern, failure stage, hidden ceiling) |
| **Diagnosis correction** | If the system revised its understanding of the child |
| **Parent coaching moment** | What the parent did between rounds — concrete, specific, not abstract |
| **Outcome under pressure** | Did the coaching hold when the timer started? |
| **The system loop** | Receipt → diagnosis → script → coaching → retest → validation |
| **What a conventional system says** | Single score, vague recommendation, no parent role |
| **What UCC says** | Specific pattern, specific script, validated outcome |

**Key rhetorical move:** Frame every finding as "most systems would see X, but this one saw Y." The parent reading this needs to feel that the system sees their child with more resolution than a test score can.

**Pitfall:** Don't sell. Show evidence and let the evidence persuade. Avoid superlatives ("amazing", "revolutionary"). The tables and the delta values do the work.

**Pitfall:** Don't skip the diagnosis correction if one happened. A system that revises its model of a child is *more* credible, not less — it shows it's data-driven, not fixed.

---

## Cross-Shape Principles

- All three shapes must label evidence. Use the M/C/M/F/N framework where precision matters: Measured (raw fact), Calculated (arithmetic), Modeled (pattern), Forecasted (prediction), Noted (human observation).
- All three shapes must show the parent's role. The system does not replace the parent — it equips the parent.
- All three shapes must be truthful. No invented data, no inflated claims, no certainty where the sample is small.
- When the audience is prospective (Shape 3), the tone is calmer and more metric-driven than Shape 1. Let the data persuade, not adjectives.
