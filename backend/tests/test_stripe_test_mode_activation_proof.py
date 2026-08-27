"""Stripe test-mode activation proof.

This regression proves the next bounded payment lane without creating Stripe
objects, collecting money, or enabling live payment claims.
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

from core.stripe_client import stripe_test_mode_activation_snapshot  # noqa: E402
from routes.subscriptions import build_router as build_subscriptions_router  # noqa: E402


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
        if key == "$and":
            if not all(_matches(doc, clause) for clause in expected):
                return False
            continue
        actual = _value(doc, key)
        if isinstance(expected, dict) and "$ne" in expected:
            if actual == expected["$ne"]:
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
    if any(v == 0 for k, v in projection.items() if k != "_id"):
        return {
            k: v
            for k, v in doc.items()
            if k != "_id" and projection.get(k, 1) != 0
        }
    included = {k for k, v in projection.items() if v and k != "_id"}
    return {k: doc.get(k) for k in included if k in doc}


class _Cursor:
    def __init__(self, rows: List[Dict[str, Any]], projection=None):
        self.rows = rows
        self.projection = projection

    def sort(self, field, direction=1):
        self.rows.sort(key=lambda row: str(_value(row, field) or ""), reverse=direction < 0)
        return self

    async def to_list(self, length=None, limit=None):
        max_rows = length if length is not None else limit
        selected = self.rows if max_rows is None else self.rows[:max_rows]
        return [_project(row, self.projection) for row in selected]


class _Collection:
    def __init__(self, rows=None):
        self.rows = list(rows or [])
        self.insert_calls = []
        self.update_calls = []

    async def find_one(self, query, projection=None):
        for row in self.rows:
            if _matches(row, query or {}):
                return _project(row, projection)
        return None

    def find(self, query=None, projection=None):
        return _Cursor([row for row in self.rows if _matches(row, query or {})], projection)

    async def insert_one(self, doc):
        self.insert_calls.append(dict(doc))
        self.rows.append(dict(doc))

    async def update_one(self, query, update, upsert=False):
        self.update_calls.append({"query": dict(query), "update": dict(update), "upsert": upsert})
        for row in self.rows:
            if _matches(row, query or {}):
                row.update((update or {}).get("$set", {}))
                for key, value in (update or {}).get("$inc", {}).items():
                    row[key] = row.get(key, 0) + value
                return type("UpdateResult", (), {"matched_count": 1})()
        if upsert:
            doc = dict(query or {})
            doc.update((update or {}).get("$setOnInsert", {}))
            doc.update((update or {}).get("$set", {}))
            for key, value in (update or {}).get("$inc", {}).items():
                doc[key] = doc.get(key, 0) + value
            self.rows.append(doc)
        return type("UpdateResult", (), {"matched_count": 0})()

    async def count_documents(self, query):
        return len([row for row in self.rows if _matches(row, query or {})])


class _FakeDB:
    def __init__(self):
        self.plans = _Collection([
            {
                "id": "starter_barn",
                "tier_code": "starter_barn",
                "name": "Starter Barn",
                "description": "Seeded test-mode subscription plan.",
                "monthly_price_cents": 7900,
                "annual_price_cents": 79000,
                "feature_limits": {"horses": 10, "users": 3, "staff_seats": 2},
                "overage": {},
                "contact_sales": False,
                "display_order": 10,
                "stripe_price_id_monthly": "price_test_starter_monthly",
                "stripe_price_id_annual": "price_test_starter_annual",
                "active": True,
            },
            {
                "id": "free",
                "tier_code": "free",
                "name": "Free",
                "description": "Free fallback.",
                "monthly_price_cents": 0,
                "annual_price_cents": 0,
                "feature_limits": {"horses": 0, "users": 1},
                "active": True,
            },
        ])
        self.barns = _Collection([
            {
                "id": "barn-stripe-proof",
                "name": "Stripe Proof Barn",
                "stripe_customer_id": None,
                "subscription_id": None,
            }
        ])
        self.subscriptions = _Collection([])
        self.billing_events = _Collection([])
        self.subscription_invoices = _Collection([])
        self.payments = _Collection([])
        self.subscription_addons = _Collection([])
        self.account_usage_limits = _Collection([])
        self.horses = _Collection([])
        self.users = _Collection([])
        self.riders = _Collection([])
        self.account_subscriptions = _Collection([])
    def __getitem__(self, name):
        return getattr(self, name)


class _FakeStripeSession(dict):
    def __getattr__(self, item):
        return self[item]


class _FakeStripeClient:
    def __init__(self, calls):
        self.calls = calls
        self.v1 = self
        self.customers = self
        self.checkout = type("Checkout", (), {"sessions": self})()
        self.billing_portal = type("BillingPortal", (), {"sessions": self})()

    def create(self, params):
        if "line_items" in params:
            self.calls.append({"kind": "checkout_session", "params": params})
            return _FakeStripeSession({
                "id": "cs_test_activation_proof",
                "url": "https://checkout.stripe.com/c/test_activation_proof",
            })
        if "return_url" in params:
            self.calls.append({"kind": "portal_session", "params": params})
            return _FakeStripeSession({"id": "bps_test_activation_proof", "url": "https://billing.stripe.com/p/session"})
        self.calls.append({"kind": "customer", "params": params})
        return _FakeStripeSession({"id": "cus_test_activation_proof"})


def _client(user: Dict[str, Any], db: _FakeDB | None = None):
    fake_db = db or _FakeDB()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_subscriptions_router(db=fake_db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), fake_db


def test_stripe_test_mode_activation_snapshot_is_redacted_and_live_disabled():
    snapshot = stripe_test_mode_activation_snapshot(
        env={
            "STRIPE_API_KEY": "rk_test_redacted",
            "STRIPE_WEBHOOK_SECRET": "whsec_redacted",
            "STRIPE_PUBLISHABLE_KEY": "pk_test_redacted",
        },
        allowed_origins=["https://app.equine-sync.test"],
        catalog_ready=True,
    )

    assert snapshot == {
        "provider": "stripe",
        "activation_target": "test_mode",
        "api_key_mode": "restricted_test",
        "publishable_key_mode": "publishable_test",
        "webhook_secret_configured": True,
        "allowed_origin_count": 1,
        "catalog_ready": True,
        "test_mode_ready": True,
        "live_money_enabled": False,
        "live_checkout_enabled": False,
        "live_portal_enabled": False,
    }
    assert "rk_test_redacted" not in json.dumps(snapshot)
    assert "whsec_redacted" not in json.dumps(snapshot)


def test_stripe_test_mode_checkout_webhook_and_owner_safe_subscription_projection(monkeypatch):
    monkeypatch.setenv("STRIPE_API_KEY", "rk_test_activation_proof")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_activation_proof")
    monkeypatch.setenv("APP_BASE_URL", "https://app.equine-sync.test")
    monkeypatch.setenv("ALLOWED_BILLING_ORIGINS", "https://app.equine-sync.test")
    calls = []

    def fake_stripe_client(api_key=None):
        assert api_key == "rk_test_activation_proof"
        return _FakeStripeClient(calls)

    def fake_construct_event(*, payload, sig_header, secret, api_key=None):
        assert sig_header == "t=1,v1=test"
        assert secret == "whsec_activation_proof"
        assert api_key == "rk_test_activation_proof"
        return json.loads(payload)

    def fake_retrieve_subscription(subscription_id):
        assert subscription_id == "sub_test_activation_proof"
        return {
            "id": subscription_id,
            "status": "active",
            "items": {"data": [{"price": {"id": "price_test_starter_monthly"}}]},
            "current_period_start": 1790000000,
            "current_period_end": 1792592000,
            "cancel_at_period_end": False,
            "trial_end": None,
        }

    monkeypatch.setattr("routes.subscriptions.stripe_client", fake_stripe_client)
    monkeypatch.setattr("routes.subscriptions.construct_webhook_event", fake_construct_event)
    monkeypatch.setattr(
        "routes.subscriptions_webhook_handlers._retrieve_stripe_subscription",
        fake_retrieve_subscription,
    )
    db = _FakeDB()
    client, _ = _client({"id": "admin-1", "barn_id": "barn-stripe-proof", "role": "admin"}, db)

    rejected = client.post("/api/subscriptions/checkout", json={
        "plan_tier_code": "starter_barn",
        "billing_cycle": "monthly",
        "origin_url": "https://evil.example",
    })
    assert rejected.status_code == 400
    assert "allow-listed" in rejected.json()["detail"]
    assert calls == []

    checkout = client.post("/api/subscriptions/checkout", json={
        "plan_tier_code": "starter_barn",
        "billing_cycle": "monthly",
        "origin_url": "https://app.equine-sync.test/dashboard",
    })
    assert checkout.status_code == 200, checkout.text
    assert checkout.json()["url"] == "https://checkout.stripe.com/c/test_activation_proof"
    assert [call["kind"] for call in calls] == ["customer", "checkout_session"]
    checkout_params = calls[-1]["params"]
    assert checkout_params["mode"] == "subscription"
    assert checkout_params["line_items"] == [{"price": "price_test_starter_monthly", "quantity": 1}]
    assert checkout_params["success_url"] == "https://app.equine-sync.test/billing/success?session_id={CHECKOUT_SESSION_ID}"
    assert checkout_params["cancel_url"] == "https://app.equine-sync.test/billing/subscription?cancelled=1"
    assert "payment_method_types" not in checkout_params
    assert "automatic_tax" not in checkout_params

    payload = {
        "id": "evt_test_activation_proof",
        "type": "checkout.session.completed",
        "created": 1790000001,
        "data": {
            "object": {
                "id": "cs_test_activation_proof",
                "customer": "cus_test_activation_proof",
                "subscription": "sub_test_activation_proof",
                "metadata": {
                    "barn_id": "barn-stripe-proof",
                    "owner_user_id": "admin-1",
                    "plan_tier_code": "starter_barn",
                    "billing_cycle": "monthly",
                },
            }
        },
    }
    webhook = client.post(
        "/api/webhook/stripe-subscriptions",
        content=json.dumps(payload, separators=(",", ":")),
        headers={"Stripe-Signature": "t=1,v1=test"},
    )
    assert webhook.status_code == 200, webhook.text
    assert webhook.json()["handled"] is True

    subscription = db.subscriptions.rows[0]
    assert subscription["stripe_subscription_id"] == "sub_test_activation_proof"
    assert subscription["stripe_customer_id"] == "cus_test_activation_proof"
    assert subscription["stripe_price_id"] == "price_test_starter_monthly"
    assert subscription["status"] == "active"
    assert "raw_stripe_payload" not in subscription
    assert db.billing_events.rows[0]["processing_status"] == "ok"

    owner_view = client.get("/api/subscriptions/me")
    assert owner_view.status_code == 200
    body = owner_view.json()
    assert body["subscription"]["plan_tier_code"] == "starter_barn"
    assert body["subscription"]["status"] == "active"
    assert "stripe_customer_id" not in body["subscription"]
    assert "stripe_subscription_id" not in body["subscription"]
    assert "stripe_price_id" not in body["subscription"]
    assert "cus_test_activation_proof" not in json.dumps(body)
    assert "sub_test_activation_proof" not in json.dumps(body)
