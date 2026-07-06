from __future__ import annotations

from pathlib import Path

from core.rf1_data_fences_capability_gates_proof import build_rf1_proof, render_rf1_report


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _section(source: str, start: str, end: str) -> str:
    start_at = source.index(start)
    end_at = source.index(end, start_at)
    return source[start_at:end_at]


def test_rf1_quickbooks_and_dashboard_invoice_reads_are_barn_scoped():
    backlog = _read("backend/routes/backlog.py")

    assert 'db.invoices.find({},' not in backlog
    assert 'invoices = await db.invoices.find({"barn_id": barn_id}' in backlog
    assert 'revenue_rows = await db.invoices.find({"barn_id": barn_id}' in backlog


def test_rf1_owner_portal_access_does_not_use_display_name_fallbacks():
    backlog = _read("backend/routes/backlog.py")
    owner_portal = _section(
        backlog,
        '@router.get("/owner-portal/media-updates")',
        '@router.get("/owner-portal/announcements")',
    )

    forbidden = [
        "_owner_ids_for_name",
        "_horse_names_for_owner",
        '"owner_name": owner_name',
        '"data.owner_name"',
        '"data.recipient_name"',
        '"data.horse_name"',
        '"data.shared_with"',
        '"data.person_name"',
        '"data.primary_contact"',
    ]
    for token in forbidden:
        assert token not in owner_portal

    assert "_owner_link_ids_for_user" in owner_portal
    assert "_owned_horse_ids_for_user" in owner_portal
    assert "_owner_account_clauses" in owner_portal
    assert "_owner_horse_context_clauses" in owner_portal
    assert 'legacy_training_q: Dict[str, Any] = {"barn_id": barn_id}' in owner_portal


def test_rf1_owner_portal_billing_is_barn_and_identity_scoped():
    backlog = _read("backend/routes/backlog.py")
    billing = _section(
        backlog,
        '@router.get("/owner-portal/billing")',
        '@router.get("/owner-portal/announcements")',
    )

    assert 'invoice_q: Dict[str, Any] = {"barn_id": barn_id}' in billing
    assert 'invoice_q: Dict[str, Any] = {"id": invoice_id, "barn_id": barn_id}' in billing
    assert 'invoice_q["$or"] = invoice_clauses' in billing
    assert 'payment_q["$or"] = invoice_clauses' in billing
    assert 'recurring_q["$or"] = invoice_clauses' in billing
    assert "_owner_ids_for_name" not in billing
    assert "_owned_horse_ids_for_user" not in billing
    assert "_owner_horse_context_clauses" not in billing
    assert "_owner_account_clauses" in billing
    assert '"owner_name"' not in billing


def test_rf1_forms_signing_uses_account_recipient_scope_not_horse_only_scope():
    backlog = _read("backend/routes/backlog.py")
    forms = _section(
        backlog,
        '@router.get("/owner-portal/forms")',
        '@router.get("/owner-portal/health-documents")',
    )

    assert "_owner_account_clauses" in forms
    assert "_owner_horse_context_clauses" not in forms
    assert "_owned_horse_ids_for_user" not in forms


def test_rf1_owner_safe_horse_endpoint_uses_stable_relationships():
    ledger = _read("backend/routes/horse_ledger.py")

    assert '@router.get("/owner/horses")' in ledger
    assert '@router.get("/owner-portal/horses")' in ledger
    assert "role not in {\"horse_owner\", \"parent\", \"rider\"}" in ledger
    assert '"barn_id": resolve_barn_id(user)' in ledger
    for field in [
        "primary_owner_id",
        "secondary_owner_ids",
        "guardian_user_ids",
        "rider_user_ids",
    ]:
        assert field in ledger


def test_rf1_owner_update_reads_include_primary_and_secondary_owner_ids():
    owner_updates = _read("backend/routes/owner_updates.py")
    owner_reader = _section(
        owner_updates,
        "async def _owner_horse_ids",
        "# ---------------- Create (staff) ----------------",
    )

    assert "primary_owner_id" in owner_reader
    assert "secondary_owner_ids" in owner_reader
    assert "owner_user_ids" in owner_reader
    assert 'barn_filter(' in owner_reader


def test_rf1_sensitive_routes_have_backend_capability_gates():
    backlog = _read("backend/routes/backlog.py")
    permissions = _read("backend/core/permissions.py")

    assert 'require_permission(user, "financial:read")' in backlog
    assert 'require_permission(user, "reporting:read")' in backlog
    assert 'require_permission(user, "reporting:write")' in backlog
    assert "def require_permission" in permissions
    assert "raise HTTPException(status_code=403" in permissions


def test_rf1_proof_report_renders_ready_rows():
    report = build_rf1_proof(ROOT)
    rendered = render_rf1_report(report)

    assert report["overall_status"] == "ready"
    assert report["status_counts"]["ready"] >= 7
    assert "RF1 Data Fences And Capability Gates Report" in rendered
    assert "## Founder Decision Rows" in rendered
    assert "legacy name-only records" in rendered
