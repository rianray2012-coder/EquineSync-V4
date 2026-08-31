import React, { useEffect, useState } from "react";
import { api, fmtDate } from "../lib/api";
import { useAuth } from "../context/AuthContext";

const STATUS_COPY = {
  owner_approved: "Owner approved",
  barn_approved: "Barn approved",
  pending_acceptance: "Pending acceptance",
  accepted: "Accepted",
  canceled: "Canceled",
};

function TransferCard({ transfer, onAccepted, canBarnApprove }) {
  const [preview, setPreview] = useState(null);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState(null);

  const loadPreview = async () => {
    setLoadingPreview(true);
    setError(null);
    try {
      const response = await api.get(`/horse-transfers/${transfer.id}/export-preview`);
      setPreview(response.data);
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not load transfer preview.");
    } finally {
      setLoadingPreview(false);
    }
  };

  const barnApprove = async () => {
    setWorking(true);
    setError(null);
    try {
      await api.post(`/horse-transfers/${transfer.id}/barn-approve`, {});
      onAccepted();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not approve transfer.");
    } finally {
      setWorking(false);
    }
  };

  const accept = async () => {
    setWorking(true);
    setError(null);
    try {
      await api.post(`/horse-transfers/${transfer.id}/accept`, {});
      onAccepted();
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not accept transfer.");
    } finally {
      setWorking(false);
    }
  };

  return (
    <article
      data-testid={`horse-transfer-card-${transfer.id}`}
      className="rounded-lg border border-equine-silver/10 bg-equine-black/40 p-4"
    >
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
        <div className="min-w-0">
          <div className="label-eyebrow">Horse passport</div>
          <div className="text-[18px] font-serif text-equine-silver mt-1 break-words">
            {transfer.horse_id}
          </div>
          <div className="text-[12px] text-equine-platinum/60 mt-2">
            {[STATUS_COPY[transfer.status] || transfer.status, fmtDate(transfer.created_at)].filter(Boolean).join(" · ")}
          </div>
        </div>
        <div className="flex flex-col sm:flex-row gap-2">
          <button
            type="button"
            onClick={loadPreview}
            disabled={loadingPreview || working}
            data-testid={`horse-transfer-preview-${transfer.id}`}
            className="min-h-11 text-[11px] tracking-[0.18em] uppercase border border-equine-silver/20 text-equine-platinum/70 hover:text-equine-silver hover:bg-equine-silver/10 px-4 py-2 rounded disabled:opacity-40"
          >
            {loadingPreview ? "Loading…" : "Preview"}
          </button>
          {transfer.status === "owner_approved" && canBarnApprove ? (
            <button
              type="button"
              onClick={barnApprove}
              disabled={working}
              data-testid={`horse-transfer-barn-approve-${transfer.id}`}
              className="min-h-11 text-[11px] tracking-[0.18em] uppercase border border-equine-silver/20 text-equine-platinum/70 hover:text-equine-silver hover:bg-equine-silver/10 px-4 py-2 rounded disabled:opacity-40"
            >
              {working ? "Approving…" : "Barn Approve"}
            </button>
          ) : null}
          <button
            type="button"
            onClick={accept}
            disabled={working || transfer.status === "owner_approved"}
            data-testid={`horse-transfer-accept-${transfer.id}`}
            className="min-h-11 text-[11px] tracking-[0.18em] uppercase border border-equine-silver/30 bg-equine-silver/10 hover:bg-equine-silver/20 text-equine-silver px-4 py-2 rounded disabled:opacity-40"
          >
            {working ? "Accepting…" : "Accept"}
          </button>
        </div>
      </div>
      {preview ? (
        <section
          data-testid={`horse-transfer-preview-body-${transfer.id}`}
          className="mt-4 rounded border border-equine-silver/10 bg-equine-silver/5 p-3"
        >
          <div className="text-[12px] text-equine-platinum/70">
            {(preview.categories || []).join(", ")}
          </div>
          <pre className="mt-3 max-h-52 overflow-auto whitespace-pre-wrap text-[11px] text-equine-platinum/60">
            {JSON.stringify(preview, null, 2)}
          </pre>
        </section>
      ) : null}
      {error ? (
        <div
          data-testid={`horse-transfer-error-${transfer.id}`}
          className="mt-3 text-[12.5px] text-equine-platinum/85 border border-equine-silver/30 bg-equine-silver/5 px-3 py-2 rounded"
        >
          {error}
        </div>
      ) : null}
    </article>
  );
}

export default function HorseTransfers() {
  const { user } = useAuth();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const canBarnApprove = ["admin", "barn_manager"].includes((user?.role || "").toLowerCase());

  const refetch = () => {
    setLoading(true);
    setError(null);
    api.get("/horse-transfers/pending")
      .then((response) => {
        setItems(response.data?.items || []);
        setLoading(false);
      })
      .catch((e) => {
        setError(e?.response?.data?.detail || "Could not load transfers.");
        setLoading(false);
      });
  };

  useEffect(() => {
    refetch();
  }, []);

  if (loading) {
    return <div className="p-6 text-equine-platinum/55" data-testid="horse-transfers-loading">Loading…</div>;
  }
  if (error) {
    return <div className="p-6 text-equine-platinum/75" data-testid="horse-transfers-error">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-6" data-testid="horse-transfers-page">
      <header className="space-y-2">
        <div className="label-eyebrow">Horse passport</div>
        <h1 className="text-3xl sm:text-4xl font-serif text-equine-silver">Pending transfers</h1>
      </header>
      {items.length ? (
        <div className="grid gap-3">
          {items.map((transfer) => (
            <TransferCard
              key={transfer.id}
              transfer={transfer}
              onAccepted={refetch}
              canBarnApprove={canBarnApprove}
            />
          ))}
        </div>
      ) : (
        <section
          data-testid="horse-transfers-empty"
          className="rounded-lg border border-equine-silver/10 bg-equine-black/40 p-5 text-[13px] text-equine-platinum/65"
        >
          No pending horse passport transfers.
        </section>
      )}
    </div>
  );
}
