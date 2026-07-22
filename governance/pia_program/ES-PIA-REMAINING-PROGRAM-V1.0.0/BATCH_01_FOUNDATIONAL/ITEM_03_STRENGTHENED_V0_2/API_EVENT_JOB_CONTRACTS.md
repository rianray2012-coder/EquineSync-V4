# API, Event, and Job Contracts

**Status:** `DOCUMENTARY_DESIGN_NOT_IMPLEMENTED`

## API request contract

`RAP-API-001` requires request ID, correlation ID, tenant/context, authenticated and acting actors, represented principal, accountable human, action, resource, fields, purpose, source-version set, policy version, restriction/revocation watermark, time, freshness, device/sync state, and idempotency key. Missing or incompatible fields fail closed.

`RAP-API-002` returns `ALLOW_BOUNDED`, `DENY`, or `STEP_UP_REQUIRED`, the minimum projection, safe reason codes, evaluated versions, watermark, generation, issue/expiry times, obligations, and evidence reference. The response does not disclose restricted relationship facts to an unauthorized caller.

## Event contracts

- `RAP-EVT-001 RELATIONSHIP_VERSION_CHANGED`
- `RAP-EVT-002 REPRESENTATION_VERSION_CHANGED`
- `RAP-EVT-003 DELEGATION_ACTIVATED`
- `RAP-EVT-004 DELEGATION_REVOKED_OR_EXPIRED`
- `RAP-EVT-005 RESTRICTION_CHANGED`
- `RAP-EVT-006 REVOCATION_WATERMARK_ADVANCED`
- `RAP-EVT-007 DISPUTE_STATE_CHANGED`
- `RAP-EVT-008 AUTHORITY_SOURCE_INVALIDATED`
- `RAP-EVT-009 CORRECTION_SUPERSEDED_SOURCE`

Each event carries event ID/version, tenant, subject, affected scope, source owner, accountable actor, prior/new version references, effective/recorded times, correlation, reason class, watermark, and evidence reference. Events contain minimum necessary data and are not themselves permission grants.

## Job contracts

- `RAP-JOB-001` expires time-bound delegations and advances the affected watermark under an explicit rule.
- `RAP-JOB-002` invalidates projections after restriction, revocation, dispute, or source-version change.
- `RAP-JOB-003` reconciles non-authoritative offline proposals through current reauthentication and reauthorization.
- `RAP-JOB-004` verifies evidence completeness and raises an attributable exception without repairing authority silently.
- `RAP-JOB-005` produces correction/supersession linkage without destructive history.

Jobs use a named system actor, accountable owner, narrow purpose, tenant scope, versioned policy, idempotency, bounded retries, dead-letter evidence, and human escalation. They may not activate relationships, renew delegations, resolve disputes, expand provider authority, or convert profile/API/appointment/payment/portal states into authority.

## Integration boundary

External identities, credentials, provider directories, professional registers, schedules, appointment systems, payment systems, and portals supply claims or context only. Canonical acceptance and permission evaluation occur under Item 03 and owning-domain controls. No integration is activated by this document.
