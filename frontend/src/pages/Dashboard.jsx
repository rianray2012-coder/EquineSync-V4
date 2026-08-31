import React, { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, money } from "../lib/api";
import { PageHeader, Stat, SectionEyebrow } from "../components/Primitives";
import {
  Pill, GraduationCap, Heart, UtensilsCrossed, Cat,
  Stethoscope, Receipt, BedDouble, Sunrise, ArrowRight, Compass,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

import SetupConciergeCard from "../components/dashboard/SetupConciergeCard";
import FacilityReadinessPanel from "../components/FacilityReadinessPanel";
import ActionTile from "../components/dashboard/ActionTile";
import AlertsCard from "../components/dashboard/AlertsCard";
import { OperationsCard, UpcomingCareCard } from "../components/dashboard/SmallCards";
import OperationalProofPanel from "../components/OperationalProofPanel";
import FounderWalkthrough, { walkthroughSeen } from "../components/FounderWalkthrough";
import LastSyncedBadge from "../components/today/LastSyncedBadge";
import { BrandLoader } from "../components/BrandLoader";
import { canManageBilling } from "../lib/permissions";
import { RESUMABLE_STATUSES, STATUS_LABEL } from "../lib/subscriptionBilling";
import { UsageMeter } from "../components/UsageMeter";
import { useSubscriptionUsage } from "../lib/useSubscriptionUsage";

/**
 * Stable Command — operational glance, not an analytics board.
 * State + composition lives here; widget rendering lives under
 * components/dashboard/*. Greeting + onboarding gating only.
 */
export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [progress, setProgress] = useState(null);
  const [steps, setSteps] = useState([]);
  const [upcoming, setUpcoming] = useState([]);
  const [upcomingLoading, setUpcomingLoading] = useState(true);
  const [walkthroughOpen, setWalkthroughOpen] = useState(false);
  const [lastSyncedAt, setLastSyncedAt] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const loadAll = useCallback(async () => {
    setRefreshing(true);
    try {
      const today = new Date();
      const in7 = new Date(today.getTime() + 7 * 24 * 3600 * 1000);
      const [summaryRes, progressRes, stepsRes, tasksRes] = await Promise.allSettled([
        api.get("/dashboard/summary"),
        api.get("/onboarding/progress"),
        api.get("/onboarding/steps"),
        api.get("/tasks", { params: { start: today.toISOString(), end: in7.toISOString(), limit: 200 } }),
      ]);
      if (summaryRes.status === "fulfilled") setSummary(summaryRes.value.data);
      if (progressRes.status === "fulfilled") setProgress(progressRes.value.data);
      if (stepsRes.status === "fulfilled") setSteps(stepsRes.value.data.steps);
      else setSteps([]);
      if (tasksRes.status === "fulfilled") {
        const items = (tasksRes.value.data?.items || []).filter(
          (t) => ["vet", "farrier", "rehab"].includes(t.category)
                 && !["completed", "skipped", "cancelled"].includes(t.status),
        );
        setUpcoming(items.slice(0, 8));
      } else {
        setUpcoming([]);
      }
      setLastSyncedAt(new Date());
    } finally {
      setUpcomingLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => { loadAll(); }, [loadAll]);

  // Calm one-time founder walkthrough auto-open: only for setup roles who
  // finished onboarding and haven't seen it yet. Never auto-shown again.
  useEffect(() => {
    if (!user) return;
    if (!["admin", "barn_manager"].includes(user.role)) return;
    if (walkthroughSeen()) return;
    if (!progress?.completed) return;
    setWalkthroughOpen(true);
  }, [user, progress]);

  const firstName = user?.full_name?.split(" ")[0] || "there";
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";

  if (!summary) {
    return (
      <div data-testid="dashboard-page" className="pb-20 lg:pb-8">
        <BrandLoader label="Loading your barn…" />
      </div>
    );
  }

  return (
    <div data-testid="dashboard-page" className="pb-20 lg:pb-8">
      <PageHeader
        eyebrow={`${greeting}, ${firstName}`}
        title="Stable Command"
        subtitle="A live overview of horses, daily care, alerts and operations across your facility."
        action={
          <div className="flex items-center gap-2 flex-wrap justify-end">
            <LastSyncedBadge
              at={lastSyncedAt}
              onRefresh={loadAll}
              refreshing={refreshing}
              verb="Updated"
              tone="secondary"
            />
            <button
              data-testid="walkthrough-launch"
              onClick={() => setWalkthroughOpen(true)}
              className="inline-flex items-center gap-1.5 text-[11.5px] uppercase tracking-[0.2em] text-equine-lilac/80 hover:text-equine-lavender transition-colors px-3 py-1.5 rounded-full border border-equine-graphite/40 hover:border-equine-lilac/50"
            >
              <Compass className="w-3.5 h-3.5" /> Founder tour
            </button>
          </div>
        }
      />

      <FounderWalkthrough
        open={walkthroughOpen}
        onClose={() => setWalkthroughOpen(false)}
      />

      <SubscriptionResumeBanner user={user} />

      <SubscriptionUsageSnapshot />

      <SetupConciergeCard progress={progress} steps={steps} />

      <OperationalProofPanel
        proofKey="facility"
        title="Facility Proof Snapshot"
        testid="facility-proof-snapshot"
      />

      <FacilityReadinessPanel progress={progress} steps={steps} />

      {/* SECTION 1 · Right now */}
      <SectionEyebrow
        action={
          <Link
            to="/today"
            className="text-[11px] uppercase tracking-[0.22em] text-equine-lilac/80 hover:text-equine-lavender inline-flex items-center gap-1.5"
          >
            Open Today <ArrowRight className="w-3 h-3" />
          </Link>
        }
      >
        Right Now · Immediate Tasks
      </SectionEyebrow>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-12 animate-fade-in">
        <ActionTile
          icon={UtensilsCrossed}
          label="Feed pending"
          value={summary?.feed_pending ?? "—"}
          caption={`of ${summary?.feed_today_total ?? 0} meals today`}
          tone="lilac"
          to="/feed"
          testid="tile-feed"
        />
        <ActionTile
          icon={Pill}
          label="Medications due"
          value={summary?.meds_due ?? "—"}
          caption={summary?.meds_missed ? `${summary.meds_missed} missed earlier` : "All on schedule"}
          tone={summary?.meds_missed > 0 ? "warning" : "sage"}
          to="/medications"
          testid="tile-meds"
        />
        <ActionTile
          icon={GraduationCap}
          label="Lessons today"
          value={summary?.lessons_today ?? "—"}
          caption="Scheduled rides & lessons"
          tone="info"
          to="/lessons"
          testid="tile-lessons"
        />
        <ActionTile
          icon={BedDouble}
          label="Stall rest"
          value={summary?.stall_rest ?? "—"}
          caption={`${summary?.active_injuries ?? 0} active injuries`}
          tone={summary?.stall_rest > 0 ? "critical" : "sage"}
          to="/stall-rest"
          testid="tile-stall"
        />
      </div>

      {/* SECTION 2 · Daily care workflows */}
      <SectionEyebrow>Daily Care · Workflows</SectionEyebrow>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12 animate-fade-in-delay-1">
        <OperationsCard summary={summary} />
        <UpcomingCareCard upcoming={upcoming} loading={upcomingLoading} />
      </div>

      {/* SECTION 3 · Attention */}
      <SectionEyebrow>Attention · Alerts</SectionEyebrow>
      <AlertsCard summary={summary} />

      {/* SECTION 4 · Operational analytics (secondary) */}
      <SectionEyebrow>Operations · Analytics</SectionEyebrow>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-5 animate-fade-in-delay-3">
        <Stat testid="stat-horses"   label="Horses in Barn"   value={summary?.total_horses ?? "—"}    caption="Active in operations" icon={Cat} />
        <Stat testid="stat-wellness" label="Avg Wellness"     value={summary?.avg_wellness ?? "—"}    accent="sage"   caption="0–100 score" icon={Heart} />
        <Stat testid="stat-meds-due" label="Meds Due"         value={summary?.meds_due ?? 0}          accent="amber"  caption={`${summary?.meds_missed ?? 0} missed today`} icon={Pill} />
        <Stat testid="stat-injuries" label="Active Injuries"  value={summary?.active_injuries ?? 0}   accent="clay"   caption={`${summary?.stall_rest ?? 0} on stall rest`} icon={Stethoscope} />
        <Stat testid="stat-revenue"  label="Outstanding"      value={money(summary?.overdue_amount ?? 0)} accent="lilac" caption={`${summary?.overdue_invoices ?? 0} invoice(s)`} icon={Receipt} />
      </div>

      {/* Mobile FAB → Today */}
      <button
        onClick={() => navigate("/today")}
        className="fab lg:hidden"
        data-testid="dashboard-fab"
        aria-label="Open today's operational pulse"
      >
        <Sunrise strokeWidth={1.6} className="w-7 h-7" />
      </button>
    </div>
  );
}

// Phase 15.F — secondary "Resume membership" CTA. Renders only for users
// with the `barn:manage` capability whose subscription is in a resumable
// state (canceled / past_due / unpaid / incomplete_expired). The primary
// action lives at /billing/subscription; this is the lightweight Dashboard
// pointer.
function SubscriptionResumeBanner({ user }) {
  const [sub, setSub] = useState(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    if (!canManageBilling(user)) {
      setReady(true);
      return;
    }
    let cancelled = false;
    api.get("/subscriptions/me")
      .then((r) => { if (!cancelled) setSub(r.data?.subscription || null); })
      .catch(() => { /* silent — banner just doesn't render */ })
      .finally(() => { if (!cancelled) setReady(true); });
    return () => { cancelled = true; };
  }, [user]);

  if (!ready) return null;
  if (!sub || !RESUMABLE_STATUSES.has(sub.status)) return null;

  return (
    <div
      className="mb-6 rounded-xl border border-equine-clay/30 bg-equine-clay/8 p-4 flex flex-wrap items-center gap-4"
      data-testid="dashboard-resume-banner"
    >
      <div className="inline-flex w-8 h-8 rounded-full bg-equine-clay/15 border border-equine-clay/30 items-center justify-center">
        <Receipt strokeWidth={1.5} className="w-4 h-4 text-equine-clay" />
      </div>
      <div className="flex-1 min-w-[200px]">
        <div className="text-equine-ink text-[14px] font-medium leading-snug">
          Your {sub.plan_tier_code} membership is {STATUS_LABEL[sub.status] || sub.status}.
        </div>
        <div className="text-equine-inkMuted text-[12.5px] mt-0.5">
          Resume from the Subscription page to keep your facility features.
        </div>
      </div>
      <Link
        to="/billing/subscription"
        data-testid="dashboard-resume-cta"
        className="inline-flex items-center gap-1.5 text-[12px] tracking-wide font-medium px-4 py-2 rounded-full bg-equine-navy text-white hover:bg-equine-navyLift transition-colors"
      >
        Resume membership <ArrowRight className="w-3.5 h-3.5" />
      </Link>
    </div>
  );
}


// Phase 15.F — Dashboard usage snapshot. Two-meter tile (horses + staff)
// for `barn:manage` users only. Always read-only. Hidden by the hook when
// the user is non-eligible or on an unlimited plan.
function SubscriptionUsageSnapshot() {
  const { usage } = useSubscriptionUsage();
  if (!usage) return null;
  // Skip entirely on unlimited plans (no meaningful meter to show).
  const hLimit = usage.usage?.horses?.limit;
  const uLimit = usage.usage?.users?.limit;
  const anyLimited = (hLimit && Number.isFinite(hLimit) && hLimit > 0)
                  || (uLimit && Number.isFinite(uLimit) && uLimit > 0);
  if (!anyLimited) return null;
  return (
    <div className="mb-6" data-testid="dashboard-usage-snapshot">
      <div className="flex items-center justify-between mb-2">
        <div className="label-eyebrow">Plan usage</div>
        <Link
          to="/billing/subscription"
          className="text-[11.5px] tracking-wide text-equine-lilacDeep hover:text-equine-ink inline-flex items-center gap-1"
          data-testid="dashboard-usage-snapshot-link"
        >
          Manage plan <ArrowRight className="w-3 h-3" />
        </Link>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <UsageMeter usage={usage} kind="horses" variant="card" />
        <UsageMeter usage={usage} kind="users" variant="card" />
      </div>
    </div>
  );
}

