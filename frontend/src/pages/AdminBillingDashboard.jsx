// Phase 15.E — Platform-admin Billing Dashboard
// ---------------------------------------------------------------------------
// Read-only operational view over the Phase 15 subscription estate. Gated at
// the route level by ROLE_GROUPS.admin and at every API call by the backend
// `admin:access` capability. No mutating actions live here (role-elevation
// has its own surface inside AdminReviewQueue.jsx).
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { RefreshCw, AlertTriangle, Search, ChevronRight, X } from "lucide-react";

import { api } from "../lib/api";
import { Card, PageHeader, SectionEyebrow, StatusPill } from "../components/Primitives";
import { BrandLoader } from "../components/BrandLoader";
import { formatCents, PLAN_ORDER, STATUS_LABEL, STATUS_TONE } from "../lib/subscriptionBilling";

const PAGE_SIZE = 25;
const PLAN_FILTER_OPTIONS = PLAN_ORDER;
const planLabel = (tier) => (tier || "")
  .split("_")
  .filter(Boolean)
  .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
  .join(" ");

export default function AdminBillingDashboard() {
  const [loading, setLoading] = useState(true);
  const [overview, setOverview] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [err, setErr] = useState("");

  // subscriptions list
  const [subs, setSubs] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [statusFilter, setStatusFilter] = useState("");
  const [tierFilter, setTierFilter] = useState("");
  const [q, setQ] = useState("");

  // detail drawer
  const [detailId, setDetailId] = useState(null);

  const loadOverview = useCallback(async () => {
    const { data } = await api.get("/admin/billing/overview");
    setOverview(data);
  }, []);

  const loadSubs = useCallback(async () => {
    const params = new URLSearchParams({
      page: String(page), page_size: String(PAGE_SIZE),
    });
    if (statusFilter) params.set("status", statusFilter);
    if (tierFilter) params.set("tier", tierFilter);
    if (q.trim()) params.set("q", q.trim());
    const { data } = await api.get(`/admin/billing/subscriptions?${params.toString()}`);
    setSubs(data.items || []);
    setTotal(data.total || 0);
  }, [page, statusFilter, tierFilter, q]);

  useEffect(() => {
    (async () => {
      setLoading(true);
      setErr("");
      try {
        await Promise.all([loadOverview(), loadSubs()]);
      } catch (e) {
        setErr(e?.response?.data?.detail || "Could not load billing admin.");
      } finally {
        setLoading(false);
      }
    })();
  }, [loadOverview, loadSubs]);

  // Refilter without showing full-page loader
  useEffect(() => {
    if (loading) return;
    loadSubs().catch(() => { /* surfaced inline */ });
  }, [page, statusFilter, tierFilter, q, loading, loadSubs]);

  const refresh = useCallback(async () => {
    setRefreshing(true);
    try { await Promise.all([loadOverview(), loadSubs()]); }
    finally { setRefreshing(false); }
  }, [loadOverview, loadSubs]);

  const pages = useMemo(() => Math.max(1, Math.ceil(total / PAGE_SIZE)), [total]);

  if (loading) {
    return (
      <div data-testid="admin-billing-page" className="pb-20 lg:pb-8">
        <BrandLoader label="Loading billing admin…" />
      </div>
    );
  }

  return (
    <div data-testid="admin-billing-page" className="pb-20 lg:pb-8">
      <PageHeader
        eyebrow="Platform admin"
        title="Billing"
        subtitle="Subscription estate, MRR, stuck webhook events, and email-dispatch failures. Read-only."
        action={
          <button
            onClick={refresh}
            disabled={refreshing}
            data-testid="admin-billing-refresh"
            className="inline-flex items-center gap-1.5 text-[11.5px] uppercase tracking-[0.2em] text-equine-lilac/80 hover:text-equine-lavender transition-colors px-3 py-1.5 rounded-full border border-equine-graphite/40 hover:border-equine-lilac/50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? "animate-spin" : ""}`} />
            {refreshing ? "Refreshing…" : "Refresh"}
          </button>
        }
      />

      {err && (
        <Card hover={false} className="mb-6 border-equine-clay/40" data-testid="admin-billing-error">
          <div className="flex items-center gap-2 text-equine-clay text-[13.5px]">
            <AlertTriangle className="w-4 h-4" /> {err}
          </div>
        </Card>
      )}

      {/* ============ HEADLINE METRICS ============ */}
      <SectionEyebrow>Headline</SectionEyebrow>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10" data-testid="admin-billing-overview">
        <MetricCard
          label="Active subscriptions"
          value={(overview?.totals?.by_status?.active || 0) + (overview?.totals?.by_status?.trialing || 0)}
          subtext={`${overview?.totals?.by_status?.trialing || 0} trialing`}
          testid="metric-active-subs"
        />
        <MetricCard
          label="Committed MRR"
          value={formatCents(overview?.mrr?.committed_monthly_cents)}
          subtext="Active + trialing + past_due"
          testid="metric-committed-mrr"
        />
        <MetricCard
          label="Active MRR"
          value={formatCents(overview?.mrr?.active_monthly_cents)}
          subtext="Cash-collecting only"
          testid="metric-active-mrr"
        />
        <MetricCard
          label="Trials ending in 7 days"
          value={overview?.trials_ending_7d ?? 0}
          subtext=" "
          testid="metric-trials-ending"
        />
      </div>

      {/* ============ STUCK QUEUES ============ */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-10" data-testid="admin-billing-stuck">
        <StuckPanel
          title="Stuck billing events"
          subtitle={`Webhook rows in retry state, older than ${overview?.stuck?.threshold_minutes ?? 10} min`}
          loadPath="/admin/billing/stuck-events"
          count={overview?.stuck?.billing_events ?? 0}
          renderRow={(row) => (
            <RowKey label={row.stripe_event_id} subLabel={`${row.processing_status} · ${row.event_type || "—"}`} time={row.updated_at} />
          )}
          testid="stuck-events"
        />
        <StuckPanel
          title="Stuck subscription emails"
          subtitle="permanent_failure rows from the dispatcher log"
          loadPath="/admin/billing/stuck-emails"
          count={overview?.stuck?.subscription_emails ?? 0}
          renderRow={(row) => (
            <RowKey
              label={`${row.event_key}`}
              subLabel={`${row.subscription_id} · ${row.last_error || "—"}`}
              time={row.updated_at}
            />
          )}
          testid="stuck-emails"
        />
      </div>

      {/* ============ SUBSCRIPTIONS TABLE ============ */}
      <SectionEyebrow>Subscriptions</SectionEyebrow>
      <Card hover={false} className="mb-8">
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <div className="relative flex-1 min-w-[220px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-equine-inkSoft" />
            <input
              type="text"
              value={q}
              onChange={(e) => { setQ(e.target.value); setPage(1); }}
              placeholder="Search by owner email or barn id"
              className="w-full pl-9 pr-3 py-2 text-[13px] bg-equine-soft/50 border border-equine-hairline rounded-full focus:outline-none focus:border-equine-lilacDeep"
              data-testid="admin-billing-search"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
            data-testid="admin-billing-status-filter"
            className="text-[12.5px] px-3 py-2 bg-equine-soft/50 border border-equine-hairline rounded-full"
          >
            <option value="">All statuses</option>
            <option value="active">Active</option>
            <option value="trialing">Trialing</option>
            <option value="past_due">Past due</option>
            <option value="canceled">Canceled</option>
            <option value="incomplete">Incomplete</option>
          </select>
          <select
            value={tierFilter}
            onChange={(e) => { setTierFilter(e.target.value); setPage(1); }}
            data-testid="admin-billing-tier-filter"
            className="text-[12.5px] px-3 py-2 bg-equine-soft/50 border border-equine-hairline rounded-full"
          >
            <option value="">All tiers</option>
            {PLAN_FILTER_OPTIONS.map((tier) => (
              <option key={tier} value={tier}>{planLabel(tier)}</option>
            ))}
          </select>
        </div>

        <div className="overflow-x-auto -mx-1" data-testid="admin-billing-subs-table">
          <table className="w-full text-[13px]">
            <thead>
              <tr className="text-equine-inkSoft text-[10.5px] tracking-[0.2em] uppercase border-b border-equine-hairline">
                <th className="text-left px-2 py-2 font-medium">Barn / Owner</th>
                <th className="text-left px-2 py-2 font-medium">Tier</th>
                <th className="text-left px-2 py-2 font-medium">Status</th>
                <th className="text-right px-2 py-2 font-medium">MRR</th>
                <th className="text-left px-2 py-2 font-medium">Period end</th>
                <th className="px-2 py-2" />
              </tr>
            </thead>
            <tbody>
              {subs.length === 0 && (
                <tr><td colSpan={6} className="text-center py-10 text-equine-inkSoft text-[13px]" data-testid="admin-billing-subs-empty">No subscriptions match.</td></tr>
              )}
              {subs.map((s) => (
                <tr key={s.subscription_id} className="border-b border-equine-hairline/60 hover:bg-equine-soft/40 cursor-pointer" onClick={() => setDetailId(s.subscription_id)} data-testid={`admin-billing-row-${s.subscription_id}`}>
                  <td className="px-2 py-3">
                    <div className="text-equine-ink">{s.barn_name || s.barn_id || "—"}</div>
                    <div className="text-equine-inkSoft text-[11.5px]">{s.owner_email || "—"}</div>
                  </td>
                  <td className="px-2 py-3 capitalize">{s.plan_tier_code || "—"}</td>
                  <td className="px-2 py-3">
                    <StatusPill tone={STATUS_TONE[s.status] || "neutral"} dot>
                      {STATUS_LABEL[s.status] || s.status}
                    </StatusPill>
                  </td>
                  <td className="px-2 py-3 text-right tabular-nums">{formatCents(s.monthly_equivalent_cents)}</td>
                  <td className="px-2 py-3 text-equine-inkMuted">
                    {s.current_period_end ? new Date(s.current_period_end).toLocaleDateString() : "—"}
                  </td>
                  <td className="px-2 py-3 text-right text-equine-inkSoft"><ChevronRight className="w-3.5 h-3.5 inline" /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="mt-4 flex items-center justify-between text-[11.5px] text-equine-inkMuted">
          <div data-testid="admin-billing-pager-info">
            Showing {(subs.length === 0 ? 0 : (page - 1) * PAGE_SIZE + 1)}–{(page - 1) * PAGE_SIZE + subs.length} of {total}
          </div>
          <div className="flex items-center gap-2">
            <button
              disabled={page <= 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              className="px-3 py-1.5 rounded-full border border-equine-hairline disabled:opacity-40"
              data-testid="admin-billing-prev-page"
            >Prev</button>
            <span data-testid="admin-billing-page-indicator">Page {page} / {pages}</span>
            <button
              disabled={page >= pages}
              onClick={() => setPage((p) => Math.min(pages, p + 1))}
              className="px-3 py-1.5 rounded-full border border-equine-hairline disabled:opacity-40"
              data-testid="admin-billing-next-page"
            >Next</button>
          </div>
        </div>
      </Card>

      {/* Drawer */}
      {detailId && (
        <SubscriptionDetailDrawer
          subscriptionId={detailId}
          onClose={() => setDetailId(null)}
        />
      )}
    </div>
  );
}


// =============================================================================
// Subcomponents
// =============================================================================

function MetricCard({ label, value, subtext, testid }) {
  return (
    <Card data-testid={testid}>
      <div className="label-eyebrow mb-2">{label}</div>
      <div className="font-display text-3xl text-equine-ink leading-none" data-testid={`${testid}-value`}>
        {value}
      </div>
      <div className="mt-2 text-[11px] text-equine-inkSoft">{subtext}</div>
    </Card>
  );
}


function StuckPanel({ title, subtitle, loadPath, count, renderRow, testid }) {
  const [open, setOpen] = useState(false);
  const [rows, setRows] = useState(null);
  const [loadErr, setLoadErr] = useState("");

  const load = useCallback(async () => {
    setLoadErr("");
    try {
      const { data } = await api.get(loadPath);
      setRows(data.items || []);
    } catch (e) {
      setLoadErr(e?.response?.data?.detail || "Could not load.");
    }
  }, [loadPath]);

  useEffect(() => { if (open) load(); }, [open, load]);

  const tone = count > 0 ? "warning" : "success";
  return (
    <Card data-testid={testid}>
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <div className="font-display text-lg text-equine-ink">{title}</div>
          <div className="text-[12px] text-equine-inkMuted mt-0.5">{subtitle}</div>
        </div>
        <StatusPill tone={tone} dot>{count}</StatusPill>
      </div>
      <button
        onClick={() => setOpen((o) => !o)}
        data-testid={`${testid}-toggle`}
        className="text-[12px] tracking-wide text-equine-lilacDeep hover:text-equine-ink mt-2"
      >
        {open ? "Hide details" : count > 0 ? "Show details" : "Show recent (none)"}
      </button>
      {open && (
        <div className="mt-3 border-t border-equine-hairline pt-3 text-[12.5px] space-y-2" data-testid={`${testid}-list`}>
          {loadErr && <div className="text-equine-clay">{loadErr}</div>}
          {rows === null && !loadErr && <div className="text-equine-inkSoft">Loading…</div>}
          {rows && rows.length === 0 && <div className="text-equine-inkSoft" data-testid={`${testid}-empty`}>Nothing stuck.</div>}
          {rows && rows.map((r, i) => (
            <div key={i} className="border-b border-equine-hairline/40 pb-2 last:border-0" data-testid={`${testid}-row-${i}`}>
              {renderRow(r)}
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

function RowKey({ label, subLabel, time }) {
  return (
    <div className="flex items-start justify-between gap-3">
      <div className="min-w-0">
        <div className="text-equine-ink truncate">{label}</div>
        <div className="text-equine-inkSoft text-[11px] truncate">{subLabel}</div>
      </div>
      <div className="text-equine-inkSoft text-[11px] flex-shrink-0">{time ? new Date(time).toLocaleString() : ""}</div>
    </div>
  );
}


function SubscriptionDetailDrawer({ subscriptionId, onClose }) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api.get(`/admin/billing/subscriptions/${subscriptionId}`)
      .then((r) => { if (!cancelled) setData(r.data); })
      .catch((e) => { if (!cancelled) setErr(e?.response?.data?.detail || "Could not load."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [subscriptionId]);

  return (
    <div
      className="fixed inset-0 z-50 flex justify-end"
      data-testid="admin-billing-drawer"
      onClick={onClose}
    >
      <div className="absolute inset-0 bg-equine-ink/20" />
      <div
        className="relative w-full max-w-2xl bg-equine-elevated h-full overflow-y-auto p-8 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-6">
          <div>
            <div className="label-eyebrow mb-1">Subscription</div>
            <div className="font-display text-2xl text-equine-ink" data-testid="admin-billing-drawer-id">
              {subscriptionId}
            </div>
          </div>
          <button onClick={onClose} data-testid="admin-billing-drawer-close" className="p-2 rounded-full hover:bg-equine-soft">
            <X className="w-4 h-4 text-equine-inkMuted" />
          </button>
        </div>

        {loading && <BrandLoader label="Loading subscription…" />}
        {err && <div className="text-equine-clay text-[13px]">{err}</div>}

        {!loading && data && (
          <>
            <div className="grid grid-cols-2 gap-4 text-[13px] mb-8" data-testid="admin-billing-drawer-summary">
              <Detail label="Barn" value={data.subscription.barn_name || data.subscription.barn_id} />
              <Detail label="Owner" value={data.subscription.owner_email} />
              <Detail label="Tier" value={data.subscription.plan_tier_code} />
              <Detail label="Status">
                <StatusPill tone={STATUS_TONE[data.subscription.status] || "neutral"} dot>
                  {STATUS_LABEL[data.subscription.status] || data.subscription.status}
                </StatusPill>
              </Detail>
              <Detail label="Cycle" value={data.subscription.billing_cycle} />
              <Detail label="MRR" value={formatCents(data.subscription.monthly_equivalent_cents)} />
              <Detail label="Period end" value={data.subscription.current_period_end ? new Date(data.subscription.current_period_end).toLocaleDateString() : "—"} />
              <Detail label="Trial end" value={data.subscription.trial_end ? new Date(data.subscription.trial_end).toLocaleDateString() : "—"} />
            </div>

            <DetailList title="Recent invoices" items={data.invoices} testid="drawer-invoices" emptyText="No invoices yet." render={(i) => (
              <RowKey
                label={i.stripe_invoice_id}
                subLabel={`${i.status} · ${formatCents(i.amount_cents)}`}
                time={i.paid_at || i.payment_failed_at || i.created_at}
              />
            )} />

            <DetailList title="Recent webhook events" items={data.billing_events} testid="drawer-events" emptyText="No billing events yet." render={(e) => (
              <RowKey
                label={e.stripe_event_id}
                subLabel={`${e.processing_status} · ${e.event_type || "—"}`}
                time={e.updated_at || e.created_at}
              />
            )} />

            <DetailList title="Recent emails" items={data.email_log} testid="drawer-emails" emptyText="No emails dispatched yet." render={(e) => (
              <RowKey
                label={e.event_key}
                subLabel={`${e.status} · attempt ${e.attempt}`}
                time={e.updated_at}
              />
            )} />
          </>
        )}
      </div>
    </div>
  );
}

function Detail({ label, value, children }) {
  return (
    <div>
      <div className="label-eyebrow mb-1.5">{label}</div>
      <div className="text-equine-ink">{children || value || "—"}</div>
    </div>
  );
}

function DetailList({ title, items, testid, emptyText, render }) {
  return (
    <div className="mb-6" data-testid={testid}>
      <div className="label-eyebrow mb-3">{title}</div>
      <div className="space-y-2 text-[12.5px]">
        {(!items || items.length === 0) && <div className="text-equine-inkSoft text-[12px]" data-testid={`${testid}-empty`}>{emptyText}</div>}
        {items && items.map((it, i) => (
          <div key={i} className="border-b border-equine-hairline/40 pb-2 last:border-0" data-testid={`${testid}-row-${i}`}>{render(it)}</div>
        ))}
      </div>
    </div>
  );
}
