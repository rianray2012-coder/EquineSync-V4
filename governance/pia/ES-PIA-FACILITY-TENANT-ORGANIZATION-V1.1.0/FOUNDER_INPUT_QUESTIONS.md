# Remaining Founder Input Questions

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `TEN_LATER_GATE_DECISIONS_OPEN`
- Candidate disposition before fresh review: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

## FAC-OQ-001 / FAC-FD-019

**Question:** What topology behavior is allowed offline?

**Why needed:** Stale authority can corrupt canonical topology.

**Unapproved candidate recommendation:** Permit only minimum-authorized expiring reads and context-neutral observations; no consequential topology mutation until online revalidation.

**Alternatives:** Allow offline create/move/merge; no offline access at all.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-002 / FAC-FD-020

**Question:** What happens on Tenant or Facility suspension?

**Why needed:** Safety evidence loss or unauthorized continuation.

**Unapproved candidate recommendation:** Deny ordinary consequential access across all surfaces, preserve emergency/safety evidence capture only through a narrowly controlled path, and require online revalidation for reinstatement.

**Alternatives:** Total lockout including safety evidence; allow reads/writes unchanged.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-003 / FAC-FD-021

**Question:** What support-access model is allowed?

**Why needed:** Privacy exposure or inability to resolve incidents.

**Unapproved candidate recommendation:** Use ticket-bound, reason-coded, time-limited, least-privilege, impersonation-free access with approval and immutable audit.

**Alternatives:** Standing superuser access; no support access.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-004 / FAC-FD-022

**Question:** What retention rules apply to topology, identity, projection, and evidence records?

**Why needed:** Unsupported legal precision or loss of evidence.

**Unapproved candidate recommendation:** Retain identity/lineage/audit under governed evidence rules, make public projections revocable, and set field-level schedules only after legal and operational review.

**Alternatives:** One universal duration; hard-delete the entire topology.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-005 / FAC-FD-023

**Question:** What capacity and suitability assertions may a first-user Facility or Area display?

**Why needed:** Unsafe reliance or poor planning.

**Unapproved candidate recommendation:** Treat them as dated, sourced assertions with units, confidence and limitations; never as guarantees of safety.

**Alternatives:** Static unqualified numbers; omit capacity entirely.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_

## FAC-OQ-006 / FAC-FD-024

**Question:** How is active context switching presented to users?

**Why needed:** Wrong-context changes.

**Unapproved candidate recommendation:** Show persistent Tenant/Facility/Organization context, require confirmation for consequential actions, and never silently switch because a link was opened.

**Alternatives:** Hidden automatic context; single sticky Barn.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_

## FAC-OQ-007 / FAC-FD-025

**Question:** Which canonical API commands, events, and jobs are permitted?

**Why needed:** Contract drift or unbuildable design.

**Unapproved candidate recommendation:** Use the candidate contracts as design interfaces only and require separate implementation authorization plus schema/security review.

**Alternatives:** Build directly from prose; defer all contracts.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-008 / FAC-FD-026

**Question:** What nonfunctional thresholds apply?

**Why needed:** False precision or untestable reliability.

**Unapproved candidate recommendation:** Require measured isolation, accessibility, recovery, latency and scale budgets in an authorized work package; retain qualitative gates until evidence exists.

**Alternatives:** Invent numeric thresholds now; omit quality gates.

**Gate:** `REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION`

**Founder input:** _not supplied_

## FAC-OQ-009 / FAC-FD-027

**Question:** What closure and suspension communication is required?

**Why needed:** Stranded users or excessive access.

**Unapproved candidate recommendation:** Notify affected context members through governed notice, show effective time/consequences, and preserve access only where separate authority requires it.

**Alternatives:** Immediate silent closure; indefinite full access.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_

## FAC-OQ-010 / FAC-FD-028

**Question:** What evidence is required before Founder design approval and later enrollment decisions?

**Why needed:** Status inflation and unreviewed doctrine.

**Unapproved candidate recommendation:** Resolve design-gate decisions, commission fresh segregated review, verify source/traceability gaps are zero, and record separate approval and later readiness decisions.

**Alternatives:** Treat this recommendation as approval; approve from summary alone.

**Gate:** `REQUIRED_BEFORE_ENROLLMENT`

**Founder input:** _not supplied_
