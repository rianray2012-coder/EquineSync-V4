"""tests/test_admin_portal_admin2.py — Admin Portal read-only dashboard.

Covers Admin-2 only (admin-1 surface untouched):
  - /api/admin/portal/kpis             — shape + 8 KPI keys + auth + cache
  - /api/admin/portal/subscription-health — counts + webhook health
  - /api/admin/portal/activity         — curated allowlist + scrubbing
  - All three endpoints: no mutation methods (405), audit emission

Strict guardrails verified:
  - MRR = booked recurring revenue (active only). Trialing NOT in MRR.
  - Stripe IDs absent from subscription-health response.
  - Activity feed filters to admin.* / subscription.* / user.* /
    auth.login.* / billing.event.* / permission.denied only.
  - Sensitive metadata keys defensively scrubbed.
"""
from __future__ import annotations

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
load_dotenv("/app/backend/.env")


def _base_url() -> str:
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
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup() -> dict:
    email = f"adm2_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "Adm2 Test", "role": "horse_owner"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _promote(db, user_id: str, platform_role: str):
    db.users.update_one({"id": user_id}, {"$set": {"platform_role": platform_role}})


def _admin_session(db, plat_role: str = "platform_admin") -> dict:
    s = _signup()
    _promote(db, s["user"]["id"], plat_role)
    return s


# ---------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------
def test_kpis_requires_platform_role():
    s = _signup()
    r = requests.get(
        f"{API}/admin/portal/kpis",
        headers={"Authorization": f"Bearer {s['token']}"},
        timeout=10,
    )
    assert r.status_code == 403


def test_kpis_unauthenticated_is_401():
    r = requests.get(f"{API}/admin/portal/kpis", timeout=10)
    assert r.status_code == 401


def test_kpis_shape_contains_all_eight_metrics_plus_trends(db):
    s = _admin_session(db)
    r = requests.get(
        f"{API}/admin/portal/kpis",
        headers={"Authorization": f"Bearer {s['token']}"},
        timeout=10,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    required = {
        "users_total", "users_new_7d",
        "facilities_total", "facilities_new_7d",
        "horses_total", "horses_new_7d",
        "subs_active", "subs_trialing", "subs_past_due",
        "approvals_pending", "mrr_cents",
        "mrr_definition", "_partial", "_generated_at",
    }
    assert required.issubset(body.keys()), (
        f"Missing keys: {required - set(body.keys())}"
    )
    # Trend metrics are integers (could be zero).
    for k in ("users_new_7d", "facilities_new_7d", "horses_new_7d"):
        assert isinstance(body[k], int), f"{k} must be int, got {type(body[k])}"


def test_kpis_mrr_excludes_trialing(db):
    """MRR per the founder direction: status=active only. Insert a
    trialing subscription with nonzero amount_cents and confirm it
    doesn't move the MRR number."""
    s = _admin_session(db)
    h = {"Authorization": f"Bearer {s['token']}"}

    # Snapshot MRR.
    before = requests.get(f"{API}/admin/portal/kpis", headers=h, timeout=10).json()
    # KPIs are 30-second cached; sleep past it so the next read recomputes.
    time.sleep(31)

    # Insert a trialing subscription with a $200/mo nominal price.
    barn_id = f"barn_a2_t_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_a2_t_{uuid.uuid4().hex[:10]}"
    db.barns.insert_one({"id": barn_id, "created_at": datetime.now(timezone.utc).isoformat()})
    db.subscriptions.insert_one({
        "id": sub_id, "barn_id": barn_id, "plan_tier_code": "starter",
        "stripe_subscription_id": sub_id, "status": "trialing",
        "amount_cents": 20000, "billing_cycle": "monthly",
        "pending_emails": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    after = requests.get(f"{API}/admin/portal/kpis", headers=h, timeout=10).json()
    # Trialing count rises by 1; MRR is UNCHANGED.
    assert after["subs_trialing"] == before["subs_trialing"] + 1
    assert after["mrr_cents"] == before["mrr_cents"], (
        f"MRR shifted ({before['mrr_cents']} → {after['mrr_cents']}) "
        f"after adding a trialing sub — trialing must NOT count."
    )

    # Cleanup.
    db.subscriptions.delete_one({"id": sub_id})
    db.barns.delete_one({"id": barn_id})


def test_kpis_cache_hit_within_30s(db):
    s = _admin_session(db)
    h = {"Authorization": f"Bearer {s['token']}"}
    requests.get(f"{API}/admin/portal/kpis", headers=h, timeout=10)
    # Second call within cache TTL must report cache_hit=true on the
    # audit metadata, not on the response body.
    requests.get(f"{API}/admin/portal/kpis", headers=h, timeout=10)
    latest = db.audit_log.find_one(
        {"action": "admin.portal.read.kpis", "actor_email": s["user"]["email"]},
        sort=[("ts", -1)],
    )
    assert latest is not None
    assert (latest.get("metadata") or {}).get("cache_hit") is True


# ---------------------------------------------------------------------
# Subscription health
# ---------------------------------------------------------------------
def test_subscription_health_shape(db):
    s = _admin_session(db)
    r = requests.get(
        f"{API}/admin/portal/subscription-health",
        headers={"Authorization": f"Bearer {s['token']}"},
        timeout=10,
    )
    assert r.status_code == 200
    body = r.json()
    assert "status_counts" in body
    assert {"active", "trialing", "past_due", "canceled", "incomplete"} <= set(body["status_counts"].keys())
    assert "webhook_health" in body
    assert {"failed_last_24h", "stuck_in_retry"} <= set(body["webhook_health"].keys())


def test_subscription_health_never_returns_stripe_ids(db):
    """Per the Admin-2 ceiling: no Stripe IDs in the subscription
    health card payload."""
    s = _admin_session(db)
    r = requests.get(
        f"{API}/admin/portal/subscription-health",
        headers={"Authorization": f"Bearer {s['token']}"},
        timeout=10,
    )
    body = r.text
    # Stripe IDs use these well-known prefixes.
    for forbidden in ("sub_", "cus_", "evt_", "price_", "pi_", "ch_"):
        assert forbidden not in body, (
            f"subscription-health leaked a Stripe ID prefix '{forbidden}'"
        )


def test_subscription_health_requires_platform_role():
    s = _signup()
    r = requests.get(
        f"{API}/admin/portal/subscription-health",
        headers={"Authorization": f"Bearer {s['token']}"},
        timeout=10,
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------
# Activity feed
# ---------------------------------------------------------------------
def test_activity_feed_filters_to_curated_allowlist(db):
    s = _admin_session(db)
    h = {"Authorization": f"Bearer {s['token']}"}

    # Plant one in-allowlist + one out-of-allowlist entry.
    now_iso = datetime.now(timezone.utc).isoformat()
    tag = uuid.uuid4().hex[:8]
    db.audit_log.insert_many([
        {"id": f"in_{tag}", "ts": now_iso, "action": "subscription.tested",
         "actor_email": f"t_{tag}@x", "outcome": "success",
         "metadata": {"tag": tag, "kind": "in"}},
        {"id": f"out_{tag}", "ts": now_iso, "action": "horse.photo.uploaded",
         "actor_email": f"t_{tag}@x", "outcome": "success",
         "metadata": {"tag": tag, "kind": "out"}},
    ])

    r = requests.get(f"{API}/admin/portal/activity?limit=100", headers=h, timeout=10)
    assert r.status_code == 200
    items = r.json()["items"]
    actions = [i["action"] for i in items]
    assert any(a == "subscription.tested" for a in actions), (
        "Allowlisted entry should be in the feed."
    )
    assert "horse.photo.uploaded" not in actions, (
        "Non-allowlisted entry leaked into the dashboard feed."
    )

    # Cleanup.
    db.audit_log.delete_many({"metadata.tag": tag})


def test_activity_feed_scrubs_sensitive_metadata_keys(db):
    s = _admin_session(db)
    h = {"Authorization": f"Bearer {s['token']}"}

    # Plant a curated-prefix entry with sensitive-looking metadata keys.
    now_iso = datetime.now(timezone.utc).isoformat()
    tag = uuid.uuid4().hex[:8]
    db.audit_log.insert_one({
        "id": f"scrub_{tag}", "ts": now_iso,
        "action": "admin.test.scrub_check",
        "actor_email": f"t_{tag}@x",
        "outcome": "success",
        "metadata": {
            "tag": tag,
            "password": "should-be-stripped",
            "stripe_secret_key": "sk_test_no",
            "user_token": "shouldnt-be-here",
            "safe_field": "ok",
        },
    })

    r = requests.get(f"{API}/admin/portal/activity?limit=100", headers=h, timeout=10)
    items = r.json()["items"]
    ours = [i for i in items if (i.get("metadata") or {}).get("tag") == tag]
    assert ours, "Planted scrub entry not found in feed."
    meta = ours[0].get("metadata") or {}
    assert "password" not in meta
    assert "stripe_secret_key" not in meta
    assert "user_token" not in meta  # contains 'token' → scrubbed
    assert meta.get("safe_field") == "ok"

    db.audit_log.delete_many({"metadata.tag": tag})


def test_activity_feed_respects_limit_param(db):
    s = _admin_session(db)
    r = requests.get(
        f"{API}/admin/portal/activity?limit=3",
        headers={"Authorization": f"Bearer {s['token']}"},
        timeout=10,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["limit"] == 3
    assert len(body["items"]) <= 3


def test_activity_feed_limit_param_bounds():
    s = _signup()
    # Even with a valid bearer, the bounds validator must reject before
    # the gate logic runs — limit must be 1..100.
    r = requests.get(
        f"{API}/admin/portal/activity?limit=999",
        headers={"Authorization": f"Bearer {s['token']}"},
        timeout=10,
    )
    assert r.status_code == 422


def test_activity_feed_requires_platform_role():
    s = _signup()
    r = requests.get(
        f"{API}/admin/portal/activity",
        headers={"Authorization": f"Bearer {s['token']}"},
        timeout=10,
    )
    assert r.status_code == 403


# ---------------------------------------------------------------------
# Surface invariants — Admin-2 read-only ceiling
# ---------------------------------------------------------------------
@pytest.mark.parametrize("path", [
    "/admin/portal/kpis",
    "/admin/portal/subscription-health",
    "/admin/portal/activity",
])
def test_no_mutations_exposed_on_admin2_endpoints(path):
    """Codex round-1 invariant extended to Admin-2: POST/PUT/PATCH/DELETE
    on any new dashboard endpoint must be rejected (no mutation surface)."""
    for method in ("post", "put", "patch", "delete"):
        r = getattr(requests, method)(
            f"{API}{path}",
            timeout=10,
            headers={"Content-Type": "application/json"},
            json={},
        )
        assert r.status_code in (401, 403, 405), (
            f"{method.upper()} {path} unexpectedly returned {r.status_code}"
        )


def test_all_three_endpoints_emit_audit_log(db):
    s = _admin_session(db)
    h = {"Authorization": f"Bearer {s['token']}"}

    before_k = db.audit_log.count_documents({"action": "admin.portal.read.kpis"})
    before_s = db.audit_log.count_documents({"action": "admin.portal.read.subscription_health"})
    before_a = db.audit_log.count_documents({"action": "admin.portal.read.activity"})

    requests.get(f"{API}/admin/portal/kpis", headers=h, timeout=10)
    requests.get(f"{API}/admin/portal/subscription-health", headers=h, timeout=10)
    requests.get(f"{API}/admin/portal/activity?limit=5", headers=h, timeout=10)

    assert db.audit_log.count_documents({"action": "admin.portal.read.kpis"}) == before_k + 1
    assert db.audit_log.count_documents({"action": "admin.portal.read.subscription_health"}) == before_s + 1
    assert db.audit_log.count_documents({"action": "admin.portal.read.activity"}) == before_a + 1
