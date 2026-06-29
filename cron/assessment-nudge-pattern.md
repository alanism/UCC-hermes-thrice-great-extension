# Assessment Nudge Cron Pattern

Sends a weekly reminder to create a Kanban assessment task and deliver a corresponding Discord message.

## Pattern Overview

Every week, the cron job:
1. Creates a Kanban task for the upcoming week's assessment (if one doesn't already exist).
2. Sends a nudge message to the designated Discord channel.

## Cron Schedule

Recommended: **Sunday 18:00 UTC** — gives the parent time to review before Monday.

```
┌───────── minute (0)
│ ┌─────── hour (18)
│ │ ┌───── day of month (*)
│ │ │ ┌─── month (*)
│ │ │ │ ┌─ day of week (0 = Sunday)
 0 18 * * 0
```

## Hermes Cron Create Command

```bash
hermes cron create \
  --name "assessment-nudge" \
  --schedule "0 18 * * 0" \
  --profile "thoth-big-pc" \
  --action '
    # Step 1: Create Kanban task (if not already present this week)
    hermes kanban add \
      --column "Assessment" \
      --title "Weekly Assessment — [Learner Name]" \
      --description "Run this week'\''s assessment items in CALM mode. See /templates/telemetry/example-receipt.json for expected output format." \
      --priority high \
      --profile "thoth-big-pc"

    # Step 2: Send Discord nudge
    hermes discord send \
      --channel [PARENT_AGENT_CHANNEL_ID] \
      --message "📚 **Weekly Assessment Nudge** — [Learner Name]

    A new assessment task has been created in the Kanban board. Please schedule ~20 minutes this week for a CALM-mode session. Review the current weekly plan for topics and standards to assess.

    Use: hermes task run assessment --learner \"[Learner Name]\" --profile thoth-big-pc"
  '
```

## What this produces

| Artifact | Purpose |
|---|---|
| Kanban task in "Assessment" column | Tracks whether the assessment was done this week |
| Discord message | Notifies the parent/agent to take action |

## Customization

- **Change the channel**: Replace `[PARENT_AGENT_CHANNEL_ID]` with the actual Discord channel ID where the parent receives notifications.
- **Change the schedule**: Adjust the cron expression. For a Saturday reminder, use `0 10 * * 6`.
- **Add learner name**: Replace `[Learner Name]` with the actual learner's name throughout.

## Verification

```bash
# List all cron jobs
hermes cron list --profile "thoth-big-pc"

# Check if the assessment nudge is set up
hermes cron describe assessment-nudge --profile "thoth-big-pc"
```
