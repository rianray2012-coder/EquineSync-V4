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

// Annual-vs-monthly savings: rounded whole percent. Returns null when one of
// the prices is missing or the annual price isn't actually a discount.
export const annualSavingsPct = (plan) => {
  const m = plan?.monthly_price_cents;
  const a = plan?.annual_price_cents;
  if (m == null || a == null || m <= 0 || a <= 0) return null;
  const fullYear = m * 12;
  if (a >= fullYear) return null;
  return Math.round(((fullYear - a) / fullYear) * 100);
};

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

// `StatusPill` tone for each status — uses the existing approved palette
// tokens (sage/amber/clay/brass/neutral) only.
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
// `has_monthly` / `has_annual` based on the presence of STRIPE_PRICE_*
// environment variables on the backend. When false, `/api/subscriptions/
// checkout` raises HTTP 500 ("missing a Stripe Price for cycle=…"). The UI
// must disable any CTA that would otherwise hit that 500 and surface a
// "Billing setup pending" message instead. Contact-sales plans
// are always considered un-checkoutable here — those use mailto.
export const isPlanCheckoutable = (plan, cycle) => {
  if (!plan || plan.contact_sales) return false;
  if (cycle === "annual") return !!plan.has_annual;
  if (cycle === "monthly") return !!plan.has_monthly;
  return !!(plan.has_monthly || plan.has_annual);
};

// Returns the first available cycle for a plan, or null if none.
export const firstAvailableCycle = (plan) => {
  if (!plan || plan.contact_sales) return null;
  if (plan.has_monthly) return "monthly";
  if (plan.has_annual) return "annual";
  return null;
};
