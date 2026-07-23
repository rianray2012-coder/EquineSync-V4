# Duplicate, Merge, and Unmerge Contract

**Source artifact:** `ES-PIA-HORSE-IDENTITY-LIFECYCLE_V0_3_FOUNDER_APPROVED_DESIGN_BASELINE.md`
**Source sections:** `9.4`, `10`, `13.6`, `15.4`, `23`, `29`, `30`, `32`, `37`
**Decision controls:** `HOR-FD-002`, `HOR-FD-016`
**Authority:** `DOCUMENTARY_DESIGN_ONLY`

## Required Design Contract

A possible duplicate opens a governed duplicate case. No duplicate or merge decision may rely only on name, color, breed, owner, facility, photo similarity, DNA/pedigree similarity, vendor ID, external identifier, payment, possession, or AI recommendation.

Merge requires explicit Item 03 authority, multi-source evidence, conflict review, lineage preservation, permission recalculation, and downstream reference reconciliation. Merge must preserve candidate IDs, source records, restrictions, disputes, prior decisions, and durable redirects or tombstones.

Merge must not grant access to records a user could not previously view. An incorrect merge must be reversible through governed unmerge or split correction, with source evidence and downstream references preserved.

The layered identity posture approved in `HOR-FD-016` is documentary only. It does not select a schema or service form and does not authorize cross-tenant convergence.

## Covered IDs

- Requirements: `HOR-REQ-040` through `HOR-REQ-049`, `HOR-REQ-089`, `HOR-REQ-092`, `HOR-REQ-101` through `HOR-REQ-104`, `HOR-REQ-108`, `HOR-REQ-119`
- Acceptance criteria: `HOR-AC-008`, `HOR-AC-009`, `HOR-AC-010`, `HOR-AC-011`, `HOR-AC-036`, `HOR-AC-041`, `HOR-AC-042`, `HOR-AC-044`
- Tests: `HOR-TST-005`, `HOR-TST-014`, `HOR-TST-015`, `HOR-TST-016`, `HOR-TST-038`, `HOR-TST-046`, `HOR-TST-048`, `HOR-TST-052`

## Deferred or Prohibited

No merge, unmerge, split correction, cross-tenant matching, schema, migration, model, AI, data repair, production, or enrollment behavior is implemented or authorized by this package.
