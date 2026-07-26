# FAC-FD-017 Adaptive-Onboarding Refinement

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `FOUNDER_APPROVED_DESIGN_DOCTRINE_REFINED`
- Candidate disposition before fresh review: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

## Controlling refinement

> EquineSync onboarding must remain adaptive to the actual user and operating context. An individual horse owner must not be forced to create unnecessary Facility, Tenant, Organization, Barn, or Business entities when those entities do not truthfully exist or are not required for the user's legitimate workflow. The onboarding model must support horse-first and individual-owner-first entry paths while preserving the canonical distinctions, isolation rules, evidence requirements, and later explicit association of facilities or organizations when applicable.

## Controlled interpretation

Tenant remains the technical application isolation boundary for every protected record. The refinement means a user is not required to invent or manually model a Tenant as a physical/legal/operating entity and is never required to create Facility, Organization, Barn, or Business topology that does not truthfully exist. A minimum private technical Tenant isolation context may be provisioned transparently because it is required for isolation; it is not presented as a Facility, Organization, Barn, Business, relationship, stewardship, or authority.

## Required paths

1. **Individual-owner / horse-first:** identity and horse-first workflow, minimum private isolation, no Facility/Organization/Barn/Business, no authority from setup.
2. **Structured facility/organization:** explicit selection, truthful distinct entities, evidence-supported associations, visible context, action-time authorization.
3. **Later association:** explicit, auditable, reversible where applicable, and owned by Relationship/Authorization controls; no default/primary assignment.

## Proof coverage

`FAC-REQ-037` through `FAC-REQ-042`, their corresponding acceptance criteria/tests, `FAC-WF-014`, `FAC-WF-015`, `FAC-API-009`, `FAC-API-010`, `FAC-EVT-004`, `FAC-PERM-018`, `FAC-PERM-019`, and `FAC-SM-005` prove the six required outcomes at the documentary level. No implementation test is represented as executed.
