#!/usr/bin/env python3
"""Build mechanical register crosswalks from the immutable Facility R3 predecessor."""
from __future__ import annotations

import csv
from pathlib import Path
import shutil


HERE = Path(__file__).resolve().parent
REPO = next(parent for parent in HERE.parents if (parent / ".git").is_dir())
SOURCE = REPO / "governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE"


def transform_requirements() -> None:
    source = SOURCE / "REQUIREMENT_REGISTER.csv"
    target = HERE / "REQUIREMENT_REGISTER.csv"
    fields = [
        "requirement_id",
        "requirement_text",
        "normative_strength",
        "source_ids",
        "decision_ids",
        "owner",
        "implementation_status",
        "acceptance_id",
        "test_id",
    ]
    with source.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "requirement_id": row["requirement_id"],
                    "requirement_text": row["requirement"],
                    "normative_strength": row["normative_strength"],
                    "source_ids": row["source_ids"],
                    "decision_ids": row["decision_ids"],
                    "owner": row["owner"],
                    "implementation_status": row["implementation_status"],
                    "acceptance_id": row["acceptance_id"],
                    "test_id": row["test_id"],
                }
            )


def copy_inherited() -> None:
    names = [
        "ACCEPTANCE_CRITERIA.csv",
        "TEST_MATRIX.csv",
        "STATE_TRANSITION_MATRIX.csv",
        "PERMISSION_MATRIX.csv",
        "DATA_DICTIONARY.md",
        "WORKFLOW_REGISTER.md",
        "GOLDEN_PATHS.md",
        "ADVERSARIAL_SCENARIOS.md",
        "API_EVENT_JOB_CONTRACTS.md",
        "EVIDENCE_MANIFEST.json",
        "FAC_FD_017_ADAPTIVE_ONBOARDING_SPECIFICATION.md",
        "FAC_FD_017_ADAPTIVE_ONBOARDING_TEST_MATRIX.csv",
        "FOUNDER_DECISION_TRACEABILITY_MATRIX.csv",
        "DEPENDENCY_REGISTER.csv",
        "AS_BUILT_RECONCILIATION.md",
        "ENGINEERING_WORK_PACKAGE_REGISTER.csv",
    ]
    for name in names:
        shutil.copy2(SOURCE / name, HERE / name)


if __name__ == "__main__":
    transform_requirements()
    copy_inherited()
    print("requirements=55")
    print("copied_inherited_files=16")
