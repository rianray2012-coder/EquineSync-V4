# W1-RF01 Identity Source-of-Truth Matrix

| Question | Current authority | Target authority |
| --- | --- | --- |
| Can credentials authenticate? | `users.password_hash`, auth token stores | Canonical account credential binding |
| Which historical user acted? | `users.id` | Immutable actor ID linked to account |
| Which barn is active? | Primarily `users.barn_id`; selected read routes use account context | Explicit active membership context |
| Which role applies? | `users.role` | Scoped, versioned membership/relationship role |
| Is platform administration allowed? | `users.platform_role` | Separate versioned platform authority |
| Can a field be viewed? | Route-specific role/capability/relationship checks | Permission Model projection |
| Is a provider authorized? | Explicit grants plus role-specific code | Time-bound relationship/grant authority |
| Is a guardian authorized? | Guardian/student records plus role checks | Verified guardian relationship and permission projection |

**Result:** the authoritative credential and immediate runtime identity source is `users`, while authorization truth is distributed. The system does not yet satisfy one canonical account plus one canonical actor across all scopes.

`W1_RF01_PHASE_1_INVENTORY_COMPLETE`

