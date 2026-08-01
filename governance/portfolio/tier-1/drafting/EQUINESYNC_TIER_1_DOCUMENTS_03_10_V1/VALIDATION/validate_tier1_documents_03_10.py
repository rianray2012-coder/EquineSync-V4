#!/usr/bin/env python3
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

BASE_REL = 'governance/portfolio/tier-1/drafting/EQUINESYNC_TIER_1_DOCUMENTS_03_10_V1'
AUTHORITY_BOUNDARY = 'DOCUMENTARY_TIER_1_DRAFTING_AND_REVIEW_ONLY_NO_ADOPTION_LOCK_ACTIVATION_IMPLEMENTATION_DEPLOYMENT_PILOT_OR_PRODUCTION_AUTHORITY'
PROTECTED_BRANCH = 'integrate-emergent-final-zip'
ROOT = Path(__file__).resolve().parents[6]
BASE = ROOT / BASE_REL
DOCS = {'03': {'dir': '03_IMPLEMENTATION_TRACEABILITY', 'id': 'EQUINESYNC_MASTER_IMPLEMENTATION_MAPPING_REQUIREMENT_TEST_AND_EVIDENCE_TRACEABILITY_PACKAGE_V1_0'}, '04': {'dir': '04_AUTHORITY_LIFECYCLE_REGISTER', 'id': 'EQUINESYNC_CURRENT_GOVERNANCE_AUTHORITY_LIFECYCLE_LOCK_ACCESSION_CUSTODY_AND_SUPERSESSION_REGISTER_V2_0'}, '05': {'dir': '05_FOUNDER_DECISION_REGISTER', 'id': 'EQUINESYNC_FOUNDER_DECISION_RATIFICATION_AND_ACCEPTANCE_REGISTER_V2_0'}, '06': {'dir': '06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS', 'id': 'EQUINESYNC_GOVERNANCE_FINDINGS_RESIDUAL_RISKS_EXCEPTIONS_AND_WAIVERS_REGISTER_V2_0'}, '07': {'dir': '07_OWNERSHIP_STEWARDSHIP_REVIEW', 'id': 'EQUINESYNC_GOVERNANCE_OWNERSHIP_STEWARDSHIP_AND_REVIEW_CALENDAR_V1_0'}, '08': {'dir': '08_SOURCE_RECONCILIATION', 'id': 'EQUINESYNC_CURRENT_REPOSITORY_VERIFIED_SOURCE_PROVENANCE_AND_SUPERSESSION_RECONCILIATION_REPORT_V2_0'}, '09': {'dir': '09_WORKSTREAM_PR_BRANCH_DISPOSITION', 'id': 'EQUINESYNC_OPEN_WORKSTREAM_PR_BRANCH_AND_EVIDENCE_DISPOSITION_REGISTER_V1_0'}, '10': {'dir': '10_CLOSING_AUDIT_PROTOCOL', 'id': 'EQUINESYNC_GOVERNANCE_CLOSING_AUDIT_PROTOCOL_AND_CERTIFICATION_PACKAGE_V1_0'}}
FORBIDDEN = ("TO" + "DO", "T" + "BD")
PROTECTED_INTEGRATION_PHRASE = "PROTECTEDLY_" + "INTEGRATED"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def parse_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def changed_paths():
    paths = set()
    for cmd in (
        ["git", "diff", "--name-only", f"origin/{PROTECTED_BRANCH}...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ):
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if result.returncode == 0:
            paths.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return sorted(paths)

def verify_checksums(package_dir):
    errors = []
    checksum_path = package_dir / "CHECKSUMS.sha256"
    if not checksum_path.exists():
        return [f"missing checksum ledger: {checksum_path}"]
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            errors.append(f"bad checksum line: {line}")
            continue
        digest, rel_path = parts[0], parts[1].strip()
        if not HEX64.match(digest):
            errors.append(f"bad checksum digest: {rel_path}")
            continue
        target = package_dir / rel_path
        if not target.exists():
            errors.append(f"checksum target missing: {rel_path}")
        elif sha256(target) != digest:
            errors.append(f"checksum mismatch: {rel_path}")
    return errors

def main():
    errors = []
    root_required = [
        "README_FIRST.md",
        "TIER_1_DOCUMENT_INVENTORY.csv",
        "MASTER_SOURCE_REGISTER.csv",
        "CROSS_DOCUMENT_ID_REGISTER.csv",
        "CROSS_DOCUMENT_RECONCILIATION_REPORT.md",
        "DOCUMENTARY_VALIDATION_REPORT.json",
        "PACKAGE_MANIFEST.json",
        "CHECKSUMS.sha256",
        "REVIEWS/TIER_1_DOCUMENTS_03_10_CROSS_DOCUMENT_RECONCILIATION_REPORT.md",
    ]
    for rel in root_required:
        if not (BASE / rel).exists():
            errors.append(f"missing root required file: {rel}")
    for num, doc in DOCS.items():
        doc_dir = BASE / doc["dir"]
        main_doc = doc_dir / f"{doc['id']}.md"
        review = doc_dir / f"{doc['id']}_REVISION_AND_CRITICAL_REVIEW_REPORT.md"
        validator = doc_dir / "validators" / f"validate_document_{num}.py"
        test = doc_dir / "tests" / f"test_document_{num}.py"
        for path in (main_doc, review, validator, test, doc_dir / "PACKAGE_MANIFEST.json", doc_dir / "CHECKSUMS.sha256"):
            if not path.exists():
                errors.append(f"missing document {num} required file: {path.relative_to(BASE)}")
        if main_doc.exists() and AUTHORITY_BOUNDARY not in main_doc.read_text(encoding="utf-8"):
            errors.append(f"authority boundary missing from document {num}")
        if validator.exists():
            result = subprocess.run([sys.executable, str(validator)], cwd=ROOT, text=True, capture_output=True)
            if result.returncode != 0:
                errors.append(f"document validator failed {num}: {result.stdout}{result.stderr}")
        errors.extend(verify_checksums(doc_dir))
    for path in BASE.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix == ".csv":
            rows = parse_csv(path)
            if rows:
                for field in rows[0].keys():
                    if field.endswith("_id") or field in {"id", "source_id", "record_id", "decision_id", "workstream_id"}:
                        seen = set()
                        for row in rows:
                            value = row.get(field, "")
                            if not value or value == "NONE":
                                continue
                            if value in seen:
                                errors.append(f"duplicate id {value} in {path.relative_to(BASE)}")
                            seen.add(value)
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        if path.suffix in {".md", ".csv", ".json", ".py"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in FORBIDDEN:
                if marker in text:
                    errors.append(f"forbidden marker {marker} in {path.relative_to(BASE)}")
            if PROTECTED_INTEGRATION_PHRASE in text:
                errors.append(f"forbidden protected-integration claim in {path.relative_to(BASE)}")
    source_rows = parse_csv(BASE / "MASTER_SOURCE_REGISTER.csv")
    for row in source_rows:
        digest = row.get("sha256", "")
        if digest and not HEX64.match(digest):
            errors.append(f"bad source sha256 {row.get('source_id')}")
        path = row.get("repository_path", "")
        if path and path not in {"NONE", "SOURCE_BYTES_UNAVAILABLE"} and not (ROOT / path).exists():
            if row.get("lifecycle_state") not in {"SOURCE_BYTES_UNAVAILABLE", "SOURCE_IDENTITY_UNRESOLVED", "UNMERGED_CANDIDATE"}:
                errors.append(f"source path unresolved without unavailable state: {path}")
    pr_rows = parse_csv(BASE / "09_WORKSTREAM_PR_BRANCH_DISPOSITION" / "WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv")
    for row in pr_rows:
        if row.get("PR_number") and not row.get("PR_state"):
            errors.append(f"PR reference without state: {row.get('PR_number')}")
        if row.get("final_disposition") and not row.get("closure_criterion"):
            errors.append(f"final disposition without closure criterion: {row.get('workstream_id')}")
    audit_rows = parse_csv(BASE / "10_CLOSING_AUDIT_PROTOCOL" / "AUDIT_REQUIREMENTS_MATRIX.csv")
    for row in audit_rows:
        if not row.get("evidence_rule"):
            errors.append(f"audit requirement missing evidence rule: {row.get('requirement_id')}")
    changed = changed_paths()
    for path in changed:
        if not path.startswith(BASE_REL + "/"):
            errors.append(f"changed path outside authorized package: {path}")
        if re.search(r"(^frontend/|^backend/|^supabase/|^\.github/|schema|migration|provider|render\.yaml|vercel\.json|package\.json|requirements)", path):
            errors.append(f"prohibited application/config path changed: {path}")
    for cmd in (
        ["git", "diff", "--check", f"origin/{PROTECTED_BRANCH}...HEAD"],
        ["git", "diff", "--check"],
        ["git", "diff", "--cached", "--check"],
    ):
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if result.returncode != 0:
            errors.append(f"diff whitespace check failed: {' '.join(cmd)} {result.stdout}{result.stderr}")
    errors.extend(verify_checksums(BASE))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("DOCUMENTARY_VALIDATION_PASS")
    print(f"documents={len(DOCS)}")
    print(f"source_rows={len(source_rows)}")
    print(f"changed_paths={len(changed)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
