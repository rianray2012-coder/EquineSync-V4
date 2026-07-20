#!/usr/bin/env python3
"""Hash installed distribution metadata and validate dependency compatibility."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "backend/requirements.txt"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--install-report", type=Path, required=True)
args = parser.parse_args()
report = json.loads(args.install_report.read_text(encoding="utf-8"))
downloads = {}
for item in report.get("install", []):
    name = canonicalize_name(item["metadata"]["name"])
    archive = item.get("download_info", {}).get("archive_info", {})
    hash_value = archive.get("hash") or next(iter((archive.get("hashes") or {}).items()), (None, None))
    if isinstance(hash_value, tuple):
        algorithm, value = hash_value
        hash_value = f"{algorithm}={value}"
    if not isinstance(hash_value, str) or not hash_value.startswith("sha256="):
        raise RuntimeError(f"missing SHA-256 archive hash in pip install report for {name}")
    downloads[name] = hash_value.removeprefix("sha256=")

inventory = []
for raw in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
    raw = raw.strip()
    if not raw or raw.startswith("#"):
        continue
    if "==" not in raw:
        raise RuntimeError(f"unpinned requirement prohibited: {raw}")
    name, expected = raw.split("==", 1)
    distribution = importlib.metadata.distribution(name)
    actual = distribution.version
    if actual != expected:
        raise RuntimeError(f"version mismatch for {name}: expected {expected}, got {actual}")
    metadata = Path(distribution._path) / "METADATA"
    artifact_sha256 = downloads.get(canonicalize_name(name))
    if artifact_sha256 is None:
        raise RuntimeError(f"pip install report missing requirement artifact: {name}")
    inventory.append({
        "name": canonicalize_name(name),
        "version": actual,
        "download_artifact_sha256": artifact_sha256,
        "metadata_sha256": sha(metadata),
    })
print(json.dumps({
    "inventory": sorted(inventory, key=lambda item: item["name"]),
    "dependency_compatibility": {
        "validator": "python -m pip check",
        "requirements_checked": len(inventory),
        "failures": 0,
    },
}, sort_keys=True))
