"""Stripe live-payment Wave B configuration readiness tests.

Wave B is read-only. These tests pin redacted config proof behavior without
calling Stripe, creating sessions, replaying webhooks, or writing data.
"""
from __future__ import annotations

import pathlib

from core.stripe_live_readiness import (
    build_stripe_live_config_readiness_report,
    render_stripe_live_config_readiness_markdown,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def _ready_env() -> dict[str, str]:
    return {
        "APP_ENV": "production",
        "STRIPE_API_KEY": "rk_live_FAKE_BACKEND_KEY_SHOULD_NOT_RENDER",
        "STRIPE_PUBLISHABLE_KEY": "pk_live_FAKE_PUBLIC_KEY_SHOULD_NOT_RENDER",
        "STRIPE_WEBHOOK_SECRET": "whsec_FAKE_WEBHOOK_SECRET_SHOULD_NOT_RENDER",
        "STRIPE_LIVE_WEBHOOK_ENDPOINT_URL": "https://api.equine-sync.com/api/webhook/stripe-subscriptions",
        "APP_BASE_URL": "https://app.equine-sync.com",
        "ALLOWED_BILLING_ORIGINS": "https://app.equine-sync.com",
        "STRIPE_LIVE_CHECKOUT_ENABLED": "false",
        "STRIPE_LIVE_PORTAL_ENABLED": "false",
    }


def test_ready_live_config_passes_without_enabling_live_money():
    report = build_stripe_live_config_readiness_report(_ready_env())

    assert report["overall_status"] == "pass"
    assert report["issue_counts"] == {}
    assert report["stripe"]["api_key_mode"] == "restricted_live"
    assert report["stripe"]["publishable_key_mode"] == "publishable_live"
    assert report["stripe"]["webhook_secret_configured"] is True
    assert report["stripe"]["live_checkout_enabled"] is False
    assert report["stripe"]["live_portal_enabled"] is False
    assert report["stripe"]["live_money_enabled"] is False
    assert report["webhook_endpoint"] == {
        "configured": True,
        "env_key": "STRIPE_LIVE_WEBHOOK_ENDPOINT_URL",
        "url_mode": "https",
    }
    assert report["allowed_origins"] == {"configured": True, "count": 1}
    assert report["proof_guards"]["provider_api_calls_performed"] is False
    assert report["proof_guards"]["checkout_sessions_created"] is False
    assert report["proof_guards"]["customer_portal_sessions_created"] is False


def test_live_config_report_blocks_incomplete_or_enabled_live_session_state():
    env = {
        "APP_ENV": "production",
        "STRIPE_API_KEY": "sk_live_FAKE_SECRET_KEY_SHOULD_NOT_RENDER",
        "STRIPE_LIVE_CHECKOUT_ENABLED": "true",
        "STRIPE_LIVE_PORTAL_ENABLED": "true",
        "STRIPE_LIVE_WEBHOOK_ENDPOINT_URL": "http://api.equine-sync.com/api/webhook/stripe-subscriptions",
    }

    report = build_stripe_live_config_readiness_report(env)
    kinds = {issue["kind"] for issue in report["issues"]}

    assert report["overall_status"] == "blocked"
    assert "stripe_api_key_not_restricted_live" in kinds
    assert "stripe_publishable_key_not_live" in kinds
    assert "stripe_webhook_secret_missing" in kinds
    assert "stripe_live_webhook_endpoint_not_https" in kinds
    assert "stripe_allowed_origins_missing" in kinds
    assert "stripe_live_checkout_flag_enabled" in kinds
    assert "stripe_live_portal_flag_enabled" in kinds
    assert report["proof_guards"]["live_money_enabled"] is True


def test_rendered_wave_b_report_never_contains_raw_secret_inputs():
    env = _ready_env()
    report = build_stripe_live_config_readiness_report(env)
    markdown = render_stripe_live_config_readiness_markdown(report)

    assert "# Stripe Live-Payment Readiness Wave B" in markdown
    assert "restricted_live" in markdown
    assert "publishable_live" in markdown
    assert "checkout_sessions_created | False" in markdown

    forbidden_fragments = [
        "FAKE_BACKEND_KEY_SHOULD_NOT_RENDER",
        "FAKE_PUBLIC_KEY_SHOULD_NOT_RENDER",
        "FAKE_WEBHOOK_SECRET_SHOULD_NOT_RENDER",
        "rk_live_",
        "pk_live_",
        "whsec_",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in markdown


def test_wave_b_helper_and_script_are_read_only_source_guard():
    helper = (ROOT / "backend" / "core" / "stripe_live_readiness.py").read_text()
    script = (ROOT / "backend" / "scripts" / "stripe_live_config_readiness.py").read_text()

    forbidden_helper_tokens = [
        "checkout.sessions.create",
        "billing_portal.sessions.create",
        "construct_event",
        "stripe_client(",
        "insert_one",
        "update_one",
        "delete_one",
        "bulk_write",
        ".find(",
    ]
    for token in forbidden_helper_tokens:
        assert token not in helper

    assert "load_dotenv" in script
    assert "write_text" in script
    for token in ("checkout.sessions.create", "billing_portal.sessions.create", "insert_one", "update_one", "delete_one"):
        assert token not in script
