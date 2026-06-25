"""Build-Next-6F DocuSign Connect webhook status sync tests.

BN6F is live-capable but disabled by default. It may process HMAC-verified
status-only DocuSign Connect payloads for existing local requests, but it must
not store raw provider payloads, documents, signer identities, or legal text.
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.document_signing import (
    docusign_account_id_matches,
    docusign_connect_configuration_matches,
    docusign_hmac_signature,
    docusign_webhook_envelope_id,
    docusign_webhook_ready,
    docusign_webhook_status,
    docusign_webhook_status_changed_at,
    document_signature_strategy_snapshot,
    verify_docusign_hmac,
)
from core.document_workflows import (
    DOCUMENT_REQUESTS_COLLECTION,
    PROVIDER_DOCUSIGN,
    WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT,
    WORKFLOW_PROVIDER_SIGNATURE,
    audit_safe_document_metadata,
    provider_status_to_local_status,
)
from routes.document_signatures import build_router


ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _webhook_env(**overrides):
    env = {
        "DOCUSIGN_WEBHOOKS_ENABLED": "true",
        "DOCUSIGN_WEBHOOK_SECRET": "webhook-secret",
        "DOCUSIGN_CONNECT_CONFIGURATION_ID": "22209160",
        "DOCUSIGN_ACCOUNT_ID": "api-account-guid",
    }
    env.update(overrides)
    return env


def _payload(**overrides):
    payload = {
        "event": "recipient-sent",
        "configurationId": "22209160",
        "generatedDateTime": "2026-06-23T01:00:00Z",
        "data": {
            "accountId": "api-account-guid",
            "envelopeId": "env_123",
            "envelopeSummary": {
                "status": "sent",
                "statusChangedDateTime": "2026-06-23T01:01:00Z",
                "emailSubject": "private subject",
                "emailBlurb": "private body",
                "sender": {"email": "sender@example.com", "userName": "Sender"},
                "recipients": {"signers": [{"email": "signer@example.com", "name": "Signer"}]},
                "envelopeDocuments": [{"name": "Private.pdf", "PDFBytes": "base64-pdf"}],
            },
        },
    }
    payload.update(overrides)
    return payload


class _FakeCollection:
    def __init__(self, rows):
        self.rows = [dict(row) for row in rows]
        self.find_filters = []
        self.update_calls = []

    async def find_one(self, query, projection=None):
        self.find_filters.append(dict(query))
        for row in self.rows:
            if all(row.get(key) == value for key, value in query.items()):
                return dict(row)
        return None

    async def update_one(self, query, update):
        self.update_calls.append({"query": dict(query), "update": dict(update)})
        for row in self.rows:
            if all(row.get(key) == value for key, value in query.items()):
                row.update(update.get("$set", {}))
                break


class _FakeDB:
    def __init__(self, rows):
        self.collection = _FakeCollection(rows)

    def __getitem__(self, name):
        assert name == DOCUMENT_REQUESTS_COLLECTION
        return self.collection


def _signed_headers(payload, secret="webhook-secret"):
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return {"X-DocuSign-Signature-1": docusign_hmac_signature(body, secret)}


def _webhook_client(fake_db, monkeypatch):
    for key, value in _webhook_env().items():
        monkeypatch.setenv(key, value)
    audit_rows = []

    async def fake_audit_record(**kwargs):
        audit_rows.append(kwargs)

    monkeypatch.setattr("routes.document_signatures.audit.record", fake_audit_record)
    app = FastAPI()
    app.include_router(build_router(get_current_user=lambda: {}, db=fake_db), prefix="/api")
    return TestClient(app), audit_rows


def test_bn6f_webhook_processing_disabled_by_default():
    ready, reason = docusign_webhook_ready({})
    snap = document_signature_strategy_snapshot(env={})

    assert ready is False
    assert reason == "webhooks_disabled"
    assert snap["webhook_status_sync_enabled"] is False
    assert snap["legal_signature_provider"]["webhook_status_sync_status"] == "webhooks_disabled"


def test_bn6f_webhook_requires_secret_even_when_enabled():
    ready, reason = docusign_webhook_ready({"DOCUSIGN_WEBHOOKS_ENABLED": "true"})

    assert ready is False
    assert reason == "webhook_secret_required"


def test_bn6f_hmac_signature_verification_uses_raw_body_and_constant_safe_header_lookup():
    body = json.dumps(_payload(), separators=(",", ":")).encode("utf-8")
    sig = docusign_hmac_signature(body, "webhook-secret")

    assert verify_docusign_hmac(body, {"X-DocuSign-Signature-1": sig}, _webhook_env()) is True
    assert verify_docusign_hmac(body, {"x-docusign-signature-1": sig}, _webhook_env()) is True
    assert verify_docusign_hmac(body + b" ", {"X-DocuSign-Signature-1": sig}, _webhook_env()) is False
    assert verify_docusign_hmac(body, {"X-DocuSign-Signature-1": "bad"}, _webhook_env()) is False


def test_bn6f_configuration_and_account_allowlist_checks():
    payload = _payload()

    assert docusign_connect_configuration_matches(payload, _webhook_env()) is True
    assert docusign_connect_configuration_matches(payload, _webhook_env(DOCUSIGN_CONNECT_CONFIGURATION_ID="other")) is False
    assert docusign_account_id_matches(payload, _webhook_env()) is True
    assert docusign_account_id_matches(payload, _webhook_env(DOCUSIGN_ACCOUNT_ID="other")) is False


def test_bn6f_extracts_status_only_from_rich_payload():
    payload = _payload()

    assert docusign_webhook_envelope_id(payload) == "env_123"
    assert docusign_webhook_status(payload) == "sent"
    assert docusign_webhook_status_changed_at(payload) == "2026-06-23T01:01:00Z"
    assert provider_status_to_local_status("completed") == "completed"
    assert provider_status_to_local_status("mystery_status") == "provider_attention"


def test_bn6f_route_updates_only_docusign_provider_signature_rows(monkeypatch):
    payload = _payload()
    fake_db = _FakeDB([
        {
            "id": "doc_req_bad",
            "barn_id": "barn_a",
            "provider_envelope_id": "env_123",
            "provider": "none",
            "workflow_kind": WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT,
            "status": "draft",
            "local_status": "draft",
        },
        {
            "id": "doc_req_good",
            "barn_id": "barn_a",
            "provider_envelope_id": "env_456",
            "provider": PROVIDER_DOCUSIGN,
            "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
            "status": "draft",
            "local_status": "draft",
        },
    ])
    client, audit_rows = _webhook_client(fake_db, monkeypatch)

    response = client.post(
        "/api/document-signatures/docusign/webhook",
        content=json.dumps(payload, separators=(",", ":")),
        headers=_signed_headers(payload),
    )

    assert response.status_code == 200
    assert response.json() == {"accepted": True, "matched": False}
    assert fake_db.collection.update_calls == []
    assert audit_rows == []
    assert fake_db.collection.find_filters[-1] == {
        "provider_envelope_id": "env_123",
        "provider": PROVIDER_DOCUSIGN,
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
    }

    payload["data"]["envelopeId"] = "env_456"
    payload["data"]["envelopeSummary"]["status"] = "completed"
    response = client.post(
        "/api/document-signatures/docusign/webhook",
        content=json.dumps(payload, separators=(",", ":")),
        headers=_signed_headers(payload),
    )

    assert response.status_code == 200
    assert response.json() == {"accepted": True, "matched": True, "status": "completed"}
    assert fake_db.collection.update_calls[-1]["query"] == {
        "id": "doc_req_good",
        "provider_envelope_id": "env_456",
        "provider": PROVIDER_DOCUSIGN,
        "workflow_kind": WORKFLOW_PROVIDER_SIGNATURE,
    }
    update = fake_db.collection.update_calls[-1]["update"]["$set"]
    assert update["provider_status"] == "completed"
    assert update["status"] == "completed"
    assert update["local_status"] == "completed"
    assert "raw_provider_payload" not in update
    assert len(audit_rows) == 1
    assert audit_rows[0]["action"] == "document_request.provider_status_updated"


def test_bn6f_audit_metadata_excludes_raw_provider_payload_and_signer_details():
    payload = _payload()
    doc = {
        "id": "doc_req_1",
        "document_type": "general_liability_waiver",
        "workflow_kind": "provider_signature",
        "provider": "docusign",
        "status": "completed",
        "local_status": "completed",
        "required_signer_user_ids": ["guardian_1"],
        "signed_user_ids": ["guardian_1"],
        "raw_provider_payload": payload,
        "provider_envelope_id": "env_123",
    }

    metadata = audit_safe_document_metadata(doc)
    blob = str(metadata).lower()

    assert metadata["status"] == "completed"
    assert metadata["local_status"] == "completed"
    assert metadata["required_signer_count"] == 1
    assert "private subject" not in blob
    assert "signer@example.com" not in blob
    assert "base64-pdf" not in blob
    assert "env_123" not in blob


def test_bn6f_route_source_is_public_webhook_but_hmac_and_config_gated():
    route_src = _read("backend/routes/document_signatures.py")

    assert '"/document-signatures/docusign/webhook"' in route_src
    assert "verify_docusign_hmac(body, request.headers)" in route_src
    assert "docusign_connect_configuration_matches(payload)" in route_src
    assert "docusign_account_id_matches(payload)" in route_src
    assert "provider_status_to_local_status(provider_status)" in route_src
    assert "document_request.provider_status_updated" in route_src
    assert '"matched": False' in route_src


def test_bn6f_webhook_match_is_limited_to_docusign_provider_signature_rows():
    route_src = _read("backend/routes/document_signatures.py")
    start = route_src.find('async def docusign_connect_webhook')
    assert start >= 0
    end = route_src.find("\n    return router", start)
    body = route_src[start:end]

    assert '"provider_envelope_id": envelope_id' in body
    assert '"provider": PROVIDER_DOCUSIGN' in body
    assert '"workflow_kind": WORKFLOW_PROVIDER_SIGNATURE' in body
    assert 'find_one(\n            match_filter' in body
    assert '{"id": doc["id"], **match_filter}' in body


def test_bn6f_source_never_persists_raw_payload_documents_or_signer_identity():
    route_src = _read("backend/routes/document_signatures.py").lower()
    signing_src = _read("backend/core/document_signing.py").lower()
    combined = f"{route_src}\n{signing_src}"

    assert "raw_provider_payload" not in route_src
    assert "envelopedocuments" not in route_src
    assert "pdfbytes" not in route_src
    assert "recipients" not in route_src
    assert "sender" not in route_src
    assert "signed_document_body" not in signing_src
    assert "signed_document_url" not in signing_src
    assert "recipient_view" not in combined
    assert "signing_url" not in combined
