from __future__ import annotations

from pathlib import Path

from core.rf7_owner_client_portal_hardening import (
    FOUNDER_DECISIONS,
    build_rf7_owner_client_portal_hardening,
    render_rf7_report,
)


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _rows_by_key():
    report = build_rf7_owner_client_portal_hardening(ROOT)
    return {row.key: row for row in report["rows"]}


def test_rf7_report_ready_with_deferred_policy_rows():
    report = build_rf7_owner_client_portal_hardening(ROOT)
    rendered = render_rf7_report(report)

    assert report["overall_status"] == "ready"
    assert report["status_counts"].get("blocked", 0) == 0
    assert report["status_counts"].get("deferred", 0) >= 2
    assert "RF7 Owner, Guardian, and Client Portal Hardening Report" in rendered
    assert "Founder Decision Rows" in rendered
    assert "must not claim full leasee support" in rendered


def test_rf7_owner_portal_uses_owner_safe_horse_inventory_for_owner_roles():
    owner_portal = _read("frontend/src/pages/OwnerPortal.jsx")
    rows = _rows_by_key()

    assert rows["owner_portal_uses_owner_safe_horse_inventory"].status == "ready"
    assert 'OWNER_PORTAL_HORSE_ROLES = new Set(["horse_owner", "parent"])' in owner_portal
    assert 'const horseEndpoint = usesOwnerSafeHorseList ? "/owner-portal/horses" : "/horses"' in owner_portal
    assert "normalizeItems(r.data)" in owner_portal
    assert "setHorses(rows)" in owner_portal


def test_rf7_owner_and_guardian_service_submission_uses_owner_care_ledger_contract():
    owner_portal = _read("frontend/src/pages/OwnerPortal.jsx")
    rows = _rows_by_key()

    assert rows["owner_guardian_requests_use_owner_care_ledger_contract"].status == "ready"
    assert 'const usesOwnerCareRequests = OWNER_PORTAL_HORSE_ROLES.has(user?.role)' in owner_portal
    assert "if (usesOwnerCareRequests)" in owner_portal
    assert "await api.post(`/horse-ledger/${form.horse_id}/owner-service-requests`" in owner_portal
    assert "request_type: ownerLedgerRequestType(form.type)" in owner_portal
    assert "preferred_contact: \"app\"" in owner_portal
    assert "api.get(`/horse-ledger/${activeHorseId}/owner-service-requests`)" in owner_portal
    assert 'requestType = s.type || s.request_type || "request"' in owner_portal


def test_rf7_backend_owner_safe_contracts_remain_present():
    horse_ledger = _read("backend/routes/horse_ledger.py")
    backlog = _read("backend/routes/backlog.py")
    rows = _rows_by_key()

    assert rows["backend_owner_safe_horse_endpoint_exists"].status == "ready"
    assert '@router.get("/owner-portal/horses")' in horse_ledger
    assert "_owner_safe_horse_projection" in horse_ledger
    for token in ["primary_owner_id", "secondary_owner_ids", "guardian_user_ids", "rider_user_ids"]:
        assert token in horse_ledger

    assert rows["backend_owner_summary_and_request_contract_remains_safe"].status == "ready"
    assert '@router.get("/horse-ledger/{horse_id}/owner-summary")' in horse_ledger
    assert '@router.post("/horse-ledger/{horse_id}/owner-service-requests")' in horse_ledger
    assert "_strip_staff_note" in horse_ledger
    assert "_OWNER_RATE_CAP" in horse_ledger
    assert "_is_horse_guardian_for" in horse_ledger
    assert "_can_use_owner_request_contract" in horse_ledger
    assert 'role not in {"horse_owner", "parent"}' in horse_ledger
    assert 'owner_uid = (user.get("id") if role in {"horse_owner", "parent"}' in horse_ledger

    assert rows["owner_portal_backlog_feeds_use_stable_clauses"].status == "ready"
    assert "def _owner_account_clauses" in backlog
    assert "def _owner_horse_context_clauses" in backlog
    assert '@router.get("/owner-portal/media-updates")' in backlog
    assert '@router.get("/owner-portal/forms")' in backlog
    assert '@router.get("/owner-portal/health-documents")' in backlog


def test_rf7_deferred_items_are_explicit_not_overclaimed():
    rows = _rows_by_key()
    enrollment_paths = _read("frontend/src/lib/enrollmentPaths.js")
    rf5_doc = _read("docs/RF5_WEB_ENROLLMENT_ACCOUNT_HEALTH.md")
    rf6_doc = _read("docs/RF6_CANONICAL_SYSTEMS_CONSOLIDATION.md")

    assert rows["owner_updates_canonical_but_media_duplicate_deferred"].status == "deferred"
    assert rows["limited_trial_and_leasee_depth_remain_explicit"].status == "deferred"
    assert "Owner Updates is canonical" in rf6_doc
    assert "limited_individual_owner_trial" in enrollment_paths
    assert "leasee_invite_rule" in enrollment_paths
    assert "Leasee access is recorded as invite-only" in rf5_doc
    assert len(FOUNDER_DECISIONS) == 4
