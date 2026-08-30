import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CalendarClock, Clock, Plus, RefreshCw, StickyNote } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { normalizeStaffDirectory, staffNameById, staffOptions } from "../lib/staffDirectory";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const fmtDateTime = (value) => {
  if (!value) return "TBD";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
};

const shiftState = (data) => {
  const now = Date.now();
  const start = new Date(data.shift_start || "").getTime();
  const end = new Date(data.shift_end || "").getTime();
  if (Number.isFinite(end) && end < now) return "complete";
  if (Number.isFinite(start) && start <= now && (!Number.isFinite(end) || end >= now)) return "active";
  return "upcoming";
};

const toneFor = { upcoming: "info", active: "warning", complete: "success" };

export default function StaffScheduling() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [staff, setStaff] = useState([]);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [r, staffRes] = await Promise.all([
        api.get("/feature-modules/staff-scheduling"),
        api.get("/staff-portal/staff-directory"),
      ]);
      setRecords(r.data.records || []);
      setStaff(normalizeStaffDirectory(staffRes.data));
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load staff schedule.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const addFields = useMemo(() => [
    { key: "staff_user_id", label: "Staff", kind: "select", required: true, opts: staffOptions(staff) },
    { key: "role", label: "Role", placeholder: "Groom" },
    { key: "shift_start", label: "Start", required: true, placeholder: "YYYY-MM-DDTHH:MM:SS" },
    { key: "shift_end", label: "End", placeholder: "YYYY-MM-DDTHH:MM:SS" },
    { key: "area", label: "Area", placeholder: "Barn area" },
    { key: "notes", label: "Shift notes", kind: "textarea", rows: 3, full: true },
  ], [staff]);

  const sorted = useMemo(() => [...records].sort((a, b) => String((a.data || {}).shift_start || "").localeCompare(String((b.data || {}).shift_start || ""))), [records]);
  const stats = useMemo(() => sorted.reduce((out, record) => {
    const state = shiftState(record.data || {});
    out[state] += 1;
    return out;
  }, { upcoming: 0, active: 0, complete: 0 }), [sorted]);

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/staff-scheduling/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive shift");
    }
  };

  return (
    <div data-testid="staff-scheduling-page">
      <PageHeader
        eyebrow="Staff"
        title="Staff Scheduling"
        subtitle="Plan shifts by staff member, role, barn area, notes, and handoff context for the day."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="staff-scheduling-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="staff-scheduling-add">
              <Plus className="w-4 h-4" /> Add shift
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-3 gap-4 mb-6">
        {Object.entries(stats).map(([state, count]) => (
          <div key={state} className="rounded-lg border border-equine-cloud bg-white/70 p-4">
            <div className="label-eyebrow-muted mb-2 capitalize">{state}</div>
            <div className="font-display text-4xl text-equine-ink leading-none">{count}</div>
          </div>
        ))}
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading staff schedule...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Staff schedule unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <CalendarClock strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No shifts scheduled</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a staff shift with area coverage and handoff notes.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="staff-scheduling-empty-add">
            <Plus className="w-4 h-4" /> Add first shift
          </button>
        </Empty>
      ) : (
        <div className="space-y-4">
          {sorted.map((record) => {
            const data = record.data || {};
            const state = shiftState(data);
            return (
              <Card key={record.id} hover={false} data-testid={`staff-shift-${record.id}`}>
                <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                  <div className="lg:w-56 flex-shrink-0">
                    <div className="label-eyebrow-muted mb-1">Shift</div>
                    <div className="text-equine-ink font-display text-2xl leading-none">{fmtDateTime(data.shift_start)}</div>
                    <div className="text-[12px] text-equine-inkMuted mt-1 inline-flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" /> Ends {fmtDateTime(data.shift_end)}
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.staff_name}</div>
                    <div className="text-[12.5px] text-equine-inkMuted">{data.role || "Role TBD"} - {data.area || "Area TBD"}</div>
                    {data.notes && (
                      <div className="mt-2 text-[13px] text-equine-inkMuted inline-flex items-start gap-2">
                        <StickyNote className="w-3.5 h-3.5 mt-0.5 flex-shrink-0" /> <span>{data.notes}</span>
                      </div>
                    )}
                  </div>
                  <StatusPill tone={toneFor[state]}>{state}</StatusPill>
                  <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink lg:self-end">
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
        title="Add staff shift"
        eyebrow="Staff"
        fields={addFields}
        endpoint="/feature-modules/staff-scheduling/records"
        initialValues={{ shift_start: new Date().toISOString().slice(0, 16) }}
        transform={(form) => ({ data: { ...form, staff_name: staffNameById(staff, form.staff_user_id) } })}
        submitLabel="Save shift"
        testidPrefix="staff-scheduling-add"
        onCreated={load}
      />
    </div>
  );
}
