import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, ClipboardList, PauseCircle, PlayCircle, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["open", "in_progress", "blocked", "complete"];
const STATUS_TONE = { open: "info", in_progress: "warning", blocked: "critical", complete: "success" };
const ADD_FIELDS = [
  { key: "title", label: "Task", required: true, placeholder: "Reset rehab stall mats", full: true },
  { key: "assigned_to", label: "Assigned to", placeholder: "Sophia Reyes" },
  { key: "due_at", label: "Due", placeholder: "2026-06-12T12:00:00" },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "handoff_notes", label: "Handoff notes", kind: "textarea", rows: 4, full: true },
];

const fmtDateTime = (value) => {
  if (!value) return "No due time";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
};

export default function StaffTasks() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/staff-tasks");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load staff tasks.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const grouped = useMemo(() => {
    const out = Object.fromEntries(STATUSES.map((status) => [status, []]));
    records.forEach((record) => {
      const status = (record.data || {}).status || "open";
      (out[status] || out.open).push(record);
    });
    Object.values(out).forEach((rows) => rows.sort((a, b) => String((a.data || {}).due_at || "9999").localeCompare(String((b.data || {}).due_at || "9999"))));
    return out;
  }, [records]);

  const setStatus = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/staff-tasks/records/${record.id}`, { data: { status } });
      toast.success("Task updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update task");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/staff-tasks/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive task");
    }
  };

  return (
    <div data-testid="staff-tasks-page">
      <PageHeader
        eyebrow="Staff"
        title="Task Assignments"
        subtitle="Assign staff work, track completion, and keep handoff notes attached to the task record."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="staff-tasks-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="staff-tasks-add">
              <Plus className="w-4 h-4" /> Add task
            </button>
          </div>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading staff tasks...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Staff tasks unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <ClipboardList strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No staff tasks</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Create a task with an assignee, due time, and handoff note.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="staff-tasks-empty-add">
            <Plus className="w-4 h-4" /> Add first task
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-4">
          {STATUSES.map((status) => (
            <Card key={status} hover={false} className="p-4" data-testid={`staff-tasks-${status}`}>
              <div className="flex items-center justify-between mb-3">
                <div className="label-eyebrow capitalize">{status.replace(/_/g, " ")}</div>
                <StatusPill tone={STATUS_TONE[status]}>{grouped[status].length}</StatusPill>
              </div>
              <div className="space-y-3">
                {grouped[status].map((record) => {
                  const data = record.data || {};
                  return (
                    <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`staff-task-card-${record.id}`}>
                      <div className="font-display text-xl leading-none text-equine-ink">{data.title}</div>
                      <div className="text-[12px] text-equine-inkMuted mt-2">{data.assigned_to || "Unassigned"} - Due {fmtDateTime(data.due_at)}</div>
                      {data.handoff_notes && <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{data.handoff_notes}</div>}
                      <div className="hairline mt-3 pt-3 flex flex-wrap items-center gap-2">
                        {status !== "in_progress" && (
                          <button type="button" onClick={() => setStatus(record, "in_progress")} className="text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1">
                            <PlayCircle className="w-3.5 h-3.5" /> Start
                          </button>
                        )}
                        {status !== "complete" && (
                          <button type="button" onClick={() => setStatus(record, "complete")} className="text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1">
                            <CheckCircle2 className="w-3.5 h-3.5" /> Complete
                          </button>
                        )}
                        {status !== "blocked" && (
                          <button type="button" onClick={() => setStatus(record, "blocked")} className="text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1">
                            <PauseCircle className="w-3.5 h-3.5" /> Block
                          </button>
                        )}
                        <button type="button" onClick={() => archiveRecord(record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">
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
        title="Add staff task"
        eyebrow="Staff"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/staff-tasks/records"
        initialValues={{ status: "open" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save task"
        testidPrefix="staff-tasks-add"
        onCreated={load}
      />
    </div>
  );
}
