import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HERMES_SOURCE = Path.home() / "AppData" / "Local" / "hermes" / "hermes-agent"
HERMES_PYTHON = HERMES_SOURCE / "venv" / "Scripts" / "python.exe"
HERMES_EXE = HERMES_SOURCE / "venv" / "Scripts" / "hermes.exe"
INSTALL_NAMES = ["ucc", "hermes-thrice-great", "thoth"]


def checkout_identity():
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=HERMES_SOURCE,
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"], cwd=HERMES_SOURCE,
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return {"head": head, "dirty": bool(dirty)}


def semantic_hashes(root):
    selected = ["SOUL.md", "distribution.yaml", "config.yaml", "skills", "plugins"]
    result = {}
    for relative in selected:
        path = root / relative
        files = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
        for item in files:
            if "__pycache__" not in item.parts:
                relative_path = item.relative_to(root).as_posix()
                content = item.read_bytes()
                if relative_path == "distribution.yaml":
                    text = content.decode("utf-8")
                    lines = text.splitlines()
                    lines[0] = "name: <profile-name>"
                    content = ("\n".join(lines) + "\n").encode("utf-8")
                result[relative_path] = hashlib.sha256(content).hexdigest()
    return result


def test_real_installs_are_semantically_equivalent_and_stock_identity_is_unchanged(tmp_path):
    before = checkout_identity()
    staging = tmp_path / "hermes-thrice-great-profile"
    built = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "build_profile_staging.py"), "--source", str(REPO_ROOT), "--output", str(staging)],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    assert built.returncode == 0, built.stderr
    home = tmp_path / "hermes-home"
    install_env = os.environ.copy()
    install_env.update({"HERMES_HOME": str(home), "HERMES_SAFE_MODE": "1", "HERMES_ENABLE_PROJECT_PLUGINS": "0"})
    install_code = (
        "import json,sys; from hermes_cli.profile_distribution import install_distribution; "
        "p=install_distribution(sys.argv[1],name=sys.argv[2]); "
        "print(json.dumps({'profile_name':p.manifest.name,'target':str(p.target_dir)}))"
    )
    installed = []
    for name in INSTALL_NAMES:
        completed = subprocess.run(
            [str(HERMES_PYTHON), "-B", "-c", install_code, str(staging), name],
            cwd=HERMES_SOURCE, env=install_env, capture_output=True, text=True, check=False,
        )
        assert completed.returncode == 0, completed.stderr
        installed.append(json.loads(completed.stdout.strip().splitlines()[-1]))
    assert [item["profile_name"] for item in installed] == INSTALL_NAMES
    roots = [Path(item["target"]) for item in installed]
    baseline_hashes = semantic_hashes(roots[0])
    assert all(semantic_hashes(root) == baseline_hashes for root in roots[1:])

    sentinel = tmp_path / "sentinel"
    sentinel.mkdir()
    marker = sentinel / "network-attempts.txt"
    (sentinel / "sitecustomize.py").write_text(
        "import os,socket\n"
        "def blocked(self,address):\n"
        "    with open(os.environ['HTG_NETWORK_MARKER'],'a',encoding='utf-8') as handle: handle.write(repr(address)+'\\n')\n"
        "    raise RuntimeError('offline alias proof blocked network')\n"
        "socket.socket.connect=blocked\n",
        encoding="utf-8",
    )
    outputs = []
    for root in roots:
        (root / "config.yaml").write_text(
            'agent:\n  disabled_toolsets: ["*"]\nplatform_toolsets:\n  cli: []\nplugins:\n  enabled: [hermes-thrice-great]\n  disabled: []\nmcp_servers: {}\n',
            encoding="utf-8",
        )
        env = os.environ.copy()
        env.update({
            "HERMES_HOME": str(root), "HERMES_ENABLE_PROJECT_PLUGINS": "0",
            "PYTHONPATH": str(sentinel), "PYTHONDONTWRITEBYTECODE": "1",
            "HTG_NETWORK_MARKER": str(marker),
        })
        completed = subprocess.run(
            [str(HERMES_EXE), "ucc", "doctor"], cwd=HERMES_SOURCE, env=env,
            capture_output=True, text=True, check=False, timeout=20,
        )
        assert completed.returncode == 0, completed.stderr
        outputs.append(json.loads(completed.stdout.strip().splitlines()[-1]))
    assert outputs[0] == outputs[1] == outputs[2]
    assert outputs[0]["network_attempts"] == outputs[0]["model_calls"] == outputs[0]["ledger_writes"] == 0
    assert not marker.exists()
    assert checkout_identity() == before == {
        "head": "2a5dc0ef3df433a36abed9ee544ea067d807c438",
        "dirty": False,
    }
