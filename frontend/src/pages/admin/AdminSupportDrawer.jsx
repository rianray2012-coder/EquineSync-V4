/**
 * AdminSupportDrawer — read + the 3 gated mutations.
 *
 * Mutations call the server, which audits each change. Note body
 * stays in the ticket record; server logs only `note_present: true`.
 * billing_admin / read_only_auditor are blocked at the API layer.
 */
import React, { useEffect, useState } from "react";
import { X, History, Mail, MessageSquare, UserPlus } from "lucide-react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";

const STATUSES = ["new", "in_progress", "waiting", "resolved"];

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

export default function AdminSupportDrawer({ ticketRef, open, onClose, onMutated }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [note, setNote] = useState("");
  const [assignee, setAssignee] = useState("");
  const [busy, setBusy] = useState(false);

  const reload = () => {
    if (!ticketRef) return;
    setLoading(true);
    api.get(`/admin/portal/support/${ticketRef}`)
      .then((r) => { setData(r.data); setErr(null); })
      .catch((e) => setErr(e?.response?.data?.detail || "Could not load ticket."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (!open || !ticketRef) return;
    let cancelled = false;
    api.get(`/admin/portal/support/${ticketRef}`)
      .then((r) => { if (!cancelled) { setData(r.data); setErr(null); } })
      .catch((e) => { if (!cancelled) setErr(e?.response?.data?.detail || "Could not load ticket."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [open, ticketRef]);

  const changeStatus = async (next) => {
    setBusy(true);
    try {
      await api.post(`/admin/portal/support/${ticketRef}/status`, { status: next });
      reload();
      onMutated && onMutated();
    } catch (e) {
      setErr(e?.response?.data?.detail || "Status change failed.");
    } finally {
      setBusy(false);
    }
  };

  const assign = async () => {
    setBusy(true);
    try {
      await api.post(`/admin/portal/support/${ticketRef}/assign`, {
        assignee_user_id: assignee.trim() || null,
      });
      reload();
      onMutated && onMutated();
    } catch (e) {
      setErr(e?.response?.data?.detail || "Assign failed.");
    } finally {
      setBusy(false);
    }
  };

  const addNote = async () => {
    if (!note.trim()) return;
    setBusy(true);
    try {
      await api.post(`/admin/portal/support/${ticketRef}/notes`, { body: note });
      setNote("");
      reload();
      onMutated && onMutated();
    } catch (e) {
      setErr(e?.response?.data?.detail || "Add-note failed.");
    } finally {
      setBusy(false);
    }
  };

  if (!open) return null;
  const ticket = data?.ticket;

  return (
    <div className="fixed inset-0 z-40 flex" data-testid="admin-support-drawer">
      <div className="flex-1 bg-equinesync-graphite/40" onClick={onClose} />
      <aside className="w-full max-w-xl bg-white border-l border-equinesync-graphite/10 overflow-y-auto">
        <header className="sticky top-0 z-10 bg-white border-b border-equinesync-graphite/10 px-5 py-4 flex items-start justify-between">
          <div className="min-w-0">
            <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              Support ticket
            </div>
            <div className="mt-0.5 font-display text-lg text-equinesync-graphite font-light truncate">
              {ticket?.subject || ticketRef}
            </div>
          </div>
          <button type="button" onClick={onClose}
                  className="text-equinesync-graphite/40 hover:text-equinesync-graphite"
                  data-testid="admin-support-drawer-close" aria-label="Close">
            <X className="w-4 h-4" />
          </button>
        </header>

        <div className="p-5 space-y-5">
          {loading && (
            <div className="space-y-3" data-testid="admin-support-drawer-loading">
              {[0,1,2].map((i) => <div key={i} className="h-16 bg-equinesync-graphite/5 rounded animate-pulse" />)}
            </div>
          )}
          {err && <div className="text-[13px] text-equinesync-graphite/70" data-testid="admin-support-drawer-error">{err}</div>}

          {ticket && (
            <>
              <section data-testid="admin-support-drawer-summary">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Mail className="w-3 h-3" />Ticket
                </div>
                <div className="rounded-lg bg-equinesync-frost p-3 text-[13px] text-equinesync-graphite space-y-1">
                  <div><span className="text-equinesync-graphite/55">From:</span> {ticket.submitter_email || ticket.submitter_user_id || "—"}</div>
                  <div><span className="text-equinesync-graphite/55">Channel:</span> {ticket.channel || "—"}</div>
                  <div><span className="text-equinesync-graphite/55">Status:</span> <UserStatusBadge value={ticket.status} /></div>
                  <div><span className="text-equinesync-graphite/55">Assignee:</span> {ticket.assignee_email || "Unassigned"}</div>
                  <div><span className="text-equinesync-graphite/55">Updated:</span> {formatTs(ticket.updated_at)}</div>
                </div>
                {ticket.description && (
                  <div className="mt-2 text-[13px] text-equinesync-graphite/80 whitespace-pre-wrap rounded-lg bg-equinesync-frost p-3">
                    {ticket.description}
                  </div>
                )}
              </section>

              <section data-testid="admin-support-drawer-status">
                <div className="text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">Change status</div>
                <div className="flex flex-wrap gap-2">
                  {STATUSES.map((s) => (
                    <button key={s} type="button" disabled={busy || s === ticket.status}
                            onClick={() => changeStatus(s)}
                            data-testid={`admin-support-status-${s}`}
                            className={`px-3 py-1.5 rounded-lg text-[12.5px] border ${
                              s === ticket.status
                                ? "bg-equinesync-graphite text-equinesync-frost border-equinesync-graphite"
                                : "border-equinesync-graphite/15 text-equinesync-graphite/80 hover:bg-equinesync-frost disabled:opacity-40"
                            }`}>{s}</button>
                  ))}
                </div>
              </section>

              <section data-testid="admin-support-drawer-assign">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <UserPlus className="w-3 h-3" />Assign
                </div>
                <div className="flex gap-2">
                  <input type="text" value={assignee}
                         onChange={(e) => setAssignee(e.target.value)}
                         placeholder="Platform admin user id (blank to clear)"
                         data-testid="admin-support-assign-input"
                         className="flex-1 px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]" />
                  <button type="button" onClick={assign} disabled={busy}
                          data-testid="admin-support-assign-btn"
                          className="px-3 py-2 rounded-lg bg-equinesync-graphite text-equinesync-frost text-[12.5px] disabled:opacity-40">
                    {busy ? "…" : "Update"}
                  </button>
                </div>
              </section>

              <section data-testid="admin-support-drawer-notes">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <MessageSquare className="w-3 h-3" />Internal notes
                </div>
                {ticket.internal_notes && ticket.internal_notes.length ? (
                  <ul className="space-y-2 mb-3">
                    {ticket.internal_notes.map((n) => (
                      <li key={n.id} className="rounded-lg bg-equinesync-frost p-3 text-[12.5px] text-equinesync-graphite/85">
                        <div className="text-equinesync-graphite/55 text-[11px] mb-1">
                          {n.author_email || n.author_user_id} · {formatTs(n.ts)}
                        </div>
                        <div className="whitespace-pre-wrap">{n.body}</div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50 mb-3">No internal notes yet.</div>
                )}
                <textarea value={note} onChange={(e) => setNote(e.target.value)}
                          rows={3} placeholder="Add a note (visible to admins only; not logged to audit metadata)…"
                          data-testid="admin-support-note-input"
                          className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px] resize-none" />
                <div className="mt-2 flex justify-end">
                  <button type="button" onClick={addNote} disabled={busy || !note.trim()}
                          data-testid="admin-support-note-submit"
                          className="px-3 py-2 rounded-lg bg-equinesync-graphite text-equinesync-frost text-[12.5px] disabled:opacity-40">
                    {busy ? "…" : "Add note"}
                  </button>
                </div>
              </section>

              <section data-testid="admin-support-drawer-audit">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <History className="w-3 h-3" />Recent activity
                </div>
                {data?.recent_activity?.length ? (
                  <ul className="space-y-1">
                    {data.recent_activity.map((a, i) => (
                      <li key={a.id || `${a.action}-${i}`} className="text-[12px] text-equinesync-graphite/75">
                        <span className="text-equinesync-graphite font-medium">{a.action}</span> · {formatTs(a.ts)} · {a.actor_email || "—"}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No recorded activity yet.</div>
                )}
              </section>
            </>
          )}
        </div>
      </aside>
    </div>
  );
}
