"""Pilot support/feedback intake proof.

Authenticated users can submit support tickets into the Admin Portal inbox.
Audit metadata must stay routing-only and must not contain the tester's
free-text report body.
"""
from __future__ import annotations

import os
import pathlib
import sys
import uuid

import pytest
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

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
    email = f"support_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={
            "email": email,
            "password": "securepass1",
            "full_name": "Support Intake Test",
            "role": role,
        },
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _promote(db, user_id: str, platform_role: str):
    db.users.update_one({"id": user_id}, {"$set": {"platform_role": platform_role}})


def _bearer(session: dict) -> dict:
    return {"Authorization": f"Bearer {session['token']}"}


def test_authenticated_support_ticket_lands_in_admin_inbox_without_body_in_audit(db):
    session = _signup("horse_owner")
    secret_phrase = f"FREE_TEXT_BODY_{uuid.uuid4().hex}"

    response = requests.post(
        f"{API}/support/tickets",
        headers=_bearer(session),
        json={
            "category": "access",
            "severity": "high",
            "subject": "Owner dashboard denied after login",
            "message": f"{secret_phrase} role home showed the wrong facility.",
            "page_url": "https://app.equine-sync.com/dashboard/owner",
            "device_context": "pytest browser proof",
            "preferred_contact": "email",
        },
        timeout=15,
    )
    assert response.status_code == 201, response.text
    created = response.json()["ticket"]
    assert created["admin_ref"].startswith("st_")
    assert created["status"] == "new"

    ticket = db.support_tickets.find_one({"id": created["id"]})
    try:
        assert ticket is not None
        assert ticket["source"] == "pilot_support_form"
        assert ticket["channel"] == "in_app_pilot"
        assert ticket["category"] == "access"
        assert ticket["severity"] == "high"
        assert ticket["submitter_user_id"] == session["user"]["id"]
        assert secret_phrase in ticket["description"]

        audit_row = db.audit_log.find_one(
            {"action": "support.ticket.create", "resource_id": created["id"]},
            {"_id": 0, "metadata": 1},
        )
        assert audit_row is not None
        assert audit_row["metadata"] == {
            "category": "access",
            "severity": "high",
            "channel": "in_app_pilot",
            "message_present": True,
            "page_url_present": True,
            "device_context_present": True,
        }
        assert secret_phrase not in str(audit_row)

        admin = _signup("horse_owner")
        _promote(db, admin["user"]["id"], "support_admin")
        inbox = requests.get(
            f"{API}/admin/portal/support?q=Owner%20dashboard%20denied&limit=5",
            headers=_bearer(admin),
            timeout=15,
        )
        assert inbox.status_code == 200, inbox.text
        items = inbox.json()["items"]
        row = next((item for item in items if item["admin_ref"] == created["admin_ref"]), None)
        assert row is not None
        assert row["category"] == "access"
        assert row["severity"] == "high"
    finally:
        db.support_tickets.delete_many({"id": created["id"]})
        db.audit_log.delete_many({"resource_id": created["id"]})
