# Hermes Thrice Great

**A UCC (UnCommon Core) Pedagogy Fork of Nous Research's Hermes Agent**

Hermes Thrice Great extends the open-source Hermes Agent (by Nous Research) with educational scaffolding designed for the UnCommon Core (UCC) learning framework. It transforms a general-purpose AI orchestration agent into a multi-layer classroom companion that operates across three distinct pedagogical scales.

---

## Three-Layer Architecture

| Layer | Scale | Scope |
|-------|-------|-------|
| **Macro** | Academic year / programme | Curriculum design, term planning, school-wide reporting |
| **Meso** | Unit / module | Learning campaigns, milestone tracking, cohort analytics |
| **Micro** | Lesson / session | Real-time tutoring, Socratic prompting, assessment items |

Each layer communicates with the others through defined schemas, enabling coherent progress tracking from a single lesson all the way up to programme-level outcomes.

---

## Core Integrations

- **Discord** — Primary front-end. Interact with the agent through slash commands, threaded conversations, and dedicated channel groups.
- **School Model Canvas (SMC)** — Strategic planning tool that maps institutional goals down to daily delivery.
- **Learning Campaign OS** — Campaign-based orchestration for meso-layer unit delivery (quests, milestones, XP-style progress).
- **Assessment Lab** — Micro-layer engine for generating, administering, and analysing formative and summative assessment items aligned to UCC standards.

---

## Repository Structure

```
Hermes_Thrice_Great/
├── README.md
├── LICENSE
├── INSTALL.md
├── skills/               # Custom Hermes skills (Python)
├── templates/
│   ├── campaigns/        # Learning campaign templates
│   └── telemetry/        # Telemetry & analytics templates
├── schemas/              # Cross-layer data schemas
├── discord/              # Discord bot config & handlers
│   └── self-heal/        # Auto-recovery scripts
├── cron/                 # Scheduled tasks
├── benchmarks/           # Performance benchmarks & test data
└── docs/                 # Extended documentation
```

---

## Getting Started

See [INSTALL.md](./INSTALL.md) for setup instructions.

---

## License

MIT — see [LICENSE](./LICENSE) for details.
