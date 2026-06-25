# Build-Next-3 - Multi-Barn / Multi-Role Account Model Gap Report

Status: Codex-approved and locked.

## Purpose

Build-Next-3 reconciles the updated build packet's multi-barn and multi-role
account requirements against the current EquineSync implementation before any
schema, invite, transfer, or permission behavior changes are made.

This phase is an audit and planning phase, not a feature phase.

## Founder Decisions Applied

- Future membership collection name: `account_memberships`.
- Users may hold multiple roles across facility, owner, parent/student, trainer,
  and lesson contexts.
- Individual users may be active without an active facility. The future flow
  should ask users to search for their facility, then collect barn information
  as a sales lead when no active membership exists.
- Billing entitlements remain account/facility scoped, except the free
  individual-owner one-horse account.
- Owner access remains horse-specific for launch.
- Preserve `users.barn_id` / `users.role` as compatibility mirrors through
  launch and migrate surface-by-surface.
- Standalone owner account ids are generated, not raw `user_id` values.
- Facility search / lead capture applies to all non-platform onboarding paths
  except invited users; individual owners may continue without an active
  facility.

## Problem To Resolve

The current platform has strong single-barn assumptions in many launch-critical
areas: user role, `barn_id`, owner links, invited owner access, subscription
limits, Admin Portal visibility, HorseOps privacy, and onboarding state.

Before expanding invite acceptance or supporting users who belong to multiple
barns/roles, the app needs a concrete map of:

- what already supports multi-barn or multi-role safely;
- what is hard-coded to one barn or one role;
- what could leak data if memberships are expanded too quickly;
- what should become the canonical membership model in a later build phase.

## Strict Scope

Allowed:

- Read source code.
- Read local Mongo data shapes.
- Produce a gap report and implementation plan.
- Add focused read-only tests that pin current assumptions.
- Add docs and output artifacts.

Not allowed:

- No schema migration.
- No database writes, except optional disposable test fixtures inside tests.
- No invite behavior changes.
- No account transfer behavior.
- No permission expansion.
- No owner projection changes.
- No Admin Portal capability changes.
- No billing, checkout, webhook, Stripe, Apple, or Phase 15R behavior changes.
- No HorseOps privacy behavior changes.
- No landing page changes.
- No native app, push, service worker, or offline sync work.
- No Phase 16 cleanup.

## Audit Surface

Backend/source audit:

- `users` role, `platform_role`, `barn_id`, account status, role status.
- `barns` ownership and subscription pointers.
- Owner linkage fields including `primary_owner_id`.
- Invite and acceptance routes.
- Auth/session user resolution.
- Permission helpers and role groups.
- Tenancy helpers, including active-facility enforcement.
- Subscription/account entitlement lookup.
- HorseOps owner-safe projection and cross-facility guardrails.
- Admin Portal read/write boundaries.

Data-shape audit:

- Existing `users` rows with duplicate emails, missing `barn_id`, pending review,
  platform roles, owner roles, barn-manager/admin roles, and demo-seeded rows.
- Existing `barns` rows and subscription/account linkage.
- Existing horse ownership links and owner portal assumptions.
- Existing invites or invite-like records, if present.

Frontend/source audit:

- Route gates and `ROLE_GROUPS`.
- Invite acceptance and signup flows.
- Dashboard/onboarding assumptions about one active facility.
- Owner portal and horse detail assumptions.
- Admin Portal display assumptions.

## Deliverables

Created:

- `outputs/build_next_3_multi_barn_multi_role_gap_report.md`
- `backend/tests/test_build_next_3_multi_barn_gap_report.py`
- Updates to `docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md`
- Updates to `docs/PHASED_EXECUTION_PLAN.md`
- Updates to `memory/PRD.md`
- Updates to `memory/ROADMAP.md`
- Package: `outputs/build_next_3_multi_barn_multi_role_gap_report.zip`

## Gap Report Must Include

- Current account model summary.
- Current barn membership assumptions.
- Current role model assumptions.
- Current invite/onboarding assumptions.
- Data privacy risks if multi-barn is enabled too early.
- Billing/entitlement risks for multi-barn users.
- Owner portal risks for multi-horse and cross-barn ownership.
- Admin Portal and platform-role interaction notes.
- Recommended target model.
- Migration phases with clear ordering.
- Exact deferrals.

## Recommended Target Model To Evaluate

Do not implement this in Build-Next-3, but evaluate it as the likely future
direction:

- Keep `users` as the global identity record.
- Introduce a future `account_memberships` collection:
  - `account_id`
  - `account_type`
  - `user_id`
  - `barn_id`
  - `role`
  - `role_status`
  - `membership_status`
  - `relationship_type`
  - `is_primary`
  - `created_at`
  - `updated_at`
- Treat current `users.barn_id` and `users.role` as compatibility fields until
  migrated.
- Resolve an active facility context explicitly for normal app users.
- Keep platform admins separate via `platform_role`.
- Keep invited owner portal access permission-based and free/manual.

## Focused Test Ideas

If tests are added, they should be source-level or read-only:

- Current route guards still rely on a single active user context.
- Owner-safe HorseOps paths still depend on `primary_owner_id`.
- Admin Portal platform roles do not imply barn membership.
- Subscription/billing account lookup remains barn/account scoped.
- Invite/onboarding routes are identified as requiring future membership
  context before multi-barn launch.

## Acceptance Criteria

- Build-Next-2B remains locked and unchanged.
- Build-Next-3 produces a concrete gap report.
- The report clearly separates safe-now behavior from future migration work.
- No runtime product behavior changes are introduced.
- Any focused tests pass.
- Package integrity passes.

## Founder Decisions Locked After Report

1. Owner access remains horse-specific for launch.
2. Preserve `users.barn_id` and `users.role` as compatibility mirrors through
   launch.
3. Individual-owner account ids are generated, not raw `user_id`.
4. Facility search / lead capture applies to all non-platform onboarding paths
   except invited users; individual owners may continue without an active
   facility.
