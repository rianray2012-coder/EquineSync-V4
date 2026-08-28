import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, FileText, RefreshCw, ShieldCheck } from "lucide-react";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";

const STATUS_TONE = {
  draft: "neutral",
  sent: "warning",
  viewed: "info",
  completed: "success",
  signed: "success",
  expired: "critical",
  declined: "critical",
  voided: "neutral",
  provider_attention: "warning",
};

const KIND_LABEL = {
  document_request: "Document request",
  local_acknowledgement: "Local acknowledgement",
};

const statusLabel = (status) => String(status || "pending").replace(/_/g, " ");

export default function OwnerDocuments() {
  const [documents, setDocuments] = useState([]);
  const [liveSigningEnabled, setLiveSigningEnabled] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get("/owner-portal/documents");
      setDocuments(response.data.documents || []);
      setLiveSigningEnabled(Boolean(response.data.live_signing_enabled));
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load documents.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const counts = useMemo(() => {
    const next = { pending: 0, completed: 0, expired: 0 };
    documents.forEach((doc) => {
      const status = doc.status || "pending";
      if (["completed", "signed"].includes(status)) next.completed += 1;
      else if (status === "expired") next.expired += 1;
      else next.pending += 1;
    });
    return next;
  }, [documents]);

  return (
    <div data-testid="owner-documents-page">
      <PageHeader
        eyebrow="Documents"
        title="My Documents"
        subtitle="Review document requests, acknowledgements, and completed status shared with your account."
        action={
          <button type="button" onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="owner-documents-refresh">
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        }
      />

      <Card hover={false} className="mb-6 border-equine-brass/30 bg-equine-brass/5">
        <div className="flex items-start gap-3">
          <ShieldCheck className="w-4 h-4 text-equine-champagne mt-0.5 flex-shrink-0" />
          <div className="text-[13px] text-equine-inkMuted leading-relaxed">
            This library shows owner-safe document status only. Legal signature sending and provider links remain unavailable unless separately enabled by the barn.
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <Metric label="Pending" value={counts.pending} tone="warning" />
        <Metric label="Completed" value={counts.completed} tone="success" />
        <Metric label="Expired" value={counts.expired} tone="critical" />
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading documents...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Documents unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : documents.length === 0 ? (
        <Empty>
          <FileText strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No documents shared yet</div>
          <div className="text-[13px] text-equine-platinum/60">Document requests and local acknowledgements will appear here when the barn shares them.</div>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5" data-testid="owner-documents-list">
          {documents.map((doc) => (
            <Card key={`${doc.kind}:${doc.id}`} hover={false} data-testid={`owner-document-card-${doc.id}`}>
              <div className="flex items-start justify-between gap-3 mb-4">
                <div className="min-w-0">
                  <div className="label-eyebrow-muted mb-1">{KIND_LABEL[doc.kind] || "Document"}</div>
                  <div className="font-display text-2xl text-equine-ink truncate">{doc.display_name || "Document"}</div>
                  <div className="text-[12.5px] text-equine-inkMuted capitalize">
                    {String(doc.document_type || "document").replace(/_/g, " ")}
                  </div>
                </div>
                <StatusPill tone={STATUS_TONE[doc.status] || "neutral"}>{statusLabel(doc.status)}</StatusPill>
              </div>

              <div className="space-y-2 text-[13px] text-equine-inkMuted">
                {doc.expires_at && <Detail label="Expires" value={fmtDate(doc.expires_at)} />}
                {doc.signed_at && <Detail label="Acknowledged" value={fmtDate(doc.signed_at)} />}
                {doc.required_signer_count > 0 && (
                  <Detail label="Signers" value={`${doc.signed_count || 0} of ${doc.required_signer_count} complete`} />
                )}
                <Detail label="Delivery" value={liveSigningEnabled ? "Provider enabled" : "Status only"} />
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

function Metric({ label, value, tone }) {
  return (
    <Card hover={false} className="p-4">
      <div className="label-eyebrow-muted mb-2">{label}</div>
      <div className="flex items-end justify-between gap-3">
        <div className="font-display text-4xl text-equine-ink leading-none">{value}</div>
        <StatusPill tone={tone}>{label.toLowerCase()}</StatusPill>
      </div>
    </Card>
  );
}

function Detail({ label, value }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <span>{label}</span>
      <span className="text-equine-ink text-right">{value}</span>
    </div>
  );
}
