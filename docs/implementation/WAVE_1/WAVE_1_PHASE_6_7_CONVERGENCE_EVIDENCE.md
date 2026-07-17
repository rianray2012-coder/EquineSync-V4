# Wave 1 Phases 6 and 7 Convergence Evidence

Phase 6: `WAVE_1_PHASE_6_ADDITIVE_CONVERGENCE_GATE_PASSED`

Phase 7: `WAVE_1_PHASE_7_ADDITIVE_IDENTITY_CONVERGENCE_COMPLETE`

Affected development/test structures: `account_memberships` and
`refresh_tokens`. Additions are nullable/deterministic identifiers, authority
provenance, effective dates, token-family lineage, and sparse indexes. Legacy
user role, barn, credentials, and attribution fields remain readable and were
not deleted or renamed.

The isolated `wave1_*` Mongo rehearsal processed 137 rows. Replay produced zero
new upserts; access delta and automatic merges were zero. The legacy digest was
identical before migration, after migration, after rollback, and after forward
recovery. Rollback removed only additive mirror rows; forward recovery restored
137 mappings. No production endpoint or data was used.

Machine-readable evidence:
`outputs/wave1_identity_convergence_rehearsal.json`.
