import React, { useEffect, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import {
  CalendarDays,
  ClipboardList,
  FileText,
  Heart,
  Cat,
  MessageSquare,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import { resolvePostLoginPath } from "../lib/roleLanding";
import { api } from "../lib/api";

const RIDER_EXPERIENCE_LEVELS = [
  ["", "Select experience"],
  ["new", "New rider"],
  ["beginner", "Beginner"],
  ["intermediate", "Intermediate"],
  ["advanced", "Advanced"],
  ["professional", "Professional"],
  ["prefer_not_to_say", "Prefer not to say"],
];

const RIDER_DISCIPLINES = [
  "Hunter/Jumper",
  "Dressage",
  "Eventing",
  "Western",
  "Trail",
  "Equitation",
  "Groundwork",
  "Not sure yet",
];

const TRAINER_PROGRAM_FOCUS = [
  ["", "Select program focus"],
  ["lessons", "Lessons"],
  ["training", "Training"],
  ["show_program", "Show program"],
  ["young_horses", "Young horses"],
  ["rehab", "Rehab"],
  ["sales", "Sales"],
  ["mixed", "Mixed"],
  ["other", "Other"],
  ["prefer_not_to_say", "Prefer not to say"],
];

const TRAINER_RIDER_LEVELS = [
  ["new", "New riders"],
  ["beginner", "Beginner"],
  ["intermediate", "Intermediate"],
  ["advanced", "Advanced"],
  ["professional", "Professional"],
  ["mixed", "Mixed levels"],
  ["prefer_not_to_say", "Prefer not to say"],
];

const MANAGER_OPERATIONS_FOCUS = [
  ["daily_tasks", "Daily tasks"],
  ["horse_care", "Horse care"],
  ["staff_coordination", "Staff coordination"],
  ["facility_maintenance", "Facility maintenance"],
  ["owner_communication", "Owner communication"],
  ["inventory", "Inventory"],
  ["scheduling", "Scheduling"],
  ["mixed", "Mixed"],
  ["other", "Other"],
  ["prefer_not_to_say", "Prefer not to say"],
];

const STAFF_EXPERIENCE_LEVELS = [
  ["", "Select experience"],
  ["new", "New to barn work"],
  ["beginner", "Beginner"],
  ["intermediate", "Intermediate"],
  ["experienced", "Experienced"],
  ["professional", "Professional"],
  ["prefer_not_to_say", "Prefer not to say"],
];

const STAFF_CARE_AREAS = [
  ["feeding", "Feeding"],
  ["water", "Water"],
  ["hay", "Hay"],
  ["hay_nets", "Hay nets"],
  ["stall_bedding", "Stall bedding"],
  ["turnout", "Turnout"],
  ["grooming", "Grooming"],
  ["blanketing", "Blanketing"],
  ["medication_support", "Medication support"],
  ["facility_checks", "Facility checks"],
  ["other", "Other"],
];

const GUARDIAN_CONTACT_PREFERENCES = [
  ["", "Select preference"],
  ["email", "Email"],
  ["sms", "Text message"],
  ["phone", "Phone call"],
  ["app", "In-app messages"],
  ["no_preference", "No preference"],
];

const MINOR_AGE_RANGES = [
  ["", "Select age range"],
  ["under_8", "Under 8"],
  ["8_12", "8-12"],
  ["13_15", "13-15"],
  ["16_17", "16-17"],
  ["prefer_not_to_say", "Prefer not to say"],
];

const OWNER_TYPES = [
  ["", "Select owner path"],
  ["facility_linked", "My horse is at a facility"],
  ["individual_owner", "I manage my own horse"],
  ["exploring_facility", "I am looking for a facility"],
  ["prefer_not_to_say", "Prefer not to say"],
];

const HORSE_COUNT_INTENTS = [
  ["", "Select horse count"],
  ["one", "1 horse"],
  ["two_to_five", "2-5 horses"],
  ["six_plus", "6+ horses"],
  ["unknown", "Not sure yet"],
];

const BARN_FACILITY_TYPES = [
  ["", "Select facility type"],
  ["boarding", "Boarding"],
  ["training", "Training"],
  ["lesson_program", "Lesson program"],
  ["private_barn", "Private barn"],
  ["rescue", "Rescue"],
  ["mixed", "Mixed"],
  ["other", "Other"],
  ["prefer_not_to_say", "Prefer not to say"],
];

const BARN_HORSE_COUNT_RANGES = [
  ["", "Select horse count"],
  ["none_yet", "None yet"],
  ["1_10", "1-10"],
  ["11_30", "11-30"],
  ["31_75", "31-75"],
  ["76_plus", "76+"],
  ["unknown", "Unknown"],
];

const BARN_STAFF_COUNT_RANGES = [
  ["", "Select staff size"],
  ["solo", "Solo"],
  ["1_3", "1-3"],
  ["4_10", "4-10"],
  ["11_plus", "11+"],
  ["unknown", "Unknown"],
];

const BARN_SETUP_TIMELINES = [
  ["", "Select timeline"],
  ["now", "Now"],
  ["30_days", "Next 30 days"],
  ["90_days", "Next 90 days"],
  ["later", "Later"],
  ["exploring", "Exploring"],
];

const BARN_SERVICES = [
  "Boarding",
  "Training",
  "Lessons",
  "Sales",
  "Rehab",
  "Retirement",
  "Shows",
  "Clinics",
];

const PROFILES = {
  rider: {
    eyebrow: "Rider Home",
    title: "Your riding day",
    subtitle: "Lessons, goals, trainer notes, and requests stay centered on your progress.",
    cards: [
      ["Next Lesson", "Trainer, horse, arena, and preparation notes.", CalendarDays],
      ["Riding Goals", "Current goals, milestones, and suggested focus.", Sparkles],
      ["Trainer Notes", "Recent lesson summary and practice focus.", MessageSquare],
    ],
    primary: { label: "Rider intake coming next" },
  },
  guardian: {
    eyebrow: "Rider Overview",
    title: "Family riding hub",
    subtitle: "Minor rider progress, schedule, documents, billing, and approvals in one place.",
    cards: [
      ["Next Lesson", "Rider, trainer, horse, time, and location.", CalendarDays],
      ["Guardian Tasks", "Documents, schedule confirmations, and approvals.", ClipboardList],
      ["Billing & Documents", "Invoices, waivers, and signed forms.", FileText],
    ],
    primary: { label: "Guardian tools coming next" },
  },
  owner: {
    eyebrow: "My Horse",
    title: "Horse-first owner portal",
    subtitle: "Daily care status, updates, requests, health, training, and documents start here.",
    cards: [
      ["Horse Status Today", "Feed, water, turnout, stall care, medications, and exceptions.", Heart],
      ["Recent Updates", "Care notes, trainer updates, and approved media.", MessageSquare],
      ["Upcoming Care", "Vet, farrier, dental, vaccines, and bodywork.", CalendarDays],
    ],
    primary: { to: "/owner-portal", label: "Open owner portal" },
  },
  trainer: {
    eyebrow: "Trainer Home",
    title: "Trainer setup intent",
    subtitle: "Capture your training focus before lessons, assignments, students, or facility workflows begin.",
    cards: [],
    primary: { label: "Trainer intake" },
  },
  manager: {
    eyebrow: "Manager Home",
    title: "Manager setup intent",
    subtitle: "Capture your operations focus before task, team, and HorseOps workflows begin.",
    cards: [],
    primary: { label: "Manager intake" },
  },
  staff: {
    eyebrow: "Staff Home",
    title: "Staff setup intent",
    subtitle: "Capture your care comfort, availability, and training needs before task or HorseOps workflows begin.",
    cards: [],
    primary: { label: "Staff intake" },
  },
  "barn-owner": {
    eyebrow: "Facility Founder",
    title: "Facility setup intent",
    subtitle: "Capture your facility profile before operational setup, memberships, billing, or staff workflows begin.",
    cards: [],
    primary: { label: "Founder intake" },
  },
};

const emptyRiderProfile = {
  preferred_name: "",
  disciplines: [],
  experience_level: "",
  goals: "",
  availability_notes: "",
  emergency_contact_name: "",
  emergency_contact_phone: "",
  consent_acknowledged: false,
};

const emptyGuardianProfile = {
  guardian_preferred_contact: "",
  minor_display_name: "",
  minor_age_range: "",
  minor_birthdate: "",
  riding_interests: [],
  experience_level: "",
  goals: "",
  availability_notes: "",
  emergency_contact_name: "",
  emergency_contact_phone: "",
  medical_allergy_notes: "",
  consent_status: "pending_formal_consent",
};

const emptyOwnerProfile = {
  preferred_name: "",
  preferred_contact: "",
  owner_type: "",
  primary_horse_name: "",
  horse_count_intent: "",
  riding_or_care_goals: "",
  facility_search_name: "",
  facility_city_state: "",
  notes: "",
};

const emptyTrainerProfile = {
  preferred_name: "",
  preferred_contact: "",
  disciplines: [],
  program_focus: "",
  rider_levels_supported: [],
  availability_notes: "",
  certification_insurance_notes: "",
  facility_connection_notes: "",
  goals: "",
  notes: "",
};

const emptyStaffProfile = {
  preferred_name: "",
  preferred_contact: "",
  availability_notes: "",
  experience_level: "",
  care_area_comfort: [],
  training_support_needs: "",
  emergency_contact_preference: "",
  notes: "",
};

const emptyManagerProfile = {
  preferred_name: "",
  preferred_contact: "",
  operations_focus: [],
  shift_availability_notes: "",
  team_coordination_notes: "",
  horse_care_oversight_notes: "",
  task_board_goals: "",
  facility_connection_notes: "",
  emergency_operations_notes: "",
  notes: "",
};

const emptyBarnOwnerProfile = {
  preferred_name: "",
  preferred_contact: "",
  facility_name: "",
  facility_city_state: "",
  facility_type: "",
  horse_count_range: "",
  staff_count_range: "",
  services_offered: [],
  setup_goals: "",
  timeline: "",
  notes: "",
};

function StaffHome({ user }) {
  const [profile, setProfile] = useState(emptyStaffProfile);
  const [completion, setCompletion] = useState({ percent: 0, missing_fields: [] });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    let alive = true;
    api
      .get("/staff-intake/profile")
      .then((r) => {
        if (!alive) return;
        setProfile({ ...emptyStaffProfile, ...r.data });
        setCompletion(r.data?.completion || { percent: 0, missing_fields: [] });
        setErr("");
      })
      .catch((e) => {
        if (!alive) return;
        setErr(e?.response?.data?.detail || "Could not load staff intake.");
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => { alive = false; };
  }, []);

  const setField = (field, value) => {
    setProfile((p) => ({ ...p, [field]: value }));
  };

  const toggleCareArea = (value) => {
    setProfile((p) => {
      const current = p.care_area_comfort || [];
      const care_area_comfort = current.includes(value)
        ? current.filter((item) => item !== value)
        : [...current, value];
      return { ...p, care_area_comfort };
    });
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        preferred_name: profile.preferred_name || null,
        preferred_contact: profile.preferred_contact || null,
        availability_notes: profile.availability_notes || null,
        experience_level: profile.experience_level || null,
        care_area_comfort: profile.care_area_comfort || [],
        training_support_needs: profile.training_support_needs || null,
        emergency_contact_preference: profile.emergency_contact_preference || null,
        notes: profile.notes || null,
      };
      const { data } = await api.patch("/staff-intake/profile", payload);
      setProfile({ ...emptyStaffProfile, ...data });
      setCompletion(data?.completion || { percent: 0, missing_fields: [] });
      toast.success("Staff intake saved");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not save staff intake");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="role-home-staff">
      <header className="mb-8">
        <div className="label-eyebrow mb-3">Staff Home</div>
        <h1 className="font-display text-4xl md:text-5xl text-equine-ivory">
          Staff setup intent{profile.preferred_name ? ` for ${profile.preferred_name}` : ""}
        </h1>
        <p className="mt-3 max-w-2xl text-equine-platinum/70 text-[15px] leading-relaxed">
          Share your availability, comfort areas, and support needs before task assignment, task completion, HorseOps records, or schedules are changed.
        </p>
      </header>

      <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)] gap-5">
        <section className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid="staff-intake-shell">
          <div className="flex items-start justify-between gap-4 mb-5">
            <div>
              <div className="label-eyebrow">Profile completion</div>
              <h2 className="font-display text-3xl text-equine-ivory mt-1">Staff intake</h2>
            </div>
            <div className="w-20 h-20 rounded-2xl bg-equine-navy/60 border border-white/10 flex items-center justify-center">
              <span className="font-display text-3xl text-equine-brassLight">{completion.percent || 0}%</span>
            </div>
          </div>

          {loading ? (
            <div className="text-equine-platinum/60 text-[13px] py-10">Loading staff intake...</div>
          ) : err ? (
            <div className="rounded-xl border border-equine-clay/40 bg-equine-clay/10 p-4 text-equine-clay text-[13px]">{err}</div>
          ) : (
            <div className="space-y-5">
              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Preferred name</span>
                  <input
                    value={profile.preferred_name || ""}
                    onChange={(e) => setField("preferred_name", e.target.value)}
                    data-testid="staff-preferred-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="What should the barn call you?"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Preferred contact</span>
                  <select
                    value={profile.preferred_contact || ""}
                    onChange={(e) => setField("preferred_contact", e.target.value)}
                    data-testid="staff-preferred-contact"
                    className="mt-2 input-luxe w-full"
                  >
                    {GUARDIAN_CONTACT_PREFERENCES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
              </div>

              <label className="block">
                <span className="label-eyebrow">Experience level</span>
                <select
                  value={profile.experience_level || ""}
                  onChange={(e) => setField("experience_level", e.target.value)}
                  data-testid="staff-experience-level"
                  className="mt-2 input-luxe w-full"
                >
                  {STAFF_EXPERIENCE_LEVELS.map(([value, label]) => (
                    <option key={value} value={value}>{label}</option>
                  ))}
                </select>
              </label>

              <div>
                <span className="label-eyebrow">Care-area comfort</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {STAFF_CARE_AREAS.map(([value, label]) => {
                    const active = (profile.care_area_comfort || []).includes(value);
                    return (
                      <button
                        key={value}
                        type="button"
                        onClick={() => toggleCareArea(value)}
                        data-testid={`staff-care-area-${value}`}
                        className={`px-3 py-2 rounded-xl border text-[12.5px] transition ${
                          active
                            ? "bg-equine-brassLight text-equine-navy border-equine-brassLight"
                            : "bg-white/[0.03] text-equine-platinum/75 border-white/10 hover:border-equine-brassLight/50"
                        }`}
                      >
                        {label}
                      </button>
                    );
                  })}
                </div>
              </div>

              <label className="block">
                <span className="label-eyebrow">Availability notes</span>
                <textarea
                  value={profile.availability_notes || ""}
                  onChange={(e) => setField("availability_notes", e.target.value)}
                  data-testid="staff-availability-notes"
                  className="mt-2 input-luxe w-full min-h-[96px]"
                  placeholder="Days, shifts, school constraints, or coverage windows."
                />
              </label>

              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Training or support needs</span>
                  <textarea
                    value={profile.training_support_needs || ""}
                    onChange={(e) => setField("training_support_needs", e.target.value)}
                    data-testid="staff-training-support-needs"
                    className="mt-2 input-luxe w-full min-h-[90px]"
                    placeholder="Where would extra guidance help?"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Emergency contact preference</span>
                  <textarea
                    value={profile.emergency_contact_preference || ""}
                    onChange={(e) => setField("emergency_contact_preference", e.target.value)}
                    data-testid="staff-emergency-contact-preference"
                    className="mt-2 input-luxe w-full min-h-[90px]"
                    placeholder="Optional contact preference only. This does not create emergency workflows."
                  />
                </label>
              </div>

              <label className="block">
                <span className="label-eyebrow">Notes</span>
                <textarea
                  value={profile.notes || ""}
                  onChange={(e) => setField("notes", e.target.value)}
                  data-testid="staff-notes"
                  className="mt-2 input-luxe w-full min-h-[80px]"
                  placeholder="Optional context. This does not create tasks, schedules, staff permissions, task completions, or HorseOps records."
                />
              </label>

              <button
                type="button"
                onClick={save}
                disabled={saving}
                data-testid="staff-intake-save"
                className="btn-primary inline-flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                {saving ? "Saving..." : "Save staff intake"}
              </button>
            </div>
          )}
        </section>

        <aside className="space-y-5">
          {[
            ["Today's Work", "Task assignment and completion stay in the approved task workflow.", ClipboardList],
            ["Assigned Horses", "Horse access is not granted from this page.", Heart],
            ["Care Checks", "HorseOps care checks are not created until the approved care workflow is used.", ShieldCheck],
            ["Schedule", "Shift or lesson scheduling is not changed by this intake.", CalendarDays],
            ["Team Notes", "Team communication remains in the approved message workflow.", MessageSquare],
            ["Safety / Training", "Training and safety needs captured here are setup context only.", FileText],
          ].map(([title, body, Icon]) => (
            <section key={title} className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid={`staff-panel-${title.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
              <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
              </div>
              <h2 className="font-display text-2xl text-equine-ivory">{title}</h2>
              <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">{body}</p>
            </section>
          ))}
        </aside>
      </div>
    </div>
  );
}

function ManagerHome({ user }) {
  const [profile, setProfile] = useState(emptyManagerProfile);
  const [completion, setCompletion] = useState({ percent: 0, missing_fields: [] });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    let alive = true;
    api
      .get("/manager-intake/profile")
      .then((r) => {
        if (!alive) return;
        setProfile({ ...emptyManagerProfile, ...r.data });
        setCompletion(r.data?.completion || { percent: 0, missing_fields: [] });
        setErr("");
      })
      .catch((e) => {
        if (!alive) return;
        setErr(e?.response?.data?.detail || "Could not load manager intake.");
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => { alive = false; };
  }, []);

  const setField = (field, value) => {
    setProfile((p) => ({ ...p, [field]: value }));
  };

  const toggleFocus = (value) => {
    setProfile((p) => {
      const current = p.operations_focus || [];
      const operations_focus = current.includes(value)
        ? current.filter((item) => item !== value)
        : [...current, value];
      return { ...p, operations_focus };
    });
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        preferred_name: profile.preferred_name || null,
        preferred_contact: profile.preferred_contact || null,
        operations_focus: profile.operations_focus || [],
        shift_availability_notes: profile.shift_availability_notes || null,
        team_coordination_notes: profile.team_coordination_notes || null,
        horse_care_oversight_notes: profile.horse_care_oversight_notes || null,
        task_board_goals: profile.task_board_goals || null,
        facility_connection_notes: profile.facility_connection_notes || null,
        emergency_operations_notes: profile.emergency_operations_notes || null,
        notes: profile.notes || null,
      };
      const { data } = await api.patch("/manager-intake/profile", payload);
      setProfile({ ...emptyManagerProfile, ...data });
      setCompletion(data?.completion || { percent: 0, missing_fields: [] });
      toast.success("Manager intake saved");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not save manager intake");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="role-home-manager">
      <header className="mb-8">
        <div className="label-eyebrow mb-3">Manager Home</div>
        <h1 className="font-display text-4xl md:text-5xl text-equine-ivory">
          Manager setup intent{profile.preferred_name ? ` for ${profile.preferred_name}` : ""}
        </h1>
        <p className="mt-3 max-w-2xl text-equine-platinum/70 text-[15px] leading-relaxed">
          Share your operations focus before task ownership, staff coordination, HorseOps records, or facility setup changes begin.
        </p>
      </header>

      <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)] gap-5">
        <section className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid="manager-intake-shell">
          <div className="flex items-start justify-between gap-4 mb-5">
            <div>
              <div className="label-eyebrow">Profile completion</div>
              <h2 className="font-display text-3xl text-equine-ivory mt-1">Manager intake</h2>
            </div>
            <div className="w-20 h-20 rounded-2xl bg-equine-navy/60 border border-white/10 flex items-center justify-center">
              <span className="font-display text-3xl text-equine-brassLight">{completion.percent || 0}%</span>
            </div>
          </div>

          {loading ? (
            <div className="text-equine-platinum/60 text-[13px] py-10">Loading manager intake...</div>
          ) : err ? (
            <div className="rounded-xl border border-equine-clay/40 bg-equine-clay/10 p-4 text-equine-clay text-[13px]">{err}</div>
          ) : (
            <div className="space-y-5">
              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Preferred name</span>
                  <input
                    value={profile.preferred_name || ""}
                    onChange={(e) => setField("preferred_name", e.target.value)}
                    data-testid="manager-preferred-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="What should the team call you?"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Preferred contact</span>
                  <select
                    value={profile.preferred_contact || ""}
                    onChange={(e) => setField("preferred_contact", e.target.value)}
                    data-testid="manager-preferred-contact"
                    className="mt-2 input-luxe w-full"
                  >
                    {GUARDIAN_CONTACT_PREFERENCES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
              </div>

              <div>
                <span className="label-eyebrow">Operations focus</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {MANAGER_OPERATIONS_FOCUS.map(([value, label]) => {
                    const active = (profile.operations_focus || []).includes(value);
                    return (
                      <button
                        key={value}
                        type="button"
                        onClick={() => toggleFocus(value)}
                        data-testid={`manager-focus-${value}`}
                        className={`px-3 py-2 rounded-xl border text-[12.5px] transition ${
                          active
                            ? "bg-equine-brassLight text-equine-navy border-equine-brassLight"
                            : "bg-white/[0.03] text-equine-platinum/75 border-white/10 hover:border-equine-brassLight/50"
                        }`}
                      >
                        {label}
                      </button>
                    );
                  })}
                </div>
              </div>

              <label className="block">
                <span className="label-eyebrow">Task board goals</span>
                <textarea
                  value={profile.task_board_goals || ""}
                  onChange={(e) => setField("task_board_goals", e.target.value)}
                  data-testid="manager-task-board-goals"
                  className="mt-2 input-luxe w-full min-h-[96px]"
                  placeholder="What should the task board help organize first?"
                />
              </label>

              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Team coordination notes</span>
                  <textarea
                    value={profile.team_coordination_notes || ""}
                    onChange={(e) => setField("team_coordination_notes", e.target.value)}
                    data-testid="manager-team-coordination-notes"
                    className="mt-2 input-luxe w-full min-h-[90px]"
                    placeholder="Staff handoffs, shift patterns, or communication needs."
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Horse care oversight</span>
                  <textarea
                    value={profile.horse_care_oversight_notes || ""}
                    onChange={(e) => setField("horse_care_oversight_notes", e.target.value)}
                    data-testid="manager-horse-care-oversight-notes"
                    className="mt-2 input-luxe w-full min-h-[90px]"
                    placeholder="Care areas you expect to oversee. This does not create HorseOps records."
                  />
                </label>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Shift availability notes</span>
                  <textarea
                    value={profile.shift_availability_notes || ""}
                    onChange={(e) => setField("shift_availability_notes", e.target.value)}
                    data-testid="manager-shift-availability-notes"
                    className="mt-2 input-luxe w-full min-h-[90px]"
                    placeholder="Usual coverage windows or constraints."
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Facility connection</span>
                  <textarea
                    value={profile.facility_connection_notes || ""}
                    onChange={(e) => setField("facility_connection_notes", e.target.value)}
                    data-testid="manager-facility-connection-notes"
                    className="mt-2 input-luxe w-full min-h-[90px]"
                    placeholder="Barn or team context, if known."
                  />
                </label>
              </div>

              <label className="block">
                <span className="label-eyebrow">Emergency operations notes</span>
                <textarea
                  value={profile.emergency_operations_notes || ""}
                  onChange={(e) => setField("emergency_operations_notes", e.target.value)}
                  data-testid="manager-emergency-operations-notes"
                  className="mt-2 input-luxe w-full min-h-[80px]"
                  placeholder="Optional planning context. This does not create policies or assignments."
                />
              </label>

              <label className="block">
                <span className="label-eyebrow">Notes</span>
                <textarea
                  value={profile.notes || ""}
                  onChange={(e) => setField("notes", e.target.value)}
                  data-testid="manager-notes"
                  className="mt-2 input-luxe w-full min-h-[80px]"
                  placeholder="Optional context. This does not create tasks, staff invites, permissions, facility setup, or HorseOps records."
                />
              </label>

              <button
                type="button"
                onClick={save}
                disabled={saving}
                data-testid="manager-intake-save"
                className="btn-primary inline-flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                {saving ? "Saving..." : "Save manager intake"}
              </button>
            </div>
          )}
        </section>

        <aside className="space-y-5">
          {[
            ["Today's Work", "Task creation and assignment stay in the approved task workflow.", ClipboardList],
            ["Team Coordination", "Staff invites, roles, and permissions are not changed from this page.", ShieldCheck],
            ["Horse Care Oversight", "HorseOps records are not created until the horse workflow is used.", Heart],
            ["Facility Tasks", "Facility setup and configuration remain separate from this intake.", CalendarDays],
            ["Owner Requests", "Owner communication and request workflows stay in their approved surfaces.", MessageSquare],
            ["Messages", "Use Messages or support channels for setup questions.", FileText],
          ].map(([title, body, Icon]) => (
            <section key={title} className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid={`manager-panel-${title.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
              <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
              </div>
              <h2 className="font-display text-2xl text-equine-ivory">{title}</h2>
              <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">{body}</p>
            </section>
          ))}
        </aside>
      </div>
    </div>
  );
}

function TrainerHome({ user }) {
  const [profile, setProfile] = useState(emptyTrainerProfile);
  const [completion, setCompletion] = useState({ percent: 0, missing_fields: [] });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    let alive = true;
    api
      .get("/trainer-intake/profile")
      .then((r) => {
        if (!alive) return;
        setProfile({ ...emptyTrainerProfile, ...r.data });
        setCompletion(r.data?.completion || { percent: 0, missing_fields: [] });
        setErr("");
      })
      .catch((e) => {
        if (!alive) return;
        setErr(e?.response?.data?.detail || "Could not load trainer intake.");
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => { alive = false; };
  }, []);

  const setField = (field, value) => {
    setProfile((p) => ({ ...p, [field]: value }));
  };

  const toggleListValue = (field, name) => {
    setProfile((p) => {
      const current = p[field] || [];
      const next = current.includes(name)
        ? current.filter((item) => item !== name)
        : [...current, name];
      return { ...p, [field]: next };
    });
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        preferred_name: profile.preferred_name || null,
        preferred_contact: profile.preferred_contact || null,
        disciplines: profile.disciplines || [],
        program_focus: profile.program_focus || null,
        rider_levels_supported: profile.rider_levels_supported || [],
        availability_notes: profile.availability_notes || null,
        certification_insurance_notes: profile.certification_insurance_notes || null,
        facility_connection_notes: profile.facility_connection_notes || null,
        goals: profile.goals || null,
        notes: profile.notes || null,
      };
      const { data } = await api.patch("/trainer-intake/profile", payload);
      setProfile({ ...emptyTrainerProfile, ...data });
      setCompletion(data?.completion || { percent: 0, missing_fields: [] });
      toast.success("Trainer intake saved");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not save trainer intake");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="role-home-trainer">
      <header className="mb-8">
        <div className="label-eyebrow mb-3">Trainer Home</div>
        <h1 className="font-display text-4xl md:text-5xl text-equine-ivory">
          Trainer setup intent{profile.preferred_name ? ` for ${profile.preferred_name}` : ""}
        </h1>
        <p className="mt-3 max-w-2xl text-equine-platinum/70 text-[15px] leading-relaxed">
          Share your training focus and availability before the barn connects lessons, students, horses, or facility assignments.
        </p>
      </header>

      <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)] gap-5">
        <section className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid="trainer-intake-shell">
          <div className="flex items-start justify-between gap-4 mb-5">
            <div>
              <div className="label-eyebrow">Profile completion</div>
              <h2 className="font-display text-3xl text-equine-ivory mt-1">Trainer intake</h2>
            </div>
            <div className="w-20 h-20 rounded-2xl bg-equine-navy/60 border border-white/10 flex items-center justify-center">
              <span className="font-display text-3xl text-equine-brassLight">{completion.percent || 0}%</span>
            </div>
          </div>

          {loading ? (
            <div className="text-equine-platinum/60 text-[13px] py-10">Loading trainer intake...</div>
          ) : err ? (
            <div className="rounded-xl border border-equine-clay/40 bg-equine-clay/10 p-4 text-equine-clay text-[13px]">{err}</div>
          ) : (
            <div className="space-y-5">
              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Preferred name</span>
                  <input
                    value={profile.preferred_name || ""}
                    onChange={(e) => setField("preferred_name", e.target.value)}
                    data-testid="trainer-preferred-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="What should riders call you?"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Preferred contact</span>
                  <select
                    value={profile.preferred_contact || ""}
                    onChange={(e) => setField("preferred_contact", e.target.value)}
                    data-testid="trainer-preferred-contact"
                    className="mt-2 input-luxe w-full"
                  >
                    {GUARDIAN_CONTACT_PREFERENCES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
              </div>

              <label className="block">
                <span className="label-eyebrow">Program focus</span>
                <select
                  value={profile.program_focus || ""}
                  onChange={(e) => setField("program_focus", e.target.value)}
                  data-testid="trainer-program-focus"
                  className="mt-2 input-luxe w-full"
                >
                  {TRAINER_PROGRAM_FOCUS.map(([value, label]) => (
                    <option key={value} value={value}>{label}</option>
                  ))}
                </select>
              </label>

              <div>
                <span className="label-eyebrow">Disciplines</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {RIDER_DISCIPLINES.filter((name) => name !== "Not sure yet").map((name) => {
                    const active = (profile.disciplines || []).includes(name);
                    return (
                      <button
                        key={name}
                        type="button"
                        onClick={() => toggleListValue("disciplines", name)}
                        data-testid={`trainer-discipline-${name.toLowerCase().replace(/[^a-z]+/g, "-")}`}
                        className={`px-3 py-2 rounded-xl border text-[12.5px] transition ${
                          active
                            ? "bg-equine-brassLight text-equine-navy border-equine-brassLight"
                            : "bg-white/[0.03] text-equine-platinum/75 border-white/10 hover:border-equine-brassLight/50"
                        }`}
                      >
                        {name}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div>
                <span className="label-eyebrow">Rider levels supported</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {TRAINER_RIDER_LEVELS.map(([value, label]) => {
                    const active = (profile.rider_levels_supported || []).includes(value);
                    return (
                      <button
                        key={value}
                        type="button"
                        onClick={() => toggleListValue("rider_levels_supported", value)}
                        data-testid={`trainer-rider-level-${value}`}
                        className={`px-3 py-2 rounded-xl border text-[12.5px] transition ${
                          active
                            ? "bg-equine-brassLight text-equine-navy border-equine-brassLight"
                            : "bg-white/[0.03] text-equine-platinum/75 border-white/10 hover:border-equine-brassLight/50"
                        }`}
                      >
                        {label}
                      </button>
                    );
                  })}
                </div>
              </div>

              <label className="block">
                <span className="label-eyebrow">Goals</span>
                <textarea
                  value={profile.goals || ""}
                  onChange={(e) => setField("goals", e.target.value)}
                  data-testid="trainer-goals"
                  className="mt-2 input-luxe w-full min-h-[96px]"
                  placeholder="What should Equine Sync help your program organize first?"
                />
              </label>

              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Availability notes</span>
                  <textarea
                    value={profile.availability_notes || ""}
                    onChange={(e) => setField("availability_notes", e.target.value)}
                    data-testid="trainer-availability-notes"
                    className="mt-2 input-luxe w-full min-h-[90px]"
                    placeholder="Days, lesson blocks, travel days, or constraints."
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Facility connection</span>
                  <textarea
                    value={profile.facility_connection_notes || ""}
                    onChange={(e) => setField("facility_connection_notes", e.target.value)}
                    data-testid="trainer-facility-connection-notes"
                    className="mt-2 input-luxe w-full min-h-[90px]"
                    placeholder="Barn or program context, if known."
                  />
                </label>
              </div>

              <label className="block">
                <span className="label-eyebrow">Certification or insurance notes</span>
                <textarea
                  value={profile.certification_insurance_notes || ""}
                  onChange={(e) => setField("certification_insurance_notes", e.target.value)}
                  data-testid="trainer-certification-insurance-notes"
                  className="mt-2 input-luxe w-full min-h-[80px]"
                  placeholder="Optional context only. This does not upload documents or verify credentials."
                />
              </label>

              <label className="block">
                <span className="label-eyebrow">Notes</span>
                <textarea
                  value={profile.notes || ""}
                  onChange={(e) => setField("notes", e.target.value)}
                  data-testid="trainer-notes"
                  className="mt-2 input-luxe w-full min-h-[80px]"
                  placeholder="Optional context. This does not create lessons, students, or horse assignments."
                />
              </label>

              <button
                type="button"
                onClick={save}
                disabled={saving}
                data-testid="trainer-intake-save"
                className="btn-primary inline-flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                {saving ? "Saving..." : "Save trainer intake"}
              </button>
            </div>
          )}
        </section>

        <aside className="space-y-5">
          {[
            ["Schedule", "Lesson blocks and availability remain separate from this intake.", CalendarDays],
            ["Assigned Horses", "Horse assignments are not created from this page.", Heart],
            ["Lesson Students", "Student enrollment stays in the approved program workflow.", Cat],
            ["Training Notes", "Training records are not created until a horse or program is connected.", ClipboardList],
            ["Documents", "Credentials, waivers, and signature envelopes stay in approved document workflows.", FileText],
            ["Messages", "Use Messages or support channels for setup questions.", MessageSquare],
          ].map(([title, body, Icon]) => (
            <section key={title} className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid={`trainer-panel-${title.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
              <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
              </div>
              <h2 className="font-display text-2xl text-equine-ivory">{title}</h2>
              <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">{body}</p>
            </section>
          ))}
        </aside>
      </div>
    </div>
  );
}

function BarnOwnerHome({ user }) {
  const [profile, setProfile] = useState(emptyBarnOwnerProfile);
  const [completion, setCompletion] = useState({ percent: 0, missing_fields: [] });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    let alive = true;
    api
      .get("/barn-owner-intake/profile")
      .then((r) => {
        if (!alive) return;
        setProfile({ ...emptyBarnOwnerProfile, ...r.data });
        setCompletion(r.data?.completion || { percent: 0, missing_fields: [] });
        setErr("");
      })
      .catch((e) => {
        if (!alive) return;
        setErr(e?.response?.data?.detail || "Could not load facility founder intake.");
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => { alive = false; };
  }, []);

  const setField = (field, value) => {
    setProfile((p) => ({ ...p, [field]: value }));
  };

  const toggleService = (name) => {
    setProfile((p) => {
      const current = p.services_offered || [];
      const services_offered = current.includes(name)
        ? current.filter((service) => service !== name)
        : [...current, name];
      return { ...p, services_offered };
    });
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        preferred_name: profile.preferred_name || null,
        preferred_contact: profile.preferred_contact || null,
        facility_name: profile.facility_name || null,
        facility_city_state: profile.facility_city_state || null,
        facility_type: profile.facility_type || null,
        horse_count_range: profile.horse_count_range || null,
        staff_count_range: profile.staff_count_range || null,
        services_offered: profile.services_offered || [],
        setup_goals: profile.setup_goals || null,
        timeline: profile.timeline || null,
        notes: profile.notes || null,
      };
      const { data } = await api.patch("/barn-owner-intake/profile", payload);
      setProfile({ ...emptyBarnOwnerProfile, ...data });
      setCompletion(data?.completion || { percent: 0, missing_fields: [] });
      toast.success("Facility founder intake saved");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not save facility founder intake");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="role-home-barn-owner">
      <header className="mb-8">
        <div className="label-eyebrow mb-3">Facility Founder</div>
        <h1 className="font-display text-4xl md:text-5xl text-equine-ivory">
          Facility setup intent{profile.facility_name ? ` for ${profile.facility_name}` : ""}
        </h1>
        <p className="mt-3 max-w-2xl text-equine-platinum/70 text-[15px] leading-relaxed">
          Share how your barn operates before the formal setup flow begins. This page does not create a facility, invite staff, add horses, start billing, or change memberships.
        </p>
      </header>

      <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)] gap-5">
        <section className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid="barn-owner-intake-shell">
          <div className="flex items-start justify-between gap-4 mb-5">
            <div>
              <div className="label-eyebrow">Profile completion</div>
              <h2 className="font-display text-3xl text-equine-ivory mt-1">Founder intake</h2>
            </div>
            <div className="w-20 h-20 rounded-2xl bg-equine-navy/60 border border-white/10 flex items-center justify-center">
              <span className="font-display text-3xl text-equine-brassLight">{completion.percent || 0}%</span>
            </div>
          </div>

          {loading ? (
            <div className="text-equine-platinum/60 text-[13px] py-10">Loading facility founder intake...</div>
          ) : err ? (
            <div className="rounded-xl border border-equine-clay/40 bg-equine-clay/10 p-4 text-equine-clay text-[13px]">{err}</div>
          ) : (
            <div className="space-y-5">
              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Preferred name</span>
                  <input
                    value={profile.preferred_name || ""}
                    onChange={(e) => setField("preferred_name", e.target.value)}
                    data-testid="barn-owner-preferred-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="What should Equine Sync call you?"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Preferred contact</span>
                  <select
                    value={profile.preferred_contact || ""}
                    onChange={(e) => setField("preferred_contact", e.target.value)}
                    data-testid="barn-owner-preferred-contact"
                    className="mt-2 input-luxe w-full"
                  >
                    {GUARDIAN_CONTACT_PREFERENCES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Facility name</span>
                  <input
                    value={profile.facility_name || ""}
                    onChange={(e) => setField("facility_name", e.target.value)}
                    data-testid="barn-owner-facility-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="Barn, stable, or program name"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Facility location</span>
                  <input
                    value={profile.facility_city_state || ""}
                    onChange={(e) => setField("facility_city_state", e.target.value)}
                    data-testid="barn-owner-facility-city-state"
                    className="mt-2 input-luxe w-full"
                    placeholder="City, state"
                  />
                </label>
              </div>

              <div className="grid md:grid-cols-3 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Facility type</span>
                  <select
                    value={profile.facility_type || ""}
                    onChange={(e) => setField("facility_type", e.target.value)}
                    data-testid="barn-owner-facility-type"
                    className="mt-2 input-luxe w-full"
                  >
                    {BARN_FACILITY_TYPES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
                <label className="block">
                  <span className="label-eyebrow">Horse count</span>
                  <select
                    value={profile.horse_count_range || ""}
                    onChange={(e) => setField("horse_count_range", e.target.value)}
                    data-testid="barn-owner-horse-count-range"
                    className="mt-2 input-luxe w-full"
                  >
                    {BARN_HORSE_COUNT_RANGES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
                <label className="block">
                  <span className="label-eyebrow">Staff size</span>
                  <select
                    value={profile.staff_count_range || ""}
                    onChange={(e) => setField("staff_count_range", e.target.value)}
                    data-testid="barn-owner-staff-count-range"
                    className="mt-2 input-luxe w-full"
                  >
                    {BARN_STAFF_COUNT_RANGES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
              </div>

              <label className="block">
                <span className="label-eyebrow">Setup timeline</span>
                <select
                  value={profile.timeline || ""}
                  onChange={(e) => setField("timeline", e.target.value)}
                  data-testid="barn-owner-timeline"
                  className="mt-2 input-luxe w-full"
                >
                  {BARN_SETUP_TIMELINES.map(([value, label]) => (
                    <option key={value} value={value}>{label}</option>
                  ))}
                </select>
              </label>

              <div>
                <span className="label-eyebrow">Services offered</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {BARN_SERVICES.map((name) => {
                    const active = (profile.services_offered || []).includes(name);
                    return (
                      <button
                        key={name}
                        type="button"
                        onClick={() => toggleService(name)}
                        data-testid={`barn-owner-service-${name.toLowerCase().replace(/[^a-z]+/g, "-")}`}
                        className={`px-3 py-2 rounded-xl border text-[12.5px] transition ${
                          active
                            ? "bg-equine-brassLight text-equine-navy border-equine-brassLight"
                            : "bg-white/[0.03] text-equine-platinum/75 border-white/10 hover:border-equine-brassLight/50"
                        }`}
                      >
                        {name}
                      </button>
                    );
                  })}
                </div>
              </div>

              <label className="block">
                <span className="label-eyebrow">Setup goals</span>
                <textarea
                  value={profile.setup_goals || ""}
                  onChange={(e) => setField("setup_goals", e.target.value)}
                  data-testid="barn-owner-setup-goals"
                  className="mt-2 input-luxe w-full min-h-[96px]"
                  placeholder="What do you want Equine Sync to help organize first?"
                />
              </label>

              <label className="block">
                <span className="label-eyebrow">Notes</span>
                <textarea
                  value={profile.notes || ""}
                  onChange={(e) => setField("notes", e.target.value)}
                  data-testid="barn-owner-notes"
                  className="mt-2 input-luxe w-full min-h-[80px]"
                  placeholder="Optional context. This remains intake-only and does not create facility records."
                />
              </label>

              <button
                type="button"
                onClick={save}
                disabled={saving}
                data-testid="barn-owner-intake-save"
                className="btn-primary inline-flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                {saving ? "Saving..." : "Save founder intake"}
              </button>
            </div>
          )}
        </section>

        <aside className="space-y-5">
          {[
            ["Facility Setup", "Formal setup remains separate. This intake only captures founder intent.", ShieldCheck],
            ["Staff & Roles", "Staff invites and role assignments are not created from this page.", ClipboardList],
            ["Horses", "Horse records are not created here; this page only records expected facility scale.", Heart],
            ["Documents", "Policies and signature envelopes stay in the approved document workflows.", FileText],
            ["Support", "Use Messages or support channels for founder setup questions.", MessageSquare],
          ].map(([title, body, Icon]) => (
            <section key={title} className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid={`barn-owner-panel-${title.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
              <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
              </div>
              <h2 className="font-display text-2xl text-equine-ivory">{title}</h2>
              <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">{body}</p>
            </section>
          ))}
        </aside>
      </div>
    </div>
  );
}

function OwnerHome({ user }) {
  const [profile, setProfile] = useState(emptyOwnerProfile);
  const [completion, setCompletion] = useState({ percent: 0, missing_fields: [] });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  const facilityLinked = Boolean(user?.barn_id || user?.facility_id);

  useEffect(() => {
    let alive = true;
    api
      .get("/owner-intake/profile")
      .then((r) => {
        if (!alive) return;
        setProfile({ ...emptyOwnerProfile, ...r.data });
        setCompletion(r.data?.completion || { percent: 0, missing_fields: [] });
        setErr("");
      })
      .catch((e) => {
        if (!alive) return;
        setErr(e?.response?.data?.detail || "Could not load owner intake.");
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => { alive = false; };
  }, []);

  const setField = (field, value) => {
    setProfile((p) => ({ ...p, [field]: value }));
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        preferred_name: profile.preferred_name || null,
        preferred_contact: profile.preferred_contact || null,
        owner_type: profile.owner_type || null,
        primary_horse_name: profile.primary_horse_name || null,
        horse_count_intent: profile.horse_count_intent || null,
        riding_or_care_goals: profile.riding_or_care_goals || null,
        facility_search_name: profile.facility_search_name || null,
        facility_city_state: profile.facility_city_state || null,
        notes: profile.notes || null,
      };
      const { data } = await api.patch("/owner-intake/profile", payload);
      setProfile({ ...emptyOwnerProfile, ...data });
      setCompletion(data?.completion || { percent: 0, missing_fields: [] });
      toast.success("Owner intake saved");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not save owner intake");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="role-home-owner">
      <header className="mb-8">
        <div className="label-eyebrow mb-3">Owner Home</div>
        <h1 className="font-display text-4xl md:text-5xl text-equine-ivory">
          Horse owner setup{profile.primary_horse_name ? ` for ${profile.primary_horse_name}` : ""}
        </h1>
        <p className="mt-3 max-w-2xl text-equine-platinum/70 text-[15px] leading-relaxed">
          Start with your horse, your care goals, and your facility connection. Billing, memberships, and care visibility stay in their approved workflows.
        </p>
      </header>

      <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)] gap-5">
        <section className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid="owner-intake-shell">
          <div className="flex items-start justify-between gap-4 mb-5">
            <div>
              <div className="label-eyebrow">Profile completion</div>
              <h2 className="font-display text-3xl text-equine-ivory mt-1">Owner intake</h2>
            </div>
            <div className="w-20 h-20 rounded-2xl bg-equine-navy/60 border border-white/10 flex items-center justify-center">
              <span className="font-display text-3xl text-equine-brassLight">{completion.percent || 0}%</span>
            </div>
          </div>

          {loading ? (
            <div className="text-equine-platinum/60 text-[13px] py-10">Loading owner intake...</div>
          ) : err ? (
            <div className="rounded-xl border border-equine-clay/40 bg-equine-clay/10 p-4 text-equine-clay text-[13px]">{err}</div>
          ) : (
            <div className="space-y-5">
              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Preferred name</span>
                  <input
                    value={profile.preferred_name || ""}
                    onChange={(e) => setField("preferred_name", e.target.value)}
                    data-testid="owner-preferred-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="What should your barn call you?"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Preferred contact</span>
                  <select
                    value={profile.preferred_contact || ""}
                    onChange={(e) => setField("preferred_contact", e.target.value)}
                    data-testid="owner-preferred-contact"
                    className="mt-2 input-luxe w-full"
                  >
                    {GUARDIAN_CONTACT_PREFERENCES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
              </div>

              <div className="grid md:grid-cols-3 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Owner path</span>
                  <select
                    value={profile.owner_type || ""}
                    onChange={(e) => setField("owner_type", e.target.value)}
                    data-testid="owner-type"
                    className="mt-2 input-luxe w-full"
                  >
                    {OWNER_TYPES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
                <label className="block">
                  <span className="label-eyebrow">Horse count</span>
                  <select
                    value={profile.horse_count_intent || ""}
                    onChange={(e) => setField("horse_count_intent", e.target.value)}
                    data-testid="owner-horse-count-intent"
                    className="mt-2 input-luxe w-full"
                  >
                    {HORSE_COUNT_INTENTS.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
                <label className="block">
                  <span className="label-eyebrow">Primary horse</span>
                  <input
                    value={profile.primary_horse_name || ""}
                    onChange={(e) => setField("primary_horse_name", e.target.value)}
                    data-testid="owner-primary-horse-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="Horse name"
                  />
                </label>
              </div>

              <label className="block">
                <span className="label-eyebrow">Riding or care goals</span>
                <textarea
                  value={profile.riding_or_care_goals || ""}
                  onChange={(e) => setField("riding_or_care_goals", e.target.value)}
                  data-testid="owner-care-goals"
                  className="mt-2 input-luxe w-full min-h-[90px]"
                  placeholder="What would make Equine Sync useful for you and your horse?"
                />
              </label>

              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Facility search</span>
                  <input
                    value={profile.facility_search_name || ""}
                    onChange={(e) => setField("facility_search_name", e.target.value)}
                    data-testid="owner-facility-search-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="Facility name, if known"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Facility location</span>
                  <input
                    value={profile.facility_city_state || ""}
                    onChange={(e) => setField("facility_city_state", e.target.value)}
                    data-testid="owner-facility-city-state"
                    className="mt-2 input-luxe w-full"
                    placeholder="City, state"
                  />
                </label>
              </div>

              <label className="block">
                <span className="label-eyebrow">Notes</span>
                <textarea
                  value={profile.notes || ""}
                  onChange={(e) => setField("notes", e.target.value)}
                  data-testid="owner-intake-notes"
                  className="mt-2 input-luxe w-full min-h-[80px]"
                  placeholder="Optional context. This does not create a facility membership or horse record."
                />
              </label>

              <button
                type="button"
                onClick={save}
                disabled={saving}
                data-testid="owner-intake-save"
                className="btn-primary inline-flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                {saving ? "Saving..." : "Save owner intake"}
              </button>
            </div>
          )}
        </section>

        <aside className="space-y-5">
          <section className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid="owner-panel-my-horse">
            <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
              <Heart className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
            </div>
            <h2 className="font-display text-2xl text-equine-ivory">My Horse</h2>
            <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">
              {profile.primary_horse_name || "Add your primary horse name to personalize this space."}
            </p>
            {facilityLinked ? (
              <Link to="/owner-portal" className="btn-secondary mt-4 inline-flex items-center gap-2" data-testid="owner-open-owner-portal">
                <Cat className="w-4 h-4" />
                Open owner portal
              </Link>
            ) : (
              <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2 text-[12.5px] text-equine-platinum/65" data-testid="owner-facility-pending">
                Facility connection is pending. Setup can continue without an active facility.
              </div>
            )}
          </section>

          {[
            ["Facility Connection", profile.facility_search_name || "Search and facility lead capture stay placeholder-only in this phase.", ShieldCheck],
            ["Daily Care", "Coming soon: approved owner-visible care status without staff notes or internal payloads.", Heart],
            ["Requests", "Coming soon: owner requests stay in the existing approved workflow.", ClipboardList],
            ["Documents", "Coming soon: policies and signed forms without creating new signature flows.", FileText],
            ["Messages", "Use Messages for approved conversations.", MessageSquare],
          ].map(([title, body, Icon]) => (
            <section key={title} className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid={`owner-panel-${title.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
              <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
              </div>
              <h2 className="font-display text-2xl text-equine-ivory">{title}</h2>
              <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">{body}</p>
            </section>
          ))}
        </aside>
      </div>
    </div>
  );
}

function RiderHome({ user }) {
  const [profile, setProfile] = useState(emptyRiderProfile);
  const [completion, setCompletion] = useState({ percent: 0, missing_fields: [] });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    let alive = true;
    api
      .get("/rider/profile")
      .then((r) => {
        if (!alive) return;
        setProfile({ ...emptyRiderProfile, ...r.data });
        setCompletion(r.data?.completion || { percent: 0, missing_fields: [] });
        setErr("");
      })
      .catch((e) => {
        if (!alive) return;
        setErr(e?.response?.data?.detail || "Could not load rider profile.");
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => { alive = false; };
  }, []);

  const setField = (field, value) => {
    setProfile((p) => ({ ...p, [field]: value }));
  };

  const toggleDiscipline = (name) => {
    setProfile((p) => {
      const current = p.disciplines || [];
      const disciplines = current.includes(name)
        ? current.filter((d) => d !== name)
        : [...current, name];
      return { ...p, disciplines };
    });
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        preferred_name: profile.preferred_name || null,
        disciplines: profile.disciplines || [],
        experience_level: profile.experience_level || null,
        goals: profile.goals || null,
        availability_notes: profile.availability_notes || null,
        emergency_contact_name: profile.emergency_contact_name || null,
        emergency_contact_phone: profile.emergency_contact_phone || null,
        consent_acknowledged: Boolean(profile.consent_acknowledged),
      };
      const { data } = await api.patch("/rider/profile", payload);
      setProfile({ ...emptyRiderProfile, ...data });
      setCompletion(data?.completion || { percent: 0, missing_fields: [] });
      toast.success("Rider profile saved");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not save rider profile");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="role-home-rider">
      <header className="mb-8">
        <div className="label-eyebrow mb-3">Rider Home</div>
        <h1 className="font-display text-4xl md:text-5xl text-equine-ivory">
          Welcome{profile.preferred_name ? `, ${profile.preferred_name}` : user?.full_name ? `, ${user.full_name}` : ""}
        </h1>
        <p className="mt-3 max-w-2xl text-equine-platinum/70 text-[15px] leading-relaxed">
          Build your rider profile, track goals, and keep messages close while lessons, schedule, and documents come online.
        </p>
      </header>

      <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)] gap-5">
        <section className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid="rider-intake-shell">
          <div className="flex items-start justify-between gap-4 mb-5">
            <div>
              <div className="label-eyebrow">Profile completion</div>
              <h2 className="font-display text-3xl text-equine-ivory mt-1">Rider intake</h2>
            </div>
            <div className="w-20 h-20 rounded-2xl bg-equine-navy/60 border border-white/10 flex items-center justify-center">
              <span className="font-display text-3xl text-equine-brassLight">{completion.percent || 0}%</span>
            </div>
          </div>

          {loading ? (
            <div className="text-equine-platinum/60 text-[13px] py-10">Loading rider profile...</div>
          ) : err ? (
            <div className="rounded-xl border border-equine-clay/40 bg-equine-clay/10 p-4 text-equine-clay text-[13px]">{err}</div>
          ) : (
            <div className="space-y-5">
              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Preferred name</span>
                  <input
                    value={profile.preferred_name || ""}
                    onChange={(e) => setField("preferred_name", e.target.value)}
                    data-testid="rider-profile-preferred-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="What should coaches call you?"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Experience</span>
                  <select
                    value={profile.experience_level || ""}
                    onChange={(e) => setField("experience_level", e.target.value)}
                    data-testid="rider-profile-experience"
                    className="mt-2 input-luxe w-full"
                  >
                    {RIDER_EXPERIENCE_LEVELS.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
              </div>

              <div>
                <span className="label-eyebrow">Riding interests</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {RIDER_DISCIPLINES.map((name) => {
                    const active = (profile.disciplines || []).includes(name);
                    return (
                      <button
                        key={name}
                        type="button"
                        onClick={() => toggleDiscipline(name)}
                        data-testid={`rider-discipline-${name.toLowerCase().replace(/[^a-z]+/g, "-")}`}
                        className={`px-3 py-2 rounded-xl border text-[12.5px] transition ${
                          active
                            ? "bg-equine-brassLight text-equine-navy border-equine-brassLight"
                            : "bg-white/[0.03] text-equine-platinum/75 border-white/10 hover:border-equine-brassLight/50"
                        }`}
                      >
                        {name}
                      </button>
                    );
                  })}
                </div>
              </div>

              <label className="block">
                <span className="label-eyebrow">Goals</span>
                <textarea
                  value={profile.goals || ""}
                  onChange={(e) => setField("goals", e.target.value)}
                  data-testid="rider-profile-goals"
                  className="mt-2 input-luxe w-full min-h-[96px]"
                  placeholder="What would you like to work toward?"
                />
              </label>

              <label className="block">
                <span className="label-eyebrow">Availability notes</span>
                <textarea
                  value={profile.availability_notes || ""}
                  onChange={(e) => setField("availability_notes", e.target.value)}
                  data-testid="rider-profile-availability"
                  className="mt-2 input-luxe w-full min-h-[80px]"
                  placeholder="Days/times that usually work best."
                />
              </label>

              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Emergency contact</span>
                  <input
                    value={profile.emergency_contact_name || ""}
                    onChange={(e) => setField("emergency_contact_name", e.target.value)}
                    data-testid="rider-profile-emergency-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="Name"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Emergency phone</span>
                  <input
                    value={profile.emergency_contact_phone || ""}
                    onChange={(e) => setField("emergency_contact_phone", e.target.value)}
                    data-testid="rider-profile-emergency-phone"
                    className="mt-2 input-luxe w-full"
                    placeholder="Phone number"
                  />
                </label>
              </div>

              <label className="flex items-start gap-3 rounded-xl bg-white/[0.03] border border-white/10 p-4">
                <input
                  type="checkbox"
                  checked={Boolean(profile.consent_acknowledged)}
                  onChange={(e) => setField("consent_acknowledged", e.target.checked)}
                  data-testid="rider-profile-consent"
                  className="mt-1"
                />
                <span className="text-[13px] text-equine-platinum/75 leading-relaxed">
                  I understand Equine Sync will use this profile to help my barn or trainer prepare a safer riding experience. Formal documents and signatures are handled separately.
                </span>
              </label>

              <button
                type="button"
                onClick={save}
                disabled={saving}
                data-testid="rider-profile-save"
                className="btn-primary inline-flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                {saving ? "Saving..." : "Save rider profile"}
              </button>
            </div>
          )}
        </section>

        <aside className="space-y-5">
          {[
            ["Schedule", "Coming soon: your barn or trainer will publish lesson and ride times here.", CalendarDays],
            ["Lessons", "Coming soon: lesson plans, prep notes, and trainer feedback.", ClipboardList],
            ["Goals", profile.goals || "Add goals in your rider intake to make this space useful.", Sparkles],
            ["Messages", "Use Messages for barn-approved conversations.", MessageSquare],
            ["Documents", "Coming soon: waivers, policies, and signed forms.", FileText],
          ].map(([title, body, Icon]) => (
            <section key={title} className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid={`rider-panel-${title.toLowerCase()}`}>
              <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
              </div>
              <h2 className="font-display text-2xl text-equine-ivory">{title}</h2>
              <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">{body}</p>
            </section>
          ))}
        </aside>
      </div>
    </div>
  );
}

function GuardianHome({ user }) {
  const [profile, setProfile] = useState(emptyGuardianProfile);
  const [completion, setCompletion] = useState({ percent: 0, missing_fields: [] });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    let alive = true;
    api
      .get("/guardian/minor-rider-profile")
      .then((r) => {
        if (!alive) return;
        setProfile({ ...emptyGuardianProfile, ...r.data });
        setCompletion(r.data?.completion || { percent: 0, missing_fields: [] });
        setErr("");
      })
      .catch((e) => {
        if (!alive) return;
        setErr(e?.response?.data?.detail || "Could not load guardian intake.");
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => { alive = false; };
  }, []);

  const setField = (field, value) => {
    setProfile((p) => ({ ...p, [field]: value }));
  };

  const toggleInterest = (name) => {
    setProfile((p) => {
      const current = p.riding_interests || [];
      const riding_interests = current.includes(name)
        ? current.filter((d) => d !== name)
        : [...current, name];
      return { ...p, riding_interests };
    });
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        guardian_preferred_contact: profile.guardian_preferred_contact || null,
        minor_display_name: profile.minor_display_name || null,
        minor_age_range: profile.minor_age_range || null,
        minor_birthdate: profile.minor_birthdate || null,
        riding_interests: profile.riding_interests || [],
        experience_level: profile.experience_level || null,
        goals: profile.goals || null,
        availability_notes: profile.availability_notes || null,
        emergency_contact_name: profile.emergency_contact_name || null,
        emergency_contact_phone: profile.emergency_contact_phone || null,
        medical_allergy_notes: profile.medical_allergy_notes || null,
      };
      const { data } = await api.patch("/guardian/minor-rider-profile", payload);
      setProfile({ ...emptyGuardianProfile, ...data });
      setCompletion(data?.completion || { percent: 0, missing_fields: [] });
      toast.success("Guardian intake saved");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not save guardian intake");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="role-home-guardian">
      <header className="mb-8">
        <div className="label-eyebrow mb-3">Guardian Home</div>
        <h1 className="font-display text-4xl md:text-5xl text-equine-ivory">
          Minor rider intake{profile.minor_display_name ? ` for ${profile.minor_display_name}` : ""}
        </h1>
        <p className="mt-3 max-w-2xl text-equine-platinum/70 text-[15px] leading-relaxed">
          Share enough context for a safer first barn conversation. Formal consent, waivers, billing, and lesson enrollment stay separate.
        </p>
      </header>

      <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)] gap-5">
        <section className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid="guardian-intake-shell">
          <div className="flex items-start justify-between gap-4 mb-5">
            <div>
              <div className="label-eyebrow">Profile completion</div>
              <h2 className="font-display text-3xl text-equine-ivory mt-1">Guardian intake</h2>
            </div>
            <div className="w-20 h-20 rounded-2xl bg-equine-navy/60 border border-white/10 flex items-center justify-center">
              <span className="font-display text-3xl text-equine-brassLight">{completion.percent || 0}%</span>
            </div>
          </div>

          {loading ? (
            <div className="text-equine-platinum/60 text-[13px] py-10">Loading guardian intake...</div>
          ) : err ? (
            <div className="rounded-xl border border-equine-clay/40 bg-equine-clay/10 p-4 text-equine-clay text-[13px]">{err}</div>
          ) : (
            <div className="space-y-5">
              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Preferred contact</span>
                  <select
                    value={profile.guardian_preferred_contact || ""}
                    onChange={(e) => setField("guardian_preferred_contact", e.target.value)}
                    data-testid="guardian-contact-preference"
                    className="mt-2 input-luxe w-full"
                  >
                    {GUARDIAN_CONTACT_PREFERENCES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
                <label className="block">
                  <span className="label-eyebrow">Minor rider name</span>
                  <input
                    value={profile.minor_display_name || ""}
                    onChange={(e) => setField("minor_display_name", e.target.value)}
                    data-testid="guardian-minor-display-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="Name the barn should use"
                  />
                </label>
              </div>

              <div className="grid md:grid-cols-3 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Age range</span>
                  <select
                    value={profile.minor_age_range || ""}
                    onChange={(e) => setField("minor_age_range", e.target.value)}
                    data-testid="guardian-minor-age-range"
                    className="mt-2 input-luxe w-full"
                  >
                    {MINOR_AGE_RANGES.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
                <label className="block">
                  <span className="label-eyebrow">Birthdate</span>
                  <input
                    value={profile.minor_birthdate || ""}
                    onChange={(e) => setField("minor_birthdate", e.target.value)}
                    data-testid="guardian-minor-birthdate"
                    className="mt-2 input-luxe w-full"
                    placeholder="Optional"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Experience</span>
                  <select
                    value={profile.experience_level || ""}
                    onChange={(e) => setField("experience_level", e.target.value)}
                    data-testid="guardian-minor-experience"
                    className="mt-2 input-luxe w-full"
                  >
                    {RIDER_EXPERIENCE_LEVELS.filter(([v]) => v !== "professional").map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
              </div>

              <div>
                <span className="label-eyebrow">Riding interests</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {RIDER_DISCIPLINES.map((name) => {
                    const active = (profile.riding_interests || []).includes(name);
                    return (
                      <button
                        key={name}
                        type="button"
                        onClick={() => toggleInterest(name)}
                        data-testid={`guardian-interest-${name.toLowerCase().replace(/[^a-z]+/g, "-")}`}
                        className={`px-3 py-2 rounded-xl border text-[12.5px] transition ${
                          active
                            ? "bg-equine-brassLight text-equine-navy border-equine-brassLight"
                            : "bg-white/[0.03] text-equine-platinum/75 border-white/10 hover:border-equine-brassLight/50"
                        }`}
                      >
                        {name}
                      </button>
                    );
                  })}
                </div>
              </div>

              <label className="block">
                <span className="label-eyebrow">Goals</span>
                <textarea
                  value={profile.goals || ""}
                  onChange={(e) => setField("goals", e.target.value)}
                  data-testid="guardian-minor-goals"
                  className="mt-2 input-luxe w-full min-h-[90px]"
                  placeholder="What would you like the rider to work toward?"
                />
              </label>

              <label className="block">
                <span className="label-eyebrow">Availability notes</span>
                <textarea
                  value={profile.availability_notes || ""}
                  onChange={(e) => setField("availability_notes", e.target.value)}
                  data-testid="guardian-minor-availability"
                  className="mt-2 input-luxe w-full min-h-[80px]"
                  placeholder="Days/times that usually work best."
                />
              </label>

              <div className="grid md:grid-cols-2 gap-4">
                <label className="block">
                  <span className="label-eyebrow">Emergency contact</span>
                  <input
                    value={profile.emergency_contact_name || ""}
                    onChange={(e) => setField("emergency_contact_name", e.target.value)}
                    data-testid="guardian-emergency-name"
                    className="mt-2 input-luxe w-full"
                    placeholder="Name"
                  />
                </label>
                <label className="block">
                  <span className="label-eyebrow">Emergency phone</span>
                  <input
                    value={profile.emergency_contact_phone || ""}
                    onChange={(e) => setField("emergency_contact_phone", e.target.value)}
                    data-testid="guardian-emergency-phone"
                    className="mt-2 input-luxe w-full"
                    placeholder="Phone number"
                  />
                </label>
              </div>

              <label className="block">
                <span className="label-eyebrow">Medical or allergy notes</span>
                <textarea
                  value={profile.medical_allergy_notes || ""}
                  onChange={(e) => setField("medical_allergy_notes", e.target.value)}
                  data-testid="guardian-medical-allergy-notes"
                  className="mt-2 input-luxe w-full min-h-[86px]"
                  placeholder="Optional. This stays in the guardian intake record until a formal barn workflow is connected."
                />
              </label>

              <div className="rounded-xl bg-white/[0.03] border border-white/10 p-4 text-[13px] text-equine-platinum/75 leading-relaxed" data-testid="guardian-consent-status">
                Consent status: <span className="text-equine-brassLight">pending formal consent</span>. This intake does not replace signed waivers, legal guardian approval, or barn participation requirements.
              </div>

              <button
                type="button"
                onClick={save}
                disabled={saving}
                data-testid="guardian-intake-save"
                className="btn-primary inline-flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                {saving ? "Saving..." : "Save guardian intake"}
              </button>
            </div>
          )}
        </section>

        <aside className="space-y-5">
          {[
            ["Rider Overview", profile.minor_display_name || "Add the rider's name to personalize this overview.", Cat],
            ["Schedule", "Coming soon: lesson and ride times once the barn connects this rider.", CalendarDays],
            ["Progress Notes", "Coming soon: barn-approved progress notes and trainer summaries.", MessageSquare],
            ["Documents", "Coming soon: waivers, barn policies, and signed forms.", FileText],
            ["Requests", "Coming soon: guardian requests without opening staff-only workflows.", ClipboardList],
            ["Emergency Info", profile.emergency_contact_name || "Add emergency contact details in the intake form.", ShieldCheck],
          ].map(([title, body, Icon]) => (
            <section key={title} className="rounded-2xl bg-equine-card border border-equine-hairline p-5" data-testid={`guardian-panel-${title.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
              <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
              </div>
              <h2 className="font-display text-2xl text-equine-ivory">{title}</h2>
              <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">{body}</p>
            </section>
          ))}
        </aside>
      </div>
    </div>
  );
}

export default function RoleHome() {
  const { profile } = useParams();
  const { user } = useAuth();
  const config = PROFILES[profile];

  if (!config) return <Navigate to={resolvePostLoginPath(user)} replace />;
  if (profile === "rider") return <RiderHome user={user} />;
  if (profile === "guardian") return <GuardianHome user={user} />;
  if (profile === "owner") return <OwnerHome user={user} />;
  if (profile === "barn-owner") return <BarnOwnerHome user={user} />;
  if (profile === "trainer") return <TrainerHome user={user} />;
  if (profile === "manager") return <ManagerHome user={user} />;
  if (profile === "staff") return <StaffHome user={user} />;

  return (
    <div
      className="max-w-5xl mx-auto pb-20 lg:pb-8"
      data-testid={`role-home-${profile}`}
    >
      <header className="mb-8">
        <div className="label-eyebrow mb-3">{config.eyebrow}</div>
        <h1 className="font-display text-4xl md:text-5xl text-equine-ivory">
          {config.title}
        </h1>
        <p className="mt-3 max-w-2xl text-equine-platinum/70 text-[15px] leading-relaxed">
          {config.subtitle}
        </p>
      </header>

      <div className="grid md:grid-cols-3 gap-5">
        {config.cards.map(([title, body, Icon]) => (
          <section
            key={title}
            className="rounded-2xl bg-equine-card border border-equine-hairline p-5"
          >
            <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
              <Icon className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
            </div>
            <h2 className="font-display text-2xl text-equine-ivory">{title}</h2>
            <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">
              {body}
            </p>
          </section>
        ))}
      </div>

      <div className="mt-7 flex flex-wrap gap-3">
        {config.primary.to ? (
          <Link
            to={config.primary.to}
            className="btn-primary inline-flex items-center gap-2"
            data-testid={`role-home-primary-${profile}`}
          >
            <Cat className="w-4 h-4" />
            {config.primary.label}
          </Link>
        ) : (
          <button
            type="button"
            disabled
            className="btn-secondary inline-flex items-center gap-2 opacity-70 cursor-not-allowed"
            data-testid={`role-home-primary-${profile}`}
          >
            <Cat className="w-4 h-4" />
            {config.primary.label}
          </button>
        )}
        <Link
          to="/messaging"
          className="btn-secondary inline-flex items-center gap-2"
          data-testid={`role-home-messages-${profile}`}
        >
          <ShieldCheck className="w-4 h-4" />
          Messages
        </Link>
      </div>
    </div>
  );
}
