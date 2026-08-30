from __future__ import annotations

import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "PILOT_SUPPORT_RUNBOOK.md"


def _text() -> str:
    assert RUNBOOK.exists(), f"missing runbook: {RUNBOOK}"
    return RUNBOOK.read_text(encoding="utf-8")


def test_gate7_pilot_support_runbook_exists_and_names_owner_and_channels():
    text = _text()

    for required in (
        "Founder / Rian Ray",
        "`super_admin`",
        "`platform_admin`",
        "`support_admin`",
        "`billing_admin` and `read_only_auditor` may not own support tickets",
        "The supported in-app channel is `/support`.",
        "`/admin/portal/support`",
    ):
        assert required in text


def test_gate7_pilot_support_runbook_defines_severity_escalation_and_triage():
    text = _text()

    for required in (
        "`urgent`",
        "`high`",
        "`medium`",
        "`low`",
        "Safety, privacy, payment, legal-send, access-boundary",
        "classify up to the safer severity",
        "Change status to `in_progress`",
        "Mark `waiting`",
        "Mark `resolved`",
    ):
        assert required in text


def test_gate7_pilot_support_runbook_covers_privacy_evidence_and_audit_limits():
    text = _text()

    for required in (
        "Redacted screenshots",
        "HTTP status codes and sanitized response shapes",
        "Console error text",
        "Passwords, refresh tokens, access tokens, API keys",
        "Full card numbers",
        "Unredacted DocuSign or Adobe Sign envelope identifiers",
        "Minor/guardian private details",
        "Support audit metadata should remain routing-only",
        "Free-text ticket bodies and",
        "internal notes may live in `support_tickets`",
    ):
        assert required in text


def test_gate7_pilot_support_runbook_carries_activation_stop_rules():
    text = _text()

    for required in (
        "Customer-facing live Checkout",
        "Live payment collection",
        "Stripe Customer Portal",
        "Live `automatic_tax`",
        "DocuSign production envelopes",
        "Adobe Sign remains deferred and inactive",
        "No official AI save authority",
        "No AI autonomous mutation",
        "Do not expand provider-live activation",
        "public provider directory behavior",
    ):
        assert required in text


def test_gate7_pilot_support_runbook_covers_suspension_and_rollback():
    text = _text()

    for required in (
        "Suspend or revoke the smallest affected access path",
        "Keep read-only support/admin visibility available",
        "Restore access only after",
        "Stop the smallest unsafe action path first",
        "Disable live payment/signature/AI/provider entry points by flag",
        "Keep pilot users on free/manual access",
        "Record the rollback action in the ticket and audit trail",
    ):
        assert required in text
