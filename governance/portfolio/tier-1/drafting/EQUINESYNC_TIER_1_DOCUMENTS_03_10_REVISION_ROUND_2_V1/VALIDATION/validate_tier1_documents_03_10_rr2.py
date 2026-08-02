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
REQUIRED_FILES = [
    "README_FIRST.md",
    "SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUMS.sha256",
    "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv",
    "04_AUTHORITY_LIFECYCLE_REGISTER/AUTHORITY_LIFECYCLE_STATE_REGISTER.csv",
    "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv",
    "04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv",
    "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv",
    "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv",
    "07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv",
    "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv",
    "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv",
    "10_CLOSING_AUDIT_PROTOCOL/TEMPLATE_INDEX.csv",
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

def add(results, check, status, detail):
    results.append({"check": check, "status": status, "detail": detail})

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
    for rel in REQUIRED_FILES:
        exists = (package / rel).is_file()
        add(results, f"required_file:{rel}", "PASS" if exists else "FAIL", "present" if exists else "missing")
        failures += 0 if exists else 1
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text())
    manifest_paths = {f["path"]: f for f in manifest["files"]}
    for rel, item in manifest_paths.items():
        path = package / rel
        if not path.is_file():
            add(results, f"manifest_file:{rel}", "FAIL", "missing")
            failures += 1
            continue
        if sha(path) != item["sha256"] or path.stat().st_size != item["byte_length"]:
            add(results, f"manifest_integrity:{rel}", "FAIL", "hash or byte length mismatch")
            failures += 1
    add(results, "manifest_accuracy", "PASS" if failures == 0 else "FAIL", f"files={len(manifest_paths)}")
    doc03 = rows(package / "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv")
    if not all(r["result"] in {"NOT_EXECUTED"} for r in doc03):
        add(results, "evidence_state_separation", "FAIL", "documentary package cannot claim executed results")
        failures += 1
    else:
        add(results, "evidence_state_separation", "PASS", "execution/runtime/production evidence remains separated")
    life = rows(package / "04_AUTHORITY_LIFECYCLE_REGISTER/AUTHORITY_LIFECYCLE_STATE_REGISTER.csv")
    invalid = [r for r in life if r["activation_state"] == "ACTIVE" and r["adoption_state"] != "ADOPTED"]
    invalid += [r for r in life if r["adoption_state"] == "ADOPTED" and not r["approval_evidence"]]
    invalid += [r for r in life if r["production_authority"] != "PRODUCTION_USE_NOT_AUTHORIZED"]
    add(results, "lifecycle_invalid_combination_rules", "PASS" if not invalid else "FAIL", f"invalid_rows={len(invalid)}")
    failures += len(invalid)
    decisions = rows(package / "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv")
    bad_decisions = [r for r in decisions if r["authority_granted"] != "NONE_BY_THIS_PACKAGE"]
    add(results, "decision_authority_boundary", "PASS" if not bad_decisions else "FAIL", f"bad_decisions={len(bad_decisions)}")
    failures += len(bad_decisions)
    frwe = rows(package / "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv")
    bad_waivers = [r for r in frwe if r["record_classification"] in {"waiver", "exception", "temporary deviation"} and (not r["expiration_date"] or r["silent_permanent_continuation_prohibited"] != "YES")]
    add(results, "waiver_expiration_controls", "PASS" if not bad_waivers else "FAIL", f"bad_waivers={len(bad_waivers)}")
    failures += len(bad_waivers)
    owners = rows(package / "07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv")
    invented = [r for r in owners if r["appointment_evidence"] != "NOT_RECORDED" and not r["effective_date"]]
    add(results, "ownership_vacancy_handling", "PASS" if not invented else "FAIL", f"invented_assignments={len(invented)}")
    failures += len(invented)
    sources = rows(package / "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv")
    add(results, "source_disposition_rules", "PASS" if all(r["source_disposition"] for r in sources) else "FAIL", f"sources={len(sources)}")
    prs = rows(package / "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv")
    add(results, "workstream_completeness", "PASS" if prs and all(r["recommended_disposition"] for r in prs) else "FAIL", f"prs={len(prs)}")
    templates = rows(package / "10_CLOSING_AUDIT_PROTOCOL/TEMPLATE_INDEX.csv")
    template_fail = len(templates) != 19
    add(results, "audit_template_completeness", "PASS" if not template_fail else "FAIL", f"templates={len(templates)}")
    failures += 1 if template_fail else 0
    if args.mode == "repository-aware":
        if not args.repo_root or not (Path(args.repo_root) / ".git").exists():
            add(results, "git_metadata", "NOT_APPLICABLE_OUTSIDE_GIT", "repository root unavailable")
        else:
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.repo_root, text=True).strip()
            add(results, "git_metadata", "PASS", head)
    else:
        add(results, "git_metadata", "NOT_APPLICABLE_OUTSIDE_GIT", "package-only validation")
    report = {
        "status": "PASS" if failures == 0 else "FAIL",
        "failures": failures,
        "python_version": sys.version,
        "platform": platform.platform(),
        "dependency_versions": {"stdlib_only": True},
        "package_root": str(package),
        "mode": args.mode,
        "results": results,
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.json_output:
        output_path = Path(args.json_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if failures == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
