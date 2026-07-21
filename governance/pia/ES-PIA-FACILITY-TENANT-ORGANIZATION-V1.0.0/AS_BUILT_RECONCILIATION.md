# As-Built Reconciliation

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
- Version: `1.0.0-candidate`
- Date: `2026-07-20`
- Status: `LEGACY_NONCONFORMANCE_RECORDED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.

## Method

Static read-only source inspection only. No application/database was started; no migration or test environment was created.

## Evidence and classification

| Evidence | Observation | Target comparison | Classification |
| --- | --- | --- | --- |
| `backend/core/tenancy.py` | `PRIMARY_BARN_ID="primary"`; missing user barn resolves to primary; comments map task-engine `tenant_id="default"` to `barn_id="primary"`. | Missing/unknown target context must fail closed or quarantine. | PROHIBITED_LEGACY_FALLBACK / IMPLEMENTATION_GAP |
| `backend/task_engine.py` and `backend/core/lifespan.py` | Task/media partition uses default tenant and primary barn compatibility mapping. | Tenant and Facility/Barn must remain distinct. | IMPLEMENTATION_GAP |
| `backend/routes/barns.py` | Barn provisioning creates a barn and first admin with one-barn-per-user language; writes `db.barn` while status gates read `db.barns`. | Target requires explicit Tenant/Facility/Organization topology and contract consistency. | IMPLEMENTATION_GAP / REVIEW_REQUIRED |
| `backend/core/account_memberships.py` | Additive facility account memberships mirror `users.barn_id` and role; comments acknowledge future transition. | Useful foundation but Role/relationship/account cannot become authority. | PARTIAL_CONFORMING_FOUNDATION |
| `backend/core/account_route_context.py` | Selected facility context resolves membership then reads barn status. | Moves toward explicit context but does not demonstrate full Tenant/Organization model. | PARTIAL_CONFORMING_FOUNDATION |
| application-wide `barn_id` fields | Many domain records are barn-scoped. | Provides partial isolation evidence, not proof of Tenant/Facility/Organization separation. | PARTIAL_CONFORMING_FOUNDATION |

## Disposition

The current software is not claimed conformant to this candidate and was not dynamically verified. The PIA records a target design independent of the legacy shortcuts. Any remediation requires a separately authorized, inventoried, reversible migration and work-package sequence. No source file outside this documentary package was modified.
