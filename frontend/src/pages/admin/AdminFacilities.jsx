/**
 * AdminFacilities — read-only cross-facility roster (Admin-4).
 *
 * Search by name, filter by tier/status, paginated. Row click opens
 * the facility-detail drawer. ZERO mutation buttons — Admin-4 is
 * strictly read-only per the locked plan (1a).
 */
import React, { useEffect, useState } from "react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";
import AdminFacilityDrawer from "./AdminFacilityDrawer";

const TIER_OPTIONS = ["", "free", "starter", "professional", "enterprise"];

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
  catch { return iso; }
};

const usageLabel = (used, limit) => {
  if (limit == null) return `${used} / ∞`;
  return `${used} / ${limit}`;
};

export default function AdminFacilities() {
  const [items, setItems] = useState(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  const [q, setQ] = useState("");
  const [tier, setTier] = useState("");
  const [cursor, setCursor] = useState(0);
  const [nextCursor, setNextCursor] = useState(null);
  const [openBarnId, setOpenBarnId] = useState(null);

  // All state transitions live inside async callbacks (see
  // AdminDashboard for the same pattern). Filter/page changes keep
  // the previous data visible until the new payload lands (SWR-style)
  // — that satisfies `react-hooks/set-state-in-effect` without
  // changing what users see meaningfully.
  useEffect(() => {
    let cancelled = false;
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (tier) params.set("tier", tier);
    params.set("limit", "25");
    params.set("cursor", String(cursor));
    api.get(`/admin/portal/facilities?${params.toString()}`)
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
        setErr(e?.response?.data?.detail || "Failed to load facilities.");
        setLoading(false);
      });
    return () => { cancelled = true; setErr(null); };
  }, [q, tier, cursor]);

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-facilities-page">
      <div className="mb-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal · Facilities
        </div>
        <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">Facility roster</h1>
        <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
          Cross-facility visibility for every platform role. Mutations (edits + soft-disable) land
          in a separately-gated Admin-4b. Subscription data is summary-only — drill-down lives in Admin-5.
        </p>
      </div>

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-4 mb-4 flex flex-wrap items-end gap-3"
           data-testid="admin-facilities-filters">
        <div className="flex-1 min-w-[220px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Search</label>
          <input
            type="text"
            value={q}
            onChange={(e) => { setCursor(0); setQ(e.target.value); }}
            placeholder="Facility name"
            data-testid="admin-facilities-search"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-equinesync-frost text-[13px] focus:outline-none focus:border-equinesync-slate"
          />
        </div>
        <div className="min-w-[160px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Tier</label>
          <select
            value={tier}
            onChange={(e) => { setCursor(0); setTier(e.target.value); }}
            data-testid="admin-facilities-tier-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {TIER_OPTIONS.map((o) => (<option key={o} value={o}>{o || "Any tier"}</option>))}
          </select>
        </div>
        <div className="text-[11.5px] text-equinesync-graphite/55 ml-auto">{total.toLocaleString()} total</div>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-facilities-error">{err}</div>
      )}

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
        {loading && !items && (
          <div className="p-6 space-y-3" data-testid="admin-facilities-loading">
            {[0,1,2,3,4].map((i) => <div key={i} className="h-9 bg-equinesync-graphite/5 rounded animate-pulse" />)}
          </div>
        )}
        {!loading && items && items.length === 0 && (
          <div className="p-10 text-center text-[13px] text-equinesync-graphite/50" data-testid="admin-facilities-empty">
            No facilities match the current filters.
          </div>
        )}
        {items && items.length > 0 && (
          <table className="w-full text-[13px]" data-testid="admin-facilities-table">
            <thead className="bg-equinesync-frost border-b border-equinesync-graphite/10">
              <tr className="text-left text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
                <th className="px-4 py-3 font-medium">Facility</th>
                <th className="px-4 py-3 font-medium">Tier</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Status</th>
                <th className="px-4 py-3 font-medium">Horses</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Users</th>
                <th className="px-4 py-3 font-medium hidden lg:table-cell">Created</th>
              </tr>
            </thead>
            <tbody>
              {items.map((b) => (
                <tr
                  key={b.id}
                  data-testid={`admin-facilities-row-${b.id}`}
                  onClick={() => setOpenBarnId(b.id)}
                  className="border-b border-equinesync-graphite/5 last:border-b-0 hover:bg-equinesync-frost cursor-pointer"
                >
                  <td className="px-4 py-3">
                    <div className="text-equinesync-graphite font-medium">{b.name || "—"}</div>
                    <div className="text-equinesync-graphite/55 text-[11.5px]">{b.id}</div>
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">{b.subscription_tier_code || "—"}</td>
                  <td className="px-4 py-3 hidden md:table-cell">
                    {b.subscription_status ? <UserStatusBadge value={b.subscription_status} /> : <span className="text-equinesync-graphite/35">—</span>}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">
                    {usageLabel(b.usage?.horses_used, b.usage?.horses_limit)}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75 hidden md:table-cell">
                    {usageLabel(b.usage?.users_used, b.usage?.users_limit)}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden lg:table-cell">{formatTs(b.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {items && items.length > 0 && (
          <div className="px-4 py-3 border-t border-equinesync-graphite/10 flex justify-between items-center text-[11.5px] text-equinesync-graphite/55"
               data-testid="admin-facilities-pagination">
            <div>Showing {cursor + 1}–{cursor + items.length} of {total.toLocaleString()}</div>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={cursor === 0}
                onClick={() => setCursor(Math.max(0, cursor - 25))}
                data-testid="admin-facilities-prev"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Previous</button>
              <button
                type="button"
                disabled={nextCursor === null}
                onClick={() => setCursor(nextCursor)}
                data-testid="admin-facilities-next"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Next</button>
            </div>
          </div>
        )}
      </div>

      <AdminFacilityDrawer
        key={openBarnId || "closed"}
        barnId={openBarnId}
        open={!!openBarnId}
        onClose={() => setOpenBarnId(null)}
      />
    </div>
  );
}
