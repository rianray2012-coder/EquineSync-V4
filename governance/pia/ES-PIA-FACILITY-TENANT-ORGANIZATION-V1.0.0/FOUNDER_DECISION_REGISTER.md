# Founder Decision Register

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
- Version: `1.0.0-candidate`
- Date: `2026-07-20`
- Status: `FOUNDER_DECISION_REQUIRED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.

## FAC-FD-001 — What is the authoritative distinction among Facility, Tenant, Organization, Barn, and Business?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Tenant is strict application context; Facility is durable physical place; Organization is entity identity; Barn is an operational context/topology label; Business is an Organization-domain operating identity. None is automatically equivalent to another.
- Alternatives: Treat Barn as Facility; treat Tenant as Facility/account; collapse Organization and Business.
- Risk if unresolved: Conflation would corrupt isolation, lineage, authority and migration decisions.
- Founder answer: _not supplied_

## FAC-FD-002 — Is Tenant the strict application data-isolation boundary?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Yes. Require an explicit Tenant context for every protected record/action or a documented global classification; missing context fails closed or quarantines.
- Alternatives: Tenant is billing only; Barn/Facility is the isolation boundary.
- Risk if unresolved: Cross-tenant leakage and unsafe default-primary fallbacks.
- Founder answer: _not supplied_

## FAC-FD-003 — May one Organization control multiple Tenants, and under what evidence?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Allow it only through separate typed, dated Tenant-Organization associations plus current action-specific authority; the association itself never proves control authority.
- Alternatives: One Organization per Tenant; Organization profile automatically controls linked Tenants.
- Risk if unresolved: Real structures may be blocked or blanket authority may be inferred.
- Founder answer: _not supplied_

## FAC-FD-004 — May one physical Facility be associated with multiple Tenants?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Allow explicit time-bounded associations where legitimate, while maintaining separate tenant-scoped records and prohibiting cross-tenant visibility or record cascade.
- Alternatives: Exactly one Tenant forever; share the same underlying tenant data across Tenants.
- Risk if unresolved: Transitions/shared operations can be trapped or tenant isolation can fail.
- Founder answer: _not supplied_

## FAC-FD-005 — What Facility-Area hierarchy is controlling?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Use Facility > Area with acyclic parent-area nesting sufficient for site, campus, structure, zone, room, stall, paddock, pasture, asset or hazard; keep labels configurable.
- Alternatives: Fixed seven-level hierarchy; flat Facility only.
- Risk if unresolved: False precision or inability to model real sites.
- Founder answer: _not supplied_

## FAC-FD-006 — Which Organization types are first-class?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Support legal entity, sole proprietor, operating business, nonprofit/rescue, professional practice, service provider/vendor, governmental/educational body and other reviewed type; preserve type provenance and allow multiple non-authorizing types.
- Alternatives: Incorporated businesses only; unrestricted free-text type only.
- Risk if unresolved: Valid operators may be excluded or semantics become ungoverned.
- Founder answer: _not supplied_

## FAC-FD-007 — What lifecycle states apply to Facility, Tenant, and Organization?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Adopt the candidate state sets in the State Transition Matrix, with closed/decommissioned identities retained and no silent reactivation.
- Alternatives: Active/inactive only; hard deletion.
- Risk if unresolved: Unsafe transitions and lost lineage.
- Founder answer: _not supplied_

## FAC-FD-008 — How are transfer, merger, split, closure, suspension, and archival controlled?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Use reviewed effective-dated change sets and lineage events; never cascade people, horses, authority, payments, agreements, private records or evidence.
- Alternatives: Mutate identifiers in place; clone or move all dependent records.
- Risk if unresolved: Silent authority transfer and evidence corruption.
- Founder answer: _not supplied_

## FAC-FD-009 — How is active Tenant/Facility context selected and audited?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Require active membership, allowed associations, explicit visible user selection and per-consequential-request revalidation; record context-selection and action audit evidence.
- Alternatives: Infer from the last visited Barn, role, payment or deep link.
- Risk if unresolved: Confused-deputy access and stale/wrong-context changes.
- Founder answer: _not supplied_

## FAC-FD-010 — Which topology facts may Relationships and Authorization consume?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Expose stable IDs, typed topology, lifecycle, effective associations and sensitivity/status facts as versioned references; consumers cannot rewrite topology and must own their own decisions.
- Alternatives: Expose raw Facility records broadly; let consumers repair topology.
- Risk if unresolved: Boundary erosion, stale decisions and unauthorized mutation.
- Founder answer: _not supplied_

## FAC-FD-011 — Are memberships and staff assignments exclusively Relationship-domain facts?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Yes. Facility PIA may reference them for context but does not create or own membership, employment or staff relationship truth.
- Alternatives: Facility owns staff lists as authority; duplicate facts in both domains.
- Risk if unresolved: Contradictory relationship truth and accidental access.
- Founder answer: _not supplied_

## FAC-FD-012 — What evidence establishes stewardship without treating payment or contact status as authority?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_DESIGN_APPROVAL`
- Recommended candidate answer: Use sourced relationship/delegation/ownership/lease/operating assertions plus current Authorization evaluation; payment/contact and Organization verification are supporting claims only.
- Alternatives: Payer, listed contact or verified Organization is steward automatically.
- Risk if unresolved: Unauthorized control and fraud.
- Founder answer: _not supplied_

## FAC-FD-013 — How are providers, vendors, and service Organizations represented?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Represent them as Organization identities with typed, dated service associations; individual professionals remain person identities representing an Organization where applicable; neither association grants record access.
- Alternatives: Free-text contact only; every provider is a user role with blanket access.
- Risk if unresolved: Impersonation, duplicate identity or overbroad access.
- Founder answer: _not supplied_

## FAC-FD-014 — What timezone, locale, and address rules apply?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Store structured postal components plus display text, IANA timezone, BCP47 locale and separately protected geolocation precision with provenance.
- Alternatives: Free text only; precise coordinates always visible.
- Risk if unresolved: Operational ambiguity or privacy exposure.
- Founder answer: _not supplied_

## FAC-FD-015 — How are duplicates detected, reviewed, and merged?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Quarantine suspected duplicates, compare evidence, then merge through a reviewed reversible change set preserving aliases, provenance, dissent and rollback metadata.
- Alternatives: Automatic fuzzy merge; delete one duplicate.
- Risk if unresolved: Wrong-site merge and irreversible loss.
- Founder answer: _not supplied_

## FAC-FD-016 — What Facility information is publicly discoverable versus Tenant-scoped?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Recommended candidate answer: Use a separate opt-in projection initially limited to public name, coarse locality, public contact channel and service summary; exclude exact layout, occupants and sensitive areas.
- Alternatives: Publish all profile fields; no public projection.
- Risk if unresolved: Location/privacy exposure or poor discovery.
- Founder answer: _not supplied_

## FAC-FD-017 — What is the minimum first-user Facility/Tenant seed?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Recommended candidate answer: Create one Tenant, one Organization record/association, one Facility and one clearly labeled unassigned Area; create no relationship, permission, ownership or payment authority merely from the seed.
- Alternatives: Tenant and Barn only; fully prepopulate a complex hierarchy.
- Risk if unresolved: Conflation or excessive onboarding.
- Founder answer: _not supplied_

## FAC-FD-018 — How are ambiguous legacy records quarantined?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Create provenance-preserving quarantine records with candidate mappings, reason, reviewer and disposition; never assign missing records to primary/default automatically.
- Alternatives: Guess primary Tenant/Facility; reject and discard all ambiguous data.
- Risk if unresolved: Cross-tenant leakage or evidence loss.
- Founder answer: _not supplied_

## FAC-FD-019 — What topology behavior is allowed offline?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Permit only minimum-authorized expiring reads and context-neutral observations; no consequential topology mutation until online revalidation.
- Alternatives: Allow offline create/move/merge; no offline access at all.
- Risk if unresolved: Stale authority can corrupt canonical topology.
- Founder answer: _not supplied_

## FAC-FD-020 — What happens on Tenant or Facility suspension?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Deny ordinary consequential access across all surfaces, preserve emergency/safety evidence capture only through a narrowly controlled path, and require online revalidation for reinstatement.
- Alternatives: Total lockout including safety evidence; allow reads/writes unchanged.
- Risk if unresolved: Safety evidence loss or unauthorized continuation.
- Founder answer: _not supplied_

## FAC-FD-021 — What support-access model is allowed?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Use ticket-bound, reason-coded, time-limited, least-privilege, impersonation-free access with approval and immutable audit.
- Alternatives: Standing superuser access; no support access.
- Risk if unresolved: Privacy exposure or inability to resolve incidents.
- Founder answer: _not supplied_

## FAC-FD-022 — What retention rules apply to topology, identity, projection, and evidence records?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Retain identity/lineage/audit under governed evidence rules, make public projections revocable, and set field-level schedules only after legal and operational review.
- Alternatives: One universal duration; hard-delete the entire topology.
- Risk if unresolved: Unsupported legal precision or loss of evidence.
- Founder answer: _not supplied_

## FAC-FD-023 — What capacity and suitability assertions may a first-user Facility or Area display?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Recommended candidate answer: Treat them as dated, sourced assertions with units, confidence and limitations; never as guarantees of safety.
- Alternatives: Static unqualified numbers; omit capacity entirely.
- Risk if unresolved: Unsafe reliance or poor planning.
- Founder answer: _not supplied_

## FAC-FD-024 — How is active context switching presented to users?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Recommended candidate answer: Show persistent Tenant/Facility/Organization context, require confirmation for consequential actions, and never silently switch because a link was opened.
- Alternatives: Hidden automatic context; single sticky Barn.
- Risk if unresolved: Wrong-context changes.
- Founder answer: _not supplied_

## FAC-FD-025 — Which canonical API commands, events, and jobs are permitted?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Use the candidate contracts as design interfaces only and require separate implementation authorization plus schema/security review.
- Alternatives: Build directly from prose; defer all contracts.
- Risk if unresolved: Contract drift or unbuildable design.
- Founder answer: _not supplied_

## FAC-FD-026 — What nonfunctional thresholds apply?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Recommended candidate answer: Require measured isolation, accessibility, recovery, latency and scale budgets in an authorized work package; retain qualitative gates until evidence exists.
- Alternatives: Invent numeric thresholds now; omit quality gates.
- Risk if unresolved: False precision or untestable reliability.
- Founder answer: _not supplied_

## FAC-FD-027 — What closure and suspension communication is required?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Recommended candidate answer: Notify affected context members through governed notice, show effective time/consequences, and preserve access only where separate authority requires it.
- Alternatives: Immediate silent closure; indefinite full access.
- Risk if unresolved: Stranded users or excessive access.
- Founder answer: _not supplied_

## FAC-FD-028 — What evidence is required before Founder design approval and later enrollment decisions?

- Status: `FOUNDER_DECISION_REQUIRED`
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Recommended candidate answer: Resolve design-gate decisions, commission fresh segregated review, verify source/traceability gaps are zero, and record separate approval and later readiness decisions.
- Alternatives: Treat this recommendation as approval; approve from summary alone.
- Risk if unresolved: Status inflation and unreviewed doctrine.
- Founder answer: _not supplied_
