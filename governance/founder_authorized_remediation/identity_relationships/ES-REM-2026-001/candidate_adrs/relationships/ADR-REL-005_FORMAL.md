# ADR-REL-005: Relationship Privacy Projections, Search, and Cross-Tenant Resolution

**Formal ADR status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0`  
**Founder-approved policy decisions:** `REL-FD-004`, `REL-FD-008`, `REL-FD-009`, `REL-FD-010`, `REL-FD-012`, `REL-FD-015`  
**Founder-approved recommendation:** `TRUE`  
**Formal wording ratified:** `FALSE`  
**Implementation authorized:** `FALSE`  
**Repository baseline:** `acb518ea5a160820e64681ff95a16b010fe1156c`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

## 1. Context

The Relationships and Delegated Authority PIA V1.1.0 is Founder-approved as an
as-designed baseline. The Founder has approved the architecture recommendation
underlying this ADR. This document formalizes that recommendation into a
controlled architecture decision record.

The formal text remains subject to final ratification after source
reconciliation and cross-domain contract review. No implementation is
authorized by this ADR draft.

## 2. Decision

Adopt server-generated, purpose-specific Relationship Projections rather than returning full canonical relationship records to clients.

Every query must be evaluated using authenticated principal, acting principal, represented principal, tenant, purpose, requested action, subject, relationship state, and privacy classification.

The relationship type registry must define default projection classes, but Authorization and protective controls determine the final projection. Separate disclosure decisions apply to:
- relationship existence;
- party identity;
- capacity and scope;
- verification status;
- evidence;
- restrictions;
- dispute status;
- historical versions.

Cross-tenant identity or relationship resolution must occur through an internal privacy-preserving resolution service. It may confirm a workflow match only when authorized and must not disclose other tenant memberships, horse relationships, guardian status, disputes, contact details, or account existence.

Search results must be minimum necessary, resistant to enumeration, rate-limited, attributable, and auditable where sensitive.

## 3. Normative Technical Rules

- Canonical relationship records are never exposed directly to ordinary clients.
- Tenant administrators do not receive global person or relationship search.
- Sensitive relationship existence may itself be confidential.
- Support visibility is case-bound and separately projected.
- Exports use the same purpose and projection controls as interactive access.
- Analytics may use approved aggregate facts but may not infer legal authority or protected traits.

## 4. Architectural Boundaries

- Identity owns canonical actor, account, principal, assurance, and representation truth.
- Relationships owns relationship and delegation facts, lifecycle, provenance, and dependencies.
- Authorization owns the final allow, deny, projection, step-up, and revocation-enforcement decision.
- Agreement and Consent owns documentary authorization, signer capacity, consent, withdrawal, and execution.
- Claims owns contested-claim procedure and final operational dispute disposition.
- Protected Participant and Safeguarding may narrow or prohibit relationship effects.
- Horse, Facility, Business, and Operations domains own their respective domain truth.
- Audit and Evidence owns attributable reconstruction and protected evidence requirements.

No adjacent domain may silently rewrite relationship truth through a side effect.

## 5. Data and State Consequences

- Stable identifiers and immutable version references are required.
- State transitions must be server enforced, attributable, and auditable.
- Material corrections supersede prior records rather than erasing them.
- Historical and current-state representations must remain reconcilable.
- Unknown, stale, conflicting, or unsupported authority states fail closed.

## 6. API, Event, and Integration Consequences

Implementations derived from this ADR must define:

- idempotent commands;
- expected-version or equivalent concurrency controls;
- structured domain events;
- audit correlation identifiers;
- retry and duplicate behavior;
- error and quarantine dispositions;
- privacy-projected read contracts;
- revocation and invalidation propagation where applicable.

External systems receive purpose-limited projections and may not create or
alter canonical relationship authority.

## 7. Security, Privacy, and Safeguarding Consequences

- Tenant and purpose boundaries are mandatory.
- Relationship existence may itself be confidential.
- High-risk changes require stronger assurance and explicit authority.
- Protected-participant controls may impose stricter rules than ordinary relationship policy.
- Evidence and dispute material must not be exposed through broad relationship payloads.
- Support access remains bounded, attributable, and non-authoritative.

## 8. Offline and Failure Behavior

- Offline state cannot independently create authoritative relationship or delegation effects.
- Protected mutations must fail closed or enter a defined quarantine path if required evidence,
  authorization, audit, or persistence controls fail.
- Recovery must preserve the first failure and all subsequent corrective evidence.
- Partial success must not leave unsupported authority active.

## 9. Alternatives Considered

### Return full relationship object and hide fields in UI

Rejected because client-side hiding is not authorization or privacy enforcement.

### Global directory of all EquineSync people and relationships

Rejected because it leaks tenant participation and sensitive relationships.

### Email-based cross-tenant lookup

Rejected because email is not canonical identity and creates enumeration risk.

## 10. Validation Obligations

- Cross-tenant search produces no unauthorized existence signal.
- Care Circle and emergency contact receive only permitted projection.
- Guardian, dispute, evidence, and restriction fields have independent disclosure tests.
- Support session projection is case-bound.
- Export and API projection parity tests.
- Enumeration, timing, and rate-limit abuse tests.

## 11. Open Implementation Parameters

- Projection vocabulary and field-level policy language.
- Search index architecture and deletion propagation.
- Permitted global support/security resolution workflows.
- Aggregate analytics privacy thresholds.

## 12. Source and Traceability Obligations

Before final ratification, this ADR must trace to:

- the locked Master Relationship Model V2.0;
- the approved Relationships and Delegated Authority PIA V1.1.0;
- the applicable Founder decisions;
- the Identity PIA and formal Identity ADRs;
- the Authorization PIA and formal Authorization ADRs;
- relevant Agreement, Claims, Safeguarding, Audit, Privacy, Horse, Facility,
  Communication, and Record Stewardship controls.

## 13. Ratification Gate

Recommended formal ADR disposition after source and contract review:

`ADR-REL-005_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

Until then:

`PROPOSED_FORMAL_ADR_DERIVED_FROM_FOUNDER_APPROVED_RECOMMENDATION_PENDING_FINAL_RATIFICATION`

## 14. Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Organization, tenant, facility, location, and program are distinct. No generic barn label collapses them.
- Care Circle participation is collaboration only and independently establishes no ownership, custody, guardianship, medical authority, financial authority, delegation, or universal record access.
- Emergency-contact status provides notification priority only and independently grants no authority, ownership, pickup right, consent capacity, or record access.
- Public-signup owner, manager, trainer, administrator, and facility-operator claims remain provisional until all required checks and governed activation complete.
- Emergency or break-glass access is a separately governed exceptional-access mechanism and is never inferred from relationship, role, Care Circle, emergency-contact, or ordinary delegation records.
