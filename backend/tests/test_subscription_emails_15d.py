"""Phase 15.D — Subscription email dispatcher tests.

Covers:
  1. Happy path: a pending event key is sent + pulled, log row marked `sent`.
  2. Per-key retry: a mailer failure keeps the key on the queue, increments
     attempt, and on the 5th attempt promotes to permanent_failure.
  3. Unknown event keys are pulled (and logged as permanent_failure) so they
     never block the queue.
  4. No recipient (owner_user_id has no email) → failed, retried.
  5. Dev-mode mailer (status="dev") counts as success.
  6. Subjects + brand copy use the approved "EquineSync" display name.
  7. Manual trigger endpoint:
     - returns 403 for a non-admin
     - returns 200 + stats for admin:access role
"""
from __future__ import annotations

import asyncio
import os
import time
import uuid

import pytest

# Force-load the same env the live app uses so MONGO_URL etc. resolve.
import dotenv
dotenv.load_dotenv("/app/backend/.env")

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db():
    """Sync handle for test setup/cleanup."""
    import pymongo
    client = pymongo.MongoClient(MONGO_URL)
    yield client[DB_NAME]
    client.close()


def _run(coro_factory):
    """Sync→async bridge. ``coro_factory`` must be a no-arg callable that
    constructs the coroutine (and any motor client) inside the new event
    loop — motor clients cannot be reused across loops.
    """
    async def runner():
        client = AsyncIOMotorClient(MONGO_URL)
        try:
            return await coro_factory(client[DB_NAME])
        finally:
            client.close()
    return asyncio.run(runner())


@pytest.fixture(autouse=True)
def _purge_stale_15d_rows(db):
    """Phase 15.D test hygiene — any subscription with id starting `sub_15d_`
    is from a prior run and must be cleared before each test so stats
    assertions count only this run's rows."""
    db.subscriptions.delete_many({"stripe_subscription_id": {"$regex": "^sub_15d_"}})
    db.subscription_email_log.delete_many({"subscription_id": {"$regex": "^sub_15d_"}})
    yield


@pytest.fixture
def seed_user(db):
    """Insert a barn-manager-style user with a known email."""
    uid = f"u_15d_{uuid.uuid4().hex[:8]}"
    email = f"{uid}@test.com"
    db.users.insert_one({
        "id": uid, "email": email, "full_name": "Test Owner",
        "role": "barn_manager",
    })
    yield uid, email
    db.users.delete_one({"id": uid})


@pytest.fixture
def seed_admin(db):
    """Insert an `admin`-role user for the manual trigger test."""
    uid = f"adm_15d_{uuid.uuid4().hex[:8]}"
    db.users.insert_one({
        "id": uid, "email": f"{uid}@test.com", "full_name": "Admin Tester",
        "role": "admin", "password_hash": "x",
    })
    yield uid
    db.users.delete_one({"id": uid})


def _make_sub(db, *, owner_user_id, pending, plan_tier="starter"):
    sid = f"sub_15d_{uuid.uuid4().hex[:8]}"
    db.subscriptions.insert_one({
        "id": sid,
        "stripe_subscription_id": sid,
        "barn_id": "primary",
        "owner_user_id": owner_user_id,
        "plan_tier_code": plan_tier,
        "billing_cycle": "monthly",
        "status": "trialing",
        "pending_emails": list(pending),
        "trial_end": "2026-03-01T12:00:00+00:00",
        "current_period_end": "2026-04-01T12:00:00+00:00",
        "created_at": "2026-02-15T00:00:00+00:00",
    })
    return sid


def _cleanup(db, sub_id):
    db.subscriptions.delete_one({"stripe_subscription_id": sub_id})
    db.subscription_email_log.delete_many({"subscription_id": sub_id})


# ---------------------------------------------------------------------------
# Mock mailer
# ---------------------------------------------------------------------------

class _Mailer:
    """Captures send() calls. ``mode`` selects behavior; uses the REAL mailer
    contract statuses (see backend/mailer.py::send)."""

    def __init__(self, mode="sent"):
        # mode: "sent" | "dev_logged" | "sandbox" | "error" | "raise"
        self.mode = mode
        self.calls = []

    async def send(self, *, to, subject, template=None, variables=None,
                   html=None, text=None, base="_base"):
        self.calls.append({
            "to": to, "subject": subject, "template": template,
            "variables": variables, "base": base,
        })
        if self.mode == "sent":
            return {"status": "sent", "id": f"msg_{len(self.calls)}", "dev": False}
        if self.mode == "dev_logged":
            return {"status": "dev_logged", "dev": True}
        if self.mode == "sandbox":
            return {"status": "sandbox", "dev": True,
                    "error": "verify a domain at resend.com/domains"}
        if self.mode == "raise":
            raise RuntimeError("mailer exploded")
        return {"status": "error", "error": "smtp down"}


def _handle(m: _Mailer):
    return {"send": m.send}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_happy_path_sent_and_pulled(db, seed_user):
    from services.subscription_email_dispatcher import run_subscription_email_pass

    uid, email = seed_user
    sub_id = _make_sub(db, owner_user_id=uid, pending=["trial_will_end"])
    try:
        m = _Mailer("sent")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["sent"] == 1
        sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
        assert "trial_will_end" not in (sub.get("pending_emails") or [])
        log = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "trial_will_end"})
        assert log["status"] == "sent"
        assert log["attempt"] == 1
        call = m.calls[0]
        assert call["to"] == email
        assert "EquineSync" in call["subject"]
        assert call["subject"] == "EquineSync — your trial ends soon"
        assert call["variables"]["full_name"] == "Test Owner"
        assert call["variables"]["plan_name"] == "Starter"
        assert call["variables"]["subscription_url"].endswith("/billing/subscription")
    finally:
        _cleanup(db, sub_id)


def test_retries_keep_key_then_permanent_after_max_attempts(db, seed_user):
    from services.subscription_email_dispatcher import run_subscription_email_pass, MAX_ATTEMPTS

    uid, _ = seed_user
    sub_id = _make_sub(db, owner_user_id=uid, pending=["payment_failed"])
    try:
        m = _Mailer("error")
        for i in range(1, MAX_ATTEMPTS):
            stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
            assert stats["failed"] == 1, f"pass {i}: expected failed=1"
            assert stats["permanent_failures"] == 0
            sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
            assert "payment_failed" in sub["pending_emails"], \
                f"pass {i}: key should remain on queue while retrying"
            log = db.subscription_email_log.find_one(
                {"subscription_id": sub_id, "event_key": "payment_failed"})
            assert log["attempt"] == i
            assert log["status"] == "failed"
            assert log["last_error"] == "smtp down"

        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["permanent_failures"] == 1
        sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
        assert "payment_failed" not in (sub.get("pending_emails") or [])
        log = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "payment_failed"})
        assert log["status"] == "permanent_failure"
        assert log["attempt"] == MAX_ATTEMPTS
    finally:
        _cleanup(db, sub_id)


def test_unknown_event_key_is_pulled_with_permanent_failure(db, seed_user):
    from services.subscription_email_dispatcher import run_subscription_email_pass

    uid, _ = seed_user
    sub_id = _make_sub(db, owner_user_id=uid,
                      pending=["trial_will_end", "totally_made_up_key"])
    try:
        m = _Mailer("sent")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["sent"] == 1
        assert stats["unknown_pulled"] == 1
        sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
        assert sub["pending_emails"] == []
        unknown_log = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "totally_made_up_key"})
        assert unknown_log["status"] == "permanent_failure"
        assert unknown_log["last_error"] == "unknown_event_key"
    finally:
        _cleanup(db, sub_id)


def test_no_recipient_when_user_missing(db):
    from services.subscription_email_dispatcher import run_subscription_email_pass

    sub_id = _make_sub(db, owner_user_id="nope_user_x",
                      pending=["payment_succeeded"])
    try:
        m = _Mailer("sent")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["failed"] == 1
        assert stats["sent"] == 0
        sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
        assert "payment_succeeded" in sub["pending_emails"]
        log = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "payment_succeeded"})
        assert log["status"] == "failed"
        assert log["last_error"] == "no_recipient_email"
    finally:
        _cleanup(db, sub_id)


def test_dev_logged_status_counts_as_sent(db, seed_user):
    from services.subscription_email_dispatcher import run_subscription_email_pass

    uid, _ = seed_user
    sub_id = _make_sub(db, owner_user_id=uid, pending=["payment_succeeded"])
    try:
        m = _Mailer("dev_logged")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["sent"] == 1
        sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
        assert "payment_succeeded" not in (sub.get("pending_emails") or [])
        log = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "payment_succeeded"})
        assert log["status"] == "sent"
    finally:
        _cleanup(db, sub_id)


def test_sandbox_status_counts_as_sent(db, seed_user):
    """Round-2 blocker #1: backend/mailer.py returns status="sandbox" when
    Resend rejects a recipient on the unverified-domain sandbox. The rest of
    the codebase (invites.py, auth.py) treats that as delivered; the
    dispatcher must too — otherwise live sandbox sends would loop into
    permanent_failure on dev/staging environments."""
    from services.subscription_email_dispatcher import run_subscription_email_pass

    uid, _ = seed_user
    sub_id = _make_sub(db, owner_user_id=uid, pending=["trial_will_end"])
    try:
        m = _Mailer("sandbox")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["sent"] == 1, "sandbox must count as delivered"
        sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
        assert "trial_will_end" not in (sub.get("pending_emails") or [])
        log = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "trial_will_end"})
        assert log["status"] == "sent"
    finally:
        _cleanup(db, sub_id)


def test_live_sent_status_counts_as_sent(db, seed_user):
    """Round-2 blocker #1: backend/mailer.py returns status="sent" on a real
    Resend success — NOT "ok". Earlier dispatcher version only accepted
    "ok"/"dev", which would mark every real send as failed. Locks the live
    success path explicitly so this regression cannot return."""
    from services.subscription_email_dispatcher import run_subscription_email_pass

    uid, _ = seed_user
    sub_id = _make_sub(db, owner_user_id=uid, pending=["trial_will_end"])
    try:
        m = _Mailer("sent")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["sent"] == 1
        log = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "trial_will_end"})
        assert log["status"] == "sent"
        assert log.get("message_id", "").startswith("msg_")
    finally:
        _cleanup(db, sub_id)


def test_mailer_raises_is_isolated_and_counted_as_failed(db, seed_user):
    from services.subscription_email_dispatcher import run_subscription_email_pass

    uid, _ = seed_user
    sub_id = _make_sub(db, owner_user_id=uid, pending=["trial_will_end"])
    try:
        m = _Mailer("raise")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["failed"] == 1
        sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
        assert "trial_will_end" in sub["pending_emails"]
        log = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "trial_will_end"})
        assert log["status"] == "failed"
        assert "mailer exploded" in (log.get("last_error") or "")
    finally:
        _cleanup(db, sub_id)


def test_empty_queue_is_a_noop():
    from services.subscription_email_dispatcher import run_subscription_email_pass

    m = _Mailer("sent")
    stats_before = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
    assert set(stats_before.keys()) == {
        "scanned", "sent", "failed", "permanent_failures", "unknown_pulled",
    }


def test_payment_succeeded_reads_15b_invoice_schema(db, seed_user):
    """Round-2 blocker #2: dispatcher must read the invoice doc using the
    real 15.B schema produced by `_upsert_subscription_invoice`:
      - lookup key:  `subscription_id` (NOT `stripe_subscription_id`)
      - amount field: `amount_cents` (NOT `amount_paid_cents`/`amount_due_cents`)
      - paid timestamp: `paid_at` (set via extra_set on payment_succeeded)
    Seeded here with the EXACT field names a real 15.B webhook would write.
    """
    from services.subscription_email_dispatcher import run_subscription_email_pass

    uid, _ = seed_user
    sub_id = _make_sub(db, owner_user_id=uid,
                      pending=["payment_succeeded"], plan_tier="professional")
    inv_id = f"in_15d_{uuid.uuid4().hex[:8]}"
    # Schema mirrors backend/routes/subscriptions_webhook_handlers
    # _upsert_subscription_invoice exactly.
    db.subscription_invoices.insert_one({
        "id": inv_id,
        "barn_id": "primary",
        "subscription_id": sub_id,                # NOT stripe_subscription_id
        "stripe_invoice_id": inv_id,
        "stripe_customer_id": "cus_test",
        "amount_cents": 14900,                    # NOT amount_paid_cents
        "currency": "usd",
        "status": "paid",
        "hosted_invoice_url": "https://invoice.stripe.com/x",
        "invoice_pdf_url": "https://invoice.stripe.com/x.pdf",
        "period_start": "2026-02-01T00:00:00+00:00",
        "period_end":   "2026-03-01T00:00:00+00:00",
        "due_date": None,
        "paid_at": "2026-02-20T10:00:00+00:00",   # via extra_set
        "payment_failure_count": 0,
        "created_at": "2026-02-20T10:00:00+00:00",
        "updated_at": "2026-02-20T10:00:00+00:00",
    })
    try:
        m = _Mailer("sent")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["sent"] == 1
        call = m.calls[0]
        assert call["subject"] == "EquineSync — payment received, you're all set"
        vars_ = call["variables"]
        # Bug regression — must resolve to $149 from amount_cents, not "—".
        assert vars_["amount_friendly"] == "$149", \
            f"expected $149 from amount_cents, got {vars_['amount_friendly']!r}"
        assert vars_["invoice_ref"] == inv_id, \
            f"expected real invoice id, got {vars_['invoice_ref']!r}"
        assert vars_["plan_name"] == "Professional"
        assert vars_["paid_at_friendly"].startswith(("February", "Feb"))
    finally:
        _cleanup(db, sub_id)
        db.subscription_invoices.delete_one({"stripe_invoice_id": inv_id})


def test_payment_failed_reads_15b_invoice_schema_with_payment_failed_at(db, seed_user):
    """Companion to the succeeded test — `payment_failed` reads
    `payment_failed_at` (set in _h_invoice_payment_failed) instead of
    `paid_at`. Also exercises the `amount_cents` field on a failed invoice
    (the 15.B handler stores amount_due there)."""
    from services.subscription_email_dispatcher import run_subscription_email_pass

    uid, _ = seed_user
    sub_id = _make_sub(db, owner_user_id=uid,
                      pending=["payment_failed"], plan_tier="starter")
    inv_id = f"in_15d_{uuid.uuid4().hex[:8]}"
    db.subscription_invoices.insert_one({
        "id": inv_id,
        "barn_id": "primary",
        "subscription_id": sub_id,
        "stripe_invoice_id": inv_id,
        "stripe_customer_id": "cus_test",
        "amount_cents": 4900,
        "currency": "usd",
        "status": "open",
        "hosted_invoice_url": "https://invoice.stripe.com/x",
        "invoice_pdf_url": "https://invoice.stripe.com/x.pdf",
        "payment_failed_at": "2026-02-22T03:00:00+00:00",
        "payment_failure_count": 1,
        "created_at": "2026-02-22T03:00:00+00:00",
        "updated_at": "2026-02-22T03:00:00+00:00",
    })
    try:
        m = _Mailer("sent")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m)))
        assert stats["sent"] == 1
        call = m.calls[0]
        assert call["subject"] == "EquineSync — payment issue, please review"
        vars_ = call["variables"]
        assert vars_["amount_friendly"] == "$49"
        assert vars_["invoice_ref"] == inv_id
        assert vars_["plan_name"] == "Starter"
    finally:
        _cleanup(db, sub_id)
        db.subscription_invoices.delete_one({"stripe_invoice_id": inv_id})


def test_requeue_after_terminal_resets_attempt_counter(db, seed_user):
    """Round-2 policy fix: when a key is re-queued after a previous terminal
    state (sent / permanent_failure), the dispatcher must reset the attempt
    counter so the new occurrence gets a fresh retry budget — not be
    silently pulled because the old counter was already >= MAX_ATTEMPTS.

    Models the realistic lifecycle:
      1. payment_failed → 5 attempts → permanent_failure  (old, ages ago)
      2. Customer updates card; a renewal succeeds later → a new
         `payment_succeeded` lands AND, separately, a different invoice
         fails → 15.B re-puts `payment_failed` on the queue via $addToSet.
      3. The dispatcher's next pass MUST treat this as a fresh send, not
         immediately promote it to permanent_failure again.
    """
    from services.subscription_email_dispatcher import run_subscription_email_pass, MAX_ATTEMPTS

    uid, _ = seed_user
    sub_id = _make_sub(db, owner_user_id=uid, pending=["payment_failed"])
    try:
        # Step 1: burn through MAX_ATTEMPTS to land in permanent_failure.
        m_fail = _Mailer("error")
        for _ in range(MAX_ATTEMPTS):
            _run(lambda adb: run_subscription_email_pass(adb, _handle(m_fail)))
        log = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "payment_failed"})
        assert log["status"] == "permanent_failure"
        assert log["attempt"] == MAX_ATTEMPTS

        # Step 2: simulate 15.B re-queuing the same key (renewal-cycle
        # failure) — exactly what $addToSet would do on a fresh webhook.
        db.subscriptions.update_one(
            {"stripe_subscription_id": sub_id},
            {"$addToSet": {"pending_emails": "payment_failed"}},
        )

        # Step 3: now the mailer is healthy. The re-queued key must SEND,
        # not be silently pulled.
        m_ok = _Mailer("sent")
        stats = _run(lambda adb: run_subscription_email_pass(adb, _handle(m_ok)))
        assert stats["sent"] == 1, \
            "re-queued key after terminal state must be re-sent, not dropped"
        sub = db.subscriptions.find_one({"stripe_subscription_id": sub_id})
        assert "payment_failed" not in (sub.get("pending_emails") or [])
        log_after = db.subscription_email_log.find_one(
            {"subscription_id": sub_id, "event_key": "payment_failed"})
        assert log_after["status"] == "sent"
        # The reset wiped the old counter; this occurrence is attempt 1.
        assert log_after["attempt"] == 1
        # The previous terminal state is preserved as a forensic breadcrumb.
        assert log_after.get("previous_terminal_status") == "permanent_failure"
    finally:
        _cleanup(db, sub_id)


# ---------------------------------------------------------------------------
# HTTP — manual trigger endpoint
# ---------------------------------------------------------------------------

import requests

API = os.environ["REACT_APP_BACKEND_URL"].rstrip("/") + "/api" \
    if "REACT_APP_BACKEND_URL" in os.environ \
    else "http://localhost:8001/api"


def _mint_session(db, role: str) -> str:
    """Create a user with `role` and call /auth/login to mint a JWT.

    Uses the same _login helper pattern as test_owner_trust_edges.py.
    """
    import bcrypt
    email = f"15d_{role}_{uuid.uuid4().hex[:8]}@test.com"
    pwd = "TestPass123!"
    pwd_hash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    uid = f"u_15d_{uuid.uuid4().hex[:8]}"
    db.users.insert_one({
        "id": uid, "email": email, "full_name": "x", "role": role,
        "password_hash": pwd_hash, "barn_id": "primary",
        "role_status": "active",
    })
    r = requests.post(f"{API}/auth/login",
                      json={"email": email, "password": pwd}, timeout=15)
    assert r.status_code == 200, r.text
    return r.json()["token"], uid


def test_manual_trigger_endpoint_forbidden_for_non_admin(db):
    token, uid = _mint_session(db, "barn_manager")
    try:
        r = requests.post(
            f"{API}/admin/subscriptions/email-pass",
            headers={"Authorization": f"Bearer {token}"}, timeout=15)
        assert r.status_code == 403, r.text
    finally:
        db.users.delete_one({"id": uid})


def test_manual_trigger_endpoint_ok_for_admin(db):
    token, uid = _mint_session(db, "admin")
    try:
        r = requests.post(
            f"{API}/admin/subscriptions/email-pass",
            headers={"Authorization": f"Bearer {token}"}, timeout=20)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["ok"] is True
        assert set(body["stats"].keys()) == {
            "scanned", "sent", "failed", "permanent_failures", "unknown_pulled"
        }
    finally:
        db.users.delete_one({"id": uid})
