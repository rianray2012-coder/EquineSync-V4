#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
VALIDATOR = BASE / "validators" / "validate_document_07.py"

def test_validator_passes():
    result = subprocess.run([sys.executable, str(VALIDATOR)], cwd=BASE, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DOCUMENT_07_VALIDATION_PASS" in result.stdout

if __name__ == "__main__":
    test_validator_passes()
    print("DOCUMENT_07_VALIDATOR_TESTS_PASS")
