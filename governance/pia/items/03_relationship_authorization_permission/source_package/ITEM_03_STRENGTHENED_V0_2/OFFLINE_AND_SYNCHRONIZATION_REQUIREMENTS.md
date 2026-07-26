# Offline and Synchronization Requirements

**Boundary:** `ONLINE_FIRST_LIMITED_FIELD_RECOVERY`
**Implementation authority:** `FALSE`

## Invariants

Offline state is a non-authoritative proposal, never a new or expanded permission. A device may not infer authority from cached roles, relationships, provider status, schedules, appointments, payments, portal visibility, or previously allowed actions. Current server-side or equivalently trusted re-evaluation is required before consequential acceptance.

## Proposal envelope

Every proposal records proposal and idempotency IDs, actor/principal chain, accountable human, tenant/context, action/resource/fields, purpose, device and session, local time and clock confidence, source-version set, policy version, restriction/revocation watermark, payload digest, reason, and local status.

## Visible states

Users must see `SAVED_LOCAL`, `QUEUED`, `SYNCING`, `BLOCKED`, `CONFLICT`, `FAILED`, `RECONCILED`, or `SUPERSEDED`. No success surface appears until the trusted evaluation accepts the action and returns evidence.

## Reconciliation order

1. Reauthenticate the current actor and principal chain.
2. Validate tenant/context and payload integrity.
3. Deduplicate by idempotency and payload digest.
4. Compare source versions, policy version, watermark, time, and clock confidence.
5. Apply current restrictions, revocations, disputes, safeguarding, and owning-domain state.
6. Reauthorize the original action and minimum fields/purpose.
7. Accept, deny, step up, conflict, or supersede with attributable evidence.

Stale, revoked, expired, disputed, wrong-tenant, duplicate, incompatible, or restriction-conflicting proposals fail closed. Ordering gaps, partial delivery, retry exhaustion, and evidence-store failure preserve the proposal and original evidence for controlled correction; they do not broaden authority.

## Conflict and correction

Current explicit restriction/revocation and authoritative source versions prevail over cached allow. Equal-authority conflicts remain blocked pending an owning-domain or human decision. Correction creates a successor proposal/result and preserves the original attempt, timestamps, versions, and reason codes.

## Provider boundary

Offline provider appointments, care notes, service completion, invoices, payments, or portal interactions cannot create provider relationship or authority. Item 03 re-evaluates provider authority; Items 07, 09, and 10 retain their domain truth.

## Deferred controls

Maximum offline duration, queue size, retry timing, watermark propagation targets, device assurance, recovery objectives, and support runbooks remain `TBD_IMPLEMENTATION_ATLAS`. No runtime or synchronization implementation is authorized.
