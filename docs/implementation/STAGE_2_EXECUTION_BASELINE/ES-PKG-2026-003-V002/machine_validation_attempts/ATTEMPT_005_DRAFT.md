# Draft Machine Validation Attempt 005

- UTC: `2026-07-20T03:47:33Z`
- Phase: `draft`
- Result: `PASS`
- Score: `41/41`
- Source recomputation: `142/142` rows, live read-only
- Snapshot recomputation: `78/78`
- Paired-format identifier parity: `24/24` pairs
- EquineSync workflow execution: not performed

The validation directly reopened immutable Git objects and all nested archive layers, compared every source-register row, recomputed the review snapshot, and checked paired-format identifiers and aggregate source-verification parity.
