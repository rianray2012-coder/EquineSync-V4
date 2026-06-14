/**
 * ConfirmActionModal — generic confirmation/note prompt for any
 * destructive or sensitive admin mutation. Used by Admin-3 for
 * reject / request-info / suspend / reactivate.
 *
 * Read-only palette: Midnight Graphite + Slate Navy + Frost White +
 * Smoky Lilac. The primary action button is Slate Navy on hover-Graphite,
 * cancel is a neutral Frost outline. Optional note field is capped
 * client-side at 500 chars to match the backend.
 */
import React, { useEffect, useState } from "react";
import { X } from "lucide-react";

const NOTE_MAX = 500;

export default function ConfirmActionModal({
  open,
  title,
  description,
  confirmLabel,
  noteLabel,
  noteRequired = false,
  busy = false,
  onCancel,
  onConfirm,
  testId,
}) {
  const [note, setNote] = useState("");

  useEffect(() => { if (!open) setNote(""); }, [open]);

  if (!open) return null;

  const noteOver = note.length > NOTE_MAX;
  const canConfirm = !busy && (!noteRequired || note.trim().length > 0) && !noteOver;

  return (
    <div
      className="fixed inset-0 z-50 bg-equinesync-graphite/60 flex items-center justify-center px-4"
      data-testid={testId || "admin-confirm-modal"}
    >
      <div className="w-full max-w-md bg-white rounded-xl border border-equinesync-graphite/10 shadow-2xl">
        <div className="p-5 border-b border-equinesync-graphite/10 flex items-start justify-between">
          <div>
            <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              Admin action
            </div>
            <h2 className="mt-1 font-display text-xl text-equinesync-graphite font-light">
              {title}
            </h2>
          </div>
          <button
            type="button"
            onClick={onCancel}
            className="text-equinesync-graphite/40 hover:text-equinesync-graphite"
            data-testid="admin-confirm-close"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
        <div className="p-5 space-y-4">
          {description && (
            <p className="text-[13.5px] text-equinesync-graphite/70 leading-relaxed">
              {description}
            </p>
          )}
          {noteLabel && (
            <div>
              <label className="block text-[11px] tracking-[0.22em] uppercase text-equinesync-graphite/60 mb-1.5">
                {noteLabel}{noteRequired && <span className="text-equinesync-slate"> *</span>}
              </label>
              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                rows={3}
                maxLength={NOTE_MAX + 100}
                data-testid="admin-confirm-note"
                className="w-full rounded-lg border border-equinesync-graphite/15 bg-equinesync-frost p-3 text-[13px] text-equinesync-graphite resize-y focus:outline-none focus:border-equinesync-slate"
                placeholder="Reason or context — visible to the user when surfaced."
              />
              <div className="mt-1 text-[10.5px] tracking-wide text-equinesync-graphite/45 flex justify-between">
                <span>Stored in the audit trail.</span>
                <span className={noteOver ? "text-equinesync-slate" : ""}>
                  {note.length} / {NOTE_MAX}
                </span>
              </div>
            </div>
          )}
        </div>
        <div className="p-5 border-t border-equinesync-graphite/10 flex justify-end gap-2">
          <button
            type="button"
            onClick={onCancel}
            disabled={busy}
            data-testid="admin-confirm-cancel"
            className="px-4 py-2 rounded-lg border border-equinesync-graphite/15 text-[13px] tracking-wide text-equinesync-graphite hover:bg-equinesync-frost disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={() => onConfirm(note.trim() || null)}
            disabled={!canConfirm}
            data-testid="admin-confirm-submit"
            className="px-4 py-2 rounded-lg bg-equinesync-slate text-equinesync-frost text-[13px] tracking-wide hover:bg-equinesync-graphite disabled:opacity-50"
          >
            {busy ? "Working…" : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
