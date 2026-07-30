from __future__ import annotations

import importlib.util
import pathlib


def load_validator():
    package_root = pathlib.Path(__file__).resolve().parents[1]
    validator_path = package_root / 'validators' / 'validate_repository_hygiene_ci_assurance_review.py'
    spec = importlib.util.spec_from_file_location('validate_repository_hygiene_ci_assurance_review', validator_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_repository_hygiene_ci_assurance_review_package_validates():
    result = load_validator().validate()
    assert result['status'] == 'PASS'
    assert result['copilot_leads'] == 10
    assert result['authorized_iwps'] == 0
