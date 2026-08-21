# NotebookLM Integration — Optional DLC for Hermes Thrice Great

> Connect Hermes Thrice Great to **Google NotebookLM / Gemini Notebook** via the `notebooklm-mcp-cli` bridge.
> This powers the **Textbook Factory** (`coach-cards/workflows/_textbook_workflow.md`) — turning any world-class thinker's NotebookLM notebook into a 12-chapter interactive textbook, delivered weekly via cron.

**Status:** Optional — not part of the F1 synthetic-offline proof. Enable only when you have internet + a Google account.

**Upstream:** [`jacob-bd/gemini-notebook-mcp-cli`](https://github.com/jacob-bd/gemini-notebook-mcp-cli) (MIT) — forked to [`alanism/gemini-notebook-mcp-cli`](https://github.com/alanism/gemini-notebook-mcp-cli) for UCC use.

---

## What You Get

| Capability | Example |
|---|---|
| 43 NotebookLM tools in Hermes | `notebook_list`, `notebook_create`, `source_add`, `notebook_query`, `studio_create`, `research_start`, … |
| CLI `nlm` | `nlm notebook list`, `nlm source add`, `nlm studio create` |
| Textbook workflow | Role card → 12-chapter outline → weekly cron delivery (Feynman Mon 6AM, Lockhart Fri 6AM) |
| Local source: `~/projects/gemini-notebook-mcp-cli` | The exact install we run here at `0.9.4` |

---

## Quick Start (mirrors our local setup)

### 1. Install

```bash
# Recommended — uv (also installs `notebooklm-mcp` server)
uv tool install notebooklm-mcp-cli

# Alternatives
pip install notebooklm-mcp-cli
# or without install:
uvx --from notebooklm-mcp-cli nlm --help
```

> After install you get two executables: `nlm` (CLI) and `notebooklm-mcp` (MCP server).

### 2. Authenticate (one-time)

```bash
# Auto — launches Chrome/Arc/Brave/Edge, you log in, cookies extracted
nlm login
nlm login --check          # verify: should show Cookies: present, Account: you@gmail.com
nlm doctor                 # full diagnostics
```

*Multi-account:*
```bash
nlm login --profile work
nlm login --profile personal
nlm login switch work
```

*Manual fallback:*
```bash
nlm login --manual --file cookies.txt
```

Tokens live in `~/.notebooklm-mcp-cli/` and auto-refresh. If calls start failing with auth errors, just `nlm login` again.

### 3. Connect to Hermes (MCP)

**Automatic (recommended):**
```bash
nlm setup add claude-code   # or gemini, cursor, windsurf, cline, antigravity, openclaw
nlm setup list              # verify
```

**Manual JSON** — point any MCP host at `notebooklm-mcp`:

```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "notebooklm-mcp"
    }
  }
}
```

For hosts that don't resolve PATH (Claude Desktop):
```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "/full/path/to/notebooklm-mcp"
    }
  }
}
```
Find it with `which notebooklm-mcp`.

**No-install mode:**
```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "uvx",
      "args": ["--from", "notebooklm-mcp-cli", "notebooklm-mcp"]
    }
  }
}
```

### 4. Install the NotebookLM Skill (so Hermes uses the tools well)

```bash
nlm skill install claude-code   # or codex, opencode, gemini, cline
nlm skill update
```

### 5. Verify

```bash
nlm notebook list
nlm doctor
```

In Hermes, try: *“list my NotebookLM notebooks”* — Hermes should call `notebook_list`.

---

## UCC Textbook Workflow — How We Use It Here

See [`coach-cards/workflows/_textbook_workflow.md`](../../coach-cards/workflows/_textbook_workflow.md) for the full mermaid flow.

**Crons we run locally:**

```bash
# Feynman — Mondays 6AM
cronjob action=create name="feynman-textbook-monday" schedule="0 6 * * 1" \
  skills='["notebooklm"]' workdir="/path/to/Learning_Coach_Heros/STEM_Heroes/Feynman_Textbook/"

# Lockhart — Fridays 6AM
cronjob action=create name="lockhart-textbook-friday" schedule="0 6 * * 5" \
  skills='["notebooklm"]' workdir="/path/to/Learning_Coach_Heros/Math_Council/Lockhart_Textbook/"
```

Each tick: read `_chapter_tracker.txt` → refresh NotebookLM auth → ask NotebookLM for 20 questions + 3 quotes → write `Chapter_NN_*.md` + supplement → bump tracker. Self-contained prompt (no chat memory).

**Cron prompt must handle auth expiry** — check `nlm login --check` and re-login path.

---

## Hermes Profile Config (optional DLC — not enabled by default)

The F1 `config.yaml` ships with `mcp_servers: {}` and `disabled_toolsets: ["*"]` for the offline proof — that's correct.

To enable NotebookLM as an **opt-in DLC**, don't edit the built payload. Instead, overlay on your local profile:

```yaml
# ~/.hermes/profiles/ucc/config.yaml (example overlay — not committed)
mcp_servers:
  notebooklm-mcp:
    command: notebooklm-mcp
    # or: ["uvx", "--from", "notebooklm-mcp-cli", "notebooklm-mcp"]
```

Or use `nlm setup add <client>` which writes the host's own MCP config (separate from Hermes profile). See [`mcp.json.example`](./mcp.json.example).

---

## Files in This Folder

| File | Purpose |
|---|---|
| `README.md` | This guide |
| `mcp.json.example` | Copy-paste MCP server JSON for any host |
| `setup.sh` | One-shot installer: checks `nlm`, installs if missing, runs `nlm doctor` |

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Authentication expired` | `nlm login` again; cookies rotate every few weeks |
| `notebooklm.google.com` vs `notebook.google.com` redirect | `notebooklm-mcp-cli >=0.9` handles both; run `uv tool upgrade notebooklm-mcp-cli` |
| Two `notebooklm` MCP servers registered | Remove legacy `notebooklm-mcp-server` / `notebooklm-cli` packages, keep only `notebooklm-mcp-cli` |
| Chrome profile lock (`Exit code 21`) | Close Chrome, `nlm login` again; Snap Chromium users get auto-redirect |
| Blind “Hermes picked wrong tool” | Rename server to `notebooklm-mcp` (not generic `notebooklm`) |

Full docs: [MCP Guide](https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/MCP_GUIDE.md) · [Authentication](https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md) · [Getting Started](https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/GETTING_STARTED.md)

---

## Fork Notes

Forked from `jacob-bd/gemini-notebook-mcp-cli` at `0.9.4` (2026-07-29 local `~/projects/gemini-notebook-mcp-cli`). This folder does **not** vendor the code — it documents the bridge and points at the fork at `alanism/gemini-notebook-mcp-cli`. For vendoring or submodule: `git submodule add https://github.com/alanism/gemini-notebook-mcp-cli.git integrations/notebooklm-mcp`.

---

## Safety

This integration uses internal, undocumented NotebookLM `batchexecute` APIs. Google may break it without notice. Use for personal/experimental purposes. Keep `~/.notebooklm-mcp-cli/` private (it holds cookies).
