# RF1 Data Fences And Capability Gates

Date: 2026-07-06

Status: CODEX-REVIEWED & LOCKED.

## Gate Summary

RF1 addresses the P0 trust risks from RF0:

| RF0 Finding | RF1 Status | Evidence |
| --- | --- | --- |
| RF0-F01 Owner-safe horse endpoint gap | ready for review | `backend/routes/horse_ledger.py` now exposes `GET /owner/horses` and `GET /owner-portal/horses` for owner/guardian/rider roles only. |
| RF0-F02 Backend capability proof | ready for review | RF1 tests assert financial/reporting direct routes retain backend `require_permission` gates. |
| RF0-F03 QuickBooks invoice export barn scope | ready for review | QuickBooks invoice export now reads invoices with `{"barn_id": barn_id}`. |
| RF0-F04 Owner portal name/free-text access | ready for review | Owner portal media/forms/health/emergency/training/billing reads use stable owner/user/horse clauses. |
| RF0-F12 Owner payment scope | ready for review | Owner billing list and payment-prep invoice lookup are both barn-scoped and owner-identity-scoped. |
| RF0-F14 Share/publish state | deferred | RF1 did not build RF11 property/location/share-state models; this remains future work. |

## Source Changes

- `backend/routes/backlog.py`
  - Adds stable owner/user/horse helper predicates for owner portal reads.
  - Removes display/free-text name matching from owner portal access predicates.
  - Keeps billing/payment and form-signing authorization on account-recipient/payer predicates, not horse linkage alone.
  - Scopes invoice export and reporting revenue reads by barn.
- `backend/routes/horse_ledger.py`
  - Adds owner-safe horse inventory endpoints with conservative projections.
- `backend/routes/owner_updates.py`
  - Expands owner-owned horse lookup to canonical primary/secondary owner ID fields.
- `backend/core/rf1_data_fences_capability_gates_proof.py`
  - Generates read-only RF1 proof rows.
- `backend/scripts/build_rf1_data_fences_capability_gates_proof.py`
  - Writes `outputs/rf1_data_fences_capability_gates_report.md`.
- `backend/scripts/seed_local_demo_test_accounts.py`
  - Dev-only helper to make the local API and integration tests runnable with documented demo accounts.
- `backend/tests/test_rf1_data_fences_capability_gates.py`
  - Guards the RF1 source contracts.

## Important Behavior Note

RF1 prefers privacy over legacy convenience. Owner-facing backlog records that only contain `owner_name`, `recipient_name`, `horse_name`, `shared_with`, or other free-text links may no longer appear to owners until RF2/RF7 migration links them to stable IDs. Staff/admin barn-scoped reads remain available where existing roles permit them.

## Review Criteria

- No global invoice reads remain in QuickBooks export or backlog dashboard revenue proof.
- Owner-facing portal access does not depend on display names or regex shared-with text.
- Billing/payment and forms access cannot be granted by horse ID alone.
- Owner horse inventory only returns linked owner/guardian/rider horses from the caller's barn.
- Financial/reporting direct routes retain backend capability gates.
- RF1 report returns `overall_status=ready`.

## Local Run Evidence

The local backend can run at `http://127.0.0.1:8001` with MongoDB on
`127.0.0.1:27017`. Use `backend/scripts/seed_local_demo_test_accounts.py` to
repair local demo accounts when an old `test_database` already exists and
auto-seed skips.

## Deferred To Later RF Phases

- RF2: full identity-based migration for staff, provider, document, message, and legacy owner records.
- RF7: owner/guardian/rider portal UX and contract completion.
- RF11: canonical property/location/share publish state.
- RF12: billing/payment/export/refund/void truth.
- RF17: feature-shell retirement and nav truth.

## RF1 Lock Note

RF1 is locked after review/fix/review. The review finding around horse-only
authorization for sensitive billing/forms records was fixed and covered by
regression tests. RF2 may proceed as the next gated phase.
