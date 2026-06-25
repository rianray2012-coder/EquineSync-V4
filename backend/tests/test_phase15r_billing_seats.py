"""Phase 15R-E — billing seat-type classification prep.

Local-only tests. They pin future user-seat fields without writing Mongo,
changing checkout, touching webhooks, or calling Stripe/Apple.
"""
from __future__ import annotations

import pathlib
import re

from core.billing_seats import (
    ACCOUNT_ORIGINS,
    BILLING_SEAT_TYPES,
    PLATFORM_BILLING_ROLES,
    PORTAL_ACCESS_STATUSES,
    build_billing_seat_dry_run,
    build_cleanup_checklist,
    classify_billing_seat,
    render_billing_seat_markdown,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_vocabulary_matches_pricing_foundation():
    assert BILLING_SEAT_TYPES == (
        "owner_manager",
        "staff",
        "helper_family",
        "client_owner_portal",
        "lesson_participant",
        "platform_admin",
        "none",
    )
    assert ACCOUNT_ORIGINS == (
        "self_subscribed",
        "invited_by_barn",
        "invited_by_trainer",
        "platform_created",
    )
    assert PORTAL_ACCESS_STATUSES == ("active", "invited", "disabled")
    permissions_src = (ROOT / "backend" / "core" / "permissions.py").read_text()
    match = re.search(r"PLATFORM_ROLES:\s*Set\[str\]\s*=\s*\{(?P<body>.*?)\}", permissions_src, re.S)
    assert match, "core.permissions.PLATFORM_ROLES set was not found"
    permission_roles = set(re.findall(r'"([^"]+)"', match.group("body")))
    assert PLATFORM_BILLING_ROLES == permission_roles


def test_existing_valid_billing_seat_type_wins():
    projected = classify_billing_seat({
        "role": "horse_owner",
        "billing_seat_type": "client_owner_portal",
        "account_origin": "invited_by_trainer",
        "portal_access_status": "invited",
    })
    assert projected == {
        "billing_seat_type": "client_owner_portal",
        "account_origin": "invited_by_trainer",
        "portal_access_status": "invited",
        "source": "explicit",
        "needs_review": False,
        "companion_issues": [],
    }


def test_platform_role_projects_to_platform_admin_seat():
    projected = classify_billing_seat({"role": "horse_owner", "platform_role": "super_admin"})
    assert projected["billing_seat_type"] == "platform_admin"
    assert projected["account_origin"] == "platform_created"
    assert projected["portal_access_status"] == "active"
    assert projected["needs_review"] is False


def test_owner_manager_and_staff_roles_project_to_billable_seats():
    assert classify_billing_seat({"role": "admin"})["billing_seat_type"] == "owner_manager"
    assert classify_billing_seat({"role": "barn_manager"})["billing_seat_type"] == "owner_manager"
    assert classify_billing_seat({"role": "barn_owner"})["billing_seat_type"] == "owner_manager"
    assert classify_billing_seat({"role": "groom"})["billing_seat_type"] == "staff"
    assert classify_billing_seat({"role": "working_student"})["billing_seat_type"] == "staff"
    assert classify_billing_seat({"role": "farrier"})["billing_seat_type"] == "staff"


def test_invited_owner_portal_accounts_stay_free_and_non_staff():
    barn_owner = classify_billing_seat({
        "role": "horse_owner",
        "account_origin": "invited_by_barn",
    })
    trainer_owner = classify_billing_seat({
        "role": "parent",
        "account_origin": "invited_by_trainer",
    })
    assert barn_owner["billing_seat_type"] == "client_owner_portal"
    assert trainer_owner["billing_seat_type"] == "client_owner_portal"
    assert barn_owner["billing_seat_type"] != "staff"
    assert trainer_owner["billing_seat_type"] != "owner_manager"
    assert barn_owner["needs_review"] is False


def test_self_subscribed_owner_projects_to_owner_manager_paid_path():
    projected = classify_billing_seat({
        "role": "horse_owner",
        "account_origin": "self_subscribed",
    })
    assert projected["billing_seat_type"] == "owner_manager"
    assert projected["account_origin"] == "self_subscribed"
    assert projected["needs_review"] is False


def test_rider_projects_to_lesson_participant():
    projected = classify_billing_seat({"role": "rider"})
    assert projected["billing_seat_type"] == "lesson_participant"
    assert projected["account_origin"] == "invited_by_barn"
    assert projected["portal_access_status"] == "active"


def test_ambiguous_professional_roles_are_warning_only():
    projected = classify_billing_seat({"role": "trainer"})
    assert projected["billing_seat_type"] == "staff"
    assert projected["needs_review"] is True
    report = build_billing_seat_dry_run([{"id": "u1", "email": "t@example.com", "role": "trainer"}])
    assert report["issue_counts"] == {"warning": 1}
    assert report["issues"][0]["kind"] == "seat_type_needs_review"


def test_invalid_existing_billing_seat_type_warns_but_does_not_block():
    report = build_billing_seat_dry_run([{
        "id": "u2",
        "email": "x@example.com",
        "role": "horse_owner",
        "billing_seat_type": "paid_owner_maybe",
    }])
    assert report["seat_counts"]["client_owner_portal"] == 1
    assert report["issue_counts"] == {"warning": 2}
    assert {issue["kind"] for issue in report["issues"]} == {
        "seat_type_needs_review",
        "invalid_existing_billing_seat_type",
    }


def test_explicit_billing_seat_type_warns_on_missing_companion_fields():
    projected = classify_billing_seat({
        "id": "u3",
        "role": "horse_owner",
        "billing_seat_type": "client_owner_portal",
    })
    assert projected["billing_seat_type"] == "client_owner_portal"
    assert projected["source"] == "explicit"
    assert projected["needs_review"] is True
    assert {issue["kind"] for issue in projected["companion_issues"]} == {
        "missing_or_invalid_account_origin",
        "missing_or_invalid_portal_access_status",
    }

    report = build_billing_seat_dry_run([{
        "id": "u3",
        "role": "horse_owner",
        "billing_seat_type": "client_owner_portal",
        "account_origin": "mystery",
        "portal_access_status": "maybe",
    }])
    assert report["seat_counts"]["client_owner_portal"] == 1
    assert report["issue_counts"] == {"warning": 3}
    assert {issue["kind"] for issue in report["issues"]} == {
        "seat_type_needs_review",
        "missing_or_invalid_account_origin",
        "missing_or_invalid_portal_access_status",
    }


def test_report_markdown_is_read_only_and_has_preview_table():
    report = build_billing_seat_dry_run([
        {"id": "u1", "email": "admin@example.com", "role": "admin"},
        {"id": "u2", "email": "owner@example.com", "role": "horse_owner", "account_origin": "invited_by_barn"},
    ])
    md = render_billing_seat_markdown(report)
    assert "# Phase 15R-E Billing Seat Classification Dry-Run" in md
    assert "No Mongo writes" in md
    assert "owner_manager" in md
    assert "client_owner_portal" in md
    assert "No `users` rows are updated." in md


def test_cleanup_checklist_groups_warning_issues_by_user_record():
    report = build_billing_seat_dry_run([
        {"id": "u1", "email": "trainer@example.com", "role": "trainer"},
        {
            "id": "u2",
            "email": "owner@example.com",
            "role": "horse_owner",
            "billing_seat_type": "client_owner_portal",
        },
    ])

    checklist = build_cleanup_checklist(report["preview_rows"], report["issues"])
    by_record = {item["record"]: item for item in checklist}

    assert set(by_record) == {"u1", "u2"}
    assert by_record["u1"]["email"] == "trainer@example.com"
    assert by_record["u1"]["suggested_billing_seat_type"] == "staff"
    assert by_record["u1"]["suggested_account_origin"] == "platform_created"
    assert by_record["u1"]["suggested_portal_access_status"] == "active"
    assert by_record["u1"]["issue_kinds"] == ["seat_type_needs_review"]
    assert by_record["u1"]["action"] == "review_before_migration"

    assert by_record["u2"]["suggested_billing_seat_type"] == "client_owner_portal"
    assert set(by_record["u2"]["issue_kinds"]) == {
        "seat_type_needs_review",
        "missing_or_invalid_account_origin",
        "missing_or_invalid_portal_access_status",
    }
    assert by_record["u2"]["action"] == "review_before_migration"


def test_cleanup_checklist_renders_in_markdown_report():
    report = build_billing_seat_dry_run([{
        "id": "u3",
        "email": "helper@example.com",
        "role": "service_provider",
    }])
    md = render_billing_seat_markdown(report)

    assert "## Founder Cleanup Checklist" in md
    assert "helper@example.com" in md
    assert "staff" in md
    assert "seat_type_needs_review" in md
    assert "review_before_migration" in md


def test_dry_run_script_is_read_only_and_requires_mongo_url():
    src = (ROOT / "backend" / "scripts" / "phase15r_billing_seat_dry_run.py").read_text()
    assert "MONGO_URL" in src
    assert "db.users.find" in src
    assert "Could not read Mongo users collection" in src
    assert "update_one" not in src
    assert "insert_one" not in src
    assert "delete_one" not in src
    assert "stripe" not in src.lower()


def test_subscription_usage_route_uses_billing_seat_type_not_role_only():
    src = (ROOT / "backend" / "routes" / "subscriptions.py").read_text()
    assert '{"billing_seat_type": "staff"}' in src
    assert '{"billing_seat_type": "owner_manager"}' in src
    assert "users_used = staff_used + owner_manager_used" in src
