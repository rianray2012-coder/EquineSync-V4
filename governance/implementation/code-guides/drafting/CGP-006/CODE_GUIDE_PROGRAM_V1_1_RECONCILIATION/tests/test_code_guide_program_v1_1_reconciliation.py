#!/usr/bin/env python3
"""Tests for the Code Guide Program V1.1 reconciliation package."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[7]
VALIDATOR_PATH = (
    ROOT
    / "governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION"
    / "validators"
    / "validate_code_guide_program_v1_1_reconciliation.py"
)
spec = importlib.util.spec_from_file_location("v1_1_reconciliation_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class ReconciliationPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = validator.repo_root()

    def test_required_files_exist(self) -> None:
        validator.assert_required_files(self.root)

    def test_required_closing_statements_are_present(self) -> None:
        validator.assert_closing_statements(self.root)

    def test_approved_source_integrity(self) -> None:
        validator.assert_source_integrity(self.root)

    def test_manifest_and_checksums(self) -> None:
        validator.assert_manifest_and_checksums(self.root)

    def test_tracker_boundary(self) -> None:
        validator.assert_tracker_boundary(self.root)

    def test_reconciliation_determinations(self) -> None:
        validator.assert_reconciliation_determinations(self.root)


if __name__ == "__main__":
    unittest.main()
