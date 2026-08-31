export const PROOF_SIGNALS = {
  facility: [
    ["Last Verified", "Dashboard data shows a refresh timestamp when loaded."],
    ["Decision Queue", "Owner requests, incidents, and billing exceptions stay visible before secondary analytics."],
    ["Audit Path", "Critical admin and billing changes remain tied to existing audit and support records."],
    ["Readiness Boundary", "Provider, payment, document, and messaging activation stay gated until their dependencies are verified."],
  ],
  handoff: [
    ["Shift Status", "Draft, submitted, and reviewed handoff reports keep shift context explicit."],
    ["Open Items", "Open tasks and shift notes are shown beside each handoff before review."],
    ["Review Proof", "Submitted and reviewed timestamps are recorded by the existing handoff update flow."],
    ["Exception Context", "Priority and blocked/open task status highlight what still needs manager attention."],
  ],
  support: [
    ["Opaque Refs", "Support rows use opaque ticket references instead of exposing internal identifiers."],
    ["Audit Path", "Status changes, assignments, and notes remain audit-logged by existing server controls."],
    ["No Unsafe Impersonation", "Support diagnostics do not create impersonation or hidden privilege in this gate."],
    ["Privacy Boundary", "Internal note bodies stay in ticket records, not audit metadata."],
  ],
  admin: [
    ["Read Only", "The platform dashboard remains read-only for operational review."],
    ["Access Summary", "Platform role and visible sections explain current admin capability."],
    ["Activity Trail", "Activity feed and subscription health remain separate so one stale feed does not hide other proof."],
    ["Launch Boundary", "Admin health visibility does not activate launch, payments, provider access, or messaging delivery."],
  ],
};

export const FACILITY_READINESS_AREAS = [
  {
    id: "horses",
    label: "Horses",
    proof: "Horse records establish the operating roster.",
  },
  {
    id: "staff",
    label: "Staff",
    proof: "Staff setup establishes who can act on daily work.",
  },
  {
    id: "owners",
    label: "Owners",
    proof: "Owner setup controls approved visibility and request paths.",
  },
  {
    id: "schedules",
    label: "Schedules",
    proof: "Scheduling context reduces handoff and lesson conflicts.",
  },
  {
    id: "billing",
    label: "Billing",
    proof: "Billing remains provider-required until payment processing is verified.",
  },
  {
    id: "documents",
    label: "Documents",
    proof: "Documents and signatures remain provider-required until workflows are verified.",
  },
  {
    id: "emergency_contacts",
    label: "Emergency Contacts",
    proof: "Emergency contact readiness supports urgent-care confidence.",
  },
  {
    id: "permissions",
    label: "Permissions",
    proof: "Role and capability boundaries explain who can see or change each surface.",
  },
];

export const readinessStatusFor = (area, progress, steps = []) => {
  const stepIds = steps.map((step) => step.id);
  const stepStatus = progress?.steps || {};
  if (stepStatus[area.id] === "complete") return "complete";
  if (stepStatus[area.id] === "in_progress") return "in_progress";
  if (stepIds.includes(area.id)) return stepStatus[area.id] || "pending";
  if (["billing", "documents"].includes(area.id)) return "provider_required";
  if (area.id === "permissions") return "gated";
  return "planned";
};
