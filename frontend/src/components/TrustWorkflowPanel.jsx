import React from "react";
import { CheckCircle2, Eye, ListChecks, ShieldCheck } from "lucide-react";
import { ROLE_NORTH_STAR } from "../lib/trustWorkflow";
import { Card, StatusPill } from "./Primitives";

const itemsFor = (config) => [
  ["Changed", config.changed, Eye],
  ["Decision", config.decision, ListChecks],
  ["Safe To Ignore", config.safe, ShieldCheck],
  ["Proof", config.proof, CheckCircle2],
];

export default function TrustWorkflowPanel({ roleKey, className = "", testid }) {
  const config = ROLE_NORTH_STAR[roleKey] || ROLE_NORTH_STAR.owner;

  return (
    <Card hover={false} className={`mb-8 ${className}`} data-testid={testid || `trust-workflow-${roleKey}`}>
      <div className="flex items-start justify-between gap-4 flex-wrap mb-5">
        <div>
          <div className="label-eyebrow mb-2">{config.eyebrow}</div>
          <h2 className="font-display text-3xl text-equine-ink leading-tight">{config.title}</h2>
        </div>
        <StatusPill tone="info" dot>{config.status}</StatusPill>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
        {itemsFor(config).map(([label, body, Icon]) => (
          <div key={label} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4 min-h-[132px]">
            <div className="flex items-center gap-2 mb-2">
              <Icon className="w-3.5 h-3.5 text-equine-brass" strokeWidth={1.7} />
              <div className="text-[10.5px] uppercase tracking-[0.2em] text-equine-inkMuted font-semibold">{label}</div>
            </div>
            <p className="text-[13px] leading-relaxed text-equine-inkMuted">{body}</p>
          </div>
        ))}
      </div>
    </Card>
  );
}
