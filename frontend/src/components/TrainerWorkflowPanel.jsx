import React from "react";
import { CalendarDays, ClipboardCheck, GraduationCap, ListChecks } from "lucide-react";
import { RELATIONSHIP_STATUS, TRAINER_WORKFLOW_SIGNALS } from "../lib/relationshipWorkflow";
import { Card, StatusPill } from "./Primitives";

const ICONS = [ListChecks, ClipboardCheck, GraduationCap, CalendarDays];
const STATUS_BY_INDEX = ["visible_now", "gated", "visible_now", "planned"];
const TONE = {
  visible_now: "success",
  review_needed: "warning",
  gated: "info",
  planned: "neutral",
};

export default function TrainerWorkflowPanel({ testid = "trainer-workflow-panel" }) {
  return (
    <Card hover={false} className="mb-10" data-testid={testid}>
      <div className="flex items-start justify-between gap-4 flex-wrap mb-5">
        <div>
          <div className="label-eyebrow mb-2">Trainer Workflow</div>
          <h2 className="font-display text-3xl text-equine-ink leading-tight">Trainer Work Map</h2>
          <p className="mt-2 text-[13px] leading-relaxed text-equine-inkMuted max-w-2xl">
            Trainer work should stay centered on assigned horses, rider context, lesson timing, and reviewed note boundaries.
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
        {TRAINER_WORKFLOW_SIGNALS.map((item, index) => {
          const Icon = ICONS[index % ICONS.length];
          const status = STATUS_BY_INDEX[index] || "planned";
          return (
            <div key={item.id} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4 min-h-[168px]" data-testid={`trainer-workflow-${item.id}`}>
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
