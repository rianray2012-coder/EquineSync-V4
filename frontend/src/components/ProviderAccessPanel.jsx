import React from "react";
import {
  Ban,
  ClipboardList,
  FileText,
  KeyRound,
  MessageSquare,
  Receipt,
  ShieldAlert,
  ShieldCheck,
} from "lucide-react";
import {
  PROVIDER_ACCESS_SIGNALS,
  PROVIDER_ACCESS_STATUS,
  PROVIDER_ACCESS_STOP_RULES,
} from "../lib/providerAccessWorkflow";
import { Card, StatusPill } from "./Primitives";

const ICONS = [KeyRound, ClipboardList, Ban, ShieldCheck, FileText, MessageSquare, Receipt, ShieldAlert];
const TONE = {
  gated: "info",
  planned: "neutral",
  review_needed: "warning",
  provider_required: "warning",
};

export default function ProviderAccessPanel({ testid = "provider-access-panel" }) {
  return (
    <Card hover={false} className="mb-10" data-testid={testid}>
      <div className="flex items-start justify-between gap-4 flex-wrap mb-5">
        <div>
          <div className="label-eyebrow mb-2">Provider Access</div>
          <h2 className="font-display text-3xl text-equine-ink leading-tight">Scoped Access Map</h2>
          <p className="mt-2 text-[13px] leading-relaxed text-equine-inkMuted max-w-2xl">
            Provider access must stay tied to explicit grants, visit context, review state, revocation, and visible audit boundaries.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
        {PROVIDER_ACCESS_SIGNALS.map((item, index) => {
          const Icon = ICONS[index % ICONS.length];
          return (
            <div key={item.id} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4 min-h-[178px]" data-testid={`provider-access-${item.id}`}>
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-2 min-w-0">
                  <Icon className="w-3.5 h-3.5 text-equine-brass flex-shrink-0" strokeWidth={1.7} />
                  <div className="text-equine-ink text-[14px] truncate">{item.label}</div>
                </div>
                <StatusPill tone={TONE[item.status] || "neutral"}>{PROVIDER_ACCESS_STATUS[item.status]}</StatusPill>
              </div>
              <p className="text-[12.5px] leading-relaxed text-equine-inkMuted">{item.proof}</p>
              <p className="mt-3 text-[12px] leading-relaxed text-equine-inkSoft">{item.nextStep}</p>
            </div>
          );
        })}
      </div>

      <div className="mt-4 rounded-lg border border-equine-hairline bg-white/55 p-4" data-testid="provider-access-stop-rules">
        <div className="text-[10.5px] uppercase tracking-[0.2em] text-equine-inkMuted font-semibold mb-3">
          Stop Rules
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {PROVIDER_ACCESS_STOP_RULES.map((rule) => (
            <div key={rule} className="text-[12.5px] leading-relaxed text-equine-inkMuted">
              {rule}
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}
