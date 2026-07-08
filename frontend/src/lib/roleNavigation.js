import { isPlatformAdmin } from "./permissions";
import { DASHBOARD_PATHS, SERVICE_PROVIDER_ROLES, SETUP_ROUTE } from "./roleLanding";

const dashboardFor = (profile) => DASHBOARD_PATHS[profile] || "/dashboard";

const item = (to, label, icon, extra = {}) => ({ to, label, icon, ...extra });

export const PLATFORM_NAVIGATION = [
  {
    label: "Platform",
    items: [
      item("/admin/portal/dashboard", "Admin Portal", "shield"),
      item("/admin/portal/users", "Users", "users"),
      item("/admin/portal/facilities", "Facilities", "facility"),
      item("/admin/portal/billing", "Platform Billing", "billing"),
    ],
  },
  {
    label: "Account",
    items: [item("/admin/portal/settings", "Profile", "settings")],
  },
];

export const FACILITY_ADMIN_NAVIGATION = [
  {
    label: "Facility Admin",
    items: [
      item(DASHBOARD_PATHS.facility, "Dashboard", "dashboard", { end: true }),
      item(SETUP_ROUTE, "Setup", "sparkles"),
      item("/horses", "Horses", "horse"),
      item("/owners", "Owners", "users"),
      item("/riders", "Riders", "profile"),
      item("/staff", "Staff", "team"),
      item("/arena-schedule", "Schedule", "calendar"),
      item("/today", "Tasks", "tasks"),
    ],
  },
  {
    label: "Business",
    items: [
      item("/billing", "Billing", "billing"),
      item("/forms-signatures", "Documents", "documents"),
      item("/reports", "Reports", "reports"),
      item("/settings", "Facility Settings", "settings"),
      item("/messaging", "Messages", "messages"),
    ],
  },
];

export const MANAGER_NAVIGATION = [
  {
    label: "Manager",
    items: [
      item(DASHBOARD_PATHS.manager, "Dashboard", "dashboard", { end: true }),
      item("/today", "Tasks", "tasks"),
      item("/horses", "Horses", "horse"),
      item("/staff", "Staff", "team"),
      item("/arena-schedule", "Schedule", "calendar"),
      item("/health", "Health Alerts", "health"),
      item("/review-queue", "Owner Requests", "requests", { reviewBadge: true }),
    ],
  },
  {
    label: "Operations",
    items: [
      item("/barn-locations", "Facility", "map"),
      item("/reports", "Reports", "reports"),
      item("/messaging", "Messages", "messages"),
      item("/settings", "Settings", "settings"),
    ],
  },
];

export const TRAINER_NAVIGATION = [
  {
    label: "Trainer",
    items: [
      item(DASHBOARD_PATHS.trainer, "Dashboard", "dashboard", { end: true }),
      item("/today", "Tasks", "tasks"),
      item("/horses", "Horses", "horse"),
      item("/arena-schedule", "Schedule", "calendar"),
      item("/health", "Health Alerts", "health"),
      item("/review-queue", "Owner Requests", "requests", { reviewBadge: true }),
    ],
  },
  {
    label: "Program",
    items: [
      item("/barn-locations", "Facility", "map"),
      item("/reports", "Reports", "reports"),
      item("/messaging", "Messages", "messages"),
      item("/settings", "Settings", "settings"),
    ],
  },
];

export const BARN_OWNER_NAVIGATION = [
  {
    label: "Facility",
    items: [
      item(DASHBOARD_PATHS.facility, "Dashboard", "dashboard", { end: true }),
      item(SETUP_ROUTE, "Setup", "sparkles"),
      item("/horses", "Horses", "horse"),
      item("/owners", "Owners", "users"),
      item("/riders", "Riders", "profile"),
      item("/today", "Tasks", "tasks"),
      item("/messaging", "Messages", "messages"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const STAFF_NAVIGATION = [
  {
    label: "Daily Work",
    items: [
      item(DASHBOARD_PATHS.staff, "Today", "tasks", { end: true }),
      item("/my-work", "My Tasks", "clipboard"),
      item("/today", "Horse Checks", "health"),
      item("/horses", "Horse List", "horse"),
      item("/today", "Facility Checks", "facility"),
      item("/messaging", "Messages", "messages"),
      item("/today", "Shift Notes", "documents"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const OWNER_NAVIGATION = [
  {
    label: "My Horse",
    items: [
      item(dashboardFor("owner"), "My Horse", "heart", { end: true }),
      item(dashboardFor("owner"), "Daily Care", "health"),
      item("/arena-schedule", "Barn Schedule", "calendar"),
      item(dashboardFor("owner"), "Training Notes", "training"),
      item(dashboardFor("owner"), "Health", "health"),
      item(dashboardFor("owner"), "Requests", "requests"),
      item(dashboardFor("owner"), "Billing", "billing"),
      item(dashboardFor("owner"), "Documents", "documents"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const INDIVIDUAL_OWNER_NAVIGATION = [
  {
    label: "My Horse",
    items: [
      item(dashboardFor("owner"), "My Horse", "heart", { end: true }),
      item(dashboardFor("owner"), "Daily Care", "health"),
      item(dashboardFor("owner"), "Training Notes", "training"),
      item(dashboardFor("owner"), "Health", "health"),
      item(dashboardFor("owner"), "Schedule", "calendar"),
      item(dashboardFor("owner"), "Requests", "requests"),
      item(dashboardFor("owner"), "Billing", "billing"),
      item(dashboardFor("owner"), "Documents", "documents"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const GUARDIAN_NAVIGATION = [
  {
    label: "Guardian",
    items: [
      item(dashboardFor("guardian"), "Rider Overview", "profile", { end: true }),
      item(dashboardFor("guardian"), "Schedule", "calendar"),
      item(dashboardFor("guardian"), "Progress Notes", "documents"),
      item(dashboardFor("guardian"), "Billing", "billing"),
      item(dashboardFor("guardian"), "Documents", "documents"),
      item(dashboardFor("guardian"), "Requests", "requests"),
      item(dashboardFor("guardian"), "Emergency Info", "alert"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const RIDER_NAVIGATION = [
  {
    label: "Rider",
    items: [
      item(dashboardFor("rider"), "Home", "dashboard", { end: true }),
      item(dashboardFor("rider"), "Schedule", "calendar"),
      item(dashboardFor("rider"), "Lessons", "training"),
      item(dashboardFor("rider"), "Progress Notes", "documents"),
      item(dashboardFor("rider"), "Goals", "sparkles"),
      item(dashboardFor("rider"), "Requests", "requests"),
      item(dashboardFor("rider"), "Barn Announcements", "messages"),
      item(dashboardFor("rider"), "Documents", "documents"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const DEFAULT_NAVIGATION = [
  {
    label: "Account",
    items: [
      item("/dashboard", "Dashboard", "dashboard", { end: true }),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const SERVICE_PROVIDER_NAVIGATION = [
  {
    label: "Provider",
    items: [
      item(DASHBOARD_PATHS.serviceProvider, "Dashboard", "dashboard", { end: true }),
      item(DASHBOARD_PATHS.serviceProvider, "Appointments", "calendar"),
      item(DASHBOARD_PATHS.serviceProvider, "Shared Horses", "horse"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const isIndividualOwnerNavigation = (user) => {
  const markers = [
    user?.customer_type,
    user?.account_type,
    user?.subscription_customer_type,
    user?.plan_code,
    user?.subscription_plan_code,
  ].map((v) => String(v || "").toLowerCase());

  if (markers.some((v) => ["individual_owner", "private_owner_plus"].includes(v))) {
    return true;
  }
  return !user?.barn_id && !user?.facility_id;
};

export const getRoleNavigation = (user) => {
  if (isPlatformAdmin(user)) return PLATFORM_NAVIGATION;

  const role = String(user?.role || "").toLowerCase();

  if (role === "admin") return FACILITY_ADMIN_NAVIGATION;
  if (role === "barn_owner") return BARN_OWNER_NAVIGATION;
  if (role === "barn_manager") return MANAGER_NAVIGATION;
  if (role === "trainer") return TRAINER_NAVIGATION;
  if (role === "groom" || role === "working_student") return STAFF_NAVIGATION;
  if (role === "parent") return GUARDIAN_NAVIGATION;
  if (role === "rider") return RIDER_NAVIGATION;
  if (SERVICE_PROVIDER_ROLES.includes(role)) return SERVICE_PROVIDER_NAVIGATION;
  if (role === "horse_owner") {
    return isIndividualOwnerNavigation(user) ? INDIVIDUAL_OWNER_NAVIGATION : OWNER_NAVIGATION;
  }

  return DEFAULT_NAVIGATION;
};
