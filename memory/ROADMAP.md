# EquineSync — Roadmap & Recent Changelog Head

> See PRD.md tail for full history. This file is the rolling **most-recent** snapshot.

## ✅ Phase 14 — Admin Review Queue + Billing Lifecycle + Trials (Feb 13 2026)

### Backend
- `routes/admin_review.py` — `GET /api/admin/review-queue` (pending), `…/history`,
  `POST …/{user_id}/approve`, `POST …/{user_id}/reject` (soft, with `reason`).
  Admin-gated via `require(user, "barn:manage")`. Audit row in
  `review_decisions` collection.
- `routes/membership.py` — `POST /api/membership/start-trial` (no card, 7 days,
  one-shot per account via `trial_used` flag), `POST /api/membership/cancel`
  (MVP local flip → `subscription_status="cancelled"`, NOT a true Stripe
  subscription cancel — labelled in code), webhook now handles
  `checkout.session.expired` in addition to `checkout.session.completed`.
- `routes/auth.py::/auth/signup` — sets `subscription_status="trialing"` +
  `trial_expires_at=now+7d` + `trial_used=True` if a paid tier is included in
  the body. Welcome email via Resend wired in (best-effort, non-blocking).
- `.env` — `STRIPE_WEBHOOK_SECRET=` placeholder; production must set this.

### Frontend
- `pages/AdminReviewQueue.jsx` — Pending / History tabs, approve + reject with
  reason input, badges for status. Route at `/admin/review-queue`
  (`ROLE_GROUPS.admin`-gated). Sidebar nav entry "Member Review".
- `pages/Signup.jsx` — Step 1 always posts `tier:"free"` so Step 3 controls
  the real choice. Step 3 offers primary "Start 7-day free trial" plus
  secondary "Or pay now →" (`signup-checkout`) for paid tiers, or
  "Start with Free" for the free tier.
- `components/AppShell.jsx::MembershipBanners` — stackable banners:
  `pending-review-banner` · `rejected-banner` · `trial-banner` ·
  `cancelled-banner`. Trial banner shows live "N days left" countdown.
- `context/AuthContext.jsx` — `refreshMe()` helper so the trial/free flips
  immediately light up the right banner.

### Testing
- `tests/test_review_queue_and_lifecycle.py` — 11/11.
- `tests/test_marketplace_signup.py` — still 14/14.
- testing_agent_v3_fork iter 31: backend 25/25 · frontend 14/15 (dead-code
  testid mismatch — fixed by removing the redundant in-page forbidden guard).

### Notes
- Stripe is intentionally **one-time Checkout, not recurring Subscriptions**.
  The `/cancel-membership` endpoint is labelled "MVP" in code — flipping to
  true Stripe Subscriptions is a future phase.

## Next up (post-Phase 14)
- **P1 — True Stripe Subscriptions** (gated, separate phase): recurring
  billing, automatic re-charges, `customer.subscription.updated/deleted`
  webhooks, proration, invoices, dunning.
- **P2 — Trial expiry job**: nightly task that flips trialing→needs-payment.
- **P2 — Email sequence**: trial reminder at day 5/6/7.
- **P2 — Resume membership flow**: streamlined Checkout for cancelled users.
