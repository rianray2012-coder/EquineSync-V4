/**
 * AdminKpiCards — Admin-2 KPI grid (read-only).
 *
 * Renders the five primary cards (Users / Facilities / Horses / each
 * card carries a 7-day trend) + three subscription/MRR cards. Loading
 * state shows skeleton boxes; error state shows a single calm message.
 */
import React from "react";
import { Users, Building2, Heart, TrendingUp, CreditCard, DollarSign } from "lucide-react";

const formatNumber = (n) => {
  if (n === null || n === undefined) return "—";
  return Number(n).toLocaleString("en-US");
};

const formatMrr = (cents) => {
  if (cents === null || cents === undefined) return "—";
  const dollars = Math.floor(Number(cents) / 100);
  return `$${dollars.toLocaleString("en-US")}`;
};

const Card = ({ icon: Icon, label, value, trend, accent = false, testid }) => (
  <div
    data-testid={testid}
    className={`rounded-xl border p-5 ${
      accent
        ? "border-equinesync-slate/30 bg-equinesync-slate text-equinesync-frost"
        : "border-equinesync-graphite/10 bg-white text-equinesync-graphite"
    }`}
  >
    <div className="flex items-start justify-between gap-3">
      <div
        className={`text-[10.5px] tracking-[0.22em] uppercase ${
          accent ? "text-equinesync-lilac" : "text-equinesync-graphite/50"
        }`}
      >
        {label}
      </div>
      <Icon
        className={`w-4 h-4 ${accent ? "text-equinesync-lilac" : "text-equinesync-graphite/40"}`}
        strokeWidth={1.5}
      />
    </div>
    <div
      className={`mt-3 font-display text-3xl font-light ${accent ? "text-equinesync-frost" : "text-equinesync-graphite"}`}
    >
      {value}
    </div>
    {trend !== undefined && trend !== null && (
      <div
        className={`mt-2 inline-flex items-center gap-1 text-[11px] tracking-wide ${
          accent ? "text-equinesync-lilac" : "text-equinesync-graphite/50"
        }`}
      >
        <TrendingUp className="w-3 h-3" strokeWidth={1.6} />
        +{formatNumber(trend)} last 7 days
      </div>
    )}
  </div>
);

const SkeletonCard = () => (
  <div className="rounded-xl border border-equinesync-graphite/10 bg-white p-5 animate-pulse min-h-[120px]">
    <div className="h-3 w-24 bg-equinesync-graphite/10 rounded mb-4" />
    <div className="h-8 w-20 bg-equinesync-graphite/10 rounded" />
  </div>
);

export default function AdminKpiCards({ kpis, loading, error }) {
  if (loading && !kpis) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4" data-testid="admin-kpi-grid">
        {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => <SkeletonCard key={i} />)}
      </div>
    );
  }
  if (error) {
    return (
      <div
        data-testid="admin-kpi-error"
        className="rounded-xl border border-equinesync-graphite/10 bg-white p-5 text-[13px] text-equinesync-graphite/70"
      >
        Could not load KPIs. The dashboard is read-only; try refreshing in a moment.
      </div>
    );
  }
  if (!kpis) return null;
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4" data-testid="admin-kpi-grid">
      <Card
        testid="admin-kpi-users"
        icon={Users}
        label="Total users"
        value={formatNumber(kpis.users_total)}
        trend={kpis.users_new_7d}
      />
      <Card
        testid="admin-kpi-facilities"
        icon={Building2}
        label="Facilities"
        value={formatNumber(kpis.facilities_total)}
        trend={kpis.facilities_new_7d}
      />
      <Card
        testid="admin-kpi-horses"
        icon={Heart}
        label="Horses on record"
        value={formatNumber(kpis.horses_total)}
        trend={kpis.horses_new_7d}
      />
      <Card
        testid="admin-kpi-active_subs"
        icon={CreditCard}
        label="Active subscriptions"
        value={formatNumber(kpis.subs_active)}
      />
      <Card
        testid="admin-kpi-trialing"
        icon={CreditCard}
        label="Trialing"
        value={formatNumber(kpis.subs_trialing)}
      />
      <Card
        testid="admin-kpi-past_due"
        icon={CreditCard}
        label="Past-due"
        value={formatNumber(kpis.subs_past_due)}
      />
      <Card
        testid="admin-kpi-approvals"
        icon={Users}
        label="Pending approvals"
        value={formatNumber(kpis.approvals_pending)}
      />
      <Card
        testid="admin-kpi-mrr"
        icon={DollarSign}
        label="MRR (active)"
        value={formatMrr(kpis.mrr_cents)}
        accent
      />
    </div>
  );
}
