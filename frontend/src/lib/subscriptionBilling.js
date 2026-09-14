// Phase 15.C — shared helpers for the Subscription Billing UI. Pure
// front-end utilities; no network calls. Source data: GET /api/billing/plans
// (see backend/routes/subscriptions.py::list_plans).

// Display order — mirrors backend PLAN_CATALOG in core/billing_provisioning.py.
// "free" is the invited owner portal/local finalize tier; public paid tiers
// use Stripe Checkout; custom-contract plans route to Contact Sales.
export const PLAN_ORDER = [
  "free",
  "individual_owner",
  "service_provider_free",
  "service_provider_premium",
  "private_owner_plus",
  "starter_barn",
  "advanced_barn",
  "elite_barn",
  "trainer_no_lesson",
  "trainer_lesson_15",
  "trainer_lesson_50",
  "enterprise",
  "community_program",
];

export const SUBSCRIBABLE_TIERS = new Set([
  "individual_owner",
  "service_provider_premium",
  "private_owner_plus",
  "starter_barn",
  "advanced_barn",
  "elite_barn",
  "trainer_no_lesson",
  "trainer_lesson_15",
  "trainer_lesson_50",
]);

export const sortPlans = (plans) => {
  const idx = (t) => {
    const i = PLAN_ORDER.indexOf(t);
    return i === -1 ? 999 : i;
  };
  return [...(plans || [])].sort((a, b) => idx(a.tier_code) - idx(b.tier_code));
};

// Convert cents → "$1,499" / "$149.99" string. Strips trailing .00.
export const formatCents = (cents) => {
  if (cents == null) return "—";
  const dollars = cents / 100;
  const hasFraction = Math.round(dollars) !== dollars;
  return `$${dollars.toLocaleString(undefined, {
    minimumFractionDigits: hasFraction ? 2 : 0,
    maximumFractionDigits: 2,
  })}`;
};

// D-14 (Sep 2026) — billing cycles the catalog can sell, in display order.
// Mirrors BILLING_PERIODS in backend/core/billing_provisioning.py. The
// six-month term exists because Apple caps auto-renewable subscriptions at
// $1,000.00: Advanced Barn and Trainer + Lessons (50) sell monthly + six-month
// in-app, and the web offers the identical six-month price so parity holds.
// A plan without `six_month_price_cents` simply does not offer the term.
export const BILLING_CYCLES = ["monthly", "six_month", "annual"];

export const CYCLE_LABEL = {
  monthly: "Monthly",
  six_month: "6-month",
  annual: "Annual",
};

// Suffix shown after a price for each cycle.
export const CYCLE_SUFFIX = {
  monthly: "/mo",
  six_month: "/6 mo",
  annual: "/yr",
};

export const CYCLE_MONTHS = { monthly: 1, six_month: 6, annual: 12 };

const CYCLE_PRICE_FIELD = {
  monthly: "monthly_price_cents",
  six_month: "six_month_price_cents",
  annual: "annual_price_cents",
};

const CYCLE_HAS_FIELD = {
  monthly: "has_monthly",
  six_month: "has_six_month",
  annual: "has_annual",
};

// Catalog amount (cents) for a cycle, or null/undefined when the plan does
// not offer that term (e.g. six_month on most tiers).
export const priceForCycle = (plan, cycle) => plan?.[CYCLE_PRICE_FIELD[cycle]];

// True when the catalog lists an amount for the cycle (independent of Stripe
// readiness — see isPlanCheckoutable for the price-ID gate).
export const planOffersCycle = (plan, cycle) =>
  !!plan && !plan.contact_sales && priceForCycle(plan, cycle) != null;

// Cycles a plan lists a price for, in display order.
export const offeredCycles = (plan) => BILLING_CYCLES.filter((c) => planOffersCycle(plan, c));

// Cycle to actually display/charge when the user's chosen cycle isn't offered
// by this plan: fall back to monthly (never silently upgrade to annual).
export const effectiveCycle = (plan, cycle) => (planOffersCycle(plan, cycle) ? cycle : "monthly");

// Savings versus paying monthly for the same number of months: rounded whole
// percent. Returns null when a price is missing or the term isn't a discount.
export const savingsPctForCycle = (plan, cycle) => {
  const m = plan?.monthly_price_cents;
  const a = priceForCycle(plan, cycle);
  const months = CYCLE_MONTHS[cycle];
  if (!months || months === 1) return null;
  if (m == null || a == null || m <= 0 || a <= 0) return null;
  const full = m * months;
  if (a >= full) return null;
  return Math.round(((full - a) / full) * 100);
};

// Annual-vs-monthly savings: rounded whole percent. Returns null when one of
// the prices is missing or the annual price isn't actually a discount.
export const annualSavingsPct = (plan) => savingsPctForCycle(plan, "annual");

// Friendly label for a subscription status returned by /api/subscriptions/me.
export const STATUS_LABEL = {
  trialing: "Free trial",
  active: "Active",
  past_due: "Payment past due",
  unpaid: "Unpaid",
  canceled: "Canceled",
  incomplete: "Awaiting first payment",
  incomplete_expired: "Checkout expired",
  paused: "Paused",
};

// `StatusPill` tone for each status using approved brand/status tokens only.
export const STATUS_TONE = {
  trialing: "info",
  active: "success",
  past_due: "warning",
  unpaid: "warning",
  canceled: "critical",
  incomplete: "warning",
  incomplete_expired: "critical",
  paused: "neutral",
};

// Statuses where the user should see a "Resume membership" CTA. Mirrors the
// 15.B webhook lifecycle states that take a barn off paid access.
export const RESUMABLE_STATUSES = new Set([
  "canceled",
  "past_due",
  "incomplete_expired",
  "unpaid",
]);

// Days remaining until an ISO timestamp; never negative. Returns null if the
// timestamp is missing or unparseable.
export const daysUntil = (iso) => {
  if (!iso) return null;
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return null;
  return Math.max(0, Math.ceil((t - Date.now()) / 86_400_000));
};

// Phase 15.C — Stripe price-ID readiness gate. `/api/billing/plans` returns
// `has_monthly` / `has_six_month` / `has_annual` based on the presence of a
// Stripe Price ID for the cycle on the backend. When false, `/api/
// subscriptions/checkout` raises HTTP 500 ("missing a Stripe Price for
// cycle=…"). The UI must disable any CTA that would otherwise hit that 500
// and surface a "Billing setup pending" message instead. Contact-sales plans
// are always considered un-checkoutable here — those use mailto.
export const isPlanCheckoutable = (plan, cycle) => {
  if (!plan || plan.contact_sales) return false;
  if (cycle) return !!plan[CYCLE_HAS_FIELD[cycle]];
  return BILLING_CYCLES.some((c) => !!plan[CYCLE_HAS_FIELD[c]]);
};

// Cycles the plan can be checked out on right now (price ID present).
export const checkoutableCycles = (plan) =>
  BILLING_CYCLES.filter((c) => isPlanCheckoutable(plan, c));

// Returns the first available cycle for a plan, or null if none.
export const firstAvailableCycle = (plan) => checkoutableCycles(plan)[0] || null;

// Best cycle to charge given the user's preference: their pick when it is
// checkoutable, otherwise the first checkoutable alternative (monthly first),
// or null when nothing is available.
export const resolveCheckoutCycle = (plan, preferred) => {
  if (isPlanCheckoutable(plan, preferred)) return preferred;
  return firstAvailableCycle(plan);
};
