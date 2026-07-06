import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, track } from "../lib/api";
import { Card, PageHeader, StatusPill } from "../components/Primitives";
import { Logo } from "../components/Logo";
import { BrandLoader } from "../components/BrandLoader";
import { Check, ChevronRight, ChevronLeft, Rocket, Building2 } from "lucide-react";
import { toast } from "sonner";

import { STEP_META } from "../lib/onboardingMeta";
import BarnStep from "../components/onboarding/BarnStep";
import CrudStep from "../components/onboarding/CrudStep";
import { OwnersStep, HorsesStep, RidersStep } from "../components/onboarding/RecordsStep";
import StaffStep from "../components/onboarding/StaffStep";
import ReviewStep from "../components/onboarding/ReviewStep";
import OperationsSetupStep from "../components/onboarding/OperationsSetupStep";

/**
 * Setup concierge — guided onboarding shell.
 * State + composition only. Step content lives under components/onboarding/*.
 * Behaviour preserved: autosave on any change, stepper navigation,
 * skip / back / save+continue, final Launch button.
 */
const renderStep = (stepId, onAnyChange, onFinish) => {
  switch (stepId) {
    case "barn":           return <BarnStep onAnyChange={onAnyChange} />;
    case "locations":      return <CrudStep kind="locations" onAnyChange={onAnyChange} />;
    case "owners":         return <OwnersStep onAnyChange={onAnyChange} />;
    case "horses":         return <HorsesStep onAnyChange={onAnyChange} />;
    case "riders":         return <RidersStep onAnyChange={onAnyChange} />;
    case "feed_templates": return <CrudStep kind="feed_templates" onAnyChange={onAnyChange} />;
    case "inventory":      return <CrudStep kind="inventory" onAnyChange={onAnyChange} />;
    case "operations_setup": return <OperationsSetupStep onAnyChange={onAnyChange} />;
    case "staff":          return <StaffStep onAnyChange={onAnyChange} />;
    case "schedules":      return <CrudStep kind="schedules" onAnyChange={onAnyChange} />;
    case "review":         return <ReviewStep onFinish={onFinish} />;
    default:               return null;
  }
};

export default function Onboarding({ setupReadiness = null }) {
  const navigate = useNavigate();
  const [steps, setSteps] = useState([]);
  const [progress, setProgress] = useState(null);
  const [readiness, setReadiness] = useState(setupReadiness);
  const [currentId, setCurrentId] = useState("barn");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (setupReadiness) setReadiness(setupReadiness);
  }, [setupReadiness]);

  useEffect(() => {
    const readinessRequest = api.get("/onboarding/readiness")
      .then((r) => r.data)
      .catch(() => setupReadiness);

    Promise.all([api.get("/onboarding/steps"), api.get("/onboarding/progress"), readinessRequest])
      .then(([s, p, ready]) => {
        // Founder-beta: recurring schedules collection is intentionally hidden
        // until the scheduler is wired to materialize tasks (see audit §J.6).
        // Backend model + endpoints remain intact so data persists across
        // releases — only the founder-facing step is removed.
        const visibleSteps = s.data.steps.filter((step) => step.id !== "schedules");
        setSteps(visibleSteps);
        setProgress(p.data);
        if (ready) setReadiness(ready);
        const startId = p.data.current_step === "schedules"
          ? (visibleSteps.find((st) => p.data.steps?.[st.id] !== "complete")?.id || visibleSteps[0].id)
          : (p.data.current_step || visibleSteps[0].id);
        setCurrentId(startId);
      })
      .finally(() => setLoading(false));
  }, [setupReadiness]);

  const setStepStatus = async (step_id, status) => {
    const r = await api.patch("/onboarding/progress", { step_id, status });
    setProgress(r.data);
  };
  const setCurrent = async (step_id) => {
    setCurrentId(step_id);
    const r = await api.patch("/onboarding/progress", { current_step: step_id });
    setProgress(r.data);
  };
  const refreshReadiness = async () => {
    const response = await api.get("/onboarding/readiness");
    setReadiness(response.data);
    return response.data;
  };

  if (loading || !progress) {
    return <BrandLoader label="Loading concierge…" />;
  }

  const stepIndex = steps.findIndex((s) => s.id === currentId);
  const current = steps[stepIndex];
  const Icon = STEP_META[current?.id]?.icon || Building2;
  // Founder-beta: compute percent off visible steps only (hidden ones don't count).
  const completedVisible = steps.filter((s) =>
    (progress.steps?.[s.id] || "pending") === "complete"
  ).length;
  const percent = steps.length === 0 ? 0 : Math.round(100 * completedVisible / steps.length);
  const currentStatus = progress.steps?.[currentId] || "pending";
  const currentStatusLabel = currentStatus.replace(/_/g, " ");
  const readinessBlockers = readiness?.blockers || [];
  const readinessWarnings = readiness?.warnings || [];
  const canFinalizeSetup = readiness?.can_finalize !== false;

  const next = async () => {
    await setStepStatus(currentId, "complete");
    track("onboarding.step_completed", { step: currentId });
    refreshReadiness().catch(() => null);
    if (stepIndex < steps.length - 1) setCurrent(steps[stepIndex + 1].id);
  };
  const skip = async () => {
    await setStepStatus(currentId, "skipped");
    track("onboarding.step_skipped", { step: currentId });
    refreshReadiness().catch(() => null);
    if (stepIndex < steps.length - 1) setCurrent(steps[stepIndex + 1].id);
  };
  const back = () => {
    if (stepIndex > 0) setCurrent(steps[stepIndex - 1].id);
  };
  const launch = async () => {
    if (!canFinalizeSetup) {
      toast.error("Only a facility admin or barn owner can launch setup.");
      return;
    }
    try {
      await setStepStatus("review", "complete");
      const response = await api.post("/onboarding/complete");
      if (response.data?.readiness) setReadiness(response.data.readiness);
      track("onboarding.completed", { percent: 100 });
      toast.success("Barn setup complete!");
      navigate("/");
    } catch (error) {
      const status = error?.response?.status;
      const detail = error?.response?.data?.detail;
      if (status === 409 && detail) {
        setReadiness(detail);
        toast.error(detail.message || "Setup still has required blockers.");
        return;
      }
      if (status === 403) {
        toast.error("Only a facility admin or barn owner can launch setup.");
        return;
      }
      toast.error("Setup could not be completed. Please try again.");
    }
  };

  return (
    <div data-testid="onboarding-page" className="max-w-7xl">
      <div className="mb-5"><Logo size={68} /></div>
      <PageHeader
        eyebrow="Setup Concierge"
        title="Welcome to your barn"
        subtitle="A guided walkthrough to bring your facility online. Skip anything — autosave keeps your progress so you can return whenever you like."
        action={
          <div className="text-right">
            <div className="label-eyebrow">Setup progress</div>
            <div className="font-display text-3xl text-equine-champagne mt-1">{percent}%</div>
          </div>
        }
      />

      {readiness && (
        <Card hover={false} className="mb-6" data-testid="setup-readiness-panel">
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <div>
              <div className="label-eyebrow">Backend Readiness</div>
              <h2 className="font-display text-2xl text-equine-ivory mt-1">
                {readiness.can_complete
                  ? "Ready To Launch"
                  : canFinalizeSetup
                    ? "Required Setup Evidence Needed"
                    : "Read-Only Setup Review"}
              </h2>
              <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">
                {canFinalizeSetup
                  ? "Facility setup completion is now checked by the server before launch."
                  : "Barn managers can inspect setup readiness, but only a facility admin or barn owner can launch the barn."}
              </p>
            </div>
            <StatusPill tone={readiness.can_complete ? "success" : canFinalizeSetup ? "warning" : "neutral"}>
              {readiness.can_complete ? "ready" : canFinalizeSetup ? `${readinessBlockers.length} blocker${readinessBlockers.length === 1 ? "" : "s"}` : "view only"}
            </StatusPill>
          </div>
          {readinessBlockers.length > 0 && (
            <div className="mt-4 grid md:grid-cols-2 gap-2" data-testid="setup-readiness-blockers">
              {readinessBlockers.slice(0, 6).map((item) => (
                <div key={item.step_id} className="rounded-xl border border-equine-rose/25 bg-equine-rose/8 px-3 py-2">
                  <div className="text-[11px] uppercase tracking-[0.16em] text-equine-rose/80">{item.step_id}</div>
                  <div className="text-[13px] text-equine-platinum/75 mt-1">{item.message}</div>
                </div>
              ))}
            </div>
          )}
          {readinessWarnings.length > 0 && (
            <div className="mt-3 text-[12px] text-equine-platinum/60" data-testid="setup-readiness-warnings">
              {readinessWarnings.length} non-blocking setup note{readinessWarnings.length === 1 ? "" : "s"} recorded.
            </div>
          )}
        </Card>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* ───── Stepper ───── */}
        <Card hover={false} className="lg:col-span-1 !p-3 self-start sticky top-24">
          <div className="px-3 py-2">
            <div className="h-1.5 rounded-full bg-equine-soft overflow-hidden">
              <div className="h-full bg-equine-champagne transition-all duration-500" style={{ width: `${percent}%` }} />
            </div>
          </div>
          <ul className="mt-2">
            {steps.map((s) => {
              const Ic = STEP_META[s.id]?.icon || Building2;
              const status = progress.steps?.[s.id] || "pending";
              const isCurrent = s.id === currentId;
              const isDone = status === "complete";
              const isSkipped = status === "skipped";
              return (
                <li key={s.id}>
                  <button
                    onClick={() => setCurrent(s.id)}
                    data-testid={`step-nav-${s.id}`}
                    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${
                      isCurrent
                        ? "bg-equine-steel/30 border border-equine-steel/40 text-equine-ivory"
                        : "hover:bg-equine-soft text-equine-silver/80"
                    }`}
                  >
                    <div className={`w-7 h-7 rounded-full flex items-center justify-center text-[11px] border ${
                      isDone     ? "bg-equine-sage/20 border-equine-sage text-equine-sage"
                      : isSkipped ? "bg-equine-soft border-equine-graphite text-equine-platinum/60"
                      : isCurrent ? "bg-equine-champagne text-equine-black border-equine-champagne"
                                  : "bg-equine-soft border-equine-graphite/60 text-equine-platinum/60"
                    }`}>
                      {isDone ? <Check className="w-3.5 h-3.5" /> : <Ic className="w-3.5 h-3.5" />}
                    </div>
                    <span className="text-[13px] flex-1 text-left">{s.label}</span>
                    {!s.required && (
                      <span className="text-[9px] tracking-[0.18em] uppercase text-equine-platinum/50">opt</span>
                    )}
                  </button>
                </li>
              );
            })}
          </ul>
          <div className="hairline mt-2 pt-3 px-3 pb-1 text-[11px] text-equine-platinum/60">
            Autosave on · You can leave &amp; resume any time.
          </div>
          <div
            data-testid="onboarding-reassurance"
            className="px-3 pb-3 pt-1 text-[11px] text-equine-platinum/55 leading-relaxed"
          >
            Most barns revisit Inventory and Operations &amp; Sharing after their first operational week. Nothing here is required to begin running daily care.
          </div>
        </Card>

        {/* ───── Content ───── */}
        <div className="lg:col-span-3">
          <Card hover={false}>
            <div className="flex items-start gap-4 mb-6">
              <div className="w-12 h-12 rounded-2xl bg-equine-steel/25 border border-equine-steel/40 flex items-center justify-center">
                <Icon strokeWidth={1.4} className="text-equine-champagne" />
              </div>
              <div className="flex-1">
                <div className="label-eyebrow">Step {stepIndex + 1} of {steps.length}</div>
                <h2 className="font-display text-3xl text-equine-ivory mt-1">{current?.label}</h2>
              </div>
              <StatusPill tone={
                currentStatus === "complete" ? "success"
                : currentStatus === "skipped" ? "neutral"
                : "info"
              }>
                {currentStatusLabel}
              </StatusPill>
            </div>

            {renderStep(currentId,
                        () => setStepStatus(currentId, "in_progress"),
                        () => navigate("/"))}

            <div className="mt-8 pt-6 hairline flex items-center justify-between">
              <button
                onClick={back}
                disabled={stepIndex === 0}
                data-testid="step-back"
                className="btn-secondary disabled:opacity-40 inline-flex items-center gap-2"
              >
                <ChevronLeft className="w-4 h-4" /> Back
              </button>
              <div className="flex items-center gap-2">
                {!current?.required && (
                  <button onClick={skip} data-testid="step-skip" className="btn-secondary">
                    Skip for now
                  </button>
                )}
                {currentId === "review" ? (
                  <button
                    onClick={launch}
                    disabled={!canFinalizeSetup}
                    data-testid="step-finish"
                    className="btn-primary disabled:opacity-40 disabled:cursor-not-allowed inline-flex items-center gap-2"
                  >
                    Launch barn <Rocket className="w-4 h-4" />
                  </button>
                ) : (
                  <button onClick={next} data-testid="step-next" className="btn-primary inline-flex items-center gap-2">
                    Save &amp; continue <ChevronRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
