# Installation Guide — Hermes Thrice Great

---

## Prerequisites

| Dependency   | Minimum Version | Notes                               |
|--------------|-----------------|-------------------------------------|
| Node.js      | 18.x            | Required by Hermes Agent runtime    |
| Python       | 3.11            | Hermes Agent skills (Python toolkit)|
| Git          | 2.x             | For cloning repositories            |
| Discord Bot  | —               | A registered application + token    |

Verify prerequisites:

```bash
node --version   # → v18.x or higher
python --version # → Python 3.11+
git --version    # → git 2.x
```

---

## Step 1 — Install Hermes Agent (Nous Research)

Follow the official Hermes Agent installation instructions at:

https://hermes-agent.nousresearch.com/docs

In short:

```bash
# Clone the Hermes Agent repository
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# Install dependencies
npm install
pip install -r requirements.txt   # if applicable
```

Make sure Hermes Agent is running and your `hermes` CLI (or desktop app) is functional before proceeding.

---

## Step 2 — Clone Hermes Thrice Great into Your Skills Directory

```bash
# Navigate to your Hermes skills directory
cd /path/to/hermes-agent/skills

# Clone this repository
git clone https://github.com/Aria-EdTech/Hermes_Thrice_Great.git

# Or, if you have a local copy:
# git clone /path/to/local/Hermes_Thrice_Great
```

On Windows (Hermes Desktop App), the skills directory is typically:

```
C:\Users\<you>\.hermes\skills\
```

---

## Step 3 — Set Up Your Discord Bot

1. Go to the **Discord Developer Portal**: https://discord.com/developers/applications
2. Click **New Application** → give it a name (e.g. "Hermes Thrice Great").
3. Go to the **Bot** tab → **Add Bot**.
4. Under the **Bot** tab:
   - Copy the **Token** (you'll need this as `DISCORD_BOT_TOKEN`).
   - Enable **Message Content Intent**, **Server Members Intent**, and **Presence Intent**.
5. Go to the **OAuth2 → URL Generator**:
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Send Messages`, `Read Message History`, `Use Slash Commands`, `Manage Threads`, `Embed Links`, `Attach Files`
   - Use the generated URL to invite the bot to your server.

---

## Step 4 — Configure Discord Channels

Create the following channels in your Discord server:

| Channel               | Purpose                                            |
|-----------------------|----------------------------------------------------|
| `#hermes-control`     | Administrative commands and agent status           |
| `#hermes-macro`       | Macro-layer (year/term) planning and reports       |
| `#hermes-meso`        | Meso-layer (unit/campaign) orchestration           |
| `#hermes-micro`       | Micro-layer (lesson/assessment) interactions       |
| `#hermes-logs`        | Agent activity log and telemetry output            |
| `#hermes-lab`         | Assessment Lab: item generation and scoring        |

---

## Step 5 — Set Environment Variables

Create a `.env` file in the root of your Hermes Agent installation or in the `Hermes_Thrice_Great` folder:

```bash
# Required
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_server_id_here

# Optional but recommended
HERMES_LOG_LEVEL=info
HERMES_SKILLS_DIR=./skills/Hermes_Thrice_Great
```

On Windows, you can also set these through the GUI or via PowerShell:

```powershell
$env:DISCORD_BOT_TOKEN="your_token_here"
$env:DISCORD_GUILD_ID="your_guild_id_here"
```

---

## Step 6 — Run the Setup Script

If a `setup.sh` or `setup.py` is provided in the repository:

```bash
cd /path/to/hermes-agent/skills/Hermes_Thrice_Great
python setup.py      # or bash setup.sh
```

This will:
- Verify all required environment variables are set.
- Register Discord slash commands.
- Create default configuration files.
- Validate the three-layer schema definitions.

---

## Step 7 — Verify the Installation

1. Restart your Hermes Agent instance so it picks up the new skills.
2. In your Discord server, go to `#hermes-control` and send:

```
/hermes ping
```

You should receive a response like:

```
🏛️ Hermes Thrice Great — UCC Pedagogy Extension
Status: ✅ Online
Layers: Macro ✅ | Meso ✅ | Micro ✅
Discord: Connected | Latency: 42ms
```

If the command succeeds, the installation is complete.

---

## Troubleshooting

| Symptom                     | Likely Cause                     | Fix                                      |
|-----------------------------|----------------------------------|------------------------------------------|
| Bot does not respond        | Token missing or invalid         | Re-check `DISCORD_BOT_TOKEN`             |
| Slash commands not found    | Commands not registered          | Re-run setup script                      |
| Skill not loaded            | Wrong skills directory           | Confirm `HERMES_SKILLS_DIR` path         |
| Permission errors           | Missing intents / bot perms      | Re-check Developer Portal settings       |
| Layer status shows ❌       | Schema validation failed         | Check `schemas/` for broken YAML/JSON    |
