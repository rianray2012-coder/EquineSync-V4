#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
PATH = ROOT / "governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_REVISION_AND_PR_44_SUCCESSOR_PREPARATION" / "validators/validate_revision_package.py"
spec = importlib.util.spec_from_file_location("primary_validator", PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)

class PrimaryPackageTests(unittest.TestCase):
    def test_package_validates(self):
        validator.validate()

if __name__ == "__main__":
    unittest.main()
