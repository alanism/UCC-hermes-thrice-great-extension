from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_public_presentation_states_identity_authority_and_safety_boundary():
    soul = (REPO_ROOT / "SOUL.md").read_text(encoding="utf-8")
    assert soul.startswith("# Hermes Thrice Great for UnCommon Core")
    assert "default install/profile name is `ucc`" in soul
    assert "proven for synthetic offline workflows only" in soul
    assert "not yet approved for real learner data" in soul
    assert "zero live model calls and zero network calls" in soul
    assert "The system validates evidence and proposes; the parent approves." in soul
    assert "thoth" not in soul.casefold()


def test_distribution_and_plugin_keep_public_identity_and_zero_tool_surface():
    distribution = (REPO_ROOT / "distribution.yaml").read_text(encoding="utf-8")
    plugin = (REPO_ROOT / "plugins" / "hermes-thrice-great" / "plugin.yaml").read_text(encoding="utf-8")
    assert "name: hermes-thrice-great" in distribution
    assert "deterministic evidence engine for UnCommon Core" in distribution
    assert "proven for synthetic offline workflows only" in distribution
    assert "name: hermes-thrice-great" in plugin
    assert "Hermes Thrice Great for UnCommon Core" in plugin
    assert "provides_tools: []" in plugin
    assert "provides_hooks: []" in plugin
