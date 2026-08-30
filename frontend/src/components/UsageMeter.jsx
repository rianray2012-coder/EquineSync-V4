// Phase 15.F — Usage meter component.
// ---------------------------------------------------------------------------
// Renders horses / users usage in two variants:
//
//   • inline  — slim 1-line indicator; great for page headers above a CTA
//   • card    — full card with progress bar; great inside modals/forms
//
// Strict rules:
//   • Never blocks any CTA. Soft-warn only.
//   • Concierge-warm threshold copy at 80% / 100%.
//   • Hidden when limit is null / unlimited / usage data is missing.
//   • Uses only approved EquineSync/status tokens.
//   • Storage meter intentionally omitted — backend `storage_gb.used` is
//     hardcoded to 0 today, so showing it would mislead (decision #1a).
import React from "react";
import { Sparkles, AlertTriangle } from "lucide-react";

const KIND_LABEL = {
  horses: "Horses",
  users:  "Staff users",
};

function _resolveMeter(usage, kind) {
  const entry = usage?.usage?.[kind];
  if (!entry) return null;
  const limit = entry.limit;
  if (limit == null || !Number.isFinite(limit) || limit <= 0) return null;
  const used = Number(entry.used) || 0;
  const pct = Math.min(2, used / limit); // cap at 200% for layout sanity
  let tone, ringClass, barClass;
  if (used >= limit) {
    tone = "clay"; ringClass = "border-equine-clay/40 bg-equine-clay/8"; barClass = "bg-equine-clay";
  } else if (pct >= 0.8) {
    tone = "amber"; ringClass = "border-equine-amber/40 bg-equine-amber/8"; barClass = "bg-equine-amber";
  } else {
    tone = "sage"; ringClass = "border-equine-lilac/30 bg-equine-lilac/8"; barClass = "bg-equine-sage";
  }
  return { used, limit, pct, tone, ringClass, barClass };
}

// Concierge-warm copy per decision #2a.
function _thresholdCopy(kind, used, limit) {
  const noun = kind === "horses" ? "horses" : "staff seats";
  if (used >= limit) {
    return `You're over your plan limit on ${noun}. Upgrading takes 60 seconds.`;
  }
  return `Approaching plan capacity on ${noun} — consider upgrading to keep room to grow.`;
}

export function UsageMeter({ usage, kind, variant = "inline", className = "" }) {
  const m = _resolveMeter(usage, kind);
  if (!m) return null;
  const showWarn = m.pct >= 0.8;

  if (variant === "inline") {
    return (
      <div
        className={`inline-flex items-center gap-2 text-[11.5px] tracking-wide px-3 py-1.5 rounded-full border ${m.ringClass} ${className}`}
        data-testid={`usage-meter-${kind}-inline`}
        title={showWarn ? _thresholdCopy(kind, m.used, m.limit) : `${m.used} of ${m.limit} ${KIND_LABEL[kind]?.toLowerCase()}`}
      >
        {m.tone === "clay" ? (
          <AlertTriangle className="w-3 h-3 text-equine-clay" />
        ) : m.tone === "amber" ? (
          <AlertTriangle className="w-3 h-3 text-equine-amber" />
        ) : (
          <Sparkles className="w-3 h-3 text-equine-lilacDeep" />
        )}
        <span className="text-equine-inkMuted">
          <span className="text-equine-ink font-medium" data-testid={`usage-meter-${kind}-count`}>
            {m.used}
          </span>
          <span className="text-equine-inkSoft"> / {m.limit} </span>
          {KIND_LABEL[kind]?.toLowerCase()}
        </span>
      </div>
    );
  }

  // card variant
  return (
    <div
      className={`rounded-xl border ${m.ringClass} p-4 ${className}`}
      data-testid={`usage-meter-${kind}-card`}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="label-eyebrow">{KIND_LABEL[kind] || kind}</div>
        <div className="text-[12px] text-equine-inkMuted">
          <span className="text-equine-ink font-medium" data-testid={`usage-meter-${kind}-count`}>{m.used}</span>
          <span className="text-equine-inkSoft"> / {m.limit}</span>
        </div>
      </div>
      <div className="h-1.5 rounded-full bg-equine-soft overflow-hidden">
        <div
          className={`h-full ${m.barClass} transition-all`}
          style={{ width: `${Math.min(1, m.pct) * 100}%` }}
          data-testid={`usage-meter-${kind}-bar`}
        />
      </div>
      {showWarn && (
        <div
          className={`mt-2 text-[11.5px] leading-snug ${m.tone === "clay" ? "text-equine-clay" : "text-equine-amber"}`}
          data-testid={`usage-meter-${kind}-warn`}
        >
          {_thresholdCopy(kind, m.used, m.limit)}
        </div>
      )}
    </div>
  );
}
