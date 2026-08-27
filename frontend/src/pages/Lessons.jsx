import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Plus, GraduationCap, RotateCcw, XCircle } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate, fmtTime } from "../lib/api";
import { Card, PageHeader, StatusPill, Empty } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";
import SoftWarning from "../components/SoftWarning";
import { normalizeStaffDirectory, staffOptions } from "../lib/staffDirectory";

const CONFLICT_WINDOW_MIN = 60;

function defaultStart() {
  // Next round half-hour
  const d = new Date();
  d.setMinutes(d.getMinutes() + 60);
  d.setSeconds(0, 0);
  d.setMinutes(d.getMinutes() < 30 ? 0 : 30);
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export default function Lessons() {
  const [lessons, setLessons] = useState([]);
  const [riders, setRiders] = useState([]);
  const [horses, setHorses] = useState([]);
  const [staff, setStaff] = useState([]);
  const [addOpen, setAddOpen] = useState(false);
  const [action, setAction] = useState(null);

  const load = useCallback(() => api.get("/lessons").then((r) => setLessons(r.data)), []);
  useEffect(() => {
    load().catch((err) => toast.error(err?.response?.data?.detail || "Could not load lessons"));
    api.get("/riders")
      .then((r) => setRiders(r.data))
      .catch(() => setRiders([]));
    api.get("/horses")
      .then((r) => setHorses(r.data))
      .catch(() => setHorses([]));
    api.get("/staff-portal/staff-directory")
      .then((r) => setStaff(normalizeStaffDirectory(r.data)))
      .catch(() => setStaff([]));
  }, [load]);

  const fields = useMemo(() => [
    {
      key: "rider_id", label: "Rider", kind: "select", required: true, full: true,
      opts: riders.length === 0
        ? [{ v: "__none__", l: "— No riders yet —" }]
        : riders.map((r) => ({ v: r.id, l: r.full_name })),
    },
    {
      key: "horse_id", label: "Horse", kind: "select", full: true,
      opts: [{ v: "__none__", l: "— TBD —" }, ...horses.map((h) => ({ v: h.id, l: h.name }))],
    },
    { key: "start_time", label: "Start time", type: "datetime-local", required: true },
    { key: "duration_min", label: "Duration (min)", type: "number", placeholder: "Minutes" },
    { key: "focus", label: "Focus", full: true, placeholder: "Lesson focus" },
  ], [riders, horses]);

  const transform = (form) => ({
    ...form,
    start_time: form.start_time ? new Date(form.start_time).toISOString() : new Date().toISOString(),
    duration_min: form.duration_min ? Number(form.duration_min) : 60,
    horse_id: form.horse_id && form.horse_id !== "__none__" ? form.horse_id : null,
  });

  // Soft scheduling-conflict awareness — never blocks, never alarms.
  // Looks for any existing lesson within ±60 min of the proposed start
  // time involving the same rider OR the same horse. Calm copy per
  // founder direction ("supportive, not corrective").
  const renderWarnings = useCallback((form) => {
    if (!form?.start_time) return null;
    const start = new Date(form.start_time).getTime();
    if (Number.isNaN(start)) return null;
    const windowMs = CONFLICT_WINDOW_MIN * 60 * 1000;
    const notes = [];

    if (form.rider_id && form.rider_id !== "__none__") {
      const clash = lessons.find((l) => {
        if (l.rider_id !== form.rider_id || !l.start_time) return false;
        const t = new Date(l.start_time).getTime();
        return Math.abs(t - start) <= windowMs;
      });
      if (clash) {
        notes.push({
          key: "rider",
          msg: `${clash.rider_name || "This rider"} already has a lesson scheduled nearby in time (${fmtDate(clash.start_time)} ${fmtTime(clash.start_time)}).`,
        });
      }
    }

    if (form.horse_id && form.horse_id !== "__none__") {
      const clash = lessons.find((l) => {
        if (l.horse_id !== form.horse_id || !l.start_time) return false;
        const t = new Date(l.start_time).getTime();
        return Math.abs(t - start) <= windowMs;
      });
      if (clash) {
        notes.push({
          key: "horse",
          msg: `${clash.horse_name || "This horse"} already has a lesson scheduled nearby in time (${fmtDate(clash.start_time)} ${fmtTime(clash.start_time)}).`,
        });
      }
    }

    if (!notes.length) return null;
    return (
      <div className="space-y-2">
        {notes.map((n) => (
          <SoftWarning key={n.key} testid={`lessons-add-conflict-${n.key}`}>
            {n.msg}
          </SoftWarning>
        ))}
      </div>
    );
  }, [lessons]);

  const ridersEmpty = riders.length === 0;

  const mutateLesson = async (lesson, type, payload) => {
    try {
      await api.post(`/lessons/${lesson.id}/${type}`, payload);
      toast.success(type === "cancel" ? "Lesson cancelled" : "Lesson substitution recorded");
      setAction(null);
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update lesson");
    }
  };

  return (
    <div data-testid="lessons-page">
      <PageHeader
        eyebrow="Program"
        title="Lesson Program"
        subtitle="Schedule, rider development, and lesson horse workload monitoring."
        action={
          <button
            onClick={() => setAddOpen(true)}
            disabled={ridersEmpty}
            data-testid="lessons-add-btn"
            className="btn-primary inline-flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
            title={ridersEmpty ? "Add a rider first" : ""}
          >
            <Plus className="w-4 h-4" /> Schedule lesson
          </button>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <h2 className="font-display text-2xl mb-4">Upcoming Lessons</h2>
          {lessons.length === 0 ? (
            <Empty>
              <GraduationCap strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
              <div className="font-display text-2xl text-equine-ivory mb-1">No lessons scheduled</div>
              <div className="text-[13px] text-equine-platinum/60 mb-4">
                {ridersEmpty
                  ? "Add a rider first, then come back to schedule their first lesson."
                  : "Schedule a lesson to get the trainer's day moving."}
              </div>
              {!ridersEmpty && (
                <button onClick={() => setAddOpen(true)} data-testid="lessons-empty-add" className="btn-primary inline-flex items-center gap-2">
                  <Plus className="w-4 h-4" /> Schedule first lesson
                </button>
              )}
            </Empty>
          ) : (
            lessons.map((l) => {
              const inactive = l.cancelled || l.status === "cancelled";
              return (
              <div key={l.id} data-testid={`lesson-${l.id}`} className="py-3 hairline flex items-center gap-4">
                <div className="font-display text-xl text-equine-champagne w-28 shrink-0">{fmtDate(l.start_time)} · {fmtTime(l.start_time)}</div>
                <div className="flex-1 min-w-0">
                  <div className="text-equine-ivory truncate">
                    {l.rider_name || "—"}{l.horse_name ? ` on ${l.horse_name}` : ""}
                  </div>
                  <div className="text-[12.5px] text-equine-platinum/60 truncate">
                    {[l.focus, l.duration_min ? `${l.duration_min} min` : null, l.trainer_name, l.substitution_state === "substituted" ? "substituted" : null]
                      .filter(Boolean).join(" · ")}
                  </div>
                </div>
                <StatusPill tone={inactive ? "critical" : l.completed ? "success" : "info"}>{inactive ? "cancelled" : l.completed ? "done" : "scheduled"}</StatusPill>
                {!inactive && (
                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      type="button"
                      onClick={() => setAction({ type: "substitute", lesson: l })}
                      className="btn-secondary text-[12px] !py-2 !px-3 inline-flex items-center gap-1.5"
                      data-testid={`lesson-substitute-${l.id}`}
                    >
                      <RotateCcw className="w-3.5 h-3.5" /> Substitute
                    </button>
                    <button
                      type="button"
                      onClick={() => setAction({ type: "cancel", lesson: l })}
                      className="btn-secondary text-[12px] !py-2 !px-3 inline-flex items-center gap-1.5 text-equine-clay"
                      data-testid={`lesson-cancel-${l.id}`}
                    >
                      <XCircle className="w-3.5 h-3.5" /> Cancel
                    </button>
                  </div>
                )}
              </div>
              );
            })
          )}
        </Card>

        <Card>
          <h2 className="font-display text-2xl mb-4">Riders</h2>
          {riders.length === 0 ? (
            <div className="text-[13px] text-equine-platinum/60 py-2">No riders yet.</div>
          ) : riders.map((r) => (
            <div key={r.id} className="py-3 hairline">
              <div className="text-equine-ivory">{r.full_name}</div>
              <div className="text-[12.5px] text-equine-platinum/60 mt-0.5">{r.skill_level}{r.goals ? ` · ${r.goals}` : ""}</div>
            </div>
          ))}
        </Card>
      </div>

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Schedule lesson"
        eyebrow="Program"
        fields={fields}
        endpoint="/lessons"
        initialValues={{ start_time: defaultStart(), duration_min: 60 }}
        transform={transform}
        renderWarnings={renderWarnings}
        submitLabel="Schedule"
        testidPrefix="lessons-add"
        onCreated={load}
      />

      {/* Mobile FAB — quick aisle-side scheduling. Hidden when no riders. */}
      {!ridersEmpty && (
        <button
          type="button"
          onClick={() => setAddOpen(true)}
          className="fab lg:hidden"
          data-testid="lessons-fab"
          aria-label="Schedule lesson"
        >
          <Plus strokeWidth={1.8} className="w-7 h-7" />
        </button>
      )}
      {action && (
        <LessonActionSheet
          action={action}
          riders={riders}
          horses={horses}
          staff={staff}
          onClose={() => setAction(null)}
          onSubmit={(payload) => mutateLesson(action.lesson, action.type, payload)}
        />
      )}
    </div>
  );
}

// Keep helper for future use (default start time).
export { defaultStart };

const LessonActionSheet = ({ action, riders, horses, staff, onClose, onSubmit }) => {
  const [reason, setReason] = useState("");
  const [substituteTrainerId, setSubstituteTrainerId] = useState("");
  const [substituteRiderId, setSubstituteRiderId] = useState(action.lesson.rider_id || "");
  const [substituteHorseId, setSubstituteHorseId] = useState(action.lesson.horse_id || "");
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
      substitute_rider_id: substituteRiderId || null,
      substitute_horse_id: substituteHorseId || null,
    });
    setSaving(false);
  };

  return (
    <div className="fixed inset-0 z-[60] flex justify-end" data-testid={`lesson-${action.type}-sheet`}>
      <div className="absolute inset-0 bg-equine-black/70 backdrop-blur-sm" onClick={onClose} />
      <form onSubmit={submit} className="relative h-full w-full max-w-md bg-equine-card border-l border-equine-hairline shadow-2xl overflow-y-auto px-6 py-6 space-y-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="label-eyebrow mb-1">Lesson workflow</div>
            <h2 className="font-display text-2xl text-equine-ivory">{isCancel ? "Cancel lesson" : "Record substitution"}</h2>
          </div>
          <button type="button" onClick={onClose} className="text-equine-platinum/60 hover:text-equine-ivory p-1.5 rounded-md hover:bg-white/[0.05]" aria-label="Close">×</button>
        </div>

        {!isCancel && (
          <div className="grid grid-cols-1 gap-4">
            <label className="block">
              <div className="label-eyebrow mb-1.5">Substitute trainer</div>
              <select value={substituteTrainerId} onChange={(e) => setSubstituteTrainerId(e.target.value)} data-testid="lesson-substitute-trainer-id" className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2.5 text-equine-ivory focus:border-equine-champagne outline-none text-[14px] min-h-[44px]">
                <option value="">No trainer change</option>
                {trainerOptions.map((trainer) => <option key={trainer.v} value={trainer.v}>{trainer.l}</option>)}
              </select>
            </label>
            <label className="block">
              <div className="label-eyebrow mb-1.5">Substitute rider</div>
              <select value={substituteRiderId} onChange={(e) => setSubstituteRiderId(e.target.value)} data-testid="lesson-substitute-rider-id" className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2.5 text-equine-ivory focus:border-equine-champagne outline-none text-[14px] min-h-[44px]">
                <option value="">No rider change</option>
                {riders.map((r) => <option key={r.id} value={r.id}>{r.full_name}</option>)}
              </select>
            </label>
            <label className="block">
              <div className="label-eyebrow mb-1.5">Substitute horse</div>
              <select value={substituteHorseId || ""} onChange={(e) => setSubstituteHorseId(e.target.value)} data-testid="lesson-substitute-horse-id" className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2.5 text-equine-ivory focus:border-equine-champagne outline-none text-[14px] min-h-[44px]">
                <option value="">No horse change</option>
                {horses.map((h) => <option key={h.id} value={h.id}>{h.name}</option>)}
              </select>
            </label>
          </div>
        )}

        <label className="block">
          <div className="label-eyebrow mb-1.5">Reason</div>
          <textarea rows={4} value={reason} onChange={(e) => setReason(e.target.value)} data-testid={`lesson-${action.type}-reason`} className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2.5 text-equine-ivory focus:border-equine-champagne outline-none text-[14px] transition-colors resize-y" />
        </label>
        <div className="sticky bottom-0 -mx-6 px-6 pt-3 pb-1 mt-4 bg-equine-card/95 backdrop-blur-md border-t border-equine-hairline flex items-center justify-end gap-2">
          <button type="button" onClick={onClose} className="btn-secondary tap-44" data-testid={`lesson-${action.type}-close`}>Close</button>
          <button type="submit" disabled={!canSubmit} className="btn-primary tap-44" data-testid={`lesson-${action.type}-submit`}>
            {saving ? "Saving..." : isCancel ? "Cancel lesson" : "Save substitution"}
          </button>
        </div>
      </form>
    </div>
  );
};
