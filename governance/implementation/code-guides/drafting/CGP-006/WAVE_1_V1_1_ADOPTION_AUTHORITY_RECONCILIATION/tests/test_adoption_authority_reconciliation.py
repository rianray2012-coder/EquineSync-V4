#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
VALIDATOR = ROOT / "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION/validators/validate_adoption_authority_reconciliation.py"
spec = importlib.util.spec_from_file_location("adoption_authority_reconciliation_validator", VALIDATOR)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class AdoptionAuthorityReconciliationTests(unittest.TestCase):
    def test_package_validates(self) -> None:
        validator.validate()

    def test_fails_when_guide_marked_v1_1_adopted(self) -> None:
        rows = [{"record_id": "ES-CG-00", "adoption_state": "ADOPTED"}]
        rows += [{"record_id": guide, "adoption_state": "NOT_ADOPTED"} for guide in sorted(validator.AFFECTED - {"ES-CG-00"})]
        with self.assertRaises(AssertionError):
            validator.assert_affected_tracker_states(rows)

    def test_fails_when_guide_marked_active(self) -> None:
        rows = []
        for guide in sorted(validator.AFFECTED):
            rows.append({"guide_id": guide, "activation_state": "ACTIVE" if guide == "ES-CG-10" else "NOT_ACTIVE", "effective_date": "NONE", "authority": "GUIDE_ACTIVATION_NOT_AUTHORIZED"})
        with self.assertRaises(AssertionError):
            validator.assert_activation_states(rows)

    def test_fails_when_activation_date_introduced(self) -> None:
        rows = []
        for guide in sorted(validator.AFFECTED):
            rows.append({"guide_id": guide, "activation_state": "NOT_ACTIVE", "effective_date": "2026-07-29" if guide == "ES-CG-13" else "NONE", "authority": "GUIDE_ACTIVATION_NOT_AUTHORIZED"})
        with self.assertRaises(AssertionError):
            validator.assert_activation_states(rows)

    def test_fails_when_pr42_described_as_void_or_unauthorized(self) -> None:
        with self.assertRaises(AssertionError):
            validator.assert_no_prohibited_pr42_treatment(["PR_42_VOID"])
        with self.assertRaises(AssertionError):
            validator.assert_no_prohibited_pr42_treatment(["PR #42 was unauthorized"])

    def test_fails_when_pr42_satisfies_stage22_claimed(self) -> None:
        with self.assertRaises(AssertionError):
            validator.assert_no_stage22_claim(["PR #42 satisfies V1.1 Stage 22"])

    def test_fails_when_prohibited_path_changes(self) -> None:
        with self.assertRaises(AssertionError):
            validator.assert_changed_paths_authorized(["backend/app.py"])

    def test_fails_when_historical_pr42_file_changes(self) -> None:
        with self.assertRaises(AssertionError):
            validator.assert_changed_paths_authorized(["governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1/README.md"])

    def test_fails_when_guide_bytes_change(self) -> None:
        with self.assertRaises(AssertionError):
            validator.assert_changed_paths_authorized(["governance/implementation/code-guides/guides/ES-CG-00/README.md"])

    def test_fails_when_gap_warning_or_cgp007_closed(self) -> None:
        for text in ["GAP_0004_CLOSED", "RETAINED_WARNINGS_CLOSED", "CGP_007_ISSUED"]:
            with self.subTest(text=text):
                with self.assertRaises(AssertionError):
                    validator.assert_gap_warning_blocker_cgp007_open([text])


if __name__ == "__main__":
    unittest.main()
