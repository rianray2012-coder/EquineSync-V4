#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

PACKAGE_NAME = "EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V1"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

def add(results, check, status, detail, failure_capable=True):
    results.append({"check": check, "status": status, "detail": detail, "failure_capable": failure_capable})
    return 1 if status == "FAIL" else 0

def fail_if(condition, results, check, detail):
    return add(results, check, "FAIL" if condition else "PASS", detail)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root")
    parser.add_argument("--package-root")
    parser.add_argument("--mode", choices=["package-only", "repository-aware"], default="package-only")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    package = Path(args.package_root) if args.package_root else Path.cwd()
    if package.name != PACKAGE_NAME and (package / PACKAGE_NAME).exists():
        package = package / PACKAGE_NAME
    results = []
    failures = 0
    required = [
        "README_FIRST.md",
        "SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md",
        "PACKAGE_MANIFEST.json",
        "CHECKSUMS.sha256",
        "MANIFEST_OF_MANIFESTS.csv",
        "EXTERNAL_REVIEW/EXTERNAL_REVIEW_FINDING_DISPOSITION_REGISTER.csv",
        "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv",
        "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv",
        "04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv",
        "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv",
        "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv",
        "08_SOURCE_RECONCILIATION/DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv",
        "10_CLOSING_AUDIT_PROTOCOL/TEMPLATE_INDEX.csv",
    ]
    for rel in required:
        failures += add(results, f"required_file:{rel}", "PASS" if (package / rel).is_file() else "FAIL", rel)
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text())
    for item in manifest["files"]:
        path = package / item["path"]
        failures += fail_if((not path.is_file()) or sha(path) != item["sha256"] or path.stat().st_size != item["byte_length"], results, f"manifest_integrity:{item['path']}", "hash/byte check")
    mom = rows(package / "MANIFEST_OF_MANIFESTS.csv")
    failures += fail_if(
        any(item["path"] in {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256", "MANIFEST_OF_MANIFESTS.csv"} for item in mom),
        results,
        "manifest_of_manifests_excludes_root_self_references",
        "root manifest/checksum files are disclosed in PACKAGE_MANIFEST metadata and cannot be self-bound after final write",
    )
    for item in mom:
        path = package / item["path"]
        failures += fail_if((not path.is_file()) or sha(path) != item["sha256"] or path.stat().st_size != int(item["byte_length"]), results, f"manifest_of_manifests:{item['path']}", "manifest/checksum binding")
    doc03 = rows(package / "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv")
    failures += fail_if(any(r["requirement_type"] != "SOURCE_TEXT_CANDIDATE" for r in doc03), results, "doc03_no_unverified_normative_requirements", "all rows must remain source candidates")
    failures += fail_if(any(r.get("verification_method") != "NOT_PERFORMED" for r in doc03), results, "doc03_verification_not_overclaimed", "verification must not be inferred from discovery")
    failures += fail_if(any(r.get("test_id") and r.get("exact_test_or_assertion_locator") != "ASSERTION_LEVEL_VERIFIED" for r in doc03), results, "doc03_test_id_assertion_locator_consistency", "test_id requires assertion-level locator")
    trans = rows(package / "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv")
    states = {r["permitted_starting_state"] for r in trans} | {r["permitted_next_state"] for r in trans}
    failures += fail_if(len(states) != 13 or len(trans) != 169, results, "lifecycle_transition_matrix_complete", f"states={len(states)} rows={len(trans)}")
    rules = rows(package / "04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv")
    failures += fail_if(any(r.get("implementation_status") != "ENFORCED_BY_VALIDATOR" or r.get("failure_capable") != "YES" for r in rules), results, "invalid_rules_marked_enforced", "all invalid rules must be failure-capable")
    life = rows(package / "04_AUTHORITY_LIFECYCLE_REGISTER/AUTHORITY_LIFECYCLE_STATE_REGISTER.csv")
    for rule in rules:
        expr = rule["validator_expression"]
        invalid = []
        for r in life:
            if "activation_state=ACTIVE and adoption_state!=ADOPTED" in expr and r["activation_state"] == "ACTIVE" and r["adoption_state"] != "ADOPTED":
                invalid.append(r)
            if "adoption_state=ADOPTED and approval_evidence empty" in expr and r["adoption_state"] == "ADOPTED" and not r["approval_evidence"]:
                invalid.append(r)
            if "accession_state=ACCESSIONED and accession_evidence empty" in expr and r["accession_state"] == "ACCESSIONED" and not r["accession_evidence"]:
                invalid.append(r)
            if "custody_state=CUSTODY_COMPLETE and accession_state!=ACCESSIONED" in expr and r["custody_state"] == "CUSTODY_COMPLETE" and r["accession_state"] != "ACCESSIONED":
                invalid.append(r)
            if "successor_or_basis empty" in expr and r["supersession_state"].startswith("SUPERSEDED") and not r["successor_or_basis"]:
                invalid.append(r)
            if "document_lifecycle_state=LOCKED and lock_evidence empty" in expr and r["document_lifecycle_state"] == "LOCKED" and not r["lock_evidence"]:
                invalid.append(r)
            if "authority_state=EFFECTIVE and effective_date empty" in expr and r["authority_state"] == "EFFECTIVE" and not r["effective_date"]:
                invalid.append(r)
            if "implementation_authority=AUTHORIZED" in expr and r["implementation_authority"] == "AUTHORIZED" and r["authority_state"] != "IMPLEMENTATION_AUTHORIZING":
                invalid.append(r)
            if "production_authority=AUTHORIZED" in expr and r["production_authority"] == "AUTHORIZED" and r["activation_state"] != "ACTIVE":
                invalid.append(r)
            if "suspension_state=SUSPENDED and activation_state=ACTIVE" in expr and r["suspension_state"] == "SUSPENDED" and r["activation_state"] == "ACTIVE":
                invalid.append(r)
            if "document_lifecycle_state=HISTORICAL_RETAINED and authority_state=CONTROLLING" in expr and r["document_lifecycle_state"] == "HISTORICAL_RETAINED" and r["authority_state"] == "CONTROLLING":
                invalid.append(r)
            if "authority_state=DOCUMENTARY_CANDIDATE_ONLY and adoption_state=ADOPTED" in expr and r["authority_state"] == "DOCUMENTARY_CANDIDATE_ONLY" and r["adoption_state"] == "ADOPTED":
                invalid.append(r)
        failures += fail_if(bool(invalid), results, f"invalid_state_rule:{rule['rule_id']}", f"invalid_rows={len(invalid)}")
    decisions = rows(package / "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv")
    failures += fail_if(any(r["selected_disposition"] != "NO_DISPOSITION_SELECTED" for r in decisions), results, "founder_decisions_no_disposition_selected", "no decision recorded")
    failures += fail_if(any(r["authority_granted"] != "NONE_BY_THIS_PACKAGE" for r in decisions), results, "founder_decisions_no_authority_granted", "no authority")
    packet = rows(package / "FOUNDER_DECISION_PACKET.csv")
    failures += fail_if({r["question_presented"] for r in decisions} != {r["question_presented"] for r in packet}, results, "founder_question_text_consistency", "register and packet question text")
    frwe = rows(package / "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv")
    failures += fail_if(any(not r.get("root_cause") for r in frwe), results, "findings_root_cause_present", "root cause required")
    failures += fail_if(any("accepted residual risk" == r["record_classification"] for r in frwe), results, "no_accepted_residual_risk_without_authority", "no accepted risk in package")
    owners = rows(package / "07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv")
    failures += fail_if(any(not r.get("accountability_gap_effect") for r in owners), results, "ownership_gap_effect_present", "vacancy effect required")
    cal = rows(package / "07_OWNERSHIP_STEWARDSHIP_REVIEW/REVIEW_CALENDAR.csv")
    failures += fail_if(any(r.get("overdue_state") != "NOT_OPERATIVE_PENDING_APPOINTMENT" for r in cal), results, "review_calendar_not_operative_pending_appointment", "no vacant schedule as operative control")
    sources = rows(package / "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv")
    clusters = rows(package / "08_SOURCE_RECONCILIATION/DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv")
    cluster_ids = {r["cluster_id"] for r in clusters}
    failures += fail_if(any(not r["duplicate_cluster_id"] for r in sources), results, "source_duplicate_fk_populated", "no blank duplicate_cluster_id")
    failures += fail_if(any(r["duplicate_cluster_id"] not in cluster_ids and r["duplicate_cluster_id"] != "NO_DUPLICATE_CLUSTER" for r in sources), results, "source_duplicate_fk_valid", "source duplicate FK valid")
    failures += fail_if(any(r["authority_state"] == "ADOPTION_OR_LOCK_EVIDENCE_PRESENT" for r in sources), results, "source_adoption_label_not_package_adoption", "adoption evidence labels scoped")
    workstreams = rows(package / "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv")
    failures += fail_if(any(not r.get("review_thread_state") or not r.get("ci_failure_analysis") for r in workstreams), results, "workstream_github_fields_populated", "review and CI analysis fields")
    templates = rows(package / "10_CLOSING_AUDIT_PROTOCOL/TEMPLATE_INDEX.csv")
    names = [r["template_name"] for r in templates]
    failures += fail_if(len(templates) != 19 or len(set(names)) != 19, results, "review_template_count_and_distinct_names", f"templates={len(templates)} unique={len(set(names))}")
    forbidden = ["CERTIFICATION", "CERTIFICATE", "AUDIT_PLAN", "RECERTIFICATION"]
    failures += fail_if(any(any(word in name for word in forbidden) for name in names), results, "terminology_exposure_reduced", "template names avoid certification/certificate/audit plan terminology")
    for n in range(3, 11):
        failures += fail_if(not (package / f"{n:02d}_" ).exists(), results, f"document_{n:02d}_directory_placeholder", "checked by glob fallback", False) if False else 0
        validators = list(package.glob(f"{n:02d}_*/validators/validate_document_{n:02d}_rr2.py"))
        tests = list(package.glob(f"{n:02d}_*/tests/test_document_{n:02d}_rr2_validator.py"))
        failures += fail_if(not validators or not tests, results, f"per_document_validator_test:{n:02d}", "per-doc validator/test present")
    if args.mode == "repository-aware":
        if not args.repo_root or not (Path(args.repo_root) / ".git").exists():
            add(results, "git_metadata", "NOT_APPLICABLE_OUTSIDE_GIT", "repository root unavailable", False)
        else:
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.repo_root, text=True).strip()
            add(results, "git_metadata", "PASS", head)
    else:
        add(results, "git_metadata", "NOT_APPLICABLE_OUTSIDE_GIT", "package-only validation", False)
    report = {
        "status": "PASS" if failures == 0 else "FAIL",
        "failures": failures,
        "python_version": sys.version,
        "platform": platform.platform(),
        "dependency_versions": {"stdlib_only": True},
        "package_root": str(package),
        "mode": args.mode,
        "assessment_limitation": "Report is stored inside the assessed package; final archive hash is reported separately after archive rebuild.",
        "results": results,
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.json_output:
        output = Path(args.json_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if failures == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
