import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CreditCard, Landmark, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["not_enrolled", "invited", "enrolled", "paused"];
const STATUS_TONE = { not_enrolled: "neutral", invited: "warning", enrolled: "success", paused: "critical" };

const ADD_FIELDS = [
  { key: "owner_name", label: "Owner", required: true, placeholder: "Charlotte Vance", full: true },
  { key: "provider", label: "Provider", kind: "select", opts: ["stripe", "manual"] },
  { key: "autopay_status", label: "Auto-pay", kind: "select", opts: STATUSES },
  { key: "customer_ref", label: "Customer ref", placeholder: "cus_…" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

export default function Payments() {
  const [records, setRecords] = useState([]);
  const [placeholders, setPlaceholders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [moduleRes, placeholderRes] = await Promise.all([
        api.get("/feature-modules/payments"),
        api.get("/integrations/placeholders"),
      ]);
      setRecords(moduleRes.data.records || []);
      setPlaceholders((placeholderRes.data || []).filter((p) => p.provider === "stripe"));
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load payments.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const stats = useMemo(() => Object.fromEntries(STATUSES.map((status) => [
    status,
    records.filter((record) => ((record.data || {}).autopay_status || "not_enrolled") === status).length,
  ])), [records]);

  const setStatus = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/payments/records/${record.id}`, { data: { autopay_status: status } });
      toast.success("Auto-pay status updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update auto-pay");
    } finally {
      setSavingId(null);
    }
  };

  const prepareStripe = async () => {
    try {
      const r = await api.post("/integrations/stripe/prepare");
      toast.success(r.data.message || "Stripe placeholder ready");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare Stripe");
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/payments/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive payment profile");
    }
  };

  return (
    <div data-testid="payments-page">
      <PageHeader
        eyebrow="Financial"
        title="Payments & Auto-Pay"
        subtitle="Track owner payment provider references and auto-pay enrollment status. Stripe integration is ready for credentials, checkout, and webhooks."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="payments-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="payments-add">
              <Plus className="w-4 h-4" /> Add profile
            </button>
          </div>
        }
      />

      <Card hover={false} className="mb-6 border-equine-brass/30 bg-equine-brass/5">
        <div className="flex flex-col lg:flex-row lg:items-center gap-4">
          <div className="flex items-start gap-3 flex-1">
            <CreditCard className="w-4 h-4 text-equine-champagne mt-0.5 flex-shrink-0" />
            <div>
              <div className="text-equine-ink text-[14px]">Stripe-ready placeholder</div>
              <div className="text-[12.5px] text-equine-inkMuted mt-1">
                No credentials or card data are stored here. Live checkout and webhooks stay behind the integration abstraction.
              </div>
              {placeholders[0] && <div className="text-[11.5px] text-equine-inkSoft mt-2">{placeholders[0].ready_for.join(" · ")}</div>}
            </div>
          </div>
          <button type="button" onClick={prepareStripe} className="btn-secondary text-[12px] py-2 px-4" data-testid="prepare-stripe">
            Prepare Stripe
          </button>
        </div>
      </Card>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {STATUSES.map((status) => (
          <Card key={status} hover={false} className="p-4">
            <div className="label-eyebrow-muted mb-2 capitalize">{status.replace(/_/g, " ")}</div>
            <div className="flex items-end justify-between gap-3">
              <div className="font-display text-4xl text-equine-ink leading-none">{stats[status]}</div>
              <StatusPill tone={STATUS_TONE[status]}>{status.replace(/_/g, " ")}</StatusPill>
            </div>
          </Card>
        ))}
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading payment profiles…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Payments unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Landmark strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No payment profiles</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add an owner payment profile or auto-pay invite status.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="payments-empty-add">
            <Plus className="w-4 h-4" /> Add first profile
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-5">
          {records.map((record) => {
            const data = record.data || {};
            const status = data.autopay_status || "not_enrolled";
            return (
              <Card key={record.id} hover={false} className={savingId === record.id ? "opacity-60" : ""} data-testid={`payment-card-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.owner_name}</div>
                    <div className="text-[12.5px] text-equine-inkMuted capitalize">{data.provider || "manual"}</div>
                  </div>
                  <StatusPill tone={STATUS_TONE[status]}>{status.replace(/_/g, " ")}</StatusPill>
                </div>
                <div className="text-[13px] text-equine-inkMuted space-y-2">
                  <div>Customer ref: <span className="text-equine-ink">{data.customer_ref || "—"}</span></div>
                  {data.notes && <div className="text-equine-ink leading-relaxed">{data.notes}</div>}
                </div>
                <div className="hairline mt-4 pt-3 flex flex-wrap items-center gap-2">
                  {STATUSES.map((next) => (
                    <button
                      key={next}
                      type="button"
                      onClick={() => setStatus(record, next)}
                      disabled={status === next}
                      className="text-[11.5px] px-2.5 py-1.5 rounded-full border border-equine-hairline bg-equine-soft text-equine-inkMuted hover:text-equine-ink disabled:opacity-35 disabled:pointer-events-none"
                    >
                      {next.replace(/_/g, " ")}
                    </button>
                  ))}
                  <button type="button" onClick={() => archiveRecord(record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">
                    Archive
                  </button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add payment profile"
        eyebrow="Financial"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/payments/records"
        initialValues={{ provider: "stripe", autopay_status: "not_enrolled" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save profile"
        testidPrefix="payments-add"
        onCreated={load}
      />
    </div>
  );
}
