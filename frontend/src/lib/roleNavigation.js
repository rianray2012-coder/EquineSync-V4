import { isPlatformAdmin } from "./permissions";

const roleHome = (profile) => `/role-home/${profile}`;

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
    items: [item("/settings", "Profile", "settings")],
  },
];

export const FACILITY_ADMIN_NAVIGATION = [
  {
    label: "Facility Admin",
    items: [
      item("/dashboard", "Dashboard", "dashboard", { end: true }),
      item("/onboarding", "Setup", "sparkles"),
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
      item("/dashboard", "Dashboard", "dashboard", { end: true }),
      item("/today", "Tasks", "tasks"),
      item("/horses", "Horses", "horse"),
      item("/staff", "Staff", "team"),
      item("/arena-schedule", "Schedule", "calendar"),
      item("/health", "Health Alerts", "health"),
      item("/owner-updates", "Owner Requests", "requests", { reviewBadge: true }),
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
      item("/dashboard", "Dashboard", "dashboard", { end: true }),
      item("/today", "Tasks", "tasks"),
      item("/horses", "Horses", "horse"),
      item("/arena-schedule", "Schedule", "calendar"),
      item("/health", "Health Alerts", "health"),
      item("/owner-updates", "Owner Requests", "requests", { reviewBadge: true }),
    ],
  },
  {
    label: "Program",
    items: [
      item("/barn-locations", "Facility", "map"),
      item("/advanced-reports", "Reports", "reports"),
      item("/messaging", "Messages", "messages"),
      item("/settings", "Settings", "settings"),
    ],
  },
];

export const BARN_OWNER_NAVIGATION = [
  {
    label: "Facility",
    items: [
      item("/dashboard", "Dashboard", "dashboard", { end: true }),
      item("/onboarding", "Setup", "sparkles"),
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
      item("/today", "Today", "tasks"),
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
      item(roleHome("owner"), "My Horse", "heart"),
      item(roleHome("owner"), "Daily Care", "health"),
      item("/arena-schedule", "Barn Schedule", "calendar"),
      item(roleHome("owner"), "Training Notes", "training"),
      item(roleHome("owner"), "Health", "health"),
      item(roleHome("owner"), "Requests", "requests"),
      item(roleHome("owner"), "Billing", "billing"),
      item(roleHome("owner"), "Documents", "documents"),
      item("/messaging", "Messages", "messages"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const INDIVIDUAL_OWNER_NAVIGATION = [
  {
    label: "My Horse",
    items: [
      item(roleHome("owner"), "My Horse", "heart"),
      item(roleHome("owner"), "Daily Care", "health"),
      item(roleHome("owner"), "Training Notes", "training"),
      item(roleHome("owner"), "Health", "health"),
      item(roleHome("owner"), "Schedule", "calendar"),
      item(roleHome("owner"), "Requests", "requests"),
      item(roleHome("owner"), "Billing", "billing"),
      item(roleHome("owner"), "Documents", "documents"),
      item("/messaging", "Messages", "messages"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const GUARDIAN_NAVIGATION = [
  {
    label: "Guardian",
    items: [
      item(roleHome("guardian"), "Rider Overview", "profile"),
      item(roleHome("guardian"), "Schedule", "calendar"),
      item(roleHome("guardian"), "Progress Notes", "documents"),
      item(roleHome("guardian"), "Billing", "billing"),
      item(roleHome("guardian"), "Documents", "documents"),
      item(roleHome("guardian"), "Requests", "requests"),
      item("/messaging", "Messages", "messages"),
      item(roleHome("guardian"), "Emergency Info", "alert"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const RIDER_NAVIGATION = [
  {
    label: "Rider",
    items: [
      item(roleHome("rider"), "Home", "dashboard"),
      item(roleHome("rider"), "Schedule", "calendar"),
      item(roleHome("rider"), "Lessons", "training"),
      item(roleHome("rider"), "Progress Notes", "documents"),
      item(roleHome("rider"), "Goals", "sparkles"),
      item(roleHome("rider"), "Requests", "requests"),
      item(roleHome("rider"), "Barn Announcements", "messages"),
      item(roleHome("rider"), "Documents", "documents"),
      item("/settings", "Profile", "settings"),
    ],
  },
];

export const DEFAULT_NAVIGATION = [
  {
    label: "Account",
    items: [
      item("/dashboard", "Dashboard", "dashboard", { end: true }),
      item("/messaging", "Messages", "messages"),
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
  if (role === "horse_owner") {
    return isIndividualOwnerNavigation(user) ? INDIVIDUAL_OWNER_NAVIGATION : OWNER_NAVIGATION;
  }

  return DEFAULT_NAVIGATION;
};
