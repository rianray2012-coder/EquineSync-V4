/**
 * OwnerCareLedger — Phase HorseOps-1E.
 *
 * Calm, owner-facing filtered view of a horse's care ledger plus the
 * "Ask the barn" follow-up flow. Backend is authoritative on every
 * owner-safe projection; this component never decides what an owner
 * may see.
 *
 * Route: /owner/horses/:horseId  (mounted in App.js)
 */
import React, { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, fmtDate, fmtTime } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { buildHorseOpsDraftKey, clearHorseOpsDraft, loadHorseOpsDraft, saveHorseOpsDraft } from "../lib/horseOpsDrafts";

const CARE_STATUS_COPY = {
  all_clear:            { label: "All clear", message: "Your horse's care is on track today." },
  barn_reviewing:       { label: "Barn team reviewing", message: "The barn team is reviewing care for this horse." },
  follow_up_available:  { label: "Follow-up in progress", message: "Your follow-up is with the barn team." },
};

const REQUEST_TYPES = [
  { value: "question",            label: "General question" },
  { value: "care_follow_up",      label: "Care follow-up" },
  { value: "appointment_request", label: "Appointment request" },
  { value: "other",               label: "Other" },
];

const CONTACT_OPTIONS = [
  { value: "app",   label: "In-app" },
  { value: "email", label: "Email" },
  { value: "phone", label: "Phone" },
];

const STATUS_LABELS = { new: "New", in_progress: "In progress", resolved: "Resolved" };

const TRANSFER_SAFE_CATEGORIES = [
  { value: "identity_public", label: "Public identity" },
  { value: "ownership_record", label: "Ownership record" },
  { value: "care_summary", label: "Care summary" },
];

const TRANSFER_BLOCKED_CATEGORIES = [
  "Daily checks",
  "Alerts",
  "Private team notes",
  "Health documents",
  "Messages",
  "Invoices",
  "Provider data",
];

const Pill = ({ status }) => (
  <span
    data-testid={`owner-request-row-status-${status}`}
    className="text-[10px] tracking-[0.16em] uppercase px-2 py-0.5 rounded border border-equine-silver/25 text-equine-platinum/75"
  >
    {STATUS_LABELS[status] || status}
  </span>
);

const TrainingSummarySection = ({ summary }) => {
  const lessons = summary?.upcoming_lessons || [];
  const training = summary?.recent_training || [];
  const plans = summary?.active_plans || [];
  if (!lessons.length && !training.length && !plans.length) return null;

  return (
    <section
      data-testid="owner-training-summary"
      className="rounded-lg border border-equine-silver/10 bg-equine-black/40 p-4"
    >
      <div className="label-eyebrow mb-3">Training & lessons</div>
      <div className="grid gap-3">
        {lessons.map((lesson) => (
          <div key={lesson.id} data-testid={`owner-training-lesson-${lesson.id}`} className="rounded border border-equine-silver/10 bg-equine-silver/5 p-3">
            <div className="text-[13px] text-equine-silver/85">Lesson scheduled</div>
            <div className="text-[12px] text-equine-platinum/65 mt-1">
              {[lesson.start_time ? `${fmtDate(lesson.start_time)} ${fmtTime(lesson.start_time)}` : null, lesson.trainer_name, lesson.focus].filter(Boolean).join(" · ")}
            </div>
          </div>
        ))}
        {training.map((row) => (
          <div key={row.id} data-testid={`owner-training-log-${row.id}`} className="rounded border border-equine-silver/10 bg-equine-silver/5 p-3">
            <div className="text-[13px] text-equine-silver/85">
              {[row.discipline || "Training update", row.date].filter(Boolean).join(" · ")}
            </div>
            <div className="text-[12px] text-equine-platinum/65 mt-1">
              {[row.exercises, row.homework, row.rating ? `Rating ${row.rating}/10` : null].filter(Boolean).join(" · ")}
            </div>
          </div>
        ))}
        {plans.map((plan) => (
          <div key={plan.id} data-testid={`owner-training-plan-${plan.id}`} className="rounded border border-equine-silver/10 bg-equine-silver/5 p-3">
            <div className="text-[13px] text-equine-silver/85">{plan.goal || "Training plan"}</div>
            <div className="text-[12px] text-equine-platinum/65 mt-1">
              {[plan.status, plan.trainer_name].filter(Boolean).join(" · ")}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default function OwnerCareLedger() {
  const { horseId } = useParams();
  const [data, setData] = useState(null);
  const [err, setErr]   = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [transferOpen, setTransferOpen] = useState(false);

  const refetch = useCallback(() => {
    return api.get(`/horse-ledger/${horseId}/owner-summary`)
      .then((r) => { setData(r.data); setErr(null); })
      .catch((e) => setErr(e?.response?.data?.detail || "Could not load."));
  }, [horseId]);

  useEffect(() => { refetch(); }, [refetch]);

  if (err)   return <div className="p-6 text-equine-platinum/75" data-testid="owner-care-error">{err}</div>;
  if (!data) return <div className="p-6 text-equine-platinum/55" data-testid="owner-care-loading">Loading…</div>;

  const statusCopy = CARE_STATUS_COPY[data.care_status] || CARE_STATUS_COPY.all_clear;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-6" data-testid="owner-care-ledger">
      <header className="space-y-2">
        <div className="label-eyebrow">Care ledger</div>
        <h1 className="text-3xl sm:text-4xl font-serif text-equine-silver">Your horse's care</h1>
      </header>

      {/* care_status banner */}
      <section
        data-testid="owner-care-status"
        data-status={data.care_status}
        className="rounded-lg border border-equine-silver/15 bg-equine-black/40 p-5"
      >
        <div className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 mb-1">
          {statusCopy.label}
        </div>
        <div className="text-[15px] text-equine-silver/90">{statusCopy.message}</div>
      </section>

      {/* summary cards */}
      <section className="grid sm:grid-cols-2 gap-3">
        {(data.summary_cards || []).map((c) => (
          <div
            key={c.key}
            data-testid={`owner-summary-card-${c.key}`}
            className="rounded-lg border border-equine-silver/10 bg-equine-black/40 p-4"
          >
            <div className="label-eyebrow">{c.label}</div>
            <div className="text-[13px] text-equine-silver/80 mt-2">{c.message}</div>
          </div>
        ))}
      </section>

      <TrainingSummarySection summary={data.training_summary} />

      <button
        type="button"
        onClick={() => setDrawerOpen(true)}
        data-testid="owner-request-ask-button"
        className="min-h-11 w-full sm:w-auto text-[11px] tracking-[0.18em] uppercase border border-equine-silver/30 bg-equine-silver/10 hover:bg-equine-silver/20 text-equine-silver px-5 py-2.5 rounded"
      >
        Ask the barn
      </button>

      <PassportTransferPanel
        horseId={horseId}
        onOpenTransfer={() => setTransferOpen(true)}
      />

      {/* recent owner requests */}
      {(data.recent_owner_requests || []).length > 0 ? (
        <section className="rounded-lg border border-equine-silver/10 bg-equine-black/40 p-4">
          <div className="label-eyebrow mb-3">Your recent requests</div>
          <ul className="space-y-2">
            {data.recent_owner_requests.map((r) => (
              <li
                key={r.id}
                data-testid={`owner-request-row-${r.id}`}
                className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 text-[13px]"
              >
                <span className="text-equine-silver/85 break-words">{r.message}</span>
                <Pill status={r.status} />
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {drawerOpen ? (
        <OwnerRequestDrawer horseId={horseId} onClose={() => setDrawerOpen(false)} onSaved={() => { setDrawerOpen(false); refetch(); }} />
      ) : null}

      {transferOpen ? (
        <PassportTransferDrawer
          horseId={horseId}
          onClose={() => setTransferOpen(false)}
        />
      ) : null}
    </div>
  );
}

function PassportTransferPanel({ horseId, onOpenTransfer }) {
  return (
    <section
      data-testid="horse-passport-transfer-panel"
      className="rounded-lg border border-equine-silver/10 bg-equine-black/40 p-4"
    >
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div className="min-w-0">
          <div className="label-eyebrow">Horse passport</div>
          <div className="text-[13px] text-equine-silver/80 mt-2">
            Transfer safe passport contents when ownership changes.
          </div>
        </div>
        <div className="flex flex-col sm:flex-row gap-2">
          <Link
            to="/horse-transfers"
            data-testid="horse-passport-transfer-pending-link"
            className="min-h-11 inline-flex items-center justify-center text-[11px] tracking-[0.18em] uppercase border border-equine-silver/20 text-equine-platinum/70 hover:text-equine-silver hover:bg-equine-silver/10 px-4 py-2 rounded"
          >
            Pending
          </Link>
          <button
            type="button"
            onClick={onOpenTransfer}
            data-testid="horse-passport-transfer-start"
            className="min-h-11 text-[11px] tracking-[0.18em] uppercase border border-equine-silver/30 bg-equine-silver/10 hover:bg-equine-silver/20 text-equine-silver px-4 py-2 rounded"
          >
            Start Transfer
          </button>
        </div>
      </div>
    </section>
  );
}

function PassportTransferDrawer({ horseId, onClose }) {
  const [newOwnerUserId, setNewOwnerUserId] = useState("");
  const [destinationBarnId, setDestinationBarnId] = useState("");
  const [categories, setCategories] = useState(new Set(TRANSFER_SAFE_CATEGORIES.map((c) => c.value)));
  const [preview, setPreview] = useState(null);
  const [created, setCreated] = useState(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const toggle = (value) => {
    const next = new Set(categories);
    if (next.has(value)) next.delete(value);
    else next.add(value);
    setCategories(next);
  };

  const createTransfer = async () => {
    setError(null);
    setPreview(null);
    if (!newOwnerUserId.trim()) {
      setError("New owner user ID is required.");
      return;
    }
    setSaving(true);
    try {
      const response = await api.post("/horse-transfers", {
        horse_id: horseId,
        new_owner_user_id: newOwnerUserId.trim(),
        destination_barn_id: destinationBarnId.trim() || null,
        categories: Array.from(categories),
      });
      setCreated(response.data);
      const exportResponse = await api.get(`/horse-transfers/${response.data.id}/export-preview`);
      setPreview(exportResponse.data);
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not start transfer.");
    } finally {
      setSaving(false);
    }
  };

  const cancelTransfer = async () => {
    if (!created?.id) return;
    setSaving(true);
    setError(null);
    try {
      await api.post(`/horse-transfers/${created.id}/cancel`, {});
      onClose();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not cancel transfer.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-stretch justify-end" data-testid="horse-passport-transfer-drawer">
      <div className="flex-1 bg-equine-black/70 backdrop-blur-sm" onClick={onClose} />
      <div className="h-full max-h-dvh w-full max-w-md bg-equine-black border-l border-equine-silver/15 flex flex-col">
        <header className="shrink-0 px-5 py-4 border-b border-equine-silver/10 flex items-start justify-between gap-4">
          <div className="min-w-0">
            <div className="label-eyebrow text-equine-platinum/55">Horse passport</div>
            <div className="text-[18px] font-serif text-equine-silver mt-1">Ownership transfer</div>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={saving}
            aria-label="Close"
            data-testid="horse-passport-transfer-close"
            className="min-h-11 min-w-11 rounded border border-equine-silver/15 text-equine-platinum/65 hover:text-equine-silver hover:bg-equine-silver/10 disabled:opacity-40"
          >
            ×
          </button>
        </header>
        <div className="min-h-0 flex-1 overflow-y-auto px-5 py-4 pb-6 space-y-4">
          <label className="block">
            <span className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 block mb-1">New owner user ID</span>
            <input
              value={newOwnerUserId}
              onChange={(e) => setNewOwnerUserId(e.target.value)}
              disabled={Boolean(created)}
              data-testid="horse-passport-transfer-new-owner"
              className="min-h-11 w-full bg-equine-black/60 border border-equine-silver/15 rounded px-3 py-2 text-[13px] text-equine-silver focus:border-equine-silver/35 outline-none disabled:opacity-60"
            />
          </label>
          <label className="block">
            <span className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 block mb-1">Destination barn ID</span>
            <input
              value={destinationBarnId}
              onChange={(e) => setDestinationBarnId(e.target.value)}
              disabled={Boolean(created)}
              data-testid="horse-passport-transfer-destination-barn"
              className="min-h-11 w-full bg-equine-black/60 border border-equine-silver/15 rounded px-3 py-2 text-[13px] text-equine-silver focus:border-equine-silver/35 outline-none disabled:opacity-60"
            />
          </label>
          <div>
            <div className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 mb-2">Transfer contents</div>
            <div className="space-y-2">
              {TRANSFER_SAFE_CATEGORIES.map((category) => (
                <label
                  key={category.value}
                  className="flex items-center gap-3 rounded border border-equine-silver/10 bg-equine-silver/5 px-3 py-2"
                >
                  <input
                    type="checkbox"
                    checked={categories.has(category.value)}
                    onChange={() => toggle(category.value)}
                    disabled={Boolean(created)}
                    data-testid={`horse-passport-transfer-category-${category.value}`}
                  />
                  <span className="text-[13px] text-equine-silver/85">{category.label}</span>
                </label>
              ))}
            </div>
          </div>
          <div>
            <div className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 mb-2">Blocked pending policy</div>
            <div className="flex flex-wrap gap-2">
              {TRANSFER_BLOCKED_CATEGORIES.map((label) => (
                <span
                  key={label}
                  data-testid={`horse-passport-transfer-blocked-${label.toLowerCase().replaceAll(" ", "-")}`}
                  className="text-[11px] border border-equine-silver/10 bg-equine-silver/5 text-equine-platinum/55 rounded px-2 py-1"
                >
                  {label}
                </span>
              ))}
            </div>
          </div>
          {preview ? (
            <section
              data-testid="horse-passport-transfer-preview"
              className="rounded border border-equine-silver/10 bg-equine-silver/5 p-3"
            >
              <div className="label-eyebrow mb-2">Export preview</div>
              <div className="text-[12px] text-equine-platinum/70">
                {preview.categories?.length || 0} safe categories ready for new-owner acceptance.
              </div>
              <pre className="mt-3 max-h-48 overflow-auto whitespace-pre-wrap text-[11px] text-equine-platinum/60">
                {JSON.stringify(preview, null, 2)}
              </pre>
            </section>
          ) : null}
          {error ? (
            <div
              data-testid="horse-passport-transfer-error"
              className="text-[12.5px] text-equine-platinum/85 border border-equine-silver/30 bg-equine-silver/5 px-3 py-2 rounded"
            >
              {error}
            </div>
          ) : null}
        </div>
        <footer className="shrink-0 px-5 py-3 pb-[calc(0.75rem+env(safe-area-inset-bottom))] border-t border-equine-silver/10 flex justify-end gap-2">
          {created ? (
            <button
              type="button"
              onClick={cancelTransfer}
              disabled={saving}
              data-testid="horse-passport-transfer-cancel"
              className="min-h-11 text-[12px] tracking-[0.18em] uppercase text-equine-platinum/55 px-4 py-2 hover:text-equine-silver disabled:opacity-40"
            >
              Cancel Request
            </button>
          ) : null}
          <button
            type="button"
            onClick={created ? onClose : createTransfer}
            disabled={saving}
            data-testid="horse-passport-transfer-submit"
            className="min-h-11 text-[12px] tracking-[0.18em] uppercase bg-equine-silver/15 hover:bg-equine-silver/25 text-equine-silver border border-equine-silver/25 px-5 py-2 rounded disabled:opacity-40"
          >
            {saving ? "Working…" : created ? "Done" : "Create Preview"}
          </button>
        </footer>
      </div>
    </div>
  );
}

function OwnerRequestDrawer({ horseId, onClose, onSaved }) {
  const { user } = useAuth();
  const draftKey = buildHorseOpsDraftKey({
    userId: user?.id || user?.email,
    horseId,
    form: "owner-request",
  });
  const [type, setType]       = useState("question");
  const [contact, setContact] = useState("app");
  const [message, setMessage] = useState("");
  const [saving, setSaving]   = useState(false);
  const [error, setError]     = useState(null);
  const [draftRestored, setDraftRestored] = useState(false);
  const [draftReady, setDraftReady] = useState(false);

  useEffect(() => {
    const draft = loadHorseOpsDraft(draftKey);
    if (!draft) { setDraftReady(true); return; }
    if (draft.type) setType(draft.type);
    if (draft.contact) setContact(draft.contact);
    if (typeof draft.message === "string") setMessage(draft.message);
    setDraftRestored(true);
    setDraftReady(true);
  }, [draftKey]);

  useEffect(() => {
    if (!draftReady) return;
    if (type !== "question" || contact !== "app" || message.trim()) {
      saveHorseOpsDraft(draftKey, { type, contact, message });
    } else {
      clearHorseOpsDraft(draftKey);
    }
  }, [draftKey, draftReady, type, contact, message]);

  const save = async () => {
    setError(null);
    if (!message.trim()) { setError("Please add a short message."); return; }
    if (message.length > 1000) { setError("Message too long."); return; }
    setSaving(true);
    try {
      await api.post(`/horse-ledger/${horseId}/owner-service-requests`, {
        request_type: type, message, preferred_contact: contact,
      });
      clearHorseOpsDraft(draftKey);
      onSaved();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not send your request.");
    } finally { setSaving(false); }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-stretch justify-end" data-testid="owner-request-drawer">
      <div className="flex-1 bg-equine-black/70 backdrop-blur-sm" onClick={onClose} />
      <div className="h-full max-h-dvh w-full max-w-md bg-equine-black border-l border-equine-silver/15 flex flex-col">
        <header className="shrink-0 px-5 py-4 border-b border-equine-silver/10 flex items-start justify-between gap-4">
          <div className="min-w-0">
            <div className="label-eyebrow text-equine-platinum/55">Ask the barn</div>
            <div className="text-[18px] font-serif text-equine-silver mt-1">New request</div>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={saving}
            aria-label="Close"
            data-testid="owner-request-drawer-close"
            className="min-h-11 min-w-11 rounded border border-equine-silver/15 text-equine-platinum/65 hover:text-equine-silver hover:bg-equine-silver/10 disabled:opacity-40"
          >
            ×
          </button>
        </header>
        <div className="min-h-0 flex-1 overflow-y-auto px-5 py-4 pb-6 space-y-3">
          {draftRestored ? (
            <div
              data-testid="owner-request-draft-restored"
              className="text-[12.5px] text-equine-platinum/70 border border-equine-silver/20 bg-equine-silver/5 px-3 py-2 rounded"
            >
              Draft restored on this device.
            </div>
          ) : null}
          <label className="block">
            <span className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 block mb-1">Type</span>
            <select
              value={type}
              onChange={(e) => setType(e.target.value)}
              data-testid="owner-request-drawer-type"
              className="min-h-11 w-full bg-equine-black/60 border border-equine-silver/15 rounded px-3 py-2 text-[13px] text-equine-silver focus:border-equine-silver/35 outline-none"
            >
              {REQUEST_TYPES.map((r) => (
                <option key={r.value} value={r.value} data-testid={`owner-request-drawer-type-${r.value}`}>{r.label}</option>
              ))}
            </select>
          </label>
          <label className="block">
            <span className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 block mb-1">Preferred contact</span>
            <select
              value={contact}
              onChange={(e) => setContact(e.target.value)}
              data-testid="owner-request-drawer-contact"
              className="min-h-11 w-full bg-equine-black/60 border border-equine-silver/15 rounded px-3 py-2 text-[13px] text-equine-silver focus:border-equine-silver/35 outline-none"
            >
              {CONTACT_OPTIONS.map((c) => (
                <option key={c.value} value={c.value} data-testid={`owner-request-drawer-contact-${c.value}`}>{c.label}</option>
              ))}
            </select>
          </label>
          <label className="block">
            <span className="text-[11px] tracking-[0.18em] uppercase text-equine-platinum/55 block mb-1">Message</span>
            <textarea
              rows={5}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              maxLength={1000}
              data-testid="owner-request-drawer-message"
              className="w-full bg-equine-black/60 border border-equine-silver/15 rounded px-3 py-2 text-[13px] text-equine-silver focus:border-equine-silver/35 outline-none resize-y"
            />
            <div className="text-[11px] text-equine-platinum/45 mt-1">{message.length}/1000</div>
          </label>
          {error ? (
            <div
              data-testid="owner-request-error"
              className="text-[12.5px] text-equine-platinum/85 border border-equine-silver/30 bg-equine-silver/5 px-3 py-2 rounded"
            >
              {error}
            </div>
          ) : null}
        </div>
        <footer className="shrink-0 px-5 py-3 pb-[calc(0.75rem+env(safe-area-inset-bottom))] border-t border-equine-silver/10 flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            disabled={saving}
            data-testid="owner-request-cancel"
            className="min-h-11 text-[12px] tracking-[0.18em] uppercase text-equine-platinum/55 px-4 py-2 hover:text-equine-silver"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={save}
            disabled={saving}
            data-testid="owner-request-submit"
            className="min-h-11 text-[12px] tracking-[0.18em] uppercase bg-equine-silver/15 hover:bg-equine-silver/25 text-equine-silver border border-equine-silver/25 px-5 py-2 rounded disabled:opacity-40"
          >
            {saving ? "Sending…" : "Send"}
          </button>
        </footer>
      </div>
    </div>
  );
}
