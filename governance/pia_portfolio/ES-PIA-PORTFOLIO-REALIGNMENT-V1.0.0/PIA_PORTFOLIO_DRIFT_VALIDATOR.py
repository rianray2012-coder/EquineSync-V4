#!/usr/bin/env python3
"""Fail-closed validator for the Founder-directed ten-item PIA portfolio."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
POSITIONS = [f"{value:02d}" for value in range(1, 11)]
TITLES = {
    "01": "Identity, Account, Actor, and Onboarding",
    "02": "Facility, Tenant, and Organizational Structure",
    "03": "Relationship, Authorization, and Permission",
    "04": "Horse Identity, Profile, and Lifecycle",
    "05": "Core Navigation, Search, and Application Shell",
    "06": "Task, Calendar, Scheduling, and Notification",
    "07": "Care Operations",
    "08": "Lessons, Training, Rider, and Guardian",
    "09": "Billing, Payments, and Financial Operations",
    "10": "Owner Portal and Communications",
}
ALLOWED_CLASSES = {
    "PRIMARY_PIA_PACKAGE",
    "PIA_COMPONENT_PACKAGE",
    "SUBORDINATE_ADR_OR_CONTRACT",
    "CROSS_PIA_REVIEW_PACKAGE",
    "CROSS_PIA_REMEDIATION_PACKAGE",
    "PIA_HANDOFF_PACKAGE",
    "CONTROLLING_PIA_STANDARD",
    "CONSTITUTIONAL_OR_CANONICAL_SOURCE",
    "MIAP_CROSS_CUTTING_PROFILE",
    "ASSURANCE_TOOLING",
    "ENGINEERING_WORK_PACKAGE",
    "HISTORICAL_SUPERSEDED",
    "NON_PIA_UNRELATED",
}
REQUIRED_FILES = {
    "PIA_PORTFOLIO_REALIGNMENT_REGISTER.md",
    "PIA_PORTFOLIO_REALIGNMENT_REGISTER.csv",
    "PIA_PORTFOLIO_MACHINE_READABLE.json",
    "PIA_PACKAGE_INVENTORY.csv",
    "PIA_PACKAGE_PLACEMENT_AND_SUPERSESSION_MAP.csv",
    "PIA_COMPONENT_OWNERSHIP_MAP.csv",
    "PIA_CROSS_CUTTING_ARTIFACT_CLASSIFICATION.csv",
    "PIA_PORTFOLIO_DRIFT_PREVENTION_RULES.md",
    "PIA_PORTFOLIO_DRIFT_VALIDATOR.py",
    "FOUNDER_DIRECTED_PORTFOLIO_LOCK_RECORD.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validation/REPOSITORY_DISCOVERY_REPORT.md",
    "validation/REPOSITORY_DISCOVERY_REPORT.json",
    "validation/DRIFT_VALIDATION_REPORT.md",
    "validation/DRIFT_VALIDATION_REPORT.json",
    "validation/SOURCE_GAPS.csv",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    findings: list[str] = []

    present = {path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file()}
    missing = sorted(REQUIRED_FILES - present)
    if missing:
        findings.append(f"REQUIRED_FILES_MISSING:{','.join(missing)}")

    register = load_csv("PIA_PORTFOLIO_REALIGNMENT_REGISTER.csv")
    inventory = load_csv("PIA_PACKAGE_INVENTORY.csv")
    components = load_csv("PIA_COMPONENT_OWNERSHIP_MAP.csv")
    machine = json.loads((ROOT / "PIA_PORTFOLIO_MACHINE_READABLE.json").read_text())

    actual_positions = [item["position"] for item in register]
    if actual_positions != POSITIONS:
        findings.append(f"PORTFOLIO_POSITION_DRIFT:{actual_positions}")
    if len(set(actual_positions)) != 10:
        findings.append("PORTFOLIO_POSITION_DUPLICATE_OR_MISSING")
    for item in register:
        if item["position"] not in TITLES:
            findings.append(f"POSITION_OUTSIDE_01_10:{item['position']}")
        elif item["controlling_title"] != TITLES[item["position"]]:
            findings.append(f"CONTROLLING_TITLE_DRIFT:{item['position']}")
        if item["implementation_authority"] != "FALSE":
            findings.append(f"IMPLEMENTATION_AUTHORITY_INFLATION:{item['position']}")

    ids: set[str] = set()
    for item in inventory:
        aid = item["artifact_id"]
        if aid in ids:
            findings.append(f"DUPLICATE_ARTIFACT_ID:{aid}")
        ids.add(aid)
        if item["artifact_class"] not in ALLOWED_CLASSES:
            findings.append(f"UNCLASSIFIED_OR_INVALID_CLASS:{aid}:{item['artifact_class']}")
        primary = item["primary_portfolio_position"]
        if primary != "NONE" and primary not in POSITIONS:
            findings.append(f"POSITION_OUTSIDE_01_10:{aid}:{primary}")
        for dependent in filter(None, item["dependent_positions"].split(";")):
            if dependent != "NONE" and dependent not in POSITIONS:
                findings.append(f"DEPENDENT_POSITION_OUTSIDE_01_10:{aid}:{dependent}")
        if item["implementation_authority"] != "FALSE":
            findings.append(f"IMPLEMENTATION_AUTHORITY_INFLATION:{aid}")
        if not item["artifact_hash"] or not item["path"] or not item["branch"] or not item["commit"]:
            findings.append(f"INCOMPLETE_INVENTORY_RECORD:{aid}")

        upper = f"{item['artifact_id']} {item['artifact_name']} {item['path']}".upper()
        if "STAGE_2A" in upper or "STAGE2A" in upper:
            if item["artifact_class"] != "MIAP_CROSS_CUTTING_PROFILE":
                findings.append(f"STAGE2A_PROMOTED_TO_PIA:{aid}")
        if "/ADOPTED_SOURCES/" in upper or "-CANON" in upper:
            if item["artifact_class"] != "CONSTITUTIONAL_OR_CANONICAL_SOURCE":
                findings.append(f"CANON_PROMOTED_OR_MISCLASSIFIED:{aid}")
        if aid.startswith("ADR-") and item["artifact_class"] != "SUBORDINATE_ADR_OR_CONTRACT":
            findings.append(f"ADR_PROMOTED_TO_PIA:{aid}")
        if aid == "ES-REM-2026-001":
            if item["artifact_class"] != "CROSS_PIA_REMEDIATION_PACKAGE" or item["founder_approval_status"] != "NOT_FOUNDER_APPROVED":
                findings.append("SUCCESSOR_REMEDIATION_STATUS_INFLATION")
        if aid == "ES-PIA-IDENTITY-ONBOARDING-V1.1.0":
            status = item["founder_approval_status"]
            if "CURRENT_SUCCESSOR_TEXT_NOT_FOUNDER_APPROVED" not in status:
                findings.append("IDENTITY_SUCCESSOR_TEXT_APPROVAL_INFLATION")
        if aid == "ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0":
            status = item["founder_approval_status"]
            if not status.startswith("CURRENT_TEXT_NOT_FOUNDER_APPROVED"):
                findings.append("RELATIONSHIPS_SUCCESSOR_TEXT_APPROVAL_INFLATION")
        if aid.startswith("ADR-IDENTITY-") or aid.startswith("ADR-REL-"):
            if item["founder_approval_status"] != "NOT_FOUNDER_APPROVED":
                findings.append(f"CANDIDATE_ADR_APPROVAL_INFLATION:{aid}")

    enrollment_components = [item for item in components if item["name"] == "Enrollment and Onboarding"]
    if len(enrollment_components) != 1 or enrollment_components[0]["position"] != "01":
        findings.append("ENROLLMENT_BECAME_ELEVENTH_PIA")
    component03 = {(item["component"], item["name"]) for item in components if item["position"] == "03"}
    required03 = {("A", "Relationships and Delegated Authority"), ("B", "Authorization"), ("C", "Permission")}
    if not required03.issubset(component03):
        findings.append("ITEM_03_COMPONENT_BOUNDARY_DRIFT")
    for item in components:
        if item["implementation_authority"] != "FALSE":
            findings.append(f"COMPONENT_IMPLEMENTATION_AUTHORITY_INFLATION:{item['position']}:{item['component']}")

    if machine.get("inventory_denominator") != len(inventory):
        findings.append("INVENTORY_DENOMINATOR_MISMATCH")
    if machine.get("unclassified_count") != 0:
        findings.append("UNCLASSIFIED_COUNT_NONZERO")
    if machine.get("implementation_authority") is not False:
        findings.append("MACHINE_IMPLEMENTATION_AUTHORITY_INFLATION")
    if machine.get("segregation_boundary") != "FRESH_IDENTITY_RELATIONSHIPS_REVIEW_NOT_MODIFIED_OR_REPRESENTED_AS_APPROVED":
        findings.append("SEGREGATION_BOUNDARY_MISSING")

    retired_term = "M" + "AIP"
    text_extensions = {".md", ".csv", ".json", ".txt", ".py", ".sha256"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in text_extensions:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(rf"\b{retired_term}\b", text):
            findings.append(f"RETIRED_TERMINOLOGY_ACTIVE:{path.relative_to(ROOT)}")

    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text())
    manifest_paths = {entry["path"] for entry in manifest["files"]}
    expected_manifest_paths = present - {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}
    if manifest_paths != expected_manifest_paths:
        findings.append("PACKAGE_MANIFEST_FILE_SET_MISMATCH")
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        if not path.is_file() or path.stat().st_size != entry["bytes"] or sha256(path) != entry["sha256"]:
            findings.append(f"PACKAGE_MANIFEST_INTEGRITY_FAILURE:{entry['path']}")

    checksum_lines = (ROOT / "CHECKSUM_MANIFEST.sha256").read_text().splitlines()
    checksum_paths: set[str] = set()
    for line in checksum_lines:
        digest, rel = line.split("  ", 1)
        checksum_paths.add(rel)
        path = ROOT / rel
        if not path.is_file() or sha256(path) != digest:
            findings.append(f"CHECKSUM_FAILURE:{rel}")
    expected_checksum_paths = present - {"CHECKSUM_MANIFEST.sha256"}
    if checksum_paths != expected_checksum_paths:
        findings.append("CHECKSUM_FILE_SET_MISMATCH")

    result = {
        "result": "PASS" if not findings else "FAIL",
        "disposition": "TEN_ITEM_PIA_PORTFOLIO_REALIGNED_AND_DRIFT_CONTROLS_ACTIVE" if not findings else "PORTFOLIO_DRIFT_VALIDATION_FAILED",
        "positions": len(register),
        "inventory_denominator": len(inventory),
        "unclassified_count": sum(1 for item in inventory if item["artifact_class"] not in ALLOWED_CLASSES),
        "findings": findings,
        "implementation_activity": "NONE",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
