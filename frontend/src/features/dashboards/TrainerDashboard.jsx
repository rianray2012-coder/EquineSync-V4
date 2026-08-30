import React, { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AlertTriangle, CalendarDays, CircleDot, ClipboardList, Dumbbell, GraduationCap, RefreshCw, Users } from "lucide-react";
import { api, fmtDate, fmtTime } from "../../lib/api";
import { Card, PageHeader, SectionEyebrow, Stat, StatusPill } from "../../components/Primitives";
import LastSyncedBadge from "../../components/today/LastSyncedBadge";

const labelFor = (value) => String(value || "").replace(/_/g, " ");

export default function TrainerDashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [lastSyncedAt, setLastSyncedAt] = useState(null);

  const load = useCallback(async () => {
    setRefreshing(true);
    setError(null);
    try {
      const response = await api.get("/trainer/operating-center");
      setData(response.data);
      setLastSyncedAt(new Date());
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load trainer operating center.");
    } finally {
      setRefreshing(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  if (error) {
    return (
      <div data-testid="dashboard-trainer">
        <PageHeader
          eyebrow="Trainer"
          title="Trainer Operating Center"
          subtitle="Assigned horses, lessons, training work, and active plan context for the trainer account."
          action={<RefreshButton onClick={load} refreshing={refreshing} />}
        />
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Trainer center unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      </div>
    );
  }

  const counts = data?.counts || {};
  const trainerName = data?.trainer?.name || "Trainer";

  return (
    <div data-testid="dashboard-trainer" className="pb-20 lg:pb-8">
      <PageHeader
        eyebrow={`Trainer, ${trainerName}`}
        title="Trainer Operating Center"
        subtitle="Your assigned horses, upcoming lessons, training logs, active plans, and rider context in one working view."
        action={
          <div className="flex items-center gap-2 flex-wrap justify-end">
            <LastSyncedBadge at={lastSyncedAt} onRefresh={load} refreshing={refreshing} verb="Updated" tone="secondary" />
            <RefreshButton onClick={load} refreshing={refreshing} />
          </div>
        }
      />

      {!data ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading trainer work...</div></Card>
      ) : (
        <>
          <div className="grid grid-cols-2 lg:grid-cols-5 gap-5 mb-10">
            <Stat label="Assigned Horses" value={counts.assigned_horses || 0} caption="Ready for lesson and plan context" icon={CircleDot} testid="trainer-stat-horses" />
            <Stat label="Riders" value={counts.riders || 0} caption="From trainer-owned lessons" accent="ice" icon={Users} testid="trainer-stat-riders" />
            <Stat label="Lessons" value={counts.upcoming_lessons || 0} caption="Scheduled and not complete" accent="lilac" icon={GraduationCap} testid="trainer-stat-lessons" />
            <Stat label="Training Logs" value={counts.recent_training || 0} caption="Recent trainer-linked work" accent="sage" icon={Dumbbell} testid="trainer-stat-training" />
            <Stat label="Active Plans" value={counts.active_plans || 0} caption="Planned or active goals" accent="amber" icon={ClipboardList} testid="trainer-stat-plans" />
          </div>

          <SectionEyebrow action={<ActionLinks />}>Trainer Work</SectionEyebrow>
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-10">
            <WorkCard
              title="Upcoming Lessons"
              icon={CalendarDays}
              empty="Lessons assigned to you will appear here with rider, horse, time, and focus notes."
              rows={data.upcoming_lessons || []}
              render={(row) => (
                <div>
                  <div className="text-equine-ink font-display text-xl leading-tight">{row.rider_name || "Rider TBD"}</div>
                  <div className="text-[12.5px] text-equine-inkMuted mt-1">
                    {fmtDate(row.start_time)} {fmtTime(row.start_time)}
                    {row.horse_name ? ` - ${row.horse_name}` : ""}
                  </div>
                  {row.focus && <div className="text-[13px] text-equine-inkMuted mt-2">{row.focus}</div>}
                </div>
              )}
            />

            <WorkCard
              title="Recent Training"
              icon={Dumbbell}
              empty="Training sessions you record or inherit will appear here for quick follow-up."
              rows={data.recent_training || []}
              render={(row) => (
                <div>
                  <div className="text-equine-ink font-display text-xl leading-tight">{row.horse_name || "Horse TBD"}</div>
                  <div className="text-[12.5px] text-equine-inkMuted mt-1">
                    {fmtDate(row.date)}{row.discipline ? ` - ${row.discipline}` : ""}{row.rating ? ` - ${row.rating}/10` : ""}
                  </div>
                  {row.exercises && <div className="text-[13px] text-equine-inkMuted mt-2">{row.exercises}</div>}
                </div>
              )}
            />

            <WorkCard
              title="Active Plans"
              icon={ClipboardList}
              empty="Active horse goals and progression plans will appear here once assigned."
              rows={data.active_plans || []}
              render={(row) => {
                const plan = row.data || {};
                return (
                  <div>
                    <div className="text-equine-ink font-display text-xl leading-tight">{plan.horse_name || "Horse TBD"}</div>
                    <div className="text-[13px] text-equine-inkMuted mt-1">{plan.goal || "Goal TBD"}</div>
                    <div className="mt-2"><StatusPill tone={plan.status === "active" ? "warning" : "info"}>{labelFor(plan.status || "planned")}</StatusPill></div>
                  </div>
                );
              }}
            />
          </div>

          <SectionEyebrow>Assigned Context</SectionEyebrow>
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
            <ContextCard
              title="Assigned Horses"
              empty="Assigned horses will appear here with status, discipline, and current training goals."
              rows={data.assigned_horses || []}
              render={(horse) => (
                <div>
                  <div className="text-equine-ink font-display text-xl">{horse.name}</div>
                  <div className="text-[12.5px] text-equine-inkMuted mt-1">
                    {[horse.status, horse.discipline].filter(Boolean).map(labelFor).join(" - ") || "No status yet"}
                  </div>
                  {horse.training_goals && <div className="text-[13px] text-equine-inkMuted mt-2">{horse.training_goals}</div>}
                </div>
              )}
            />
            <ContextCard
              title="Riders"
              empty="Riders connected through your lessons will appear here with skill level and goals."
              rows={data.riders || []}
              render={(rider) => (
                <div>
                  <div className="text-equine-ink font-display text-xl">{rider.full_name}</div>
                  <div className="text-[12.5px] text-equine-inkMuted mt-1">{rider.skill_level || "Skill level TBD"}</div>
                  {rider.goals && <div className="text-[13px] text-equine-inkMuted mt-2">{rider.goals}</div>}
                </div>
              )}
            />
          </div>
        </>
      )}
    </div>
  );
}

const RefreshButton = ({ onClick, refreshing }) => (
  <button onClick={onClick} disabled={refreshing} className="btn-secondary inline-flex items-center gap-2 disabled:opacity-50" data-testid="trainer-dashboard-refresh">
    <RefreshCw className="w-4 h-4" /> Refresh
  </button>
);

const ActionLinks = () => (
  <div className="flex items-center gap-3 text-[11px] uppercase tracking-[0.18em]">
    <Link to="/lessons" className="text-equine-lilac/80 hover:text-equine-lavender">Lessons</Link>
    <Link to="/training" className="text-equine-lilac/80 hover:text-equine-lavender">Training</Link>
    <Link to="/training-plans" className="text-equine-lilac/80 hover:text-equine-lavender">Plans</Link>
  </div>
);

const WorkCard = ({ title, icon: Icon, rows, empty, render }) => (
  <Card hover={false} data-testid={`trainer-${title.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
    <div className="flex items-center gap-2 mb-4">
      <Icon className="w-4 h-4 text-equine-lilac" />
      <h2 className="font-display text-2xl text-equine-ink">{title}</h2>
    </div>
    {rows.length === 0 ? (
      <SoftEmpty text={empty} />
    ) : (
      <div className="space-y-3">
        {rows.map((row) => (
          <div key={row.id} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4">{render(row)}</div>
        ))}
      </div>
    )}
  </Card>
);

const ContextCard = ({ title, rows, empty, render }) => (
  <Card hover={false} data-testid={`trainer-context-${title.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
    <h2 className="font-display text-2xl text-equine-ink mb-4">{title}</h2>
    {rows.length === 0 ? (
      <SoftEmpty text={empty} />
    ) : (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {rows.map((row) => (
          <div key={row.id} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4">{render(row)}</div>
        ))}
      </div>
    )}
  </Card>
);

const SoftEmpty = ({ text }) => (
  <div className="rounded-lg border border-dashed border-equine-cloud bg-equine-soft/45 py-8 px-5 text-center">
    <div className="mx-auto mb-3 h-1 w-10 rounded-full bg-equine-lavender" />
    <div className="text-[13px] leading-relaxed text-equine-inkMuted">{text}</div>
  </div>
);
