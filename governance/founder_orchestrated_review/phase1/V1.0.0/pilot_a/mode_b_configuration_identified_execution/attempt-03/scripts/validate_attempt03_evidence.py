#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[6]
AUTH_SOURCE = Path("/Users/rianray/.codex/attachments/ebc83d30-8d27-4463-98d4-33f53f459b3c/pasted-text.txt")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(ROOT.name == "attempt-03", f"unexpected evidence root: {ROOT}")
    require(not any(path.is_symlink() for path in ROOT.rglob("*")), "symlink found in evidence package")

    json_files = sorted(ROOT.rglob("*.json"))
    parsed = {path.relative_to(ROOT).as_posix(): json.loads(path.read_text(encoding="utf-8")) for path in json_files}
    require(len(json_files) >= 7, "too few JSON artifacts")

    for path in sorted(ROOT.rglob("*.csv")):
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        require(len(rows) >= 2, f"CSV has no data rows: {path}")
        width = len(rows[0])
        require(width > 0 and all(len(row) == width for row in rows), f"CSV width mismatch: {path}")

    invocation = parsed["MODE_B_INVOCATION_EVIDENCE.json"]
    require(invocation["model_requests"] == 0, "model request count is not zero")
    require(invocation["model_responses"] == 0, "model response count is not zero")
    require(invocation["canonical_roles_executed"] == 0, "role execution count is not zero")
    require(invocation["phase_2_activity"] == 0, "Phase 2 activity is not zero")
    require(invocation["provider_bound_preflight_requests"] == 2, "provider-bound request count mismatch")

    violation = parsed["preflight/PROVIDER_PREFLIGHT_VIOLATION.json"]
    require(violation["result"] == "FAIL", "provider prohibition is not failed")
    require(violation["qualification_effect"] == "BLOCK_ALL_ROLE_MODEL_PROVIDER_EXECUTION", "qualification effect mismatch")
    require(violation["packets_modified_after_failure"] is False, "packet mutation recorded after failure")

    manifests = sorted((ROOT / "packet_manifests").glob("ES-RA-*_INPUT_MANIFEST.json"))
    envelopes = sorted((ROOT / "control_envelopes").glob("ES-RA-*_CONTROL_ENVELOPE.txt"))
    require(len(manifests) == 4, "packet-manifest count mismatch")
    require(len(envelopes) == 4, "control-envelope count mismatch")
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        require(manifest["attempt_id"] == "ES-PH1-PILOT-A-MODE-B-ATTEMPT-03", f"attempt mismatch: {manifest_path}")
        require(manifest["starting_commit"] == "dc5dc547df84eca59c265c355f86331f80c2ee59", f"commit mismatch: {manifest_path}")
        require(manifest["hidden_oracle_included"] is False, f"oracle leak declaration: {manifest_path}")
        require(manifest["other_role_canaries_included"] == [], f"cross-canary declaration: {manifest_path}")
        require(manifest["other_role_outputs_included"] == [], f"cross-output declaration: {manifest_path}")

    role_rows = list(csv.DictReader((ROOT / "MODE_B_ROLE_CONFIGURATION_REGISTER.csv").open("r", encoding="utf-8", newline="")))
    require(len(role_rows) == 4, "role register count mismatch")
    require(all(row["execution_status"] == "NOT_ATTEMPTED" for row in role_rows), "role register overclaims execution")

    preflight_rows = list(csv.DictReader((ROOT / "preflight/MODE_B_PREFLIGHT_CHECKS.csv").open("r", encoding="utf-8", newline="")))
    failures = [row for row in preflight_rows if row["result"] == "FAIL"]
    require(len(failures) == 1 and failures[0]["control_id"] == "A03-PF-026", "preflight failure set mismatch")
    require(any(row["result"] == "NOT_COMPLETED" for row in preflight_rows), "stopped controls not disclosed")

    auth_copy = ROOT / "authority/FOUNDER_AUTHORIZATION_RECEIVED_TRANSCRIPTION.md"
    require(sha256(auth_copy) == sha256(AUTH_SOURCE), "Founder authorization transcription bytes differ")
    require((ROOT / "oracle/MODE_B_ATTEMPT_03_HIDDEN_DEFECT_ORACLE.csv").is_file(), "oracle evidence missing")
    require("PILOT_A_CONFIGURATION_IDENTIFIED_EXECUTION_BLOCKED" in (ROOT / "PHASE_1_MODE_B_FOUNDER_PACKAGE.md").read_text(encoding="utf-8"), "blocked disposition missing")

    attempt01 = "governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-01"
    attempt02 = "governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-02"
    historical = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--exit-code", "--quiet", "HEAD", "--", attempt01, attempt02],
        check=False,
    )
    require(historical.returncode == 0, "Attempt 01 or Attempt 02 differs from HEAD")

    print(json.dumps({
        "result": "PASS",
        "evidence_root": str(ROOT),
        "json_files_parsed": len(json_files),
        "packet_manifests": len(manifests),
        "control_envelopes": len(envelopes),
        "role_executions": 0,
        "provider_prohibition_failure_preserved": True,
        "attempt_01_and_02_unchanged": True,
    }, indent=2))


if __name__ == "__main__":
    main()
