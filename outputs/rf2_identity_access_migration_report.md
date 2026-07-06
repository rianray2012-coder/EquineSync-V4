# RF2 Identity-Based Access Migration Report

Phase: `RF2`

Lock status: `Codex-reviewed and locked`

Overall status: `ready`

## Readiness Rows

| Key | Status | Evidence | Next Action |
| --- | --- | --- | --- |
| `staff_identity_predicate_helpers` | `ready` | `backend/routes/backlog.py` has shared staff access helpers keyed to stable user IDs. | RF8 should migrate/backfill all legacy staff records to these stable ID fields. |
| `staff_my_work_identity_scope` | `ready` | Staff My Work now queries shifts, tasks, handoffs, and time entries through stable user-ID clauses. | RF8 should convert the staff scheduling UI/forms to write stable IDs natively. |
| `staff_task_status_identity_scope` | `ready` | Non-admin task status updates are authorized by assignment user IDs and completion stores `completed_by_user_id`. | RF8 should retire legacy `assigned_to` text assignment fields after migration. |
| `time_clock_identity_scope` | `ready` | Staff clock-in/clock-out ownership uses stable user-ID predicates and new entries stamp `staff_user_id`. | RF8 should add audited correction/backfill tooling for legacy time-clock rows. |
| `payroll_export_identity_filter` | `ready` | Payroll export supports `staff_user_id` as the stable staff filter while retaining `staff_name` as an admin legacy/display filter. | RF8/RF12 should make `staff_user_id` the canonical payroll export selector and deprecate name filtering. |
| `document_signature_identity_scope` | `ready` | Document signature requests already use subject/guardian/countersigner user IDs plus barn-scoped reads. | RF14 should consolidate legal signature truth, provider status, and signed-document storage. |
| `remaining_identity_models_deferred` | `deferred` | Provider grants, message-recipient IDs, full workforce membership, and feature-shell form rewrites require RF8/RF10/RF13/RF17 model work. | Do not claim universal identity migration until those later RF phases are implemented and reviewed. |

## Founder Decision Rows

| Decision | Status | RF Phase | Notes |
| --- | --- | --- | --- |
| Accept strict staff self-service matching for stable user-ID records only. | accepted in RF2 lock | RF2, RF8 | RF2 intentionally does not expose staff self-service records that only match a display/free-text staff name. Legacy records need RF8 migration/backfill. |
| Decide when to retire admin payroll `staff_name` filtering. | deferred by RF2 lock | RF8, RF12 | RF2 keeps the legacy name filter for admin reporting compatibility, but `staff_user_id` is now the preferred filter. |
| Keep provider grants, message recipients, and full workforce membership deferred. | accepted deferral in RF2 lock | RF8, RF10, RF13 | RF2 records those as model-dependent follow-on work; no provider or messaging expansion is included here. |

## Acceptance Boundary

- RF2 replaces known staff self-service access predicates with stable user-ID predicates.
- RF2 preserves display names and import/form labels where they are not authorization predicates.
- RF2 does not build the RF8 workforce model, RF10 provider multi-barn model, RF13 messaging delivery model, or RF17 feature-shell UX truth pass.
- RF2 does not mutate provider services, Stripe, Apple, Google, DocuSign, Resend, MongoDB Atlas, Vercel, Render, GitHub, or UAT accounts.
