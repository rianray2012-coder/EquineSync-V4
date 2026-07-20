# ADR-REL-002: Relationship-Type Registry, Versioning, and Change Control

**Formal ADR status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0`  
**Founder-approved policy decisions:** `REL-FD-002`, `REL-FD-013`  
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

Adopt a versioned Relationship Type Registry as the only approved source of production relationship semantics.

Each relationship type version must define:
- stable type ID and semantic version;
- owning domain;
- allowed party classes and capacities;
- directionality and cardinality;
- allowed subjects and scopes;
- required and optional evidence;
- verification rules and permitted reviewers;
- lifecycle and state transitions;
- privacy projections;
- authorization facts it may expose;
- delegation eligibility and restrictions;
- safeguarding constraints;
- migration, deprecation, and supersession rules.

The registry must be source-controlled, machine-readable, schema-validated, reviewable, and promoted through controlled release. Runtime services may cache or materialize the approved registry but may not create new semantic types through free text, feature flags, database inserts, or interface labels.

A type version change is classified as:
- PATCH: editorial or non-semantic clarification;
- MINOR: backward-compatible optional capability or metadata extension;
- MAJOR: changed meaning, party rules, authority effect, evidence, privacy, lifecycle, or safeguarding behavior.

Existing relationship records remain bound to the type version under which they were created until a governed migration or reclassification occurs.

## 3. Normative Technical Rules

- Unknown type IDs fail closed.
- Deprecated types remain readable for historical reconstruction.
- New creation against a deprecated type is prohibited after its cutoff date.
- Registry changes affecting authority, privacy, minors, evidence, or lifecycle require structured review and Founder approval where constitutionally material.
- Application code may reference stable type IDs but cannot redefine their meaning.

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

### Free-text relationship types

Rejected because meaning, permissions, and evidence requirements would drift.

### Code enums only

Rejected because code enums do not contain sufficient governance, privacy, evidence, migration, or lifecycle metadata.

### Database-admin-managed types

Rejected because uncontrolled runtime editing would bypass source review and change control.

## 10. Validation Obligations

- Schema validation of every registry entry.
- Unknown/deprecated type creation denial.
- Backward compatibility and version binding tests.
- Major-version migration dry run.
- Permission and privacy projection tests for each authority-relevant type.
- Machine check that no production workflow accepts arbitrary type strings.

## 11. Open Implementation Parameters

- Exact registry path and serialization format.
- Registry distribution and cache refresh mechanism.
- Approval thresholds for non-material PATCH changes.

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

`ADR-REL-002_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

Until then:

`PROPOSED_FORMAL_ADR_DERIVED_FROM_FOUNDER_APPROVED_RECOMMENDATION_PENDING_FINAL_RATIFICATION`

## 14. Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- The registry must reject an unqualified generic `barn relationship`; organization, tenant, facility, location, program, employment, service, horse, care, custody, and authority-bearing semantics remain separately typed.
- Every production type has an immutable identifier, semantic version, owning domain, party and capacity rules, lifecycle, evidence, privacy projection, authorization facts, delegation eligibility, migration behavior, and predecessor aliases.
- Free text, interface labels, configuration, or code cannot introduce a production relationship type.
