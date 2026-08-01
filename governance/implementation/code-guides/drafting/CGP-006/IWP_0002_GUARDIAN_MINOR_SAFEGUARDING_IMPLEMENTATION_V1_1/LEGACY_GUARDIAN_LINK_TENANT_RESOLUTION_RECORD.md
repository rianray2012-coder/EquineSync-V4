# Legacy Guardian Link Tenant Resolution Record

Status: `CORRECTED`

Legacy guardian links without `barn_id` now have one consistent rule: they fail closed unless the link carries independent barn proof and the referenced student is in the active barn.

Accepted proof fields:

- `migration_verified_barn_id` equals the active barn;
- `legacy_barn_id` equals the active barn;
- `barn_scope_verified` is true; or
- `legacy_barn_scope_verified` is true.

Links with explicit cross-barn `barn_id`, missing proof, or disagreement with the student barn are rejected with the disclosure-safe guarded-workflow response.

Evidence:

- `GMS-T-008`: explicit cross-barn Guardian link denies without leaking relationship state.
- `GMS-T-049`: missing `barn_id` without proof fails closed.
- `GMS-T-050`: missing `barn_id` with verified barn proof allows when authority and consent are otherwise valid.
