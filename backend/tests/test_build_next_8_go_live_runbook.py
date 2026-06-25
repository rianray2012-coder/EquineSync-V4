"""Build-Next-8 production go-live runbook checks.

BN8 is a runbook/sign-off package only. It must not contain secrets, product
behavior changes, provider calls, or launch approval claims.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

README = ROOT / "BUILD_NEXT_8_PRODUCTION_GO_LIVE_RUNBOOK_README.md"
RUNBOOK = ROOT / "outputs/build_next_8_go_live_runbook.md"
ENV_CHECKLIST = ROOT / "outputs/build_next_8_env_boolean_checklist.md"
PACKAGE_FILES = [
    ROOT / "BUILD_NEXT_8_PRODUCTION_GO_LIVE_RUNBOOK_README.md",
    ROOT / "backend/tests/test_build_next_8_go_live_runbook.py",
    ROOT / "outputs/build_next_8_go_live_runbook.md",
    ROOT / "outputs/build_next_8_env_boolean_checklist.md",
    ROOT / "docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md",
    ROOT / "docs/PHASED_EXECUTION_PLAN.md",
    ROOT / "memory/PRD.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn8_required_artifacts_exist_and_are_nonempty():
    for path in [README, RUNBOOK, ENV_CHECKLIST]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 100, str(path)


def test_bn8_does_not_claim_launch_or_pilot_approval():
    text = f"{_read(README)}\n{_read(RUNBOOK)}"

    assert "Production launch: not approved by this phase" in text
    assert "First-client pilot: still requires BN7A UAT evidence closure" in text
    assert "Broad public launch: still no-go" in text
    assert "First-client pilot | Hold" in text
    assert "Broad public launch | No-go" in text
    assert "public launch approved. | no-go" in text
    assert "Ready for unrestricted launch" not in text
    assert "launch approved" not in text.lower().replace("public launch approved. | no-go", "")


def test_bn8_runbook_contains_provider_rollback_support_and_signoff_sections():
    runbook = _read(RUNBOOK)

    for phrase in [
        "Pre-Launch Sequence",
        "Stripe Go-Live Checklist",
        "DocuSign Go-Live Checklist",
        "Rollback Plan",
        "Support And Monitoring Plan",
        "Founder Decision Sheet",
        "Stop-Launch Criteria",
    ]:
        assert phrase in runbook

    for phrase in [
        "checkout.session.completed",
        "customer.subscription.created/updated/deleted",
        "invoice.payment_failed",
        "DOCUSIGN_WEBHOOKS_ENABLED=true",
        "Disable web checkout entry points",
        "Disable DocuSign webhook processing",
    ]:
        assert phrase in runbook


def test_bn8_env_checklist_is_boolean_only_and_covers_core_providers():
    checklist = _read(ENV_CHECKLIST)

    assert "Do not paste environment values" in checklist
    assert "configured" in checklist
    assert "missing" in checklist
    for area in [
        "Core Runtime",
        "Stripe",
        "DocuSign",
        "Email / Notifications",
        "Operations",
    ]:
        assert area in checklist
    for key in [
        "MONGO_URL",
        "JWT_SECRET",
        "Stripe webhook secret",
        "DocuSign private key path",
        "DocuSign Connect HMAC secret",
        "Database backup configured",
    ]:
        assert key in checklist


def test_bn8_package_files_do_not_contain_secret_shaped_values():
    combined = "\n".join(_read(path) for path in PACKAGE_FILES)
    forbidden = [
        "sk" + "_live_",
        "sk" + "_test_",
        "rk" + "_live_",
        "rk" + "_test_",
        "wh" + "sec_",
        "-----" + "BEGIN",
        "Authorization" + ": Bearer",
        "DOCUSIGN" + "_PRIVATE_KEY=",
        "DOCUSIGN" + "_WEBHOOK_SECRET=",
        "STRIPE" + "_API_KEY=",
        "JWT" + "_SECRET=",
        "mongodb" + "+srv://",
        "password" + ":",
    ]
    for fragment in forbidden:
        assert fragment not in combined


def test_bn8_readme_scope_is_runbook_only_no_behavior_changes():
    readme = _read(README)
    for phrase in [
        "No product behavior changes",
        "No provider API calls",
        "No public launch/deploy action",
        "No secret values",
        "outputs/build_next_8_production_go_live_runbook.zip",
    ]:
        assert phrase in readme
