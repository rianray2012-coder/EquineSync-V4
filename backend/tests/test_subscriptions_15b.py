"""tests/test_subscriptions_15b.py — Phase 15.B webhook lifecycle.

Status-gated idempotency model, 10 handler groups / 11 event types, no
side-effect leakage into Phase 9 collections, no email sends, no hard
enforcement. All tests are DB-level + monkey-patched Stripe SDK.
"""
from __future__ import annotations

import asyncio
import os
import pathlib
import sys
import time
import uuid
from datetime import datetime, timezone, timedelta

import pytest
import requests
from pymongo import MongoClient

BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


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


# ----- DB access -----
@pytest.fixture
def db():
    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "test_database"
    c = MongoClient(mongo_url)
    yield c[db_name]
    c.close()


def _post_event(event: dict) -> requests.Response:
    return requests.post(f"{API}/webhook/stripe-subscriptions", json=event, timeout=15)


def _evt(event_type: str, obj: dict, *, event_id: str | None = None) -> dict:
    return {
        "id": event_id or f"evt_test_{uuid.uuid4().hex[:14]}",
        "type": event_type,
        "created": int(time.time()),
        "data": {"object": obj},
    }


# =====================================================================
# Idempotency / retry model (the main blocker fix)
# =====================================================================

def test_billing_events_replay_short_circuits_when_status_is_ok(db):
    """After successful processing, replay returns idempotent + zero mutations."""
    barn_id = f"barn_ok_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_ok_{uuid.uuid4().hex[:8]}"
    db.subscriptions.insert_one({
        "id": sub_id, "stripe_subscription_id": sub_id, "barn_id": barn_id,
        "plan_tier_code": "starter", "status": "active",
        "pending_emails": [], "created_at": "x",
    })
    e = _evt("customer.subscription.trial_will_end", {
        "id": sub_id, "trial_end": int(time.time()) + 86400,
        "metadata": {"barn_id": barn_id},
    })
    r1 = _post_event(e)
    assert r1.status_code == 200, r1.text
    sub_after_first = db.subscriptions.find_one({"id": sub_id})
    assert "trial_will_end" in sub_after_first["pending_emails"]
    pending_count_before = len(sub_after_first["pending_emails"])
    last_event_at_before = sub_after_first.get("last_event_at")

    r2 = _post_event(e)
    assert r2.status_code == 200
    body = r2.json()
    assert body.get("idempotent") is True and body.get("status") == "ok"
    sub_after_replay = db.subscriptions.find_one({"id": sub_id})
    assert len(sub_after_replay["pending_emails"]) == pending_count_before
    assert sub_after_replay.get("last_event_at") == last_event_at_before

    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_billing_events_replay_runs_handler_when_status_is_retry_502(db):
    """An event row marked retry_502 must replay through the handler on next
    delivery and converge to ok."""
    barn_id = f"barn_retry_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_retry_{uuid.uuid4().hex[:8]}"
    db.subscriptions.insert_one({
        "id": sub_id, "stripe_subscription_id": sub_id, "barn_id": barn_id,
        "plan_tier_code": "starter", "status": "active",
        "pending_emails": [], "created_at": "x",
    })
    event_id = f"evt_retry_{uuid.uuid4().hex[:10]}"
    # Pre-seed billing_events as retry_502 to simulate previous failure.
    db.billing_events.insert_one({
        "id": event_id, "stripe_event_id": event_id,
        "event_type": "customer.subscription.trial_will_end",
        "processing_status": "retry_502",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "retry_count": 1, "created_at": "x", "updated_at": "x",
    })
    e = _evt("customer.subscription.trial_will_end", {
        "id": sub_id, "trial_end": int(time.time()) + 86400,
        "metadata": {"barn_id": barn_id},
    }, event_id=event_id)
    r = _post_event(e)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("handled") is True
    assert body.get("idempotent") is False  # actually ran handler
    row = db.billing_events.find_one({"stripe_event_id": event_id})
    assert row["processing_status"] == "ok"
    assert row["retry_count"] == 2  # incremented on the replay claim
    sub_after = db.subscriptions.find_one({"id": sub_id})
    assert "trial_will_end" in sub_after["pending_emails"]

    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": event_id})


def test_billing_events_first_delivery_failure_yields_502_and_retry_502_status(monkeypatch, db):
    """Stripe API failure inside a handler must surface 502 and persist
    processing_status=retry_502."""
    import stripe as stripe_sdk
    from routes import subscriptions_webhook_handlers as h

    class _BoomError(stripe_sdk.error.StripeError):
        pass

    def _boom(*a, **k):
        raise _BoomError("simulated stripe outage")

    monkeypatch.setattr(h, "_retrieve_stripe_subscription", _boom)

    barn_id = f"barn_boom_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_boom_{uuid.uuid4().hex[:8]}"
    event_id = f"evt_boom_{uuid.uuid4().hex[:10]}"
    event = _evt("checkout.session.completed", {
        "id": f"cs_{uuid.uuid4().hex[:10]}",
        "subscription": sub_id, "customer": f"cus_{uuid.uuid4().hex[:6]}",
        "metadata": {
            "barn_id": barn_id, "owner_user_id": "u",
            "plan_tier_code": "starter", "billing_cycle": "monthly",
        },
    }, event_id=event_id)

    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "test_database"
    async_db = AsyncIOMotorClient(mongo_url)[db_name]
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as ex:
        asyncio.run(h.process_event(async_db, event))
    assert ex.value.status_code == 502
    row = db.billing_events.find_one({"stripe_event_id": event_id})
    assert row is not None
    assert row["processing_status"] == "retry_502"

    db.billing_events.delete_one({"stripe_event_id": event_id})


def test_billing_events_replay_short_circuits_on_unknown_event(db):
    e = _evt("invoice.voided", {"id": f"in_x_{uuid.uuid4().hex[:6]}"})
    r1 = _post_event(e)
    assert r1.status_code == 200
    assert r1.json().get("status") == "unknown_event"
    pre_count = db.billing_events.count_documents({})

    r2 = _post_event(e)
    assert r2.status_code == 200
    assert r2.json().get("idempotent") is True
    assert db.billing_events.count_documents({}) == pre_count

    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_billing_events_stale_processing_lock_is_reclaimed(db):
    """A stale `processing` row must be reclaimed and replayed."""
    event_id = f"evt_stale_{uuid.uuid4().hex[:10]}"
    stale_ts = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
    db.billing_events.insert_one({
        "id": event_id, "stripe_event_id": event_id,
        "event_type": "invoice.voided",
        "processing_status": "processing",
        "processed_at": stale_ts,
        "retry_count": 0, "created_at": "x", "updated_at": "x",
    })
    e = _evt("invoice.voided", {"id": "in_stale"}, event_id=event_id)
    r = _post_event(e)
    assert r.status_code == 200
    row = db.billing_events.find_one({"stripe_event_id": event_id})
    # Unknown event type → reclaim then close as unknown_event.
    assert row["processing_status"] == "unknown_event"

    db.billing_events.delete_one({"stripe_event_id": event_id})


def test_billing_events_active_processing_lock_returns_409(db):
    event_id = f"evt_active_{uuid.uuid4().hex[:10]}"
    fresh_ts = datetime.now(timezone.utc).isoformat()
    db.billing_events.insert_one({
        "id": event_id, "stripe_event_id": event_id,
        "event_type": "customer.subscription.updated",
        "processing_status": "processing",
        "processed_at": fresh_ts,
        "retry_count": 0, "created_at": "x", "updated_at": "x",
    })
    e = _evt("customer.subscription.updated",
             {"id": "sub_in_flight"}, event_id=event_id)
    r = _post_event(e)
    assert r.status_code == 409, r.text
    body = r.json()
    assert body.get("in_flight") is True
    # Row unchanged.
    row = db.billing_events.find_one({"stripe_event_id": event_id})
    assert row["processing_status"] == "processing"

    db.billing_events.delete_one({"stripe_event_id": event_id})


# =====================================================================
# Per-event lifecycle
# =====================================================================

def _seed_local_sub(db, *, barn_id=None, sub_id=None,
                    plan_tier_code="starter", customer_id=None,
                    price_id="price_local_monthly"):
    barn_id = barn_id or f"barn_{uuid.uuid4().hex[:8]}"
    sub_id = sub_id or f"sub_{uuid.uuid4().hex[:8]}"
    customer_id = customer_id or f"cus_{uuid.uuid4().hex[:8]}"
    db.subscriptions.insert_one({
        "id": sub_id, "stripe_subscription_id": sub_id,
        "stripe_customer_id": customer_id,
        "barn_id": barn_id,
        "plan_tier_code": plan_tier_code, "status": "active",
        "stripe_price_id": price_id,
        "pending_emails": [], "created_at": "x",
        "entitlements_snapshot": {"horses": 50, "users": 5},
    })
    return barn_id, sub_id, customer_id


def test_subscription_updated_syncs_status_and_period(db):
    barn_id, sub_id, _ = _seed_local_sub(db)
    new_pe = int(time.time()) + 86400
    e = _evt("customer.subscription.updated", {
        "id": sub_id, "status": "past_due", "cancel_at_period_end": True,
        "current_period_end": new_pe,
        "items": {"data": [{"price": {"id": "price_local_monthly"}}]},
    })
    r = _post_event(e)
    assert r.status_code == 200, r.text
    sub = db.subscriptions.find_one({"id": sub_id})
    assert sub["status"] == "past_due"
    assert sub["cancel_at_period_end"] is True
    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_subscription_updated_canceled_status_clears_barn_mirror_to_free_limits(db):
    """BN15B: status-only cancellation updates must not leave the barn mirror
    pointing at paid entitlements after account_usage_limits has fallen back.
    """
    barn_id, sub_id, _ = _seed_local_sub(db, plan_tier_code="starter_barn")
    db.barns.update_one(
        {"id": barn_id},
        {"$set": {
            "id": barn_id,
            "subscription_id": sub_id,
            "subscription_entitlements": {"horses": 10, "staff_seats": 3},
        }},
        upsert=True,
    )
    db.plans.update_one(
        {"tier_code": "free"},
        {"$set": {
            "id": "free",
            "tier_code": "free",
            "feature_limits": {"horses": 1, "staff_seats": 0},
        }},
        upsert=True,
    )
    e = _evt("customer.subscription.updated", {
        "id": sub_id,
        "status": "canceled",
        "items": {"data": [{"price": {"id": "price_local_monthly"}}]},
    })

    r = _post_event(e)
    assert r.status_code == 200, r.text
    barn = db.barns.find_one({"id": barn_id})
    assert barn["subscription_id"] is None
    assert barn["subscription_entitlements"]["horses"] == 1
    assert barn["subscription_entitlements"]["staff_seats"] == 0
    assert barn["last_inactive_subscription_id"] == sub_id
    usage_limits = db.account_usage_limits.find_one({"account_id": barn_id})
    assert usage_limits["plan_code"] == "free"
    assert usage_limits["subscription_status"] == "canceled"

    db.subscriptions.delete_one({"id": sub_id})
    db.barns.delete_one({"id": barn_id})
    db.account_subscriptions.delete_one({"account_id": barn_id})
    db.account_usage_limits.delete_one({"account_id": barn_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_subscription_deleted_marks_canceled_and_clears_barn_pointer(db):
    barn_id, sub_id, _ = _seed_local_sub(db)
    db.barns.insert_one({"id": barn_id, "subscription_id": sub_id})
    db.plans.update_one({"tier_code": "free"},
                        {"$setOnInsert": {"feature_limits": {"horses": 1}}},
                        upsert=True)
    e = _evt("customer.subscription.deleted", {"id": sub_id})
    r = _post_event(e)
    assert r.status_code == 200
    sub = db.subscriptions.find_one({"id": sub_id})
    assert sub["status"] == "canceled"
    assert sub.get("canceled_at")
    barn = db.barns.find_one({"id": barn_id})
    assert barn["subscription_id"] is None
    db.subscriptions.delete_one({"id": sub_id})
    db.barns.delete_one({"id": barn_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_trial_will_end_addtoset_appends_email_flag(db):
    barn_id, sub_id, _ = _seed_local_sub(db)
    # Pre-existing flag — must NOT be lost when a new one arrives.
    db.subscriptions.update_one({"id": sub_id},
                                {"$addToSet": {"pending_emails": "payment_failed"}})
    e = _evt("customer.subscription.trial_will_end",
             {"id": sub_id, "trial_end": int(time.time()) + 86400,
              "metadata": {"barn_id": barn_id}})
    _post_event(e)
    sub = db.subscriptions.find_one({"id": sub_id})
    assert set(sub["pending_emails"]) == {"payment_failed", "trial_will_end"}
    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_checkout_completed_unknown_plan_does_not_lock_empty_entitlements(monkeypatch):
    """BN15B: checkout must use the same guarded entitlement resolver as
    subscription lifecycle events. Unknown plans stay retryable, not OK-empty.
    """
    from routes import subscriptions_webhook_handlers as h

    def _fake_retrieve_subscription(_subscription_id):
        return {
            "id": _subscription_id,
            "status": "active",
            "items": {"data": [{"price": {"id": "price_checkout_unknown"}}]},
        }

    sub_id = f"sub_checkout_unknown_{uuid.uuid4().hex[:8]}"
    e = _evt("checkout.session.completed", {
        "id": f"cs_{uuid.uuid4().hex[:8]}",
        "customer": f"cus_{uuid.uuid4().hex[:8]}",
        "subscription": sub_id,
        "metadata": {
            "barn_id": f"barn_checkout_unknown_{uuid.uuid4().hex[:8]}",
            "plan_tier_code": "not_a_real_plan",
            "owner_user_id": "u_checkout",
            "billing_cycle": "monthly",
        },
    })

    monkeypatch.setattr(h, "_retrieve_stripe_subscription", _fake_retrieve_subscription)

    class _NoPlanCollection:
        async def find_one(self, *args, **kwargs):
            return None

        async def insert_one(self, *args, **kwargs):
            raise AssertionError("subscription insert must not happen for unknown plans")

        async def update_one(self, *args, **kwargs):
            raise AssertionError("barn mirror update must not happen for unknown plans")

    class _StubDB:
        subscriptions = _NoPlanCollection()
        plans = _NoPlanCollection()
        barns = _NoPlanCollection()

    with pytest.raises(h._MetadataMissing) as ex:
        asyncio.run(h._h_checkout_session_completed(_StubDB(), e))
    assert ex.value.retryable is True
    assert "plan_tier_code not resolvable" in ex.value.reason


def test_invoice_paid_inserts_subscription_invoice_and_payment_row(db):
    barn_id, sub_id, customer_id = _seed_local_sub(db)
    inv_id = f"in_{uuid.uuid4().hex[:8]}"
    pi_id = f"pi_{uuid.uuid4().hex[:8]}"
    e = _evt("invoice.paid", {
        "id": inv_id, "subscription": sub_id, "customer": customer_id,
        "amount_paid": 4900, "currency": "usd", "status": "paid",
        "payment_intent": pi_id,
        "hosted_invoice_url": "https://hosted.example", "invoice_pdf": "https://pdf.example",
        "status_transitions": {"paid_at": int(time.time())},
    })
    r = _post_event(e)
    assert r.status_code == 200, r.text
    inv = db.subscription_invoices.find_one({"stripe_invoice_id": inv_id})
    assert inv["status"] == "paid" and inv["amount_cents"] == 4900
    pay = db.payments.find_one({"stripe_payment_intent_id": pi_id})
    assert pay["status"] == "succeeded" and pay["barn_id"] == barn_id
    sub = db.subscriptions.find_one({"id": sub_id})
    assert "payment_succeeded" in sub["pending_emails"]
    db.subscription_invoices.delete_one({"stripe_invoice_id": inv_id})
    db.payments.delete_one({"stripe_payment_intent_id": pi_id})
    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_invoice_payment_failed_mirrors_stripe_status_and_increments_counter(db):
    barn_id, sub_id, customer_id = _seed_local_sub(db)
    inv_id = f"in_fail_{uuid.uuid4().hex[:8]}"
    e = _evt("invoice.payment_failed", {
        "id": inv_id, "subscription": sub_id, "customer": customer_id,
        "amount_due": 4900, "currency": "usd",
        "status": "open",   # Stripe will keep retrying — NOT uncollectible.
    })
    r = _post_event(e)
    assert r.status_code == 200, r.text
    inv = db.subscription_invoices.find_one({"stripe_invoice_id": inv_id})
    assert inv["status"] == "open"  # mirror, not forced to uncollectible
    assert inv["payment_failure_count"] >= 1
    assert inv["payment_failed_at"]
    barn = db.barns.find_one({"id": barn_id})
    assert barn and barn.get("last_payment_failed_at")
    sub = db.subscriptions.find_one({"id": sub_id})
    assert "payment_failed" in sub["pending_emails"]
    db.subscription_invoices.delete_one({"stripe_invoice_id": inv_id})
    db.barns.delete_one({"id": barn_id})
    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_payment_intent_succeeded_upserts_payments_row_idempotently(db):
    barn_id, sub_id, customer_id = _seed_local_sub(db)
    pi_id = f"pi_idem_{uuid.uuid4().hex[:8]}"
    obj = {
        "id": pi_id, "customer": customer_id, "amount": 4900, "currency": "usd",
        "charges": {"data": [{"payment_method_details": {
            "card": {"brand": "visa", "last4": "4242"}}}]},
    }
    r1 = _post_event(_evt("payment_intent.succeeded", obj))
    assert r1.status_code == 200, r1.text
    p1 = db.payments.find_one({"stripe_payment_intent_id": pi_id})
    assert p1["status"] == "succeeded"
    assert p1["payment_method_brand"] == "visa" and p1["payment_method_last4"] == "4242"
    # Different event id, same payment_intent → still one row.
    r2 = _post_event(_evt("payment_intent.succeeded", obj))
    assert r2.status_code == 200
    assert db.payments.count_documents({"stripe_payment_intent_id": pi_id}) == 1
    db.payments.delete_one({"stripe_payment_intent_id": pi_id})
    db.subscriptions.delete_one({"id": sub_id})


# =====================================================================
# Metadata-resolution semantics
# =====================================================================

def test_unresolvable_subscription_event_marks_metadata_missing_retryable(db):
    """Codex round-3 #1: retryable metadata miss now returns 503 (not 200)
    so Stripe replays. Row is persisted with status=metadata_missing_retryable.
    """
    e = _evt("customer.subscription.updated",
             {"id": f"sub_ghost_{uuid.uuid4().hex[:6]}",
              "status": "active",
              "items": {"data": [{"price": {"id": "price_x"}}]}})
    r = _post_event(e)
    assert r.status_code == 503, r.text
    row = db.billing_events.find_one({"stripe_event_id": e["id"]})
    assert row is not None
    assert row["processing_status"] == "metadata_missing_retryable"
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_unresolvable_deletion_event_marks_metadata_missing_permanent(db):
    e = _evt("customer.subscription.deleted",
             {"id": f"sub_ghost_del_{uuid.uuid4().hex[:6]}"})
    r = _post_event(e)
    assert r.status_code == 200
    assert r.json().get("status") == "metadata_missing_permanent"
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


# =====================================================================
# Phase 9 isolation
# =====================================================================

def test_phase9_invoices_collection_untouched(db):
    before = db.invoices.count_documents({})
    barn_id, sub_id, customer_id = _seed_local_sub(db)
    inv_id = f"in_p9_{uuid.uuid4().hex[:6]}"
    e = _evt("invoice.created", {
        "id": inv_id, "subscription": sub_id, "customer": customer_id,
        "amount_due": 4900, "currency": "usd", "status": "draft",
    })
    r = _post_event(e)
    assert r.status_code == 200
    assert db.invoices.count_documents({}) == before, \
        "Phase 9 `invoices` collection MUST NOT be mutated by 15.B"
    db.subscription_invoices.delete_one({"stripe_invoice_id": inv_id})
    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


# =====================================================================
# Security / payload hygiene
# =====================================================================

def test_billing_events_summary_never_exceeds_500_chars(db):
    # Send a known event and inspect the persisted row.
    barn_id, sub_id, _ = _seed_local_sub(db)
    e = _evt("customer.subscription.trial_will_end",
             {"id": sub_id, "trial_end": int(time.time()) + 1,
              "metadata": {"barn_id": barn_id}})
    _post_event(e)
    row = db.billing_events.find_one({"stripe_event_id": e["id"]})
    assert row and isinstance(row.get("summary"), str)
    assert len(row["summary"]) <= 500
    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_no_raw_stripe_payload_persisted_in_collections(db):
    """The summary string must NOT contain known payload-only keys."""
    forbidden_substrings = ["last_payment_error", "client_secret", "tax_ids", "discount"]
    barn_id, sub_id, customer_id = _seed_local_sub(db)
    e = _evt("invoice.paid", {
        "id": f"in_clean_{uuid.uuid4().hex[:6]}",
        "subscription": sub_id, "customer": customer_id,
        "amount_paid": 4900, "currency": "usd", "status": "paid",
        "payment_intent": f"pi_{uuid.uuid4().hex[:6]}",
    })
    _post_event(e)
    row = db.billing_events.find_one({"stripe_event_id": e["id"]})
    for s in forbidden_substrings:
        assert s not in (row.get("summary") or "")
    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


# =====================================================================
# Carryover from 15.A — webhook handler happy-path smoke for
# customer.subscription.updated. The deeper 502/retry_502 invariant is
# covered by:
#   - test_billing_events_first_delivery_failure_yields_502_and_retry_502_status
#     (checkout.session.completed → stripe.retrieve outage path)
#   - test_non_duplicate_db_insert_failure_raises_502_without_recursion
#     (motor write outage on the claim insert)
# =====================================================================

def test_subscription_updated_happy_path_smoke_200_and_status_ok(monkeypatch, db):
    """Smoke: a well-formed customer.subscription.updated on an existing
    local subscription returns 200 and lands billing_events.processing_status
    == 'ok'. The 502 / retry_502 paths are covered by the dedicated tests
    referenced in the comment block above this test.
    """
    barn_id, sub_id, _ = _seed_local_sub(db)
    e = _evt("customer.subscription.updated",
             {"id": sub_id, "status": "active",
              "items": {"data": [{"price": {"id": "price_local_monthly"}}]}})
    r = _post_event(e)
    assert r.status_code == 200
    row = db.billing_events.find_one({"stripe_event_id": e["id"]})
    assert row and row["processing_status"] == "ok"
    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


# =====================================================================
# Codex round-3 reliability fixes — focused regression tests
# =====================================================================

def test_retryable_metadata_miss_returns_non_2xx_then_replays_successfully(db):
    """Codex round-3 #1: a retryable metadata miss returns 503; once the
    local subscription row lands, a replay with the SAME event_id succeeds.
    """
    sub_id = f"sub_late_{uuid.uuid4().hex[:8]}"
    barn_id = f"barn_late_{uuid.uuid4().hex[:8]}"
    # No local subscription row yet — first delivery should 503.
    e = _evt("customer.subscription.trial_will_end",
             {"id": sub_id, "trial_end": int(time.time()) + 86400})
    r1 = _post_event(e)
    assert r1.status_code == 503, r1.text
    row = db.billing_events.find_one({"stripe_event_id": e["id"]})
    assert row["processing_status"] == "metadata_missing_retryable"

    # Now the local subscription lands (e.g., subscription.created caught up).
    db.subscriptions.insert_one({
        "id": sub_id, "stripe_subscription_id": sub_id, "barn_id": barn_id,
        "plan_tier_code": "starter", "status": "active",
        "pending_emails": [], "created_at": "x",
    })
    r2 = _post_event(e)
    assert r2.status_code == 200, r2.text
    row2 = db.billing_events.find_one({"stripe_event_id": e["id"]})
    assert row2["processing_status"] == "ok"
    sub = db.subscriptions.find_one({"id": sub_id})
    assert "trial_will_end" in sub["pending_emails"]

    db.subscriptions.delete_one({"id": sub_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_subscription_created_repairs_barn_pointer_and_entitlements(db):
    """Codex round-3 #4: customer.subscription.created (arriving before our
    checkout.session.completed in an out-of-order delivery) must stamp the
    barn pointer + entitlements snapshot.
    """
    barn_id = f"barn_created_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_created_{uuid.uuid4().hex[:8]}"
    db.barns.delete_one({"id": barn_id})  # ensure no pre-existing row
    db.plans.update_one({"tier_code": "starter"},
                        {"$setOnInsert": {
                            "id": "starter", "tier_code": "starter",
                            "feature_limits": {"horses": 50, "users": 5}}},
                        upsert=True)
    e = _evt("customer.subscription.created", {
        "id": sub_id, "status": "trialing",
        "metadata": {"barn_id": barn_id, "plan_tier_code": "starter",
                     "owner_user_id": "u", "billing_cycle": "monthly"},
        "items": {"data": [{"price": {"id": "p_x"}}]},
    })
    r = _post_event(e)
    assert r.status_code == 200, r.text
    barn = db.barns.find_one({"id": barn_id})
    assert barn is not None, "barn row must be upserted"
    assert barn["subscription_id"] == sub_id
    assert barn["subscription_entitlements"]["horses"] == 10
    db.subscriptions.delete_one({"stripe_subscription_id": sub_id})
    db.barns.delete_one({"id": barn_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_subscription_created_unknown_plan_does_not_lock_empty_entitlements(db):
    """BN15B: an unresolved created-event plan must remain retryable instead
    of writing an OK billing row with empty subscription/barn entitlements.
    """
    barn_id = f"barn_created_unknown_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_created_unknown_{uuid.uuid4().hex[:8]}"
    db.barns.delete_one({"id": barn_id})
    db.subscriptions.delete_one({"stripe_subscription_id": sub_id})
    e = _evt("customer.subscription.created", {
        "id": sub_id,
        "status": "active",
        "metadata": {"barn_id": barn_id, "plan_tier_code": "not_a_real_plan"},
        "items": {"data": [{"price": {"id": "price_unknown", "unit_amount": 9999}}]},
    })

    r = _post_event(e)
    assert r.status_code == 503, r.text
    assert db.subscriptions.find_one({"stripe_subscription_id": sub_id}) is None
    barn = db.barns.find_one({"id": barn_id})
    assert not barn or not barn.get("subscription_entitlements")
    row = db.billing_events.find_one({"stripe_event_id": e["id"]})
    assert row["processing_status"] == "metadata_missing_retryable"
    assert "plan_tier_code not resolvable" in row["summary"]

    db.barns.delete_one({"id": barn_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_subscription_created_normalizes_founder_plan_alias_metadata(db):
    """15R-C: webhook metadata may carry founder-facing Stripe lookup codes
    like trainer_lessons_15. The handler must store the canonical code and
    resolve real entitlements instead of writing an empty snapshot.
    """
    barn_id = f"barn_alias_cr_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_alias_cr_{uuid.uuid4().hex[:8]}"
    db.barns.delete_one({"id": barn_id})
    db.subscriptions.delete_one({"stripe_subscription_id": sub_id})
    db.account_subscriptions.delete_one({"account_id": barn_id})
    db.account_usage_limits.delete_one({"account_id": barn_id})
    db.plans.update_one(
        {"tier_code": "trainer_lesson_15"},
        {"$set": {
            "id": "trainer_lesson_15",
            "tier_code": "trainer_lesson_15",
            "feature_limits": {
                "horses": 15,
                "staff_seats": 3,
                "owner_manager_seats": 1,
                "lesson_participants": 15,
            },
        }},
        upsert=True,
    )
    e = _evt("customer.subscription.created", {
        "id": sub_id, "status": "active",
        "metadata": {"barn_id": barn_id, "plan_tier_code": "trainer_lessons_15",
                     "owner_user_id": "u", "billing_cycle": "monthly"},
        "items": {"data": [{"price": {"id": "price_alias", "unit_amount": 9999}}]},
    })

    r = _post_event(e)
    assert r.status_code == 200, r.text
    sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
    assert sub["plan_tier_code"] == "trainer_lesson_15"
    assert sub["entitlements_snapshot"]["lesson_participants"] == 15
    barn = db.barns.find_one({"id": barn_id})
    assert barn["subscription_entitlements"]["lesson_participants"] == 15
    usage_limits = db.account_usage_limits.find_one({"account_id": barn_id})
    assert usage_limits["plan_code"] == "trainer_lesson_15"
    assert usage_limits["lesson_participant_limit"] == 15

    db.subscriptions.delete_one({"stripe_subscription_id": sub_id})
    db.barns.delete_one({"id": barn_id})
    db.account_subscriptions.delete_one({"account_id": barn_id})
    db.account_usage_limits.delete_one({"account_id": barn_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_subscription_updated_upserts_when_no_local_row_but_metadata_present(db):
    """Codex round-3 #4 / round-4 blocker: with metadata.barn_id +
    plan_tier_code present but no local sub row, customer.subscription.updated
    must upsert a FULL subscription record (plan tier, entitlements snapshot)
    AND repair the barn pointer (subscription_id + subscription_entitlements
    mirror) — not a partial row.
    """
    barn_id = f"barn_upd_up_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_upd_up_{uuid.uuid4().hex[:8]}"
    db.barns.delete_one({"id": barn_id})
    db.subscriptions.delete_one({"stripe_subscription_id": sub_id})
    # Ensure plans catalog has a known canonical tier so entitlements_snapshot is
    # deterministic.
    db.plans.update_one(
        {"tier_code": "starter_barn"},
        {"$setOnInsert": {
            "id": "starter_barn", "tier_code": "starter_barn",
            "feature_limits": {"horses": 10, "staff_seats": 3},
        }},
        upsert=True,
    )
    e = _evt("customer.subscription.updated", {
        "id": sub_id, "status": "active",
        "metadata": {"barn_id": barn_id, "plan_tier_code": "starter",
                     "billing_cycle": "monthly", "owner_user_id": "u_x"},
        "items": {"data": [{"price": {"id": "price_x"}}]},
    })
    r = _post_event(e)
    assert r.status_code == 200, r.text

    # Subscription row upserted with FULL record.
    sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
    assert sub is not None, "subscription row must be upserted on update + metadata"
    assert sub["status"] == "active"
    assert sub["barn_id"] == barn_id
    assert sub["plan_tier_code"] == "starter_barn"
    assert sub.get("entitlements_snapshot", {}).get("horses") == 10
    assert sub.get("entitlements_snapshot", {}).get("staff_seats") == 3

    # Barn pointer + entitlements mirror repaired.
    barn = db.barns.find_one({"id": barn_id})
    assert barn is not None, "barn row must be upserted to repair pointer"
    assert barn["subscription_id"] == sub_id
    assert barn["subscription_entitlements"]["horses"] == 10
    assert barn["subscription_entitlements"]["staff_seats"] == 3

    # billing_events row closed as ok.
    row = db.billing_events.find_one({"stripe_event_id": e["id"]})
    assert row and row["processing_status"] == "ok"

    db.subscriptions.delete_one({"stripe_subscription_id": sub_id})
    db.barns.delete_one({"id": barn_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_subscription_updated_bootstrap_normalizes_founder_plan_alias_metadata(db):
    """15R-C: the no-local-row bootstrap path must normalize alias metadata
    before resolving plan rows and account limits.
    """
    barn_id = f"barn_alias_up_{uuid.uuid4().hex[:8]}"
    sub_id = f"sub_alias_up_{uuid.uuid4().hex[:8]}"
    db.barns.delete_one({"id": barn_id})
    db.subscriptions.delete_one({"stripe_subscription_id": sub_id})
    db.account_subscriptions.delete_one({"account_id": barn_id})
    db.account_usage_limits.delete_one({"account_id": barn_id})
    db.plans.update_one(
        {"tier_code": "trainer_lesson_50"},
        {"$set": {
            "id": "trainer_lesson_50",
            "tier_code": "trainer_lesson_50",
            "feature_limits": {
                "horses": 25,
                "staff_seats": 6,
                "owner_manager_seats": 3,
                "lesson_participants": 50,
            },
        }},
        upsert=True,
    )
    e = _evt("customer.subscription.updated", {
        "id": sub_id, "status": "active",
        "metadata": {"barn_id": barn_id, "plan_tier_code": "trainer_lessons_50",
                     "billing_cycle": "annual", "owner_user_id": "u_x"},
        "items": {"data": [{"price": {"id": "price_alias_50", "unit_amount": 179900}}]},
    })

    r = _post_event(e)
    assert r.status_code == 200, r.text
    sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
    assert sub["plan_tier_code"] == "trainer_lesson_50"
    assert sub["entitlements_snapshot"]["lesson_participants"] == 50
    usage_limits = db.account_usage_limits.find_one({"account_id": barn_id})
    assert usage_limits["plan_code"] == "trainer_lesson_50"
    assert usage_limits["horse_limit"] == 25
    assert usage_limits["lesson_participant_limit"] == 50

    db.subscriptions.delete_one({"stripe_subscription_id": sub_id})
    db.barns.delete_one({"id": barn_id})
    db.account_subscriptions.delete_one({"account_id": barn_id})
    db.account_usage_limits.delete_one({"account_id": barn_id})
    db.billing_events.delete_one({"stripe_event_id": e["id"]})


def test_non_duplicate_db_insert_failure_raises_502_without_recursion(monkeypatch):
    """Codex round-3 #2: a non-DuplicateKey DB error on the claim insert
    must surface 502 (Stripe replays) without infinite recursion.
    """
    from routes import subscriptions_webhook_handlers as h
    from fastapi import HTTPException

    class _Coll:
        async def find_one(self, *a, **k):
            return None
        async def insert_one(self, *a, **k):
            raise RuntimeError("simulated mongo write outage")
        async def update_one(self, *a, **k):
            return None
        async def count_documents(self, *a, **k):
            return 0
    class _StubDB:
        billing_events = _Coll()
        subscriptions = _Coll()
        barns = _Coll()
        plans = _Coll()
        subscription_invoices = _Coll()
        payments = _Coll()

    event = _evt("customer.subscription.updated",
                 {"id": f"sub_db_fail_{uuid.uuid4().hex[:6]}"})
    with pytest.raises(HTTPException) as ex:
        asyncio.run(h.process_event(_StubDB(), event))
    assert ex.value.status_code == 502
    assert "claim insert" in ex.value.detail.lower()


def test_stale_processing_lock_with_invalid_iso_does_not_crash(db):
    """Codex round-3 #3: an existing 'processing' row with a non-ISO
    processed_at value must NOT crash the dispatcher; it should be reclaimed.
    """
    event_id = f"evt_bad_iso_{uuid.uuid4().hex[:8]}"
    db.billing_events.insert_one({
        "id": event_id, "stripe_event_id": event_id,
        "event_type": "invoice.voided",
        "processing_status": "processing",
        "processed_at": "not-a-real-iso-timestamp",
        "retry_count": 0, "created_at": "x", "updated_at": "x",
    })
    e = _evt("invoice.voided", {"id": "in_bad_iso"}, event_id=event_id)
    r = _post_event(e)
    assert r.status_code == 200
    row = db.billing_events.find_one({"stripe_event_id": event_id})
    assert row["processing_status"] == "unknown_event"  # reclaimed + closed
    db.billing_events.delete_one({"stripe_event_id": event_id})
