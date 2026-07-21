# Founder Decision Register

All recommendations are non-approved candidate treatments. No silence, delay, or continued drafting counts as a decision.

## FAC-FD-001

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** Define Facility, Tenant, Organization, Barn, and Business.  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Use five distinct concepts: Tenant is the application isolation and operating-context boundary; Facility is a durable physical or operational place; Organization is a durable legal, operating, administrative, or service entity; Barn is a facility subtype or an operation at a facility, not a universal synonym; Business is an Organization participating in commercial activity.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Conflation creates cross-tenant access, duplicate identity, lifecycle, and migration errors.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-001 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-002

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** Is Tenant the strict application data-isolation boundary?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Yes. Every tenant-scoped object, read, write, search projection, cache, export, job, event, and offline bundle must be bound to exactly one active tenant unless a separately governed cross-tenant workflow is explicitly authorized.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Privacy, permission, search, recovery, and current RF01 evidence all require fail-closed separation.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-002 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-003

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** May one organization control multiple tenants, and under what evidence?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Yes, through explicit, temporal Organization-Tenant control relationships with verified authority evidence; access remains separately granted per tenant and never inherits from common ownership or email domain.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Supports multi-business operations without collapsing isolation.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-003 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-004

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** May one physical facility be associated with multiple tenants?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Yes, only through explicit temporal Tenant-Facility association records with purpose, scope, steward, status, and conflict rules; facility identity may be shared while tenant-private projections remain isolated.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Multiple operators may use one place, but shared place does not mean shared customer data or authority.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-004 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-005

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** What facility-area hierarchy is controlling?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Use stable Facility -> Managed Area/Parcel -> Structure -> Zone/Space -> Subspace/Fixture/Asset containment, with separately modeled adjacency, route, overlap, and shared-resource relationships. Each effective containment version has one parent; history and aliases remain resolvable.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Matches Facility canon while preventing ambiguous tree/DAG semantics.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-005 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-006

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** Which organization types are first-class?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Use capability-oriented types: legal_entity, operating_business, service_provider_or_practice, nonprofit_or_association, public_body, and informal_operating_group. Type is multi-valued, jurisdiction-aware, evidenced, and never permission-bearing by itself.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Avoids an inflexible legal-form enum and prevents type labels from becoming authority.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-006 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-007

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** What lifecycle states apply to Facility, Tenant, and Organization?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Adopt explicit entity-specific state machines: Tenant DRAFT/PENDING_VERIFICATION/ACTIVE/RESTRICTED/SUSPENDED/WIND_DOWN/CLOSED/ARCHIVED; Facility DRAFT/VERIFIED/ACTIVE/PARTIALLY_RESTRICTED/SUSPENDED/CLOSED/DECOMMISSIONED/ARCHIVED; Organization DRAFT/PENDING_VERIFICATION/ACTIVE/RESTRICTED/SUSPENDED/WIND_DOWN/CLOSED/ARCHIVED.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Distinct states preserve physical truth, operating access, and organizational continuity.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-007 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-008

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** How are transfer, merger, split, closure, suspension, and archival controlled?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Use explicit proposed -> reviewed -> approved -> effective -> reconciled events; preserve lineage and prior identifiers; prohibit automatic transfer or merge of people, relationships, horses, invoices, permissions, agreements, or evidence.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Material topology changes are not safe CRUD updates.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-008 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-009

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** How is active tenant/facility context selected and audited?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Require a visible tenant context and, when relevant, a nested facility context. Bind both identifiers plus context version into server authorization, show them persistently, audit every switch, expire stale context, and require reconfirmation for consequential cross-context actions.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Prevents confused-deputy and stale-session errors.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-009 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-010

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** Which topology facts may Relationships and Authorization consume?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Expose stable IDs, entity type, lifecycle availability, tenant-scoped association, containment path, public/private projection, provenance, effective time, and freshness. Consumers may reference but not rewrite Facility truth.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Supports authorization inputs without transferring domain ownership.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-010 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-011

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** Are memberships and staff assignments exclusively Relationship-domain facts?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Yes. Facility stores no authoritative membership, employment, staff, delegation, guardianship, or representation fact; it may hold references to Relationship-owned records for display and evaluation.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Role and facility association must never silently become authority.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-011 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-012

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** What evidence establishes stewardship without treating payment/contact status as authority?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Require an explicit stewardship assertion with subject, scope, source type, source reference, claimant, verifier, effective period, confidence, dispute state, and review outcome. Payment, possession, contact, profile, lease, or role is corroborating evidence only.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Preserves the distinction among custody, stewardship, ownership, and permission.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-012 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-013

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** How are providers, vendors, and service organizations represented?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Represent each real entity as an Organization Identity with provider/service capabilities; connect it to tenants and facilities through Relationship- and Agreement-owned temporal records; retain accountable human actors for consequential actions.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Avoids treating vendor profile, contract, or payment row as organizational authority.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-013 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-014

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** What timezone, locale, and address rules apply?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Use IANA timezone IDs, BCP 47 locale tags, structured postal-address components plus country/jurisdiction, and separate geocode precision/confidence/source. Preserve historical versions; never require precise address in a public projection.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Schedules, notices, privacy, and physical identity require explicit time and location semantics.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-014 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-015

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** How are duplicates detected, reviewed, and merged?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Create duplicate candidates using name/address/geometry/external-ID/topology signals, but prohibit automatic merge. A governed merge requires human review, tenant-impact analysis, lineage, conflict register, downstream reconciliation, and a feasible reversal plan.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Same address or similar name is not identity.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-015 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-016

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** What is publicly discoverable versus tenant-scoped?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Private by default. Publish only a separate, field-specific, revocable public projection authorized by a competent actor, with generalized location where needed, anti-enumeration controls, no private topology, and no minor or security-sensitive data.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Public search must not turn tenant records into a directory or expose sensitive place data.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-016 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-017

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** What is the minimum first-user Facility/Tenant seed?  
**Earliest gate:** `BLOCKING_BEFORE_FIRST_USER_ENROLLMENT`  
**Recommended candidate treatment:** Create one Tenant operating context. Create a DRAFT Facility only when the user is establishing a physical operation; create an Organization only when a real organization is asserted. Seeding creates no membership or permission beyond separately approved onboarding controls.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Avoids fabricating a legal organization for individual owners while supporting facility operators.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-017 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`

## FAC-FD-018

**Status:** `FOUNDER_DECISION_REQUIRED`  
**Question:** How are ambiguous legacy records quarantined?  
**Earliest gate:** `BLOCKING_BEFORE_DESIGN_APPROVAL`  
**Recommended candidate treatment:** Import ambiguous rows into a tenant-scoped quarantine with source snapshot, candidates, confidence, conflicts, reviewer, and no authority-bearing or public projection. Promote only through reviewed reconciliation; never guess tenant, organization, facility, or permission.  
**Alternatives:** Defer; adopt a narrower single-tenant/single-facility rule; or provide Founder-specific replacement language.  
**Rationale:** Legacy convergence must preserve uncertainty and fail closed.  
**Benefits:** Clear ownership, auditable lifecycle, safer isolation, and lower migration ambiguity.  
**Risks:** The recommendation may not match Founder business preference or future operating model until expressly decided.  
**Security/privacy/safeguarding:** Material; affects isolation, discoverability, attribution, location sensitivity, or authority boundaries.  
**Operational impact:** Shapes onboarding, context switching, restructuring, support, and closure workflows.  
**Engineering impact:** Shapes identifiers, constraints, APIs, authorization inputs, jobs, indexes, and tests; no implementation is authorized.  
**Migration impact:** Requires explicit mapping and quarantine rules; no migration is authorized.  
**First-user impact:** Must be resolved before the applicable first-user or design gate.  
**Deferral:** Candidate package remains non-approved and cannot authorize implementation.  
**Candidate-only:** `TRUE`  
**Proposed Founder language:** `APPROVE FAC-FD-018 RECOMMENDED_CANDIDATE_TREATMENT AS DESIGN DIRECTION; IMPLEMENTATION AUTHORITY REMAINS FALSE`
