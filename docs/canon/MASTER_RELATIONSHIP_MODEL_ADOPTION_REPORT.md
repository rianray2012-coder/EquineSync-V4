# Master Relationship Model Adoption Report

## Decision

Founder correction and canon adoption: `APPROVED`

Current state: `MASTER_RELATIONSHIP_MODEL_READY_FOR_FOUNDER_LOCK`

The founder-approved model has been preserved at
`docs/canon/MASTER_RELATIONSHIP_MODEL.md`, expanded without materially reducing
the original coverage, and entered into the canon index as Tier 3 foundational
domain canon. This adoption establishes conceptual authority only. It does not
declare schema, migration, permission, Passport, workflow, external-service, or
production implementation complete.

## Source and Result

| Item | Value |
| --- | --- |
| Original source | `/Users/rianray/Downloads/MASTER_RELATIONSHIP_MODEL.md` |
| Original SHA-256 | `b46602a552a4919bcc4fb1af4b1141c8929bf0ab47bc620079a00b7a44025fdf` |
| Canonical path | `docs/canon/MASTER_RELATIONSHIP_MODEL.md` |
| Corrected SHA-256 | `dc59187c60cc86498466d8ca959767b0a9188ea7fcf33440a742c633f1f57e4a` |
| Original line count | 1,622 |
| Corrected line count | 1,958 |
| Source commit | `9f812280542f6e9c43935563badec2de1448947b` |
| Founder approval recorded | `2026-07-12T06:04:19Z` |

## Adopted Governance

- Canon tier: Tier 3 after the Master Ecosystem Model and before lifecycle and
  domain canons.
- Authority order: Product Vision, Ecosystem Model, Relationship Model, domain
  and lifecycle canons, then Permission Model for authorization enforcement.
- RF31 title: `RF31 Horse Transfer and Passport Continuity`.
- RF27 retains physical intake, arrival, location, and facility assignment.
- Canonical representation: binary relationship edges plus versioned groups and
  party edges for multi-party contexts.
- Relationship evidence informs authorization but never independently grants
  field-level access or bypasses backend redaction.
- Migration boundary: additive shadow model, provenance, reconciliation,
  access-delta reporting, quarantine, rollback eligibility, and no production
  mutation.
- External-service boundary: vendors report or execute external events but do
  not create EquineSync relationship authority.

## Correction Trace

| Correction | Resolution | Canon location |
| --- | --- | --- |
| MRM-C01 | Normalized RF31 to Horse Transfer and Passport Continuity and preserved RF27 physical-intake ownership. | Header; 24.1; ATLAS2 and ATLAS5 dependency records |
| MRM-C02 | Defined organization, barn account/operating context, facility, and location as separate principals. | Section 8 |
| MRM-C03 | Approved binary edges plus versioned relationship groups and party edges. | Section 4.3 |
| MRM-C04 | Made subject/counterparty references authoritative and convenience IDs validated projections. | Section 4.2 |
| MRM-C05 | Added relationship, authority, permission, visibility policy versions, provenance, confidence, and correlation. | Sections 4.1, 4.7, 4.8 |
| MRM-C06 | Declared uppercase statuses semantic canon with explicit lowercase storage/API normalization and separate state dimensions. | Sections 4.4 and 4.5 |
| MRM-C07 | Added controlled entity, relationship, authority, scope, termination, and dispute registries. | Section 4.6 |
| MRM-C08 | Added lawful-erasure, retention, legal-hold, safety, and audit-minimization precedence. | Sections 5.9 and 17.3 |
| MRM-C09 | Added the exact permission boundary: relationships inform authorization but do not grant fields. | Section 2.3 |
| MRM-C10 | Added Care Circle source/inviter authority, acceptance, verification, dates, policy versions, provenance, and supersession. | Section 6.9 |
| MRM-C11 | Added multi-guardian conflict, court restrictions, confidential contact, jurisdiction, emancipation, and age-of-majority transition. | Section 7.2 |
| MRM-C12 | Enumerated separate financial and responsibility party roles. | Section 10 |
| MRM-C13 | Added versioned Calendar participant-edge requirements. | Section 11 |
| MRM-C14 | Separated retention, stewardship, authorship, and direct access; required transfer visibility classification. | Sections 12.4 and 14.4 |
| MRM-C15 | Added deterministic duplicate candidates, provenance, confidence, human threshold, reversible evidence, and no name/photo auto-merge. | Section 13.6 |
| MRM-C16 | Added neutral dispute preservation, legal holds, temporary authority, appeal lineage, and no legal adjudication claim. | Section 15.3 |
| MRM-C17 | Added completed sale and governed foster, sanctuary, seizure, missing/stolen, donation, and reproductive extensions. | Sections 16.3 and 16.7 |
| MRM-C18 | Added schema/type versions, privacy, projection, idempotency, causation, and before/after-state event requirements. | Section 18.3 |
| MRM-C19 | Added analytics purpose limitation, suppression, retention, audience, and no-inference rules. | Section 20 |
| MRM-C20 | Added the additive shadow-model migration framework, provenance, access deltas, quarantine, dual-read comparison, no dual writes, and rollback. | Section 22 |
| MRM-C21 | Replaced the all-inclusive claim with the founder-approved broad-baseline wording. | Section 27 |
| MRM-C22 | Added implementation prerequisites for registries, multi-party contracts, authority policies, privacy/retention, migration access deltas, tests, and rollback. | Sections 26 and 29 |

All corrections MRM-C01 through MRM-C22 are resolved in the canonical document.

## Dependency Updates

- `docs/canon/CANON_INDEX.md` contains the approved Tier 3 row and mandatory
  relationship traceability rule.
- `docs/ATLAS2/CRITICAL_WORKFLOW_FIX_PLAN.md` contains the approved RF31 and RF32
  dependency language and final RF31 title.
- `docs/ATLAS5/ATLAS5_CONTROLLED_INTAKE_REPORT.md` contains the approved
  predecessor rule and maintains RF33-RF36 as proposed and unopened.
- `docs/ATLAS5/ATLAS5_PROPOSED_DOCUMENT_CORRECTIONS.md` uses the final RF31 title
  and records the Master Relationship Model predecessor.

## Locked Canon Conflict Review

No locked canon conflict was introduced. The Relationship Model specializes the
Ecosystem Model's graph and time principles, the Horse Lifecycle's identity and
continuity rules, the Business Lifecycle's organization separation, the
Facility Model's physical-location boundary, and the Permission Model's
authorization and projection rules. Where semantics overlap, the approved
authority order and stop-on-conflict rule apply.

RF29 and RF30 files were not modified. RF29 Calendar controls and RF30 AI
controls remain governed by their existing locked, default-off boundaries.

## Non-Implementation Attestation

- Production code changed: `false`
- Schema implemented: `false`
- Data migrated: `false`
- Permission behavior changed: `false`
- Passport behavior changed: `false`
- RF31-RF36 implementation performed: `false`
- RF33-RF36 opened: `false`
- External service activated: `false`
- Legacy fields promoted to verified authority: `false`
- Implementation completion declared: `false`

## Lock Readiness

The conceptual canon adoption and correction work is complete. Founder lock is
still a separate governance action.

`MASTER_RELATIONSHIP_MODEL_READY_FOR_FOUNDER_LOCK`
