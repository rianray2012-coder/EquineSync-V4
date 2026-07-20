#!/usr/bin/env python3
"""Capture SHA-256 evidence for immutable inputs from the starting Git commit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


STARTING_COMMIT = "e93d3acc65a45835d3f3c63473f5dd98e1d1bcf5"
SCRIPT = Path(__file__).resolve()
RUN_ROOT = SCRIPT.parent.parent
REPO = SCRIPT.parents[6]
OUTPUT = RUN_ROOT / "baseline" / "BASELINE_BYTE_MANIFEST.json"

PATHS = [
    "AGENTS.md",
    ".codex/config.toml",
    ".codex/agents",
    "governance/founder_orchestrated_review/RUNTIME_PERMISSION_CONTROL.md",
    "governance/founder_orchestrated_review/agent_config/V1.0.0",
    "governance/founder_orchestrated_review/agent_config/packages",
    "governance/founder_orchestrated_review/activation/runs/FORA-ACT-2026-001",
    "governance/founder_orchestrated_review/activation/scripts",
    "governance/founder_orchestrated_review/runtime_remediation",
]


def git(*args: str, binary: bool = False):
    completed = subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True,
        check=True,
        text=not binary,
    )
    return completed.stdout


def category(path: str) -> str:
    if path.startswith("governance/founder_orchestrated_review/agent_config/V1.0.0/"):
        return "sealed_package"
    if path.startswith("governance/founder_orchestrated_review/agent_config/packages/"):
        return "approved_package_artifacts"
    if path.startswith(".codex/agents/"):
        return "registered_role_files"
    if "/activation/runs/FORA-ACT-2026-001/" in path:
        return "prior_activation_evidence"
    if "/runtime_remediation/" in path:
        return "prior_runtime_and_calibration_evidence"
    if path.endswith("config.toml") or "/activation/scripts/" in path:
        return "runtime_or_launcher_configuration"
    return "orchestration_configuration"


def main() -> int:
    lines = git("ls-tree", "-r", "--full-tree", STARTING_COMMIT, "--", *PATHS).splitlines()
    entries = []
    for line in lines:
        metadata, path = line.split("\t", 1)
        mode, object_type, object_id = metadata.split()
        if object_type != "blob":
            continue
        content = git("show", f"{STARTING_COMMIT}:{path}", binary=True)
        entries.append(
            {
                "path": path,
                "category": category(path),
                "git_mode": mode,
                "git_blob": object_id,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    counts = {}
    for entry in entries:
        counts[entry["category"]] = counts.get(entry["category"], 0) + 1
    result = {
        "schema_version": "1.0.0",
        "run_id": "FORA-REMEDIATION-2026-001",
        "source_commit": STARTING_COMMIT,
        "entry_count": len(entries),
        "category_counts": counts,
        "entries": entries,
        "status": "PASS",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "entries": len(entries), "status": "PASS"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
