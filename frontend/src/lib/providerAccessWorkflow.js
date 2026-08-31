export const PROVIDER_ACCESS_SIGNALS = [
  {
    id: "invite_scope",
    label: "Invite Scope",
    status: "gated",
    proof: "Provider access begins with an explicit facility grant for a specific horse, service type, and time window.",
    nextStep: "Add scoped invite creation only after audit persistence and expiration rules are approved.",
  },
  {
    id: "visit_packet",
    label: "Visit Packet",
    status: "planned",
    proof: "A visit packet should contain only approved horse context, appointment details, care cautions, and provider-safe documents.",
    nextStep: "Create packet assembly after document visibility and emergency fields are verified.",
  },
  {
    id: "revocation",
    label: "Revocation",
    status: "gated",
    proof: "Every provider grant needs an owner or facility-visible revoke path and a clear expiration state.",
    nextStep: "Add revoke controls only after backend grant lifecycle transitions are tested.",
  },
  {
    id: "reviewed_notes",
    label: "Reviewed Notes",
    status: "review_needed",
    proof: "Provider notes and outcomes should enter review before broader owner or staff visibility.",
    nextStep: "Connect note drafts to review states before any owner-facing publish action exists.",
  },
  {
    id: "document_boundary",
    label: "Document Boundary",
    status: "provider_required",
    proof: "Provider document upload and signature workflows remain provider-required until storage and signature proof exists.",
    nextStep: "Keep document actions informational until provider-backed storage and signature gates are approved.",
  },
  {
    id: "communication_boundary",
    label: "Communication Boundary",
    status: "gated",
    proof: "Provider communication should stay inside reviewed EquineSync surfaces until external delivery is separately approved.",
    nextStep: "Add message delivery only after channel consent, urgency rules, and audit trails are verified.",
  },
  {
    id: "billing_handoff",
    label: "Billing Handoff",
    status: "planned",
    proof: "Provider billing can show handoff context without activating payments or invoice collection.",
    nextStep: "Move billing workflows to TW-9 with payment-provider proof.",
  },
  {
    id: "emergency_mode",
    label: "Emergency Mode",
    status: "gated",
    proof: "Emergency provider access needs narrow scope, reason capture, expiration, and visible audit evidence.",
    nextStep: "Require a separate emergency-access approval path before any live emergency grant.",
  },
];

export const PROVIDER_ACCESS_STATUS = {
  gated: "Gated",
  planned: "Planned",
  review_needed: "Review needed",
  provider_required: "Provider required",
};

export const PROVIDER_ACCESS_STOP_RULES = [
  "Provider users are not staff, trainer, owner, or admin substitutes.",
  "No live invite, revoke, emergency, document upload, signature, payment, external message, or multi-facility action is created in TW-8.",
  "Provider-visible context must remain grant-scoped and review-aware.",
];
