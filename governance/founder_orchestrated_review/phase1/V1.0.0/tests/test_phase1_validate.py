import importlib.util
import json
import unittest
from pathlib import Path, PurePosixPath


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase1_validate.py"
SPEC = importlib.util.spec_from_file_location("phase1_validate", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class Phase1ValidatorTests(unittest.TestCase):
    def test_canonical_hash_ignores_mapping_order(self):
        self.assertEqual(MODULE.canonical_sha256({"a": 1, "b": 2}), MODULE.canonical_sha256({"b": 2, "a": 1}))

    def test_schema_subset_accepts_valid_profile(self):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "schemas" / "phase1_review_execution_profile.schema.json").read_text())
        profile = json.loads((root / "profiles" / "ES-RA-02_REVIEW_EXECUTION_PROFILE_V1.0.0.json").read_text())
        self.assertEqual([], MODULE.validate_schema(profile, schema))

    def test_schema_subset_rejects_missing_required_fields(self):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "schemas" / "phase1_role_output.schema.json").read_text())
        invalid = json.loads((root / "pilot_a" / "fixtures" / "output_schema" / "invalid_output.json").read_text())
        self.assertTrue(MODULE.validate_schema(invalid, schema))

    def test_path_traversal_detection_primitive(self):
        self.assertIn("..", PurePosixPath("../escape.txt").parts)
        self.assertNotIn("..", PurePosixPath("safe/file.txt").parts)


if __name__ == "__main__":
    unittest.main()
