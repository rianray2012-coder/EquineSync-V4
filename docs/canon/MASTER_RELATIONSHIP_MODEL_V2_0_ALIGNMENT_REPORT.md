# Master Relationship Model v2.0 Alignment Report

Status: `MASTER_RELATIONSHIP_MODEL_V2_0_READY_FOR_FOUNDER_REVIEW`

## Review Boundary

This is a controlled successor review. The proposal remains non-canonical,
unlocked, and unimplemented. The controlling relationship canon at
`docs/canon/MASTER_RELATIONSHIP_MODEL.md` was not overwritten or amended.

Reviewed:

- proposed v2.0 source, 843 lines, SHA-256
  `b0c0a37dacd8d351a000a07fc3ee021efb942eb8249633d4cf7a64e2bca1ae3a`;
- controlling Master Relationship Model;
- prior alignment, correction, and adoption reports;
- Master Permission, Ecosystem, Horse, Barn, Business, and Facility canons;
- Master Record Stewardship and Retention Model v2.0 from Downloads;
- RF29 and RF30 locked boundaries;
- current RF31/RF32 and ATLAS5 planning artifacts;
- current Passport, Care Circle, provider, guardian, membership, billing,
  agreement, Calendar, and notification code.

Evidence limitations:

- `MASTER_RELATIONSHIP_MODEL_FINAL_LOCKED.md` does not exist under that name in
  the repository. The controlling file is `docs/canon/MASTER_RELATIONSHIP_MODEL.md`.
- The current repository adoption record says `READY_FOR_FOUNDER_LOCK`, while
  this directive identifies the model as founder-locked. Successor text should
  reference the canonical path and a verified lock record rather than a missing
  filename.
- `MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0.md` was not found in the
  repository, Downloads, or supplied attachments. Claims-owned wording cannot
  receive final cross-canon clearance until that model is supplied.
- Stewardship v2.0 was reviewed as directed. A separate v2.1 file also exists in
  Downloads; founder governance must identify which version controls before a
  successor amendment is adopted.

## Overall Finding

Version 2.0 preserves the locked relationship principles and adds useful
operational semantics. No direct weakening of Version 1 was found. It is not a
safe full successor because it does not restate the full semantic model and is
less than half its length. It is best treated as a proposed formal amendment
after corrections and missing-canon review.

Recommended strategy: **Option B, Formal Amendment**.

Proposed canonical name after approval:

`docs/canon/MASTER_RELATIONSHIP_MODEL_AMENDMENT_1.md`

## Fifteen-Section Review

| Section | Belongs in relationship canon? | Boundary and finding | Required action |
| --- | --- | --- | --- |
| Cross-canon boundary | Yes | Correctly makes Relationship semantics distinct from Stewardship, Claims, Permission, lifecycle, and vendor architecture. The Claims canon and named External Architecture authority are unavailable. | Retain as amendment framing; replace vague/missing document references with canonical paths or governed placeholders. |
| Delegated authority | Yes, for relationship evidence | Permission Model already defines delegation and non-escalation. Claims canon should govern validity disputes; Permission governs executable authority. | Narrow to delegation-edge evidence and lifecycle; explicitly defer action authorization to Permission. |
| Authority precedence | Partly | Relationship should identify competing sources and route a conflict. Claims canon should resolve claim procedure; Permission already defines general enforcement precedence. | Remove any implication that this amendment independently resolves legal or permission precedence. |
| Purpose limitation | Yes | Strongly aligned with Permission purpose-bound access and existing relationship scope. | Retain; map purpose registry values to Permission purpose IDs rather than creating a competing vocabulary. |
| Source/derived/inferred/projected states | Yes | Directly addresses current derived Care Circle and legacy-field risks. `DISPUTED` and `SUPERSEDED` are not origin classes. | Split origin, lifecycle, verification, and dispute dimensions. |
| Dependencies/prerequisites | Yes | Useful for guardian, provider, agreement, organization, and event dependencies. | Retain; require acyclic graph validation, versioned dependency rules, and fail-closed review states. |
| Suspension-effects matrix | Yes, for semantic effects | Permission and domain policies decide actual access and obligations. `surviving_permissions` risks embedding authorization in relationship state. | Rename to required permission reevaluation inputs/outcomes; adapter effects are requested states, not automatic external actions. |
| Succession/substitution | Yes, for relationship edges | Overlaps Business Lifecycle and Stewardship v2.0 organization succession and record transfer. | Keep relationship-edge semantics only; cross-reference business succession and record stewardship rather than duplicating their rules. |
| Inactive-account continuity | Yes, for person/account separation | Strongly aligned, but account deletion and pseudonymization are controlled in Stewardship and identity/security domains. | Keep identity-continuity rule; defer credential disposal and record pseudonymization mechanics. |
| Confirmation/reverification | Yes | Useful for guardian, provider, agent, emergency, and delegated authority. | Retain; missed verification creates a review input, not automatic permission change without policy evaluation and audit. |
| Negative/restricted/prohibited relationships | Conditionally | Explicit restrictions are necessary, but highly sensitive. An ended employee relationship is not automatically a negative edge. Claims and Permission ownership is unresolved. | Rename to restrictive authority edges; require authority, confidentiality, non-disclosure projection, expiry/review, and Claims-canon validation. |
| Visibility classification | Metadata belongs here | Permission Model owns final visibility and field projection. A second independent class registry could drift. | Define relationship sensitivity metadata mapped to Permission classifications; do not create a parallel authorization taxonomy. |
| Consent lifecycle | Relationship effect belongs here | Stewardship owns consent records/evidence; Permission and legal policy govern processing; Relationship owns the relationship effect. | Replace full consent-record ownership with a versioned consent reference and effect contract. |
| Relationship-aware notifications | Eligibility belongs here | Communications domain owns routing/delivery; Permission owns payload projection. Current routing remains fragmented. | Define recipient eligibility/restriction inputs and change effects only; delivery cannot prove receipt, authority, consent, or legal service. |
| Change-impact events | Yes, as intent/evidence | Valuable coordination contract, but could imply automatic permission, Calendar, adapter, or external mutation. | Define immutable impact intents and per-domain acknowledgements/failures; prohibit automatic external or canonical mutation absent later RF authorization. |

## Repository Reality

- Care Circle combines stored members with owner, trainer, and provider-derived
  entries; v2.0 origin and promotion rules directly address this risk.
- Provider access uses active `horse_provider_assignments`, not a canonical
  delegated-authority or dependency graph.
- Guardians are represented across guardian links, account memberships, student
  profiles, and a separate intake profile; reverification and restrictive edges
  are not unified.
- Account memberships are compatibility mirrors for current role/barn context,
  not canonical person-to-organization relationships.
- Billing uses `owner_id` and local invoice status, not the full payer,
  guarantor, settlement, purpose, and dependency model.
- Agreement routes store signer roles and user IDs, not versioned relationship
  authority snapshots.
- RF29 Calendar uses relationship arrays and permission-safe projection in local
  evidence, but routes, adapters, workers, providers, and persistence remain
  default-off under the locked RF29 boundary.
- Notification eligibility and routing remain domain-specific; live delivery or
  preview does not establish relationship authority.

These are future planning gaps, not authorization to implement v2.0.

## Preservation Attestation

| Locked rule | Preserved? | Evidence in v2.0 |
| --- | --- | --- |
| Relationship truth is separate from permission enforcement. | Yes | Sections 2, 3, 14.3, and 24 preserve Permission as final authority. |
| Ownership, custody, possession, access, responsibility, authority, authorship, stewardship, and payment remain distinct. | Yes | Section 2 explicitly preserves separation; examples reinforce it. |
| Role labels do not independently prove authority. | Yes | Sections 2, 3.2, and 7.4. |
| Payment creates neither ownership nor guardianship. | Yes | Sections 3.2, 5.3, 6.3, and 20. |
| Barn/facility assignment creates neither title nor custody. | Yes | Sections 2 and 6.3 preserve the physical-assignment boundary. |
| External vendors do not create EquineSync authority. | Yes | Sections 2, 3.2, and 21. |
| Historical records and authorship survive termination. | Yes | Sections 2, 9, 10, and 11, subject to Stewardship rules. |
| Disputed/unverified relationships are neutrally preserved. | Yes | Sections 2, 5.4, 7, and 10.3. |
| Migration remains additive, provenance-bearing, reversible, and access-delta reviewed. | Yes | Sections 2 and 22. |
| RF27 retains physical intake/location ownership. | Yes | Sections 2 and 19. |
| RF29 remains locked and unchanged. | Yes | Sections 2 and 24. |
| RF30 remains locked and unchanged. | Yes | Sections 2 and 24. |
| RF31-RF36 are not opened or implemented. | Yes | Sections 2, 19-25. |

Preservation result: **13 of 13 locked rules intact**. Cross-canon ownership
corrections are still required before adoption, but no preservation failure was
found.

## Proposed Dependency Language

### RF31

```markdown
RF31 Horse Transfer and Passport Continuity depends on the locked Master
Relationship Model and, if founder-adopted, Relationship Model Amendment 1.
RF31 must apply purpose-limited delegation, origin/promotion evidence,
relationship dependencies, scoped suspension, succession, inactive-identity
continuity, reverification, restrictive authority edges, relationship
sensitivity metadata, consent effects, notification eligibility, and impact
events without bypassing the Master Permission Model, Record Stewardship canon,
or Claims/Disputes canon. RF27 retains physical intake and location ownership.
```

### RF32

```markdown
RF32 Barn Payment Issue Workflow depends on the locked Master Relationship Model
and, if founder-adopted, Relationship Model Amendment 1. RF32 must distinguish
owner, payer, guarantor, invoice recipient, payment-method owner, settlement
source, refund recipient, beneficiary, and dispute claimant; preserve
purpose-limited authority and obligation dependencies; and treat suspension,
succession, inactive accounts, reverification, restricted contact, consent,
notice eligibility, and impact events as governed inputs. Payment status cannot
change ownership, guardianship, emergency duties, stewardship, or Passport
continuity.
```

### ATLAS5

```markdown
ATLAS5 remains downstream of the locked Master Relationship Model and any later
founder-adopted amendment. External services may consume only purpose-limited,
permission-filtered, policy-versioned relationship projections. No vendor may
broaden delegation, resolve authority conflicts, promote inferred relationships,
inherit succession scope, restore inactive access, convert delivery into consent
or acceptance, execute relationship impact actions, or become the source of
relationship truth. RF33-RF36 remain proposed and unopened.
```

## Founder Decisions

1. Approve Option B, Formal Amendment, or select another strategy.
2. Confirm the controlling predecessor lock artifact/path and reconcile the
   missing `MASTER_RELATIONSHIP_MODEL_FINAL_LOCKED.md` reference.
3. Supply and identify the controlling Master Claims, Disputes, and Authority
   Model before final cross-canon adoption review.
4. Identify whether Stewardship v2.0 or v2.1 controls this amendment review.
5. Approve the ownership split for all fifteen sections.
6. Approve delegation/re-delegation evidence boundaries and Permission control.
7. Approve the separated origin, lifecycle, verification, and dispute registries.
8. Approve dependency-failure and suspension reevaluation semantics.
9. Approve restrictive authority edges, confidentiality, review, and expiry.
10. Approve mapping relationship sensitivity metadata to Permission classes.
11. Approve consent-reference/effect semantics rather than duplicate consent
    record ownership.
12. Approve notification eligibility versus communications delivery ownership.
13. Approve impact events as intents requiring domain acknowledgement, not
    autonomous actions.
14. Approve the corrected RF31, RF32, and ATLAS5 dependency language.

## Stop-State Attestation

- Proposed v2.0 adopted: `false`
- Proposed v2.0 locked: `false`
- Controlling relationship canon overwritten: `false`
- Canon Index changed: `false`
- Production code/schema/data/permissions changed: `false`
- Passport or Care Circle behavior changed: `false`
- RF31-RF36 opened or implemented: `false`
- External service activated: `false`
- RF29 or RF30 modified: `false`

`MASTER_RELATIONSHIP_MODEL_V2_0_READY_FOR_FOUNDER_REVIEW`
