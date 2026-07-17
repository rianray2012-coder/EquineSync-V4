# W1-RF01 Relationship and Membership Alignment Report

Current `account_memberships` safely adds invite-derived contexts without overwriting existing users. That is a useful migration foundation, but product authorization still usually reads `users.role` and `users.barn_id`. The `/account/context` endpoint is explicitly read-only and only selected read routes consume the chosen context.

Required alignment:

- treat membership as scoped relationship evidence, not field permission by itself;
- require active, effective, non-suspended membership plus applicable relationship and permission projection;
- make context selection server-validated and bind it to request authorization;
- preserve inviter, invite, role, barn, effective dates, termination, and provenance;
- recalculate permissions on relationship, role, facility, or account-state change;
- use generic non-existence responses across barn boundaries;
- keep guardian and provider grants independent from general membership;
- retain historical memberships after access ends.

The existing compatibility mirror must not become a second permanent source of truth.

