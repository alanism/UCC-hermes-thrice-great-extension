# Replicating the Hermes_Thrice_Great System

A step-by-step guide for setting up your own personalized education orchestration system using Hermes Agent.

---

## 1. Define Your School Model Canvas (SMC)

Start by understanding your learner and your educational context.

1. Copy the template: `cp templates/SMC-TEMPLATE.md smc/[LEARNER_NAME]-smc.md`
2. Fill out every section honestly — **this document drives everything else**.
3. Keep it in version control and revisit it each term.

**Key outcome:** A completed SMC that answers *who you're teaching, how you teach, and what matters.*

---

## 2. Deploy the Campaign OS App

The Campaign OS app is the web-based dashboard for creating and managing weekly plans.

1. Clone or copy the app to your server/local machine.
2. Install dependencies (see Campaign OS README).
3. Configure the app to read from your SMC directory.
4. Expose the app (local network or cloud) so Hermes can reach its API/webhook.

**Key outcome:** A running Campaign OS instance where you can create weekly plans and Hermes can read them.

---

## 3. Set Up Discord

Discord serves as the communication layer between you, your learner (indirectly), and Hermes.

1. Create a Discord server (or use an existing one).
2. Create the channels as documented in `discord/channel-architecture.md`.
3. Create a Discord bot application at https://discord.com/developers/applications.
4. Invite the bot to your server with appropriate permissions.
5. Note the channel IDs (right-click channel → Copy ID with Developer Mode enabled).
6. Configure the gateway as documented in `discord/gateway-setup.md`.

**Key outcome:** A Discord server with 6 channels, a connected bot, and the gateway configured.

---

## 4. Connect Hermes

Wire Hermes Agent to your SMC, Campaign OS, and Discord.

1. Ensure Hermes is installed and configured.
2. Create or update your Hermes profile:
   ```bash
   hermes profile use thoth-big-pc
   ```
3. Set environment variables in your profile's `.env`:
   - Discord bot token
   - Allowed channel IDs
   - Campaign OS webhook URL
   - Path to SMC directory
4. Create the cron jobs:
   ```bash
   # Assessment nudge (Sunday 18:00 UTC)
   hermes cron create --name "assessment-nudge" --schedule "0 18 * * 0" --profile thoth-big-pc --action '...'

   # Self-heal (every 4 hours)
   hermes cron create --name "self-heal" --schedule "0 */4 * * *" --profile thoth-big-pc --action '...'
   ```
5. Test the connection:
   ```bash
   hermes discord send --channel [PARENT_AGENT_CHANNEL_ID] --message "Hermes is online."
   ```

**Key outcome:** Hermes is connected to Discord, has cron jobs active, and can read your SMC and Campaign OS.

---

## 5. Run Your First Week

1. Open Campaign OS and create a weekly plan using the template at `templates/campaigns/example-weekly-plan.json`.
2. Fill in real dates, activities, and standards aligned to your SMC.
3. Save the plan so Hermes can discover it.
4. Throughout the week:
   - Follow the schedule in the weekly plan.
   - Run assessments in CALM mode.
   - Log observations in the `#learner-journal` Discord channel.
5. At the end of the week, review the telemetry receipt (see `templates/telemetry/example-receipt.json` for format).

**Key outcome:** One complete week of planned instruction, assessment, and reflection.

---

## 6. Iterate

Education is never "done" — iterate continuously.

1. **Weekly review:** At the end of each week, review:
   - Was the weekly plan realistic?
   - Did the learner engage well with the activities?
   - What needs to change for next week?
2. **SMC revision:** Update the SMC when your learner's needs or your approach changes significantly.
3. **Campaign refinement:** Adjust campaign difficulty, pacing, and activities based on assessment data.
4. **Automation improvements:** Tweak cron schedules, add new cron jobs, or refine the self-heal script.

---

## File Map

```
Hermes_Thrice_Great/
├── smc/                          # Your completed School Model Canvases
│   └── [LEARNER_NAME]-smc.md
├── templates/                    # Templates for new files
│   ├── SMC-TEMPLATE.md
│   ├── campaigns/
│   │   └── example-weekly-plan.json
│   └── telemetry/
│       └── example-receipt.json
├── cron/                         # Cron job documentation
│   ├── assessment-nudge-pattern.md
│   └── self-heal-pattern.md
├── discord/                      # Discord setup docs
│   ├── channel-architecture.md
│   └── gateway-setup.md
├── benchmarks/                   # Assessment item packs
│   └── README.md
├── scripts/                      # Automation scripts
│   └── self-heal.sh
├── items/                        # Downloaded assessment items
│   ├── math/
│   └── ela/
└── logs/                         # Runtime logs
    └── self-heal.log
```

## Tips

- **Start small.** Run the system for 2–3 weeks before adding advanced automation.
- **Use version control.** This entire directory should be a Git repository.
- **Keep the SMC alive.** It's a living document — update it as you learn.
- **CALM mode is key.** Assessments should feel low-pressure and learner-led.
- **Ask for help.** If something breaks, the Hermes Agent docs and community are your first stop.
