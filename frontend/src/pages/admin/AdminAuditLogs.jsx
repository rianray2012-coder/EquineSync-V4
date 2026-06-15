/**
 * AdminAuditLogs — searchable read-only audit log roster (Admin-6).
 *
 * Strict guardrails:
 *   - READ-ONLY. No mutation buttons.
 *   - Opaque `al_*` refs only. Raw `resource_id` is never surfaced
 *     (server replaces it with a `resource.kind` + `resource.admin_ref`
 *     pair when the resource type is known).
 *   - Server-side metadata scrub: Stripe-shaped values are redacted to
 *     `[stripe_id_redacted]`; sensitive keys (token/secret/password/…)
 *     are dropped entirely; long strings truncated.
 *   - Approved Equine-Sync palette only.
 */
import React, { useEffect, useState } from "react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";
import AdminAuditLogDrawer from "./AdminAuditLogDrawer";

const OUTCOMES = ["", "success", "denied", "error"];

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

export default function AdminAuditLogs() {
  const [items, setItems] = useState(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  const [q, setQ] = useState("");
  const [actionPrefix, setActionPrefix] = useState("");
  const [actor, setActor] = useState("");
  const [outcome, setOutcome] = useState("");
  const [cursor, setCursor] = useState(0);
  const [nextCursor, setNextCursor] = useState(null);
  const [openRef, setOpenRef] = useState(null);

  useEffect(() => {
    let cancelled = false;
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (actionPrefix) params.set("action_prefix", actionPrefix);
    if (actor) params.set("actor_email", actor);
    if (outcome) params.set("outcome", outcome);
    params.set("limit", "25");
    params.set("cursor", String(cursor));
    api.get(`/admin/portal/audit-logs?${params.toString()}`)
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
        setErr(e?.response?.data?.detail || "Failed to load audit logs.");
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [q, actionPrefix, actor, outcome, cursor]);

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-audit-logs-page">
      <div className="mb-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal · Audit Logs
        </div>
        <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">Audit log</h1>
        <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
          Read-only operator audit trail. Metadata is scrubbed before serialization.
          Stripe-shaped IDs are redacted; only opaque refs are surfaced.
        </p>
      </div>

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-4 mb-4 flex flex-wrap items-end gap-3"
           data-testid="admin-audit-logs-filters">
        <div className="flex-1 min-w-[220px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Search</label>
          <input
            type="text"
            value={q}
            onChange={(e) => { setCursor(0); setQ(e.target.value); }}
            placeholder="Action or actor email"
            data-testid="admin-audit-logs-search"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-equinesync-frost text-[13px] focus:outline-none focus:border-equinesync-slate"
          />
        </div>
        <div className="min-w-[180px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Action prefix</label>
          <input
            type="text"
            value={actionPrefix}
            onChange={(e) => { setCursor(0); setActionPrefix(e.target.value); }}
            placeholder="admin.portal."
            data-testid="admin-audit-logs-action-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          />
        </div>
        <div className="min-w-[160px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Outcome</label>
          <select
            value={outcome}
            onChange={(e) => { setCursor(0); setOutcome(e.target.value); }}
            data-testid="admin-audit-logs-outcome-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {OUTCOMES.map((o) => (<option key={o} value={o}>{o || "Any outcome"}</option>))}
          </select>
        </div>
        <div className="text-[11.5px] text-equinesync-graphite/55 ml-auto">{total.toLocaleString()} total</div>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-audit-logs-error">{err}</div>
      )}

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
        {loading && !items && (
          <div className="p-6 space-y-3" data-testid="admin-audit-logs-loading">
            {[0,1,2,3,4].map((i) => <div key={i} className="h-9 bg-equinesync-graphite/5 rounded animate-pulse" />)}
          </div>
        )}
        {!loading && items && items.length === 0 && (
          <div className="p-10 text-center text-[13px] text-equinesync-graphite/50" data-testid="admin-audit-logs-empty">
            No audit rows match the current filters.
          </div>
        )}
        {items && items.length > 0 && (
          <table className="w-full text-[13px]" data-testid="admin-audit-logs-table">
            <thead className="bg-equinesync-frost border-b border-equinesync-graphite/10">
              <tr className="text-left text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
                <th className="px-4 py-3 font-medium">When</th>
                <th className="px-4 py-3 font-medium">Action</th>
                <th className="px-4 py-3 font-medium">Actor</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Outcome</th>
                <th className="px-4 py-3 font-medium hidden lg:table-cell">Resource</th>
              </tr>
            </thead>
            <tbody>
              {items.map((row) => (
                <tr
                  key={row.admin_ref}
                  data-testid={`admin-audit-logs-row-${row.admin_ref}`}
                  onClick={() => setOpenRef(row.admin_ref)}
                  className="border-b border-equinesync-graphite/5 last:border-b-0 hover:bg-equinesync-frost cursor-pointer"
                >
                  <td className="px-4 py-3 text-equinesync-graphite/65 whitespace-nowrap">{formatTs(row.ts)}</td>
                  <td className="px-4 py-3 text-equinesync-graphite font-medium">{row.action}</td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">{row.actor_email || "—"}</td>
                  <td className="px-4 py-3 hidden md:table-cell">
                    {row.outcome ? <UserStatusBadge value={row.outcome} /> : <span className="text-equinesync-graphite/35">—</span>}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden lg:table-cell">
                    {row.resource?.kind || "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {items && items.length > 0 && (
          <div className="px-4 py-3 border-t border-equinesync-graphite/10 flex justify-between items-center text-[11.5px] text-equinesync-graphite/55"
               data-testid="admin-audit-logs-pagination">
            <div>Showing {cursor + 1}–{cursor + items.length} of {total.toLocaleString()}</div>
            <div className="flex gap-2">
              <button type="button" disabled={cursor === 0}
                      onClick={() => setCursor(Math.max(0, cursor - 25))}
                      data-testid="admin-audit-logs-prev"
                      className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40">Previous</button>
              <button type="button" disabled={nextCursor === null}
                      onClick={() => setCursor(nextCursor)}
                      data-testid="admin-audit-logs-next"
                      className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40">Next</button>
            </div>
          </div>
        )}
      </div>

      <AdminAuditLogDrawer
        key={openRef || "closed"}
        auditRef={openRef}
        open={!!openRef}
        onClose={() => setOpenRef(null)}
      />
    </div>
  );
}
