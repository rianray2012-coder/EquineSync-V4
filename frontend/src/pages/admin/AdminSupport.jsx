/**
 * AdminSupport — support ticket inbox (Admin-6).
 *
 * Read + gated mutations (status change, assign, add note).
 * support_admin, platform_admin, super_admin can mutate.
 * billing_admin / read_only_auditor → 403 from the server.
 *
 * Strict guardrails:
 *   - Opaque `st_*` refs only.
 *   - Approved palette only.
 *   - Note body NEVER appears in audit metadata (server enforces; tests
 *     plant `STRIPELEAK`, `sub_*`, `token`, `password` payloads and
 *     assert the audit row carries only `note_present: true`).
 */
import React, { useEffect, useState } from "react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";
import AdminSupportDrawer from "./AdminSupportDrawer";
import OperationalProofPanel from "../../components/OperationalProofPanel";

const STATUS_OPTIONS = ["", "new", "in_progress", "waiting", "resolved"];

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

export default function AdminSupport() {
  const [items, setItems] = useState(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  const [status, setStatus] = useState("");
  const [q, setQ] = useState("");
  const [cursor, setCursor] = useState(0);
  const [nextCursor, setNextCursor] = useState(null);
  const [openRef, setOpenRef] = useState(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    const params = new URLSearchParams();
    if (status) params.set("status", status);
    if (q) params.set("q", q);
    params.set("limit", "25");
    params.set("cursor", String(cursor));
    api.get(`/admin/portal/support?${params.toString()}`)
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
        setErr(e?.response?.data?.detail || "Failed to load tickets.");
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [status, q, cursor, reloadKey]);

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-support-page">
      <div className="mb-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal · Support
        </div>
        <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">Support inbox</h1>
        <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
          Tickets submitted by users. Status changes, assignments, and internal notes
          are audit-logged. Note bodies stay in the ticket record only.
        </p>
      </div>

      <OperationalProofPanel
        proofKey="support"
        title="Support Proof Snapshot"
        testid="support-proof-snapshot"
      />

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-4 mb-4 flex flex-wrap items-end gap-3"
           data-testid="admin-support-filters">
        <div className="flex-1 min-w-[220px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Search</label>
          <input type="text" value={q}
                 onChange={(e) => { setCursor(0); setQ(e.target.value); }}
                 placeholder="Subject or submitter email"
                 data-testid="admin-support-search"
                 className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-equinesync-frost text-[13px] focus:outline-none focus:border-equinesync-slate" />
        </div>
        <div className="min-w-[160px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Status</label>
          <select value={status}
                  onChange={(e) => { setCursor(0); setStatus(e.target.value); }}
                  data-testid="admin-support-status-filter"
                  className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]">
            {STATUS_OPTIONS.map((o) => (<option key={o} value={o}>{o || "Any status"}</option>))}
          </select>
        </div>
        <div className="text-[11.5px] text-equinesync-graphite/55 ml-auto">{total.toLocaleString()} total</div>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-support-error">{err}</div>
      )}

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
        {loading && !items && (
          <div className="p-6 space-y-3" data-testid="admin-support-loading">
            {[0,1,2,3,4].map((i) => <div key={i} className="h-9 bg-equinesync-graphite/5 rounded animate-pulse" />)}
          </div>
        )}
        {!loading && items && items.length === 0 && (
          <div className="p-10 text-center text-[13px] text-equinesync-graphite/50" data-testid="admin-support-empty">
            No tickets match the current filters.
          </div>
        )}
        {items && items.length > 0 && (
          <table className="w-full text-[13px]" data-testid="admin-support-table">
            <thead className="bg-equinesync-frost border-b border-equinesync-graphite/10">
              <tr className="text-left text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
                <th className="px-4 py-3 font-medium">Subject</th>
                <th className="px-4 py-3 font-medium">Facility</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Assignee</th>
                <th className="px-4 py-3 font-medium hidden lg:table-cell">Updated</th>
              </tr>
            </thead>
            <tbody>
              {items.map((t) => (
                <tr key={t.admin_ref}
                    data-testid={`admin-support-row-${t.admin_ref}`}
                    onClick={() => setOpenRef(t.admin_ref)}
                    className="border-b border-equinesync-graphite/5 last:border-b-0 hover:bg-equinesync-frost cursor-pointer">
                  <td className="px-4 py-3">
                    <div className="text-equinesync-graphite font-medium">{t.subject || "—"}</div>
                    <div className="text-equinesync-graphite/55 text-[11.5px] font-mono">{t.admin_ref}</div>
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">{t.facility_name || t.barn_id || "—"}</td>
                  <td className="px-4 py-3">
                    {t.status ? <UserStatusBadge value={t.status} /> : <span className="text-equinesync-graphite/35">—</span>}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75 hidden md:table-cell">{t.assignee_email || "Unassigned"}</td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden lg:table-cell">{formatTs(t.updated_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {items && items.length > 0 && (
          <div className="px-4 py-3 border-t border-equinesync-graphite/10 flex justify-between items-center text-[11.5px] text-equinesync-graphite/55"
               data-testid="admin-support-pagination">
            <div>Showing {cursor + 1}–{cursor + items.length} of {total.toLocaleString()}</div>
            <div className="flex gap-2">
              <button type="button" disabled={cursor === 0}
                      onClick={() => setCursor(Math.max(0, cursor - 25))}
                      data-testid="admin-support-prev"
                      className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40">Previous</button>
              <button type="button" disabled={nextCursor === null}
                      onClick={() => setCursor(nextCursor)}
                      data-testid="admin-support-next"
                      className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40">Next</button>
            </div>
          </div>
        )}
      </div>

      <AdminSupportDrawer
        key={openRef || "closed"}
        ticketRef={openRef}
        open={!!openRef}
        onClose={() => setOpenRef(null)}
        onMutated={() => setReloadKey((k) => k + 1)}
      />
    </div>
  );
}
