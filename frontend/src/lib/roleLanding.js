import { isPlatformAdmin } from "./permissions";

export const SETUP_ROUTE = "/setup/facility";
export const LEGACY_SETUP_ROUTE = "/onboarding";

export const ROLE_HOME_PATHS = {
  rider: "/role-home/rider",
  guardian: "/role-home/guardian",
  owner: "/role-home/owner",
  barnOwner: "/role-home/barn-owner",
  trainer: "/role-home/trainer",
  manager: "/role-home/manager",
  staff: "/role-home/staff",
  facilityAdmin: "/dashboard",
  platformAdmin: "/admin/portal/dashboard",
};

export const DASHBOARD_PATHS = {
  facility: "/dashboard/facility",
  manager: "/dashboard/manager",
  staff: "/dashboard/staff",
  trainer: "/dashboard/trainer",
  owner: "/dashboard/owner",
  guardian: "/dashboard/guardian",
  rider: "/dashboard/rider",
  serviceProvider: "/dashboard/service-provider",
  platformAdmin: "/admin/portal/dashboard",
};

export const ROLE_INTAKE_PATHS = {
  rider: "/role-intake/rider",
  guardian: "/role-intake/guardian",
  owner: "/role-intake/owner",
  barnOwner: "/role-intake/barn-owner",
  trainer: "/role-intake/trainer",
  manager: "/role-intake/manager",
  staff: "/role-intake/staff",
};

export const SETUP_READINESS_ROLES = ["admin", "barn_owner", "barn_manager"];
export const SETUP_ELIGIBLE_ROLES = ["admin", "barn_owner", "barn_manager"];
export const SERVICE_PROVIDER_ROLES = ["service_provider", "veterinarian", "farrier"];

export const isFacilitySetupVisible = (user) => {
  if (!user || isPlatformAdmin(user)) return false;
  return SETUP_READINESS_ROLES.includes(String(user.role || "").toLowerCase());
};

export const isFacilitySetupEligible = (user) => {
  if (!user || isPlatformAdmin(user)) return false;
  return SETUP_ELIGIBLE_ROLES.includes(String(user.role || "").toLowerCase());
};

export const shouldRouteToFacilitySetup = (user) => {
  if (!isFacilitySetupEligible(user)) return false;
  return user.onboarding_completed === false || user.facility_setup_complete === false;
};

export const ownerHorsePath = (user) => {
  const horseId =
    user?.primary_horse_id ||
    user?.horse_id ||
    user?.linked_horse_id ||
    user?.owner_horse_id;
  return horseId ? `/owner/horses/${horseId}` : ROLE_INTAKE_PATHS.owner;
};

export const isRoleIntakeComplete = (user) =>
  user?.role_intake_completed === true ||
  user?.intake_completed === true ||
  user?.profile_completed === true;

export const shouldRouteToSubscriptionBilling = (user) => {
  const role = String(user?.role || "").toLowerCase();
  const status = String(user?.subscription_status || "").toLowerCase();
  const plan = String(user?.subscription_plan_code || user?.membership_tier || "").toLowerCase();

  return (
    role === "horse_owner" &&
    ["individual_owner", "private_owner_plus"].includes(plan) &&
    ["pending_payment", "incomplete", "incomplete_expired", "past_due", "unpaid"].includes(status)
  );
};

export const resolveDashboardPath = (user) => {
  if (!user) return "/login";
  if (isPlatformAdmin(user)) return DASHBOARD_PATHS.platformAdmin;

  const role = String(user.role || "").toLowerCase();

  if (role === "admin" || role === "barn_owner") return DASHBOARD_PATHS.facility;
  if (role === "barn_manager") return DASHBOARD_PATHS.manager;
  if (role === "trainer") return DASHBOARD_PATHS.trainer;
  if (role === "groom" || role === "working_student") return DASHBOARD_PATHS.staff;
  if (role === "horse_owner") return DASHBOARD_PATHS.owner;
  if (role === "parent") return DASHBOARD_PATHS.guardian;
  if (role === "rider") return DASHBOARD_PATHS.rider;
  if (SERVICE_PROVIDER_ROLES.includes(role)) return DASHBOARD_PATHS.serviceProvider;

  return "/settings";
};

export const resolveRoleIntakePath = (user) => {
  const role = String(user?.role || "").toLowerCase();

  if (role === "trainer") return ROLE_INTAKE_PATHS.trainer;
  if (role === "barn_manager") return ROLE_INTAKE_PATHS.manager;
  if (role === "groom" || role === "working_student") return ROLE_INTAKE_PATHS.staff;
  if (role === "horse_owner") return ROLE_INTAKE_PATHS.owner;
  if (role === "parent") return ROLE_INTAKE_PATHS.guardian;
  if (role === "rider") return ROLE_INTAKE_PATHS.rider;

  return resolveDashboardPath(user);
};

export const legacyIntakePathFor = (requestedPath) => {
  const legacy = {
    "/intake/facility-founder": ROLE_INTAKE_PATHS.barnOwner,
    "/intake/manager": ROLE_INTAKE_PATHS.manager,
    "/intake/staff": ROLE_INTAKE_PATHS.staff,
    "/intake/trainer": ROLE_INTAKE_PATHS.trainer,
    "/intake/owner": ROLE_INTAKE_PATHS.owner,
    "/intake/guardian": ROLE_INTAKE_PATHS.guardian,
    "/intake/rider": ROLE_INTAKE_PATHS.rider,
  };
  return legacy[requestedPath] || null;
};

export const resolvePostLoginPath = (user) => {
  if (!user) return "/login";
  if (isPlatformAdmin(user)) return DASHBOARD_PATHS.platformAdmin;

  const role = String(user.role || "").toLowerCase();

  if (shouldRouteToSubscriptionBilling(user)) return "/billing/subscription";

  if (SETUP_ELIGIBLE_ROLES.includes(role)) {
    return shouldRouteToFacilitySetup(user) ? SETUP_ROUTE : resolveDashboardPath(user);
  }

  if (SERVICE_PROVIDER_ROLES.includes(role)) return DASHBOARD_PATHS.serviceProvider;

  if (["trainer", "groom", "working_student", "horse_owner", "parent", "rider"].includes(role)) {
    return isRoleIntakeComplete(user) ? resolveDashboardPath(user) : resolveRoleIntakePath(user);
  }

  return resolveDashboardPath(user);
};

export const safeRedirectPath = (user, requestedPath) => {
  if (!requestedPath || !requestedPath.startsWith("/") || requestedPath.startsWith("//")) {
    return resolvePostLoginPath(user);
  }
  if (isPlatformAdmin(user)) {
    return requestedPath.startsWith("/admin/portal")
      ? requestedPath
      : ROLE_HOME_PATHS.platformAdmin;
  }
  if (requestedPath.startsWith("/admin/portal")) return resolvePostLoginPath(user);
  if (requestedPath === LEGACY_SETUP_ROUTE) {
    return isFacilitySetupVisible(user) ? SETUP_ROUTE : resolvePostLoginPath(user);
  }
  const legacyIntakePath = legacyIntakePathFor(requestedPath);
  if (legacyIntakePath) return legacyIntakePath;
  const isSetupPath = requestedPath === SETUP_ROUTE || requestedPath.startsWith(`${SETUP_ROUTE}/`);
  if (isSetupPath && !isFacilitySetupVisible(user)) {
    return resolvePostLoginPath(user);
  }
  return requestedPath;
};
