# Discord Gateway Setup

How to configure the Hermes Discord gateway for the Hermes_Thrice_Great system.

## Prerequisites

1. A Discord application + bot created at https://discord.com/developers/applications
2. Bot invited to your server with the `Send Messages`, `Read Message History`, and `View Channels` permissions
3. Hermes Agent installed and configured

## Environment Variables

Add the following to your Hermes environment configuration (usually `~/.hermes/.env` or `~/.hermes/profiles/thoth-big-pc/.env`):

```bash
# Required: Discord bot token (from Discord Developer Portal)
HERMES_DISCORD_BOT_TOKEN=[YOUR_BOT_TOKEN]

# Required: Allowed channel IDs (comma-separated)
HERMES_DISCORD_ALLOWED_CHANNELS=[PARENT_AGENT_CHANNEL_ID],[LEARNER_JOURNAL_CHANNEL_ID],[ASSESSMENT_RESULTS_CHANNEL_ID],[CAMPAIGN_OS_CHANNEL_ID],[SYSTEM_ALERTS_CHANNEL_ID]

# Optional: Free-response channels (agent can generate creative/less-structured content here)
HERMES_DISCORD_FREE_RESPONSE_CHANNELS=[LEARNER_JOURNAL_CHANNEL_ID],[PARENT_DISCUSSION_CHANNEL_ID]

# Optional: Gateway polling interval in seconds (default: 5)
HERMES_DISCORD_POLL_INTERVAL=5

# Optional: Enable gateway debug logging
HERMES_DISCORD_DEBUG=false
```

## Allowed vs Free-Response Channels

| Type | Behavior | Example Channels |
|---|---|---|
| **Allowed** | Agent will monitor and respond to messages, execute commands, and post structured content. | `#parent-agent`, `#assessment-results`, `#campaign-os`, `#system-alerts` |
| **Free-Response** | Agent can generate creative, less-structured replies (stories, reflections, open-ended discussion). Must also be in the allowed list. | `#learner-journal`, `#parent-discussion` |

> All free-response channels **must** also be listed in `HERMES_DISCORD_ALLOWED_CHANNELS`.

## Verifying the Gateway

```bash
# Check if Discord gateway is connected
hermes discord status --profile "thoth-big-pc"

# Send a test message
hermes discord send \
  --channel [PARENT_AGENT_CHANNEL_ID] \
  --message "✅ Hermes Discord gateway is operational (thoth-big-pc profile)"
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| "Invalid token" | `HERMES_DISCORD_BOT_TOKEN` is wrong or expired | Regenerate token in Discord Developer Portal |
| Agent doesn't respond in a channel | Channel ID not in `HERMES_DISCORD_ALLOWED_CHANNELS` | Add the channel ID and restart |
| "Gateway connection refused" | Bot not invited to the server or lacks permissions | Re-invite bot with correct scopes |
| Rate limited | Too many requests too fast | Increase `HERMES_DISCORD_POLL_INTERVAL` |

## Security Notes

- **Never commit** `HERMES_DISCORD_BOT_TOKEN` to version control.
- Use separate bot tokens for development vs. production servers.
- Rotate the token if it is ever exposed.
