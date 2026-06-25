"""Build-Next-6B document workflow provider contract tests.

BN6B defines launch workflow contracts only. It must not create live signing
envelopes, provider webhooks, signed-document storage, legal text, or
participation gates.
"""
from __future__ import annotations

from pathlib import Path

from core.document_signing import PROVIDER_DOCUSIGN
from core.document_workflows import (
    ACKNOWLEDGEMENT_DOCUMENT_TYPES,
    DOCUMENT_TYPE_MATRIX,
    LEGAL_DOCUMENT_TYPES,
    PROVIDER_NONE,
    SIGNER_FACILITY_COUNTERSIGNER,
    SIGNER_GUARDIAN,
    SIGNER_SUBJECT,
    WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT,
    WORKFLOW_PROVIDER_SIGNATURE,
    audit_safe_document_metadata,
    build_template_contract,
    document_matrix,
    document_type_contract,
    project_document_record,
    provider_envelope_contract_preview,
    provider_status_to_local_status,
    signer_requirements_for_subject,
)


ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_document_matrix_classifies_every_launch_document():
    matrix = document_matrix()

    assert set(LEGAL_DOCUMENT_TYPES).issubset(matrix)
    assert set(ACKNOWLEDGEMENT_DOCUMENT_TYPES).issubset(matrix)
    assert len(matrix) == 10
    for doc_type, contract in matrix.items():
        assert contract["workflow_kind"] in {
            WORKFLOW_PROVIDER_SIGNATURE,
            WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT,
        }
        if doc_type in LEGAL_DOCUMENT_TYPES:
            assert contract["provider"] == PROVIDER_DOCUSIGN
            assert contract["exportable_evidence"] is True
        if doc_type in ACKNOWLEDGEMENT_DOCUMENT_TYPES:
            assert contract["provider"] == PROVIDER_NONE
        # BN6B keeps all participation effects soft until legal approval.
        assert contract["launch_behavior"] == "soft_warning"


def test_template_contract_matches_future_schema_without_writing_records():
    template = build_template_contract(
        "lesson_program_agreement",
        template_id="tmpl_lesson",
        barn_id="barn_1",
        provider_template_id="provider_template_ref",
        version=3,
    )

    expected = {
        "id",
        "barn_id",
        "platform_template",
        "document_type",
        "display_name",
        "workflow_kind",
        "provider",
        "provider_template_id",
        "version",
        "status",
        "required_for_customer_types",
        "required_for_roles",
        "required_for_workflows",
        "requires_guardian_signature",
        "requires_facility_countersignature",
        "requires_platform_countersignature",
        "expires_after_days",
        "launch_behavior",
        "exportable_evidence",
    }
    assert set(template) == expected
    assert template["barn_id"] == "barn_1"
    assert template["platform_template"] is False
    assert template["provider"] == PROVIDER_DOCUSIGN
    assert template["requires_facility_countersignature"] is True


def test_unknown_document_type_fails_closed():
    try:
        document_type_contract("unreviewed_custom_waiver")
    except ValueError as exc:
        assert "Unknown document type" in str(exc)
    else:
        raise AssertionError("unknown document type should fail closed")


def test_signer_requirements_respect_minor_and_guardian_rules():
    adult = signer_requirements_for_subject(
        "lesson_program_agreement",
        minor_status="adult",
    )
    teen = signer_requirements_for_subject(
        "lesson_program_agreement",
        minor_status="minor_13_to_17",
    )
    under_13 = signer_requirements_for_subject(
        "lesson_program_agreement",
        minor_status="under_13",
    )

    assert adult["signer_roles"] == [SIGNER_SUBJECT, SIGNER_FACILITY_COUNTERSIGNER]
    assert SIGNER_GUARDIAN in teen["signer_roles"]
    assert SIGNER_SUBJECT in teen["signer_roles"]
    assert SIGNER_FACILITY_COUNTERSIGNER in teen["signer_roles"]
    assert SIGNER_GUARDIAN in under_13["signer_roles"]
    assert SIGNER_SUBJECT not in under_13["signer_roles"]
    assert under_13["under_13_policy"] == "parent_managed_only"


def test_provider_status_mapping_has_safe_attention_fallback():
    assert provider_status_to_local_status("completed") == "completed"
    assert provider_status_to_local_status("delivered") == "viewed"
    assert provider_status_to_local_status("voided") == "voided"
    assert provider_status_to_local_status("unknown-provider-status") == "provider_attention"


def test_provider_envelope_preview_is_not_a_live_api_payload():
    template = build_template_contract(
        "general_liability_waiver",
        template_id="tmpl_waiver",
        barn_id="barn_1",
        provider_template_id="provider_template_ref",
    )
    request = {
        "id": "doc_req_1",
        "barn_id": "barn_1",
        "provider_envelope_id": "envelope_should_not_drive_api",
    }
    preview = provider_envelope_contract_preview(
        request=request,
        template=template,
        signer_roles=[SIGNER_GUARDIAN, SIGNER_SUBJECT],
    )

    assert preview["provider"] == PROVIDER_DOCUSIGN
    assert preview["request_id"] == "doc_req_1"
    assert preview["recipient_roles"] == [SIGNER_GUARDIAN, SIGNER_SUBJECT]
    assert preview["creates_live_envelope"] is False
    assert "provider_envelope_id" not in preview


def test_document_projection_strips_provider_refs_and_sensitive_payloads_by_default():
    projected = project_document_record({
        "_id": "mongo",
        "id": "doc_req_1",
        "status": "sent",
        "provider_envelope_id": "env_secret",
        "provider_signature_id": "sig_secret",
        "provider_certificate_ref": "cert_secret",
        "legal_text": "full legal language",
        "signed_document_body": "pdf bytes",
        "raw_provider_payload": {"anything": "provider-private"},
        "provider_access_token": "token",
        "webhook_secret": "secret",
        "guardian_consent_text": "private consent",
        "birthdate": "2014-01-01",
        "staff_notes": "private staff note",
    })

    blob = str(projected).lower()
    assert projected == {"id": "doc_req_1", "status": "sent"}
    for forbidden in (
        "env_secret",
        "sig_secret",
        "cert_secret",
        "full legal",
        "provider-private",
        "token",
        "private consent",
        "2014",
        "private staff",
    ):
        assert forbidden not in blob


def test_audit_metadata_keeps_counts_and_status_not_raw_values():
    metadata = audit_safe_document_metadata({
        "document_type": "minor_participant_liability_waiver",
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        "provider": PROVIDER_DOCUSIGN,
        "status": "sent",
        "required_signer_user_ids": ["guardian_1", "facility_1"],
        "signed_user_ids": ["guardian_1"],
        "legal_text": "full legal language",
        "provider_envelope_id": "env_secret",
        "birthdate": "2014-01-01",
    })

    assert metadata == {
        "document_type": "minor_participant_liability_waiver",
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
        "provider": PROVIDER_DOCUSIGN,
        "status": "sent",
        "required_signer_count": 2,
        "signed_count": 1,
    }


def test_bn6b_source_has_no_live_signing_or_provider_webhook_implementation():
    core_src = _read("backend/core/document_workflows.py")
    server_src = _read("backend/server.py")
    requirements = _read("backend/requirements.txt").lower()
    route_src = _read("backend/routes/document_signatures.py")

    assert "docusign-esign" not in requirements
    assert "create_envelope" not in core_src
    assert "send_envelope" not in core_src
    assert "recipient_view" not in core_src
    assert "signing_url" not in core_src
    assert "provider webhook" not in route_src.lower()
    assert "document_workflows" not in server_src
    assert "document_templates" in core_src
    assert "document_requests" in core_src
    assert "document_signatures" in core_src
    assert "document_acknowledgements" in core_src
