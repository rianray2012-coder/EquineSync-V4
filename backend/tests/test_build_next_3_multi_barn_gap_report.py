"""Build-Next-3 - multi-barn / multi-role gap report guards.

These tests intentionally pin the current single-context assumptions and the
read-only BN3 report. They do not require Mongo, Stripe, a browser, or a
running backend.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_3_MULTI_BARN_MULTI_ROLE_GAP_REPORT_README.md"
REPORT = ROOT / "outputs" / "build_next_3_multi_barn_multi_role_gap_report.md"


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_build_next_3_report_records_founder_decisions_and_open_items():
    text = REPORT.read_text(encoding="utf-8")

    for required in [
        "Codex-approved and locked",
        "Future collection name should be `account_memberships`",
        "Users may hold multiple roles",
        "Individual users may be active without being attached to an active facility",
        "collect barn information as a possible sales lead",
        "Billing entitlements remain account/facility scoped",
        "free individual owner with one horse account",
        "Owner access shape: horse-specific, barn-wide, or both",
        "Locked after report: horse-specific for launch",
        "Locked after report: preserve `users.barn_id` and `users.role` mirrors through launch",
        "Standalone individual-owner account ids should be generated",
        "Facility search / lead capture should apply to all non-platform onboarding",
    ]:
        assert required in text


def test_build_next_3_report_preserves_read_only_scope():
    combined = README.read_text(encoding="utf-8") + "\n" + REPORT.read_text(encoding="utf-8")
    for guardrail in [
        "No schema migration",
        "No database writes",
        "No invite behavior changes",
        "No account transfer behavior",
        "No permission expansion",
        "No owner projection changes",
        "No Admin Portal capability changes",
        "No billing, checkout, webhook, Stripe, Apple, or Phase 15R behavior changes",
        "No HorseOps privacy behavior changes",
        "No landing page changes",
        "No native app",
        "No Phase 16 cleanup",
    ]:
        assert guardrail in combined


def test_bn4_invite_acceptance_attaches_existing_users_via_memberships():
    invite_src = _read("backend/routes/invites.py")
    report = REPORT.read_text(encoding="utf-8")

    assert "upsert_invite_membership" in invite_src
    assert "accepted_existing_user" in invite_src
    assert "accepted_membership_id" in invite_src
    assert "Do not start Build-Next-4 existing-user invite acceptance until" in report
    assert "`account_memberships` exists" in report


def test_current_tenancy_and_frontend_permissions_are_single_context():
    tenancy_src = _read("backend/core/tenancy.py")
    frontend_permissions = _read("frontend/src/lib/permissions.js")
    horses_src = _read("backend/routes/horses.py")

    assert "def resolve_barn_id" in tenancy_src
    assert "PRIMARY_BARN_ID" in tenancy_src
    assert "return user.get(\"barn_id\") or PRIMARY_BARN_ID" in tenancy_src
    assert "roles.includes(user?.role)" in frontend_permissions
    assert "barn_filter(user" in horses_src


def test_platform_roles_stay_separate_from_future_account_memberships():
    permissions_src = _read("backend/core/permissions.py")
    frontend_permissions = _read("frontend/src/lib/permissions.js")
    report = REPORT.read_text(encoding="utf-8")

    assert "PLATFORM_ROLES" in permissions_src
    assert "platform_role" in permissions_src
    assert "User.platform_role and are SEPARATE" in permissions_src
    assert "user.platform_role and are SEPARATE" in frontend_permissions
    assert "Future `account_memberships` should not replace" in report
    assert "`platform_role`" in report


def test_build_next_3_recommends_compatibility_mirror_not_direct_cutover():
    text = REPORT.read_text(encoding="utf-8")

    assert "Option A — Preserve `users.barn_id` and `users.role` through launch" in text
    assert "Option B — Stop using `users.barn_id` / `users.role` for authorization" in text
    assert "Preserve `users.barn_id` and `users.role` as compatibility mirrors" in text
    assert "through\nlaunch" in text
    assert "Very high blast radius" in text
