from __future__ import annotations

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

from core.document_workflows import build_template_contract  # noqa: E402
from routes.backlog import build_router as build_backlog_router  # noqa: E402
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
        if isinstance(field, list):
            for name, order in reversed(field):
                self.rows.sort(key=lambda row: str(_value(row, name) or ""), reverse=order < 0)
            return self
        if field:
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

    async def count_documents(self, query):
        return len([row for row in self.rows if _matches(row, query or {})])


class _FakeDB:
    def __init__(self):
        self.document_templates = _Collection([
            {
                **build_template_contract(
                    "minor_participant_liability_waiver",
                    template_id="tmpl-minor",
                    barn_id="barn-1",
                    provider_template_id="provider-template-1",
                    status="active",
                ),
                "created_at": "2026-07-07T08:00:00Z",
                "updated_at": "2026-07-07T08:00:00Z",
            }
        ])
        self.document_requests = _Collection([])
        self.student_profiles = _Collection([])
        self.audit_log = _Collection([])
        self.backlog_audit_events = _Collection([])
        self.owners = _Collection([
            {"id": "owner-doc-1", "barn_id": "barn-1", "user_id": "owner-1"},
            {"id": "owner-doc-2", "barn_id": "barn-1", "user_id": "owner-2"},
        ])
        self.digital_forms = _Collection([
            {
                "id": "form-owner",
                "barn_id": "barn-1",
                "archived_at": None,
                "created_at": "2026-07-07T08:00:00Z",
                "updated_at": "2026-07-07T08:00:00Z",
                "data": {
                    "title": "Barn Rules",
                    "status": "sent",
                    "owner_user_id": "owner-1",
                    "signature_provider": "internal",
                },
            },
            {
                "id": "form-other-owner",
                "barn_id": "barn-1",
                "archived_at": None,
                "created_at": "2026-07-07T08:01:00Z",
                "updated_at": "2026-07-07T08:01:00Z",
                "data": {
                    "title": "Other Owner Rules",
                    "status": "sent",
                    "owner_user_id": "owner-2",
                    "signature_provider": "internal",
                },
            },
        ])
        self.integration_connections = _Collection([])

    def __getitem__(self, name):
        return getattr(self, name)


def _client(user: Dict[str, Any]):
    db = _FakeDB()

    async def get_current_user():
        return dict(user)

    def new_id():
        return f"new-{len(db.digital_forms.rows) + len(db.backlog_audit_events.rows) + 1}"

    app = FastAPI()
    app.include_router(build_backlog_router(db=db, get_current_user=get_current_user, new_id=new_id), prefix="/api")
    app.include_router(build_document_signature_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_guardian_required_document_request_requires_guardian_user_ids():
    client, db = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin"})

    missing_guardian = client.post("/api/document-signatures/requests", json={
        "template_id": "tmpl-minor",
        "subject_user_id": "student-1",
        "minor_status": "minor_13_to_17",
    })
    assert missing_guardian.status_code == 422
    assert "guardian_user_ids is required" in missing_guardian.json()["detail"]
    assert db.document_requests.rows == []

    created = client.post("/api/document-signatures/requests", json={
        "template_id": "tmpl-minor",
        "subject_user_id": "student-1",
        "minor_status": "minor_13_to_17",
        "guardian_user_ids": ["guardian-1"],
    })
    assert created.status_code == 200
    body = created.json()
    assert body["signer_roles"] == ["guardian", "subject"]
    assert body["required_signer_count"] == 2
    assert "required_signer_user_ids" not in body
    assert "provider_envelope_id" not in body
    assert len(db.document_requests.rows) == 1


def test_forms_signature_records_are_local_or_provider_readiness_truth():
    client, _db = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin"})

    local = client.post("/api/feature-modules/forms-signatures/records", json={
        "data": {
            "form_name": "Local barn acknowledgement",
            "status": "sent",
            "signature_provider": "internal",
        },
    })
    assert local.status_code == 200
    assert local.json()["data"]["signature_scope"] == "local_acknowledgement_only"
    assert local.json()["data"]["legal_signature_status"] == "not_legal_signature"

    ready_only = client.post("/api/feature-modules/forms-signatures/records", json={
        "data": {
            "form_name": "Provider readiness row",
            "status": "draft",
            "signature_provider": "docusign_ready",
        },
    })
    assert ready_only.status_code == 200
    assert ready_only.json()["data"]["signature_scope"] == "provider_readiness_only"
    assert ready_only.json()["data"]["legal_signature_status"] == "provider_not_sent"


def test_owner_form_acknowledgement_is_scoped_and_not_legal_signature():
    client, _db = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner", "full_name": "Owner One"})

    denied = client.post("/api/owner-portal/forms/form-other-owner/sign")
    assert denied.status_code == 404

    signed = client.post("/api/owner-portal/forms/form-owner/sign")
    assert signed.status_code == 200
    data = signed.json()["data"]
    assert data["status"] == "signed"
    assert data["signed_by"] == "owner-1"
    assert data["signature_scope"] == "local_acknowledgement_only"
    assert data["legal_signature_status"] == "not_legal_signature"
    assert data["signed_claim"] == "local_acknowledgement_not_legal_signature"


def test_owner_document_library_is_scoped_and_private_field_safe():
    client, db = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner", "full_name": "Owner One"})
    db.document_requests.rows.extend([
        {
            "id": "doc-owner",
            "barn_id": "barn-1",
            "template_id": "tmpl-minor",
            "document_type": "general_liability_waiver",
            "display_name": "General liability waiver",
            "workflow_kind": "provider_signature",
            "provider": "docusign",
            "subject_user_id": "owner-1",
            "guardian_user_ids": [],
            "required_signer_user_ids": ["owner-1"],
            "provider_envelope_id": "env-private",
            "provider_signature_id": "sig-private",
            "provider_certificate_ref": "cert-private",
            "signed_document_url": "https://example.invalid/private.pdf",
            "staff_notes": "Internal handling note",
            "status": "sent",
            "local_status": "sent",
            "launch_behavior": "soft_warning",
            "required_signer_count": 1,
            "signed_count": 0,
            "created_at": "2026-07-07T09:00:00Z",
            "updated_at": "2026-07-07T09:01:00Z",
            "expires_at": "2027-07-07",
        },
        {
            "id": "doc-other",
            "barn_id": "barn-1",
            "template_id": "tmpl-minor",
            "document_type": "general_liability_waiver",
            "display_name": "Other owner waiver",
            "workflow_kind": "provider_signature",
            "provider": "docusign",
            "subject_user_id": "owner-2",
            "required_signer_user_ids": ["owner-2"],
            "provider_envelope_id": "env-other",
            "status": "sent",
            "local_status": "sent",
            "created_at": "2026-07-07T09:02:00Z",
            "updated_at": "2026-07-07T09:03:00Z",
        },
    ])

    response = client.get("/api/owner-portal/documents")
    assert response.status_code == 200
    body = response.json()
    assert body["live_signing_enabled"] is False
    assert body["provider_live_activation"] == "disabled"
    documents = body["documents"]
    ids = {row["id"] for row in documents}
    assert "doc-owner" in ids
    assert "form-owner" in ids
    assert "doc-other" not in ids
    assert "form-other-owner" not in ids

    owner_doc = [row for row in documents if row["id"] == "doc-owner"][0]
    assert owner_doc["kind"] == "document_request"
    assert owner_doc["status"] == "sent"
    assert owner_doc["live_signing_enabled"] is False
    forbidden_keys = {
        "provider_envelope_id",
        "provider_signature_id",
        "provider_certificate_ref",
        "signed_document_url",
        "staff_notes",
        "required_signer_user_ids",
    }
    assert forbidden_keys.isdisjoint(owner_doc)


def test_document_scan_prepare_upload_is_upload_intent_only():
    client, _db = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin"})

    response = client.post("/api/integrations/document-scans/prepare-upload", json={
        "filename": "coggins.pdf",
        "mime_type": "application/pdf",
        "byte_size": 2048,
        "document_type": "coggins",
        "horse_name": "Cedar",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "upload_intent_ready"
    assert body["storage_claim"] == "upload_intent_only_no_external_file_mutation_by_rf14"
    assert body["upload"]["upload_url"]
    assert body["message"].startswith("Upload intent only.")
