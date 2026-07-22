#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat


REPO = Path("/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_execution.nosync/EquineSync-V4")
RUNTIME = Path("/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_runtime.nosync")
AUTHORIZATION = Path("/Users/rianray/.codex/attachments/ebc83d30-8d27-4463-98d4-33f53f459b3c/pasted-text.txt")
PHASE1 = REPO / "governance/founder_orchestrated_review/phase1/V1.0.0"
AGENT_CONFIG = REPO / "governance/founder_orchestrated_review/agent_config/V1.0.0"
EXPECTED_COMMIT = "dc5dc547df84eca59c265c355f86331f80c2ee59"
EXPECTED_ORACLE_SHA256 = "6451ffe911c607a6cef66ecc0604abfc965fb8ff33a78eb88db285ab2180ac51"

ROLES = {
    "ES-RA-02": (
        "ES-RA-02_REVIEW_EXECUTION_PROFILE_V1.0.0.json",
        "ES-RA-02_SEGREGATED_REVIEW_AGENT.md",
        "ES-PH1-MB03-CANARY-ESRA02-86f98e1791ca4de7",
    ),
    "ES-RA-03": (
        "ES-RA-03_REVIEW_EXECUTION_PROFILE_V1.0.0.json",
        "ES-RA-03_ADVERSARIAL_CHALLENGE_AGENT.md",
        "ES-PH1-MB03-CANARY-ESRA03-e4a526f98e54400e",
    ),
    "ES-RA-04": (
        "ES-RA-04_REVIEW_EXECUTION_PROFILE_V1.0.0.json",
        "ES-RA-04_MACHINE_VALIDATION_AGENT.md",
        "ES-PH1-MB03-CANARY-ESRA04-6fd55149510c4f31",
    ),
    "ES-RA-05": (
        "ES-RA-05_REVIEW_EXECUTION_PROFILE_V1.0.0.json",
        "ES-RA-05_EVIDENCE_CUSTODIAN.md",
        "ES-PH1-MB03-CANARY-ESRA05-5a80c641614f4c01",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify() -> None:
    require(RUNTIME.name.endswith(".nosync"), "runtime root is not .nosync")
    inputs_root = RUNTIME / "role_inputs"
    outputs_root = RUNTIME / "role_outputs"
    evidence_root = RUNTIME / "evidence"
    oracle_root = RUNTIME / "hidden_oracle"
    for path in (RUNTIME, inputs_root, outputs_root, evidence_root, oracle_root):
        require(path.is_dir(), f"missing directory: {path}")
        require(not path.is_symlink(), f"symlinked directory: {path}")

    all_canaries = {role: values[2] for role, values in ROLES.items()}
    packet_results = []
    source_candidate = PHASE1 / "pilot_a/fixtures/candidate"
    expected_candidate = {
        path.relative_to(source_candidate).as_posix(): sha256(path)
        for path in sorted(source_candidate.rglob("*"))
        if path.is_file()
    }

    for role_id, (profile_name, source_name, own_canary) in ROLES.items():
        packet = inputs_root / role_id
        require(packet.is_dir(), f"missing packet: {role_id}")
        require(not packet.is_symlink(), f"symlinked packet: {role_id}")
        files = [path for path in sorted(packet.rglob("*")) if path.is_file()]
        require(files, f"empty packet: {role_id}")
        require(all(not path.is_symlink() for path in files), f"symlink in packet: {role_id}")
        require(all(not (path.stat().st_mode & stat.S_IWUSR) for path in files), f"writable frozen file: {role_id}")
        require(all(not (path.stat().st_mode & stat.S_IWUSR) for path in packet.rglob("*") if path.is_dir()), f"writable frozen subdirectory: {role_id}")
        require(not (packet.stat().st_mode & stat.S_IWUSR), f"writable packet root: {role_id}")

        manifest_path = packet / "INPUT_MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        require(manifest["attempt_id"] == "ES-PH1-PILOT-A-MODE-B-ATTEMPT-03", f"attempt mismatch: {role_id}")
        require(manifest["role_id"] == role_id, f"role mismatch: {role_id}")
        require(manifest["starting_commit"] == EXPECTED_COMMIT, f"commit mismatch: {role_id}")
        require(manifest["authorized_canary"] == own_canary, f"canary manifest mismatch: {role_id}")
        require(manifest["other_role_canaries_included"] == [], f"cross-canary declaration: {role_id}")
        require(manifest["other_role_outputs_included"] == [], f"cross-output declaration: {role_id}")
        require(manifest["hidden_oracle_included"] is False, f"oracle declaration: {role_id}")

        recorded = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
        actual = {
            path.relative_to(packet).as_posix(): sha256(path)
            for path in files
            if path.name != "INPUT_MANIFEST.json"
        }
        require(recorded == actual, f"manifest bytes or denominator mismatch: {role_id}")
        listing = "".join(f"{actual[path]}  {path}\n" for path in sorted(actual)).encode("utf-8")
        require(hashlib.sha256(listing).hexdigest() == manifest["frozen_file_list_sha256"], f"listing hash mismatch: {role_id}")

        profile_source = PHASE1 / "profiles" / profile_name
        role_source = AGENT_CONFIG / "prompts" / source_name
        profile = json.loads(profile_source.read_text(encoding="utf-8"))
        require(sha256(packet / "ROLE_CONFIGURATION.json") == sha256(profile_source), f"profile file mismatch: {role_id}")
        require(sha256(packet / "ROLE_SOURCE.md") == sha256(role_source), f"role source mismatch: {role_id}")
        require(manifest["profile_checksum"] == profile["profile_checksum"], f"profile payload checksum mismatch: {role_id}")
        require(manifest["profile_file_sha256"] == sha256(profile_source), f"profile file hash mismatch: {role_id}")
        require(manifest["source_sha256"] == sha256(role_source), f"source hash mismatch: {role_id}")
        require(sha256(packet / "FOUNDER_AUTHORIZATION.md") == sha256(AUTHORIZATION), f"authorization mismatch: {role_id}")
        require((packet / "ROLE_CANARY.txt").read_text(encoding="utf-8").strip() == own_canary, f"own canary mismatch: {role_id}")

        packet_text = b"\n".join(path.read_bytes() for path in files)
        for other_role, other_canary in all_canaries.items():
            occurrences = packet_text.count(other_canary.encode("utf-8"))
            if other_role == role_id:
                require(occurrences >= 2, f"own canary absent from packet/manifest: {role_id}")
            else:
                require(occurrences == 0, f"cross-role canary leak {other_role} -> {role_id}")
        require(b"MODE_B_ATTEMPT_03_HIDDEN_DEFECT_ORACLE" not in packet_text, f"oracle filename leak: {role_id}")
        require(b"A03-DEF-" not in packet_text, f"oracle content leak: {role_id}")

        packet_candidate = {
            path.relative_to(packet / "candidate").as_posix(): sha256(path)
            for path in sorted((packet / "candidate").rglob("*"))
            if path.is_file()
        }
        require(packet_candidate == expected_candidate, f"candidate drift: {role_id}")
        output = outputs_root / role_id
        require(output.is_dir() and not output.is_symlink(), f"output directory invalid: {role_id}")
        require(list(output.iterdir()) == [], f"output directory not empty: {role_id}")
        require(bool(output.stat().st_mode & stat.S_IWUSR), f"output directory not writable: {role_id}")
        packet_results.append({
            "role_id": role_id,
            "file_count_including_manifest": len(files),
            "manifest_sha256": sha256(manifest_path),
            "packet_file_list_sha256": manifest["frozen_file_list_sha256"],
            "profile_file_sha256": sha256(profile_source),
            "profile_payload_checksum": profile["profile_checksum"],
            "source_sha256": sha256(role_source),
            "canary_containment": "PASS",
            "output_initially_empty": True,
        })

    oracle = oracle_root / "MODE_B_ATTEMPT_03_HIDDEN_DEFECT_ORACLE.csv"
    require(oracle.is_file() and not oracle.is_symlink(), "oracle missing or symlinked")
    require(sha256(oracle) == EXPECTED_ORACLE_SHA256, "oracle hash mismatch")
    require(not (oracle.stat().st_mode & stat.S_IWUSR), "oracle is writable")
    require(list(evidence_root.iterdir()) == [], "evidence directory not initially empty")
    require(bool(evidence_root.stat().st_mode & stat.S_IWUSR), "evidence directory not writable")

    print(json.dumps({
        "result": "PASS",
        "runtime_root": str(RUNTIME),
        "runtime_root_nosync": True,
        "starting_commit": EXPECTED_COMMIT,
        "packet_results": packet_results,
        "oracle_sha256": sha256(oracle),
        "evidence_initially_empty": True,
    }, indent=2))


if __name__ == "__main__":
    verify()
