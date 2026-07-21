# Data Dictionary

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
- Version: `1.0.0-candidate`
- Date: `2026-07-20`
- Status: `FOUNDER_DECISION_REQUIRED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.

| Entity ID | Entity | Purpose | Minimum fields | Boundary |
| --- | --- | --- | --- | --- |
| FAC-ENT-001 | Tenant | Strict application isolation and governance context | tenant_id, display_name, state, created_at, closed_at, version | No physical, legal, billing or authority equivalence |
| FAC-ENT-002 | Organization | Durable entity identity for legal, operating, administrative or service bodies | organization_id, names, types, verification_state, provenance, lifecycle | Identity is separate from authority and Business operation |
| FAC-ENT-003 | Facility | Durable physical-place identity | facility_id, names, address_id, timezone, locale, state, lineage | No implied owner, operator, tenant or authority |
| FAC-ENT-004 | FacilityArea | Nested topology element | area_id, facility_id, parent_area_id, area_type, name, state, lineage | Acyclic; sensitive classes private by default |
| FAC-ENT-005 | TenantOrganizationAssociation | Typed relationship between Tenant and Organization | association_id, tenant_id, organization_id, type, effective interval, source | Non-authorizing |
| FAC-ENT-006 | TenantFacilityAssociation | Facility availability in a Tenant context | association_id, tenant_id, facility_id, effective interval, source | Non-authorizing; supports controlled moves |
| FAC-ENT-007 | OrganizationFacilityAssociation | Owns/leases/operates/manages/services assertion | association_id, organization_id, facility_id, type, effective interval, evidence | Non-authorizing and disputable |
| FAC-ENT-008 | BarnOperationalContext | Named operating context associated with Facility/Area | barn_context_id, facility_id, area_ids, organization_ids, label, lifecycle | Not Tenant and not durable physical identity |
| FAC-ENT-009 | Address | Structured physical/mailing address assertion | address_id, components, display_text, geocode_precision, provenance, visibility | Coordinates and sensitive details protected separately |
| FAC-ENT-010 | TopologyChangeSet | Atomic proposal/evidence for material topology mutation | change_set_id, actor, context, before, after, reason, approvals, result | Append-only evidence and idempotency key |
| FAC-ENT-011 | FacilityAlias | Historical/external name or identifier | alias_id, facility_id, value, type, source, effective interval | Not a new Facility and not authority |
| FAC-ENT-012 | PublicFacilityProjection | Revocable public subset | projection_id, facility_id, fields, purpose, approved_by, published_at, revoked_at | Never source of canonical private truth |
| FAC-ENT-013 | LegacyQuarantineRecord | Unresolved imported identity/context | quarantine_id, source_locator, raw_hash, candidates, reason, disposition | Not visible as canonical topology |
| FAC-ENT-014 | OrganizationVerificationAssertion | Dated verification claim | assertion_id, organization_id, method, issuer, evidence, state, expiry, dispute | Does not create authorization |
| FAC-ENT-015 | CapacitySuitabilityAssertion | Dated operational assertion | assertion_id, target_id, type, value, unit, source, confidence, limitations | Not a guarantee of safety |

## Global provenance fields

Every entity or assertion carries stable ID, tenant/global classification, created/updated actor or service, source, observed/effective time, version, correction lineage, lifecycle state and sensitivity. `BarnOperationalContext` is expressly not a Tenant or Facility. `OrganizationVerificationAssertion` is expressly not authorization.
