"""tests/test_marketplace_signup.py — public marketplace signup + Stripe flow.

Tightly scoped to the new /auth/signup endpoint and /membership/* routes.
Does NOT touch /auth/register (Security Patch 2E still owns that).
"""
from __future__ import annotations

import os
import pathlib
import time

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


def _payload(role: str, *, tier: str | None = None, profile: dict | None = None):
    return {
        "email": f"mkt_{role}_{time.time_ns()}@test.com",
        "password": "marketpass1",
        "full_name": f"Mkt {role}",
        "role": role,
        "phone": "555-0100",
        "location": "Lexington, KY",
        "tier": tier or "free",
        "profile": profile or {},
    }


def test_tier_catalog_public():
    r = requests.get(f"{API}/membership/tiers", timeout=10)
    assert r.status_code == 200, r.text
    tiers = {t["id"]: t for t in r.json()}
    assert {"free", "owner_rider", "trainer_provider", "barn_facility"} <= set(tiers)
    assert tiers["free"]["amount"] == 0.0
    assert tiers["owner_rider"]["amount"] == 15.0
    assert tiers["trainer_provider"]["amount"] == 49.0
    assert tiers["barn_facility"]["amount"] == 149.0


def test_signup_horse_owner_active():
    r = requests.post(f"{API}/auth/signup", json=_payload("horse_owner"), timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    u = body["user"]
    assert u["role"] == "horse_owner"
    assert u["role_status"] == "active"
    assert body.get("token")  # session issued under default enforce=off


def test_signup_rider_active():
    r = requests.post(f"{API}/auth/signup", json=_payload("rider"), timeout=15)
    assert r.status_code == 200, r.text
    assert r.json()["user"]["role_status"] == "active"


def test_signup_trainer_pending_review():
    r = requests.post(f"{API}/auth/signup", json=_payload("trainer"), timeout=15)
    assert r.status_code == 200, r.text
    assert r.json()["user"]["role_status"] == "pending_review"


def test_signup_barn_owner_pending_review():
    r = requests.post(f"{API}/auth/signup", json=_payload("barn_owner"), timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user"]["role_status"] == "pending_review"
    assert body.get("token")  # still issued — banner UX, not blocked


def test_signup_service_provider_pending_review():
    r = requests.post(f"{API}/auth/signup", json=_payload("service_provider"), timeout=15)
    assert r.status_code == 200, r.text
    assert r.json()["user"]["role_status"] == "pending_review"


def test_signup_rejects_unknown_role():
    p = _payload("rider")
    p["role"] = "admin"  # NOT in marketplace whitelist
    r = requests.post(f"{API}/auth/signup", json=p, timeout=15)
    assert r.status_code == 400, r.text


def test_signup_rejects_short_password():
    p = _payload("rider")
    p["password"] = "short"
    r = requests.post(f"{API}/auth/signup", json=p, timeout=15)
    assert r.status_code == 400, r.text


def test_signup_rejects_duplicate_email():
    p = _payload("rider")
    a = requests.post(f"{API}/auth/signup", json=p, timeout=15)
    assert a.status_code == 200
    b = requests.post(f"{API}/auth/signup", json=p, timeout=15)
    assert b.status_code == 400, b.text


def test_register_endpoint_still_role_locked():
    """Security Patch 2E invariant: /auth/register must NOT honor a privileged role."""
    payload = {
        "email": f"locked_{time.time_ns()}@test.com",
        "password": "lockedpass1",
        "full_name": "Locked",
        "role": "admin",
    }
    r = requests.post(f"{API}/auth/register", json=payload, timeout=15)
    assert r.status_code == 200, r.text
    assert r.json()["user"]["role"] == "horse_owner"  # forced


def test_checkout_free_flips_subscription_status():
    p = _payload("horse_owner", tier="free")
    r = requests.post(f"{API}/auth/signup", json=p, timeout=15)
    assert r.status_code == 200
    token = r.json()["token"]
    h = {"Authorization": f"Bearer {token}"}
    r2 = requests.post(
        f"{API}/membership/checkout",
        json={"tier": "free", "origin_url": BASE},
        headers=h, timeout=15,
    )
    assert r2.status_code == 200, r2.text
    body = r2.json()
    assert body["url"] is None
    assert body["status"] == "free"
    # /auth/me reflects free subscription_status
    me = requests.get(f"{API}/auth/me", headers=h, timeout=15)
    assert me.status_code == 200
    assert me.json().get("subscription_status") == "free"


def test_checkout_paid_returns_stripe_url():
    p = _payload("horse_owner", tier="owner_rider")
    r = requests.post(f"{API}/auth/signup", json=p, timeout=15)
    assert r.status_code == 200
    token = r.json()["token"]
    h = {"Authorization": f"Bearer {token}"}
    r2 = requests.post(
        f"{API}/membership/checkout",
        json={"tier": "owner_rider", "origin_url": BASE},
        headers=h, timeout=20,
    )
    assert r2.status_code == 200, r2.text
    body = r2.json()
    assert body["url"] and body["url"].startswith("https://checkout.stripe.com/")
    assert body["session_id"]
    assert body["tier"] == "owner_rider"
    assert body["amount"] == 15.0


def test_checkout_rejects_invalid_tier():
    p = _payload("rider")
    r = requests.post(f"{API}/auth/signup", json=p, timeout=15)
    token = r.json()["token"]
    h = {"Authorization": f"Bearer {token}"}
    bad = requests.post(
        f"{API}/membership/checkout",
        json={"tier": "platinum", "origin_url": BASE},
        headers=h, timeout=10,
    )
    assert bad.status_code == 400


def test_checkout_status_blocks_other_users_session():
    # User A creates a session, user B can't poll it.
    a = requests.post(f"{API}/auth/signup", json=_payload("horse_owner"), timeout=15).json()
    b = requests.post(f"{API}/auth/signup", json=_payload("rider"), timeout=15).json()
    ha = {"Authorization": f"Bearer {a['token']}"}
    hb = {"Authorization": f"Bearer {b['token']}"}
    co = requests.post(
        f"{API}/membership/checkout",
        json={"tier": "owner_rider", "origin_url": BASE},
        headers=ha, timeout=15,
    ).json()
    r = requests.get(
        f"{API}/membership/checkout/status/{co['session_id']}",
        headers=hb, timeout=15,
    )
    assert r.status_code == 403, r.text
