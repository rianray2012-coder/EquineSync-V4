# Facility, Tenant, and Organization PIA

**Package:** `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE`  
**Version:** `1.0.1`  
**Review cycle:** `ES-REV-2026-021`  
**Authority disposition:** `FAC-FD-001_THROUGH_FAC-FD-018_FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`  
**Implementation authority:** `false`  
**Adopted:** `false`  
**Locked:** `false`

## 1. Purpose and scope

This successor candidate incorporates Founder-approved design direction for `FAC-FD-001` through `FAC-FD-018`, including the mandatory adaptive-onboarding refinement to `FAC-FD-017`. It is a documentary design package. It does not authorize or perform application, database, migration, schema, startup, release, deployment, enrollment, or production work.

## 2. Controlling concepts

- **Tenant** is the strict application data-isolation and active operating-context boundary.
- **Facility** is a durable physical or operational place. A shared physical Facility does not collapse Tenant isolation.
- **Organization** is a durable legal, operating, administrative, or service entity.
- **Barn** is a Facility subtype or an operation at a Facility, not a universal synonym for Facility, Tenant, or Organization.
- **Business** is an Organization participating in commercial activity; the label does not grant authority.

Topology, relationships, memberships, stewardship, and permission are separate facts with separate owning domains. Common ownership, email domain, address, payment, contact, role label, or onboarding sequence never grants access.

## 3. Isolation and association

Every tenant-scoped object, read, write, search projection, cache, export, job, event, and offline bundle belongs to exactly one active Tenant unless a separately governed cross-tenant workflow is explicitly authorized. One Organization may control multiple Tenants only through explicit, temporal, verified Organization-Tenant control evidence; access is separately granted per Tenant. One physical Facility may serve multiple Tenants through explicit temporal Tenant-Facility association records while private projections remain isolated.

## 4. Facility topology

The containment hierarchy is Facility -> Managed Area/Parcel -> Structure -> Zone/Space -> Subspace/Fixture/Asset. Each effective containment version has one parent. Adjacency, routes, overlaps, and shared-resource relationships are modeled separately. Stable identifiers, aliases, provenance, effective time, and prior references remain resolvable through change.

## 5. Organization model

Organization types are capability-oriented and multi-valued: `legal_entity`, `operating_business`, `service_provider_or_practice`, `nonprofit_or_association`, `public_body`, and `informal_operating_group`. Types are jurisdiction-aware and evidenced but never permission-bearing. Providers and vendors are Organizations connected through temporal Relationship- and Agreement-owned records with explicit governed capabilities and accountable human actors.

## 6. Lifecycle and material change

Tenant states are DRAFT, PENDING_VERIFICATION, ACTIVE, RESTRICTED, SUSPENDED, WIND_DOWN, CLOSED, and ARCHIVED. Facility states are DRAFT, VERIFIED, ACTIVE, PARTIALLY_RESTRICTED, SUSPENDED, CLOSED, DECOMMISSIONED, and ARCHIVED. Organization states are DRAFT, PENDING_VERIFICATION, ACTIVE, RESTRICTED, SUSPENDED, WIND_DOWN, CLOSED, and ARCHIVED.

Transfer, merger, split, closure, suspension, and archival use proposed -> reviewed -> approved -> effective -> reconciled events. Lineage and prior identifiers remain. People, relationships, horses, invoices, permissions, agreements, and evidence never transfer or merge automatically.

## 7. Active context and authorization inputs

Tenant context is visible; Facility context is nested only when relevant. Server authorization binds principal, Tenant, optional Facility, context version, permission version, and resource scope. Context switches are audited. Stale context expires. Consequential cross-context actions require confirmation. Relationships and Authorization may consume only stable topology facts: stable IDs, type, lifecycle availability, tenant-scoped association, containment path, projection classification, provenance, effective time, and freshness. Consumers may not rewrite Facility truth.

## 8. Relationships, stewardship, and permission

Membership, employment, staff assignment, representation, delegation, and guardianship are Relationship-domain facts. Stewardship requires an explicit assertion with subject, scope, source, claimant, verifier, effective period, confidence, dispute state, and outcome. Payment, possession, contact, profile, lease, or role is corroboration only. Permission remains owned by the Permission domain and consumes referenced current facts; no Facility artifact grants permission.

## 9. Adaptive onboarding

Onboarding is role-sensitive and purpose-driven. An unaffiliated individual horse owner may establish the minimum Tenant operating context needed for isolation and add a horse without creating a Facility or Organization. Facility and Organization steps appear only when an immediate real-world assertion or purpose requires them. Later associations are explicit, temporal, reviewable, and reversible. Tenant creation or assignment implies no legal Organization, Business, Facility, Barn, provider, membership, stewardship, or access. Default seed records are minimal, justified, reversible, and non-authority-bearing.

Supported contexts include unaffiliated individual owner; owner associated with a barn; independent trainer; trainer operating within a Facility; Facility operator; multi-Facility Organization; provider/vendor Organization; and multiple Tenants at one physical Facility. Detailed rules are in `FAC_FD_017_ADAPTIVE_ONBOARDING_SPECIFICATION.md`.

## 10. Privacy and public projection

Facility, Organization, Tenant, people, horses, and precise location are private and non-discoverable by default. Public discovery uses a separate field-specific, revocable projection authorized by a competent actor. Location is generalized where necessary. Private topology, minors, horse location, security systems, hazards, and emergency resources are excluded unless separately governed. Search and error behavior are anti-enumerating.

## 11. Standards and evidence

Timezone uses IANA identifiers; locale uses BCP 47 tags; address uses structured jurisdiction-aware components; geocode precision, confidence, source, and effective time are separate. Historical versions remain. Every material topology and lifecycle fact carries provenance, responsible actor, effective time, and verification state.

## 12. Duplicate and legacy controls

Duplicate candidates may use name, address, geometry, external ID, and topology signals. No merge is automatic. Human review, Tenant-impact analysis, conflict records, lineage, downstream reconciliation, and feasible reversal are required. Ambiguous legacy rows remain tenant-scoped, private, non-authority-bearing, attributable, and quarantined until reviewed reconciliation; the design never guesses Tenant, Organization, Facility, or permission.

## 13. Requirements, acceptance, and tests

The complete normative population is registered in `REQUIREMENT_REGISTER.csv`. Acceptance criteria are in `ACCEPTANCE_CRITERIA.csv`; positive, negative, and boundary design tests are in `TEST_MATRIX.csv`. The decision-to-design-to-requirement-to-test-to-risk-to-review chain is in `FOUNDER_DECISION_TRACEABILITY_MATRIX.csv` and `STRUCTURED_REVIEW_TRACEABILITY_MATRIX.csv` after review.

## 14. Source and segregation boundary

Exact adopted sources remain traceable and unmodified. Mandatory exact-source gaps remain zero at incorporation intake. The current successor Identity and Relationships text is a separate pending review dependency and is not Founder-approved authority for this package. This PIA references locked canons and does not alter or close unrelated findings.

## 15. Authority boundary

Founder design approval of `FAC-FD-001` through `FAC-FD-018` is recorded. The package remains a review candidate, not adopted or locked. Implementation authority is false. The next permitted gate after a qualifying structured review is Founder adoption review; no later gate is implied.
