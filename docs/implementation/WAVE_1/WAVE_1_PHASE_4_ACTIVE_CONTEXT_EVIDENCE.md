# Wave 1 Phase 4 Active-Context Evidence

State: `WAVE_1_PHASE_4_ACTIVE_CONTEXT_HARDENING_COMPLETE`

The optional `X-Equine-Account-Context` header selects only an authenticated
account's active, effective membership. Unknown, cross-account, pending,
expired, and future memberships are rejected. Role and barn are projected from
the selected membership with authority provenance. Selection emits
`identity.context.selected`.

The default path preserves documented legacy compatibility. Explicit selection
never broadens authority through legacy `users.role` or `users.barn_id`.
Deterministic canonical account and actor identifiers are additive. Tests cover
owned context, unrelated context, pending/expired/future state, multi-role
projection, provider/trainer compatibility boundaries, and stable identifiers.

Access delta from the isolated convergence rehearsal: `0` broadened,
`0` narrowed, `0` ambiguous automatic merges across 137 synthetic/legacy-safe
rows. Legacy values and historical attribution remained unchanged.
