"""Native offline Hermes Thrice Great CLI registration."""

from .hermes_thrice_great.plugin.commands import handle_cli, setup_cli


def register(ctx):
    """Register one offline CLI tree and no agent, gateway, hook, or tool surface."""
    ctx.register_cli_command(
        "ucc",
        "Offline deterministic UCC validation commands",
        setup_cli,
        handler_fn=handle_cli,
        description="Doctor, validate, and dry-run the local synthetic UCC core.",
    )
