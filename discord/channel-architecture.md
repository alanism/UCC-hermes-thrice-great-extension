# Discord Channel Architecture

Defines the required Discord channels for the Hermes_Thrice_Great system, their purposes, who speaks in each, and tone guidelines.

> **Note:** No real Discord channel IDs appear in this document. All IDs are shown as placeholders — replace them with actual channel IDs during setup.

---

## Channel Table

| # | Channel Name | Purpose | Who Speaks | Tone Guidelines |
|---|---|---|---|---|
| 1 | `#parent-agent` | Primary communication channel between the parent and Hermes agent. Weekly plans, nudge messages, assessment reminders, and general coordination. | Parent, Hermes Agent | Clear, concise, action-oriented. Agent uses task-like formatting with bold headers. |
| 2 | `#learner-journal` | Logged observations, achievements, struggles, and reflections after each session or day. | Parent (writing on behalf of learner), Hermes Agent (summaries) | Reflective, narrative, honest. No judgment. Focus on growth and patterns. |
| 3 | `#assessment-results` | Telemetry receipts and assessment summaries from CALM-mode sessions. | Hermes Agent (posts receipts) | Data-oriented, structured. Use code blocks or embeds for JSON receipts. |
| 4 | `#campaign-os` | Campaign OS app status updates, weekly plan creation notifications, and sync events. | Campaign OS App (webhook), Hermes Agent | Informational, timestamped. Brief bullet points preferred. |
| 5 | `#system-alerts` | Critical alerts: self-heal failures, Discord gateway disconnects, cron job failures, or configuration issues. | Hermes Agent (self-heal script), System | Urgent tone when needed. Use `@here` sparingly — only for actionable failures. |
| 6 | `#parent-discussion` | Parent-only channel for reflection, questions, and collaboration with other parents or mentors (if applicable). | Parent(s), optionally invited mentors | Supportive, collaborative. Agent does **not** post here unless @mentioned. |

---

## Channel ID Placeholders

Use the following placeholders in your Hermes configuration (`.env`, cron commands, etc.):

| Placeholder | Channel |
|---|---|
| `[PARENT_AGENT_CHANNEL_ID]` | `#parent-agent` |
| `[LEARNER_JOURNAL_CHANNEL_ID]` | `#learner-journal` |
| `[ASSESSMENT_RESULTS_CHANNEL_ID]` | `#assessment-results` |
| `[CAMPAIGN_OS_CHANNEL_ID]` | `#campaign-os` |
| `[SYSTEM_ALERTS_CHANNEL_ID]` | `#system-alerts` |
| `[PARENT_DISCUSSION_CHANNEL_ID]` | `#parent-discussion` |

---

## Permission Recommendations

- **`#parent-discussion`** should be private (restricted to parent + invited mentors only).
- **`#system-alerts`** should be visible to the parent and Hermes agent only.
- All other channels can be public to the server (or restricted as desired).

## Channel Order (Recommended)

1. `#parent-agent` (top — most used)
2. `#learner-journal`
3. `#assessment-results`
4. `#campaign-os`
5. `#system-alerts`
6. `#parent-discussion` (bottom, in its own category)
