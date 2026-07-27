#!/usr/bin/env python3
"""CGP-006 Wave 1 adoption-readiness validator tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_cgp006_wave1_adoption_readiness


CODE_GUIDE_ROOT = Path(__file__).resolve().parents[2]


class CGP006Wave1AdoptionReadinessValidatorTests(unittest.TestCase):
    def test_current_adoption_readiness_package_validates(self):
        result = validate_cgp006_wave1_adoption_readiness.validate_cgp006_wave1_adoption_readiness(CODE_GUIDE_ROOT)
        self.assertEqual(result.status, "PASS", result.to_dict())
        self.assertEqual(result.summary["guides_reviewed"], 4)
        self.assertEqual(result.summary["controls_reviewed"], 22)
        self.assertEqual(result.summary["invariants_reviewed"], 22)
        self.assertEqual(result.summary["mandatory_questions_reviewed"], 32)
        self.assertEqual(result.summary["warnings_reviewed"], 5)
        self.assertEqual(result.summary["gap0004_records"], 1)
        self.assertEqual(result.summary["founder_decisions_required"], 0)

    def test_missing_package_fails(self):
        original = validate_cgp006_wave1_adoption_readiness.PACKAGE_REL
        try:
            validate_cgp006_wave1_adoption_readiness.PACKAGE_REL = Path("drafting/CGP-006/MISSING_ADOPTION_READINESS_PACKAGE")
            result = validate_cgp006_wave1_adoption_readiness.validate_cgp006_wave1_adoption_readiness(CODE_GUIDE_ROOT)
        finally:
            validate_cgp006_wave1_adoption_readiness.PACKAGE_REL = original
        self.assertEqual(result.status, "FAIL", result.to_dict())
        self.assertTrue(any(issue.code == "missing_package" for issue in result.issues), result.to_dict())


if __name__ == "__main__":
    unittest.main()
