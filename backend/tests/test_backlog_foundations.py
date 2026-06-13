"""Regression coverage for additive feature-backlog foundations."""
import os
import uuid

import pytest
import requests

from ._test_creds import ADMIN, OWNER, DEMO_PASSWORD


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://preflight-check-8.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"


def _login(email, password):
    r = requests.post(f"{API}/auth/login", json={"email": email, "password": password}, timeout=30)
    assert r.status_code == 200, r.text
    return r.json()["token"]


@pytest.fixture(scope="module")
def admin_h():
    return {"Authorization": f"Bearer {_login(ADMIN['email'], ADMIN['password'])}"}


@pytest.fixture(scope="module")
def owner_h():
    return {"Authorization": f"Bearer {_login(OWNER['email'], DEMO_PASSWORD)}"}


def test_feature_modules_catalog_is_role_filtered(admin_h, owner_h):
    admin = requests.get(f"{API}/feature-modules", headers=admin_h, timeout=30)
    assert admin.status_code == 200, admin.text
    admin_keys = {m["key"] for m in admin.json()}
    assert {"stall-map", "payments", "staff-scheduling", "ai-automation"}.issubset(admin_keys)

    owner = requests.get(f"{API}/feature-modules", headers=owner_h, timeout=30)
    assert owner.status_code == 200, owner.text
    owner_keys = {m["key"] for m in owner.json()}
    assert "health-reminders" not in owner_keys
    assert "staff-scheduling" not in owner_keys


def test_feature_record_validation_and_audit_fields(admin_h):
    missing = requests.post(
        f"{API}/feature-modules/waitlist/records",
        headers=admin_h,
        json={"data": {"horse_name": "TEST_missing_client"}},
        timeout=30,
    )
    assert missing.status_code == 422

    suffix = uuid.uuid4().hex[:8]
    payload = {
        "data": {
            "client_name": f"TEST Waitlist {suffix}",
            "horse_name": "TEST Prospect",
            "service_type": "board",
            "priority": "high",
            "target_date": "2026-09-01",
        },
    }
    created = requests.post(
        f"{API}/feature-modules/waitlist/records",
        headers=admin_h,
        json=payload,
        timeout=30,
    )
    assert created.status_code == 200, created.text
    body = created.json()
    assert body["data"]["client_name"] == payload["data"]["client_name"]
    for key in ["id", "barn_id", "created_at", "updated_at", "created_by", "updated_by"]:
        assert body.get(key), key

    listed = requests.get(f"{API}/feature-modules/waitlist", headers=admin_h, timeout=30)
    assert listed.status_code == 200
    assert any(r["id"] == body["id"] for r in listed.json()["records"])


def test_owner_cannot_write_staff_records(owner_h):
    r = requests.post(
        f"{API}/feature-modules/staff-scheduling/records",
        headers=owner_h,
        json={"data": {"staff_name": "TEST Staff", "shift_start": "2026-09-01T07:00:00"}},
        timeout=30,
    )
    assert r.status_code == 403


def test_backlog_dashboard_and_integration_placeholders(admin_h):
    d = requests.get(f"{API}/reports/backlog-dashboard", headers=admin_h, timeout=30)
    assert d.status_code == 200, d.text
    body = d.json()
    assert "occupancy" in body and "financial" in body and "exports" in body
    assert body["exports"]["excel"] == "export_ready"

    p = requests.get(f"{API}/integrations/placeholders", headers=admin_h, timeout=30)
    assert p.status_code == 200
    providers = {x["provider"] for x in p.json()}
    assert {"stripe", "quickbooks", "google_calendar", "qr_horse_id"}.issubset(providers)
