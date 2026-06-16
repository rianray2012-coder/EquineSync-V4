export const ADMIN_ROLES = ["admin", "barn_manager"];
export const STAFF_ROLES = ["admin", "barn_manager", "trainer", "groom", "working_student"];
export const CARE_PARTNER_ROLES = ["veterinarian", "farrier"];
export const OWNER_ROLES = ["horse_owner", "parent"];
// Marketplace-only roles — these accounts are self-signup. They get a session
// but no privileged scope; `role_status` (`active` | `pending_review`) gates
// any future admin elevation. Listed here for completeness/visibility only.
export const MARKETPLACE_ROLES = ["horse_owner", "rider", "trainer", "barn_owner", "service_provider"];

// Phase 15.C — mirror of the backend `barn:manage` capability (see
// /app/backend/core/permissions.py CAPABILITIES["barn:manage"]). Used to gate
// the Subscription Billing portal route + sidebar link. Stay in lockstep with
// the backend; if the backend extends `barn:manage`, extend this set too.
export const BARN_MANAGE_ROLES = [...ADMIN_ROLES];

export const ROLE_GROUPS = {
  admin: ADMIN_ROLES,
  staff: STAFF_ROLES,
  care: [...STAFF_ROLES, ...CARE_PARTNER_ROLES],
  financial: ADMIN_ROLES,
  training: STAFF_ROLES,
  communication: STAFF_ROLES,
  operations: STAFF_ROLES,
  locationShare: [...STAFF_ROLES, ...OWNER_ROLES],
  reporting: ["admin", "barn_manager", "trainer"],
  integrations: ADMIN_ROLES,
  ownerPortal: ["admin", "barn_manager", "trainer", ...OWNER_ROLES],
  barnManage: BARN_MANAGE_ROLES,
};

export const canAccessRole = (user, roles) => {
  if (!roles || roles.length === 0) return true;
  return roles.includes(user?.role);
};

// Phase 15.C — frontend mirror of `require(user, "barn:manage")`. Returns
// true when the current user can reach the subscription billing portal /
// kick off a Stripe Checkout. Source of truth is the backend capability
// table; this helper exists so individual pages don't hard-code role names.
export const canManageBilling = (user) => canAccessRole(user, BARN_MANAGE_ROLES);

// ----------------------------------------------------------------------
// Admin Portal — platform-level roles (Admin-1, Feb 2026)
// ----------------------------------------------------------------------
// Mirrors backend core/permissions.py::PLATFORM_ROLES. These live on
// user.platform_role and are SEPARATE from the barn-scoped user.role.
// Existing role="admin" users are NOT auto-elevated to platform admin.
export const PLATFORM_ROLES = [
  "super_admin",
  "platform_admin",
  "support_admin",
  "billing_admin",
  "read_only_auditor",
];

export const getPlatformRole = (user) =>
  String((user?.platform_role || "")).trim().toLowerCase();

export const isPlatformAdmin = (user) =>
  PLATFORM_ROLES.includes(getPlatformRole(user));

export const hasPlatformRole = (user, ...allowed) => {
  const pr = getPlatformRole(user);
  if (!pr || !PLATFORM_ROLES.includes(pr)) return false;
  if (!allowed.length) return true;
  return allowed.map((r) => String(r).toLowerCase()).includes(pr);
};

export const canAccessAdminPortal = (user) => isPlatformAdmin(user);

// Section → allowed platform_role values. Mirrors backend
// admin_portal.SECTION_CAPABILITIES. Kept here only for sidebar gating;
// the backend is the source of truth and re-checks on every read.
export const ADMIN_SECTION_CAPS = {
  dashboard:     ["super_admin", "platform_admin", "support_admin", "billing_admin", "read_only_auditor"],
  users:         ["super_admin", "platform_admin", "support_admin"],
  facilities:    ["super_admin", "platform_admin", "support_admin"],
  horses:        ["super_admin", "platform_admin", "support_admin"],
  approvals:     ["super_admin", "platform_admin"],
  subscriptions: ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
  billing:       ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
  permissions:   ["super_admin", "platform_admin"],
  support:       ["super_admin", "platform_admin", "support_admin"],
  alerts:        ["super_admin", "platform_admin", "support_admin", "billing_admin"],
  reports:       ["super_admin", "platform_admin", "support_admin", "billing_admin", "read_only_auditor"],
  integrations:  ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
  settings:      ["super_admin", "platform_admin"],
  audit_logs:    ["super_admin", "platform_admin", "read_only_auditor"],
};

export const canSeeAdminSection = (user, sectionKey) => {
  const allowed = ADMIN_SECTION_CAPS[sectionKey];
  if (!allowed) return false;
  return allowed.includes(getPlatformRole(user));
};

// Admin-7B (locked Feb 2026) — reports CSV export is gated tighter
// than reports read. support_admin can SEE reports but cannot export.
// Mirrors backend portal.py::_REPORTS_CSV_ROLES.
export const ADMIN_REPORTS_CSV_ROLES = [
  "super_admin", "platform_admin", "billing_admin", "read_only_auditor",
];

export const canExportAdminReports = (user) =>
  ADMIN_REPORTS_CSV_ROLES.includes(getPlatformRole(user));
