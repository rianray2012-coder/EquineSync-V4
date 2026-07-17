# W1-RF01 Schema Impact Assessment

## Current Collections in Scope

`users`, `refresh_tokens`, `auth_tokens`, `login_attempts`, `account_memberships`, `invites`, `onboarding_progress`, `audit_log`, `barn`/`barns`, guardian/student/provider grant records, domain person/profile collections, and seed/UAT data.

## Potential Additive Fields or Records

Canonical account/actor/person IDs, session/token-family IDs, authority and policy revisions, membership/relationship effective periods, provenance, confirmation/reverification, selected context, supersession links, and migration correlation/checkpoint records.

## Constraints

- No schema is authorized by this assessment.
- Existing IDs and historical attribution must remain stable.
- Unique indexes require duplicate preflight.
- Legacy compatibility fields must remain until access-delta evidence passes.
- `barn` versus `barns` and missing-primary fallbacks must be reconciled before constraints tighten.
- High-risk identities enter quarantine rather than automatic merge.

Schema readiness: `FALSE_PENDING_SEPARATE_DESIGN_AND_AUTHORITY`.

