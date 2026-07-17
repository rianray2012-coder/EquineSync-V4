# Master EquineSync Wave 2 Schema and Migration Gate

Disposition: `WAVE_2_ADDITIVE_SCHEMA_AND_MIGRATION_GATE_PASSED`

## Additive Changes

- Sparse canonical horse/facility identity and revision indexes.
- Request-id idempotency indexes scoped by barn.
- Horse profile history and duplicate-candidate collections.
- Additive provenance, revision, actor, facility, correlation, and timestamps.
- Existing canonical collections retain their names and records.

No field or collection is dropped or renamed. No horse is merged. No audit or
assignment history is rewritten. Legacy `locations`, `stall_assignments`, horse
stall text, and fragmented care rows remain readable during transition.

Migration is deterministic from existing stable row IDs and barn IDs. Missing
stable identity, cross-barn references, and ambiguous location mappings enter an
exception ledger. Rehearsal is local/synthetic only and must prove idempotency,
legacy checksum preservation, rollback of additive metadata, and forward
recovery before lock.

P0: `0`. Blocking schema P1: `0`. Production migration: `FALSE`.
