import React from "react";
import { Eye, ListChecks, MonitorSmartphone, Route, ShieldCheck, WandSparkles } from "lucide-react";
import { LAUNCH_READINESS_EVIDENCE, QA_STATUS, TW10_QA_CHECKS } from "../lib/qualityGate";
import { Card, StatusPill } from "./Primitives";

const ICONS = [WandSparkles, MonitorSmartphone, Eye, Route, ListChecks, ShieldCheck];
const TONE = {
  ready_for_review: "success",
  guarded: "info",
  blocked_until_verified: "warning",
};

export default function QualityGatePanel({ testid = "tw10-quality-gate-panel" }) {
  return (
    <Card hover={false} className="mb-8" data-testid={testid}>
      <div className="flex items-start justify-between gap-4 flex-wrap mb-5">
        <div>
          <div className="label-eyebrow mb-2">TW10 Quality Gate</div>
          <h2 className="font-display text-3xl text-equine-ink leading-tight">Launch-Readiness Evidence</h2>
          <p className="mt-2 text-[13px] leading-relaxed text-equine-inkMuted max-w-2xl">
            Final review evidence should prove visual consistency, mobile readiness, accessibility posture, route safety, data-state coverage, and claim boundaries before launch authority is considered.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
        {TW10_QA_CHECKS.map((item, index) => {
          const Icon = ICONS[index % ICONS.length];
          return (
            <div key={item.id} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4 min-h-[166px]" data-testid={`tw10-check-${item.id}`}>
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-2 min-w-0">
                  <Icon className="w-3.5 h-3.5 text-equine-brass flex-shrink-0" strokeWidth={1.7} />
                  <div className="text-equine-ink text-[14px] truncate">{item.label}</div>
                </div>
                <StatusPill tone={TONE[item.status] || "neutral"}>{QA_STATUS[item.status]}</StatusPill>
              </div>
              <p className="text-[12.5px] leading-relaxed text-equine-inkMuted">{item.proof}</p>
              <p className="mt-3 text-[12px] leading-relaxed text-equine-inkSoft">{item.evidence}</p>
            </div>
          );
        })}
      </div>

      <div className="mt-4 rounded-lg border border-equine-hairline bg-white/55 p-4" data-testid="tw10-launch-evidence">
        <div className="text-[10.5px] uppercase tracking-[0.2em] text-equine-inkMuted font-semibold mb-3">
          Evidence Summary
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {LAUNCH_READINESS_EVIDENCE.map(([label, value]) => (
            <div key={label}>
              <div className="text-[12px] text-equine-ink font-medium">{label}</div>
              <div className="text-[12.5px] leading-relaxed text-equine-inkMuted mt-1">{value}</div>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}
