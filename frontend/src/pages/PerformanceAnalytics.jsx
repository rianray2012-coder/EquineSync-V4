import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, BarChart3, RefreshCw, Target, Trophy } from "lucide-react";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";

const safeNum = (value) => Number(value) || 0;

export default function PerformanceAnalytics() {
  const [sessions, setSessions] = useState([]);
  const [plans, setPlans] = useState([]);
  const [competitions, setCompetitions] = useState([]);
  const [rides, setRides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [trainingRes, plansRes, competitionsRes, rideRes] = await Promise.all([
        api.get("/training"),
        api.get("/feature-modules/training-plans"),
        api.get("/feature-modules/competitions"),
        api.get("/feature-modules/ride-gps"),
      ]);
      setSessions(trainingRes.data || []);
      setPlans(plansRes.data.records || []);
      setCompetitions(competitionsRes.data.records || []);
      setRides(rideRes.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load performance analytics.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const analytics = useMemo(() => {
    const ratings = sessions.map((row) => safeNum(row.rating)).filter(Boolean);
    const averageRating = ratings.length ? ratings.reduce((sum, n) => sum + n, 0) / ratings.length : 0;
    const activePlans = plans.filter((record) => ((record.data || {}).status || "planned") === "active").length;
    const achievedGoals = plans.filter((record) => ((record.data || {}).status || "") === "achieved").length;
    const acceptedShows = competitions.filter((record) => ((record.data || {}).entry_status || "") === "accepted").length;
    const rideMiles = rides.reduce((sum, record) => sum + safeNum((record.data || {}).distance_miles), 0);

    const byTrainer = {};
    sessions.forEach((row) => {
      const key = row.trainer_name || "Unassigned";
      byTrainer[key] = byTrainer[key] || { trainer: key, sessions: 0, ratingTotal: 0, rated: 0, horses: new Set() };
      byTrainer[key].sessions += 1;
      byTrainer[key].horses.add(row.horse_name || row.horse_id || "Horse");
      if (safeNum(row.rating)) {
        byTrainer[key].ratingTotal += safeNum(row.rating);
        byTrainer[key].rated += 1;
      }
    });
    plans.forEach((record) => {
      const data = record.data || {};
      const key = data.trainer_name || "Unassigned";
      byTrainer[key] = byTrainer[key] || { trainer: key, sessions: 0, ratingTotal: 0, rated: 0, horses: new Set() };
      byTrainer[key].activePlans = (byTrainer[key].activePlans || 0) + (data.status === "active" ? 1 : 0);
      byTrainer[key].achievedGoals = (byTrainer[key].achievedGoals || 0) + (data.status === "achieved" ? 1 : 0);
    });

    const byHorse = {};
    sessions.forEach((row) => {
      const key = row.horse_name || row.horse_id || "Unassigned horse";
      byHorse[key] = byHorse[key] || { horse: key, sessions: 0, ratingTotal: 0, rated: 0, competitions: 0, miles: 0 };
      byHorse[key].sessions += 1;
      if (safeNum(row.rating)) {
        byHorse[key].ratingTotal += safeNum(row.rating);
        byHorse[key].rated += 1;
      }
    });
    competitions.forEach((record) => {
      const key = (record.data || {}).horse_name || "Unassigned horse";
      byHorse[key] = byHorse[key] || { horse: key, sessions: 0, ratingTotal: 0, rated: 0, competitions: 0, miles: 0 };
      byHorse[key].competitions += 1;
    });
    rides.forEach((record) => {
      const data = record.data || {};
      const key = data.horse_name || "Unassigned horse";
      byHorse[key] = byHorse[key] || { horse: key, sessions: 0, ratingTotal: 0, rated: 0, competitions: 0, miles: 0 };
      byHorse[key].miles += safeNum(data.distance_miles);
    });

    const trainers = Object.values(byTrainer)
      .map((row) => ({ ...row, horses: row.horses.size, averageRating: row.rated ? row.ratingTotal / row.rated : 0 }))
      .sort((a, b) => b.sessions - a.sessions || b.averageRating - a.averageRating);

    const horses = Object.values(byHorse)
      .map((row) => ({ ...row, averageRating: row.rated ? row.ratingTotal / row.rated : 0 }))
      .sort((a, b) => b.sessions + b.competitions + b.miles - (a.sessions + a.competitions + a.miles));

    return { averageRating, activePlans, achievedGoals, acceptedShows, rideMiles, trainers, horses };
  }, [sessions, plans, competitions, rides]);

  return (
    <div data-testid="performance-analytics-page">
      <PageHeader
        eyebrow="Training"
        title="Performance Analytics"
        subtitle="Trainer workload, horse progress signals, goal status, competition inputs, ride metrics, and performance trend summaries."
        action={
          <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="performance-refresh">
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading performance analytics...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Performance analytics unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : sessions.length === 0 && plans.length === 0 && competitions.length === 0 && rides.length === 0 ? (
        <Empty>
          <BarChart3 strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No performance data yet</div>
          <div className="text-[13px] text-equine-platinum/60">Log rides, plans, shows, or GPS tracks to populate analytics.</div>
        </Empty>
      ) : (
        <>
          <div className="grid grid-cols-2 xl:grid-cols-5 gap-4 mb-6">
            <Metric label="Training sessions" value={sessions.length} />
            <Metric label="Avg rating" value={analytics.averageRating ? analytics.averageRating.toFixed(1) : "—"} />
            <Metric label="Active goals" value={analytics.activePlans} />
            <Metric label="Accepted shows" value={analytics.acceptedShows} />
            <Metric label="GPS miles" value={analytics.rideMiles.toFixed(1)} />
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
            <Card hover={false} className="xl:col-span-3">
              <div className="flex items-center gap-2 mb-5">
                <Trophy className="w-4 h-4 text-equine-brass" />
                <h2 className="font-display text-3xl text-equine-ink">Trainer performance</h2>
              </div>
              {analytics.trainers.length === 0 ? (
                <SoftEmpty text="No trainer data yet." />
              ) : (
                <div className="space-y-3">
                  {analytics.trainers.map((row) => (
                    <div key={row.trainer} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`trainer-performance-${row.trainer.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`}>
                      <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                        <div className="flex-1 min-w-0">
                          <div className="font-display text-2xl text-equine-ink truncate">{row.trainer}</div>
                          <div className="text-[12.5px] text-equine-inkMuted">{row.horses} horse{row.horses === 1 ? "" : "s"} in work</div>
                        </div>
                        <InlineStat label="Sessions" value={row.sessions} />
                        <InlineStat label="Avg rating" value={row.averageRating ? row.averageRating.toFixed(1) : "—"} />
                        <InlineStat label="Active goals" value={row.activePlans || 0} />
                        <StatusPill tone={(row.achievedGoals || 0) > 0 ? "success" : "info"}>{row.achievedGoals || 0} achieved</StatusPill>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </Card>

            <Card hover={false} className="xl:col-span-2">
              <div className="flex items-center gap-2 mb-5">
                <Target className="w-4 h-4 text-equine-brass" />
                <h2 className="font-display text-3xl text-equine-ink">Horse progress</h2>
              </div>
              {analytics.horses.length === 0 ? (
                <SoftEmpty text="No horse progress data yet." />
              ) : (
                <div className="space-y-3">
                  {analytics.horses.slice(0, 8).map((row) => (
                    <div key={row.horse} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`horse-performance-${row.horse.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`}>
                      <div className="flex items-start justify-between gap-3 mb-3">
                        <div className="min-w-0">
                          <div className="font-display text-2xl text-equine-ink truncate">{row.horse}</div>
                          <div className="text-[12.5px] text-equine-inkMuted">
                            {row.sessions} sessions - {row.competitions} shows - {row.miles.toFixed(1)} GPS miles
                          </div>
                        </div>
                        <StatusPill tone="neutral">{row.averageRating ? `${row.averageRating.toFixed(1)}/10` : "unrated"}</StatusPill>
                      </div>
                      <Progress value={Math.min(100, Math.round((row.averageRating || 0) * 10))} />
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </div>
        </>
      )}
    </div>
  );
}

const Metric = ({ label, value }) => (
  <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
    <div className="label-eyebrow-muted mb-2">{label}</div>
    <div className="font-display text-4xl text-equine-ink leading-none">{value}</div>
  </div>
);

const InlineStat = ({ label, value }) => (
  <div className="min-w-[82px]">
    <div className="label-eyebrow-muted mb-1">{label}</div>
    <div className="font-display text-2xl text-equine-ink leading-none">{value}</div>
  </div>
);

const Progress = ({ value }) => (
  <div>
    <div className="h-2 rounded-full bg-equine-cloud overflow-hidden">
      <div className="h-full rounded-full bg-equine-brass" style={{ width: `${value}%` }} />
    </div>
    <div className="text-[11px] text-equine-inkSoft mt-1">Performance signal: {value}%</div>
  </div>
);

const SoftEmpty = ({ text }) => (
  <div className="rounded-xl border border-dashed border-equine-cloud bg-white/45 py-8 text-center text-[13px] text-equine-inkMuted">
    {text}
  </div>
);
