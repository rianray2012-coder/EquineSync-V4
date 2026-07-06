# Build-Next-15C-B - Barn Visibility Policy

Status: Codex-approved & locked

Date: 2026-07-02

## Purpose

BN15C-B adds a barn-level choice for community-style versus siloed owner-safe
summary visibility.

Some barns operate as communities where owners help with, see, or ride other
owners' horses. Other barns are intentionally siloed around each owner's own
horse. This phase lets a barn owner or barn manager choose whether owner,
guardian, and rider role-home views may see the barn-wide total horse count.

## Scope

Included:

- New `barn_visibility_policies` read/write surface behind `/api/pulse`.
- New manager-only endpoints:
  - `GET /api/pulse/visibility-policy`
  - `PUT /api/pulse/visibility-policy`
- Default-safe policy mode: `siloed`.
- `community` mode exposes only `horse_care.horses` to owner-safe facility
  roles.
- Settings page card for barn leaders:
  - `Siloed`
  - `Community Count`
- Focused tests for default behavior, community count behavior, custom false
  behavior, normalization, membership-scoped authorization, and frontend
  source guards.

Excluded:

- No staff notes.
- No raw daily-check payloads.
- No alert triggers.
- No `source_check_id`.
- No audit diffs.
- No Stripe IDs.
- No billing, entitlement, checkout, Apple, DocuSign, Admin Portal, task,
  HorseOps, notification-delivery, Text/SMS, push, native mobile, offline sync,
  AI, scheduler, or workflow-engine behavior changes.

## Privacy Model

The only owner-safe summary count added in this phase is:

- `owner_safe_summary_counts.total_horses`

The following remain hidden from owner-safe facility roles even in community
mode:

- open alert counts,
- urgent alert counts,
- alert details,
- staff notes,
- request details,
- care payload internals,
- audit details,
- billing/private subscription fields.

Unknown policy modes fail closed to `siloed`. Unknown toggle keys are ignored.

## Round-1 Fix

Codex review found that the first version authorized visibility-policy changes
from `user.role` instead of the resolved active facility membership role. That
would let a multi-role user who is a manager in one barn update policy for a
second barn where they are only an owner.

Fixed:

- Backend resolves the requested facility context first.
- Backend authorizes using `active_context.role` and requires active facility
  membership.
- Frontend Settings card reads `/api/account/context` and gates the card on the
  active facility membership role instead of the global user role.
- New regressions cover both sides:
  - global manager + requested owner-only membership => `403`;
  - global owner + requested manager membership => allowed.

## Round-2 Fix

Codex re-review found the policy endpoint was fixed, but the main
`GET /api/pulse/today` response still derived facility card visibility from
the global `user.role`.

Fixed:

- Facility Today Pulse cards now use the resolved active/requested membership
  role.
- `scope.role` now reflects the effective facility membership role for facility
  contexts.
- New regressions cover:
  - global manager + requested owner-only membership => owner-safe cards only;
  - global owner + requested manager membership => manager cards allowed.

## Verification

Focused tests:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_15a_today_pulse_contract.py \
  backend/tests/test_build_next_15c_a_today_pulse_frontend_wiring.py \
  backend/tests/test_build_next_15c_b_barn_visibility_policy.py -q
```

Result:

- 22 passed.

Frontend build:

```bash
cd frontend
CI=false GENERATE_SOURCEMAP=false npm run build
```

## Review Checklist

- Owner-safe roles default to zero barn-wide horse count.
- `community` policy exposes only total horse count.
- Owner-safe alert counts remain zero.
- Settings page does not mention or bind `open_alerts` / `urgent_alerts`.
- Today Pulse route remains read-only; only policy PUT writes.
- Zip integrity passes.

## Lock Note

BN15C-B is Codex-reviewed and locked. Round-1 and Round-2 findings are closed:
visibility-policy writes and Today Pulse facility card reads both derive authority
from the resolved active/requested membership role, not the global user role.

Recommended next gate:

- BN15C-C - Today's Pulse role-home evidence and UX hardening.
