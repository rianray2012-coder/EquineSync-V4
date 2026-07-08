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

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
# Load backend/.env so MONGO_URL/DB_NAME are present when running standalone.
load_dotenv(ROOT / "backend" / ".env")


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
    assert {
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
    }.issubset(tiers)


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
        json={"tier": "starter_barn", "origin_url": "http://localhost:3000"},
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

    # Pull the live starter_barn plan so plan_tier_code resolves an entitlements snapshot.
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
            "plan_tier_code": "starter_barn",
            "billing_cycle": "monthly",
        },
        "items": {"data": [{"price": {"id": "price_test_starter_barn_m", "unit_amount": 6999}}]},
    }
    r = _post_event(_evt("customer.subscription.created", obj))
    assert r.status_code == 200, r.text

    sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
    assert sub is not None
    assert sub.get("amount_cents") == 6999
    assert sub.get("plan_tier_code") == "starter_barn"


def test_subscription_updated_persists_amount_cents(db):
    barn_id = f"barn_15g_u_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_15g_u_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": barn_id, "created_at": datetime.now(timezone.utc).isoformat()})
    db.subscriptions.insert_one({
        "id": sub_id,
        "barn_id": barn_id,
        "stripe_subscription_id": sub_id,
        "plan_tier_code": "starter_barn",
        "status": "active",
        "amount_cents": 6999,
        "stripe_price_id": "price_test_starter_barn_m",
        "billing_cycle": "monthly",
        "pending_emails": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })

    # Simulate a price upgrade Starter Barn → Advanced Barn.
    obj = {
        "id": sub_id,
        "customer": "cus_test_15g_updated",
        "status": "active",
        "current_period_start": int(time.time()),
        "current_period_end": int(time.time()) + 30 * 86400,
        "cancel_at_period_end": False,
        "trial_end": None,
        "metadata": {"barn_id": barn_id, "plan_tier_code": "advanced_barn"},
        "items": {"data": [{"price": {"id": "price_test_advanced_barn_m", "unit_amount": 14999}}]},
    }
    r = _post_event(_evt("customer.subscription.updated", obj))
    assert r.status_code == 200, r.text

    sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
    assert sub is not None
    assert sub.get("amount_cents") == 14999



# ---------------------------------------------------------------------
# Round-2 blockers (Codex review)
# ---------------------------------------------------------------------
def test_legacy_membership_checkout_status_is_410():
    """Codex round-2 blocker #1: the legacy status polling endpoint must
    also return 410 — pre-15.G it ran the old polling + user-flip logic.
    """
    sess = _signup_user("horse_owner")
    r = requests.get(
        f"{API}/membership/checkout/status/cs_test_sessfake",
        headers={"Authorization": f"Bearer {sess['token']}"},
        timeout=15,
    )
    assert r.status_code == 410, r.text
    detail = (r.json() or {}).get("detail") or {}
    assert isinstance(detail, dict)
    assert detail.get("code") == "membership_checkout_status_sunset"
    assert "subscriptions/me" in (detail.get("successor") or "")


def test_free_checkout_visible_via_subscriptions_me():
    """Codex round-2 blocker #2: finalizing Free must produce a row that
    `/api/subscriptions/me` actually returns. Previously the row was
    written but barn.subscription_id was never stamped, so /me returned
    null.
    """
    sess = _signup_user("horse_owner")
    h = {"Authorization": f"Bearer {sess['token']}"}
    r = requests.post(
        f"{API}/subscriptions/checkout",
        headers=h,
        json={
            "plan_tier_code": "free",
            "billing_cycle": "monthly",
            "origin_url": "http://localhost:3000",
        },
        timeout=15,
    )
    assert r.status_code == 200, r.text

    me = requests.get(f"{API}/subscriptions/me", headers=h, timeout=15)
    assert me.status_code == 200, me.text
    body = me.json()
    sub = body.get("subscription")
    assert sub is not None, "Free subscription must be visible via /subscriptions/me"
    assert sub.get("plan_tier_code") == "free"
    assert sub.get("status") == "active"
    assert sub.get("amount_cents") == 0


def test_subscription_updated_amount_cents_not_overwritten_when_missing(db):
    """Codex round-2 should-fix: an update event WITHOUT
    items[0].price.unit_amount must NOT overwrite an existing nonzero
    amount_cents with 0 (defensive revenue-reporting guarantee).
    """
    barn_id = f"barn_15g_def_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_15g_def_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": barn_id, "created_at": datetime.now(timezone.utc).isoformat()})
    db.subscriptions.insert_one({
        "id": sub_id,
        "barn_id": barn_id,
        "stripe_subscription_id": sub_id,
        "plan_tier_code": "starter_barn",
        "status": "active",
        "amount_cents": 6999,  # pre-existing known value
        "stripe_price_id": "price_test_starter_barn_m",
        "billing_cycle": "monthly",
        "pending_emails": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })

    # Event with no unit_amount (defensive shape).
    obj = {
        "id": sub_id,
        "customer": "cus_test_15g_defensive",
        "status": "active",
        "current_period_start": int(time.time()),
        "current_period_end": int(time.time()) + 30 * 86400,
        "cancel_at_period_end": False,
        "trial_end": None,
        "metadata": {"barn_id": barn_id, "plan_tier_code": "starter_barn"},
        "items": {"data": [{"price": {"id": "price_test_starter_barn_m"}}]},  # NO unit_amount
    }
    r = _post_event(_evt("customer.subscription.updated", obj))
    assert r.status_code == 200, r.text

    sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
    assert sub is not None
    assert sub.get("amount_cents") == 6999, "amount_cents must NOT be overwritten with 0"



# ---------------------------------------------------------------------
# Round-2 blocker #3 — Landing must not fall back to static prices
# ---------------------------------------------------------------------
def test_landing_jsx_has_no_static_plan_prices():
    """Codex round-2 blocker #3: confirm Landing.jsx no longer contains
    a static plan catalog (full plan rows with monthly_price_cents). The
    file may keep bullet-only marketing copy keyed by tier_code, but
    must source prices, names, and descriptions from
    /api/billing/plans-public exclusively.
    """
    landing = (ROOT / "frontend" / "src" / "pages" / "Landing.jsx").read_text()
    # The retired fallback name must no longer appear (defense-in-depth
    # against drift if someone re-introduces a static catalog).
    assert "LANDING_PLANS_FALLBACK" not in landing
    # No hard-coded `monthly_price_cents:` literals (the field name only
    # appears as derived data through props).
    assert "monthly_price_cents:" not in landing
    assert "annual_price_cents:" not in landing
    # Confirms the public endpoint is the source of truth.
    assert "/billing/plans-public" in landing


def test_landing_jsx_exposes_graceful_unavailable_state():
    """Landing should expose a pricing-unavailable test id so the
    operational team has a way to detect the error fallback (no static
    prices) during synthetic monitoring.
    """
    landing = (ROOT / "frontend" / "src" / "pages" / "Landing.jsx").read_text()
    assert "pricing-unavailable" in landing
    assert "pricing-loading" in landing
    assert "pricing-grid" in landing


def test_landing_jsx_hides_legacy_pricing_options():
    """The public homepage must not display retired Starter/Professional
    options, but it must keep the new barn-size and trainer catalog tiers.
    """
    landing = (ROOT / "frontend" / "src" / "pages" / "Landing.jsx").read_text()
    assert "HIDDEN_LANDING_PRICING_TIERS" in landing
    assert '"starter"' in landing
    assert '"professional"' in landing
    hidden_section = landing.split("const HIDDEN_LANDING_PRICING_TIERS", 1)[1].split("]);", 1)[0]
    assert '"starter_barn"' not in hidden_section
    assert '"advanced_barn"' not in hidden_section
    assert '"trainer_no_lesson"' not in hidden_section
    assert '"trainer_lesson_15"' not in hidden_section
    assert '"trainer_lesson_50"' not in hidden_section
    assert "!HIDDEN_LANDING_PRICING_TIERS.has(plan.tier_code)" in landing


def test_landing_jsx_private_owner_plus_uses_additional_profile_copy():
    """Private Owner Plus must advertise one additional profile, not staff seats."""
    landing = (ROOT / "frontend" / "src" / "pages" / "Landing.jsx").read_text()
    assert 'plan.tier_code === "private_owner_plus"' in landing
    assert "Includes everything in Individual Horse Owner" in landing
    assert "one additional profile and private-owner tools" in landing
    assert 'parts.push("1 additional profile")' in landing
    assert "staff user" not in landing


def test_landing_jsx_exposes_service_provider_pricing_and_cta_path():
    """The homepage pricing band must include free and premium provider options."""
    landing = (ROOT / "frontend" / "src" / "pages" / "Landing.jsx").read_text()
    assert "service_provider_free" in landing
    assert "service_provider_premium" in landing
    assert "Basic horse info, calendar and appointment scheduling" in landing
    assert "$15/month premium provider subscription" in landing
    assert 'startsWith("service_provider")' in landing


def test_landing_role_cards_do_not_show_verification_required_badges():
    """Public role-photo cards should not scare visitors with unclear verification language."""
    landing = (ROOT / "frontend" / "src" / "pages" / "Landing.jsx").read_text()
    assert "Verification required" not in landing
    assert "card.pending" not in landing


def test_shared_logo_links_to_home():
    """The shared brand mark should behave as a home link on every page using Logo."""
    logo = (ROOT / "frontend" / "src" / "components" / "Logo.jsx").read_text()
    assert 'import { Link } from "react-router-dom";' in logo
    assert 'linkTo = "/"' in logo
    assert 'to: linkTo' in logo
    assert 'aria-label": "Equine Sync home"' in logo
    assert 'data-testid={linkTo ? "logo-home-link" : "logo"}' in logo


def test_landing_footer_uses_founder_equestrian_positioning():
    """Footer copy should signal lived equestrian context without generic marketing filler."""
    landing = (ROOT / "frontend" / "src" / "pages" / "Landing.jsx").read_text()
    assert "Crafted for the equestrian world" not in landing
    assert "Built by horse owners and equestrians" in landing
    assert "people and facilities who care for horses" in landing


def test_signup_jsx_defaults_service_provider_to_provider_free_plan():
    """Service-provider signup must not borrow the invited-owner free tier."""
    signup = (ROOT / "frontend" / "src" / "pages" / "Signup.jsx").read_text()
    assert 'service_provider: "service_provider_free"' in signup
    assert 'new Set(["free", "service_provider_free"])' in signup
    assert 'plan_tier_code: tier' in signup
    assert "Start Service Provider Free" in signup
