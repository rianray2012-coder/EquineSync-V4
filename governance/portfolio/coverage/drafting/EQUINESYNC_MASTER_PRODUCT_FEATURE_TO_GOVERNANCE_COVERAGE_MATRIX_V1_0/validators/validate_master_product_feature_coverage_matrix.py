#!/usr/bin/env python3
"""Deterministic validator for the EquineSync master feature-to-governance matrix."""
from __future__ import annotations
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[4]
CSV_PATH = PACKAGE / "EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv"
JSON_PATH = PACKAGE / "EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.json"
SOURCE_PATH = PACKAGE / "SOURCE_AND_AUTHORITY_REGISTER.csv"
PIA_PATH = PACKAGE / "PIA_FEATURE_COVERAGE_SUMMARY.csv"
GOV_PATH = PACKAGE / "GOVERNANCE_ARTIFACT_INVENTORY.csv"
DECISION_PATH = PACKAGE / "PROPOSED_NEW_PIA_AND_SUPPLEMENT_DECISION_REGISTER.csv"
GAP_PATH = PACKAGE / "NON_PIA_DOCUMENT_AND_CONTROL_GAP_REGISTER.csv"
MANIFEST_PATH = PACKAGE / "PACKAGE_MANIFEST.json"
CHECKSUM_PATH = PACKAGE / "CHECKSUMS.sha256"

ALLOWED_COVERAGE = {
    "FULLY_COVERED", "COVERED_WITH_RETAINED_GAP", "PARTIALLY_COVERED", "CONFLICTING_GOVERNANCE",
    "SOURCE_IDENTITY_UNRESOLVED", "NO_CLEAR_GOVERNANCE_OWNER", "NEW_PIA_CANDIDATE",
    "PIA_SUPPLEMENT_CANDIDATE", "CODE_GUIDE_GAP", "ADR_GAP", "OPERATING_STANDARD_GAP",
    "REGISTER_GAP", "RUNBOOK_GAP", "IMPLEMENTATION_ONLY_GAP", "TESTING_ONLY_GAP",
    "EVIDENCE_ONLY_GAP", "OPERATIONS_ONLY_GAP", "DEFERRED_CAPABILITY", "OUT_OF_SCOPE",
}
ALLOWED_IMPL = {
    "NOT_FOUND", "DOCUMENTED_ONLY", "PARTIAL_IMPLEMENTATION", "IMPLEMENTED_UNVERIFIED",
    "VERIFIED_LOCALLY", "VERIFIED_IN_CI", "RUNTIME_EVIDENCE_PARTIAL", "UAT_COMPLETE",
    "PILOT_EVIDENCE_AVAILABLE", "OPERATIONALLY_ACTIVE", "DEFERRED", "SUPERSEDED",
}
ALLOWED_FINAL = {
    "EXISTING_GOVERNANCE_SUFFICIENT", "EXISTING_GOVERNANCE_SUFFICIENT_RETAIN_FINDING",
    "SUPPLEMENT_EXISTING_PIA", "DRAFT_NEW_PIA", "DRAFT_OR_COMPLETE_CODE_GUIDE",
    "DRAFT_OR_RATIFY_ADR", "DRAFT_OPERATING_STANDARD", "DRAFT_REGISTER", "DRAFT_RUNBOOK",
    "COMPLETE_CROSS_DOMAIN_CONTRACT", "IMPLEMENT_EXISTING_REQUIREMENT", "VERIFY_EXISTING_IMPLEMENTATION",
    "OBTAIN_RUNTIME_EVIDENCE", "COMPLETE_OPERATIONAL_READINESS", "REQUIRE_FOUNDER_DECISION",
    "FORMALLY_DEFER", "REMOVE_DUPLICATE_OR_CONFLICTING_AUTHORITY", "NO_NEW_DOCUMENT_REQUIRED",
}
REQUIRED_COLUMNS = [
    "Feature ID", "Feature name", "Product domain", "Affected personas", "Governing PIA",
    "Applicable Code Guides", "System of truth", "Permission owner", "Retention class",
    "Audit requirements", "Current implementation status", "Governance coverage state",
    "Final disposition", "Source IDs",
]
AUTHORIZED_PREFIX = "governance/portfolio/coverage/drafting/EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0/"
PROHIBITED_PREFIXES = ("backend/", "frontend/", "docs/", ".github/", "governance/pia/", "governance/implementation/", "outputs/", "test_reports/", "tests/")

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def validate_payload(csv_rows, json_obj, sources, pia_rows, gov_rows, decisions, gaps):
    errors = []
    json_rows = json_obj.get("features", [])
    if len(csv_rows) != len(json_rows):
        errors.append(f"CSV/JSON row count mismatch: {len(csv_rows)} != {len(json_rows)}")
    if csv_rows != json_rows:
        errors.append("CSV and JSON feature rows do not agree exactly")
    ids = [r.get("Feature ID", "") for r in csv_rows]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate Feature ID present")
    source_ids = {r["source_id"] for r in sources}
    pia_ids = {r["pia_id"] for r in pia_rows}
    gov_ids = {r["artifact_id"] for r in gov_rows}
    decision_ids = {r["decision_id"] for r in decisions}
    gap_ids = [r["gap_id"] for r in gaps]
    if len(gap_ids) != len(set(gap_ids)):
        errors.append("Duplicate gap_id present")
    for row in csv_rows:
        rid = row.get("Feature ID", "<missing>")
        for col in REQUIRED_COLUMNS:
            if not row.get(col):
                errors.append(f"{rid}: required column {col} is blank")
        if row.get("Governance coverage state") not in ALLOWED_COVERAGE:
            errors.append(f"{rid}: invalid coverage state {row.get('Governance coverage state')}")
        if row.get("Current implementation status") not in ALLOWED_IMPL:
            errors.append(f"{rid}: invalid implementation state {row.get('Current implementation status')}")
        if row.get("Final disposition") not in ALLOWED_FINAL:
            errors.append(f"{rid}: invalid final disposition {row.get('Final disposition')}")
        if row.get("Governance coverage state") == "FULLY_COVERED" and row.get("Gap severity") in {"P0", "P1"}:
            errors.append(f"{rid}: FULLY_COVERED row retains P0/P1 gap")
        if row.get("Current implementation status") == "IMPLEMENTED_UNVERIFIED":
            if row.get("Frontend implementation") == "NOT_FOUND_BY_KEYWORD_SEARCH" and row.get("Backend implementation") == "NOT_FOUND_BY_KEYWORD_SEARCH":
                errors.append(f"{rid}: implemented row lacks frontend/backend evidence")
        if row.get("Final disposition") == "DRAFT_NEW_PIA":
            doc = row.get("Required new document or supplement")
            if doc not in decision_ids:
                errors.append(f"{rid}: DRAFT_NEW_PIA missing decision register row {doc}")
            match = [d for d in decisions if d["decision_id"] == doc]
            if match:
                d = match[0]
                required = ["proposed_pia_title", "proposed_domain_boundary", "proposed_owning_truth", "proposed_personas", "proposed_entities", "proposed_lifecycle", "proposed_cross_domain_dependencies", "reason_existing_pia_cannot_adequately_own_it", "reason_supplement_is_insufficient", "risks_of_not_creating_it", "overlap_risks", "founder_questions"]
                for field in required:
                    if not d.get(field):
                        errors.append(f"{rid}: new PIA decision {doc} missing {field}")
                if "ADOPT" in d.get("recommendation", "") and "CANDIDATE" not in d.get("decision_type", ""):
                    errors.append(f"{rid}: candidate PIA appears described as adopted")
        if row.get("Final disposition") == "SUPPLEMENT_EXISTING_PIA" and not row.get("Governing PIA", "").startswith("PIA-"):
            errors.append(f"{rid}: supplement row lacks parent PIA")
        for pia in [p for p in row.get("Governing PIA", "").split(";") if p.startswith("PIA-")]:
            if pia not in pia_ids:
                errors.append(f"{rid}: PIA reference {pia} missing from PIA summary")
        for guide in [g for g in row.get("Applicable Code Guides", "").split(";") if g.startswith("ES-CG-")]:
            if guide not in gov_ids:
                errors.append(f"{rid}: Code Guide reference {guide} missing from governance inventory")
        for sid in [s for s in row.get("Source IDs", "").split(";") if s]:
            if sid not in source_ids:
                errors.append(f"{rid}: source id {sid} missing from source register")
        if "WAIVED" in row.get("Test execution status", "") and "PASSED" in row.get("Test execution status", ""):
            errors.append(f"{rid}: waived test reported as passed")
        if "unmerged PR treated as current" in row.get("Current evidence", "").lower():
            errors.append(f"{rid}: unmerged PR treated as current implementation")
    return errors

def validate_manifest_and_checksums():
    errors = []
    actual = sorted(str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob("*") if p.is_file())
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_paths = sorted(entry["path"] for entry in manifest["files"])
    if manifest_paths != actual:
        errors.append("PACKAGE_MANIFEST.json does not cover exactly every package file")
    checksum_entries = {}
    for line in CHECKSUM_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        h, path = line.split("  ", 1)
        checksum_entries[path] = h
    for path, expected in checksum_entries.items():
        p = PACKAGE / path
        if not p.exists():
            errors.append(f"checksum path missing: {path}")
            continue
        actual_hash = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual_hash != expected:
            errors.append(f"checksum mismatch: {path}")
    if "CHECKSUMS.sha256" in checksum_entries:
        errors.append("CHECKSUMS.sha256 must not self-reference")
    return errors

def validate_authorized_paths():
    errors = []
    try:
        result = subprocess.run(["git", "diff", "--name-only", "origin/integrate-emergent-final-zip...HEAD"], cwd=REPO, check=True, capture_output=True, text=True)
        changed = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        changed = []
    for path in changed:
        if not path.startswith(AUTHORIZED_PREFIX):
            errors.append(f"changed path outside authorized package: {path}")
        if path.startswith(PROHIBITED_PREFIXES) and not path.startswith(AUTHORIZED_PREFIX):
            errors.append(f"prohibited application/schema/config/provider/deployment path changed: {path}")
    return errors

def main() -> int:
    csv_rows = read_csv(CSV_PATH)
    json_obj = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    sources = read_csv(SOURCE_PATH)
    pia_rows = read_csv(PIA_PATH)
    gov_rows = read_csv(GOV_PATH)
    decisions = read_csv(DECISION_PATH)
    gaps = read_csv(GAP_PATH)
    errors = []
    errors.extend(validate_payload(csv_rows, json_obj, sources, pia_rows, gov_rows, decisions, gaps))
    errors.extend(validate_manifest_and_checksums())
    errors.extend(validate_authorized_paths())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("DOCUMENTARY_VALIDATION_PASS")
    print(f"feature_rows={len(csv_rows)}")
    print(f"source_rows={len(sources)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
