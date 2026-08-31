import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CalendarClock, PauseCircle, PlayCircle, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate, money } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["active", "paused", "draft"];
const FREQUENCIES = ["monthly", "weekly", "per_lesson", "custom"];
const STATUS_TONE = { active: "success", paused: "warning", draft: "neutral" };

const ADD_FIELDS = [
  { key: "name", label: "Rule", required: true, placeholder: "Billing rule name", full: true },
  { key: "owner_name", label: "Owner", placeholder: "Owner name" },
  { key: "horse_name", label: "Horse", placeholder: "Horse name" },
  { key: "amount", label: "Amount", type: "number", required: true },
  { key: "frequency", label: "Frequency", kind: "select", opts: FREQUENCIES },
  { key: "next_run_date", label: "Next run", type: "date" },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
];

const monthlyValue = (data) => {
  const amount = Number(data.amount) || 0;
  if (data.frequency === "weekly") return amount * 4.33;
  if (data.frequency === "monthly") return amount;
  return 0;
};

export default function RecurringBilling() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/recurring-billing");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load recurring billing.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const stats = useMemo(() => {
    const active = records.filter((record) => (record.data || {}).status === "active");
    return {
      active: active.length,
      paused: records.filter((record) => (record.data || {}).status === "paused").length,
      draft: records.filter((record) => ((record.data || {}).status || "draft") === "draft").length,
      monthly: active.reduce((sum, record) => sum + monthlyValue(record.data || {}), 0),
    };
  }, [records]);

  const setStatus = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/recurring-billing/records/${record.id}`, { data: { status } });
      toast.success("Billing rule updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update billing rule");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/recurring-billing/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive rule");
    }
  };

  return (
    <div data-testid="recurring-billing-page">
      <PageHeader
        eyebrow="Financial"
        title="Recurring Billing"
        subtitle="Define recurring charge rules for board, training, lessons, and custom services. Invoice automation remains review-first."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="recurring-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="recurring-add">
              <Plus className="w-4 h-4" /> Add rule
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <Kpi label="Active rules" value={stats.active} tone="success" />
        <Kpi label="Paused" value={stats.paused} tone="warning" />
        <Kpi label="Draft" value={stats.draft} tone="neutral" />
        <Kpi label="Est. monthly" value={money(stats.monthly)} tone="info" />
      </div>

      <Card hover={false} className="mb-6 border-equine-icy/30 bg-equine-icy/5">
        <div className="flex items-start gap-3">
          <CalendarClock className="w-4 h-4 text-equine-lilac mt-0.5 flex-shrink-0" />
          <div className="text-[13px] text-equine-inkMuted leading-relaxed">
            These rules are automation-ready data. They do not create invoices automatically until a reviewed invoice generation service is enabled.
          </div>
        </div>
      </Card>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading recurring rules…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Recurring billing unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <CalendarClock strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No recurring rules</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a board, training, lesson, or custom recurring charge.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="recurring-empty-add">
            <Plus className="w-4 h-4" /> Add first rule
          </button>
        </Empty>
      ) : (
        <Card hover={false} data-testid="recurring-list">
          <div className="space-y-3">
            {records.map((record) => {
              const data = record.data || {};
              const status = data.status || "draft";
              return (
                <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`recurring-row-${record.id}`}>
                  <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <div className="font-display text-2xl text-equine-ink truncate">{data.name}</div>
                        <StatusPill tone={STATUS_TONE[status]}>{status}</StatusPill>
                      </div>
                      <div className="text-[13px] text-equine-inkMuted">
                        {data.owner_name || "Owner TBD"}{data.horse_name ? ` · ${data.horse_name}` : ""}
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-3 min-w-[240px]">
                      <Metric label="Amount" value={money(data.amount)} />
                      <Metric label="Frequency" value={(data.frequency || "custom").replace(/_/g, " ")} />
                    </div>
                    <div className="text-[12.5px] text-equine-inkMuted lg:w-28">Next {fmtDate(data.next_run_date)}</div>
                    <div className="flex items-center gap-2 lg:justify-end">
                      {status === "active" ? (
                        <button type="button" onClick={() => setStatus(record, "paused")} className="btn-secondary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                          <PauseCircle className="w-3.5 h-3.5" /> Pause
                        </button>
                      ) : (
                        <button type="button" onClick={() => setStatus(record, "active")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                          <PlayCircle className="w-3.5 h-3.5" /> Activate
                        </button>
                      )}
                      <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink px-2">
                        Archive
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add recurring rule"
        eyebrow="Financial"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/recurring-billing/records"
        initialValues={{ frequency: "monthly", status: "draft" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save rule"
        testidPrefix="recurring-add"
        onCreated={load}
      />
    </div>
  );
}

const Kpi = ({ label, value, tone }) => (
  <Card hover={false} className="p-4">
    <div className="label-eyebrow-muted mb-2">{label}</div>
    <div className="flex items-end justify-between gap-3">
      <div className="font-display text-4xl text-equine-ink leading-none">{value}</div>
      <StatusPill tone={tone}>{label.split(" ")[0]}</StatusPill>
    </div>
  </Card>
);

const Metric = ({ label, value }) => (
  <div className="rounded-lg border border-equine-hairline bg-equine-card p-3">
    <div className="label-eyebrow-muted mb-1">{label}</div>
    <div className="font-display text-2xl text-equine-ink leading-none capitalize">{value}</div>
  </div>
);
