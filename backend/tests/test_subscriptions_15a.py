"""tests/test_subscriptions_15a.py — Phase 15.A facility subscriptions.

Scope: plan catalog, usage read, subscription checkout for public paid tiers,
customer portal, and checkout.session.completed webhook.

Stripe SDK is monkey-patched at the test boundary so we don't require a live
Stripe key. The dev environment's STRIPE_API_KEY=<test-placeholder> is not a
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
ROOT = pathlib.Path(__file__).resolve().parents[2]


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

def test_plans_catalog_returns_updated_pricing_tiers():
    out = _signup()
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.get(f"{API}/billing/plans", headers=h, timeout=15)
    assert r.status_code == 200, r.text
    plans = {p["tier_code"]: p for p in r.json()}
    expected = {
        "free",
        "individual_owner",
        "private_owner_plus",
        "service_provider_free",
        "service_provider_premium",
        "starter_barn",
        "advanced_barn",
        "elite_barn",
        "trainer_no_lesson",
        "trainer_lesson_15",
        "trainer_lesson_50",
        "enterprise",
        "community_program",
    }
    assert expected <= set(plans)
    assert plans["enterprise"]["contact_sales"] is True
    assert plans["enterprise"]["monthly_price_cents"] is None
    assert plans["individual_owner"]["monthly_price_cents"] == 1499
    assert plans["individual_owner"]["annual_price_cents"] == 14900
    assert plans["service_provider_free"]["monthly_price_cents"] == 0
    assert plans["service_provider_premium"]["monthly_price_cents"] == 1500
    assert plans["service_provider_premium"]["annual_price_cents"] == 18000
    assert plans["starter_barn"]["monthly_price_cents"] == 6999
    assert plans["starter_barn"]["annual_price_cents"] == 69900
    assert plans["advanced_barn"]["monthly_price_cents"] == 14999
    assert plans["advanced_barn"]["annual_price_cents"] == 149900
    assert plans["trainer_lesson_50"]["feature_limits"]["lesson_participants"] == 50
    # Custom-contract tiers have no checkout pricing — frontend renders sales contact.
    assert plans["enterprise"]["feature_limits"]["horses"] is None
    assert plans["enterprise"]["feature_limits"]["users"] is None
    assert plans["community_program"]["contact_sales"] is True


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


def test_individual_owner_checkout_uses_personal_billing_workspace():
    import sys
    import types

    sys.modules.setdefault(
        "stripe",
        types.SimpleNamespace(error=types.SimpleNamespace(StripeError=Exception)),
    )
    from routes.subscriptions import (
        _billing_workspace_id,
        _uses_individual_owner_billing_workspace,
    )

    user = {
        "id": "u_individual_owner",
        "role": "horse_owner",
        "barn_id": "primary",
        "full_name": "Individual Owner",
    }

    assert _uses_individual_owner_billing_workspace(user, "individual_owner") is True
    assert _uses_individual_owner_billing_workspace(user, "private_owner_plus") is True
    assert _uses_individual_owner_billing_workspace(user, "starter_barn") is False

    account_id = _billing_workspace_id(user, "individual_owner")
    assert account_id.startswith("acct_owner_")
    assert account_id != "primary"


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
        json={"plan_tier_code": "starter_barn", "billing_cycle": "biennial", "origin_url": BASE},
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
        json={"plan_tier_code": "starter_barn", "billing_cycle": "monthly", "origin_url": BASE},
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
    starter_barn = next(p for p in plans if p["tier_code"] == "starter_barn")
    if not starter_barn["has_monthly"]:
        r = requests.post(
            f"{API}/subscriptions/checkout",
            json={"plan_tier_code": "starter_barn", "billing_cycle": "monthly", "origin_url": BASE},
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
    """Verifies the /subscriptions/me null path. Because marketplace
    signups share PRIMARY_BARN_ID under the current single-tenant model,
    we explicitly clear barn.subscription_id at the test boundary so the
    contract under test (no subscription → null response) is exercised.
    """
    import os as _os
    from dotenv import load_dotenv as _load_dotenv
    from pymongo import MongoClient as _MongoClient
    _load_dotenv(ROOT / "backend" / ".env")
    _mc = _MongoClient(_os.environ["MONGO_URL"])
    _db = _mc[_os.environ.get("DB_NAME") or "test_database"]
    _db.barns.update_one(
        {"id": "primary"},
        {"$unset": {"subscription_id": "", "subscription_entitlements": "",
                    "subscription_tier_code": "", "subscription_updated_at": ""}},
    )
    _mc.close()

    out = _signup()
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.get(f"{API}/subscriptions/me", headers=h, timeout=15)
    assert r.status_code == 200
    assert r.json()["subscription"] is None


# ---------- minimal webhook ----------

def test_webhook_ignores_unknown_event_types_with_200():
    """All event types not in the dispatcher's HANDLED_EVENTS set → 200 + no
    subscription state mutation. (15.B: `invoice.voided` is a genuine unknown
    type; `invoice.created` is now handled.)
    """
    fake_event = {
        "id": f"evt_test_{uuid.uuid4().hex[:12]}",
        "type": "invoice.voided",
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
    """15.B status-gated semantics: a fresh event_id processes the handler;
    a replay of the same event_id short-circuits via billing_events.

    We also verify the within-handler subscription-row idempotency: when a
    sub already exists for the same stripe_subscription_id but a DIFFERENT
    event_id arrives (e.g. Stripe re-sends the checkout completion under a
    new event), the handler's existing-subscription branch repairs the
    barn pointer without duplicating the subscription row.
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
        "plan_tier_code": "starter_barn",
        "status": "active",
        "pending_emails": [],
        "created_at": "2026-01-01T00:00:00+00:00",
    })
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
                "plan_tier_code": "starter_barn",
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
    # First delivery: dispatcher ran handler → handled=True, idempotent=False.
    assert body.get("handled") is True

    # Within-handler idempotency: barn pointer repaired even though sub already existed.
    barn = db.barns.find_one({"id": barn_id})
    assert barn is not None
    assert barn.get("subscription_id") == sub_id

    # Replay with SAME event_id → status-gated short-circuit.
    r2 = requests.post(
        f"{API}/webhook/stripe-subscriptions",
        json=fake_event, timeout=15,
    )
    assert r2.status_code == 200
    assert r2.json().get("idempotent") is True
    assert db.subscriptions.count_documents({"stripe_subscription_id": sub_id}) == 1

    # Cleanup
    db.subscriptions.delete_one({"id": sub_id})
    db.barns.delete_one({"id": barn_id})
    db.billing_events.delete_one({"stripe_event_id": fake_event["id"]})
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
    sys.path.insert(0, str(ROOT / "backend"))
    import stripe as stripe_sdk
    from fastapi import HTTPException
    from routes.subscriptions import build_router

    class _StubError(stripe_sdk.error.StripeError):
        pass

    def _boom(*a, **k):
        raise _StubError("simulated stripe outage")

    monkeypatch.setattr(stripe_sdk.Subscription, "retrieve", _boom)
    monkeypatch.setenv("STRIPE_API_KEY", "stripe_test_key_placeholder")
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
        async def count_documents(self, *a, **k):
            return 0
    class _StubDB:
        plans = _Coll()
        subscriptions = _Coll()
        barns = _Coll()
        billing_events = _Coll()
        subscription_invoices = _Coll()
        payments = _Coll()

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
                    '"plan_tier_code":"starter_barn","billing_cycle":"monthly"}}}}').encode()
    with pytest.raises(HTTPException) as ex:
        asyncio.run(handler(_StubReq()))
    assert ex.value.status_code == 502
    assert "stripe" in ex.value.detail.lower()


# ---------- /membership/checkout legacy still works (free tier only) ----------

def test_legacy_membership_checkout_free_tier_still_works():
    """Phase 15.G sunset: /api/membership/checkout now returns HTTP 410
    for all tiers. The 15.A invariant that the legacy endpoint reachable
    was relaxed by the user-approved migration cleanup; see
    tests/test_subscriptions_15g.py for the new contract.
    """
    out = _signup()
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.post(
        f"{API}/membership/checkout",
        json={"tier": "free", "origin_url": BASE},
        headers=h, timeout=15,
    )
    assert r.status_code == 410


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
    sys.path.insert(0, str(ROOT / "backend"))
    from core import billing_provisioning

    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("STRIPE_API_KEY", "stripe_test_key_placeholder")
    # Clear any Price IDs that may be set in the env so the prod validator fails.
    for k in (
        "STRIPE_PRICE_INDIVIDUAL_OWNER_MONTHLY",
        "STRIPE_PRICE_INDIVIDUAL_OWNER_ANNUAL",
        "STRIPE_PRICE_PRIVATE_OWNER_PLUS_MONTHLY",
        "STRIPE_PRICE_PRIVATE_OWNER_PLUS_ANNUAL",
        "STRIPE_PRICE_STARTER_BARN_MONTHLY",
        "STRIPE_PRICE_STARTER_BARN_ANNUAL",
        "STRIPE_PRICE_ADVANCED_BARN_MONTHLY",
        "STRIPE_PRICE_ADVANCED_BARN_ANNUAL",
        "STRIPE_PRICE_ELITE_BARN_MONTHLY",
        "STRIPE_PRICE_ELITE_BARN_ANNUAL",
        "STRIPE_PRICE_TRAINER_NO_LESSON_MONTHLY",
        "STRIPE_PRICE_TRAINER_NO_LESSON_ANNUAL",
        "STRIPE_PRICE_TRAINER_LESSON_15_MONTHLY",
        "STRIPE_PRICE_TRAINER_LESSON_15_ANNUAL",
        "STRIPE_PRICE_TRAINER_LESSON_50_MONTHLY",
        "STRIPE_PRICE_TRAINER_LESSON_50_ANNUAL",
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


# Codex finding #3: dev-mode catalog must upsert all pricing-addendum plans even when the
# Stripe key is missing or unreachable.
def test_plans_catalog_contains_all_updated_tiers_even_without_stripe():
    """Local /billing/plans MUST always return the updated pricing catalog,
    regardless of Stripe connectivity. Paid tiers may have null Stripe IDs in
    dev (the `has_monthly`/`has_annual` flags reflect this).
    """
    out = _signup()
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.get(f"{API}/billing/plans", headers=h, timeout=15)
    assert r.status_code == 200
    tiers = {p["tier_code"] for p in r.json()}
    assert tiers == {
        "free",
        "individual_owner",
        "private_owner_plus",
        "service_provider_free",
        "service_provider_premium",
        "starter_barn",
        "advanced_barn",
        "elite_barn",
        "trainer_no_lesson",
        "trainer_lesson_15",
        "trainer_lesson_50",
        "enterprise",
        "community_program",
    }, (
        f"Catalog must always contain the updated pricing tiers in dev (got {tiers})"
    )


# Codex finding #4: origin_url must be allow-listed.
def test_checkout_rejects_unlisted_origin():
    tok, _ = _admin_token()
    h = {"Authorization": f"Bearer {tok}"}
    r = requests.post(
        f"{API}/subscriptions/checkout",
        json={
            "plan_tier_code": "starter_barn",
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
        "plan_tier_code": "starter_barn",
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
    assert sub["plan_tier_code"] == "starter_barn"
    assert sub["status"] == "active"

    # Cleanup
    db.subscriptions.delete_one({"id": sub_id})
    db.barns.delete_one({"id": barn_id})
    client.close()
