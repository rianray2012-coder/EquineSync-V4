"""Build-Next-6C local document template/request foundation contract tests.

BN6C may create local template/request records, but it must still not create
live provider envelopes, signing URLs, provider callback receivers,
signed-document storage, legal text, or participation gates.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from core.document_workflows import (
    SIGNER_FACILITY_COUNTERSIGNER,
    SIGNER_GUARDIAN,
    SIGNER_SUBJECT,
    audit_safe_document_metadata,
    build_template_contract,
    document_type_contract,
    project_document_record,
    signer_requirements_for_subject,
)


ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


ROUTE_SRC = _read("backend/routes/document_signatures.py")
FRONTEND_SRC = _read("frontend/src/pages/FormsSignatures.jsx")


def _route_body(function_name: str) -> str:
    marker = f"async def {function_name}"
    start = ROUTE_SRC.find(marker)
    assert start >= 0, f"Missing route function {function_name}"
    body_start = ROUTE_SRC.find(":\n", start)
    assert body_start >= 0, f"Missing route body for {function_name}"
    body_start += 2
    candidates = [
        idx for idx in (
            ROUTE_SRC.find("\n    @router.", body_start),
            ROUTE_SRC.find("\n    return router", body_start),
        )
        if idx >= 0
    ]
    assert candidates, f"Missing route boundary after {function_name}"
    return ROUTE_SRC[body_start:min(candidates)]


def test_bn6c_route_surface_adds_local_template_and_request_foundation():
    assert '"/document-signatures/document-types"' in ROUTE_SRC
    assert '"/document-signatures/templates"' in ROUTE_SRC
    assert '"/document-signatures/requests"' in ROUTE_SRC
    assert '"/document-signatures/requests/{request_id}"' in ROUTE_SRC
    assert "DOCUMENT_TEMPLATES_COLLECTION" in ROUTE_SRC
    assert "DOCUMENT_REQUESTS_COLLECTION" in ROUTE_SRC
    assert "document_template.created" in ROUTE_SRC
    assert "document_request.created" in ROUTE_SRC


def test_bn6c_template_and_request_reads_are_manager_only():
    """Request rows include subject refs, so owner-facing reads remain deferred."""
    for function_name in (
        "list_document_templates",
        "list_document_requests",
        "get_document_request",
    ):
        body = _route_body(function_name)
        assert "_require_document_manager(user)" in body
        assert "require_permission(user, DOCUMENT_READ_CAPABILITY)" not in body

    type_body = _route_body("document_signature_document_types")
    assert "require_permission(user, DOCUMENT_READ_CAPABILITY)" in type_body


def test_bn6c_templates_are_limited_to_reviewed_document_types():
    template = build_template_contract(
        "lesson_program_agreement",
        template_id="tmpl_1",
        barn_id="barn_a",
        provider_template_id="provider_template_ref",
        version=2,
        status="active",
    )

    assert template["document_type"] == "lesson_program_agreement"
    assert template["provider"] == "docusign"
    assert template["launch_behavior"] == "soft_warning"
    assert template["provider_template_id"] == "provider_template_ref"
    with pytest.raises(ValueError):
        document_type_contract("custom_unreviewed_waiver")


def test_bn6c_request_signer_rules_cover_teen_and_under_13_subjects():
    teen = signer_requirements_for_subject(
        "lesson_program_agreement",
        minor_status="minor_13_to_17",
    )
    under_13 = signer_requirements_for_subject(
        "lesson_program_agreement",
        minor_status="under_13",
    )

    assert teen["signer_roles"] == [
        SIGNER_GUARDIAN,
        SIGNER_SUBJECT,
        SIGNER_FACILITY_COUNTERSIGNER,
    ]
    assert under_13["signer_roles"] == [SIGNER_GUARDIAN, SIGNER_FACILITY_COUNTERSIGNER]
    assert under_13["under_13_policy"] == "parent_managed_only"


def test_bn6c_response_projection_and_audit_metadata_stay_private():
    record = {
        "id": "doc_req_1",
        "status": "draft",
        "provider_envelope_id": "env_secret",
        "provider_signature_id": "sig_secret",
        "provider_certificate_ref": "cert_secret",
        "legal_text": "full legal body",
        "signed_document_url": "https://example.invalid/signed.pdf",
        "raw_provider_payload": {"secret": "payload"},
        "guardian_consent_text": "private consent",
        "birthdate": "2014-01-01",
        "private_notes": "private note",
        "required_signer_user_ids": ["student_user_1", "guardian_1"],
        "signed_user_ids": ["guardian_1"],
    }

    projected = project_document_record(record)
    metadata = audit_safe_document_metadata(record)
    blob = f"{projected} {metadata}".lower()

    assert projected["id"] == "doc_req_1"
    assert "provider_envelope_id" not in projected
    assert metadata["required_signer_count"] == 2
    assert metadata["signed_count"] == 1
    for forbidden in (
        "env_secret",
        "sig_secret",
        "cert_secret",
        "full legal",
        "signed.pdf",
        "private consent",
        "2014",
        "private note",
        "student_user_1",
        "guardian_1",
    ):
        assert forbidden not in blob


def test_bn6c_frontend_exposes_local_foundation_without_live_send_action():
    assert 'api.get("/document-signatures/document-types")' in FRONTEND_SRC
    assert 'api.get("/document-signatures/templates")' in FRONTEND_SRC
    assert 'api.get("/document-signatures/requests")' in FRONTEND_SRC
    assert 'endpoint="/document-signatures/templates"' in FRONTEND_SRC
    assert 'endpoint="/document-signatures/requests"' in FRONTEND_SRC
    assert "No signing link is generated" in FRONTEND_SRC
    assert "send-envelope" not in FRONTEND_SRC


def test_bn6c_source_has_no_live_signing_or_provider_receiver_implementation():
    requirements = _read("backend/requirements.txt").lower()

    assert "docusign-esign" not in requirements
    for forbidden in (
        "create_envelope",
        "send_envelope",
        "recipient_view",
        "signing_url",
        '@router.post("/document-signatures/webhook',
        '@router.post("/document-signatures/provider',
        "hard_block",
    ):
        assert forbidden not in ROUTE_SRC.lower()
    assert "creates_live_envelope" in _read("backend/core/document_workflows.py")
