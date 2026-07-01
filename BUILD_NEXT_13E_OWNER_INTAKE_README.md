# Build-Next-13E - Owner Intake Shell

Status: CODEX-REVIEWED AND LOCKED

Lock note: BN13E was reviewed clean. The focused BN13A/B/C/D/E backend suite
passed at 49/49, malformed owner intake values return 422 instead of 500,
frontend build compiled successfully, and the review package integrity check
passed.

## Purpose

BN13E follows locked BN13A through BN13D by giving `role="horse_owner"` users a
safe first-login owner setup surface. It supports both facility-linked owners
and individual/unattached owners without creating memberships, billing changes,
horse records, or HorseOps visibility.

## Files

- `backend/routes/owner_intake.py`
- `backend/server.py`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13e_owner_intake_shell.py`
- `memory/PRD.md`
- `outputs/build_next_13e_owner_intake_shell.zip`

## Scope

- Adds authenticated horse-owner-only endpoints:
  - `GET /api/owner-intake/profile`
  - `PATCH /api/owner-intake/profile`
- Stores records in `owner_intake_profiles`, keyed only by the current
  authenticated user.
- Captures safe owner intake fields:
  - preferred name
  - preferred contact
  - owner path (`facility_linked`, `individual_owner`, `exploring_facility`, or
    `prefer_not_to_say`)
  - primary horse name
  - intended horse count
  - riding/care goals
  - facility search name
  - facility city/state
  - notes
- Adds a real owner role-home shell at `/role-home/owner`.
- Facility-linked owners may see the existing safe `/owner-portal` entry point.
- Unattached or individual owners see a facility-connection placeholder that
  does not create a facility membership or horse record.

## Safety Rules

- Current-user scoped: client-supplied identity, role, barn, billing, and Stripe
  fields are ignored.
- Horse-owner only: riders, parents, facility admins, managers, and other roles
  receive 403.
- Response allowlist: internal fields such as admin notes, source IDs, Stripe
  IDs, subscription status, Mongo `_id`, or password hashes are not projected.
- The server registration intentionally avoids `PRODUCT_FACILITY_DEPS` because
  individual owner accounts may exist before joining an active facility.
- Owner navigation keeps unfinished individual-owner tools on safe role-home
  placeholders.

## Explicit Non-Scope

- No facility membership creation or approval.
- No horse CRUD replacement.
- No HorseOps owner projection or Care Ledger privacy changes.
- No owner request workflow expansion.
- No billing, checkout, Stripe, Apple, or subscription enforcement changes.
- No Admin Portal, landing page, email, notification, service worker, push,
  native app, offline, AI, or provider behavior changes.

## Verification

Focused checks cover:

- artifact presence,
- horse-owner-only access,
- current-user scoping,
- response scrubbing,
- whitelisted PATCH behavior,
- identity/billing/admin fields ignored,
- invalid enum and malformed type rejection,
- server registration without product facility dependency,
- owner UI endpoint wiring,
- owner UI not linking to private workflows,
- individual-owner navigation remaining placeholder-safe.

Expected command:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13a_role_routing.py \
  backend/tests/test_build_next_13b_role_navigation.py \
  backend/tests/test_build_next_13c_rider_intake_shell.py \
  backend/tests/test_build_next_13d_guardian_minor_intake.py \
  backend/tests/test_build_next_13e_owner_intake_shell.py -q
```

Frontend build:

```bash
cd frontend && npm run build
```

## Deferred

- Facility search results and lead workflow.
- Facility membership request/approval.
- Owner horse creation wizard.
- Billing checkout and subscription-management changes.
- Owner-facing Care Ledger projection changes.
- Owner request workflow expansion.
