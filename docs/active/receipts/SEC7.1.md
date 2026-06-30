# Receipt: SEC7.1

Agent: `codex-sec7-green-01`

Completed: `2026-06-30T19:25:20Z`

## Result

PASS. The actual distribution `config.yaml` mechanically produces a zero-tool offline Hermes surface under the pinned runtime.

## Evidence

- Actual-config and adversarial synthetic-config restriction tests: 2 passed in 5.74 seconds.
- Final restricted tool definitions: zero.
- Web, browser, terminal, messaging, Discord, MCP, and project-plugin surfaces: absent.
- Plugin discovery and MCP server counts: zero under safe mode.
- Socket-connect sentinel attempts: zero.
- Hermes remains clean at `2a5dc0ef3df433a36abed9ee544ea067d807c438`.

Pinned Hermes resolves the stock `kanban` platform name before final filtering; the `disabled_toolsets: ["*"]` final subtraction removes it and every other tool. No Docker/container isolation is claimed.

## Next task

SEC7.2 Windows path containment and log-redaction guards.
