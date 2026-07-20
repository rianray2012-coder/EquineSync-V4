# ADR-REL-006: Offline Proposals, Authoritative Time, Conflict Detection, and Reconciliation

**Formal ADR status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0`  
**Founder-approved policy decisions:** `REL-FD-005`, `REL-FD-006`, `REL-FD-007`, `REL-FD-010`, `REL-FD-014`, `REL-FD-016`  
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

Offline clients may create only bounded Relationship Proposals. They may not represent a relationship, delegation, revocation, acceptance, verification, dispute resolution, or authority change as active until the authoritative server validates and accepts it.

Every offline proposal must include:
- immutable operation ID and idempotency key;
- actor, device, tenant, and represented context;
- proposal type;
- base relationship version;
- referenced authority and policy versions;
- client-observed time;
- queued time;
- scope and payload hash;
- local status clearly labeled PENDING_AUTHORITATIVE_VALIDATION.

The server supplies accepted time and final effective treatment. Client clocks never establish authoritative expiry, revocation, or activation.

On synchronization, the server revalidates identity, relationship, source authority, delegation, restrictions, policy, and current versions. Stale, conflicting, revoked, or unsupported proposals are rejected or quarantined with an explainable reason.

Automatic merge is permitted only for explicitly commutative, low-risk metadata changes. Authority, evidence, ownership, guardianship, delegation, restriction, and dispute conflicts require controlled review or explicit user correction.

## 3. Normative Technical Rules

- High-risk relationship actions are online-only.
- Offline queues are encrypted and scoped to the authenticated device/session policy.
- Accepted and rejected operations remain correlated to the original operation ID.
- Retry is idempotent and cannot create duplicate relationships or grants.
- Revocation and authority-watermark checks occur at acceptance time.
- User interface must distinguish local proposal, synchronized acceptance, rejection, conflict, and quarantine.

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

### Last-write-wins synchronization

Rejected because it can erase restrictions, evidence, or newer authority changes.

### Client timestamp determines effective state

Rejected because device clocks are untrusted.

### Full offline relationship administration

Rejected because authoritative identity, authority, and dispute checks cannot be safely guaranteed.

## 10. Validation Obligations

- Duplicate retry produces one accepted operation.
- Revoked delegation queued offline is rejected.
- Stale base version cannot overwrite a newer restriction.
- Forged or unreasonable client time has no authority effect.
- Interrupted synchronization resumes safely.
- Quarantine and manual reconciliation evidence is preserved.
- Offline user interface never displays pending authority as active.

## 11. Open Implementation Parameters

- Approved low-risk offline proposal types.
- Maximum queue duration and device-storage limits.
- Reconciliation user experience and support escalation.
- Trusted server-time implementation.

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

`ADR-REL-006_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

Until then:

`PROPOSED_FORMAL_ADR_DERIVED_FROM_FOUNDER_APPROVED_RECOMMENDATION_PENDING_FINAL_RATIFICATION`

## 14. Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Offline state is a proposal only and never relationship, verification, acceptance, delegation, or authorization truth.
- Synchronization must reject stale or version-incompatible identity, relationship, source-authority, restriction, policy, and authorization facts and preserve the attributable reason and evidence.
- Candidate title is canonical for this successor; all prior stage titles remain immutable predecessor aliases.
