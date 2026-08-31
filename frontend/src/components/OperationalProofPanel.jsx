import React from "react";
import { ClipboardCheck, History, ShieldCheck, TimerReset } from "lucide-react";
import { PROOF_SIGNALS } from "../lib/operationalProof";
import { Card } from "./Primitives";

const ICONS = [TimerReset, ClipboardCheck, History, ShieldCheck];

export default function OperationalProofPanel({ proofKey = "facility", title = "Operational Proof", testid }) {
  const rows = PROOF_SIGNALS[proofKey] || PROOF_SIGNALS.facility;

  return (
    <Card hover={false} className="mb-8" data-testid={testid || `operational-proof-${proofKey}`}>
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <div className="label-eyebrow mb-2">Proof Layer</div>
          <h2 className="font-display text-3xl text-equine-ink leading-tight">{title}</h2>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
        {rows.map(([label, body], index) => {
          const Icon = ICONS[index % ICONS.length];
          return (
            <div key={label} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4 min-h-[120px]">
              <div className="flex items-center gap-2 mb-2">
                <Icon className="w-3.5 h-3.5 text-equine-brass" strokeWidth={1.7} />
                <div className="text-[10.5px] uppercase tracking-[0.2em] text-equine-inkMuted font-semibold">{label}</div>
              </div>
              <p className="text-[13px] leading-relaxed text-equine-inkMuted">{body}</p>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
