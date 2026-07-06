# RF8 Staff Workforce Model Report

Phase: `RF8`
Overall status: `ready`

## Status Rows

| Key | Area | Status | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| staff_directory_endpoint | Stable staff directory | ready | RF8 adds a same-barn staff directory with safe user id/name/role projection for admin staff workflows. | RF18 should browser-smoke staff selector behavior with seeded admin/manager accounts. |
| server_side_staff_identity_normalization | Server-side staff identity stamping | ready | Create paths require stable staff ids for staff scheduling, tasks, handoffs, and time-clock rows; create/update paths verify supplied ids and stamp display names from trusted user records. | Backfill legacy name-only rows after founder accepts a migration plan. |
| frontend_staff_forms_submit_stable_ids | Staff workflow forms | ready | Live staff module create flows now require and submit stable staff ids while preserving display labels for readability. | RF17 can further relabel or hide noncanonical staff feature shells after Task Engine migration decisions. |
| self_service_predicates_remain_id_based | My Work self-service predicates | ready | My Work, task status mutation, handoffs, and time-clock ownership stay on stable ID predicates, not display-name matching. | Keep legacy display names as labels only, not authorization keys. |
| payroll_export_stable_filter_retained | Payroll export identity | ready | Payroll export keeps the stable `staff_user_id` filter; legacy `staff_name` remains an admin compatibility filter, not self-service authorization. | RF12 should decide when the admin name filter can be retired from payroll/export tooling. |
| staff_tasks_task_engine_decision_deferred | Staff Tasks versus Task Engine | deferred | Task Engine remains canonical; RF8 prevents new staff-task ID drift but does not migrate or hide Staff Tasks. | RF17 or a founder-approved RF8 follow-up should migrate, hide, or relabel Staff Tasks. |
| legacy_staff_rows_backfill_deferred | Legacy staff rows | deferred | Legacy display-name rows remain visible for admins but are not treated as self-service authorization truth. | Founder should approve a data migration/backfill plan before changing historical records. |

## Founder Decision Rows

| Decision | Status | Phase | Notes |
| --- | --- | --- | --- |
| Accept Task Engine as canonical over Staff Tasks while Staff Tasks remains migration/hide work. | requires founder review | RF8, RF17 | RF8 prevents new staff-task ID drift but does not migrate Staff Tasks into Task Engine. |
| Approve a legacy staff-row backfill strategy. | requires founder review | RF8, RF18 | Legacy rows with only staff display names remain visible/admin-editable but are not self-service authorization truth. |
| Decide when to retire admin payroll staff-name filtering. | requires founder review | RF8, RF12 | RF8 keeps `staff_user_id` as the stable payroll selector while preserving the old staff-name filter for admin compatibility. |

## RF8 Boundary

- RF8 hardens staff workforce identity for live staff-module create flows and self-service staff views.
- RF8 does not migrate historical rows, delete Staff Tasks, rebuild Task Engine, change billing truth, add provider grants, or mark founder decisions accepted.
- Current launch claims may say new staff scheduling, task, handoff, and time-clock creates require stable staff ids. They must not claim historical workforce backfill or Staff Tasks migration completion.
