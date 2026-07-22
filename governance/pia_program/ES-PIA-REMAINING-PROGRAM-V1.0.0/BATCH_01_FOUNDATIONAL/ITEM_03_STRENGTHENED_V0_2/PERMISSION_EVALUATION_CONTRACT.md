# Permission Evaluation Contract

**Contract ID:** `RAP-CONTRACT-PERMISSION-001`
**Status:** `DOCUMENTARY_CANDIDATE_NOT_IMPLEMENTATION_AUTHORITY`

## Boundary

Authorization assembles and evaluates current source inputs for one request. Permission is the minimum enforceable projection returned by that evaluation. Identity, account, actor, role, relationship, representation, delegation, agreement, context, payment, provider status, schedule, onboarding, API, appointment, and portal state are inputs or external facts; none alone is permission.

## Required request

Every request carries `request_id`, `correlation_id`, authenticated actor, acting actor, represented principal when applicable, accountable human, tenant/context, action, resource, requested fields, purpose, current time, device/sync state, source versions, policy version, restriction/revocation watermark, and requested duration.

Input identifiers and freshness requirements are defined in `AUTHORIZATION_INPUT_REGISTER.csv`. Missing, unverifiable, stale, disputed, revoked, expired, wrong-tenant, incompatible, or restriction-conflicting material fails closed.

## Evaluation order

1. Validate request integrity, tenant isolation, action, resource, fields, and purpose.
2. Authenticate and attribute the actor chain; require an accountable human for authority-changing action unless a separately authorized named system action applies.
3. Resolve canonical identity and context without treating either as authority.
4. Resolve current relationship and representation evidence.
5. Validate delegation scope, source authority, acceptance, time, restrictions, disputes, and chain depth.
6. Apply current agreement, consent, safeguarding, claims, and owning-domain constraints.
7. Apply explicit restriction, revocation, expiry, dispute, and protective narrowing before any allow rule.
8. Evaluate the versioned policy and return the minimum projection.
9. Record exact versions, watermark, outcome, reasons, expiry, evidence, and correction lineage.

## Outcomes

- `ALLOW_BOUNDED`: returns only the allowed action, resource, fields, purpose, tenant, time, state, and obligations.
- `DENY`: returns safe reason codes without protected-data leakage.
- `STEP_UP_REQUIRED`: identifies the permitted assurance step without pre-authorizing the requested action.

There is no implicit allow. A cached prior allow is not reusable after its expiry, source-version change, restriction/revocation-watermark change, tenant/context change, purpose change, or incompatible policy change.

## Restriction and conflict precedence

Current explicit restriction, revocation, protective narrowing, dispute hold, legal hold, source invalidation, and policy incompatibility take precedence over role, relationship, delegation, agreement, payment, appointment, provider, portal, schedule, or cached allow. Conflict resolution never broadens access. Unresolved equal-authority conflict returns `DENY` or `STEP_UP_REQUIRED` under a controlling policy.

## Response and evidence

The response carries outcome, minimum projection, safe reason codes, evaluated source and policy versions, restriction and revocation watermark, generation, issued time, expiry, step-up requirement, obligations, correlation, and evidence reference. `AUDIT_AND_EVIDENCE_REQUIREMENTS.csv` defines the reconstruction minimum.

## Offline boundary

An offline device may preserve a non-authoritative proposal but may not issue a new or expanded permission. Synchronization must reauthenticate and re-evaluate the entire current request. `OFFLINE_AND_SYNCHRONIZATION_REQUIREMENTS.md` controls failure and reconciliation.

## Authority limitation

This contract is documentary design only. It does not authorize code, schema, policy deployment, provider execution, migration, activation, production use, or enrollment.
