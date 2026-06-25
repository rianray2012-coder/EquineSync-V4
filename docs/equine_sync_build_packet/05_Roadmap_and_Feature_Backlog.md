# Equine Sync Roadmap and Feature Backlog

## 1. Priority definitions

| Priority | Meaning |
|---|---|
| P0 | Launch blocker or foundation required for many features. |
| P1 | Core barn operations and client experience. Needed for useful launch. |
| P2 | Business/advanced workflows. Important but can follow foundation. |
| P3 | Optimization, integrations, polish, or later expansion. |

## 2. Phase 0 - Product and architecture alignment

Goal: approve the decisions that prevent rework.

Deliverables:

- Final role and permission matrix.
- Data model review.
- Invite/registration flow approval.
- Minor/student communication rules approval.
- Payment processor and funds-flow decision.
- Document signature approach decision.
- MVP scope lock.

Exit criteria:

- Engineering has approved entities and permission model.
- Product has approved MVP and phase boundaries.
- Legal/accounting advisors have been identified for payments, waivers, minor/student, and e-signature review.

## 3. Phase 1 - Foundation and access control

Goal: make the system structurally safe and usable.

| Epic | Priority | Dependencies | Notes |
|---|---|---|---|
| Admin full-access fix | P0 | Existing auth/roles | Remove accidental read-only behavior. |
| Role/permission implementation | P0 | Matrix approval | Server-side enforcement. |
| Multi-barn user model | P0 | Data model | Required for transfers and multiple roles. |
| Core barn/user/horse model | P0 | Data model | Foundation for all modules. |
| Invite and registration | P0 | Auth, memberships | New/existing users, duplicate prevention. |
| Dashboard/navigation | P0 | Role context | Logo returns to role dashboard. |
| Audit logging | P0 | Permission layer | Required for trust, transfers, legal docs, payments. |
| Basic horse profile | P0 | Horse model | Identity, ownership, care basics. |

Exit criteria:

- Every role can sign in and see correct dashboard.
- Admin is not read-only.
- Barn Owner can invite users.
- Client can accept invite.
- Horse profile can be created and linked to owner/barn.
- Audit logs record critical changes.

## 4. Phase 2 - Barn operations MVP

Goal: replace the physical whiteboard and organize daily barn work.

| Epic | Priority | Dependencies | Notes |
|---|---|---|---|
| Digital whiteboard | P1 | Tasks, roles | Daily care/task board. |
| Action logging | P1 | Whiteboard, permissions | Staff and approved non-staff logging. |
| Barn calendar | P1 | Notifications, horses | Farrier, vet, bodyworker, lessons. |
| Notifications | P1 | User prefs | In-app/email first; push/SMS later. |
| Maps/location basics | P1 | Horse/location model | Stall, pasture, dry lot, turnout. |
| Health photo upload | P1 | Media storage, horse profile | Wounds, surgery, recovery tracking. |
| Barn directory | P1 | Profiles, privacy settings | Names, horses, contact info with controls. |

Exit criteria:

- Barn can run a day of operations from the whiteboard.
- Users can log actions from phone.
- Horse locations can be tracked.
- Owners receive calendar alerts.

## 5. Phase 3 - Communication, lessons, and trainer workflows

Goal: make trainer/client/student communication and event management usable.

| Epic | Priority | Dependencies | Notes |
|---|---|---|---|
| Group messaging | P1 | Notifications, roles | Barn-wide and filtered groups. |
| Direct messaging | P1 | Messaging, roles | Must include minor protections. |
| Parent/guardian profile | P1 | User roles | Required for lesson minors. |
| Minor communication safeguards | P1 | Parent profile, messaging | Server-side enforcement. |
| Ride tracking | P1/P2 | Horse profile | User ride logs and trainer updates. |
| Trainer event signup requests | P1/P2 | Calendar, messaging | Shows, clinics, group lessons, bodywork. |
| Onboarding for new clients | P1 | Documents, checklists | Boarders and lesson families. |
| Staff onboarding | P1 | Checklists, roles | Training and required forms. |

Exit criteria:

- Barn/trainer can communicate with clients.
- Minor student communication includes guardian.
- Trainer can send signup request.
- Client can track and share ride updates.

## 6. Phase 4 - Payments, legal documents, and integrations

Goal: support business operations and formal paperwork.

| Epic | Priority | Dependencies | Notes |
|---|---|---|---|
| Client payments | P2 | Processor decision | Invoices, payment status, receipts. |
| Recurring billing | P2 | Payments | Board/training/lesson packages. |
| Refunds/credits | P2 | Payments | Needed for real operations. |
| Legal document sending/signing | P2 | Document decision | Templates, envelopes, signed copies. |
| Required-document gates | P2 | Onboarding/events | Block participation until complete. |
| Google sign-in | P2 | Auth | Account linking and duplicate prevention. |
| Google Calendar sync | P3 | Calendar, OAuth | Later integration. |
| Advanced reports/exports | P2/P3 | Data completeness | Operations and records. |

Exit criteria:

- Invoices can be paid and tracked.
- Documents can be sent, signed/tracked, and stored or integrated externally.
- Google sign-in works without duplicate accounts.

## 7. Master backlog

| ID | Item | Priority | Owner |
|---|---|---|---|
| ES-001 | Fix Admin read-only status. | P0 | Engineering |
| ES-002 | Approve and implement roles/permissions. | P0 | Product/Engineering |
| ES-003 | Build multi-barn/multi-role account model. | P0 | Engineering |
| ES-004 | Implement audit logging. | P0 | Engineering |
| ES-005 | Build invite and registration flow. | P0 | Product/Engineering |
| ES-006 | Support existing user invite acceptance. | P0 | Engineering |
| ES-007 | Add role-specific dashboards. | P0 | Product/UX/Engineering |
| ES-008 | Fix logo/icon navigation to dashboard/home. | P0 | Engineering |
| ES-009 | Build core horse profile. | P0 | Product/Engineering |
| ES-010 | Build horse ownership transfer. | P1 | Product/Engineering |
| ES-011 | Build client barn/trainer transfer. | P1 | Product/Engineering |
| ES-012 | Build digital whiteboard. | P1 | Product/UX/Engineering |
| ES-013 | Build action logging for staff and approved non-staff. | P1 | Product/Engineering |
| ES-014 | Build barn/stall/pasture/dry lot/turnout maps. | P1 | UX/Engineering |
| ES-015 | Add drag-and-drop horse placement. | P1 | UX/Engineering |
| ES-016 | Build barn calendar and shared alerts. | P1 | Product/Engineering |
| ES-017 | Build group messaging. | P1 | Engineering |
| ES-018 | Build direct messaging. | P1 | Engineering |
| ES-019 | Build parent/guardian profile. | P1 | Product/Engineering |
| ES-020 | Enforce minor communication safeguards. | P1 | Engineering |
| ES-021 | Build trainer event signup requests. | P1/P2 | Product/Engineering |
| ES-022 | Build ride tracking and trainer updates. | P1/P2 | Product/Engineering |
| ES-023 | Add health photo uploads and timeline. | P1 | Engineering |
| ES-024 | Build barn directory with privacy settings. | P1 | Product/Engineering |
| ES-025 | Build staff onboarding. | P1 | Product/Engineering |
| ES-026 | Build client onboarding for boarders. | P1 | Product/Engineering |
| ES-027 | Build lesson client/student onboarding. | P1 | Product/Engineering |
| ES-028 | Add legal document send/sign/save/track. | P2 | Product/Engineering/Legal |
| ES-029 | Add client payments to barns/trainers. | P2 | Product/Engineering/Finance |
| ES-030 | Add recurring billing, refunds, credits, failed payment handling. | P2 | Engineering/Finance |
| ES-031 | Add Google sign-in/account linking. | P2 | Engineering |
| ES-032 | Add reports and exports. | P2/P3 | Product/Engineering |
| ES-033 | Build launch support/admin tools. | P2 | Engineering/Support |

## 8. Risk register

| Risk | Impact | Mitigation |
|---|---|---|
| Permissions are too simple for real barns. | Data leakage or unusable workflows. | Build scoped RBAC and test multi-role/multi-barn cases. |
| Admin remains partially read-only. | Support cannot operate. | Add admin regression tests. |
| Minor messaging rules are only UI-based. | Safety/compliance failure. | Enforce on server and audit threads. |
| Payments are built before funds-flow is decided. | Expensive rebuild. | Decide platform/direct payout model first. |
| Legal docs are built without signature/record requirements. | Unreliable paperwork. | Legal review before launch. |
| Horse transfers leak records. | Privacy and trust issue. | Build transfer state machine and access cleanup. |
| Barn map UX is too complex on mobile. | Low adoption. | Start with simple location assignments, then visual drag/drop. |
| Notifications become noisy. | Users ignore alerts. | Prioritize notification preferences and alert types. |

## 9. Definition of Ready

A ticket is ready when it has:

- Clear user story.
- Role(s) affected.
- Permission requirements.
- Data entities involved.
- Acceptance criteria.
- Edge cases.
- Audit/logging requirements.
- Notification behavior if applicable.
- QA test notes.

## 10. Definition of Done

A ticket is done when:

- Feature works in UI and API.
- Server-side permissions are enforced.
- Tests cover allowed and denied access.
- Mobile behavior is checked for core flows.
- Audit log records high-risk actions.
- Error and empty states are handled.
- Product owner accepts against acceptance criteria.
