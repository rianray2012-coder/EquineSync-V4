
#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib


def test_pr62_documentary_baseline_custody_validator_passes() -> None:
    validator_path = pathlib.Path(__file__).resolve().parents[1] / 'validators' / 'validate_pr62_documentary_baseline_custody.py'
    spec = importlib.util.spec_from_file_location('validate_pr62_documentary_baseline_custody', validator_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    result = module.validate()
    assert result['status'] == 'PASS'
    assert result['gap_rows'] == 18
    assert result['finding_rows'] == 16
    assert result['candidate_iwp_rows'] == 15
    assert result['authorized_iwps'] == 0


if __name__ == '__main__':
    test_pr62_documentary_baseline_custody_validator_passes()
    print('PASS test_pr62_documentary_baseline_custody_validator_passes')
