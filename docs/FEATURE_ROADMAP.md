# FEATURE_ROADMAP.md
# EquineSync Feature Roadmap

## Product Direction
EquineSync is evolving into a comprehensive equine operations platform focused on: operational clarity, trust, communication, accountability, modern barn management.

This roadmap tracks: planned features, active development, future opportunities, experimental systems.

## Build Packet Source

The updated launch/build packet lives in
`docs/equine_sync_build_packet/`. Use it as the source for new gated phase
prompts, acceptance criteria, QA planning, compliance/payment decisions, and
launch checklist work. It does not override the existing rule that each
implementation phase needs explicit scope, guardrails, tests, and deferrals.

The current proposed execution sequence is in
`docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md`.

## Status Legend
`Planned` · `In Progress` · `Active` · `Experimental` · `Deferred` · `Deprecated`

## Core Platform
**Authentication** — *In Progress*: Login, Registration, Password Reset, Email Verification, Session Management, Multi-role Authentication.
**User Management** — *Active*: Role Management, User Profiles, Staff Assignment, Owner Accounts, Trainer Accounts.

## Horse Management
**Horse Profiles** — *Active*: Horse Records, Breed Information, Ownership, Trainer Assignment, Care Instructions, Medical Notes.
**Horse Media** — *Planned*: Photo Uploads, Video Uploads, Progress Galleries, Owner Sharing.

## Care Operations
**Care Tasks** — *Active*: Feeding, Turnout, Stall Cleaning, Grooming, Medication, Exercise.
**Medication Management** — *In Progress*: Scheduling, Dosage Tracking, Completion Logs, Alerts, Expiration Tracking.
**Rehab & Stall Rest** — *Planned*: Rehab Plans, Restricted Exercise, Recovery Notes, Progress Tracking.

## Trainer Tools
**Training Management** — *Planned*: Training Notes, Ride Tracking, Progress Reports, Rider Assignments.
**Show Management** — *Planned*: Show Signups, Scheduling, Hauling Coordination, Show Billing, Results Tracking, Competition Goals.

## Owner Portal
**Owner Dashboard** — *In Progress*: Horse Updates, Billing Visibility, Photos, Messages, Reports.
**Weekly Recaps** — *Planned*: Automated Summaries, Care Highlights, Training Notes, Media Updates.

## Billing & Finance
**Invoicing** — *In Progress*: Board Billing, Training Charges, Lesson Charges, Medication Charges, Custom Charges.
**Payments** — *Planned*: Stripe Integration, Payment Tracking, Auto-pay, Payment Reminders.

## Staff Operations
**Task Management** — *Active*: Task Assignment, Daily Workflow Tracking, Completion Tracking, Notes.
**Shift Operations** — *Planned*: Staff Scheduling, Shift Assignments, Coverage Tracking.

## Communications
**Messaging** — *Planned*: Staff Messaging, Owner Messaging, Group Announcements.
**Notifications** — *In Progress*: Email Alerts, Task Reminders, Owner Notifications.

## Reporting
**Operational Reporting** — *Planned*: Task Completion Metrics, Care Compliance, Billing Reports, Revenue Reports.
**Owner Reports** — *Planned*: Horse Activity Summaries, Training Progress, Billing Summaries.

## Mobile Experience
**Mobile Workflow Optimization** — *In Progress*: Mobile Task Completion, Quick Notes, Photo Uploads, Mobile Horse Profiles.

## AI Features
**AI Summaries** — *Experimental*: Weekly Recaps, Operational Summaries, Smart Notifications.
**AI Operational Insights** — *Experimental*: Care Trend Detection, Scheduling Insights, Operational Alerts.

## Future Ecosystem Features
**Marketplace Integrations** — *Deferred*: Vendor Integrations, Supply Ordering, Service Marketplace.
**Veterinary Integrations** — *Deferred*: Vet Portal, Appointment Sync, Medical Records.
**Financial Intelligence** — *Deferred*: Forecasting, Barn Profitability, Revenue Analytics.

## Product Priority Order
1. Security & Stability
2. Mobile Workflows
3. Care Operations
4. Owner Trust Features
5. Billing Clarity
6. Reporting
7. AI Assistance
8. Ecosystem Expansion

## Near-Term Build Order

1. Billing clarity: Build-Next-1 is Codex-approved and locked with a read-only
   live Stripe catalog readiness report and Apple placeholder contract.
2. Mobile readiness: Build-Next-2A is Codex-approved and locked with a mobile
   evidence inventory matrix, existing HorseOps 390x844 screenshots,
   source-pinned billing/signup/dashboard/mobile-readiness contracts, and a
   required Build-Next-2B live screenshot gate.
3. Build-packet launch foundations: multi-barn/multi-role account model,
   invite/onboarding polish, minor/student communication safeguards,
   document/signature decision, and QA/UAT gates.
4. Phase 16: legacy billing reconciliation and hard-delete sequence only after
   a separate approved plan.
