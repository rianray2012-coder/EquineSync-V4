"""Build-Next-6E DocuSign sandbox envelope creation tests.

BN6E may create a sandbox draft envelope only when explicitly enabled. It must
not send envelopes, generate signing URLs, register webhooks, fetch/store signed
documents, or expose provider identifiers in normal API projections.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from core.document_signing import (
    DOCUSIGN_DEFAULT_AUTH_SERVER,
    DOCUSIGN_DEMO_BASE_URL,
    create_docusign_sandbox_envelope,
    docusign_demo_base_url_matches,
    docusign_sandbox_ready,
    document_signature_strategy_snapshot,
)
from core.document_workflows import project_document_record


ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _sandbox_env(**overrides):
    env = {
        "DOCUSIGN_INTEGRATION_KEY": "integration-key",
        "DOCUSIGN_USER_ID": "user-guid",
        "DOCUSIGN_ACCOUNT_ID": "api-account-guid",
        "DOCUSIGN_PRIVATE_KEY": "FAKE_DOCUSIGN_KEY_FOR_TESTS",
        "DOCUSIGN_AUTH_SERVER": DOCUSIGN_DEFAULT_AUTH_SERVER,
        "DOCUSIGN_BASE_URL": DOCUSIGN_DEMO_BASE_URL,
        "DOCUSIGN_SANDBOX_ENVELOPES_ENABLED": "true",
        "DOCUSIGN_SANDBOX_SIGNER_EMAIL": "sandbox-signer@example.com",
        "DOCUSIGN_SANDBOX_SIGNER_NAME": "Sandbox Signer",
    }
    env.update(overrides)
    return env


def test_bn6e_sandbox_envelope_creation_is_disabled_by_default():
    ready, reason = docusign_sandbox_ready({})
    snap = document_signature_strategy_snapshot(env={})

    assert ready is False
    assert reason == "sandbox_envelopes_disabled"
    assert snap["live_signing_enabled"] is False
    assert snap["envelope_creation_enabled"] is False
    assert snap["sandbox_envelope_creation_enabled"] is False


@pytest.mark.parametrize(
    ("override", "reason"),
    [
        ({"DOCUSIGN_AUTH_SERVER": "account.docusign.com"}, "sandbox_auth_server_required"),
        ({"DOCUSIGN_BASE_URL": "https://www.docusign.net/restapi"}, "sandbox_base_url_required"),
        ({"DOCUSIGN_SANDBOX_SIGNER_EMAIL": ""}, "sandbox_signer_email_required"),
    ],
)
def test_bn6e_sandbox_ready_fails_closed_for_non_sandbox_or_missing_test_signer(override, reason):
    ready, actual = docusign_sandbox_ready(_sandbox_env(**override))

    assert ready is False
    assert actual == reason


def test_bn6e_demo_base_url_validation_rejects_prefix_lookalikes():
    bad = _sandbox_env(DOCUSIGN_BASE_URL="https://demo.docusign.net/restapi.evil.example")
    ready, reason = docusign_sandbox_ready(bad)

    assert docusign_demo_base_url_matches(bad) is False
    assert ready is False
    assert reason == "sandbox_base_url_required"


def test_bn6e_top_level_snapshot_reports_full_sandbox_readiness_not_flag_only():
    flag_only = _sandbox_env(DOCUSIGN_BASE_URL="https://www.docusign.net/restapi")
    ready = document_signature_strategy_snapshot(env=_sandbox_env())
    unsafe = document_signature_strategy_snapshot(env=flag_only)

    assert ready["sandbox_envelope_creation_enabled"] is True
    assert unsafe["sandbox_envelope_creation_enabled"] is False
    assert unsafe["legal_signature_provider"]["sandbox_envelope_creation_status"] == "sandbox_base_url_required"


def test_bn6e_create_sandbox_envelope_uses_demo_draft_payload(monkeypatch):
    calls = []

    def fake_token(env, timeout):
        calls.append({"kind": "token", "timeout": timeout})
        return {"access_token": "token-secret"}

    class FakeResponse:
        status_code = 201

        def json(self):
            return {"envelopeId": "env_sandbox_123", "status": "created"}

    def fake_post(url, headers, json, timeout):
        calls.append({
            "kind": "envelope",
            "url": url,
            "headers": headers,
            "json": json,
            "timeout": timeout,
        })
        return FakeResponse()

    monkeypatch.setattr("core.document_signing.request_docusign_access_token", fake_token)
    monkeypatch.setattr("core.document_signing.requests.post", fake_post)

    result = create_docusign_sandbox_envelope(
        account_id="api-account-guid",
        provider_template_id="provider_template_ref",
        recipient_roles=["guardian", "facility_countersigner"],
        request_id="doc_req_123",
        env=_sandbox_env(),
        timeout=9,
    )

    assert result == {
        "provider_envelope_id": "env_sandbox_123",
        "provider_status": "created",
    }
    envelope_call = [call for call in calls if call["kind"] == "envelope"][0]
    assert envelope_call["url"] == f"{DOCUSIGN_DEMO_BASE_URL}/v2.1/accounts/api-account-guid/envelopes"
    assert envelope_call["headers"] == {
        "Authorization": "Bearer token-secret",
        "Content-Type": "application/json",
    }
    assert envelope_call["json"]["status"] == "created"
    assert envelope_call["json"]["templateId"] == "provider_template_ref"
    assert envelope_call["json"]["templateRoles"] == [
        {"email": "sandbox-signer@example.com", "name": "Sandbox Signer", "roleName": "guardian"},
        {"email": "sandbox-signer@example.com", "name": "Sandbox Signer", "roleName": "facility_countersigner"},
    ]
    assert envelope_call["json"]["customFields"]["textCustomFields"][0]["value"] == "doc_req_123"
    assert "recipientViewRequest" not in str(envelope_call["json"])
    assert "signing_url" not in str(envelope_call["json"]).lower()


def test_bn6e_normal_projection_still_strips_provider_envelope_id():
    projected = project_document_record({
        "id": "doc_req_1",
        "status": "draft",
        "provider_status": "created",
        "provider_envelope_id": "env_secret",
        "sandbox_envelope_created_at": "2026-06-23T00:00:00+00:00",
    })

    assert projected == {
        "id": "doc_req_1",
        "status": "draft",
        "provider_status": "created",
        "sandbox_envelope_created_at": "2026-06-23T00:00:00+00:00",
    }


def test_bn6e_route_source_keeps_sandbox_envelope_manager_only_and_gated():
    route_src = _read("backend/routes/document_signatures.py")

    assert '"/document-signatures/requests/{request_id}/sandbox-envelope"' in route_src
    assert "_require_document_manager(user)" in route_src
    assert "docusign_sandbox_ready()" in route_src
    assert "document_request.sandbox_envelope_created" in route_src
    assert "include_provider_refs=False" in route_src
    assert "provider_envelope_id" in route_src
    assert "sandbox_envelope_created" in route_src


def test_bn6e_source_has_no_signing_url_webhook_storage_or_sdk():
    route_src = _read("backend/routes/document_signatures.py").lower()
    signing_src = _read("backend/core/document_signing.py").lower()
    requirements = _read("backend/requirements.txt").lower()
    combined = f"{route_src}\n{signing_src}"

    assert "docusign-esign" not in requirements
    assert "recipient_view" not in combined
    assert "signing_url" not in combined
    assert '@router.post("/document-signatures/webhook' not in route_src
    assert "signed_document_body" not in signing_src
    assert "signed_document_url" not in signing_src
    assert "get_document" not in signing_src
    assert "status\": \"sent\"" not in signing_src
    assert '"status": "created"' in signing_src
