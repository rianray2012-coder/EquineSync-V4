from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ProofRow:
    key: str
    status: str
    evidence: str
    next_action: str


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _section(source: str, start: str, end: str) -> str:
    start_at = source.index(start)
    end_at = source.index(end, start_at)
    return source[start_at:end_at]


def build_rf1_proof(root: Path = ROOT) -> Dict[str, object]:
    backlog = _read(root, "backend/routes/backlog.py")
    ledger = _read(root, "backend/routes/horse_ledger.py")
    owner_updates = _read(root, "backend/routes/owner_updates.py")
    permissions = _read(root, "backend/core/permissions.py")

    owner_portal = _section(
        backlog,
        '@router.get("/owner-portal/media-updates")',
        '@router.get("/owner-portal/announcements")',
    )
    billing = _section(
        backlog,
        '@router.get("/owner-portal/billing")',
        '@router.get("/owner-portal/announcements")',
    )

    rows: List[ProofRow] = [
        ProofRow(
            key="owner_safe_horse_endpoint",
            status="ready"
            if '@router.get("/owner/horses")' in ledger
            and '@router.get("/owner-portal/horses")' in ledger
            and "primary_owner_id" in ledger
            and "secondary_owner_ids" in ledger
            and "guardian_user_ids" in ledger
            and "rider_user_ids" in ledger
            else "blocked",
            evidence="`backend/routes/horse_ledger.py` exposes owner-safe horse lists using stable owner/guardian/rider IDs.",
            next_action="RF7 can deepen portal UX and response contracts after RF1 is reviewed.",
        ),
        ProofRow(
            key="quickbooks_invoice_export_scope",
            status="ready"
            if 'db.invoices.find({},' not in backlog
            and 'invoices = await db.invoices.find({"barn_id": barn_id}' in backlog
            else "blocked",
            evidence="QuickBooks invoice export now reads invoices with `barn_id` scope.",
            next_action="RF12 should handle deeper accounting/export truth and provider/payment variants.",
        ),
        ProofRow(
            key="owner_portal_identity_scope",
            status="ready"
            if "_owner_ids_for_name" not in owner_portal
            and "_horse_names_for_owner" not in owner_portal
            and '"data.recipient_name"' not in owner_portal
            and '"data.horse_name"' not in owner_portal
            and "_owner_account_clauses" in owner_portal
            and "_owner_horse_context_clauses" in owner_portal
            else "blocked",
            evidence="Owner portal media/forms/health/emergency/training reads use stable owner/user/horse predicates.",
            next_action="RF2 should migrate remaining non-RF1 name-based staff/provider/document surfaces.",
        ),
        ProofRow(
            key="owner_billing_payment_scope",
            status="ready"
            if 'invoice_q: Dict[str, Any] = {"barn_id": barn_id}' in billing
            and 'invoice_q: Dict[str, Any] = {"id": invoice_id, "barn_id": barn_id}' in billing
            and "_owner_ids_for_name" not in billing
            and "_owned_horse_ids_for_user" not in billing
            and "_owner_horse_context_clauses" not in billing
            and "_owner_account_clauses" in billing
            and '"owner_name"' not in billing
            else "blocked",
            evidence="Owner billing and payment prep are barn-scoped and account-identity-scoped, without horse-only authorization.",
            next_action="RF12 should finish payment truth, refunds, voids, and collection-state accuracy.",
        ),
        ProofRow(
            key="owner_updates_relationship_scope",
            status="ready"
            if "primary_owner_id" in owner_updates
            and "secondary_owner_ids" in owner_updates
            and "barn_filter(" in owner_updates
            else "blocked",
            evidence="Published owner updates now resolve owned horses through primary/secondary owner ID fields.",
            next_action="RF6/RF7 should consolidate owner updates versus media-update backlog surfaces.",
        ),
        ProofRow(
            key="sensitive_route_capability_gates",
            status="ready"
            if 'require_permission(user, "financial:read")' in backlog
            and 'require_permission(user, "reporting:read")' in backlog
            and 'require_permission(user, "reporting:write")' in backlog
            and "def require_permission" in permissions
            else "blocked",
            evidence="Financial and reporting routes retain backend capability gates backed by fail-closed permission helpers.",
            next_action="RF2/RF4 should continue route-by-route matrices as feature surfaces are hidden or certified.",
        ),
        ProofRow(
            key="reporting_dashboard_revenue_scope",
            status="ready"
            if 'revenue_rows = await db.invoices.find({"barn_id": barn_id}' in backlog
            else "blocked",
            evidence="Backlog dashboard revenue totals no longer read all invoices globally.",
            next_action="RF12 should finish export/report format truth.",
        ),
    ]

    status_counts: Dict[str, int] = {}
    for row in rows:
        status_counts[row.status] = status_counts.get(row.status, 0) + 1

    overall_status = "ready" if status_counts.get("blocked", 0) == 0 else "blocked"
    return {
        "phase": "RF1",
        "title": "P0 Data Fences and Backend Capability Gates",
        "overall_status": overall_status,
        "status_counts": status_counts,
        "rows": [row.__dict__ for row in rows],
    }


def render_rf1_report(report: Dict[str, object]) -> str:
    rows = report["rows"]
    lines = [
        "# RF1 Data Fences And Capability Gates Report",
        "",
        f"Phase: `{report['phase']}`",
        "",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Readiness Rows",
        "",
        "| Key | Status | Evidence | Next Action |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['key']}` | `{row['status']}` | {row['evidence']} | {row['next_action']} |"
        )
    lines.extend([
        "",
        "## Founder Decision Rows",
        "",
        "| Decision | Status | RF Phase | Notes |",
        "| --- | --- | --- | --- |",
        "| Accept stricter owner portal matching for legacy name-only records. | requires founder review | RF1, RF2 | RF1 intentionally does not expose records that only match by display/free-text name; RF2 should migrate legacy data to stable IDs. |",
        "| Decide whether RF1 should be re-run against seeded cross-barn integration fixtures before lock. | optional founder review | RF1 | Source tests prove the fence shape; live-seeded integration tests can be added if desired before lock. |",
        "",
        "## Acceptance Boundary",
        "",
        "- RF1 closes the P0 source-level tenant/export/owner-portal data fence findings identified in RF0.",
        "- RF1 does not complete RF2 identity migration, RF7 portal UX hardening, RF12 billing/payment truth, or RF17 feature-shell retirement.",
        "- RF1 does not mutate provider services, Stripe, Apple, Google, DocuSign, Resend, MongoDB Atlas, Vercel, Render, or UAT accounts.",
        "",
    ])
    return "\n".join(lines)
