#!/usr/bin/env python3
"""Deterministic validator for the Facility PIA V1.0.1 review candidate."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_DECISIONS = {f"FAC-FD-{i:03d}" for i in range(1, 19)}
APPROVED = "FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED"
FINAL_REQUIRED = {
    "SEGREGATED_REVIEW_REPORT.md",
    "ADVERSARIAL_CHALLENGE_REPORT.md",
    "DOMAIN_REVIEW_REPORT.md",
    "MACHINE_VALIDATION_REPORT.md",
    "SYNTHETIC_GOLDEN_PATH_REPORT.md",
    "EVIDENCE_CUSTODY_REPORT.md",
    "STRUCTURED_REVIEW_FINDINGS_REGISTER.csv",
    "STRUCTURED_REVIEW_CORRECTION_LOG.csv",
    "STRUCTURED_REVIEW_TRACEABILITY_MATRIX.csv",
    "FINAL_STRUCTURED_REVIEW_DISPOSITION.md",
    "CHANGE_MANIFEST.txt",
    "WORK_COMPLETENESS_LEDGER.csv",
    "CLAIM_TO_EVIDENCE_REGISTER.csv",
    "OMISSION_REGISTER.csv",
    "CROSS_AGENT_DISCREPANCY_REGISTER.csv",
    "WHAT_THIS_REVIEW_DID_NOT_ESTABLISH.md",
}
SEALED = {
    "source_evidence/CURRENT_PIA_APPROVAL_STATUS.md": "8abfbe0b1be12fcdd9d488659ca68f691e92da47bce1291176791d709baf237e",
    "source_evidence/FACILITY_PIA_FOUNDER_DECISION_REGISTER_SEED.csv": "c4b23a91fb9681e95a58fd8e82563414b3fbef9f92a2d24af3e9ae8780d72b45",
    "source_evidence/FACILITY_PIA_SCOPE_AND_BOUNDARY_SEED.md": "d01b40bf393a4dfab7e78dee321c55a9f01613e07e405a6a417d411a7d540f08",
    "source_evidence/HANDOFF_PACKAGE_MANIFEST.json": "bb348cc18cdfcf23702bf2e34c8d8d0f5c65161cc6b70dff6053e06c59b9163c",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


checks: list[dict[str, object]] = []


def check(check_id: str, condition: bool, evidence: object) -> None:
    checks.append({"check_id": check_id, "result": "PASSED" if condition else "FAILED", "evidence": evidence})


manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
machine = json.loads((ROOT / "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json").read_text(encoding="utf-8"))
decisions = read_csv("FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv")
requirements = read_csv("REQUIREMENT_REGISTER.csv")
criteria = read_csv("ACCEPTANCE_CRITERIA.csv")
tests = read_csv("TEST_MATRIX.csv")
trace = read_csv("FOUNDER_DECISION_TRACEABILITY_MATRIX.csv")

check("MV-001-manifest-files", all((ROOT / row["path"]).is_file() for row in manifest["files"]), len(manifest["files"]))
manifest_mismatch = [row["path"] for row in manifest["files"] if digest(ROOT / row["path"]) != row["sha256"] or (ROOT / row["path"]).stat().st_size != row["bytes"]]
check("MV-002-manifest-hashes", not manifest_mismatch, manifest_mismatch)

checksum_mismatch = []
for line in (ROOT / "CHECKSUMS.sha256").read_text(encoding="utf-8").splitlines():
    expected, rel = line.split("  ", 1)
    if not (ROOT / rel).is_file() or digest(ROOT / rel) != expected:
        checksum_mismatch.append(rel)
check("MV-003-checksums", not checksum_mismatch, checksum_mismatch)
check("MV-004-checksum-alias", (ROOT / "CHECKSUMS.sha256").read_bytes() == (ROOT / "CHECKSUM_MANIFEST.sha256").read_bytes(), "byte parity")

all_files = [p for p in ROOT.rglob("*") if p.is_file()]
allowed_suffixes = {".md", ".csv", ".json", ".py", ".sha256", ".txt"}
check("MV-005-authorized-file-types", all(p.suffix in allowed_suffixes for p in all_files), [p.name for p in all_files if p.suffix not in allowed_suffixes])

decision_ids = {row["decision_id"] for row in decisions}
check("MV-006-decisions-complete", decision_ids == EXPECTED_DECISIONS, sorted(decision_ids))
check("MV-007-decision-status", all(row["status"] == APPROVED and row["founder_disposition"] == APPROVED for row in decisions), "18 approved-design statuses")
check("MV-008-decision-authority", all(row["implementation_authority"] == "FALSE" and row["adoption_status"] == "NOT_ADOPTED" and row["lock_status"] == "NOT_LOCKED" for row in decisions), "all false/not adopted/not locked")
check("MV-009-fd17-refinement", "horse owner" in (ROOT / "FAC_FD_017_ADAPTIVE_ONBOARDING_SPECIFICATION.md").read_text(encoding="utf-8").lower() and "not required to create a facility" in (ROOT / "FAC_FD_017_ADAPTIVE_ONBOARDING_SPECIFICATION.md").read_text(encoding="utf-8").lower(), "adaptive spec")

req_ids = [row["requirement_id"] for row in requirements]
ac_ids = [row["acceptance_id"] for row in criteria]
test_ids = [row["test_id"] for row in tests]
check("MV-010-unique-identifiers", len(req_ids) == len(set(req_ids)) and len(ac_ids) == len(set(ac_ids)) and len(test_ids) == len(set(test_ids)), {"requirements": len(req_ids), "criteria": len(ac_ids), "tests": len(test_ids)})
check("MV-011-counts", (len(requirements), len(criteria), len(tests), len(trace)) == (55, 55, 85, 18), {"requirements": len(requirements), "criteria": len(criteria), "tests": len(tests), "trace": len(trace)})

ac_by_req = {row["requirement_id"] for row in criteria}
tests_by_req = {row["requirement_id"] for row in tests}
check("MV-012-requirement-mapping", all(row["requirement_id"] in ac_by_req and row["requirement_id"] in tests_by_req for row in requirements), "every requirement has acceptance and tests")
new_types: dict[str, set[str]] = {}
for row in tests:
    if int(row["requirement_id"].rsplit("-", 1)[1]) >= 41:
        new_types.setdefault(row["requirement_id"], set()).add(row["test_type"])
check("MV-013-positive-negative-boundary", all(types == {"POSITIVE_DESIGN", "NEGATIVE_DESIGN", "BOUNDARY_DESIGN"} for types in new_types.values()) and len(new_types) == 15, {key: sorted(value) for key, value in new_types.items()})

trace_decisions = {row["decision_id"] for row in trace}
check("MV-014-decision-trace", trace_decisions == EXPECTED_DECISIONS and all(row["requirement_ids"] and row["acceptance_ids"] and row["test_ids"] and row["risk_or_control_ids"] for row in trace), sorted(trace_decisions))
check("MV-015-permission-alias", (ROOT / "PERMISSION_MATRIX.csv").read_bytes() == (ROOT / "PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv").read_bytes(), "byte parity")

sealed_mismatch = [rel for rel, expected in SEALED.items() if not (ROOT / rel).is_file() or digest(ROOT / rel) != expected]
check("MV-016-sealed-sources", not sealed_mismatch, sealed_mismatch)
check("MV-017-founder-directive-hash", digest(ROOT / "source_evidence/FOUNDER_DIRECTIVE_FAC_FD_001_THROUGH_FAC_FD_018.md") == "7bd8fa59f4720f261194f1148f4a0f19665f91700656e0632953e40079438ac4", "recalculated")

check("MV-018-authority-false", manifest["implementation_authority"] is False and machine["implementation_authority"] is False and machine["implementation_activity"] is False, "manifest and machine record")
check("MV-019-not-adopted-locked", manifest["adopted"] is False and manifest["locked"] is False and machine["adopted"] is False and machine["locked"] is False, "manifest and machine record")
machine_text = json.dumps(machine).lower()
check("MV-020-identity-segregation", machine["segregation_boundary"]["identity_relationships_successor_founder_approved"] is False and "identity_relationships_successor_founder_approved\": true" not in machine_text, "explicit false")

md_refs = []
broken_refs = []
external_refs = {"W1_RF01_TENANT_AND_FACILITY_ISOLATION_REPORT.md"}
for path in ROOT.glob("*.md"):
    text = path.read_text(encoding="utf-8")
    for ref in re.findall(r"`([^`]+\.(?:md|csv|json|sha256|txt))`", text):
        if ("/" not in ref or ref.startswith("source_evidence/")) and ref not in external_refs:
            md_refs.append((path.name, ref))
            if not (ROOT / ref).exists():
                broken_refs.append((path.name, ref))
check("MV-021-measurable-references", not broken_refs, {"examined": len(md_refs), "broken": broken_refs})

final_stage = (ROOT / "FINAL_STRUCTURED_REVIEW_DISPOSITION.md").exists()
if final_stage:
    missing = sorted(name for name in FINAL_REQUIRED if not (ROOT / name).is_file())
    check("MV-022-final-required-artifacts", not missing, missing)
    findings = read_csv("STRUCTURED_REVIEW_FINDINGS_REGISTER.csv")
    allowed_severity = {"P0", "P1", "P2", "P3"}
    check("MV-023-finding-severity-values", all(row["severity"] in allowed_severity for row in findings), sorted({row["severity"] for row in findings}))

failed = [row for row in checks if row["result"] == "FAILED"]
result = {
    "schema_version": "1.0.0",
    "package_id": manifest["package_id"],
    "stage": "FINAL" if final_stage else "DESIGN_FREEZE",
    "environment": {"python": sys.version.split()[0], "platform": platform.platform()},
    "checks_executed": len(checks),
    "checks_passed": len(checks) - len(failed),
    "checks_failed": len(failed),
    "result": "PASSED" if not failed else "FAILED",
    "checks": checks,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if not failed else 1)
