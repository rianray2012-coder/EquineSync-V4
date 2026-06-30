# Build-Next-13A - Role Routing + Landing Fixes

Status: ready for review.

## Purpose

BN13A fixes the first screen after sign-in. EquineSync should send each user to
the correct role context instead of sending everyone to the same barn dashboard.

This is a routing-contract phase only. It does not build the full role-specific
dashboards, change backend permissions, add billing behavior, modify Stripe or
DocuSign, or approve launch.

## Scope

- Centralized post-login route resolver:
  `frontend/src/lib/roleLanding.js`
- Login now routes through the resolver instead of hardcoding `/dashboard`.
- Already-authenticated visits to `/login` also route through the resolver.
- Platform admins resolve to `/admin/portal/dashboard`.
- Client-facing roles resolve to safe role homes instead of barn setup.
- Staff and manager roles resolve to the current operations hub.
- `/onboarding` is guarded so only facility-setup eligible users can enter.
- Sidebar Dashboard link now points to `/dashboard`, not the marketing root.
- Minimal role home shell:
  `frontend/src/pages/RoleHome.jsx`

## Role Landing Matrix

| Role/Profile | BN13A Landing |
| --- | --- |
| Any valid `platform_role` | `/admin/portal/dashboard` |
| Facility admin / barn owner with incomplete setup signal | `/onboarding` |
| Facility admin / barn owner with no incomplete setup signal | `/dashboard` |
| Barn manager / trainer | `/today` |
| Groom / working student | `/today` |
| Horse owner with linked horse id on user payload | `/owner/horses/{horseId}` |
| Horse owner without linked horse id | `/role-home/owner` |
| Guardian / parent | `/role-home/guardian` |
| Lesson participant / rider | `/role-home/rider` |

## Deferred to BN13B+

- Full role-specific navigation menus.
- Rider Intake Wizard.
- Owner + Horse Intake Wizard.
- Guardian + Minor Rider Intake Wizard.
- Staff Profile Setup.
- Manager Setup.
- Owner, rider, guardian, staff, manager, and facility-admin full dashboards.
- Body-check workflow.

## Verification

Focused checks:

```bash
python -m pytest backend/tests/test_build_next_13a_role_routing.py -q
```

## Current Verdict

`role routing ready`

BN13A makes the role doors correct. BN13B should make each role's menu match
the new destination.
