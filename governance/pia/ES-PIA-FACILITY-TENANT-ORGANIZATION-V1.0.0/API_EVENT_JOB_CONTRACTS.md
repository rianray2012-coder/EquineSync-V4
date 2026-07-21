# API, Event, and Job Contracts

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
- Version: `1.0.0-candidate`
- Date: `2026-07-20`
- Status: `FOUNDER_DECISION_REQUIRED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.

| ID | Interface | Kind | Permission/actor | Input | Output/consumer | Evidence | Failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FAC-API-001 | POST /tenants/{tenant}/facilities | Command | facility:create | tenant context, idempotency key, proposed identity/address | Facility candidate plus change_set_id | facility.created | 409 duplicate candidate; 403 generic deny |
| FAC-API-002 | POST /contexts/select | Command | context:switch | tenant/facility/org association tuple | short-lived context reference and display labels | context.selected | 404 unavailable context |
| FAC-API-003 | POST /facilities/{id}/areas | Command | facility_area:write | parent/version/type/provenance | area and change_set_id | facility_area.created | 409 cycle/stale version |
| FAC-API-004 | POST /facilities/{id}/association-changes | Command | organization:associate | typed before/after associations and effective time | change proposal/result | facility.association_changed | 422 unresolved authority/evidence |
| FAC-API-005 | POST /facilities/merge-proposals | Command | facility:merge | candidate ids, survivor proposal, evidence | quarantined proposal | facility.merge_proposed | 409 unresolved identity |
| FAC-API-006 | POST /facilities/{id}/close | Command | facility:close | effective time, reason, impact acknowledgement | closed state/change set | facility.closed | 409 unresolved dependencies |
| FAC-API-007 | PUT /facilities/{id}/public-projection | Command | facility:publish | approved field subset/purpose/expiry | projection version | facility.public_projection_changed | 422 sensitive field |
| FAC-API-008 | GET /facility-search | Query | facility:read | active context, purpose, filter | permission-filtered results only | search.executed | generic empty/deny |
| FAC-EVT-001 | facility.context_invalidated | Event | system | tenant/facility/org, cause, effective_at | Consumers revoke cached context | append-only | Dead-letter if context unknown |
| FAC-EVT-002 | facility.topology_changed | Event | system | change_set_id, before/after refs, tenant | Consumers re-evaluate projections | append-only | Retry idempotently |
| FAC-EVT-003 | organization.facility_association_changed | Event | system | association id/type/interval/status | Consumers recalculate only their owned effects | append-only | No authority side effect |
| FAC-JOB-001 | context-expiry sweeper | Job | service identity | tenant partitions and current time | expire context caches | job evidence | Fail closed; retry partition |
| FAC-JOB-002 | public-projection expiry | Job | service identity | projection expiry | unpublish expired fields | job evidence | Fail private |
| FAC-JOB-003 | topology reconciliation | Job | service identity | quarantine/change-set ledgers | report only unless separately authorized | job evidence | Never auto-merge |

All identifiers and routes are candidate contracts. They are not active endpoints, schemas, jobs, or implementation authority. Every command requires tenant context, idempotency, optimistic version, authorization reference and audit correlation unless explicitly documented otherwise.
