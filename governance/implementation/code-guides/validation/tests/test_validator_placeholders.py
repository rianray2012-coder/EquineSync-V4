#!/usr/bin/env python3
"""Tests proving CGP-001 validators do not falsely pass."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


VALIDATORS = [
        'validate_code_guide_structure.py',
        'validate_control_registry.py',
        'validate_invariant_registry.py',
        'validate_guide_questions.py',
        'validate_guide_dependencies.py',
        'validate_atlas_traceability.py',
        'validate_repository_mapping.py',
        'validate_control_verification.py',
        'validate_implementation_profiles.py',
        'validate_evidence_records.py',
        'validate_exceptions.py',
        'validate_supersession.py',
        'validate_package_integrity.py',
        'validate_portfolio_consistency.py',
]


class ValidatorPlaceholderTests(unittest.TestCase):
    def test_validators_require_cgp002_and_do_not_pass(self):
        validation_dir = Path(__file__).resolve().parents[1]
        for validator_name in VALIDATORS:
            validator_path = validation_dir / validator_name
            with self.subTest(validator=validator_name):
                result = subprocess.run(
                    [sys.executable, str(validator_path), "--substantive"],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                combined_output = result.stdout + result.stderr
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("NOT_IMPLEMENTED_CGP_002_REQUIRED", combined_output)
                self.assertNotIn("PASS", combined_output.upper())


if __name__ == "__main__":
    unittest.main()
