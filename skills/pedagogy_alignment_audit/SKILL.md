---
name: pedagogy_alignment_audit
description: "Check whether a UCC feature, app, lesson, prompt, or workflow follows UnCommon Core pedagogy."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ucc, pedagogy, audit, alignment]
    related_skills: [feynman_explanation_gate, assessment_app_reviewer]
---

# Pedagogy Alignment Audit

## Overview

Check whether a UCC feature, app, lesson, prompt, or workflow follows UnCommon Core pedagogy.

Do not use this skill for UI polish or copywriting unless the issue affects learning mechanics.

## Procedure

1. Identify intended learning purpose
2. Map to UCC learning principles
3. Identify supported learning function
4. Check feedback loop
5. Check difficulty calibration
6. Check transfer and retention
7. Check parent signal
8. Flag drift and fixes

## Output Format

- **Intended purpose**: what the feature claims to teach
- **UCC principles present**: which of the 10+ principles are active
- **Missing principles**: principles that should be present but aren't
- **False mastery risks**: where the system could misreport competence
- **Evidence gaps**: where an output lacks learner thinking, explanation, transfer, revision judgment, or validated independent performance
- **Parent signal**: whether the parent gets actionable information
- **Required fixes**: specific changes to restore alignment

---

## Reference: Probabilistic Fallback Design Principle

UCC does not police AI use or detect cheating. When auditing a feature that involves receipt quality, assessment interpretation, or practice generation, distinguish useful AI-assisted output from valid mastery evidence. Consult `references/probabilistic-fallback-design.md` for the degraded/void evidence-state rationale. Key check items:

- When deterministic validation fails, does the feature hide the score? (Required)
- Does it label every claim as `[PROBABILISTIC]` or `[D]`? (Required)
- Does it cap practice scope (6 items max, concrete stage) when degraded? (Required)
- Does it require parent acknowledgment before acting on degraded evidence? (Required)
- Does it recommend a clean rerun? (Required)
- Does it distinguish degraded (evidence exists) from void (no evidence)? (Required)
