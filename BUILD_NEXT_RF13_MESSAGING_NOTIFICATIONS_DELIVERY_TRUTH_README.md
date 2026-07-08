# RF13 Messaging, Notifications, and Delivery Truth Package

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Scope

RF13 is a narrow refinement gate for communication truth. It reconciles
existing Task Engine notifications, Group Messaging records, owner
announcements, push-preview manifests, and community-help messaging posture
without turning on external provider delivery.

RF13 includes:

- same-barn recipient scoping for Task Engine notification candidates;
- stable `recipient_user_ids` normalization for custom Group Messaging rows;
- owner/guardian announcement projection hardening;
- preview-only push payload metadata with no live delivery claim;
- Group Messaging UI wording that describes local logs rather than provider
  delivery;
- focused backend tests and a generated RF13 proof report;
- founder-decision rows for live channel selection, guardian/minor rules,
  provider/trainer messaging, and community-help scope.

RF13 does not include:

- APNs, FCM, Twilio, Resend, SendGrid, Mailgun, Google, Apple, Stripe,
  QuickBooks, DocuSign, MongoDB Atlas, Vercel, Render, UAT, or provider calls;
- live push, SMS, email, provider messaging, public community messaging, or
  device-token credential work;
- broad trainer/provider messaging implementation;
- founder acceptance auto-marking.

## Evidence

- Source hardening: `backend/routes/backlog.py`, `backend/notifications.py`,
  `frontend/src/pages/GroupMessaging.jsx`
- Proof core: `backend/core/rf13_messaging_notifications_delivery_truth.py`
- Report script: `backend/scripts/build_rf13_messaging_notifications_delivery_truth.py`
- Focused tests: `backend/tests/test_rf13_messaging_notifications_delivery_truth.py`
- Review doc: `docs/RF13_MESSAGING_NOTIFICATIONS_DELIVERY_TRUTH.md`
- Generated report: `outputs/rf13_messaging_notifications_delivery_truth_report.md`
- Review package: `outputs/build_next_rf13_messaging_notifications_delivery_truth.zip`

## Review Command

```bash
.venv/bin/python -m pytest backend/tests/test_rf13_messaging_notifications_delivery_truth.py
.venv/bin/python backend/scripts/build_rf13_messaging_notifications_delivery_truth.py --fail-on-blockers
npm --prefix frontend run build
unzip -t outputs/build_next_rf13_messaging_notifications_delivery_truth.zip
```

## Launch Claim Boundary

Current claims may say EquineSync has scoped communication readiness, local
message logs, in-app notification dispatch foundations, owner/guardian-safe
announcement projections, and push-preview manifests.

Current claims must not say EquineSync has live APNs/FCM push delivery, SMS,
broad email messaging, provider messaging, public community messaging, live
provider delivery receipts, or native device-token delivery implemented by RF13.
