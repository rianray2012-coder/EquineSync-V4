/**
 * CareLedgerTab — Phase HorseOps-1A/1B Care Ledger surface.
 *
 * Compact UI label: "Care Ledger" (billing-safe).
 *
 * Read:  GET /api/horse-ledger/{horse_id}
 * Write (manager only, Phase HorseOps-1B):
 *   PATCH /api/horse-ledger/{horse_id}/care-profile
 *   PUT   /api/horse-ledger/{horse_id}/owner-visibility-policy
 *   POST  /api/horse-ledger/{horse_id}/equipment
 *   PATCH /api/horse-ledger/{horse_id}/equipment/{equipment_id}
 *   POST  /api/horse-ledger/{horse_id}/service-providers
 *   POST  /api/horse-ledger/{horse_id}/provider-assignments
 *   PATCH /api/horse-ledger/{horse_id}/provider-assignments/{assignment_id}
 *
 * Privacy stays backend-authoritative — the UI never decides what the
 * owner can see. We only show edit affordances when the current user's
 * role is `admin` or `barn_manager`. Owners never see edit controls;
 * the read view is unchanged from 1-A.
 */
import React, { useEffect, useState } from "react";
import { api } from "../lib/api";
import { useAuth } from "../context/AuthContext";

const SECTION_LABELS = {
  feeding:           "Feeding",
  hay_access:        "Hay & Hay Nets",
  stall_bedding:     "Stall & Bedding",
  turnout:           "Turnout",
  handling_behavior: "Behavior & Handling",
  riding_training:   "Riding & Training",
};

const MUTATOR_ROLES = new Set(["admin", "barn_manager"]);

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

const EditButton = ({ section, onClick }) => (
  <button
    type="button"
    onClick={onClick}
    data-testid={`horse-ledger-edit-${section}`}
    className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/60 hover:text-equine-silver border border-equine-silver/15 px-2.5 py-1 rounded transition-colors"
  >
    Edit
  </button>
);

const SectionShell = ({ id, title, canEdit, onEdit, children }) => (
  <section
    data-testid={`horse-ledger-section-${id}`}
    className="rounded-lg border border-equine-silver/10 bg-equine-black/40 p-4"
  >
    <div className="flex items-center justify-between mb-2">
      <div className="label-eyebrow">{title}</div>
      {canEdit && onEdit ? <EditButton section={id} onClick={onEdit} /> : null}
    </div>
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

// ---------------------------------------------------------------------
// Drawer primitive — right-side slide-in. Matches QuickAddSheet vocab
// (max-w-md, ESC close, backdrop click close, sticky header + footer).
// ---------------------------------------------------------------------
const Drawer = ({ open, title, eyebrow, onClose, onSave, saving, error, children, saveLabel = "Save" }) => {
  useEffect(() => {
    if (!open) return undefined;
    const onKey = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex" data-testid="horse-ledger-drawer">
      <div
        className="flex-1 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
        data-testid="horse-ledger-drawer-backdrop"
      />
      <div className="w-full max-w-md bg-equine-black border-l border-equine-silver/15 shadow-2xl flex flex-col">
        <header className="px-5 py-4 border-b border-equine-silver/10 sticky top-0 bg-equine-black z-10">
          <div className="label-eyebrow text-[10.5px] text-equine-platinum/55">{eyebrow}</div>
          <div className="text-[18px] font-serif text-equine-silver mt-1">{title}</div>
        </header>
        <form
          className="flex-1 overflow-y-auto px-5 py-4 space-y-3"
          onSubmit={(e) => { e.preventDefault(); onSave(); }}
          data-testid="horse-ledger-drawer-form"
        >
          {children}
          {error ? (
            <div
              className="text-[12.5px] text-rose-300/90 border border-rose-400/30 bg-rose-400/5 px-3 py-2 rounded"
              data-testid="horse-ledger-drawer-error"
            >
              {error}
            </div>
          ) : null}
          {/* hidden submit so Enter works */}
          <button type="submit" hidden />
        </form>
        <footer className="px-5 py-3 border-t border-equine-silver/10 flex justify-end gap-2 sticky bottom-0 bg-equine-black">
          <button
            type="button"
            onClick={onClose}
            disabled={saving}
            data-testid="horse-ledger-drawer-cancel"
            className="text-[12px] tracking-[0.18em] uppercase text-equine-platinum/55 px-3 py-2 hover:text-equine-silver"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={onSave}
            disabled={saving}
            data-testid="horse-ledger-drawer-save"
            className="text-[12px] tracking-[0.18em] uppercase bg-equine-silver/15 hover:bg-equine-silver/25 text-equine-silver border border-equine-silver/25 px-4 py-2 rounded disabled:opacity-40"
          >
            {saving ? "Saving…" : saveLabel}
          </button>
        </footer>
      </div>
    </div>
  );
};

const Field = ({ label, name, value, onChange, type = "text", placeholder, testid }) => (
  <label className="block">
    <span className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 block mb-1">{label}</span>
    <input
      type={type}
      value={value ?? ""}
      placeholder={placeholder}
      onChange={(e) => onChange(name, type === "number" ? (e.target.value === "" ? "" : Number(e.target.value)) : e.target.value)}
      data-testid={testid}
      className="w-full bg-equine-black/60 border border-equine-silver/15 rounded px-3 py-2 text-[13px] text-equine-silver focus:border-equine-silver/35 outline-none"
    />
  </label>
);

const TextArea = ({ label, name, value, onChange, placeholder, testid, rows = 3 }) => (
  <label className="block">
    <span className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 block mb-1">{label}</span>
    <textarea
      rows={rows}
      value={value ?? ""}
      placeholder={placeholder}
      onChange={(e) => onChange(name, e.target.value)}
      data-testid={testid}
      className="w-full bg-equine-black/60 border border-equine-silver/15 rounded px-3 py-2 text-[13px] text-equine-silver focus:border-equine-silver/35 outline-none resize-y"
    />
  </label>
);

const Select = ({ label, name, value, onChange, options, testid }) => (
  <label className="block">
    <span className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 block mb-1">{label}</span>
    <select
      value={value ?? ""}
      onChange={(e) => onChange(name, e.target.value)}
      data-testid={testid}
      className="w-full bg-equine-black/60 border border-equine-silver/15 rounded px-3 py-2 text-[13px] text-equine-silver focus:border-equine-silver/35 outline-none"
    >
      <option value="">—</option>
      {options.map((o) => (
        <option key={o} value={o}>{o}</option>
      ))}
    </select>
  </label>
);

const Toggle = ({ label, name, value, onChange, testid }) => (
  <label className="flex items-center justify-between py-2">
    <span className="text-[13px] text-equine-silver">{label}</span>
    <button
      type="button"
      onClick={() => onChange(name, !value)}
      data-testid={testid}
      className={`w-10 h-6 rounded-full transition-colors ${value ? "bg-equine-silver/60" : "bg-equine-silver/15"}`}
    >
      <span className={`block w-4 h-4 rounded-full bg-equine-black mt-1 transition-transform ${value ? "translate-x-5" : "translate-x-1"}`} />
    </button>
  </label>
);

// ---------------------------------------------------------------------
// Section editors. Each one shapes the PATCH body for /care-profile.
// ---------------------------------------------------------------------
const PROVIDER_CATEGORIES = ["vet", "farrier", "body_worker", "chiropractor", "massage", "acupuncturist", "saddle_fitter", "nutritionist", "dentist", "trainer", "other"];

// Allowlist keys we expose in the visibility policy UI per section. The
// backend rejects forbidden keys; this list is purely for ergonomics.
const POLICY_KEYS = {
  feeding:         ["grain_feed_type", "amount_value", "amount_unit", "supplements"],
  hay_access:      ["access_type", "hay_type", "quantity_per_feeding"],
  turnout:         ["schedule", "pasture_paddock_assignment", "turnout_group"],
  riding_training: ["discipline", "current_level", "goals_short_term", "goals_long_term", "competition_goals"],
  equipment:       ["category", "label"],
};

export default function CareLedgerTab({ horseId }) {
  const { user } = useAuth();
  const role = (user?.role || "").toLowerCase();
  const canEdit = MUTATOR_ROLES.has(role);

  const [data, setData] = useState(null);
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(true);
  const [drawer, setDrawer] = useState(null); // {kind: string, ...payload}

  const refetch = () => {
    setLoading(true);
    return api.get(`/horse-ledger/${horseId}`)
      .then((r) => { setData(r.data); setErr(null); })
      .catch((e) => setErr(e?.response?.data?.detail || "Could not load Care Ledger."))
      .finally(() => setLoading(false));
  };

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

  const openDrawer = (kind, extra = {}) => setDrawer({ kind, ...extra });
  const closeDrawer = () => setDrawer(null);

  return (
    <div data-testid="horse-ledger-tab" className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <div className="label-eyebrow">Care Ledger</div>
          <div className="text-[12.5px] text-equine-platinum/55 mt-1">
            {isOwner
              ? "Owner view — operational details visible to your barn's staff only."
              : canEdit
                ? "Staff view — full operational profile. Tap Edit on any section."
                : "Staff view — full operational profile."}
          </div>
        </div>
        {canEdit && !isOwner ? (
          <button
            type="button"
            onClick={() => openDrawer("visibility_policy")}
            data-testid="horse-ledger-edit-visibility_policy"
            className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/60 hover:text-equine-silver border border-equine-silver/15 px-3 py-1.5 rounded"
          >
            Owner visibility
          </button>
        ) : null}
      </div>

      {/* Feeding */}
      <SectionShell id="feeding" title={SECTION_LABELS.feeding}
                    canEdit={canEdit && !isOwner}
                    onEdit={() => openDrawer("feeding")}>
        <StructuredLegacyEnvelope envelope={data.feeding} renderStructured={renderFeedingStructured} />
      </SectionShell>

      {/* Hay & Hay Nets */}
      <SectionShell id="hay_access" title={SECTION_LABELS.hay_access}
                    canEdit={canEdit && !isOwner}
                    onEdit={() => openDrawer("hay_access")}>
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
          <KV label="Status" value="No structured hay profile yet." />
        )}
      </SectionShell>

      {/* Stall & Bedding — owners never see this section */}
      <SectionShell id="stall_bedding" title={SECTION_LABELS.stall_bedding}
                    canEdit={canEdit && !isOwner}
                    onEdit={() => openDrawer("stall_bedding")}>
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
          <KV label="Status" value="No structured bedding profile yet." />
        )}
      </SectionShell>

      {/* Turnout */}
      <SectionShell id="turnout" title={SECTION_LABELS.turnout}
                    canEdit={canEdit && !isOwner}
                    onEdit={() => openDrawer("turnout")}>
        <StructuredLegacyEnvelope envelope={data.turnout} renderStructured={renderTurnoutStructured} />
      </SectionShell>

      {/* Handling & Behavior — owners never see this section */}
      <SectionShell id="handling_behavior" title={SECTION_LABELS.handling_behavior}
                    canEdit={canEdit && !isOwner}
                    onEdit={() => openDrawer("handling_behavior")}>
        {isOwner ? (
          <HiddenPlaceholder label="handling_behavior" />
        ) : (
          <StructuredLegacyEnvelope envelope={data.handling_behavior} />
        )}
      </SectionShell>

      {/* Riding & Training */}
      <SectionShell id="riding_training" title={SECTION_LABELS.riding_training}
                    canEdit={canEdit && !isOwner}
                    onEdit={() => openDrawer("riding_training")}>
        <StructuredLegacyEnvelope envelope={data.riding_training} renderStructured={renderRidingTrainingStructured} />
      </SectionShell>

      {/* Equipment */}
      <SectionShell id="equipment" title="Equipment"
                    canEdit={canEdit && !isOwner}
                    onEdit={() => openDrawer("equipment_new")}>
        {Array.isArray(data.equipment) && data.equipment.length > 0 ? (
          <ul className="space-y-1.5">
            {data.equipment.map((eq) => (
              <li key={eq.id} className="flex items-center justify-between text-[13px]">
                <span className="text-equine-silver">
                  {eq.category}{eq.label ? ` — ${eq.label}` : ""}
                  {eq.status && eq.status !== "active" ? (
                    <span className="ml-2 text-[10.5px] uppercase tracking-[0.18em] text-equine-platinum/45">
                      ({eq.status})
                    </span>
                  ) : null}
                </span>
                {canEdit && !isOwner ? (
                  <button
                    type="button"
                    onClick={() => openDrawer("equipment_edit", { equipment: eq })}
                    data-testid={`horse-ledger-equipment-edit-${eq.id}`}
                    className="text-[10.5px] tracking-[0.18em] uppercase text-equine-platinum/55 hover:text-equine-silver"
                  >
                    Edit
                  </button>
                ) : null}
              </li>
            ))}
          </ul>
        ) : (
          <KV label="Status" value="No equipment recorded." />
        )}
      </SectionShell>

      {/* Service providers (staff view only — owners see hidden list per backend) */}
      <SectionShell id="service_providers" title="Service providers"
                    canEdit={canEdit && !isOwner}
                    onEdit={() => openDrawer("provider_new")}>
        {Array.isArray(data.service_providers) && data.service_providers.length === 0 ? (
          <KV label="Status" value="No providers assigned yet." />
        ) : (
          <ul className="space-y-1.5">
            {(data.service_providers || []).map((sp, idx) => (
              <li key={sp.id || idx} className="text-[13px] text-equine-silver/80 flex items-center justify-between">
                <span>{sp.category}{sp.name ? ` — ${sp.name}` : ""}</span>
                {canEdit && !isOwner && sp.assignment_id ? (
                  <button
                    type="button"
                    onClick={() => openDrawer("assignment_edit", { assignment: sp })}
                    data-testid={`horse-ledger-assignment-edit-${sp.assignment_id}`}
                    className="text-[10.5px] tracking-[0.18em] uppercase text-equine-platinum/55 hover:text-equine-silver"
                  >
                    Edit
                  </button>
                ) : null}
              </li>
            ))}
          </ul>
        )}
        {canEdit && !isOwner ? (
          <button
            type="button"
            onClick={() => openDrawer("assignment_new")}
            data-testid="horse-ledger-assignment-new"
            className="mt-3 text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 hover:text-equine-silver"
          >
            + Assign provider to horse
          </button>
        ) : null}
      </SectionShell>

      {/* Daily checks / alerts — placeholders for 1-C / 1-D */}
      <SectionShell id="daily_checks" title="Daily checks">
        <KV label="Status" value="Daily checks land in HorseOps-1C." />
      </SectionShell>
      <SectionShell id="alerts" title="Alerts">
        <KV label="Status" value="Alerts land in HorseOps-1D." />
      </SectionShell>

      {drawer ? (
        <EditDrawerRouter
          drawer={drawer}
          horseId={horseId}
          data={data}
          onClose={closeDrawer}
          onSaved={() => { closeDrawer(); refetch(); }}
        />
      ) : null}
    </div>
  );
}

// ---------------------------------------------------------------------
// Drawer router — renders the right editor for the active drawer kind.
// All drawers POST/PATCH to backend; on success they refetch the tab.
// ---------------------------------------------------------------------
function EditDrawerRouter({ drawer, horseId, data, onClose, onSaved }) {
  if (drawer.kind === "feeding")
    return <CareProfileSectionDrawer section="feeding" title="Feeding" eyebrow="Edit · Care Ledger"
              horseId={horseId} initial={data.feeding?.structured} onClose={onClose} onSaved={onSaved}
              fields={[
                { name: "grain_feed_type", kind: "text", label: "Grain / feed type" },
                { name: "amount_value", kind: "number", label: "Amount" },
                { name: "amount_unit", kind: "select", label: "Amount unit", options: ["lb", "kg", "scoop", "flake"] },
                { name: "schedule", kind: "text", label: "Schedule" },
                { name: "prep_instructions", kind: "textarea", label: "Prep instructions" },
                { name: "horse_preferences", kind: "textarea", label: "Horse preferences" },
                { name: "sensitivities", kind: "textarea", label: "Sensitivities" },
                { name: "staff_only_warnings", kind: "textarea", label: "Staff-only warnings" },
              ]}
            />;

  if (drawer.kind === "hay_access")
    return <CareProfileSectionDrawer section="hay_access" title="Hay & Hay Nets" eyebrow="Edit · Care Ledger"
              horseId={horseId} initial={data.hay_access?.structured} onClose={onClose} onSaved={onSaved}
              fields={[
                { name: "access_type", kind: "select", label: "Access type", options: ["free_choice", "scheduled", "limited"] },
                { name: "hay_type", kind: "text", label: "Hay type" },
                { name: "quantity_per_feeding", kind: "text", label: "Per feeding" },
                { name: "quantity_value", kind: "number", label: "Quantity value" },
                { name: "quantity_unit", kind: "select", label: "Quantity unit", options: ["lb", "kg", "flake"] },
                { name: "source_location", kind: "text", label: "Source location" },
                { name: "allergy_restriction_notes", kind: "textarea", label: "Allergy / restriction notes" },
                { name: "slow_feeder_used", kind: "toggle", label: "Slow feeder used" },
                { name: "exception_notes", kind: "textarea", label: "Exception notes" },
              ]}
            />;

  if (drawer.kind === "stall_bedding")
    return <CareProfileSectionDrawer section="stall_bedding" title="Stall & Bedding" eyebrow="Edit · Care Ledger"
              horseId={horseId} initial={data.stall_bedding?.structured} onClose={onClose} onSaved={onSaved}
              fields={[
                { name: "stall_number", kind: "text", label: "Stall number" },
                { name: "barn_aisle_section", kind: "text", label: "Aisle / section" },
                { name: "stall_type", kind: "select", label: "Stall type", options: ["box", "tie", "mare_motel"] },
                { name: "bedding_type", kind: "select", label: "Bedding type", options: ["shavings", "straw", "pellets", "rubber_mat", "other"] },
                { name: "bedding_depth_preference", kind: "text", label: "Bedding depth" },
                { name: "banked_bedding_required", kind: "toggle", label: "Banked bedding required" },
                { name: "dust_sensitivity", kind: "toggle", label: "Dust sensitivity" },
                { name: "stall_safety_notes", kind: "textarea", label: "Stall safety notes" },
                { name: "automatic_waterer_present", kind: "toggle", label: "Automatic waterer present" },
              ]}
            />;

  if (drawer.kind === "turnout")
    return <CareProfileSectionDrawer section="turnout" title="Turnout" eyebrow="Edit · Care Ledger"
              horseId={horseId} initial={data.turnout?.structured} onClose={onClose} onSaved={onSaved}
              fields={[
                { name: "schedule", kind: "text", label: "Schedule" },
                { name: "pasture_paddock_assignment", kind: "text", label: "Paddock / pasture" },
                { name: "turnout_group", kind: "text", label: "Turnout group" },
                { name: "buddies", kind: "text", label: "Buddies (comma-sep)" },
                { name: "avoid", kind: "text", label: "Avoid (comma-sep)" },
                { name: "grass_restrictions", kind: "textarea", label: "Grass restrictions" },
                { name: "weather_rules", kind: "textarea", label: "Weather rules" },
                { name: "required_apparel", kind: "text", label: "Required apparel" },
                { name: "injury_risk_notes", kind: "textarea", label: "Injury risk notes" },
                { name: "catching_notes", kind: "textarea", label: "Catching notes" },
              ]}
            />;

  if (drawer.kind === "handling_behavior")
    return <CareProfileSectionDrawer section="handling_behavior" title="Behavior & Handling" eyebrow="Edit · Care Ledger"
              horseId={horseId} initial={data.handling_behavior?.structured} onClose={onClose} onSaved={onSaved}
              fields={[
                { name: "catching_notes", kind: "textarea", label: "Catching notes" },
                { name: "grooming_sensitivities", kind: "textarea", label: "Grooming sensitivities" },
                { name: "tacking_preferences", kind: "textarea", label: "Tacking preferences" },
                { name: "trailer_loading_notes", kind: "textarea", label: "Trailer loading notes" },
                { name: "clipping_notes", kind: "textarea", label: "Clipping notes" },
                { name: "injection_behavior", kind: "text", label: "Injection behavior" },
                { name: "farrier_behavior", kind: "text", label: "Farrier behavior" },
                { name: "vet_behavior", kind: "text", label: "Vet behavior" },
                { name: "known_risks", kind: "textarea", label: "Known risks" },
                { name: "required_staff_experience_level", kind: "select", label: "Required staff experience", options: ["novice", "intermediate", "experienced", "advanced"] },
              ]}
            />;

  if (drawer.kind === "riding_training")
    return <CareProfileSectionDrawer section="riding_training" title="Riding & Training" eyebrow="Edit · Care Ledger"
              horseId={horseId} initial={data.riding_training?.structured} onClose={onClose} onSaved={onSaved}
              fields={[
                { name: "discipline", kind: "text", label: "Discipline" },
                { name: "current_level", kind: "text", label: "Current level" },
                { name: "goals_short_term", kind: "textarea", label: "Short-term goals" },
                { name: "goals_long_term", kind: "textarea", label: "Long-term goals" },
                { name: "weekly_work_plan", kind: "textarea", label: "Weekly work plan" },
                { name: "trainer_notes", kind: "textarea", label: "Trainer notes" },
                { name: "exercise_restrictions", kind: "textarea", label: "Exercise restrictions" },
                { name: "competition_goals", kind: "textarea", label: "Competition goals" },
              ]}
            />;

  if (drawer.kind === "equipment_new" || drawer.kind === "equipment_edit")
    return <EquipmentDrawer horseId={horseId} mode={drawer.kind === "equipment_edit" ? "edit" : "new"}
              equipment={drawer.equipment} onClose={onClose} onSaved={onSaved} />;

  if (drawer.kind === "provider_new")
    return <ProviderDrawer horseId={horseId} onClose={onClose} onSaved={onSaved} />;

  if (drawer.kind === "assignment_new" || drawer.kind === "assignment_edit")
    return <AssignmentDrawer horseId={horseId} mode={drawer.kind === "assignment_edit" ? "edit" : "new"}
              assignment={drawer.assignment} onClose={onClose} onSaved={onSaved} />;

  if (drawer.kind === "visibility_policy")
    return <VisibilityPolicyDrawer horseId={horseId} onClose={onClose} onSaved={onSaved} />;

  return null;
}

// ---------------------------------------------------------------------
// Care-profile section drawer (feeding, hay_access, stall_bedding, etc.)
// Renders a field list from a config and PATCHes /care-profile.
// ---------------------------------------------------------------------
function CareProfileSectionDrawer({ section, title, eyebrow, horseId, initial, fields, onClose, onSaved }) {
  const [form, setForm] = useState(() => {
    const init = {};
    for (const f of fields) {
      if (initial && initial[f.name] !== undefined && initial[f.name] !== null) {
        init[f.name] = initial[f.name];
      } else {
        init[f.name] = f.kind === "toggle" ? false : "";
      }
    }
    return init;
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const setField = (name, value) => setForm((prev) => ({ ...prev, [name]: value }));

  const save = async () => {
    setError(null);
    // Only send non-empty fields, so we don't clobber existing data with blanks.
    const payload = {};
    for (const f of fields) {
      const v = form[f.name];
      if (f.kind === "toggle") {
        // Always include toggle if it differs from initial false/undefined
        if (initial && typeof initial[f.name] === "boolean") {
          if (v !== initial[f.name]) payload[f.name] = v;
        } else if (v === true) {
          payload[f.name] = v;
        }
      } else if (v !== "" && v !== null && v !== undefined) {
        payload[f.name] = v;
      }
    }
    if (Object.keys(payload).length === 0) {
      setError("Make a change first, then save.");
      return;
    }
    setSaving(true);
    try {
      await api.patch(`/horse-ledger/${horseId}/care-profile`, { [section]: payload });
      onSaved();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not save.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Drawer open={true} title={title} eyebrow={eyebrow} onClose={onClose}
            onSave={save} saving={saving} error={error}>
      {fields.map((f) => {
        const testid = `horse-ledger-${section}-field-${f.name}`;
        if (f.kind === "textarea") return <TextArea key={f.name} label={f.label} name={f.name} value={form[f.name]} onChange={setField} testid={testid} />;
        if (f.kind === "select")   return <Select   key={f.name} label={f.label} name={f.name} value={form[f.name]} onChange={setField} options={f.options} testid={testid} />;
        if (f.kind === "toggle")   return <Toggle   key={f.name} label={f.label} name={f.name} value={!!form[f.name]} onChange={setField} testid={testid} />;
        return <Field key={f.name} label={f.label} name={f.name} value={form[f.name]} onChange={setField} type={f.kind} testid={testid} />;
      })}
    </Drawer>
  );
}

// ---------------------------------------------------------------------
// Equipment drawer (POST new / PATCH retire)
// ---------------------------------------------------------------------
function EquipmentDrawer({ horseId, mode, equipment, onClose, onSaved }) {
  const [form, setForm] = useState(() => ({
    category: equipment?.category || "saddle",
    label:    equipment?.label    || "",
    brand:    equipment?.brand    || "",
    size:     equipment?.size     || "",
    fit_notes: equipment?.fit_notes || "",
    status:   equipment?.status   || "active",
  }));
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const setField = (name, value) => setForm((p) => ({ ...p, [name]: value }));

  const save = async () => {
    setError(null);
    setSaving(true);
    try {
      if (mode === "edit") {
        const payload = {};
        ["label", "brand", "size", "fit_notes", "status"].forEach((k) => {
          if (form[k] !== (equipment?.[k] ?? "")) payload[k] = form[k];
        });
        if (Object.keys(payload).length === 0) {
          setError("Make a change first, then save.");
          setSaving(false);
          return;
        }
        await api.patch(`/horse-ledger/${horseId}/equipment/${equipment.id}`, payload);
      } else {
        if (!form.category) { setError("category is required."); setSaving(false); return; }
        const payload = { category: form.category };
        ["label", "brand", "size", "fit_notes"].forEach((k) => {
          if (form[k]) payload[k] = form[k];
        });
        await api.post(`/horse-ledger/${horseId}/equipment`, payload);
      }
      onSaved();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not save.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Drawer open={true}
            title={mode === "edit" ? "Edit equipment" : "Add equipment"}
            eyebrow="Equipment · Care Ledger"
            onClose={onClose} onSave={save} saving={saving} error={error}>
      <Select label="Category" name="category" value={form.category} onChange={setField}
              options={["saddle", "bridle", "blanket", "boots", "halter", "bit", "girth", "other"]}
              testid="horse-ledger-equipment-field-category" />
      <Field  label="Label"    name="label"    value={form.label}    onChange={setField} testid="horse-ledger-equipment-field-label" />
      <Field  label="Brand"    name="brand"    value={form.brand}    onChange={setField} testid="horse-ledger-equipment-field-brand" />
      <Field  label="Size"     name="size"     value={form.size}     onChange={setField} testid="horse-ledger-equipment-field-size" />
      <TextArea label="Fit notes" name="fit_notes" value={form.fit_notes} onChange={setField} testid="horse-ledger-equipment-field-fit_notes" />
      {mode === "edit" ? (
        <Select label="Status" name="status" value={form.status} onChange={setField}
                options={["active", "retired"]}
                testid="horse-ledger-equipment-field-status" />
      ) : null}
    </Drawer>
  );
}

// ---------------------------------------------------------------------
// Service provider drawer (POST new). Assignment drawer below.
// ---------------------------------------------------------------------
function ProviderDrawer({ horseId, onClose, onSaved }) {
  const [form, setForm] = useState({ category: "vet", name: "", company: "", phone: "", email: "" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const setField = (n, v) => setForm((p) => ({ ...p, [n]: v }));
  const save = async () => {
    setError(null); setSaving(true);
    try {
      if (!form.category || !form.name) {
        setError("Category and name are required.");
        setSaving(false); return;
      }
      const payload = { category: form.category, name: form.name };
      ["company", "phone", "email"].forEach((k) => { if (form[k]) payload[k] = form[k]; });
      await api.post(`/horse-ledger/${horseId}/service-providers`, payload);
      onSaved();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not save.");
    } finally { setSaving(false); }
  };
  return (
    <Drawer open={true} title="Add service provider" eyebrow="Providers · Care Ledger"
            onClose={onClose} onSave={save} saving={saving} error={error}>
      <Select label="Category" name="category" value={form.category} onChange={setField}
              options={PROVIDER_CATEGORIES} testid="horse-ledger-provider-field-category" />
      <Field  label="Name"     name="name"     value={form.name}     onChange={setField} testid="horse-ledger-provider-field-name" />
      <Field  label="Company"  name="company"  value={form.company}  onChange={setField} testid="horse-ledger-provider-field-company" />
      <Field  label="Phone"    name="phone"    value={form.phone}    onChange={setField} testid="horse-ledger-provider-field-phone" />
      <Field  label="Email"    name="email"    value={form.email}    onChange={setField} type="email" testid="horse-ledger-provider-field-email" />
    </Drawer>
  );
}

function AssignmentDrawer({ horseId, mode, assignment, onClose, onSaved }) {
  const [providers, setProviders] = useState([]);
  const [form, setForm] = useState(() => ({
    provider_id:   assignment?.provider_id || "",
    category:      assignment?.category    || "vet",
    interval_days: assignment?.interval_days ?? "",
    is_primary_for_horse: !!assignment?.is_primary_for_horse,
    notes:         assignment?.notes || "",
    status:        assignment?.status || "active",
  }));
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const setField = (n, v) => setForm((p) => ({ ...p, [n]: v }));

  // Load barn providers so the manager can pick one. We just refetch
  // the ledger and use its full provider catalog approximation, falling
  // back to "type the id" if the endpoint isn't there.
  useEffect(() => {
    let cancelled = false;
    api.get(`/horse-ledger/${horseId}`).then((r) => {
      if (cancelled) return;
      const sp = Array.isArray(r.data?.service_providers) ? r.data.service_providers : [];
      setProviders(sp.filter((p) => p.id));
    }).catch(() => {});
    return () => { cancelled = true; };
  }, [horseId]);

  const save = async () => {
    setError(null); setSaving(true);
    try {
      if (mode === "edit") {
        const payload = {};
        ["category", "interval_days", "is_primary_for_horse", "notes", "status"].forEach((k) => {
          if (form[k] !== (assignment?.[k] ?? (k === "is_primary_for_horse" ? false : ""))) payload[k] = form[k];
        });
        if (Object.keys(payload).length === 0) {
          setError("Make a change first, then save."); setSaving(false); return;
        }
        await api.patch(`/horse-ledger/${horseId}/provider-assignments/${assignment.id}`, payload);
      } else {
        if (!form.provider_id) { setError("provider_id is required."); setSaving(false); return; }
        const payload = { provider_id: form.provider_id };
        if (form.category) payload.category = form.category;
        if (form.interval_days !== "" && form.interval_days !== null) payload.interval_days = Number(form.interval_days);
        if (form.is_primary_for_horse) payload.is_primary_for_horse = true;
        if (form.notes) payload.notes = form.notes;
        await api.post(`/horse-ledger/${horseId}/provider-assignments`, payload);
      }
      onSaved();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not save.");
    } finally { setSaving(false); }
  };

  return (
    <Drawer open={true}
            title={mode === "edit" ? "Edit provider assignment" : "Assign provider"}
            eyebrow="Providers · Care Ledger"
            onClose={onClose} onSave={save} saving={saving} error={error}>
      {mode === "new" ? (
        providers.length > 0 ? (
          <Select label="Provider" name="provider_id" value={form.provider_id} onChange={setField}
                  options={providers.map((p) => p.id)}
                  testid="horse-ledger-assignment-field-provider_id" />
        ) : (
          <Field label="Provider id" name="provider_id" value={form.provider_id} onChange={setField}
                 placeholder="sp_..." testid="horse-ledger-assignment-field-provider_id" />
        )
      ) : null}
      <Select label="Category" name="category" value={form.category} onChange={setField}
              options={PROVIDER_CATEGORIES} testid="horse-ledger-assignment-field-category" />
      <Field label="Interval (days)" name="interval_days" value={form.interval_days} onChange={setField}
             type="number" testid="horse-ledger-assignment-field-interval_days" />
      <Toggle label="Primary for this horse" name="is_primary_for_horse"
              value={form.is_primary_for_horse} onChange={setField}
              testid="horse-ledger-assignment-field-is_primary_for_horse" />
      <TextArea label="Notes" name="notes" value={form.notes} onChange={setField}
                testid="horse-ledger-assignment-field-notes" />
      {mode === "edit" ? (
        <Select label="Status" name="status" value={form.status} onChange={setField}
                options={["active", "archived"]}
                testid="horse-ledger-assignment-field-status" />
      ) : null}
    </Drawer>
  );
}

// ---------------------------------------------------------------------
// Owner-visibility policy drawer. Toggle which safe keys per section
// owners are allowed to see. Forbidden keys are excluded from the UI;
// the backend will reject them anyway.
// ---------------------------------------------------------------------
function VisibilityPolicyDrawer({ horseId, onClose, onSaved }) {
  const [allow, setAllow] = useState({});
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const toggleKey = (section, key) => setAllow((prev) => {
    const cur = new Set(prev[section] || []);
    if (cur.has(key)) cur.delete(key); else cur.add(key);
    return { ...prev, [section]: Array.from(cur) };
  });

  const save = async () => {
    setError(null); setSaving(true);
    try {
      const sections = {};
      for (const [section, keys] of Object.entries(allow)) {
        if (keys && keys.length > 0) sections[section] = { allowlist: keys };
      }
      if (Object.keys(sections).length === 0) {
        setError("Pick at least one key to share with the owner."); setSaving(false); return;
      }
      await api.put(`/horse-ledger/${horseId}/owner-visibility-policy`, { sections });
      onSaved();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not save.");
    } finally { setSaving(false); }
  };

  return (
    <Drawer open={true} title="Owner visibility policy"
            eyebrow="Privacy · Care Ledger"
            onClose={onClose} onSave={save} saving={saving} error={error}>
      <p className="text-[12px] text-equine-platinum/60 leading-relaxed">
        Pick the operational details this horse&apos;s owner is allowed to see.
        Staff-only sections (Stall &amp; Bedding, Behavior &amp; Handling,
        Service Providers, etc.) stay hidden regardless of this policy —
        privacy is enforced on the server.
      </p>
      {Object.entries(POLICY_KEYS).map(([section, keys]) => (
        <div key={section} className="border border-equine-silver/10 rounded p-3"
             data-testid={`horse-ledger-policy-section-${section}`}>
          <div className="label-eyebrow text-[10.5px] mb-2">{SECTION_LABELS[section] || section}</div>
          <div className="space-y-1">
            {keys.map((k) => (
              <label key={k} className="flex items-center justify-between gap-3 text-[13px] py-1 cursor-pointer">
                <span className="text-equine-silver/85">{k}</span>
                <input
                  type="checkbox"
                  checked={(allow[section] || []).includes(k)}
                  onChange={() => toggleKey(section, k)}
                  data-testid={`horse-ledger-policy-${section}-${k}`}
                  className="accent-equine-silver"
                />
              </label>
            ))}
          </div>
        </div>
      ))}
    </Drawer>
  );
}
