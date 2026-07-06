from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RF10Row:
    key: str
    area: str
    status: str
    evidence: str
    next_action: str


FOUNDER_DECISIONS = [
    {
        "decision": "Choose first RF10 provider type for UAT.",
        "status": "requires founder review",
        "phase": "RF10",
        "notes": "Recommended first choice remains farrier or veterinarian because both require explicit horse grants and visit-note context.",
    },
    {
        "decision": "Decide service-provider signup review posture.",
        "status": "requires founder review",
        "phase": "RF5, RF10",
        "notes": "RF5 separates service-provider enrollment; RF10 keeps approval posture as founder-review work.",
    },
    {
        "decision": "Decide provider grant authority.",
        "status": "requires founder review",
        "phase": "RF10, RF18",
        "notes": "Current RF10 mutation path is barn admin / manager through Care Ledger provider assignment rows.",
    },
    {
        "decision": "Decide provider invoice/payment timing.",
        "status": "requires founder review",
        "phase": "RF10, RF12",
        "notes": "RF10 does not implement provider invoice/payment/payout truth.",
    },
]


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _status_counts(rows: Iterable[RF10Row]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf10_service_provider_care_partner(root: Path = ROOT) -> Dict[str, object]:
    provider_access = _read(root, "backend/core/provider_access.py")
    provider_center = _read(root, "backend/routes/service_provider_center.py")
    horses = _read(root, "backend/routes/horses.py")
    care = _read(root, "backend/routes/care.py")
    horse_ledger = _read(root, "backend/routes/horse_ledger.py")
    server = _read(root, "backend/server.py")
    dashboard = _read(root, "frontend/src/features/dashboards/ServiceProviderDashboard.jsx")
    app = _read(root, "frontend/src/App.js")
    rf10_plan = _read(root, "docs/RF10_SERVICE_PROVIDER_CARE_PARTNER_PLAN.md")

    rows = [
        RF10Row(
            key="provider_grant_helper",
            area="Explicit provider grant helper",
            status="ready"
            if _contains_all(
                provider_access,
                [
                    "PROVIDER_ROLES",
                    "provider_grants",
                    "horse_provider_assignments",
                    "provider_user_id",
                    "ACTIVE_GRANT_STATUS",
                    "require_provider_horse_access",
                ],
            )
            else "blocked",
            evidence="RF10 adds a shared provider-access helper driven by active explicit horse-provider assignments, same-barn stable provider user IDs, and explicit provider catalog links.",
            next_action="RF18 should seed revoked/cross-barn/provider-type UAT cases.",
        ),
        RF10Row(
            key="provider_operating_center",
            area="Service-provider operating center API",
            status="ready"
            if _contains_all(
                provider_center,
                [
                    '@router.get("/operating-center")',
                    "_require_provider(user)",
                    "grant_horse_filter(grants)",
                    "grant_care_filter(grants)",
                    "_safe_grant",
                    "provider_visit_notes",
                    '"provider_invoices": "RF12 billing/payment/provider invoice truth"',
                ],
            )
            and _contains_all(server, ["build_service_provider_center_router", "dependencies=PRODUCT_FACILITY_DEPS"])
            else "blocked",
            evidence="RF10 adds a provider-role operating center for grant-scoped horses, vet records, farrier records, and provider-authored visit notes.",
            next_action="RF18 should browser-smoke seeded provider accounts.",
        ),
        RF10Row(
            key="direct_horse_and_care_scoping",
            area="Direct route provider scoping",
            status="ready"
            if _contains_all(horses, ["is_provider_user(user)", "provider_grants(db, user)", "grant_horse_filter"])
            and _contains_all(care, ["is_provider_user(user)", "_provider_care_scope", "grant_care_filter", "_provider_medication_log_filter", "Service providers cannot manage owner records"])
            else "blocked",
            evidence="Provider roles no longer inherit broad direct horse/care reads; legacy horse and care routes use explicit provider grants, including medication-log filtering by granted medication and barn.",
            next_action="RF18 should add full browser UAT against direct-route attempts.",
        ),
        RF10Row(
            key="provider_canonical_care_writes_restricted",
            area="Canonical care write boundary",
            status="ready"
            if _contains_all(
                care,
                [
                    "_reject_provider_care_write",
                    "Service providers must use provider visit notes for RF10 care entries",
                    '@router.post("/vet-records")',
                    '@router.post("/wellness")',
                    '@router.post("/medication-logs")',
                ],
            )
            else "blocked",
            evidence="RF10 limits provider-authored care entries to provider visit notes; canonical care creates remain facility-owned until a later policy phase.",
            next_action="Founder should decide which provider types may write canonical care records before that scope is enabled.",
        ),
        RF10Row(
            key="provider_assignment_stable_user_ids",
            area="Provider assignment stable IDs",
            status="ready"
            if _contains_all(
                horse_ledger,
                [
                    '"provider_user_id"',
                    "service_provider_user_exists",
                    "provider_user_id must reference a same-barn provider user",
                    "provider_user_id must match the linked provider",
                ],
            )
            else "blocked",
            evidence="Care Ledger service-provider and assignment rows can now link to stable provider user IDs with same-barn validation.",
            next_action="Founder should decide grant authority and provider approval posture before broader claims.",
        ),
        RF10Row(
            key="account_level_provider_identity",
            area="Cross-facility provider identity",
            status="deferred",
            evidence="RF10 proves explicit grant scoping and same-barn stable provider_user_id assignment validation; account-level provider identity across unrelated barns remains deferred.",
            next_action="RF18 or a future account-membership policy phase should prove stable cross-facility provider identity before stronger multi-barn claims.",
        ),
        RF10Row(
            key="provider_dashboard_not_shell",
            area="Service-provider dashboard",
            status="ready"
            if _contains_all(
                dashboard,
                [
                    "/service-provider/operating-center",
                    "Service Provider Center",
                    "shared_horses",
                    "recent_vet_records",
                    "recent_farrier_records",
                    'data-testid="dashboard-service-provider"',
                ],
            )
            and 'path="/dashboard/service-provider"' in app
            else "blocked",
            evidence="Service-provider dashboard now renders grant-scoped provider work instead of static shell cards.",
            next_action="RF18 should capture provider screenshots with seeded grants.",
        ),
        RF10Row(
            key="provider_billing_deferred",
            area="Provider billing and payouts",
            status="deferred"
            if _contains_all(rf10_plan, ["RF12", "provider invoice/payment timing"])
            else "blocked",
            evidence="RF10 does not implement provider invoices, payouts, refunds, Stripe, or payment truth.",
            next_action="RF12 owns billing/payment/provider invoice truth.",
        ),
        RF10Row(
            key="provider_documents_messaging_deferred",
            area="Provider documents and messaging",
            status="deferred"
            if _contains_all(rf10_plan, ["RF13", "RF14"])
            else "blocked",
            evidence="RF10 does not implement messaging delivery truth, legal signatures, or provider document storage truth.",
            next_action="RF13 owns delivery truth; RF14 owns legal document/signature/storage truth.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF10",
        "title": "RF10 Service Provider / Care Partner Multi-Barn Model",
        "overall_status": "ready" if counts.get("blocked", 0) == 0 and counts.get("missing", 0) == 0 else "blocked",
        "status_counts": counts,
        "rows": rows,
        "founder_decisions": FOUNDER_DECISIONS,
    }


def _table(headers: List[str], rows: List[List[str]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def render_rf10_report(report: Dict[str, object]) -> str:
    rows: List[RF10Row] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    return "\n".join([
        "# RF10 Service Provider / Care Partner Report",
        "",
        "Phase: `RF10`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Status Rows",
        "",
        _table(
            ["Key", "Area", "Status", "Evidence", "Next Action"],
            [[row.key, row.area, row.status, row.evidence, row.next_action] for row in rows],
        ),
        "",
        "## Founder Decision Rows",
        "",
        _table(
            ["Decision", "Status", "Phase", "Notes"],
            [[item["decision"], item["status"], item["phase"], item["notes"]] for item in founder_decisions],
        ),
        "",
        "## RF10 Boundary",
        "",
        "- RF10 hardens service-provider access through explicit active horse grants, same-barn stable provider user IDs, and explicit provider catalog links.",
        "- RF10 provider-authored writes are limited to `/service-provider/visit-notes`; canonical care writes remain facility-owned until a later policy phase.",
        "- RF10 does not implement provider invoices, payouts, Stripe, live provider API calls, messaging delivery truth, legal signatures/storage truth, native/offline behavior, or founder acceptance auto-marking.",
        "- Current launch claims may say providers have grant-scoped horse/care context and provider-authored visit notes. They must not claim broad barn-wide provider access, account-level cross-facility provider identity, canonical care-write authority, payment truth, messaging delivery, or legal document workflows are complete.",
        "",
    ])
