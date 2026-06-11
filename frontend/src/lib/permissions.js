export const ADMIN_ROLES = ["admin", "barn_manager"];
export const STAFF_ROLES = ["admin", "barn_manager", "trainer", "groom", "working_student"];
export const CARE_PARTNER_ROLES = ["veterinarian", "farrier"];
export const OWNER_ROLES = ["horse_owner", "parent"];

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
};

export const canAccessRole = (user, roles) => {
  if (!roles || roles.length === 0) return true;
  return roles.includes(user?.role);
};
