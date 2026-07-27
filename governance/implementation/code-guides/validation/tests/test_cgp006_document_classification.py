#!/usr/bin/env python3
"""CGP-006 document classification package validator tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_cgp006_document_classification


CODE_GUIDE_ROOT = Path(__file__).resolve().parents[2]


class CGP006DocumentClassificationValidatorTests(unittest.TestCase):
    def test_current_cgp006_document_classification_package_validates(self):
        result = validate_cgp006_document_classification.validate_cgp006_document_classification(CODE_GUIDE_ROOT)
        self.assertEqual(result.status, "PASS", result.to_dict())

    def test_missing_required_file_fails(self):
        result = validate_cgp006_document_classification.validate_cgp006_document_classification(
            CODE_GUIDE_ROOT,
            required_files=("CGP_006_DOCUMENT_CLASSIFICATION_REPORT.md", "MISSING_CGP006_CLASSIFICATION_FILE.md"),
        )
        self.assertEqual(result.status, "FAIL", result.to_dict())
        self.assertTrue(
            any(issue.code == "missing_classification_artifact" for issue in result.issues),
            result.to_dict(),
        )


if __name__ == "__main__":
    unittest.main()
