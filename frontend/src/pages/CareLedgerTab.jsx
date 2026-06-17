/**
 * CareLedgerTab — Phase HorseOps-1A read-only Care Ledger surface.
 *
 * Compact UI label: "Care Ledger" (billing-safe).
 * Backend: GET /api/horse-ledger/{horse_id}
 *
 * READ-ONLY in 1-A. No edit affordances, no drawers. Hidden sections
 * (owner view) render a neutral "Operational — staff only" placeholder
 * instead of being silently omitted, so the layout remains predictable.
 */
import React, { useEffect, useState } from "react";
import { api } from "../lib/api";

const SECTION_LABELS = {
  feeding:           "Feeding",
  hay_access:        "Hay & Hay Nets",
  stall_bedding:     "Stall & Bedding",
  turnout:           "Turnout",
  handling_behavior: "Behavior & Handling",
  riding_training:   "Riding & Training",
};

const KV = ({ label, value }) => (
  <div className="py-1.5 flex gap-3 text-[13px]">
    <div className="text-equine-platinum/55 min-w-[140px]">{label}</div>
    <div className="text-equine-silver">{value ?? "—"}</div>
  </div>
);

const HiddenPlaceholder = ({ label }) => (
  <div
    data-testid={`horse-ledger-empty-${label}`}
    className="text-[12.5px] text-equine-platinum/45 italic py-2"
  >
    Operational — staff only.
  </div>
);

const SectionShell = ({ id, title, children }) => (
  <section
    data-testid={`horse-ledger-section-${id}`}
    className="rounded-lg border border-equine-silver/10 bg-equine-black/40 p-4"
  >
    <div className="label-eyebrow mb-2">{title}</div>
    {children}
  </section>
);

const StructuredLegacyEnvelope = ({ envelope, renderStructured }) => {
  if (envelope === null || envelope === undefined) return <KV label="Status" value="No data" />;
  const { structured, legacy } = envelope;
  return (
    <>
      {structured && renderStructured ? renderStructured(structured) : null}
      {legacy && (
        <div className="mt-3 pt-3 border-t border-equine-silver/10">
          <div className="text-[10.5px] tracking-[0.22em] uppercase text-equine-platinum/40 mb-1">
            Legacy value (from existing record)
          </div>
          <div className="text-[13px] text-equine-silver/70 whitespace-pre-wrap">
            {Array.isArray(legacy) ? legacy.join(", ") : String(legacy)}
          </div>
        </div>
      )}
      {!structured && !legacy && <KV label="Status" value="No data" />}
    </>
  );
};

// Hoisted structured-section renderers — declared outside the component
// so React reconciliation stays stable on every parent render.
const renderFeedingStructured = (s) => (
  <>
    {s.grain_feed_type && <KV label="Grain / feed" value={s.grain_feed_type} />}
    {s.amount_value != null && <KV label="Amount" value={`${s.amount_value} ${s.amount_unit || ""}`} />}
    {Array.isArray(s.supplements) && s.supplements.length > 0 && (
      <KV label="Supplements" value={s.supplements.map((x) => x?.name || x).join(", ")} />
    )}
  </>
);

const renderTurnoutStructured = (s) => (
  <>
    {s.pasture_paddock_assignment && <KV label="Paddock" value={s.pasture_paddock_assignment} />}
    {s.turnout_group && <KV label="Group" value={s.turnout_group} />}
  </>
);

const renderRidingTrainingStructured = (s) => (
  <>
    {s.discipline && <KV label="Discipline" value={s.discipline} />}
    {s.current_level && <KV label="Level" value={s.current_level} />}
    {s.goals_short_term && <KV label="Short-term goals" value={s.goals_short_term} />}
  </>
);

export default function CareLedgerTab({ horseId }) {
  const [data, setData] = useState(null);
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    api.get(`/horse-ledger/${horseId}`)
      .then((r) => { if (!cancelled) { setData(r.data); setErr(null); } })
      .catch((e) => { if (!cancelled) setErr(e?.response?.data?.detail || "Could not load Care Ledger."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [horseId]);

  if (loading) return <div className="text-equine-platinum/60" data-testid="horse-ledger-loading">Loading Care Ledger…</div>;
  if (err) return <div className="text-equine-platinum/70" data-testid="horse-ledger-error">{err}</div>;
  if (!data) return null;

  const isOwner = data.view === "owner";

  return (
    <div data-testid="horse-ledger-tab" className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <div className="label-eyebrow">Care Ledger</div>
          <div className="text-[12.5px] text-equine-platinum/55 mt-1">
            {isOwner
              ? "Owner view — operational details visible to your barn's staff only."
              : "Staff view — full operational profile."}
          </div>
        </div>
      </div>

      {/* Feeding */}
      <SectionShell id="feeding" title={SECTION_LABELS.feeding}>
        <StructuredLegacyEnvelope envelope={data.feeding} renderStructured={renderFeedingStructured} />
      </SectionShell>

      {/* Hay & Hay Nets */}
      <SectionShell id="hay_access" title={SECTION_LABELS.hay_access}>
        {data.hay_access?.structured ? (
          <>
            <KV label="Access type" value={data.hay_access.structured.access_type} />
            <KV label="Hay type" value={data.hay_access.structured.hay_type} />
            <KV label="Per feeding" value={data.hay_access.structured.quantity_per_feeding} />
            {!isOwner && Array.isArray(data.hay_access.structured.hay_nets) && (
              <KV label="Hay nets" value={`${data.hay_access.structured.hay_nets.length} configured`} />
            )}
          </>
        ) : (
          <KV label="Status" value="No structured hay profile yet (lands in 1-B)." />
        )}
      </SectionShell>

      {/* Stall & Bedding — owners never see this section */}
      <SectionShell id="stall_bedding" title={SECTION_LABELS.stall_bedding}>
        {isOwner ? (
          <HiddenPlaceholder label="stall_bedding" />
        ) : data.stall_bedding?.structured ? (
          <>
            <KV label="Stall" value={data.stall_bedding.structured.stall_number} />
            <KV label="Bedding type" value={data.stall_bedding.structured.bedding_type} />
            <KV label="Depth" value={data.stall_bedding.structured.bedding_depth_preference} />
            <KV label="Banked" value={data.stall_bedding.structured.banked_bedding_required ? "Required" : "—"} />
          </>
        ) : (
          <KV label="Status" value="No structured bedding profile yet (lands in 1-B)." />
        )}
      </SectionShell>

      {/* Turnout */}
      <SectionShell id="turnout" title={SECTION_LABELS.turnout}>
        <StructuredLegacyEnvelope envelope={data.turnout} renderStructured={renderTurnoutStructured} />
      </SectionShell>

      {/* Handling & Behavior — owners never see this section */}
      <SectionShell id="handling_behavior" title={SECTION_LABELS.handling_behavior}>
        {isOwner ? (
          <HiddenPlaceholder label="handling_behavior" />
        ) : (
          <StructuredLegacyEnvelope envelope={data.handling_behavior} />
        )}
      </SectionShell>

      {/* Riding & Training */}
      <SectionShell id="riding_training" title={SECTION_LABELS.riding_training}>
        <StructuredLegacyEnvelope envelope={data.riding_training} renderStructured={renderRidingTrainingStructured} />
      </SectionShell>

      {/* Service providers */}
      <SectionShell id="service_providers" title="Service providers">
        {Array.isArray(data.service_providers) && data.service_providers.length === 0 ? (
          <KV label="Status" value="No providers assigned yet (lands in 1-B)." />
        ) : (
          <div className="text-[13px] text-equine-silver/80">
            {data.service_providers.length} provider assignment(s)
          </div>
        )}
      </SectionShell>

      {/* Daily checks / alerts / audit — empty in 1-A */}
      <SectionShell id="daily_checks" title="Daily checks">
        <KV label="Status" value="Daily checks land in HorseOps-1C." />
      </SectionShell>
      <SectionShell id="alerts" title="Alerts">
        <KV label="Status" value="Alerts land in HorseOps-1D." />
      </SectionShell>
    </div>
  );
}
