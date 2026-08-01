"""Pytest wrapper for the Guardian/Minor implementation package validator."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_guardian_minor_implementation_package_validator_passes():
    root = Path(__file__).resolve().parent
    validator = root / "validate_guardian_minor_implementation_package.py"
    result = subprocess.run(
        [sys.executable, str(validator)],
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
