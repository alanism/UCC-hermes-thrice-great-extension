import argparse
import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "hermes-thrice-great"


class NativeContextProbe:
    def __init__(self):
        self.cli_commands = []
        self.slash_commands = []
        self.tools = []

    def register_cli_command(self, name, help, setup_fn, handler_fn=None, description=""):
        self.cli_commands.append({"name": name, "help": help, "setup_fn": setup_fn, "handler_fn": handler_fn, "description": description})

    def register_command(self, *args, **kwargs):
        self.slash_commands.append((args, kwargs))

    def register_tool(self, *args, **kwargs):
        self.tools.append((args, kwargs))


def load_plugin():
    sys.path.insert(0, str(PLUGIN_ROOT))
    spec = importlib.util.spec_from_file_location(
        "hermes_thrice_great_native",
        PLUGIN_ROOT / "__init__.py",
        submodule_search_locations=[str(PLUGIN_ROOT)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_native_registration_exposes_only_offline_ucc_cli(capsys):
    context = NativeContextProbe()
    load_plugin().register(context)
    assert [item["name"] for item in context.cli_commands] == ["ucc"]
    assert context.slash_commands == []
    assert context.tools == []
    command = context.cli_commands[0]
    parser = argparse.ArgumentParser()
    command["setup_fn"](parser)
    for argv in (["doctor"], ["validate", "--synthetic"], ["dry-run", "--synthetic"]):
        args = parser.parse_args(argv)
        assert command["handler_fn"](args) == 0
        result = json.loads(capsys.readouterr().out.strip())
        assert result["status"] == "ok"
        assert result["model_calls"] == result["network_attempts"] == result["ledger_writes"] == 0
