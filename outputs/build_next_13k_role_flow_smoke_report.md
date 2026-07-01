# Build-Next-13K Role Flow Smoke Report

Status: READY FOR CODEX REVIEW

Generated: 2026-07-01

## Scope

Evidence-only role-flow smoke packet for the BN13 role-first experience. This
report records source-level pass evidence and the remaining credentialed
staging rows that must be completed before launch/UAT acceptance.

## Environment Position

| Item | Value |
| --- | --- |
| Candidate frontend | `https://app.equine-sync.com` |
| Candidate API | Production Render API behind the configured frontend |
| Official environment status | Pending founder acceptance for this smoke packet |
| Localhost evidence | Reference-only; not accepted as official UAT closure |
| Browser screenshots | Not captured in this packet |

## Summary

| Check | Status | Evidence |
| --- | --- | --- |
| Source role landing matrix | PASS | `frontend/src/lib/roleLanding.js` |
| Role-home shells | PASS | `frontend/src/pages/RoleHome.jsx` |
| Role navigation boundaries | PASS | `frontend/src/lib/roleNavigation.js` |
| BN13 intake route gates | PASS | `backend/server.py` and BN13 route modules |
| Credentialed staging login smoke | BLOCKED | Role passwords/sessions were not available to this evidence phase |
| Screenshot evidence | BLOCKED | Screenshots require credentialed role sessions |
| Launch/UAT acceptance | BLOCKED | BN13K does not approve public launch or official UAT closure |

## Role Smoke Matrix

| Row | Role | Candidate account | Expected first landing | Expected surface | Smoke status | Evidence / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| UAT-R1 | `platform_admin` | `uat.platform@equine-sync.com` | `/admin/portal/dashboard` | Platform Admin Portal | BLOCKED | Blocked pending credentialed login in official environment. |
| UAT-R2a | `admin` | `uat.facility-admin@equine-sync.com` | `/onboarding` when setup incomplete, else `/dashboard` | Facility admin shell | BLOCKED | Blocked pending credentialed login and setup-state confirmation. |
| UAT-R2b | `barn_owner` | `uat.facility-admin@equine-sync.com` or dedicated barn-owner account | `/role-home/barn-owner` | Barn owner intake shell | BLOCKED | BN12A account label is facility admin / barn owner; actual role marker must be confirmed. |
| BN13K-T1 | `trainer` | Needed | `/role-home/trainer` | Trainer intake shell | BLOCKED | No dedicated trainer UAT credential is listed in BN12A. |
| UAT-R3 | `barn_manager` | `uat.manager@equine-sync.com` | `/role-home/manager` | Manager intake shell | BLOCKED | Blocked pending credentialed login in official environment. |
| UAT-R4a | `groom` | `uat.staff@equine-sync.com` | `/role-home/staff` | Staff intake shell | BLOCKED | Blocked pending credentialed login and exact staff role confirmation. |
| BN13K-W1 | `working_student` | Needed | `/role-home/staff` | Staff intake shell | BLOCKED | No dedicated working-student UAT credential is listed in BN12A. |
| UAT-R5 | `horse_owner` | `uat.owner@equine-sync.com` | `/owner/horses/{horseId}` when linked, else `/role-home/owner` | Owner-safe horse surface or owner shell | BLOCKED | Blocked pending credentialed login and owner-horse linkage confirmation. |
| UAT-R6 | `parent` | `uat.guardian@equine-sync.com` | `/role-home/guardian` | Guardian intake shell | BLOCKED | Blocked pending credentialed login in official environment. |
| UAT-R7 | `rider` | `uat.participant@equine-sync.com` | `/role-home/rider` | Rider intake shell | BLOCKED | BN12A calls this lesson participant; actual `rider` role marker must be confirmed. |
| UAT-R8 | `horse_owner` standalone | `uat.individual-owner@equine-sync.com` | `/role-home/owner` unless linked to a horse | Individual owner shell | BLOCKED | Blocked pending credentialed login and individual-owner account markers. |

## Source Evidence

### First Landing

`frontend/src/lib/roleLanding.js` defines:

- `platformAdmin: "/admin/portal/dashboard"`
- `facilityAdmin: "/dashboard"`
- `barnOwner: "/role-home/barn-owner"`
- `trainer: "/role-home/trainer"`
- `manager: "/role-home/manager"`
- `staff: "/role-home/staff"`
- `owner: "/role-home/owner"`
- `guardian: "/role-home/guardian"`
- `rider: "/role-home/rider"`

The owner path remains horse-aware: linked horse owners can land on
`/owner/horses/{horseId}` while unlinked owners land on `/role-home/owner`.

### Role Home Shells

`frontend/src/pages/RoleHome.jsx` contains role-scoped shells for:

- `data-testid="role-home-rider"`
- `data-testid="role-home-guardian"`
- `data-testid="role-home-owner"`
- `data-testid="role-home-barn-owner"`
- `data-testid="role-home-trainer"`
- `data-testid="role-home-manager"`
- `data-testid="role-home-staff"`

### Navigation Boundaries

`frontend/src/lib/roleNavigation.js` keeps platform, facility admin, manager,
trainer, barn owner, staff, owner, guardian, and rider navigation separated.
Client/participant roles route unfinished workflow entries back to their
role-home shell instead of exposing direct staff, billing, admin, report,
checkout, or document-signature workflows.

### Intake Route Gates

BN13 intake routers remain registered before product facility gates and keep
their source-level role checks:

- `backend/routes/rider_profile.py`
- `backend/routes/guardian_intake.py`
- `backend/routes/owner_intake.py`
- `backend/routes/barn_owner_intake.py`
- `backend/routes/trainer_intake.py`
- `backend/routes/manager_intake.py`
- `backend/routes/staff_intake.py`

## Required To Turn Smoke Rows Green

1. Confirm the official staging/production-like environment for role smoke.
2. Provide or rotate safe UAT credentials without committing passwords.
3. Confirm exact role markers for ambiguous rows:
   - facility admin vs barn owner,
   - groom vs working student,
   - lesson participant vs rider,
   - linked vs standalone horse owner.
4. Capture one sanitized browser screenshot per role landing/sidebar/intake
   row in the official environment.
5. Record founder acceptance separately from this source-level packet.

## Deferred / Out Of Scope

- No product behavior changes.
- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, launch, UAT, Stripe, Apple, or DocuSign changes.
- No intake fields or workflow links added.
- No seeded-demo changes.
