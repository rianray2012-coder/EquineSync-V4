/**
 * AdminFacilityDrawer — facility detail + Admin-4b mutations.
 *
 * Read surface unchanged. Admin-4b adds three mutations gated by
 * `me.capabilities.facilities_write` (super_admin / platform_admin only):
 *
 *   1. PATCH /admin/portal/facilities/{barn_id}
 *      — whitelisted profile edit (name, address, phone, contact_email,
 *        timezone, notes).
 *   2. POST  /admin/portal/facilities/{barn_id}/disable
 *      — confirmation modal w/ enum reason category + optional details.
 *   3. POST  /admin/portal/facilities/{barn_id}/reenable
 *      — confirmation modal.
 *
 * Color discipline: disabled state uses the approved EquineSync lilac
 * (`equinesync-lilac`); no red / orange / yellow drift.
 */
import React, { useEffect, useState } from "react";
import {
  X, Building2, CreditCard, History, Heart, Pencil, Power, RotateCcw,
} from "lucide-react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";

const REASON_CATEGORIES = [
  { value: "billing_dispute",  label: "Billing dispute" },
  { value: "customer_request", label: "Customer request" },
  { value: "abuse",            label: "Abuse / TOS violation" },
  { value: "security",         label: "Security concern" },
  { value: "other",            label: "Other" },
];

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

const formatMrr = (cents) => {
  if (cents == null) return "—";
  const d = Math.floor(Number(cents) / 100);
  return `$${d.toLocaleString("en-US")}`;
};

const Tile = ({ label, value, testid }) => (
  <div
    data-testid={testid}
    className="rounded-lg border border-equinesync-graphite/10 bg-equinesync-frost px-3 py-2.5"
  >
    <div className="text-[9.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55">{label}</div>
    <div className="mt-1 font-display text-lg text-equinesync-graphite font-light leading-tight">
      {value ?? "—"}
    </div>
  </div>
);

const DisabledBadge = () => (
  <span
    data-testid="facility-disabled-badge"
    className="inline-flex items-center gap-1.5 rounded-full bg-equinesync-lilac/30 px-2.5 py-0.5 text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/80 border border-equinesync-lilac/40"
  >
    <span className="w-1.5 h-1.5 rounded-full bg-equinesync-lilac" />
    Disabled
  </span>
);

// ----------------------------------------------------------------------
// Edit form — whitelisted fields only.
// ----------------------------------------------------------------------
function FacilityEditForm({ barn, onCancel, onSaved, onError }) {
  const [form, setForm] = useState({
    name:          barn?.name          || "",
    address:       barn?.address       || "",
    phone:         barn?.phone         || "",
    contact_email: barn?.contact_email || "",
    timezone:      barn?.timezone      || "",
    notes:         barn?.notes         || "",
  });
  const [saving, setSaving] = useState(false);
  const [localErr, setLocalErr] = useState(null);

  const change = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const submit = async () => {
    setSaving(true);
    setLocalErr(null);
    try {
      // Send ONLY changed fields so the server's "Empty body" guard is
      // never tripped by re-saving an unchanged form.
      const body = {};
      for (const k of ["name", "address", "phone", "contact_email", "timezone", "notes"]) {
        if ((form[k] || "") !== (barn?.[k] || "")) body[k] = form[k];
      }
      if (Object.keys(body).length === 0) {
        setLocalErr("No changes to save.");
        setSaving(false);
        return;
      }
      const r = await api.patch(`/admin/portal/facilities/${barn.id}`, body);
      onSaved(r.data?.barn || null);
    } catch (e) {
      const detail = e?.response?.data?.detail || "Could not save changes.";
      setLocalErr(detail);
      onError?.(detail);
    } finally {
      setSaving(false);
    }
  };

  const labelCls = "block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1";
  const inputCls = "w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px] focus:outline-none focus:border-equinesync-slate";

  return (
    <div className="space-y-3" data-testid="facility-edit-drawer">
      <div>
        <label className={labelCls} htmlFor="facility-field-name">Name</label>
        <input id="facility-field-name" data-testid="facility-field-name"
               className={inputCls} value={form.name} onChange={change("name")} />
      </div>
      <div>
        <label className={labelCls} htmlFor="facility-field-address">Address</label>
        <input id="facility-field-address" data-testid="facility-field-address"
               className={inputCls} value={form.address} onChange={change("address")} />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className={labelCls} htmlFor="facility-field-phone">Phone</label>
          <input id="facility-field-phone" data-testid="facility-field-phone"
                 className={inputCls} value={form.phone} onChange={change("phone")} />
        </div>
        <div>
          <label className={labelCls} htmlFor="facility-field-timezone">Timezone (IANA)</label>
          <input id="facility-field-timezone" data-testid="facility-field-timezone"
                 className={inputCls} value={form.timezone} onChange={change("timezone")} placeholder="America/New_York" />
        </div>
      </div>
      <div>
        <label className={labelCls} htmlFor="facility-field-contact_email">Contact email</label>
        <input id="facility-field-contact_email" data-testid="facility-field-contact_email"
               className={inputCls} type="email" value={form.contact_email} onChange={change("contact_email")} />
      </div>
      <div>
        <label className={labelCls} htmlFor="facility-field-notes">Notes</label>
        <textarea id="facility-field-notes" data-testid="facility-field-notes"
                  rows={3} className={`${inputCls} resize-y`} value={form.notes} onChange={change("notes")} />
      </div>
      {localErr && (
        <div className="text-[12.5px] text-equinesync-graphite/75 bg-equinesync-frost border border-equinesync-graphite/15 rounded-lg p-2.5"
             data-testid="facility-edit-error">{localErr}</div>
      )}
      <div className="flex gap-2 pt-1">
        <button type="button"
                data-testid="facility-edit-save-btn"
                disabled={saving}
                onClick={submit}
                className="px-4 py-2 rounded-lg bg-equinesync-graphite text-equinesync-frost text-[12.5px] tracking-[0.18em] uppercase disabled:opacity-50">
          {saving ? "Saving…" : "Save changes"}
        </button>
        <button type="button"
                data-testid="facility-edit-cancel-btn"
                onClick={onCancel}
                disabled={saving}
                className="px-4 py-2 rounded-lg border border-equinesync-graphite/15 text-equinesync-graphite text-[12.5px] tracking-[0.18em] uppercase">
          Cancel
        </button>
      </div>
    </div>
  );
}

// ----------------------------------------------------------------------
// Disable / Re-enable confirmation dialogs (inline overlay).
// ----------------------------------------------------------------------
function ConfirmDisable({ barnId, onCancel, onDone }) {
  const [category, setCategory] = useState("");
  const [details, setDetails] = useState("");
  const [busy, setBusy] = useState(false);
  const [localErr, setLocalErr] = useState(null);

  const submit = async () => {
    if (!category) { setLocalErr("Choose a reason category."); return; }
    setBusy(true);
    setLocalErr(null);
    try {
      await api.post(`/admin/portal/facilities/${barnId}/disable`, {
        reason_category: category,
        ...(details ? { reason_details: details } : {}),
      });
      onDone();
    } catch (e) {
      setLocalErr(e?.response?.data?.detail || "Could not disable.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-equinesync-graphite/50 flex items-center justify-center p-6"
         data-testid="facility-disable-dialog">
      <div className="bg-white rounded-xl border border-equinesync-graphite/10 w-full max-w-md p-5">
        <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">Confirm soft-disable</div>
        <h3 className="font-display text-xl text-equinesync-graphite font-light mt-1.5">
          Disable this facility?
        </h3>
        <p className="mt-2 text-[12.5px] text-equinesync-graphite/70">
          Members of this facility will lose access to product routes immediately.
          Subscription, billing, and invoice records are not deleted; this is
          a reversible soft-disable.
        </p>
        <div className="mt-4 space-y-3">
          <div>
            <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">
              Reason category
            </label>
            <select
              data-testid="facility-disable-reason-category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
            >
              <option value="">Select a reason…</option>
              {REASON_CATEGORIES.map((r) => (
                <option key={r.value} value={r.value}>{r.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">
              Details <span className="text-equinesync-graphite/40">(optional, internal-only, max 200)</span>
            </label>
            <textarea
              data-testid="facility-disable-reason-details"
              rows={2}
              maxLength={200}
              value={details}
              onChange={(e) => setDetails(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px] resize-y"
            />
          </div>
        </div>
        {localErr && (
          <div className="mt-3 text-[12.5px] text-equinesync-graphite/75 bg-equinesync-frost border border-equinesync-graphite/15 rounded-lg p-2.5"
               data-testid="facility-disable-error">{localErr}</div>
        )}
        <div className="mt-5 flex gap-2 justify-end">
          <button type="button"
                  data-testid="facility-disable-cancel-btn"
                  disabled={busy}
                  onClick={onCancel}
                  className="px-4 py-2 rounded-lg border border-equinesync-graphite/15 text-equinesync-graphite text-[12.5px] tracking-[0.18em] uppercase">
            Cancel
          </button>
          <button type="button"
                  data-testid="facility-disable-confirm-btn"
                  disabled={busy}
                  onClick={submit}
                  className="px-4 py-2 rounded-lg bg-equinesync-graphite text-equinesync-frost text-[12.5px] tracking-[0.18em] uppercase disabled:opacity-50">
            {busy ? "Disabling…" : "Disable facility"}
          </button>
        </div>
      </div>
    </div>
  );
}

function ConfirmReenable({ barnId, onCancel, onDone }) {
  const [busy, setBusy] = useState(false);
  const [localErr, setLocalErr] = useState(null);

  const submit = async () => {
    setBusy(true);
    setLocalErr(null);
    try {
      await api.post(`/admin/portal/facilities/${barnId}/reenable`);
      onDone();
    } catch (e) {
      setLocalErr(e?.response?.data?.detail || "Could not re-enable.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-equinesync-graphite/50 flex items-center justify-center p-6"
         data-testid="facility-reenable-dialog">
      <div className="bg-white rounded-xl border border-equinesync-graphite/10 w-full max-w-md p-5">
        <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">Confirm re-enable</div>
        <h3 className="font-display text-xl text-equinesync-graphite font-light mt-1.5">
          Re-enable this facility?
        </h3>
        <p className="mt-2 text-[12.5px] text-equinesync-graphite/70">
          Members will regain access to all product routes immediately.
          Historical disabled-at / disabled-by records are preserved for audit.
        </p>
        {localErr && (
          <div className="mt-3 text-[12.5px] text-equinesync-graphite/75 bg-equinesync-frost border border-equinesync-graphite/15 rounded-lg p-2.5"
               data-testid="facility-reenable-error">{localErr}</div>
        )}
        <div className="mt-5 flex gap-2 justify-end">
          <button type="button"
                  data-testid="facility-reenable-cancel-btn"
                  disabled={busy}
                  onClick={onCancel}
                  className="px-4 py-2 rounded-lg border border-equinesync-graphite/15 text-equinesync-graphite text-[12.5px] tracking-[0.18em] uppercase">
            Cancel
          </button>
          <button type="button"
                  data-testid="facility-reenable-confirm-btn"
                  disabled={busy}
                  onClick={submit}
                  className="px-4 py-2 rounded-lg bg-equinesync-graphite text-equinesync-frost text-[12.5px] tracking-[0.18em] uppercase disabled:opacity-50">
            {busy ? "Re-enabling…" : "Re-enable facility"}
          </button>
        </div>
      </div>
    </div>
  );
}


export default function AdminFacilityDrawer({ barnId, open, onClose, onMutated }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [canWrite, setCanWrite] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [showDisable, setShowDisable] = useState(false);
  const [showReenable, setShowReenable] = useState(false);
  // bumping `reloadTick` re-fetches the facility detail after a mutation.
  const [reloadTick, setReloadTick] = useState(0);

  useEffect(() => {
    if (!open || !barnId) return;
    let cancelled = false;
    // All state writes happen inside async callbacks (SWR-style):
    // previous data stays on screen until the new payload lands.
    // Matches the existing AdminDashboard pattern; satisfies
    // `react-hooks/set-state-in-effect`.
    Promise.all([
      api.get(`/admin/portal/facilities/${barnId}`),
      api.get("/admin/portal/me").catch(() => null),
    ]).then(([detail, me]) => {
      if (cancelled) return;
      setData(detail.data);
      setErr(null);
      setCanWrite(Boolean(me?.data?.capabilities?.facilities_write));
    }).catch((e) => {
      if (!cancelled) setErr(e?.response?.data?.detail || "Could not load facility.");
    }).finally(() => {
      if (!cancelled) setLoading(false);
    });
    return () => { cancelled = true; };
  }, [open, barnId, reloadTick]);

  if (!open) return null;
  const b = data?.barn;
  const sub = data?.subscription_summary;
  const usage = data?.usage || {};
  const isDisabled = (b?.status || "").toLowerCase() === "disabled";

  const afterMutation = () => {
    setEditMode(false);
    setShowDisable(false);
    setShowReenable(false);
    setReloadTick((t) => t + 1);
    onMutated?.();
  };

  return (
    <div className="fixed inset-0 z-40 flex" data-testid="admin-facility-drawer">
      <div className="flex-1 bg-equinesync-graphite/40" onClick={onClose} />
      <aside className="w-full max-w-xl bg-white border-l border-equinesync-graphite/10 overflow-y-auto">
        <header className="sticky top-0 z-10 bg-white border-b border-equinesync-graphite/10 px-5 py-4 flex items-start justify-between">
          <div className="min-w-0">
            <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              Facility detail
            </div>
            <div className="mt-0.5 font-display text-lg text-equinesync-graphite font-light truncate flex items-center gap-2">
              {b?.name || b?.id || "—"}
              {isDisabled && <DisabledBadge />}
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="text-equinesync-graphite/40 hover:text-equinesync-graphite"
            data-testid="admin-facility-drawer-close"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </header>

        <div className="p-5 space-y-5">
          {loading && (
            <div className="space-y-3" data-testid="admin-facility-drawer-loading">
              {[0,1,2].map((i) => <div key={i} className="h-16 bg-equinesync-graphite/5 rounded animate-pulse" />)}
            </div>
          )}
          {err && <div className="text-[13px] text-equinesync-graphite/70" data-testid="admin-facility-drawer-error">{err}</div>}

          {b && (
            <>
              {/* Profile / edit */}
              <section data-testid="admin-facility-drawer-profile">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55">
                    <Building2 className="w-3 h-3" />Profile
                  </div>
                  {canWrite && !editMode && (
                    <button
                      type="button"
                      onClick={() => setEditMode(true)}
                      data-testid="facility-edit-btn"
                      className="inline-flex items-center gap-1 text-[11.5px] tracking-[0.16em] uppercase text-equinesync-graphite/70 hover:text-equinesync-graphite border border-equinesync-graphite/15 rounded-lg px-2.5 py-1"
                    >
                      <Pencil className="w-3 h-3" /> Edit
                    </button>
                  )}
                </div>

                {!editMode ? (
                  <div className="rounded-lg bg-equinesync-frost p-3 text-[13px] text-equinesync-graphite space-y-1">
                    <div><span className="text-equinesync-graphite/55">ID:</span> {b.id}</div>
                    {b.contact_email && <div><span className="text-equinesync-graphite/55">Contact:</span> {b.contact_email}</div>}
                    {b.phone && <div><span className="text-equinesync-graphite/55">Phone:</span> {b.phone}</div>}
                    {b.address && <div><span className="text-equinesync-graphite/55">Address:</span> {b.address}</div>}
                    {b.timezone && <div><span className="text-equinesync-graphite/55">Timezone:</span> {b.timezone}</div>}
                    {b.notes && <div><span className="text-equinesync-graphite/55">Notes:</span> {b.notes}</div>}
                    <div className="text-[11.5px] text-equinesync-graphite/55 pt-1">
                      Created {formatTs(b.created_at)}
                    </div>
                  </div>
                ) : (
                  <FacilityEditForm
                    barn={b}
                    onCancel={() => setEditMode(false)}
                    onSaved={() => afterMutation()}
                    onError={() => {}}
                  />
                )}
              </section>

              {/* Status / actions */}
              {canWrite && !editMode && (
                <section
                  data-testid="facility-status-banner"
                  className="rounded-lg border border-equinesync-graphite/10 bg-white p-3 flex items-center justify-between gap-3"
                >
                  <div className="text-[12.5px] text-equinesync-graphite/75">
                    {isDisabled
                      ? "This facility is currently disabled. Members cannot access product routes."
                      : "This facility is active. Members can access product routes."}
                  </div>
                  {isDisabled ? (
                    <button
                      type="button"
                      onClick={() => setShowReenable(true)}
                      data-testid="facility-reenable-btn"
                      className="inline-flex items-center gap-1 text-[11.5px] tracking-[0.16em] uppercase text-equinesync-graphite border border-equinesync-graphite/15 rounded-lg px-3 py-1.5"
                    >
                      <RotateCcw className="w-3 h-3" /> Re-enable
                    </button>
                  ) : (
                    <button
                      type="button"
                      onClick={() => setShowDisable(true)}
                      data-testid="facility-disable-btn"
                      className="inline-flex items-center gap-1 text-[11.5px] tracking-[0.16em] uppercase text-equinesync-graphite border border-equinesync-graphite/15 rounded-lg px-3 py-1.5"
                    >
                      <Power className="w-3 h-3" /> Disable
                    </button>
                  )}
                </section>
              )}

              <section data-testid="admin-facility-drawer-subscription">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <CreditCard className="w-3 h-3" />Subscription summary
                </div>
                {sub ? (
                  <div className="grid grid-cols-2 gap-2.5">
                    <Tile label="Plan" value={sub.plan_tier_code} testid="admin-facility-sub-plan" />
                    <Tile label="Status" value={sub.status} testid="admin-facility-sub-status" />
                    <Tile label="Cycle" value={sub.billing_cycle || "—"} testid="admin-facility-sub-cycle" />
                    <Tile label="Recurring amount" value={formatMrr(sub.amount_cents)} testid="admin-facility-sub-mrr" />
                    <Tile label="Period ends" value={sub.current_period_end ? formatTs(sub.current_period_end) : "—"} testid="admin-facility-sub-period" />
                    <Tile label="Trial ends" value={sub.trial_end ? formatTs(sub.trial_end) : "—"} testid="admin-facility-sub-trial" />
                  </div>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No subscription on file.</div>
                )}
              </section>

              <section data-testid="admin-facility-drawer-usage">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Heart className="w-3 h-3" />Usage
                </div>
                <div className="grid grid-cols-2 gap-2.5">
                  <Tile
                    label="Horses"
                    value={`${usage.horses_used ?? 0} / ${usage.horses_limit ?? "∞"}`}
                    testid="admin-facility-usage-horses"
                  />
                  <Tile
                    label="Users"
                    value={`${usage.users_used ?? 0} / ${usage.users_limit ?? "∞"}`}
                    testid="admin-facility-usage-users"
                  />
                </div>
              </section>

              <section data-testid="admin-facility-drawer-audit">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <History className="w-3 h-3" />Recent admin activity
                </div>
                {data?.recent_activity?.length ? (
                  <ul className="space-y-1.5">
                    {data.recent_activity.map((a, i) => (
                      <li key={a.id || `${a.action}-${i}`} className="text-[12px] text-equinesync-graphite/75">
                        <span className="text-equinesync-graphite font-medium">{a.action}</span>{" "}
                        · {formatTs(a.ts)}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No recent admin activity for this facility.</div>
                )}
              </section>
            </>
          )}
        </div>
      </aside>

      {showDisable && (
        <ConfirmDisable
          barnId={b?.id}
          onCancel={() => setShowDisable(false)}
          onDone={() => afterMutation()}
        />
      )}
      {showReenable && (
        <ConfirmReenable
          barnId={b?.id}
          onCancel={() => setShowReenable(false)}
          onDone={() => afterMutation()}
        />
      )}
    </div>
  );
}
