from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RF13Row:
    key: str
    area: str
    status: str
    evidence: str
    next_action: str


FOUNDER_DECISIONS = [
    {
        "decision": "Decide what Group Messaging `sent` means before provider delivery exists.",
        "status": "requires founder review",
        "phase": "RF13, RF17",
        "notes": "RF13 recommends treating existing `sent` as a local communication log until live provider delivery is implemented.",
    },
    {
        "decision": "Decide first live communication channel.",
        "status": "requires founder review",
        "phase": "RF13, RF18",
        "notes": "Options include in-app only, email, push, SMS, or staged combinations; RF13 does not turn on external delivery.",
    },
    {
        "decision": "Decide guardian/minor communication rules.",
        "status": "requires founder review",
        "phase": "RF13, RF14, RF18",
        "notes": "Confirm guardian-only, guardian-copy, or direct minor messaging before stronger claims.",
    },
    {
        "decision": "Decide provider/trainer messaging scope.",
        "status": "requires founder review",
        "phase": "RF10, RF13, RF18",
        "notes": "Provider/trainer audiences should stay grant- and ID-scoped before pilot claims.",
    },
    {
        "decision": "Decide community-help audience and escalation model.",
        "status": "requires founder review",
        "phase": "RF11, RF13, RF18",
        "notes": "RF11 deferred whether help is barn-internal, linked-user, provider-linked, or broader community behavior.",
    },
]


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _status_counts(rows: Iterable[RF13Row]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf13_messaging_notifications_delivery_truth(root: Path = ROOT) -> Dict[str, object]:
    backlog = _read(root, "backend/routes/backlog.py")
    notifications = _read(root, "backend/notifications.py")
    group_messaging = _read(root, "frontend/src/pages/GroupMessaging.jsx")
    feature_backlog = _read(root, "docs/FEATURE_BACKLOG_FOUNDATIONS.md")
    rf4_doc = _read(root, "docs/RF4_FEATURE_COMPLETION_CERTIFICATION.md")
    rf11_doc = _read(root, "docs/RF11_PROPERTY_LOCATION_MAP_COMMUNITY_HELP.md")
    rf13_plan = _read(root, "docs/RF13_MESSAGING_NOTIFICATIONS_DELIVERY_TRUTH_PLAN.md")
    rf13_tests = _read(root, "backend/tests/test_rf13_messaging_notifications_delivery_truth.py")

    rows = [
        RF13Row(
            key="communication_surface_inventory",
            area="Communication surface inventory",
            status="ready"
            if _contains_all(
                feature_backlog,
                [
                    "Group messaging with audience/channel/status tracking",
                    "Owner portal announcements feed",
                    "Live push notification delivery",
                    "preview-only APNs/FCM payload manifests",
                ],
            )
            and _contains_all(
                backlog,
                [
                    "MODULES: Dict[str, Dict[str, Any]] = {",
                    '"group-messaging"',
                    '@router.get("/owner-portal/announcements")',
                    '@router.post("/integrations/push-notifications/preview")',
                ],
            )
            else "blocked",
            evidence="RF13 inventories Group Messaging, owner announcements, push-preview manifests, and Task Engine notification dispatch.",
            next_action="RF18 should UAT seeded communication paths after founder accepts messaging posture.",
        ),
        RF13Row(
            key="group_message_recipient_ids",
            area="Group-message recipient identity",
            status="ready"
            if _contains_all(
                backlog,
                [
                    '"recipient_user_ids"',
                    "def _normalize_group_message_data",
                    "data = _normalize_group_message_data(module_key, data)",
                ],
            )
            and _contains_all(
                rf13_tests,
                [
                    "test_group_message_custom_recipients_are_normalized_and_push_preview_only",
                    '["owner-1", "parent-1"]',
                ],
            )
            else "blocked",
            evidence="Group-message custom recipients normalize to stable `recipient_user_ids` instead of relying on display names or broad custom labels.",
            next_action="RF13/RF18 should decide whether custom recipient picking needs a richer UI selector.",
        ),
        RF13Row(
            key="owner_guardian_announcement_scope",
            area="Owner and guardian announcement scope",
            status="ready"
            if _contains_all(
                backlog,
                [
                    "def _owner_announcement_clauses",
                    'if user.get("role") == "horse_owner":',
                    'q["$or"] = clauses',
                ],
            )
            and _contains_all(
                rf13_tests,
                [
                    "test_owner_and_guardian_announcements_are_relationship_scoped",
                    'owner_ids == {"owners-all", "owner-targeted"}',
                    'guardian_ids == {"guardian-targeted"}',
                ],
            )
            else "blocked",
            evidence="Horse owners receive barn owner-audience announcements plus targeted custom rows; guardians/parents receive only explicitly targeted rows.",
            next_action="Founder should decide whether guardians should receive default barnwide owner announcements or guardian-only announcements.",
        ),
        RF13Row(
            key="push_preview_delivery_truth",
            area="Push-preview delivery truth",
            status="ready"
            if _contains_all(
                backlog,
                [
                    '"delivery_status": "preview_only"',
                    '"delivery_claim": "preview_only_no_external_delivery"',
                    "APNs/FCM credentials and device tokens are required before live delivery is enabled.",
                ],
            )
            and _contains_all(
                rf13_tests,
                [
                    '"push_preview_ready"',
                    '"preview_only"',
                    '"preview_only_no_external_delivery"',
                ],
            )
            else "blocked",
            evidence="Push payloads remain preview-only manifests and expose no device-token/provider-delivery claim.",
            next_action="A later provider-delivery gate should add APNs/FCM credentials, device tokens, send results, and retry/audit evidence.",
        ),
        RF13Row(
            key="task_notification_same_barn_scope",
            area="Task notification recipient scope",
            status="ready"
            if _contains_all(
                notifications,
                [
                    "barn_id = event.get(\"barn_id\") or event.get(\"tenant_id\")",
                    "staff_q[\"barn_id\"] = barn_id",
                    "horse_q[\"barn_id\"] = barn_id",
                    "owner_q[\"barn_id\"] = barn_id",
                ],
            )
            and _contains_all(
                rf13_tests,
                [
                    "test_task_notification_candidates_stay_in_event_barn",
                    'assert "admin-2" not in recipients',
                    'assert "owner-2" not in recipients',
                ],
            )
            else "blocked",
            evidence="Task notification candidate resolution is scoped to the event barn/tenant for staff, horses, and owner users.",
            next_action="RF18 should browser/UAT notification inbox behavior with seeded cross-barn users.",
        ),
        RF13Row(
            key="group_messaging_ui_truth",
            area="Group Messaging UI truth",
            status="ready"
            if _contains_all(
                group_messaging,
                [
                    'sent: "logged locally"',
                    "Log locally",
                    "Local communication log",
                    "Current records track channel intent and local status without sending external push notifications.",
                ],
            )
            else "blocked",
            evidence="Group Messaging UI labels local status as logged locally rather than claiming provider delivery.",
            next_action="RF17 should hide/demote or further label any remaining feature-shell communication surfaces if founder wants fewer readiness surfaces.",
        ),
        RF13Row(
            key="provider_trainer_messaging_scope",
            area="Provider and trainer messaging",
            status="deferred"
            if _contains_all(
                rf13_plan,
                [
                    "Decide provider/trainer messaging scope.",
                    "Confirm whether providers/trainers can receive direct barn messages in pilot and under which grants.",
                ],
            )
            else "blocked",
            evidence="RF13 records provider/trainer messaging as a founder-decision row rather than claiming broad external delivery.",
            next_action="Founder should accept provider/trainer messaging scope before implementation or UAT claims.",
        ),
        RF13Row(
            key="community_help_delivery_scope",
            area="Community-help communication scope",
            status="deferred"
            if _contains_all(
                rf11_doc,
                [
                    "Public community-help network or emergency dispatch behavior",
                    "Decide community-help audience and escalation model.",
                ],
            )
            and _contains_all(
                rf13_plan,
                [
                    "Decide community-help audience and escalation model.",
                    "barn-internal, linked-user, provider-linked, or broader community behavior",
                ],
            )
            else "blocked",
            evidence="Community-help messaging remains founder-decision work and is not expanded into public/community delivery by RF13.",
            next_action="Founder should decide community-help audience before RF18 UAT or public community claims.",
        ),
        RF13Row(
            key="rf4_truth_boundary_preserved",
            area="RF4 communication truth boundary",
            status="ready"
            if _contains_all(
                rf4_doc,
                [
                    "Group Messaging now labels push behavior as preview metadata",
                    "RF13: live messaging delivery, recipient IDs, and delivery logs.",
                ],
            )
            else "blocked",
            evidence="RF13 builds on locked RF4 truth labeling without claiming live push delivery.",
            next_action="Keep RF4/RF13 wording aligned until provider delivery is implemented.",
        ),
        RF13Row(
            key="live_provider_delivery_boundary",
            area="Live provider delivery boundary",
            status="ready"
            if _contains_all(
                rf13_plan,
                [
                    "RF13 must not:",
                    "send live push, SMS, email, or provider messages",
                    "mutate production notification provider credentials, device tokens, or",
                ],
            )
            else "blocked",
            evidence="RF13 remains no-provider-call work and does not enable APNs/FCM/SMS/email provider delivery.",
            next_action="Live delivery requires a later founder-approved provider phase with credentials, device-token, result, and retry evidence.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF13",
        "title": "RF13 Messaging, Notifications, and Delivery Truth",
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


def render_rf13_report(report: Dict[str, object]) -> str:
    rows: List[RF13Row] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    return "\n".join([
        "# RF13 Messaging, Notifications, and Delivery Truth Report",
        "",
        "Phase: `RF13`",
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
        "## RF13 Boundary",
        "",
        "- RF13 fixes same-barn notification recipient scoping and owner/guardian announcement projection truth.",
        "- RF13 normalizes custom group-message recipient user IDs and records push payloads as preview-only manifests.",
        "- RF13 keeps Group Messaging status truthful as a local communication log unless future provider delivery is implemented.",
        "- RF13 does not call APNs, FCM, Twilio, Resend, SendGrid, Mailgun, Google, Apple, Stripe, QuickBooks, DocuSign, MongoDB Atlas, Vercel, Render, UAT systems, or external provider messaging systems.",
        "- Current launch claims may say EquineSync has scoped communication readiness, local logs, in-app notification dispatch foundations, and push-preview manifests. They must not claim live push/SMS/email/provider delivery, public community messaging, or broad provider/trainer messaging is implemented by RF13.",
        "",
    ])
