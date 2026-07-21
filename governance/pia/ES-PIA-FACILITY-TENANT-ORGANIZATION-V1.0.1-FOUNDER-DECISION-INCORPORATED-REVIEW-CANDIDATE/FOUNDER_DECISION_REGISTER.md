# Founder Decision Register - Facility, Tenant, and Organization PIA

**Package:** `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE`  
**Review cycle:** `ES-REV-2026-021`  
**Founder approval date:** `2026-07-21`  
**Approved disposition:** `FAC-FD-001_THROUGH_FAC-FD-018_FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`  
**Authority:** Founder design approval only  
**Implementation authority:** `false`  
**Adoption:** `false`  
**Lock:** `false`

The original questions, recommendations, alternatives, rationales, benefits, risks, and engineering impacts are preserved below. The Founder approved the recommendations as design direction. This register does not authorize implementation, adoption, lock, migration, startup, release, deployment, enrollment, or production activity.

## Audit status model

- Original recommendation: preserved verbatim from the V1.0.0 candidate matrix.
- Founder disposition: `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`.
- Incorporated consequence: controlling design direction for this successor candidate.
- Review status: fresh structured review pending at the design freeze.
- Implementation status: not authorized and not performed.

## FAC-FD-001

- **Original question:** Define Facility, Tenant, Organization, Barn, and Business.
- **Original recommendation:** Use five distinct concepts: Tenant is the application isolation and operating-context boundary; Facility is a durable physical or operational place; Organization is a durable legal, operating, administrative, or service entity; Barn is a facility subtype or an operation at a facility, not a universal synonym; Business is an Organization participating in commercial activity.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Conflation creates cross-tenant access, duplicate identity, lifecycle, and migration errors.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Use five distinct concepts: Tenant is the application isolation and operating-context boundary; Facility is a durable physical or operational place; Organization is a durable legal, operating, administrative, or service entity; Barn is a facility subtype or an operation at a facility, not a universal synonym; Business is an Organization participating in commercial activity.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-002

- **Original question:** Is Tenant the strict application data-isolation boundary?
- **Original recommendation:** Yes. Every tenant-scoped object, read, write, search projection, cache, export, job, event, and offline bundle must be bound to exactly one active tenant unless a separately governed cross-tenant workflow is explicitly authorized.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Privacy, permission, search, recovery, and current RF01 evidence all require fail-closed separation.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Yes. Every tenant-scoped object, read, write, search projection, cache, export, job, event, and offline bundle must be bound to exactly one active tenant unless a separately governed cross-tenant workflow is explicitly authorized.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-003

- **Original question:** May one organization control multiple tenants, and under what evidence?
- **Original recommendation:** Yes, through explicit, temporal Organization-Tenant control relationships with verified authority evidence; access remains separately granted per tenant and never inherits from common ownership or email domain.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Supports multi-business operations without collapsing isolation.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Yes, through explicit, temporal Organization-Tenant control relationships with verified authority evidence; access remains separately granted per tenant and never inherits from common ownership or email domain.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-004

- **Original question:** May one physical facility be associated with multiple tenants?
- **Original recommendation:** Yes, only through explicit temporal Tenant-Facility association records with purpose, scope, steward, status, and conflict rules; facility identity may be shared while tenant-private projections remain isolated.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Multiple operators may use one place, but shared place does not mean shared customer data or authority.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Yes, only through explicit temporal Tenant-Facility association records with purpose, scope, steward, status, and conflict rules; facility identity may be shared while tenant-private projections remain isolated.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-005

- **Original question:** What facility-area hierarchy is controlling?
- **Original recommendation:** Use stable Facility -> Managed Area/Parcel -> Structure -> Zone/Space -> Subspace/Fixture/Asset containment, with separately modeled adjacency, route, overlap, and shared-resource relationships. Each effective containment version has one parent; history and aliases remain resolvable.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Matches Facility canon while preventing ambiguous tree/DAG semantics.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Use stable Facility -> Managed Area/Parcel -> Structure -> Zone/Space -> Subspace/Fixture/Asset containment, with separately modeled adjacency, route, overlap, and shared-resource relationships. Each effective containment version has one parent; history and aliases remain resolvable.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-006

- **Original question:** Which organization types are first-class?
- **Original recommendation:** Use capability-oriented types: legal_entity, operating_business, service_provider_or_practice, nonprofit_or_association, public_body, and informal_operating_group. Type is multi-valued, jurisdiction-aware, evidenced, and never permission-bearing by itself.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Avoids an inflexible legal-form enum and prevents type labels from becoming authority.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Use capability-oriented types: legal_entity, operating_business, service_provider_or_practice, nonprofit_or_association, public_body, and informal_operating_group. Type is multi-valued, jurisdiction-aware, evidenced, and never permission-bearing by itself.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-007

- **Original question:** What lifecycle states apply to Facility, Tenant, and Organization?
- **Original recommendation:** Adopt explicit entity-specific state machines: Tenant DRAFT/PENDING_VERIFICATION/ACTIVE/RESTRICTED/SUSPENDED/WIND_DOWN/CLOSED/ARCHIVED; Facility DRAFT/VERIFIED/ACTIVE/PARTIALLY_RESTRICTED/SUSPENDED/CLOSED/DECOMMISSIONED/ARCHIVED; Organization DRAFT/PENDING_VERIFICATION/ACTIVE/RESTRICTED/SUSPENDED/WIND_DOWN/CLOSED/ARCHIVED.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Distinct states preserve physical truth, operating access, and organizational continuity.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Adopt explicit entity-specific state machines: Tenant DRAFT/PENDING_VERIFICATION/ACTIVE/RESTRICTED/SUSPENDED/WIND_DOWN/CLOSED/ARCHIVED; Facility DRAFT/VERIFIED/ACTIVE/PARTIALLY_RESTRICTED/SUSPENDED/CLOSED/DECOMMISSIONED/ARCHIVED; Organization DRAFT/PENDING_VERIFICATION/ACTIVE/RESTRICTED/SUSPENDED/WIND_DOWN/CLOSED/ARCHIVED.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-008

- **Original question:** How are transfer, merger, split, closure, suspension, and archival controlled?
- **Original recommendation:** Use explicit proposed -> reviewed -> approved -> effective -> reconciled events; preserve lineage and prior identifiers; prohibit automatic transfer or merge of people, relationships, horses, invoices, permissions, agreements, or evidence.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Material topology changes are not safe CRUD updates.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Use explicit proposed -> reviewed -> approved -> effective -> reconciled events; preserve lineage and prior identifiers; prohibit automatic transfer or merge of people, relationships, horses, invoices, permissions, agreements, or evidence.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-009

- **Original question:** How is active tenant/facility context selected and audited?
- **Original recommendation:** Require a visible tenant context and, when relevant, a nested facility context. Bind both identifiers plus context version into server authorization, show them persistently, audit every switch, expire stale context, and require reconfirmation for consequential cross-context actions.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Prevents confused-deputy and stale-session errors.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Require a visible tenant context and, when relevant, a nested facility context. Bind both identifiers plus context version into server authorization, show them persistently, audit every switch, expire stale context, and require reconfirmation for consequential cross-context actions.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-010

- **Original question:** Which topology facts may Relationships and Authorization consume?
- **Original recommendation:** Expose stable IDs, entity type, lifecycle availability, tenant-scoped association, containment path, public/private projection, provenance, effective time, and freshness. Consumers may reference but not rewrite Facility truth.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Supports authorization inputs without transferring domain ownership.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Expose stable IDs, entity type, lifecycle availability, tenant-scoped association, containment path, public/private projection, provenance, effective time, and freshness. Consumers may reference but not rewrite Facility truth.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-011

- **Original question:** Are memberships and staff assignments exclusively Relationship-domain facts?
- **Original recommendation:** Yes. Facility stores no authoritative membership, employment, staff, delegation, guardianship, or representation fact; it may hold references to Relationship-owned records for display and evaluation.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Role and facility association must never silently become authority.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Yes. Facility stores no authoritative membership, employment, staff, delegation, guardianship, or representation fact; it may hold references to Relationship-owned records for display and evaluation.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-012

- **Original question:** What evidence establishes stewardship without treating payment/contact status as authority?
- **Original recommendation:** Require an explicit stewardship assertion with subject, scope, source type, source reference, claimant, verifier, effective period, confidence, dispute state, and review outcome. Payment, possession, contact, profile, lease, or role is corroborating evidence only.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Preserves the distinction among custody, stewardship, ownership, and permission.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Require an explicit stewardship assertion with subject, scope, source type, source reference, claimant, verifier, effective period, confidence, dispute state, and review outcome. Payment, possession, contact, profile, lease, or role is corroborating evidence only.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-013

- **Original question:** How are providers, vendors, and service organizations represented?
- **Original recommendation:** Represent each real entity as an Organization Identity with provider/service capabilities; connect it to tenants and facilities through Relationship- and Agreement-owned temporal records; retain accountable human actors for consequential actions.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Avoids treating vendor profile, contract, or payment row as organizational authority.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Represent each real entity as an Organization Identity with provider/service capabilities; connect it to tenants and facilities through Relationship- and Agreement-owned temporal records; retain accountable human actors for consequential actions.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-014

- **Original question:** What timezone, locale, and address rules apply?
- **Original recommendation:** Use IANA timezone IDs, BCP 47 locale tags, structured postal-address components plus country/jurisdiction, and separate geocode precision/confidence/source. Preserve historical versions; never require precise address in a public projection.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Schedules, notices, privacy, and physical identity require explicit time and location semantics.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Use IANA timezone IDs, BCP 47 locale tags, structured postal-address components plus country/jurisdiction, and separate geocode precision/confidence/source. Preserve historical versions; never require precise address in a public projection.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-015

- **Original question:** How are duplicates detected, reviewed, and merged?
- **Original recommendation:** Create duplicate candidates using name/address/geometry/external-ID/topology signals, but prohibit automatic merge. A governed merge requires human review, tenant-impact analysis, lineage, conflict register, downstream reconciliation, and a feasible reversal plan.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Same address or similar name is not identity.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Create duplicate candidates using name/address/geometry/external-ID/topology signals, but prohibit automatic merge. A governed merge requires human review, tenant-impact analysis, lineage, conflict register, downstream reconciliation, and a feasible reversal plan.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-016

- **Original question:** What is publicly discoverable versus tenant-scoped?
- **Original recommendation:** Private by default. Publish only a separate, field-specific, revocable public projection authorized by a competent actor, with generalized location where needed, anti-enumeration controls, no private topology, and no minor or security-sensitive data.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Public search must not turn tenant records into a directory or expose sensitive place data.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Private by default. Publish only a separate, field-specific, revocable public projection authorized by a competent actor, with generalized location where needed, anti-enumeration controls, no private topology, and no minor or security-sensitive data.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-017

- **Original question:** What is the minimum first-user Facility/Tenant seed?
- **Original recommendation:** Create one Tenant operating context. Create a DRAFT Facility only when the user is establishing a physical operation; create an Organization only when a real organization is asserted. Seeding creates no membership or permission beyond separately approved onboarding controls.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Avoids fabricating a legal organization for individual owners while supporting facility operators.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Create one Tenant operating context. Create a DRAFT Facility only when the user is establishing a physical operation; create an Organization only when a real organization is asserted. Seeding creates no membership or permission beyond separately approved onboarding controls. Mandatory Founder refinement: onboarding is adaptive and role-sensitive; an individual horse owner may use a horse-first flow without creating a Facility or Organization unless a real relationship is asserted or needed.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## FAC-FD-018

- **Original question:** How are ambiguous legacy records quarantined?
- **Original recommendation:** Import ambiguous rows into a tenant-scoped quarantine with source snapshot, candidates, confidence, conflicts, reviewer, and no authority-bearing or public projection. Promote only through reviewed reconciliation; never guess tenant, organization, facility, or permission.
- **Original alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.
- **Original rationale:** Legacy convergence must preserve uncertainty and fail closed.
- **Original benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.
- **Original risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.
- **Original security/privacy/safeguarding impact:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.
- **Original operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.
- **Original engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.
- **Original migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.
- **Original first-user impact:** Must be resolved before the applicable first-user or design gate.
- **Original consequence of deferral:** Candidate package remains non-approved and cannot authorize implementation.
- **Founder disposition:** `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`
- **Approval date:** `2026-07-21`
- **Authority:** Founder design approval
- **Incorporated design consequence:** Import ambiguous rows into a tenant-scoped quarantine with source snapshot, candidates, confidence, conflicts, reviewer, and no authority-bearing or public projection. Promote only through reviewed reconciliation; never guess tenant, organization, facility, or permission.
- **Remaining review status:** `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_PERMISSION_CONTROL`
- **Implementation authorization status:** `FALSE_NOT_AUTHORIZED`
- **Adoption/lock status:** `NOT_ADOPTED_NOT_LOCKED`

## Mandatory FAC-FD-017 refinement

The Founder additionally approved: onboarding must remain adaptive. Individual horse owners must not be forced to create unnecessary Facility or Organization entities merely because the architecture supports those entities. `FAC_FD_017_ADAPTIVE_ONBOARDING_SPECIFICATION.md` is the controlling incorporated design elaboration for this candidate.

## Reserved authority

Only a later explicit Founder disposition may adopt or lock this package or authorize implementation. The current successor Identity and Relationships text remains segregated, is not incorporated as approved authority, and is not represented as Founder-approved.
