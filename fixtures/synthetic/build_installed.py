"""Build installed synthetic resources inside the allowlisted plugin payload."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "fixtures" / "synthetic"
TARGET = ROOT / "plugins" / "hermes-thrice-great" / "hermes_thrice_great" / "resources" / "synthetic"


def load(relative: str):
    return json.loads((SOURCE / relative).read_text(encoding="utf-8"))


def canonical_hash(value) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def clean_extensions(value):
    if isinstance(value, dict):
        return {key: clean_extensions(item) for key, item in value.items() if key != "extensions"}
    if isinstance(value, list):
        return [clean_extensions(item) for item in value]
    return value


if TARGET.exists():
    shutil.rmtree(TARGET)
TARGET.mkdir(parents=True)

documents = {
    "valid/smc.json": load("valid/smc.json"),
    "valid/calm-receipt.json": load("valid/calm-receipt.json"),
    "valid/pressure-receipt.json": load("valid/pressure-receipt.json"),
    "valid/pairing.json": load("valid/pairing.json"),
    "valid/proposal.json": load("valid/proposal.json"),
    "valid/approval.json": load("valid/approval.json"),
    "valid/ledger.json": load("valid/ledger.json"),
    "valid/workflow.json": load("valid/workflow.json"),
    "valid/week.json": load("valid/week.json"),
    "adversarial/week-cases.json": load("adversarial/week-cases.json"),
}

documents["valid/week.json"]["inputs"] = {
    key: f"valid/{Path(value).name}"
    for key, value in documents["valid/week.json"]["inputs"].items()
}
documents["valid/pairing.json"]["calm_receipt"] = "valid/calm-receipt.json"
documents["valid/pairing.json"]["pressure_receipt"] = "valid/pressure-receipt.json"
documents["valid/workflow.json"]["inputs"] = {
    "receipt": "valid/calm-receipt.json",
    "pair": "valid/pairing.json",
    "proposal": "valid/proposal.json",
}
documents["adversarial/week-cases.json"]["base_week"] = "valid/week.json"

proposal = documents["valid/proposal.json"]["ucc_parent_proposal"]
proposal["smc_ref"]["source_path"] = "valid/smc.json"
projection = clean_extensions(proposal)
projection.pop("canonical_hash")
projection.pop("proposal_status")
proposal["canonical_hash"] = canonical_hash(projection)

approval = documents["valid/approval.json"]["ucc_parent_approval_event"]
approval["proposal_hash"] = proposal["canonical_hash"]
approval_projection = clean_extensions(approval)
approval_projection.pop("canonical_hash")
approval["canonical_hash"] = canonical_hash(approval_projection)

for relative, document in documents.items():
    path = TARGET / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

schema_target = TARGET / "schema" / "contract-registry.v1.schema.json"
schema_target.parent.mkdir(parents=True)
shutil.copy2(ROOT / "schemas" / "contract-registry.v1.schema.json", schema_target)

files = [
    {"path": path.relative_to(TARGET).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    for path in sorted(TARGET.rglob("*"))
    if path.is_file()
]
manifest = {
    "schema_version": "ucc.installed_synthetic_manifest.v1.0.0",
    "synthetic_set_id": "ucc-synthetic-week-v1",
    "distribution_id": "hermes-thrice-great",
    "files": files,
}
manifest["canonical_hash"] = canonical_hash(manifest)
(TARGET / "manifest.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
