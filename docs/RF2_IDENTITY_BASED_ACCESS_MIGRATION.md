# RF2 Identity-Based Access Migration

Date: 2026-07-06

Status: CODEX-REVIEWED & LOCKED.

## Objective

RF2 addresses the highest-confidence remaining identity-access finding after RF1:
staff scheduling, tasks, handoffs, and time-clock self-service could be matched
through display/free-text staff names. RF2 changes those backend access decisions
to stable user-ID predicates and records later identity work that should not be
overclaimed yet.

## Source Changes

### Staff Access Predicates

`backend/routes/backlog.py` now centralizes staff access clauses:

- `_staff_shift_clauses(user_id)`
- `_staff_task_clauses(user_id)`
- `_staff_handoff_clauses(user_id)`
- `_staff_time_clock_clauses(user_id)`

These helpers match stable fields such as:

- `staff_user_id`
- `data.staff_user_id`
- `data.staff_user_ids`
- `assigned_user_id`
- `assigned_staff_user_id`
- `data.assigned_user_id`
- `data.assigned_to_user_id`
- `data.assigned_staff_user_id`
- `data.incoming_staff_user_id`
- `data.outgoing_staff_user_id`

They do not use `staff_name`, `assigned_to`, `incoming_staff`, `outgoing_staff`,
`full_name`, or `_exact_name_query` as access predicates.

### Staff Portal My Work

`GET /staff-portal/my-work` now loads:

- shifts through `_staff_shift_clauses(user_id)`
- staff task assignments through `_staff_task_clauses(user_id)`
- shift handoff reports through `_staff_handoff_clauses(user_id)`
- time-clock entries through `_staff_time_clock_clauses(user_id)`

Legacy display fields can still be present in returned records, but they are not
used to decide whether the staff user can access the record.

### Staff Task Status

`PATCH /staff-portal/tasks/{record_id}/status` now scopes non-admin status
updates through `_staff_task_clauses(user.get("id"))`.

When a task is completed, RF2 stores:

- `completed_by_user_id`
- `completed_by_name`

The name remains display evidence only; the stable ID is the durable actor link.

### Time Clock

Staff clock-in and clock-out ownership checks now use
`_staff_time_clock_clauses(user.get("id"))`.

New clock-in entries stamp:

- `staff_user_id`
- `staff_name`

`staff_name` remains a display/reporting value. `staff_user_id` is the ownership
predicate.

### Payroll Export

`POST /staff-portal/payroll-export` now accepts `staff_user_id` and applies it as
`data.staff_user_id`.

The previous `staff_name` admin report filter remains for compatibility. It is
not used for self-service authorization and should be retired or limited after
RF8/RF12 decisions.

## Evidence Rows

The generated report at `outputs/rf2_identity_access_migration_report.md`
contains these rows:

- `staff_identity_predicate_helpers`
- `staff_my_work_identity_scope`
- `staff_task_status_identity_scope`
- `time_clock_identity_scope`
- `payroll_export_identity_filter`
- `document_signature_identity_scope`
- `remaining_identity_models_deferred`

Overall RF2 status can be `ready` while still carrying deferred rows, because
those rows belong to model-expansion phases rather than this narrow migration
gate.

## Deferred Work

RF2 does not claim universal identity migration.

Deferred:

- RF8: full staff workforce model, account-membership joins, backfill, audited corrections, and UI form conversion from name text fields to user selectors.
- RF10: service provider multi-barn/client access-grant model.
- RF13: message-recipient identity model and delivery truth.
- RF14: deeper legal-signature truth and signed-document storage.
- RF17: feature-shell UX truth pass for remaining name-based forms.

## Founder Review

| Decision | Status | Notes |
| --- | --- | --- |
| Accept strict staff self-service matching for stable user-ID records only. | accepted in RF2 lock | This protects staff privacy and assignment boundaries, but legacy name-only rows need RF8 migration/backfill before they appear in self-service. |
| Decide whether admin payroll `staff_name` filtering can remain during pilot. | deferred by RF2 lock | It is now a compatibility filter, not the preferred canonical identity selector. |
| Accept RF2 deferrals for provider grants, message recipients, and full workforce membership. | accepted deferral in RF2 lock | These are model phases, not safe one-off predicate patches. |

## Lock Note

RF2 is Codex-reviewed and locked as a narrow identity-access migration. RF2 does
not authorize claims that EquineSync has completed universal identity migration.
RF8/RF10/RF13/RF17 remain responsible for full workforce, provider, messaging,
and feature-shell identity work.

## Verification

Focused RF2 verification:

```bash
./.venv/bin/python -m pytest backend/tests/test_rf2_identity_access_migration.py -q
./.venv/bin/python -m backend.scripts.build_rf2_identity_access_migration_proof --output outputs/rf2_identity_access_migration_report.md --fail-on-blockers
```

Packaging verification:

```bash
unzip -t outputs/build_next_rf2_identity_access_migration.zip
```
