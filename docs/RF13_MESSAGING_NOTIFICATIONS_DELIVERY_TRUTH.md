# RF13 Messaging, Notifications, and Delivery Truth

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Purpose

RF13 makes EquineSync communication claims truthful and auditable. It separates
local logs, in-app notification dispatch, owner/guardian announcements, and
push-preview manifests from live external provider delivery.

## Implemented In RF13

- Task Engine notification candidate resolution now scopes admin, manager,
  horse, and owner recipients to the event `barn_id` or `tenant_id`.
- Group Messaging custom recipients normalize to stable `recipient_user_ids`.
- Push-preview payloads include recipient-count metadata and an explicit
  `preview_only_no_external_delivery` claim.
- Owner portal announcements are relationship-scoped:
  - horse owners receive barnwide owner-audience announcements and targeted
    custom rows;
  - guardians/parents receive only explicitly targeted rows.
- Group Messaging UI labels the final state as a local communication log rather
  than provider delivery.

## Surface Inventory

| Surface | Current Evidence | RF13 Status |
| --- | --- | --- |
| Task Engine notifications | `backend/notifications.py` | same-barn recipient scoped |
| Group Messaging | `/feature-modules/group-messaging` | local log / recipient-ID readiness |
| Owner announcements | `/owner-portal/announcements` | owner/guardian-safe projection |
| Push preview | `/integrations/push-notifications/preview` | preview-only manifest |
| Community help | RF11 decision row | deferred |
| Provider/trainer messaging | RF10/RF13 decision row | deferred |
| Live push/SMS/email provider delivery | no provider call in RF13 | deferred |

## Fixed Findings

| Finding | RF13 Fix | Evidence |
| --- | --- | --- |
| Task notification candidates could include admins/managers from another barn. | Candidate staff, horse, and owner queries now scope to event `barn_id`/`tenant_id` when present. | `backend/notifications.py`; focused RF13 test plants users and horses in two barns and expects only barn-1 recipients. |
| Owner/guardian announcements could overexpose custom or owner-audience messages. | Custom rows require stable targeted user IDs; guardians/parents only see explicitly targeted rows. | `backend/routes/backlog.py`; focused RF13 test covers owner and guardian views. |
| Group Messaging status could imply delivery. | UI labels the final state as a local communication log; push payload metadata remains preview-only. | `frontend/src/pages/GroupMessaging.jsx`; focused RF13 test verifies preview metadata. |

## Deferred Boundaries

| Boundary | Status | Owner |
| --- | --- | --- |
| Live APNs/FCM push delivery | deferred | future provider-delivery gate |
| SMS or broad email messaging | deferred | founder decision / future provider phase |
| Provider/trainer direct messaging | deferred | RF13/RF18 founder decision |
| Community-help public or cross-barn messaging | deferred | RF11/RF13/RF18 founder decision |
| Device-token collection and delivery receipts | deferred | future native/provider phase |

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Decide what Group Messaging `sent` means before provider delivery exists. | requires founder review | Recommended: local sent/logged status only until live provider delivery is implemented. |
| Decide first live communication channel. | requires founder review | Options include in-app only, email, push, SMS, or staged combinations; RF13 does not send externally. |
| Decide guardian/minor communication rules. | requires founder review | Confirm guardian-only, guardian-copy, or direct minor messaging before stronger claims. |
| Decide provider/trainer messaging scope. | requires founder review | Confirm whether providers/trainers can receive direct barn messages in pilot and under which grants. |
| Decide community-help audience and escalation model. | requires founder review | RF11 deferred whether help is barn-internal, linked-user, provider-linked, or broader community behavior. |

## Verification

RF13 is verified by:

- focused backend tests in
  `backend/tests/test_rf13_messaging_notifications_delivery_truth.py`;
- report generation through
  `backend/scripts/build_rf13_messaging_notifications_delivery_truth.py`;
- frontend build because RF13 touches Group Messaging UI copy;
- package integrity verification against
  `outputs/build_next_rf13_messaging_notifications_delivery_truth.zip`;
- secret-shape scan over RF13 package files.

## Launch Claim Boundary

Current launch claims may say:

- EquineSync has scoped communication readiness and local communication logs.
- Owner and guardian announcement projections are backend scoped.
- Task Engine notification candidate resolution is same-barn scoped.
- Push notifications have preview-only manifests.

Current launch claims must not say:

- EquineSync has live push, SMS, broad email, provider messaging, public
  community messaging, device-token delivery, provider receipts, or native
  notification delivery implemented by RF13.
