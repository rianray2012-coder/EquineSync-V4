#!/usr/bin/env python3
import subprocess
from pathlib import Path

def test_document_06_validator_runs():
    validator = Path(__file__).resolve().parents[1] / 'validators' / 'validate_document_06_rr2.py'
    result = subprocess.run(['python3', str(validator)], text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
