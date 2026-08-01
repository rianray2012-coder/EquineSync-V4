#!/usr/bin/env python3
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[5]
CGP006_DIR = PACKAGE_DIR.parent
MAPPING_DIR = CGP006_DIR / "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AND_CURRENT_STATE_GAP_AUDIT_V1"
PROGRAM_STATUS = PACKAGE_DIR.parents[2] / "PROGRAM_STATUS.md"

READY_STATUS = "CGP_006_IWP_0002_POST_MERGE_FINDINGS_CORRECTED_CUSTODY_REFRESHED_AND_SCOPE_LIMITED_CLOSURE_READY_FOR_PROTECTED_MERGE"
TERMINAL_STATUS = "CGP_006_IWP_0002_POST_MERGE_FINDINGS_CORRECTED_CUSTODY_REFRESHED_AND_SCOPE_LIMITED_CLOSURE_COMPLETE"
EVENT = "VERIFIED_PROTECTED_MERGE_OF_REFRESHED_PR_72_POST_MERGE_CUSTODY_AND_CLOSURE"
PR75_HEAD = "4c144c08be7e4c25910694186972a91d2302fbb3"
PR75_MERGE = "a5461072b36fd991b4cfcba343e53aa83d70df66"
FIND_CLOSED = "CGP006_MAP_FIND_0002_CLOSED_WITH_SERVER_SIDE_GUARDIAN_MINOR_ENFORCEMENT_POST_MERGE_CORRECTION_AND_REGRESSION_ABUSE_EVIDENCE"
GAP_CLOSED = "CGP006_MAP_GAP_0003_CLOSED_WITH_REPOSITORY_IMPLEMENTATION_POST_MERGE_CORRECTION_VERIFICATION_AND_CUSTODY"
IWP_CLOSED = "CGP006_IWP_0002=IMPLEMENTED_CORRECTED_VERIFIED_MERGED_CUSTODY_COMPLETE"

REQUIRED = {
    "AUTHORIZED_PATH_REPORT.md",
    "BLOCKED_CUSTODY_HISTORICAL_RECORD.md",
    "CANONICAL_STATUS_REGISTER_RECONCILIATION.md",
    "CHECKSUM_MANIFEST.sha256",
    "CLOSURE_CRITERIA_SATISFACTION_MATRIX.csv",
    "CORRECTED_PROTECTED_HEAD_AND_FILE_IDENTITY_RECORD.json",
    "CORRECTIVE_TEST_EVIDENCE_CUSTODY.csv",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "FINAL_REVIEW_THREAD_RESOLUTION_RECORD.md",
    "FINDING_AND_GAP_CLOSURE_DISPOSITION.md",
    "FOUNDER_CONDITIONAL_CLOSURE_AUTHORITY_RECORD.md",
    "IMPLEMENTATION_EVIDENCE_CUSTODY_REGISTER.csv",
    "IMPLEMENTATION_PR_MERGE_RECEIPT.md",
    "PACKAGE_MANIFEST.json",
    "POST_MERGE_CORRECTIVE_PR_MERGE_RECEIPT.md",
    "POST_MERGE_FINDINGS_CORRECTION_CUSTODY_RECORD.md",
    "PROTECTED_HEAD_AND_MERGED_FILE_IDENTITY_RECORD.json",
    "README.md",
    "REGRESSION_AND_ABUSE_TEST_CUSTODY_RECORD.csv",
    "REVIEW_AND_CORRECTION_CUSTODY_RECORD.md",
    "SCHEMA_INDEX_AND_ROLLBACK_CUSTODY_RECORD.md",
    "UPDATED_CLOSURE_CRITERIA_SATISFACTION_MATRIX.csv",
    "VALIDATION_REPORT.md",
    "WORKFLOW_ENFORCEMENT_POST_MERGE_VERIFICATION.csv",
    "validate_post_merge_custody_package.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_one(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    hits = [row for row in rows if row.get(key) == value]
    assert len(hits) == 1, f"expected one {key}={value}, got {len(hits)}"
    return hits[0]


def main() -> int:
    names = {p.name for p in PACKAGE_DIR.iterdir() if p.is_file()}
    missing = sorted(REQUIRED - names)
    assert not missing, f"missing required files: {missing}"

    combined = "\n".join(
        p.read_text(encoding="utf-8")
        for p in PACKAGE_DIR.iterdir()
        if p.is_file() and p.suffix in {".md", ".csv", ".json"}
    )
    for token in [READY_STATUS, TERMINAL_STATUS, EVENT, "CGP006-MAP-FIND-0002=CLOSED", "CGP006-MAP-GAP-0003=CLOSED", FIND_CLOSED, GAP_CLOSED, IWP_CLOSED]:
        assert token in combined, f"closure token missing: {token}"
    for token in ["NO_PRODUCT_CODE_ON_PR_72", "NO_DEPLOYMENT", "NO_STAGING", "NO_PILOT", "NO_PRODUCTION_USE", "GAP_0004_REMAINS_OPEN", "NO_WAVE_2", "NO_CGP_007"]:
        assert token in combined, f"boundary token missing: {token}"

    criteria = read_rows(PACKAGE_DIR / "UPDATED_CLOSURE_CRITERIA_SATISFACTION_MATRIX.csv")
    statuses = {row["closure_gate"]: row["status"] for row in criteria}
    allowed_pending = {"PR_72_REQUIRED_CHECKS_AND_REVIEWS_PASS"}
    for gate, status in statuses.items():
        if gate in allowed_pending:
            assert status == "PENDING_PROTECTED_PR_72_CHECKS", f"unexpected pending gate status for {gate}: {status}"
        else:
            assert status.startswith("PASS"), f"non-pass closure gate {gate}: {status}"

    identity = json.loads((PACKAGE_DIR / "CORRECTED_PROTECTED_HEAD_AND_FILE_IDENTITY_RECORD.json").read_text(encoding="utf-8"))
    assert identity["corrective_pr"] == 75
    assert identity["corrective_final_head"] == PR75_HEAD
    assert identity["corrective_merge_commit"] == PR75_MERGE
    assert identity["corrected_protected_head"] == PR75_MERGE
    assert identity["post_merge_unresolved_findings"] == []
    findings = identity["post_merge_findings"]
    assert len(findings) == 2
    assert all(item["resolved_after_corrective_merge"] is True for item in findings)
    assert {item["thread_id"] for item in findings} == {"PRRT_kwDOS5bRRs6Vmf5A", "PRRT_kwDOS5bRRs6Vmf5B"}
    paths = {item["path"] for item in identity["corrected_file_identities"]}
    assert "backend/core/minor_safety.py" in paths
    assert "backend/core/minor_communication.py" in paths
    assert "backend/routes/billing.py" in paths
    assert "backend/routes/recurring_charges.py" in paths

    current_gap = find_one(read_rows(MAPPING_DIR / "CURRENT_STATE_GAP_REGISTER.csv"), "gap_id", "CGP006-MAP-GAP-0003")
    assert current_gap["status"] == "CLOSED"
    assert current_gap["current_state_classification"] == "IMPLEMENTED_CORRECTED_VERIFIED_MERGED_CUSTODY_COMPLETE"
    finding = find_one(read_rows(MAPPING_DIR / "SECURITY_PRIVACY_AND_SAFEGUARDING_FINDINGS_REGISTER.csv"), "finding_id", "CGP006-MAP-FIND-0002")
    assert finding["status"] == "CLOSED"
    backlog = find_one(read_rows(MAPPING_DIR / "IMPLEMENTATION_WORK_PACKAGE_CANDIDATE_BACKLOG.csv"), "work_package_id", "CGP006-IWP-CANDIDATE-0002")
    assert backlog["implementation_authorization_status"] == "IMPLEMENTED_CORRECTED_VERIFIED_MERGED_CUSTODY_COMPLETE"
    control_rows = [row for row in read_rows(MAPPING_DIR / "GUARDIAN_MINOR_SAFEGUARDING_CONTROL_MAP.csv") if row.get("gap_ids") == "CGP006-MAP-GAP-0003"]
    assert control_rows, "missing control rows for gap"
    assert all(row["current_state_classification"] == "IMPLEMENTED_CORRECTED_VERIFIED_SCOPE_LIMITED" for row in control_rows)
    pia = find_one(read_rows(MAPPING_DIR / "PIA_AND_FOUNDER_DECISION_TO_REPOSITORY_TRACEABILITY_MATRIX.csv"), "mapping_id", "PIA-MAP-0008")
    assert pia["current_state_classification"] == "IMPLEMENTED_CORRECTED_VERIFIED_SCOPE_LIMITED"

    status_text = PROGRAM_STATUS.read_text(encoding="utf-8")
    for token in [TERMINAL_STATUS, EVENT, FIND_CLOSED, GAP_CLOSED, IWP_CLOSED, "GAP_0004_REMAINS_OPEN", "NO_CGP_007"]:
        assert token in status_text, f"PROGRAM_STATUS token missing: {token}"

    manifest = json.loads((PACKAGE_DIR / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    expected_manifest_names = sorted(names - {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"})
    assert sorted(manifest["files"].keys()) == expected_manifest_names
    for name, meta in manifest["files"].items():
        path = PACKAGE_DIR / name
        assert path.exists(), f"manifest file missing: {name}"
        assert meta["bytes"] == path.stat().st_size, f"byte mismatch: {name}"
        assert meta["sha256"] == sha256(path), f"sha mismatch: {name}"

    checksums = {}
    for line in (PACKAGE_DIR / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        checksums[name] = digest
    expected_checksum_names = sorted(names - {"CHECKSUM_MANIFEST.sha256"})
    assert sorted(checksums) == expected_checksum_names
    for name, digest in checksums.items():
        assert sha256(PACKAGE_DIR / name) == digest, f"checksum mismatch: {name}"

    print("PASS post-merge custody package: correction merged, threads resolved, closure staged for protected PR #72 merge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
