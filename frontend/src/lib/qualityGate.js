export const TW10_QA_CHECKS = [
  {
    id: "visual_system",
    label: "Visual System",
    status: "ready_for_review",
    proof: "Shared panels use existing Card, StatusPill, spacing, typography, and equine color tokens.",
    evidence: "Review homepage, role dashboards, admin, provider, billing, reporting, and mobile readiness surfaces.",
  },
  {
    id: "mobile_context",
    label: "Mobile Context",
    status: "ready_for_review",
    proof: "Mobile readiness remains the anchor for field recovery, scan intake, QR stall cards, and native handoff posture.",
    evidence: "Run mobile viewport screenshots before production launch review.",
  },
  {
    id: "accessibility",
    label: "Accessibility",
    status: "ready_for_review",
    proof: "Buttons, links, headings, loading states, empty states, and status labels need keyboard and screen-reader review.",
    evidence: "Run axe, focus, contrast, and reduced-motion checks in the release candidate.",
  },
  {
    id: "role_routes",
    label: "Role Routes",
    status: "guarded",
    proof: "Role dashboards, role landing paths, and role navigation stay mapped by explicit role groups.",
    evidence: "Route taxonomy tests must pass before any launch-readiness handoff.",
  },
  {
    id: "data_states",
    label: "Data States",
    status: "guarded",
    proof: "Critical surfaces should expose loading, empty, error, refresh, and last-verified states where relevant.",
    evidence: "Review data-loaded pages for empty/error state parity before launch.",
  },
  {
    id: "claim_boundary",
    label: "Claim Boundary",
    status: "blocked_until_verified",
    proof: "Launch, payments, signatures, provider lifecycle, broad messaging, exports, AI mutation, and multi-facility remain gated.",
    evidence: "Copy-drift scans must stay clean across public and app surfaces.",
  },
];

export const QA_STATUS = {
  ready_for_review: "Ready for review",
  guarded: "Guarded",
  blocked_until_verified: "Blocked until verified",
};

export const ROLE_ROUTE_QA_MATRIX = [
  ["facility", "/dashboard/facility", "admin, barn_owner"],
  ["manager", "/dashboard/manager", "barn_manager"],
  ["staff", "/dashboard/staff", "groom, working_student"],
  ["trainer", "/dashboard/trainer", "trainer"],
  ["owner", "/dashboard/owner", "horse_owner"],
  ["guardian", "/dashboard/guardian", "parent"],
  ["rider", "/dashboard/rider", "rider"],
  ["serviceProvider", "/dashboard/service-provider", "service_provider, veterinarian, farrier"],
  ["platformAdmin", "/admin/portal/dashboard", "platform role"],
];

export const LAUNCH_READINESS_EVIDENCE = [
  ["Approved Gates", "TW0 through TW9 are approved or implemented with tests."],
  ["TW10 Scope", "QA evidence, route contracts, accessibility posture, mobile checks, and copy-drift controls."],
  ["Release Blockers", "Provider-backed payments, signatures, exports, external messages, AI mutation, and multi-facility still need separate proof."],
  ["Visual Evidence", "Browser screenshots and mobile screenshots are required before founder launch review."],
];
