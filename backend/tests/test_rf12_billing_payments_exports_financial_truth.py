from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017/test")
os.environ.setdefault("DB_NAME", "equinesync_test")

from routes.backlog import build_router as build_backlog_router


ROOT = Path(__file__).resolve().parents[2]


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
            if actual not in expected["$in"]:
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

    async def count_documents(self, query):
        return len([row for row in self.rows if _matches(row, query or {})])


class _FakeDB:
    def __init__(self):
        self.owners = _Collection([
            {"id": "owner-doc-1", "barn_id": "barn-1", "user_id": "owner-1"},
            {"id": "owner-doc-2", "barn_id": "barn-2", "user_id": "owner-2"},
        ])
        self.horses = _Collection([])
        self.invoices = _Collection([
            {
                "id": "invoice-own",
                "barn_id": "barn-1",
                "owner_user_id": "owner-1",
                "owner_id": "owner-doc-1",
                "owner_name": "Owner One",
                "status": "overdue",
                "total": 120.0,
                "due_date": "2026-07-01",
            },
            {
                "id": "invoice-other-barn",
                "barn_id": "barn-2",
                "owner_user_id": "owner-2",
                "owner_id": "owner-doc-2",
                "owner_name": "Owner Two",
                "status": "overdue",
                "total": 999.0,
                "due_date": "2026-07-01",
            },
            {
                "id": "invoice-paid",
                "barn_id": "barn-1",
                "owner_user_id": "owner-1",
                "status": "paid",
                "total": 75.0,
                "due_date": "2026-07-02",
            },
        ])
        self.payment_profiles = _Collection([
            {
                "id": "profile-own",
                "barn_id": "barn-1",
                "owner_user_id": "owner-1",
                "data": {"autopay_status": "not_enrolled"},
                "updated_at": "2026-07-06T09:00:00Z",
            },
            {
                "id": "profile-other",
                "barn_id": "barn-2",
                "owner_user_id": "owner-2",
                "data": {"autopay_status": "not_enrolled"},
                "updated_at": "2026-07-06T09:00:00Z",
            },
        ])
        self.recurring_billing_rules = _Collection([])
        self.expenses = _Collection([
            {
                "id": "expense-own",
                "barn_id": "barn-1",
                "data": {
                    "spent_at": "2026-07-05",
                    "vendor": "Feed Store",
                    "category": "feed",
                    "amount": 40,
                    "notes": "Barn 1 hay",
                },
            },
            {
                "id": "expense-other",
                "barn_id": "barn-2",
                "data": {
                    "spent_at": "2026-07-05",
                    "vendor": "Other Feed",
                    "category": "feed",
                    "amount": 500,
                    "notes": "Barn 2 hay",
                },
            },
        ])
        self.health_reminders = _Collection([])
        self.injury_lameness_cases = _Collection([])
        self.staff_task_assignments = _Collection([])
        self.owner_media_updates = _Collection([])
        self.training_plans = _Collection([])
        self.show_entries = _Collection([])
        self.automation_suggestions = _Collection([])
        self.backlog_audit_events = _Collection([])

    def __getitem__(self, name):
        return getattr(self, name)


def _client(user: Dict[str, Any]):
    db = _FakeDB()

    async def get_current_user():
        return dict(user)

    def new_id():
        return f"new-{len(db.automation_suggestions.rows) + len(db.backlog_audit_events.rows) + 1}"

    app = FastAPI()
    app.include_router(build_backlog_router(db=db, get_current_user=get_current_user, new_id=new_id), prefix="/api")
    return TestClient(app), db


def test_automation_billing_recommendation_counts_only_current_barn_invoices():
    client, _db = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin", "full_name": "Admin"})

    response = client.post("/api/automation/generate-drafts")
    assert response.status_code == 200
    body = response.json()

    billing = next(row for row in body["records"] if row["data"]["suggestion_type"] == "billing_recommendation")
    assert "1 overdue invoice(s)" in billing["data"]["summary"]
    assert "999" not in billing["data"]["summary"]


def test_owner_payment_prepare_is_scoped_and_configuration_only():
    client, _db = _client({"id": "owner-1", "barn_id": "barn-1", "role": "horse_owner"})

    listing = client.get("/api/owner-portal/billing")
    assert listing.status_code == 200
    assert [row["id"] for row in listing.json()["invoices"]] == ["invoice-paid", "invoice-own"]

    denied = client.post("/api/owner-portal/billing/invoice-other-barn/prepare-payment")
    assert denied.status_code == 404

    prepared = client.post("/api/owner-portal/billing/invoice-own/prepare-payment")
    assert prepared.status_code == 200
    body = prepared.json()
    assert body == {
        "invoice_id": "invoice-own",
        "provider": "stripe",
        "status": "configuration_ready",
        "amount": 120.0,
        "message": "Stripe checkout credentials are required before live payment collection is enabled.",
    }
    assert "checkout_url" not in body
    assert "payment_intent" not in body
    assert "client_secret" not in body


def test_quickbooks_export_is_barn_scoped_manifest_not_live_sync():
    client, _db = _client({"id": "admin-1", "barn_id": "barn-1", "role": "admin"})

    response = client.post("/api/integrations/quickbooks/export", json={
        "include_expenses": True,
        "include_invoices": True,
    })
    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "quickbooks_export_ready"
    assert body["provider"] == "quickbooks"
    assert body["content_type"] == "text/csv"
    assert "before configuring live QuickBooks sync" in body["message"]
    assert {row["transaction_id"] for row in body["rows"]} == {"expense-own", "invoice-own", "invoice-paid"}
    assert "expense-other" not in str(body)
    assert "invoice-other-barn" not in str(body)
