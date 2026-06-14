// Phase 15.C — Facility Subscription Billing Portal
// ---------------------------------------------------------------------------
// Lives at /billing/subscription. Distinct from /billing (Phase 9 invoices —
// see pages/Billing.jsx; untouched). Gated by `canManageBilling` which mirrors
// the backend `barn:manage` capability.
//
// Reads:
//   GET /api/subscriptions/me        (status, plan tier, period, trial)
//   GET /api/billing/usage           (soft-warn usage meters)
//   GET /api/billing/plans           (catalog for the "Change plan" picker)
//
// Writes:
//   POST /api/subscriptions/checkout         (change plan / resume)
//   POST /api/subscriptions/customer-portal  (manage card / cancel)
//
// Soft-enforcement only. Usage meters change accent color past 80% / 100% but
// never disable any CTA. All copy stays within the approved Equine-Sync brand
// palette — no matte black, no champagne aesthetics, no new tokens.
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "sonner";
import {
  CheckCircle2, ExternalLink, RefreshCw, ArrowRight, Sparkles,
  AlertTriangle, CalendarClock,
} from "lucide-react";

import { api } from "../lib/api";
import { Card, PageHeader, SectionEyebrow, StatusPill } from "../components/Primitives";
import { BrandLoader } from "../components/BrandLoader";
import {
  STATUS_LABEL, STATUS_TONE, RESUMABLE_STATUSES,
  SUBSCRIBABLE_TIERS, sortPlans, formatCents, annualSavingsPct, daysUntil,
} from "../lib/subscriptionBilling";

const fmtDate = (iso) => {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
};

export default function SubscriptionBilling() {
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");
  const [me, setMe] = useState(null);          // { barn_id, subscription }
  const [usage, setUsage] = useState(null);    // { plan_tier_code, usage, feature_flags }
  const [plans, setPlans] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [busyAction, setBusyAction] = useState(""); // "portal" | "checkout:<tier>:<cycle>"

  const load = useCallback(async () => {
    setErr("");
    try {
      const [meR, uR, pR] = await Promise.all([
        api.get("/subscriptions/me"),
        api.get("/billing/usage"),
        api.get("/billing/plans"),
      ]);
      setMe(meR.data);
      setUsage(uR.data);
      setPlans(sortPlans(pR.data));
    } catch (e) {
      setErr(e?.response?.data?.detail || "Could not load your subscription.");
    }
  }, []);

  useEffect(() => {
    (async () => {
      setLoading(true);
      await load();
      setLoading(false);
    })();
  }, [load]);

  const refresh = useCallback(async () => {
    setRefreshing(true);
    await load();
    setRefreshing(false);
  }, [load]);

  const openPortal = useCallback(async () => {
    setBusyAction("portal");
    try {
      const { data } = await api.post("/subscriptions/customer-portal", {
        origin_url: window.location.origin,
      });
      window.location.assign(data.url);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not open the Stripe portal.");
      setBusyAction("");
    }
  }, []);

  const launchCheckout = useCallback(async (tier, cycle) => {
    const key = `checkout:${tier}:${cycle}`;
    setBusyAction(key);
    try {
      const { data } = await api.post("/subscriptions/checkout", {
        plan_tier_code: tier,
        billing_cycle: cycle,
        origin_url: window.location.origin,
      });
      window.location.assign(data.url);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not start checkout.");
      setBusyAction("");
    }
  }, []);

  if (loading) {
    return (
      <div data-testid="subscription-billing-page" className="pb-20 lg:pb-8">
        <BrandLoader label="Loading your subscription…" />
      </div>
    );
  }

  const sub = me?.subscription || null;
  const status = sub?.status || (usage?.plan_tier_code === "free" ? "free" : null);
  const planTier = sub?.plan_tier_code || usage?.plan_tier_code || "free";
  const isResumable = sub && RESUMABLE_STATUSES.has(sub.status);
  const isTrialing = sub?.status === "trialing";
  const trialDays = isTrialing ? daysUntil(sub?.trial_end) : null;

  return (
    <div data-testid="subscription-billing-page" className="pb-20 lg:pb-8">
      <PageHeader
        eyebrow="Membership"
        title="Subscription"
        subtitle="Manage your facility plan, billing cycle, and usage. Invoices and recurring boarder charges live on the separate Billing page."
        action={
          <button
            onClick={refresh}
            disabled={refreshing}
            data-testid="subscription-refresh-btn"
            className="inline-flex items-center gap-1.5 text-[11.5px] uppercase tracking-[0.2em] text-equine-brass/80 hover:text-equine-brassLight transition-colors px-3 py-1.5 rounded-full border border-equine-graphite/40 hover:border-equine-brass/50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? "animate-spin" : ""}`} />
            {refreshing ? "Refreshing…" : "Refresh"}
          </button>
        }
      />

      {err && (
        <Card hover={false} className="mb-6 border-equine-clay/40" data-testid="subscription-load-error">
          <div className="flex items-start gap-3 text-equine-clay">
            <AlertTriangle className="w-4 h-4 mt-0.5" />
            <div className="text-[13.5px]">{err}</div>
          </div>
        </Card>
      )}

      {/* RESUME CTA — primary placement when the subscription is canceled,
          past_due, unpaid, or incomplete_expired. Soft-warn, not blocking. */}
      {isResumable && (
        <Card
          hover={false}
          className="mb-6 border-equine-clay/40 bg-equine-clay/8"
          data-testid="subscription-resume-card"
        >
          <div className="flex items-start gap-4 flex-wrap">
            <div className="rounded-full bg-equine-clay/15 p-2 border border-equine-clay/30">
              <AlertTriangle className="w-4 h-4 text-equine-clay" />
            </div>
            <div className="flex-1 min-w-[220px]">
              <div className="font-display text-xl text-equine-ink mb-1">
                Resume your membership
              </div>
              <p className="text-[13.5px] text-equine-inkMuted leading-relaxed">
                Your <span className="font-medium capitalize">{planTier}</span> plan is{" "}
                <span className="font-medium">{STATUS_LABEL[sub.status] || sub.status}</span>.
                Pick a cycle below to restart with the same tier — or change plans anytime.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {SUBSCRIBABLE_TIERS.has(planTier) && (
                <>
                  <button
                    onClick={() => launchCheckout(planTier, "monthly")}
                    disabled={busyAction.startsWith("checkout:")}
                    data-testid={`subscription-resume-${planTier}-monthly`}
                    className="px-4 py-2 rounded-full text-[12.5px] tracking-wide font-medium bg-equine-navy text-white hover:bg-equine-navyLift disabled:opacity-50 transition-colors inline-flex items-center gap-1.5"
                  >
                    Resume monthly <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                  <button
                    onClick={() => launchCheckout(planTier, "annual")}
                    disabled={busyAction.startsWith("checkout:")}
                    data-testid={`subscription-resume-${planTier}-annual`}
                    className="px-4 py-2 rounded-full text-[12.5px] tracking-wide font-medium border border-equine-saddleDeep/50 text-equine-saddleDeep hover:bg-equine-saddle/15 disabled:opacity-50 transition-colors inline-flex items-center gap-1.5"
                  >
                    Resume annual
                  </button>
                </>
              )}
            </div>
          </div>
        </Card>
      )}

      {/* STATUS CARD */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-10" data-testid="subscription-status-card">
        <Card className="lg:col-span-2">
          <div className="flex items-start justify-between gap-4 flex-wrap mb-5">
            <div>
              <div className="label-eyebrow mb-2">Current plan</div>
              <div className="font-display text-3xl text-equine-ink capitalize" data-testid="subscription-plan-tier">
                {planTier}
              </div>
              <div className="mt-2 flex items-center gap-2 flex-wrap">
                {status && (
                  <span data-testid="subscription-status-pill">
                    <StatusPill tone={STATUS_TONE[status] || "neutral"} dot>
                      {STATUS_LABEL[status] || status}
                    </StatusPill>
                  </span>
                )}
                {sub?.billing_cycle && (
                  <span className="text-[11.5px] uppercase tracking-[0.2em] text-equine-inkSoft">
                    {sub.billing_cycle === "annual" ? "Annual cycle" : "Monthly cycle"}
                  </span>
                )}
              </div>
            </div>
            <div className="flex flex-col items-end gap-2">
              <button
                onClick={openPortal}
                disabled={!sub || busyAction === "portal"}
                data-testid="subscription-manage-stripe-btn"
                className="inline-flex items-center gap-1.5 text-[12.5px] tracking-wide px-4 py-2 rounded-full bg-equine-navy text-white hover:bg-equine-navyLift disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                title={sub ? "Manage in Stripe" : "Available after first checkout"}
              >
                {busyAction === "portal" ? "Opening…" : "Manage in Stripe"}{" "}
                <ExternalLink className="w-3.5 h-3.5" />
              </button>
              {!sub && (
                <div className="text-[11px] text-equine-inkSoft text-right max-w-[180px]">
                  Available after your first subscription checkout.
                </div>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-5 text-[13px] border-t border-equine-hairline pt-5">
            <Detail label="Period start" value={fmtDate(sub?.current_period_start)} testid="sub-period-start" />
            <Detail label="Period end"   value={fmtDate(sub?.current_period_end)}   testid="sub-period-end" />
            {isTrialing ? (
              <Detail
                label="Trial ends"
                value={trialDays != null ? `${fmtDate(sub.trial_end)} · ${trialDays}d left` : "—"}
                testid="sub-trial-end"
                icon={CalendarClock}
              />
            ) : (
              <Detail
                label="Auto-renew"
                value={sub?.cancel_at_period_end === false ? "On" : sub?.cancel_at_period_end === true ? "Off" : "—"}
                testid="sub-auto-renew"
              />
            )}
          </div>
        </Card>

        {/* Quick facts card */}
        <Card className="bg-equine-card">
          <div className="label-eyebrow mb-3">Why this matters</div>
          <ul className="space-y-3 text-[13px] text-equine-inkMuted leading-relaxed">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 text-equine-saddleDeep flex-shrink-0" />
              <span>Limits below are <span className="text-equine-ink font-medium">soft</span> — going over never blocks horse or user creation.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 text-equine-saddleDeep flex-shrink-0" />
              <span>Cancellation, card updates, and invoice history live in Stripe&apos;s portal.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 text-equine-saddleDeep flex-shrink-0" />
              <span>Boarder invoices &amp; recurring charges are tracked separately on the <Link to="/billing" className="underline text-equine-saddleDeep hover:text-equine-ink">Billing</Link> page.</span>
            </li>
          </ul>
        </Card>
      </div>

      {/* USAGE METERS */}
      <SectionEyebrow>Usage · Soft limits</SectionEyebrow>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-12" data-testid="subscription-usage-grid">
        <UsageMeter
          label="Horses"
          used={usage?.usage?.horses?.used ?? 0}
          limit={usage?.usage?.horses?.limit}
          testid="usage-horses"
        />
        <UsageMeter
          label="Users"
          used={usage?.usage?.users?.used ?? 0}
          limit={usage?.usage?.users?.limit}
          testid="usage-users"
        />
        <UsageMeter
          label="Storage (GB)"
          used={usage?.usage?.storage_gb?.used ?? 0}
          limit={usage?.usage?.storage_gb?.limit}
          testid="usage-storage"
        />
      </div>

      {/* CHANGE PLAN */}
      <SectionEyebrow>Change plan</SectionEyebrow>
      <p className="text-[13.5px] text-equine-inkMuted mb-5 max-w-2xl leading-relaxed">
        Switching plans starts a new Stripe Checkout. Annual cycles get a discount when the
        catalog includes one. Free is solo-only — upgrade any time to unlock facility features.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5" data-testid="subscription-plan-grid">
        {plans
          .filter((p) => p.tier_code !== "free")
          .map((plan) => (
            <PlanPickerCard
              key={plan.tier_code}
              plan={plan}
              currentTier={planTier}
              currentCycle={sub?.billing_cycle}
              onCheckout={launchCheckout}
              busyAction={busyAction}
            />
          ))}
      </div>
    </div>
  );
}

// =============================================================================
// Sub-components
// =============================================================================

function Detail({ label, value, testid, icon: Icon }) {
  return (
    <div data-testid={testid}>
      <div className="label-eyebrow mb-1.5 flex items-center gap-1.5">
        {Icon && <Icon strokeWidth={1.5} className="w-3 h-3 text-equine-inkSoft" />}
        {label}
      </div>
      <div className="text-equine-ink text-[14px]">{value}</div>
    </div>
  );
}

function UsageMeter({ label, used, limit, testid }) {
  const hasLimit = limit != null && Number.isFinite(limit) && limit > 0;
  const pct = hasLimit ? Math.min(1, used / limit) : 0;
  // Color tones — all approved palette tokens. Sage = healthy, amber = soft
  // warning at ≥80%, clay = at/over limit. NO new tokens introduced.
  let toneBar = "bg-equine-sage";
  let tonePill = "info";
  let toneCopy = null;
  if (hasLimit) {
    if (used >= limit) {
      toneBar = "bg-equine-clay";
      tonePill = "critical";
      toneCopy = "Over plan limit — upgrade for more headroom.";
    } else if (pct >= 0.8) {
      toneBar = "bg-equine-amber";
      tonePill = "warning";
      toneCopy = "Approaching plan limit.";
    } else {
      toneBar = "bg-equine-saddle";
      tonePill = "info";
    }
  } else {
    toneBar = "bg-equine-saddle";
  }

  const limitDisplay = hasLimit ? `${used} / ${limit}` : `${used} / unlimited`;
  return (
    <Card data-testid={testid}>
      <div className="flex items-start justify-between mb-3">
        <div className="label-eyebrow">{label}</div>
        <StatusPill tone={tonePill} dot>{hasLimit ? `${Math.round(pct * 100)}%` : "Unlimited"}</StatusPill>
      </div>
      <div className="font-display text-3xl text-equine-ink leading-none" data-testid={`${testid}-count`}>
        {limitDisplay}
      </div>
      <div className="mt-4 h-1.5 rounded-full bg-equine-soft overflow-hidden">
        <div
          className={`h-full ${toneBar} transition-all`}
          style={{ width: hasLimit ? `${Math.round(pct * 100)}%` : "100%" }}
          data-testid={`${testid}-bar`}
        />
      </div>
      {toneCopy && (
        <div className="mt-3 text-[11.5px] text-equine-inkMuted leading-relaxed" data-testid={`${testid}-warn`}>
          {toneCopy}
        </div>
      )}
    </Card>
  );
}

function PlanPickerCard({ plan, currentTier, currentCycle, onCheckout, busyAction }) {
  const [cycle, setCycle] = useState("monthly");
  const monthly = plan.monthly_price_cents;
  const annual = plan.annual_price_cents;
  const savings = annualSavingsPct(plan);
  const isCurrent = plan.tier_code === currentTier;
  const isCurrentCycle = isCurrent && currentCycle === cycle;
  const contactSales = !!plan.contact_sales;
  const checkoutKey = `checkout:${plan.tier_code}:${cycle}`;
  const busy = busyAction === checkoutKey;

  const handleClick = () => {
    if (contactSales) {
      window.location.assign("mailto:sales@equinesync.com?subject=Enterprise%20plan%20enquiry");
      return;
    }
    onCheckout(plan.tier_code, cycle);
  };

  const ctaCopy = contactSales
    ? "Contact sales"
    : isCurrentCycle
    ? "Current plan"
    : isCurrent
    ? `Switch to ${cycle}`
    : busy
    ? "Opening…"
    : `Switch to ${plan.name || plan.tier_code}`;

  return (
    <Card
      hover={!isCurrent}
      className={isCurrent ? "border-equine-saddleDeep/50" : ""}
      data-testid={`plan-card-${plan.tier_code}`}
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div>
          <div className="label-eyebrow mb-1.5">{plan.name || plan.tier_code}</div>
          <div className="font-display text-2xl text-equine-ink capitalize">{plan.tier_code}</div>
        </div>
        {isCurrent && (
          <StatusPill tone="saddle" dot>Current</StatusPill>
        )}
      </div>

      {!contactSales && (plan.has_monthly || plan.has_annual) && (
        <div className="inline-flex bg-equine-soft rounded-full p-0.5 mb-4" data-testid={`plan-cycle-toggle-${plan.tier_code}`}>
          <button
            type="button"
            onClick={() => setCycle("monthly")}
            disabled={!plan.has_monthly}
            className={`px-3 py-1.5 text-[11.5px] tracking-wide rounded-full transition-colors ${
              cycle === "monthly"
                ? "bg-equine-elevated text-equine-ink shadow-sm"
                : "text-equine-inkMuted hover:text-equine-ink disabled:opacity-40"
            }`}
            data-testid={`plan-cycle-monthly-${plan.tier_code}`}
          >
            Monthly
          </button>
          <button
            type="button"
            onClick={() => setCycle("annual")}
            disabled={!plan.has_annual}
            className={`px-3 py-1.5 text-[11.5px] tracking-wide rounded-full transition-colors inline-flex items-center gap-1.5 ${
              cycle === "annual"
                ? "bg-equine-elevated text-equine-ink shadow-sm"
                : "text-equine-inkMuted hover:text-equine-ink disabled:opacity-40"
            }`}
            data-testid={`plan-cycle-annual-${plan.tier_code}`}
          >
            Annual
            {savings != null && (
              <span className="text-[10px] tracking-wider uppercase text-equine-saddleDeep font-medium" data-testid={`plan-savings-${plan.tier_code}`}>
                Save {savings}%
              </span>
            )}
          </button>
        </div>
      )}

      <div className="mb-4">
        {contactSales ? (
          <div className="font-display text-3xl text-equine-ink">Let&apos;s talk</div>
        ) : cycle === "monthly" ? (
          <div className="font-display text-3xl text-equine-ink">
            {formatCents(monthly)}
            <span className="text-[12px] text-equine-inkSoft font-sans ml-1">/mo</span>
          </div>
        ) : (
          <div className="font-display text-3xl text-equine-ink">
            {formatCents(annual)}
            <span className="text-[12px] text-equine-inkSoft font-sans ml-1">/yr</span>
          </div>
        )}
        {plan.description && (
          <p className="mt-2 text-[12.5px] text-equine-inkMuted leading-relaxed">{plan.description}</p>
        )}
      </div>

      {plan.feature_limits && (
        <ul className="space-y-1.5 mb-5 text-[12.5px] text-equine-inkMuted">
          {plan.feature_limits.horses != null && (
            <li className="flex items-center gap-2">
              <Sparkles className="w-3 h-3 text-equine-saddleDeep" />
              Up to <span className="text-equine-ink">{plan.feature_limits.horses}</span> horses
            </li>
          )}
          {plan.feature_limits.users != null && (
            <li className="flex items-center gap-2">
              <Sparkles className="w-3 h-3 text-equine-saddleDeep" />
              Up to <span className="text-equine-ink">{plan.feature_limits.users}</span> users
            </li>
          )}
          {plan.feature_limits.storage_gb != null && (
            <li className="flex items-center gap-2">
              <Sparkles className="w-3 h-3 text-equine-saddleDeep" />
              <span className="text-equine-ink">{plan.feature_limits.storage_gb} GB</span> storage
            </li>
          )}
        </ul>
      )}

      <button
        onClick={handleClick}
        disabled={busy || isCurrentCycle}
        data-testid={`plan-cta-${plan.tier_code}`}
        className={`w-full text-[12.5px] tracking-wide font-medium py-2.5 rounded-full transition-colors inline-flex items-center justify-center gap-1.5 ${
          isCurrentCycle
            ? "bg-equine-soft text-equine-inkSoft cursor-default"
            : isCurrent || contactSales
            ? "border border-equine-saddleDeep/50 text-equine-saddleDeep hover:bg-equine-saddle/15"
            : "bg-equine-navy text-white hover:bg-equine-navyLift"
        } disabled:opacity-60`}
      >
        {ctaCopy} {!isCurrentCycle && <ArrowRight className="w-3.5 h-3.5" />}
      </button>
    </Card>
  );
}
