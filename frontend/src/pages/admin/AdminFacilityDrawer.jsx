/**
 * AdminFacilityDrawer — read-only health page for ONE facility.
 *
 * Surfaces:
 *   - Safe profile (name, address, contact, tier, created)
 *   - Subscription SUMMARY (plan, status, period end, recurring amount) — NO Stripe IDs
 *   - Usage vs limits (horses, users)
 *   - Recent admin activity for the barn
 *
 * ZERO mutation buttons. Admin-4b will add edits + soft-disable
 * against a separately-gated plan.
 */
import React, { useEffect, useState } from "react";
import { X, Building2, CreditCard, History, Users, Heart } from "lucide-react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

const formatMrr = (cents) => {
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

export default function AdminFacilityDrawer({ barnId, open, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!open || !barnId) return;
    let cancelled = false;
    setLoading(true); setErr(null); setData(null);
    api.get(`/admin/portal/facilities/${barnId}`)
      .then((r) => { if (!cancelled) setData(r.data); })
      .catch((e) => { if (!cancelled) setErr(e?.response?.data?.detail || "Could not load facility."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [open, barnId]);

  if (!open) return null;
  const b = data?.barn;
  const sub = data?.subscription_summary;
  const usage = data?.usage || {};

  return (
    <div className="fixed inset-0 z-40 flex" data-testid="admin-facility-drawer">
      <div className="flex-1 bg-equinesync-graphite/40" onClick={onClose} />
      <aside className="w-full max-w-xl bg-white border-l border-equinesync-graphite/10 overflow-y-auto">
        <header className="sticky top-0 z-10 bg-white border-b border-equinesync-graphite/10 px-5 py-4 flex items-start justify-between">
          <div className="min-w-0">
            <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              Facility detail
            </div>
            <div className="mt-0.5 font-display text-lg text-equinesync-graphite font-light truncate">
              {b?.name || b?.id || "—"}
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="text-equinesync-graphite/40 hover:text-equinesync-graphite"
            data-testid="admin-facility-drawer-close"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </header>

        <div className="p-5 space-y-5">
          {loading && (
            <div className="space-y-3" data-testid="admin-facility-drawer-loading">
              {[0,1,2].map((i) => <div key={i} className="h-16 bg-equinesync-graphite/5 rounded animate-pulse" />)}
            </div>
          )}
          {err && <div className="text-[13px] text-equinesync-graphite/70" data-testid="admin-facility-drawer-error">{err}</div>}

          {b && (
            <>
              <section data-testid="admin-facility-drawer-profile">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Building2 className="w-3 h-3" />Profile
                </div>
                <div className="rounded-lg bg-equinesync-frost p-3 text-[13px] text-equinesync-graphite space-y-1">
                  <div><span className="text-equinesync-graphite/55">ID:</span> {b.id}</div>
                  {b.contact_email && <div><span className="text-equinesync-graphite/55">Contact:</span> {b.contact_email}</div>}
                  {b.phone && <div><span className="text-equinesync-graphite/55">Phone:</span> {b.phone}</div>}
                  {b.address && <div><span className="text-equinesync-graphite/55">Address:</span> {b.address}</div>}
                  {b.timezone && <div><span className="text-equinesync-graphite/55">Timezone:</span> {b.timezone}</div>}
                  <div className="text-[11.5px] text-equinesync-graphite/55 pt-1">
                    Created {formatTs(b.created_at)}
                  </div>
                </div>
              </section>

              <section data-testid="admin-facility-drawer-subscription">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <CreditCard className="w-3 h-3" />Subscription summary
                </div>
                {sub ? (
                  <div className="grid grid-cols-2 gap-2.5">
                    <Tile label="Plan" value={sub.plan_tier_code} testid="admin-facility-sub-plan" />
                    <Tile label="Status" value={sub.status} testid="admin-facility-sub-status" />
                    <Tile label="Cycle" value={sub.billing_cycle || "—"} testid="admin-facility-sub-cycle" />
                    <Tile label="Recurring amount" value={formatMrr(sub.amount_cents)} testid="admin-facility-sub-mrr" />
                    <Tile label="Period ends" value={sub.current_period_end ? formatTs(sub.current_period_end) : "—"} testid="admin-facility-sub-period" />
                    <Tile label="Trial ends" value={sub.trial_end ? formatTs(sub.trial_end) : "—"} testid="admin-facility-sub-trial" />
                  </div>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No subscription on file.</div>
                )}
              </section>

              <section data-testid="admin-facility-drawer-usage">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Heart className="w-3 h-3" />Usage
                </div>
                <div className="grid grid-cols-2 gap-2.5">
                  <Tile
                    label="Horses"
                    value={`${usage.horses_used ?? 0} / ${usage.horses_limit ?? "∞"}`}
                    testid="admin-facility-usage-horses"
                  />
                  <Tile
                    label="Users"
                    value={`${usage.users_used ?? 0} / ${usage.users_limit ?? "∞"}`}
                    testid="admin-facility-usage-users"
                  />
                </div>
              </section>

              <section data-testid="admin-facility-drawer-audit">
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
                  <div className="text-[12.5px] text-equinesync-graphite/50">No recent admin activity for this facility.</div>
                )}
              </section>
            </>
          )}
        </div>
      </aside>
    </div>
  );
}
