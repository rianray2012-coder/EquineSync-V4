import { isPlatformAdmin } from "./permissions";

export const ROLE_HOME_PATHS = {
  rider: "/role-home/rider",
  guardian: "/role-home/guardian",
  owner: "/role-home/owner",
  barnOwner: "/role-home/barn-owner",
  staff: "/today",
  manager: "/today",
  facilityAdmin: "/dashboard",
  platformAdmin: "/admin/portal/dashboard",
};

export const SETUP_ELIGIBLE_ROLES = ["admin", "barn_owner"];

export const isFacilitySetupEligible = (user) => {
  if (!user || isPlatformAdmin(user)) return false;
  return SETUP_ELIGIBLE_ROLES.includes(user.role);
};

export const ownerHorsePath = (user) => {
  const horseId =
    user?.primary_horse_id ||
    user?.horse_id ||
    user?.linked_horse_id ||
    user?.owner_horse_id;
  return horseId ? `/owner/horses/${horseId}` : ROLE_HOME_PATHS.owner;
};

export const resolvePostLoginPath = (user) => {
  if (!user) return "/login";
  if (isPlatformAdmin(user)) return ROLE_HOME_PATHS.platformAdmin;

  const role = String(user.role || "").toLowerCase();

  if (role === "barn_owner") return ROLE_HOME_PATHS.barnOwner;

  if (role === "admin") {
    if (user.onboarding_completed === false || user.facility_setup_complete === false) {
      return "/onboarding";
    }
    return ROLE_HOME_PATHS.facilityAdmin;
  }

  if (role === "barn_manager" || role === "trainer") return ROLE_HOME_PATHS.manager;
  if (role === "groom" || role === "working_student") return ROLE_HOME_PATHS.staff;
  if (role === "horse_owner") return ownerHorsePath(user);
  if (role === "parent") return ROLE_HOME_PATHS.guardian;
  if (role === "rider") return ROLE_HOME_PATHS.rider;

  return "/dashboard";
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
  if (requestedPath === "/onboarding" && !isFacilitySetupEligible(user)) {
    return resolvePostLoginPath(user);
  }
  return requestedPath;
};
