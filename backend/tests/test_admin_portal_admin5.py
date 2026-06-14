"""tests/test_admin_portal_admin5.py — Subscription + Billing Control Center.

Covers the four READ-ONLY Admin-5 endpoints:
  - GET /api/admin/portal/subscriptions
  - GET /api/admin/portal/subscriptions/{id}
  - GET /api/admin/portal/billing-events
  - GET /api/admin/portal/payments

Locked founder decisions:
  1a — READ-ONLY only.
  2a — support_admin reads subscriptions; 403 on billing-events + payments.
  3a — no manual email-pass retry action (no mutation surface).
  4a — Stripe IDs OMITTED from API responses.
  5a — one Billing Control Center page (frontend).
  6a — sidebar keeps two items.
  7a — subscription detail recent_activity comes from audit_log only.
  8a — Admin-5 read audits excluded from Admin-2 activity feed.

Critical invariants:
  - All four endpoints require a platform_role; barn-scoped users → 403.
  - support_admin gets 200 on /subscriptions(*), 403 on /billing-events
    and /payments.
  - No mutation methods exposed (POST/PUT/PATCH/DELETE → 401/403/405).
  - No Stripe ID prefixes (`sub_`, `cus_`, `evt_`, `price_`, `pi_`,
    `ch_`, `in_`) or `stripe_*` keys in any response.
  - No Phase 9 `invoices` / `recurring_charges` references; planting a
    Phase 9 invoice document must NOT appear in /payments.
  - Admin-5 read audit actions are filtered out of the Admin-2 activity
    feed.
"""
from __future__ import annotations

import os
import pathlib
import sys
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


def _signup(role: str = "horse_owner") -> dict:
    email = f"adm5_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "Adm5 Test", "role": role},
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


def _bearer(s: dict) -> dict:
    return {"Authorization": f"Bearer {s['token']}"}


def _plant_subscription(db, *, barn_id: str = None, sub_id: str = None) -> str:
    """Plant a deterministic subscription row with known Stripe IDs so
    leak-guard tests can scan for the exact values in the response.

    The local `id` is intentionally NOT marked with `LEAK` — that field
    is the entity identifier (also happens to be the Stripe id by design
    of the webhook handler). We tag ONLY the Stripe foreign-key fields
    (`stripe_customer_id`, `stripe_price_id`) with the `LEAK` marker so
    response text scans can prove those fields never cross the boundary.
    """
    barn_id = barn_id or f"barn_adm5_{uuid.uuid4().hex[:8]}"
    sub_id = sub_id or f"sub_internal_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    db.barns.insert_one({
        "id": barn_id, "name": f"Adm5Barn_{barn_id[-4:]}",
        "subscription_tier_code": "starter", "subscription_id": sub_id,
        "created_at": now,
    })
    db.subscriptions.insert_one({
        "id": sub_id,
        "barn_id": barn_id,
        "plan_tier_code": "starter",
        "status": "active",
        "billing_cycle": "month",
        "amount_cents": 4900,
        "currency": "usd",
        # `LEAK` tagged so the test can prove these fields never appear
        # in the response payload.
        "stripe_customer_id": f"cus_STRIPELEAK_{uuid.uuid4().hex[:6]}",
        "stripe_subscription_id": sub_id,
        "stripe_price_id": f"price_STRIPELEAK_{uuid.uuid4().hex[:6]}",
        "current_period_start": now,
        "current_period_end": now,
        "trial_end": None,
        "cancel_at_period_end": False,
        "entitlements_snapshot": {"horses": 25, "users": 10},
        "pending_emails": [],
        "created_at": now, "updated_at": now,
    })
    return sub_id


def _plant_billing_event(db, *, barn_id: str = None, sub_id: str = None,
                        status: str = "ok") -> str:
    barn_id = barn_id or f"barn_evt_{uuid.uuid4().hex[:6]}"
    eid = f"evt_internal_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    db.billing_events.insert_one({
        "id": eid,
        # The stripe_event_id field MUST not appear in responses; mark
        # the value so the leak scan can detect any regression.
        "stripe_event_id": f"evt_STRIPELEAK_{uuid.uuid4().hex[:6]}",
        "event_type": "customer.subscription.updated",
        "event_created_at": now,
        "object_id": sub_id or f"sub_internal_{uuid.uuid4().hex[:6]}",
        "barn_id": barn_id,
        "summary": "subscription updated",
        "processing_status": status,
        "processed_at": now,
        "retry_count": 0,
        "last_error_class": None,
        "created_at": now, "updated_at": now,
    })
    return eid


def _plant_subscription_invoice(db, *, barn_id: str, sub_id: str) -> str:
    iid = f"in_internal_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    db.subscription_invoices.insert_one({
        "id": iid,
        "barn_id": barn_id,
        "subscription_id": sub_id,
        "stripe_invoice_id": f"in_STRIPELEAK_{uuid.uuid4().hex[:6]}",
        "stripe_customer_id": f"cus_STRIPELEAK_{uuid.uuid4().hex[:6]}",
        "amount_cents": 4900,
        "currency": "usd",
        "status": "paid",
        "hosted_invoice_url": "https://stripe-leak.test/hosted",
        "invoice_pdf_url": "https://stripe-leak.test/pdf",
        "period_start": now, "period_end": now,
        "due_date": now,
        "payment_failure_count": 0,
        "created_at": now, "updated_at": now,
    })
    return iid


def _plant_phase9_invoice(db, *, barn_id: str) -> str:
    """Plant a Phase 9 `invoices` doc that MUST NOT appear in Admin-5."""
    iid = f"phase9_inv_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    db.invoices.insert_one({
        "id": iid,
        "barn_id": barn_id,
        "amount_cents": 12345,
        "status": "paid",
        "invoice_number": iid,
        "created_at": now,
    })
    return iid


import re

# Stripe-shaped ID VALUE regex — matches a quoted JSON value whose
# contents look exactly like a Stripe id (e.g. "sub_…", "evt_…", "in_…",
# "cus_…", "price_…"). The pattern is anchored to the opening quote so
# legitimate field names like "admin_ref" (which contains "in_" as a
# substring) and barn ids like "barn_evt_…" do NOT trigger false matches.
STRIPE_VALUE_RE = re.compile(
    r'"(sub|evt|in|cus|price)_[A-Za-z0-9_]{4,}"'
)

# Stripe foreign-key field NAMES that must never serialize.
STRIPE_KEY_TOKENS = (
    "stripe_customer_id", "stripe_subscription_id",
    "stripe_price_id", "stripe_invoice_id", "stripe_event_id",
)


def _assert_no_stripe_value_leak(text: str, where: str) -> None:
    """Run both the regex value-scan AND the explicit key-name scan."""
    m = STRIPE_VALUE_RE.search(text)
    if m:
        raise AssertionError(
            f"{where} leaked a Stripe-shaped value: {m.group(0)}"
        )
    for k in STRIPE_KEY_TOKENS:
        if k in text:
            raise AssertionError(f"{where} leaked Stripe field key '{k}'")


# Kept for backwards reference in older assertions that import it.
STRIPE_LEAK_TOKENS = STRIPE_KEY_TOKENS


def _admin_ref_for(db, collection: str, local_id: str, prefix: str) -> str:
    """Look up the Mongo `_id` for a planted row and mint the same opaque
    admin_ref the API would mint. Lets tests address the new
    `/admin/portal/{kind}/{admin_ref}` route without ever exposing the
    raw Stripe-shaped local id in the URL."""
    row = getattr(db, collection).find_one({"id": local_id}, {"_id": 1})
    assert row, f"No {collection} row found for local id {local_id}"
    return f"{prefix}_{str(row['_id'])}"


def _admin_ref_for_subscription(db, sub_local_id: str) -> str:
    return _admin_ref_for(db, "subscriptions", sub_local_id, "as")


# ---------------------------------------------------------------------
# Access boundary
# ---------------------------------------------------------------------
ENDPOINTS_ALL_PLATFORM_ROLES = (
    "/admin/portal/subscriptions",
)
ENDPOINTS_BILLING_TAB_ONLY = (
    "/admin/portal/billing-events",
    "/admin/portal/payments",
)


@pytest.mark.parametrize("platform_role", [
    "super_admin", "platform_admin", "support_admin",
    "billing_admin", "read_only_auditor",
])
def test_subscriptions_list_visible_to_every_platform_role(db, platform_role):
    """All 5 platform roles can read /subscriptions (summary)."""
    s = _admin_session(db, platform_role)
    r = requests.get(f"{API}/admin/portal/subscriptions?limit=5",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200, (
        f"{platform_role} got {r.status_code} on /subscriptions: {r.text}"
    )


@pytest.mark.parametrize("path", ENDPOINTS_BILLING_TAB_ONLY)
def test_support_admin_blocked_from_billing_tab(db, path):
    """Decision 2a: support_admin can read subscriptions but NOT
    billing-events / payments."""
    s = _admin_session(db, "support_admin")
    r = requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
    assert r.status_code == 403, (
        f"support_admin reached {path} (status={r.status_code}, body={r.text})"
    )


@pytest.mark.parametrize("platform_role", [
    "super_admin", "platform_admin", "billing_admin", "read_only_auditor",
])
@pytest.mark.parametrize("path", ENDPOINTS_BILLING_TAB_ONLY)
def test_billing_tab_visible_to_non_support_platform_roles(db, platform_role, path):
    s = _admin_session(db, platform_role)
    r = requests.get(f"{API}{path}?limit=5", headers=_bearer(s), timeout=10)
    assert r.status_code == 200, (
        f"{platform_role} got {r.status_code} on {path}: {r.text}"
    )


@pytest.mark.parametrize("path", [
    "/admin/portal/subscriptions",
    "/admin/portal/billing-events",
    "/admin/portal/payments",
])
def test_barn_admin_without_platform_role_is_403(db, path):
    """Barn-level role='admin' must NOT inherit Admin-5 access."""
    s = _signup()
    db.users.update_one({"id": s["user"]["id"]}, {"$set": {"role": "admin"}})
    r = requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
    assert r.status_code == 403


@pytest.mark.parametrize("path", [
    "/admin/portal/subscriptions",
    "/admin/portal/billing-events",
    "/admin/portal/payments",
])
def test_horse_owner_is_403(db, path):
    s = _signup()
    r = requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
    assert r.status_code == 403


@pytest.mark.parametrize("path", [
    "/admin/portal/subscriptions",
    "/admin/portal/billing-events",
    "/admin/portal/payments",
])
def test_unauthenticated_is_401(path):
    r = requests.get(f"{API}{path}", timeout=10)
    assert r.status_code == 401


def test_subscription_detail_404_for_missing(db):
    s = _admin_session(db, "platform_admin")
    # Malformed ref (not the `as_<24-hex>` pattern) → 404, not 422.
    r = requests.get(
        f"{API}/admin/portal/subscriptions/does-not-exist-{uuid.uuid4().hex[:6]}",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 404
    # Well-formed but nonexistent ref → 404.
    r = requests.get(
        f"{API}/admin/portal/subscriptions/as_" + "f" * 24,
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 404


def test_subscription_detail_rejects_raw_stripe_shaped_id(db):
    """Locked decision 4a: the detail route must NOT accept a raw
    Stripe-shaped subscription id. Only the opaque `as_<oid>` ref."""
    s = _admin_session(db, "platform_admin")
    sub_id = _plant_subscription(db)
    try:
        r = requests.get(
            f"{API}/admin/portal/subscriptions/{sub_id}",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 404, (
            f"Detail route accepted raw Stripe-shaped id: {r.status_code}"
        )
    finally:
        db.subscriptions.delete_one({"id": sub_id})
        db.barns.delete_many({"id": {"$regex": "^barn_adm5_"}})


# ---------------------------------------------------------------------
# Shape + leak guards — /subscriptions list
# ---------------------------------------------------------------------
def test_subscriptions_list_shape_and_no_stripe_id_leak(db):
    s = _admin_session(db, "platform_admin")
    sub_id = _plant_subscription(db)
    try:
        r = requests.get(
            f"{API}/admin/portal/subscriptions?status=active&limit=100",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        body = r.json()
        assert "items" in body and "total" in body and "next_cursor" in body
        # The raw Stripe-shaped local id MUST NOT appear anywhere in
        # the response — only the opaque admin_ref does.
        assert sub_id not in r.text, (
            f"/subscriptions leaked the raw Stripe-shaped local id '{sub_id}'"
        )
        # Find our planted row via barn_id (which is safe — UUID-shaped).
        barn = db.barns.find_one({"subscription_id": sub_id}, {"_id": 0, "id": 1})
        ours = [x for x in body["items"] if x.get("barn_id") == barn["id"]]
        assert ours, "Planted subscription missing from list (lookup by barn_id)."
        row = ours[0]
        for k in ("admin_ref", "barn_id", "plan_tier_code", "status",
                  "billing_cycle", "amount_cents", "facility_name"):
            assert k in row, f"Missing key {k} in subscription row"
        assert "id" not in row, (
            "Subscription row leaked raw `id` — only `admin_ref` is allowed"
        )
        assert row["admin_ref"].startswith("as_"), (
            f"admin_ref has wrong prefix: {row['admin_ref']}"
        )
        _assert_no_stripe_value_leak(r.text, "/subscriptions list")
        assert "STRIPELEAK" not in r.text, (
            "/subscriptions leaked a planted Stripe ID value"
        )
    finally:
        db.subscriptions.delete_one({"id": sub_id})
        db.barns.delete_many({"id": {"$regex": "^barn_adm5_"}})


def test_subscriptions_list_filters_by_status_and_tier(db):
    s = _admin_session(db, "platform_admin")
    sub_id = _plant_subscription(db)
    try:
        barn = db.barns.find_one({"subscription_id": sub_id}, {"_id": 0, "id": 1})
        # status filter — exact match
        r = requests.get(
            f"{API}/admin/portal/subscriptions?status=canceled&limit=100",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        barn_ids = [x["barn_id"] for x in r.json()["items"]]
        assert barn["id"] not in barn_ids, (
            "Active sub leaked through status=canceled filter"
        )

        # plan_tier_code filter
        r = requests.get(
            f"{API}/admin/portal/subscriptions?plan_tier_code=starter&limit=100",
            headers=_bearer(s), timeout=10,
        )
        barn_ids = [x["barn_id"] for x in r.json()["items"]]
        assert barn["id"] in barn_ids
    finally:
        db.subscriptions.delete_one({"id": sub_id})
        db.barns.delete_many({"id": {"$regex": "^barn_adm5_"}})


# ---------------------------------------------------------------------
# Shape + leak guards — /subscriptions/{id} detail
# ---------------------------------------------------------------------
def test_subscription_detail_shape_and_no_stripe_ids(db):
    s = _admin_session(db, "platform_admin")
    sub_id = _plant_subscription(db)
    ref = _admin_ref_for_subscription(db, sub_id)
    try:
        r = requests.get(f"{API}/admin/portal/subscriptions/{ref}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        body = r.json()
        assert "subscription" in body
        assert "facility" in body
        assert "recent_activity" in body
        sub = body["subscription"]
        # The opaque admin_ref is the only id surfaced.
        assert sub.get("admin_ref") == ref
        assert "id" not in sub, (
            "Detail leaked raw `id` field — only `admin_ref` is allowed"
        )
        for forbidden_key in ("stripe_customer_id", "stripe_subscription_id",
                              "stripe_price_id"):
            assert forbidden_key not in sub, (
                f"Detail leaked '{forbidden_key}' in subscription payload"
            )
        # No raw Stripe id tokens anywhere in the body.
        _assert_no_stripe_value_leak(r.text, "/subscriptions detail")
        # Strongest check: the raw Stripe-shaped local id MUST NOT
        # appear anywhere — only admin_ref is allowed out.
        assert sub_id not in r.text, (
            f"Detail leaked raw Stripe-shaped local id '{sub_id}'"
        )
        assert "STRIPELEAK" not in r.text, "Detail leaked a planted Stripe ID value"
    finally:
        db.subscriptions.delete_one({"id": sub_id})
        db.barns.delete_many({"id": {"$regex": "^barn_adm5_"}})


def test_subscription_detail_recent_activity_is_audit_log_only(db):
    """Decision 7a: recent_activity comes from audit_log — NOT
    billing_events. Plant a billing_event referencing the subscription
    and confirm it does NOT show up in recent_activity."""
    s = _admin_session(db, "platform_admin")
    sub_id = _plant_subscription(db)
    ref = _admin_ref_for_subscription(db, sub_id)
    _plant_billing_event(db, sub_id=sub_id)
    try:
        r = requests.get(f"{API}/admin/portal/subscriptions/{ref}",
                         headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        activity = r.json()["recent_activity"]
        # Every entry must look like an audit_log row (must have `action`,
        # NOT `event_type`).
        for row in activity:
            assert "action" in row
            assert "event_type" not in row, (
                "recent_activity leaked a billing_event row"
            )
            # The audit row must NOT leak the Stripe-shaped resource_id
            # that lives on the underlying audit_log document.
            assert "resource_id" not in row, (
                "recent_activity leaked raw resource_id (Stripe-shaped)"
            )
    finally:
        db.subscriptions.delete_one({"id": sub_id})
        db.billing_events.delete_many({"id": {"$regex": "^evt_internal_"}})
        db.barns.delete_many({"id": {"$regex": "^barn_adm5_"}})


# ---------------------------------------------------------------------
# Shape + leak guards — /billing-events
# ---------------------------------------------------------------------
def test_billing_events_shape_and_no_stripe_id_leak(db):
    s = _admin_session(db, "platform_admin")
    eid = _plant_billing_event(db)
    try:
        r = requests.get(
            f"{API}/admin/portal/billing-events?limit=100",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        body = r.json()
        assert "items" in body and "total" in body
        # Find our planted row by event_type (id is now opaque admin_ref).
        ours = [x for x in body["items"]
                if x.get("event_type") == "customer.subscription.updated"]
        assert ours, "Planted billing_event missing from list."
        row = ours[0]
        assert "id" not in row, (
            "/billing-events leaked raw `id` — only `admin_ref` is allowed"
        )
        assert row.get("admin_ref", "").startswith("ae_"), (
            f"admin_ref has wrong prefix: {row.get('admin_ref')}"
        )
        # Allowlist shape — no stripe_event_id, no object_id raw.
        for forbidden in ("stripe_event_id", "object_id"):
            assert forbidden not in row, (
                f"/billing-events leaked '{forbidden}'"
            )
        for token in STRIPE_LEAK_TOKENS:
            assert token not in r.text, (
                f"/billing-events leaked Stripe token '{token}'"
            )
        _assert_no_stripe_value_leak(r.text, "/billing-events list")
        assert eid not in r.text, (
            f"/billing-events leaked raw Stripe-shaped local id '{eid}'"
        )
        assert "STRIPELEAK" not in r.text, "/billing-events leaked a planted ID"
    finally:
        db.billing_events.delete_many({"id": {"$regex": "^evt_internal_"}})


def test_billing_events_filters_by_processing_status(db):
    s = _admin_session(db, "platform_admin")
    eid_ok = _plant_billing_event(db, status="ok")
    eid_retry = _plant_billing_event(db, status="retry_502")
    try:
        # We filter by status and confirm the count matches what we
        # planted — we can't filter by Stripe-shaped local id anymore.
        # Each row must NOT carry the raw evt_… id either.
        r = requests.get(
            f"{API}/admin/portal/billing-events?processing_status=retry_502&limit=100",
            headers=_bearer(s), timeout=10,
        )
        items = r.json()["items"]
        statuses = [x.get("processing_status") for x in items]
        assert "retry_502" in statuses
        assert "ok" not in statuses
        assert eid_ok not in r.text and eid_retry not in r.text
    finally:
        db.billing_events.delete_many({"id": {"$regex": "^evt_internal_"}})


# ---------------------------------------------------------------------
# Shape + leak guards — /payments + Phase 9 isolation
# ---------------------------------------------------------------------
def test_payments_shape_and_no_stripe_id_leak(db):
    s = _admin_session(db, "platform_admin")
    sub_id = _plant_subscription(db)
    barn = db.barns.find_one({"subscription_id": sub_id}, {"_id": 0, "id": 1})
    iid = _plant_subscription_invoice(db, barn_id=barn["id"], sub_id=sub_id)
    try:
        r = requests.get(
            f"{API}/admin/portal/payments?limit=100",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        body = r.json()
        # Find our planted row via barn_id (id is now opaque admin_ref).
        ours = [x for x in body["items"] if x.get("barn_id") == barn["id"]]
        assert ours, "Planted subscription_invoice missing from /payments."
        row = ours[0]
        assert "id" not in row, (
            "/payments leaked raw `id` — only `admin_ref` is allowed"
        )
        assert row.get("admin_ref", "").startswith("ap_"), (
            f"admin_ref has wrong prefix: {row.get('admin_ref')}"
        )
        # The Stripe-shaped foreign `subscription_id` MUST be replaced
        # with the opaque `subscription_admin_ref`.
        assert "subscription_id" not in row, (
            "/payments leaked raw Stripe-shaped `subscription_id`"
        )
        assert row.get("subscription_admin_ref", "").startswith("as_"), (
            f"subscription_admin_ref wrong shape: {row.get('subscription_admin_ref')}"
        )
        # No Stripe-side keys, no hosted URLs.
        for forbidden in ("stripe_customer_id", "stripe_invoice_id",
                          "hosted_invoice_url", "invoice_pdf_url"):
            assert forbidden not in row, f"/payments leaked '{forbidden}'"
        for token in STRIPE_LEAK_TOKENS:
            assert token not in r.text, (
                f"/payments leaked Stripe token '{token}'"
            )
        _assert_no_stripe_value_leak(r.text, "/payments list")
        # The planted raw ids (Stripe-shaped) must not appear.
        assert iid not in r.text, (
            f"/payments leaked the raw invoice local id '{iid}'"
        )
        assert sub_id not in r.text, (
            f"/payments leaked the raw subscription_id '{sub_id}'"
        )
        assert "stripe-leak.test" not in r.text, (
            "/payments leaked hosted Stripe URL"
        )
        assert "STRIPELEAK" not in r.text, "/payments leaked a planted Stripe ID"
    finally:
        db.subscription_invoices.delete_many({"id": {"$regex": "^in_internal_"}})
        db.subscriptions.delete_one({"id": sub_id})
        db.barns.delete_many({"id": {"$regex": "^barn_adm5_"}})


def test_payments_does_not_leak_phase9_invoices(db):
    """Strong Phase 9 isolation guard (founder direction): planting a
    Phase 9 `invoices` document MUST NOT make it appear in /payments,
    which reads exclusively from `subscription_invoices`."""
    s = _admin_session(db, "platform_admin")
    sub_id = _plant_subscription(db)
    barn = db.barns.find_one({"subscription_id": sub_id}, {"_id": 0, "id": 1})
    phase9_id = _plant_phase9_invoice(db, barn_id=barn["id"])
    try:
        r = requests.get(
            f"{API}/admin/portal/payments?limit=100",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        body_text = r.text
        assert phase9_id not in body_text, (
            f"/payments leaked Phase 9 invoice id '{phase9_id}'"
        )
        # The Phase 9 collection name MUST NEVER appear in the response.
        assert "recurring_charges" not in body_text
    finally:
        db.invoices.delete_one({"id": phase9_id})
        db.subscriptions.delete_one({"id": sub_id})
        db.barns.delete_many({"id": {"$regex": "^barn_adm5_"}})


def test_subscriptions_endpoints_do_not_reference_phase9_invoices(db):
    """Same Phase 9 guard against the subscription list + detail
    endpoints — naming is similar so the boundary needs an explicit
    test."""
    s = _admin_session(db, "platform_admin")
    sub_id = _plant_subscription(db)
    ref = _admin_ref_for_subscription(db, sub_id)
    barn = db.barns.find_one({"subscription_id": sub_id}, {"_id": 0, "id": 1})
    phase9_id = _plant_phase9_invoice(db, barn_id=barn["id"])
    try:
        for path in (f"/admin/portal/subscriptions?barn_id={barn['id']}&limit=100",
                     f"/admin/portal/subscriptions/{ref}"):
            r = requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
            assert r.status_code == 200
            text = r.text
            assert phase9_id not in text, (
                f"{path} leaked Phase 9 invoice id"
            )
            for forbidden in ("recurring_charges",):
                assert forbidden not in text, (
                    f"{path} leaked Phase 9 reference '{forbidden}'"
                )
    finally:
        db.invoices.delete_one({"id": phase9_id})
        db.subscriptions.delete_one({"id": sub_id})
        db.barns.delete_many({"id": {"$regex": "^barn_adm5_"}})


# ---------------------------------------------------------------------
# Read-only ceiling (decision 1a)
# ---------------------------------------------------------------------
@pytest.mark.parametrize("path", [
    "/admin/portal/subscriptions",
    "/admin/portal/subscriptions/primary",
    "/admin/portal/billing-events",
    "/admin/portal/payments",
])
def test_no_mutations_exposed_on_admin5_endpoints(path):
    for method in ("post", "put", "patch", "delete"):
        r = getattr(requests, method)(
            f"{API}{path}", timeout=10,
            headers={"Content-Type": "application/json"}, json={},
        )
        assert r.status_code in (401, 403, 405), (
            f"{method.upper()} {path} unexpectedly returned {r.status_code}"
        )


# ---------------------------------------------------------------------
# Activity-feed self-flood guard (decision 8a)
# ---------------------------------------------------------------------
def test_admin5_reads_excluded_from_activity_feed(db):
    """Hitting an Admin-5 read endpoint must NOT pollute the curated
    Admin-2 activity feed — same self-flood guard as Admin-4."""
    s = _admin_session(db, "platform_admin")
    h = _bearer(s)
    # Trigger one read per Admin-5 endpoint.
    requests.get(f"{API}/admin/portal/subscriptions?limit=2", headers=h, timeout=10)
    requests.get(f"{API}/admin/portal/billing-events?limit=2", headers=h, timeout=10)
    requests.get(f"{API}/admin/portal/payments?limit=2", headers=h, timeout=10)
    # Pull the activity feed and confirm none of the Admin-5 read
    # actions appear.
    r = requests.get(f"{API}/admin/portal/activity?limit=100",
                     headers=h, timeout=10)
    assert r.status_code == 200
    actions = [x.get("action") for x in r.json()["items"]]
    forbidden = (
        "admin.portal.read.subscriptions",
        "admin.portal.read.subscription_detail",
        "admin.portal.read.billing_events",
        "admin.portal.read.payments",
    )
    for f in forbidden:
        assert f not in actions, f"Activity feed leaked Admin-5 read action '{f}'"


# ---------------------------------------------------------------------
# Audit emission
# ---------------------------------------------------------------------
def test_admin5_endpoints_emit_audit_log(db):
    s = _admin_session(db, "platform_admin")
    h = _bearer(s)
    before = {
        "subscriptions": db.audit_log.count_documents({"action": "admin.portal.read.subscriptions"}),
        "billing_events": db.audit_log.count_documents({"action": "admin.portal.read.billing_events"}),
        "payments": db.audit_log.count_documents({"action": "admin.portal.read.payments"}),
    }
    requests.get(f"{API}/admin/portal/subscriptions?limit=2", headers=h, timeout=10)
    requests.get(f"{API}/admin/portal/billing-events?limit=2", headers=h, timeout=10)
    requests.get(f"{API}/admin/portal/payments?limit=2", headers=h, timeout=10)
    after = {
        "subscriptions": db.audit_log.count_documents({"action": "admin.portal.read.subscriptions"}),
        "billing_events": db.audit_log.count_documents({"action": "admin.portal.read.billing_events"}),
        "payments": db.audit_log.count_documents({"action": "admin.portal.read.payments"}),
    }
    for k in before:
        assert after[k] == before[k] + 1, f"Missing audit emission for {k}"
