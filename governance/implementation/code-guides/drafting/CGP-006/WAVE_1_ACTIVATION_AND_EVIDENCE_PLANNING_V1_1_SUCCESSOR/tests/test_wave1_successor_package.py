#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
PATH = ROOT / "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING_V1_1_SUCCESSOR" / "validators/validate_wave1_successor_package.py"
spec = importlib.util.spec_from_file_location("successor_validator", PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)

class SuccessorPackageTests(unittest.TestCase):
    def test_package_validates(self):
        validator.validate()

if __name__ == "__main__":
    unittest.main()
