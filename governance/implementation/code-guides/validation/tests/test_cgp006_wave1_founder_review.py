#!/usr/bin/env python3
"""CGP-006 Wave 1 structured Founder-review validator tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_cgp006_wave1_founder_review


CODE_GUIDE_ROOT = Path(__file__).resolve().parents[2]


class CGP006Wave1FounderReviewValidatorTests(unittest.TestCase):
    def test_current_founder_review_package_validates(self):
        result = validate_cgp006_wave1_founder_review.validate_cgp006_wave1_founder_review(CODE_GUIDE_ROOT)
        self.assertEqual(result.status, "PASS", result.to_dict())

    def test_missing_review_package_fails(self):
        original = validate_cgp006_wave1_founder_review.PACKAGE_REL
        try:
            validate_cgp006_wave1_founder_review.PACKAGE_REL = Path("drafting/CGP-006/MISSING_REVIEW_PACKAGE")
            result = validate_cgp006_wave1_founder_review.validate_cgp006_wave1_founder_review(CODE_GUIDE_ROOT)
        finally:
            validate_cgp006_wave1_founder_review.PACKAGE_REL = original
        self.assertEqual(result.status, "FAIL", result.to_dict())
        self.assertTrue(any(issue.code == "missing_package" for issue in result.issues), result.to_dict())


if __name__ == "__main__":
    unittest.main()
