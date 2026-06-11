"""Local contract checks for backlog module metadata and permissions."""

import pytest

from core.permissions import can
from routes.backlog import (
    BACKLOG_AUDIT_COLLECTION,
    BACKLOG_COLLECTIONS,
    BACKLOG_LOCATION_SHARE_COLLECTION,
    BACKLOG_RESET_COLLECTIONS,
    MODULES,
    _accounting_amount,
    _accounting_label,
    _calendar_event,
    _events_to_ics,
    _location_board_payload,
    _matches_report_filters,
    _payroll_hours,
    _push_payload,
    _stall_card_svg,
    _required_fields,
    _safe_filename,
)
from storage import validate_upload


def test_backlog_modules_cover_requested_feature_groups():
    groups = {m["group"] for m in MODULES.values()}
    assert {
        "Operations",
        "Health",
        "Financial",
        "Communication",
        "Training",
        "Staff",
        "AI & Automation",
        "Mobile & Integrations",
    }.issubset(groups)


def test_module_required_fields_are_declared():
    assert "stall_id" in _required_fields(MODULES["stall-map"])
    assert "client_name" in _required_fields(MODULES["waitlist"])
    assert "amount" in _required_fields(MODULES["expenses"])
    assert "name" in _required_fields(MODULES["supply-inventory"])
    assert "horse_name" in _required_fields(MODULES["farrier-history"])
    assert "medication_name" in _required_fields(MODULES["medication-logs"])
    assert "case_title" in _required_fields(MODULES["injury-tracking"])
    assert "horse_name" in _required_fields(MODULES["emergency-workflows"])
    assert "form_name" in _required_fields(MODULES["forms-signatures"])
    assert "shift_start" in _required_fields(MODULES["staff-scheduling"])
    assert "summary" in _required_fields(MODULES["handoff-reports"])
    assert "target_module" in _required_fields(MODULES["offline-sync"])
    assert "file_url" in _required_fields(MODULES["document-scans"])
    assert "qr_code" in _required_fields(MODULES["qr-horse-id"])
    assert "subject" in _required_fields(MODULES["ai-automation"])


def test_backlog_collection_export_matches_modules():
    assert sorted({m["collection"] for m in MODULES.values()}) == BACKLOG_COLLECTIONS
    assert "shift_handoff_reports" in BACKLOG_COLLECTIONS
    assert "document_scan_jobs" in BACKLOG_COLLECTIONS
    assert BACKLOG_AUDIT_COLLECTION in BACKLOG_RESET_COLLECTIONS
    assert BACKLOG_LOCATION_SHARE_COLLECTION in BACKLOG_RESET_COLLECTIONS


def test_permission_matrix_for_backlog_roles():
    assert can({"role": "admin"}, "financial:write")
    assert can({"role": "barn_manager"}, "staff:write")
    assert can({"role": "trainer"}, "training:write")
    assert can({"role": "groom"}, "operations:write")
    assert not can({"role": "horse_owner"}, "health:read")
    assert not can({"role": "horse_owner"}, "staff:write")
    assert not can({"role": "groom"}, "financial:write")


def test_report_export_helpers_are_stable():
    record = {"status": "active", "data": {"horse_name": "Valentino", "category": "feed"}}
    assert _safe_filename("Monthly Barn Performance!") == "monthly-barn-performance"
    assert _matches_report_filters(record, {"status": "active", "horse_name": "Valentino"})
    assert _matches_report_filters(record, {"category": ["feed", "hay"]})
    assert not _matches_report_filters(record, {"status": "archived"})


def test_payroll_hours_account_for_breaks_and_open_entries():
    assert _payroll_hours({
        "clock_in": "2026-06-10T07:00:00",
        "clock_out": "2026-06-10T15:30:00",
        "break_minutes": 30,
    }) == 8.0
    assert _payroll_hours({
        "clock_in": "2026-06-10T07:00:00",
        "clock_out": "",
        "break_minutes": 0,
    }) == 0.0


def test_calendar_export_helpers_create_ics_events():
    event = _calendar_event(
        source="competitions",
        record={"id": "show-1"},
        title="Show: Silver Waters",
        start="2026-07-18",
        all_day=True,
        description="Valentino",
    )
    ics = _events_to_ics([event])
    assert event["uid"] == "competitions-show-1@equinesync.local"
    assert event["all_day"] is True
    assert "BEGIN:VEVENT" in ics
    assert "SUMMARY:Show: Silver Waters" in ics
    assert "DTSTART;VALUE=DATE:20260718" in ics


def test_quickbooks_export_helpers_normalize_accounting_values():
    assert _accounting_amount("42") == "42.00"
    assert _accounting_amount("bad") == "0.00"
    assert _accounting_label("accounts_receivable") == "accounts receivable"
    assert _accounting_label("") == "uncategorized"


def test_push_payload_preview_is_bounded_and_readable():
    payload = _push_payload(
        source="group_messages",
        record={"id": "msg-1"},
        title="A" * 100,
        body="B" * 220,
        audience="all_staff",
        metadata={"channel": "push_ready"},
    )
    assert payload["record_id"] == "msg-1"
    assert payload["audience"] == "all staff"
    assert payload["delivery_status"] == "preview_only"
    assert len(payload["title"]) == 80
    assert len(payload["body"]) == 180


def test_stall_card_svg_includes_horse_qr_and_escaped_text():
    svg = _stall_card_svg({
        "horse_name": "Valentino & Co",
        "qr_code": "EQSYNC-VAL-001",
        "profile_url": "/horses/valentino",
        "stall_location": "A-01",
    })
    assert svg.startswith("<svg")
    assert "Valentino &amp; Co" in svg
    assert "EQSYNC-VAL-001" in svg
    assert "/horses/valentino" in svg


def test_document_scan_upload_validation_allows_documents_only():
    validate_upload("document", "application/pdf", 1024)
    with pytest.raises(Exception):
        validate_upload("document", "text/plain", 1024)


def test_location_board_payload_combines_stalls_and_pastures():
    payload = _location_board_payload(
        share={"enabled": True, "title": "Board"},
        stalls=[{"id": "stall-1", "data": {"horse_name": "Valentino", "stall_id": "A-01", "status": "occupied"}}],
        pastures=[{"id": "pasture-1", "data": {"pasture": "North", "horse_names": "Mercury, Juniper", "status": "active"}}],
    )
    assert payload["stats"]["horses_located"] == 3
    assert payload["horse_locations"][0]["horse_name"] == "Juniper"
    assert any(row["location_type"] == "pasture" for row in payload["horse_locations"])
