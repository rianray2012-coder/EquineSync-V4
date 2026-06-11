import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, CloudSun, Plus, RefreshCw, Trees } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["planned", "active", "weather_hold", "complete"];
const STATUS_TONE = {
  planned: "info",
  active: "success",
  weather_hold: "warning",
  complete: "neutral",
};

const ADD_FIELDS = [
  { key: "pasture", label: "Pasture", required: true, placeholder: "North Field" },
  { key: "group_name", label: "Group", placeholder: "Geldings A" },
  { key: "horse_names", label: "Horses", kind: "textarea", rows: 3, full: true, placeholder: "Valentino, Mercury" },
  { key: "start_time", label: "Start", placeholder: "08:00" },
  { key: "end_time", label: "End", placeholder: "14:00" },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "weather_rule", label: "Weather rule", kind: "textarea", rows: 3, full: true },
];

const timeValue = (s) => String(s || "99:99");

export default function PastureSchedule() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/pasture-schedule");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load pasture schedule.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const sorted = useMemo(() => [...records].sort((a, b) => {
    const ad = a.data || {};
    const bd = b.data || {};
    return timeValue(ad.start_time).localeCompare(timeValue(bd.start_time))
      || String(ad.pasture || "").localeCompare(String(bd.pasture || ""));
  }), [records]);

  const stats = useMemo(() => Object.fromEntries(STATUSES.map((status) => [
    status,
    records.filter((record) => ((record.data || {}).status || "planned") === status).length,
  ])), [records]);

  const setStatus = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/pasture-schedule/records/${record.id}`, { data: { status } });
      toast.success("Schedule updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update schedule");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/pasture-schedule/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive block");
    }
  };

  return (
    <div data-testid="pasture-schedule-page">
      <PageHeader
        eyebrow="Operations"
        title="Pasture Schedule"
        subtitle="Plan turnout groups by pasture, time block, and weather rule without replacing the existing Today turnout task flow."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="pasture-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="pasture-add">
              <Plus className="w-4 h-4" /> Add block
            </button>
          </div>
        }
      />

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
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading pasture schedule…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Pasture schedule unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Trees strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No pasture blocks planned</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a turnout block for a pasture or group.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="pasture-empty-add">
            <Plus className="w-4 h-4" /> Add first block
          </button>
        </Empty>
      ) : (
        <Card hover={false} data-testid="pasture-list">
          <div className="space-y-3">
            {sorted.map((record) => {
              const data = record.data || {};
              const status = data.status || "planned";
              return (
                <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`pasture-row-${record.id}`}>
                  <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                    <div className="w-full lg:w-32 flex-shrink-0">
                      <div className="label-eyebrow-muted mb-1">Time</div>
                      <div className="font-display text-2xl text-equine-ink leading-none">{data.start_time || "—"}</div>
                      <div className="text-[12px] text-equine-inkMuted mt-1">to {data.end_time || "—"}</div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <div className="font-display text-2xl text-equine-ink truncate">{data.pasture}</div>
                        <StatusPill tone={STATUS_TONE[status]}>{status.replace(/_/g, " ")}</StatusPill>
                      </div>
                      <div className="text-[13px] text-equine-inkMuted">{data.group_name || "Group TBD"}</div>
                      {data.horse_names && <div className="text-[13px] text-equine-ink mt-1">{data.horse_names}</div>}
                      {data.weather_rule && (
                        <div className="mt-2 inline-flex items-start gap-2 text-[12px] text-equine-inkMuted bg-equine-card border border-equine-hairline rounded-lg px-3 py-2">
                          <CloudSun className="w-3.5 h-3.5 mt-0.5 flex-shrink-0" />
                          <span>{data.weather_rule}</span>
                        </div>
                      )}
                    </div>
                    <div className="flex flex-wrap items-center gap-2 lg:justify-end">
                      <button type="button" onClick={() => setStatus(record, "active")} className="btn-secondary text-[12px] py-2 px-4" disabled={status === "active"}>Start</button>
                      <button type="button" onClick={() => setStatus(record, "weather_hold")} className="btn-secondary text-[12px] py-2 px-4" disabled={status === "weather_hold"}>Hold</button>
                      <button type="button" onClick={() => setStatus(record, "complete")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1" disabled={status === "complete"}>
                        <CheckCircle2 className="w-3.5 h-3.5" /> Done
                      </button>
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
        title="Add pasture block"
        eyebrow="Operations"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/pasture-schedule/records"
        initialValues={{ status: "planned" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save block"
        testidPrefix="pasture-add"
        onCreated={load}
      />
    </div>
  );
}
