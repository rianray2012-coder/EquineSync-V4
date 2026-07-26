#!/usr/bin/env python3
"""CGP-004 validator behavior tests."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

import cgp_validation as validators


CODE_GUIDE_ROOT = Path(__file__).resolve().parents[2]


class CGP004CurrentStateValidatorTests(unittest.TestCase):
    def write_csv(self, path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def test_current_cgp004_artifacts_validate(self):
        self.assertEqual(validators.validate_repository_component_register(CODE_GUIDE_ROOT).status, "PASS")
        self.assertEqual(validators.validate_repository_authority_alignment(CODE_GUIDE_ROOT).status, "PASS")
        self.assertEqual(validators.validate_current_state_assessment(CODE_GUIDE_ROOT).status, "PASS")

    def test_component_register_rejects_uncontrolled_state(self):
        fields = [
            "component_id",
            "component_name",
            "component_type",
            "repository_path",
            "deployable_unit",
            "implementation_state",
            "authority_alignment",
            "confidence",
            "evidence_basis",
            "source_ids",
            "applicable_guides",
            "owner_or_boundary",
            "risk_domains",
            "notes",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "components.csv"
            self.write_csv(
                path,
                fields,
                [
                    {
                        "component_id": "CGP004-COMP-9999",
                        "component_name": "Invalid component",
                        "component_type": "TEST",
                        "repository_path": "backend/server.py",
                        "deployable_unit": "backend-api",
                        "implementation_state": "MAGICALLY_DONE",
                        "authority_alignment": "ALIGNED_WITH_CONTROLLING_AUTHORITY",
                        "confidence": "HIGH",
                        "evidence_basis": "negative fixture",
                        "source_ids": "CGSRC-REPO-0621",
                        "applicable_guides": "ES-CG-00",
                        "owner_or_boundary": "fixture",
                        "risk_domains": "fixture",
                        "notes": "Invalid controlled value should fail.",
                    }
                ],
            )
            result = validators.validate_repository_component_register(CODE_GUIDE_ROOT, path)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any(issue.code == "invalid_implementation_state" for issue in result.issues))

    def test_authority_alignment_rejects_unknown_component(self):
        component_fields = [
            "component_id",
            "component_name",
            "component_type",
            "repository_path",
            "deployable_unit",
            "implementation_state",
            "authority_alignment",
            "confidence",
            "evidence_basis",
            "source_ids",
            "applicable_guides",
            "owner_or_boundary",
            "risk_domains",
            "notes",
        ]
        alignment_fields = [
            "alignment_id",
            "component_id",
            "repository_component",
            "repository_path",
            "authority_source_ids",
            "applicable_guides",
            "authority_alignment",
            "evidence_basis",
            "classification_rationale",
            "required_next_action",
            "confidence",
            "status",
            "notes",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            component_path = Path(tmp) / "components.csv"
            alignment_path = Path(tmp) / "alignment.csv"
            self.write_csv(component_path, component_fields, [])
            self.write_csv(
                alignment_path,
                alignment_fields,
                [
                    {
                        "alignment_id": "CGP004-ALIGN-9999",
                        "component_id": "CGP004-COMP-4040",
                        "repository_component": "Unknown",
                        "repository_path": "backend/server.py",
                        "authority_source_ids": "CGSRC-REPO-0621",
                        "applicable_guides": "ES-CG-00",
                        "authority_alignment": "ALIGNED_WITH_CONTROLLING_AUTHORITY",
                        "evidence_basis": "negative fixture",
                        "classification_rationale": "Unknown component must fail.",
                        "required_next_action": "Record valid component first.",
                        "confidence": "HIGH",
                        "status": "PARTIAL",
                        "notes": "Invalid cross-reference should fail.",
                    }
                ],
            )
            result = validators.validate_repository_authority_alignment(CODE_GUIDE_ROOT, alignment_path, component_path)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any(issue.code == "unknown_component_id" for issue in result.issues))


if __name__ == "__main__":
    unittest.main()
