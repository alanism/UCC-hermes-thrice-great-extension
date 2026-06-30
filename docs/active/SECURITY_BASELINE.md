# Hermes Security Baseline

Status: R4.2 PASS

Runtime: `hermes-agent==0.16.0`, clean checkout `2a5dc0ef3df433a36abed9ee544ea067d807c438`

## Enforceable readiness baseline

The Stage 4 baseline is deny-all:

```yaml
agent:
  disabled_toolsets: ["*"]
platform_toolsets:
  cli: []
plugins:
  enabled: []
  disabled: []
mcp_servers: {}
```

Offline verification additionally sets `HERMES_SAFE_MODE=1` and `HERMES_ENABLE_PROJECT_PLUGINS=0`. In pinned Hermes, safe mode prevents plugin discovery and causes MCP configuration loading to return no servers. The `*` toolset alias resolves all current and future toolsets, and `model_tools.get_tool_definitions()` applies disabled toolsets as a final subtraction.

This is an execution-readiness baseline, not the final distribution configuration. Phase 7 may minimally enable only the production `hermes-thrice-great` plugin after its RED tests exist. It may not enable terminal, file, browser, web, messaging, model, MCP, adapter, or other Hermes toolsets merely to make product tests pass.

## Mechanical proof

An isolated temporary Hermes home contained both an enabled synthetic MCP endpoint and a synthetic user plugin whose module would write a marker if imported. Under the baseline:

- unrestricted pinned Hermes exposed 27 tool definitions;
- the restricted session exposed zero tool definitions;
- plugin discovery produced zero plugins and the import marker remained absent;
- MCP loading produced zero servers;
- a patched socket sentinel recorded zero connection attempts;
- the Hermes checkout remained clean at the pinned commit.

The restricted platform resolver still named `kanban` and the synthetic MCP key before final subtraction. This is why an empty platform list alone is insufficient. The deny-all `agent.disabled_toolsets` layer and safe-mode MCP/plugin gates are mandatory for this proof baseline.

## Windows containment decision

Docker is unavailable on the acceptance host, and pinned Hermes has no native WSL terminal backend. R4.2 therefore does not claim container isolation. It prevents the model from receiving any terminal, execution, filesystem, browser, web, messaging, or MCP tool definition. Because no execution tool is exposed, Hermes' default local terminal backend is unreachable through the accepted tool surface.

Future trusted plugin code remains in the Hermes host process. Its deterministic, zero-network and path-containment behavior must be established by Phase 4 RED tests and the Phase 7 privacy/sandbox gate before sensitive-data mode. Prose in `SOUL.md` is never an enforcement boundary.

## Fail-closed conditions

R4 becomes invalid if any of the following occurs:

- the pin or clean checkout changes;
- restricted tool definition count is nonzero;
- plugin code imports under safe mode;
- an MCP server is returned under safe mode;
- any socket connection is attempted by the proof;
- a later profile enables an untested toolset or plugin.
