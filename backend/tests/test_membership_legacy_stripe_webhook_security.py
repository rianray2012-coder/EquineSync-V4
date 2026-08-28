from __future__ import annotations

import hmac
import hashlib
import json
import logging
import time
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.membership import build_router as build_membership_router
from routes.subscriptions import build_router as build_subscriptions_router


WEBHOOK_SECRET = "whsec_legacy_route_test"


def _payload(event_type: str | None, session: dict[str, Any], event_id: str = "evt_legacy") -> bytes:
    event = {
        "id": event_id,
        "object": "event",
        "data": {"object": {"object": "checkout.session", **session}},
    }
    if event_type is not None:
        event["type"] = event_type
    return json.dumps(event, separators=(",", ":")).encode("utf-8")


def _stripe_signature(payload: bytes, secret: str = WEBHOOK_SECRET, timestamp: int | None = None) -> str:
    ts = int(timestamp or time.time())
    signed_payload = f"{ts}.".encode("utf-8") + payload
    digest = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return f"t={ts},v1={digest}"


class _UpdateResult:
    def __init__(self, matched_count: int):
        self.matched_count = matched_count


class _FakeCollection:
    def __init__(self, rows: list[dict[str, Any]] | None = None):
        self.rows = rows or []
        self.update_calls: list[tuple[dict[str, Any], dict[str, Any]]] = []
        self.find_calls: list[dict[str, Any]] = []

    async def find_one(self, query: dict[str, Any], projection: dict[str, Any] | None = None):
        self.find_calls.append(dict(query))
        for row in self.rows:
            if all(row.get(key) == value for key, value in query.items()):
                return row
        return None

    async def update_one(self, query: dict[str, Any], update: dict[str, Any]):
        self.update_calls.append((dict(query), dict(update)))
        for row in self.rows:
            if all(row.get(key) == value for key, value in query.items()):
                row.update(update.get("$set", {}))
                return _UpdateResult(1)
        return _UpdateResult(0)


class _FakeDb:
    def __init__(self):
        self.payment_transactions = _FakeCollection(
            [
                {
                    "session_id": "cs_complete",
                    "user_id": "user_1",
                    "tier": "owner_rider",
                    "payment_status": "unpaid",
                    "status": "pending",
                },
                {
                    "session_id": "cs_expired",
                    "user_id": "user_2",
                    "tier": "trainer_provider",
                    "payment_status": "unpaid",
                    "status": "pending",
                },
            ]
        )
        self.users = _FakeCollection(
            [
                {
                    "id": "user_1",
                    "membership_tier": "free",
                    "subscription_status": "trialing",
                    "trial_expires_at": "2026-01-01T00:00:00+00:00",
                },
                {
                    "id": "user_2",
                    "membership_tier": "free",
                    "subscription_status": "trialing",
                    "trial_expires_at": "2026-01-01T00:00:00+00:00",
                },
            ]
        )


async def _fake_get_current_user():
    return {"id": "user_1", "role": "admin"}


@pytest.fixture
def legacy_client(monkeypatch):
    monkeypatch.setenv("STRIPE_API_KEY", "sk_test_legacy_route")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    db = _FakeDb()
    app = FastAPI()
    app.include_router(
        build_membership_router(db=db, get_current_user=_fake_get_current_user),
        prefix="/api",
    )
    return TestClient(app), db


def _post_legacy(client: TestClient, payload: bytes, signature: str | None):
    headers = {"Stripe-Signature": signature} if signature is not None else {}
    return client.post("/api/webhook/stripe", content=payload, headers=headers)


def test_legacy_webhook_rejects_missing_webhook_secret(monkeypatch, legacy_client):
    client, db = legacy_client
    monkeypatch.delenv("STRIPE_WEBHOOK_SECRET", raising=False)
    payload = _payload("checkout.session.completed", {"id": "cs_complete", "payment_status": "paid"})

    response = _post_legacy(client, payload, _stripe_signature(payload))

    assert response.status_code == 500
    assert response.json()["detail"] == "Stripe webhook signing is not configured."
    assert db.users.update_calls == []
    assert db.payment_transactions.update_calls == []


def test_legacy_webhook_rejects_missing_stripe_signature(legacy_client):
    client, db = legacy_client
    payload = _payload("checkout.session.completed", {"id": "cs_complete", "payment_status": "paid"})

    response = _post_legacy(client, payload, signature=None)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid webhook signature."
    assert db.users.update_calls == []
    assert db.payment_transactions.update_calls == []


def test_legacy_webhook_rejects_invalid_signature(legacy_client):
    client, db = legacy_client
    payload = _payload("checkout.session.completed", {"id": "cs_complete", "payment_status": "paid"})

    response = _post_legacy(client, payload, "t=1234567890,v1=invalid")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid webhook signature."
    assert db.users.update_calls == []
    assert db.payment_transactions.update_calls == []


def test_legacy_webhook_unsigned_json_cannot_reach_membership_mutation(legacy_client):
    client, db = legacy_client
    payload = _payload("checkout.session.completed", {"id": "cs_complete", "payment_status": "paid"})

    response = client.post("/api/webhook/stripe", content=payload)

    assert response.status_code == 400
    assert db.users.rows[0]["subscription_status"] == "trialing"
    assert db.payment_transactions.rows[0]["payment_status"] == "unpaid"
    assert db.users.update_calls == []
    assert db.payment_transactions.update_calls == []


def test_legacy_webhook_valid_signed_unrelated_event_acknowledges_without_mutation(
    caplog,
    legacy_client,
):
    caplog.set_level(logging.INFO, logger="routes.membership")
    client, db = legacy_client
    payload = _payload(
        "invoice.expired",
        {"id": "cs_complete", "payment_status": "paid", "status": "complete"},
    )

    response = _post_legacy(client, payload, _stripe_signature(payload))

    assert response.status_code == 200
    assert response.json() == {"received": True}
    assert db.users.rows[0]["subscription_status"] == "trialing"
    assert db.payment_transactions.rows[0]["payment_status"] == "unpaid"
    assert db.payment_transactions.rows[0]["status"] == "pending"
    assert db.users.update_calls == []
    assert db.payment_transactions.update_calls == []
    ignored = [
        record
        for record in caplog.records
        if record.getMessage() == "legacy stripe webhook event ignored"
    ]
    assert ignored
    assert ignored[-1].reason == "unsupported_event_type"
    assert ignored[-1].stripe_event_type == "invoice.expired"
    assert "cs_complete" not in ignored[-1].getMessage()
    assert "payment_status" not in ignored[-1].getMessage()


@pytest.mark.parametrize("event_type", ["", None])
def test_legacy_webhook_valid_signed_empty_or_missing_event_type_acknowledges_without_mutation(
    event_type,
    legacy_client,
):
    client, db = legacy_client
    payload = _payload(event_type, {"id": "cs_complete", "payment_status": "paid"})

    response = _post_legacy(client, payload, _stripe_signature(payload))

    assert response.status_code == 200
    assert response.json() == {"received": True}
    assert db.users.rows[0]["subscription_status"] == "trialing"
    assert db.payment_transactions.rows[0]["payment_status"] == "unpaid"
    assert db.payment_transactions.rows[0]["status"] == "pending"
    assert db.users.update_calls == []
    assert db.payment_transactions.update_calls == []


def test_legacy_webhook_accepts_valid_signed_completed_event(legacy_client):
    client, db = legacy_client
    payload = _payload(
        "checkout.session.completed",
        {"id": "cs_complete", "payment_status": "paid", "status": "complete"},
    )

    response = _post_legacy(client, payload, _stripe_signature(payload))

    assert response.status_code == 200
    assert response.json() == {"received": True}
    assert db.users.rows[0]["membership_tier"] == "owner_rider"
    assert db.users.rows[0]["subscription_status"] == "active"
    assert db.users.rows[0]["trial_expires_at"] is None
    assert db.payment_transactions.rows[0]["payment_status"] == "paid"
    assert db.payment_transactions.rows[0]["status"] == "complete"


def test_legacy_webhook_accepts_valid_signed_expired_event_without_user_mutation(legacy_client):
    client, db = legacy_client
    payload = _payload(
        "checkout.session.expired",
        {"id": "cs_expired", "payment_status": "unpaid", "status": "expired"},
    )

    response = _post_legacy(client, payload, _stripe_signature(payload))

    assert response.status_code == 200
    assert response.json() == {"received": True}
    assert db.users.update_calls == []
    assert db.payment_transactions.rows[1]["payment_status"] == "unpaid"
    assert db.payment_transactions.rows[1]["status"] == "expired"


def test_legacy_webhook_duplicate_valid_completed_event_does_not_duplicate_mutation(legacy_client):
    client, db = legacy_client
    payload = _payload(
        "checkout.session.completed",
        {"id": "cs_complete", "payment_status": "paid", "status": "complete"},
        event_id="evt_duplicate",
    )

    first = _post_legacy(client, payload, _stripe_signature(payload))
    user_updates_after_first = len(db.users.update_calls)
    tx_updates_after_first = len(db.payment_transactions.update_calls)
    second = _post_legacy(client, payload, _stripe_signature(payload))

    assert first.status_code == 200
    assert second.status_code == 200
    assert len(db.users.update_calls) == user_updates_after_first == 1
    assert len(db.payment_transactions.update_calls) == tx_updates_after_first == 1


def test_legacy_webhook_internal_sdk_exception_details_do_not_leak(monkeypatch, legacy_client):
    client, db = legacy_client
    payload = _payload("checkout.session.completed", {"id": "cs_complete", "payment_status": "paid"})

    def raise_internal_error(*args, **kwargs):
        raise RuntimeError("raw sdk failure secret customer@example.com")

    monkeypatch.setattr("routes.membership.construct_webhook_event", raise_internal_error)

    response = _post_legacy(client, payload, "t=1234567890,v1=placeholder")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid webhook signature."
    assert "customer@example.com" not in response.text
    assert "raw sdk failure" not in response.text
    assert "secret" not in response.text
    assert db.users.update_calls == []
    assert db.payment_transactions.update_calls == []


def test_subscription_webhook_valid_signed_event_remains_unaffected(monkeypatch):
    monkeypatch.setenv("STRIPE_API_KEY", "sk_test_subscription_route")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    calls: list[dict[str, Any]] = []

    def fake_construct_event(payload, sig_header, secret, api_key=None):
        assert sig_header
        assert secret == WEBHOOK_SECRET
        assert api_key == "sk_test_subscription_route"
        return json.loads(payload)

    async def fake_process_event(db, event):
        calls.append(event)
        return 202, {"received": True, "handled": "subscription-route"}

    monkeypatch.setattr("routes.subscriptions.construct_webhook_event", fake_construct_event)
    monkeypatch.setattr("routes.subscriptions_webhook_handlers.process_event", fake_process_event)
    app = FastAPI()
    app.include_router(
        build_subscriptions_router(db=object(), get_current_user=_fake_get_current_user),
        prefix="/api",
    )
    client = TestClient(app)
    payload = _payload(
        "checkout.session.completed",
        {"id": "cs_subscription", "payment_status": "paid", "status": "complete"},
    )

    response = client.post(
        "/api/webhook/stripe-subscriptions",
        content=payload,
        headers={"Stripe-Signature": _stripe_signature(payload)},
    )

    assert response.status_code == 202
    assert response.json() == {"received": True, "handled": "subscription-route"}
    assert calls[0]["type"] == "checkout.session.completed"
