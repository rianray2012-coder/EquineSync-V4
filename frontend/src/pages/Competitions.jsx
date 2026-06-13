import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CalendarDays, CheckCircle2, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["planning", "submitted", "accepted", "scratched"];
const STATUS_TONE = { planning: "info", submitted: "warning", accepted: "success", scratched: "critical" };
const ADD_FIELDS = [
  { key: "show_name", label: "Show", required: true, placeholder: "Show name", full: true },
  { key: "horse_name", label: "Horse", placeholder: "Horse name" },
  { key: "rider_name", label: "Rider", placeholder: "Rider name" },
  { key: "start_date", label: "Start", type: "date" },
  { key: "entry_status", label: "Entry", kind: "select", opts: STATUSES },
  { key: "results", label: "Results", kind: "textarea", rows: 3, full: true },
];

export default function Competitions() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/competitions");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load competitions.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const sorted = useMemo(() => [...records].sort((a, b) => String((a.data || {}).start_date || "9999").localeCompare(String((b.data || {}).start_date || "9999"))), [records]);
  const stats = useMemo(() => Object.fromEntries(STATUSES.map((status) => [
    status,
    records.filter((record) => ((record.data || {}).entry_status || "planning") === status).length,
  ])), [records]);

  const setStatus = async (record, entry_status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/competitions/records/${record.id}`, { data: { entry_status } });
      toast.success("Show entry updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update show entry");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/competitions/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive show entry");
    }
  };

  return (
    <div data-testid="competitions-page">
      <PageHeader
        eyebrow="Training"
        title="Shows & Competitions"
        subtitle="Track competition calendar dates, show entries, horse/rider assignments, entry status, and results."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="competitions-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="competitions-add">
              <Plus className="w-4 h-4" /> Add show
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {STATUSES.map((status) => (
          <Card key={status} hover={false} className="p-4">
            <div className="label-eyebrow-muted mb-2 capitalize">{status}</div>
            <div className="flex items-end justify-between gap-3">
              <div className="font-display text-4xl text-equine-ink leading-none">{stats[status]}</div>
              <StatusPill tone={STATUS_TONE[status]}>{status}</StatusPill>
            </div>
          </Card>
        ))}
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading shows…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Shows unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <CalendarDays strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No shows tracked</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a competition or show entry to start the calendar.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="competitions-empty-add">
            <Plus className="w-4 h-4" /> Add first show
          </button>
        </Empty>
      ) : (
        <Card hover={false} data-testid="competitions-list">
          <div className="space-y-3">
            {sorted.map((record) => {
              const data = record.data || {};
              const status = data.entry_status || "planning";
              return (
                <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`competition-row-${record.id}`}>
                  <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                    <div className="lg:w-32 flex-shrink-0">
                      <div className="label-eyebrow-muted mb-1">Start</div>
                      <div className="font-display text-2xl text-equine-ink leading-none">{fmtDate(data.start_date)}</div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-display text-2xl text-equine-ink truncate">{data.show_name}</div>
                      <div className="text-[12.5px] text-equine-inkMuted">
                        {data.horse_name || "Horse TBD"}{data.rider_name ? ` · ${data.rider_name}` : ""}
                      </div>
                      {data.results && <div className="mt-2 text-[13px] text-equine-inkMuted">{data.results}</div>}
                    </div>
                    <StatusPill tone={STATUS_TONE[status]}>{status}</StatusPill>
                    <div className="flex flex-wrap items-center gap-2 lg:justify-end">
                      {status !== "submitted" && <button type="button" onClick={() => setStatus(record, "submitted")} className="btn-secondary text-[12px] py-2 px-4">Submit</button>}
                      {status !== "accepted" && <button type="button" onClick={() => setStatus(record, "accepted")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1"><CheckCircle2 className="w-3.5 h-3.5" /> Accepted</button>}
                      {status !== "scratched" && <button type="button" onClick={() => setStatus(record, "scratched")} className="btn-secondary text-[12px] py-2 px-4">Scratch</button>}
                      <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink px-2">Archive</button>
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
        title="Add show entry"
        eyebrow="Training"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/competitions/records"
        initialValues={{ entry_status: "planning" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save show"
        testidPrefix="competitions-add"
        onCreated={load}
      />
    </div>
  );
}
