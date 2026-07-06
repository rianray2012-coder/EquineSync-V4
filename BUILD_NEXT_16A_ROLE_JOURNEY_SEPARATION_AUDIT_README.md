# Build-Next-16A - Role Journey Separation Audit

Status: Codex-reviewed and locked - audit only, no product behavior changed

Date: 2026-07-04

## Purpose

BN16A inserts a new gate before the next launch-hardening work to separate the
current first-login, setup, role-intake, and dashboard surfaces.

This phase is an audit and contract phase only. It does not change routes,
components, backend schemas, permissions, onboarding behavior, seeded data,
billing, documents, notifications, or dashboard behavior.

## Why This Phase Exists

The current app has several role-home and dashboard concepts sharing paths and
components:

- `/onboarding` is facility setup.
- `/role-home/:profile` is acting as role intake, role home, and placeholder
  dashboard content.
- `/dashboard` is the Stable Command facility dashboard used by multiple barn
  roles.
- Sidebar navigation still points several role-specific menu entries back into
  `/role-home/:profile`.

This is workable for the recently locked role screenshot evidence, but it is
not clean enough for launch-ready first-login behavior.

## Deliverables

BN16A adds:

- `outputs/build_next_16a_role_journey_audit.md`
- this README
- a PRD status note
- `outputs/build_next_16a_role_journey_audit.zip`

## Current-State Findings

The audit report records these current source-level facts:

- `frontend/src/lib/roleLanding.js` maps most roles to `/role-home/*`.
- `frontend/src/App.js` registers `/dashboard`, `/role-home/:profile`, and
  `/onboarding`, but no separated `/role-intake/:profile` or role-specific
  dashboard routes.
- `frontend/src/pages/RoleHome.jsx` still owns intake-like role pages and some
  dashboard-like cards.
- `backend/routes/onboarding.py` exposes onboarding progress and completion but
  no readiness endpoint.
- `frontend/src/pages/Onboarding.jsx` completes setup through
  `/onboarding/complete` without blocker handling.
- `frontend/src/components/dashboard/SetupConciergeCard.jsx` still includes
  launch-risk copy saying setup is not required to start operations.

## Recommended BN16 Sequence

BN16A recommends splitting the remaining work into these gates:

1. BN16B - Backend Setup Readiness Contract
2. BN16C - Frontend Route Separation
3. BN16D - Role Intake Refactor
4. BN16E - Dashboard Resolver and Role Dashboards
5. BN16F - Production Copy and Placeholder Cleanup
6. BN16G - Guardrails, Accessibility, and Mobile Evidence
7. BN16H - Founder UAT Evidence Packet

## Strict Scope

- No product behavior changes.
- No backend route/schema/auth/permission changes.
- No frontend route/component/runtime changes.
- No owner projection changes.
- No onboarding completion behavior changes.
- No billing, Stripe, Apple, entitlement, DocuSign, Admin Portal, notification,
  Text/SMS, landing page, service worker, native mobile, offline, AI, scheduler,
  or workflow-engine changes.
- No seed script, demo account, UAT-account, credential, production-data, or
  password changes.
- No public-launch or founder-acceptance claim.

## Verification

Verification for this doc-only phase:

- Audit report exists.
- README exists.
- PRD note exists.
- Zip integrity passes.
- Package contains only expected BN16A audit files.

## Lock Notes

Codex review found no blocking issues. The package remains audit-only and
lock-ready with no product behavior changes.

## Package

Expected package:

- `outputs/build_next_16a_role_journey_audit.zip`

Expected files:

- `BUILD_NEXT_16A_ROLE_JOURNEY_SEPARATION_AUDIT_README.md`
- `outputs/build_next_16a_role_journey_audit.md`
- `memory/PRD.md`

## Next Gate

If BN16A is approved, proceed with BN16B:

Backend-authoritative setup readiness contract for facility setup completion,
including readiness blockers, setup role eligibility, visible/deferred step
alignment, and safe completion semantics.
