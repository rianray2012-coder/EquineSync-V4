import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, FileSignature, PenLine, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["draft", "sent", "signed", "expired"];
const STATUS_TONE = { draft: "neutral", sent: "warning", signed: "success", expired: "critical" };
const ADD_FIELDS = [
  { key: "form_name", label: "Form", required: true, placeholder: "Form name", full: true },
  { key: "recipient_name", label: "Recipient", placeholder: "Recipient name" },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "signature_provider", label: "Provider", kind: "select", opts: ["internal", "docusign_ready"] },
  { key: "signed_at", label: "Signed at", type: "date" },
];

export default function FormsSignatures() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/forms-signatures");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load forms.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const stats = useMemo(() => Object.fromEntries(STATUSES.map((status) => [
    status,
    records.filter((record) => ((record.data || {}).status || "draft") === status).length,
  ])), [records]);

  const setStatus = async (record, status) => {
    setSavingId(record.id);
    const data = { status };
    if (status === "signed") data.signed_at = new Date().toISOString().slice(0, 10);
    try {
      await api.patch(`/feature-modules/forms-signatures/records/${record.id}`, { data });
      toast.success("Form updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update form");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/forms-signatures/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive form");
    }
  };

  return (
    <div data-testid="forms-signatures-page">
      <PageHeader
        eyebrow="Communication"
        title="Forms & Signatures"
        subtitle="Track digital forms, recipients, signature-provider readiness, and signing status."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="forms-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="forms-add">
              <Plus className="w-4 h-4" /> Add form
            </button>
          </div>
        }
      />

      <Card hover={false} className="mb-6 border-equine-brass/30 bg-equine-brass/5">
        <div className="flex items-start gap-3">
          <FileSignature className="w-4 h-4 text-equine-champagne mt-0.5 flex-shrink-0" />
          <div className="text-[13px] text-equine-inkMuted leading-relaxed">
            Signature providers are configuration-ready. This screen tracks workflow state until a live e-signature integration is configured.
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {STATUSES.map((status) => (
          <Card key={status} hover={false} className="p-4">
            <div className="label-eyebrow-muted mb-2 capitalize">{status}</div>
            <div className="flex items-end justify-between gap-3">
              <div className="font-display text-4xl text-equine-ink leading-none">{stats[status]}</div>
              <StatusPill tone={STATUS_TONE[status]}>{status}</StatusPill>
            </div>
          </Card>
        ))}
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading forms…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Forms unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <PenLine strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No forms tracked</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a waiver, release, boarding document, or signature request.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="forms-empty-add">
            <Plus className="w-4 h-4" /> Add first form
          </button>
        </Empty>
      ) : (
        <Card hover={false} data-testid="forms-list">
          <div className="space-y-3">
            {records.map((record) => {
              const data = record.data || {};
              const status = data.status || "draft";
              return (
                <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`form-row-${record.id}`}>
                  <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="font-display text-2xl text-equine-ink truncate">{data.form_name}</div>
                      <div className="text-[12.5px] text-equine-inkMuted">
                        {data.recipient_name || "Recipient TBD"} · {(data.signature_provider || "internal").replace(/_/g, " ")}
                      </div>
                      {data.signed_at && <div className="text-[12px] text-equine-sage mt-1">Signed {fmtDate(data.signed_at)}</div>}
                    </div>
                    <StatusPill tone={STATUS_TONE[status]}>{status}</StatusPill>
                    <div className="flex flex-wrap items-center gap-2">
                      {status === "draft" && <button type="button" onClick={() => setStatus(record, "sent")} className="btn-secondary text-[12px] py-2 px-4">Send</button>}
                      {status === "sent" && <button type="button" onClick={() => setStatus(record, "signed")} className="btn-primary text-[12px] py-2 px-4">Mark signed</button>}
                      {status !== "expired" && status !== "signed" && <button type="button" onClick={() => setStatus(record, "expired")} className="btn-secondary text-[12px] py-2 px-4">Expire</button>}
                      <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink px-2">Archive</button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add form"
        eyebrow="Communication"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/forms-signatures/records"
        initialValues={{ status: "draft", signature_provider: "internal" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save form"
        testidPrefix="forms-add"
        onCreated={load}
      />
    </div>
  );
}
