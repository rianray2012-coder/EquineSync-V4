# Founder Decision Brief

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
- Version: `1.0.0-candidate`
- Date: `2026-07-20`
- Status: `FOUNDER_DECISION_REQUIRED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.

## Decision posture

There are `28` unresolved decisions: 12 before design approval, 10 before implementation authorization, and 6 before enrollment. The package recommends a coherent model but does not adopt it. Decide the design-gate set first; the remaining questions can then be answered without reopening core definitions unless the Founder selects an alternative.

## Recommended model in one view

- Tenant: strict application isolation/governance context.
- Facility: durable physical-place identity and topology.
- Organization: durable legal/operating/admin/service entity identity.
- Barn: named operating context tied to a Facility/Area, never Tenant.
- Association, membership, role, payment and agreement: evidence inputs, never automatic authority.
- Consequential action: explicit visible context plus action-time authorization.
- Transfer/merge/closure: lineage-preserving and non-cascading.
- Public discovery: separate revocable coarse projection.
- Offline: minimum expiring reads/observations only; no consequential topology mutation.

## Highest-risk unresolved choices

1. FAC-FD-001/FAC-FD-002 — core distinctions and strict Tenant isolation. Choosing equivalence preserves the current ambiguity and is not recommended.
2. FAC-FD-008/FAC-FD-011/FAC-FD-012 — transition, relationship and authority boundaries. Any cascade or inferred authority risks cross-domain harm.
3. FAC-FD-019/FAC-FD-020 — offline and suspension behavior. Partial enforcement is a P1 risk.
4. FAC-FD-022/FAC-FD-016 — retention and public location. Both require deliberate data-risk decisions.
5. FAC-FD-017/FAC-FD-024 — first-user seed and context UX. These gate safe enrollment, not merely interface polish.

## Evidence limits

The documents were internally reviewed and revised and passed machine validation. The same Codex run used procedurally separated passes; this is not represented as an ES-RA review or a fresh external/segregated reviewer. Software was inspected statically only and is not conformant, verified, operational, or enrollment-ready.
