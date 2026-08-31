import React from "react";
import { BarChart3, ClipboardCheck, CreditCard, FileText, ShieldCheck, TrendingUp } from "lucide-react";
import { BUSINESS_PROOF_SIGNALS, BUSINESS_STATUS } from "../lib/businessWorkflow";
import { Card, StatusPill } from "./Primitives";

const ICONS = [ClipboardCheck, CreditCard, TrendingUp, ShieldCheck, FileText, BarChart3];
const TONE = {
  visible_now: "success",
  provider_required: "warning",
  gated: "info",
  planned: "neutral",
};

export default function BusinessReadinessPanel({ title = "Business Readiness", testid = "business-readiness-panel" }) {
  return (
    <Card hover={false} className="mb-8" data-testid={testid}>
      <div className="flex items-start justify-between gap-4 flex-wrap mb-5">
        <div>
          <div className="label-eyebrow mb-2">Business Proof</div>
          <h2 className="font-display text-3xl text-equine-ink leading-tight">{title}</h2>
          <p className="mt-2 text-[13px] leading-relaxed text-equine-inkMuted max-w-2xl">
            Business surfaces should separate plan fit, billing records, activation signals, portability, and public proof from provider-backed launch claims.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
        {BUSINESS_PROOF_SIGNALS.map((item, index) => {
          const Icon = ICONS[index % ICONS.length];
          return (
            <div key={item.id} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4 min-h-[168px]" data-testid={`business-proof-${item.id}`}>
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-2 min-w-0">
                  <Icon className="w-3.5 h-3.5 text-equine-brass flex-shrink-0" strokeWidth={1.7} />
                  <div className="text-equine-ink text-[14px] truncate">{item.label}</div>
                </div>
                <StatusPill tone={TONE[item.status] || "neutral"}>{BUSINESS_STATUS[item.status]}</StatusPill>
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
