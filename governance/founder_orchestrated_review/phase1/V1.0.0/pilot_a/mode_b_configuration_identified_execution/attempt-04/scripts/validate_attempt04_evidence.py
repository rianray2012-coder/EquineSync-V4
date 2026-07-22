#!/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[6]
START = "34c427c0196d3f8273ac3ea88ad05a2bbe5a2c29"
AUTH_SOURCE = Path("/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_04_preflight.nosync/FOUNDER_AUTHORIZATION_ATTEMPT_04.md")
REQUIRED_ROLES = {"ES-RA-02", "ES-RA-03", "ES-RA-04", "ES-RA-05"}
QUALIFIED_OUTPUTS = {
    "ES-RA-02": ("ES-RA-02-RETRY-01", "ES-PH1-PILOT-A-MB04-ESRA02-RETRY-01"),
    "ES-RA-03": ("ES-RA-03", "ES-PH1-PILOT-A-MB04-ESRA03-RUN-01"),
    "ES-RA-04": ("ES-RA-04", "ES-PH1-PILOT-A-MB04-ESRA04-RUN-01"),
    "ES-RA-05": ("ES-RA-05", "ES-PH1-PILOT-A-MB04-ESRA05-RUN-01"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(rows, f"CSV contains no data rows: {path}")
    require(None not in rows[0], f"CSV width mismatch: {path}")
    return rows


def main() -> None:
    require(ROOT.name == "attempt-04", f"unexpected root: {ROOT}")
    require(not any(path.is_symlink() for path in ROOT.rglob("*")), "symlink in Attempt 04 package")
    json_files = sorted(ROOT.rglob("*.json"))
    parsed = {path.relative_to(ROOT).as_posix(): json.loads(path.read_text(encoding="utf-8")) for path in json_files}
    for path in sorted(ROOT.rglob("*.csv")):
        csv_rows(path)

    authorization = ROOT / "authority/FOUNDER_AUTHORIZATION_RECEIVED_TRANSCRIPTION.md"
    require(sha256(authorization) == sha256(AUTH_SOURCE), "Founder authorization transcription differs")
    require("Phase 2 remains `NOT_AUTHORIZED`" in authorization.read_text(encoding="utf-8"), "Phase 2 boundary missing")

    preflight = parsed["preflight/FORMAL_NO_PROVIDER_PREFLIGHT.json"]
    counts = preflight["pre_execution_counts"]
    require(preflight["result"] == "PASS", "formal preflight not PASS")
    require(all(counts[key] == 0 for key in counts), f"nonzero pre-boundary count: {counts}")
    require(preflight["local_checks"]["codex_doctor_invocations"] == 0, "codex doctor invocation recorded")
    require(len(preflight["commands_and_processes"]) == 10, "formal preflight command denominator mismatch")
    require(all(command["exit"] == 0 for command in preflight["commands_and_processes"]), "formal preflight command failure")

    boundary = parsed["preflight/AUTHORIZED_EXECUTION_BOUNDARY_RECEIPT.json"]
    require(boundary["result"] == "PASS" and boundary["codex_doctor_invocations"] == 0, "execution boundary invalid")
    require(boundary["phase_2"] == "NOT_AUTHORIZED", "Phase 2 boundary receipt drift")

    role_register = csv_rows(ROOT / "MODE_B_ROLE_CONFIGURATION_REGISTER.csv")
    require({row["role_id"] for row in role_register} == REQUIRED_ROLES, "role register denominator mismatch")
    require(all(row["execution_status"] == "QUALIFIED" for row in role_register), "role register contains nonqualified role")

    validation = parsed["scoring/ROLE_OUTPUT_VALIDATION.json"]
    require(validation["result"] == "PASS" and validation["roles_qualified"] == 4 and validation["replay_qualified"] is True, "role output validation failed")
    for role, (key, execution_id) in QUALIFIED_OUTPUTS.items():
        raw_path = ROOT / "role_outputs" / key / "RAW_ROLE_OUTPUT.json"
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        require(raw["execution_identity"]["execution_id"] == execution_id, f"execution ID mismatch: {role}")
        require(raw["execution_identity"]["role_id"] == role, f"role ID mismatch: {role}")
        require((ROOT / "role_outputs" / key / "OUTPUT_SEAL.json").is_file(), f"output seal missing: {role}")
        require(len(raw["findings"]) > 0, f"no findings: {role}")

    initial = ROOT / "role_outputs/ES-RA-02"
    require(not (initial / "RAW_ROLE_OUTPUT.json").exists(), "initial schema failure has role output")
    require("invalid_json_schema" in (initial / "CODEX_EVENT_STREAM.jsonl").read_text(encoding="utf-8"), "initial schema failure missing")
    require((ROOT / "role_outputs/ES-RA-02-RETRY-01/RETRY_PROVENANCE.json").is_file(), "retry provenance missing")

    scoring = parsed["scoring/EXECUTION_SCORING_SUMMARY.json"]
    require(scoring["roles_required"] == 4 and scoring["roles_qualified"] == 4, "required role qualification mismatch")
    require(scoring["oracle_defects_detected"] == 12 and scoring["oracle_defect_denominator"] == 12, "oracle denominator mismatch")
    require(scoring["blocking_misses"] == 0, "blocking oracle miss")
    require(scoring["replay_variance_class"] == "MINOR_NONDISPOSITIVE_VARIANCE", "replay variance mismatch")
    require(scoring["supported_assurance_classification"] == "PROCEDURALLY_SEGREGATED_INTERNAL_AI_REVIEW", "assurance classification mismatch")
    require(scoring["phase_2"] == "NOT_AUTHORIZED", "Phase 2 status mismatch")

    oracle_rows = csv_rows(ROOT / "scoring/ORACLE_SCORING.csv")
    require(len(oracle_rows) == 23, "oracle role-detection pair denominator mismatch")
    require(all(row["detected"] == "True" for row in oracle_rows), "oracle detection miss")
    require(sum(row["severity_acceptable"] == "True" for row in oracle_rows) == 17, "severity accuracy numerator mismatch")

    reconciliation = csv_rows(ROOT / "MODE_B_RECONCILIATION_REGISTER.csv")
    require(len(reconciliation) == 34, "reconciliation denominator mismatch")
    require(all(row["original_finding_id"] and row["original_wording"] for row in reconciliation), "reconciliation lost original finding data")
    require(all("does not weaken" in row["rationale"] for row in reconciliation), "reconciliation authority boundary missing")

    output_manifest = csv_rows(ROOT / "MODE_B_PACKET_OUTPUT_MANIFEST.csv")
    require(len(output_manifest) == 36, "packet output manifest denominator mismatch")
    for row in output_manifest:
        path = ROOT / "role_outputs" / row["output_directory"] / row["path"]
        require(path.is_file(), f"packaged output missing: {path}")
        require(path.stat().st_size == int(row["size_bytes"]), f"output size mismatch: {path}")
        require(sha256(path) == row["sha256"], f"output hash mismatch: {path}")

    invocation = parsed["MODE_B_INVOCATION_EVIDENCE.json"]
    require(all(value == 0 for value in invocation["pre_boundary"].values()), "invocation pre-boundary count nonzero")
    require(invocation["post_boundary"]["unique_canonical_roles_qualified"] == 4, "qualified invocation count mismatch")
    require(invocation["phase_2_activity"] == 0, "Phase 2 activity recorded")
    require(invocation["disposition"] == "PILOT_A_CONFIGURATION_IDENTIFIED_EXECUTION_VALIDATED_READY_FOR_FOUNDER_REVIEW", "disposition mismatch")

    attempt03_rel = "governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-03"
    historical = subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", str(REPO), "diff", "--exit-code", START, "--", attempt03_rel], check=False)
    require(historical.returncode == 0, "Attempt 03 differs from starting commit")
    status = subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", str(REPO), "status", "--porcelain=v1", "--untracked-files=all"], text=True, capture_output=True, check=True).stdout.splitlines()
    allowed = "governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-04/"
    changed_paths = [line[3:].split(" -> ", 1)[-1] for line in status]
    require(changed_paths and all(path.startswith(allowed) for path in changed_paths), "change outside additive Attempt 04 scope")

    print(json.dumps({
        "result": "PASS",
        "json_files_parsed": len(json_files),
        "roles_required": 4,
        "roles_qualified": 4,
        "oracle_defects": 12,
        "blocking_misses": 0,
        "severity_pairs_acceptable": 17,
        "severity_pairs_total": 23,
        "reconciliation_rows": len(reconciliation),
        "output_manifest_rows": len(output_manifest),
        "attempt03_immutable": True,
        "additive_only": True,
        "phase_2": "NOT_AUTHORIZED",
    }, indent=2))


if __name__ == "__main__":
    main()
