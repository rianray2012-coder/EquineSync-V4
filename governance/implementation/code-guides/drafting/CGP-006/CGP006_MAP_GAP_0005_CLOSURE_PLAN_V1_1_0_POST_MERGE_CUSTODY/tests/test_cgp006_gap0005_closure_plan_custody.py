#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def load_validator():
    validator_path = Path(__file__).resolve().parents[1] / "validators" / "validate_cgp006_gap0005_closure_plan_custody.py"
    spec = importlib.util.spec_from_file_location("validate_cgp006_gap0005_closure_plan_custody", validator_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_cgp006_gap0005_closure_plan_custody_validator_passes() -> None:
    module = load_validator()
    result = module.validate()
    assert result["status"] == "PASS"
    assert result["accession_dependency_status"] == "PASS"
    assert result["accession_merge_commit"] == "95a4c9b4006f4bd4377f75b3d0fef57d5f424dee"
    assert result["approved_zip_git_sha256"] == module.EXPECTED_ZIP_SHA
    assert result["approved_zip_git_bytes"] == module.EXPECTED_ZIP_BYTES
    assert result["gap_status"] == "CGP006_MAP_GAP_0005_REMAINS_OPEN"
    assert result["source_identity_rows"] == 8


def test_custody_validator_requires_successful_accession_validation(monkeypatch) -> None:
    module = load_validator()

    def failing_accession(_root):
        raise AssertionError("accession gate failed")

    monkeypatch.setattr(module, "run_accession_validation", failing_accession)
    with pytest.raises(AssertionError, match="accession gate failed"):
        module.validate()


def test_custody_boundary_token_cannot_be_validator_only(monkeypatch) -> None:
    module = load_validator()
    monkeypatch.setattr(
        module,
        "AUTHORITATIVE_TOKEN_LOCATIONS",
        {module.FOUNDER_APPROVAL_ID: {module.CUSTODY_PATH / "validators" / "validate_cgp006_gap0005_closure_plan_custody.py"}},
    )
    with pytest.raises(AssertionError, match="non-authoritative token source"):
        module.validate_boundary_tokens(module.repo_root())


def test_custody_boundary_token_must_remain_in_authoritative_file(monkeypatch) -> None:
    module = load_validator()
    token = "NO_LIVE_STRIPE_OBJECT_OR_SECRET_USED"
    original_read_text = Path.read_text

    def redacted_read_text(path, *args, **kwargs):
        text = original_read_text(path, *args, **kwargs)
        if path.name in {"README.md", "DIRECTIVE_EXECUTION_RECORD.md", "VALIDATION_REPORT.md"} or path.name.endswith("CUSTODY_RECEIPT.md"):
            return text.replace(token, "TOKEN_REMOVED_FROM_AUTHORITATIVE_FILE")
        return text

    monkeypatch.setattr(Path, "read_text", redacted_read_text)
    with pytest.raises(AssertionError, match="authoritative governance files"):
        module.validate_boundary_tokens(module.repo_root())


def test_custody_rejects_accession_placeholder(monkeypatch) -> None:
    module = load_validator()
    original = module.git_tracked_files

    def files_with_placeholder(root, package):
        files = set(original(root, package))
        if package == module.ACCESSION_PATH:
            files.add("CURRENT_EVIDENCE_POSTURE.csv")
        return files

    monkeypatch.setattr(module, "git_tracked_files", files_with_placeholder)
    with pytest.raises(AssertionError, match="prohibited future-evidence placeholders"):
        module.validate_accession_placeholder_prohibitions(module.repo_root())


def test_custody_rejects_wrong_git_zip_bytes(monkeypatch) -> None:
    module = load_validator()
    zip_rel = (module.ACCESSION_PATH / "APPROVED_SOURCE" / module.ZIP_NAME).as_posix()
    original = module.git_object_bytes

    def wrong_git_object(root, rel):
        if rel == zip_rel:
            return b"not the approved zip"
        return original(root, rel)

    monkeypatch.setattr(module, "git_object_bytes", wrong_git_object)
    with pytest.raises(AssertionError, match="ZIP Git object identity mismatch"):
        module.validate_git_zip_object(module.repo_root())


def test_custody_rejects_provider_assurance_completion_claim(monkeypatch) -> None:
    module = load_validator()
    original_read_text = Path.read_text

    def injected_claim(path, *args, **kwargs):
        text = original_read_text(path, *args, **kwargs)
        if path.name == "PROGRAM_STATUS.md":
            return text + "\nCGP006_MAP_GAP_0005_PROVIDER_ASSURANCE_COMPLETE\n"
        return text

    monkeypatch.setattr(Path, "read_text", injected_claim)
    with pytest.raises(AssertionError, match="unauthorized provider or production readiness claim"):
        module.validate_status_and_claims(module.repo_root())


def test_custody_authorized_paths_reject_product_code(monkeypatch) -> None:
    module = load_validator()

    def fake_run_git(_root, *args, check=True):
        if args[:2] == ("diff", "--name-only"):
            return "backend/routes/billing.py"
        return ""

    monkeypatch.setattr(module, "run_git", fake_run_git)
    with pytest.raises(AssertionError, match="unauthorized changed paths"):
        module.validate_authorized_paths(module.repo_root())


if __name__ == "__main__":
    test_cgp006_gap0005_closure_plan_custody_validator_passes()
    print("PASS test_cgp006_gap0005_closure_plan_custody_validator_passes")
