# Equine Sync Product Requirements Document

## 1. Product summary

Equine Sync is a role-based platform for horse barns, trainers, staff, clients, parents, and lesson students. It replaces scattered whiteboards, texts, paper forms, spreadsheets, and informal reminders with one shared system for horse care, barn operations, scheduling, communication, documents, payments, and client onboarding.

## 2. Primary product goals

- Give barn owners and managers one operational dashboard for horses, clients, staff, calendars, care tasks, maps, documents, payments, and communication.
- Give trainers a reliable way to manage clients, lesson students, ride updates, events, communications, and parent-included minor communication.
- Give clients and horse owners access to their horse's care information, schedule, bills, documents, ride logs, messages, and transfer options.
- Replace the physical barn whiteboard with a digital whiteboard that tracks tasks, daily changes, and completed actions.
- Support safe communication workflows for students under 18 by including parent/guardian profiles and blocking private adult-to-minor communication.
- Support multi-barn and multi-role users so the same person can be a client at one barn and a trainer or staff member at another.

## 3. Key personas

| Persona | Main needs |
|---|---|
| Equine Sync Admin | Full system management, troubleshooting, user support, settings access, and audit visibility. |
| Barn Owner | Facility setup, clients, horses, staff, maps, documents, payments, calendar, communications, and reporting. |
| Barn Manager | Daily operations, staff/task oversight, whiteboard, horse locations, calendar, and client communication. |
| Trainer | Client management, lesson schedule, ride updates, event signups, messaging, student/parent communication, and payments. |
| Staff | Complete assigned tasks, log horse care, view approved horse details, and receive barn notices. |
| Client / Horse Owner | View and update permitted horse information, pay invoices, sign documents, receive barn alerts, message barn/trainer, and track rides. |
| Parent / Guardian | Manage student profile, receive all student communications, sign waivers, pay invoices, and approve events. |
| Lesson Student | View appropriate lesson information, log permitted actions, and communicate only through parent-included channels. |
| Vendor | Limited appointment and horse/service visibility when approved by the barn. |

## 4. Current known gaps from review

- Admin is currently read-only or partially read-only and must be changed to full authorized access.
- User roles need a full permission matrix.
- Navigation should return users to the proper role-specific dashboard when clicking the icon or Equine Sync name.
- All user functions must be tested to confirm accidental read-only behavior does not exist.
- Barn owners, managers, and trainers need a structured invite and registration sequence.
- Horse profiles need a transfer process when a horse is sold.
- Registered users need account transfer/membership changes when moving barns or trainers.
- Group messaging, direct messaging, digital whiteboard, Google sign-in, payments, health photo uploads, ride tracking, parent profiles, maps, action logging, calendar, event signups, directory, legal documents, staff onboarding, and client onboarding are not fully built or need expansion.

## 5. Functional requirements by module

### 5.1 Admin, roles, and permissions

Priority: P0 - launch blocker.

Requirements:

- Admin can create, view, edit, archive, delete, invite, approve, transfer, message, upload, assign, and manage settings across all authorized areas.
- Implement role-based access control with deny-by-default behavior.
- Support multiple roles per user.
- Support multiple barn memberships per user.
- Log all critical actions in an audit log.
- Create test accounts for every role.

Acceptance criteria:

- Admin is not read-only unless a specific read-only admin role is intentionally assigned.
- Each role sees only the modules and records it should see.
- Users with two roles can switch context or access combined permissions without data leakage.
- A user removed from a barn immediately loses access to barn-only data.

### 5.2 Navigation and dashboard

Priority: P0.

Requirements:

- Clicking the Equine Sync logo or icon returns the user to their correct dashboard.
- Dashboards are role-aware: Admin, Barn Owner, Manager, Trainer, Staff, Client, Parent, Student, and Vendor.
- Mobile navigation must be easy to use in barn conditions.
- Empty states must guide users to the next action.

Acceptance criteria:

- Logo click works from every authenticated page.
- Browser back/forward behavior is predictable.
- Users with multiple barn memberships can choose or switch context.

### 5.3 Invite, registration, and onboarding

Priority: P0.

Requirements:

- Barn owners/managers can invite clients, staff, trainers, parents, students, and vendors.
- Trainers can invite clients and lesson families.
- Invites can assign role, barn, horse, and optional onboarding checklist.
- Invite status is visible: draft, sent, opened, accepted, expired, revoked.
- Existing users can accept invites without creating duplicate accounts.
- New users can register by email/password or approved social login.

Acceptance criteria:

- Invited users land in the correct barn and role after registration.
- Existing user invite acceptance links to the existing account.
- Expired/revoked invites cannot be accepted.
- Minor student onboarding requires parent/guardian connection.

### 5.4 Horse profile and transfer

Priority: P0 for basic profile; P1 for advanced transfer.

Requirements:

- Horse profile includes identity, ownership, contacts, care, feed, turnout, blanketing, health, documents, location, training, and behavior notes.
- Horse can be linked to owner, co-owner, lessee, trainer, staff, parent/student, and vendor as allowed.
- Horse profile transfer supports sold horses or changed ownership.
- Transfer process defines what data moves, what is archived, and who keeps history.
- Old-barn access is removed when horse leaves unless explicitly retained.

Acceptance criteria:

- New owner must accept horse transfer.
- Transfer history is logged.
- Prior owner and prior barn cannot access future private data after transfer.
- Export option is available before transfer.

### 5.5 Digital whiteboard and action logging

Priority: P1.

Requirements:

- Daily digital whiteboard shows care tasks, changes, alerts, and special instructions.
- Tasks include feed, hay, water, turnout, stall cleaning, meds, supplements, blanketing, grooming, wound check, ride, lesson prep, and facility notes.
- Approved non-staff users can log actions if the barn allows it.
- Some action types can require manager approval.
- Every action records user, time, horse, location, action type, notes, and optional photo.

Acceptance criteria:

- Staff can complete assigned tasks from a phone in 2-3 taps.
- Owners/students can log only actions the barn has permitted.
- Medication-related actions can be restricted to approved users.
- Missed or overdue tasks are visible to managers.

### 5.6 Maps and horse location

Priority: P1.

Requirements:

- Barn map, stall map, pasture map, dry lot map, and turnout map.
- Drag-and-drop horse placement.
- Support permanent home location and temporary current location.
- Track horse location history.
- Enforce or warn on capacity limits.
- Mobile map view and print/export options.

Acceptance criteria:

- Moving a horse updates current location and audit log.
- Users can see only location data permitted by their role.
- Stall/pasture capacity warnings display before saving.

### 5.7 Calendar and event signups

Priority: P1.

Requirements:

- Shared barn calendar for farrier, vet, bodyworker, shows, clinics, lessons, closures, and maintenance.
- Horse-specific and barn-wide events.
- Reminders and owner approvals for services.
- Trainer event signup requests for shows, specialty lessons, group lessons, bodyworker appointments, and clinics.
- Roster view with pending, confirmed, declined, and waitlisted status.

Acceptance criteria:

- Owners receive alerts for horse-related appointments.
- Trainer can request signup and client can accept/decline.
- Required forms/payments can be tied to signup.

### 5.8 Messaging

Priority: P1.

Requirements:

- Group messaging for barn-wide and role-specific announcements.
- Direct messaging between permitted users.
- Horse-specific and event-specific message threads.
- Parent/guardian inclusion for communications involving students under 18.
- No private adult-to-minor direct messages.
- Message attachments, notifications, read receipts, and archive/report options.

Acceptance criteria:

- Adult trainer cannot create a private 1:1 message with a minor student.
- Parent/guardian is automatically included on student-related communication.
- Barn owner can message all clients or filtered groups.

### 5.9 Payments

Priority: P2 unless business model requires earlier.

Requirements:

- Invoices for board, training, lessons, event fees, show fees, hauling, farrier/bodyworker pass-throughs, deposits, and late fees.
- Recurring billing and one-time payments.
- Payment history and receipts.
- Support payment recipients such as barn owner, trainer, or platform.
- Refunds, credits, failed payment retry, and payment notification rules.
- Choose payment processor and platform funds-flow model before development.

Acceptance criteria:

- Client can pay an invoice and see receipt.
- Barn/trainer can see paid/unpaid status.
- Failed payment creates notification and status update.

### 5.10 Documents and signatures

Priority: P1/P2 depending on launch model.

Requirements:

- Upload, send, sign, save, track, and renew legal documents.
- Boarding contracts, liability waivers, vet approvals, emergency authorizations, lesson agreements, media releases, and payment agreements.
- Status tracking: draft, sent, viewed, signed, declined, expired, voided, countersigned.
- Parent/guardian signature required for minor student documents.
- Version control and required-doc gates.

Acceptance criteria:

- Barn can see who has missing documents.
- User can access signed copies.
- Required document can block participation, event signup, or onboarding completion when configured.

### 5.11 Google sign-in and account linking

Priority: P2.

Requirements:

- Users can sign in with Google.
- Existing accounts can link a Google identity.
- Invite links support Google sign-in.
- Duplicate prevention based on verified email and account-linking rules.
- Maintain backup recovery path.

Acceptance criteria:

- Existing user with same email can link Google without creating duplicate account.
- Invited user using Google is placed into the correct barn/role after acceptance.

## 6. Non-functional requirements

| Area | Requirement |
|---|---|
| Mobile usability | Core barn workflows must work from a phone, outdoors, and with limited time. |
| Performance | Dashboard, horse profile, whiteboard, and task completion should feel fast under normal barn usage. |
| Reliability | Task completion, payments, signatures, and transfers must be idempotent and recoverable. |
| Security | Role-based access, audit logs, secure file storage, payment-token handling, and protected minor data. |
| Accessibility | Forms, buttons, and navigation should be accessible by keyboard and screen reader where practical. |
| Data export | Users and barns should be able to export key records. |
| Supportability | Admin tools must allow support staff to diagnose access, invites, transfers, and failed payments. |

## 7. Launch blockers

The following must be complete before broad launch:

- Role and permission matrix approved and implemented.
- Admin read-only issue fixed.
- Invitation and registration flows tested.
- User/barn/horse membership model supports transfers.
- Minor communication protections implemented.
- Payment and document workflows reviewed for legal/accounting/compliance needs.
- QA test plan completed for every role.
