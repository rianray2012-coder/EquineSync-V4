# Transfer Effective Time and Continuity Contract

**Source artifact:** `ES-PIA-HORSE-IDENTITY-LIFECYCLE_V0_3_FOUNDER_APPROVED_DESIGN_BASELINE.md`
**Source sections:** `9.10`, `10`, `13.5`, `13.10`, `16`, `23`, `29`, `30`, `33`, `36`, `37`
**Decision controls:** `HOR-FD-001`, `HOR-FD-010`, `HOR-FD-012`, `HOR-FD-014`, `HOR-FD-017`
**Authority:** `DOCUMENTARY_DESIGN_ONLY`

## Required Design Contract

Transfer is a governed state machine, not an edit to an owner field. Transfer must preserve canonical Horse ID while identifying parties, authority, evidence, restrictions, disputes, purpose, source versions, and impact-specific effective times.

Relationship, custody, possession, access, care responsibility, facility assignment, communications, scheduling, financial context, record stewardship, and transfer-case completion retain separate effective times and reconciliation states. Transfer-case completion must not imply that every impact became effective at the same time.

A continuity packet is permission-filtered and must identify omissions, conflicts, stale sources, restricted items, completeness limitations, and external-copy limitations. Former parties retain only purpose-specific history permitted by current governance.

## Covered IDs

- Requirements: `HOR-REQ-050` through `HOR-REQ-062`, `HOR-REQ-110`, `HOR-REQ-111`, `HOR-REQ-112`, `HOR-REQ-117`, `HOR-REQ-120`
- Acceptance criteria: `HOR-AC-016`, `HOR-AC-017`, `HOR-AC-018`, `HOR-AC-019`, `HOR-AC-020`, `HOR-AC-046`, `HOR-AC-049`, `HOR-AC-050`
- Tests: `HOR-TST-017`, `HOR-TST-018`, `HOR-TST-019`, `HOR-TST-020`, `HOR-TST-021`, `HOR-TST-041`, `HOR-TST-054`, `HOR-TST-055`, `HOR-TST-059`, `HOR-TST-060`

## Deferred or Prohibited

No transfer workflow, access recalculation, custody operation, financial context change, downstream reconciliation, schema, migration, deployment, production use, or enrollment state is implemented or authorized by this package.
