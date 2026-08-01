from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def load_validator():
    validator = Path(__file__).resolve().parents[1] / "validators" / "validate_cgp006_gap0005_post_correction_custody_refresh.py"
    spec = importlib.util.spec_from_file_location("validate_cgp006_gap0005_post_correction_custody_refresh", validator)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_post_correction_custody_refresh_package_passes():
    module = load_validator()
    result = module.validate()
    assert result["status"] == "PASS"
    assert result["approved_zip_git_sha256"] == module.EXPECTED_ZIP_SHA
    assert result["approved_zip_git_bytes"] == module.EXPECTED_ZIP_BYTES
    assert result["bugbot_findings"] == 3


def test_refresh_validator_rejects_missing_zip_git_object(monkeypatch):
    module = load_validator()

    def missing_zip(_root, rel):
        if rel == module.ZIP_PATH:
            raise AssertionError("missing ZIP Git object")
        return b""

    monkeypatch.setattr(module, "git_object_bytes", missing_zip)
    with pytest.raises(AssertionError, match="missing ZIP Git object"):
        module.validate()


def test_refresh_validator_rejects_boundary_self_satisfaction(monkeypatch):
    module = load_validator()
    monkeypatch.setattr(module, "load_authoritative_text", lambda _root, _package: "")
    with pytest.raises(AssertionError, match="boundary token missing"):
        module.validate()


def test_refresh_validator_rejects_secret_like_text(monkeypatch):
    module = load_validator()
    original = Path.read_text

    def injected_secret(path, *args, **kwargs):
        text = original(path, *args, **kwargs)
        if path.name == "README.md" and "POST_CORRECTION_CUSTODY_REFRESH_V2" in str(path):
            return text + "\n" + "STRIPE_" + "API_KEY=" + "sk" + "_test_do_not_commit\n"
        return text

    monkeypatch.setattr(Path, "read_text", injected_secret)
    with pytest.raises(AssertionError, match="secret-like value"):
        module.validate()


def test_refresh_validator_rejects_unresolved_bugbot_row(monkeypatch):
    module = load_validator()
    original = module.read_csv_dicts

    def unresolved(path):
        rows = original(path)
        if path.name == "BUGBOT_FINDING_FINAL_DISPOSITION_MATRIX.csv":
            rows[0]["result"] = "FAIL"
        return rows

    monkeypatch.setattr(module, "read_csv_dicts", unresolved)
    with pytest.raises(AssertionError, match="Bugbot finding matrix contains unresolved row"):
        module.validate()


def test_refresh_validator_rejects_unauthorized_changed_path(monkeypatch):
    module = load_validator()
    original = module.run_git

    def changed_path(root, *args, check=True):
        if args[:2] == ("diff", "--name-only"):
            return "frontend/package.json"
        return original(root, *args, check=check)

    monkeypatch.setattr(module, "run_git", changed_path)
    with pytest.raises(AssertionError, match="unauthorized changed paths"):
        module.validate()
