/**
 * AdminApprovals — pending-review queue.
 *
 * Reuses UserDetailDrawer + ConfirmActionModal from AdminUsers so the
 * approve / reject / request-info flows behave identically. The page
 * only renders users with role_status="pending_review".
 */
import React, { useCallback, useEffect, useState } from "react";
import { api } from "../../lib/api";
import { useAuth } from "../../context/AuthContext";
import UserStatusBadge from "./UserStatusBadge";
import UserDetailDrawer from "./UserDetailDrawer";
import ConfirmActionModal from "./ConfirmActionModal";

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
  catch { return iso; }
};

export default function AdminApprovals() {
  const { user: actor } = useAuth();
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  const [openUserId, setOpenUserId] = useState(null);
  const [pendingAction, setPendingAction] = useState(null);
  const [busyAction, setBusyAction] = useState(null);

  const load = useCallback(async () => {
    setLoading(true); setErr(null);
    try {
      const { data } = await api.get("/admin/portal/approvals?limit=100");
      setItems(data.items);
    } catch (e) {
      setErr(e?.response?.data?.detail || "Failed to load approvals.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleAction = (action) => {
    if (!openUserId) return;
    if (action === "approve") {
      setPendingAction({
        id: openUserId, action,
        label: "Approve user",
        description: "Sets role_status to active.",
        confirmLabel: "Approve",
      });
    } else if (action === "reject") {
      setPendingAction({
        id: openUserId, action,
        label: "Reject user",
        description: "Soft-reject the application. The account stays for audit history.",
        noteLabel: "Reason / note",
        noteRequired: true,
        confirmLabel: "Reject",
      });
    } else if (action === "request-info") {
      setPendingAction({
        id: openUserId, action,
        label: "Request more info",
        description: "Sets an info-requested timestamp + note on the user. Status stays pending_review.",
        noteLabel: "What do you need from them?",
        noteRequired: true,
        confirmLabel: "Send",
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
      setOpenUserId(null);
      await load();
    } catch (e) {
      setErr(e?.response?.data?.detail || "Action failed.");
    } finally {
      setBusyAction(null);
    }
  };

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-approvals-page">
      <div className="mb-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal · Approvals
        </div>
        <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">Pending approvals</h1>
        <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
          Marketplace signups waiting for platform-admin review. All
          decisions are audit-logged with the actor, target, before/after
          status, and whether a reviewer note was provided.
        </p>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-approvals-error">
          {err}
        </div>
      )}

      <div className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
        {loading && !items && (
          <div className="p-6 space-y-3" data-testid="admin-approvals-loading">
            {[0,1,2,3].map((i) => <div key={i} className="h-9 bg-equinesync-graphite/5 rounded animate-pulse" />)}
          </div>
        )}
        {!loading && items && items.length === 0 && (
          <div className="p-10 text-center text-[13px] text-equinesync-graphite/55" data-testid="admin-approvals-empty">
            Inbox zero — no users currently awaiting review.
          </div>
        )}
        {items && items.length > 0 && (
          <table className="w-full text-[13px]" data-testid="admin-approvals-table">
            <thead className="bg-equinesync-frost border-b border-equinesync-graphite/10">
              <tr className="text-left text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
                <th className="px-4 py-3 font-medium">Applicant</th>
                <th className="px-4 py-3 font-medium">Role</th>
                <th className="px-4 py-3 font-medium hidden md:table-cell">Signed up</th>
                <th className="px-4 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {items.map((u) => (
                <tr
                  key={u.id}
                  data-testid={`admin-approvals-row-${u.id}`}
                  onClick={() => setOpenUserId(u.id)}
                  className="border-b border-equinesync-graphite/5 last:border-b-0 hover:bg-equinesync-frost cursor-pointer"
                >
                  <td className="px-4 py-3">
                    <div className="text-equinesync-graphite font-medium">{u.full_name || "—"}</div>
                    <div className="text-equinesync-graphite/55 text-[11.5px]">{u.email}</div>
                  </td>
                  <td className="px-4 py-3 text-equinesync-graphite/75">{u.role || "—"}</td>
                  <td className="px-4 py-3 text-equinesync-graphite/65 hidden md:table-cell">
                    {formatTs(u.created_at)}
                  </td>
                  <td className="px-4 py-3">
                    <UserStatusBadge value={u.role_status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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
