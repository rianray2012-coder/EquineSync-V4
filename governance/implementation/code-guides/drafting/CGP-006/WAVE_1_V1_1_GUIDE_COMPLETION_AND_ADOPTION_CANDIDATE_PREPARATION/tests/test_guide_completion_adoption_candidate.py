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
        self.assertEqual(result["stage22_rows"], 4)

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

    def test_stage22_record_rejects_unreviewed_hash(self) -> None:
        freeze = validator.read_json(PACKAGE / "ADOPTION_CANDIDATE_BYTE_FREEZE.json")["guides"]
        rows = validator.read_csv(PACKAGE / "STAGE_22_ADOPTION_RECORD.csv")
        rows[0]["source_sha256"] = "0" * 64
        with self.assertRaises(AssertionError):
            validator.assert_stage22_record(rows, freeze)

    def test_byte_freeze_rejects_changed_adopted_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp_package = Path(td)
            source = validator.read_json(PACKAGE / "ADOPTION_CANDIDATE_BYTE_FREEZE.json")
            source["guides"][0]["sha256"] = "0" * 64
            (temp_package / "ADOPTION_CANDIDATE_BYTE_FREEZE.json").write_text(
                __import__("json").dumps(source),
                encoding="utf-8",
            )
            with self.assertRaises(AssertionError):
                validator.assert_adoption_byte_freeze(ROOT, temp_package)

    def test_guide_marked_active_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "ADOPTION_CANDIDATE_READINESS_MATRIX.csv")
        rows[0]["activation_state"] = "ACTIVE"
        with self.assertRaises(AssertionError):
            validator.assert_stage22_adoption_boundaries(PACKAGE, rows)

    def test_activation_date_introduced_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "ADOPTION_CANDIDATE_READINESS_MATRIX.csv")
        rows[0]["activation_effective_date"] = "2026-07-29"
        with self.assertRaises(AssertionError):
            validator.assert_stage22_adoption_boundaries(PACKAGE, rows)

    def test_warning_closed_fails(self) -> None:
        findings = validator.read_csv(PACKAGE / "OPEN_FINDING_REGISTER.csv")
        retained = validator.read_csv(PACKAGE / "RETAINED_CONDITION_WARNING_GAP_REGISTER.csv")
        for row in retained:
            if row["record_id"] == "CGP006-CLF-0001":
                row["current_state"] = "CLOSED"
        with self.assertRaises(AssertionError):
            validator.assert_finding_treatment(findings, retained)

    def test_gap_0004_closed_fails(self) -> None:
        findings = validator.read_csv(PACKAGE / "OPEN_FINDING_REGISTER.csv")
        retained = validator.read_csv(PACKAGE / "RETAINED_CONDITION_WARNING_GAP_REGISTER.csv")
        for row in retained:
            if row["record_id"] == "CGP005-TA-APP-GAP-0004":
                row["current_state"] = "GAP_0004_CLOSED"
        with self.assertRaises(AssertionError):
            validator.assert_finding_treatment(findings, retained)

    def test_stage22_adoption_row_lacks_founder_disposition_fails(self) -> None:
        freeze = validator.read_json(PACKAGE / "ADOPTION_CANDIDATE_BYTE_FREEZE.json")["guides"]
        rows = validator.read_csv(PACKAGE / "STAGE_22_ADOPTION_RECORD.csv")
        rows[0]["founder_disposition"] = ""
        with self.assertRaises(AssertionError):
            validator.assert_stage22_record(rows, freeze)

    def test_premature_custody_claim_fails(self) -> None:
        freeze = validator.read_json(PACKAGE / "ADOPTION_CANDIDATE_BYTE_FREEZE.json")["guides"]
        rows = validator.read_csv(PACKAGE / "STAGE_22_ADOPTION_RECORD.csv")
        rows[0]["custody_state"] = "CUSTODY_COMPLETE"
        with self.assertRaises(AssertionError):
            validator.assert_stage22_record(rows, freeze)

    def test_custody_receipt_missing_merge_metadata_fails(self) -> None:
        with self.assertRaises(AssertionError):
            validator.assert_custody_receipt_complete(
                "CGP_006_WAVE_1_V1_1_STAGE_22_ADOPTION_AND_STAGE_23_PROTECTED_ACCESSION_CUSTODY_COMPLETE"
            )

    def test_historical_pr42_record_rewrite_fails(self) -> None:
        with self.assertRaises(AssertionError):
            validator.assert_historical_pr42_preserved([
                "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION/FOUNDER_ADOPTION_AUTHORITY_DISPOSITION.md"
            ])

    def test_implementation_claim_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "ADOPTION_CANDIDATE_READINESS_MATRIX.csv")
        with tempfile.TemporaryDirectory() as td:
            temp_package = Path(td)
            (temp_package / "claim.md").write_text("IMPLEMENTATION_CLAIMED", encoding="utf-8")
            with self.assertRaises(AssertionError):
                validator.assert_stage22_adoption_boundaries(temp_package, rows)

    def test_runtime_evidence_claim_fails(self) -> None:
        rows = validator.read_csv(PACKAGE / "ADOPTION_CANDIDATE_READINESS_MATRIX.csv")
        with tempfile.TemporaryDirectory() as td:
            temp_package = Path(td)
            (temp_package / "claim.md").write_text("RUNTIME_EVIDENCE_CLAIMED", encoding="utf-8")
            with self.assertRaises(AssertionError):
                validator.assert_stage22_adoption_boundaries(temp_package, rows)

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
