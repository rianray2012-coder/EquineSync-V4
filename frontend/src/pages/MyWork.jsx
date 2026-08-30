import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CalendarDays, CheckCircle2, Clock, ClipboardList, FileText, LogIn, LogOut, PauseCircle, PlayCircle, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, PageHeader, StatusPill } from "../components/Primitives";

const STATUS_TONE = { open: "info", in_progress: "warning", blocked: "critical", complete: "success" };

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

export default function MyWork() {
  const [work, setWork] = useState({ shifts: [], tasks: [], handoffs: [], time_entries: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [savingId, setSavingId] = useState(null);
  const [clockBusy, setClockBusy] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/staff-portal/my-work");
      setWork({
        shifts: r.data?.shifts || [],
        tasks: r.data?.tasks || [],
        handoffs: r.data?.handoffs || [],
        time_entries: r.data?.time_entries || [],
      });
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load your work.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const openTimeEntry = useMemo(
    () => work.time_entries.find((record) => !(record.data || {}).clock_out),
    [work.time_entries],
  );

  const updateTask = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/staff-portal/tasks/${record.id}/status`, { data: { status } });
      toast.success("Task updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update task");
    } finally {
      setSavingId(null);
    }
  };

  const clockIn = async () => {
    setClockBusy(true);
    try {
      await api.post("/staff-portal/time-clock/clock-in");
      toast.success("Clocked in");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not clock in");
    } finally {
      setClockBusy(false);
    }
  };

  const clockOut = async () => {
    if (!openTimeEntry) return;
    setClockBusy(true);
    try {
      await api.post(`/staff-portal/time-clock/${openTimeEntry.id}/clock-out`);
      toast.success("Clocked out");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not clock out");
    } finally {
      setClockBusy(false);
    }
  };

  return (
    <div data-testid="my-work-page">
      <PageHeader
        eyebrow="Daily"
        title="My Work"
        subtitle="Your assigned shifts, tasks, handoff notes, and time clock controls in one focused view."
        action={
          <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="my-work-refresh">
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading your work…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">My Work unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : (
        <>
          <Card className="mb-6" hover={false} data-testid="my-work-clock-card">
            <div className="flex items-center justify-between gap-4 flex-wrap">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
                  <Clock strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
                </div>
                <div>
                  <h2 className="font-display text-2xl text-equine-ink">Time Clock</h2>
                  <div className="text-[12.5px] text-equine-inkMuted">
                    {openTimeEntry ? `Clocked in ${fmtDateTime((openTimeEntry.data || {}).clock_in)}` : "No open time entry."}
                  </div>
                </div>
              </div>
              {openTimeEntry ? (
                <button onClick={clockOut} disabled={clockBusy} className="btn-primary inline-flex items-center gap-2 disabled:opacity-60" data-testid="my-work-clock-out">
                  <LogOut className="w-4 h-4" /> Clock out
                </button>
              ) : (
                <button onClick={clockIn} disabled={clockBusy} className="btn-primary inline-flex items-center gap-2 disabled:opacity-60" data-testid="my-work-clock-in">
                  <LogIn className="w-4 h-4" /> Clock in
                </button>
              )}
            </div>
          </Card>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
            <WorkSection title="My Shifts" icon={CalendarDays} empty="No shifts assigned.">
              {work.shifts.map((record) => {
                const data = record.data || {};
                const state = shiftState(data);
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`my-shift-${record.id}`}>
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="font-display text-xl text-equine-ink">{data.area || "Shift"}</div>
                      <StatusPill tone={state === "active" ? "warning" : state === "complete" ? "success" : "info"}>{state}</StatusPill>
                    </div>
                    <div className="text-[12.5px] text-equine-inkMuted">{fmtDateTime(data.shift_start)} - {fmtDateTime(data.shift_end)}</div>
                    {data.notes && <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{data.notes}</div>}
                  </div>
                );
              })}
            </WorkSection>

            <WorkSection title="My Tasks" icon={ClipboardList} empty="No tasks assigned.">
              {work.tasks.map((record) => {
                const data = record.data || {};
                const status = data.status || "open";
                return (
                  <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`my-task-${record.id}`}>
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="font-display text-xl text-equine-ink">{data.title || "Task"}</div>
                      <StatusPill tone={STATUS_TONE[status]}>{status.replace(/_/g, " ")}</StatusPill>
                    </div>
                    <div className="text-[12.5px] text-equine-inkMuted">Due {fmtDateTime(data.due_at)}</div>
                    {data.handoff_notes && <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{data.handoff_notes}</div>}
                    <div className="hairline mt-3 pt-3 flex flex-wrap gap-2">
                      {status !== "in_progress" && <TaskButton onClick={() => updateTask(record, "in_progress")} icon={PlayCircle}>Start</TaskButton>}
                      {status !== "complete" && <TaskButton onClick={() => updateTask(record, "complete")} icon={CheckCircle2}>Complete</TaskButton>}
                      {status !== "blocked" && <TaskButton onClick={() => updateTask(record, "blocked")} icon={PauseCircle}>Block</TaskButton>}
                    </div>
                  </div>
                );
              })}
            </WorkSection>

            <WorkSection title="Handoffs" icon={FileText} empty="No handoff reports assigned.">
              {work.handoffs.map((record) => {
                const data = record.data || {};
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`my-handoff-${record.id}`}>
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="font-display text-xl text-equine-ink">{data.area || "Handoff"}</div>
                      <StatusPill tone={data.status === "reviewed" ? "success" : data.status === "submitted" ? "warning" : "neutral"}>{data.status || "draft"}</StatusPill>
                    </div>
                    <div className="text-[12.5px] text-equine-inkMuted">{data.shift_date || "No date"} · {data.outgoing_staff || "Outgoing"} to {data.incoming_staff || "Incoming"}</div>
                    <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{data.summary || "No summary"}</div>
                    {data.open_items && <div className="text-[12.5px] text-equine-ink mt-2 leading-relaxed">{data.open_items}</div>}
                  </div>
                );
              })}
            </WorkSection>
          </div>
        </>
      )}
    </div>
  );
}

const WorkSection = ({ title, icon: Icon, empty, children }) => {
  const hasChildren = React.Children.count(children) > 0;
  return (
    <Card hover={false} className="p-4">
      <div className="flex items-center gap-2 mb-4">
        <Icon className="w-4 h-4 text-equine-inkSoft" />
        <h2 className="font-display text-2xl text-equine-ink">{title}</h2>
      </div>
      {hasChildren ? <div className="space-y-3">{children}</div> : (
        <div className="rounded-xl border border-dashed border-equine-hairline bg-equine-soft/45 py-8 text-center text-[13px] text-equine-inkMuted">
          {empty}
        </div>
      )}
    </Card>
  );
};

const TaskButton = ({ onClick, icon: Icon, children }) => (
  <button type="button" onClick={onClick} className="text-[12px] text-equine-navy hover:text-equine-lilac inline-flex items-center gap-1">
    <Icon className="w-3.5 h-3.5" /> {children}
  </button>
);
