# Build-Next-13B — Role Navigation Shells

Status: ready for Codex review

Date: 2026-06-30

## Purpose

BN13B is a navigation-only follow-up to BN13A. BN13A sends each role to the right first screen after login; BN13B makes the left sidebar match that role so users no longer see the broad barn-operations menu by default.

## Scope

- Add `frontend/src/lib/roleNavigation.js` as the source of truth for role-specific sidebar groups.
- Update `frontend/src/components/Sidebar.jsx` to render the role navigation contract instead of the old broad `NAV_SECTIONS` array.
- Preserve existing route guards in `App.js`; the sidebar is not treated as an authorization layer.
- Keep client-facing unfinished surfaces on safe role-home placeholders rather than linking riders, guardians, or owners into legacy operational routes.

## Explicit Non-Scope

- No backend route, schema, auth, permission, or database behavior changes.
- No permission changes.
- No new product workflow.
- No intake wizard implementation.
- No billing, Stripe, DocuSign, Admin Portal, or launch evidence changes.

## Role Menus

### Platform Admin

- Admin Portal
- Users
- Facilities
- Platform Billing
- Profile

### Facility Admin

- Dashboard
- Setup
- Horses
- Owners
- Riders
- Staff
- Schedule
- Tasks
- Billing
- Documents
- Reports
- Facility Settings
- Messages

### Manager / Trainer

Manager:

- Dashboard
- Tasks
- Horses
- Staff
- Schedule
- Health Alerts
- Owner Requests
- Facility
- Reports
- Messages
- Settings

Trainer:

- Dashboard
- Tasks
- Horses
- Schedule
- Health Alerts
- Owner Requests
- Facility
- Reports
- Messages
- Settings

### Staff

- Today
- My Tasks
- Horse Checks
- Horse List
- Facility Checks
- Messages
- Shift Notes
- Profile

### Horse Owner

- My Horse
- Daily Care
- Barn Schedule
- Training Notes
- Health
- Requests
- Billing
- Documents
- Messages
- Profile

### Individual Owner

- My Horse
- Daily Care
- Training Notes
- Health
- Schedule
- Requests
- Billing
- Documents
- Messages
- Profile

### Guardian / Parent

- Rider Overview
- Schedule
- Progress Notes
- Billing
- Documents
- Requests
- Messages
- Emergency Info
- Profile

### Rider / Lesson Participant

- Home
- Schedule
- Lessons
- Progress Notes
- Goals
- Requests
- Barn Announcements
- Documents
- Profile

## Safety Notes

- Riders and guardians do not link to `/lessons`; they stay on safe role-home placeholders until the rider/guardian surfaces are built.
- Owners see a Billing item, but it does not link to the existing barn-admin billing route.
- Staff do not see Billing, Setup, Staff Admin, Audit Log, Integrations, or platform-admin surfaces.
- Trainers do not see the admin-only `/staff`, `/reports`, or billing routes; their Reports item points to the trainer-allowed reporting route.
- `barn_owner` uses a safe setup-oriented navigation shell until BN13C+ decides whether to expand barn-owner permissions.
- Platform admins are pointed back to the Admin Portal lane.

## Review Fixes

- Trainer navigation no longer includes admin-only `Staff`, `/reports`, or billing links.
- Barn-owner navigation no longer mirrors full facility-admin routes that the current route guards deny.
- Sidebar list keys now include section, label, and route so placeholder-heavy menus do not produce duplicate React keys.

## Verification

- `backend/tests/test_build_next_13b_role_navigation.py`
- `backend/tests/test_build_next_13a_role_routing.py`
- Frontend production build
- Zip integrity check for `outputs/build_next_13b_role_navigation.zip`

## Deferred

- BN13C: rider intake shell and safe first-login rider profile experience.
- BN13D: guardian/minor rider intake shell.
- BN13E: individual owner + horse intake shell.
- BN13F+: role-specific dashboard content and UAT evidence.
