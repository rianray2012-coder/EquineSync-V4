export const BUSINESS_PROOF_SIGNALS = [
  {
    id: "plan_fit",
    label: "Plan Fit",
    status: "visible_now",
    proof: "Pricing and subscription surfaces should explain which plan fits the user's operating model.",
    nextStep: "Add segment-specific plan guidance after public catalog copy is reviewed.",
  },
  {
    id: "billing_clarity",
    label: "Billing Clarity",
    status: "provider_required",
    proof: "Billing records, payment profiles, subscriptions, and provider processing must stay visibly separate.",
    nextStep: "Move payment activation to a separate provider-proof gate before live collection claims.",
  },
  {
    id: "activation_metrics",
    label: "Activation Metrics",
    status: "visible_now",
    proof: "Setup health and invite acceptance can show adoption signals without claiming production readiness.",
    nextStep: "Add owner and trainer activation metrics after event definitions are approved.",
  },
  {
    id: "capability_matrix",
    label: "Capability Matrix",
    status: "visible_now",
    proof: "Public pages should distinguish available, pilot, provider-required, gated, and planned capabilities.",
    nextStep: "Keep the matrix aligned with the product-status registry before marketing expansion.",
  },
  {
    id: "portability",
    label: "Portability",
    status: "gated",
    proof: "Horse ledger, account data, and report exports need clear portability posture before live export promises.",
    nextStep: "Add export workflows only after scope, format, permissions, and audit evidence are approved.",
  },
  {
    id: "public_proof",
    label: "Public Proof",
    status: "planned",
    proof: "Screenshots, demos, testimonials, and founder scenarios should only claim verified product behavior.",
    nextStep: "Create public proof assets after visual QA and launch-safe claims review.",
  },
];

export const BUSINESS_STATUS = {
  visible_now: "Visible now",
  provider_required: "Provider required",
  gated: "Gated",
  planned: "Planned",
};

export const PUBLIC_CAPABILITY_MATRIX = [
  ["Horse Ledger & Passport", "Visible now", "Care history positioning and record foundation are approved."],
  ["Barn Operations", "Visible now", "Core horse, staff, care, owner, and facility surfaces exist within role gates."],
  ["Owner Requests", "Pilot", "Request and review language is present; deeper state persistence remains gated."],
  ["Provider Access", "Gated", "Provider workflow is mapped in TW8 but live invite and revocation controls remain gated."],
  ["Payments", "Provider required", "Billing readiness is visible; live processing depends on Stripe proof."],
  ["Documents & Signatures", "Provider required", "Document records exist; signature activation requires provider proof."],
  ["Data Export & Portability", "Gated", "Export posture is planned and must be separately approved before live claims."],
  ["Multi-Facility", "Unavailable", "Multi-facility switching remains unavailable until permission-safe isolation is proven."],
];
