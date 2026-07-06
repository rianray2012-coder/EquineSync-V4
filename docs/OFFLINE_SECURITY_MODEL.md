# Offline Security Model

Date: 2026-07-05

Purpose: define the security boundaries for any EquineSync offline, draft, retry, or lock-screen recovery behavior.

## Security Principle

Offline support must not weaken EquineSync role, barn, owner, guardian, rider, provider, billing, or admin boundaries. Local device storage is a convenience layer only. The backend remains authoritative for permissions, ownership, facility membership, subscription status, owner-safe projections, and audit behavior.

## Data Classification

| Data class | Local storage allowed | Notes |
| --- | --- | --- |
| Auth token | No new storage beyond existing auth model | Do not duplicate tokens into offline queues or debug files. |
| Passwords or one-time passwords | Never | Must not appear in screenshots, logs, docs, queues, reports, or local drafts. |
| Stripe IDs, prices, customers, subscriptions | Never in owner/staff queues | Billing provider data stays online-only and admin-safe. |
| DocuSign envelope IDs/status | Online-only unless explicitly approved | Provider/legal data should not be cached for general offline use. |
| Owner-safe horse updates | Only through owner-safe projection | No staff notes, alert triggers, raw daily-check payloads, source IDs, or audit diffs. |
| Staff notes and internal care details | Draft/queue allowed only for the staff actor | Must be scoped to actor, barn, horse, and operation type. |
| Medical-like notes and incidents | Strong caution | Require explicit conflict handling and founder acceptance. |
| Admin portal data | No | Admin surfaces remain online-only. |

## Local Queue Requirements

Any queued write must store:

- Actor user id.
- Active role/context id.
- Barn id.
- Target entity id.
- Operation type.
- Minimal payload.
- Client request id.
- Created timestamp.
- Retry count.
- Last error summary.

Any queued write must not store:

- Auth tokens.
- Passwords.
- Raw Stripe IDs.
- Raw DocuSign private keys or secrets.
- Provider secret values.
- Full audit diffs.
- Owner-hidden staff notes in owner-visible queues.

## Backend Requirements

The backend must:

- Re-check auth and role permissions at sync time.
- Re-check active facility/membership at sync time.
- Reject cross-barn and cross-role replay.
- Use idempotency keys for queued writes.
- Emit audit rows only after accepted writes.
- Avoid creating denial artifacts where the locked privacy model says denial should be a plain 403 with no record.
- Return conflict responses when server state changed.
- Keep owner projection backend-authoritative after sync.

## Conflict Model

Conflicts must not auto-merge sensitive care or safety data silently. The minimum accepted conflict states are:

- Pending retry.
- Requires review.
- Superseded by server.
- Rejected by permission change.
- Rejected by facility disabled.
- Rejected by stale version.

Conflict review must show safe summaries. It must not expose staff-only fields to owners or provider-only fields to unrelated roles.

## Lock-Screen Recovery

Lock-screen recovery must preserve unsaved user work only for the same browser profile and user session. On resume:

- Confirm current user is still authenticated.
- Confirm current role/context still matches the draft.
- Show a clear pending/draft state.
- Require explicit retry or submit when appropriate.
- Clear draft after successful save.

If auth expires, the user should be asked to sign in again before any queued write is sent.

## Logging And Evidence Rules

- No screenshots may include passwords, auth tokens, API keys, Stripe IDs, DocuSign secrets, or private keys.
- Evidence reports may include role labels, workflow names, status booleans, and redacted identifiers only.
- Test data must be tagged as UAT/demo/test where applicable.
- Production proof must not insert demo fixtures unless an approved production-safe seed script is used.

## Founder Acceptance Required

Founder acceptance is required before launch for:

- Any workflow intentionally kept online-only.
- Any workflow using local storage for sensitive data.
- Any workflow that cannot survive lock screen, refresh, tab close, or signal drop.
- Any workflow with manual conflict review rather than automatic sync.
- Any workflow that remains web-only while app-store launch is deferred.
