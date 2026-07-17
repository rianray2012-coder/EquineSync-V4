# W1-RF01 Authorization Enforcement Assessment

## Strengths

JWT claims are not trusted as the final role/barn authority; protected requests re-read the user. Unknown capabilities fail closed. Barn filters overwrite caller-provided barn scope. Platform roles are separately allowlisted. Newer Passport, Care Circle, provider, facility, and Calendar work contains relationship and projection safeguards.

## Gaps

- Direct role checks and centralized capabilities coexist.
- `role_status` is not part of central authorization.
- Membership-aware context is not universal.
- Frontend role maps mirror backend policy manually.
- Relationship, guardian, provider, and horse-object checks remain domain-specific.
- Role/relationship revisions do not automatically invalidate access tokens.
- Some routes rely on broad role groups rather than object-level relationships.

Authorization readiness is `NOT_READY_FOR_BROAD_RUNTIME_CHANGE`; a bounded hardening RF can be considered.

