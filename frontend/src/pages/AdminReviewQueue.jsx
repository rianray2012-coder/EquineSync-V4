import React, { useCallback, useEffect, useState } from "react";
import { api } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { CheckCircle2, XCircle, Clock, AlertCircle, Loader2, KeyRound, X } from "lucide-react";

const ROLE_LABEL = {
  trainer: "Trainer",
  barn_owner: "Barn / Facility",
  service_provider: "Service Provider",
  horse_owner: "Horse Owner",
  rider: "Rider",
};

// Phase 15.E — roles that are candidates for facility-access elevation.
// `barn_manager` and `admin` already have `barn:manage`, so the button is
// hidden for them.
const ELEVATION_ELIGIBLE_ROLES = new Set([
  "barn_owner", "trainer", "service_provider",
]);

export default function AdminReviewQueue() {
  const { user } = useAuth();
  // Route-level RoleProtected (App.js) already gates non-admins to the
  // generic Forbidden page — no in-page guard needed.

  const [tab, setTab] = useState("pending"); // pending | history
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busyId, setBusyId] = useState(null);
  const [rejectingId, setRejectingId] = useState(null);
  const [rejectReason, setRejectReason] = useState("");
  // Phase 15.E — grant-facility-access modal state.
  const [grantingUser, setGrantingUser] = useState(null);

  const fetchData = useCallback(async () => {
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
  }, [tab]);

  useEffect(() => {
    setLoading(true);
    fetchData();
  }, [fetchData]);

  if (!user) return null;

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
        <div className="text-[11px] tracking-[0.28em] uppercase text-equine-lilac font-medium mb-2">Admin</div>
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
                ? "border-equine-lilac text-equine-ivory"
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
          return renderRow(u, decided);
        })}
      </div>

      {grantingUser && (
        <GrantFacilityAccessModal
          target={grantingUser}
          onClose={() => setGrantingUser(null)}
          onGranted={async () => {
            setGrantingUser(null);
            await fetchData();
          }}
        />
      )}
    </div>
  );

  function renderRow(u, decided) {
    return (
            <div
              key={u.id}
              className="border border-white/10 rounded-xl p-5 bg-equine-navy/30 flex flex-col md:flex-row md:items-center gap-4"
              data-testid={`review-item-${u.id}`}
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 mb-1">
                  <div className="font-display text-lg text-equine-ivory">{u.full_name || u.email}</div>
                  <span className="text-[10px] tracking-[0.2em] uppercase text-equine-lilac bg-equine-lilac/10 border border-equine-lilac/30 px-2 py-0.5 rounded-full">
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
                {u.role === "barn_manager" && u.barn_id && (
                  <div className="text-[11px] text-equine-lilac/80 mt-1" data-testid={`facility-granted-${u.id}`}>
                    Facility access granted · barn {u.barn_id}
                  </div>
                )}
              </div>

              {decided
                && u.role_status === "approved"
                && ELEVATION_ELIGIBLE_ROLES.has(u.role) && (
                <div className="shrink-0">
                  <button
                    onClick={() => setGrantingUser(u)}
                    disabled={busyId === u.id}
                    data-testid={`grant-facility-${u.id}`}
                    className="border border-equine-lilac/40 text-equine-lilac hover:bg-equine-lilac/10 disabled:opacity-40 transition-colors px-4 py-2 rounded-full text-[12.5px] tracking-wide font-medium inline-flex items-center gap-1.5"
                  >
                    <KeyRound className="w-3.5 h-3.5" /> Grant facility access
                  </button>
                </div>
              )}

              {!decided && (
                <div className="flex items-center gap-2 shrink-0">
                  {rejectingId === u.id ? (
                    <div className="flex items-center gap-2 flex-wrap">
                      <input
                        autoFocus
                        value={rejectReason}
                        onChange={(e) => setRejectReason(e.target.value)}
                        placeholder="Reason (optional)"
                        className="bg-equine-navyDeep/50 border border-white/10 text-equine-ivory placeholder:text-white/30 px-3 py-2 rounded-lg text-[12px] focus:outline-none focus:border-equine-lilac/60"
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
                        className="bg-equine-lilac text-equine-navyDeep hover:bg-white disabled:opacity-40 transition-colors px-4 py-2 rounded-full text-[12.5px] tracking-wide font-medium inline-flex items-center gap-1.5"
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
  }
}


function GrantFacilityAccessModal({ target, onClose, onGranted }) {
  const [mode, setMode] = useState("existing"); // "existing" | "create"
  const [barns, setBarns] = useState([]);
  const [barnQuery, setBarnQuery] = useState("");
  const [selectedBarnId, setSelectedBarnId] = useState("");
  const [newBarnName, setNewBarnName] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    let cancelled = false;
    const params = barnQuery.trim() ? `?q=${encodeURIComponent(barnQuery.trim())}` : "";
    api.get(`/admin/barns${params}`)
      .then((r) => { if (!cancelled) setBarns(r.data.items || []); })
      .catch(() => { /* silent */ });
    return () => { cancelled = true; };
  }, [barnQuery]);

  const submit = async () => {
    setErr("");
    setSubmitting(true);
    try {
      const body = mode === "create"
        ? { create_new_barn: true, new_barn_name: newBarnName.trim() }
        : { barn_id: selectedBarnId };
      await api.post(`/admin/users/${target.id}/grant-facility-access`, body);
      await onGranted();
    } catch (e) {
      setErr(e?.response?.data?.detail || "Could not grant facility access.");
    } finally {
      setSubmitting(false);
    }
  };

  const canSubmit = mode === "existing"
    ? !!selectedBarnId
    : newBarnName.trim().length > 0;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-equine-navyDeep/60"
      data-testid="grant-facility-modal"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-lg bg-equine-navy border border-white/10 rounded-2xl p-7 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          data-testid="grant-facility-close"
          className="absolute top-4 right-4 p-2 rounded-full text-equine-platinum/60 hover:text-equine-ivory hover:bg-white/5"
        >
          <X className="w-4 h-4" />
        </button>
        <div className="text-[11px] tracking-[0.28em] uppercase text-equine-lilac font-medium mb-3">Grant facility access</div>
        <div className="font-display text-2xl text-equine-ivory mb-1">{target.full_name || target.email}</div>
        <div className="text-[12.5px] text-equine-platinum/60 mb-5">
          Elevates role from <span className="text-equine-platinum">{ROLE_LABEL[target.role] || target.role}</span> to
          <span className="text-equine-lilac"> Barn Manager</span>. Audited.
        </div>

        <div className="inline-flex bg-white/5 border border-white/10 rounded-full p-0.5 mb-5">
          <button
            type="button"
            onClick={() => setMode("existing")}
            data-testid="grant-mode-existing"
            className={`px-4 py-1.5 text-[12px] rounded-full ${mode === "existing" ? "bg-equine-lilac text-equine-navyDeep" : "text-equine-platinum/65 hover:text-equine-ivory"}`}
          >
            Pick existing
          </button>
          <button
            type="button"
            onClick={() => setMode("create")}
            data-testid="grant-mode-create"
            className={`px-4 py-1.5 text-[12px] rounded-full ${mode === "create" ? "bg-equine-lilac text-equine-navyDeep" : "text-equine-platinum/65 hover:text-equine-ivory"}`}
          >
            Create new
          </button>
        </div>

        {mode === "existing" && (
          <div className="space-y-3" data-testid="grant-existing-form">
            <input
              type="text"
              value={barnQuery}
              onChange={(e) => setBarnQuery(e.target.value)}
              placeholder="Search barn by id or name"
              className="w-full bg-equine-navyDeep/50 border border-white/10 text-equine-ivory placeholder:text-white/30 px-3 py-2 rounded-lg text-[13px] focus:outline-none focus:border-equine-lilac/60"
              data-testid="grant-barn-search"
            />
            <div className="max-h-56 overflow-y-auto border border-white/10 rounded-lg divide-y divide-white/5" data-testid="grant-barn-list">
              {barns.length === 0 && (
                <div className="text-[12px] text-equine-platinum/50 px-3 py-4" data-testid="grant-barn-list-empty">
                  No barns match. Try &ldquo;Create new&rdquo; instead.
                </div>
              )}
              {barns.map((b) => (
                <label
                  key={b.id}
                  className={`flex items-center gap-3 px-3 py-2 cursor-pointer text-[12.5px] ${selectedBarnId === b.id ? "bg-equine-lilac/10" : "hover:bg-white/5"}`}
                  data-testid={`grant-barn-option-${b.id}`}
                >
                  <input
                    type="radio"
                    name="barn"
                    value={b.id}
                    checked={selectedBarnId === b.id}
                    onChange={() => setSelectedBarnId(b.id)}
                  />
                  <div>
                    <div className="text-equine-ivory">{b.name || b.id}</div>
                    <div className="text-equine-platinum/50 text-[11px]">{b.id}</div>
                  </div>
                </label>
              ))}
            </div>
          </div>
        )}

        {mode === "create" && (
          <div data-testid="grant-create-form">
            <input
              type="text"
              autoFocus
              value={newBarnName}
              onChange={(e) => setNewBarnName(e.target.value)}
              placeholder="New barn name"
              className="w-full bg-equine-navyDeep/50 border border-white/10 text-equine-ivory placeholder:text-white/30 px-3 py-2 rounded-lg text-[13px] focus:outline-none focus:border-equine-lilac/60"
              data-testid="grant-new-barn-name"
            />
            <div className="text-[11.5px] text-equine-platinum/50 mt-2">
              A new barn record is created and the user is set as its Barn Manager.
            </div>
          </div>
        )}

        {err && <div className="text-equine-clay text-[12.5px] mt-4" data-testid="grant-facility-error">{err}</div>}

        <div className="mt-6 flex items-center justify-end gap-2">
          <button
            onClick={onClose}
            className="text-equine-platinum/60 hover:text-equine-ivory text-[12.5px] px-3 py-2"
          >Cancel</button>
          <button
            onClick={submit}
            disabled={!canSubmit || submitting}
            data-testid="grant-facility-submit"
            className="bg-equine-lilac text-equine-navyDeep hover:bg-white disabled:opacity-40 disabled:cursor-not-allowed transition-colors px-5 py-2 rounded-full text-[12.5px] tracking-wide font-medium inline-flex items-center gap-1.5"
          >
            {submitting ? "Granting…" : "Grant access"}
          </button>
        </div>
      </div>
    </div>
  );
}
