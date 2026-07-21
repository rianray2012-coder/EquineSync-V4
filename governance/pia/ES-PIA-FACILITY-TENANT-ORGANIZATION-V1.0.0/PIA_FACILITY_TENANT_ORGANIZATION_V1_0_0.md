# Facility, Tenant, and Organizational Structure PIA

**Package ID:** `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`  
**Portfolio position:** `02`  
**Version:** `1.0.0`  
**PIA Standard:** `ES-PIA-MASTER-STANDARD-V1.1`  
**Task A base commit:** `b8f34aef390c5fec6f942a6253edf6acc9488c44`  
**Disposition:** `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_PENDING_FOUNDER_DECISIONS_AND_STRUCTURED_REVIEW`  
**Founder approval:** `FALSE`  
**Implementation authority:** `FALSE`  
**Execution authority:** `FALSE`

## 1. Executive purpose

This candidate PIA defines the design boundary for Facility, Tenant, Organization, facility topology, lifecycle, active context, and topology change. It is decision-ready, testable, and traceable, but it is not approved doctrine and authorizes no code, schema, migration, startup, enrollment, deployment, or production activity.

## 2. Scope and ownership

The PIA owns durable Facility identity and profile; facility areas and topology; Tenant identity as the candidate application isolation and operating-context boundary; Organization identity and lifecycle; explicit Organization-Tenant and Tenant-Facility topology; multi-facility and multi-organization context; lifecycle transitions; context selection and audit; identifiers; duplicate candidates; and ambiguous legacy quarantine.

It does not own people, accounts, credentials, authentication, memberships, employment, staff assignments, representation, delegation, guardianship, permission decisions, horse identity, care, scheduling, lessons, billing, or owner communications. Those domains may consume stable topology references but cannot rewrite Facility truth.

## 3. Definitions under Founder decision

The candidate definitions are the recommendation in `FAC-FD-001`: Tenant is an isolation/operating context; Facility is a place; Organization is a non-person entity; Barn is a Facility subtype or operating label; Business is a commercially active Organization. They remain `FOUNDER_DECISION_REQUIRED`.

## 4. Governing invariants

1. Shared facility, staff, address, email domain, owner, payment, lease, profile, role, or contact never creates cross-tenant access or permission.
2. Every current action has a visible, authoritative Tenant context and, where relevant, Facility context.
3. Memberships and staff assignments are Relationship facts; authorization is a Permission fact.
4. Facility, Organization, and Tenant lifecycle changes preserve stable identity, effective time, provenance, evidence, and prior state.
5. Transfer, merge, split, suspension, closure, and archive never cascade into unrelated people, horses, relationships, agreements, invoices, permissions, or evidence.
6. Public discovery is a separate minimal projection and private by default.
7. Ambiguous legacy facts remain quarantined and non-authority-bearing.
8. Offline, search, background, support, API, export, integration, and recovery paths enforce the same isolation boundary.

## 5. Canon inheritance and conflicts

Facility canon owns physical truth. Barn Lifecycle owns operational use. Business Lifecycle owns commercial and organizational lifecycle. Identity owns people/accounts/actors. Relationship owns memberships and representation. Permission owns access decisions. Agreement owns contractual authorization. Privacy owns personal-information use and exposure. Audit and Stewardship own evidence and historical truth. Search owns discovery. Horse and Financial domains retain their own truth.

Several adopted substantive files retain historical candidate labels in their body. Their separate adoption and lock records control lifecycle; the source bytes were not edited. The later Governance V1.0 lock certificate controls over stale historical prose in the Canon Index.

## 6. Candidate entity model

The design uses Tenant, Facility, Organization, FacilityArea, TopologyEdge, OrganizationTenantControl, TenantFacilityAssociation, FacilityStewardshipAssertion, ActiveContext, ContextSwitchEvent, FacilityPublicProjection, DuplicateCandidate, TopologyChange, LegacyQuarantineRecord, AddressVersion, ExternalIdentifier, LifecycleEvidence, and ReconciliationCase. `DATA_DICTIONARY.md` records ownership, identifiers, scope, lifecycle, and public exposure.

## 7. Tenant isolation and context

Every tenant-scoped object and operation carries an authoritative tenant identifier. Object lookup occurs only after tenant authorization. Cross-tenant workflows require a separately named contract, purpose, authority, minimum-necessary projection, audit, and test suite. The active context is selected through an eligible Relationship and Permission decision, bound to session/context versions, continuously visible, and audited on every switch. Stale or revoked context fails closed.

## 8. Facility topology

Containment uses stable effective versions from Facility to managed area, structure, zone/space, and subspace/fixture/asset. Adjacency, routes, overlap, and shared resources are separate edge types. One contained object has one effective containment parent while non-containment edges may form a graph. Names and addresses are attributes; they are not identity.

## 9. Organization and operating topology

An Organization may control multiple Tenants only through explicit temporal evidence. A Facility may be associated with multiple Tenants only through explicit Tenant-Facility records whose private projections remain isolated. Provider and vendor Organizations act through Relationship- and Agreement-owned links and accountable human actors.

## 10. Lifecycle and material change

Entity-specific state machines appear in `STATE_TRANSITION_MATRIX.csv`. Material changes follow proposed, reviewed, approved, effective, reconciling, and complete stages. Suspension propagates to current access, offline bundles, search, exports, jobs, support, and integrations. Closure ends ordinary use but does not erase history. Restoration re-evaluates current authority and cannot resurrect stale access.

## 11. Permission and authorization boundary

Facility data supplies current topology facts, never permission. A facility association, Organization link, stewardship assertion, agreement, role, lease, payment, or contact can be an input or evidence but cannot independently grant access. `PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv` assigns each action to its owning domain and lists forbidden inference.

## 12. Privacy, security, and safeguarding

Precise address, horse or person location, minor-associated areas, security systems, cameras, access points, hazards, and emergency resources are sensitive. Public discovery requires a separate, minimal, field-specific, revocable projection with generalized location and anti-enumeration controls. Minor-related place and schedule information is never public. Support access is narrow, attributable, time-bound, and auditable.

## 13. Offline, degraded, and recovery behavior

Offline bundles record Tenant, Facility, subject, scope, permission/context version, issue time, expiry, and revocation state. Stale data may support bounded read continuity but cannot authorize consequential mutation. Suspension and revocation propagate at the earliest synchronization. Restore and replay reconcile current lifecycle, permission, tenant, merge, and deletion state before access resumes.

## 14. Data, API, events, jobs, and integrations

All contracts are provider-neutral and carry tenant, entity, version, effective time, provenance, actor chain, purpose, and idempotency where material. Jobs are tenant-partitioned and suspendable. Derived indexes and caches are invalidated on lifecycle and visibility changes. External IDs never replace canonical IDs.

## 15. Search and discovery

Private-by-default search is tenant-scoped and permission-filtered before result display. Error messages, counts, timing, autocomplete, exports, and indexes cannot reveal cross-tenant existence. Public discovery uses only the approved public projection. Stale results do not restore access or establish truth.

## 16. Duplicate, transfer, merge, and split

Similarity creates a candidate, not a merge. Human review examines identity, topology, tenant impact, history, conflicting evidence, and downstream dependencies. A merge preserves retired IDs, aliases, lineage, evidence, audit, conflict disposition, and feasible reversal. Organization or Facility change never merges unrelated domain data.

## 17. Legacy and migration boundary

Legacy `barn`, `barns`, `users.barn_id`, account membership mirrors, and primary fallback are current-state evidence only. Ambiguous rows enter quarantine. This package specifies no migration steps and grants no database authority. A future migration plan must be separately authorized and must include access-delta, unrelated-user, rollback, idempotency, and reconciliation evidence.

## 18. First-user relevance

The recommended candidate seed is one Tenant operating context, a DRAFT Facility only when a physical operation is being established, and an Organization only when a real entity is asserted. Seeding creates no membership or permission. `FAC-FD-017` remains open and blocks first-user enrollment for this domain.

## 19. Requirements, acceptance, and tests

Forty candidate requirements map one-to-one to acceptance criteria and test specifications. Documentary validation demonstrates completeness and consistency only. No executable product test, migration, database action, application startup, or customer-data operation occurred.

## 20. Risks and deviations

No P0 finding is open. Three P1 findings remain: the Founder decision set, the as-built model gap, and absence of executed offline/suspension evidence. P2 findings cover segregated successor dependency, public discovery, taxonomy/address choices, shared-facility projections, and reconciliation breadth. See `RISK_FINDING_DEVIATION_REGISTER.csv`.

## 21. Founder decisions and approval gate

All 18 seeded decisions remain open with one recommendation, alternatives, rationale, impacts, deferral consequence, and proposed disposition language. Recommendations are candidate treatments only. The next action is a Founder decision review of `FOUNDER_DECISION_REGISTER.md` and `FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv`, followed by the required fresh structured review—not implementation.

## 22. Explicit non-goals

No code, schema, migration, database, application startup, provider activation, enrollment, PR, merge, tag, release, deployment, production use, or public claim is authorized. The ongoing fresh Identity and Relationships review is not modified, incorporated, or represented as approved.

## 23. Disposition

`FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_PENDING_FOUNDER_DECISIONS_AND_STRUCTURED_REVIEW`
