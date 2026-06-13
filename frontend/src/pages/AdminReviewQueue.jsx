import React, { useCallback, useEffect, useState } from "react";
import { api } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { Navigate } from "react-router-dom";
import { CheckCircle2, XCircle, Clock, ShieldX, AlertCircle, Loader2 } from "lucide-react";

const ROLE_LABEL = {
  trainer: "Trainer",
  barn_owner: "Barn / Facility",
  service_provider: "Service Provider",
  horse_owner: "Horse Owner",
  rider: "Rider",
};

export default function AdminReviewQueue() {
  const { user } = useAuth();
  const isAdmin = ["admin", "barn_manager"].includes(user?.role);

  const [tab, setTab] = useState("pending"); // pending | history
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busyId, setBusyId] = useState(null);
  const [rejectingId, setRejectingId] = useState(null);
  const [rejectReason, setRejectReason] = useState("");

  const fetchData = useCallback(async () => {
    if (!isAdmin) return;
    try {
      const url = tab === "pending" ? "/admin/review-queue" : "/admin/review-queue/history";
      const { data } = await api.get(url);
      setItems(data.items || []);
      setError("");
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not load review queue.");
    } finally {
      setLoading(false);
    }
  }, [isAdmin, tab]);

  useEffect(() => {
    setLoading(true);
    fetchData();
  }, [fetchData]);

  if (!user) return <Navigate to="/login" replace />;
  if (!isAdmin) {
    return (
      <div className="max-w-md mt-20 mx-auto text-center" data-testid="admin-review-forbidden">
        <ShieldX className="w-12 h-12 mx-auto text-equine-saddle mb-4" />
        <h1 className="font-display text-3xl text-equine-ivory mb-2">Admin access only</h1>
        <p className="text-equine-platinum/70 text-[14px]">This page is restricted to admins and barn managers.</p>
      </div>
    );
  }

  const approve = async (id) => {
    setBusyId(id);
    try {
      await api.post(`/admin/review-queue/${id}/approve`);
      await fetchData();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not approve.");
    } finally {
      setBusyId(null);
    }
  };

  const submitReject = async (id) => {
    setBusyId(id);
    try {
      await api.post(`/admin/review-queue/${id}/reject`, { reason: rejectReason });
      setRejectingId(null);
      setRejectReason("");
      await fetchData();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not reject.");
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div className="max-w-5xl" data-testid="admin-review-queue">
      <div className="mb-8">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle font-medium mb-2">Admin</div>
        <h1 className="font-display text-4xl text-equine-ivory mb-1">Review queue</h1>
        <p className="text-equine-platinum/70 text-[14px]">
          Approve or reject professionals (trainers, barns, service providers) who applied via the public signup.
        </p>
      </div>

      <div className="flex items-center gap-1 mb-6 border-b border-white/10">
        {[
          { id: "pending", label: "Pending", icon: Clock },
          { id: "history", label: "History", icon: CheckCircle2 },
        ].map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex items-center gap-2 px-4 py-3 text-[13px] tracking-wide transition-colors border-b-2 -mb-px ${
              tab === t.id
                ? "border-equine-saddle text-equine-ivory"
                : "border-transparent text-equine-platinum/60 hover:text-equine-ivory"
            }`}
            data-testid={`review-tab-${t.id}`}
          >
            <t.icon className="w-3.5 h-3.5" /> {t.label}
          </button>
        ))}
      </div>

      {loading && (
        <div className="flex items-center gap-2 text-equine-platinum/60 text-[13px] py-12">
          <Loader2 className="w-4 h-4 animate-spin" /> Loading…
        </div>
      )}

      {error && (
        <div className="text-equine-clay text-[13px] mb-4 flex items-center gap-2" data-testid="review-error">
          <AlertCircle className="w-4 h-4" /> {error}
        </div>
      )}

      {!loading && !items.length && (
        <div className="text-equine-platinum/50 text-[14px] py-16 text-center" data-testid="review-empty">
          {tab === "pending" ? "No applications waiting on you." : "No decisions on record yet."}
        </div>
      )}

      <div className="space-y-3" data-testid="review-list">
        {items.map((u) => {
          const decided = u.role_status === "approved" || u.role_status === "rejected";
          return (
            <div
              key={u.id}
              className="border border-white/10 rounded-xl p-5 bg-equine-navy/30 flex flex-col md:flex-row md:items-center gap-4"
              data-testid={`review-item-${u.id}`}
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 mb-1">
                  <div className="font-display text-lg text-equine-ivory">{u.full_name || u.email}</div>
                  <span className="text-[10px] tracking-[0.2em] uppercase text-equine-saddle bg-equine-saddle/10 border border-equine-saddle/30 px-2 py-0.5 rounded-full">
                    {ROLE_LABEL[u.role] || u.role}
                  </span>
                  {decided && (
                    <span
                      className={`text-[10px] tracking-[0.2em] uppercase px-2 py-0.5 rounded-full border ${
                        u.role_status === "approved"
                          ? "border-green-400/40 text-green-300 bg-green-400/10"
                          : "border-red-400/40 text-red-300 bg-red-400/10"
                      }`}
                      data-testid={`review-status-${u.id}`}
                    >
                      {u.role_status}
                    </span>
                  )}
                </div>
                <div className="text-[12.5px] text-equine-platinum/65 truncate">{u.email}</div>
                {(u.phone || u.location) && (
                  <div className="text-[12px] text-equine-platinum/50 mt-1">
                    {[u.location, u.phone].filter(Boolean).join(" · ")}
                  </div>
                )}
                {u.profile && Object.keys(u.profile).length > 0 && (
                  <div className="text-[12px] text-equine-platinum/60 mt-2 italic">
                    {Object.entries(u.profile)
                      .filter(([, v]) => !!v)
                      .slice(0, 3)
                      .map(([k, v]) => `${k.replace(/_/g, " ")}: ${v}`)
                      .join(" · ")}
                  </div>
                )}
                {u.review_rejection_reason && (
                  <div className="text-[12px] text-red-300/80 mt-2">Reason: {u.review_rejection_reason}</div>
                )}
                {u.review_decided_at && (
                  <div className="text-[11px] text-equine-platinum/40 mt-1">
                    Decided {new Date(u.review_decided_at).toLocaleString()}
                  </div>
                )}
              </div>

              {!decided && (
                <div className="flex items-center gap-2 shrink-0">
                  {rejectingId === u.id ? (
                    <div className="flex items-center gap-2 flex-wrap">
                      <input
                        autoFocus
                        value={rejectReason}
                        onChange={(e) => setRejectReason(e.target.value)}
                        placeholder="Reason (optional)"
                        className="bg-equine-navyDeep/50 border border-white/10 text-equine-ivory placeholder:text-white/30 px-3 py-2 rounded-lg text-[12px] focus:outline-none focus:border-equine-saddle/60"
                        data-testid={`reject-reason-${u.id}`}
                      />
                      <button
                        onClick={() => submitReject(u.id)}
                        disabled={busyId === u.id}
                        className="bg-red-500/80 text-white hover:bg-red-500 disabled:opacity-40 transition-colors px-3 py-2 rounded-lg text-[12px] font-medium"
                        data-testid={`confirm-reject-${u.id}`}
                      >
                        Confirm reject
                      </button>
                      <button
                        onClick={() => { setRejectingId(null); setRejectReason(""); }}
                        className="text-equine-platinum/60 hover:text-equine-ivory text-[12px] px-2 py-2"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <>
                      <button
                        onClick={() => approve(u.id)}
                        disabled={busyId === u.id}
                        className="bg-equine-saddle text-equine-navyDeep hover:bg-white disabled:opacity-40 transition-colors px-4 py-2 rounded-full text-[12.5px] tracking-wide font-medium inline-flex items-center gap-1.5"
                        data-testid={`approve-${u.id}`}
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" /> Approve
                      </button>
                      <button
                        onClick={() => setRejectingId(u.id)}
                        disabled={busyId === u.id}
                        className="border border-white/15 text-equine-platinum hover:text-equine-ivory hover:border-white/30 disabled:opacity-40 transition-colors px-4 py-2 rounded-full text-[12.5px] tracking-wide font-medium inline-flex items-center gap-1.5"
                        data-testid={`reject-${u.id}`}
                      >
                        <XCircle className="w-3.5 h-3.5" /> Reject
                      </button>
                    </>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
