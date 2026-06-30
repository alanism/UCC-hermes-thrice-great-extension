"""Verify the pinned Hermes deny-all tool baseline without network access."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import socket
import subprocess
import sys
from pathlib import Path


PINNED_HEAD = "2a5dc0ef3df433a36abed9ee544ea067d807c438"


def git(source: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(source), *args], check=True, capture_output=True, text=True
    )
    return completed.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hermes-source", type=Path, required=True)
    parser.add_argument("--temp-home", type=Path, required=True)
    parser.add_argument("--config-source", type=Path)
    args = parser.parse_args()

    source = args.hermes_source.resolve(strict=True)
    temp_home = args.temp_home.resolve(strict=True)
    config_path = temp_home / "config.yaml"
    marker = temp_home / "PLUGIN_EXECUTED"
    plugin_dir = temp_home / "plugins" / "synthetic-blocked"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / "plugin.yaml").write_text(
        "name: synthetic-blocked\nversion: 1.0.0\ndescription: synthetic sentinel\nkind: standalone\n",
        encoding="utf-8",
    )
    (plugin_dir / "plugin.py").write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('unsafe')\ndef register(ctx):\n    pass\n",
        encoding="utf-8",
    )
    if args.config_source is not None:
        config_source = args.config_source.resolve(strict=True)
        config_path.write_bytes(config_source.read_bytes())
    else:
        config_path.write_text(
            "agent:\n"
            "  disabled_toolsets: ['*']\n"
            "platform_toolsets:\n"
            "  cli: []\n"
            "plugins:\n"
            "  enabled: []\n"
            "  disabled: []\n"
            "mcp_servers:\n"
            "  synthetic-blocked:\n"
            "    url: http://127.0.0.1:9/forbidden\n"
            "    enabled: true\n",
            encoding="utf-8",
        )

    os.environ["HERMES_HOME"] = str(temp_home)
    os.environ["HERMES_CONFIG"] = str(config_path)
    os.environ["HERMES_SAFE_MODE"] = "1"
    os.environ["HERMES_ENABLE_PROJECT_PLUGINS"] = "0"
    os.environ.pop("HERMES_PROFILE", None)
    os.environ.pop("HERMES_KANBAN_TASK", None)
    os.chdir(temp_home)
    sys.path.insert(0, str(source))

    network_attempts: list[str] = []

    def blocked_connect(_socket, address):
        network_attempts.append(repr(address))
        raise RuntimeError("network disabled by R4.2 sentinel")

    socket.socket.connect = blocked_connect
    socket.socket.connect_ex = blocked_connect

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        from hermes_cli.config import load_config
        from hermes_cli.plugins import PluginManager
        from hermes_cli.tools_config import _get_platform_tools
        from tools.mcp_tool import _load_mcp_config
        import model_tools

        config = load_config()
        enabled = sorted(_get_platform_tools(config, "cli"))
        disabled = config.get("agent", {}).get("disabled_toolsets", [])
        unrestricted = model_tools.get_tool_definitions(
            enabled_toolsets=None,
            disabled_toolsets=None,
            quiet_mode=True,
            skip_tool_search_assembly=True,
        )
        restricted = model_tools.get_tool_definitions(
            enabled_toolsets=enabled,
            disabled_toolsets=disabled,
            quiet_mode=True,
            skip_tool_search_assembly=True,
        )
        manager = PluginManager()
        manager.discover_and_load()
        mcp_servers = _load_mcp_config()

    head = git(source, "rev-parse", "HEAD")
    clean = git(source, "status", "--porcelain") == ""
    restricted_names = sorted(
        item.get("function", {}).get("name") for item in restricted if item.get("function", {}).get("name")
    )
    report = {
        "hermes_head": head,
        "hermes_clean": clean,
        "unrestricted_tool_count": len(unrestricted),
        "restricted_tool_count": len(restricted),
        "restricted_tool_names": restricted_names,
        "configured_enabled_toolsets": enabled,
        "configured_disabled_toolsets": disabled,
        "plugin_count": len(manager._plugins),
        "plugin_marker_created": marker.exists(),
        "mcp_server_count": len(mcp_servers),
        "network_attempts": len(network_attempts),
    }
    print(json.dumps(report, sort_keys=True))
    passed = (
        head == PINNED_HEAD
        and clean
        and len(unrestricted) > 0
        and not restricted
        and disabled == ["*"]
        and not manager._plugins
        and not marker.exists()
        and not mcp_servers
        and not network_attempts
    )
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
