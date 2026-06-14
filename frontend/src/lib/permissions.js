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
