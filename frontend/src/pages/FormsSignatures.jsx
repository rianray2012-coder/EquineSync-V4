import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, FileSignature, PenLine, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["draft", "sent", "signed", "expired"];
const STATUS_TONE = { draft: "neutral", sent: "warning", signed: "success", expired: "critical" };
const DISPLAY_LABELS = { draft: "draft", sent: "ready locally", signed: "acknowledged locally", expired: "expired" };
const ADD_FIELDS = [
  { key: "form_name", label: "Form", required: true, placeholder: "Form name", full: true },
  { key: "recipient_name", label: "Recipient", placeholder: "Recipient name" },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "signature_provider", label: "Provider", kind: "select", opts: ["internal", "docusign_ready"] },
  { key: "signed_at", label: "Signed at", type: "date" },
];
const TEMPLATE_STATUS = ["draft", "active", "archived"];
const MINOR_STATUSES = ["adult", "minor_13_to_17", "under_13", "unknown"];

export default function FormsSignatures() {
  const [records, setRecords] = useState([]);
  const [documentTypes, setDocumentTypes] = useState({});
  const [templates, setTemplates] = useState([]);
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [templateOpen, setTemplateOpen] = useState(false);
  const [requestOpen, setRequestOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);
  const [providerReadiness, setProviderReadiness] = useState(null);

  const loadDocumentWorkflow = useCallback(async () => {
    try {
      const [typesRes, templatesRes, requestsRes] = await Promise.all([
        api.get("/document-signatures/document-types"),
        api.get("/document-signatures/templates"),
        api.get("/document-signatures/requests"),
      ]);
      setDocumentTypes(typesRes.data.document_types || {});
      setTemplates(templatesRes.data.templates || []);
      setRequests(requestsRes.data.requests || []);
    } catch {
      setDocumentTypes({});
      setTemplates([]);
      setRequests([]);
    }
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [r] = await Promise.all([
        api.get("/feature-modules/forms-signatures"),
        loadDocumentWorkflow(),
      ]);
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load forms.");
    } finally {
      setLoading(false);
    }
  }, [loadDocumentWorkflow]);

  useEffect(() => { load(); }, [load]);

  useEffect(() => {
    api.get("/document-signatures/providers")
      .then((r) => setProviderReadiness(r.data))
      .catch(() => setProviderReadiness(null));
  }, []);

  const stats = useMemo(() => Object.fromEntries(STATUSES.map((status) => [
    status,
    records.filter((record) => ((record.data || {}).status || "draft") === status).length,
  ])), [records]);
  const documentTypeOptions = useMemo(() => Object.keys(documentTypes).sort(), [documentTypes]);
  const templateOptions = useMemo(() => templates.map((template) => template.id), [templates]);

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
        subtitle="Track local acknowledgement records, recipients, signature-provider readiness, and status without claiming live legal delivery."
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

      <Card hover={false} className="mb-6 border-equine-icy/30 bg-equine-icy/5">
        <div className="flex items-start gap-3">
          <FileSignature className="w-4 h-4 text-equine-lilac mt-0.5 flex-shrink-0" />
          <div className="text-[13px] text-equine-inkMuted leading-relaxed">
            Signature providers use a hybrid model: legal signatures route to a third-party provider, while lower-risk acknowledgements stay internal.
            {providerReadiness?.legal_signature_provider && (
              <span className="block mt-2">
                {providerReadiness.legal_signature_provider.label}:{" "}
                <span className="font-semibold text-equine-ink">
                  {providerReadiness.legal_signature_provider.configured ? "credentials ready" : "credentials needed"}
                </span>
                . Envelope sending appears only after the signature provider is enabled for this account.
              </span>
            )}
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-5 mb-6" data-testid="document-workflow-foundation">
        <Card hover={false}>
          <div className="flex items-start justify-between gap-4 mb-4">
            <div>
              <div className="label-eyebrow-muted mb-1">Local template registry</div>
              <div className="font-display text-2xl text-equine-ink">Document templates</div>
              <div className="text-[12.5px] text-equine-inkMuted mt-1">Local setup only. Provider template IDs may be stored, but no envelope is sent.</div>
            </div>
            <button onClick={() => setTemplateOpen(true)} className="btn-secondary inline-flex items-center gap-2" data-testid="document-template-add">
              <Plus className="w-4 h-4" /> Template
            </button>
          </div>
          {templates.length === 0 ? (
            <div className="text-[13px] text-equine-inkMuted py-4">No document templates registered yet.</div>
          ) : (
            <div className="space-y-3">
              {templates.slice(0, 5).map((template) => (
                <div key={template.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-3">
                  <div className="flex items-center justify-between gap-3">
                    <div className="min-w-0">
                      <div className="font-medium text-equine-ink truncate">{template.display_name}</div>
                      <div className="text-[12px] text-equine-inkMuted truncate">{template.document_type} · {template.workflow_kind}</div>
                    </div>
                    <StatusPill tone="neutral">{template.status}</StatusPill>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>

        <Card hover={false}>
          <div className="flex items-start justify-between gap-4 mb-4">
            <div>
              <div className="label-eyebrow-muted mb-1">Soft-warning request tracking</div>
              <div className="font-display text-2xl text-equine-ink">Document requests</div>
              <div className="text-[12.5px] text-equine-inkMuted mt-1">Creates local requests and signer-role requirements only. No signing link is generated.</div>
            </div>
            <button onClick={() => setRequestOpen(true)} disabled={templates.length === 0} className="btn-secondary inline-flex items-center gap-2 disabled:opacity-50" data-testid="document-request-add">
              <Plus className="w-4 h-4" /> Request
            </button>
          </div>
          {requests.length === 0 ? (
            <div className="text-[13px] text-equine-inkMuted py-4">No document requests created yet.</div>
          ) : (
            <div className="space-y-3">
              {requests.slice(0, 5).map((request) => (
                <div key={request.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-3">
                  <div className="flex items-center justify-between gap-3">
                    <div className="min-w-0">
                      <div className="font-medium text-equine-ink truncate">{request.display_name}</div>
                      <div className="text-[12px] text-equine-inkMuted truncate">
                        {request.minor_status || "unknown"} · {request.required_signer_count || 0} required signer(s)
                      </div>
                    </div>
                    <StatusPill tone="warning">{request.status}</StatusPill>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {STATUSES.map((status) => (
          <Card key={status} hover={false} className="p-4">
            <div className="label-eyebrow-muted mb-2 capitalize">{status}</div>
            <div className="flex items-end justify-between gap-3">
              <div className="font-display text-4xl text-equine-ink leading-none">{stats[status]}</div>
              <StatusPill tone={STATUS_TONE[status]}>{DISPLAY_LABELS[status] || status}</StatusPill>
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
          <PenLine strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
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
                    <StatusPill tone={STATUS_TONE[status]}>{DISPLAY_LABELS[status] || status}</StatusPill>
                    <div className="flex flex-wrap items-center gap-2">
                      {status === "draft" && <button type="button" onClick={() => setStatus(record, "sent")} className="btn-secondary text-[12px] py-2 px-4">Mark ready locally</button>}
                      {status === "sent" && <button type="button" onClick={() => setStatus(record, "signed")} className="btn-primary text-[12px] py-2 px-4">Record acknowledgement</button>}
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
      <QuickAddSheet
        open={templateOpen}
        onClose={() => setTemplateOpen(false)}
        title="Register document template"
        eyebrow="Documents"
        fields={[
          { key: "document_type", label: "Document type", kind: "select", opts: documentTypeOptions, required: true, full: true },
          { key: "provider_template_id", label: "Provider template ID", placeholder: "Optional local reference", full: true },
          { key: "version", label: "Version", type: "number" },
          { key: "status", label: "Status", kind: "select", opts: TEMPLATE_STATUS },
        ]}
        endpoint="/document-signatures/templates"
        initialValues={{ version: 1, status: "draft" }}
        submitLabel="Save template"
        testidPrefix="document-template-add"
        onCreated={loadDocumentWorkflow}
      />
      <QuickAddSheet
        open={requestOpen}
        onClose={() => setRequestOpen(false)}
        title="Create document request"
        eyebrow="Documents"
        fields={[
          { key: "template_id", label: "Template", kind: "select", opts: templateOptions, required: true, full: true },
          { key: "subject_user_id", label: "Subject user ID", placeholder: "Optional when using student profile", full: true },
          { key: "subject_student_profile_id", label: "Student profile ID", placeholder: "Optional when using user ID", full: true },
          { key: "minor_status", label: "Minor status", kind: "select", opts: MINOR_STATUSES },
          { key: "guardian_user_ids", label: "Guardian user IDs", placeholder: "Comma-separated, if required", full: true },
          { key: "facility_countersigner_user_id", label: "Facility countersigner", placeholder: "Optional user ID", full: true },
          { key: "expires_at", label: "Expires at", type: "date" },
          { key: "note", label: "Private note present", rows: 2, full: true },
        ]}
        endpoint="/document-signatures/requests"
        initialValues={{ minor_status: "unknown" }}
        transform={(form) => ({
          ...form,
          guardian_user_ids: String(form.guardian_user_ids || "")
            .split(",")
            .map((item) => item.trim())
            .filter(Boolean),
        })}
        submitLabel="Create request"
        testidPrefix="document-request-add"
        onCreated={loadDocumentWorkflow}
      />
    </div>
  );
}
