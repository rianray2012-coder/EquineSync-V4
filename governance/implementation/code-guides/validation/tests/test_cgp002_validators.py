#!/usr/bin/env python3
"""Unit tests for CGP-002 validators and fixtures."""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parents[1]
CODE_GUIDE_ROOT = VALIDATION_DIR.parent
sys.path.insert(0, str(VALIDATION_DIR))

import cgp_validation as cv  # noqa: E402


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def result_codes(result: cv.ValidationResult) -> set[str]:
    return {issue.code for issue in result.issues}


class Cgp002ValidatorTests(unittest.TestCase):
    def test_positive_fixtures_pass_for_applicable_validators(self):
        positive = FIXTURES / "positive"
        self.assertEqual(cv.validate_control_registry(CODE_GUIDE_ROOT, positive / "control_register_valid.csv").status, "PASS")
        self.assertEqual(cv.validate_invariant_registry(CODE_GUIDE_ROOT, positive / "invariant_register_valid.csv").status, "PASS")
        self.assertEqual(cv.validate_guide_questions(CODE_GUIDE_ROOT, positive / "guide_questions_valid.csv").status, "PASS")
        self.assertEqual(cv.validate_guide_dependencies(CODE_GUIDE_ROOT, positive / "dependency_valid.csv").status, "PASS")
        self.assertEqual(cv.validate_exceptions(CODE_GUIDE_ROOT, positive / "exceptions_valid.csv").status, "PASS")

    def test_negative_register_fixtures_fail_for_specific_reasons(self):
        negative = FIXTURES / "negative"
        cases = [
            (cv.validate_control_registry, "duplicate_control_ids.csv", "duplicate_control_id"),
            (cv.validate_invariant_registry, "duplicate_invariant_ids.csv", "duplicate_invariant_id"),
            (cv.validate_control_registry, "missing_governing_authority.csv", "missing_governing_authority"),
            (cv.validate_invariant_registry, "missing_verification_method.csv", "missing_verification_method"),
            (cv.validate_control_registry, "invalid_assurance_class.csv", "invalid_assurance_class"),
            (cv.validate_control_registry, "invalid_evidence_grade.csv", "invalid_evidence_grade"),
            (cv.validate_guide_questions, "unanswered_required_question.csv", "unanswered_required_question"),
            (cv.validate_guide_dependencies, "broken_guide_dependency.csv", "missing_upstream_guide"),
            (cv.validate_guide_dependencies, "circular_dependency.csv", "circular_dependency"),
            (cv.validate_exceptions, "expired_exception.csv", "expired_exception"),
            (cv.validate_control_registry, "missing_activation_boundary.csv", "missing_activation_boundary"),
            (cv.validate_control_registry, "high_risk_no_negative_test.csv", "missing_high_risk_negative_test"),
            (cv.validate_guide_dependencies, "superseded_control_no_compatibility.csv", "superseded_control_without_compatibility"),
            (cv.validate_control_registry, "unrecognized_controlled_value.csv", "unrecognized_controlled_value"),
        ]
        for func, filename, code in cases:
            with self.subTest(filename=filename, code=code):
                result = func(CODE_GUIDE_ROOT, negative / filename)
                self.assertEqual(result.status, "FAIL")
                self.assertIn(code, result_codes(result))

    def test_malformed_csv_fixture_fails(self):
        result = cv.ValidationResult("malformed-csv-test")
        cv.read_csv_strict(FIXTURES / "negative" / "malformed.csv", result)
        result.finalize()
        self.assertEqual(result.status, "FAIL")
        self.assertIn("malformed_csv", result_codes(result))

    def test_malformed_json_fixture_fails(self):
        with self.assertRaises(json.JSONDecodeError):
            json.loads((FIXTURES / "schemas" / "negative" / "malformed_json.json").read_text(encoding="utf-8"))

    def test_missing_evidence_artifact_fails(self):
        result = cv.validate_evidence_records(CODE_GUIDE_ROOT, FIXTURES / "negative" / "evidence_missing_artifact.csv")
        self.assertEqual(result.status, "FAIL")
        self.assertIn("missing_evidence_artifact", result_codes(result))

    def test_placeholder_falsely_adopted_fails_portfolio_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp) / "governance" / "implementation" / "code-guides"
            tmp_root.mkdir(parents=True)
            for child in ("schemas", "registers", "guides/ES-CG-00"):
                (tmp_root / child).mkdir(parents=True, exist_ok=True)
            (tmp_root / "schemas" / "CODE_GUIDE_CONTROLLED_VALUES.json").write_text(
                (CODE_GUIDE_ROOT / "schemas" / "CODE_GUIDE_CONTROLLED_VALUES.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (tmp_root / "CONTROLLED_VALUES.md").write_text(
                (CODE_GUIDE_ROOT / "CONTROLLED_VALUES.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (tmp_root / "registers" / "CODE_GUIDE_CONTROL_REGISTER.csv").write_text(
                (CODE_GUIDE_ROOT / "registers" / "CODE_GUIDE_CONTROL_REGISTER.csv").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (tmp_root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv").write_text(
                (FIXTURES / "negative" / "adopted_without_accession_tracker.csv").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = cv.validate_portfolio_consistency(tmp_root)
            self.assertEqual(result.status, "FAIL")
            self.assertIn("adopted_guide_without_accession", result_codes(result))

    def test_package_integrity_negative_fixtures_fail(self):
        for dirname, code in [
            ("checksum_mismatch_package", "checksum_mismatch"),
            ("manifest_omission_package", "package_manifest_omission"),
        ]:
            with self.subTest(dirname=dirname):
                fixture_root = FIXTURES / "negative" / dirname
                result = cv.validate_package_integrity(fixture_root, fixture_root / "packages" / "CGP_002_CREATED_ARTIFACT_MANIFEST.json")
                self.assertEqual(result.status, "FAIL")
                self.assertIn(code, result_codes(result))

    def test_schema_fixtures_parse_and_validate_controlled_values(self):
        for path in (FIXTURES / "schemas" / "positive").glob("*.json"):
            with self.subTest(path=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(data["schema_version"], "0.2.0")
        negative = json.loads((FIXTURES / "schemas" / "negative" / "invalid_control_assurance_class.json").read_text(encoding="utf-8"))
        self.assertEqual(negative["assurance_class"], "A9_UNKNOWN")


if __name__ == "__main__":
    unittest.main()
