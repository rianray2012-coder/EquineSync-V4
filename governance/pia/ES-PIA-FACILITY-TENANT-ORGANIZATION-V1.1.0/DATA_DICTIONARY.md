# Data Dictionary

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED`
- Candidate disposition before fresh review: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

| Entity ID | Entity | Purpose | Minimum fields | Boundary |
| --- | --- | --- | --- | --- |
| FAC-ENT-001 | Tenant | Strict application isolation and governance context; an individual user need not manually invent or portray it as a physical/legal entity | tenant_id, display_name, state, created_at, closed_at, version | No physical, legal, billing or authority equivalence; minimum technical context may be system-provisioned transparently |
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
| FAC-ENT-016 | OnboardingPlan | Ephemeral selection of a truthful individual-owner or structured path | plan_id, actor_id, selected_path, isolation_context_ref, requested_entities, expiry, audit_ref | Not Tenant, Facility, Organization, Barn, Business, relationship, or authority |

## Controlled domain term — Business

`Business` means an Organization-domain operating identity or classification used to represent how an Organization conducts an operation. It is not a separate Facility-domain entity, Tenant isolation boundary, physical Facility, Barn context, human identity, relationship, stewardship fact, or source of authority. Where Business attributes are required, the Organization domain owns their meaning, provenance, and lifecycle.

## Adaptive-onboarding invariant

An `OnboardingPlan` may request creation or association but creates no canonical topology or authority by itself. The individual-owner path has no required Facility, Organization, Barn, or Business. Every protected record remains Tenant-isolated.
