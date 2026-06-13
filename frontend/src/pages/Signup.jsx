import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api, tokens } from "../lib/api";
import { Logo } from "../components/Logo";
import { Check, ArrowRight, ArrowLeft } from "lucide-react";

const ROLE_OPTIONS = [
  { id: "horse_owner", label: "Horse Owner", blurb: "Track your horse's care, billing, progress.", recommendedTier: "owner_rider" },
  { id: "rider", label: "Rider", blurb: "Log sessions, follow your training plan.", recommendedTier: "owner_rider" },
  { id: "trainer", label: "Trainer", blurb: "Manage clients, sessions, and notes.", recommendedTier: "trainer_provider", pending: true },
  { id: "barn_owner", label: "Barn / Facility", blurb: "Run a full operation under one roof.", recommendedTier: "barn_facility", pending: true },
  { id: "service_provider", label: "Service Provider", blurb: "Connect with barns that need your craft.", recommendedTier: "trainer_provider", pending: true },
];

const ROLE_PROFILE_FIELDS = {
  horse_owner: [
    { name: "horse_name", label: "Your horse's name", placeholder: "Optional" },
    { name: "horse_breed", label: "Breed", placeholder: "Optional" },
    { name: "discipline", label: "Discipline", placeholder: "Dressage, jumping, trail…" },
  ],
  rider: [
    { name: "discipline", label: "Discipline", placeholder: "Dressage, jumping, trail…" },
    { name: "skill_level", label: "Skill level", placeholder: "Beginner / Intermediate / Advanced" },
    { name: "goals", label: "What are you working towards?", placeholder: "Optional", textarea: true },
  ],
  trainer: [
    { name: "specialties", label: "Specialties", placeholder: "e.g. Hunter/Jumper, Eventing" },
    { name: "years_experience", label: "Years of experience", placeholder: "Optional" },
    { name: "certifications", label: "Certifications", placeholder: "Optional", textarea: true },
  ],
  barn_owner: [
    { name: "barn_name", label: "Barn / facility name", placeholder: "" },
    { name: "stall_capacity", label: "Stall capacity", placeholder: "Approx. number of stalls" },
    { name: "boarding_options", label: "Boarding options", placeholder: "Full / Pasture / Self-care…", textarea: true },
  ],
  service_provider: [
    { name: "service_type", label: "Service type", placeholder: "Veterinarian, farrier, body worker…" },
    { name: "service_radius_miles", label: "Service radius (miles)", placeholder: "Optional" },
    { name: "bio", label: "Short bio", placeholder: "Optional", textarea: true },
  ],
};

const STEPS = ["Account", "Profile", "Membership"];

export default function Signup() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const { setSession, refreshMe } = useAuth();

  const initialRole = params.get("role");
  const initialIsRole = ROLE_OPTIONS.some((r) => r.id === initialRole);
  const initialTier = initialIsRole
    ? ROLE_OPTIONS.find((r) => r.id === initialRole).recommendedTier
    : "";

  const [stepIdx, setStepIdx] = useState(0);
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    phone: "",
    password: "",
    location: "",
    role: initialIsRole ? initialRole : "",
  });
  const [profile, setProfile] = useState({});
  const [tier, setTier] = useState(initialTier);
  const [tiers, setTiers] = useState([]);
  const [err, setErr] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const role = ROLE_OPTIONS.find((r) => r.id === form.role);

  useEffect(() => {
    api.get("/membership/tiers").then((r) => setTiers(r.data)).catch(() => setTiers([]));
  }, []);

  const updateForm = (k, v) => setForm((f) => ({ ...f, [k]: v }));
  const updateProfile = (k, v) => setProfile((p) => ({ ...p, [k]: v }));

  const pickRole = (roleId) => {
    setForm((f) => ({ ...f, role: roleId }));
    const r = ROLE_OPTIONS.find((x) => x.id === roleId);
    if (r && !tier) setTier(r.recommendedTier);
  };

  const canProceedStep0 = useMemo(() => {
    return (
      form.full_name.trim().length >= 2 &&
      /\S+@\S+\.\S+/.test(form.email) &&
      form.password.length >= 8 &&
      !!form.role
    );
  }, [form]);

  const submitAccount = async () => {
    setErr("");
    setSubmitting(true);
    try {
      const payload = {
        email: form.email.trim().toLowerCase(),
        password: form.password,
        full_name: form.full_name.trim(),
        role: form.role,
        phone: form.phone || null,
        location: form.location || null,
        // Tier is selected on Step 3 (membership). Always create the account
        // on the free tier first so Step 3 can call /membership/start-trial
        // or /membership/checkout without colliding with a pre-committed tier.
        tier: "free",
        profile,
      };
      const { data } = await api.post("/auth/signup", payload);
      if (data.pending_verification) {
        // Email-verification enforcement is ON — no session yet.
        navigate(`/login?verify_email=${encodeURIComponent(payload.email)}`);
        return data;
      }
      tokens.set({ token: data.token, refresh_token: data.refresh_token });
      setSession(data.user);
      return data;
    } catch (e) {
      const msg = e?.response?.data?.detail || "Could not create your account.";
      setErr(typeof msg === "string" ? msg : "Could not create your account.");
      throw e;
    } finally {
      setSubmitting(false);
    }
  };

  const launchCheckout = async () => {
    setErr("");
    setSubmitting(true);
    try {
      const { data } = await api.post("/membership/checkout", {
        tier,
        origin_url: window.location.origin,
      });
      if (data.url) {
        window.location.href = data.url;
        return;
      }
      // Free fallthrough (shouldn't happen here).
      navigate("/dashboard");
    } catch (e) {
      setErr(e?.response?.data?.detail || "Could not start checkout.");
    } finally {
      setSubmitting(false);
    }
  };

  const startTrial = async () => {
    // 7-day free trial on a paid tier — no card needed. Server-side only.
    setErr("");
    setSubmitting(true);
    try {
      await api.post("/membership/start-trial", { tier, origin_url: window.location.origin });
      await refreshMe();
      navigate("/dashboard");
    } catch (e) {
      setErr(e?.response?.data?.detail || "Could not start trial.");
    } finally {
      setSubmitting(false);
    }
  };

  const finalizeFreeRefreshed = async () => {
    setSubmitting(true);
    try {
      await api.post("/membership/checkout", { tier: "free", origin_url: window.location.origin });
      await refreshMe();
      navigate("/dashboard");
    } catch (e) {
      setErr("Could not finalize free plan.");
    } finally {
      setSubmitting(false);
    }
  };

  // ----- Step actions -----
  const nextStep = async () => {
    setErr("");
    if (stepIdx === 0) {
      if (!canProceedStep0) {
        setErr("Please complete name, email, an 8+ character password, and choose a role.");
        return;
      }
      // Create account on transition from Step 0 → Step 1 so the next steps
      // can call authenticated endpoints (checkout requires auth).
      try {
        await submitAccount();
      } catch {
        return;
      }
      setStepIdx(1);
    } else if (stepIdx === 1) {
      setStepIdx(2);
    }
  };

  const skipProfile = () => {
    setProfile({});
    setStepIdx(2);
  };

  const back = () => setStepIdx((i) => Math.max(0, i - 1));

  return (
    <div className="min-h-screen w-full bg-equine-navyDeep text-white font-sans" data-testid="signup-page">
      <header className="px-6 md:px-12 py-6 max-w-5xl mx-auto flex items-center justify-between">
        <Logo onNavy />
        <Link to="/" className="text-[12px] tracking-wide text-white/60 hover:text-white" data-testid="signup-back-landing">
          ← Back to home
        </Link>
      </header>

      <div className="max-w-2xl mx-auto px-6 pb-20">
        {/* Step indicator */}
        <div className="flex items-center justify-between mb-10" data-testid="signup-step-indicator">
          {STEPS.map((label, i) => (
            <React.Fragment key={label}>
              <div className="flex items-center gap-3">
                <div
                  className={`w-7 h-7 rounded-full flex items-center justify-center text-[12px] font-medium border ${
                    i < stepIdx
                      ? "bg-equine-saddle text-equine-navyDeep border-equine-saddle"
                      : i === stepIdx
                      ? "border-equine-saddle text-equine-saddle"
                      : "border-white/15 text-white/30"
                  }`}
                >
                  {i < stepIdx ? <Check className="w-3.5 h-3.5" /> : i + 1}
                </div>
                <div className={`text-[12px] tracking-[0.2em] uppercase ${i === stepIdx ? "text-white" : "text-white/40"}`}>
                  {label}
                </div>
              </div>
              {i < STEPS.length - 1 && <div className="flex-1 h-px bg-white/10 mx-3" />}
            </React.Fragment>
          ))}
        </div>

        <div className="bg-equine-navy/60 border border-white/10 rounded-2xl p-8 md:p-10 backdrop-blur-xl shadow-2xl">
          {/* Step 1 — account basics */}
          {stepIdx === 0 && (
            <div data-testid="signup-step-account">
              <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle font-medium mb-3">Step 1 of 3</div>
              <h2 className="font-display text-3xl md:text-4xl font-light text-white mb-2">Create your account</h2>
              <p className="text-white/60 text-[14px] mb-8">A few basics — you can finish your profile later.</p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Field label="Full name" required>
                  <input
                    value={form.full_name}
                    onChange={(e) => updateForm("full_name", e.target.value)}
                    className={inputCls}
                    data-testid="signup-full-name"
                    placeholder="Jane Doe"
                  />
                </Field>
                <Field label="Email" required>
                  <input
                    type="email"
                    value={form.email}
                    onChange={(e) => updateForm("email", e.target.value)}
                    className={inputCls}
                    data-testid="signup-email"
                    placeholder="you@your-barn.com"
                  />
                </Field>
                <Field label="Phone">
                  <input
                    value={form.phone}
                    onChange={(e) => updateForm("phone", e.target.value)}
                    className={inputCls}
                    data-testid="signup-phone"
                    placeholder="Optional"
                  />
                </Field>
                <Field label="Location">
                  <input
                    value={form.location}
                    onChange={(e) => updateForm("location", e.target.value)}
                    className={inputCls}
                    data-testid="signup-location"
                    placeholder="City, State"
                  />
                </Field>
                <Field label="Password" required full>
                  <input
                    type="password"
                    value={form.password}
                    onChange={(e) => updateForm("password", e.target.value)}
                    className={inputCls}
                    data-testid="signup-password"
                    placeholder="At least 8 characters"
                  />
                </Field>
              </div>

              <div className="mt-8">
                <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle font-medium mb-3">I am a…</div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3" data-testid="signup-role-grid">
                  {ROLE_OPTIONS.map((r) => (
                    <button
                      key={r.id}
                      type="button"
                      onClick={() => pickRole(r.id)}
                      className={`text-left p-4 rounded-xl border transition-all ${
                        form.role === r.id
                          ? "border-equine-saddle bg-equine-saddle/10"
                          : "border-white/10 bg-white/5 hover:border-white/30"
                      }`}
                      data-testid={`signup-role-${r.id}`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="font-display text-lg text-white">{r.label}</div>
                        {r.pending && (
                          <span className="text-[9px] tracking-[0.2em] uppercase text-equine-saddle bg-equine-saddle/10 border border-equine-saddle/30 px-1.5 py-0.5 rounded-full whitespace-nowrap">
                            Review
                          </span>
                        )}
                      </div>
                      <div className="text-[12px] text-white/55 mt-1 leading-relaxed">{r.blurb}</div>
                    </button>
                  ))}
                </div>
              </div>

              {err && <div className="mt-5 text-equine-clay text-[13px]" data-testid="signup-error">{err}</div>}

              <div className="mt-8 flex items-center justify-between">
                <Link to="/login" className="text-[13px] text-white/60 hover:text-white" data-testid="signup-have-account">
                  Already a member? Sign in
                </Link>
                <button
                  onClick={nextStep}
                  disabled={!canProceedStep0 || submitting}
                  className="bg-white text-equine-navyDeep hover:bg-equine-saddle disabled:opacity-40 disabled:cursor-not-allowed transition-all px-6 py-3 text-[13px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                  data-testid="signup-step-next"
                >
                  {submitting ? "Creating…" : "Continue"} <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 2 — profile */}
          {stepIdx === 1 && (
            <div data-testid="signup-step-profile">
              <div className="flex items-center justify-between mb-3">
                <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle font-medium">Step 2 of 3</div>
                <button
                  onClick={skipProfile}
                  className="text-[12px] tracking-wide text-equine-saddle hover:text-white transition-colors px-3 py-1 rounded-full border border-equine-saddle/30 hover:bg-equine-saddle/10"
                  data-testid="signup-skip-profile"
                >
                  Skip & complete later
                </button>
              </div>
              <h2 className="font-display text-3xl md:text-4xl font-light text-white mb-2">
                Tell us about your {role?.label?.toLowerCase()}
              </h2>
              <p className="text-white/60 text-[14px] mb-8">
                Optional — fill out anything you want now, the rest can wait.
              </p>

              <div className="space-y-4">
                {(ROLE_PROFILE_FIELDS[form.role] || []).map((f) => (
                  <Field key={f.name} label={f.label} full>
                    {f.textarea ? (
                      <textarea
                        rows={3}
                        value={profile[f.name] || ""}
                        onChange={(e) => updateProfile(f.name, e.target.value)}
                        className={inputCls}
                        data-testid={`signup-profile-${f.name}`}
                        placeholder={f.placeholder}
                      />
                    ) : (
                      <input
                        value={profile[f.name] || ""}
                        onChange={(e) => updateProfile(f.name, e.target.value)}
                        className={inputCls}
                        data-testid={`signup-profile-${f.name}`}
                        placeholder={f.placeholder}
                      />
                    )}
                  </Field>
                ))}
              </div>

              <div className="mt-8 flex items-center justify-between">
                <button onClick={back} className="text-[13px] text-white/60 hover:text-white inline-flex items-center gap-2" data-testid="signup-step-back">
                  <ArrowLeft className="w-4 h-4" /> Back
                </button>
                <button
                  onClick={nextStep}
                  disabled={submitting}
                  className="bg-white text-equine-navyDeep hover:bg-equine-saddle transition-all px-6 py-3 text-[13px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                  data-testid="signup-step-next"
                >
                  Continue <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Step 3 — membership + Stripe */}
          {stepIdx === 2 && (
            <div data-testid="signup-step-membership">
              <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle font-medium mb-3">Step 3 of 3</div>
              <h2 className="font-display text-3xl md:text-4xl font-light text-white mb-2">Choose your tier</h2>
              <p className="text-white/60 text-[14px] mb-8">
                Paid tiers include a <span className="text-equine-saddle font-medium">7-day free trial</span> — no card needed.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {tiers.map((t) => {
                  const selected = tier === t.id;
                  return (
                    <button
                      key={t.id}
                      type="button"
                      onClick={() => setTier(t.id)}
                      className={`text-left p-5 rounded-xl border transition-all ${
                        selected
                          ? "border-equine-saddle bg-equine-saddle/10"
                          : "border-white/10 bg-white/5 hover:border-white/30"
                      }`}
                      data-testid={`signup-tier-${t.id}`}
                    >
                      <div className="flex items-baseline justify-between">
                        <div className="font-display text-xl text-white">{t.label}</div>
                        <div className="text-white font-display text-2xl">
                          ${t.amount}<span className="text-[12px] text-white/40 font-sans"> /mo</span>
                        </div>
                      </div>
                      <div className="text-[12.5px] text-white/55 mt-2 leading-relaxed">{t.blurb}</div>
                    </button>
                  );
                })}
              </div>

              {err && <div className="mt-5 text-equine-clay text-[13px]" data-testid="signup-error">{err}</div>}

              <div className="mt-8 flex items-center justify-between flex-wrap gap-4">
                <button onClick={back} className="text-[13px] text-white/60 hover:text-white inline-flex items-center gap-2" data-testid="signup-step-back">
                  <ArrowLeft className="w-4 h-4" /> Back
                </button>
                {tier === "free" ? (
                  <button
                    onClick={finalizeFreeRefreshed}
                    disabled={submitting}
                    className="bg-white text-equine-navyDeep hover:bg-equine-saddle transition-all px-7 py-3 text-[13px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                    data-testid="signup-finish-free"
                  >
                    {submitting ? "Finishing…" : "Start with Free"} <ArrowRight className="w-4 h-4" />
                  </button>
                ) : (
                  <div className="flex flex-wrap items-center gap-3">
                    <button
                      onClick={startTrial}
                      disabled={submitting || !tier}
                      className="bg-equine-saddle text-equine-navyDeep hover:bg-white disabled:opacity-40 disabled:cursor-not-allowed transition-all px-7 py-3 text-[13px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                      data-testid="signup-start-trial"
                    >
                      {submitting ? "Starting…" : "Start 7-day free trial"} <ArrowRight className="w-4 h-4" />
                    </button>
                    <button
                      onClick={launchCheckout}
                      disabled={submitting || !tier}
                      className="text-[13px] tracking-wide text-white/70 hover:text-white disabled:opacity-40 transition-colors px-4 py-3"
                      data-testid="signup-checkout"
                    >
                      Or pay now →
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const inputCls =
  "w-full bg-equine-navyDeep/50 border border-white/10 text-white placeholder:text-white/30 px-4 py-3 rounded-lg text-[14px] focus:outline-none focus:border-equine-saddle/60 transition-colors";

function Field({ label, required, full, children }) {
  return (
    <label className={`block ${full ? "md:col-span-2" : ""}`}>
      <span className="block text-[11px] tracking-[0.2em] uppercase text-white/60 mb-2">
        {label}
        {required && <span className="text-equine-saddle ml-1">*</span>}
      </span>
      {children}
    </label>
  );
}
