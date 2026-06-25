"""Phase 15R-D — usage/add-on prompt readiness.

Local-only tests. They pin the soft-prompt contract without calling Stripe,
Apple, Checkout, webhooks, or Mongo.
"""
from __future__ import annotations

import pathlib

from core.subscription_usage import (
    build_addon_suggestions,
    build_usage_entry,
    scrub_addon_catalog,
    suggested_addon_code,
    usage_pressure,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_usage_pressure_is_soft_and_threshold_based():
    assert usage_pressure(0, None) == "unlimited"
    assert usage_pressure(0, 0) == "ok"
    assert usage_pressure(1, 0) == "over"
    assert usage_pressure(7, 10) == "ok"
    assert usage_pressure(8, 10) == "approaching"
    assert usage_pressure(10, 10) == "over"
    assert usage_pressure(12, 10) == "over"


def test_usage_entry_adds_soft_upgrade_prompt_at_threshold():
    entry = build_usage_entry(
        key="horses",
        used=8,
        limit=10,
        plan_code="starter_barn",
    )
    assert entry == {
        "used": 8,
        "limit": 10,
        "remaining": 2,
        "pressure": "approaching",
        "soft_only": True,
        "upgrade_prompt": True,
        "suggested_addon_code": "additional_horse_starter",
    }


def test_usage_entry_never_prompts_for_unlimited_limits():
    entry = build_usage_entry(
        key="horses",
        used=999,
        limit=None,
        plan_code="enterprise",
    )
    assert entry["pressure"] == "unlimited"
    assert entry["remaining"] is None
    assert entry["soft_only"] is True
    assert entry["upgrade_prompt"] is False
    assert "suggested_addon_code" not in entry


def test_plan_specific_addon_suggestions_are_stable():
    assert suggested_addon_code("horses", "starter_barn") == "additional_horse_starter"
    assert suggested_addon_code("horses", "advanced_barn") == "additional_horse_advanced"
    assert suggested_addon_code("horses", "trainer_lesson_50") == "additional_horse_standard"
    assert suggested_addon_code("staff", "starter_barn") == "additional_staff_seat"
    assert suggested_addon_code("owner_managers", "elite_barn") == "elite_owner_manager_seat"
    assert suggested_addon_code("owner_managers", "advanced_barn") == "additional_owner_manager_seat"
    assert suggested_addon_code("lesson_participants", "trainer_lesson_50") == "additional_lesson_participant"
    assert suggested_addon_code("storage_gb", "starter_barn") == "extra_storage"


def test_addon_suggestions_are_derived_from_usage_entries_only():
    usage = {
        "horses": build_usage_entry(key="horses", used=11, limit=10, plan_code="starter_barn"),
        "staff": build_usage_entry(key="staff", used=1, limit=3, plan_code="starter_barn"),
        "storage_gb": build_usage_entry(key="storage_gb", used=5, limit=None, plan_code="starter_barn"),
    }
    assert build_addon_suggestions(usage) == [{
        "usage_key": "horses",
        "pressure": "over",
        "addon_code": "additional_horse_starter",
        "soft_only": True,
    }]


def test_scrub_addon_catalog_omits_operational_stripe_ids():
    rows = [{
        "addon_code": "additional_staff_seat",
        "stripe_product_id": "prod_should_not_cross_boundary",
        "stripe_price_id": "price_should_not_cross_boundary",
        "billing_provider": "stripe",
        "billing_channel": "web",
        "recurring": True,
        "limit_field": "staff_limit",
        "quantity_field": "extra_staff_quantity",
        "is_active": True,
    }]
    scrubbed = scrub_addon_catalog(rows)
    assert scrubbed == [{
        "addon_code": "additional_staff_seat",
        "billing_provider": "stripe",
        "billing_channel": "web",
        "recurring": True,
        "limit_field": "staff_limit",
        "quantity_field": "extra_staff_quantity",
        "is_active": True,
    }]
    assert "stripe_price_id" not in scrubbed[0]
    assert "stripe_product_id" not in scrubbed[0]


def test_addons_route_projects_out_operational_stripe_ids_before_scrubbing():
    src = (ROOT / "backend" / "routes" / "subscriptions.py").read_text()
    assert '"stripe_product_id": 0' in src
    assert '"stripe_price_id": 0' in src


def test_billing_usage_route_prefers_account_usage_limits_and_keeps_legacy_keys():
    src = (ROOT / "backend" / "routes" / "subscriptions.py").read_text()
    assert 'db.account_usage_limits.find_one({"account_id": barn["id"]}' in src
    assert 'plan_doc = await db.plans.find_one({"tier_code": plan_tier}' in src
    assert '"users": users_limit' in src
    assert '"limits_source": limits_source' in src
    assert '"add_on_suggestions": build_addon_suggestions(usage)' in src
    assert '"horses": build_usage_entry(' in src
    assert '"users": build_usage_entry(' in src
    assert '"storage_gb": build_usage_entry(' in src
    assert '"staff": build_usage_entry(' in src
    assert '"owner_managers": build_usage_entry(' in src
    assert '"lesson_participants": build_usage_entry(' in src


def test_billing_usage_users_meter_excludes_free_owner_portal_accounts():
    src = (ROOT / "backend" / "routes" / "subscriptions.py").read_text()
    assert "BILLABLE_STAFF_ROLES" in src
    assert "BILLABLE_OWNER_MANAGER_ROLES" in src
    assert '{"billing_seat_type": "staff"}' in src
    assert '{"billing_seat_type": "owner_manager"}' in src
    assert "users_used = staff_used + owner_manager_used" in src
    usage_section = src.split('@router.get("/billing/usage")', 1)[1].split('@router.post("/subscriptions/checkout")', 1)[0]
    assert '"role_status": {"$ne": "rejected"}' in usage_section
    assert "client_owner_portal" not in usage_section
    assert 'db.users.count_documents({\n            "barn_id": barn["id"],\n            "role_status": {"$ne": "rejected"},\n        })' not in usage_section


def test_billing_addons_route_is_read_only_and_scrubs_stripe_ids():
    src = (ROOT / "backend" / "routes" / "subscriptions.py").read_text()
    assert '@router.get("/billing/addons")' in src
    section = src.split('@router.get("/billing/addons")', 1)[1].split('@router.get("/billing/usage")', 1)[0]
    assert "stripe_price_id" in section
    assert "scrub_addon_catalog" in section
    assert "update_one" not in section
    assert "insert_one" not in section
    assert "stripe.checkout.Session.create" not in section
