# Equine Sync QA and UAT Test Plan

## 1. QA goals

The QA plan should prove that Equine Sync works for real barn workflows, not just individual screens.

Primary goals:

- Verify role-based access is correct.
- Verify Admin is not read-only.
- Verify users can be invited, registered, onboarded, transferred, and removed.
- Verify horse data stays scoped to the right barn/users.
- Verify minor/student communication rules are enforced.
- Verify whiteboard and action logging work from mobile.
- Verify calendar, messaging, payments, documents, and notifications update the correct status.

## 2. Test environments

| Environment | Purpose |
|---|---|
| Local/dev | Developer validation. |
| Staging | Product QA and UAT with realistic data. |
| Payment sandbox | Payment testing with test cards/accounts. |
| Document/signature sandbox | Legal document workflow testing. |
| Production | Release only after launch checklist is complete. |

## 3. Test users to create

| User | Roles |
|---|---|
| Alice Admin | Equine Sync Admin. |
| Olivia Owner | Barn Owner at Barn A. |
| Mary Manager | Barn Manager at Barn A. |
| Tina Trainer | Trainer at Barn A and Client at Barn B. |
| Sam Staff | Staff at Barn A. |
| Clara Client | Horse Owner at Barn A. |
| Peter Parent | Parent/Guardian of minor student. |
| Sophie Student | Lesson Student under 18. |
| Victor Vendor | Farrier/Vendor. |
| Riley ReadOnly | Optional read-only guest. |

Also create:

- Barn A and Barn B.
- Horse 1 owned by Clara at Barn A.
- Horse 2 used in lesson program.
- Horse 3 being sold/transferred.
- A farrier event, vet event, group lesson, show signup, invoice, waiver, and daily whiteboard.

## 4. Admin and permission tests

| Test | Steps | Expected result |
|---|---|---|
| Admin full access | Admin opens users, barns, horses, settings, documents, payments, audit logs. | Admin can manage all authorized modules. |
| Admin create/edit/delete | Admin creates and edits test barn, user, horse, setting. | Changes save and audit log records action. |
| Barn Owner settings | Barn Owner edits Barn A settings. | Allowed for Barn A only. |
| Manager settings | Manager edits operational settings. | Allowed only where configured. |
| Trainer unassigned horse | Trainer opens horse not assigned to them. | Access denied. |
| Client other horse | Client opens another client's horse. | Access denied unless barn explicitly allows. |
| Staff billing | Staff tries to view invoices. | Access denied. |
| Student settings | Student tries to edit barn settings. | Access denied. |
| Multi-barn separation | Tina switches Barn A and Barn B. | Data and permissions change by barn context. |

## 5. Invite and registration tests

| Test | Expected result |
|---|---|
| New client invite | Client receives invite, registers, joins correct barn/horse. |
| Existing user invite | Existing account accepts new barn without duplicate account. |
| Expired invite | Invite cannot be accepted. |
| Revoked invite | Invite cannot be accepted. |
| Wrong email invite | System handles correction/resend. |
| Invite with horse link | Client lands with linked horse access. |
| Staff invite | Staff sees staff dashboard and tasks only. |
| Parent/student invite | Parent account required before student communication. |

## 6. Dashboard/navigation tests

| Test | Expected result |
|---|---|
| Logo from horse page | Routes to role-specific dashboard. |
| Logo from calendar | Routes to role-specific dashboard. |
| Logo from messages | Routes to role-specific dashboard. |
| Multi-role dashboard | User can switch context or sees appropriate combined dashboard. |
| Empty dashboard | Helpful next step is shown. |
| Mobile menu | Navigation is usable on phone. |

## 7. Horse profile and transfer tests

| Test | Expected result |
|---|---|
| Create horse | Horse profile saves with owner and barn link. |
| Edit care notes | Authorized user can edit; unauthorized cannot. |
| Upload health photo | Photo appears in health timeline. |
| Export horse record | Export includes selected permitted records. |
| Transfer horse | New owner receives and accepts request. |
| Cancel transfer | Transfer stops before acceptance. |
| Old owner access | Old owner loses future access after completed transfer. |
| Old barn access | Old barn staff lose access after horse leaves. |

## 8. Whiteboard/action log tests

| Test | Expected result |
|---|---|
| Create daily board | Tasks appear by horse/location/category. |
| Staff completes task | Status changes to done with timestamp/user. |
| Staff flags issue | Manager sees needs-attention alert. |
| Client logs hay refill | Allowed if barn permits. |
| Student logs stall cleaned | Allowed only if student role permits. |
| Unauthorized med action | Blocked. |
| Approval-required action | Status remains pending until manager approves. |
| Mobile completion | Task can be completed quickly from phone. |

## 9. Maps/location tests

| Test | Expected result |
|---|---|
| Create stall map | Stalls can be added and named. |
| Assign horse to stall | Horse location updates. |
| Drag/drop horse | Location changes and audit log records move. |
| Capacity warning | Warning appears when over capacity. |
| Temporary turnout | Current location differs from home location. |
| Client visibility | Client sees only permitted horse/location info. |

## 10. Calendar/event tests

| Test | Expected result |
|---|---|
| Farrier event | Owners and staff receive alert. |
| Vet event | Horse-specific event appears on horse profile. |
| Owner approval | Owner can approve/decline service. |
| Trainer event signup | Client receives request and accepts/declines. |
| Minor signup | Parent approval required. |
| Waitlist | Capacity limit moves extra signups to waitlist. |

## 11. Messaging tests

| Test | Expected result |
|---|---|
| Barn-wide group message | All selected clients receive message. |
| Role-filtered message | Only selected role group receives message. |
| Horse-specific thread | Connected users receive thread. |
| Direct client/trainer message | Allowed when scoped. |
| Adult-to-minor private DM | Blocked or parent automatically included. |
| Remove parent from minor thread | Blocked unless another approved guardian rule applies. |
| Attachment | File/photo attaches and permissions are enforced. |
| Read receipt | Status updates if enabled. |

## 12. Documents tests

| Test | Expected result |
|---|---|
| Upload template | Template is saved with version. |
| Send waiver | Recipient receives document. |
| Sign document | Status changes to signed/completed. |
| Minor waiver | Parent/guardian signs. |
| Expired document | Status changes to expired. |
| Required doc gate | User/event/onboarding blocked until completed. |
| Download signed copy | Authorized user can download. |

## 13. Payments tests

| Test | Expected result |
|---|---|
| Create invoice | Client receives invoice. |
| Pay invoice success | Invoice marked paid and receipt sent. |
| Payment failure | Invoice remains unpaid; failure notification sent. |
| Partial payment | Status reflects partial payment if enabled. |
| Refund | Refund status recorded and receipt updated. |
| Recurring billing | Invoice generates on schedule if enabled. |
| Unauthorized invoice access | Blocked. |

## 14. Onboarding tests

| Test | Expected result |
|---|---|
| Staff onboarding | Staff completes checklist and required forms. |
| Boarder onboarding | Client completes horse, docs, payment, care info. |
| Lesson onboarding | Parent/student setup, waiver, emergency info. |
| Missing required step | Onboarding remains incomplete. |
| Completed onboarding | Dashboard shows active status. |

## 15. Regression checklist before every release

- Sign in/out.
- Password reset.
- Google login if enabled.
- Invite accept.
- Role switch.
- Barn switch.
- Admin access.
- Horse profile open/edit.
- Whiteboard open/task complete.
- Calendar event create.
- Message send.
- Minor message enforcement.
- Document send/sign.
- Invoice pay in sandbox.
- Photo upload.
- Notification delivery.
- Audit log creation.

## 16. UAT sign-off questions

Ask barn owners/managers/trainers:

- Can you run a normal barn day from the digital whiteboard?
- Can staff understand what to do without extra explanation?
- Can owners see what they need without seeing too much?
- Can parents understand student communication and documents?
- Can trainers manage client events and ride updates?
- Can you find horses, people, documents, payments, and calendar items quickly?
- What would still force you back to a physical whiteboard, group text, or spreadsheet?

## 17. Release acceptance gate

Do not release until:

- P0 test cases pass.
- No known role-permission data leaks exist.
- No known minor communication bypass exists.
- Payment/document workflows are either production-ready or disabled behind feature flags.
- Admin can support users without direct database intervention.
- UAT users approve the core workflows.
