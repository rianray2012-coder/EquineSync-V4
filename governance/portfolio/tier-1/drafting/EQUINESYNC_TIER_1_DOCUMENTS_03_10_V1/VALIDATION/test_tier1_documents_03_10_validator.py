#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
VALIDATOR = BASE / "validate_tier1_documents_03_10.py"

def test_root_validator_passes():
    result = subprocess.run([sys.executable, str(VALIDATOR)], cwd=BASE.parents[5], text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DOCUMENTARY_VALIDATION_PASS" in result.stdout

if __name__ == "__main__":
    test_root_validator_passes()
    print("TIER1_VALIDATOR_TESTS_PASS")
