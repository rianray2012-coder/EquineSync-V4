#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
PACKAGE = ROOT / "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION"
VALIDATOR = PACKAGE / "validators/validate_guide_completion_adoption_candidate.py"
spec = importlib.util.spec_from_file_location("guide_completion_validator", VALIDATOR)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class GuideCompletionAdoptionCandidateTests(unittest.TestCase):
    def test_positive_package_validates(self) -> None:
        result = validator.validate()
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["controls"], 22)
        self.assertEqual(result["questions"], 32)

    def test_missing_file_fixture_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(AssertionError):
                validator.assert_required_files(Path(td))

    def test_malformed_csv_fixture_fails(self) -> None:
        with self.assertRaises(AssertionError):
            validator.read_csv(PACKAGE / "tests/fixtures/malformed_csv/broken.csv")

    def test_malformed_json_fixture_fails(self) -> None:
        with self.assertRaises(Exception):
            validator.read_json(PACKAGE / "tests/fixtures/malformed_json/broken.json")

    def test_duplicate_id_fixture_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "tests/fixtures/duplicate_id/duplicate.csv")
        with self.assertRaises(AssertionError):
            validator.assert_unique_ids(rows, "identifier")

    def test_invalid_controlled_value_fixture_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "tests/fixtures/invalid_controlled_value/stage22.csv")
        with self.assertRaises(AssertionError):
            validator.assert_stage_matrix(rows)

    def test_incomplete_question_fixture_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "tests/fixtures/incomplete_question/question.csv")
        with self.assertRaises(AssertionError):
            validator.assert_questions_complete(rows)

    def test_prohibited_implementation_mapping_fixture_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "tests/fixtures/prohibited_mapping/mapping.csv")
        with self.assertRaises(AssertionError):
            validator.assert_repository_traceability(rows)

    def test_false_adoption_fixture_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "tests/fixtures/false_adoption/readiness.csv")
        with self.assertRaises(AssertionError):
            validator.assert_no_false_adoption_activation(PACKAGE, rows)

    def test_false_activation_fixture_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "tests/fixtures/false_activation/readiness.csv")
        with self.assertRaises(AssertionError):
            validator.assert_no_false_adoption_activation(PACKAGE, rows)

    def test_unsupported_evidence_grade_fixture_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "tests/fixtures/unsupported_evidence_grade/grade.csv")
        with self.assertRaises(AssertionError):
            validator.assert_evidence_grades(rows)

    def test_broken_reference_fixture_fails(self) -> None:
        controls = validator.read_csv(PACKAGE / "tests/fixtures/broken_reference/control.csv")
        invariants = [{"invariant_id": "OTHER", "related_controls": "C1"}]
        with self.assertRaises(AssertionError):
            validator.assert_references(controls, invariants, [], [], [])

    def test_checksum_failure_fixture_fails(self) -> None:
        with self.assertRaises(AssertionError):
            validator.assert_checksum_digest(PACKAGE / "tests/fixtures/checksum_failure/file.txt", "0" * 64)

    def test_unauthorized_path_fixture_fails(self) -> None:
        paths = (PACKAGE / "tests/fixtures/unauthorized_path/path.txt").read_text().splitlines()
        with self.assertRaises(AssertionError):
            validator.assert_changed_paths_authorized(paths)


if __name__ == "__main__":
    unittest.main()
