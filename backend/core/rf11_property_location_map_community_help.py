from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RF11Row:
    key: str
    area: str
    status: str
    evidence: str
    next_action: str


FOUNDER_DECISIONS = [
    {
        "decision": "Accept default property/location privacy posture.",
        "status": "requires founder review",
        "phase": "RF11, RF18",
        "notes": "Recommended default remains private until a barn admin or manager explicitly enables a share surface.",
    },
    {
        "decision": "Decide owner/rider map visibility depth.",
        "status": "requires founder review",
        "phase": "RF11, RF17, RF18",
        "notes": "Current RF11 owner evidence covers explicitly published owner/parent location and arena shares only; rider map visibility remains deferred.",
    },
    {
        "decision": "Decide community-help audience and escalation model.",
        "status": "requires founder review",
        "phase": "RF11, RF13, RF18",
        "notes": "Current emergency/help posture remains internal/owner-safe evidence only, with no public community network or dispatch claim.",
    },
    {
        "decision": "Decide QR/stall-card claim level.",
        "status": "requires founder review",
        "phase": "RF11, RF17",
        "notes": "Current claim may say printable local stall-card SVG; it must not claim true QR encoding or native scanning.",
    },
]


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _status_counts(rows: Iterable[RF11Row]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf11_property_location_map_community_help(root: Path = ROOT) -> Dict[str, object]:
    backlog = _read(root, "backend/routes/backlog.py")
    app = _read(root, "frontend/src/App.js")
    feature_backlog = _read(root, "docs/FEATURE_BACKLOG_FOUNDATIONS.md")
    field_reliability = _read(root, "docs/FIELD_RELIABILITY_OFFLINE_MATRIX.md")
    rf11_plan = _read(root, "docs/RF11_PROPERTY_LOCATION_MAP_COMMUNITY_HELP_PLAN.md")
    rf11_tests = _read(root, "backend/tests/test_rf11_property_location_map_community_help.py")

    rows = [
        RF11Row(
            key="surface_inventory",
            area="Property/location/map/help surface inventory",
            status="ready"
            if _contains_all(
                app,
                [
                    "StallMap",
                    "BarnLocations",
                    "ArenaSchedule",
                    "EmergencyContacts",
                    "EmergencyWorkflows",
                ],
            )
            and _contains_all(
                backlog,
                [
                    "stall-map",
                    "pasture-schedule",
                    "arena-schedule",
                    "emergency-contacts",
                    "emergency-workflows",
                    "qr-horse-id",
                ],
            )
            else "blocked",
            evidence="RF11 inventories the existing web surfaces: stall map, barn locations, arena schedule, emergency contacts/workflows, and QR horse ID stall-card routes.",
            next_action="RF17 should complete a broader feature-shell UX truth pass before public map/community claims expand.",
        ),
        RF11Row(
            key="explicit_location_share_state",
            area="Barn location publish/share state",
            status="ready"
            if _contains_all(
                backlog,
                [
                    "BACKLOG_LOCATION_SHARE_COLLECTION",
                    "Barn location sharing is not enabled",
                    "share_state",
                    "barn_admin_share_setting",
                    'audience": "owner_parent"',
                    "owner_view = role in",
                ],
            )
            else "blocked",
            evidence="Owner/parent location reads require the stored barn-location share to be enabled and now return explicit share-state metadata.",
            next_action="RF18 should UAT enabled/disabled share states across owner, parent, and staff seeded accounts.",
        ),
        RF11Row(
            key="owner_safe_location_projection",
            area="Owner-safe location projection",
            status="ready"
            if _contains_all(
                backlog,
                [
                    "if not owner_view:",
                    'row["notes"] = data.get("notes") or ""',
                    'row["weather_rule"] = data.get("weather_rule") or ""',
                    "_share_payload(share, owner_view=owner_view)",
                    "_location_board_payload(share=share, stalls=stalls, pastures=pastures, owner_view=owner_view)",
                ],
            )
            and _contains_all(rf11_tests, ['"created_by" not in body["share"]', '"updated_by" not in body["share"]'])
            else "blocked",
            evidence="Owner/parent barn-location shares omit staff-only stall notes, pasture weather-rule text, and internal share metadata while staff keeps operational fields.",
            next_action="RF18 should add browser evidence with seeded internal notes to prove no owner-facing leakage.",
        ),
        RF11Row(
            key="arena_owner_publish_projection",
            area="Arena schedule owner visibility",
            status="ready"
            if _contains_all(
                backlog,
                [
                    'data.get("visibility", "shared_with_owners") != "shared_with_owners"',
                    'row["owner_name"] = data.get("owner_name") or ""',
                    'row["notes"] = data.get("notes") or ""',
                    "_share_payload(share, owner_view=owner_view)",
                    "_arena_schedule_payload(share=share, records=records, owner_view=owner_view)",
                ],
            )
            and _contains_all(rf11_tests, ['"created_by" not in body["share"]', '"updated_by" not in body["share"]'])
            else "blocked",
            evidence="Owner/parent arena shares include only `shared_with_owners` blocks and omit internal owner-name, notes, and share metadata fields.",
            next_action="RF18 should UAT staff-only, owner-shared, and maintenance arena blocks.",
        ),
        RF11Row(
            key="stall_card_claim_boundary",
            area="Stall-card and QR claim truth",
            status="ready"
            if _contains_all(
                backlog,
                [
                    "stall_card_ready",
                    "Printable stall-card SVG generated locally",
                    "A true QR encoder can replace the preview grid",
                ],
            )
            and _contains_all(feature_backlog, ["True QR-code image encoding/native scanning", "printable stall-card SVG"])
            else "blocked",
            evidence="The QR horse ID route returns a local printable SVG and explicitly avoids claiming true QR encoding or native scanning.",
            next_action="RF17 or a native-readiness follow-up should prove true QR encoding/scanning before claim expansion.",
        ),
        RF11Row(
            key="movement_audit_deferred",
            area="Movement audit and canonical map model",
            status="deferred"
            if _contains_all(rf11_plan, ["Movement audit", "Canonical location model"])
            else "blocked",
            evidence="RF11 documents that canonical property/location models and movement-audit depth are not fully implemented in this package.",
            next_action="A later RF11 follow-up or RF18 migration/UAT pass should add canonical property/location IDs and movement audit proof.",
        ),
        RF11Row(
            key="offline_native_map_deferred",
            area="Offline/native/live-map boundary",
            status="deferred"
            if _contains_all(
                field_reliability,
                ["Barn map / location board", "No offline proof", "online-only"]
            )
            and _contains_all(rf11_plan, ["call live maps", "implement native/offline behavior"])
            else "blocked",
            evidence="RF11 preserves the BN18D posture: location/map surfaces are online-only, with no live maps, geocoding, route navigation, native, or offline claim.",
            next_action="BN22A/RF17/RF18 should handle native shell readiness, app-store evidence, and browser/device UAT separately.",
        ),
        RF11Row(
            key="community_help_deferred",
            area="Community help and emergency escalation",
            status="deferred"
            if _contains_all(rf11_plan, ["community-help audience", "no live-dispatch claims"])
            else "blocked",
            evidence="RF11 records community-help/emergency escalation as a founder-decision topic and does not implement public community networking or dispatch.",
            next_action="Founder should choose internal barn-only, owner/rider-linked, provider-linked, or broader community behavior before implementation.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF11",
        "title": "RF11 Property, Location, Map, and Community Help System",
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


def render_rf11_report(report: Dict[str, object]) -> str:
    rows: List[RF11Row] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    return "\n".join([
        "# RF11 Property, Location, Map, and Community Help Report",
        "",
        "Phase: `RF11`",
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
        "## RF11 Boundary",
        "",
        "- RF11 hardens existing barn-location and arena-share projections with explicit share-state evidence and owner-safe field/share metadata projections.",
        "- RF11 inventories property/location/map/stall-card/emergency-help surfaces without adding live maps, geocoding, dispatch, public community networking, native behavior, or offline behavior.",
        "- RF11 keeps stall-card/QR claims limited to deterministic local printable SVG readiness; it does not claim true QR encoding or native scanning.",
        "- Current launch claims may say EquineSync supports admin-enabled owner/parent location and arena share views with owner-safe projections. They must not claim public maps, universal location sharing, audited movement history, live routing, dispatch, true QR scanning, or offline/native map support.",
        "",
    ])
