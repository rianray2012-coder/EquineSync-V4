import React from "react";
import { HeartPulse, ListChecks, ShieldCheck, Sparkles } from "lucide-react";
import { OWNER_WELLBEING_SIGNALS, RELATIONSHIP_STATUS } from "../lib/relationshipWorkflow";
import { Card, StatusPill } from "./Primitives";

const ICONS = [HeartPulse, ListChecks, ShieldCheck, Sparkles];
const STATUS_BY_INDEX = ["visible_now", "review_needed", "gated", "planned"];
const TONE = {
  visible_now: "success",
  review_needed: "warning",
  gated: "info",
  planned: "neutral",
};

export default function OwnerWellbeingPanel({ profile = "owner", testid = "owner-wellbeing-panel" }) {
  const profileLabel = profile === "guardian" ? "guardian" : profile === "rider" ? "rider" : "owner";

  return (
    <Card hover={false} className="mb-4" data-testid={testid}>
      <div className="flex items-start justify-between gap-4 flex-wrap mb-5">
        <div>
          <div className="label-eyebrow mb-2">Owner Wellbeing</div>
          <h2 className="font-display text-3xl text-equine-ink leading-tight">Wellbeing Trust Map</h2>
          <p className="mt-2 text-[13px] leading-relaxed text-equine-inkMuted max-w-2xl">
            A {profileLabel} view should explain care confidence, request status, visibility boundaries, and the first-week path without exposing internal barn context.
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
        {OWNER_WELLBEING_SIGNALS.map((item, index) => {
          const Icon = ICONS[index % ICONS.length];
          const status = STATUS_BY_INDEX[index] || "planned";
          return (
            <div key={item.id} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4 min-h-[168px]" data-testid={`owner-wellbeing-${item.id}`}>
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-2 min-w-0">
                  <Icon className="w-3.5 h-3.5 text-equine-brass flex-shrink-0" strokeWidth={1.7} />
                  <div className="text-equine-ink text-[14px] truncate">{item.label}</div>
                </div>
                <StatusPill tone={TONE[status]}>{RELATIONSHIP_STATUS[status]}</StatusPill>
              </div>
              <p className="text-[12.5px] leading-relaxed text-equine-inkMuted">{item.proof}</p>
              <p className="mt-3 text-[12px] leading-relaxed text-equine-inkSoft">{item.nextStep}</p>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
