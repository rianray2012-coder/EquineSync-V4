# Build-Next-16A Role Journey Separation Audit

Generated: 2026-07-04

Status: Codex-reviewed and locked - audit only

## Executive Summary

BN16 should be inserted before final launch-hardening because the current
first-login journey is functionally useful but conceptually muddy:

- Facility setup lives at `/onboarding`.
- Role intake and role home both live at `/role-home/:profile`.
- Stable Command lives at `/dashboard`, but several roles use it as their daily
  surface.
- Some client-facing role pages still contain placeholder or "coming next"
  style copy.
- Onboarding completion is not yet backed by a readiness/blocker endpoint.

BN16A makes no product changes. It records the current state and recommends a
safe gated implementation sequence.

Review result: no blocking findings. BN16A is locked as an audit-only phase.

## Strict Scope

This phase is evidence and planning only.

No code behavior changed:

- No backend route/schema/auth/permission changes.
- No frontend route/component/runtime changes.
- No owner projection changes.
- No onboarding completion changes.
- No billing, Stripe, Apple, entitlement, DocuSign, Admin Portal, notification,
  Text/SMS, landing page, service worker, native mobile, offline, AI, scheduler,
  or workflow-engine changes.
- No seed script, demo account, UAT-account, credential, production-data, or
  password changes.
- No founder-acceptance or public-launch claim.

## Current Route Inventory

| Surface | Current route | Current owner | Current launch concern |
| --- | --- | --- | --- |
| Platform Admin | `/admin/portal/dashboard` | Admin Portal shell | Correctly separate from barn app routes. |
| Facility setup | `/onboarding` | `Onboarding.jsx` | Setup completion lacks backend readiness blockers. |
| Facility dashboard | `/dashboard` | `Dashboard.jsx` | Stable Command is a real dashboard but shared by too many role journeys. |
| Role home / role intake | `/role-home/:profile` | `RoleHome.jsx` | Intake, role home, and placeholder dashboard copy are mixed. |
| Staff pulse | `/today` | `Today.jsx` | Operational Pulse is mature enough to become a staff dashboard surface. |
| Owner care ledger | `/owner/horses/:horseId` | `OwnerCareLedger.jsx` | Owner-linked horse path is separate and privacy-aware. |

## Current Source References

| Finding | Source |
| --- | --- |
| Role destinations map most non-admin roles to `/role-home/*`. | `frontend/src/lib/roleLanding.js` lines 3-12 |
| Setup eligibility only lists `admin` and `barn_owner`. | `frontend/src/lib/roleLanding.js` line 15 |
| Barn owner first login bypasses `/onboarding` and goes to `/role-home/barn-owner`. | `frontend/src/lib/roleLanding.js` line 35 |
| Facility admin goes to `/onboarding` only when completion flags are false. | `frontend/src/lib/roleLanding.js` lines 37-43 |
| App routes include `/dashboard`, `/role-home/:profile`, and `/onboarding`; no `/role-intake/:profile`. | `frontend/src/App.js` lines 178-183 |
| Onboarding backend step list includes `schedules`. | `backend/routes/onboarding.py` lines 20-32 |
| Backend onboarding percent uses all backend steps. | `backend/routes/onboarding.py` lines 183-188 and 205-208 |
| Onboarding completion simply marks progress complete. | `backend/routes/onboarding.py` lines 210-216 |
| Setup concierge says nothing is required to start operations. | `frontend/src/components/dashboard/SetupConciergeCard.jsx` line 94 |
| RoleHome still owns seven role-specific shells. | `frontend/src/pages/RoleHome.jsx` lines 492, 742, 1012, 1298, 1580, 1848, 2098 |
| Prior BN13 tests intentionally locked the old `/role-home/*` contract. | `backend/tests/test_build_next_13a_role_routing.py` and `backend/tests/test_build_next_13j_role_first_login_matrix.py` |

## Current First-Login Matrix

| User type | Current first-login destination | Should BN16 target |
| --- | --- | --- |
| `platform_admin` | `/admin/portal/dashboard` | Keep as-is. |
| `admin` incomplete setup | `/onboarding` | Keep, but make completion backend-authoritative. |
| `admin` complete setup | `/dashboard` | Move toward `/dashboard/facility` or resolver-backed facility dashboard. |
| `barn_owner` | `/role-home/barn-owner` | Evaluate moving first-login to `/onboarding` or setup readiness gate. |
| `barn_manager` | `/role-home/manager` | Add setup eligibility where appropriate; then dashboard route. |
| `trainer` | `/role-home/trainer` | Separate `/role-intake/trainer` from `/dashboard/trainer`. |
| `groom` | `/role-home/staff` | Separate `/role-intake/staff` from `/dashboard/staff` or `/today`. |
| `working_student` | `/role-home/staff` | Same as staff, with role label preserved. |
| `horse_owner` linked to horse | `/owner/horses/:horseId` | Keep owner-safe horse path. |
| `horse_owner` not linked | `/role-home/owner` | Separate `/role-intake/owner` from `/dashboard/owner`. |
| `parent` | `/role-home/guardian` | Separate `/role-intake/guardian` from `/dashboard/guardian`. |
| `rider` | `/role-home/rider` | Separate `/role-intake/rider` from `/dashboard/rider`. |

## Setup Readiness Gaps

Current backend setup progress is not enough for launch readiness because:

- Completion is a write-only flag with no blocker response.
- Required and deferred setup steps are not normalized into a readiness contract.
- The frontend hides at least one deferred setup concept while backend progress
  still counts all backend steps.
- `barn_manager` is not listed in setup eligibility even though the dashboard
  copy and operational model involve managers.
- The setup concierge tells operators nothing is required to start operations,
  which conflicts with a controlled launch posture.

BN16B should address this before frontend route separation.

## Role Intake / Dashboard Muddying

`RoleHome.jsx` is currently doing too much:

- intake form surface,
- role landing shell,
- placeholder dashboard cards,
- owner/guardian/rider future-state copy,
- staff/manager/trainer setup intent forms.

BN16 should split this into:

- `/role-intake/:profile` for first-login profile intent,
- role dashboard routes for daily work,
- a temporary redirect from `/role-home/:profile` until old links are gone.

## Navigation Findings

`frontend/src/lib/roleNavigation.js` currently points many sidebar entries back
to `roleHome(profile)`. That is useful for the placeholder/intake era but should
not remain the final launch shape.

BN16C/BN16E should replace those links with role-appropriate routes:

- staff/groom/working student: `/today`, `/my-work`, `/dashboard/staff`
- trainer: `/dashboard/trainer`, schedule/training surfaces
- manager: `/dashboard/manager`, operations surfaces
- horse owner: `/dashboard/owner` or owner horse path
- parent: `/dashboard/guardian`
- rider: `/dashboard/rider`

## Copy / UX Findings

Launch-risk copy to fix in later BN16 gates:

- "Coming Next" style labels on role surfaces.
- "nothing is locked or required to start operations" in setup guidance.
- Any production-facing placeholder copy that makes a finished shell feel like
  an internal scaffold.

Title Case convention should remain explicit for role/profile page headings.

## Recommended BN16 Gate Sequence

### BN16B - Backend Setup Readiness Contract

Purpose:

- Add backend-authoritative readiness before setup completion.

Recommended scope:

- `GET /api/onboarding/readiness`
- readiness blockers/warnings shape
- `POST /api/onboarding/complete` refuses incomplete required blockers
- align visible, required, optional, and deferred setup steps
- include `admin`, `barn_owner`, and `barn_manager` in setup role decisions
  if founder-approved
- focused backend tests

Strictly defer:

- UI refactor
- role dashboard split
- new setup workflow features

### BN16C - Frontend Route Separation

Purpose:

- Establish route contracts without fully redesigning every page.

Recommended scope:

- Add `/role-intake/:profile`
- Add role dashboard routes or a dashboard resolver
- Preserve `/role-home/:profile` as redirect/compatibility route
- Update `resolvePostLoginPath`
- Update sidebar navigation where safe
- Add route-level tests

### BN16D - Role Intake Refactor

Purpose:

- Make role intake screens clearly intake-only.

Recommended scope:

- Extract current RoleHome intake sections into role-intake components.
- Remove dashboard cards from intake pages.
- Preserve existing backend intake endpoints.
- Preserve privacy and role gating.
- Apply Title Case headings.

### BN16E - Role Dashboard Split

Purpose:

- Make each role land on a work surface, not an intake surface.

Recommended scope:

- Facility Admin / Barn Owner: Stable Command.
- Barn Manager: operations dashboard.
- Staff / Groom / Working Student: Operational Pulse / Today.
- Trainer: training program dashboard.
- Owner: Owner Portal / linked horse view.
- Guardian: minor rider dashboard.
- Rider: lesson participant dashboard.
- Use live data where available and honest empty states where not available.

### BN16F - Production Copy Cleanup

Purpose:

- Remove production-facing placeholder/scaffold copy.

Recommended scope:

- Source sweep for "Coming Next", "placeholder", "demo", "dev", and similar
  production-facing copy.
- Preserve docs/tests/internal notes.
- Keep title casing consistent.

### BN16G - Guardrails, Accessibility, and Mobile Evidence

Purpose:

- Ensure the split works on desktop and mobile.

Recommended scope:

- Route guard tests.
- Role destination tests.
- Accessibility smoke checks.
- Mobile screenshots for core first-login and dashboard surfaces.

### BN16H - Founder UAT Evidence Packet

Purpose:

- Produce the founder-review packet after route separation and copy cleanup.

Recommended scope:

- Role-by-role screenshot matrix.
- Backend response evidence where safe.
- Privacy exclusions.
- No founder acceptance unless Rian explicitly marks it.

## BN16B Founder Decisions To Lock

Before code changes in BN16B, lock:

1. Should `barn_manager` be allowed to complete facility setup, or only resume
   incomplete setup without final completion?
2. Should `barn_owner` first-login route to `/onboarding` until setup-ready, or
   stay in role intake with a setup CTA?
3. Which setup blockers are required for launch completion?
   - barn profile
   - locations
   - horse profiles
   - owners/clients
   - feed templates
   - review/launch
4. Should `schedules` remain deferred and excluded from completion percent until
   the scheduler/workflow materialization is fully ready?
5. Should setup completion be per barn/facility instead of per user?
6. What exact copy replaces "nothing is locked or required to start operations"?

## Acceptance Criteria For BN16A

- Audit report exists.
- Current route/role/setup/dashboard state is documented.
- Next BN16 gates are defined.
- No product files are changed.
- No launch/founder acceptance is claimed.
- Package integrity passes.
