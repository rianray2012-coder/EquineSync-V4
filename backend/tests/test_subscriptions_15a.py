"""tests/test_subscriptions_15a.py — Phase 15.A facility subscriptions.

Scope: plan catalog, usage read, subscription checkout (Starter/Professional
only), customer portal, and minimal checkout.session.completed webhook.

Stripe SDK is monkey-patched at the test boundary so we don't require a live
Stripe key. The dev environment's STRIPE_API_KEY=sk_test_emergent is not a
real Stripe key — the production code path is exercised end-to-end with
stub responses.
"""
from __future__ import annotations

import os
import pathlib
import time
import uuid
from unittest.mock import MagicMock

import pytest
import requests


def _base_url():
    v = os.environ.get("REACT_APP_BACKEND_URL")
    if v:
        return v.rstrip("/")
    env = pathlib.Path(__file__).resolve().parents[2] / "frontend" / ".env"
    for line in env.read_text().splitlines():
        if line.startswith("REACT_APP_BACKEND_URL="):
            return line.split("=", 1)[1].strip().rstrip("/")
    raise RuntimeError("REACT_APP_BACKEND_URL not configured")


BASE = _base_url()
API = f"{BASE}/api"


# ---------- helpers ----------

def _signup(role: str = "horse_owner", pwd: str = "phase15apass"):
    payload = {
        "email": f"ph15a_{role}_{time.time_ns()}@test.com",
        "password": pwd,
        "full_name": f"P15A {role}",
        "role": role,
    }
    r = requests.post(f"{API}/auth/signup", json=payload, timeout=15)
    assert r.status_code == 200, r.text
    return r.json()


def _promote_admin(uid: str):
    """Direct DB write to flip the user to admin so `barn:manage` is granted."""
    from pymongo import MongoClient
    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "test_database"
    client = MongoClient(mongo_url)
    client[db_name].users.update_one({"id": uid}, {"$set": {"role": "admin"}})
    client.close()


def _admin_token():
    out = _signup()
    _promote_admin(out["user"]["id"])
    r = requests.post(
        f"{API}/auth/login",
        json={"email": out["user"]["email"], "password": "phase15apass"},
        timeout=15,
    )
    assert r.status_code == 200, r.text
    return r.json()["token"], r.json()["user"]


# ---------- plans catalog ----------

def test_plans_catalog_returns_all_four_tiers():
    out = _signup()
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.get(f"{API}/billing/plans", headers=h, timeout=15)
    assert r.status_code == 200, r.text
    plans = {p["tier_code"]: p for p in r.json()}
    assert {"free", "starter", "professional", "enterprise"} <= set(plans)
    assert plans["enterprise"]["contact_sales"] is True
    assert plans["enterprise"]["monthly_price_cents"] is None
    assert plans["starter"]["monthly_price_cents"] == 4900
    assert plans["starter"]["annual_price_cents"] == 49980
    assert plans["professional"]["monthly_price_cents"] == 14900
    assert plans["professional"]["annual_price_cents"] == 151980
    # Enterprise has no contact_sales pricing — frontend renders "Talk to sales".
    assert plans["enterprise"]["feature_limits"]["horses"] is None
    assert plans["enterprise"]["feature_limits"]["users"] is None


# ---------- usage (barn-scoped, non-blocking) ----------

def test_usage_reports_used_and_limits_without_blocking():
    out = _signup()
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.get(f"{API}/billing/usage", headers=h, timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["barn_id"]
    assert "horses" in body["usage"]
    assert "users" in body["usage"]
    # Soft-warn semantics: limit may already be exceeded (Free defaults to 1).
    # Server MUST NOT block on this endpoint; it just reports counts.
    assert isinstance(body["usage"]["users"]["used"], int)
    assert "feature_flags" in body
    # Free tier flags are all False.
    assert body["feature_flags"]["advanced_reporting"] is False


# ---------- subscription checkout ----------

def test_checkout_rejects_enterprise():
    tok, _ = _admin_token()
    h = {"Authorization": f"Bearer {tok}"}
    r = requests.post(
        f"{API}/subscriptions/checkout",
        json={"plan_tier_code": "enterprise", "billing_cycle": "monthly", "origin_url": BASE},
        headers=h, timeout=15,
    )
    assert r.status_code == 400, r.text
    assert "contact" in r.json()["detail"].lower()


def test_checkout_rejects_unknown_tier():
    tok, _ = _admin_token()
    h = {"Authorization": f"Bearer {tok}"}
    r = requests.post(
        f"{API}/subscriptions/checkout",
        json={"plan_tier_code": "platinum", "billing_cycle": "monthly", "origin_url": BASE},
        headers=h, timeout=15,
    )
    assert r.status_code == 400


def test_checkout_rejects_bad_billing_cycle():
    tok, _ = _admin_token()
    h = {"Authorization": f"Bearer {tok}"}
    r = requests.post(
        f"{API}/subscriptions/checkout",
        json={"plan_tier_code": "starter", "billing_cycle": "biennial", "origin_url": BASE},
        headers=h, timeout=15,
    )
    assert r.status_code == 400


def test_checkout_requires_barn_manage_capability():
    """horse_owner (no admin / barn_manager) must NOT be able to start a
    facility subscription checkout."""
    out = _signup("horse_owner")
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.post(
        f"{API}/subscriptions/checkout",
        json={"plan_tier_code": "starter", "billing_cycle": "monthly", "origin_url": BASE},
        headers=h, timeout=15,
    )
    assert r.status_code == 403, r.text


def test_checkout_requires_stripe_price_id_configured():
    """When the dev catalog couldn't reach Stripe, the plan row will lack
    stripe_price_id_monthly/_annual. The endpoint should return a clear
    500 (NOT crash, NOT pretend to succeed)."""
    tok, _ = _admin_token()
    h = {"Authorization": f"Bearer {tok}"}
    # Inspect the current plan to know whether to expect 500 or 200(stub).
    plans = requests.get(f"{API}/billing/plans", headers=h, timeout=15).json()
    starter = next(p for p in plans if p["tier_code"] == "starter")
    if not starter["has_monthly"]:
        r = requests.post(
            f"{API}/subscriptions/checkout",
            json={"plan_tier_code": "starter", "billing_cycle": "monthly", "origin_url": BASE},
            headers=h, timeout=15,
        )
        assert r.status_code == 500
        assert "stripe price" in r.json()["detail"].lower()
    else:
        # Real Stripe key is configured — the call should reach Stripe.
        # (Skipped in the emergent test env which uses the magic key.)
        pytest.skip("Stripe Price IDs are present — live-key path; covered by integration tests, not unit.")


# ---------- customer portal ----------

def test_customer_portal_requires_existing_stripe_customer():
    """No prior subscription → no stripe_customer_id → 400 with clear message."""
    tok, _ = _admin_token()
    h = {"Authorization": f"Bearer {tok}"}
    r = requests.post(
        f"{API}/subscriptions/customer-portal",
        json={"origin_url": BASE},
        headers=h, timeout=15,
    )
    assert r.status_code == 400
    assert "no stripe customer" in r.json()["detail"].lower()


def test_customer_portal_requires_barn_manage():
    out = _signup("horse_owner")
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.post(
        f"{API}/subscriptions/customer-portal",
        json={"origin_url": BASE},
        headers=h, timeout=15,
    )
    assert r.status_code == 403


# ---------- /subscriptions/me ----------

def test_subscriptions_me_returns_null_when_no_sub():
    out = _signup()
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.get(f"{API}/subscriptions/me", headers=h, timeout=15)
    assert r.status_code == 200
    assert r.json()["subscription"] is None


# ---------- minimal webhook ----------

def test_webhook_ignores_unknown_event_types_with_200():
    """All event types other than checkout.session.completed → 200 + no
    subscription state mutation (15.A explicit scope guard)."""
    # Stripe sends signed events in prod; in dev we accept unsigned JSON for
    # convenience. Send a totally unknown event_type and assert no mutation.
    fake_event = {
        "id": f"evt_test_{uuid.uuid4().hex[:12]}",
        "type": "invoice.created",  # NOT handled in 15.A
        "data": {"object": {"id": f"in_test_{uuid.uuid4().hex[:12]}"}},
    }
    r = requests.post(
        f"{API}/webhook/stripe-subscriptions",
        json=fake_event, timeout=15,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("received") is True
    assert body.get("handled") is False


def test_webhook_checkout_completed_is_idempotent():
    """Test the idempotency guard directly against the DB layer (not Stripe).

    Because we can't actually create a real Subscription in Stripe (test env
    has the magic emergent key), we insert a subscription row by hand with a
    known stripe_subscription_id, then POST a webhook for the same sub id —
    the endpoint should detect the existing row and short-circuit
    (handled=True, idempotent=True). Codex round-2 #2: also verify the barn's
    subscription_id pointer is repaired on replay.
    """
    from pymongo import MongoClient
    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "test_database"
    client = MongoClient(mongo_url)
    db = client[db_name]
    sub_id = f"sub_test_{uuid.uuid4().hex[:12]}"
    barn_id = f"barn_idemp_{uuid.uuid4().hex[:8]}"
    db.subscriptions.insert_one({
        "id": sub_id,
        "barn_id": barn_id,
        "owner_user_id": "test-owner",
        "stripe_subscription_id": sub_id,
        "plan_tier_code": "starter",
        "status": "active",
        "created_at": "2026-01-01T00:00:00+00:00",
    })
    # Pre-condition: barn either missing or missing the subscription_id pointer.
    db.barns.delete_one({"id": barn_id})

    fake_event = {
        "id": f"evt_test_{uuid.uuid4().hex[:12]}",
        "type": "checkout.session.completed",
        "data": {"object": {
            "id": f"cs_test_{uuid.uuid4().hex[:12]}",
            "subscription": sub_id,
            "customer": f"cus_test_{uuid.uuid4().hex[:12]}",
            "metadata": {
                "barn_id": barn_id,
                "owner_user_id": "test-owner",
                "plan_tier_code": "starter",
                "billing_cycle": "monthly",
            },
        }},
    }
    r = requests.post(
        f"{API}/webhook/stripe-subscriptions",
        json=fake_event, timeout=15,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("handled") is True
    assert body.get("idempotent") is True

    # Codex round-2 #2: barn pointer must be repaired idempotently.
    barn = db.barns.find_one({"id": barn_id})
    assert barn is not None, "barn row must be upserted on idempotent replay"
    assert barn.get("subscription_id") == sub_id, (
        "idempotent replay must repair barn.subscription_id"
    )
    assert barn.get("subscription_updated_at")

    # Second replay — still idempotent, same pointer.
    r2 = requests.post(
        f"{API}/webhook/stripe-subscriptions",
        json=fake_event, timeout=15,
    )
    assert r2.status_code == 200
    assert r2.json().get("idempotent") is True
    barn2 = db.barns.find_one({"id": barn_id})
    assert barn2.get("subscription_id") == sub_id
    # Still exactly one subscription row for this stripe_subscription_id.
    assert db.subscriptions.count_documents({"stripe_subscription_id": sub_id}) == 1

    # Cleanup
    db.subscriptions.delete_one({"id": sub_id})
    db.barns.delete_one({"id": barn_id})
    client.close()


# Codex round-2 #1: Stripe.Subscription.retrieve failure must return a
# retryable non-2xx (502), NOT 200 handled:false. That guarantees Stripe
# replays the event and we eventually reconcile the subscription.
def test_webhook_returns_502_when_stripe_retrieve_fails(monkeypatch):
    """Mock stripe.Subscription.retrieve to raise; assert the webhook
    endpoint surfaces 502.

    We can't monkeypatch the running server process, so this test reaches
    in via a direct in-process call to the route handler.
    """
    import asyncio
    import sys
    sys.path.insert(0, "/app/backend")
    import stripe as stripe_sdk
    from fastapi import HTTPException
    from routes.subscriptions import build_router

    class _StubError(stripe_sdk.error.StripeError):
        pass

    def _boom(*a, **k):
        raise _StubError("simulated stripe outage")

    monkeypatch.setattr(stripe_sdk.Subscription, "retrieve", _boom)
    monkeypatch.setenv("STRIPE_API_KEY", "sk_test_anything")
    monkeypatch.delenv("STRIPE_WEBHOOK_SECRET", raising=False)

    # Build a stub DB whose subscriptions.find_one returns None (so the
    # idempotent short-circuit is bypassed and we hit the retrieve path).
    class _Coll:
        def __init__(self, store=None):
            self.store = store or {}
        async def find_one(self, *a, **k):
            return None
        async def update_one(self, *a, **k):
            return None
        async def insert_one(self, *a, **k):
            return None
    class _StubDB:
        plans = _Coll()
        subscriptions = _Coll()
        barns = _Coll()

    async def _fake_get_current_user():
        return {"id": "tester"}

    router = build_router(db=_StubDB(), get_current_user=_fake_get_current_user)
    # Find the webhook handler.
    handler = None
    for route in router.routes:
        if route.path == "/webhook/stripe-subscriptions":
            handler = route.endpoint
            break
    assert handler is not None, "webhook route missing"

    class _StubReq:
        headers = {}
        async def body(self):
            sub_id = f"sub_boom_{uuid.uuid4().hex[:6]}"
            return ('{"id":"evt_test","type":"checkout.session.completed",'
                    '"data":{"object":{"id":"cs_test","subscription":"'
                    + sub_id + '","customer":"cus_test","metadata":{'
                    '"barn_id":"barn_boom","owner_user_id":"u",'
                    '"plan_tier_code":"starter","billing_cycle":"monthly"}}}}').encode()
    with pytest.raises(HTTPException) as ex:
        asyncio.run(handler(_StubReq()))
    assert ex.value.status_code == 502
    assert "stripe" in ex.value.detail.lower()


# ---------- /membership/checkout legacy still works (free tier only) ----------

def test_legacy_membership_checkout_free_tier_still_works():
    """15.A explicitly keeps the old one-time endpoint untouched. The free
    tier short-circuit must still flip subscription_status to 'free'.
    """
    out = _signup()
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.post(
        f"{API}/membership/checkout",
        json={"tier": "free", "origin_url": BASE},
        headers=h, timeout=15,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["url"] is None
    assert body["status"] == "free"


# ===================================================================
# Codex review fixes — focused regression tests
# ===================================================================

# Codex finding #1: production fail-fast must NOT be swallowed.
def test_lifespan_production_fail_fast_is_not_swallowed(monkeypatch):
    """Simulate the production startup path with missing Stripe Price IDs:
    `ensure_stripe_catalog` MUST raise (not log-and-continue), and the
    lifespan wrapper MUST re-raise rather than swallow.
    """
    import asyncio
    import sys
    sys.path.insert(0, "/app/backend")
    from core import billing_provisioning

    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("STRIPE_API_KEY", "sk_test_pretend")
    # Clear any Price IDs that may be set in the env so the prod validator fails.
    for k in (
        "STRIPE_PRICE_STARTER_MONTHLY",
        "STRIPE_PRICE_STARTER_ANNUAL",
        "STRIPE_PRICE_PROFESSIONAL_MONTHLY",
        "STRIPE_PRICE_PROFESSIONAL_ANNUAL",
    ):
        monkeypatch.delenv(k, raising=False)

    class _StubDB:
        class _Plans:
            async def update_one(self, *a, **k): return None
            async def find_one(self, *a, **k): return None
        plans = _Plans()

    db = _StubDB()
    with pytest.raises(RuntimeError) as ex:
        asyncio.run(billing_provisioning.ensure_stripe_catalog(db))
    assert "STRIPE_PRICE" in str(ex.value)


# Codex finding #2: GET /billing/usage and GET /subscriptions/me must NOT
# create barn rows.
def test_usage_endpoint_is_read_only_no_barn_insert():
    """Calling /billing/usage for a user whose barn has no DB row must not
    create one. Repeated calls produce the same answer; barns collection
    document count is unchanged.
    """
    from pymongo import MongoClient
    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "test_database"
    client = MongoClient(mongo_url)
    barns = client[db_name].barns

    # Set the user's barn_id to a unique value that definitely has no row.
    out = _signup()
    uid = out["user"]["id"]
    unique_barn = f"phantom_barn_{uuid.uuid4().hex[:8]}"
    client[db_name].users.update_one({"id": uid}, {"$set": {"barn_id": unique_barn}})

    h = {"Authorization": f"Bearer {out['token']}"}
    # Re-login so the JWT carries the updated barn_id.
    login = requests.post(
        f"{API}/auth/login",
        json={"email": out["user"]["email"], "password": "phase15apass"},
        timeout=15,
    ).json()
    h = {"Authorization": f"Bearer {login['token']}"}

    before = barns.count_documents({"id": unique_barn})
    assert before == 0

    r1 = requests.get(f"{API}/billing/usage", headers=h, timeout=15)
    r2 = requests.get(f"{API}/billing/usage", headers=h, timeout=15)
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["barn_id"] == unique_barn

    after = barns.count_documents({"id": unique_barn})
    assert after == 0, f"GET /billing/usage created a barn row (before={before}, after={after})"


def test_subscriptions_me_is_read_only_no_barn_insert():
    """Same invariant for /subscriptions/me — pure read."""
    from pymongo import MongoClient
    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "test_database"
    client = MongoClient(mongo_url)
    barns = client[db_name].barns

    out = _signup()
    uid = out["user"]["id"]
    unique_barn = f"phantom_barn_{uuid.uuid4().hex[:8]}"
    client[db_name].users.update_one({"id": uid}, {"$set": {"barn_id": unique_barn}})
    login = requests.post(
        f"{API}/auth/login",
        json={"email": out["user"]["email"], "password": "phase15apass"},
        timeout=15,
    ).json()
    h = {"Authorization": f"Bearer {login['token']}"}

    assert barns.count_documents({"id": unique_barn}) == 0
    r = requests.get(f"{API}/subscriptions/me", headers=h, timeout=15)
    assert r.status_code == 200
    assert r.json()["barn_id"] == unique_barn
    assert r.json()["subscription"] is None
    assert barns.count_documents({"id": unique_barn}) == 0


# Codex finding #3: dev-mode catalog must upsert ALL 4 plans even when the
# Stripe key is missing or unreachable.
def test_plans_catalog_contains_all_four_tiers_even_without_stripe():
    """Local /billing/plans MUST always return Free, Starter, Professional,
    Enterprise — regardless of Stripe connectivity. Starter + Professional
    may have null Stripe IDs in dev (the `has_monthly`/`has_annual` flags
    on the public payload reflect this).
    """
    out = _signup()
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.get(f"{API}/billing/plans", headers=h, timeout=15)
    assert r.status_code == 200
    tiers = {p["tier_code"] for p in r.json()}
    assert tiers == {"free", "starter", "professional", "enterprise"}, (
        f"Catalog must always contain all four tiers in dev (got {tiers})"
    )


# Codex finding #4: origin_url must be allow-listed.
def test_checkout_rejects_unlisted_origin():
    tok, _ = _admin_token()
    h = {"Authorization": f"Bearer {tok}"}
    r = requests.post(
        f"{API}/subscriptions/checkout",
        json={
            "plan_tier_code": "starter",
            "billing_cycle": "monthly",
            "origin_url": "https://evil.example.com",  # NOT allow-listed
        },
        headers=h, timeout=15,
    )
    assert r.status_code == 400, r.text
    assert "allow-list" in r.json()["detail"].lower()


# Codex finding #5: /subscriptions/me strips raw Stripe IDs.
def test_subscriptions_me_strips_stripe_ids():
    """When a subscription doc carries Stripe IDs in the DB, the /me endpoint
    must NOT echo them back."""
    from pymongo import MongoClient
    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "test_database"
    client = MongoClient(mongo_url)
    db = client[db_name]

    out = _signup()
    uid = out["user"]["id"]
    barn_id = f"barn_strip_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_strip_{uuid.uuid4().hex[:8]}"
    db.users.update_one({"id": uid}, {"$set": {"barn_id": barn_id}})
    db.barns.insert_one({
        "id": barn_id,
        "stripe_customer_id": "cus_secret_should_not_leak",
        "subscription_id": sub_id,
    })
    db.subscriptions.insert_one({
        "id": sub_id,
        "barn_id": barn_id,
        "owner_user_id": uid,
        "plan_tier_code": "starter",
        "status": "active",
        "billing_cycle": "monthly",
        "stripe_customer_id": "cus_secret_should_not_leak",
        "stripe_subscription_id": "sub_secret_should_not_leak",
        "stripe_price_id": "price_secret_should_not_leak",
    })

    login = requests.post(
        f"{API}/auth/login",
        json={"email": out["user"]["email"], "password": "phase15apass"},
        timeout=15,
    ).json()
    h = {"Authorization": f"Bearer {login['token']}"}
    r = requests.get(f"{API}/subscriptions/me", headers=h, timeout=15)
    assert r.status_code == 200
    sub = r.json()["subscription"]
    assert sub is not None
    for k in ("stripe_customer_id", "stripe_subscription_id", "stripe_price_id"):
        assert k not in sub, f"raw Stripe id {k} leaked in /subscriptions/me"
    # ...but the non-secret fields still come through.
    assert sub["plan_tier_code"] == "starter"
    assert sub["status"] == "active"

    # Cleanup
    db.subscriptions.delete_one({"id": sub_id})
    db.barns.delete_one({"id": barn_id})
    client.close()
