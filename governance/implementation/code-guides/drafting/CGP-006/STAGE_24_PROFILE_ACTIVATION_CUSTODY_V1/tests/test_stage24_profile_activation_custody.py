from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
PKG = ROOT / "governance/implementation/code-guides/drafting/CGP-006/STAGE_24_PROFILE_ACTIVATION_CUSTODY_V1"
VALIDATOR_PATH = PKG / "validators/validate_stage24_profile_activation_custody.py"
spec = importlib.util.spec_from_file_location("custody_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)

class Stage24CustodyValidatorTests(unittest.TestCase):
    def test_positive_custody_package_validates(self):
        self.assertEqual(validator.validate(ROOT, enforce_git_paths=False)["status"], "PASS")

    def test_authorized_paths_include_only_governance_custody(self):
        result = validator.validate(ROOT, enforce_git_paths=True)
        self.assertEqual(result["active_guides"], 4)

    def test_product_path_rejected(self):
        with self.assertRaises(validator.ValidationError):
            validator.check_authorized_paths(["frontend/src/App.jsx"])

if __name__ == "__main__":
    unittest.main()
