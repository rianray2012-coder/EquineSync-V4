# Master Relationship Model Proposed Corrections

Status: Proposed corrections only. The supplied source remains unchanged and is
the presumptive governing conceptual model pending founder review.

## Correction Ledger

| ID | Source area | Proposed correction | Reason |
| --- | --- | --- | --- |
| MRM-C01 | Primary Purpose; 24.1 | Replace `RF31 Horse Identity & Transfer Continuity` with the founder-approved RF31 title and state that RF27 owns physical intake/location while RF31 owns transfer and Passport relationship continuity. | Prevents title drift and reopening RF27. |
| MRM-C02 | 3.4; 8 | Define `organization`, `barn account/operating context`, and `facility` as distinct canonical principals. A barn label must not ambiguously mean both a business and physical place. | Locked Business and Facility canons require this separation; current code often uses `barn_id` for tenancy. |
| MRM-C03 | 4.1 | Specify whether the core relationship is binary, and add a canonical party-edge/participant object for multi-party agreements, co-ownership decisions, syndicates, guardians, invoices, and Calendar events. | A single subject/counterparty pair cannot safely express every listed multi-party case. |
| MRM-C04 | 4.1-4.2 | Designate subject/counterparty IDs as authoritative and convenience fields such as `horse_id`, `person_id`, `organization_id`, and `facility_id` as validated projections, not independently editable truth. | Prevents contradictory duplicate identifiers. |
| MRM-C05 | 4.1; 18 | Add `relationship_type_version`, `authority_policy_version`, `permission_policy_version`, `visibility_policy_version`, `correlation_id`, and source provenance/confidence fields. | Permissions and imported claims must be reproducible against the policy and evidence active at the time. |
| MRM-C06 | 4.3-4.4 | State that uppercase values are semantic canon and require an explicit mapping to repository lowercase storage/API values. Define precedence between lifecycle status, verification status, and dispute status. | Prevents incompatible status rewrites and ambiguous combinations. |
| MRM-C07 | 4; 22 | Add controlled registries for relationship types, entity types, authority sources, scopes, termination reasons, and dispute types. Extensions require governed registration. | Free-form strings would recreate terminology drift. |
| MRM-C08 | 5.9; 17.3 | Replace blanket soft-deletion language with preservation-by-default subject to lawful erasure, retention, legal hold, safety, and audit-minimization policy. | Privacy erasure and legal retention can conflict; neither should be silently absolute. |
| MRM-C09 | 6.9; 12 | State that a relationship can make a user eligible for a permission evaluation but does not itself grant fields. Final access still requires current policy, consent, sensitivity, tenant, suspension, and projection checks. | Preserves the Master Permission Model and Passport backend redaction as enforcement authority. |
| MRM-C10 | 6.9 | Require Care Circle source authority, inviter authority, acceptance state, verification state where applicable, effective dates, policy versions, and supersession. Derived UI members must not be promoted automatically to verified canonical relationships. | Current Care Circle can derive owner/trainer/provider entries from legacy fields. |
| MRM-C11 | 7.2-7.3 | Add multiple-guardian conflicts, court-restricted communication, confidential-contact rules, emancipated minors where legally supported, jurisdiction/age-of-majority policy, and transition evidence. | Current guardian truth is split and edge cases affect safety and privacy. |
| MRM-C12 | 10 | Add obligation, invoice recipient, payer, guarantor, payment-method owner, settlement source, refund recipient, dispute claimant, and beneficiary as distinct relationship/party roles. | RF32 and RF35 must not conflate internal invoice state with settled money or ownership. |
| MRM-C13 | 11 | Require Calendar participant edges to capture participation role, relationship snapshot/reference, invitation/attendance state, visibility basis, and event-effective period. | Free-floating relationship arrays cannot preserve why access was valid. |
| MRM-C14 | 13.3; 14.4 | Define a transfer visibility matrix by record category and distinguish retention from continuing direct application access. Former organizations retain valid evidence but do not automatically retain live horse access. | Avoids privacy overreach while preserving authorship and legal history. |
| MRM-C15 | 13.6 | Add deterministic identifiers, source provenance, match confidence, manual-review threshold, merge authority, reversible link/merge evidence, and an explicit prohibition on automated merge from names/photos alone. | Duplicate-horse resolution is trust-critical and current canonical tooling is absent. |
| MRM-C16 | 15 | Add legal-hold state, neutral claim language, temporary safety authority, appeal/review lineage, and a rule that EquineSync records claims and decisions without adjudicating legal ownership. | Prevents the platform from overclaiming legal authority. |
| MRM-C17 | 16 | Add sold/completed sale as an explicit transition outcome and consider foster, sanctuary, seizure/impound, missing/stolen, donation, and reproductive-material relationships as governed registry candidates. | Improves required edge-case and future-domain coverage without calling the model all-inclusive. |
| MRM-C18 | 18.3 | Add event schema version, relationship type/version, privacy classification, projection class, idempotency key, causation ID, and before/after state references. | Separate domain audits currently lack one reproducible relationship event contract. |
| MRM-C19 | 20 | Add purpose limitation, minimum cohort, suppression, retention, and no-inference rules for relationship analytics. | Relationship analytics can expose sensitive ownership, guardian, medical, or dispute facts. |
| MRM-C20 | 22 | Require an additive shadow model, source-precedence matrix, per-row provenance, exception ledger, access-delta report, dual-read comparison, no-dual-write rule, rollback eligibility, and founder authorization before any shared-data execution. | Current relationship truth spans compatibility mirrors and many collections; permission drift is a P1 migration risk. |
| MRM-C21 | 27 | Replace `all-inclusive for the currently identified EquineSync ecosystem` with `broad baseline for currently identified relationship domains, subject to explicit edge-case review and governed extension`. | The document itself correctly acknowledges that unknown business and jurisdictional cases remain. |
| MRM-C22 | 26; 29 | Add explicit approval requirements for the relationship-type registry, multi-party representation, authority-source registry, privacy/retention precedence, and migration access-delta evidence. | Founder approval of broad prose alone does not resolve these implementation-critical ambiguities. |

## Proposed Exact Text Additions

### Canon and Permission Boundary

Add after Canonical Principle 2.3:

```markdown
A relationship is evidence used by authorization; it is not itself a field-level
permission. Final access must be resolved by the Master Permission Model using
current identity, tenant, relationship status, scope, consent, sensitivity,
suspension, policy version, and approved response projection. Relationship data
must never bypass backend field redaction.
```

### Multi-Party Representation

Add to the Core Relationship Object:

```markdown
The base subject/counterparty form represents a binary edge. Multi-party legal,
financial, care, agreement, and participation contexts must use a canonical
relationship group or transaction plus versioned party edges. Each edge records
the entity, party role, scope, authority, effective period, status, and policy
references. A list of user IDs without party semantics is not a canonical
multi-party relationship.
```

### Historical Access

Add to Section 14.4:

```markdown
Retention, stewardship, authorship, and direct application access are separate.
Ending a relationship preserves required records and attribution, but does not
automatically preserve live access to the current horse, organization, or later
records. Post-termination access requires an explicit purpose, scope, period,
legal basis, and permission projection.
```

### Migration Safety

Add to Section 22:

```markdown
Legacy values may be migrated as claims or unverified relationship candidates;
they must not be promoted to verified legal authority solely because they appear
in `owner_id`, role, payer, signer, creator, barn, Care Circle, provider,
guardian, or participant fields. Every migration must report permission deltas
before activation and quarantine ambiguous or conflicting sources.
```

## Proposed Roadmap Dependency Text

```markdown
RF31 and RF32 are immediate consumers of the founder-approved Master
Relationship Model. Proposed RF33-RF36 remain downstream and unopened. No
external-service phase may use a vendor event, signature, payment, message,
calendar projection, identity assertion, or stored artifact as independent proof
of EquineSync relationship authority.
```

## Unresolved Founder Decisions

- Canon hierarchy placement and conflict-resolution order.
- Final RF31 title and physical-intake boundary wording.
- Binary plus party-edge versus first-class multi-party representation.
- Initial relationship-type and authority-source registries.
- Beneficial ownership and co-owner decision depth.
- Former-party historical access model.
- Guardian/minor conflict and age-of-majority model.
- Payer-without-account and split-responsibility model.
- Emergency authority and spending limits.
- Dispute freeze and temporary restriction authority.
- Privacy erasure, retention, and legal-hold precedence.
- Import verification thresholds and administrator resolution authority.

`MASTER_RELATIONSHIP_MODEL_READY_FOR_FOUNDER_REVIEW`
