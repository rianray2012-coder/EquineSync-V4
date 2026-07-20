# ADR-REL-001: Canonical Relationship Graph, Temporal Model, and Aggregate Boundaries

**Formal ADR status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0`  
**Founder-approved policy decisions:** `REL-FD-001`, `REL-FD-002`, `REL-FD-003`, `REL-FD-007`, `REL-FD-011`, `REL-FD-013`  
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

Adopt a canonical relationship graph composed of first-class Relationship aggregates with immutable opaque identifiers, typed parties and capacities, explicit subject and context scopes, effective-time and recorded-time semantics, and append-only version history.

Use a bitemporal logical model:
- valid time records when the relationship was effective in the represented world;
- transaction time records when EquineSync learned, recorded, corrected, or superseded the relationship.

Maintain a current relationship head for efficient operational lookup and an immutable version chain for as-of reconstruction. The current head is a projection of accepted versions and is never the sole historical record.

Define aggregate boundaries so that:
- Relationship owns its type, parties, capacities, scope, status, provenance, restrictions, and version chain;
- Identity owns canonical actors and principals;
- Authorization consumes relationship facts but does not mutate relationship truth;
- Agreement owns documentary execution and consent;
- Claims owns final dispute workflows;
- Horse, Facility, Business, and Protected Participant domains own their domain facts and expose governed references.

Represent multi-party relationships directly when the relationship has shared semantics, such as co-ownership or multiple guardians. Do not simulate every multi-party relationship through disconnected pairs when that would lose shared scope, evidence, or conflict meaning.

## 3. Normative Technical Rules

- Use immutable opaque IDs; concrete ID format selected during repository-stack implementation design.
- Use optimistic concurrency with expected relationship version.
- Every accepted change creates a new version; no in-place historical rewrite.
- Current-state projection must be reproducible from accepted versions and events.
- Relationship state changes and audit evidence must commit atomically or enter a protected quarantine workflow.
- Hard deletion is prohibited for material relationship history except where an approved privacy/retention rule expressly permits category-specific deletion without corrupting required evidence.

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

### Role-centric or foreign-key-only model

Rejected because it cannot safely represent temporal, disputed, concurrent, multi-party, or evidence-bearing relationships.

### Event store as the only operational representation

Rejected as the mandatory baseline because it may create unnecessary implementation complexity; append-only versions plus reconstructable projections satisfy the control objective.

### Mutable relationship row with audit log

Rejected because the mutable row can diverge from incomplete or failed audit writes and makes reliable as-of reconstruction harder.

## 10. Validation Obligations

- Concurrent relationship and co-owner tests.
- Effective-time versus recorded-time correction tests.
- Stale version write rejection.
- As-of reconstruction across activation, suspension, dispute, supersession, and termination.
- Atomic relationship-event-audit persistence failure tests.
- Cross-domain mutation tests confirming Authorization cannot rewrite Relationship truth.

## 11. Open Implementation Parameters

- Concrete persistence collections/tables and index definitions.
- Identifier format.
- Projection rebuild mechanism and service-level objectives.
- Retention periods by relationship and evidence category.

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

`ADR-REL-001_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

Until then:

`PROPOSED_FORMAL_ADR_DERIVED_FROM_FOUNDER_APPROVED_RECOMMENDATION_PENDING_FINAL_RATIFICATION`

## 14. Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Every party is carried as a typed, versioned `party_ref`. When one actor represents another, `representation_basis` carries basis type, source owner, immutable version, scope, effective interval, restrictions, and dispute state.
- Identity owns authenticated and attributed session context. The source domain owns the legal, relationship, agreement, guardianship, fiduciary, or other authority basis; Identity cannot manufacture it.
- Organization, tenant, facility, location, and program are distinct relationship contexts. One organization may operate multiple facilities or programs, and tenancy separation is determined by the owning cross-domain rules.
- The governed taxonomy contains no unqualified generic `barn relationship`.
