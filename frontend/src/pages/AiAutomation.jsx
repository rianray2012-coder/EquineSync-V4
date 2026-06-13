import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, Plus, RefreshCw, Sparkles, XCircle } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const TYPES = ["care_summary", "health_risk", "schedule_reminder", "owner_update", "billing_recommendation"];
const STATUSES = ["draft", "reviewed", "approved", "dismissed"];
const STATUS_TONE = { draft: "info", reviewed: "warning", approved: "success", dismissed: "neutral" };

const ADD_FIELDS = [
  { key: "suggestion_type", label: "Type", kind: "select", opts: TYPES },
  { key: "subject", label: "Subject", required: true, placeholder: "Care summary subject", full: true },
  { key: "summary", label: "Summary", required: true, kind: "textarea", rows: 5, full: true },
  { key: "confidence", label: "Confidence", type: "number", placeholder: "Confidence score" },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
];

const labelFor = (value) => String(value || "").replace(/_/g, " ");

export default function AiAutomation() {
  const [records, setRecords] = useState([]);
  const [module, setModule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);
  const [generating, setGenerating] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/ai-automation");
      setModule(r.data.module);
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load AI automation.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const stats = useMemo(() => Object.fromEntries(STATUSES.map((status) => [
    status,
    records.filter((record) => ((record.data || {}).status || "draft") === status).length,
  ])), [records]);

  const sorted = useMemo(() => [...records].sort((a, b) => String(b.updated_at || "").localeCompare(String(a.updated_at || ""))), [records]);

  const setStatus = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/ai-automation/records/${record.id}`, { data: { status } });
      toast.success("Automation item updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update automation item");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/ai-automation/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive automation item");
    }
  };

  const generateDrafts = async () => {
    setGenerating(true);
    try {
      const r = await api.post("/automation/generate-drafts");
      const created = r.data.created || 0;
      const skipped = r.data.skipped || 0;
      if (created > 0) toast.success(`Generated ${created} draft${created === 1 ? "" : "s"} for review`);
      else toast.info(skipped > 0 ? "Today's drafts already exist" : "No draft suggestions generated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not generate automation drafts");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div data-testid="ai-automation-page">
      <PageHeader
        eyebrow="AI & Automation"
        title="AI Automation Review"
        subtitle="Review care summaries, health-risk alerts, owner updates, reporting notes, and billing recommendations before anything is approved."
        action={
          <div className="flex items-center gap-3">
            <button onClick={generateDrafts} disabled={generating} className="btn-secondary inline-flex items-center gap-2 disabled:opacity-50" data-testid="ai-automation-generate">
              <Sparkles className="w-4 h-4" /> {generating ? "Generating..." : "Generate drafts"}
            </button>
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="ai-automation-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="ai-automation-add">
              <Plus className="w-4 h-4" /> Add draft
            </button>
          </div>
        }
      />

      {module?.placeholder && (
        <Card hover={false} className="mb-6 border-equine-brass/30 bg-equine-brass/5">
          <div className="flex items-start gap-3">
            <Sparkles className="w-4 h-4 text-equine-champagne mt-0.5 flex-shrink-0" />
            <div className="text-[13px] text-equine-inkMuted leading-relaxed">{module.placeholder}</div>
          </div>
        </Card>
      )}

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {STATUSES.map((status) => (
          <div key={status} className="rounded-lg border border-equine-cloud bg-white/70 p-4">
            <div className="label-eyebrow-muted mb-2 capitalize">{labelFor(status)}</div>
            <div className="flex items-end justify-between gap-3">
              <div className="font-display text-4xl text-equine-ink leading-none">{stats[status]}</div>
              <StatusPill tone={STATUS_TONE[status]}>{labelFor(status)}</StatusPill>
            </div>
          </div>
        ))}
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading automation review...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Automation review unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Sparkles strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No automation drafts</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a review-first automation item for staff approval.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="ai-automation-empty-add">
            <Plus className="w-4 h-4" /> Add first draft
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
          {sorted.map((record) => {
            const data = record.data || {};
            const status = data.status || "draft";
            return (
              <Card key={record.id} hover={false} data-testid={`ai-automation-card-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.subject}</div>
                    <div className="text-[12.5px] text-equine-inkMuted capitalize">{labelFor(data.suggestion_type || "care_summary")}</div>
                  </div>
                  <StatusPill tone={STATUS_TONE[status]}>{labelFor(status)}</StatusPill>
                </div>
                <div className="text-[13.5px] text-equine-inkMuted leading-relaxed">{data.summary}</div>
                <div className="hairline mt-4 pt-3 flex flex-wrap items-center gap-2">
                  {data.confidence !== undefined && <StatusPill tone="neutral">Confidence {Number(data.confidence).toFixed(2)}</StatusPill>}
                  {status !== "reviewed" && (
                    <button type="button" onClick={() => setStatus(record, "reviewed")} disabled={savingId === record.id} className="btn-secondary text-[12px] py-2 px-4">
                      Mark reviewed
                    </button>
                  )}
                  {status !== "approved" && (
                    <button type="button" onClick={() => setStatus(record, "approved")} disabled={savingId === record.id} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Approve
                    </button>
                  )}
                  {status !== "dismissed" && (
                    <button type="button" onClick={() => setStatus(record, "dismissed")} disabled={savingId === record.id} className="btn-secondary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                      <XCircle className="w-3.5 h-3.5" /> Dismiss
                    </button>
                  )}
                  <button type="button" onClick={() => archiveRecord(record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">
                    Archive
                  </button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add automation draft"
        eyebrow="AI & Automation"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/ai-automation/records"
        initialValues={{ suggestion_type: "care_summary", status: "draft", confidence: 0.5 }}
        transform={(form) => ({ data: form })}
        submitLabel="Save draft"
        testidPrefix="ai-automation-add"
        onCreated={load}
      />
    </div>
  );
}
