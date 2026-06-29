# Self-Heal Cron Pattern

Automatically detects and repairs common Hermes agent issues (stale sessions, misconfigured skills, missing directories, etc.)

## Pattern Overview

The self-heal cron runs on a frequent schedule and executes a self-heal script. If the script detects any issues it can fix automatically, it does so and logs the action.

## Cron Schedule

Recommended: **Every 4 hours** (balances responsiveness with resource usage).

```
 0 */4 * * *
```

## Hermes Cron Create Command

```bash
hermes cron create \
  --name "self-heal" \
  --schedule "0 */4 * * *" \
  --profile "thoth-big-pc" \
  --action '
    # Run the self-heal script
    bash /c/Users/[YOUR_USERNAME]/OneDrive/Documents/Aria-EdTech/Hermes_Thrice_Great/scripts/self-heal.sh \
      --profile "thoth-big-pc" \
      --log /c/Users/[YOUR_USERNAME]/OneDrive/Documents/Aria-EdTech/Hermes_Thrice_Great/logs/self-heal.log
  '
```

## What the Self-Heal Script Checks

| Check | Auto-Fix? | Description |
|---|---|---|
| Hermes agent is responsive | Yes | Restarts the agent daemon if unresponsive |
| Required directories exist | Yes | Creates missing directories (templates, campaigns, telemetry, logs) |
| Kanban board is reachable | No (alerts only) | Logs a warning if the Kanban service is down |
| Profile configuration intact | Yes | Restores missing or corrupted profile config from backup |
| Discord gateway connection | No (alerts only) | Logs if Discord gateway heartbeat has no recent activity |

## Expected Script Location

Place the self-heal script at:

```
Hermes_Thrice_Great/
└── scripts/
    └── self-heal.sh
```

## Example Log Output

```
[2026-06-29 14:00:01] Self-heal starting (profile: thoth-big-pc)
[2026-06-29 14:00:02] ✓ Hermes agent responsive
[2026-06-29 14:00:02] ✓ All required directories exist
[2026-06-29 14:00:03] ✓ Kanban board reachable
[2026-06-29 14:00:03] ✓ Profile config intact
[2026-06-29 14:00:04] ⚠ Discord gateway last heartbeat: 47 min ago (threshold: 60 min)
[2026-06-29 14:00:04] Self-heal complete (0 fixes applied, 1 warning)
```

## Verification

```bash
# Check cron job exists
hermes cron list --profile "thoth-big-pc"

# View last self-heal log
cat /c/Users/[YOUR_USERNAME]/OneDrive/Documents/Aria-EdTech/Hermes_Thrice_Great/logs/self-heal.log

# Force a run
hermes cron run self-heal --profile "thoth-big-pc"
```

## Customization

- **Frequency**: Change `0 */4 * * *` to `0 */1 * * *` for hourly checks, or `0 */12 * * *` for twice-daily.
- **Replace** `[YOUR_USERNAME]` with your actual Windows username (e.g., `jsmith`).
- **Add checks**: Extend the self-heal script with additional validation as needed.
