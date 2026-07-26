# API, Event, and Job Contracts

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED`
- Candidate disposition before fresh review: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

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
| FAC-API-009 | POST /onboarding/plans | Command | onboarding:initialize | actor and explicitly selected individual-owner or structured path; no presumed topology | expiring OnboardingPlan and visible isolation/context explanation | onboarding.path_selected | 422 if truthful path cannot be represented without invention |
| FAC-API-010 | POST /onboarding/individual-owner | Command | onboarding:initialize | actor, horse-first intent and minimum identity/horse references | private Tenant-isolated individual context; no Facility/Organization/Barn/Business | onboarding.domain_setup_complete | Atomic rollback if minimum isolation fails |
| FAC-EVT-004 | onboarding.context_association_requested | Event | authorized actor | explicit target association, purpose and authority reference | Relationship/Authorization domains evaluate request | append-only | No association or authority on failure |

All interfaces remain candidate design contracts. The onboarding-plan interface creates no domain entity or authority by itself. The individual-owner interface establishes minimum Tenant isolation without presenting Tenant as a Facility, Organization, Barn, or Business.
