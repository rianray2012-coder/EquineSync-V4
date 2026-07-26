#!/usr/bin/env python3
"""Implementation smoke tests for CGP-002 validators."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


VALIDATION_DIR = Path(__file__).resolve().parents[1]
VALIDATOR_FILES = [
    "validate_code_guide_structure.py",
    "validate_control_registry.py",
    "validate_invariant_registry.py",
    "validate_guide_questions.py",
    "validate_guide_dependencies.py",
    "validate_atlas_traceability.py",
    "validate_repository_mapping.py",
    "validate_control_verification.py",
    "validate_implementation_profiles.py",
    "validate_evidence_records.py",
    "validate_exceptions.py",
    "validate_supersession.py",
    "validate_package_integrity.py",
    "validate_portfolio_consistency.py",
    "validate_source_accession.py",
    "validate_repository_component_register.py",
    "validate_repository_authority_alignment.py",
    "validate_current_state_assessment.py",
    "validate_source_freeze.py",
    "validate_wave_1_drafting_readiness.py",
]


class ValidatorImplementationTests(unittest.TestCase):
    def test_validators_emit_json_and_are_not_placeholders(self):
        for validator in VALIDATOR_FILES:
            with self.subTest(validator=validator):
                proc = subprocess.run(
                    [sys.executable, str(VALIDATION_DIR / validator), "--json"],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                combined = proc.stdout + proc.stderr
                self.assertNotIn("NOT_IMPLEMENTED_CGP_002_REQUIRED", combined)
                self.assertEqual(proc.returncode, 0, combined)
                payload = json.loads(proc.stdout)
                self.assertIn(payload["status"], {"PASS", "WARNING", "NOT_YET_APPLICABLE"})
                self.assertEqual(payload["validator"], validator.removeprefix("validate_").removesuffix(".py").replace("_", "-"))


if __name__ == "__main__":
    unittest.main()
