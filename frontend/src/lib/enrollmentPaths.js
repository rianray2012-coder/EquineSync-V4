export const ENROLLMENT_PATHS = [
  {
    id: "individual_horse_owner",
    label: "Individual Horse Owner",
    audience: "Owners not joining through an EquineSync barn",
    role: "horse_owner",
    deferredPhase: "RF7",
    signupPath: "/signup?enrollment=individual_horse_owner&role=horse_owner",
    summary:
      "For owners whose barn is not using EquineSync, horses kept on private land, or family and informal care situations.",
    criticalData: ["Owner identity", "Horse basics", "Care location", "Emergency contact"],
    availabilityNote: "Start with individual owner tools; barn-connected features unlock when a facility relationship is confirmed.",
  },
  {
    id: "barn_facility_owner",
    label: "Barn Owner / Manager",
    audience: "Barn owners, managers, facility operators, and program leads",
    role: "barn_owner",
    deferredPhase: "RF5/RF12",
    signupPath: "/signup?enrollment=barn_facility_owner&role=barn_owner",
    summary:
      "For barns, barn managers, boarding facilities, training facilities, rehab barns, and private operations starting a workspace.",
    criticalData: ["Account lead", "Facility name", "Location", "Approximate capacity"],
    availabilityNote: "Create the workspace first, then invite your team and configure daily operations.",
  },
  {
    id: "service_provider",
    label: "Service Provider",
    audience: "Vets, farriers, body workers, haulers, and care partners",
    role: "service_provider",
    deferredPhase: "RF10",
    signupPath: "/signup?enrollment=service_provider&role=service_provider",
    summary:
      "For providers who need basic horse info, calendar visibility, appointment scheduling, and optional premium provider tools.",
    criticalData: ["Provider identity", "Service type", "Service area", "Business contact"],
    availabilityNote: "Provider accounts begin with profile review, then continue into grant-scoped horse context and visit-note tools where approved.",
  },
  {
    id: "trainer",
    label: "Trainer",
    audience: "Independent trainers and training businesses",
    role: "trainer",
    deferredPhase: "RF9",
    signupPath: "/signup?enrollment=trainer&role=trainer",
    summary:
      "For trainers who need a reviewed profile, assigned-work visibility, and a governed path toward client, horse, lesson, and program workflows.",
    criticalData: ["Trainer identity", "Specialties", "Service area", "Business contact"],
    availabilityNote: "Trainer accounts begin with profile review and trainer intake tools; expanded client, horse, lesson, and program workflows unlock as they are approved.",
  },
];

export const LIMITED_INDIVIDUAL_OWNER_TRIAL = {
  id: "limited_individual_owner_trial",
  label: "Limited Individual Owner Trial",
  audience: "Riders, guardians, and staff without an invite",
  role: "horse_owner",
  signupPath: "/signup?enrollment=limited_individual_owner_trial&role=horse_owner&trial=limited",
  summary:
    "For riders, parents/guardians, or staff who do not have an invite yet and can provide contact information for their boarding facility, trainer, or equine provider.",
  criticalData: ["Personal contact", "Horse basics", "Facility or trainer contact", "Provider relationship"],
  availabilityNote: "Limited access helps confirm the right facility connection without opening invite-only role permissions.",
  limitedAccess: true,
};

export const LEASEE_INVITE_RULE = {
  id: "leasee_invite_rule",
  summary:
    "Leasee access should be invite-only from the horse owner or the horse's assigned trainer, while the owner keeps oversight access.",
  availabilityNote: "Leasee access remains invite-only so owner oversight and facility permissions stay clear.",
};

export const ENROLLMENT_PATH_BY_ID = ENROLLMENT_PATHS.reduce((memo, path) => {
  memo[path.id] = path;
  return memo;
}, {});

export const ENROLLMENT_CONTEXT_BY_ID = {
  ...ENROLLMENT_PATH_BY_ID,
  [LIMITED_INDIVIDUAL_OWNER_TRIAL.id]: LIMITED_INDIVIDUAL_OWNER_TRIAL,
};

export const ENROLLMENT_PATH_BY_ROLE = ENROLLMENT_PATHS.reduce((memo, path) => {
  memo[path.role] = path;
  return memo;
}, {});
