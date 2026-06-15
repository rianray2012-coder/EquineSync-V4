/**
 * AdminAuditLogDrawer — full audit row with scrubbed metadata.
 *
 * Read-only. Opaque `al_*` ref routing. Cross-surface ref shown when
 * the server resolved the row's resource_type into a known Admin entity.
 */
import React, { useEffect, useState } from "react";
import { X, History } from "lucide-react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

export default function AdminAuditLogDrawer({ auditRef, open, onClose }) {
  const [row, setRow] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!open || !auditRef) return;
    let cancelled = false;
    api.get(`/admin/portal/audit-logs/${auditRef}`)
      .then((r) => { if (!cancelled) { setRow(r.data.row); setErr(null); } })
      .catch((e) => { if (!cancelled) setErr(e?.response?.data?.detail || "Could not load audit row."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [open, auditRef]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-40 flex" data-testid="admin-audit-log-drawer">
      <div className="flex-1 bg-equinesync-graphite/40" onClick={onClose} />
      <aside className="w-full max-w-xl bg-white border-l border-equinesync-graphite/10 overflow-y-auto">
        <header className="sticky top-0 z-10 bg-white border-b border-equinesync-graphite/10 px-5 py-4 flex items-start justify-between">
          <div className="min-w-0">
            <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              Audit row · read-only
            </div>
            <div className="mt-0.5 font-display text-lg text-equinesync-graphite font-light truncate">
              {row?.action || auditRef}
            </div>
          </div>
          <button type="button" onClick={onClose}
                  className="text-equinesync-graphite/40 hover:text-equinesync-graphite"
                  data-testid="admin-audit-log-drawer-close" aria-label="Close">
            <X className="w-4 h-4" />
          </button>
        </header>

        <div className="p-5 space-y-5">
          {loading && (
            <div className="space-y-3" data-testid="admin-audit-log-drawer-loading">
              {[0,1,2].map((i) => <div key={i} className="h-16 bg-equinesync-graphite/5 rounded animate-pulse" />)}
            </div>
          )}
          {err && <div className="text-[13px] text-equinesync-graphite/70" data-testid="admin-audit-log-drawer-error">{err}</div>}

          {row && (
            <>
              <section className="space-y-2 text-[13px]" data-testid="admin-audit-log-drawer-summary">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <History className="w-3 h-3" />Summary
                </div>
                <div className="rounded-lg bg-equinesync-frost p-3 space-y-1">
                  <div><span className="text-equinesync-graphite/55">When:</span> {formatTs(row.ts)}</div>
                  <div><span className="text-equinesync-graphite/55">Action:</span> {row.action}</div>
                  <div><span className="text-equinesync-graphite/55">Actor:</span> {row.actor_email || row.actor_user_id || "—"}</div>
                  <div className="flex items-center gap-2">
                    <span className="text-equinesync-graphite/55">Outcome:</span>
                    {row.outcome ? <UserStatusBadge value={row.outcome} /> : "—"}
                    {row.status_code != null && (
                      <span className="text-equinesync-graphite/55 text-[11.5px]">· {row.status_code}</span>
                    )}
                  </div>
                  {row.resource && (
                    <div>
                      <span className="text-equinesync-graphite/55">Resource:</span>{" "}
                      <span>{row.resource.kind}</span>
                      {row.resource.admin_ref && (
                        <span className="text-equinesync-graphite/55 font-mono text-[11.5px]"> · {row.resource.admin_ref}</span>
                      )}
                    </div>
                  )}
                  {row.ip_address && (
                    <div><span className="text-equinesync-graphite/55">IP:</span> {row.ip_address}</div>
                  )}
                </div>
              </section>

              <section data-testid="admin-audit-log-drawer-metadata">
                <div className="text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  Metadata (scrubbed)
                </div>
                {row.metadata && Object.keys(row.metadata).length ? (
                  <div className="rounded-lg bg-equinesync-frost p-3 text-[12.5px] grid grid-cols-1 gap-1">
                    {Object.entries(row.metadata).map(([k, v]) => (
                      <div key={k}>
                        <span className="text-equinesync-graphite/55">{k}:</span>{" "}
                        <span className="text-equinesync-graphite break-all">
                          {typeof v === "object" ? JSON.stringify(v) : String(v)}
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No metadata for this row.</div>
                )}
              </section>
            </>
          )}
        </div>
      </aside>
    </div>
  );
}
