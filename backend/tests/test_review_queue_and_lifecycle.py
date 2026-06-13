"""tests/test_review_queue_and_lifecycle.py — Phase 14 backend coverage.

Covers:
- Admin review-queue: list pending, approve, reject (soft, with reason),
  history endpoint, 403 for non-admins, 404 for missing user, 409 for
  already-decided.
- 7-day trial on signup: paid-tier signup sets trialing + trial_expires_at;
  /membership/start-trial endpoint flips status and consumes the trial
  (cannot be re-used).
- MVP billing lifecycle: /membership/cancel flips local subscription_status
  to cancelled without touching Stripe.
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


def _signup(role: str, *, tier: str | None = None):
    p = {
        "email": f"r14_{role}_{time.time_ns()}@test.com",
        "password": "phase14pass",
        "full_name": f"P14 {role}",
        "role": role,
    }
    if tier:
        p["tier"] = tier
    r = requests.post(f"{API}/auth/signup", json=p, timeout=15)
    assert r.status_code == 200, r.text
    return r.json()


def _admin_session():
    """Promote a fresh marketplace owner to admin and return its session.

    Uses a sync pymongo client (not motor) so we can mutate the user record
    without fighting motor's per-call event loop.
    """
    out = _signup("horse_owner")
    uid = out["user"]["id"]
    from pymongo import MongoClient
    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "test_database"
    client = MongoClient(mongo_url)
    client[db_name].users.update_one({"id": uid}, {"$set": {"role": "admin"}})
    client.close()
    r = requests.post(f"{API}/auth/login",
                      json={"email": out["user"]["email"], "password": "phase14pass"}, timeout=15)
    assert r.status_code == 200, r.text
    return r.json()["token"], uid


# ---------- Admin review queue ----------

def test_review_queue_lists_pending_user():
    trainer = _signup("trainer")
    tid = trainer["user"]["id"]
    admin_tok, _ = _admin_session()
    r = requests.get(f"{API}/admin/review-queue", headers={"Authorization": f"Bearer {admin_tok}"}, timeout=15)
    assert r.status_code == 200, r.text
    ids = [u["id"] for u in r.json()["items"]]
    assert tid in ids


def test_review_queue_forbidden_to_owners():
    owner = _signup("horse_owner")
    r = requests.get(f"{API}/admin/review-queue",
                     headers={"Authorization": f"Bearer {owner['token']}"}, timeout=15)
    assert r.status_code == 403


def test_review_queue_approve_flow():
    trainer = _signup("trainer")
    tid = trainer["user"]["id"]
    admin_tok, _ = _admin_session()
    h = {"Authorization": f"Bearer {admin_tok}"}
    r = requests.post(f"{API}/admin/review-queue/{tid}/approve", headers=h, timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["role_status"] == "approved"
    assert body.get("review_decided_at")
    # Repeat approve should 409.
    r2 = requests.post(f"{API}/admin/review-queue/{tid}/approve", headers=h, timeout=15)
    assert r2.status_code == 409


def test_review_queue_reject_with_reason():
    barn = _signup("barn_owner")
    bid = barn["user"]["id"]
    admin_tok, _ = _admin_session()
    h = {"Authorization": f"Bearer {admin_tok}"}
    r = requests.post(f"{API}/admin/review-queue/{bid}/reject",
                      json={"reason": "Insufficient credentials"}, headers=h, timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["role_status"] == "rejected"
    assert body["review_rejection_reason"] == "Insufficient credentials"
    # Soft reject — user still exists.
    me = requests.get(f"{API}/auth/me",
                      headers={"Authorization": f"Bearer {barn['token']}"}, timeout=15)
    assert me.status_code == 200
    assert me.json()["role_status"] == "rejected"


def test_review_queue_404_for_unknown_user():
    admin_tok, _ = _admin_session()
    h = {"Authorization": f"Bearer {admin_tok}"}
    r = requests.post(f"{API}/admin/review-queue/nope-nope/approve", headers=h, timeout=15)
    assert r.status_code == 404


def test_review_queue_history_lists_decisions():
    # Create a fresh rejected user so history is non-empty.
    trainer = _signup("trainer")
    tid = trainer["user"]["id"]
    admin_tok, _ = _admin_session()
    h = {"Authorization": f"Bearer {admin_tok}"}
    requests.post(f"{API}/admin/review-queue/{tid}/reject",
                  json={"reason": "test"}, headers=h, timeout=15)
    r = requests.get(f"{API}/admin/review-queue/history", headers=h, timeout=15)
    assert r.status_code == 200
    ids = [u["id"] for u in r.json()["items"]]
    assert tid in ids


# ---------- 7-day trial ----------

def test_paid_tier_signup_starts_trial():
    out = _signup("horse_owner", tier="owner_rider")
    u = out["user"]
    assert u["subscription_status"] == "trialing"
    assert u.get("trial_expires_at")
    assert u.get("trial_used") is True


def test_free_tier_signup_no_trial():
    out = _signup("horse_owner")  # default tier=free
    u = out["user"]
    assert u["subscription_status"] == "free"
    assert u.get("trial_expires_at") in (None, "")
    assert u.get("trial_used") is False


def test_start_trial_endpoint_idempotent_once():
    # Free signup → call /start-trial to begin a paid-tier trial.
    out = _signup("horse_owner")
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.post(f"{API}/membership/start-trial",
                      json={"tier": "owner_rider", "origin_url": BASE}, headers=h, timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user"]["subscription_status"] == "trialing"
    assert body["user"]["trial_used"] is True
    # Second call must 409.
    r2 = requests.post(f"{API}/membership/start-trial",
                       json={"tier": "barn_facility", "origin_url": BASE}, headers=h, timeout=15)
    assert r2.status_code == 409, r2.text


def test_start_trial_rejects_free_tier():
    out = _signup("horse_owner")
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.post(f"{API}/membership/start-trial",
                      json={"tier": "free", "origin_url": BASE}, headers=h, timeout=15)
    assert r.status_code == 400


# ---------- MVP billing lifecycle ----------

def test_cancel_membership_flips_local_status():
    # Trialing → cancelled.
    out = _signup("horse_owner", tier="owner_rider")
    h = {"Authorization": f"Bearer {out['token']}"}
    r = requests.post(f"{API}/membership/cancel", headers=h, timeout=15)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user"]["subscription_status"] == "cancelled"
    assert body["user"]["membership_tier"] == "free"
