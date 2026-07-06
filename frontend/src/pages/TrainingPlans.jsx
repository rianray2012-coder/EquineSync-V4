import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, ClipboardList, PauseCircle, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import { api, fmtDate } from "../lib/api";
import { normalizeStaffDirectory, staffNameById, staffOptions } from "../lib/staffDirectory";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["planned", "active", "achieved", "paused"];
const STATUS_TONE = { planned: "info", active: "warning", achieved: "success", paused: "neutral" };
const TRAINING_PLAN_WRITE_ROLES = ["admin", "barn_manager", "trainer"];

export default function TrainingPlans() {
  const { user } = useAuth();
  const [records, setRecords] = useState([]);
  const [horses, setHorses] = useState([]);
  const [trainers, setTrainers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);
  const canWriteTrainingPlan = TRAINING_PLAN_WRITE_ROLES.includes(user?.role);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [planRes, horseRes] = await Promise.all([
        api.get("/feature-modules/training-plans"),
        api.get("/horses"),
      ]);
      setRecords(planRes.data.records || []);
      setHorses(Array.isArray(horseRes.data) ? horseRes.data : []);
      if (canWriteTrainingPlan) {
        const trainerRes = await api.get("/trainer/directory");
        setTrainers(normalizeStaffDirectory(trainerRes.data));
      } else {
        setTrainers([]);
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load training plans.");
    } finally {
      setLoading(false);
    }
  }, [canWriteTrainingPlan]);

  useEffect(() => { load(); }, [load]);

  const addFields = useMemo(() => [
    {
      key: "horse_id", label: "Horse", required: true, kind: "select",
      opts: horses.map((horse) => ({ v: horse.id, l: horse.name || horse.id })),
    },
    { key: "trainer_user_id", label: "Trainer", required: true, kind: "select", opts: staffOptions(trainers) },
    { key: "goal", label: "Goal", required: true, placeholder: "Consistent changes", full: true },
    { key: "target_date", label: "Target date", type: "date" },
    { key: "status", label: "Status", kind: "select", opts: STATUSES },
    { key: "plan_notes", label: "Plan", kind: "textarea", rows: 4, full: true },
  ], [horses, trainers]);

  const grouped = useMemo(() => {
    const out = Object.fromEntries(STATUSES.map((status) => [status, []]));
    records.forEach((record) => {
      const status = (record.data || {}).status || "planned";
      (out[status] || out.planned).push(record);
    });
    Object.values(out).forEach((rows) => rows.sort((a, b) => String((a.data || {}).target_date || "9999").localeCompare(String((b.data || {}).target_date || "9999"))));
    return out;
  }, [records]);

  const setStatus = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/training-plans/records/${record.id}`, { data: { status } });
      toast.success("Training plan updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update plan");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/training-plans/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive plan");
    }
  };

  return (
    <div data-testid="training-plans-page">
      <PageHeader
        eyebrow="Training"
        title="Training Plans & Goals"
        subtitle="Track each horse's plan, goal, trainer assignment, target date, and progress status alongside the daily ride log."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="training-plans-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            {canWriteTrainingPlan && (
              <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="training-plans-add">
                <Plus className="w-4 h-4" /> Add plan
              </button>
            )}
          </div>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading training plans…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Training plans unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <ClipboardList strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No training plans</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Create a plan and attach it to a horse, trainer, and target date.</div>
          {canWriteTrainingPlan && (
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="training-plans-empty-add">
              <Plus className="w-4 h-4" /> Add first plan
            </button>
          )}
        </Empty>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-4">
          {STATUSES.map((status) => (
            <Card key={status} hover={false} className="p-4" data-testid={`training-plans-${status}`}>
              <div className="flex items-center justify-between mb-3">
                <div className="label-eyebrow capitalize">{status}</div>
                <StatusPill tone={STATUS_TONE[status]}>{grouped[status].length}</StatusPill>
              </div>
              <div className="space-y-3">
                {grouped[status].map((record) => {
                  const data = record.data || {};
                  return (
                    <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`training-plan-card-${record.id}`}>
                      <div className="font-display text-xl leading-none text-equine-ink">{data.horse_name}</div>
                      <div className="text-[13px] text-equine-ink mt-2">{data.goal}</div>
                      <div className="text-[12px] text-equine-inkMuted mt-2">
                        {data.trainer_name || "Trainer TBD"} · Target {fmtDate(data.target_date)}
                      </div>
                      {data.plan_notes && <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{data.plan_notes}</div>}
                      {canWriteTrainingPlan && (
                        <div className="hairline mt-3 pt-3 flex flex-wrap items-center gap-2">
                          {status !== "achieved" && (
                            <button type="button" onClick={() => setStatus(record, "achieved")} className="text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1">
                              <CheckCircle2 className="w-3.5 h-3.5" /> Achieved
                            </button>
                          )}
                          {status !== "paused" && (
                            <button type="button" onClick={() => setStatus(record, "paused")} className="text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1">
                              <PauseCircle className="w-3.5 h-3.5" /> Pause
                            </button>
                          )}
                          {status !== "active" && (
                            <button type="button" onClick={() => setStatus(record, "active")} className="text-[12px] text-equine-navy hover:text-equine-saddle">
                              Activate
                            </button>
                          )}
                          <button type="button" onClick={() => archiveRecord(record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">
                            Archive
                          </button>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </Card>
          ))}
        </div>
      )}

      {canWriteTrainingPlan && (
        <QuickAddSheet
          open={addOpen}
          onClose={() => setAddOpen(false)}
          title="Add training plan"
          eyebrow="Training"
          fields={addFields}
          endpoint="/feature-modules/training-plans/records"
          initialValues={{ status: "planned" }}
          transform={(form) => {
            const horse = horses.find((row) => row.id === form.horse_id);
            return {
              data: {
                ...form,
                horse_name: horse?.name || "",
                trainer_name: staffNameById(trainers, form.trainer_user_id),
              },
            };
          }}
          submitLabel="Save plan"
          testidPrefix="training-plans-add"
          onCreated={load}
        />
      )}
    </div>
  );
}
