"""Build-Next-15C-B - barn visibility policy tests.

This phase lets barn leaders choose whether owner-safe facility roles see a
count-only total horse summary. It must not expose alerts, request details,
staff notes, task payloads, audit diffs, Stripe IDs, or other private fields.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from fastapi import HTTPException

from routes import pulse
from routes.pulse import build_today_pulse, normalize_barn_visibility_policy
from backend.tests.test_build_next_15a_today_pulse_contract import FakeDb, _membership


ROOT = Path(__file__).resolve().parents[2]


def _owner_user(role: str = "horse_owner"):
    return {"id": f"u_{role}", "role": role, "barn_id": "barn_a"}


def _owner_membership(role: str = "horse_owner"):
    return _membership(user_id=f"u_{role}", role=role, relationship_type=role)


def test_owner_safe_facility_roles_default_to_siloed_zero_barn_wide_horse_count():
    db = FakeDb(
        account_memberships=[_owner_membership()],
        barns=[{"id": "barn_a", "status": "active"}],
        horses=[
            {"id": "h1", "barn_id": "barn_a"},
            {"id": "h2", "barn_id": "barn_a"},
        ],
    )

    body = asyncio.run(build_today_pulse(db, _owner_user()))

    assert body["cards"]["horse_care"]["visible"] is True
    assert body["cards"]["horse_care"]["visibility_policy"] == "siloed"
    assert body["cards"]["horse_care"]["horses"] == 0
    assert body["cards"]["horse_care"]["open_alerts"] == 0
    assert body["cards"]["horse_care"]["urgent_alerts"] == 0


def test_community_policy_exposes_only_owner_safe_total_horse_count():
    db = FakeDb(
        account_memberships=[_owner_membership("parent")],
        barns=[{"id": "barn_a", "status": "active"}],
        barn_visibility_policies=[
            {
                "barn_id": "barn_a",
                "mode": "community",
                "owner_safe_summary_counts": {"total_horses": True, "open_alerts": True},
            }
        ],
        horses=[
            {"id": "h1", "barn_id": "barn_a", "staff_note": "horse private note"},
            {"id": "h2", "barn_id": "barn_a"},
        ],
        horse_ledger_alerts=[
            {
                "barn_id": "barn_a",
                "status": "open",
                "severity": "urgent",
                "triggers": ["owner unsafe trigger"],
                "source_check_id": "chk_hidden",
            }
        ],
        service_requests=[
            {
                "barn_id": "barn_a",
                "source": "owner_care_ledger",
                "status": "new",
                "staff_note": "request private note",
            }
        ],
        account_usage_limits=[
            {"account_id": "barn_a", "stripe_subscription_id": "sub_hidden"}
        ],
    )

    body = asyncio.run(build_today_pulse(db, _owner_user("parent")))

    assert body["cards"]["horse_care"]["visibility_policy"] == "community"
    assert body["cards"]["horse_care"]["horses"] == 2
    assert body["cards"]["horse_care"]["open_alerts"] == 0
    assert body["cards"]["horse_care"]["urgent_alerts"] == 0
    assert body["cards"]["owner_requests"]["visible"] is False
    assert body["cards"]["plan_usage"]["visible"] is False
    serialized = json.dumps(body).lower()
    assert "owner unsafe trigger" not in serialized
    assert "chk_hidden" not in serialized
    assert "private note" not in serialized
    assert "sub_hidden" not in serialized


def test_custom_policy_can_keep_owner_safe_total_horse_count_off():
    db = FakeDb(
        account_memberships=[_owner_membership("rider")],
        barns=[{"id": "barn_a", "status": "active"}],
        barn_visibility_policies=[
            {
                "barn_id": "barn_a",
                "mode": "custom",
                "owner_safe_summary_counts": {"total_horses": False},
            }
        ],
        horses=[
            {"id": "h1", "barn_id": "barn_a"},
            {"id": "h2", "barn_id": "barn_a"},
        ],
    )

    body = asyncio.run(build_today_pulse(db, _owner_user("rider")))

    assert body["cards"]["horse_care"]["visibility_policy"] == "custom"
    assert body["cards"]["horse_care"]["horses"] == 0


def test_visibility_policy_normalization_fails_closed_and_drops_unknown_toggles():
    policy = normalize_barn_visibility_policy(
        {
            "mode": "surprise",
            "owner_safe_summary_counts": {
                "total_horses": True,
                "open_alerts": True,
                "staff_notes": True,
            },
        }
    )

    assert policy["mode"] == "siloed"
    assert policy["owner_safe_summary_counts"] == {"total_horses": False}


def test_visibility_policy_denies_global_manager_on_requested_owner_only_membership():
    db = FakeDb(
        account_memberships=[
            _membership(id="m_manager", account_id="barn_manager", barn_id="barn_manager", user_id="u_multi", role="barn_manager", is_primary=True),
            _membership(id="m_owner", account_id="barn_owner_only", barn_id="barn_owner_only", user_id="u_multi", role="horse_owner", relationship_type="owner", is_primary=False),
        ],
        barns=[
            {"id": "barn_manager", "status": "active"},
            {"id": "barn_owner_only", "status": "active"},
        ],
    )

    try:
        asyncio.run(
            pulse._resolve_visibility_policy_barn(
                db,
                {"id": "u_multi", "role": "barn_manager"},
                account_id="barn_owner_only",
            )
        )
    except HTTPException as exc:
        assert exc.status_code == 403
    else:
        raise AssertionError("Owner-only membership must not inherit manager powers from another facility")


def test_visibility_policy_allows_membership_manager_even_when_global_role_is_owner():
    db = FakeDb(
        account_memberships=[
            _membership(id="m_owner", account_id="barn_owner", barn_id="barn_owner", user_id="u_multi", role="horse_owner", relationship_type="owner", is_primary=True),
            _membership(id="m_manager", account_id="barn_manager", barn_id="barn_manager", user_id="u_multi", role="barn_manager", is_primary=False),
        ],
        barns=[
            {"id": "barn_owner", "status": "active"},
            {"id": "barn_manager", "status": "active"},
        ],
    )

    barn_id = asyncio.run(
        pulse._resolve_visibility_policy_barn(
            db,
            {"id": "u_multi", "role": "horse_owner"},
            account_id="barn_manager",
        )
    )

    assert barn_id == "barn_manager"


def test_today_pulse_uses_requested_owner_only_membership_role_not_global_manager_role():
    db = FakeDb(
        account_memberships=[
            _membership(id="m_manager", account_id="barn_manager", barn_id="barn_manager", user_id="u_multi", role="barn_manager", is_primary=True),
            _membership(id="m_owner", account_id="barn_owner_only", barn_id="barn_owner_only", user_id="u_multi", role="horse_owner", relationship_type="owner", is_primary=False),
        ],
        barns=[
            {"id": "barn_manager", "status": "active"},
            {"id": "barn_owner_only", "status": "active"},
        ],
        horses=[
            {"id": "h1", "barn_id": "barn_owner_only"},
            {"id": "h2", "barn_id": "barn_owner_only"},
        ],
        horse_ledger_alerts=[
            {
                "barn_id": "barn_owner_only",
                "status": "open",
                "severity": "urgent",
                "triggers": ["owner unsafe trigger"],
                "source_check_id": "chk_hidden",
            }
        ],
        service_requests=[
            {
                "barn_id": "barn_owner_only",
                "source": "owner_care_ledger",
                "status": "new",
                "staff_note": "request private note",
            }
        ],
    )

    body = asyncio.run(
        build_today_pulse(
            db,
            {"id": "u_multi", "role": "barn_manager"},
            account_id="barn_owner_only",
        )
    )

    assert body["scope"]["role"] == "horse_owner"
    assert body["cards"]["todays_work"]["visible"] is False
    assert body["cards"]["horse_care"]["visible"] is True
    assert body["cards"]["horse_care"]["horses"] == 0
    assert body["cards"]["horse_care"]["open_alerts"] == 0
    assert body["cards"]["horse_care"]["urgent_alerts"] == 0
    assert body["cards"]["owner_requests"]["visible"] is False
    assert body["cards"]["plan_usage"]["visible"] is False
    serialized = json.dumps(body).lower()
    assert "owner unsafe trigger" not in serialized
    assert "chk_hidden" not in serialized
    assert "private note" not in serialized


def test_today_pulse_uses_requested_manager_membership_role_not_global_owner_role():
    db = FakeDb(
        account_memberships=[
            _membership(id="m_owner", account_id="barn_owner", barn_id="barn_owner", user_id="u_multi", role="horse_owner", relationship_type="owner", is_primary=True),
            _membership(id="m_manager", account_id="barn_manager", barn_id="barn_manager", user_id="u_multi", role="barn_manager", is_primary=False),
        ],
        barns=[
            {"id": "barn_owner", "status": "active"},
            {"id": "barn_manager", "status": "active"},
        ],
        horses=[{"id": "h1", "barn_id": "barn_manager"}],
        service_requests=[
            {"barn_id": "barn_manager", "source": "owner_care_ledger", "status": "new"},
        ],
    )

    body = asyncio.run(
        build_today_pulse(
            db,
            {"id": "u_multi", "role": "horse_owner"},
            account_id="barn_manager",
        )
    )

    assert body["scope"]["role"] == "barn_manager"
    assert body["cards"]["todays_work"]["visible"] is True
    assert body["cards"]["horse_care"]["horses"] == 1
    assert body["cards"]["owner_requests"]["visible"] is True
    assert body["cards"]["owner_requests"]["pending"] == 1
    assert body["cards"]["plan_usage"]["visible"] is True


def test_visibility_policy_settings_ui_is_count_only_and_manager_gated():
    settings = (ROOT / "frontend" / "src" / "pages" / "Settings.jsx").read_text(encoding="utf-8")

    assert 'data-testid="barn-visibility-policy-card"' in settings
    assert 'api.get("/account/context")' in settings
    assert 'api.get("/pulse/visibility-policy")' in settings
    assert 'api.put("/pulse/visibility-policy"' in settings
    assert "VISIBILITY_POLICY_ROLES" in settings
    assert "activeFacilityRole" in settings
    assert "activeContext?.membership_status === \"active\"" in settings
    assert "Community Count" in settings
    assert "Siloed" in settings
    assert "staff notes" in settings
    assert "alert details" in settings
    assert "open_alerts" not in settings
    assert "urgent_alerts" not in settings
