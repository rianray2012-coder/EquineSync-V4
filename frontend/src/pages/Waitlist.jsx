import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, ArrowRight, ClipboardList, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["new", "contacted", "offered", "scheduled", "closed"];
const PRIORITY_TONE = { high: "critical", normal: "info", low: "neutral" };

const ADD_FIELDS = [
  { key: "client_name", label: "Client", required: true, placeholder: "Client name", full: true },
  { key: "horse_name", label: "Horse", placeholder: "Horse name" },
  { key: "service_type", label: "Service", kind: "select", opts: ["board", "training", "lesson", "rehab"] },
  { key: "priority", label: "Priority", kind: "select", opts: ["low", "normal", "high"] },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "target_date", label: "Target date", type: "date" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

export default function Waitlist() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/waitlist");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load waitlist.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const grouped = useMemo(() => {
    const out = Object.fromEntries(STATUSES.map((status) => [status, []]));
    records.forEach((record) => {
      const status = (record.data || {}).status || "new";
      (out[status] || out.new).push(record);
    });
    Object.values(out).forEach((rows) => rows.sort((a, b) => {
      const priority = { high: 0, normal: 1, low: 2 };
      const ap = priority[(a.data || {}).priority || "normal"] ?? 1;
      const bp = priority[(b.data || {}).priority || "normal"] ?? 1;
      if (ap !== bp) return ap - bp;
      return String((a.data || {}).target_date || "").localeCompare(String((b.data || {}).target_date || ""));
    }));
    return out;
  }, [records]);

  const updateStatus = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/waitlist/records/${record.id}`, { data: { status } });
      toast.success("Waitlist updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update status");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/waitlist/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive entry");
    }
  };

  return (
    <div data-testid="waitlist-page">
      <PageHeader
        eyebrow="Operations"
        title="Waitlist"
        subtitle="Track board, training, lesson, and rehab prospects from first inquiry to scheduled move-in."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="waitlist-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="waitlist-add">
              <Plus className="w-4 h-4" /> Add prospect
            </button>
          </div>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading waitlist…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Waitlist unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <ClipboardList strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No prospects waiting</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add the first inquiry and keep the pipeline visible.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="waitlist-empty-add">
            <Plus className="w-4 h-4" /> Add first prospect
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
          {STATUSES.map((status, index) => (
            <Card key={status} hover={false} className="p-4 min-h-[280px]" data-testid={`waitlist-column-${status}`}>
              <div className="flex items-center justify-between mb-3">
                <div className="label-eyebrow capitalize">{status}</div>
                <StatusPill tone="neutral">{grouped[status].length}</StatusPill>
              </div>
              <div className="space-y-3">
                {grouped[status].map((record) => {
                  const data = record.data || {};
                  const nextStatus = STATUSES[Math.min(index + 1, STATUSES.length - 1)];
                  return (
                    <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`waitlist-card-${record.id}`}>
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <div className="min-w-0">
                          <div className="font-display text-xl leading-none text-equine-ink truncate">{data.client_name}</div>
                          <div className="text-[12.5px] text-equine-inkMuted mt-1 truncate">{data.horse_name || "Horse TBD"}</div>
                        </div>
                        <StatusPill tone={PRIORITY_TONE[data.priority] || "info"}>{data.priority || "normal"}</StatusPill>
                      </div>
                      <div className="text-[12px] text-equine-inkMuted space-y-1">
                        <div>{(data.service_type || "board").replace(/_/g, " ")}</div>
                        <div>Target {fmtDate(data.target_date)}</div>
                      </div>
                      {data.notes && <div className="mt-3 text-[12.5px] text-equine-ink leading-relaxed">{data.notes}</div>}
                      <div className="hairline mt-3 pt-3 flex items-center justify-between gap-2">
                        {status !== "closed" ? (
                          <button
                            type="button"
                            onClick={() => updateStatus(record, nextStatus)}
                            className="text-[12px] text-equine-navy hover:text-equine-lilac inline-flex items-center gap-1"
                            data-testid={`waitlist-advance-${record.id}`}
                          >
                            Move to {nextStatus} <ArrowRight className="w-3 h-3" />
                          </button>
                        ) : <span className="text-[11px] text-equine-inkSoft">Completed pipeline</span>}
                        <button
                          type="button"
                          onClick={() => archiveRecord(record)}
                          className="text-[12px] text-equine-clay hover:text-equine-ink"
                          data-testid={`waitlist-archive-${record.id}`}
                        >
                          Archive
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          ))}
        </div>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add waitlist prospect"
        eyebrow="Operations"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/waitlist/records"
        initialValues={{ priority: "normal", status: "new", service_type: "board" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save prospect"
        testidPrefix="waitlist-add"
        onCreated={load}
      />
    </div>
  );
}
