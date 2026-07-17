# W1-RF01 Rollback and Forward-Recovery Plan

| Scenario | Rollback posture | Required safeguards |
| --- | --- | --- |
| Existing-foundation hardening | Feature-flag or code rollback; data-neutral where possible | Old/new auth parity tests; session invalidation plan |
| Additive convergence | Disable new reads/writes and retain additive rows | Idempotency, lineage, checkpoints, access-delta ledger, no legacy deletion |
| Full restructuring | Rollback difficult after identity writes | Dual-run, immutable mapping, restore rehearsal, forward-recovery preference |
| External IdP | Disable adapter and retain internal login fallback where approved | Account-link provenance, provider outage mode, no provider-owned actor truth |

Stop on unexplained access expansion, lockout, attribution loss, duplicate actors, unresolved mapping, cross-tenant delta, non-idempotent replay, or inability to restore authentication.

Rollback must never erase historical actor attribution or accepted relationship evidence.

