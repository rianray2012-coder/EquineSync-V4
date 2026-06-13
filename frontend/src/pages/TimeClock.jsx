import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, Clock3, Download, LogOut, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const ADD_FIELDS = [
  { key: "staff_name", label: "Staff", required: true, placeholder: "Staff name" },
  { key: "clock_in", label: "Clock in", required: true, placeholder: "YYYY-MM-DDTHH:MM:SS" },
  { key: "clock_out", label: "Clock out", placeholder: "YYYY-MM-DDTHH:MM:SS" },
  { key: "break_minutes", label: "Break minutes", type: "number", placeholder: "Minutes" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const fmtDateTime = (value) => {
  if (!value) return "Open";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
};

const hoursFor = (data) => {
  const start = new Date(data.clock_in || "").getTime();
  const end = new Date(data.clock_out || "").getTime();
  if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) return 0;
  const breakMinutes = Number(data.break_minutes || 0);
  return Math.max(0, (end - start) / 3600000 - breakMinutes / 60);
};

const csvCell = (value) => `"${String(value ?? "").replace(/"/g, '""')}"`;

export default function TimeClock() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);
  const [exporting, setExporting] = useState(false);
  const [exportManifest, setExportManifest] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/time-clock");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load time clock.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const sorted = useMemo(() => [...records].sort((a, b) => String((b.data || {}).clock_in || "").localeCompare(String((a.data || {}).clock_in || ""))), [records]);
  const totals = useMemo(() => ({
    open: records.filter((record) => !(record.data || {}).clock_out).length,
    hours: records.reduce((sum, record) => sum + hoursFor(record.data || {}), 0),
  }), [records]);

  const clockOut = async (record) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/time-clock/records/${record.id}`, { data: { clock_out: new Date().toISOString().slice(0, 16) } });
      toast.success("Clocked out");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not clock out");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/time-clock/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive time entry");
    }
  };

  const exportPayroll = async () => {
    setExporting(true);
    try {
      const r = await api.post("/staff-portal/payroll-export", {});
      const manifest = r.data;
      setExportManifest(manifest);
      const header = manifest.columns || ["staff_name", "clock_in", "clock_out", "break_minutes", "hours", "notes", "entry_id"];
      const rows = (manifest.rows || []).map((row) => header.map((column) => csvCell(row[column])).join(","));
      const csv = [header.join(","), ...rows].join("\n");
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = manifest.filename || `equinesync-payroll-export-${new Date().toISOString().slice(0, 10)}.csv`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Payroll export prepared");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare payroll export");
    } finally {
      setExporting(false);
    }
  };

  return (
    <div data-testid="time-clock-page">
      <PageHeader
        eyebrow="Staff"
        title="Time Clock"
        subtitle="Track clock-ins, clock-outs, breaks, notes, and payroll-ready export rows."
        action={
          <div className="flex items-center gap-3">
            <button onClick={exportPayroll} disabled={!records.length || exporting} className="btn-secondary inline-flex items-center gap-2 disabled:opacity-50" data-testid="time-clock-export">
              <Download className="w-4 h-4" /> {exporting ? "Preparing" : "Export"}
            </button>
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="time-clock-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="time-clock-add">
              <Plus className="w-4 h-4" /> Add entry
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
          <div className="label-eyebrow-muted mb-2">Open entries</div>
          <div className="font-display text-4xl text-equine-ink leading-none">{totals.open}</div>
        </div>
        <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
          <div className="label-eyebrow-muted mb-2">Payroll hours</div>
          <div className="font-display text-4xl text-equine-ink leading-none">{totals.hours.toFixed(2)}</div>
        </div>
      </div>

      {exportManifest && (
        <Card hover={false} className="mb-6" data-testid="time-clock-export-manifest">
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <div>
              <div className="label-eyebrow-muted mb-1">Latest payroll export</div>
              <div className="font-display text-2xl text-equine-ink">{exportManifest.filename}</div>
              <div className="text-[12.5px] text-equine-inkMuted">
                {exportManifest.row_count} row(s) · {Number(exportManifest.total_hours || 0).toFixed(2)} total hours
              </div>
            </div>
            <StatusPill tone="success">{exportManifest.status.replace(/_/g, " ")}</StatusPill>
          </div>
        </Card>
      )}

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading time clock...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Time clock unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Clock3 strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No time entries</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a clock-in record to start payroll-ready tracking.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="time-clock-empty-add">
            <Plus className="w-4 h-4" /> Add first entry
          </button>
        </Empty>
      ) : (
        <Card hover={false} data-testid="time-clock-list">
          <div className="space-y-3">
            {sorted.map((record) => {
              const data = record.data || {};
              const open = !data.clock_out;
              return (
                <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`time-clock-row-${record.id}`}>
                  <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="font-display text-2xl text-equine-ink truncate">{data.staff_name}</div>
                      <div className="text-[12.5px] text-equine-inkMuted">{fmtDateTime(data.clock_in)} - {fmtDateTime(data.clock_out)}</div>
                      {data.notes && <div className="mt-2 text-[13px] text-equine-inkMuted">{data.notes}</div>}
                    </div>
                    <StatusPill tone={open ? "warning" : "success"}>{open ? "clocked in" : `${hoursFor(data).toFixed(2)} hrs`}</StatusPill>
                    {open && (
                      <button type="button" onClick={() => clockOut(record)} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                        <LogOut className="w-3.5 h-3.5" /> Clock out
                      </button>
                    )}
                    <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink px-2">Archive</button>
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
        title="Add time entry"
        eyebrow="Staff"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/time-clock/records"
        initialValues={{ clock_in: new Date().toISOString().slice(0, 16), break_minutes: 0 }}
        transform={(form) => ({ data: form })}
        submitLabel="Save entry"
        testidPrefix="time-clock-add"
        onCreated={load}
      />
    </div>
  );
}
