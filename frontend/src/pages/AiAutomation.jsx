import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, ClipboardCheck, FileSearch, FileUp, RefreshCw, ShieldCheck, Sparkles, XCircle } from "lucide-react";
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
  approved_no_save: "Accept draft, no save",
  rejected: "Rejected",
};

const REVIEW_STATUS_LABEL = {
  pending_review: "Pending review",
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

const REVIEW_LANES = [
  "Invoices",
  "Service notes",
  "Ride data",
  "Scheduling notes",
  "Voice transcripts",
  "Photo inventory",
];

const REVIEW_CHECKLIST = [
  "Confirm the source belongs to the current barn or user context.",
  "Edit or reject uncertain line items, names, quantities, dates, and prices.",
  "Treat health scores and service suggestions as decision support only.",
  "Save final records only from the correct destination workflow.",
];

const DESTINATION_BY_SOURCE_TYPE = {
  invoice: "Inventory, expenses, billing, or horse records",
  service_invoice: "Service history, expenses, billing, or horse records",
  photo_inventory: "Inventory or equipment records",
  ride_data: "Ride log, training note, or performance review",
  lesson_schedule: "Lesson calendar or training schedule",
  training_note: "Training plan or horse progress note",
  voice_transcript: "Tasks, notes, invoices, inventory, or schedule drafts",
  health_observation: "Health log or care follow-up",
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

const reviewLabelFor = (value) => REVIEW_STATUS_LABEL[value] || labelFor(value);

const formatConfidence = (value) => {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return null;
  return numeric <= 1 ? `${Math.round(numeric * 100)}%` : `${Math.round(numeric)}%`;
};

const arrayValue = (value) => Array.isArray(value) ? value.filter(Boolean) : [];

const draftResultFor = (job) => job.draft_result || {};

const structuredSummaryFor = (job) => {
  const result = draftResultFor(job);
  return result.review_summary || "Review required before saving to any workflow.";
};

const metadataRowsFor = (job) => {
  const result = draftResultFor(job);
  return [
    ["Destination", DESTINATION_BY_SOURCE_TYPE[job.source_type] || "Destination workflow review"],
    result.extraction_status ? ["Extraction", labelFor(result.extraction_status)] : null,
    result.fallback_used ? ["Fallback", labelFor(result.fallback_used)] : null,
    arrayValue(result.attempted_methods).length ? ["Methods", arrayValue(result.attempted_methods).map(labelFor).join(", ")] : null,
    formatConfidence(result.confidence) ? ["Confidence", formatConfidence(result.confidence)] : null,
  ].filter(Boolean);
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
        title="AI Draft Review"
        subtitle="Upload invoices, feed-room and tack-room photos, ride data, schedules, training notes, or voice transcripts. Each extraction is a review-first automation item that must be reviewed before anything is approved and before any official record is saved."
        action={
          <button onClick={loadJobs} className="btn-secondary inline-flex items-center gap-2" data-testid="ai-draft-refresh">
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        }
      />

      <Card hover={false} className="mb-6 border-equine-brass/30 bg-equine-brass/5">
        <div className="flex items-start gap-3">
          <ShieldCheck className="w-5 h-5 text-equine-champagne mt-0.5 flex-shrink-0" />
          <div>
            <div className="text-equine-ivory font-display text-2xl mb-1">Draft-only guardrail</div>
            <div className="text-[13px] text-equine-inkMuted leading-relaxed">
              This lane can extract and summarize. It cannot diagnose, charge, message, alter access, or write official horse, inventory, billing, schedule, or service records.
            </div>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 xl:grid-cols-[1.1fr_0.9fr] gap-5 mb-6">
        <Card hover={false}>
          <div className="flex items-start gap-3">
            <FileSearch className="w-5 h-5 text-equine-brassLight mt-0.5 flex-shrink-0" />
            <div className="min-w-0">
              <div className="label-eyebrow-muted mb-3">Pilot Review Lanes</div>
              <div className="flex flex-wrap gap-2">
                {REVIEW_LANES.map((lane) => (
                  <StatusPill
                    key={lane}
                    tone="neutral"
                    data-testid={`ai-draft-review-lane-${lane.toLowerCase().replace(/[^a-z]+/g, "-")}`}
                  >
                    {lane}
                  </StatusPill>
                ))}
              </div>
            </div>
          </div>
        </Card>
        <Card hover={false}>
          <div className="flex items-start gap-3">
            <ClipboardCheck className="w-5 h-5 text-equine-sage mt-0.5 flex-shrink-0" />
            <div>
              <div className="label-eyebrow-muted mb-3">Reviewer Checklist</div>
              <ul className="space-y-1.5 text-[13px] text-equine-inkMuted leading-relaxed" data-testid="ai-draft-review-checklist">
                {REVIEW_CHECKLIST.map((item) => (
                  <li key={item} data-testid={`ai-draft-review-check-${item.toLowerCase().replace(/[^a-z]+/g, "-").replace(/-$/, "")}`}>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </Card>
      </div>

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
              Generate drafts from private PDFs and photos, or paste text from ride data, scheduling notes, or voice transcripts.
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
          <div className="text-[13px] text-equine-platinum/60">Create the first draft from a file or source text. Drafts stay review-required and do not save official records.</div>
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
                  <StatusPill tone={STATUS_TONE[job.review_status] || "neutral"}>{reviewLabelFor(job.review_status)}</StatusPill>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 mb-4 text-[12.5px] text-equine-inkMuted">
                <div>Draft only: <span className="text-equine-ink font-semibold">{String(job.draft_only)}</span></div>
                <div>Review required: <span className="text-equine-ink font-semibold">{String(job.review_required)}</span></div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-4">
                {metadataRowsFor(job).map(([label, value]) => (
                  <div key={label} className="rounded-lg border border-equine-cloud bg-equine-cloud/30 px-3 py-2">
                    <div className="label-eyebrow-muted mb-1">{label}</div>
                    <div className="text-[12.5px] text-equine-ink truncate">{value}</div>
                  </div>
                ))}
              </div>
              {arrayValue(draftResultFor(job).review_questions).length > 0 && (
                <div className="mb-4 rounded-lg border border-equine-brass/25 bg-equine-brass/5 p-3">
                  <div className="label-eyebrow-muted mb-2">Questions Before Saving Elsewhere</div>
                  <ul className="space-y-1.5 text-[13px] text-equine-inkMuted leading-relaxed">
                    {arrayValue(draftResultFor(job).review_questions).map((question) => <li key={question}>{question}</li>)}
                  </ul>
                </div>
              )}
              <div
                className="mb-4 rounded-lg border border-equine-cloud bg-white/70 p-3"
                data-testid={`ai-draft-structured-review-${job.id}`}
              >
                <div className="label-eyebrow-muted mb-2">Draft Review Summary</div>
                <div
                  className="text-[13px] text-equine-inkMuted leading-relaxed mb-3"
                  data-testid={`ai-draft-review-summary-${job.id}`}
                >
                  {structuredSummaryFor(job)}
                </div>
                {formatConfidence(draftResultFor(job).confidence) && (
                  <div className="mb-3 rounded-lg border border-equine-cloud bg-equine-cloud/25 px-3 py-2">
                    <div className="label-eyebrow-muted mb-1">Confidence</div>
                    <div className="text-[12.5px] text-equine-ink">{formatConfidence(draftResultFor(job).confidence)}</div>
                  </div>
                )}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                  <div data-testid={`ai-draft-missing-info-${job.id}`}>
                    <div className="label-eyebrow-muted mb-1.5">Missing Information</div>
                    {arrayValue(draftResultFor(job).missing_information).length > 0 ? (
                      <ul className="space-y-1 text-[12.5px] text-equine-inkMuted leading-relaxed">
                        {arrayValue(draftResultFor(job).missing_information).map((item) => <li key={item}>{item}</li>)}
                      </ul>
                    ) : (
                      <div className="text-[12.5px] text-equine-inkMuted">None listed by draft extractor.</div>
                    )}
                  </div>
                  <div data-testid={`ai-draft-blocked-actions-${job.id}`}>
                    <div className="label-eyebrow-muted mb-1.5">Blocked Actions</div>
                    {arrayValue(draftResultFor(job).blocked_actions).length > 0 ? (
                      <ul className="space-y-1 text-[12.5px] text-equine-inkMuted leading-relaxed">
                        {arrayValue(draftResultFor(job).blocked_actions).map((item) => <li key={item}>{labelFor(item)}</li>)}
                      </ul>
                    ) : (
                      <div className="text-[12.5px] text-equine-inkMuted">Official saves remain blocked by reviewer workflow.</div>
                    )}
                  </div>
                </div>
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
                    placeholder="Optional review note. This marks the draft only; save final records from the correct workflow."
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
