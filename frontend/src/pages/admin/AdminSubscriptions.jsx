/**
 * AdminSubscriptions — read-only Phase 15 subscription roster (Admin-5).
 *
 * Strict guardrails (founder decisions 1a / 4a):
 *   - READ-ONLY. ZERO mutation buttons.
 *   - NO Stripe IDs surfaced anywhere on the page.
 *   - Approved Equine-Sync palette only (Graphite / Slate / Frost / Lilac).
 *   - support_admin still hits this page (summary-only is enough), but
 *     they're blocked at the API layer from /billing-events and
 *     /payments.
 */
import React, { useEffect, useState } from "react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";
import AdminSubscriptionDrawer from "./AdminSubscriptionDrawer";

const STATUS_OPTIONS = ["", "active", "trialing", "past_due", "canceled", "incomplete", "unpaid"];
const TIER_OPTIONS = ["", "free", "starter", "professional", "enterprise"];
const CYCLE_OPTIONS = ["", "month", "year"];

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
  catch { return iso; }
};

const formatMoney = (cents) => {
  if (cents == null) return "—";
  const d = Math.floor(Number(cents) / 100);
  return `$${d.toLocaleString("en-US")}`;
};

export default function AdminSubscriptions() {
  const [items, setItems] = useState(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  const [q, setQ] = useState("");
  const [status, setStatus] = useState("");
  const [tier, setTier] = useState("");
  const [cycle, setCycle] = useState("");
  const [cursor, setCursor] = useState(0);
  const [nextCursor, setNextCursor] = useState(null);
  const [openRef, setOpenRef] = useState(null);

  // All state transitions live inside async callbacks — same pattern
  // as AdminDashboard / AdminFacilities. Filter or page changes keep
  // the previous data visible until the new payload lands (SWR-style);
  // satisfies `react-hooks/set-state-in-effect` without changing
  // user-visible behavior.
  useEffect(() => {
    let cancelled = false;
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (status) params.set("status", status);
    if (tier) params.set("plan_tier_code", tier);
    if (cycle) params.set("billing_cycle", cycle);
    params.set("limit", "25");
    params.set("cursor", String(cursor));
    api.get(`/admin/portal/subscriptions?${params.toString()}`)
      .then((r) => {
        if (cancelled) return;
        setItems(r.data.items);
        setTotal(r.data.total);
        setNextCursor(r.data.next_cursor);
        setErr(null);
        setLoading(false);
      })
      .catch((e) => {
        if (cancelled) return;
        setErr(e?.response?.data?.detail || "Failed to load subscriptions.");
        setLoading(false);
      });
    // Smooth stale-error UX (Admin-5a carry-forward 7a): when the user
    // changes filters or paginates after a failed request, the cleanup
    // clears `err` before the next request starts so the old message
    // does not linger until the new request succeeds.
    return () => { cancelled = true; setErr(null); };
  }, [q, status, tier, cycle, cursor]);

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-subscriptions-page">
      <div className="mb-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal · Subscriptions
        </div>
        <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">Subscription roster</h1>
        <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
          Read-only Phase 15 subscriptions. Stripe IDs are omitted by design.
          Mutations (cancel / refund / comp) are deferred to a separately-gated phase.
        </p>
      </div>

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-4 mb-4 flex flex-wrap items-end gap-3"
           data-testid="admin-subscriptions-filters">
        <div className="flex-1 min-w-[220px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Search</label>
          <input
            type="text"
            value={q}
            onChange={(e) => { setCursor(0); setQ(e.target.value); }}
            placeholder="Facility name"
            data-testid="admin-subscriptions-search"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-equinesync-frost text-[13px] focus:outline-none focus:border-equinesync-slate"
          />
        </div>
        <div className="min-w-[140px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Status</label>
          <select
            value={status}
            onChange={(e) => { setCursor(0); setStatus(e.target.value); }}
            data-testid="admin-subscriptions-status-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {STATUS_OPTIONS.map((o) => (<option key={o} value={o}>{o || "Any status"}</option>))}
          </select>
        </div>
        <div className="min-w-[140px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Plan</label>
          <select
            value={tier}
            onChange={(e) => { setCursor(0); setTier(e.target.value); }}
            data-testid="admin-subscriptions-tier-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {TIER_OPTIONS.map((o) => (<option key={o} value={o}>{o || "Any plan"}</option>))}
          </select>
        </div>
        <div className="min-w-[120px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Cycle</label>
          <select
            value={cycle}
            onChange={(e) => { setCursor(0); setCycle(e.target.value); }}
            data-testid="admin-subscriptions-cycle-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {CYCLE_OPTIONS.map((o) => (<option key={o} value={o}>{o || "Any cycle"}</option>))}
          </select>
        </div>
        <div className="text-[11.5px] text-equinesync-graphite/55 ml-auto">{total.toLocaleString()} total</div>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-subscriptions-error">{err}</div>
      )}

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
        {loading && !items && (
          <div className="p-6 space-y-3" data-testid="admin-subscriptions-loading">
            {[0,1,2,3,4].map((i) => <div key={i} className="h-9 bg-equinesync-graphite/5 rounded animate-pulse" />)}
          </div>
        )}
        {!loading && items && items.length === 0 && (
          <div className="p-10 text-center text-[13px] text-equinesync-graphite/50" data-testid="admin-subscriptions-empty">
            No subscriptions match the current filters.
          </div>
        )}
        {items && items.length > 0 && (
          <table className="w-full text-[13px]" data-testid="admin-subscriptions-table">
            <thead className="bg-equinesync-frost border-b border-equinesync-graphite/10">
              <tr className="text-left text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
                <th className="px-4 py-3 font-medium">Facility</th>
                <th className="px-4 py-3 font-medium">Plan</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Cycle</th>
                <th className="px-4 py-3 font-medium">Recurring</th>
                <th className="px-4 py-3 font-medium hidden lg:table-cell">Period ends</th>
                <th className="px-4 py-3 font-medium hidden lg:table-cell">Trial ends</th>
              </tr>
            </thead>
            <tbody>
              {items.map((s) => (
                <tr
                  key={s.admin_ref}
                  data-testid={`admin-subscriptions-row-${s.admin_ref}`}
                  onClick={() => setOpenRef(s.admin_ref)}
                  className="border-b border-equinesync-graphite/5 last:border-b-0 hover:bg-equinesync-frost cursor-pointer"
                >
                  <td className="px-4 py-3">
                    <div className="text-equinesync-graphite font-medium">{s.facility_name || s.barn_id || "—"}</div>
                    <div className="text-equinesync-graphite/55 text-[11.5px] font-mono">{s.admin_ref}</div>
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">{s.plan_tier_code || "—"}</td>
                  <td className="px-4 py-3">
                    {s.status ? <UserStatusBadge value={s.status} /> : <span className="text-equinesync-graphite/35">—</span>}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75 hidden md:table-cell">{s.billing_cycle || "—"}</td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">{formatMoney(s.amount_cents)}</td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden lg:table-cell">{formatTs(s.current_period_end)}</td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden lg:table-cell">{formatTs(s.trial_end)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {items && items.length > 0 && (
          <div className="px-4 py-3 border-t border-equinesync-graphite/10 flex justify-between items-center text-[11.5px] text-equinesync-graphite/55"
               data-testid="admin-subscriptions-pagination">
            <div>Showing {cursor + 1}–{cursor + items.length} of {total.toLocaleString()}</div>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={cursor === 0}
                onClick={() => setCursor(Math.max(0, cursor - 25))}
                data-testid="admin-subscriptions-prev"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Previous</button>
              <button
                type="button"
                disabled={nextCursor === null}
                onClick={() => setCursor(nextCursor)}
                data-testid="admin-subscriptions-next"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Next</button>
            </div>
          </div>
        )}
      </div>

      <AdminSubscriptionDrawer
        key={openRef || "closed"}
        adminRef={openRef}
        open={!!openRef}
        onClose={() => setOpenRef(null)}
      />
    </div>
  );
}
