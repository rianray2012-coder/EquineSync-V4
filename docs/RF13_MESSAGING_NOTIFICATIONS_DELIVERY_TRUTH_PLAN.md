# RF13 Messaging, Notifications, and Delivery Truth Plan

Date: 2026-07-06

Status: superseded by locked RF13.

## Purpose

RF13 should make EquineSync communication claims truthful and auditable. It
should reconcile existing Task Engine notifications, feature-module Group
Messaging records, owner announcements, push-preview manifests, and
community-help escalation notes without implying live APNs/FCM, SMS, broad
email delivery, or external provider delivery before source proof exists.

## Locked Inputs

- RF4 records Group Messaging as push-preview/local-status readiness, not
  external delivery.
- RF6 records integration readiness as manifest/status evidence until
  provider-specific phases prove live sync.
- RF7 protects owner, guardian, and client portal visibility.
- RF8/RF9/RF10 provide stable staff, trainer, and provider identity foundations
  that RF13 can reference for recipient IDs.
- RF11 records community-help audience and escalation model as founder-decision
  work.
- RF12 is locked and keeps app-store/native provider billing boundaries out of
  messaging scope.

## Strict Scope

RF13 may:

- inventory messaging, notification, owner-announcement, push-preview, and
  community-help communication surfaces;
- replace or narrow misleading local `sent` wording where delivery is not
  proven;
- add backend-authoritative recipient projections for existing group-message
  and announcement surfaces when they can be scoped safely by stable user,
  role, barn, owner, guardian, trainer, staff, or provider IDs;
- add delivery-log or delivery-manifest evidence for local/in-app delivery
  when no external provider call occurs;
- harden guardian/minor communication rules where existing routes expose
  owner/guardian announcement or request-message surfaces;
- add focused tests proving no cross-barn, cross-owner, cross-guardian, or
  cross-provider communication leakage;
- produce an RF13 report, review package, and founder-decision rows.

RF13 must not:

- call APNs, FCM, Twilio, Resend, SendGrid, Mailgun, Google, Apple, Stripe,
  QuickBooks, DocuSign, MongoDB Atlas, Vercel, Render, or UAT systems;
- send live push, SMS, email, or provider messages unless a later explicit
  provider-delivery gate is approved;
- mutate production notification provider credentials, device tokens, or
  external delivery state;
- broaden rider, guardian, owner, trainer, staff, or provider visibility;
- auto-mark founder decisions accepted.

## Candidate Evidence Targets

| Area | RF13 Question | Expected RF13 Output |
| --- | --- | --- |
| Task Engine notifications | Are in-app notification recipients stable-ID scoped and auditable? | Source proof and focused tests for recipient resolution and no self/cross-role leakage. |
| Group Messaging | Does `sent` mean delivered, logged, or local status only? | Truthful status language, delivery-log/readiness evidence, or explicit demotion. |
| Owner announcements | Are owner/guardian announcement reads barn- and relationship-scoped? | Backend tests for owner, guardian, staff, trainer, and unrelated-user visibility. |
| Push previews | Are APNs/FCM claims clearly preview-only? | Manifest proof and stale-copy scan preventing live-push claims. |
| Guardian/minor communication | Are guardian/minor surfaces safe and invite/link scoped? | Tests and decision rows for minor communication boundaries. |
| Provider/trainer messaging | Are provider/trainer audiences ID-scoped before claims? | Scoped recipient inventory or deferred founder-decision rows. |
| Community help escalation | Is help/community communication internal, linked, or public? | Founder-decision rows and no public/community overclaim. |

## Acceptance Criteria

- RF13 report status is `ready` with zero blocker rows, or any blocker is
  explicitly recorded as `blocked` rather than hidden.
- Group Messaging, owner announcements, notification inbox, and push-preview
  claims use truthful delivery language.
- Recipient selection uses stable IDs where RF13 claims delivery/read
  authorization; display names and free-text labels are not authorization
  predicates.
- Guardian/minor communication rules are either enforced in source or recorded
  as deferred founder/UAT work without stronger launch claims.
- No live provider calls or live message delivery occur during RF13.
- Focused RF13 tests pass.
- Report generation passes.
- Zip integrity passes.
- Secret-shape scan is clean.
- Expected files only.

## Founder Decision Rows To Include

| Decision | Status | Notes |
| --- | --- | --- |
| Decide what Group Messaging `sent` means before provider delivery exists. | requires founder review | Recommended: local sent/logged status only until live provider delivery is implemented. |
| Decide first live communication channel. | requires founder review | Options include in-app only, email, push, SMS, or staged combinations; RF13 should not send externally without approval. |
| Decide guardian/minor communication rules. | requires founder review | Confirm whether minors receive direct messages, guardian copies, or guardian-only communication. |
| Decide provider/trainer messaging scope. | requires founder review | Confirm whether providers/trainers can receive direct barn messages in pilot and under which grants. |
| Decide community-help audience and escalation model. | requires founder review | RF11 deferred whether help is barn-internal, linked-user, provider-linked, or broader community behavior. |

## Suggested RF13 Files

- `BUILD_NEXT_RF13_MESSAGING_NOTIFICATIONS_DELIVERY_TRUTH_README.md`
- `docs/RF13_MESSAGING_NOTIFICATIONS_DELIVERY_TRUTH.md`
- `backend/core/rf13_messaging_notifications_delivery_truth.py`
- `backend/scripts/build_rf13_messaging_notifications_delivery_truth.py`
- `backend/tests/test_rf13_messaging_notifications_delivery_truth.py`
- `outputs/rf13_messaging_notifications_delivery_truth_report.md`
- `outputs/build_next_rf13_messaging_notifications_delivery_truth.zip`

## Verification Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf13_messaging_notifications_delivery_truth.py
.venv/bin/python backend/scripts/build_rf13_messaging_notifications_delivery_truth.py --fail-on-blockers
unzip -t outputs/build_next_rf13_messaging_notifications_delivery_truth.zip
```
