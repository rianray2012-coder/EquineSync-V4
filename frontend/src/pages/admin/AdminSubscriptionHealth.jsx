/**
 * AdminSubscriptionHealth — single dense card with status + webhook
 * health. No Stripe IDs displayed; counts only. Pure read.
 */
import React from "react";
import { Activity, AlertTriangle } from "lucide-react";

const StatusPill = ({ label, value, tone }) => {
  // Admin Portal palette only — Midnight Graphite, Slate Navy, Frost
  // White, Smoky Lilac. Codex round-1 (Admin-2) blocker fix: no
  // bg-red-*/text-red-*/bg-amber-*/text-amber-* tokens here. Severity
  // is communicated through opacity weight + the brand's darkest tone:
  //   danger → solid Slate Navy w/ Frost White text (highest emphasis)
  //   warn   → Smoky Lilac at 40% w/ Slate Navy border + Graphite text
  //   muted  → Graphite-on-Frost at low opacity (zero counts)
  //   default (informational) → Smoky Lilac highlight
  const toneCls =
    tone === "danger"
      ? "bg-equinesync-slate text-equinesync-frost border-equinesync-slate"
      : tone === "warn"
      ? "bg-equinesync-lilac/40 text-equinesync-graphite border-equinesync-slate/30"
      : tone === "muted"
      ? "bg-equinesync-graphite/5 text-equinesync-graphite/55 border-equinesync-graphite/10"
      : "bg-equinesync-lilac/15 text-equinesync-graphite/80 border-equinesync-lilac/30";
  return (
    <div
      data-testid={`admin-sub-health-${label.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
      data-tone={tone || "default"}
      className={`rounded-lg border px-3 py-2 ${toneCls}`}
    >
      <div className="text-[9.5px] tracking-[0.22em] uppercase opacity-80">
        {label}
      </div>
      <div className="mt-1 font-display text-xl font-light leading-tight">
        {value ?? "—"}
      </div>
    </div>
  );
};

const SkeletonRow = () => (
  <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
    {[0, 1, 2, 3, 4].map((i) => (
      <div key={i} className="h-14 rounded-lg bg-equinesync-graphite/5 animate-pulse" />
    ))}
  </div>
);

export default function AdminSubscriptionHealth({ data, loading, error }) {
  return (
    <section
      className="rounded-xl border border-equinesync-graphite/10 bg-white p-5"
      data-testid="admin-subscription-health"
    >
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <div className="text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/50">
            Subscription health
          </div>
          <div className="mt-1 text-[13px] text-equinesync-graphite/65">
            Status counts + Stripe webhook health, derived locally — no Stripe API call.
          </div>
        </div>
        <Activity className="w-4 h-4 text-equinesync-graphite/40" strokeWidth={1.5} />
      </div>

      {loading && !data && <SkeletonRow />}
      {error && (
        <div className="text-[13px] text-equinesync-graphite/70" data-testid="admin-subscription-health-error">
          Could not load subscription health.
        </div>
      )}
      {data && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            <StatusPill label="Active" value={data.status_counts?.active} />
            <StatusPill label="Trialing" value={data.status_counts?.trialing} />
            <StatusPill label="Past-due" value={data.status_counts?.past_due} tone={data.status_counts?.past_due ? "danger" : "muted"} />
            <StatusPill label="Canceled" value={data.status_counts?.canceled} tone="muted" />
            <StatusPill label="Incomplete" value={data.status_counts?.incomplete} tone="muted" />
          </div>

          <div className="mt-5 pt-5 border-t border-equinesync-graphite/10">
            <div className="flex items-center gap-2 mb-3">
              <AlertTriangle className="w-3.5 h-3.5 text-equinesync-graphite/55" strokeWidth={1.6} />
              <div className="text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55">
                Webhook health (last 24 h)
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <StatusPill
                label="Failed (24 h)"
                value={data.webhook_health?.failed_last_24h}
                tone={data.webhook_health?.failed_last_24h ? "danger" : "muted"}
              />
              <StatusPill
                label="Stuck in retry"
                value={data.webhook_health?.stuck_in_retry}
                tone={data.webhook_health?.stuck_in_retry ? "warn" : "muted"}
              />
            </div>
          </div>
        </>
      )}
    </section>
  );
}
