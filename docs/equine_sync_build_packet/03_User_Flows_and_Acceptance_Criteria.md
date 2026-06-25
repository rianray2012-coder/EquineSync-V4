# Equine Sync User Flows and Acceptance Criteria

## 1. Admin full-access flow

Actors: Equine Sync Admin.

Trigger: Admin signs in to manage platform or support a barn.

Steps:

1. Admin signs in.
2. Admin lands on platform admin dashboard.
3. Admin selects barn, user, horse, payment, document, or support tool.
4. Admin creates, edits, archives, deletes, invites, approves, transfers, or configures settings as needed.
5. System logs action in audit log.

Acceptance criteria:

- Admin is not read-only by default.
- Admin can manage all records within the support/admin scope.
- High-risk actions require confirmation.
- Audit log records actor, action, timestamp, target object, before/after values when practical.

## 2. Logo/home navigation flow

Actors: Any signed-in user.

Trigger: User clicks Equine Sync logo or top icon.

Steps:

1. User clicks logo/icon.
2. System determines current barn/context and primary role.
3. User is routed to the correct dashboard.
4. If user has multiple barns/roles, current context is preserved or the user is prompted to choose.

Acceptance criteria:

- Logo click works from all authenticated pages.
- Users do not land on an unauthorized dashboard.
- Empty dashboard states show next actions.

## 3. Barn Owner invites new client

Actors: Barn Owner or Barn Manager, new Client.

Trigger: Barn adds a new boarder or horse owner.

Steps:

1. Barn Owner selects Invite User.
2. Owner enters client name, email/phone, role, horse link, onboarding checklist, and optional message.
3. System creates invite with token and expiration.
4. Client receives invite.
5. Client opens invite and creates account or signs in.
6. Client accepts barn membership.
7. Client completes onboarding checklist.
8. Barn Owner sees accepted status.

Acceptance criteria:

- Invite status updates accurately.
- Invite cannot be accepted after revocation/expiration.
- User is linked to the correct barn and horse.
- Duplicate accounts are not created when email already exists.

## 4. Trainer invites lesson client with minor student

Actors: Trainer, Parent/Guardian, Student.

Trigger: Trainer adds a lesson student under 18.

Steps:

1. Trainer selects Invite Lesson Family.
2. Trainer enters parent/guardian contact and student details.
3. System requires parent/guardian account setup first.
4. Parent accepts invite.
5. Parent creates student profile.
6. Parent signs required waiver and communication consent.
7. Trainer can schedule lessons and communicate only through parent-included threads.

Acceptance criteria:

- Student cannot be fully onboarded without parent/guardian account.
- Trainer cannot create private 1:1 adult-to-minor direct message.
- Parent/guardian receives all student-related messages and approvals.

## 5. Existing user accepts additional barn invite

Actors: Existing User, Barn Owner/Manager.

Trigger: A person who already has an Equine Sync account joins another barn.

Steps:

1. Barn sends invite to existing user's email.
2. User opens invite and signs in.
3. System recognizes existing account.
4. User accepts new barn membership.
5. User can switch between barns.

Acceptance criteria:

- No duplicate account is created.
- Data remains separated by barn context.
- User roles can differ by barn.

## 6. Client requests to move barns or trainers

Actors: Client, Old Barn, New Barn, Trainer.

Trigger: Client changes boarding facility or trainer.

Steps:

1. Client opens Account/Barn Memberships.
2. Client requests to leave old barn or accepts invite from new barn.
3. System checks active invoices, documents, horse assignments, and pending events.
4. Old barn access is scheduled for removal or removed immediately.
5. New barn membership is activated.
6. Horse profile transfer is handled separately if needed.

Acceptance criteria:

- Client keeps the same login.
- Old barn loses access to new records after transfer.
- Historical records remain available only as configured.
- Outstanding payments/documents are not silently lost.

## 7. Horse profile transfer after sale

Actors: Current Owner, New Owner, Barn Owner/Manager, Admin if needed.

Trigger: Horse is sold or ownership changes.

Steps:

1. Current Owner or authorized barn admin starts horse transfer.
2. Transfer wizard asks what data should move: identity, health, photos, documents, training notes, messages, invoices, ownership records, and location history.
3. New Owner receives transfer request.
4. New Owner accepts.
5. System updates ownership, access, and barn membership links.
6. System archives old owner access as configured.
7. Transfer record is stored in audit log.

Acceptance criteria:

- New Owner must accept transfer.
- Old Owner cannot see future records after transfer unless granted access.
- Export option is available before transfer.
- Transfer can be canceled before acceptance.

## 8. Daily digital whiteboard task completion

Actors: Manager, Staff, approved Client/Student.

Trigger: Daily care task is due.

Steps:

1. Manager creates or reviews daily whiteboard.
2. System displays tasks by horse, location, category, due time, and assignee.
3. User taps task.
4. User marks done, skipped, issue, or needs attention.
5. User adds notes/photo if needed.
6. System updates status and logs action.
7. Manager sees completion dashboard.

Acceptance criteria:

- Task can be completed from mobile in 2-3 taps.
- Overdue or issue tasks are visible.
- User can log only permitted actions.
- Medication tasks require approved permission.

## 9. Non-staff action logging

Actors: Client/Horse Owner, Lesson Student, Staff, Manager.

Trigger: A non-staff user completes an approved barn action.

Steps:

1. User opens horse or whiteboard.
2. User selects Log Action.
3. System shows only allowed action types for that user.
4. User enters details and optional photo.
5. If action requires approval, status is Pending Review.
6. Manager approves or rejects if needed.

Acceptance criteria:

- Owner can log approved actions such as refilling hay net or water bucket.
- Lesson student can log only allowed actions.
- Restricted actions do not appear for unauthorized users.

## 10. Barn calendar service visit

Actors: Barn Owner/Manager, Client, Staff, Vendor.

Trigger: Farrier, vet, bodyworker, or other vendor is scheduled.

Steps:

1. Manager creates calendar event.
2. Manager selects horses and owners affected.
3. Optional service approval request is sent.
4. Owner approves, declines, or asks question.
5. Staff view prep list.
6. Event happens.
7. System logs completion and optional notes/documents/photos.

Acceptance criteria:

- Owners receive timely alerts.
- Staff can see which horses need to be ready.
- Event history is stored on each horse profile.

## 11. Trainer event signup request

Actors: Trainer, Client/Parent, Student.

Trigger: Trainer offers show, clinic, group lesson, specialty lesson, or bodyworker appointment.

Steps:

1. Trainer creates event with date, cost, capacity, deadline, notes, required forms, and payment requirement.
2. Trainer selects invited clients/students/horses.
3. Client/Parent receives request.
4. Client/Parent accepts, declines, or asks a question.
5. System updates roster.
6. If payment or documents are required, the client is prompted to complete them.

Acceptance criteria:

- Trainer sees pending, confirmed, declined, and waitlisted list.
- Parent must approve minor student participation.
- Required documents/payment status is visible.

## 12. Group messaging

Actors: Barn Owner/Manager/Trainer, recipients.

Trigger: Barn or trainer needs to communicate with a group.

Steps:

1. Sender chooses message type: announcement, group message, event message, horse-specific message, emergency alert.
2. Sender selects audience or filter.
3. System expands recipients based on roles and permissions.
4. Sender writes message and optional attachments.
5. System sends notifications based on preferences and priority.
6. Message is archived.

Acceptance criteria:

- Barn Owner can message all clients.
- Trainer can message assigned clients or event participants.
- Emergency alerts can bypass normal low-priority preferences if policy allows.

## 13. Direct messaging with minor protection

Actors: Trainer, Student, Parent/Guardian.

Trigger: Trainer attempts to message student.

Steps:

1. Trainer starts direct message.
2. System identifies student is under 18.
3. System automatically adds parent/guardian or blocks the message until parent is included.
4. Message is sent only when compliant participants are included.
5. Audit log records minor-involved thread creation.

Acceptance criteria:

- Private adult-to-minor direct message cannot be created.
- Parent/guardian remains in thread.
- Removing parent/guardian from thread is not allowed unless another approved guardian/adult rule is satisfied.

## 14. Client payment flow

Actors: Barn Owner/Trainer, Client, payment processor.

Trigger: Invoice is due.

Steps:

1. Barn Owner/Trainer creates invoice.
2. Client receives invoice notification.
3. Client opens invoice.
4. Client pays with approved payment method.
5. Payment processor returns success/failure.
6. Invoice status updates.
7. Receipt is stored and sent.

Acceptance criteria:

- Successful payment updates invoice status.
- Failed payment triggers notification and retry path.
- Payment recipient and platform fee behavior are clear before payment.

## 15. Document signature flow

Actors: Barn Owner/Trainer, Client/Parent, optional countersigner.

Trigger: Document needs to be signed.

Steps:

1. Barn uploads or selects document template.
2. Barn sends document to recipient.
3. Recipient receives notification.
4. Recipient reviews and signs.
5. Optional countersigner signs.
6. System stores signed document and status.
7. Required-doc gate is cleared.

Acceptance criteria:

- Document status is visible to sender and recipient.
- Parent/guardian signs for minor student where required.
- Signed copy is stored and downloadable.

## 16. Health photo upload flow

Actors: Client, Staff, Trainer, Manager.

Trigger: User tracks wound, surgery, swelling, lameness, hoof issue, or recovery progress.

Steps:

1. User opens horse health record.
2. User selects Add Health Update.
3. User uploads or captures photo.
4. User enters date, body location, notes, severity, treatment, and follow-up date.
5. System saves entry to health timeline.
6. Notifications/reminders are created if configured.

Acceptance criteria:

- Photo upload works from mobile camera.
- Health record visibility follows permissions.
- Timeline can compare progress over time.

## 17. Ride tracking and trainer update

Actors: Client/Rider, Trainer.

Trigger: Rider completes a ride.

Steps:

1. Rider opens Ride Log.
2. Rider records horse, date, duration, discipline, intensity, notes, and optional media.
3. Rider chooses privacy: private, trainer, owner, barn.
4. If shared with trainer, trainer receives update.
5. Trainer can comment or assign homework.

Acceptance criteria:

- Rider can keep a ride private or share with trainer.
- Trainer can respond when shared.
- Horse workload can be summarized.
