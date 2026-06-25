# Equine Sync Data Model and Technical Guide

## 1. Technical principle

Build the system around memberships, roles, and relationships rather than assuming one account equals one barn or one user type.

Recommended high-level model:

- User is global.
- Barn is a workspace/facility.
- BarnMembership connects user to barn.
- RoleAssignment grants scoped permissions.
- Horse can have ownership, barn location, trainer assignment, staff visibility, parent/student links, and transfer history.

## 2. Suggested core entities

| Entity | Purpose | Key fields |
|---|---|---|
| User | Global person account. | id, name, email, phone, date_of_birth_optional, status, created_at. |
| AccountIdentity | Login method such as password or Google. | id, user_id, provider, provider_subject, verified_email, linked_at. |
| Barn | Facility/workspace. | id, name, address, timezone, owner_user_id, status, settings. |
| BarnMembership | User relationship to barn. | id, barn_id, user_id, status, joined_at, left_at. |
| RoleAssignment | Scoped role permissions. | id, membership_id, role, scope_type, scope_id, starts_at, ends_at. |
| Horse | Horse profile. | id, display_name, registered_name, breed, color, sex, dob, status. |
| HorseOwnership | Owner/lessee/co-owner relation. | id, horse_id, user_id, relationship_type, start_date, end_date. |
| HorseBarnLink | Horse relationship to barn. | id, horse_id, barn_id, status, arrival_date, departure_date. |
| HorseAccessGrant | Explicit user/role access to horse. | id, horse_id, user_id or membership_id, permission_level, reason. |
| LocationArea | Barn area such as stall, pasture, dry lot, turnout. | id, barn_id, type, name, capacity, map_coordinates. |
| HorseLocationAssignment | Current or historical horse location. | id, horse_id, area_id, assignment_type, start_at, end_at, assigned_by. |
| TaskTemplate | Recurring care task definition. | id, barn_id, horse_id_optional, category, schedule_rule, required_role. |
| TaskInstance | Specific scheduled task. | id, template_id, due_at, status, assignee_id, priority. |
| ActionLog | Completed or reported action. | id, barn_id, horse_id_optional, user_id, action_type, status, notes, photo_ids. |
| HealthRecord | Health timeline event. | id, horse_id, category, date, notes, severity, follow_up_at. |
| MediaAsset | Uploaded file/photo. | id, owner_user_id, barn_id, horse_id_optional, storage_key, mime_type, visibility. |
| RideLog | Rider/trainer ride entry. | id, horse_id, rider_user_id, date, duration, discipline, visibility, notes. |
| CalendarEvent | Barn/horse/vendor/lesson/show event. | id, barn_id, type, title, start_at, end_at, visibility, status. |
| EventParticipant | User/horse participation. | id, event_id, user_id, horse_id_optional, status, role. |
| EventSignupRequest | Trainer request for client signup. | id, event_id, recipient_user_id, horse_id_optional, status, deadline. |
| MessageThread | Conversation. | id, barn_id, type, created_by, minor_involved_flag, status. |
| MessageParticipant | Users in thread. | id, thread_id, user_id, role_in_thread, required_participant_flag. |
| Message | Message content. | id, thread_id, sender_user_id, body, attachment_ids, created_at. |
| DocumentTemplate | Barn/trainer document template. | id, barn_id, owner_user_id, type, title, version, status. |
| DocumentEnvelope | Sent document package. | id, template_id, sender_id, recipient_id, status, due_at. |
| SignatureRecord | Signature event/status. | id, envelope_id, signer_user_id, signed_at, ip_info_optional, status. |
| Invoice | Bill to client. | id, barn_id, issuer_user_id, recipient_user_id, amount, due_date, status. |
| Payment | Payment transaction. | id, invoice_id, processor, processor_payment_id, amount, status. |
| Notification | In-app/email/push notification. | id, user_id, type, target_type, target_id, status. |
| AuditLog | Security and operations audit. | id, actor_user_id, action, target_type, target_id, before_json, after_json, created_at. |
| OnboardingChecklist | Required setup for role/client/staff. | id, barn_id, user_id, template_id, status. |
| OnboardingTask | Individual onboarding step. | id, checklist_id, title, required_flag, status. |
| TransferRequest | Horse or membership transfer. | id, type, target_id, from_party, to_party, status, effective_at. |

## 3. Key relationships

- User has many AccountIdentities.
- User has many BarnMemberships.
- BarnMembership has many RoleAssignments.
- Barn has many HorseBarnLinks.
- Horse has many HorseOwnership records.
- Horse can have many HorseLocationAssignments, but should have one current home location unless the barn permits multiple.
- MessageThread has many MessageParticipants and Messages.
- DocumentEnvelope has many SignatureRecords.
- Invoice can have many Payment attempts.
- TransferRequest references either a horse transfer or a barn membership transfer.

## 4. State machines

### 4.1 Invite status

Draft -> Sent -> Opened -> Accepted

Alternate terminal states:

- Expired
- Revoked
- Declined

Rules:

- Accepted invite creates or updates BarnMembership.
- Revoked/Expired invite cannot be accepted.
- Resend should create a new token or rotate the current token.

### 4.2 Barn membership status

Pending -> Active -> Suspended -> Left -> Archived

Rules:

- Suspended user cannot access barn data.
- Left user may retain own exported records depending on data policy.
- Archived keeps history but removes active access.

### 4.3 Horse transfer status

Draft -> Sent -> Accepted -> Completed

Alternate terminal states:

- Canceled
- Declined
- Expired

Rules:

- New owner must accept before ownership changes.
- Access cleanup runs on completion.
- Audit log records data-sharing choices.

### 4.4 Task status

Not Started -> In Progress -> Done

Alternate states:

- Skipped
- Needs Attention
- Pending Review
- Rejected

Rules:

- Restricted actions require approved role.
- Pending Review is used when non-staff logs an action that needs manager approval.

### 4.5 Document envelope status

Draft -> Sent -> Viewed -> Signed -> Completed

Alternate states:

- Declined
- Voided
- Expired
- Needs Countersignature

Rules:

- Required-doc gates clear only when Completed.
- New template version should not modify already signed documents.

### 4.6 Invoice/payment status

Invoice:

Draft -> Sent -> Viewed -> Paid

Alternate states:

- Partially Paid
- Past Due
- Void
- Refunded

Payment:

Created -> Processing -> Succeeded

Alternate states:

- Failed
- Canceled
- Refunded

Rules:

- Do not mark invoice Paid until payment processor confirms success.
- Failed attempts are retained.

### 4.7 Event signup status

Requested -> Pending -> Accepted -> Confirmed

Alternate states:

- Declined
- Waitlisted
- Canceled
- Expired

Rules:

- Minor student signup requires parent/guardian approval.
- Required documents/payments can block Confirmed.

## 5. Permission middleware requirements

Every API endpoint should check:

1. Is the user authenticated?
2. What barn context is active?
3. Is the user an active member of that barn or otherwise explicitly granted access?
4. What roles does the user have in this scope?
5. Does a safety override apply, such as minor messaging rules?
6. Is the target object in the permitted scope?
7. Should the action be audited?

Example access check pseudo-logic:

```text
can(user, action, target):
  memberships = active memberships for user
  roles = roles for target barn/scope
  if target involves minor communication:
      enforce guardian inclusion
  if action not allowed by role permission:
      deny
  if target not in user scope:
      deny
  allow
```

## 6. Suggested API groups

| API group | Examples |
|---|---|
| Auth | register, login, link Google, password reset, accept invite. |
| Users | profile, memberships, roles, notification preferences. |
| Barns | create barn, settings, directory, maps, locations. |
| Horses | profile CRUD, ownership, care notes, health records, media, transfers. |
| Tasks | whiteboard, task templates, task instances, action logs, approvals. |
| Calendar | events, reminders, participants, service approvals. |
| Messaging | threads, participants, messages, attachments, read receipts, reports. |
| Documents | templates, envelopes, signatures, document status, downloads. |
| Payments | invoices, payment sessions, payment methods, refunds, receipts. |
| Onboarding | checklist templates, assigned checklists, completion tracking. |
| Reports | task reports, document reports, payment reports, horse exports. |
| Admin | support tools, audit logs, admin overrides, platform settings. |

## 7. File/photo storage requirements

- Store files outside the relational database in secure object storage.
- Database stores metadata and access rules.
- Use signed URLs or equivalent controlled access.
- Virus/malware scan uploads if available.
- Resize/compress photos for display while retaining original where needed.
- Associate each file with owner, barn, horse, document, message, or health record.
- Audit deletion or visibility changes.

## 8. Notifications model

Notification types:

- Invite received.
- Message received.
- Minor/student message created.
- Task assigned/due/overdue/issue.
- Health follow-up due.
- Calendar appointment reminder.
- Event signup request.
- Document signature request.
- Invoice due/payment failed/receipt.
- Horse transfer request.
- Barn transfer/membership change.
- Emergency barn alert.

Delivery channels:

- In-app.
- Email.
- Push notification.
- SMS only if business approves cost/compliance requirements.

## 9. Audit log design notes

Audit logs should be append-only. Avoid editing audit log entries. For high-risk actions, store before/after snapshots or diffs.

Minimum audit fields:

- actor_user_id.
- actor_role_context.
- barn_id if applicable.
- target_type.
- target_id.
- action.
- result.
- timestamp.
- metadata.

## 10. Security and privacy requirements

- Deny-by-default API authorization.
- Separate authentication from role authorization.
- Scoped access by barn, horse, event, document, invoice, and student relationship.
- Parent/guardian rules enforced server-side.
- Payment card data should be handled by payment provider, not stored directly by Equine Sync.
- Document and health photo access should use controlled permissions.
- Logs should not expose sensitive payment or private document contents.
- Admin override actions should be visible in audit logs.

## 11. Reporting/export requirements

- Export horse profile and health records.
- Export action/task history.
- Export document completion report.
- Export payment/invoice report.
- Export barn directory subject to privacy controls.
- Export transfer record.

## 12. Engineering milestones

1. Data model migrations for users, barns, memberships, roles, horses, and audit logs.
2. Permission middleware.
3. Admin access fixes.
4. Invite/registration flows.
5. Horse profile and barn links.
6. Dashboard/navigation.
7. Whiteboard/action logs.
8. Calendar/events.
9. Messaging with minor rules.
10. Documents/payments integrations or MVP placeholders.
11. QA automation and UAT support tools.
