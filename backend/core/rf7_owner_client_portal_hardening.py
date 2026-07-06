from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RF7Row:
    key: str
    area: str
    status: str
    evidence: str
    next_action: str


FOUNDER_DECISIONS = [
    {
        "decision": "Accept that RF7 hardens owner portal reads and owner request submission without implementing a leasee grant model.",
        "status": "requires founder review",
        "phase": "RF7, RF18",
        "notes": "Leasee invites remain invite-only from the horse owner or assigned trainer, with owner oversight preserved, but grant/revocation data model work is deferred.",
    },
    {
        "decision": "Accept limited modified-individual-owner trial posture as documented but not fully enforced in RF7.",
        "status": "requires founder review",
        "phase": "RF7, RF18",
        "notes": "Rider, guardian, and staff public self-signup must stay invite-first except the limited fallback path; server-side access caps remain RF18/UAT work.",
    },
    {
        "decision": "Accept Owner Updates lifecycle as canonical for owner-trust updates.",
        "status": "requires founder review",
        "phase": "RF6, RF7, RF17",
        "notes": "Feature-module owner media updates remain migration/hide candidates and must not be presented as the canonical owner-update workflow.",
    },
    {
        "decision": "Accept the legacy concierge service request workflow for staff/admin preview users while horse owners submit through owner-care-ledger requests.",
        "status": "requires founder review",
        "phase": "RF7, RF12",
        "notes": "RF7 keeps staff approval/decline behavior intact; later payment/concierge billing truth stays RF12.",
    },
]


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _status_counts(rows: Iterable[RF7Row]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf7_owner_client_portal_hardening(root: Path = ROOT) -> Dict[str, object]:
    owner_portal = _read(root, "frontend/src/pages/OwnerPortal.jsx")
    owner_care_ledger = _read(root, "frontend/src/pages/OwnerCareLedger.jsx")
    horse_ledger = _read(root, "backend/routes/horse_ledger.py")
    backlog = _read(root, "backend/routes/backlog.py")
    owner_updates = _read(root, "backend/routes/owner_updates.py")
    rf5_doc = _read(root, "docs/RF5_WEB_ENROLLMENT_ACCOUNT_HEALTH.md")
    rf6_doc = _read(root, "docs/RF6_CANONICAL_SYSTEMS_CONSOLIDATION.md")
    enrollment_paths = _read(root, "frontend/src/lib/enrollmentPaths.js")

    rows = [
        RF7Row(
            key="owner_portal_uses_owner_safe_horse_inventory",
            area="Owner portal horse inventory",
            status="ready"
            if _contains_all(
                owner_portal,
                [
                    'OWNER_PORTAL_HORSE_ROLES = new Set(["horse_owner", "parent"])',
                    'const horseEndpoint = usesOwnerSafeHorseList ? "/owner-portal/horses" : "/horses"',
                    "normalizeItems(r.data)",
                    "setHorses(rows)",
                ],
            )
            else "blocked",
            evidence="Owner and guardian portal horse lists now use `/owner-portal/horses` and normalize the `{items}` response. Staff preview users stay on the barn horse list.",
            next_action="RF18 should browser-smoke the owner, guardian, and staff-preview portal paths with seeded accounts.",
        ),
        RF7Row(
            key="owner_guardian_requests_use_owner_care_ledger_contract",
            area="Owner and guardian service requests",
            status="ready"
            if _contains_all(
                owner_portal,
                [
                    'const usesOwnerCareRequests = OWNER_PORTAL_HORSE_ROLES.has(user?.role)',
                    "if (usesOwnerCareRequests)",
                    "`/horse-ledger/${form.horse_id}/owner-service-requests`",
                    "request_type: ownerLedgerRequestType(form.type)",
                    "preferred_contact: \"app\"",
                    "`/horse-ledger/${activeHorseId}/owner-service-requests`",
                    "requestType = s.type || s.request_type || \"request\"",
                    "requestDetails = s.details || s.message || \"No additional notes\"",
                ],
            )
            else "blocked",
            evidence="Horse-owner and guardian submissions now go through the owner-care-ledger request route, which validates owner/guardian horse linkage, rate limits, and strips staff notes on owner/guardian reads.",
            next_action="Keep the legacy `/service-requests` approval workflow for staff/admin preview users until RF12 decides concierge billing/payment truth.",
        ),
        RF7Row(
            key="backend_owner_safe_horse_endpoint_exists",
            area="Backend owner-safe horse contract",
            status="ready"
            if _contains_all(
                horse_ledger,
                [
                    '@router.get("/owner/horses")',
                    '@router.get("/owner-portal/horses")',
                    "_owner_safe_horse_projection",
                    "primary_owner_id",
                    "secondary_owner_ids",
                    "guardian_user_ids",
                    "rider_user_ids",
                ],
            )
            else "blocked",
            evidence="RF1 owner-safe horse endpoints remain present and are based on stable owner, guardian, and rider identity fields.",
            next_action="Do not reintroduce `/horses` as the default owner portal inventory endpoint.",
        ),
        RF7Row(
            key="backend_owner_summary_and_request_contract_remains_safe",
            area="Owner care ledger contract",
            status="ready"
            if _contains_all(
                horse_ledger,
                [
                    '@router.get("/horse-ledger/{horse_id}/owner-summary")',
                    '@router.post("/horse-ledger/{horse_id}/owner-service-requests")',
                    '@router.get("/horse-ledger/{horse_id}/owner-service-requests")',
                    "_strip_staff_note",
                    "_OWNER_RATE_CAP",
                    'role not in {"horse_owner", "parent"}',
                    "_is_horse_guardian_for",
                    "_can_use_owner_request_contract",
                    'role in {"admin", "barn_manager"}',
                ],
            )
            and _contains_all(
                owner_care_ledger,
                [
                    "api.post(`/horse-ledger/${horseId}/owner-service-requests`",
                    "api.get(`/horse-ledger/${horseId}/owner-summary`",
                ],
            )
            else "blocked",
            evidence="Owner summaries and owner-care requests remain on the hardened HorseOps owner ledger contract rather than raw barn operational records.",
            next_action="RF18 should verify no owner surface renders raw alert internals, staff notes, audit rows, or hidden handling fields.",
        ),
        RF7Row(
            key="owner_portal_backlog_feeds_use_stable_clauses",
            area="Backlog owner portal feeds",
            status="ready"
            if _contains_all(
                backlog,
                [
                    "async def _owner_link_ids_for_user",
                    "async def _owned_horse_ids_for_user",
                    "def _owner_account_clauses",
                    "def _owner_horse_context_clauses",
                    '@router.get("/owner-portal/media-updates")',
                    '@router.get("/owner-portal/forms")',
                    '@router.get("/owner-portal/health-documents")',
                    "primary_owner_id",
                    "secondary_owner_ids",
                    "guardian_user_ids",
                    "rider_user_ids",
                ],
            )
            else "blocked",
            evidence="Owner portal media/forms/health-document feeds continue to rely on stable owner/user/horse clauses rather than display-name matching.",
            next_action="RF17 should migrate or hide feature-module owner media feeds after founder accepts Owner Updates as canonical.",
        ),
        RF7Row(
            key="owner_updates_canonical_but_media_duplicate_deferred",
            area="Owner updates canonical surface",
            status="deferred"
            if _contains_all(rf6_doc, ["Owner Updates is canonical", "Owner media updates should migrate or hide"])
            and _contains_all(owner_updates, ["db.owner_updates", '@router.post("/owner-updates")', '@router.get("/owner-updates")'])
            and "owner_media_updates" in backlog
            else "blocked",
            evidence="Owner Updates remains canonical, but feature-module `owner_media_updates` still exists as a migration/hide candidate.",
            next_action="RF17 should hide, redirect, or migrate owner media updates; RF7 does not remove feature-module data.",
        ),
        RF7Row(
            key="limited_trial_and_leasee_depth_remain_explicit",
            area="Enrollment caveats",
            status="deferred"
            if _contains_all(
                enrollment_paths,
                [
                    "limited_individual_owner_trial",
                    "leasee_invite_rule",
                    "Riders, guardians, and staff without an invite",
                    "invite-only from the horse owner or the horse's assigned trainer",
                ],
            )
            and _contains_all(
                rf5_doc,
                [
                    "limited seven-day individual-owner trial",
                    "Leasee access is recorded as invite-only",
                    "RF7 owns the real invite/grant model",
                ],
            )
            else "blocked",
            evidence="RF5/RF7 documents preserve the limited-trial and leasee requirements without claiming the deeper grant, revocation, and access-cap implementation is complete.",
            next_action="Implement leasee grants/revocation and limited-trial server caps only when founder accepts that policy and RF18 UAT scope is ready.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF7",
        "title": "RF7 Owner, Guardian, and Client Portal Hardening",
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


def render_rf7_report(report: Dict[str, object]) -> str:
    rows: List[RF7Row] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    lines = [
        "# RF7 Owner, Guardian, and Client Portal Hardening Report",
        "",
        "Phase: `RF7`",
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
            [
                [item["decision"], item["status"], item["phase"], item["notes"]]
                for item in founder_decisions
            ],
        ),
        "",
        "## RF7 Boundary",
        "",
        "- RF7 hardens owner/guardian/client portal reads and owner request submission against existing owner-safe backend contracts.",
        "- RF7 does not implement native apps, provider calls, billing mutations, Stripe changes, account deletion flows, broad feature-shell retirement, or founder acceptance auto-marking.",
        "- RF7 does not implement the full leasee grant/revocation model or fully enforce limited-trial access caps; those remain explicit founder/UAT decisions.",
        "- Current launch claims may say owner portal horse inventory and owner/guardian request submission now use owner-safe contracts. They must not claim full leasee support or fully enforced limited-trial access caps.",
        "",
    ]
    return "\n".join(lines)
