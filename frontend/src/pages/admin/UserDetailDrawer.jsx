/**
 * UserDetailDrawer — right-side slide-in panel showing a user's safe
 * profile + barn summary + horses count + recent audit log. Admin-3
 * surface: ONLY the actions allowed by the actor's platform_role are
 * rendered. Read-only roles see no mutation buttons.
 */
import React, { useEffect, useState } from "react";
import { X, Mail, Building2, Heart, History } from "lucide-react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

export default function UserDetailDrawer({
  userId,
  actor,            // current platform admin (for permission gates)
  open,
  onClose,
  onAction,         // (actionName) => void  — page-level handler
  busyAction,       // string | null  — currently-running action
}) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!open || !userId) return;
    let cancelled = false;
    setLoading(true);
    setDetail(null);
    setErr(null);
    api.get(`/admin/portal/users/${userId}`)
      .then((r) => { if (!cancelled) setDetail(r.data); })
      .catch((e) => { if (!cancelled) setErr(e?.response?.data?.detail || "Could not load user."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [open, userId]);

  if (!open) return null;

  const u = detail?.user;
  const actorPlatformRole = String((actor?.platform_role || "")).toLowerCase();
  const targetIsSelf = u && actor && u.id === actor.id;
  const targetIsSuperAdmin = u && String((u.platform_role || "")).toLowerCase() === "super_admin";

  // Mutation visibility: matches the backend role matrix exactly.
  const canFullMutate =
    ["super_admin", "platform_admin"].includes(actorPlatformRole) &&
    !targetIsSelf &&
    !(actorPlatformRole !== "super_admin" && targetIsSuperAdmin);
  const canRequestInfo =
    ["super_admin", "platform_admin", "support_admin"].includes(actorPlatformRole) &&
    !targetIsSelf &&
    !(actorPlatformRole !== "super_admin" && targetIsSuperAdmin);

  const isPending  = u?.role_status === "pending_review";
  const isActive   = u?.role_status === "active";
  const isSuspended = u?.account_status === "suspended";

  const Btn = ({ id, label, onClick, primary }) => (
    <button
      type="button"
      onClick={onClick}
      disabled={!!busyAction}
      data-testid={`admin-user-action-${id}`}
      className={`px-3 py-1.5 rounded-lg text-[12px] tracking-wide disabled:opacity-50 ${
        primary
          ? "bg-equinesync-slate text-equinesync-frost hover:bg-equinesync-graphite"
          : "border border-equinesync-graphite/15 text-equinesync-graphite hover:bg-equinesync-frost"
      }`}
    >
      {busyAction === id ? "Working…" : label}
    </button>
  );

  return (
    <div className="fixed inset-0 z-40 flex" data-testid="admin-user-drawer">
      <div className="flex-1 bg-equinesync-graphite/40" onClick={onClose} />
      <aside className="w-full max-w-lg bg-white border-l border-equinesync-graphite/10 overflow-y-auto">
        <header className="sticky top-0 z-10 bg-white border-b border-equinesync-graphite/10 px-5 py-4 flex items-start justify-between">
          <div className="min-w-0">
            <div className="text-[10.5px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              User detail
            </div>
            <div className="mt-0.5 font-display text-lg text-equinesync-graphite font-light truncate">
              {u?.full_name || u?.email || "—"}
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="text-equinesync-graphite/40 hover:text-equinesync-graphite"
            data-testid="admin-user-drawer-close"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </header>

        <div className="p-5 space-y-5">
          {loading && (
            <div className="space-y-3" data-testid="admin-user-drawer-loading">
              <div className="h-4 bg-equinesync-graphite/5 rounded animate-pulse" />
              <div className="h-4 bg-equinesync-graphite/5 rounded animate-pulse w-3/4" />
              <div className="h-20 bg-equinesync-graphite/5 rounded animate-pulse" />
            </div>
          )}
          {err && (
            <div className="text-[13px] text-equinesync-graphite/70" data-testid="admin-user-drawer-error">
              {err}
            </div>
          )}

          {u && (
            <>
              {/* Identity row */}
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-[13.5px] text-equinesync-graphite">
                  <Mail className="w-3.5 h-3.5 text-equinesync-graphite/40" />
                  {u.email}
                </div>
                <div className="flex flex-wrap gap-1.5">
                  <UserStatusBadge value={u.role} kind="role" />
                  <UserStatusBadge value={u.role_status} kind="status" />
                  {u.account_status && (
                    <UserStatusBadge value={u.account_status} kind="account" />
                  )}
                  {u.platform_role && (
                    <UserStatusBadge value={u.platform_role} kind="platform" />
                  )}
                </div>
                <div className="text-[11.5px] text-equinesync-graphite/55">
                  Created {formatTs(u.created_at)}
                  {u.last_login_at && <> · Last login {formatTs(u.last_login_at)}</>}
                </div>
              </div>

              {/* Mutation buttons — visibility = permission */}
              {(canFullMutate || canRequestInfo) && (
                <div
                  data-testid="admin-user-actions"
                  className="flex flex-wrap gap-2 pt-1"
                >
                  {canFullMutate && isPending && (
                    <Btn id="approve" label="Approve" primary onClick={() => onAction("approve")} />
                  )}
                  {canFullMutate && isPending && (
                    <Btn id="reject" label="Reject" onClick={() => onAction("reject")} />
                  )}
                  {canRequestInfo && isPending && (
                    <Btn id="request-info" label="Request info" onClick={() => onAction("request-info")} />
                  )}
                  {canFullMutate && isActive && !isSuspended && (
                    <Btn id="suspend" label="Suspend" onClick={() => onAction("suspend")} />
                  )}
                  {canFullMutate && isSuspended && (
                    <Btn id="reactivate" label="Reactivate" primary onClick={() => onAction("reactivate")} />
                  )}
                </div>
              )}

              {/* Barn / facility summary */}
              <section data-testid="admin-user-drawer-barn">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Building2 className="w-3 h-3" />
                  Facility
                </div>
                {detail?.barn ? (
                  <div className="rounded-lg bg-equinesync-frost p-3 text-[13px] text-equinesync-graphite">
                    <div className="font-medium">{detail.barn.name || detail.barn.id}</div>
                    <div className="text-[11.5px] text-equinesync-graphite/55 mt-0.5">
                      {detail.barn.subscription_tier_code || "—"} ·{" "}
                      {detail.barn.id}
                    </div>
                  </div>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No facility associated.</div>
                )}
              </section>

              {/* Horses */}
              <section data-testid="admin-user-drawer-horses">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <Heart className="w-3 h-3" />
                  Horses ({detail?.horses?.count || 0})
                </div>
                {detail?.horses?.recent?.length ? (
                  <ul className="space-y-1">
                    {detail.horses.recent.map((h) => (
                      <li
                        key={h.id}
                        className="text-[12.5px] text-equinesync-graphite/80 flex items-center justify-between"
                      >
                        <span>{h.name || h.id}</span>
                        <span className="text-equinesync-graphite/40">{formatTs(h.created_at)}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No horses on record.</div>
                )}
              </section>

              {/* Recent audit */}
              <section data-testid="admin-user-drawer-audit">
                <div className="flex items-center gap-2 text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-2">
                  <History className="w-3 h-3" />
                  Recent admin activity
                </div>
                {detail?.recent_audit?.length ? (
                  <ul className="space-y-1.5">
                    {detail.recent_audit.map((a, i) => (
                      <li key={a.id || `${a.action}-${i}`} className="text-[12px] text-equinesync-graphite/75">
                        <span className="text-equinesync-graphite font-medium">{a.action}</span>{" "}
                        · {formatTs(a.ts)}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="text-[12.5px] text-equinesync-graphite/50">No matching audit entries.</div>
                )}
              </section>
            </>
          )}
        </div>
      </aside>
    </div>
  );
}
