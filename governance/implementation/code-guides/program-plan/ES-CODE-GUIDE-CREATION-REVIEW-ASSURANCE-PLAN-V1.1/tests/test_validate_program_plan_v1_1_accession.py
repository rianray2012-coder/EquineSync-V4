from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = PACKAGE_ROOT / "validation" / "validate_program_plan_v1_1_accession.py"


spec = importlib.util.spec_from_file_location("validate_program_plan_v1_1_accession", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class ProgramPlanV11AccessionTests(unittest.TestCase):
    def test_required_files_exist(self):
        validator.validate_required_files()

    def test_exact_source_identity(self):
        validator.validate_source_identity()

    def test_manifest_and_checksums(self):
        validator.validate_json_manifests()
        validator.validate_checksum_manifest()

    def test_authority_boundary_tokens(self):
        validator.validate_required_tokens()

    def test_guide_state_preservation(self):
        validator.validate_program_state_preservation()


if __name__ == "__main__":
    unittest.main()
