# W1-RF01 Account and Actor Mapping Specification

## Mapping Rules

1. Preserve every existing `users.id` as historical actor lineage.
2. Introduce canonical account and actor IDs additively; do not replace identifiers in place.
3. One account may authenticate one or more explicitly linked actors only through governed selection.
4. One actor may hold multiple time-bound memberships and relationships without collapsing roles.
5. Email is a contact/credential locator, not durable person identity.
6. Names, emails, and phone numbers must never drive automatic merges.
7. Platform authority remains separate from barn/facility authority.
8. Membership, relationship, and permission versions must support before/after evidence.
9. Ambiguous, duplicate, minor, deceased, disputed, or provider identities enter quarantine/manual review.
10. Legacy fields remain compatibility projections until access-delta evidence permits retirement.

## Proposed Additive Keys

`account_id`, `actor_id`, `person_id`, `membership_id`, `relationship_id`, `authority_revision`, and provenance/correlation fields. These are planning names, not schema authorization.

