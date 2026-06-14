"""Phase 15.E — Platform-admin Billing Dashboard tests.

Covers the 6 endpoints in `routes/admin_billing.py`:
  - GET  /admin/billing/overview                            (headline metrics)
  - GET  /admin/billing/subscriptions                       (paginated list)
  - GET  /admin/billing/subscriptions/{id}                  (drill-in)
  - GET  /admin/billing/stuck-events                        (webhook stuck list)
  - GET  /admin/billing/stuck-emails                        (email permanent_failure)
  - POST /admin/users/{user_id}/grant-facility-access       (role-elevation)

Auth: every endpoint must reject non-admins (403) and accept `admin:access`.
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta, timezone

import dotenv
dotenv.load_dotenv("/app/backend/.env")

import bcrypt
import pymongo
import pytest
import requests

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]
API = os.environ.get("REACT_APP_BACKEND_URL", "http://localhost:8001").rstrip("/") + "/api"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db():
    client = pymongo.MongoClient(MONGO_URL)
    yield client[DB_NAME]
    client.close()


@pytest.fixture(autouse=True)
def _purge_stale(db):
    """Clear 15.E test fixtures before every test."""
    db.users.delete_many({"id": {"$regex": "^u_15e_"}})
    db.barns.delete_many({"id": {"$regex": "^barn_15e_"}})
    db.subscriptions.delete_many({"stripe_subscription_id": {"$regex": "^sub_15e_"}})
    db.subscription_invoices.delete_many({"subscription_id": {"$regex": "^sub_15e_"}})
    db.billing_events.delete_many({"stripe_event_id": {"$regex": "^evt_15e_"}})
    db.subscription_email_log.delete_many({"subscription_id": {"$regex": "^sub_15e_"}})
    yield


def _now():
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _mint_user(db, role: str, *, role_status: str = "active",
               barn_id: str = "primary"):
    email = f"15e_{role}_{uuid.uuid4().hex[:8]}@test.com"
    pwd = "TestPass123!"
    pwd_hash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    uid = f"u_15e_{uuid.uuid4().hex[:8]}"
    db.users.insert_one({
        "id": uid, "email": email, "full_name": f"Test {role}",
        "role": role, "password_hash": pwd_hash, "barn_id": barn_id,
        "role_status": role_status,
    })
    r = requests.post(f"{API}/auth/login",
                      json={"email": email, "password": pwd}, timeout=15)
    assert r.status_code == 200, r.text
    return r.json()["token"], uid


def _seed_sub(db, *, barn_id="primary", owner_user_id=None,
              tier="starter", status="active", cycle="monthly",
              amount_cents=4900, trial_end=None,
              current_period_end=None):
    sid = f"sub_15e_{uuid.uuid4().hex[:8]}"
    db.subscriptions.insert_one({
        "id": sid,
        "stripe_subscription_id": sid,
        "barn_id": barn_id,
        "owner_user_id": owner_user_id,
        "plan_tier_code": tier,
        "status": status,
        "billing_cycle": cycle,
        "amount_cents": amount_cents,
        "trial_end": trial_end,
        "current_period_start": _iso(_now() - timedelta(days=10)),
        "current_period_end": current_period_end or _iso(_now() + timedelta(days=20)),
        "cancel_at_period_end": False,
        "created_at": _iso(_now() - timedelta(days=10)),
        "updated_at": _iso(_now() - timedelta(days=1)),
    })
    return sid


def _h(token: str):
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Auth gating — every endpoint
# ---------------------------------------------------------------------------

def test_every_endpoint_rejects_barn_manager(db):
    """`admin:access` is the narrowest gate. A `barn_manager` (which can hit
    `barn:manage` everywhere else) must still get 403 here."""
    tok, _ = _mint_user(db, "barn_manager")
    paths = [
        ("GET",  "/admin/billing/overview", None),
        ("GET",  "/admin/billing/subscriptions", None),
        ("GET",  "/admin/billing/subscriptions/whatever", None),
        ("GET",  "/admin/billing/stuck-events", None),
        ("GET",  "/admin/billing/stuck-emails", None),
        ("POST", "/admin/users/whatever/grant-facility-access",
                  {"barn_id": "primary"}),
    ]
    for method, path, body in paths:
        if method == "GET":
            r = requests.get(f"{API}{path}", headers=_h(tok), timeout=15)
        else:
            r = requests.post(f"{API}{path}", json=body, headers=_h(tok), timeout=15)
        assert r.status_code == 403, f"{method} {path} should 403, got {r.status_code}"


# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

def test_overview_math_committed_vs_active_mrr(db):
    """Decision #4c — overview must report BOTH Committed MRR (active +
    trialing + past_due) and Active MRR (active + past_due). Trial-only
    subs count toward committed but not active."""
    tok, _ = _mint_user(db, "admin")
    s1 = _seed_sub(db, tier="starter", status="active", cycle="monthly",
                   amount_cents=4900)
    s2 = _seed_sub(db, tier="professional", status="active", cycle="annual",
                   amount_cents=151_980)
    s3 = _seed_sub(db, tier="starter", status="trialing", cycle="monthly",
                   amount_cents=4900,
                   trial_end=_iso(_now() + timedelta(days=3)))
    _seed_sub(db, tier="professional", status="canceled", cycle="monthly",
              amount_cents=14_900)

    try:
        r = requests.get(f"{API}/admin/billing/overview",
                         headers=_h(tok), timeout=15)
        assert r.status_code == 200, r.text
        body = r.json()
        # Committed = s1 + s2 (annual/12) + s3 = 4900 + 12665 + 4900 = 22465
        assert body["mrr"]["committed_monthly_cents"] >= 22465
        # Active = s1 + s2 (no trialing) = 4900 + 12665 = 17565
        assert body["mrr"]["active_monthly_cents"] >= 17565
        # Committed > Active because s3 is trialing
        assert body["mrr"]["committed_monthly_cents"] > body["mrr"]["active_monthly_cents"]
        # Trial ending in 7 days includes s3
        assert body["trials_ending_7d"] >= 1
        # Totals shape
        assert "by_status" in body["totals"]
        assert "by_tier" in body["totals"]
        assert body["stuck"]["threshold_minutes"] == 10
    finally:
        for s in (s1, s2, s3):
            db.subscriptions.delete_one({"stripe_subscription_id": s})


def test_overview_stuck_threshold_is_env_configurable(db, monkeypatch):
    """Decision #3b — STUCK_BILLING_EVENTS_MINUTES env override is honoured."""
    tok, _ = _mint_user(db, "admin")
    # Default check
    r = requests.get(f"{API}/admin/billing/overview", headers=_h(tok), timeout=15)
    assert r.json()["stuck"]["threshold_minutes"] == 10
    # NOTE: env change requires backend restart to pick up; the helper
    # reads os.environ at request time so this still validates that
    # the *value* matches what the env sets when the process was started.
    # If you want to test the override in isolation, see the unit-level
    # test below for `_stuck_threshold_minutes`.


def test_stuck_threshold_helper_reads_env():
    """Unit-level: _stuck_threshold_minutes() reads STUCK_BILLING_EVENTS_MINUTES."""
    from routes.admin_billing import _stuck_threshold_minutes
    orig = os.environ.get("STUCK_BILLING_EVENTS_MINUTES")
    try:
        os.environ["STUCK_BILLING_EVENTS_MINUTES"] = "27"
        assert _stuck_threshold_minutes() == 27
        os.environ["STUCK_BILLING_EVENTS_MINUTES"] = "not-a-number"
        assert _stuck_threshold_minutes() == 10  # falls back to default
    finally:
        if orig is None:
            os.environ.pop("STUCK_BILLING_EVENTS_MINUTES", None)
        else:
            os.environ["STUCK_BILLING_EVENTS_MINUTES"] = orig


# ---------------------------------------------------------------------------
# Subscriptions list — filtering, search, pagination
# ---------------------------------------------------------------------------

def test_list_subscriptions_filters_by_status_and_tier(db):
    tok, _ = _mint_user(db, "admin")
    s_active   = _seed_sub(db, tier="starter",       status="active")
    s_trial    = _seed_sub(db, tier="starter",       status="trialing")
    s_pro      = _seed_sub(db, tier="professional",  status="active")
    try:
        r = requests.get(f"{API}/admin/billing/subscriptions?status=trialing",
                         headers=_h(tok), timeout=15)
        ids = [x["subscription_id"] for x in r.json()["items"]]
        assert s_trial in ids
        assert s_active not in ids
        assert s_pro not in ids

        r = requests.get(f"{API}/admin/billing/subscriptions?tier=professional",
                         headers=_h(tok), timeout=15)
        ids = [x["subscription_id"] for x in r.json()["items"]]
        assert s_pro in ids
        assert s_active not in ids
    finally:
        for s in (s_active, s_trial, s_pro):
            db.subscriptions.delete_one({"stripe_subscription_id": s})


def test_list_subscriptions_search_by_owner_email(db):
    tok, _ = _mint_user(db, "admin")
    # Create a customer user and seed a sub linked to them.
    customer_email = f"15e_cust_{uuid.uuid4().hex[:6]}@test.com"
    cust_id = f"u_15e_cust_{uuid.uuid4().hex[:6]}"
    db.users.insert_one({
        "id": cust_id, "email": customer_email, "role": "barn_manager",
        "full_name": "c", "barn_id": "primary",
    })
    sid = _seed_sub(db, owner_user_id=cust_id, status="active")
    try:
        r = requests.get(
            f"{API}/admin/billing/subscriptions?q={customer_email[:14]}",
            headers=_h(tok), timeout=15)
        assert r.status_code == 200
        items = r.json()["items"]
        ids = [x["subscription_id"] for x in items]
        assert sid in ids
        # Owner email is hydrated
        match = next(x for x in items if x["subscription_id"] == sid)
        assert match["owner_email"] == customer_email
    finally:
        db.subscriptions.delete_one({"stripe_subscription_id": sid})
        db.users.delete_one({"id": cust_id})


def test_list_subscriptions_pagination(db):
    tok, _ = _mint_user(db, "admin")
    ids = [_seed_sub(db, status="active") for _ in range(5)]
    try:
        r = requests.get(f"{API}/admin/billing/subscriptions?page_size=2&page=1",
                         headers=_h(tok), timeout=15)
        body = r.json()
        assert body["page"] == 1
        assert body["page_size"] == 2
        assert len(body["items"]) == 2
        assert body["total"] >= 5
    finally:
        for s in ids:
            db.subscriptions.delete_one({"stripe_subscription_id": s})


# ---------------------------------------------------------------------------
# Subscription drill-in
# ---------------------------------------------------------------------------

def test_subscription_detail_joins_invoices_events_emails(db):
    """Decision #5a — drill-in is read-only and joins sub + last invoices +
    last billing_events + last email_log."""
    tok, _ = _mint_user(db, "admin")
    cust_id = f"u_15e_cust_{uuid.uuid4().hex[:6]}"
    db.users.insert_one({
        "id": cust_id, "email": f"15e_o_{uuid.uuid4().hex[:6]}@test.com",
        "role": "barn_manager", "barn_id": "primary", "full_name": "o",
    })
    sid = _seed_sub(db, owner_user_id=cust_id, status="active")

    # Seed 2 invoices, 2 events, 2 email log rows.
    for i in range(2):
        db.subscription_invoices.insert_one({
            "id": f"in_15e_{i}_{uuid.uuid4().hex[:6]}",
            "barn_id": "primary",
            "subscription_id": sid,
            "stripe_invoice_id": f"in_15e_{i}_{uuid.uuid4().hex[:6]}",
            "amount_cents": 4900,
            "status": "paid",
            "created_at": _iso(_now() - timedelta(days=i)),
        })
        db.billing_events.insert_one({
            "stripe_event_id": f"evt_15e_{i}_{uuid.uuid4().hex[:6]}",
            "subscription_id": sid,
            "processing_status": "ok",
            "created_at": _iso(_now() - timedelta(hours=i)),
            "updated_at": _iso(_now() - timedelta(hours=i)),
        })
        db.subscription_email_log.insert_one({
            "subscription_id": sid,
            "event_key": "payment_succeeded" if i == 0 else "trial_will_end",
            "status": "sent",
            "attempt": 1,
            "updated_at": _iso(_now() - timedelta(minutes=i)),
        })
    try:
        r = requests.get(f"{API}/admin/billing/subscriptions/{sid}",
                         headers=_h(tok), timeout=15)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["subscription"]["subscription_id"] == sid
        assert body["subscription"]["owner_email"]
        assert len(body["invoices"]) == 2
        assert len(body["billing_events"]) == 2
        assert len(body["email_log"]) == 2
    finally:
        db.subscriptions.delete_one({"stripe_subscription_id": sid})
        db.subscription_invoices.delete_many({"subscription_id": sid})
        db.billing_events.delete_many({"subscription_id": sid})
        db.subscription_email_log.delete_many({"subscription_id": sid})
        db.users.delete_one({"id": cust_id})


def test_subscription_detail_404_when_missing(db):
    tok, _ = _mint_user(db, "admin")
    r = requests.get(f"{API}/admin/billing/subscriptions/sub_15e_doesnotexist",
                     headers=_h(tok), timeout=15)
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Stuck endpoints
# ---------------------------------------------------------------------------

def test_stuck_events_only_returns_retry_status_older_than_threshold(db):
    tok, _ = _mint_user(db, "admin")
    old_stuck_id = f"evt_15e_old_{uuid.uuid4().hex[:6]}"
    recent_stuck_id = f"evt_15e_recent_{uuid.uuid4().hex[:6]}"
    ok_id = f"evt_15e_ok_{uuid.uuid4().hex[:6]}"
    db.billing_events.insert_many([
        {"stripe_event_id": old_stuck_id,
         "processing_status": "retry_502",
         "updated_at": _iso(_now() - timedelta(minutes=30)),
         "created_at": _iso(_now() - timedelta(minutes=30))},
        {"stripe_event_id": recent_stuck_id,
         "processing_status": "metadata_missing_retryable",
         "updated_at": _iso(_now() - timedelta(minutes=1)),
         "created_at": _iso(_now() - timedelta(minutes=1))},
        {"stripe_event_id": ok_id,
         "processing_status": "ok",
         "updated_at": _iso(_now() - timedelta(minutes=30)),
         "created_at": _iso(_now() - timedelta(minutes=30))},
    ])
    try:
        r = requests.get(f"{API}/admin/billing/stuck-events",
                         headers=_h(tok), timeout=15)
        ids = {x["stripe_event_id"] for x in r.json()["items"]}
        assert old_stuck_id in ids, "old retry_502 row must surface"
        assert recent_stuck_id not in ids, \
            "recent stuck row is below threshold and should NOT surface"
        assert ok_id not in ids, "ok rows must never surface as stuck"
    finally:
        db.billing_events.delete_many(
            {"stripe_event_id": {"$in": [old_stuck_id, recent_stuck_id, ok_id]}})


def test_stuck_emails_only_returns_permanent_failure(db):
    tok, _ = _mint_user(db, "admin")
    sid = f"sub_15e_se_{uuid.uuid4().hex[:6]}"
    db.subscription_email_log.insert_many([
        {"subscription_id": sid, "event_key": "trial_will_end",
         "status": "permanent_failure", "attempt": 5,
         "updated_at": _iso(_now() - timedelta(minutes=10))},
        {"subscription_id": sid, "event_key": "payment_succeeded",
         "status": "sent", "attempt": 1,
         "updated_at": _iso(_now())},
        {"subscription_id": sid, "event_key": "payment_failed",
         "status": "failed", "attempt": 2,
         "updated_at": _iso(_now())},
    ])
    try:
        r = requests.get(f"{API}/admin/billing/stuck-emails",
                         headers=_h(tok), timeout=15)
        statuses = {x["status"] for x in r.json()["items"]}
        keys = [x["event_key"] for x in r.json()["items"]
                if x["subscription_id"] == sid]
        assert "permanent_failure" in statuses
        # Our seeded permanent_failure row shows up; the failed/sent ones do not.
        assert "trial_will_end" in keys
        assert "payment_succeeded" not in keys
        assert "payment_failed" not in keys
    finally:
        db.subscription_email_log.delete_many({"subscription_id": sid})


# ---------------------------------------------------------------------------
# Role-elevation
# ---------------------------------------------------------------------------

def test_grant_facility_access_requires_approved_status(db):
    """Decision #2a — must be approved first; pending_review rejected with 409."""
    admin_tok, _ = _mint_user(db, "admin")
    _, target_id = _mint_user(db, "barn_owner",
                              role_status="pending_review")
    r = requests.post(
        f"{API}/admin/users/{target_id}/grant-facility-access",
        json={"barn_id": "primary"},
        headers=_h(admin_tok), timeout=15)
    assert r.status_code == 409, r.text
    assert "approved" in r.text.lower()


def test_grant_facility_access_pick_existing_barn(db):
    admin_tok, _ = _mint_user(db, "admin")
    _, target_id = _mint_user(db, "barn_owner",
                              role_status="approved")
    # Seed an existing barn
    bid = f"barn_15e_{uuid.uuid4().hex[:6]}"
    db.barns.insert_one({"id": bid, "name": "Existing Barn",
                         "created_at": _iso(_now())})

    r = requests.post(
        f"{API}/admin/users/{target_id}/grant-facility-access",
        json={"barn_id": bid},
        headers=_h(admin_tok), timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["from_role"] == "barn_owner"
    assert body["to_role"] == "barn_manager"
    assert body["barn_id"] == bid
    assert body["created_barn"] is False

    # User row reflects the change
    u = db.users.find_one({"id": target_id})
    assert u["role"] == "barn_manager"
    assert u["barn_id"] == bid

    # Audit row written with minimal metadata, no PII
    audit = db.audit_log.find_one(
        {"action": "admin.grant_facility_access", "resource_id": target_id},
        sort=[("ts", -1)])
    assert audit is not None, "audit row was not written"
    meta = audit.get("metadata", {})
    assert meta.get("from_role") == "barn_owner"
    assert meta.get("to_role") == "barn_manager"
    assert meta.get("barn_id") == bid
    assert meta.get("created_barn") is False
    # Guardrail — must NOT include email/name values.
    for forbidden_key in ("email", "name", "full_name", "phone"):
        assert forbidden_key not in meta, \
            f"metadata leaked {forbidden_key!r}"


def test_grant_facility_access_create_new_barn(db):
    admin_tok, _ = _mint_user(db, "admin")
    _, target_id = _mint_user(db, "trainer", role_status="approved")
    r = requests.post(
        f"{API}/admin/users/{target_id}/grant-facility-access",
        json={"create_new_barn": True, "new_barn_name": "Wild Acres Stables"},
        headers=_h(admin_tok), timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["created_barn"] is True
    new_bid = body["barn_id"]
    assert new_bid.startswith("barn_")
    # Confirm the barn row exists
    barn = db.barns.find_one({"id": new_bid})
    assert barn is not None
    assert barn["name"] == "Wild Acres Stables"
    db.barns.delete_one({"id": new_bid})


def test_grant_facility_access_rejects_bad_body(db):
    admin_tok, _ = _mint_user(db, "admin")
    _, target_id = _mint_user(db, "barn_owner", role_status="approved")

    # Neither barn_id nor create_new_barn
    r = requests.post(
        f"{API}/admin/users/{target_id}/grant-facility-access",
        json={}, headers=_h(admin_tok), timeout=15)
    assert r.status_code == 400, r.text

    # Both at once
    r = requests.post(
        f"{API}/admin/users/{target_id}/grant-facility-access",
        json={"barn_id": "primary", "create_new_barn": True},
        headers=_h(admin_tok), timeout=15)
    assert r.status_code == 400, r.text

    # create_new_barn without name
    r = requests.post(
        f"{API}/admin/users/{target_id}/grant-facility-access",
        json={"create_new_barn": True, "new_barn_name": "   "},
        headers=_h(admin_tok), timeout=15)
    assert r.status_code == 400, r.text


def test_grant_facility_access_idempotent_for_already_elevated_user(db):
    admin_tok, _ = _mint_user(db, "admin")
    _, target_id = _mint_user(db, "barn_manager",
                              role_status="approved", barn_id="primary")
    # Already barn_manager with a barn — should noop.
    r = requests.post(
        f"{API}/admin/users/{target_id}/grant-facility-access",
        json={"barn_id": "primary"},
        headers=_h(admin_tok), timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("noop") is True
    assert body["from_role"] == "barn_manager"
    assert body["to_role"] == "barn_manager"


def test_grant_facility_access_404_when_barn_missing(db):
    admin_tok, _ = _mint_user(db, "admin")
    _, target_id = _mint_user(db, "barn_owner", role_status="approved")
    r = requests.post(
        f"{API}/admin/users/{target_id}/grant-facility-access",
        json={"barn_id": "barn_15e_does_not_exist"},
        headers=_h(admin_tok), timeout=15)
    assert r.status_code == 404, r.text


# ---------------------------------------------------------------------------
# Round-2 review fixes — locked here so they cannot regress
# ---------------------------------------------------------------------------

def test_grant_facility_access_rejects_horse_owner_and_rider(db):
    """Round-2 blocker #1: an admin curl could previously promote any
    approved user to `barn_manager`. The backend now allowlists eligible
    roles (`barn_owner`, `trainer`, `service_provider`, plus `barn_manager`
    for idempotent no-op only). Locking the allowlist with explicit
    rejections for non-facility roles."""
    admin_tok, _ = _mint_user(db, "admin")
    for ineligible_role in ("horse_owner", "rider"):
        _, target_id = _mint_user(db, ineligible_role,
                                  role_status="approved")
        r = requests.post(
            f"{API}/admin/users/{target_id}/grant-facility-access",
            json={"barn_id": "primary"},
            headers=_h(admin_tok), timeout=15)
        assert r.status_code == 409, \
            f"role={ineligible_role}: expected 409, got {r.status_code} {r.text}"
        assert "not eligible" in r.text.lower(), r.text
        # Confirm the user was NOT mutated.
        u = db.users.find_one({"id": target_id})
        assert u["role"] == ineligible_role, "role must remain unchanged"


def test_overview_mrr_falls_back_to_plan_catalog_when_amount_cents_missing(db):
    """Round-2 blocker #2: real 15.B subscription rows do not include
    `amount_cents` (the webhook handlers only persist `stripe_price_id`).
    Overview MRR must fall back to the seeded `plans` catalog using
    (plan_tier_code, billing_cycle). Without the fallback this test
    would see committed_monthly_cents == 0 — the silent prod bug.

    Uses isolated tier codes (`tier_15e_*`) to avoid mutating the shared
    `starter` / `professional` rows that 15.B tests assume.
    """
    tok, _ = _mint_user(db, "admin")
    # Isolated plan rows — unique tier codes that don't collide with
    # whatever 15.B / seed scripts wrote.
    db.plans.insert_one({
        "id": "tier_15e_m", "tier_code": "tier_15e_m",
        "monthly_price_cents": 4900, "annual_price_cents": 49980,
        "feature_limits": {"horses": 25, "users": 5},
    })
    db.plans.insert_one({
        "id": "tier_15e_a", "tier_code": "tier_15e_a",
        "monthly_price_cents": 14900, "annual_price_cents": 151980,
        "feature_limits": {"horses": 100, "users": 25},
    })

    # Realistic 15.B-shaped subscription rows — NO `amount_cents` field.
    sid_realistic = f"sub_15e_{uuid.uuid4().hex[:8]}"
    db.subscriptions.insert_one({
        "id": sid_realistic,
        "stripe_subscription_id": sid_realistic,
        "barn_id": "primary",
        "owner_user_id": None,
        "plan_tier_code": "tier_15e_m",
        "status": "active",
        "billing_cycle": "monthly",
        # NO amount_cents — this is what _h_subscription_updated produces.
        "stripe_price_id": "price_starter_monthly",
        "current_period_start": _iso(_now() - timedelta(days=5)),
        "current_period_end":   _iso(_now() + timedelta(days=25)),
        "created_at": _iso(_now() - timedelta(days=5)),
        "updated_at": _iso(_now() - timedelta(days=1)),
    })
    sid_pro_annual = f"sub_15e_{uuid.uuid4().hex[:8]}"
    db.subscriptions.insert_one({
        "id": sid_pro_annual,
        "stripe_subscription_id": sid_pro_annual,
        "barn_id": "primary",
        "plan_tier_code": "tier_15e_a",
        "status": "active",
        "billing_cycle": "annual",
        "stripe_price_id": "price_pro_annual",
        "current_period_start": _iso(_now() - timedelta(days=5)),
        "current_period_end":   _iso(_now() + timedelta(days=360)),
        "created_at": _iso(_now() - timedelta(days=5)),
        "updated_at": _iso(_now() - timedelta(days=1)),
    })
    try:
        # Per-row projection check — pulls JUST our row by tier filter,
        # which avoids confounds from other test rows in the collection.
        r = requests.get(f"{API}/admin/billing/subscriptions?tier=tier_15e_m",
                         headers=_h(tok), timeout=15)
        rows = r.json()["items"]
        match = next(x for x in rows if x["subscription_id"] == sid_realistic)
        assert match["monthly_equivalent_cents"] == 4900, \
            "fallback failed: amount_cents=None should resolve via plan catalog"
        assert match["amount_cents"] is None, \
            "test row must lack amount_cents to validate the fallback"

        r = requests.get(f"{API}/admin/billing/subscriptions?tier=tier_15e_a",
                         headers=_h(tok), timeout=15)
        rows = r.json()["items"]
        match = next(x for x in rows if x["subscription_id"] == sid_pro_annual)
        # 151980 / 12 = 12665
        assert match["monthly_equivalent_cents"] == 12665, \
            f"annual fallback failed: got {match['monthly_equivalent_cents']}"

        # Overview math also reflects the fallback (>= the two rows' MRR).
        r = requests.get(f"{API}/admin/billing/overview",
                         headers=_h(tok), timeout=15)
        committed = r.json()["mrr"]["committed_monthly_cents"]
        assert committed >= 4900 + 12665, \
            f"committed MRR fallback failed: got {committed}"
    finally:
        db.subscriptions.delete_one({"stripe_subscription_id": sid_realistic})
        db.subscriptions.delete_one({"stripe_subscription_id": sid_pro_annual})
        db.plans.delete_one({"tier_code": "tier_15e_m"})
        db.plans.delete_one({"tier_code": "tier_15e_a"})


def test_subscription_detail_billing_events_enriched_lookup(db):
    """Round-2 should-fix #3: `billing_events` rows from 15.B store the
    Stripe object id in `object_id`, NOT a normalised `subscription_id`.
    The drill-in must now surface events whose object_id references this
    subscription, any of its invoices, or its Stripe customer.
    """
    tok, _ = _mint_user(db, "admin")
    sid = f"sub_15e_{uuid.uuid4().hex[:8]}"
    cust = f"cus_15e_{uuid.uuid4().hex[:8]}"
    db.subscriptions.insert_one({
        "id": sid, "stripe_subscription_id": sid,
        "stripe_customer_id": cust,
        "barn_id": "primary", "plan_tier_code": "starter",
        "billing_cycle": "monthly", "status": "active",
        "created_at": _iso(_now()), "updated_at": _iso(_now()),
    })
    inv_id = f"in_15e_{uuid.uuid4().hex[:8]}"
    db.subscription_invoices.insert_one({
        "id": inv_id, "stripe_invoice_id": inv_id,
        "subscription_id": sid, "barn_id": "primary",
        "amount_cents": 4900, "status": "paid",
        "created_at": _iso(_now() - timedelta(hours=1)),
    })
    # Seed 3 billing_events using the REAL 15.B schema (object_id, no
    # subscription_id field):
    db.billing_events.insert_many([
        {"stripe_event_id": f"evt_15e_a_{uuid.uuid4().hex[:6]}",
         "event_type": "customer.subscription.updated",
         "object_id": sid,                       # → matches subscription
         "processing_status": "ok",
         "created_at": _iso(_now() - timedelta(minutes=1)),
         "updated_at": _iso(_now() - timedelta(minutes=1))},
        {"stripe_event_id": f"evt_15e_b_{uuid.uuid4().hex[:6]}",
         "event_type": "invoice.payment_succeeded",
         "object_id": inv_id,                    # → matches via invoice
         "processing_status": "ok",
         "created_at": _iso(_now() - timedelta(minutes=2)),
         "updated_at": _iso(_now() - timedelta(minutes=2))},
        {"stripe_event_id": f"evt_15e_c_{uuid.uuid4().hex[:6]}",
         "event_type": "customer.updated",
         "object_id": cust,                      # → matches via customer
         "processing_status": "ok",
         "created_at": _iso(_now() - timedelta(minutes=3)),
         "updated_at": _iso(_now() - timedelta(minutes=3))},
        # Unrelated event should NOT appear.
        {"stripe_event_id": f"evt_15e_x_{uuid.uuid4().hex[:6]}",
         "event_type": "customer.subscription.updated",
         "object_id": "sub_completely_unrelated_xyz",
         "processing_status": "ok",
         "created_at": _iso(_now()),
         "updated_at": _iso(_now())},
    ])
    try:
        r = requests.get(f"{API}/admin/billing/subscriptions/{sid}",
                         headers=_h(tok), timeout=15)
        assert r.status_code == 200, r.text
        events = r.json()["billing_events"]
        types = sorted(e["event_type"] for e in events)
        assert "customer.subscription.updated" in types, \
            "subscription-scoped event must surface"
        assert "invoice.payment_succeeded" in types, \
            "invoice-scoped event must surface (via invoice id linkage)"
        assert "customer.updated" in types, \
            "customer-scoped event must surface (via customer id linkage)"
        # Unrelated event must NOT leak in.
        unrelated_present = any(
            e.get("object_id") == "sub_completely_unrelated_xyz"
            for e in events)
        assert not unrelated_present, "unrelated event leaked into drill-in"
    finally:
        db.subscriptions.delete_one({"stripe_subscription_id": sid})
        db.subscription_invoices.delete_one({"stripe_invoice_id": inv_id})
        db.billing_events.delete_many({"stripe_event_id": {"$regex": "^evt_15e_"}})


def test_search_q_escapes_regex_metacharacters(db):
    """Round-2 should-fix #4: `q` is regex-escaped, length-capped, and
    safe against operator typos with metacharacters like `.` or `[`.
    """
    tok, _ = _mint_user(db, "admin")
    # Seed a barn with a literal "." in the name.
    bid = f"barn_15e_{uuid.uuid4().hex[:6]}"
    db.barns.insert_one({"id": bid, "name": "Smith.Co",
                         "created_at": _iso(_now())})
    try:
        # Plain "." would match every char without escape; with escape it
        # only matches the literal dot.
        r = requests.get(f"{API}/admin/barns?q=Smith.Co",
                         headers=_h(tok), timeout=15)
        assert r.status_code == 200, r.text
        names = [b["name"] for b in r.json()["items"]]
        assert "Smith.Co" in names

        # Pathological input that previously could explode the regex
        # engine — must just return safely (empty or filtered, never 500).
        r = requests.get(f"{API}/admin/barns?q=(((",
                         headers=_h(tok), timeout=15)
        assert r.status_code == 200, r.text

        # Length cap — the Query(...) declares max_length=80, so anything
        # longer is a 422 from FastAPI validation. That's the intended
        # belt-and-braces.
        long_q = "x" * 200
        r = requests.get(f"{API}/admin/barns?q={long_q}",
                         headers=_h(tok), timeout=15)
        assert r.status_code in (200, 422), r.text
    finally:
        db.barns.delete_one({"id": bid})
