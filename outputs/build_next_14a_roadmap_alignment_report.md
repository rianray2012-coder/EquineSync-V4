# BN14A Roadmap Alignment Report

## Executive Summary

The uploaded roadmap is directionally correct, but the current EquineSync app is
already beyond the roadmap's Phase 0 and Phase 1 baseline. Admin Portal,
HorseOps, billing, role routing, DocuSign, UAT evidence, and role-home surfaces
are materially built.

The main pre-expansion risk is not lack of foundations. The risk is treating
generic backlog modules, setup-intent role pages, and placeholder-aware surfaces
as finished product workflows.

Recommendation: lock BN14A as the alignment packet, run BN14B for hardening and
role UX cleanup, then begin BN15A with Today's Pulse Data Contract.

## Current Code Inventory

### Backend

Observed route decorators: 268.

Major implemented areas:

- Authentication and email verification routes.
- Account context and multi-membership foundations.
- Admin Portal modular package.
- Admin users, facilities, horses, billing, subscriptions, reports, alerts,
  audit logs, support, integrations, and settings.
- HorseOps Care Ledger routes including owner-safe summaries, daily checks,
  alerts, service requests, visibility policies, manager pulse, templates, and
  platform horse summaries.
- Billing, subscriptions, Stripe webhook handlers, usage limits, add-ons,
  recurring charges, and subscription email foundations.
- DocuSign/document signature provider prep, templates, requests, sandbox
  envelope creation, and webhook status sync.
- Owner updates and review lifecycle.
- Invite, minor/guardian, role intake, onboarding, care, operations, reports,
  and generic backlog routes.

### Frontend

Major implemented areas:

- Role-specific navigation.
- Post-login role routing.
- Role-home surfaces for platform, facility admin, barn owner, barn manager,
  trainer, staff, horse owner, guardian, rider, and individual owner.
- Admin Portal shell and pages.
- Today, My Work, Horse Profile, Owner Care Ledger, Care Ledger tab.
- Billing/subscription UI.
- DocuSign/forms UI.
- Generic feature workspaces for many future roadmap modules.

### Foundation vs Workflow Boundary

The following are meaningful foundations but should not be counted as complete
roadmap workflows yet:

- `routes/backlog.py` feature modules.
- `FeatureWorkspace.jsx` pages.
- role-home setup-intent forms.
- pages that store records but do not yet enforce roadmap-specific state
  machines, approvals, visibility, Today’s Pulse integration, or timeline
  integration.

## Uploaded Roadmap Alignment

See `outputs/build_next_14a_phase_matrix.md` for phase-by-phase classification.

Highest-confidence built or mostly built areas:

- Admin/platform control.
- Role routing and role shells.
- Minor/guardian safety foundations.
- HorseOps privacy-first care ledger.
- Owner-safe service requests.
- Billing entitlement / Stripe catalog foundations.
- DocuSign provider foundations.
- UAT/evidence tooling.

Highest-priority gaps:

1. Unified Today's Pulse contract.
2. Horse Watchlist.
3. Horse Timeline.
4. Changed Since Last Login / Last Shift.
5. Staff workflow safety states.
6. Facility ticket state machine.
7. Client onboarding/gear/tack/grooming workflows.
8. Trainer recommendations and owner shopping list.
9. Communication preferences and media controls.
10. Compliance/service package/billing approval workflows.

## Verification Performed

### Frontend Build

Result: PASS.

`npm run build` completed successfully. The build emitted only dependency/tooling
deprecation warnings.

### Focused Test Check

Result: PARTIAL.

Passed:

- `test_build_next_13p_role_home_title_case.py`
- `test_build_next_13o_role_screenshot_pass.py`

Failed:

- `test_admin_portal_route_lock_guard.py`

Failure reason: test path portability. The test hardcodes `/app/backend/...` for
its import path, admin-portal package scan path, and `portal.py` read path. In
this relocated Codex checkout, the static scan sees zero local route decorators
before the hardcoded `portal.py` read fails. This is a hardening issue and
should be fixed before expansion, but it is not evidence of missing Admin Portal
product routes.

## Worktree Hygiene

The worktree contains current BN13O/BN13P modifications and untracked files.
Several untracked files appear to be duplicate copies with ` 2` in their names.
BN14A did not remove them.

Recommended: BN14B should include controlled cleanup after confirming no file is
needed.

## Founder-Facing Decision

Recommended next action:

Proceed with BN14B - Role UX + Hardening Cleanup.

Do not begin new feature expansion until:

- route-lock test portability is fixed;
- duplicate notification categories are triaged;
- docs/status reconciliation is done;
- permission matrix artifact is prepared;
- current BN13P/BN14A packages are committed or otherwise preserved.
