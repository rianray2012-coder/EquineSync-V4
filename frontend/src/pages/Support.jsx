import React, { useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, LifeBuoy, Send, Sparkles } from "lucide-react";
import { toast } from "sonner";
import { Card, PageHeader, StatusPill } from "../components/Primitives";
import { api } from "../lib/api";
import { useAuth } from "../context/AuthContext";

const CATEGORIES = [
  ["bug", "Bug or broken flow"],
  ["access", "Access or role issue"],
  ["billing", "Billing or membership"],
  ["data", "Data looks wrong"],
  ["workflow", "Workflow question"],
  ["feedback", "Product feedback"],
  ["other", "Other"],
];

const SEVERITIES = [
  ["low", "Low"],
  ["medium", "Medium"],
  ["high", "High"],
  ["urgent", "Urgent"],
];

const INITIAL_FORM = {
  category: "bug",
  severity: "medium",
  subject: "",
  message: "",
  preferred_contact: "app",
};

const fieldClass =
  "mt-2 w-full rounded-xl border border-equine-cloud bg-white px-3 py-3 text-equine-ink placeholder:text-equine-inkSoft outline-none focus:border-equine-lilac focus:ring-2 focus:ring-equine-lavender/35";

const severityCopy = {
  low: "Cosmetic, confusing, or nice-to-have.",
  medium: "Blocks a small task but has a workaround.",
  high: "Blocks normal use for a pilot role.",
  urgent: "Safety, privacy, payment, or access boundary concern.",
};

export default function Support() {
  const { user } = useAuth();
  const [form, setForm] = useState(INITIAL_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [createdTicket, setCreatedTicket] = useState(null);

  const pageUrl = useMemo(() => {
    if (typeof window === "undefined") return "";
    return window.location.href;
  }, []);

  const update = (key, value) => setForm((current) => ({ ...current, [key]: value }));

  const submit = async (event) => {
    event.preventDefault();
    if (!form.subject.trim() || !form.message.trim()) {
      toast.error("Add a subject and details before sending.");
      return;
    }
    setSubmitting(true);
    try {
      const response = await api.post("/support/tickets", {
        ...form,
        subject: form.subject.trim(),
        message: form.message.trim(),
        page_url: pageUrl,
        device_context: typeof navigator !== "undefined" ? navigator.userAgent : "",
      });
      setCreatedTicket(response.data.ticket);
      setForm(INITIAL_FORM);
      toast.success("Support request sent");
    } catch (error) {
      toast.error(error?.response?.data?.detail || "Could not send support request");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div data-testid="support-page">
      <PageHeader
        eyebrow="Pilot Support"
        title="Support"
        subtitle="Send bugs, access issues, workflow questions, and product feedback directly to the EquineSync pilot support queue."
        action={
          <StatusPill tone={createdTicket ? "success" : "info"} dot>
            {createdTicket ? "Submitted" : "Founder triage"}
          </StatusPill>
        }
      />

      {createdTicket && (
        <Card className="mb-6 !border-equine-sage/30" data-testid="support-confirmation">
          <div className="flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-equine-sage mt-0.5 flex-shrink-0" />
            <div>
              <div className="label-eyebrow">Request received</div>
              <h2 className="font-display text-2xl text-equine-ink mt-1">Ticket {createdTicket.admin_ref}</h2>
              <p className="text-equine-inkMuted text-[13.5px] mt-2">
                Status is {createdTicket.status}. Rian will triage this in the platform Support dashboard.
              </p>
            </div>
          </div>
        </Card>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-[minmax(0,1fr)_320px] gap-6">
        <Card hover={false}>
          <form onSubmit={submit} className="space-y-5" data-testid="support-form">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <label className="block">
                <span className="label-eyebrow">Category</span>
                <select
                  value={form.category}
                  onChange={(event) => update("category", event.target.value)}
                  data-testid="support-category"
                  className={fieldClass}
                >
                  {CATEGORIES.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
                </select>
              </label>
              <label className="block">
                <span className="label-eyebrow">Severity</span>
                <select
                  value={form.severity}
                  onChange={(event) => update("severity", event.target.value)}
                  data-testid="support-severity"
                  className={fieldClass}
                >
                  {SEVERITIES.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
                </select>
              </label>
            </div>

            <label className="block">
              <span className="label-eyebrow">Subject</span>
              <input
                type="text"
                value={form.subject}
                onChange={(event) => update("subject", event.target.value)}
                maxLength={140}
                data-testid="support-subject"
                className={fieldClass}
                placeholder="Short summary"
              />
            </label>

            <label className="block">
              <span className="label-eyebrow">Details</span>
              <textarea
                value={form.message}
                onChange={(event) => update("message", event.target.value)}
                rows={8}
                maxLength={4000}
                data-testid="support-message"
                className={`${fieldClass} resize-y`}
                placeholder="What happened, what you expected, and what role or horse/facility context you were using."
              />
            </label>

            <label className="block">
              <span className="label-eyebrow">Preferred follow-up</span>
              <select
                value={form.preferred_contact}
                onChange={(event) => update("preferred_contact", event.target.value)}
                data-testid="support-preferred-contact"
                className={fieldClass}
              >
                <option value="app">In-app / account email</option>
                <option value="email">Email</option>
                <option value="phone">Phone if already on file</option>
                <option value="no_preference">No preference</option>
              </select>
            </label>

            <div className="flex items-center justify-between gap-4 flex-wrap pt-1">
              <div className="text-[12px] text-equine-inkMuted">
                Signed in as {user?.email || "current user"}
              </div>
              <button
                type="submit"
                disabled={submitting}
                data-testid="support-submit"
                className="btn-primary inline-flex items-center gap-2 disabled:opacity-50"
              >
                <Send className="w-4 h-4" />
                {submitting ? "Sending..." : "Send request"}
              </button>
            </div>
          </form>
        </Card>

        <div className="space-y-4">
          <Card hover={false} data-testid="support-severity-guide">
            <div className="flex items-center gap-2 label-eyebrow">
              <AlertTriangle className="w-3.5 h-3.5" />
              Severity guide
            </div>
            <div className="mt-4 space-y-3">
              {SEVERITIES.map(([value, label]) => (
                <div key={value} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-3">
                  <div className="text-equine-ink text-[13px] font-medium">{label}</div>
                  <div className="text-equine-inkMuted text-[12px] mt-1 leading-relaxed">{severityCopy[value]}</div>
                </div>
              ))}
            </div>
          </Card>

          <Card hover={false}>
            <div className="flex items-center gap-2 label-eyebrow">
              <LifeBuoy className="w-3.5 h-3.5" />
              Pilot owner
            </div>
            <div className="mt-3 flex items-start gap-3">
              <Sparkles className="w-4 h-4 text-equine-lilac mt-0.5 flex-shrink-0" />
              <div className="text-[13px] text-equine-inkMuted leading-relaxed">
                Founder Rian Ray owns support review and triage before outside tester launch.
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
