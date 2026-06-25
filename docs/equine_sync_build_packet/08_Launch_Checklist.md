# Equine Sync Launch Checklist

## 1. Launch decision

Launch should happen only when the product is stable enough for real barn operations. A broken barn management system can create confusion around horse care, payments, schedules, student communication, and legal documents.

## 2. Product readiness

| Item | Status |
|---|---|
| Admin no longer read-only. | Not started / In progress / Done |
| Role/permission matrix approved. | Not started / In progress / Done |
| Permission checks implemented server-side. | Not started / In progress / Done |
| Multi-barn and multi-role users supported. | Not started / In progress / Done |
| Invite and registration flows work. | Not started / In progress / Done |
| Dashboard/navigation works by role. | Not started / In progress / Done |
| Core horse profile works. | Not started / In progress / Done |
| Horse ownership transfer works or is clearly disabled until ready. | Not started / In progress / Done |
| Client barn/trainer transfer works or is clearly disabled until ready. | Not started / In progress / Done |
| Digital whiteboard works. | Not started / In progress / Done |
| Action logging works with permissions. | Not started / In progress / Done |
| Calendar and alerts work. | Not started / In progress / Done |
| Group/direct messaging works. | Not started / In progress / Done |
| Minor/student message protection works. | Not started / In progress / Done |
| Parent/guardian profile works. | Not started / In progress / Done |
| Health photo upload works. | Not started / In progress / Done |
| Maps/location assignment works. | Not started / In progress / Done |
| Barn directory has privacy controls. | Not started / In progress / Done |
| Onboarding workflows work. | Not started / In progress / Done |

## 3. Payment/document readiness

| Item | Status |
|---|---|
| Payment model approved. | Not started / In progress / Done |
| Payment processor sandbox tests pass. | Not started / In progress / Done |
| Webhook handling tested. | Not started / In progress / Done |
| Failed payment path tested. | Not started / In progress / Done |
| Refund/credit behavior defined. | Not started / In progress / Done |
| Document signature approach approved. | Not started / In progress / Done |
| Required document gates tested. | Not started / In progress / Done |
| Parent/guardian signature process tested. | Not started / In progress / Done |
| Legal/accounting review completed. | Not started / In progress / Done |

## 4. Security/privacy readiness

| Item | Status |
|---|---|
| Role-based access tested for every role. | Not started / In progress / Done |
| No known cross-barn data leaks. | Not started / In progress / Done |
| No known client-to-client private data leaks. | Not started / In progress / Done |
| Minor communication bypass testing passed. | Not started / In progress / Done |
| File/photo access permissions tested. | Not started / In progress / Done |
| Payment data not stored directly by Equine Sync. | Not started / In progress / Done |
| Signed document access permissions tested. | Not started / In progress / Done |
| Audit logging verified. | Not started / In progress / Done |
| Admin override logging verified. | Not started / In progress / Done |
| Backup and recovery plan confirmed. | Not started / In progress / Done |

## 5. QA readiness

| Item | Status |
|---|---|
| P0 tests pass. | Not started / In progress / Done |
| Regression checklist passes. | Not started / In progress / Done |
| Mobile testing completed. | Not started / In progress / Done |
| Browser testing completed. | Not started / In progress / Done |
| Payment sandbox testing completed. | Not started / In progress / Done |
| Document/signature testing completed. | Not started / In progress / Done |
| UAT barn owner approved. | Not started / In progress / Done |
| UAT trainer approved. | Not started / In progress / Done |
| UAT client/parent approved. | Not started / In progress / Done |

## 6. Support readiness

| Item | Status |
|---|---|
| Admin can view invite status. | Not started / In progress / Done |
| Admin can troubleshoot role access. | Not started / In progress / Done |
| Admin can resend/revoke invites. | Not started / In progress / Done |
| Admin can resolve transfer issues. | Not started / In progress / Done |
| Admin can inspect payment/document statuses. | Not started / In progress / Done |
| Help docs created for barn owners. | Not started / In progress / Done |
| Help docs created for clients/parents. | Not started / In progress / Done |
| Support contact path defined. | Not started / In progress / Done |

## 7. Training materials to prepare

- Barn Owner quick start.
- Barn Manager daily whiteboard guide.
- Staff action logging guide.
- Client onboarding guide.
- Parent/student guide.
- Trainer event signup guide.
- Payment guide.
- Document signing guide.
- Horse transfer guide.
- Troubleshooting invites and login guide.

## 8. Go-live runbook

1. Freeze launch branch.
2. Confirm environment variables and third-party keys.
3. Confirm database migration plan.
4. Confirm backups.
5. Run smoke tests.
6. Run role/permission tests.
7. Run payment/document sandbox or production verification as applicable.
8. Enable feature flags for selected launch barns.
9. Invite pilot barn owners.
10. Monitor signups, errors, support requests, and audit logs.
11. Hold first production review after pilot use.

## 9. Feature flag recommendations

Use feature flags for:

- Payments.
- Legal document signatures.
- Google sign-in.
- Horse transfer.
- Barn/client transfer.
- Minor student messaging.
- Vendor access.
- Drag-and-drop maps.
- SMS notifications.

## 10. Post-launch metrics

Track:

- Invites sent/accepted/expired.
- Active barns.
- Active users by role.
- Horses created.
- Whiteboard tasks completed.
- Missed/overdue tasks.
- Messages sent.
- Minor-involved threads created with parent included.
- Calendar events created.
- Health photo uploads.
- Documents sent/signed/missing.
- Invoices sent/paid/failed.
- Support tickets by category.
- Permission denied events.
- Error rates and page load times.

## 11. Stop-launch criteria

Delay or pause launch if:

- Admin is still read-only.
- Known data leak exists between barns or users.
- Minor message safeguards can be bypassed.
- Payments can produce incorrect invoice status.
- Required documents/signatures are stored incorrectly.
- Horse transfer leaks private records.
- Users cannot reliably accept invites.
- Whiteboard/task flow is unreliable for daily care.
