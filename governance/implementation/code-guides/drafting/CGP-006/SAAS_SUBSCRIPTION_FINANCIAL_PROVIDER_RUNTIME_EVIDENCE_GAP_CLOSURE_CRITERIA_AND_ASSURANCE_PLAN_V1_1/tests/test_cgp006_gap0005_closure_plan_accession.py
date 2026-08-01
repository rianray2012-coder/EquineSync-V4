from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def load_validator():
    validator = Path(__file__).resolve().parents[1] / "validators" / "validate_cgp006_gap0005_closure_plan_accession.py"
    spec = importlib.util.spec_from_file_location("cgp006_gap0005_accession_validator", validator)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_cgp006_gap0005_closure_plan_accession_package():
    module = load_validator()
    result = module.validate()
    assert result["status"] == "PASS"
    assert result["approved_zip_git_sha256"] == module.EXPECTED_ZIP_SHA
    assert result["approved_zip_git_bytes"] == module.EXPECTED_ZIP_BYTES


def test_boundary_token_must_be_in_authoritative_file(monkeypatch):
    module = load_validator()
    package = module.repo_root() / module.PACKAGE_REL
    token = "PROVIDER_CONNECTED_ASSURANCE_WORKSTREAM_NOT_AUTHORIZED_BY_THIS_DIRECTIVE"
    original = module.authoritative_text

    def redacted_authoritative_text(pkg, rel):
        text = original(pkg, rel)
        if rel == "CURRENT_GAP_STATUS_OVERLAY.md":
            return text.replace(token, "TOKEN_REMOVED_FROM_AUTHORITATIVE_FILE")
        return text

    monkeypatch.setattr(module, "authoritative_text", redacted_authoritative_text)
    with pytest.raises(AssertionError, match="authoritative governance files"):
        module.validate_boundary_tokens(package)


def test_manifest_cannot_satisfy_boundary_token(monkeypatch):
    module = load_validator()
    package = module.repo_root() / module.PACKAGE_REL
    monkeypatch.setattr(module, "AUTHORITATIVE_TOKEN_LOCATIONS", {module.FOUNDER_APPROVAL_ID: {"PACKAGE_MANIFEST.json"}})
    with pytest.raises(AssertionError, match="manifest/checksum cannot satisfy"):
        module.validate_boundary_tokens(package)


def test_validator_source_cannot_satisfy_boundary_token(monkeypatch):
    module = load_validator()
    package = module.repo_root() / module.PACKAGE_REL
    monkeypatch.setattr(
        module,
        "AUTHORITATIVE_TOKEN_LOCATIONS",
        {module.FOUNDER_APPROVAL_ID: {"validators/validate_cgp006_gap0005_closure_plan_accession.py"}},
    )
    with pytest.raises(AssertionError, match="non-authoritative token source"):
        module.validate_boundary_tokens(package)


def test_git_zip_object_is_required(monkeypatch):
    module = load_validator()
    root = module.repo_root()
    package = root / module.PACKAGE_REL
    zip_rel = (module.PACKAGE_REL / "APPROVED_SOURCE" / module.ZIP_NAME).as_posix()

    def missing_git_object(_root, rel):
        if rel == zip_rel:
            raise AssertionError("missing committed ZIP")
        return module.git_object_bytes(_root, rel)

    monkeypatch.setattr(module, "git_object_bytes", missing_git_object)
    with pytest.raises(AssertionError, match="missing committed ZIP"):
        module.validate_git_zip_and_approved_sources(root, package)


def test_wrong_git_zip_bytes_are_rejected(monkeypatch):
    module = load_validator()
    root = module.repo_root()
    package = root / module.PACKAGE_REL
    zip_rel = (module.PACKAGE_REL / "APPROVED_SOURCE" / module.ZIP_NAME).as_posix()
    original = module.git_object_bytes

    def wrong_git_object(_root, rel):
        if rel == zip_rel:
            return b"not the approved zip"
        return original(_root, rel)

    monkeypatch.setattr(module, "git_object_bytes", wrong_git_object)
    with pytest.raises(AssertionError, match="ZIP Git object identity mismatch"):
        module.validate_git_zip_and_approved_sources(root, package)


def test_prohibited_future_evidence_placeholder_is_rejected():
    module = load_validator()
    package = module.repo_root() / module.PACKAGE_REL
    found = set(module.REQUIRED_FILES)
    found.add("CURRENT_EVIDENCE_POSTURE.csv")
    with pytest.raises(AssertionError, match="future evidence placeholders"):
        module.validate_file_hygiene(package, found)


def test_unexpected_approved_source_file_is_rejected():
    module = load_validator()
    package = module.repo_root() / module.PACKAGE_REL
    found = set(module.REQUIRED_FILES)
    found.add("APPROVED_SOURCE/unapproved-local-copy.zip")
    with pytest.raises(AssertionError, match="unexpected approved-source"):
        module.validate_file_hygiene(package, found)


def test_authorized_paths_reject_product_code(monkeypatch):
    module = load_validator()

    def fake_run_git(_root, *args, check=True):
        if args[:2] == ("diff", "--name-only"):
            return "backend/routes/billing.py"
        return ""

    monkeypatch.setattr(module, "run_git", fake_run_git)
    with pytest.raises(AssertionError, match="unauthorized changed paths"):
        module.validate_authorized_paths(module.repo_root())
