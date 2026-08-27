"""Gate 6 DocuSign sandbox-only activation proof.

This regression uses one seeded provider-signature document fixture and proves
the bounded activation contract without reaching DocuSign or storing signed
documents locally.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017/test")
os.environ.setdefault("DB_NAME", "equinesync_test")

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from core.document_signing import (  # noqa: E402
    DOCUSIGN_DEFAULT_AUTH_SERVER,
    DOCUSIGN_DEMO_BASE_URL,
    docusign_hmac_signature,
)
from core.document_workflows import build_template_contract  # noqa: E402
from routes.document_signatures import build_router as build_document_signature_router  # noqa: E402


def _value(doc: Dict[str, Any], key: str) -> Any:
    actual: Any = doc
    for part in key.split("."):
        if not isinstance(actual, dict):
            return None
        actual = actual.get(part)
    return actual


def _matches(doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
    for key, expected in (query or {}).items():
        if key == "$or":
            if not any(_matches(doc, clause) for clause in expected):
                return False
            continue
        actual = _value(doc, key)
        if isinstance(expected, dict) and "$exists" in expected:
            exists = actual is not None
            if exists is not bool(expected["$exists"]):
                return False
        elif isinstance(expected, dict) and "$in" in expected:
            if isinstance(actual, list):
                if not any(item in expected["$in"] for item in actual):
                    return False
            elif actual not in expected["$in"]:
                return False
        elif isinstance(actual, list):
            if expected not in actual:
                return False
        elif actual != expected:
            return False
    return True


def _project(doc: Dict[str, Any], projection: Dict[str, Any] | None) -> Dict[str, Any]:
    if not projection or projection == {"_id": 0}:
        return {k: v for k, v in doc.items() if k != "_id"}
    included = {k for k, v in projection.items() if v and k != "_id"}
    return {k: doc.get(k) for k in included if k in doc}


class _Cursor:
    def __init__(self, rows: List[Dict[str, Any]], projection=None):
        self.rows = rows
        self.projection = projection

    def sort(self, field, direction=1):
        self.rows.sort(key=lambda row: str(_value(row, field) or ""), reverse=direction < 0)
        return self

    async def to_list(self, limit):
        return [_project(row, self.projection) for row in self.rows[:limit]]


class _Collection:
    def __init__(self, rows=None):
        self.rows = list(rows or [])

    async def find_one(self, query, projection=None):
        for row in self.rows:
            if _matches(row, query):
                return _project(row, projection)
        return None

    def find(self, query=None, projection=None):
        return _Cursor([row for row in self.rows if _matches(row, query or {})], projection)

    async def insert_one(self, doc):
        self.rows.append(dict(doc))

    async def update_one(self, query, update, upsert=False):
        for row in self.rows:
            if _matches(row, query):
                row.update((update or {}).get("$set", {}))
                return type("UpdateResult", (), {"matched_count": 1})()
        if upsert:
            doc = dict(query)
            doc.update((update or {}).get("$set", {}))
            self.rows.append(doc)
        return type("UpdateResult", (), {"matched_count": 0})()


class _FakeDB:
    def __init__(self):
        self.document_templates = _Collection([
            {
                **build_template_contract(
                    "general_liability_waiver",
                    template_id="tmpl-docusign-provider",
                    barn_id="barn-1",
                    provider_template_id="provider-template-sandbox",
                    status="active",
                ),
                "created_at": "2026-08-27T08:00:00Z",
                "updated_at": "2026-08-27T08:00:00Z",
            }
        ])
        self.document_requests = _Collection([
            {
                "id": "doc-owner-sandbox",
                "barn_id": "barn-1",
                "template_id": "tmpl-docusign-provider",
                "document_type": "general_liability_waiver",
                "display_name": "General liability waiver",
                "workflow_kind": "provider_signature",
                "provider": "docusign",
                "subject_user_id": "owner-1",
                "subject_student_profile_id": None,
                "minor_status": "adult",
                "signer_roles": ["subject"],
                "required_signer_user_ids": ["owner-1"],
                "required_signer_count": 1,
                "signed_user_ids": [],
                "signed_count": 0,
                "provider_envelope_id": None,
                "status": "draft",
                "local_status": "draft",
                "launch_behavior": "soft_warning",
                "requested_by_user_id": "admin-1",
                "created_at": "2026-08-27T08:01:00Z",
                "updated_at": "2026-08-27T08:01:00Z",
                "expires_at": "2027-08-27",
            },
            {
                "id": "doc-other-owner",
                "barn_id": "barn-1",
                "template_id": "tmpl-docusign-provider",
                "document_type": "general_liability_waiver",
                "display_name": "Other owner waiver",
                "workflow_kind": "provider_signature",
                "provider": "docusign",
                "subject_user_id": "owner-2",
                "signer_roles": ["subject"],
                "required_signer_user_ids": ["owner-2"],
                "provider_envelope_id": "env-other-owner-private",
                "status": "sent",
                "local_status": "sent",
                "created_at": "2026-08-27T08:02:00Z",
                "updated_at": "2026-08-27T08:02:00Z",
            },
        ])
        self.student_profiles = _Collection([])
        self.digital_forms = _Collection([])
        self.audit_log = _Collection([])

    def __getitem__(self, name):
        return getattr(self, name)


def _client(user: Dict[str, Any], db: _FakeDB | None = None):
    fake_db = db or _FakeDB()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_document_signature_router(db=fake_db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), fake_db


def _set_sandbox_env(monkeypatch, **overrides):
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
        "DOCUSIGN_WEBHOOKS_ENABLED": "true",
        "DOCUSIGN_WEBHOOK_SECRET": "webhook-secret",
        "DOCUSIGN_CONNECT_CONFIGURATION_ID": "config-gate6",
    }
    env.update(overrides)
    for key, value in env.items():
        monkeypatch.setenv(key, value)


def _webhook_payload(envelope_id: str, status: str = "completed") -> Dict[str, Any]:
    return {
        "event": "recipient-completed",
        "configurationId": "config-gate6",
        "generatedDateTime": "2026-08-27T09:00:00Z",
        "data": {
            "accountId": "api-account-guid",
            "envelopeId": envelope_id,
            "envelopeSummary": {
                "status": status,
                "statusChangedDateTime": "2026-08-27T09:01:00Z",
                "emailSubject": "private subject must not persist",
                "recipients": {"signers": [{"email": "owner@example.test", "name": "Owner One"}]},
                "envelopeDocuments": [{"name": "Signed.pdf", "PDFBytes": "base64-private"}],
            },
        },
    }


def _signed_headers(payload: Dict[str, Any]) -> Dict[str, str]:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return {"X-DocuSign-Signature-1": docusign_hmac_signature(body, "webhook-secret")}


def test_gate6_docusign_sandbox_fixture_enforces_authority_reference_only_storage_and_owner_projection(monkeypatch):
    _set_sandbox_env(monkeypatch)
    calls = []

    def fake_create_envelope(*, account_id, provider_template_id, recipient_roles, request_id):
        calls.append({
            "account_id": account_id,
            "provider_template_id": provider_template_id,
            "recipient_roles": recipient_roles,
            "request_id": request_id,
        })
        return {
            "provider_envelope_id": "env-sandbox-proof",
            "provider_status": "created",
        }

    monkeypatch.setattr("routes.document_signatures.create_docusign_sandbox_envelope", fake_create_envelope)
    db = _FakeDB()

    owner_client, _ = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner"}, db)
    denied = owner_client.post("/api/document-signatures/requests/doc-owner-sandbox/sandbox-envelope")
    assert denied.status_code == 403
    assert denied.json()["detail"] == "Admin/Manager only"
    assert calls == []
    assert db.document_requests.rows[0]["provider_envelope_id"] is None

    admin_client, _ = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin"}, db)
    created = admin_client.post("/api/document-signatures/requests/doc-owner-sandbox/sandbox-envelope")
    assert created.status_code == 200
    created_body = created.json()
    assert created_body["sandbox_envelope_created"] is True
    assert created_body["provider_status"] == "created"
    assert created_body["status"] == "draft"
    assert "provider_envelope_id" not in created_body
    assert "signing_url" not in json.dumps(created_body).lower()
    assert calls == [{
        "account_id": "api-account-guid",
        "provider_template_id": "provider-template-sandbox",
        "recipient_roles": ["subject"],
        "request_id": "doc-owner-sandbox",
    }]

    stored = db.document_requests.rows[0]
    assert stored["provider_envelope_id"] == "env-sandbox-proof"
    assert stored["provider_status"] == "created"
    assert stored["local_status"] == "draft"
    private_blob = json.dumps(stored).lower()
    assert "signed_document_url" not in stored
    assert "signed_document_body" not in stored
    assert "raw_provider_payload" not in stored
    assert "signing_url" not in private_blob

    duplicate = admin_client.post("/api/document-signatures/requests/doc-owner-sandbox/sandbox-envelope")
    assert duplicate.status_code == 409

    payload = _webhook_payload("env-sandbox-proof", status="completed")
    webhook = admin_client.post(
        "/api/document-signatures/docusign/webhook",
        content=json.dumps(payload, separators=(",", ":")),
        headers=_signed_headers(payload),
    )
    assert webhook.status_code == 200
    assert webhook.json() == {"accepted": True, "matched": True, "status": "completed"}
    assert stored["provider_status"] == "completed"
    assert stored["local_status"] == "completed"
    assert stored["provider_status_changed_at"] == "2026-08-27T09:01:00Z"
    completed_blob = json.dumps(stored).lower()
    assert "private subject must not persist" not in completed_blob
    assert "owner@example.test" not in completed_blob
    assert "base64-private" not in completed_blob
    assert "raw_provider_payload" not in stored
    assert "signed_document_body" not in stored
    assert "signed_document_url" not in stored

    owner_documents = owner_client.get("/api/owner-portal/documents")
    assert owner_documents.status_code == 200
    body = owner_documents.json()
    assert body["live_signing_enabled"] is False
    assert body["provider_live_activation"] == "disabled"
    rows = body["documents"]
    ids = {row["id"] for row in rows}
    assert "doc-owner-sandbox" in ids
    assert "doc-other-owner" not in ids
    owner_doc = [row for row in rows if row["id"] == "doc-owner-sandbox"][0]
    assert owner_doc["status"] == "completed"
    assert owner_doc["live_signing_enabled"] is False
    forbidden = {
        "provider_envelope_id",
        "provider_signature_id",
        "provider_certificate_ref",
        "signed_document_url",
        "required_signer_user_ids",
        "staff_notes",
    }
    assert forbidden.isdisjoint(owner_doc)


def test_gate6_docusign_sandbox_fixture_rejects_production_base_url_before_provider_call(monkeypatch):
    _set_sandbox_env(monkeypatch, DOCUSIGN_BASE_URL="https://www.docusign.net/restapi")
    calls = []

    def fake_create_envelope(**kwargs):
        calls.append(kwargs)
        return {"provider_envelope_id": "env-should-not-exist", "provider_status": "created"}

    monkeypatch.setattr("routes.document_signatures.create_docusign_sandbox_envelope", fake_create_envelope)
    admin_client, db = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin"})

    response = admin_client.post("/api/document-signatures/requests/doc-owner-sandbox/sandbox-envelope")

    assert response.status_code == 403
    assert "sandbox_base_url_required" in response.json()["detail"]
    assert calls == []
    assert db.document_requests.rows[0]["provider_envelope_id"] is None


def test_gate6_docusign_sandbox_fixture_allows_manager_send_authority(monkeypatch):
    _set_sandbox_env(monkeypatch)

    def fake_create_envelope(**kwargs):
        return {"provider_envelope_id": "env-manager-sandbox", "provider_status": "created"}

    monkeypatch.setattr("routes.document_signatures.create_docusign_sandbox_envelope", fake_create_envelope)
    manager_client, db = _client({"id": "manager-1", "barn_id": "barn-1", "role": "barn_manager"})

    response = manager_client.post("/api/document-signatures/requests/doc-owner-sandbox/sandbox-envelope")

    assert response.status_code == 200
    assert response.json()["sandbox_envelope_created"] is True
    assert db.document_requests.rows[0]["provider_envelope_id"] == "env-manager-sandbox"
