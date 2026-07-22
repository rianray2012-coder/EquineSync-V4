# FAC-FD-017 Adaptive Onboarding Specification

**Package:** `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE`  
**Decision:** `FAC-FD-017`  
**Authority:** Founder-approved design direction dated `2026-07-21`  
**Implementation authority:** `false`

## Design rule

Onboarding must remain adaptive. An individual horse owner must not be forced to create a Facility or Organization merely because the architecture supports those entities. The journey asks for an entity only when the user has an immediate real-world purpose and can make the required assertion.

## Normative rules

1. Onboarding is adaptive and role-sensitive.
2. An individual horse owner may start with a horse-first flow.
3. An owner is not required to create a Facility unless a real Facility relationship is asserted or needed.
4. An owner is not required to create an Organization unless a real Organization relationship is asserted or needed.
5. Tenant creation or assignment implies no legal Organization, Business, Facility, Barn, or provider entity.
6. Facility and Organization creation or association may occur later without blocking initial onboarding.
7. The journey supports each operating context in the persona table below.
8. Architecture-driven entity-creation steps with no immediate user purpose remain hidden.
9. Any seed record is minimal, justified, reversible, attributable, and non-authority-bearing.
10. Entity creation or association implies no authority, stewardship, membership, Relationship fact, or access right.

## Persona and operating-context matrix

| Persona/context | Initial minimum | Facility behavior | Organization behavior | Prohibited inference |
|---|---|---|---|---|
| Unaffiliated individual owner | Tenant context plus horse-first record | Omitted | Omitted | No barn, business, stewardship, or access inferred |
| Owner associated with a barn | Tenant context plus horse; optional explicit association | Associate later or during purpose-driven step | Omitted unless real | Barn association grants no membership or permission |
| Independent trainer | Tenant context plus trainer operating profile/reference | Optional | Omitted | No legal entity fabricated |
| Trainer within a Facility | Tenant context plus explicit temporal Facility association | Required only for asserted operation | Optional | Facility association grants no staff authority |
| Facility operator | Tenant context plus justified DRAFT Facility | Purpose-driven creation | Optional if no real Organization | Operator label grants no permission |
| Multi-Facility Organization | Explicit Organization and temporal Facility/Tenant links | Multiple explicit links | Real Organization required | Common control does not collapse Tenants |
| Provider/vendor Organization | Explicit Organization plus governed capabilities | Optional explicit service links | Real provider Organization | Provider type grants no capability or Tenant access |
| Shared physical Facility/multiple Tenants | One stable Facility identity plus isolated Tenant projections | Explicit temporal links per Tenant | Optional per operator | No cross-Tenant visibility or authority |

## Decision flow

1. Establish the minimum Tenant context required for isolation; do not describe it as a legal Organization or physical Facility.
2. Ask the user’s immediate purpose in plain language, such as add a horse, manage a physical operation, work at a Facility, or represent a real Organization.
3. If the purpose is horse-first, continue without Facility or Organization creation.
4. If a Facility relationship is asserted, collect only the association evidence and scope needed for that purpose.
5. If a real Organization is asserted, collect the Organization evidence appropriate to its type and jurisdiction.
6. Present a clear summary of records that will be created or associated and state that no authority follows automatically.
7. Record the decision path, actor, timestamp, stated purpose, created/associated identifiers, reversibility information, and separate permission outcome.

## Seed controls

A seed record requires a recorded purpose, minimum fields, source, actor, timestamp, lifecycle state, reversal path, and explicit `authority_conferred=false`. A Tenant seed may exist without Facility or Organization records. Reversal cannot erase audit evidence or silently transfer records. No seed creates Relationship, stewardship, membership, staff, provider capability, or permission facts.

## Later association

Later Facility or Organization association is explicit, temporal, scoped, attributable, revocable, and separately authorized. It preserves prior history and triggers no automatic migration, merge, data sharing, or access. Shared addresses, emails, payment records, user overlap, or similarity scores are insufficient evidence.

## UX boundary

The user sees purpose-driven language, not internal architecture vocabulary unless necessary for informed action. Facility and Organization steps are progressively disclosed. Skipping an unnecessary entity must not block the horse-first path. Context remains visible after selection, and wrong-context consequential actions require reconfirmation.

## Evidence and tests

`FAC_FD_017_ADAPTIVE_ONBOARDING_TEST_MATRIX.csv` covers all eight contexts and the mandatory positive, negative, and boundary cases. `TEST_MATRIX.csv` maps each changed or added requirement to documentary tests. These are design specifications only; no application was started and no production-like record was created.
