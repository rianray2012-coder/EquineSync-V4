export const DECISION_STATES = {
  submitted: {
    label: "Submitted",
    tone: "info",
    meaning: "The request or note has been created and is waiting for review.",
  },
  seen: {
    label: "Seen",
    tone: "neutral",
    meaning: "An authorized team member has viewed it.",
  },
  assigned: {
    label: "Assigned",
    tone: "info",
    meaning: "A responsible person is attached to the work.",
  },
  scheduled: {
    label: "Scheduled",
    tone: "warning",
    meaning: "The next action has a planned time or service window.",
  },
  needs_review: {
    label: "Needs Review",
    tone: "warning",
    meaning: "It must be checked before broader visibility or completion.",
  },
  owner_visible: {
    label: "Owner Visible",
    tone: "success",
    meaning: "The item is approved for owner-facing visibility.",
  },
  internal_only: {
    label: "Internal Only",
    tone: "neutral",
    meaning: "The item stays inside staff or facility operations.",
  },
  completed: {
    label: "Completed",
    tone: "success",
    meaning: "The work is closed with a recorded outcome.",
  },
  declined_with_note: {
    label: "Declined With Note",
    tone: "neutral",
    meaning: "The request is not approved and includes owner-safe context when provided.",
  },
};

// Role North Star copy answers: What changed, what needs a decision,
// what is safe to ignore, and what proof supports trust.
export const ROLE_NORTH_STAR = {
  trainer: {
    eyebrow: "Trainer North Star",
    title: "Today's Trainer Work",
    status: "gated-read-only",
    changed: "Assigned horses, lessons, active plans, and rider context update from the trainer operating center.",
    decision: "Review owner requests and training context before publishing owner-visible follow-up.",
    safe: "Billing, provider grants, staff admin, and multi-facility switching remain outside this trainer surface.",
    proof: "Read-only assigned-work visibility stays facility-gated and tied to stable trainer identity.",
  },
  owner: {
    eyebrow: "Owner North Star",
    title: "Horse Confidence",
    status: "facility-gated",
    changed: "Facility-approved care, requests, documents, messages, and billing context stay organized around the horse.",
    decision: "Use approved request paths for care questions, scheduling needs, billing questions, or barn follow-up.",
    safe: "Staff-only notes and internal payloads stay hidden unless the facility approves visibility.",
    proof: "Owner-facing status should show source, visibility, and review state before it appears as trusted truth.",
  },
  guardian: {
    eyebrow: "Guardian North Star",
    title: "Rider Support",
    status: "facility-gated",
    changed: "Schedule, progress notes, documents, requests, and emergency context center on the minor rider.",
    decision: "Use guardian-safe requests and document workflows for follow-up that needs barn review.",
    safe: "Formal consent, waivers, billing, and staff-only work remain separate from rider-facing progress.",
    proof: "Guardian-visible information must be barn-approved and linked to the correct rider relationship.",
  },
  rider: {
    eyebrow: "Rider North Star",
    title: "Program Progress",
    status: "program-gated",
    changed: "Lessons, schedule, goals, progress notes, and announcements appear as the program is connected.",
    decision: "Keep requests focused on barn-approved rider support and lesson follow-up.",
    safe: "Rider profile updates do not replace guardian consent, signed waivers, or formal enrollment.",
    proof: "Rider progress should remain tied to trainer or barn-approved source context.",
  },
  manager: {
    eyebrow: "Manager North Star",
    title: "Daily Operations Desk",
    status: "live-plus-gated",
    changed: "Tasks, horses, owner requests, health alerts, schedule pressure, and facility setup status are the priority scan.",
    decision: "Clear overdue work, owner requests, document gaps, incidents, and schedule conflicts before secondary analytics.",
    safe: "Provider access, payments, broad messages, and documents stay governed by their own readiness gates.",
    proof: "Use timestamps, review queues, audit logs, and setup readiness to explain what happened and what remains blocked.",
  },
  serviceProvider: {
    eyebrow: "Provider North Star",
    title: "Scoped Visit Context",
    status: "gated-provider-access",
    changed: "Shared horses, visit notes, vet/farrier records, and appointment context are limited to explicit grants.",
    decision: "Provider notes and outcomes require review before broader owner or staff visibility.",
    safe: "Provider users are not staff, trainer, owner, or admin substitutes.",
    proof: "Every provider view or action needs scoped grant, expiration, review, and audit evidence before expansion.",
  },
};

export const normalizeDecisionState = (status) => {
  const key = String(status || "submitted").toLowerCase();
  return DECISION_STATES[key] ? key : "submitted";
};

export const decisionStateForServiceRequest = (request) => {
  const status = String(request?.status || "pending").toLowerCase();
  if (status === "approved" || status === "completed") return "completed";
  if (status === "declined" || status === "rejected") return "declined_with_note";
  if (status === "scheduled") return "scheduled";
  if (status === "assigned") return "assigned";
  if (request?.seen_at || request?.reviewed_at) return "seen";
  return "submitted";
};
