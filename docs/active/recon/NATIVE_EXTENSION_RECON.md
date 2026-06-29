# Native Skill, Plugin, Profile-Name, and Config Recon

Task: H1.4

Date: 2026-06-30 local / 2026-06-29 UTC

## Result

PASS for compatibility characterization. This does not approve or implement product behavior.

## Native skill format and discovery

Pinned Hermes reads profile skills from `<HERMES_HOME>/skills` (`hermes_constants.py:406`), walks nested skill directories for `SKILL.md` while excluding dependency/cache/VCS paths (`agent/skill_utils.py:632`), and parses YAML frontmatter (`agent/skill_utils.py:88`).

An isolated installed profile containing `skills/native-probe/SKILL.md` was discovered through `iter_skill_index_files()`. Frontmatter `name`, `description`, and `platforms: [windows]` parsed correctly, and the platform predicate accepted it on native Windows.

## Plugin opt-in and command surfaces

Pinned Hermes discovers user plugins beneath `<HERMES_HOME>/plugins` through `PluginManager` (`hermes_cli/plugins.py:1087,1118`). Standalone user plugins are opt-in through `plugins.enabled` (`hermes_cli/plugins.py:198`); `plugins.disabled` is an explicit deny and wins over enablement (`hermes_cli/plugins.py:182`).

The synthetic `hermes-thrice-great` plugin contained only an inert `register(ctx)` function. With the plugin named in `plugins.enabled`, discovery reported:

- source `user`;
- kind `standalone`;
- enabled `true`;
- no load error;
- one registered in-session command.

The same registration also exposed a synthetic CLI subcommand through `PluginContext.register_cli_command()` (`hermes_cli/plugins.py:390`). The in-session command used `register_command()` (`hermes_cli/plugins.py:415`). Neither command was invoked, and neither contains product behavior.

## Arbitrary profile names

The same generated staging tree was installed as `ucc-probe` and `thoth-probe` under one isolated temporary Hermes root. Both targets remained contained under that root. Installed manifests used the requested names, and SHA-256 hashes for `SOUL.md`, `config.yaml`, the native skill, and both plugin files were identical across names.

Profile naming therefore does not alter the payload. Product code must resolve `HERMES_HOME` and must not hard-code a profile name.

## Restricted configuration keys

The pinned schema defaults `agent.disabled_toolsets` to an empty list (`hermes_cli/config.py:932`). The synthetic installed config was read back as:

- `plugins.enabled: [hermes-thrice-great]`
- `plugins.disabled: []`
- `agent.disabled_toolsets: [terminal, browser]`

These are the characterized configuration keys. `SOUL.md` is not an enforcement boundary. The later R4.2 security-baseline task must prove the exact disabled toolsets and containment behavior before implementation readiness; H1.4 does not claim that a particular restriction list is yet sufficient.

## Payload boundary correction

The governance hash inventory is emitted as sibling `dist/hermes-thrice-great-profile.inventory.json`, not inside the Hermes install payload. The staging test now requires exact payload equality with the human allowlist. The synthetic install contained exactly the four root payload files plus the selected skill and plugin files; governance metadata and representative forbidden files were absent.

## Safety

All evidence used synthetic files, local internal APIs, an isolated temporary Hermes root, and the exact pinned checkout. No network, live model, gateway, messaging, learner data, Hermes edit, or persistent profile was involved.
