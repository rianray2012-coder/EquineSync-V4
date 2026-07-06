# Build-Next-15B - Billing Webhook Entitlement Hardening

Status: Codex-approved & locked.

## Purpose

BN15B hardens the Stripe subscription webhook mirror so billing events cannot
mark themselves successful while leaving subscription, barn, or entitlement
rows in an unsafe partial state.

This phase is a backend billing correctness phase. It does not add checkout
features, public pricing changes, Apple billing, add-on mutations, hard usage
enforcement, Admin Portal capabilities, role-home UX, landing-page behavior, or
new product workflows.

## Locked Fixes

- `checkout.session.completed`, `customer.subscription.created`, and the
  no-local-row bootstrap path for `customer.subscription.updated` now resolve
  plan codes through the guarded entitlement resolver before writing
  subscription or barn mirrors.
- Unknown or unresolvable plan codes remain retryable metadata failures instead
  of writing OK billing rows with empty entitlement snapshots.
- Legacy/founder-facing plan aliases continue to normalize through the canonical
  entitlement vocabulary.
- Canceled/deleted inactive subscription paths clear the barn mirror back to the
  free-plan entitlement limits.
- The focused 15B test module now resolves the backend import path from the
  local checkout instead of hardcoding `/app/backend`.

## Guardrails

- No Stripe secret keys are stored in code or docs.
- No Stripe API catalog provisioning changes.
- No Apple receipt validation or App Store server notification work.
- No checkout UI or Customer Portal UI changes.
- No subscription add-on mutation behavior.
- No hard usage enforcement behavior.
- No Phase 9 invoice behavior changes.
- No Admin Portal response-shape expansion.

## Verification

Focused verification completed on July 2, 2026:

- `backend/tests/test_subscriptions_15b.py`
- `backend/tests/test_phase15r_entitlements.py`
- `backend/tests/test_phase15r_migration_dry_run.py`

Result:

```text
70 passed
```

Python compile check also passed for:

- `backend/routes/subscriptions_webhook_handlers.py`
- `backend/tests/test_subscriptions_15b.py`

## Lock

BN15B is Codex-approved and locked. Review found no remaining blocking or
non-blocking findings in the BN15B scope.

## Deferred

- Full live Stripe checkout/UAT evidence against production objects.
- Add-on subscription item mutation.
- Apple in-app subscription receipt validation.
- App Store Server Notifications.
- Hard usage enforcement and upgrade-blocking flows.
- Public pricing/plan comparison polish.
