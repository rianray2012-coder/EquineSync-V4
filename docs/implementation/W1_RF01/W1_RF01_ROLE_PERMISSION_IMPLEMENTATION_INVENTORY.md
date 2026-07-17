# W1-RF01 Role and Permission Implementation Inventory

| Plane | Implementation | Risk |
| --- | --- | --- |
| Barn role | `users.role` and direct route checks | Broad, single-role, legacy source |
| Capabilities | `backend/core/permissions.py` | Central map exists but not universally wired |
| Platform role | `users.platform_role` | Correctly separated from barn role; assignment governance still required |
| Frontend mirrors | `frontend/src/lib/permissions.js` | Navigation only; can drift and is not authoritative |
| Barn scope | `users.barn_id`, `barn_filter()` | Strong basic isolation; single-context limitation |
| Account-context reads | membership-aware helpers on selected reads | Pilot only, not universal |
| Guardian/provider access | relationship/grant-specific route logic | Domain-specific and uneven |
| Role status | `role_status` | Recorded but not consumed by central capability evaluation |

Highest-risk mismatch: marketplace users may self-select trainer, barn-owner, or service-provider roles, receive sessions, and then encounter guards that evaluate only `role`, not `role_status`.

