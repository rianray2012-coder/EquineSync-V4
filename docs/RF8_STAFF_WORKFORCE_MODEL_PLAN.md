# RF8 Staff Workforce Model Plan

Date: 2026-07-06

Status: completed and locked.

## Purpose

RF8 should unify staff identity, scheduling, task assignment, handoff, time
clock, and payroll export semantics so workforce workflows use stable user IDs
and account membership context instead of display-name matching.

## Entry Conditions

- RF7 is Codex-reviewed and locked.
- RF2 stable-ID backend self-service predicates remain locked.
- RF6 Task Engine canonical decision remains locked.

## Strict Scope

RF8 may:

- inventory workforce records that still depend on `staff_name`, `assigned_to`,
  incoming/outgoing staff names, or similar display text;
- add or validate `staff_user_id`, `assigned_user_id`,
  `incoming_staff_user_id`, `outgoing_staff_user_id`, and
  `account_membership_id` fields where needed;
- backfill or migration-plan legacy workforce records;
- replace highest-risk staff text inputs with stable staff selectors where the
  surrounding UI is already live;
- align Staff Tasks with Task Engine posture by migrate, hide, or admin-readiness
  decision;
- prove My Work, scheduling, handoff, time clock, and payroll export use stable
  identity filters.

RF8 must not:

- rebuild the trainer operating center;
- implement service-provider multi-barn grants;
- change billing/payment truth;
- add native mobile behavior;
- call providers;
- mark founder decisions accepted;
- retire broad feature shells outside the staff/workforce scope.

## Target Workstreams

| Workstream | Goal | Evidence Required |
| --- | --- | --- |
| Workforce identity inventory | Find every staff/workforce display-name dependency. | Source scan report with route, collection, field, and risk classification. |
| Stable staff selectors | Replace high-risk name text inputs where workflows are live. | Frontend source evidence and focused tests. |
| Staff schedule and handoff identity | Ensure assignments and handoffs use stable user IDs. | Backend route tests for self-service and admin views. |
| Time clock and payroll | Keep clock ownership and payroll filters user-ID based. | Tests proving `staff_user_id` filters and export metadata. |
| Staff Tasks vs Task Engine | Resolve or defer the duplicate staff task surface after RF6 canonical decision. | migration/hide/admin-readiness decision row and source evidence. |
| Legacy row handling | Avoid breaking older rows while preventing name-only authorization. | Backfill plan or compatibility tests. |

## Acceptance Criteria

- RF8 report status is `ready` with zero blocker rows.
- Staff self-service access does not depend on display names.
- Payroll export can filter by stable staff user ID.
- Staff assignment forms do not create new name-only authorization dependencies
  on live workflows.
- Staff Tasks has a clear Task Engine migration, hide, or admin-readiness
  posture.
- Founder-decision rows exist for any migration, backfill, or feature-shell hide
  choice that cannot be completed in RF8.

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Accept Task Engine as the canonical staff task lifecycle over Staff Tasks. | requires founder review | RF6 recorded this; RF8 must either implement or defer the migration/hide action. |
| Approve legacy staff-row backfill approach. | requires founder review | Legacy rows with only staff display names may require data migration timing and rollback posture. |
| Decide whether Staff Tasks remains visible during migration. | requires founder review | If not migrated in RF8, it should be hidden, relabeled, or moved to admin-readiness. |

## Recommended Verification

- Focused RF8 proof tests.
- Report generation with `--fail-on-blockers`.
- Any touched frontend build or targeted route tests.
- Zip integrity and expected manifest check.
- `git diff --check`.
- Secret-shape scan.
