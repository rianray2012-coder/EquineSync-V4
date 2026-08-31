from __future__ import annotations

from typing import Any, Dict, List

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from notifications import (
    _expected_twilio_signature,
    _hash_value,
    _is_sms_configured,
    _safe_sms_body,
    _twilio_basic_auth,
    build_router,
)


def _matches(doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
    for key, expected in (query or {}).items():
        if doc.get(key) != expected:
            return False
    return True


class _Collection:
    def __init__(self, rows=None):
        self.rows: List[Dict[str, Any]] = list(rows or [])

    async def find_one(self, query, projection=None):
        for row in self.rows:
            if _matches(row, query):
                return {k: v for k, v in row.items() if k != "_id"}
        return None

    async def insert_one(self, doc):
        self.rows.append(dict(doc))

    async def update_one(self, query, update, upsert=False):
        for row in self.rows:
            if _matches(row, query):
                row.update((update or {}).get("$set", {}))
                return type("UpdateResult", (), {"matched_count": 1})()
        if upsert:
            doc = dict(query)
            doc.update((update or {}).get("$set", {}))
            self.rows.append(doc)
        return type("UpdateResult", (), {"matched_count": 0})()

    async def update_many(self, query, update):
        count = 0
        for row in self.rows:
            if _matches(row, query):
                row.update((update or {}).get("$set", {}))
                count += 1
        return type("UpdateResult", (), {"matched_count": count, "modified_count": count})()

    async def create_index(self, *args, **kwargs):
        return None


class _FakeDB:
    def __init__(self):
        self.notifications = _Collection()
        self.notification_preferences = _Collection()
        self.sms_consent_records = _Collection()
        self.sms_delivery_events = _Collection()


def _client(user=None):
    db = _FakeDB()

    async def get_current_user():
        return dict(user or {"id": "founder-1", "role": "platform_admin", "barn_id": "barn-1"})

    app = FastAPI()
    app.include_router(build_router(db, get_current_user), prefix="/api")
    return TestClient(app), db


def test_sms_consent_stores_active_preference_and_hashed_audit_record():
    client, db = _client()

    response = client.put(
        "/api/notifications/sms-consent",
        json={
            "sms_enabled": True,
            "phone_number": "(816) 601-9036",
            "source": "contact_preferences",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["sms_enabled"] is True
    assert payload["sms_consent_status"] == "opted_in"
    assert payload["sms_phone_hash"] == _hash_value("+18166019036")
    assert "sms_phone_number" not in payload
    assert db.notification_preferences.rows[0]["sms_phone_number"] == "+18166019036"
    assert db.sms_consent_records.rows[0]["phone_hash"] == _hash_value("+18166019036")
    assert "phone_e164" not in db.sms_consent_records.rows[0]


def test_twilio_stop_keyword_opts_out_by_phone_hash_without_raw_event_storage():
    client, db = _client()
    db.notification_preferences.rows.append({
        "user_id": "founder-1",
        "sms_enabled": True,
        "sms_phone_number": "+18166019036",
        "sms_phone_hash": _hash_value("+18166019036"),
        "sms_consent_status": "opted_in",
    })

    response = client.post(
        "/api/notifications/sms/inbound",
        data={"From": "+18166019036", "Body": "STOP", "MessageSid": "SM123"},
    )

    assert response.status_code == 200
    assert "opted out" in response.text
    assert db.notification_preferences.rows[0]["sms_enabled"] is False
    assert db.notification_preferences.rows[0]["sms_consent_status"] == "opted_out"
    assert db.sms_delivery_events.rows[0]["phone_hash"] == _hash_value("+18166019036")
    assert "phone_e164" not in db.sms_delivery_events.rows[0]


def test_twilio_help_keyword_returns_branded_help_message():
    client, _db = _client()

    response = client.post(
        "/api/notifications/sms/inbound",
        data={"From": "+18166019036", "Body": "HELP", "MessageSid": "SM124"},
    )

    assert response.status_code == 200
    assert "EquineSync: For help" in response.text
    assert "Reply STOP" in response.text


def test_twilio_inbound_rejects_bad_signature_when_validation_enabled(monkeypatch):
    monkeypatch.setenv("TWILIO_VALIDATE_WEBHOOK_SIGNATURES", "true")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "test-token")
    monkeypatch.setenv("TWILIO_WEBHOOK_BASE_URL", "http://testserver")
    client, _db = _client()

    response = client.post(
        "/api/notifications/sms/inbound",
        data={"From": "+18166019036", "Body": "HELP", "MessageSid": "SM124"},
        headers={"X-Twilio-Signature": "invalid"},
    )

    assert response.status_code == 403


def test_twilio_inbound_accepts_valid_signature_when_validation_enabled(monkeypatch):
    monkeypatch.setenv("TWILIO_VALIDATE_WEBHOOK_SIGNATURES", "true")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "test-token")
    monkeypatch.setenv("TWILIO_WEBHOOK_BASE_URL", "http://testserver")
    client, _db = _client()
    params = {"From": "+18166019036", "Body": "HELP", "MessageSid": "SM124"}
    signature = _expected_twilio_signature(
        "http://testserver/api/notifications/sms/inbound",
        params,
        "test-token",
    )

    response = client.post(
        "/api/notifications/sms/inbound",
        data=params,
        headers={"X-Twilio-Signature": signature},
    )

    assert response.status_code == 200
    assert "EquineSync: For help" in response.text


def test_twilio_status_callback_logs_status_without_raw_phone():
    client, db = _client()

    response = client.post(
        "/api/notifications/sms/status",
        data={
            "MessageSid": "SM125",
            "MessageStatus": "delivered",
            "To": "+18166019036",
            "ErrorCode": "",
        },
    )

    assert response.status_code == 200
    row = db.sms_delivery_events.rows[0]
    assert row["message_sid"] == "SM125"
    assert row["status"] == "delivered"
    assert row["phone_hash"] == _hash_value("+18166019036")
    assert "phone_e164" not in row


def test_sms_proof_send_is_blocked_until_live_sending_is_enabled(monkeypatch):
    monkeypatch.delenv("TWILIO_SMS_ENABLED", raising=False)
    client, _db = _client()

    response = client.post(
        "/api/notifications/sms/proof-send",
        json={"phone_number": "+18166019036"},
    )

    assert response.status_code == 409


def test_sms_config_accepts_twilio_api_key_credentials(monkeypatch):
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "AC123")
    monkeypatch.setenv("TWILIO_MESSAGING_SERVICE_SID", "MG123")
    monkeypatch.delenv("TWILIO_AUTH_TOKEN", raising=False)
    monkeypatch.setenv("TWILIO_API_KEY_SID", "SK123")
    monkeypatch.setenv("TWILIO_API_KEY_SECRET", "secret")

    assert _is_sms_configured() is True
    assert _twilio_basic_auth() == ("SK123", "secret")


def test_sms_config_still_accepts_twilio_auth_token(monkeypatch):
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "AC123")
    monkeypatch.setenv("TWILIO_MESSAGING_SERVICE_SID", "MG123")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "token")
    monkeypatch.delenv("TWILIO_API_KEY_SID", raising=False)
    monkeypatch.delenv("TWILIO_API_KEY_SECRET", raising=False)

    assert _is_sms_configured() is True
    assert _twilio_basic_auth() == ("AC123", "token")


def test_sms_safe_body_rejects_sensitive_detail_terms():
    with pytest.raises(Exception):
        _safe_sms_body(
            "EquineSync: A minor account detail is ready. Reply STOP to opt out or HELP for help."
        )
