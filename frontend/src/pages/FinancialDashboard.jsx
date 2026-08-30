import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CreditCard, Landmark, RefreshCw, Receipt, TrendingUp } from "lucide-react";
import { api, fmtDate, money } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";

const STATUS_TONE = { paid: "success", open: "info", overdue: "critical", enrolled: "success", invited: "warning", paused: "critical", not_enrolled: "neutral" };

export default function FinancialDashboard() {
  const [invoices, setInvoices] = useState([]);
  const [payments, setPayments] = useState([]);
  const [recurring, setRecurring] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [invoiceRes, paymentRes, recurringRes, expenseRes, dashboardRes] = await Promise.all([
        api.get("/invoices"),
        api.get("/feature-modules/payments"),
        api.get("/feature-modules/recurring-billing"),
        api.get("/feature-modules/expenses"),
        api.get("/reports/backlog-dashboard"),
      ]);
      setInvoices(invoiceRes.data || []);
      setPayments(paymentRes.data.records || []);
      setRecurring(recurringRes.data.records || []);
      setExpenses(expenseRes.data.records || []);
      setDashboard(dashboardRes.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load financial dashboard.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const stats = useMemo(() => {
    const invoiceTotals = invoices.reduce((out, invoice) => {
      const status = invoice.status || "open";
      out[status] = (out[status] || 0) + Number(invoice.total || 0);
      return out;
    }, {});
    const mrr = recurring
      .filter((record) => ((record.data || {}).status || "active") === "active")
      .reduce((sum, record) => sum + Number((record.data || {}).amount || 0), 0);
    const expenseTotal = expenses.reduce((sum, record) => sum + Number((record.data || {}).amount || 0), 0);
    const autopayEnrolled = payments.filter((record) => ((record.data || {}).autopay_status || "") === "enrolled").length;
    const autopayInvited = payments.filter((record) => ((record.data || {}).autopay_status || "") === "invited").length;
    return {
      open: invoiceTotals.open || 0,
      overdue: invoiceTotals.overdue || 0,
      paid: invoiceTotals.paid || 0,
      mrr,
      expenseTotal,
      autopayEnrolled,
      autopayInvited,
      profitLoss: dashboard?.financial?.profit_loss ?? (invoiceTotals.paid || 0) - expenseTotal,
    };
  }, [dashboard, expenses, invoices, payments, recurring]);

  const recentExpenses = useMemo(() => [...expenses].sort((a, b) => String((b.data || {}).spent_at || b.created_at || "").localeCompare(String((a.data || {}).spent_at || a.created_at || ""))).slice(0, 6), [expenses]);
  const recentInvoices = useMemo(() => [...invoices].sort((a, b) => String(b.due_date || "").localeCompare(String(a.due_date || ""))).slice(0, 6), [invoices]);

  return (
    <div data-testid="financial-dashboard-page">
      <PageHeader
        eyebrow="Financial"
        title="Financial Dashboard"
        subtitle="Revenue, overdue invoices, auto-pay readiness, recurring billing, expense load, and profit/loss signals."
        action={
          <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="financial-dashboard-refresh">
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading financial dashboard...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Financial dashboard unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : invoices.length === 0 && payments.length === 0 && recurring.length === 0 && expenses.length === 0 ? (
        <Empty>
          <Landmark strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No financial records yet</div>
          <div className="text-[13px] text-equine-platinum/60">Create invoices, payment profiles, recurring rules, or expenses to populate this dashboard.</div>
        </Empty>
      ) : (
        <>
          <div className="grid grid-cols-2 xl:grid-cols-5 gap-4 mb-6">
            <Metric label="Open invoices" value={money(stats.open)} icon={Receipt} />
            <Metric label="Overdue" value={money(stats.overdue)} icon={AlertTriangle} tone="critical" />
            <Metric label="Paid" value={money(stats.paid)} icon={TrendingUp} tone="success" />
            <Metric label="Recurring" value={money(stats.mrr)} icon={CreditCard} />
            <Metric label="P/L signal" value={money(stats.profitLoss)} icon={Landmark} tone={stats.profitLoss >= 0 ? "success" : "critical"} />
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
            <Card hover={false} className="xl:col-span-2">
              <div className="label-eyebrow mb-2">Auto-pay readiness</div>
              <h2 className="font-display text-3xl text-equine-ink mb-5">Payment profiles</h2>
              <div className="grid grid-cols-2 gap-3 mb-5">
                <Compact label="Enrolled" value={stats.autopayEnrolled} tone="success" />
                <Compact label="Invited" value={stats.autopayInvited} tone="warning" />
              </div>
              <div className="space-y-3">
                {payments.slice(0, 6).map((record) => {
                  const data = record.data || {};
                  const status = data.autopay_status || "not_enrolled";
                  return (
                    <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`finance-payment-${record.id}`}>
                      <div className="flex items-center justify-between gap-3">
                        <div className="min-w-0">
                          <div className="font-display text-xl text-equine-ink truncate">{data.owner_name}</div>
                          <div className="text-[12px] text-equine-inkMuted">{data.provider || "manual"} - {data.customer_ref || "no customer ref"}</div>
                        </div>
                        <StatusPill tone={STATUS_TONE[status] || "neutral"}>{status.replace(/_/g, " ")}</StatusPill>
                      </div>
                    </div>
                  );
                })}
                {payments.length === 0 && <SoftEmpty text="No payment profiles yet." />}
              </div>
            </Card>

            <Card hover={false} className="xl:col-span-3">
              <div className="label-eyebrow mb-2">Revenue pipeline</div>
              <h2 className="font-display text-3xl text-equine-ink mb-5">Recent invoices</h2>
              <div className="space-y-3">
                {recentInvoices.map((invoice) => (
                  <div key={invoice.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`finance-invoice-${invoice.id}`}>
                    <div className="flex flex-col lg:flex-row lg:items-center gap-3">
                      <div className="flex-1 min-w-0">
                        <div className="font-display text-xl text-equine-ink truncate">{invoice.owner_name || "Owner"} - {invoice.horse_name || "Horse"}</div>
                        <div className="text-[12px] text-equine-inkMuted">Due {fmtDate(invoice.due_date)}</div>
                      </div>
                      <div className="font-display text-2xl text-equine-ink">{money(invoice.total)}</div>
                      <StatusPill tone={STATUS_TONE[invoice.status] || "info"}>{invoice.status || "open"}</StatusPill>
                    </div>
                  </div>
                ))}
                {recentInvoices.length === 0 && <SoftEmpty text="No invoices yet." />}
              </div>
            </Card>
          </div>

          <Card hover={false} className="mt-6">
            <div className="flex items-center justify-between gap-4 mb-5">
              <div>
                <div className="label-eyebrow mb-2">Expenses</div>
                <h2 className="font-display text-3xl text-equine-ink">Recent spend</h2>
              </div>
              <StatusPill tone="neutral">{money(stats.expenseTotal)} tracked</StatusPill>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-3">
              {recentExpenses.map((record) => {
                const data = record.data || {};
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`finance-expense-${record.id}`}>
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <div className="font-display text-xl text-equine-ink truncate">{data.vendor}</div>
                        <div className="text-[12px] text-equine-inkMuted capitalize">{data.category || "other"} - {fmtDate(data.spent_at)}</div>
                      </div>
                      <div className="font-display text-2xl text-equine-ink">{money(data.amount)}</div>
                    </div>
                  </div>
                );
              })}
              {recentExpenses.length === 0 && <SoftEmpty text="No expenses yet." />}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}

const Metric = ({ label, value, icon: Icon, tone }) => {
  const color = tone === "critical" ? "text-equine-clay" : tone === "success" ? "text-equine-sage" : "text-equine-ink";
  return (
    <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="label-eyebrow-muted mb-2">{label}</div>
          <div className={`font-display text-3xl text-equine-ink leading-none ${color}`}>{value}</div>
        </div>
        <Icon className="w-4 h-4 text-equine-lilac" />
      </div>
    </div>
  );
};

const Compact = ({ label, value, tone }) => (
  <div className="rounded-lg border border-equine-cloud bg-white/70 p-3">
    <div className="label-eyebrow-muted mb-1">{label}</div>
    <div className="flex items-end justify-between gap-2">
      <div className="font-display text-3xl text-equine-ink leading-none">{value}</div>
      <StatusPill tone={tone}>{label.toLowerCase()}</StatusPill>
    </div>
  </div>
);

const SoftEmpty = ({ text }) => (
  <div className="rounded-xl border border-dashed border-equine-cloud bg-white/45 py-8 text-center text-[13px] text-equine-inkMuted">
    {text}
  </div>
);
