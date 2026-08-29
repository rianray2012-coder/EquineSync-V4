"""Stripe live-payment Wave F environment contract tests."""
from __future__ import annotations

import pathlib

from core.stripe_live_environment_contract import (
    build_stripe_live_environment_contract_report,
    render_stripe_live_environment_contract_markdown,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def _contract_ready_env() -> dict[str, str]:
    return {
        "APP_ENV": "production",
        "STRIPE_API_KEY": "rk_live_FAKE_RESTRICTED_KEY_SHOULD_NOT_RENDER",
        "STRIPE_PUBLISHABLE_KEY": "pk_live_FAKE_PUBLIC_KEY_SHOULD_NOT_RENDER",
        "REACT_APP_STRIPE_PUBLISHABLE_KEY": "pk_live_FAKE_PUBLIC_KEY_SHOULD_NOT_RENDER",
        "STRIPE_WEBHOOK_SECRET": "whsec_FAKE_WEBHOOK_SECRET_SHOULD_NOT_RENDER",
        "STRIPE_LIVE_WEBHOOK_ENDPOINT_URL": "https://api.equine-sync.com/api/webhook/stripe-subscriptions",
        "APP_BASE_URL": "https://app.equine-sync.com",
        "ALLOWED_BILLING_ORIGINS": "https://app.equine-sync.com",
        "STRIPE_LIVE_CHECKOUT_ENABLED": "false",
        "STRIPE_LIVE_PORTAL_ENABLED": "false",
        "STRIPE_LIVE_FOUNDER_CHECKOUT_PROOF_ENABLED": "false",
    }


def test_live_environment_contract_passes_when_inputs_are_present_and_guards_off():
    report = build_stripe_live_environment_contract_report(_contract_ready_env())

    assert report["overall_status"] == "pass"
    assert report["ready_for_founder_live_smoke"] is True
    assert report["config_report_overall_status"] == "pass"
    assert report["publishable_key_match_status"] == "match"
    assert report["issue_counts"] == {}
    assert report["proof_guards"] == {
        "provider_api_calls_performed": False,
        "checkout_sessions_created": False,
        "customer_portal_sessions_created": False,
        "webhook_events_replayed": False,
        "database_writes_performed": False,
        "live_payment_collection_performed": False,
    }
    assert all(report["input_presence"].values())
    assert any(item["key"] == "STRIPE_API_KEY" and item["secret"] is True for item in report["required_inputs"])
    assert any(item["key"] == "REACT_APP_STRIPE_PUBLISHABLE_KEY" for item in report["required_inputs"])


def test_live_environment_contract_blocks_missing_frontend_key_and_mismatch():
    missing_frontend = dict(_contract_ready_env())
    missing_frontend.pop("REACT_APP_STRIPE_PUBLISHABLE_KEY")
    missing_report = build_stripe_live_environment_contract_report(missing_frontend)
    missing_kinds = {issue["kind"] for issue in missing_report["issues"]}

    assert missing_report["overall_status"] == "blocked"
    assert missing_report["ready_for_founder_live_smoke"] is False
    assert missing_report["publishable_key_match_status"] == "not_comparable"
    assert "stripe_frontend_publishable_key_missing" in missing_kinds

    mismatch = dict(_contract_ready_env())
    mismatch["REACT_APP_STRIPE_PUBLISHABLE_KEY"] = "pk_live_OTHER_PUBLIC_KEY_SHOULD_NOT_RENDER"
    mismatch_report = build_stripe_live_environment_contract_report(mismatch)
    mismatch_kinds = {issue["kind"] for issue in mismatch_report["issues"]}

    assert mismatch_report["overall_status"] == "blocked"
    assert mismatch_report["publishable_key_match_status"] == "mismatch"
    assert "stripe_publishable_key_mismatch" in mismatch_kinds


def test_rendered_live_environment_contract_is_redacted_and_explicit():
    env = _contract_ready_env()
    report = build_stripe_live_environment_contract_report(env)
    markdown = render_stripe_live_environment_contract_markdown(report)

    assert "# Stripe Live-Payment Readiness Wave F" in markdown
    assert "Ready for founder live smoke | True" in markdown
    assert "REACT_APP_STRIPE_PUBLISHABLE_KEY" in markdown
    assert "No live payment collection." in markdown
    assert "checkout_sessions_created | False" in markdown

    forbidden_fragments = [
        "FAKE_RESTRICTED_KEY_SHOULD_NOT_RENDER",
        "FAKE_PUBLIC_KEY_SHOULD_NOT_RENDER",
        "FAKE_WEBHOOK_SECRET_SHOULD_NOT_RENDER",
        "rk_live_",
        "pk_live_",
        "whsec_",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in markdown


def test_live_environment_contract_helper_and_script_are_read_only_source_guard():
    helper = (ROOT / "backend" / "core" / "stripe_live_environment_contract.py").read_text()
    script = (ROOT / "backend" / "scripts" / "stripe_live_environment_contract.py").read_text()

    forbidden_helper_tokens = [
        "stripe_client(",
        "checkout.sessions.create",
        "billing_portal.sessions.create",
        "construct_event",
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
    for token in ("stripe_client(", "checkout.sessions.create", "billing_portal.sessions.create", "insert_one", "update_one", "delete_one"):
        assert token not in script
