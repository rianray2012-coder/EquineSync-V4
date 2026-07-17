# W1-RF01 Migration Scenario Analysis

| Scenario | Benefit | Risk | Recommendation |
| --- | --- | --- | --- |
| 1. No schema migration | Fastest security containment; preserves runtime model | Canonical split remains | Use for immediate hardening only |
| 2. Additive convergence | Canonical IDs, memberships, provenance without destructive rewrite | Dual-read complexity and access drift | Preferred convergence path after design/rehearsal |
| 3. Full restructuring | Cleanest long-term model | Highest lockout, attribution, migration, and rollback risk | Defer; not recommended as first runtime wave |
| 4. External IdP transition | Managed authentication capabilities | Provider dependency, account-linking and outage risk | Defer provider selection; preserve internal actor truth |

Recommended sequence is staged hybrid: Scenario 1 security controls, then Scenario 2 additive convergence. Scenario 4 may be researched later but cannot replace EquineSync actor, relationship, or permission truth.

