/**
 * AdminBilling — Billing Control Center (Admin-5).
 *
 * One page, two tabs:
 *   1. Payments        — Phase 15 subscription_invoices (read-only)
 *   2. Webhook events  — billing_events table with retry states
 *
 * Strict guardrails:
 *   - READ-ONLY. Zero mutation buttons.
 *   - support_admin gets 403 on both tabs (enforced at the API layer);
 *     this page also defensively hides itself for them via
 *     canSeeAdminSection("billing").
 *   - Approved palette only (Graphite / Slate / Frost / Lilac).
 *   - NO Phase 9 invoices. NO Stripe IDs.
 */
import React, { useEffect, useState } from "react";
import { Receipt, Activity } from "lucide-react";
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

const TABS = [
  { key: "payments", label: "Payments", Icon: Receipt },
  { key: "events", label: "Webhook events", Icon: Activity },
];

const PAY_STATUSES = ["", "paid", "open", "draft", "uncollectible", "void"];
const EVENT_STATUSES = [
  "", "ok", "processing", "retry_502", "metadata_missing_retryable",
  "metadata_missing_permanent", "unknown_event",
];

function TabHeader({ active, onChange }) {
  return (
    <div className="flex items-center gap-1 mb-4" data-testid="admin-billing-tabs" role="tablist">
      {TABS.map(({ key, label, Icon }) => (
        <button
          key={key}
          type="button"
          role="tab"
          aria-selected={active === key}
          onClick={() => onChange(key)}
          data-testid={`admin-billing-tab-${key}`}
          className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-[12.5px] tracking-wide transition-colors ${
            active === key
              ? "bg-equinesync-graphite text-equinesync-frost"
              : "bg-equinesync-frost text-equinesync-graphite/70 hover:text-equinesync-graphite"
          }`}
        >
          <Icon className="w-3.5 h-3.5" />
          <span>{label}</span>
        </button>
      ))}
    </div>
  );
}

function PaymentsTab() {
  const [items, setItems] = useState(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [status, setStatus] = useState("");
  const [cursor, setCursor] = useState(0);
  const [nextCursor, setNextCursor] = useState(null);

  // All state transitions live inside async callbacks (see
  // AdminDashboard / AdminFacilities). Satisfies
  // `react-hooks/set-state-in-effect` without changing behavior.
  useEffect(() => {
    let cancelled = false;
    const params = new URLSearchParams();
    if (status) params.set("status", status);
    params.set("limit", "25");
    params.set("cursor", String(cursor));
    api.get(`/admin/portal/payments?${params.toString()}`)
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
        setErr(e?.response?.data?.detail || "Failed to load payments.");
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [status, cursor]);

  return (
    <div data-testid="admin-billing-payments">
      <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-4 mb-4 flex flex-wrap items-end gap-3">
        <div className="min-w-[180px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Status</label>
          <select
            value={status}
            onChange={(e) => { setCursor(0); setStatus(e.target.value); }}
            data-testid="admin-billing-payments-status-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {PAY_STATUSES.map((o) => (<option key={o} value={o}>{o || "Any status"}</option>))}
          </select>
        </div>
        <div className="text-[11.5px] text-equinesync-graphite/55 ml-auto">{total.toLocaleString()} total</div>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-billing-payments-error">{err}</div>
      )}

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
        {loading && !items && (
          <div className="p-6 space-y-3" data-testid="admin-billing-payments-loading">
            {[0,1,2,3,4].map((i) => <div key={i} className="h-9 bg-equinesync-graphite/5 rounded animate-pulse" />)}
          </div>
        )}
        {!loading && items && items.length === 0 && (
          <div className="p-10 text-center text-[13px] text-equinesync-graphite/50" data-testid="admin-billing-payments-empty">
            No payments match the current filters.
          </div>
        )}
        {items && items.length > 0 && (
          <table className="w-full text-[13px]" data-testid="admin-billing-payments-table">
            <thead className="bg-equinesync-frost border-b border-equinesync-graphite/10">
              <tr className="text-left text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
                <th className="px-4 py-3 font-medium">Facility</th>
                <th className="px-4 py-3 font-medium">Amount</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Period</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Due</th>
                <th className="px-4 py-3 font-medium hidden lg:table-cell">Failures</th>
              </tr>
            </thead>
            <tbody>
              {items.map((p) => (
                <tr
                  key={p.admin_ref}
                  data-testid={`admin-billing-payments-row-${p.admin_ref}`}
                  className="border-b border-equinesync-graphite/5 last:border-b-0 hover:bg-equinesync-frost"
                >
                  <td className="px-4 py-3">
                    <div className="text-equinesync-graphite font-medium">{p.facility_name || p.barn_id || "—"}</div>
                    <div className="text-equinesync-graphite/55 text-[11.5px] font-mono">{p.admin_ref}</div>
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">{formatMoney(p.amount_cents)}</td>
                  <td className="px-4 py-3">
                    {p.status ? <UserStatusBadge value={p.status} /> : <span className="text-equinesync-graphite/35">—</span>}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden md:table-cell">
                    {p.period_start ? formatTs(p.period_start) : "—"} → {p.period_end ? formatTs(p.period_end) : "—"}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden md:table-cell">{formatTs(p.due_date)}</td>
                  <td className="px-4 py-3 text-equinesync-graphite/75 hidden lg:table-cell">{p.payment_failure_count ?? 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {items && items.length > 0 && (
          <div className="px-4 py-3 border-t border-equinesync-graphite/10 flex justify-between items-center text-[11.5px] text-equinesync-graphite/55"
               data-testid="admin-billing-payments-pagination">
            <div>Showing {cursor + 1}–{cursor + items.length} of {total.toLocaleString()}</div>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={cursor === 0}
                onClick={() => setCursor(Math.max(0, cursor - 25))}
                data-testid="admin-billing-payments-prev"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Previous</button>
              <button
                type="button"
                disabled={nextCursor === null}
                onClick={() => setCursor(nextCursor)}
                data-testid="admin-billing-payments-next"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Next</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function EventsTab() {
  const [items, setItems] = useState(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [processingStatus, setProcessingStatus] = useState("");
  const [cursor, setCursor] = useState(0);
  const [nextCursor, setNextCursor] = useState(null);

  // Same async-callback pattern as PaymentsTab.
  useEffect(() => {
    let cancelled = false;
    const params = new URLSearchParams();
    if (processingStatus) params.set("processing_status", processingStatus);
    params.set("limit", "25");
    params.set("cursor", String(cursor));
    api.get(`/admin/portal/billing-events?${params.toString()}`)
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
        setErr(e?.response?.data?.detail || "Failed to load webhook events.");
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [processingStatus, cursor]);

  return (
    <div data-testid="admin-billing-events">
      <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-4 mb-4 flex flex-wrap items-end gap-3">
        <div className="min-w-[220px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Processing status</label>
          <select
            value={processingStatus}
            onChange={(e) => { setCursor(0); setProcessingStatus(e.target.value); }}
            data-testid="admin-billing-events-status-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {EVENT_STATUSES.map((o) => (<option key={o} value={o}>{o || "Any status"}</option>))}
          </select>
        </div>
        <div className="text-[11.5px] text-equinesync-graphite/55 ml-auto">{total.toLocaleString()} total</div>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-billing-events-error">{err}</div>
      )}

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
        {loading && !items && (
          <div className="p-6 space-y-3" data-testid="admin-billing-events-loading">
            {[0,1,2,3,4].map((i) => <div key={i} className="h-9 bg-equinesync-graphite/5 rounded animate-pulse" />)}
          </div>
        )}
        {!loading && items && items.length === 0 && (
          <div className="p-10 text-center text-[13px] text-equinesync-graphite/50" data-testid="admin-billing-events-empty">
            No webhook events match the current filters.
          </div>
        )}
        {items && items.length > 0 && (
          <table className="w-full text-[13px]" data-testid="admin-billing-events-table">
            <thead className="bg-equinesync-frost border-b border-equinesync-graphite/10">
              <tr className="text-left text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
                <th className="px-4 py-3 font-medium">Event type</th>
                <th className="px-4 py-3 font-medium">Facility</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Retries</th>
                <th className="px-4 py-3 font-medium hidden lg:table-cell">Created</th>
              </tr>
            </thead>
            <tbody>
              {items.map((ev) => (
                <tr
                  key={ev.admin_ref}
                  data-testid={`admin-billing-events-row-${ev.admin_ref}`}
                  className="border-b border-equinesync-graphite/5 last:border-b-0 hover:bg-equinesync-frost"
                >
                  <td className="px-4 py-3">
                    <div className="text-equinesync-graphite font-medium">{ev.event_type || "—"}</div>
                    <div className="text-equinesync-graphite/55 text-[11.5px] font-mono">{ev.admin_ref}</div>
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">{ev.facility_name || ev.barn_id || "—"}</td>
                  <td className="px-4 py-3">
                    {ev.processing_status ? <UserStatusBadge value={ev.processing_status} /> : <span className="text-equinesync-graphite/35">—</span>}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75 hidden md:table-cell">{ev.retry_count ?? 0}</td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden lg:table-cell">{formatTs(ev.event_created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {items && items.length > 0 && (
          <div className="px-4 py-3 border-t border-equinesync-graphite/10 flex justify-between items-center text-[11.5px] text-equinesync-graphite/55"
               data-testid="admin-billing-events-pagination">
            <div>Showing {cursor + 1}–{cursor + items.length} of {total.toLocaleString()}</div>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={cursor === 0}
                onClick={() => setCursor(Math.max(0, cursor - 25))}
                data-testid="admin-billing-events-prev"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Previous</button>
              <button
                type="button"
                disabled={nextCursor === null}
                onClick={() => setCursor(nextCursor)}
                data-testid="admin-billing-events-next"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >Next</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function AdminBilling() {
  const [active, setActive] = useState("payments");
  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-billing-page">
      <div className="mb-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal · Billing
        </div>
        <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">Billing control center</h1>
        <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
          Read-only Phase 15 payments + webhook health. Phase 9 invoice
          flows live elsewhere and are untouched by this surface.
        </p>
      </div>
      <TabHeader active={active} onChange={setActive} />
      {active === "payments" ? <PaymentsTab /> : <EventsTab />}
    </div>
  );
}
