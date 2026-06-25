/**
 * AdminHorses - HorseOps-1G cross-facility Care Ledger inspection.
 *
 * Read-only platform surface. It deliberately shows summary counts
 * only; raw daily-check payloads, alert triggers, source_check_id,
 * staff notes, owner request messages, and audit diffs never render.
 */
import React, { useEffect, useState } from "react";
import { Activity, AlertTriangle, Search, Shield, X } from "lucide-react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";

const STATUS_OPTIONS = ["", "active", "inactive", "archived"];

const formatTs = (iso) => {
  if (!iso) return "-";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

const SummaryTile = ({ label, value, testid }) => (
  <div
    data-testid={testid}
    className="rounded-lg border border-equinesync-graphite/10 bg-equinesync-frost px-3 py-2.5"
  >
    <div className="text-[9.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55">{label}</div>
    <div className="mt-1 font-display text-xl text-equinesync-graphite font-light leading-tight">
      {value ?? "-"}
    </div>
  </div>
);

function AdminHorseDrawer({ horseId, open, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!open || !horseId) return;
    let cancelled = false;
    api.get(`/admin/portal/horses/${horseId}/ledger-summary`)
      .then((r) => {
        if (cancelled) return;
        setData(r.data);
        setErr(null);
      })
      .catch((e) => {
        if (cancelled) return;
        setErr(e?.response?.data?.detail || "Could not load horse ledger summary.");
      })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [open, horseId]);

  if (!open) return null;
  const horse = data?.horse;
  const summary = data?.ledger_summary || {};
  const severity = summary.active_alerts_by_severity || {};

  return (
    <div className="fixed inset-0 z-40 flex items-stretch justify-end" data-testid="admin-horse-drawer">
      <div className="flex-1 bg-equinesync-graphite/40" onClick={onClose} />
      <aside className="h-full max-h-dvh w-full max-w-xl bg-white border-l border-equinesync-graphite/10 flex flex-col">
        <header className="shrink-0 sticky top-0 z-10 bg-white border-b border-equinesync-graphite/10 px-5 py-4 flex items-start justify-between">
          <div className="min-w-0">
            <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              Horse ledger summary - read-only
            </div>
            <div className="mt-0.5 font-display text-lg text-equinesync-graphite font-light truncate">
              {horse?.name || horseId}
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="min-h-11 min-w-11 rounded-lg border border-equinesync-graphite/10 text-equinesync-graphite/40 hover:text-equinesync-graphite hover:bg-equinesync-frost"
            data-testid="admin-horse-drawer-close"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </header>

        <div className="min-h-0 flex-1 overflow-y-auto p-5 pb-[calc(1.25rem+env(safe-area-inset-bottom))] space-y-5">
          {loading && (
            <div className="space-y-3" data-testid="admin-horse-drawer-loading">
              {[0,1,2].map((i) => <div key={i} className="h-16 bg-equinesync-graphite/5 rounded animate-pulse" />)}
            </div>
          )}
          {err && (
            <div className="text-[13px] text-equinesync-graphite/70" data-testid="admin-horse-drawer-error">
              {err}
            </div>
          )}

          {horse && (
            <>
              <section data-testid="admin-horse-drawer-identity">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Shield className="w-3 h-3" />Identity
                </div>
                <div className="rounded-lg bg-equinesync-frost p-3 text-[13px] text-equinesync-graphite space-y-1">
                  <div className="break-words"><span className="text-equinesync-graphite/55">Horse ID:</span> <span className="break-all">{horse.id}</span></div>
                  <div className="break-words"><span className="text-equinesync-graphite/55">Facility:</span> <span className="break-all">{horse.barn_name || horse.barn_id || "-"}</span></div>
                  <div><span className="text-equinesync-graphite/55">Status:</span> {horse.status || "-"}</div>
                  {horse.breed && <div><span className="text-equinesync-graphite/55">Breed:</span> {horse.breed}</div>}
                  {horse.age != null && <div><span className="text-equinesync-graphite/55">Age:</span> {horse.age}</div>}
                </div>
              </section>

              <section data-testid="admin-horse-drawer-ledger-summary">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Activity className="w-3 h-3" />Care Ledger
                </div>
                <div className="grid grid-cols-2 gap-2.5">
                  <SummaryTile label="Active equipment" value={summary.equipment_active} testid="admin-horse-equipment-active" />
                  <SummaryTile label="Checks in 24h" value={summary.daily_checks_24h} testid="admin-horse-checks-24h" />
                  <SummaryTile label="Open alerts" value={summary.active_alerts} testid="admin-horse-alerts-open" />
                  <SummaryTile label="Owner requests" value={summary.owner_requests_open} testid="admin-horse-owner-requests" />
                </div>
              </section>

              <section data-testid="admin-horse-drawer-alerts">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <AlertTriangle className="w-3 h-3" />Alert severity counts
                </div>
                <div className="rounded-lg bg-equinesync-frost p-3 text-[13px] grid grid-cols-1 sm:grid-cols-3 gap-2 text-equinesync-graphite">
                  <div><span className="text-equinesync-graphite/55">Urgent:</span> {severity.urgent || 0}</div>
                  <div><span className="text-equinesync-graphite/55">Attention:</span> {severity.attention || 0}</div>
                  <div><span className="text-equinesync-graphite/55">Info:</span> {severity.info || 0}</div>
                </div>
              </section>

              <section data-testid="admin-horse-drawer-visibility">
                <div className="text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  Owner visibility policy
                </div>
                <div className="rounded-lg bg-equinesync-frost p-3 text-[13px] text-equinesync-graphite space-y-1">
                  <div><span className="text-equinesync-graphite/55">Configured:</span> {summary.visibility_policy?.configured ? "yes" : "no"}</div>
                  <div><span className="text-equinesync-graphite/55">Version:</span> {summary.visibility_policy?.policy_version ?? 0}</div>
                  <div className="break-words"><span className="text-equinesync-graphite/55">Sections:</span> {(summary.visibility_policy?.sections || []).join(", ") || "-"}</div>
                  <div><span className="text-equinesync-graphite/55">Updated:</span> {formatTs(summary.visibility_policy?.updated_at)}</div>
                </div>
              </section>
            </>
          )}
        </div>
      </aside>
    </div>
  );
}

export default function AdminHorses() {
  const [items, setItems] = useState(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [q, setQ] = useState("");
  const [status, setStatus] = useState("");
  const [cursor, setCursor] = useState(0);
  const [nextCursor, setNextCursor] = useState(null);
  const [openHorseId, setOpenHorseId] = useState(null);

  useEffect(() => {
    let cancelled = false;
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (status) params.set("status", status);
    params.set("limit", "25");
    params.set("cursor", String(cursor));
    api.get(`/admin/portal/horses?${params.toString()}`)
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
        setErr(e?.response?.data?.detail || "Failed to load horses.");
        setLoading(false);
      });
    return () => { cancelled = true; setErr(null); };
  }, [q, status, cursor]);

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-horses-page">
      <div className="mb-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal - Horses
        </div>
        <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">Horse directory</h1>
        <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
          Cross-facility Care Ledger inspection for platform operators. Rows open a
          summary-only drawer; staff notes, raw check payloads, alert triggers, and
          owner request messages stay hidden.
        </p>
      </div>

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-4 mb-4 flex flex-wrap items-end gap-3"
           data-testid="admin-horses-filters">
        <div className="flex-1 min-w-[220px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Search</label>
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-equinesync-graphite/35" />
            <input
              type="text"
              value={q}
              onChange={(e) => { setCursor(0); setQ(e.target.value); }}
              placeholder="Horse name"
              data-testid="admin-horses-search"
              className="w-full pl-9 pr-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-equinesync-frost text-[13px] focus:outline-none focus:border-equinesync-slate"
            />
          </div>
        </div>
        <div className="min-w-[150px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Status</label>
          <select
            value={status}
            onChange={(e) => { setCursor(0); setStatus(e.target.value); }}
            data-testid="admin-horses-status-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {STATUS_OPTIONS.map((o) => (<option key={o} value={o}>{o || "Any status"}</option>))}
          </select>
        </div>
        <div className="text-[11.5px] text-equinesync-graphite/55 ml-auto">{total.toLocaleString()} total</div>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-horses-error">{err}</div>
      )}

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
        {loading && !items && (
          <div className="p-6 space-y-3" data-testid="admin-horses-loading">
            {[0,1,2,3,4].map((i) => <div key={i} className="h-9 bg-equinesync-graphite/5 rounded animate-pulse" />)}
          </div>
        )}
        {!loading && items && items.length === 0 && (
          <div className="p-10 text-center text-[13px] text-equinesync-graphite/50" data-testid="admin-horses-empty">
            No horses match the current filters.
          </div>
        )}
        {items && items.length > 0 && (
          <div className="md:hidden divide-y divide-equinesync-graphite/10" data-testid="admin-horses-mobile-cards">
            {items.map((h) => (
              <button
                key={h.id}
                type="button"
                onClick={() => setOpenHorseId(h.id)}
                data-testid={`admin-horses-card-${h.id}`}
                className="w-full text-left p-4 min-h-[96px] bg-white hover:bg-equinesync-frost transition-colors"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="text-equinesync-graphite font-medium truncate">{h.name || "-"}</div>
                    <div className="mt-1 text-[11.5px] text-equinesync-graphite/55 truncate">{h.id}</div>
                  </div>
                  <UserStatusBadge value={h.status || "active"} />
                </div>
                <div className="mt-3 grid grid-cols-2 gap-2 text-[12px] text-equinesync-graphite/65">
                  <div className="min-w-0">
                    <span className="block text-[9.5px] tracking-[0.18em] uppercase text-equinesync-graphite/45">Facility</span>
                    <span className="block truncate">{h.barn_name || h.barn_id || "-"}</span>
                  </div>
                  <div className="min-w-0">
                    <span className="block text-[9.5px] tracking-[0.18em] uppercase text-equinesync-graphite/45">Breed</span>
                    <span className="block truncate">{h.breed || "-"}</span>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
        {items && items.length > 0 && (
          <table className="hidden md:table w-full text-[13px]" data-testid="admin-horses-table">
            <thead className="bg-equinesync-frost border-b border-equinesync-graphite/10">
              <tr className="text-left text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
                <th className="px-4 py-3 font-medium">Horse</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Facility</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Breed</th>
                <th className="px-4 py-3 font-medium hidden lg:table-cell">Created</th>
              </tr>
            </thead>
            <tbody>
              {items.map((h) => (
                <tr
                  key={h.id}
                  data-testid={`admin-horses-row-${h.id}`}
                  onClick={() => setOpenHorseId(h.id)}
                  className="border-b border-equinesync-graphite/5 last:border-b-0 hover:bg-equinesync-frost cursor-pointer"
                >
                  <td className="px-4 py-3">
                    <div className="text-equinesync-graphite font-medium">{h.name || "-"}</div>
                    <div className="text-equinesync-graphite/55 text-[11.5px]">{h.id}</div>
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75 hidden md:table-cell">
                    {h.barn_name || h.barn_id || "-"}
                  </td>
                  <td className="px-4 py-3">
                    <UserStatusBadge value={h.status || "active"} />
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75 hidden md:table-cell">{h.breed || "-"}</td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden lg:table-cell">{formatTs(h.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {items && items.length > 0 && (
          <div className="px-4 py-3 border-t border-equinesync-graphite/10 flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-3 text-[11.5px] text-equinesync-graphite/55"
               data-testid="admin-horses-pagination">
            <div>Showing {cursor + 1}-{cursor + items.length} of {total.toLocaleString()}</div>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={cursor === 0}
                onClick={() => setCursor(Math.max(0, cursor - 25))}
                data-testid="admin-horses-prev"
                className="min-h-11 flex-1 sm:flex-none px-3 py-2 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Previous</button>
              <button
                type="button"
                disabled={nextCursor === null}
                onClick={() => setCursor(nextCursor)}
                data-testid="admin-horses-next"
                className="min-h-11 flex-1 sm:flex-none px-3 py-2 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Next</button>
            </div>
          </div>
        )}
      </div>

      <AdminHorseDrawer
        key={openHorseId || "closed"}
        horseId={openHorseId}
        open={!!openHorseId}
        onClose={() => setOpenHorseId(null)}
      />
    </div>
  );
}
