# RF18 QA, UAT, Migration, and Public Launch Re-Readiness

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Purpose

RF18 consolidates the locked RF1-RF17 refinement evidence into a final
QA/UAT/public-launch re-readiness gate. It is not a launch approval.

## Current Status

| Area | RF18 Status |
| --- | --- |
| Locked RF1-RF17 source evidence | ready for founder/UAT review |
| Public launch | no-go until UAT acceptance |
| Staging UAT | required |
| Founder acceptance | required |
| Destructive migrations/backfills | deferred unless separately approved |
| Store submission/native billing/provider sync/full offline | deferred |

## UAT Rows

| Area | Status | Required Evidence |
| --- | --- | --- |
| Enrollment and signup | requires staging UAT | Individual owner, barn owner/manager, trainer, service provider, and invite-first rider/guardian/staff paths. |
| Owner/guardian/rider visibility | requires staging UAT | Relationship-scoped portal views and unrelated-user denial. |
| Staff/trainer workflows | requires staging UAT | Staff My Work/Today, trainer operating center, assigned-horse, unrelated-horse denial, owner-visible training summary. |
| Service-provider grants | requires staging UAT | First provider type, grant, revocation, denied access, visit note, unrelated-horse denial. |
| Billing/payment/export truth | requires staging UAT | Owner billing, admin billing, export, configuration-only payment state, no checkout/client-secret leakage. |
| Documents/signatures/messaging | requires staging UAT | Guardian-required docs, local form acknowledgement, push-preview/local-log, announcement visibility. |
| Field reliability/native shell | requires staging UAT | Weak-signal task retry/draft recovery smoke and native shell smoke without store submission. |

## Migration / Backfill Rows

| Migration Area | RF18 Status |
| --- | --- |
| Historical name-only staff rows | classify only |
| `staff_task_assignments` | classify only |
| `supply_inventory_items` | classify only |
| `owner_media_updates` | classify only |
| Leasee grants/revocation | deferred to explicit implementation |
| Limited modified-individual-owner trial enforcement | deferred to explicit implementation |

## Founder Decision Rows

| Decision | Status |
| --- | --- |
| Accept RF18 as evidence/UAT gate, not public launch approval. | requires founder review |
| Choose official UAT environment and accounts. | requires founder review |
| Approve or defer remaining migration/backfill work. | requires founder review |
| Approve public launch or keep launch no-go. | requires founder review |

## Boundary

RF18 does not mutate production, staging, seeded-demo, or UAT accounts. It does
not call providers, submit stores, collect live payments, run destructive
migrations, or approve public launch.
