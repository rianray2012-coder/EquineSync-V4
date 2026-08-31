import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, ClipboardCheck, Edit3, FileSearch, FileUp, PackageCheck, RefreshCw, ShieldCheck, Sparkles, XCircle } from "lucide-react";
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
  official_saved: "Official saved",
};

const STATUS_TONE = {
  draft_ready: "success",
  running: "info",
  extraction_failed: "critical",
  pending_review: "warning",
  approved_no_save: "success",
  rejected: "neutral",
  official_saved: "success",
};

const REVIEW_LANES = [
  "Invoices",
  "Service notes",
  "Ride data",
  "Scheduling notes",
  "Voice transcripts",
  "Photo inventory",
  "Health observations",
];

const REVIEW_CHECKLIST = [
  "Confirm the source belongs to the current barn or user context.",
  "Edit or reject uncertain line items, names, quantities, dates, and prices.",
  "Treat health scores and service suggestions as draft decision support only.",
  "Do not use AI health drafts as diagnosis, treatment, medication, emergency triage, or provider-message instructions.",
  "Use official save only for Founder-approved inventory and work-ticket lanes.",
];

const OFFICIAL_SAVE_LANES = {
  inventory_supply: {
    label: "Save Official Inventory",
    collectionLabel: "Inventory",
    description: "Creates reviewed inventory, feed, tack, supply, or equipment records.",
  },
  work_task_repair: {
    label: "Save Official Work Ticket",
    collectionLabel: "Work tickets",
    description: "Creates reviewed work, task, repair, or barn-operations tickets.",
  },
};

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
  if (sourceType === "health_observation") {
    return "Organize draft health observations and a review-only health score candidate from user-provided details. Do not diagnose, recommend treatment, change medication, triage emergencies, notify participants, or save an official health record.";
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

const inventoryCandidatesFor = (job) => arrayValue(draftResultFor(job).draft_inventory_candidates);
const isInvoiceSource = (sourceType) => sourceType === "invoice" || sourceType === "service_invoice";
const invoicePaymentReviewFor = (job) => {
  const result = draftResultFor(job);
  const review = result.draft_payment_review || result.draft_payment_status_candidate;
  if (!review || typeof review !== "object" || Array.isArray(review)) return null;
  return {
    ...review,
    candidate_status: review.candidate_status || review.status || "review_required",
  };
};
const isScheduleSource = (sourceType) => sourceType === "lesson_schedule";
const scheduleReviewBoundaryFor = (job) => {
  const boundary = draftResultFor(job).calendar_review_boundary;
  return {
    ...(boundary && typeof boundary === "object" && !Array.isArray(boundary) ? boundary : {}),
    candidate_status: boundary?.candidate_status || "review_required",
    official_calendar_change_allowed: false,
    participant_notification_allowed: false,
    automated_send_allowed: false,
  };
};

const healthScoreCandidateFor = (job) => {
  const candidate = draftResultFor(job).draft_health_score_candidate;
  return candidate && typeof candidate === "object" ? candidate : null;
};

const textFromValue = (value) => {
  if (value === null || value === undefined || value === "") return "";
  if (Array.isArray(value)) return value.filter(Boolean).map(textFromValue).filter(Boolean).join("; ");
  if (typeof value === "object") {
    const primaryText = [
      value.title,
      value.name,
      value.task,
      value.summary,
      value.description,
      value.details,
      value.work_summary,
      value.note,
    ].filter(Boolean).map(textFromValue).join(" - ");
    if (primaryText) return primaryText;
    return Object.entries(value)
      .filter(([, entryValue]) => entryValue !== null && entryValue !== undefined && entryValue !== "" && !(Array.isArray(entryValue) && entryValue.length === 0))
      .map(([key, entryValue]) => `${labelFor(key)}: ${textFromValue(entryValue) || String(entryValue)}`)
      .filter(Boolean)
      .join("; ");
  }
  return String(value);
};

const workCandidatesFor = (job) => {
  const result = draftResultFor(job);
  const candidates = [
    ...arrayValue(result.draft_tasks),
    ...arrayValue(result.draft_work_ticket_candidates),
    ...arrayValue(result.draft_training_note?.follow_up_tasks),
    ...arrayValue(result.draft_records).filter((record) => {
      const type = String(record?.type || record?.category || "").toLowerCase();
      return type.includes("task") || type.includes("repair") || type.includes("work");
    }),
  ];
  return candidates.map((candidate, index) => {
    if (typeof candidate === "string") {
      return {
        id: `work-${index}`,
        name: candidate,
        title: candidate,
        category: "task",
        details: candidate,
        priority: "standard",
        source_confidence: "medium",
        review_status: "needs_review",
      };
    }
    return {
      id: candidate?.id || `work-${index}`,
      name: candidate?.name || candidate?.title || candidate?.task || candidate?.summary || `Work item ${index + 1}`,
      title: candidate?.title || candidate?.name || candidate?.task || candidate?.summary || `Work item ${index + 1}`,
      category: candidate?.category || candidate?.type || "task",
      details: candidate?.details || candidate?.description || candidate?.summary || textFromValue(candidate),
      priority: candidate?.priority || "standard",
      due_date: candidate?.due_date || candidate?.date || null,
      assigned_user_id: candidate?.assigned_user_id || null,
      assigned_role: candidate?.assigned_role || null,
      source_confidence: candidate?.source_confidence || candidate?.confidence || "medium",
      review_status: candidate?.review_status || "needs_review",
      notes: candidate?.notes || [],
    };
  });
};

const displayListValue = (value, fallback = "Needs review") => {
  const text = textFromValue(value);
  return text || fallback;
};

const sourceLanePreviewFor = (job) => {
  const result = draftResultFor(job);
  if (job.source_type === "photo_inventory") {
    return {
      testId: `ai-draft-expanded-photo-inventory-${job.id}`,
      title: "Photo Inventory Draft",
      items: [
        ["Room or area", result.room_or_area],
        ["Storage state", result.visible_storage_state],
        ["Visible categories", result.visible_inventory_categories],
        ["Count estimates", result.visible_count_estimates],
        ["Uncertain or not counted", result.not_counted_or_uncertain],
        ["Reorder or organization cues", result.organization_or_reorder_suggestions],
      ],
    };
  }
  if (isInvoiceSource(job.source_type)) {
    return {
      testId: `ai-draft-expanded-invoice-service-${job.id}`,
      title: "Invoice and Service Draft",
      items: [
        ["Vendor or provider", result.vendor_or_provider],
        ["Document type", result.document_type],
        ["Order or service date", result.order_date],
        ["Inventory candidates", result.draft_inventory_candidates],
        ["Service-history candidates", result.draft_service_history_candidates],
        ["Invoice candidates", result.draft_invoice_candidates],
        ["Expense candidates", result.draft_expense_candidates],
        ["Payment status", result.draft_payment_status_candidate],
        ["Payment review", result.draft_payment_review],
        ["Reconciliation questions", result.draft_reconciliation_questions],
      ],
    };
  }
  if (job.source_type === "voice_transcript") {
    return {
      testId: `ai-draft-expanded-voice-capture-${job.id}`,
      title: "Voice Capture Draft",
      items: [
        ["Capture context", result.voice_capture_context],
        ["Work-ticket candidates", result.draft_work_ticket_candidates],
        ["Inventory candidates", result.draft_inventory_candidates],
        ["Invoice candidates", result.draft_invoice_candidates],
        ["Schedule candidates", result.draft_schedule_candidates],
        ["Training notes", result.draft_training_notes],
      ],
    };
  }
  if (job.source_type === "ride_data") {
    return {
      testId: `ai-draft-expanded-ride-data-${job.id}`,
      title: "Ride Data Draft",
      items: [
        ["Ride summary", result.draft_ride_summary],
        ["Training candidates", result.draft_training_candidates],
      ],
    };
  }
  if (job.source_type === "lesson_schedule") {
    return {
      testId: `ai-draft-expanded-schedule-${job.id}`,
      title: "Schedule Draft",
      items: [
        ["Schedule candidates", result.draft_schedule_candidates],
        ["Itinerary candidates", result.draft_itinerary_candidates],
        ["Notification preview", result.draft_notification_preview],
        ["Calendar boundary", result.calendar_review_boundary],
      ],
    };
  }
  if (job.source_type === "training_note") {
    return {
      testId: `ai-draft-expanded-training-note-${job.id}`,
      title: "Training Note Draft",
      items: [["Training note", result.draft_training_note]],
    };
  }
  return null;
};

const candidateFieldValue = (candidate, field, fallback = "Needs review") => {
  const value = candidate?.[field];
  if (value === null || value === undefined || value === "") return fallback;
  if (Array.isArray(value)) return value.length ? value.join(", ") : fallback;
  if (typeof value === "boolean") return value ? "Yes" : "No";
  return String(value);
};

const candidateKeyFor = (job, index) => `${job.id}:${index}`;

const saveCandidateKeyFor = (job, lane, index) => `${job.id}:${lane}:${index}`;

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

const formatCount = (value) => Number.isFinite(Number(value)) ? Number(value).toLocaleString() : "Unmetered";

const formatBytes = (value) => {
  const size = Number(value);
  if (!Number.isFinite(size)) return "Unmetered";
  if (size >= 1024 * 1024) return `${Math.round(size / 1024 / 1024)} MB`;
  if (size >= 1024) return `${Math.round(size / 1024)} KB`;
  return `${size} B`;
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
  const [candidateEdits, setCandidateEdits] = useState({});
  const [candidateDisposition, setCandidateDisposition] = useState({});
  const [officialSaveConfirm, setOfficialSaveConfirm] = useState(null);
  const [officialSaveChecked, setOfficialSaveChecked] = useState(false);
  const [savingOfficialId, setSavingOfficialId] = useState(null);
  const [usagePolicy, setUsagePolicy] = useState(null);

  const loadJobs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [jobsResponse, usageResponse] = await Promise.all([
        api.get("/ai/draft-jobs?limit=25"),
        api.get("/ai/draft-jobs/usage-policy").catch(() => null),
      ]);
      setJobs(jobsResponse.data.jobs || []);
      setUsagePolicy(usageResponse?.data?.usage || null);
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

  const buildOfficialSaveItems = (job, lane) => {
    if (lane === "inventory_supply") {
      return inventoryCandidatesFor(job).map((candidate, index) => {
        const disposition = candidateDisposition[candidateKeyFor(job, index)];
        const edits = candidateEdits[candidateKeyFor(job, index)] || {};
        const display = { ...candidate, ...edits };
        if (disposition === "rejected" || disposition === "duplicate") return null;
        return {
          name: candidateFieldValue(display, "item_name", "Unnamed inventory item"),
          category: candidateFieldValue(display, "category", "uncategorized"),
          quantity: Number.isFinite(Number(display.quantity)) ? Number(display.quantity) : null,
          unit: display.unit || null,
          storage_location: display.storage_location || null,
          horse_or_barn_assignment: display.horse_or_barn_assignment || null,
          source_confidence: display.source_confidence || display.confidence || "medium",
          review_status: disposition === "locally_reviewed" ? "reviewed" : (display.review_status === "corrected" ? "corrected" : "reviewed"),
          notes: arrayValue(display.notes),
        };
      }).filter(Boolean);
    }
    return workCandidatesFor(job).map((candidate, index) => {
      const disposition = candidateDisposition[saveCandidateKeyFor(job, lane, index)];
      if (disposition === "rejected" || disposition === "duplicate") return null;
      return {
        name: candidate.name || candidate.title || `Work item ${index + 1}`,
        title: candidate.title || candidate.name || `Work item ${index + 1}`,
        category: candidate.category || "task",
        details: candidate.details || candidate.name || candidate.title || `Work item ${index + 1}`,
        priority: ["critical", "standard", "informational"].includes(candidate.priority) ? candidate.priority : "standard",
        due_date: candidate.due_date || null,
        assigned_user_id: candidate.assigned_user_id || null,
        assigned_role: candidate.assigned_role || null,
        source_confidence: candidate.source_confidence || "medium",
        review_status: disposition === "locally_reviewed" ? "reviewed" : (candidate.review_status === "corrected" ? "corrected" : "reviewed"),
        notes: arrayValue(candidate.notes),
      };
    }).filter(Boolean);
  };

  const openOfficialSaveConfirm = (job, lane) => {
    setOfficialSaveConfirm({ jobId: job.id, lane });
    setOfficialSaveChecked(false);
  };

  const cancelOfficialSaveConfirm = () => {
    setOfficialSaveConfirm(null);
    setOfficialSaveChecked(false);
  };

  const officialSaveDraft = async (job, lane) => {
    const items = buildOfficialSaveItems(job, lane);
    if (!items.length) {
      toast.error("No reviewed items are available for official save.");
      return;
    }
    setSavingOfficialId(`${job.id}:${lane}`);
    try {
      await api.post(`/ai/draft-jobs/${job.id}/official-save`, {
        lane,
        items,
        reviewer_note: reviewNotes[job.id] || `Human-confirmed ${OFFICIAL_SAVE_LANES[lane].collectionLabel} save from AI draft review.`,
      });
      toast.success(`${OFFICIAL_SAVE_LANES[lane].collectionLabel} saved after human confirmation`);
      cancelOfficialSaveConfirm();
      await loadJobs();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not save official records.");
    } finally {
      setSavingOfficialId(null);
    }
  };

  const updateCandidateEdit = (job, index, field, value) => {
    const key = candidateKeyFor(job, index);
    setCandidateEdits((current) => ({
      ...current,
      [key]: {
        ...(current[key] || {}),
        [field]: value,
      },
    }));
  };

  const markCandidateDisposition = (job, index, disposition) => {
    const key = candidateKeyFor(job, index);
    setCandidateDisposition((current) => ({
      ...current,
      [key]: disposition,
    }));
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

      {usagePolicy && (
        <Card hover={false} className="mb-6 border-equine-cloud bg-white/75" data-testid="ai-draft-budget-guardrail">
          <div className="flex items-start gap-3">
            <ShieldCheck className="w-5 h-5 text-equine-sage mt-0.5 flex-shrink-0" />
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-start justify-between gap-3 mb-3">
                <div>
                  <div className="label-eyebrow-muted mb-1">AI Budget Guardrail</div>
                  <div className="text-[13px] text-equine-inkMuted leading-relaxed" data-testid="ai-draft-budget-policy">
                    Draft extraction remains review-required, human-confirmed, and budget-gated for pilot use.
                  </div>
                </div>
                <StatusPill tone={usagePolicy.enforcement_enabled ? "success" : "warning"} data-testid="ai-draft-budget-enforcement">
                  {usagePolicy.enforcement_enabled ? "Enforced" : "Monitor only"}
                </StatusPill>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="rounded-lg border border-equine-cloud bg-equine-cloud/25 p-3" data-testid="ai-draft-budget-jobs">
                  <div className="label-eyebrow-muted mb-1">Jobs Today</div>
                  <div className="text-equine-ink font-semibold">{formatCount(usagePolicy.draft_jobs_created)} / {formatCount(usagePolicy.daily_job_limit)}</div>
                  <div className="text-[12px] text-equine-inkMuted">Remaining {formatCount(usagePolicy.remaining_jobs)}</div>
                </div>
                <div className="rounded-lg border border-equine-cloud bg-equine-cloud/25 p-3" data-testid="ai-draft-budget-tokens">
                  <div className="label-eyebrow-muted mb-1">Estimated Tokens</div>
                  <div className="text-equine-ink font-semibold">{formatCount(usagePolicy.estimated_tokens_used)} / {formatCount(usagePolicy.daily_estimated_token_limit)}</div>
                  <div className="text-[12px] text-equine-inkMuted">Remaining {formatCount(usagePolicy.remaining_estimated_tokens)}</div>
                </div>
                <div className="rounded-lg border border-equine-cloud bg-equine-cloud/25 p-3" data-testid="ai-draft-budget-source-bytes">
                  <div className="label-eyebrow-muted mb-1">Source Volume</div>
                  <div className="text-equine-ink font-semibold">{formatBytes(usagePolicy.source_bytes_processed)} / {formatBytes(usagePolicy.daily_source_byte_limit)}</div>
                  <div className="text-[12px] text-equine-inkMuted">Remaining {formatBytes(usagePolicy.remaining_source_bytes)}</div>
                </div>
              </div>
            </div>
          </div>
        </Card>
      )}

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
              {job.source_type === "health_observation" && (
                <div
                  className="mb-4 rounded-lg border border-equine-clay/30 bg-equine-clay/5 p-3"
                  data-testid={`ai-health-draft-only-boundary-${job.id}`}
                >
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="w-5 h-5 text-equine-clay mt-0.5 flex-shrink-0" />
                    <div className="min-w-0 flex-1">
                      <div className="label-eyebrow-muted mb-1">Health Draft Review Boundary</div>
                      <div className="text-[13px] text-equine-inkMuted leading-relaxed" data-testid={`ai-health-no-diagnosis-boundary-${job.id}`}>
                        This health score is a review-only candidate. It is not a diagnosis, treatment plan, medication instruction, emergency triage decision, provider message, notification, or official horse-health record.
                      </div>
                      <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2" data-testid={`ai-health-boundary-checklist-${job.id}`}>
                        <StatusPill tone="warning" data-testid={`ai-health-candidate-only-${job.id}`}>Candidate Only</StatusPill>
                        <StatusPill tone="warning" data-testid={`ai-health-reviewer-decides-escalation-${job.id}`}>Reviewer Decides Escalation</StatusPill>
                        <StatusPill tone="critical" data-testid={`ai-health-do-not-notify-save-${job.id}`}>Do Not Notify or Save</StatusPill>
                        <StatusPill tone="critical" data-testid={`ai-health-no-clinical-action-${job.id}`}>No Clinical Action</StatusPill>
                      </div>
                      {healthScoreCandidateFor(job) && (
                        <div className="mt-3 rounded-lg border border-equine-cloud bg-white/75 px-3 py-2" data-testid={`ai-health-score-candidate-${job.id}`}>
                          <div className="label-eyebrow-muted mb-1">Draft Health Score Candidate</div>
                          <div className="text-[12.5px] text-equine-ink">
                            {candidateFieldValue(healthScoreCandidateFor(job), "score", "Score needs review")}
                            {healthScoreCandidateFor(job)?.scale ? ` / ${healthScoreCandidateFor(job).scale}` : ""}
                          </div>
                          <div className="text-[12px] text-equine-inkMuted mt-1" data-testid={`ai-health-score-save-gated-${job.id}`}>
                            Human review required; official health-score save remains separately gated.
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}
              {isInvoiceSource(job.source_type) && (
                <div
                  className="mb-4 rounded-lg border border-equine-brass/30 bg-equine-brass/5 p-3"
                  data-testid={`ai-invoice-payment-boundary-${job.id}`}
                >
                  <div className="flex items-start gap-3">
                    <ShieldCheck className="w-5 h-5 text-equine-champagne mt-0.5 flex-shrink-0" />
                    <div className="min-w-0 flex-1">
                      <div className="label-eyebrow-muted mb-1">Invoice Payment Review Boundary</div>
                      <div className="text-[13px] text-equine-inkMuted leading-relaxed">
                        Payment status is draft review only. AI cannot finalize invoices, mark paid or unpaid, charge, refund, issue credits, or change EquineSync subscription entitlements.
                      </div>
                      <div className="text-[12.5px] text-equine-inkMuted leading-relaxed mt-2" data-testid={`ai-invoice-subscription-separation-${job.id}`}>
                        Trainer and facility receivables stay separate from EquineSync subscription billing and require human-confirmed workflow authority.
                      </div>
                      <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2">
                        <StatusPill tone="critical" data-testid={`ai-invoice-no-payment-mutation-${job.id}`}>No Payment Mutation</StatusPill>
                        <StatusPill tone="critical" data-testid={`ai-invoice-no-finalization-${job.id}`}>No Invoice Finalization</StatusPill>
                      </div>
                      {invoicePaymentReviewFor(job) && (
                        <div className="mt-3 rounded-lg border border-equine-cloud bg-white/75 px-3 py-2" data-testid={`ai-invoice-payment-review-candidate-${job.id}`}>
                          <div className="label-eyebrow-muted mb-1">Draft Payment Review Candidate</div>
                          <div className="text-[12.5px] text-equine-ink">
                            {candidateFieldValue(invoicePaymentReviewFor(job), "candidate_status", "Review required")}
                          </div>
                          <div className="text-[12px] text-equine-inkMuted mt-1">
                            {candidateFieldValue(invoicePaymentReviewFor(job), "confidence", "Confidence needs review")} · {displayListValue(invoicePaymentReviewFor(job)?.basis, "Basis needs review")}
                          </div>
                          {arrayValue(draftResultFor(job).draft_reconciliation_questions).length > 0 && (
                            <div className="mt-2 text-[12px] text-equine-inkMuted" data-testid={`ai-invoice-reconciliation-questions-${job.id}`}>
                              {arrayValue(draftResultFor(job).draft_reconciliation_questions).join(" ")}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}
              {isScheduleSource(job.source_type) && (
                <div
                  className="mb-4 rounded-lg border border-equine-brass/30 bg-equine-brass/5 p-3"
                  data-testid={`ai-schedule-calendar-boundary-${job.id}`}
                >
                  <div className="flex items-start gap-3">
                    <ShieldCheck className="w-5 h-5 text-equine-champagne mt-0.5 flex-shrink-0" />
                    <div className="min-w-0 flex-1">
                      <div className="label-eyebrow-muted mb-1">Schedule Review Boundary</div>
                      <div className="text-[13px] text-equine-inkMuted leading-relaxed" data-testid={`ai-schedule-no-calendar-mutation-copy-${job.id}`}>
                        Lesson and training schedule AI can draft schedule options, itineraries, conflict notes, and notification copy for human review. AI cannot create, update, delete, or publish calendar events.
                      </div>
                      <div className="text-[12.5px] text-equine-inkMuted leading-relaxed mt-2" data-testid={`ai-schedule-participant-notification-gate-${job.id}`}>
                        Participant notifications require separate human approval, recipient opt-in review, privacy-safe copy review, and an explicit send workflow.
                      </div>
                      <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2">
                        <StatusPill tone="critical" data-testid={`ai-schedule-no-calendar-mutation-${job.id}`}>No Calendar Mutation</StatusPill>
                        <StatusPill tone="critical" data-testid={`ai-schedule-no-participant-notification-${job.id}`}>No Participant Notification</StatusPill>
                        <StatusPill tone="warning" data-testid={`ai-schedule-human-confirmation-required-${job.id}`}>Human Confirmation Required</StatusPill>
                        <StatusPill tone="warning" data-testid={`ai-schedule-privacy-review-required-${job.id}`}>Privacy Review Required</StatusPill>
                      </div>
                      <div className="mt-3 rounded-lg border border-equine-cloud bg-white/75 px-3 py-2" data-testid={`ai-schedule-review-candidate-${job.id}`}>
                        <div className="label-eyebrow-muted mb-1">Draft Schedule Review Candidate</div>
                        <div className="text-[12.5px] text-equine-ink">
                          {candidateFieldValue(scheduleReviewBoundaryFor(job), "candidate_status", "Review required")}
                        </div>
                        <div className="text-[12px] text-equine-inkMuted mt-1">
                          Calendar change allowed: {candidateFieldValue(scheduleReviewBoundaryFor(job), "official_calendar_change_allowed", "No")} · Notification allowed: {candidateFieldValue(scheduleReviewBoundaryFor(job), "participant_notification_allowed", "No")}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              {sourceLanePreviewFor(job) && (
                <div
                  className="mb-4 rounded-lg border border-equine-cloud bg-white/75 p-3"
                  data-testid={sourceLanePreviewFor(job).testId}
                >
                  <div className="label-eyebrow-muted mb-2">{sourceLanePreviewFor(job).title}</div>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-2">
                    {sourceLanePreviewFor(job).items.map(([label, value]) => (
                      <div key={label} className="rounded-lg border border-equine-cloud bg-equine-cloud/25 px-3 py-2">
                        <div className="label-eyebrow-muted mb-1">{label}</div>
                        <div className="text-[12.5px] text-equine-inkMuted leading-relaxed">
                          {displayListValue(value)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {arrayValue(draftResultFor(job).review_questions).length > 0 && (
                <div className="mb-4 rounded-lg border border-equine-brass/25 bg-equine-brass/5 p-3">
                  <div className="label-eyebrow-muted mb-2">Questions Before Saving Elsewhere</div>
                  <ul className="space-y-1.5 text-[13px] text-equine-inkMuted leading-relaxed">
                    {arrayValue(draftResultFor(job).review_questions).map((question) => <li key={question}>{question}</li>)}
                  </ul>
                </div>
              )}
              {(inventoryCandidatesFor(job).length > 0 || workCandidatesFor(job).length > 0) && job.review_status === "pending_review" && job.status === "draft_ready" ? (
                <div
                  className="mb-4 rounded-lg border border-equine-brass/35 bg-equine-brass/5 p-3"
                  data-testid={`ai-draft-official-save-panel-${job.id}`}
                >
                  <div className="flex items-start gap-3">
                    <ShieldCheck className="w-5 h-5 text-equine-champagne mt-0.5 flex-shrink-0" />
                    <div className="min-w-0 flex-1">
                      <div className="label-eyebrow-muted mb-1">Official Save Requires Human Confirmation</div>
                      <div className="text-[13px] text-equine-inkMuted leading-relaxed mb-3">
                        Only Lane 1 inventory/supply and Lane 2 work-ticket records can be saved here. Health, billing, legal, notifications, and calendar changes remain blocked from this action.
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {inventoryCandidatesFor(job).length > 0 && (
                          <button
                            className="btn-secondary inline-flex items-center gap-1.5 disabled:opacity-50"
                            data-testid={`ai-draft-official-save-open-inventory-${job.id}`}
                            disabled={savingOfficialId === `${job.id}:inventory_supply`}
                            onClick={() => openOfficialSaveConfirm(job, "inventory_supply")}
                            type="button"
                          >
                            <PackageCheck className="w-3.5 h-3.5" /> {OFFICIAL_SAVE_LANES.inventory_supply.label}
                          </button>
                        )}
                        {workCandidatesFor(job).length > 0 && (
                          <button
                            className="btn-secondary inline-flex items-center gap-1.5 disabled:opacity-50"
                            data-testid={`ai-draft-official-save-open-work-${job.id}`}
                            disabled={savingOfficialId === `${job.id}:work_task_repair`}
                            onClick={() => openOfficialSaveConfirm(job, "work_task_repair")}
                            type="button"
                          >
                            <ClipboardCheck className="w-3.5 h-3.5" /> {OFFICIAL_SAVE_LANES.work_task_repair.label}
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                  {officialSaveConfirm?.jobId === job.id ? (
                    <div
                      className="mt-4 rounded-lg border border-equine-cloud bg-white/85 p-3"
                      data-testid={`ai-draft-official-save-confirm-${job.id}`}
                    >
                      <div className="font-semibold text-equine-ink mb-1">
                        Confirm {OFFICIAL_SAVE_LANES[officialSaveConfirm.lane].collectionLabel} Save
                      </div>
                      <div className="text-[12.5px] text-equine-inkMuted leading-relaxed mb-3">
                        {OFFICIAL_SAVE_LANES[officialSaveConfirm.lane].description} This will write official records for this barn context and create audit evidence.
                      </div>
                      <label className="flex items-start gap-2 text-[13px] text-equine-ink" data-testid={`ai-draft-official-save-checkbox-label-${job.id}`}>
                        <input
                          checked={officialSaveChecked}
                          className="mt-1"
                          data-testid={`ai-draft-official-save-checkbox-${job.id}`}
                          onChange={(event) => setOfficialSaveChecked(event.target.checked)}
                          type="checkbox"
                        />
                        <span>I reviewed this AI draft, confirmed the barn context, and approve official save for this lane only.</span>
                      </label>
                      <div className="mt-3 flex flex-wrap gap-2">
                        <button
                          className="btn-primary inline-flex items-center gap-1.5 disabled:opacity-50"
                          data-testid={`ai-draft-official-save-confirm-submit-${job.id}`}
                          disabled={!officialSaveChecked || savingOfficialId === `${job.id}:${officialSaveConfirm.lane}`}
                          onClick={() => officialSaveDraft(job, officialSaveConfirm.lane)}
                          type="button"
                        >
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          {savingOfficialId === `${job.id}:${officialSaveConfirm.lane}` ? "Saving..." : "Confirm Official Save"}
                        </button>
                        <button
                          className="btn-secondary"
                          data-testid={`ai-draft-official-save-cancel-${job.id}`}
                          onClick={cancelOfficialSaveConfirm}
                          type="button"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : null}
                </div>
              ) : null}
              {inventoryCandidatesFor(job).length > 0 && (
                <div
                  className="mb-4 rounded-lg border border-equine-sage/25 bg-equine-sage/5 p-3"
                  data-testid={`ai-draft-inventory-candidates-${job.id}`}
                >
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div>
                      <div className="label-eyebrow-muted mb-1">Inventory Candidates</div>
                      <div className="text-[13px] text-equine-inkMuted leading-relaxed">
                        Review and correct these candidate items here, then use the explicit official-save confirmation when this lane is appropriate.
                      </div>
                    </div>
                    <StatusPill tone="warning" data-testid={`ai-draft-inventory-no-save-${job.id}`}>Not Saved</StatusPill>
                  </div>
                  <div className="space-y-3">
                    {inventoryCandidatesFor(job).map((candidate, index) => {
                      const editKey = candidateKeyFor(job, index);
                      const edits = candidateEdits[editKey] || {};
                      const disposition = candidateDisposition[editKey] || "needs_review";
                      const display = { ...candidate, ...edits };
                      return (
                        <div
                          key={editKey}
                          className="rounded-lg border border-equine-cloud bg-white/80 p-3"
                          data-testid={`ai-draft-inventory-candidate-${job.id}-${index}`}
                        >
                          <div className="flex flex-wrap items-start justify-between gap-3 mb-3">
                            <div className="min-w-0">
                              <div className="flex items-center gap-2 text-equine-ink font-display text-xl">
                                <PackageCheck className="w-4 h-4 text-equine-sage flex-shrink-0" />
                                <span className="truncate" data-testid={`ai-draft-inventory-candidate-name-${job.id}-${index}`}>
                                  {candidateFieldValue(display, "item_name", "Unnamed candidate")}
                                </span>
                              </div>
                              <div className="text-[12.5px] text-equine-inkMuted mt-1">
                                {candidateFieldValue(display, "category")} · {candidateFieldValue(display, "quantity", "Qty needs review")} {candidateFieldValue(display, "unit", "")}
                              </div>
                            </div>
                            <div className="flex flex-wrap gap-2 justify-end">
                              <StatusPill tone={disposition === "rejected" ? "critical" : disposition === "duplicate" ? "warning" : "neutral"} data-testid={`ai-draft-inventory-candidate-disposition-${job.id}-${index}`}>
                                {disposition === "duplicate" ? "Possible duplicate" : disposition === "rejected" ? "Rejected locally" : reviewLabelFor(display.review_status || "needs_review")}
                              </StatusPill>
                              <StatusPill tone="neutral" data-testid={`ai-draft-inventory-candidate-confidence-${job.id}-${index}`}>
                                {candidateFieldValue(display, "source_confidence", "Confidence needed")}
                              </StatusPill>
                            </div>
                          </div>
                          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3 mb-3">
                            {[
                              ["item_name", "Item"],
                              ["category", "Category"],
                              ["quantity", "Quantity"],
                              ["storage_location", "Storage"],
                            ].map(([field, label]) => (
                              <label key={field} className="block">
                                <span className="block text-[11px] uppercase tracking-[0.16em] text-equine-inkMuted mb-1">{label}</span>
                                <input
                                  className="w-full rounded-lg border border-equine-cloud bg-white px-3 py-2 text-[13px] text-equine-ink"
                                  data-testid={`ai-draft-inventory-edit-${field}-${job.id}-${index}`}
                                  onChange={(event) => updateCandidateEdit(job, index, field, event.target.value)}
                                  value={candidateFieldValue(display, field, "")}
                                />
                              </label>
                            ))}
                          </div>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mb-3 text-[12.5px] text-equine-inkMuted">
                            <div><span className="font-semibold text-equine-ink">Assign:</span> {candidateFieldValue(display, "horse_or_barn_assignment")}</div>
                            <div><span className="font-semibold text-equine-ink">Reorder:</span> {candidateFieldValue(display, "reorder_candidate", "Needs review")}</div>
                            <div><span className="font-semibold text-equine-ink">Unit:</span> {candidateFieldValue(display, "unit", "Needs review")}</div>
                          </div>
                          {arrayValue(display.notes).length > 0 && (
                            <div className="mb-3 text-[12.5px] text-equine-inkMuted" data-testid={`ai-draft-inventory-candidate-notes-${job.id}-${index}`}>
                              <span className="font-semibold text-equine-ink">Notes:</span> {arrayValue(display.notes).join(" ")}
                            </div>
                          )}
                          <div className="flex flex-wrap gap-2">
                            <button
                              className="btn-secondary inline-flex items-center gap-1.5 !py-1.5 !px-3 text-[12.5px]"
                              data-testid={`ai-draft-inventory-mark-reviewed-${job.id}-${index}`}
                              onClick={() => markCandidateDisposition(job, index, "locally_reviewed")}
                              type="button"
                            >
                              <CheckCircle2 className="w-3.5 h-3.5" /> Mark reviewed
                            </button>
                            <button
                              className="btn-secondary inline-flex items-center gap-1.5 !py-1.5 !px-3 text-[12.5px]"
                              data-testid={`ai-draft-inventory-mark-duplicate-${job.id}-${index}`}
                              onClick={() => markCandidateDisposition(job, index, "duplicate")}
                              type="button"
                            >
                              <Edit3 className="w-3.5 h-3.5" /> Mark duplicate
                            </button>
                            <button
                              className="btn-secondary inline-flex items-center gap-1.5 !py-1.5 !px-3 text-[12.5px]"
                              data-testid={`ai-draft-inventory-mark-rejected-${job.id}-${index}`}
                              onClick={() => markCandidateDisposition(job, index, "rejected")}
                              type="button"
                            >
                              <XCircle className="w-3.5 h-3.5" /> Reject candidate
                            </button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
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
