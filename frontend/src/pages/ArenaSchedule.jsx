import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CalendarDays, CheckCircle2, Copy, Plus, RefreshCw, Share2 } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { ADMIN_ROLES } from "../lib/permissions";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["open", "requested", "reserved", "lesson", "maintenance", "private"];
const STATUS_TONE = {
  open: "success",
  requested: "warning",
  reserved: "info",
  lesson: "lilac",
  maintenance: "critical",
  private: "neutral",
};

const DURATION_LABEL = {
  "": "Flexible",
  "30_min": "30 min",
  "1_hour": "1 hour",
  half_day: "Half day",
  full_day: "Full day",
};

const ADD_FIELDS = [
  { key: "arena_name", label: "Arena", required: true, placeholder: "Arena name" },
  { key: "title", label: "Title", required: true, placeholder: "Open ride, lesson block, rental", full: true },
  { key: "date", label: "Date", type: "date", required: true },
  { key: "start_time", label: "Start", placeholder: "HH:MM" },
  { key: "end_time", label: "End", placeholder: "HH:MM" },
  { key: "rental_duration", label: "Duration", kind: "select", opts: ["30_min", "1_hour", "half_day", "full_day"] },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "visibility", label: "Visibility", kind: "select", opts: ["shared_with_owners", "staff_only"] },
  { key: "horse_name", label: "Horse", placeholder: "Horse name" },
  { key: "owner_name", label: "Owner", placeholder: "Owner name" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const labelFor = (value) => String(value || "").replace(/_/g, " ");
const timeKey = (row) => `${row.date || "9999"} ${row.start_time || "99:99"} ${row.arena_name || ""}`;

export default function ArenaSchedule() {
  const { user } = useAuth();
  const canManage = ADMIN_ROLES.includes(user?.role);
  const canPublish = ADMIN_ROLES.includes(user?.role);
  const [board, setBoard] = useState(null);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);
  const [sharing, setSharing] = useState(false);
  const [note, setNote] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [shareRes, moduleRes] = await Promise.all([
        api.get("/arena-schedule-share"),
        canManage
          ? api.get("/feature-modules/arena-schedule")
          : Promise.resolve({ data: { records: [] } }),
      ]);
      setBoard(shareRes.data);
      setNote(shareRes.data?.share?.note || "");
      setRecords(canManage ? (moduleRes.data.records || []) : (shareRes.data.blocks || []).map((row) => ({ id: row.id, data: row })));
    } catch (err) {
      setError(err?.response?.data?.detail || "Arena schedule is not available.");
    } finally {
      setLoading(false);
    }
  }, [canManage]);

  useEffect(() => { load(); }, [load]);

  const rows = useMemo(() => {
    const source = canManage ? records.map((record) => ({ id: record.id, ...(record.data || {}) })) : (board?.blocks || []);
    return [...source].sort((a, b) => timeKey(a).localeCompare(timeKey(b)));
  }, [board, canManage, records]);

  const stats = useMemo(() => ({
    blocks: rows.length,
    open: rows.filter((row) => row.status === "open").length,
    reserved: rows.filter((row) => row.status === "reserved").length,
    maintenance: rows.filter((row) => row.status === "maintenance").length,
  }), [rows]);

  const publish = async (enabled) => {
    setSharing(true);
    try {
      await api.post("/arena-schedule-share", {
        enabled,
        title: board?.share?.title || "Arena Schedule",
        note,
      });
      toast.success(enabled ? "Arena schedule shared" : "Arena schedule sharing paused");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update sharing");
    } finally {
      setSharing(false);
    }
  };

  const copyLink = async () => {
    const path = board?.share?.share_path || "/arena-schedule";
    try {
      await navigator.clipboard.writeText(`${window.location.origin}${path}`);
      toast.success("Arena schedule link copied");
    } catch {
      toast.error("Could not copy link");
    }
  };

  const setStatus = async (row, status) => {
    if (!canManage) return;
    setSavingId(row.id);
    try {
      await api.patch(`/feature-modules/arena-schedule/records/${row.id}`, { data: { status } });
      toast.success("Arena block updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update arena block");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (row) => {
    try {
      await api.delete(`/feature-modules/arena-schedule/records/${row.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive arena block");
    }
  };

  return (
    <div data-testid="arena-schedule-page">
      <PageHeader
        eyebrow="Operations"
        title={board?.share?.title || "Arena Schedule"}
        subtitle="Share arena availability and reservations with staff, trainers, and horse owners."
        action={
          <div className="flex items-center gap-3">
            <button onClick={copyLink} className="btn-secondary inline-flex items-center gap-2" data-testid="arena-copy">
              <Copy className="w-4 h-4" /> Copy link
            </button>
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="arena-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            {canManage && (
              <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="arena-add">
                <Plus className="w-4 h-4" /> Add block
              </button>
            )}
          </div>
        }
      />

      {canPublish && (
        <Card hover={false} className="mb-6 border-equine-lilac/30 bg-equine-lilac/5" data-testid="arena-share-controls">
          <div className="flex flex-col xl:flex-row xl:items-end gap-4">
            <div className="flex-1">
              <div className="label-eyebrow-muted mb-1.5">Owner note</div>
              <textarea
                value={note}
                onChange={(event) => setNote(event.target.value)}
                rows={2}
                placeholder="Note: Arena use is approved after barn confirmation."
                className="w-full bg-white border border-equine-cloud rounded-lg px-3 py-2.5 text-[13px] text-equine-ink outline-none focus:border-equine-lilac"
                data-testid="arena-share-note"
              />
            </div>
            <div className="flex items-center gap-2">
              <button type="button" onClick={() => publish(true)} disabled={sharing} className="btn-primary inline-flex items-center gap-2 disabled:opacity-60" data-testid="arena-publish">
                <Share2 className="w-4 h-4" /> Publish
              </button>
              <button type="button" onClick={() => publish(false)} disabled={sharing} className="btn-secondary disabled:opacity-60" data-testid="arena-pause">
                Pause sharing
              </button>
            </div>
          </div>
        </Card>
      )}

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading arena schedule...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Arena schedule unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : (
        <>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <Metric label="Sharing" value={board?.share?.enabled ? "Live" : "Paused"} tone={board?.share?.enabled ? "success" : "warning"} />
            <Metric label="Blocks" value={stats.blocks} />
            <Metric label="Open" value={stats.open} />
            <Metric label="Reserved" value={stats.reserved} />
          </div>

          {board?.share?.note && (
            <Card hover={false} className="mb-6">
              <div className="label-eyebrow-muted mb-2">Barn note</div>
              <div className="text-[14px] text-equine-inkMuted leading-relaxed">{board.share.note}</div>
            </Card>
          )}

          {rows.length === 0 ? (
            <Empty>
              <CalendarDays strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
              <div className="font-display text-2xl text-equine-ivory mb-1">No arena blocks shared</div>
              <div className="text-[13px] text-equine-platinum/60 mb-4">
                {canManage ? "Add an availability, lesson, rental, or maintenance block." : "The barn has not published arena availability yet."}
              </div>
              {canManage && (
                <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="arena-empty-add">
                  <Plus className="w-4 h-4" /> Add first block
                </button>
              )}
            </Empty>
          ) : (
            <Card hover={false} data-testid="arena-list">
              <div className="space-y-3">
                {rows.map((row) => {
                  const status = row.status || "open";
                  return (
                    <div key={row.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === row.id ? "opacity-60" : ""}`} data-testid={`arena-row-${row.id}`}>
                      <div className="flex flex-col xl:flex-row xl:items-center gap-4">
                        <div className="w-full xl:w-40 flex-shrink-0">
                          <div className="label-eyebrow-muted mb-1">{row.date || "Date TBD"}</div>
                          <div className="font-display text-2xl text-equine-ink leading-none">{row.start_time || "—"}</div>
                          <div className="text-[12px] text-equine-inkMuted mt-1">to {row.end_time || "—"}</div>
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 flex-wrap mb-1">
                            <div className="font-display text-2xl text-equine-ink truncate">{row.title || "Arena block"}</div>
                            <StatusPill tone={STATUS_TONE[status] || "info"}>{labelFor(status)}</StatusPill>
                          </div>
                          <div className="text-[13px] text-equine-inkMuted">
                            {row.arena_name || "Arena"} · {DURATION_LABEL[row.rental_duration || ""] || labelFor(row.rental_duration)}
                            {row.owner_name ? ` · ${row.owner_name}` : ""}
                            {row.horse_name ? ` · ${row.horse_name}` : ""}
                          </div>
                          {row.notes && <div className="text-[13px] text-equine-ink mt-1">{row.notes}</div>}
                        </div>
                        {canManage && (
                          <div className="flex flex-wrap items-center gap-2 xl:justify-end">
                            <button type="button" onClick={() => setStatus(row, "open")} className="btn-secondary text-[12px] py-2 px-4" disabled={status === "open"}>Open</button>
                            <button type="button" onClick={() => setStatus(row, "reserved")} className="btn-secondary text-[12px] py-2 px-4" disabled={status === "reserved"}>Reserve</button>
                            <button type="button" onClick={() => setStatus(row, "maintenance")} className="btn-secondary text-[12px] py-2 px-4" disabled={status === "maintenance"}>Maintenance</button>
                            <button type="button" onClick={() => setStatus(row, "lesson")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1" disabled={status === "lesson"}>
                              <CheckCircle2 className="w-3.5 h-3.5" /> Lesson
                            </button>
                            <button type="button" onClick={() => archiveRecord(row)} className="text-[12px] text-equine-clay hover:text-equine-ink px-2">Archive</button>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          )}
        </>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add arena block"
        eyebrow="Operations"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/arena-schedule/records"
        initialValues={{ status: "open", visibility: "shared_with_owners" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save block"
        testidPrefix="arena-add"
        onCreated={load}
      />
    </div>
  );
}

const Metric = ({ label, value, tone }) => (
  <Card hover={false} className="p-4">
    <div className="label-eyebrow-muted mb-2">{label}</div>
    <div className="flex items-end justify-between gap-3">
      <div className="font-display text-3xl text-equine-ink leading-none">{value}</div>
      {tone && <StatusPill tone={tone}>{String(value).toLowerCase()}</StatusPill>}
    </div>
  </Card>
);
