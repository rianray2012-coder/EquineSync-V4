# Founder Input Questions

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
- Version: `1.0.0-candidate`
- Date: `2026-07-20`
- Status: `FOUNDER_DECISION_REQUIRED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.

## FAC-OQ-001 / FAC-FD-001

**Question:** What is the authoritative distinction among Facility, Tenant, Organization, Barn, and Business?

**Why needed:** Conflation would corrupt isolation, lineage, authority and migration decisions.

**Recommended candidate answer:** Tenant is strict application context; Facility is durable physical place; Organization is entity identity; Barn is an operational context/topology label; Business is an Organization-domain operating identity. None is automatically equivalent to another.

**Alternatives:** Treat Barn as Facility; treat Tenant as Facility/account; collapse Organization and Business.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-002 / FAC-FD-002

**Question:** Is Tenant the strict application data-isolation boundary?

**Why needed:** Cross-tenant leakage and unsafe default-primary fallbacks.

**Recommended candidate answer:** Yes. Require an explicit Tenant context for every protected record/action or a documented global classification; missing context fails closed or quarantines.

**Alternatives:** Tenant is billing only; Barn/Facility is the isolation boundary.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-003 / FAC-FD-003

**Question:** May one Organization control multiple Tenants, and under what evidence?

**Why needed:** Real structures may be blocked or blanket authority may be inferred.

**Recommended candidate answer:** Allow it only through separate typed, dated Tenant-Organization associations plus current action-specific authority; the association itself never proves control authority.

**Alternatives:** One Organization per Tenant; Organization profile automatically controls linked Tenants.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-004 / FAC-FD-004

**Question:** May one physical Facility be associated with multiple Tenants?

**Why needed:** Transitions/shared operations can be trapped or tenant isolation can fail.

**Recommended candidate answer:** Allow explicit time-bounded associations where legitimate, while maintaining separate tenant-scoped records and prohibiting cross-tenant visibility or record cascade.

**Alternatives:** Exactly one Tenant forever; share the same underlying tenant data across Tenants.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-005 / FAC-FD-005

**Question:** What Facility-Area hierarchy is controlling?

**Why needed:** False precision or inability to model real sites.

**Recommended candidate answer:** Use Facility > Area with acyclic parent-area nesting sufficient for site, campus, structure, zone, room, stall, paddock, pasture, asset or hazard; keep labels configurable.

**Alternatives:** Fixed seven-level hierarchy; flat Facility only.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-006 / FAC-FD-006

**Question:** Which Organization types are first-class?

**Why needed:** Valid operators may be excluded or semantics become ungoverned.

**Recommended candidate answer:** Support legal entity, sole proprietor, operating business, nonprofit/rescue, professional practice, service provider/vendor, governmental/educational body and other reviewed type; preserve type provenance and allow multiple non-authorizing types.

**Alternatives:** Incorporated businesses only; unrestricted free-text type only.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-007 / FAC-FD-007

**Question:** What lifecycle states apply to Facility, Tenant, and Organization?

**Why needed:** Unsafe transitions and lost lineage.

**Recommended candidate answer:** Adopt the candidate state sets in the State Transition Matrix, with closed/decommissioned identities retained and no silent reactivation.

**Alternatives:** Active/inactive only; hard deletion.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-008 / FAC-FD-008

**Question:** How are transfer, merger, split, closure, suspension, and archival controlled?

**Why needed:** Silent authority transfer and evidence corruption.

**Recommended candidate answer:** Use reviewed effective-dated change sets and lineage events; never cascade people, horses, authority, payments, agreements, private records or evidence.

**Alternatives:** Mutate identifiers in place; clone or move all dependent records.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-009 / FAC-FD-009

**Question:** How is active Tenant/Facility context selected and audited?

**Why needed:** Confused-deputy access and stale/wrong-context changes.

**Recommended candidate answer:** Require active membership, allowed associations, explicit visible user selection and per-consequential-request revalidation; record context-selection and action audit evidence.

**Alternatives:** Infer from the last visited Barn, role, payment or deep link.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-010 / FAC-FD-010

**Question:** Which topology facts may Relationships and Authorization consume?

**Why needed:** Boundary erosion, stale decisions and unauthorized mutation.

**Recommended candidate answer:** Expose stable IDs, typed topology, lifecycle, effective associations and sensitivity/status facts as versioned references; consumers cannot rewrite topology and must own their own decisions.

**Alternatives:** Expose raw Facility records broadly; let consumers repair topology.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-011 / FAC-FD-011

**Question:** Are memberships and staff assignments exclusively Relationship-domain facts?

**Why needed:** Contradictory relationship truth and accidental access.

**Recommended candidate answer:** Yes. Facility PIA may reference them for context but does not create or own membership, employment or staff relationship truth.

**Alternatives:** Facility owns staff lists as authority; duplicate facts in both domains.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-012 / FAC-FD-012

**Question:** What evidence establishes stewardship without treating payment or contact status as authority?

**Why needed:** Unauthorized control and fraud.

**Recommended candidate answer:** Use sourced relationship/delegation/ownership/lease/operating assertions plus current Authorization evaluation; payment/contact and Organization verification are supporting claims only.

**Alternatives:** Payer, listed contact or verified Organization is steward automatically.

**Gate:** `REQUIRED_BEFORE_DESIGN_APPROVAL`

**Founder input:** _not supplied_

## FAC-OQ-013 / FAC-FD-013

**Question:** How are providers, vendors, and service Organizations represented?

**Why needed:** Impersonation, duplicate identity or overbroad access.

**Recommended candidate answer:** Represent them as Organization identities with typed, dated service associations; individual professionals remain person identities representing an Organization where applicable; neither association grants record access.

**Alternatives:** Free-text contact only; every provider is a user role with blanket access.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-014 / FAC-FD-014

**Question:** What timezone, locale, and address rules apply?

**Why needed:** Operational ambiguity or privacy exposure.

**Recommended candidate answer:** Store structured postal components plus display text, IANA timezone, BCP47 locale and separately protected geolocation precision with provenance.

**Alternatives:** Free text only; precise coordinates always visible.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-015 / FAC-FD-015

**Question:** How are duplicates detected, reviewed, and merged?

**Why needed:** Wrong-site merge and irreversible loss.

**Recommended candidate answer:** Quarantine suspected duplicates, compare evidence, then merge through a reviewed reversible change set preserving aliases, provenance, dissent and rollback metadata.

**Alternatives:** Automatic fuzzy merge; delete one duplicate.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-016 / FAC-FD-016

**Question:** What Facility information is publicly discoverable versus Tenant-scoped?

**Why needed:** Location/privacy exposure or poor discovery.

**Recommended candidate answer:** Use a separate opt-in projection initially limited to public name, coarse locality, public contact channel and service summary; exclude exact layout, occupants and sensitive areas.

**Alternatives:** Publish all profile fields; no public projection.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_

## FAC-OQ-017 / FAC-FD-017

**Question:** What is the minimum first-user Facility/Tenant seed?

**Why needed:** Conflation or excessive onboarding.

**Recommended candidate answer:** Create one Tenant, one Organization record/association, one Facility and one clearly labeled unassigned Area; create no relationship, permission, ownership or payment authority merely from the seed.

**Alternatives:** Tenant and Barn only; fully prepopulate a complex hierarchy.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_

## FAC-OQ-018 / FAC-FD-018

**Question:** How are ambiguous legacy records quarantined?

**Why needed:** Cross-tenant leakage or evidence loss.

**Recommended candidate answer:** Create provenance-preserving quarantine records with candidate mappings, reason, reviewer and disposition; never assign missing records to primary/default automatically.

**Alternatives:** Guess primary Tenant/Facility; reject and discard all ambiguous data.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-019 / FAC-FD-019

**Question:** What topology behavior is allowed offline?

**Why needed:** Stale authority can corrupt canonical topology.

**Recommended candidate answer:** Permit only minimum-authorized expiring reads and context-neutral observations; no consequential topology mutation until online revalidation.

**Alternatives:** Allow offline create/move/merge; no offline access at all.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-020 / FAC-FD-020

**Question:** What happens on Tenant or Facility suspension?

**Why needed:** Safety evidence loss or unauthorized continuation.

**Recommended candidate answer:** Deny ordinary consequential access across all surfaces, preserve emergency/safety evidence capture only through a narrowly controlled path, and require online revalidation for reinstatement.

**Alternatives:** Total lockout including safety evidence; allow reads/writes unchanged.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-021 / FAC-FD-021

**Question:** What support-access model is allowed?

**Why needed:** Privacy exposure or inability to resolve incidents.

**Recommended candidate answer:** Use ticket-bound, reason-coded, time-limited, least-privilege, impersonation-free access with approval and immutable audit.

**Alternatives:** Standing superuser access; no support access.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-022 / FAC-FD-022

**Question:** What retention rules apply to topology, identity, projection, and evidence records?

**Why needed:** Unsupported legal precision or loss of evidence.

**Recommended candidate answer:** Retain identity/lineage/audit under governed evidence rules, make public projections revocable, and set field-level schedules only after legal and operational review.

**Alternatives:** One universal duration; hard-delete the entire topology.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-023 / FAC-FD-023

**Question:** What capacity and suitability assertions may a first-user Facility or Area display?

**Why needed:** Unsafe reliance or poor planning.

**Recommended candidate answer:** Treat them as dated, sourced assertions with units, confidence and limitations; never as guarantees of safety.

**Alternatives:** Static unqualified numbers; omit capacity entirely.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_

## FAC-OQ-024 / FAC-FD-024

**Question:** How is active context switching presented to users?

**Why needed:** Wrong-context changes.

**Recommended candidate answer:** Show persistent Tenant/Facility/Organization context, require confirmation for consequential actions, and never silently switch because a link was opened.

**Alternatives:** Hidden automatic context; single sticky Barn.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_

## FAC-OQ-025 / FAC-FD-025

**Question:** Which canonical API commands, events, and jobs are permitted?

**Why needed:** Contract drift or unbuildable design.

**Recommended candidate answer:** Use the candidate contracts as design interfaces only and require separate implementation authorization plus schema/security review.

**Alternatives:** Build directly from prose; defer all contracts.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-026 / FAC-FD-026

**Question:** What nonfunctional thresholds apply?

**Why needed:** False precision or untestable reliability.

**Recommended candidate answer:** Require measured isolation, accessibility, recovery, latency and scale budgets in an authorized work package; retain qualitative gates until evidence exists.

**Alternatives:** Invent numeric thresholds now; omit quality gates.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-027 / FAC-FD-027

**Question:** What closure and suspension communication is required?

**Why needed:** Stranded users or excessive access.

**Recommended candidate answer:** Notify affected context members through governed notice, show effective time/consequences, and preserve access only where separate authority requires it.

**Alternatives:** Immediate silent closure; indefinite full access.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_

## FAC-OQ-028 / FAC-FD-028

**Question:** What evidence is required before Founder design approval and later enrollment decisions?

**Why needed:** Status inflation and unreviewed doctrine.

**Recommended candidate answer:** Resolve design-gate decisions, commission fresh segregated review, verify source/traceability gaps are zero, and record separate approval and later readiness decisions.

**Alternatives:** Treat this recommendation as approval; approve from summary alone.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_
