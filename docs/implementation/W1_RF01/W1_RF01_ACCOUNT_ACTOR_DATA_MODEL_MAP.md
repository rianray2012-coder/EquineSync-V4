# W1-RF01 Account and Actor Data Model Map

| Canon concept | Current representation | Alignment |
| --- | --- | --- |
| Account | `users` credential/profile document | Conflated with person and actor |
| Actor | `users.id` plus role fields | Implicit, not independently versioned |
| Person | User/profile/owner/rider/guardian records | Duplicated by domain |
| Organization | Barn/facility records and account context | Partial |
| Facility | `barns`/legacy `barn`; `barn_id` | Distinct data exists, identity link is legacy |
| Membership | `account_memberships` plus `users.role/barn_id` | Transitional dual representation |
| Relationship | Role fields, memberships, provider/guardian/domain grants | Distributed |
| Authority | Role/capability checks and platform role | Provenance incomplete |
| Session | JWT plus refresh-token document | Active but no canonical session entity |
| Device | User-agent/IP on refresh token | Observational only |

The safe target is additive account/actor identifiers and versioned memberships while retaining historical `users.id` attribution.

