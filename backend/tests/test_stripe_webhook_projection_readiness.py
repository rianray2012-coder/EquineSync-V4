"""Stripe live-payment Wave E webhook/projection readiness tests."""
from __future__ import annotations

import asyncio
import json
import pathlib

from core.stripe_webhook_projection_readiness import (
    build_stripe_webhook_projection_readiness_report,
    render_stripe_webhook_projection_readiness_markdown,
)
from routes.subscriptions_webhook_handlers import process_event
from tests.test_stripe_test_mode_activation_proof import _FakeDB, _client


ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_wave_e_report_covers_initial_live_event_scope_without_live_calls():
    report = build_stripe_webhook_projection_readiness_report()

    assert report["overall_status"] == "pass"
    assert report["issue_counts"] == {}
    assert report["webhooks"]["handled_event_count"] == 11
    assert report["webhooks"]["initial_live_event_scope_covered"] is True
    assert set(report["webhooks"]["initial_live_event_scope"]) <= set(report["webhooks"]["handled_events"])
    assert report["owner_projection"]["subscription_endpoint"] == "/api/subscriptions/me"
    assert report["owner_projection"]["redacted_subscription_fields"] == (
        "stripe_customer_id",
        "stripe_subscription_id",
        "stripe_price_id",
    )
    assert report["proof_guards"]["provider_api_calls_performed"] is False
    assert report["proof_guards"]["live_webhook_events_replayed"] is False
    assert report["proof_guards"]["database_writes_performed_by_report"] is False


def test_wave_e_rendered_report_is_redacted_and_explicit_about_guards():
    markdown = render_stripe_webhook_projection_readiness_markdown(
        build_stripe_webhook_projection_readiness_report()
    )

    assert "# Stripe Live-Payment Readiness Wave E" in markdown
    assert "checkout.session.completed" in markdown
    assert "invoice.payment_failed" in markdown
    assert "provider_api_calls_performed | False" in markdown
    assert "live_webhook_events_replayed | False" in markdown
    assert "stripe_customer_id, stripe_subscription_id, stripe_price_id" in markdown
    for forbidden in ("rk_live_", "sk_live_", "pk_live_", "whsec_", "cus_live_", "sub_live_"):
        assert forbidden not in markdown


def test_seeded_payment_failed_webhook_maps_state_and_owner_projection_stays_safe():
    db = _FakeDB()
    db.barns.rows[0].update({
        "subscription_id": "sub_wave_e_projection",
        "stripe_customer_id": "cus_wave_e_projection",
    })
    db.subscriptions.rows.append({
        "id": "sub_wave_e_projection",
        "stripe_subscription_id": "sub_wave_e_projection",
        "stripe_customer_id": "cus_wave_e_projection",
        "stripe_price_id": "price_wave_e_projection",
        "barn_id": "barn-stripe-proof",
        "owner_user_id": "admin-1",
        "plan_tier_code": "starter_barn",
        "status": "active",
        "pending_emails": [],
        "created_at": "x",
        "entitlements_snapshot": {"horses": 10, "users": 3},
    })
    event = {
        "id": "evt_wave_e_payment_failed",
        "type": "invoice.payment_failed",
        "created": 1790000001,
        "data": {
            "object": {
                "id": "in_wave_e_projection",
                "subscription": "sub_wave_e_projection",
                "customer": "cus_wave_e_projection",
                "amount_due": 7900,
                "currency": "usd",
                "status": "open",
                "hosted_invoice_url": "https://invoice.stripe.com/i/test",
                "invoice_pdf": "https://invoice.stripe.com/i/test.pdf",
            },
        },
    }

    status_code, body = asyncio.run(process_event(db, event))

    assert status_code == 200
    assert body["handled"] is True
    invoice = db.subscription_invoices.rows[0]
    assert invoice["stripe_invoice_id"] == "in_wave_e_projection"
    assert invoice["status"] == "open"
    assert invoice["payment_failure_count"] == 1
    assert db.barns.rows[0]["last_payment_failed_at"]
    assert "payment_failed" in db.subscriptions.rows[0]["pending_emails"]
    assert db.billing_events.rows[0]["processing_status"] == "ok"
    assert "raw_stripe_payload" not in json.dumps(db.billing_events.rows)

    client, _ = _client({"id": "admin-1", "barn_id": "barn-stripe-proof", "role": "admin"}, db)
    owner_view = client.get("/api/subscriptions/me")
    assert owner_view.status_code == 200
    body = owner_view.json()
    assert body["subscription"]["plan_tier_code"] == "starter_barn"
    assert "stripe_customer_id" not in body["subscription"]
    assert "stripe_subscription_id" not in body["subscription"]
    assert "stripe_price_id" not in body["subscription"]
    assert "cus_wave_e_projection" not in json.dumps(body)
    assert "sub_wave_e_projection" not in json.dumps(body)
    assert "price_wave_e_projection" not in json.dumps(body)


def test_wave_e_helper_and_script_are_read_only_source_guard():
    helper = (ROOT / "backend" / "core" / "stripe_webhook_projection_readiness.py").read_text()
    script = (ROOT / "backend" / "scripts" / "stripe_webhook_projection_readiness.py").read_text()

    for token in (
        "stripe_client(",
        "construct_event",
        "checkout.sessions.create",
        "billing_portal.sessions.create",
        "insert_one",
        "update_one",
        "delete_one",
        "bulk_write",
        ".find(",
    ):
        assert token not in helper

    assert "write_text" in script
    for token in ("stripe_client(", "construct_event", "checkout.sessions.create", "insert_one", "update_one"):
        assert token not in script
