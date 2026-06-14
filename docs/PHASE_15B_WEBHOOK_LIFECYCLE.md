# Phase 15.B — Webhook Lifecycle Operational Reference

> Implementation of the approved v2 plan. Status-gated idempotency model
> with 10 handler groups / 11 Stripe event types.

## Status enum (closed set, `billing_events.processing_status`)

| Status | Meaning | Replay behavior |
|---|---|---|
| `processing` | An attempt is currently in flight | Recent → return **409**. Stale (older than `BILLING_EVENTS_STALE_LOCK_SECONDS`, default 60s) → reclaim and replay |
| `ok` | Handler completed successfully | Short-circuit, return 200 + `idempotent: True` |
| `retry_502` | Stripe / motor transient failure inside handler | Replay handler, `$inc retry_count` |
| `metadata_missing_retryable` | Domain row needed for resolution hasn't synced yet | **HTTP 503** so Stripe replays. Row persisted with this status |
| `metadata_missing_permanent` | Event references state we have no record of | Short-circuit 200 |
| `unknown_event` | Event type outside the 11-type set | Short-circuit 200 |

## Pipeline diagram

```
inbound webhook
  │
  ▼
billing_events.find_one(stripe_event_id)
  │
  ├── exists & status ∈ {ok, unknown_event, metadata_missing_permanent}
  │     → 200 idempotent
  │
  ├── exists & status == processing
  │     ├── stale (age > BILLING_EVENTS_STALE_LOCK_SECONDS) → reclaim, replay
  │     └── recent                                          → 409 in_flight
  │
  ├── exists & status ∈ {retry_502, metadata_missing_retryable}
  │     → claim ($set processing, $inc retry_count), replay handler
  │
  └── new (insert claim row, processing_status="processing")
        → run handler
              ├── success                              → status=ok, 200
              ├── _MetadataMissing(retryable=True)     → status=metadata_missing_retryable, 200
              ├── _MetadataMissing(retryable=False)    → status=metadata_missing_permanent, 200
              ├── _TransientStripeError                → status=retry_502, 502
              └── handler crash (other exception)      → status=retry_502, 502
```

## Handler groups (10 / 11 event types)

| Group | Stripe event type(s) | Resolves `barn_id` via | Missing → |
|---|---|---|---|
| 1 | `checkout.session.completed` | `session.metadata.barn_id` | metadata_missing_permanent |
| 2 | `customer.subscription.created` | (a) `obj.metadata.barn_id` (b) local `subscriptions` row | metadata_missing_retryable |
| 3 | `customer.subscription.updated` | local `subscriptions` row (refresh entitlements if price changed) | metadata_missing_retryable |
| 4 | `customer.subscription.deleted` | local `subscriptions` row | metadata_missing_permanent |
| 5 | `customer.subscription.trial_will_end` | local `subscriptions` row → metadata | metadata_missing_retryable |
| 6 | `invoice.created` | local subscription by `obj.subscription` → by `obj.customer` | metadata_missing_retryable |
| 7 | `invoice.finalized` | same | metadata_missing_retryable |
| 8 | `invoice.paid` | local subscription_invoice → fallback subscription | metadata_missing_retryable |
| 9 | `invoice.payment_failed` | same | metadata_missing_retryable |
| 10 | `payment_intent.succeeded` + `payment_intent.payment_failed` | local subscription_invoice → fallback subscription | metadata_missing_retryable |

## Email side-effects

`subscriptions.pending_emails: [str]` — additive set via `$addToSet`.
Possible values: `trial_will_end`, `payment_succeeded`, `payment_failed`.
15.D will consume by reading + `$pull`-ing on send. **15.B never sends email.**

## Invariants

- **Phase 9 boundary**: `db.invoices` collection is never touched. Enforced by
  `test_phase9_invoices_collection_untouched`.
- **No raw Stripe payloads** in `billing_events.summary` or any collection.
  Only the deliberately-listed fields are persisted. Card data limited to
  `payment_method_brand` + `payment_method_last4`.
- **No frontend / email / hard-enforcement / admin-dashboard** in 15.B.
- **Production fail-fast** on missing `STRIPE_API_KEY` / `STRIPE_PRICE_*` —
  same contract as 15.A (re-raised by `lifespan.on_startup`).

## Env

```
BILLING_EVENTS_STALE_LOCK_SECONDS=60   # how long before a `processing` lock is reclaimable
```
