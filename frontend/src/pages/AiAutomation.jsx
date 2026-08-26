import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, FileUp, RefreshCw, Sparkles, XCircle } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";

const SOURCE_TYPES = [
  ["invoice", "Invoice"],
  ["service_invoice", "Service invoice"],
  ["photo_inventory", "Photo-to-inventory"],
  ["ride_data", "Ride data"],
  ["lesson_schedule", "Lesson schedule"],
  ["training_note", "Training note"],
  ["voice_transcript", "Voice-note transcript"],
  ["health_observation", "Health observation"],
];

const REVIEW_ACTION_LABEL = {
  approved_no_save: "Reviewed, not saved",
  rejected: "Rejected",
};

const STATUS_TONE = {
  draft_ready: "success",
  running: "info",
  extraction_failed: "critical",
  pending_review: "warning",
  approved_no_save: "success",
  rejected: "neutral",
};

const defaultPromptFor = (sourceType) => {
  if (sourceType === "invoice" || sourceType === "service_invoice") {
    return "Extract draft vendor/provider, dates, line items, inventory candidates, service-history candidates, and review questions.";
  }
  if (sourceType === "photo_inventory") {
    return "Create draft inventory candidates from visible tack, feed, tools, hay, or barn supplies. Include uncertainty and review questions.";
  }
  if (sourceType === "ride_data") {
    return "Summarize draft ride metrics and training observations. Do not make medical or safety decisions.";
  }
  if (sourceType === "lesson_schedule") {
    return "Create draft lesson or training schedule candidates and conflicts for human review.";
  }
  if (sourceType === "voice_transcript") {
    return "Turn the voice note into draft tasks, inventory notes, lesson notes, invoice notes, or review questions.";
  }
  return "Extract draft records, review questions, and blocked actions. Keep all output review-required.";
};

const labelFor = (value) => {
  const pair = SOURCE_TYPES.find(([key]) => key === value);
  return pair ? pair[1] : String(value || "").replace(/_/g, " ");
};

const inferMimeType = (file) => {
  if (file.type) return file.type;
  const name = file.name.toLowerCase();
  if (name.endsWith(".pdf")) return "application/pdf";
  if (name.endsWith(".jpg") || name.endsWith(".jpeg")) return "image/jpeg";
  if (name.endsWith(".png")) return "image/png";
  if (name.endsWith(".webp")) return "image/webp";
  if (name.endsWith(".csv")) return "text/csv";
  if (name.endsWith(".json")) return "application/json";
  return "text/plain";
};

const sha256File = async (file) => {
  const bytes = await file.arrayBuffer();
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
};

const jsonPreview = (value) => JSON.stringify(value || {}, null, 2);

export default function AiAutomation() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sourceType, setSourceType] = useState("invoice");
  const [sourceText, setSourceText] = useState("");
  const [prompt, setPrompt] = useState(defaultPromptFor("invoice"));
  const [file, setFile] = useState(null);
  const [creating, setCreating] = useState(false);
  const [reviewingId, setReviewingId] = useState(null);
  const [reviewNotes, setReviewNotes] = useState({});

  const loadJobs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get("/ai/draft-jobs?limit=25");
      setJobs(response.data.jobs || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load AI draft queue.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadJobs(); }, [loadJobs]);

  const stats = useMemo(() => ({
    pending: jobs.filter((job) => job.review_status === "pending_review").length,
    reviewed: jobs.filter((job) => job.review_status === "approved_no_save").length,
    rejected: jobs.filter((job) => job.review_status === "rejected").length,
    failed: jobs.filter((job) => job.status === "extraction_failed").length,
  }), [jobs]);

  const onSourceTypeChange = (nextType) => {
    setSourceType(nextType);
    setPrompt(defaultPromptFor(nextType));
  };

  const createDraft = async () => {
    if (!file && !sourceText.trim()) {
      toast.error("Add a file or source text first.");
      return;
    }
    setCreating(true);
    try {
      let sourceId = null;
      if (file) {
        const mimeType = inferMimeType(file);
        const intent = await api.post("/ai/draft-jobs/upload-intents", {
          source_type: sourceType,
          filename: file.name,
          mime_type: mimeType,
          byte_size: file.size,
          prompt_hint: prompt,
        });
        await fetch(intent.data.upload.url, {
          method: "PUT",
          headers: intent.data.upload.headers || { "Content-Type": mimeType },
          body: file,
        }).then((response) => {
          if (!response.ok) throw new Error(`Private upload failed with ${response.status}`);
        });
        sourceId = intent.data.source.id;
        await api.post(`/ai/draft-jobs/upload-intents/${sourceId}/confirm`, {
          source_id: sourceId,
          sha256: await sha256File(file),
          byte_size: file.size,
        });
      }

      await api.post("/ai/draft-jobs", {
        source_type: sourceType,
        requested_output: "draft_extraction",
        prompt,
        ...(sourceId ? { source_id: sourceId } : { source_text: sourceText }),
      });
      toast.success("Draft extraction created for review");
      setFile(null);
      setSourceText("");
      await loadJobs();
    } catch (err) {
      toast.error(err?.response?.data?.detail || err?.message || "Could not create draft extraction.");
    } finally {
      setCreating(false);
    }
  };

  const reviewDraft = async (job, action) => {
    setReviewingId(job.id);
    try {
      await api.post(`/ai/draft-jobs/${job.id}/review`, {
        action,
        note: reviewNotes[job.id] || null,
      });
      toast.success(action === "rejected" ? "Draft rejected" : "Draft marked reviewed without saving");
      await loadJobs();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update draft review.");
    } finally {
      setReviewingId(null);
    }
  };

  return (
    <div data-testid="ai-draft-review-page">
      <PageHeader
        eyebrow="AI & Automation"
        title="Draft Extraction Review"
        subtitle="Upload invoices, feed-room and tack-room photos, ride data, schedules, training notes, or voice transcripts. Each extraction is a review-first automation item that must be reviewed before anything is approved and before any official record is saved."
        action={
          <button onClick={loadJobs} className="btn-secondary inline-flex items-center gap-2" data-testid="ai-draft-refresh">
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        }
      />

      <Card hover={false} className="mb-6 border-equine-brass/30 bg-equine-brass/5">
        <div className="flex items-start gap-3">
          <Sparkles className="w-4 h-4 text-equine-champagne mt-0.5 flex-shrink-0" />
          <div>
            <div className="text-equine-ivory font-display text-2xl mb-1">Draft-only guardrail</div>
            <div className="text-[13px] text-equine-inkMuted leading-relaxed">
              This lane can extract and summarize. It cannot diagnose, charge, message, alter access, or write official horse, inventory, billing, schedule, or service records.
            </div>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="rounded-lg border border-equine-cloud bg-white/70 p-4" data-testid="ai-draft-stat-pending">
          <div className="label-eyebrow-muted mb-2">Pending Review</div>
          <div className="font-display text-4xl text-equine-ink leading-none">{stats.pending}</div>
        </div>
        <div className="rounded-lg border border-equine-cloud bg-white/70 p-4" data-testid="ai-draft-stat-reviewed">
          <div className="label-eyebrow-muted mb-2">Reviewed</div>
          <div className="font-display text-4xl text-equine-ink leading-none">{stats.reviewed}</div>
        </div>
        <div className="rounded-lg border border-equine-cloud bg-white/70 p-4" data-testid="ai-draft-stat-rejected">
          <div className="label-eyebrow-muted mb-2">Rejected</div>
          <div className="font-display text-4xl text-equine-ink leading-none">{stats.rejected}</div>
        </div>
        <div className="rounded-lg border border-equine-cloud bg-white/70 p-4" data-testid="ai-draft-stat-failed">
          <div className="label-eyebrow-muted mb-2">Failed</div>
          <div className="font-display text-4xl text-equine-ink leading-none">{stats.failed}</div>
        </div>
      </div>

      <Card hover={false} className="mb-7" data-testid="ai-draft-create-card">
        <div className="grid grid-cols-1 xl:grid-cols-[0.95fr_1.35fr] gap-5">
          <div>
            <div className="font-display text-2xl text-equine-ink mb-2">Create Review Draft</div>
            <p className="text-[13.5px] text-equine-inkMuted leading-relaxed mb-4">
              Use private upload for PDFs and photos, or paste text from ride data, scheduling notes, or voice transcripts.
            </p>
            <label className="block text-[12px] uppercase tracking-[0.18em] text-equine-inkMuted mb-2">Source type</label>
            <select
              className="w-full rounded-lg border border-equine-cloud bg-white px-3 py-2.5 text-[14px] text-equine-ink"
              data-testid="ai-draft-source-type"
              onChange={(event) => onSourceTypeChange(event.target.value)}
              value={sourceType}
            >
              {SOURCE_TYPES.map(([key, label]) => <option key={key} value={key}>{label}</option>)}
            </select>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-[12px] uppercase tracking-[0.18em] text-equine-inkMuted mb-2">Prompt</label>
              <textarea
                className="w-full min-h-[84px] rounded-lg border border-equine-cloud bg-white px-3 py-2.5 text-[14px] text-equine-ink"
                data-testid="ai-draft-prompt"
                onChange={(event) => setPrompt(event.target.value)}
                value={prompt}
              />
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <label className="block text-[12px] uppercase tracking-[0.18em] text-equine-inkMuted mb-2">Private file source</label>
                <input
                  className="block w-full text-[13px] text-equine-ink"
                  data-testid="ai-draft-file"
                  onChange={(event) => setFile(event.target.files?.[0] || null)}
                  type="file"
                />
                {file && <div className="mt-2 text-[12px] text-equine-inkMuted">{file.name} · {Math.round(file.size / 1024)} KB</div>}
              </div>
              <div>
                <label className="block text-[12px] uppercase tracking-[0.18em] text-equine-inkMuted mb-2">Inline source text</label>
                <textarea
                  className="w-full min-h-[110px] rounded-lg border border-equine-cloud bg-white px-3 py-2.5 text-[14px] text-equine-ink"
                  data-testid="ai-draft-source-text"
                  onChange={(event) => setSourceText(event.target.value)}
                  placeholder="Paste a voice-note transcript, ride summary, lesson schedule, or short invoice text."
                  value={sourceText}
                />
              </div>
            </div>
            <button
              className="btn-primary inline-flex items-center gap-2 disabled:opacity-50"
              data-testid="ai-draft-create"
              disabled={creating}
              onClick={createDraft}
              type="button"
            >
              <FileUp className="w-4 h-4" /> {creating ? "Creating draft..." : "Create draft extraction"}
            </button>
          </div>
        </div>
      </Card>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading draft queue...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Draft queue unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : jobs.length === 0 ? (
        <Empty>
          <Sparkles strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No AI draft extractions yet</div>
          <div className="text-[13px] text-equine-platinum/60">Create the first draft from a file or source text.</div>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
          {jobs.map((job) => (
            <Card key={job.id} hover={false} data-testid={`ai-draft-job-${job.id}`}>
              <div className="flex items-start justify-between gap-3 mb-4">
                <div className="min-w-0">
                  <div className="font-display text-2xl text-equine-ink truncate">{labelFor(job.source_type)}</div>
                  <div className="text-[12.5px] text-equine-inkMuted">{job.id}</div>
                </div>
                <div className="flex items-center gap-2 flex-wrap justify-end">
                  <StatusPill tone={STATUS_TONE[job.status] || "neutral"}>{labelFor(job.status)}</StatusPill>
                  <StatusPill tone={STATUS_TONE[job.review_status] || "neutral"}>{labelFor(job.review_status)}</StatusPill>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 mb-4 text-[12.5px] text-equine-inkMuted">
                <div>Draft only: <span className="text-equine-ink font-semibold">{String(job.draft_only)}</span></div>
                <div>Review required: <span className="text-equine-ink font-semibold">{String(job.review_required)}</span></div>
              </div>
              <pre className="max-h-[320px] overflow-auto rounded-lg bg-equine-navy text-equine-platinum/85 p-4 text-[12px] leading-relaxed whitespace-pre-wrap" data-testid={`ai-draft-result-${job.id}`}>
                {jsonPreview(job.draft_result || { error_code: job.error_code || "pending" })}
              </pre>
              {job.review_status === "pending_review" && job.status === "draft_ready" ? (
                <div className="mt-4 space-y-3">
                  <textarea
                    className="w-full min-h-[76px] rounded-lg border border-equine-cloud bg-white px-3 py-2.5 text-[13px] text-equine-ink"
                    data-testid={`ai-draft-review-note-${job.id}`}
                    onChange={(event) => setReviewNotes((current) => ({ ...current, [job.id]: event.target.value }))}
                    placeholder="Optional review note. This does not save official records."
                    value={reviewNotes[job.id] || ""}
                  />
                  <div className="flex flex-wrap gap-2">
                    <button
                      className="btn-primary inline-flex items-center gap-1.5 disabled:opacity-50"
                      data-testid={`ai-draft-reviewed-${job.id}`}
                      disabled={reviewingId === job.id}
                      onClick={() => reviewDraft(job, "approved_no_save")}
                      type="button"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" /> {REVIEW_ACTION_LABEL.approved_no_save}
                    </button>
                    <button
                      className="btn-secondary inline-flex items-center gap-1.5 disabled:opacity-50"
                      data-testid={`ai-draft-reject-${job.id}`}
                      disabled={reviewingId === job.id}
                      onClick={() => reviewDraft(job, "rejected")}
                      type="button"
                    >
                      <XCircle className="w-3.5 h-3.5" /> Reject
                    </button>
                  </div>
                </div>
              ) : null}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
