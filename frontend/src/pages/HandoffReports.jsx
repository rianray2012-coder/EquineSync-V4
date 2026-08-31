import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, ClipboardList, FileText, Plus, RefreshCw, Send } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { normalizeStaffDirectory, staffNameById, staffOptions } from "../lib/staffDirectory";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import OperationalProofPanel from "../components/OperationalProofPanel";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["draft", "submitted", "reviewed"];
const STATUS_TONE = { draft: "neutral", submitted: "warning", reviewed: "success" };
const PRIORITY_TONE = { low: "neutral", normal: "info", high: "critical" };

const today = () => new Date().toISOString().slice(0, 10);
const labelFor = (value) => String(value || "").replace(/_/g, " ");

export default function HandoffReports() {
  const [reports, setReports] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [shifts, setShifts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);
  const [staff, setStaff] = useState([]);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [reportRes, taskRes, shiftRes, staffRes] = await Promise.all([
        api.get("/feature-modules/handoff-reports"),
        api.get("/feature-modules/staff-tasks"),
        api.get("/feature-modules/staff-scheduling"),
        api.get("/staff-portal/staff-directory"),
      ]);
      setReports(reportRes.data.records || []);
      setTasks(taskRes.data.records || []);
      setShifts(shiftRes.data.records || []);
      setStaff(normalizeStaffDirectory(staffRes.data));
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load handoff reports.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const addFields = useMemo(() => [
    { key: "shift_date", label: "Shift date", type: "date", required: true },
    { key: "outgoing_staff_user_id", label: "Outgoing staff", kind: "select", required: true, opts: staffOptions(staff) },
    { key: "incoming_staff_user_id", label: "Incoming staff", kind: "select", required: true, opts: staffOptions(staff) },
    { key: "area", label: "Area", placeholder: "Barn area" },
    { key: "priority", label: "Priority", kind: "select", opts: ["low", "normal", "high"] },
    { key: "status", label: "Status", kind: "select", opts: STATUSES },
    { key: "summary", label: "Summary", kind: "textarea", rows: 4, required: true, full: true },
    { key: "open_items", label: "Open items", kind: "textarea", rows: 4, full: true },
  ], [staff]);

  const stats = useMemo(() => Object.fromEntries(STATUSES.map((status) => [
    status,
    reports.filter((record) => ((record.data || {}).status || "draft") === status).length,
  ])), [reports]);

  const openTasks = useMemo(() => tasks
    .filter((record) => !["complete"].includes((record.data || {}).status || "open"))
    .sort((a, b) => String((a.data || {}).due_at || "").localeCompare(String((b.data || {}).due_at || "")))
    .slice(0, 6), [tasks]);

  const shiftNotes = useMemo(() => shifts
    .filter((record) => (record.data || {}).notes)
    .sort((a, b) => String((b.data || {}).shift_start || "").localeCompare(String((a.data || {}).shift_start || "")))
    .slice(0, 4), [shifts]);

  const sorted = useMemo(() => [...reports].sort((a, b) => String((b.data || {}).shift_date || b.created_at || "").localeCompare(String((a.data || {}).shift_date || a.created_at || ""))), [reports]);

  const updateStatus = async (record, status) => {
    setSavingId(record.id);
    const data = { status };
    if (status === "submitted") data.submitted_at = new Date().toISOString();
    if (status === "reviewed") data.reviewed_at = new Date().toISOString();
    try {
      await api.patch(`/feature-modules/handoff-reports/records/${record.id}`, { data });
      toast.success("Handoff report updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update handoff report");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/handoff-reports/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive handoff report");
    }
  };

  return (
    <div data-testid="handoff-reports-page">
      <PageHeader
        eyebrow="Staff"
        title="Shift Handoff Reports"
        subtitle="Capture outgoing notes, incoming staff context, open items, priority, and manager review state for each shift handoff."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="handoff-reports-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="handoff-reports-add">
              <Plus className="w-4 h-4" /> Add report
            </button>
          </div>
        }
      />

      <OperationalProofPanel
        proofKey="handoff"
        title="Handoff Proof Snapshot"
        testid="handoff-proof-snapshot"
      />

      <div className="grid grid-cols-3 gap-4 mb-6">
        {STATUSES.map((status) => (
          <Metric key={status} label={labelFor(status)} value={stats[status]} tone={STATUS_TONE[status]} />
        ))}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-5 gap-6 mb-6">
        <Card hover={false} className="xl:col-span-3">
          <div className="flex items-center gap-2 mb-4">
            <ClipboardList className="w-4 h-4 text-equine-lilac" />
            <h2 className="font-display text-2xl text-equine-ink">Open task context</h2>
          </div>
          <div className="space-y-3">
            {openTasks.length === 0 ? (
              <SoftEmpty text="No open staff tasks to hand off." />
            ) : openTasks.map((record) => {
              const data = record.data || {};
              return (
                <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <div className="font-display text-xl text-equine-ink truncate">{data.title}</div>
                      <div className="text-[12px] text-equine-inkMuted">{data.assigned_to || "Unassigned"} - {data.due_at || "No due time"}</div>
                    </div>
                    <StatusPill tone={data.status === "blocked" ? "critical" : "warning"}>{labelFor(data.status || "open")}</StatusPill>
                  </div>
                  {data.handoff_notes && <div className="text-[13px] text-equine-inkMuted mt-2">{data.handoff_notes}</div>}
                </div>
              );
            })}
          </div>
        </Card>

        <Card hover={false} className="xl:col-span-2">
          <div className="flex items-center gap-2 mb-4">
            <FileText className="w-4 h-4 text-equine-lilac" />
            <h2 className="font-display text-2xl text-equine-ink">Recent shift notes</h2>
          </div>
          <div className="space-y-3">
            {shiftNotes.length === 0 ? (
              <SoftEmpty text="No shift notes captured yet." />
            ) : shiftNotes.map((record) => {
              const data = record.data || {};
              return (
                <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
                  <div className="font-display text-xl text-equine-ink">{data.staff_name}</div>
                  <div className="text-[12px] text-equine-inkMuted">{data.area || "Area TBD"} - {data.shift_start || "No start time"}</div>
                  <div className="text-[13px] text-equine-inkMuted mt-2">{data.notes}</div>
                </div>
              );
            })}
          </div>
        </Card>
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading handoff reports...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Handoff reports unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : reports.length === 0 ? (
        <Empty>
          <FileText strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No handoff reports</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add the first end-of-shift handoff report.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="handoff-reports-empty-add">
            <Plus className="w-4 h-4" /> Add first report
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
          {sorted.map((record) => {
            const data = record.data || {};
            const status = data.status || "draft";
            const priority = data.priority || "normal";
            return (
              <Card key={record.id} hover={false} className={savingId === record.id ? "opacity-60" : ""} data-testid={`handoff-report-card-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.area || "Barn"} handoff</div>
                    <div className="text-[12.5px] text-equine-inkMuted">
                      {fmtDate(data.shift_date)} - {data.outgoing_staff || "Outgoing TBD"} to {data.incoming_staff || "Incoming TBD"}
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    <StatusPill tone={STATUS_TONE[status]}>{labelFor(status)}</StatusPill>
                    <StatusPill tone={PRIORITY_TONE[priority]}>{labelFor(priority)}</StatusPill>
                  </div>
                </div>
                <div className="text-[13.5px] text-equine-inkMuted leading-relaxed">{data.summary}</div>
                {data.open_items && (
                  <div className="mt-3 rounded-lg border border-equine-cloud bg-white/60 p-3">
                    <div className="label-eyebrow-muted mb-1">Open items</div>
                    <div className="text-[13px] text-equine-inkMuted">{data.open_items}</div>
                  </div>
                )}
                <div className="hairline mt-4 pt-3 flex flex-wrap items-center gap-2">
                  {status === "draft" && (
                    <button type="button" onClick={() => updateStatus(record, "submitted")} className="btn-secondary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                      <Send className="w-3.5 h-3.5" /> Submit
                    </button>
                  )}
                  {status !== "reviewed" && (
                    <button type="button" onClick={() => updateStatus(record, "reviewed")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Review
                    </button>
                  )}
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
        title="Add handoff report"
        eyebrow="Staff"
        fields={addFields}
        endpoint="/feature-modules/handoff-reports/records"
        initialValues={{ shift_date: today(), priority: "normal", status: "draft" }}
        transform={(form) => ({
          data: {
            ...form,
            outgoing_staff: staffNameById(staff, form.outgoing_staff_user_id),
            incoming_staff: staffNameById(staff, form.incoming_staff_user_id),
          },
        })}
        submitLabel="Save report"
        testidPrefix="handoff-reports-add"
        onCreated={load}
      />
    </div>
  );
}

const Metric = ({ label, value, tone }) => (
  <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
    <div className="label-eyebrow-muted mb-2 capitalize">{label}</div>
    <div className="flex items-end justify-between gap-3">
      <div className="font-display text-4xl text-equine-ink leading-none">{value}</div>
      <StatusPill tone={tone}>{label}</StatusPill>
    </div>
  </div>
);

const SoftEmpty = ({ text }) => (
  <div className="rounded-xl border border-dashed border-equine-cloud bg-white/45 py-8 text-center text-[13px] text-equine-inkMuted">
    {text}
  </div>
);
