from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def load_validator():
    validator = Path(__file__).resolve().parents[1] / 'validators' / 'validate_cgp006_gap0005_custody_integrity_correction.py'
    spec = importlib.util.spec_from_file_location('validate_cgp006_gap0005_custody_integrity_correction', validator)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_custody_integrity_correction_package_passes():
    module = load_validator()
    result = module.validate()
    assert result['status'] == 'PASS'
    assert result['approved_zip_git_sha256'] == module.EXPECTED_ZIP_SHA
    assert result['approved_zip_git_bytes'] == module.EXPECTED_ZIP_BYTES


def test_correction_validator_rejects_missing_zip_git_object(monkeypatch):
    module = load_validator()

    def missing_zip(_root, rel):
        if rel == module.ZIP_PATH:
            raise AssertionError('missing ZIP Git object')
        return b''

    monkeypatch.setattr(module, 'git_object_bytes', missing_zip)
    with pytest.raises(AssertionError, match='missing ZIP Git object'):
        module.validate()


def test_correction_validator_rejects_secret_like_text(monkeypatch):
    module = load_validator()
    original = Path.read_text

    def injected_secret(path, *args, **kwargs):
        text = original(path, *args, **kwargs)
        if path.name == 'README.md' and 'CGP006_MAP_GAP_0005_CLOSURE_PLAN_CUSTODY_INTEGRITY_CORRECTION_V1' in str(path):
            return text + '\n' + 'STRIPE_' + 'API_KEY=' + 'sk' + '_test_do_not_commit\n'
        return text

    monkeypatch.setattr(Path, 'read_text', injected_secret)
    with pytest.raises(AssertionError, match='secret-like value'):
        module.validate()
