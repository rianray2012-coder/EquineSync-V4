# State Token Propagation Correction Record

Status: `IMPLEMENTED_AND_FOCUSED_TESTED`

Correction:

- `backend/routes/recurring_charges.py` now returns the authoritative payment gate result from `_payment_gate`.
- The materializer captures that result as `gate = await _payment_gate(...)` and skips invoice creation when no allowed gate is returned.
- Materialized invoice documents now include `guardian_guard_state_token` from `gate.get("state_token")`.
- The recurring-charge row update carries refreshed `guardian_guard_scope_reference` and `guardian_guard_state_token` from the in-memory authorized charge record when present.
- `backend/routes/billing.py` continues to pass invoice `guardian_guard_state_token` as `expected_state_token` and now treats minor-involved `invoice.pay` without a stored token as an explicit fail-closed retry condition.

Legacy invoice rule:

Legacy minor-involved invoices without `guardian_guard_state_token` cannot silently proceed through `invoice.pay`. The correction supplies sentinel `__missing_guardian_guard_state_token__` as the expected token, causing the central guard to return `INTERNAL_AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED` and requiring fresh authorization state.

Focused tests:

- `GMS-T-058` verifies materialized invoices copy the authoritative gate state token and preserve skip-on-block behavior.
- `GMS-T-059` verifies the missing-token `invoice.pay` fail-closed retry behavior at the central guard boundary.
- Existing prior tests `GMS-T-048`, `GMS-T-051`, and `GMS-T-054` preserve stale-token and persisted-token safeguards from PR #71.

Provider boundary:

No payment processor, provider call, provider configuration, production data access, backfill, scheduler, or deployment action was performed.
