# API, Event, and Job Contracts

**Status:** `DESIGN_CANDIDATE_NOT_AUTHORIZED`

## API envelope

Every request resolves authenticated principal, acting/represented actor chain, tenant, optional facility, context version, permission version, purpose, request ID, and idempotency key before resource lookup. Caller-supplied tenant or facility identifiers are constraints, never authority. Non-enumerating `404` or equivalent safe errors apply after authorization policy.

Candidate resources: `/tenants`, `/facilities`, `/organizations`, `/facility-areas`, `/topology-edges`, `/tenant-facility-associations`, `/organization-tenant-controls`, `/active-contexts`, `/duplicate-candidates`, `/topology-changes`, `/legacy-quarantine`, and `/facility-public-projections`. No route is authorized by this package.

## Events

Candidate event families include `tenant.lifecycle.changed`, `facility.lifecycle.changed`, `organization.lifecycle.changed`, `facility.topology.changed`, `tenant_facility.association.changed`, `organization_tenant.control.changed`, `active_context.switched`, `facility.public_projection.changed`, `facility.duplicate_candidate.changed`, `facility.topology_change.reconciliation_required`, and `legacy_topology.quarantine.changed`.

Every event carries event ID, schema version, canonical entity and version, tenant or explicit governed cross-tenant scope, effective/recorded time, source/provenance, actor chain, reason, evidence references, prior/new state, idempotency key, correlation/causation IDs, privacy class, and replay policy. Consumers cannot infer permission from event receipt.

## Jobs

Candidate jobs include projection invalidation, lifecycle enforcement, duplicate-candidate generation, topology consistency validation, legacy quarantine analysis, retention handoff, external-ID reconciliation, and stale-context revocation. Every job is tenant-partitioned, checkpointed, idempotent, permission-aware, suspendable, rate-limited, and auditable. Cross-tenant aggregation requires a separately authorized purpose and minimum-necessary projection.

## Failure and recovery

Retries preserve idempotency and ordering constraints. Poison messages quarantine without cross-tenant spill. Replay re-evaluates current lifecycle and permission state. Recovery cannot resurrect closed, revoked, merged, or stale authority. External systems remain adapters and never overwrite canonical truth silently.
