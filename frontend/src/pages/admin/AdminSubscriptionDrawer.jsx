/**
 * AdminSubscriptionDrawer — read-only detail panel for ONE subscription.
 *
 * Surfaces:
 *   - Facility summary (id, name, contact, tier, created)
 *   - Plan / status / billing cycle / recurring amount / period / trial
 *   - Entitlements snapshot
 *   - Pending email flags (operator visibility, NOT a retry trigger)
 *   - Recent admin activity from audit_log (decision 7a)
 *
 * ZERO mutation buttons. ZERO Stripe IDs anywhere on the surface.
 */
import React, { useEffect, useState } from "react";
import { X, CreditCard, Building2, History, Mail, ListChecks } from "lucide-react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

const formatMoney = (cents) => {
  if (cents == null) return "—";
  const d = Math.floor(Number(cents) / 100);
  return `$${d.toLocaleString("en-US")}`;
};

const Tile = ({ label, value, testid }) => (
  <div
    data-testid={testid}
    className="rounded-lg border border-equinesync-graphite/10 bg-equinesync-frost px-3 py-2.5"
  >
    <div className="text-[9.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55">{label}</div>
    <div className="mt-1 font-display text-lg text-equinesync-graphite font-light leading-tight">
      {value ?? "—"}
    </div>
  </div>
);

export default function AdminSubscriptionDrawer({ adminRef, open, onClose }) {
  // Parent passes `key={adminRef}` so this drawer remounts per
  // subscription. Initial state already represents "loading, no data,
  // no err" — the effect just kicks off the fetch and writes state
  // exclusively from async callbacks (silences
  // `react-hooks/set-state-in-effect`).
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!open || !adminRef) return;
    let cancelled = false;
    api.get(`/admin/portal/subscriptions/${adminRef}`)
      .then((r) => { if (!cancelled) { setData(r.data); setErr(null); } })
      .catch((e) => { if (!cancelled) setErr(e?.response?.data?.detail || "Could not load subscription."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [open, adminRef]);

  if (!open) return null;
  const sub = data?.subscription;
  const facility = data?.facility;
  const entitlements = sub?.entitlements_snapshot || {};

  return (
    <div className="fixed inset-0 z-40 flex" data-testid="admin-subscription-drawer">
      <div className="flex-1 bg-equinesync-graphite/40" onClick={onClose} />
      <aside className="w-full max-w-xl bg-white border-l border-equinesync-graphite/10 overflow-y-auto">
        <header className="sticky top-0 z-10 bg-white border-b border-equinesync-graphite/10 px-5 py-4 flex items-start justify-between">
          <div className="min-w-0">
            <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              Subscription detail · read-only
            </div>
            <div className="mt-0.5 font-display text-lg text-equinesync-graphite font-light truncate">
              {facility?.name || sub?.barn_id || adminRef}
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="text-equinesync-graphite/40 hover:text-equinesync-graphite"
            data-testid="admin-subscription-drawer-close"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </header>

        <div className="p-5 space-y-5">
          {loading && (
            <div className="space-y-3" data-testid="admin-subscription-drawer-loading">
              {[0,1,2].map((i) => <div key={i} className="h-16 bg-equinesync-graphite/5 rounded animate-pulse" />)}
            </div>
          )}
          {err && <div className="text-[13px] text-equinesync-graphite/70" data-testid="admin-subscription-drawer-error">{err}</div>}

          {sub && (
            <>
              <section data-testid="admin-subscription-drawer-facility">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Building2 className="w-3 h-3" />Facility
                </div>
                <div className="rounded-lg bg-equinesync-frost p-3 text-[13px] text-equinesync-graphite space-y-1">
                  <div><span className="text-equinesync-graphite/55">ID:</span> {facility?.id || sub.barn_id || "—"}</div>
                  {facility?.name && <div><span className="text-equinesync-graphite/55">Name:</span> {facility.name}</div>}
                  {facility?.contact_email && <div><span className="text-equinesync-graphite/55">Contact:</span> {facility.contact_email}</div>}
                  {facility?.subscription_tier_code && <div><span className="text-equinesync-graphite/55">Tier:</span> {facility.subscription_tier_code}</div>}
                </div>
              </section>

              <section data-testid="admin-subscription-drawer-summary">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <CreditCard className="w-3 h-3" />Subscription
                </div>
                <div className="grid grid-cols-2 gap-2.5">
                  <Tile label="Plan" value={sub.plan_tier_code} testid="admin-sub-detail-plan" />
                  <Tile label="Status" value={sub.status} testid="admin-sub-detail-status" />
                  <Tile label="Cycle" value={sub.billing_cycle || "—"} testid="admin-sub-detail-cycle" />
                  <Tile label="Recurring amount" value={formatMoney(sub.amount_cents)} testid="admin-sub-detail-amount" />
                  <Tile label="Period ends" value={sub.current_period_end ? formatTs(sub.current_period_end) : "—"} testid="admin-sub-detail-period" />
                  <Tile label="Trial ends" value={sub.trial_end ? formatTs(sub.trial_end) : "—"} testid="admin-sub-detail-trial" />
                </div>
              </section>

              <section data-testid="admin-subscription-drawer-entitlements">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <ListChecks className="w-3 h-3" />Entitlements snapshot
                </div>
                {Object.keys(entitlements).length ? (
                  <div className="rounded-lg bg-equinesync-frost p-3 text-[13px] grid grid-cols-2 gap-1.5">
                    {Object.entries(entitlements).map(([k, v]) => (
                      <div key={k}>
                        <span className="text-equinesync-graphite/55">{String(k).replace(/_/g, " ")}:</span>{" "}
                        <span className="text-equinesync-graphite">{v == null ? "∞" : String(v)}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No entitlements snapshot on file.</div>
                )}
              </section>

              <section data-testid="admin-subscription-drawer-pending-emails">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Mail className="w-3 h-3" />Pending email flags
                </div>
                {sub.pending_emails && sub.pending_emails.length ? (
                  <ul className="rounded-lg bg-equinesync-frost p-3 text-[12.5px] text-equinesync-graphite/80 space-y-1">
                    {sub.pending_emails.map((e, i) => (
                      <li key={`${e}-${i}`}>· {e}</li>
                    ))}
                  </ul>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No queued subscription emails.</div>
                )}
              </section>

              <section data-testid="admin-subscription-drawer-audit">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <History className="w-3 h-3" />Recent admin activity
                </div>
                {data?.recent_activity?.length ? (
                  <ul className="space-y-1.5">
                    {data.recent_activity.map((a, i) => (
                      <li key={a.id || `${a.action}-${i}`} className="text-[12px] text-equinesync-graphite/75">
                        <span className="text-equinesync-graphite font-medium">{a.action}</span>{" "}
                        · {formatTs(a.ts)}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No recent admin activity for this subscription.</div>
                )}
              </section>
            </>
          )}
        </div>
      </aside>
    </div>
  );
}
