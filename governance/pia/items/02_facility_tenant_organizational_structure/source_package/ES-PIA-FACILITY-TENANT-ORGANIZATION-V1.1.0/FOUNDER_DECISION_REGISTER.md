# Founder Decision Register

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED`
- Candidate disposition before fresh review: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

## FAC-FD-001 — What is the authoritative distinction among Facility, Tenant, Organization, Barn, and Business?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Tenant is strict application context; Facility is durable physical place; Organization is entity identity; Barn is an operational context/topology label; Business is an Organization-domain operating identity. None is automatically equivalent to another.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-002 — Is Tenant the strict application data-isolation boundary?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Yes. Require an explicit Tenant context for every protected record/action or a documented global classification; missing context fails closed or quarantines.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-003 — May one Organization control multiple Tenants, and under what evidence?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Allow it only through separate typed, dated Tenant-Organization associations plus current action-specific authority; the association itself never proves control authority.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-004 — May one physical Facility be associated with multiple Tenants?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Allow explicit time-bounded associations where legitimate, while maintaining separate tenant-scoped records and prohibiting cross-tenant visibility or record cascade.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-005 — What Facility-Area hierarchy is controlling?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Use Facility > Area with acyclic parent-area nesting sufficient for site, campus, structure, zone, room, stall, paddock, pasture, asset or hazard; keep labels configurable.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-006 — Which Organization types are first-class?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Support legal entity, sole proprietor, operating business, nonprofit/rescue, professional practice, service provider/vendor, governmental/educational body and other reviewed type; preserve type provenance and allow multiple non-authorizing types.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-007 — What lifecycle states apply to Facility, Tenant, and Organization?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Adopt the candidate state sets in the State Transition Matrix, with closed/decommissioned identities retained and no silent reactivation.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-008 — How are transfer, merger, split, closure, suspension, and archival controlled?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Use reviewed effective-dated change sets and lineage events; never cascade people, horses, authority, payments, agreements, private records or evidence.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-009 — How is active Tenant/Facility context selected and audited?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Require active membership, allowed associations, explicit visible user selection and per-consequential-request revalidation; record context-selection and action audit evidence.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-010 — Which topology facts may Relationships and Authorization consume?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Expose stable IDs, typed topology, lifecycle, effective associations and sensitivity/status facts as versioned references; consumers cannot rewrite topology and must own their own decisions.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-011 — Are memberships and staff assignments exclusively Relationship-domain facts?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Yes. Facility PIA may reference them for context but does not create or own membership, employment or staff relationship truth.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-012 — What evidence establishes stewardship without treating payment or contact status as authority?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Use sourced relationship/delegation/ownership/lease/operating assertions plus current Authorization evaluation; payment/contact and Organization verification are supporting claims only.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-013 — How are providers, vendors, and service Organizations represented?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Represent them as Organization identities with typed, dated service associations; individual professionals remain person identities representing an Organization where applicable; neither association grants record access.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-014 — What timezone, locale, and address rules apply?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Store structured postal components plus display text, IANA timezone, BCP47 locale and separately protected geolocation precision with provenance.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-015 — How are duplicates detected, reviewed, and merged?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Quarantine suspected duplicates, compare evidence, then merge through a reviewed reversible change set preserving aliases, provenance, dissent and rollback metadata.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-016 — What Facility information is publicly discoverable versus Tenant-scoped?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Use a separate opt-in projection initially limited to public name, coarse locality, public contact channel and service summary; exclude exact layout, occupants and sensitive areas.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-017 — What is the minimum first-user Facility/Tenant seed?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `SUPERSEDED_OR_REFINED`
- Decision date: `2026-07-21`
- Approved design doctrine: Use adaptive paths. For an individual-owner or horse-first path, establish only the minimum required technical Tenant isolation context without asking the user to invent a Facility, Organization, Barn, or Business. For a real facility/organization context, create only truthful selected structures and explicit associations. Neither path creates authority or stewardship.
- Founder refinement: EquineSync onboarding must remain adaptive to the actual user and operating context. An individual horse owner must not be forced to create unnecessary Facility, Tenant, Organization, Barn, or Business entities when those entities do not truthfully exist or are not required for the user's legitimate workflow. The onboarding model must support horse-first and individual-owner-first entry paths while preserving the canonical distinctions, isolation rules, evidence requirements, and later explicit association of facilities or organizations when applicable.
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-018 — How are ambiguous legacy records quarantined?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Classification: `FOUNDER_APPROVED_DESIGN_DOCTRINE`
- Decision date: `2026-07-21`
- Approved design doctrine: Create provenance-preserving quarantine records with candidate mappings, reason, reviewer and disposition; never assign missing records to primary/default automatically.
- Founder refinement: None
- Gate: `DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY`
- Implementation authority: `FALSE`

## FAC-FD-019 — What topology behavior is allowed offline?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Classification: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Decision date: `not decided`
- Unapproved candidate recommendation: Permit only minimum-authorized expiring reads and context-neutral observations; no consequential topology mutation until online revalidation.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Implementation authority: `FALSE`

## FAC-FD-020 — What happens on Tenant or Facility suspension?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Classification: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Decision date: `not decided`
- Unapproved candidate recommendation: Deny ordinary consequential access across all surfaces, preserve emergency/safety evidence capture only through a narrowly controlled path, and require online revalidation for reinstatement.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Implementation authority: `FALSE`

## FAC-FD-021 — What support-access model is allowed?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Classification: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Decision date: `not decided`
- Unapproved candidate recommendation: Use ticket-bound, reason-coded, time-limited, least-privilege, impersonation-free access with approval and immutable audit.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Implementation authority: `FALSE`

## FAC-FD-022 — What retention rules apply to topology, identity, projection, and evidence records?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Classification: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Decision date: `not decided`
- Unapproved candidate recommendation: Retain identity/lineage/audit under governed evidence rules, make public projections revocable, and set field-level schedules only after legal and operational review.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Implementation authority: `FALSE`

## FAC-FD-023 — What capacity and suitability assertions may a first-user Facility or Area display?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_ENROLLMENT`
- Classification: `OPEN_BEFORE_ENROLLMENT`
- Decision date: `not decided`
- Unapproved candidate recommendation: Treat them as dated, sourced assertions with units, confidence and limitations; never as guarantees of safety.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Implementation authority: `FALSE`

## FAC-FD-024 — How is active context switching presented to users?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_ENROLLMENT`
- Classification: `OPEN_BEFORE_ENROLLMENT`
- Decision date: `not decided`
- Unapproved candidate recommendation: Show persistent Tenant/Facility/Organization context, require confirmation for consequential actions, and never silently switch because a link was opened.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Implementation authority: `FALSE`

## FAC-FD-025 — Which canonical API commands, events, and jobs are permitted?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Classification: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Decision date: `not decided`
- Unapproved candidate recommendation: Use the candidate contracts as design interfaces only and require separate implementation authorization plus schema/security review.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Implementation authority: `FALSE`

## FAC-FD-026 — What nonfunctional thresholds apply?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Classification: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Decision date: `not decided`
- Unapproved candidate recommendation: Require measured isolation, accessibility, recovery, latency and scale budgets in an authorized work package; retain qualitative gates until evidence exists.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`
- Implementation authority: `FALSE`

## FAC-FD-027 — What closure and suspension communication is required?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_ENROLLMENT`
- Classification: `OPEN_BEFORE_ENROLLMENT`
- Decision date: `not decided`
- Unapproved candidate recommendation: Notify affected context members through governed notice, show effective time/consequences, and preserve access only where separate authority requires it.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Implementation authority: `FALSE`

## FAC-FD-028 — What evidence is required before Founder design approval and later enrollment decisions?

- Prior status: `FOUNDER_DECISION_REQUIRED`
- Current status: `OPEN_BEFORE_ENROLLMENT`
- Classification: `OPEN_BEFORE_ENROLLMENT`
- Decision date: `not decided`
- Unapproved candidate recommendation: Resolve design-gate decisions, commission fresh segregated review, verify source/traceability gaps are zero, and record separate approval and later readiness decisions.
- Founder refinement: None
- Gate: `REQUIRED_BEFORE_ENROLLMENT`
- Implementation authority: `FALSE`
