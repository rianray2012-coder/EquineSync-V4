# Master Relationship Model v2.0 Preservation Matrix

Every numbered Version 1 section is accounted for below. `modified=false` means
no Version 1 rule was removed or materially narrowed; integrated Version 2.0
language is additive clarification.

| version_1_section | version_1_rule | version_2_location | preserved | modified | clarified | removed | conflict_status | reason | founder_decision_required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 Executive Summary | Relationships are explicit, temporal, scoped, and cross-domain. | 1, plus 1.2 cross-canon boundary | true | false | true | false | none | Full text retained; canon ownership clarified. | false |
| 2 Canonical Principles | Identity, relationship, authority, permission, responsibility, visibility, custody, and authorship are separate. | 2; reinforced in 4.9 and 12.6 | true | false | true | false | none | Purpose and visibility metadata remain subordinate to Permission. | false |
| 3 Scope | Covers animals, people, organizations, places, governance, and transaction entities. | 3 unchanged | true | false | false | false | none | Entire entity scope retained. | false |
| 4 Core Relationship Object | Binary edges, party groups, registries, provenance, policy versions. | 4, expanded through 4.9-4.11 | true | false | true | false | none | Adds purpose, origin/promotion, dependencies, and v2 registries. | true |
| 5 Relationship Lifecycle | Create, accept, verify, activate, modify, suspend, dispute, terminate, archive. | 5, with reverification and suspension matrix | true | false | true | false | none | Existing lifecycle retained; effects made explicit. | true |
| 6 Horse-Centered Model | Owner, lease, custody, barn, trainer, rider, Care Circle, providers, insurer, aliases. | 6 unchanged | true | false | false | false | none | No horse relationship was removed. | false |
| 7 Human and Guardian Relationships | Person/account, guardian/minor, emergency contact, agent/fiduciary. | 7, plus 7.6 delegation and 7.7 inactive identity | true | false | true | false | none | Adds delegated authority and account continuity without changing guardian rules. | true |
| 8 Organization and Facility Relationships | Organization, barn context, facility, location, staff, inter-organization edges. | 8, plus 8.6 succession/substitution | true | false | true | false | none | Adds successor edges while retaining Business and Stewardship ownership. | true |
| 9 Agreement Relationships | Parties, effects, immutable continuity. | 9, plus 9.4 consent effects | true | false | true | false | none | Consent record remains Stewardship-owned; relationship effects added. | true |
| 10 Financial Relationships | Payer and recipient roles remain distinct from ownership and relationship state. | 10 unchanged | true | false | false | false | none | V2 RF32 language does not alter financial separation. | false |
| 11 Calendar and Participation | Participation references relationships; visibility follows scope/sensitivity. | 11, plus notification eligibility | true | false | true | false | none | Communications delivery remains separate. | true |
| 12 Permissions Derived from Relationships | Deny by default; role insufficient; historical and emergency access governed. | 12, plus sensitivity mapping | true | false | true | false | none | Permission Model remains final enforcement authority. | true |
| 13 Horse Transfer and Passport Continuity | Transfer is coordinated transition with duplicate prevention. | 13 unchanged | true | false | false | false | none | No transfer or RF27 boundary was weakened. | false |
| 14 Record Stewardship and Continuity | Authorship, stewardship, visibility, and correction are distinct. | 14 unchanged | true | false | false | false | none | Record Stewardship canon remains controlling for records. | false |
| 15 Disputes and Competing Claims | Preserve competing evidence; no silent winner or legal adjudication. | 15, plus scoped precedence and restrictive edges | true | false | true | false | conditional external review | Claims canon must validate procedural ownership before final lock. | true |
| 16 Special Lifecycle Events | Death, retirement, sale, trial, estate, surrender, extensions. | 16 unchanged | true | false | false | false | none | All exceptional cases retained. | false |
| 17 Data Model Constraints | Exclusivity, effective dates, soft deletion, idempotency, referential integrity. | 17 unchanged | true | false | false | false | none | No schema authorization implied. | false |
| 18 API and Event Contracts | Relationship commands/events and privacy-safe event evidence. | 18, plus 18.4 impact intents | true | false | true | false | none | Impact events explicitly cannot execute autonomous mutations. | true |
| 19 External Service Boundaries | Vendors are adapters, not relationship authorities. | 19 unchanged; reinforced in 1.2 and 18.4 | true | false | true | false | none | No external activation or authority expansion. | false |
| 20 Analytics and Reporting | Authorized relationship metrics without sensitive leakage or inference. | 20 unchanged | true | false | false | false | none | Purpose and visibility additions strengthen this rule. | false |
| 21 Administrative Controls | Least-privileged, audited review and correction tools. | 21 unchanged | true | false | false | false | none | No admin implementation added. | false |
| 22 Migration and Legacy Convergence | Additive shadow model, provenance, quarantine, access deltas, rollback. | 22 unchanged; origin/dependency additions feed it | true | false | true | false | none | No migration authorized. | false |
| 23 Validation Scenarios | Ownership, guardian, provider, payments, Calendar, continuity scenarios. | 23 unchanged | true | false | false | false | none | All 35 scenarios retained. | false |
| 24 RF31 and Later Governance | RF31/RF32 dependencies and external-service boundaries. | 24 unchanged; candidate dependency proposals externalized | true | false | true | false | none | RF31-RF36 remain unopened. | true |
| 25 Founder Decision Ledger | Product-policy decisions remain founder-gated. | 25 unchanged | true | false | false | false | none | V2 adds separate lock decisions. | true |
| 26 Completion Criteria | Canon adoption is not implementation completion. | 26 unchanged | true | false | false | false | none | Successor remains unlocked. | false |
| 27 Inclusiveness Assessment | Broad baseline subject to governed extension. | 27 unchanged | true | false | false | false | none | No all-inclusive claim restored. | false |
| 28 Canonical Declaration | Persistent horse identity and no shortcut to authority. | 28 preserved as Version 1 declaration proposed for succession | true | false | true | false | none | Candidate does not claim current canonical status. | false |
| 29 Approval State | Version 1 state and implementation prohibitions. | 29 replaced only with candidate-state bookkeeping | true | false | true | false | none | Semantic restrictions preserved; candidate accurately says non-canonical/unlocked. | true |

## Result

- Version 1 numbered sections accounted for: `29/29`
- Removed rules: `0`
- Materially weakened rules: `0`
- Conditional external-canon review items: `1` (Claims/Disputes ownership)
- Version 1 historical checksum preserved: `dc59187c60cc86498466d8ca959767b0a9188ea7fcf33440a742c633f1f57e4a`

`MASTER_RELATIONSHIP_MODEL_V2_0_READY_FOR_FOUNDER_LOCK_REVIEW`
