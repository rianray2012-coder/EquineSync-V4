import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Plus, Dumbbell, RotateCcw, XCircle } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, PageHeader, StatusPill, Empty } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";
import SoftWarning from "../components/SoftWarning";
import { normalizeStaffDirectory, staffOptions } from "../lib/staffDirectory";

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

export default function Training() {
  const [sessions, setSessions] = useState([]);
  const [horses, setHorses] = useState([]);
  const [staff, setStaff] = useState([]);
  const [addOpen, setAddOpen] = useState(false);
  const [action, setAction] = useState(null);

  const load = useCallback(() => api.get("/training").then((r) => setSessions(r.data)), []);
  useEffect(() => {
    load().catch((err) => toast.error(err?.response?.data?.detail || "Could not load training sessions"));
    api.get("/horses")
      .then((r) => setHorses(r.data))
      .catch(() => setHorses([]));
    api.get("/staff-portal/staff-directory")
      .then((r) => setStaff(normalizeStaffDirectory(r.data)))
      .catch(() => setStaff([]));
  }, [load]);

  const fields = useMemo(() => [
    {
      key: "horse_id", label: "Horse", kind: "select", required: true, full: true,
      opts: horses.length === 0
        ? [{ v: "__none__", l: "— No horses yet —" }]
        : horses.map((h) => ({ v: h.id, l: h.name })),
    },
    { key: "date", label: "Date", type: "date", required: true },
    { key: "discipline", label: "Discipline", placeholder: "Discipline" },
    { key: "exercises", label: "Exercises", full: true, kind: "textarea", rows: 3,
      placeholder: "Training notes" },
    { key: "notes", label: "Notes", full: true, kind: "textarea", rows: 2 },
    { key: "rating", label: "Rating (1–10)", type: "number", placeholder: "Rating" },
    { key: "homework", label: "Homework" },
  ], [horses]);

  const horsesEmpty = horses.length === 0;

  const mutateTraining = async (session, type, payload) => {
    try {
      await api.post(`/training/${session.id}/${type}`, payload);
      toast.success(type === "cancel" ? "Training session cancelled" : "Training substitution recorded");
      setAction(null);
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update training session");
    }
  };

  // Soft per-horse-per-day awareness — informational only.
  const renderWarnings = useCallback((form) => {
    if (!form?.horse_id || form.horse_id === "__none__" || !form?.date) return null;
    const clash = sessions.find(
      (s) => s.horse_id === form.horse_id && s.date === form.date,
    );
    if (!clash) return null;
    return (
      <SoftWarning testid="training-add-conflict">
        {`${clash.horse_name || "This horse"} already has training logged for ${fmtDate(form.date)}.`}
      </SoftWarning>
    );
  }, [sessions]);

  return (
    <div data-testid="training-page">
      <PageHeader
        eyebrow="Development"
        title="Training Log"
        subtitle="Daily rides, exercises, ratings, and homework — across every horse in work."
        action={
          <button
            onClick={() => setAddOpen(true)}
            disabled={horsesEmpty}
            data-testid="training-add-btn"
            className="btn-primary inline-flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
            title={horsesEmpty ? "Add a horse first" : ""}
          >
            <Plus className="w-4 h-4" /> Log session
          </button>
        }
      />

      {sessions.length === 0 ? (
        <Empty>
          <Dumbbell strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No training sessions logged</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Log the work — exercises, ratings, homework — to build each horse's development arc.</div>
          {!horsesEmpty && (
            <button onClick={() => setAddOpen(true)} data-testid="training-empty-add" className="btn-primary inline-flex items-center gap-2">
              <Plus className="w-4 h-4" /> Log first session
            </button>
          )}
        </Empty>
      ) : (
        <Card>
          {sessions.map((t) => {
            const inactive = t.cancelled || t.status === "cancelled";
            return (
            <div key={t.id} data-testid={`training-${t.id}`} className="py-4 hairline">
              <div className="flex items-center justify-between mb-1 gap-3">
                <div className="font-display text-xl text-equine-ivory">{t.horse_name || "—"}</div>
                <div className="flex items-center gap-2 shrink-0">
                  {t.discipline && <StatusPill tone="neutral">{t.discipline}</StatusPill>}
                  {inactive && <StatusPill tone="critical">cancelled</StatusPill>}
                  {t.substitution_state === "substituted" && <StatusPill tone="warning">substituted</StatusPill>}
                </div>
              </div>
              <div className="text-[12.5px] text-equine-platinum/60 mb-2">
                {fmtDate(t.date)}{t.trainer_name ? ` · ${t.trainer_name}` : ""}
                {t.rating ? ` · ${t.rating}/10` : ""}
              </div>
              {t.exercises && <div className="text-equine-silver/80 text-[14px]">{t.exercises}</div>}
              {t.notes && <div className="text-[13px] text-equine-platinum/80 mt-1.5">Notes: {t.notes}</div>}
              {t.homework && <div className="text-[12.5px] text-equine-lilac mt-1.5">Homework: {t.homework}</div>}
              {!inactive && (
                <div className="mt-3 flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setAction({ type: "substitute", session: t })}
                    className="btn-secondary text-[12px] !py-2 !px-3 inline-flex items-center gap-1.5"
                    data-testid={`training-substitute-${t.id}`}
                  >
                    <RotateCcw className="w-3.5 h-3.5" /> Substitute
                  </button>
                  <button
                    type="button"
                    onClick={() => setAction({ type: "cancel", session: t })}
                    className="btn-secondary text-[12px] !py-2 !px-3 inline-flex items-center gap-1.5 text-equine-clay"
                    data-testid={`training-cancel-${t.id}`}
                  >
                    <XCircle className="w-3.5 h-3.5" /> Cancel
                  </button>
                </div>
              )}
            </div>
            );
          })}
        </Card>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Log training session"
        eyebrow="Development"
        fields={fields}
        endpoint="/training"
        initialValues={{ date: todayISO() }}
        transform={(form) => ({ ...form, date: form.date || todayISO() })}
        renderWarnings={renderWarnings}
        submitLabel="Save session"
        testidPrefix="training-add"
        onCreated={load}
      />

      {/* Mobile FAB — log the ride before you forget. Hidden if no horses. */}
      {!horsesEmpty && (
        <button
          type="button"
          onClick={() => setAddOpen(true)}
          className="fab lg:hidden"
          data-testid="training-fab"
          aria-label="Log training session"
        >
          <Plus strokeWidth={1.8} className="w-7 h-7" />
        </button>
      )}
      {action && (
        <TrainingActionSheet
          action={action}
          horses={horses}
          staff={staff}
          onClose={() => setAction(null)}
          onSubmit={(payload) => mutateTraining(action.session, action.type, payload)}
        />
      )}
    </div>
  );
}

const TrainingActionSheet = ({ action, horses, staff, onClose, onSubmit }) => {
  const [reason, setReason] = useState("");
  const [substituteTrainerId, setSubstituteTrainerId] = useState("");
  const [substituteHorseId, setSubstituteHorseId] = useState(action.session.horse_id || "");
  const [saving, setSaving] = useState(false);
  const isCancel = action.type === "cancel";
  const canSubmit = reason.trim().length > 0 && !saving;
  const trainerOptions = staffOptions((staff || []).filter((person) => person.role === "trainer"));

  const submit = async (e) => {
    e.preventDefault();
    if (!canSubmit) return;
    setSaving(true);
    await onSubmit(isCancel ? {
      reason: reason.trim(),
      cancelled_at: new Date().toISOString(),
    } : {
      reason: reason.trim(),
      substitute_trainer_id: substituteTrainerId || null,
      substitute_horse_id: substituteHorseId || null,
    });
    setSaving(false);
  };

  return (
    <div className="fixed inset-0 z-[60] flex justify-end" data-testid={`training-${action.type}-sheet`}>
      <div className="absolute inset-0 bg-equine-black/70 backdrop-blur-sm" onClick={onClose} />
      <form onSubmit={submit} className="relative h-full w-full max-w-md bg-equine-card border-l border-equine-hairline shadow-2xl overflow-y-auto px-6 py-6 space-y-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="label-eyebrow mb-1">Training workflow</div>
            <h2 className="font-display text-2xl text-equine-ivory">{isCancel ? "Cancel session" : "Record substitution"}</h2>
          </div>
          <button type="button" onClick={onClose} className="text-equine-platinum/60 hover:text-equine-ivory p-1.5 rounded-md hover:bg-white/[0.05]" aria-label="Close">×</button>
        </div>

        {!isCancel && (
          <div className="grid grid-cols-1 gap-4">
            <label className="block">
              <div className="label-eyebrow mb-1.5">Substitute trainer</div>
              <select value={substituteTrainerId} onChange={(e) => setSubstituteTrainerId(e.target.value)} data-testid="training-substitute-trainer-id" className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2.5 text-equine-ivory focus:border-equine-lilac outline-none text-[14px] min-h-[44px]">
                <option value="">No trainer change</option>
                {trainerOptions.map((trainer) => <option key={trainer.v} value={trainer.v}>{trainer.l}</option>)}
              </select>
            </label>
            <label className="block">
              <div className="label-eyebrow mb-1.5">Substitute horse</div>
              <select value={substituteHorseId || ""} onChange={(e) => setSubstituteHorseId(e.target.value)} data-testid="training-substitute-horse-id" className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2.5 text-equine-ivory focus:border-equine-lilac outline-none text-[14px] min-h-[44px]">
                <option value="">No horse change</option>
                {horses.map((h) => <option key={h.id} value={h.id}>{h.name}</option>)}
              </select>
            </label>
          </div>
        )}

        <label className="block">
          <div className="label-eyebrow mb-1.5">Reason</div>
          <textarea rows={4} value={reason} onChange={(e) => setReason(e.target.value)} data-testid={`training-${action.type}-reason`} className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2.5 text-equine-ivory focus:border-equine-lilac outline-none text-[14px] transition-colors resize-y" />
        </label>
        <div className="sticky bottom-0 -mx-6 px-6 pt-3 pb-1 mt-4 bg-equine-card/95 backdrop-blur-md border-t border-equine-hairline flex items-center justify-end gap-2">
          <button type="button" onClick={onClose} className="btn-secondary tap-44" data-testid={`training-${action.type}-close`}>Close</button>
          <button type="submit" disabled={!canSubmit} className="btn-primary tap-44" data-testid={`training-${action.type}-submit`}>
            {saving ? "Saving..." : isCancel ? "Cancel session" : "Save substitution"}
          </button>
        </div>
      </form>
    </div>
  );
};
