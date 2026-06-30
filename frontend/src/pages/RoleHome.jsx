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

export default function RoleHome() {
  const { profile } = useParams();
  const { user } = useAuth();
  const config = PROFILES[profile];

  if (!config) return <Navigate to={resolvePostLoginPath(user)} replace />;
  if (profile === "rider") return <RiderHome user={user} />;

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
