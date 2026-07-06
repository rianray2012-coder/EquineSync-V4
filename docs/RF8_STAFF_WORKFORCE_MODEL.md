# RF8 Staff Workforce Model

Date: 2026-07-06

Status: CODEX-REVIEWED & LOCKED.

## Purpose

RF8 hardens staff workforce identity across scheduling, task assignment,
handoff, time clock, payroll export, and My Work surfaces without rebuilding the
entire workforce model.

## Completed Hardening

| Area | RF8 Status | Evidence |
| --- | --- | --- |
| Staff directory | ready | Adds `/staff-portal/staff-directory`, scoped by `staff:read`, same barn, and staff roles only. Projection returns safe user id, name, email, and role fields. |
| Server-side identity normalization | ready | New staff scheduling, Staff Tasks, handoff, and time-clock creates require stable staff user ids; create/update paths verify supplied ids and stamp display names from trusted user records. |
| Staff scheduling form | ready | New shifts require and submit `staff_user_id` plus display `staff_name`; My Work already uses stable staff-user predicates. |
| Staff task form | ready | New Staff Tasks require and submit `assigned_user_id` plus display `assigned_to`; staff task self-service status updates remain ID-scoped. |
| Handoff form | ready | New handoff reports require and submit `incoming_staff_user_id` and `outgoing_staff_user_id` plus display names. |
| Time clock form | ready | New admin-created time entries require and submit `staff_user_id`; staff portal clock-in already stamps stable `staff_user_id`. |
| Payroll export | ready | Stable `staff_user_id` filter remains available and recorded in export metadata. |

## Deferred or Founder-Decision Items

| Item | Status | Next Action |
| --- | --- | --- |
| Historical staff rows | deferred | Legacy rows that only carry display names remain visible/admin-editable. Founder should approve backfill timing and rollback before mutation. |
| Staff Tasks migration | deferred | Task Engine is canonical from RF6, but RF8 does not migrate or hide `staff_task_assignments`. RF17 or a founder-approved RF8 follow-up should migrate, hide, or relabel it. |
| Admin payroll name filter | deferred | RF8 keeps the legacy `staff_name` export filter for compatibility. RF12 should decide when to retire it. |

## Founder Decision Rows

| Decision | Status | Phase |
| --- | --- | --- |
| Accept Task Engine as canonical over Staff Tasks while Staff Tasks remains migration/hide work. | requires founder review | RF8/RF17 |
| Approve a legacy staff-row backfill strategy. | requires founder review | RF8/RF18 |
| Decide when to retire admin payroll staff-name filtering. | requires founder review | RF8/RF12 |

## Launch Claim Boundary

Current launch/pilot claims may say new staff scheduling, task, handoff, and
time-clock creates require stable staff user ids.

Do not claim:

- historical workforce backfill is complete;
- Staff Tasks has been migrated into Task Engine;
- all staff feature shells are production-complete;
- payroll/export name filtering has been retired;
- trainer or provider workforce expansion is complete.

## Evidence

Generated report:
`outputs/rf8_staff_workforce_model_report.md`.

Locked package:
`outputs/build_next_rf8_staff_workforce_model.zip`.
