#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path

PACKAGE_STATUS = "REVISION_REQUIRED_PENDING_BOUNDED_INDEPENDENT_CLOSURE_REREVIEW"

def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

def main():
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    checks = []
    failures = 0
    def check(name, ok, kind="STRUCTURAL_PASS", detail=""):
        nonlocal failures
        status = "PASS" if ok else "FAIL"
        if not ok:
            failures += 1
        checks.append({"check": name, "status": status, "kind": kind, "detail": detail})

    required = [
        "README_FIRST.md",
        "00_PROGRAM_CONTROL/AUTHENTICATED_REPOSITORY_AND_PACKAGE_CUSTODY_RECORD_V2.json",
        "OUTSIDE_REVIEW/T1C_CONSOLIDATED_FINDINGS_DISPOSITION_REGISTER.csv",
        "OUTSIDE_REVIEW/PER_FINDING_CLOSURE_EVIDENCE_REGISTER.csv",
        "OUTSIDE_REVIEW/EQUINESYNC_TIER_1_DOCS_03_10_CONSOLIDATED_OUTSIDE_REVIEW_REGISTER.md",
        "FOUNDER_DECISION_PACKET.md",
        "VALIDATION/FIXTURES/negative/decision_text_lifecycle_count_mismatch.json",
    ]
    for rel in required:
        check("required_file:" + rel, (package / rel).is_file())
    findings = rows(package / "OUTSIDE_REVIEW/T1C_CONSOLIDATED_FINDINGS_DISPOSITION_REGISTER.csv")
    check("t1c_population_complete", len(findings) == 20, detail=str(len(findings)))
    check("no_self_closed_findings", all("OPEN" in r["closure_state"] or "RETAINED" in r["closure_state"] for r in findings))
    check("second_reviewer_not_fabricated", all(r["second_reviewer_state"] == "NOT_PERFORMED_NOT_FABRICATED" for r in findings))
    packet = (package / "FOUNDER_DECISION_PACKET.md").read_text(encoding="utf-8")
    check("founder_packet_no_preselected_approval", "NO_DISPOSITION_SELECTED" in packet and "APPROVED" not in packet, "SUBSTANTIVE_CONTROL_PASS")
    check("authority_boundary_present", "MERGE_NOT_AUTHORIZED" in packet and "PRODUCTION_USE_NOT_AUTHORIZED" in packet, "SUBSTANTIVE_CONTROL_PASS")
    closure_blocked = any(r["closure_state"].startswith("OPEN") for r in findings)
    report = {
        "status": "STRUCTURAL_PASS_SUBSTANTIVE_CONTROL_BLOCKED" if failures == 0 and closure_blocked else ("PASS" if failures == 0 else "FAIL"),
        "package_status": PACKAGE_STATUS,
        "failures": failures,
        "closure_blocked_by_second_review": closure_blocked,
        "results": checks,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if failures == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
