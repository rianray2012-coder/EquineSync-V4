/**
 * AdminUsers — paginated, searchable, filterable user roster with a
 * detail drawer. First Admin Portal MUTATION page (gated by platform
 * role, with confirmation modals for every sensitive action).
 */
import React, { useCallback, useEffect, useState } from "react";
import { api } from "../../lib/api";
import { useAuth } from "../../context/AuthContext";
import UserStatusBadge from "./UserStatusBadge";
import UserDetailDrawer from "./UserDetailDrawer";
import ConfirmActionModal from "./ConfirmActionModal";

const ROLE_OPTIONS = ["", "horse_owner", "rider", "trainer", "barn_owner", "service_provider", "admin"];
const STATUS_OPTIONS = ["", "active", "pending_review", "rejected"];

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
  catch { return iso; }
};

export default function AdminUsers() {
  const { user: actor } = useAuth();
  const [items, setItems] = useState(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  // Filters
  const [q, setQ] = useState("");
  const [role, setRole] = useState("");
  const [status, setStatus] = useState("");
  const [cursor, setCursor] = useState(0);
  const [nextCursor, setNextCursor] = useState(null);

  // Drawer + modal
  const [openUserId, setOpenUserId] = useState(null);
  const [pendingAction, setPendingAction] = useState(null);     // {id, action, label, note?}
  const [busyAction, setBusyAction] = useState(null);

  const load = useCallback(async () => {
    setLoading(true); setErr(null);
    try {
      const params = new URLSearchParams();
      if (q) params.set("q", q);
      if (role) params.set("role", role);
      if (status) params.set("role_status", status);
      params.set("limit", "25");
      params.set("cursor", String(cursor));
      const { data } = await api.get(`/admin/portal/users?${params.toString()}`);
      setItems(data.items);
      setTotal(data.total);
      setNextCursor(data.next_cursor);
    } catch (e) {
      setErr(e?.response?.data?.detail || "Failed to load users.");
    } finally {
      setLoading(false);
    }
  }, [q, role, status, cursor]);

  useEffect(() => { load(); }, [load]);

  const handleAction = (action) => {
    if (!openUserId) return;
    const needsNote = action === "reject" || action === "request-info";
    if (needsNote) {
      setPendingAction({
        id: openUserId, action,
        label: action === "reject" ? "Reject user" : "Request more info",
        description: action === "reject"
          ? "Soft-rejects the user. They keep the account but lose access to gated features. This is reversible by a super_admin via direct DB change."
          : "Sets a note on the user's review; the account stays in pending_review.",
        noteLabel: "Reason / note",
        noteRequired: true,
        confirmLabel: action === "reject" ? "Reject" : "Send",
      });
    } else if (action === "suspend") {
      setPendingAction({
        id: openUserId, action,
        label: "Suspend user",
        description: "Suspended users lose login session access at the next request. Reversible via Reactivate.",
        confirmLabel: "Suspend",
      });
    } else if (action === "approve") {
      setPendingAction({
        id: openUserId, action,
        label: "Approve user",
        description: "Sets role_status to active. Optional barn assignment is not provided in this prompt — use the user record directly if needed.",
        confirmLabel: "Approve",
      });
    } else if (action === "reactivate") {
      setPendingAction({
        id: openUserId, action,
        label: "Reactivate user",
        description: "Clears the suspended state and restores access.",
        confirmLabel: "Reactivate",
      });
    }
  };

  const confirmMutation = async (note) => {
    if (!pendingAction) return;
    setBusyAction(pendingAction.action);
    try {
      const body = note ? { review_note: note } : {};
      await api.post(`/admin/portal/users/${pendingAction.id}/${pendingAction.action}`, body);
      setPendingAction(null);
      // Refresh list and (optionally) refresh drawer by closing+reopening.
      const re = openUserId;
      setOpenUserId(null);
      await load();
      setOpenUserId(re);
    } catch (e) {
      setErr(e?.response?.data?.detail || "Action failed.");
    } finally {
      setBusyAction(null);
    }
  };

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-users-page">
      <div className="mb-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal · Users
        </div>
        <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">User management</h1>
        <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
          Search and review platform users. Sensitive actions are gated by
          your platform role and require confirmation.
        </p>
      </div>

      {/* Filter bar */}
      <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-4 mb-4 flex flex-wrap items-end gap-3"
           data-testid="admin-users-filters">
        <div className="flex-1 min-w-[220px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Search</label>
          <input
            type="text"
            value={q}
            onChange={(e) => { setCursor(0); setQ(e.target.value); }}
            placeholder="Email or full name"
            data-testid="admin-users-search"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-equinesync-frost text-[13px] focus:outline-none focus:border-equinesync-slate"
          />
        </div>
        <div className="min-w-[160px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Role</label>
          <select
            value={role}
            onChange={(e) => { setCursor(0); setRole(e.target.value); }}
            data-testid="admin-users-role-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {ROLE_OPTIONS.map((o) => (<option key={o} value={o}>{o || "Any role"}</option>))}
          </select>
        </div>
        <div className="min-w-[160px]">
          <label className="block text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/55 mb-1">Status</label>
          <select
            value={status}
            onChange={(e) => { setCursor(0); setStatus(e.target.value); }}
            data-testid="admin-users-status-filter"
            className="w-full px-3 py-2 rounded-lg border border-equinesync-graphite/15 bg-white text-[13px]"
          >
            {STATUS_OPTIONS.map((o) => (<option key={o} value={o}>{o ? o.replace(/_/g, " ") : "Any status"}</option>))}
          </select>
        </div>
        <div className="text-[11.5px] text-equinesync-graphite/55 ml-auto">
          {total.toLocaleString()} total
        </div>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-users-error">
          {err}
        </div>
      )}

      {/* Table */}
      <div className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
        {loading && !items && (
          <div className="p-6 space-y-3" data-testid="admin-users-loading">
            {[0,1,2,3,4].map((i) => (
              <div key={i} className="h-9 bg-equinesync-graphite/5 rounded animate-pulse" />
            ))}
          </div>
        )}
        {!loading && items && items.length === 0 && (
          <div className="p-10 text-center text-[13px] text-equinesync-graphite/50" data-testid="admin-users-empty">
            No users match the current filters.
          </div>
        )}
        {items && items.length > 0 && (
          <table className="w-full text-[13px]" data-testid="admin-users-table">
            <thead className="bg-equinesync-frost border-b border-equinesync-graphite/10">
              <tr className="text-left text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
                <th className="px-4 py-3 font-medium">Email</th>
                <th className="px-4 py-3 font-medium">Role</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Platform</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Created</th>
              </tr>
            </thead>
            <tbody>
              {items.map((u) => (
                <tr
                  key={u.id}
                  data-testid={`admin-users-row-${u.id}`}
                  onClick={() => setOpenUserId(u.id)}
                  className="border-b border-equinesync-graphite/5 last:border-b-0 hover:bg-equinesync-frost cursor-pointer"
                >
                  <td className="px-4 py-3">
                    <div className="text-equinesync-graphite font-medium">{u.full_name || "—"}</div>
                    <div className="text-equinesync-graphite/55 text-[11.5px]">{u.email}</div>
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">{u.role || "—"}</td>
                  <td className="px-4 py-3">
                    <div className="flex flex-wrap gap-1">
                      <UserStatusBadge value={u.role_status} />
                      {u.account_status === "suspended" && (
                        <UserStatusBadge value="suspended" kind="account" />
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-3 hidden md:table-cell">
                    {u.platform_role ? <UserStatusBadge value={u.platform_role} kind="platform" /> : (
                      <span className="text-equinesync-graphite/35">—</span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden md:table-cell">
                    {formatTs(u.created_at)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* Pagination */}
        {items && items.length > 0 && (
          <div className="px-4 py-3 border-t border-equinesync-graphite/10 flex justify-between items-center text-[11.5px] text-equinesync-graphite/55"
               data-testid="admin-users-pagination">
            <div>
              Showing {cursor + 1}–{cursor + items.length} of {total.toLocaleString()}
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={cursor === 0}
                onClick={() => setCursor(Math.max(0, cursor - 25))}
                data-testid="admin-users-prev"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >
                Previous
              </button>
              <button
                type="button"
                disabled={nextCursor === null}
                onClick={() => setCursor(nextCursor)}
                data-testid="admin-users-next"
                className="px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 disabled:opacity-40"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>

      <UserDetailDrawer
        userId={openUserId}
        actor={actor}
        open={!!openUserId}
        onClose={() => setOpenUserId(null)}
        onAction={handleAction}
        busyAction={busyAction}
      />

      <ConfirmActionModal
        open={!!pendingAction}
        title={pendingAction?.label || ""}
        description={pendingAction?.description}
        confirmLabel={pendingAction?.confirmLabel || "Confirm"}
        noteLabel={pendingAction?.noteLabel}
        noteRequired={pendingAction?.noteRequired}
        busy={!!busyAction}
        onCancel={() => setPendingAction(null)}
        onConfirm={confirmMutation}
        testId={`admin-confirm-${pendingAction?.action || "none"}`}
      />
    </div>
  );
}
