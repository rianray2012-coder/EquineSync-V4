"""Build-Next-18A provider-live proof tests.

BN18A is evidence-only. It must distinguish configured from live-proven without
calling Stripe, Resend, DocuSign, or MongoDB, and without rendering raw secrets.
"""
from __future__ import annotations

import pathlib

from core.provider_live_proof import (
    build_provider_live_proof,
    render_provider_live_proof_markdown,
    stripe_key_mode,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def _live_env() -> dict[str, str]:
    return {
        "APP_ENV": "production",
        "STRIPE_SECRET_KEY": "rk_live_FAKE_BACKEND_KEY_SHOULD_NOT_RENDER",
        "STRIPE_PUBLISHABLE_KEY": "pk_live_FAKE_PUBLIC_KEY_SHOULD_NOT_RENDER",
        "STRIPE_WEBHOOK_SECRET": "whsec_FAKE_STRIPE_WEBHOOK_SHOULD_NOT_RENDER",
        "RESEND_API_KEY": "re_FAKE_RESEND_KEY_SHOULD_NOT_RENDER",
        "RESEND_FROM": "EquineSync <hello@equine-sync.com>",
        "DOCUSIGN_INTEGRATION_KEY": "integration-key-should-not-render",
        "DOCUSIGN_USER_ID": "user-id-should-not-render",
        "DOCUSIGN_ACCOUNT_ID": "account-id-should-not-render",
        "DOCUSIGN_PRIVATE_KEY_PATH": "/tmp/docusign-private-key-should-not-render.pem",
        "DOCUSIGN_AUTH_SERVER": "account.docusign.com",
        "DOCUSIGN_BASE_URL": "https://na4.docusign.net/restapi",
        "DOCUSIGN_WEBHOOKS_ENABLED": "true",
        "DOCUSIGN_WEBHOOK_SECRET": "docusign-webhook-should-not-render",
        "DOCUSIGN_CONNECT_CONFIGURATION_ID": "configuration-id-should-not-render",
        "SCHEDULER_ENABLED": "true",
    }


def test_stripe_key_mode_returns_safe_classes_only():
    assert stripe_key_mode("rk_live_abc") == "restricted_live"
    assert stripe_key_mode("sk_live_abc") == "secret_live"
    assert stripe_key_mode("rk_test_abc") == "restricted_test"
    assert stripe_key_mode("sk_test_abc") == "secret_test"
    assert stripe_key_mode("pk_live_abc") == "publishable_live"
    assert stripe_key_mode("pk_test_abc") == "publishable_test"
    assert stripe_key_mode("") == "missing"
    assert stripe_key_mode("mystery") == "configured_unknown"


def test_live_like_env_can_prove_provider_readiness_without_blockers():
    report = build_provider_live_proof(_live_env())
    assert report["overall_status"] == "pass"
    assert report["issue_counts"] == {}
    assert {row["provider"]: row["status"] for row in report["providers"]} == {
        "stripe": "pass",
        "resend": "pass",
        "docusign": "pass",
        "background_jobs": "pass",
    }
    assert report["stripe"]["secret_key_mode"] == "restricted_live"
    assert report["stripe"]["compatibility_api_key_mode"] == "missing"
    assert report["stripe"]["publishable_key_mode"] == "publishable_live"
    assert report["resend"]["sender_domain_is_equine_sync"] is True
    assert report["docusign"]["auth_server_mode"] == "live"
    assert report["docusign"]["base_url_mode"] == "live"


def test_sandbox_docusign_is_deferred_not_claimed_live():
    env = _live_env()
    env.update({
        "APP_ENV": "development",
        "DOCUSIGN_AUTH_SERVER": "account-d.docusign.com",
        "DOCUSIGN_BASE_URL": "https://demo.docusign.net/restapi",
    })
    report = build_provider_live_proof(env)
    statuses = {row["provider"]: row["status"] for row in report["providers"]}
    assert statuses["docusign"] == "deferred"
    docusign_kinds = {
        issue["kind"] for issue in report["issues"]
        if issue["provider"] == "docusign"
    }
    assert "docusign_auth_not_live" in docusign_kinds
    assert "docusign_base_not_live" in docusign_kinds


def test_custom_docusign_base_url_is_not_claimed_live():
    env = _live_env()
    env["DOCUSIGN_BASE_URL"] = "https://example.com/restapi"

    report = build_provider_live_proof(env)
    statuses = {row["provider"]: row["status"] for row in report["providers"]}
    docusign_kinds = {
        issue["kind"] for issue in report["issues"]
        if issue["provider"] == "docusign"
    }

    assert report["overall_status"] == "deferred"
    assert statuses["docusign"] == "deferred"
    assert report["docusign"]["base_url_mode"] == "custom"
    assert "docusign_base_not_live" in docusign_kinds


def test_resend_non_equine_sync_sender_domain_is_not_claimed_production_ready():
    env = _live_env()
    env["RESEND_FROM"] = "EquineSync <hello@gmail.com>"

    report = build_provider_live_proof(env)
    statuses = {row["provider"]: row["status"] for row in report["providers"]}
    resend_kinds = {
        issue["kind"] for issue in report["issues"]
        if issue["provider"] == "resend"
    }

    assert report["overall_status"] == "blocked"
    assert statuses["resend"] == "blocked"
    assert report["resend"]["sender_domain"] == "gmail.com"
    assert report["resend"]["sender_domain_is_equine_sync"] is False
    assert "resend_sender_domain_not_equine_sync" in resend_kinds


def test_production_missing_provider_values_are_blockers():
    report = build_provider_live_proof({"APP_ENV": "production"})
    assert report["overall_status"] == "blocked"
    assert report["issue_counts"]["blocker"] >= 3
    kinds = {issue["kind"] for issue in report["issues"]}
    assert "stripe_secret_key_not_live" in kinds
    assert "stripe_webhook_secret_missing" in kinds
    assert "resend_api_key_missing" in kinds
    assert "docusign_credentials_missing" in kinds


def test_rendered_report_never_contains_raw_secret_inputs():
    env = _live_env()
    report = build_provider_live_proof(env)
    markdown = render_provider_live_proof_markdown(report)

    assert "restricted_live" in markdown
    assert "publishable_live" in markdown
    assert "equine-sync.com" in markdown

    forbidden_fragments = [
        "FAKE_BACKEND_KEY_SHOULD_NOT_RENDER",
        "FAKE_PUBLIC_KEY_SHOULD_NOT_RENDER",
        "FAKE_STRIPE_WEBHOOK_SHOULD_NOT_RENDER",
        "FAKE_RESEND_KEY_SHOULD_NOT_RENDER",
        "integration-key-should-not-render",
        "user-id-should-not-render",
        "account-id-should-not-render",
        "docusign-private-key-should-not-render",
        "docusign-webhook-should-not-render",
        "configuration-id-should-not-render",
        "rk_live_",
        "pk_live_",
        "whsec_",
        "re_",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in markdown


def test_bn18a_source_does_not_call_providers_or_write_mongo():
    core_src = (ROOT / "backend" / "core" / "provider_live_proof.py").read_text()
    script_src = (ROOT / "backend" / "scripts" / "build_next_18a_provider_live_proof.py").read_text()
    combined = core_src + "\n" + script_src

    forbidden = [
        "stripe.checkout",
        "stripe.Webhook.construct_event",
        "resend.Emails.send",
        "request_docusign_access_token",
        "create_docusign_sandbox_envelope",
        "requests.post",
        "AsyncIOMotorClient",
        "insert_one",
        "update_one",
        "delete_one",
        "bulk_write",
    ]
    for token in forbidden:
        assert token not in combined


def test_bn18a_script_loads_dotenv_but_has_no_provider_lifecycle_flags():
    script_src = (ROOT / "backend" / "scripts" / "build_next_18a_provider_live_proof.py").read_text()
    assert "load_dotenv" in script_src
    assert "--fail-on-blockers" in script_src
    for token in ("--send-email", "--create-checkout", "--create-envelope", "--replay-webhook"):
        assert token not in script_src
