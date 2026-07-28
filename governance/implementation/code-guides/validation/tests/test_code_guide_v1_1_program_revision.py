#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
VALIDATOR = ROOT / "governance/implementation/code-guides" / "validation/validate_code_guide_v1_1_program_revision.py"
FIXTURES = ROOT / "governance/implementation/code-guides" / "validation/tests/fixtures/v1_1_program_revision"
spec = importlib.util.spec_from_file_location("v11_validator", VALIDATOR)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)

class V11ProgramRevisionValidatorTests(unittest.TestCase):
    def test_positive_fixture_profile(self):
        validator.assert_profile_generic(validator.load_profile(FIXTURES / "positive_profile.yaml"))

    def test_negative_fixture_profile_rejects_repository_specific_reference(self):
        with self.assertRaises(AssertionError):
            validator.assert_profile_generic(validator.load_profile(FIXTURES / "negative_profile_repository_specific.yaml"))

    def test_malformed_fixture_rejected(self):
        with self.assertRaises(json.JSONDecodeError):
            validator.load_profile(FIXTURES / "malformed_profile.yaml")

    def test_boundary_controlled_values(self):
        obj = json.loads((FIXTURES / "boundary_controlled_values.json").read_text())
        validator.validate_controlled_values_obj(obj)

    def test_full_workstream_validates(self):
        validator.validate_all()

if __name__ == "__main__":
    unittest.main()
