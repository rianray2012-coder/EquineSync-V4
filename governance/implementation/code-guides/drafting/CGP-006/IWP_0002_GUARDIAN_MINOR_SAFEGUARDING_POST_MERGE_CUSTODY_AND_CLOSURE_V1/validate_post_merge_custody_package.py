#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
PACKAGE_DIR = Path(__file__).resolve().parent
REQUIRED = {
"README.md","IMPLEMENTATION_PR_MERGE_RECEIPT.md","PROTECTED_HEAD_AND_MERGED_FILE_IDENTITY_RECORD.json","FOUNDER_CONDITIONAL_CLOSURE_AUTHORITY_RECORD.md","IMPLEMENTATION_EVIDENCE_CUSTODY_REGISTER.csv","CLOSURE_CRITERIA_SATISFACTION_MATRIX.csv","WORKFLOW_ENFORCEMENT_POST_MERGE_VERIFICATION.csv","REGRESSION_AND_ABUSE_TEST_CUSTODY_RECORD.csv","REVIEW_AND_CORRECTION_CUSTODY_RECORD.md","SCHEMA_INDEX_AND_ROLLBACK_CUSTODY_RECORD.md","FINDING_AND_GAP_CLOSURE_DISPOSITION.md","CANONICAL_STATUS_REGISTER_RECONCILIATION.md","AUTHORIZED_PATH_REPORT.md","VALIDATION_REPORT.md","DIRECTIVE_EXECUTION_RECORD.md","PACKAGE_MANIFEST.json","CHECKSUM_MANIFEST.sha256","validate_post_merge_custody_package.py"}
BLOCKED = "CGP_006_IWP_0002_POST_MERGE_CUSTODY_COMPLETE_CLOSURE_BLOCKED_PENDING_FOUNDER_REVIEW"
def sha256(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def main() -> int:
    names={p.name for p in PACKAGE_DIR.iterdir() if p.is_file()}
    missing=sorted(REQUIRED-names)
    assert not missing, f"missing required files: {missing}"
    combined="\n".join(p.read_text(encoding="utf-8") for p in PACKAGE_DIR.iterdir() if p.is_file() and p.suffix in {".md",".csv",".json"})
    assert BLOCKED in combined, "blocked terminal status missing"
    forbidden = ["CGP006-MAP-FIND-0002" + "=CLOSED", "CGP006-MAP-GAP-0003" + "=CLOSED"]
    for token in forbidden: assert token not in combined, f"forbidden closure token present: {token}"
    criteria=list(csv.DictReader((PACKAGE_DIR/"CLOSURE_CRITERIA_SATISFACTION_MATRIX.csv").open(newline="")))
    assert any(row["criterion_id"]=="CC-06" and row["status"]=="FAIL" for row in criteria), "CC-06 must fail"
    identity=json.loads((PACKAGE_DIR/"PROTECTED_HEAD_AND_MERGED_FILE_IDENTITY_RECORD.json").read_text())
    assert identity["implementation_pr"] == 71
    assert identity["closure_status"] == BLOCKED
    assert len(identity["post_merge_unresolved_findings"]) == 2
    manifest=json.loads((PACKAGE_DIR/"PACKAGE_MANIFEST.json").read_text())
    for name, meta in manifest["files"].items():
        if name == "CHECKSUM_MANIFEST.sha256": continue
        path=PACKAGE_DIR/name
        assert path.exists(), f"manifest file missing: {name}"
        assert meta["bytes"] == path.stat().st_size, f"byte mismatch: {name}"
        assert meta["sha256"] == sha256(path), f"sha mismatch: {name}"
    checksums={}
    for line in (PACKAGE_DIR/"CHECKSUM_MANIFEST.sha256").read_text().splitlines():
        digest,name=line.split("  ",1); checksums[name]=digest
    for name,digest in checksums.items(): assert sha256(PACKAGE_DIR/name)==digest, f"checksum mismatch: {name}"
    print("PASS post-merge custody package: closure blocked pending Founder review; no closure tokens recorded")
    return 0
if __name__ == "__main__": raise SystemExit(main())
