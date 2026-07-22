# ES-PIA-RELATIONSHIP-AUTHORIZATION-PERMISSION Source Packet

**Status:** `PARTIAL_PIA_BLOCKED_BY_COMPONENT_COMPLETION_AND_FRESH_REVIEW`  
**Component A:** current Relationships successor candidate; underlying design previously approved  
**Component B:** bounded Authorization interface candidate only  
**Component C:** locked Permission canon exists; integrated PIA component not complete

## Primary evidence

- frozen Relationships PIA V1.1.0 and related controlled-sequence packages;
- `ES-REM-2026-001` candidate ADRs, source reconciliation, contracts, and acceptance mapping;
- `AUTHORIZATION_INTERFACE_PIA_CANDIDATE.md`;
- Relationship V2.0 and Permission V1.1 locked canons;
- Agreement, Consent, and Authorization V2.1;
- Claims, Audit, Records, Privacy, Safeguarding, Identity, and Facility interfaces; and
- PIA Master Standard V1.1.

## Required integrated boundary

- Component A owns relationship and delegation truth.
- Component B owns authorization inputs, evaluation request/response contracts, decision evidence, and revocation effects without creating source truth.
- Component C owns final permission evaluation and enforcement contract.
- Identity authenticates principals but does not grant authority.
- Facility/Tenant/Organization context constrains evaluation but does not grant authority.
- Payment, contact, role label, provider status, possession, or cached fact never grants authority.

## Unresolved matters

The current Component A successor and its formal ADRs are unratified. Components B and C need one canonical 43-section Item 03 package, exact five-question responses, source/requirement/workflow/entity/state/permission/acceptance/test/evidence registers, and a fresh review. Owning-domain concurrence is required for cross-contracts. No dependent PIA may invent missing Item 03 answers.
