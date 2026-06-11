import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CalendarClock, CheckCircle2, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["expired", "due", "scheduled", "complete"];
const STATUS_TONE = { expired: "critical", due: "warning", scheduled: "info", complete: "success" };

const ADD_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Valentino" },
  { key: "reminder_type", label: "Type", kind: "select", opts: ["vaccine", "coggins", "dental", "deworming"] },
  { key: "due_date", label: "Due date", type: "date", required: true },
  { key: "provider", label: "Provider", placeholder: "Dr. Henrik Vossler" },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const computeStatus = (data) => {
  if (data.status === "complete") return "complete";
  if (!data.due_date) return data.status || "scheduled";
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const due = new Date(data.due_date);
  if (!Number.isNaN(due.getTime()) && due < today) return "expired";
  return data.status || "scheduled";
};

export default function HealthReminders() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/health-reminders");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load health reminders.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const grouped = useMemo(() => {
    const out = Object.fromEntries(STATUSES.map((status) => [status, []]));
    records.forEach((record) => {
      const status = computeStatus(record.data || {});
      (out[status] || out.scheduled).push(record);
    });
    Object.values(out).forEach((rows) => rows.sort((a, b) => String((a.data || {}).due_date || "").localeCompare(String((b.data || {}).due_date || ""))));
    return out;
  }, [records]);

  const setStatus = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/health-reminders/records/${record.id}`, { data: { status } });
      toast.success("Reminder updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update reminder");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/health-reminders/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive reminder");
    }
  };

  return (
    <div data-testid="health-reminders-page">
      <PageHeader
        eyebrow="Health"
        title="Vaccines & Coggins"
        subtitle="Track vaccination, Coggins, dental, and deworming due dates with clear overdue and completion states."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="health-reminders-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="health-reminders-add">
              <Plus className="w-4 h-4" /> Add reminder
            </button>
          </div>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading reminders…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Health reminders unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <CalendarClock strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No reminders yet</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a vaccine or Coggins due date to start tracking.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="health-reminders-empty-add">
            <Plus className="w-4 h-4" /> Add first reminder
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-4">
          {STATUSES.map((status) => (
            <Card key={status} hover={false} className="p-4" data-testid={`health-reminders-${status}`}>
              <div className="flex items-center justify-between mb-3">
                <div className="label-eyebrow capitalize">{status}</div>
                <StatusPill tone={STATUS_TONE[status]}>{grouped[status].length}</StatusPill>
              </div>
              <div className="space-y-3">
                {grouped[status].map((record) => {
                  const data = record.data || {};
                  return (
                    <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`health-reminder-card-${record.id}`}>
                      <div className="flex items-start justify-between gap-2">
                        <div className="min-w-0">
                          <div className="font-display text-xl leading-none text-equine-ink truncate">{data.horse_name}</div>
                          <div className="text-[12.5px] text-equine-inkMuted mt-1 capitalize">{(data.reminder_type || "health").replace(/_/g, " ")}</div>
                        </div>
                        <StatusPill tone={STATUS_TONE[status]}>{status}</StatusPill>
                      </div>
                      <div className="mt-3 text-[12.5px] text-equine-inkMuted">
                        Due {fmtDate(data.due_date)}
                        {data.provider ? ` · ${data.provider}` : ""}
                      </div>
                      {data.notes && <div className="mt-2 text-[12.5px] text-equine-ink leading-relaxed">{data.notes}</div>}
                      <div className="hairline mt-3 pt-3 flex items-center justify-between gap-2">
                        {status !== "complete" ? (
                          <button type="button" onClick={() => setStatus(record, "complete")} className="text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1" data-testid={`health-reminder-complete-${record.id}`}>
                            <CheckCircle2 className="w-3.5 h-3.5" /> Mark complete
                          </button>
                        ) : (
                          <button type="button" onClick={() => setStatus(record, "scheduled")} className="text-[12px] text-equine-navy hover:text-equine-saddle">
                            Reopen
                          </button>
                        )}
                        <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink">
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
        title="Add health reminder"
        eyebrow="Health"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/health-reminders/records"
        initialValues={{ reminder_type: "vaccine", status: "scheduled" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save reminder"
        testidPrefix="health-reminders-add"
        onCreated={load}
      />
    </div>
  );
}
