export const ENROLLMENT_PATHS = [
  {
    id: "individual_horse_owner",
    label: "Individual Horse Owner",
    audience: "Owners not joining through an EquineSync barn",
    role: "horse_owner",
    signupPath: "/signup?enrollment=individual_horse_owner&role=horse_owner",
    summary:
      "For owners whose barn is not using EquineSync, horses kept on private land, or family and informal care situations.",
    criticalData: ["Owner identity", "Horse basics", "Care location", "Emergency contact"],
    deferredPhase: "RF7",
  },
  {
    id: "barn_facility_owner",
    label: "Barn Owner / Manager",
    audience: "Barn owners, managers, facility operators, and program leads",
    role: "barn_owner",
    signupPath: "/signup?enrollment=barn_facility_owner&role=barn_owner",
    summary:
      "For barns, barn managers, boarding facilities, training facilities, rehab barns, and private operations starting a workspace.",
    criticalData: ["Account lead", "Facility name", "Location", "Approximate capacity"],
    deferredPhase: "RF5/RF12",
  },
  {
    id: "service_provider",
    label: "Service Provider",
    audience: "Vets, farriers, body workers, haulers, and care partners",
    role: "service_provider",
    signupPath: "/signup?enrollment=service_provider&role=service_provider",
    summary:
      "For providers who need scoped client or barn access after the provider grant model is implemented.",
    criticalData: ["Provider identity", "Service type", "Service area", "Business contact"],
    deferredPhase: "RF10",
  },
  {
    id: "trainer",
    label: "Trainer",
    audience: "Independent trainers and training businesses",
    role: "trainer",
    signupPath: "/signup?enrollment=trainer&role=trainer",
    summary:
      "For trainers who need client, horse, lesson, or program workflows after account review.",
    criticalData: ["Trainer identity", "Specialties", "Service area", "Business contact"],
    deferredPhase: "RF9",
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
  deferredPhase: "RF7/RF18",
  limitedAccess: true,
};

export const LEASEE_INVITE_RULE = {
  id: "leasee_invite_rule",
  summary:
    "Leasee access should be invite-only from the horse owner or the horse's assigned trainer, while the owner keeps oversight access.",
  deferredPhase: "RF7",
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
