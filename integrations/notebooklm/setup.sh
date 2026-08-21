#!/usr/bin/env bash
set -euo pipefail
# Hermes Thrice Great — NotebookLM DLC one-shot setup
# Mirrors the local install at ~/projects/gemini-notebook-mcp-cli (0.9.4)

echo "== Hermes Thrice Great — NotebookLM setup =="

if command -v nlm >/dev/null 2>&1; then
  echo "✓ nlm found: $(which nlm) ($(nlm --version 2>&1 | head -n1))"
else
  echo "→ installing notebooklm-mcp-cli via uv..."
  if command -v uv >/dev/null 2>&1; then
    uv tool install notebooklm-mcp-cli
  elif command -v pipx >/dev/null 2>&1; then
    pipx install notebooklm-mcp-cli
  else
    pip install notebooklm-mcp-cli
  fi
fi

echo ""
echo "→ checking auth..."
if nlm login --check 2>&1 | grep -q "Cookies: present"; then
  echo "✓ already authenticated"
else
  echo "→ launching browser auth (nlm login)..."
  nlm login
fi

echo ""
echo "→ doctor..."
nlm doctor || true

echo ""
echo "→ MCP setup hints:"
echo "  nlm setup add claude-code   # or gemini | cursor | windsurf | codex | opencode"
echo "  nlm setup list"
echo "  nlm skill install claude-code"
echo ""
echo "Manual JSON is at integrations/notebooklm/mcp.json.example"
echo "Docs: integrations/notebooklm/README.md and coach-cards/workflows/_textbook_workflow.md"
echo "Done."
