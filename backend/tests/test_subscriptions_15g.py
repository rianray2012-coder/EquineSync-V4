"""tests/test_subscriptions_15g.py — Phase 15.G migration cleanup.

Verifies:
  1. /api/billing/plans-public is public, scrubbed, and cached.
  2. /api/subscriptions/checkout {tier:"free"} writes a local subscription
     with no Stripe round-trip and returns {url: null}.
  3. Legacy /api/membership/checkout returns HTTP 410 Gone with a
     non-sensitive pointer payload.
  4. customer.subscription.created and .updated webhook handlers persist
     `amount_cents` from the price's unit_amount.
"""
from __future__ import annotations

import asyncio
import os
import pathlib
import sys
import time
import uuid
from datetime import datetime, timezone

import pytest
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

sys.path.insert(0, "/app/backend")
# Load backend/.env so MONGO_URL/DB_NAME are present when running standalone.
load_dotenv("/app/backend/.env")


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


@pytest.fixture
def db():
    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "test_database"
    c = MongoClient(mongo_url)
    yield c[db_name]
    c.close()


def _signup_user(role: str = "horse_owner") -> dict:
    email = f"g15g_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={
            "email": email,
            "password": "securepass1",
            "full_name": "G15G Test",
            "role": role,
        },
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------
# 1. /billing/plans-public — public, scrubbed, cached
# ---------------------------------------------------------------------
def test_plans_public_no_auth_required():
    r = requests.get(f"{API}/billing/plans-public", timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list) and len(body) >= 3
    tiers = {p["tier_code"] for p in body}
    assert {"free", "starter", "professional"}.issubset(tiers)


def test_plans_public_strips_secrets():
    r = requests.get(f"{API}/billing/plans-public", timeout=10)
    body = r.json()
    for p in body:
        for k in (
            "stripe_price_id_monthly",
            "stripe_price_id_annual",
            "stripe_product_id",
            "has_monthly",
            "has_annual",
        ):
            assert k not in p, f"{p['tier_code']} should not expose {k}"


def test_plans_public_has_cache_header():
    # The Cache-Control header is set at the origin (FastAPI). Some proxy
    # tiers (Cloudflare, ingress) override it for the public preview URL,
    # so we verify at the origin directly. This is the contract the app
    # owns — the edge tier is configurable separately at deploy time.
    r = requests.get("http://localhost:8001/api/billing/plans-public", timeout=10)
    cc = (r.headers.get("Cache-Control") or "").lower()
    assert "public" in cc and "max-age=300" in cc


# ---------------------------------------------------------------------
# 2. Free-tier finalize via /subscriptions/checkout — no Stripe call
# ---------------------------------------------------------------------
def test_free_checkout_writes_local_subscription(db):
    sess = _signup_user("horse_owner")
    token = sess["token"]
    user_id = sess["user"]["id"]
    r = requests.post(
        f"{API}/subscriptions/checkout",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "plan_tier_code": "free",
            "billing_cycle": "monthly",
            "origin_url": "http://localhost:3000",
        },
        timeout=15,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["url"] is None
    assert body["session_id"] is None
    assert body["tier"] == "free"

    # Verify a local Free subscription row exists for this user's barn.
    user = db.users.find_one({"id": user_id})
    assert user is not None
    barn_id = user.get("barn_id")
    assert barn_id is not None
    sub = db.subscriptions.find_one({"barn_id": barn_id, "plan_tier_code": "free"})
    assert sub is not None
    assert sub.get("stripe_subscription_id") is None
    assert sub.get("status") == "active"
    assert sub.get("amount_cents") == 0


def test_free_checkout_no_barn_manage_required():
    """horse_owner has no barn:manage capability — free finalize should
    still succeed because the Phase 15.G charter keeps Free as a solo
    user tier."""
    sess = _signup_user("horse_owner")
    r = requests.post(
        f"{API}/subscriptions/checkout",
        headers={"Authorization": f"Bearer {sess['token']}"},
        json={
            "plan_tier_code": "free",
            "billing_cycle": "monthly",
            "origin_url": "http://localhost:3000",
        },
        timeout=15,
    )
    assert r.status_code == 200


# ---------------------------------------------------------------------
# 3. Legacy /membership/checkout → 410 Gone
# ---------------------------------------------------------------------
def test_legacy_membership_checkout_is_410():
    sess = _signup_user("horse_owner")
    r = requests.post(
        f"{API}/membership/checkout",
        headers={"Authorization": f"Bearer {sess['token']}"},
        json={"tier": "free", "origin_url": "http://localhost:3000"},
        timeout=15,
    )
    assert r.status_code == 410, r.text
    body = r.json()
    detail = body.get("detail")
    # Detail is the structured payload we wrote (FastAPI passes through).
    assert isinstance(detail, dict)
    assert detail.get("code") == "membership_checkout_sunset"
    assert "subscriptions/checkout" in (detail.get("successor") or "")
    assert "no longer available" in (detail.get("message") or "")


def test_legacy_membership_checkout_410_for_paid_tiers_too():
    sess = _signup_user("horse_owner")
    r = requests.post(
        f"{API}/membership/checkout",
        headers={"Authorization": f"Bearer {sess['token']}"},
        json={"tier": "barn_facility", "origin_url": "http://localhost:3000"},
        timeout=15,
    )
    assert r.status_code == 410


# ---------------------------------------------------------------------
# 4. Webhook persists amount_cents for subscription created / updated
# ---------------------------------------------------------------------
def _evt(event_type: str, obj: dict) -> dict:
    return {
        "id": f"evt_15g_{uuid.uuid4().hex[:14]}",
        "type": event_type,
        "created": int(time.time()),
        "data": {"object": obj},
    }


def _post_event(ev: dict):
    return requests.post(f"{API}/webhook/stripe-subscriptions", json=ev, timeout=15)


def test_subscription_created_persists_amount_cents(db):
    barn_id = f"barn_15g_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_15g_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": barn_id, "created_at": datetime.now(timezone.utc).isoformat()})

    # Pull the live starter plan so plan_tier_code resolves an entitlements snapshot.
    obj = {
        "id": sub_id,
        "customer": "cus_test_15g_created",
        "status": "active",
        "current_period_start": int(time.time()),
        "current_period_end": int(time.time()) + 30 * 86400,
        "cancel_at_period_end": False,
        "trial_end": None,
        "metadata": {
            "barn_id": barn_id,
            "owner_user_id": "u_test_owner",
            "plan_tier_code": "starter",
            "billing_cycle": "monthly",
        },
        "items": {"data": [{"price": {"id": "price_test_starter_m", "unit_amount": 4900}}]},
    }
    r = _post_event(_evt("customer.subscription.created", obj))
    assert r.status_code == 200, r.text

    sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
    assert sub is not None
    assert sub.get("amount_cents") == 4900
    assert sub.get("plan_tier_code") == "starter"


def test_subscription_updated_persists_amount_cents(db):
    barn_id = f"barn_15g_u_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_15g_u_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": barn_id, "created_at": datetime.now(timezone.utc).isoformat()})
    db.subscriptions.insert_one({
        "id": sub_id,
        "barn_id": barn_id,
        "stripe_subscription_id": sub_id,
        "plan_tier_code": "starter",
        "status": "active",
        "amount_cents": 4900,
        "stripe_price_id": "price_test_starter_m",
        "billing_cycle": "monthly",
        "pending_emails": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })

    # Simulate a price upgrade Starter → Professional.
    obj = {
        "id": sub_id,
        "customer": "cus_test_15g_updated",
        "status": "active",
        "current_period_start": int(time.time()),
        "current_period_end": int(time.time()) + 30 * 86400,
        "cancel_at_period_end": False,
        "trial_end": None,
        "metadata": {"barn_id": barn_id, "plan_tier_code": "professional"},
        "items": {"data": [{"price": {"id": "price_test_professional_m", "unit_amount": 14900}}]},
    }
    r = _post_event(_evt("customer.subscription.updated", obj))
    assert r.status_code == 200, r.text

    sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
    assert sub is not None
    assert sub.get("amount_cents") == 14900
