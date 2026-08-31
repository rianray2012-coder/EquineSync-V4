import React from "react";
import { CheckCircle2, CircleDot, LockKeyhole, PlugZap } from "lucide-react";
import { FACILITY_READINESS_AREAS, readinessStatusFor } from "../lib/operationalProof";
import { Card, StatusPill } from "./Primitives";

const TONE = {
  complete: "success",
  in_progress: "warning",
  pending: "neutral",
  provider_required: "warning",
  gated: "info",
  planned: "neutral",
};

const ICON = {
  complete: CheckCircle2,
  provider_required: PlugZap,
  gated: LockKeyhole,
  in_progress: CircleDot,
  pending: CircleDot,
  planned: CircleDot,
};

const labelFor = (value) => String(value || "").replace(/_/g, " ");

export default function FacilityReadinessPanel({ progress, steps = [], testid = "facility-readiness-panel" }) {
  return (
    <Card hover={false} className="mb-8" data-testid={testid}>
      <div className="flex items-start justify-between gap-4 flex-wrap mb-5">
        <div>
          <div className="label-eyebrow mb-2">Launch Readiness</div>
          <h2 className="font-display text-3xl text-equine-ink leading-tight">Facility Readiness</h2>
          <p className="mt-2 text-[13px] leading-relaxed text-equine-inkMuted max-w-2xl">
            Setup, provider, and permission signals show what is ready, blocked, or still governed before a facility expands use.
          </p>
        </div>
        <StatusPill tone={progress?.completed ? "success" : "warning"} dot>
          {progress?.completed ? "setup complete" : "setup in progress"}
        </StatusPill>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3">
        {FACILITY_READINESS_AREAS.map((area) => {
          const status = readinessStatusFor(area, progress, steps);
          const Icon = ICON[status] || CircleDot;
          return (
            <div key={area.id} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4 min-h-[132px]" data-testid={`readiness-${area.id}`}>
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-2 min-w-0">
                  <Icon className="w-3.5 h-3.5 text-equine-brass flex-shrink-0" strokeWidth={1.7} />
                  <div className="text-equine-ink text-[14px] truncate">{area.label}</div>
                </div>
                <StatusPill tone={TONE[status] || "neutral"}>{labelFor(status)}</StatusPill>
              </div>
              <p className="text-[12.5px] leading-relaxed text-equine-inkMuted">{area.proof}</p>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
