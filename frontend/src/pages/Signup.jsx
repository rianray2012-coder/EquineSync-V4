import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api, tokens } from "../lib/api";
import { Logo } from "../components/Logo";
import { Check, ArrowRight, ArrowLeft } from "lucide-react";
import {
  sortPlans, formatCents, annualSavingsPct, isPlanCheckoutable,
} from "../lib/subscriptionBilling";

// Phase 15.C — these recommendations map the marketplace role pick (Step 0)
// to a default facility plan tier for Step 3. Solo roles default to "free";
// barn/facility roles default to "starter" (the cheapest paid B2B plan). The
// user can always override on Step 3.
const ROLE_TO_PLAN = {
  horse_owner: "free",
  rider: "free",
  trainer: "free",
  service_provider: "free",
  barn_owner: "starter",
};

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
    ? ROLE_TO_PLAN[initialRole] || "free"
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
  const [signupCycle, setSignupCycle] = useState("monthly");
  // Plan catalog from /api/billing/plans — populated after the account is
  // created (the endpoint requires auth). Falls back to an empty array, which
  // hides the catalog UI and lets the user proceed on Free.
  const [plans, setPlans] = useState([]);
  const [err, setErr] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const role = ROLE_OPTIONS.find((r) => r.id === form.role);

  // Lazy-load the plan catalog when Step 3 becomes reachable (after the
  // account is created and the session is set in submitAccount).
  useEffect(() => {
    if (stepIdx < 1) return;
    if (plans.length) return;
    api.get("/billing/plans").then((r) => setPlans(sortPlans(r.data))).catch(() => setPlans([]));
  }, [stepIdx, plans.length]);

  const updateForm = (k, v) => setForm((f) => ({ ...f, [k]: v }));
  const updateProfile = (k, v) => setProfile((p) => ({ ...p, [k]: v }));

  const pickRole = (roleId) => {
    setForm((f) => ({ ...f, role: roleId }));
    if (!tier) setTier(ROLE_TO_PLAN[roleId] || "free");
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
    // Enterprise → contact sales (no Stripe checkout).
    if (tier === "enterprise") {
      window.location.assign("mailto:sales@equinesync.com?subject=Enterprise%20plan%20enquiry");
      return;
    }
    // Free uses the legacy membership endpoint (untouched in 15.C — 15.G will
    // remove it). Paid (Starter/Professional) uses the new Phase 15 endpoint
    // which bakes in the 14-day Stripe trial via subscription_data.
    setSubmitting(true);
    try {
      if (tier === "free") {
        const { data } = await api.post("/membership/checkout", {
          tier,
          origin_url: window.location.origin,
        });
        if (data.url) {
          window.location.href = data.url;
          return;
        }
        navigate("/dashboard");
        return;
      }
      const selectedPlan = plans.find((p) => p.tier_code === tier);
      // Phase 15.C — pick the safest cycle: prefer the user's selection, but
      // fall back to whichever cycle is actually checkoutable. The Step 3 UI
      // already disables the CTA when neither cycle is checkoutable, so by
      // the time we get here at least one is guaranteed.
      let cycleToUse = signupCycle;
      if (!isPlanCheckoutable(selectedPlan, cycleToUse)) {
        cycleToUse = signupCycle === "monthly" ? "annual" : "monthly";
      }
      const { data } = await api.post("/subscriptions/checkout", {
        plan_tier_code: tier,
        billing_cycle: cycleToUse,
        origin_url: window.location.origin,
      });
      if (data.url) {
        window.location.href = data.url;
        return;
      }
      navigate("/dashboard");
    } catch (e) {
      setErr(e?.response?.data?.detail || "Could not start checkout.");
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

          {/* Step 3 — membership + Stripe (Phase 15.C) */}
          {stepIdx === 2 && (
            <div data-testid="signup-step-membership">
              <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle font-medium mb-3">Step 3 of 3</div>
              <div className="flex items-end justify-between flex-wrap gap-4 mb-3">
                <h2 className="font-display text-3xl md:text-4xl font-light text-white">Choose your plan</h2>
                {/* Monthly / Annual toggle — only meaningful for paid tiers */}
                <div
                  className="inline-flex bg-white/5 border border-white/10 rounded-full p-0.5"
                  data-testid="signup-cycle-toggle"
                  role="tablist"
                  aria-label="Billing cycle"
                >
                  {["monthly", "annual"].map((c) => (
                    <button
                      key={c}
                      type="button"
                      onClick={() => setSignupCycle(c)}
                      data-testid={`signup-cycle-${c}`}
                      className={`px-4 py-1.5 text-[11.5px] tracking-wide uppercase rounded-full transition-colors ${
                        signupCycle === c
                          ? "bg-equine-saddle text-equine-navyDeep"
                          : "text-white/65 hover:text-white"
                      }`}
                    >
                      {c}
                    </button>
                  ))}
                </div>
              </div>
              <p className="text-white/60 text-[14px] mb-8">
                Paid plans include a <span className="text-equine-saddle font-medium">14-day free trial</span>.
                Cancel from your account anytime — Free stays free forever.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" data-testid="signup-plan-grid">
                {plans.length === 0 && (
                  <div className="col-span-full text-white/40 text-[13px]" data-testid="signup-plan-empty">
                    Loading plans…
                  </div>
                )}
                {plans.map((p) => {
                  const selected = tier === p.tier_code;
                  const isFree = p.tier_code === "free";
                  const isEnterprise = p.tier_code === "enterprise" || !!p.contact_sales;
                  const priceCents =
                    signupCycle === "annual" && p.annual_price_cents != null
                      ? p.annual_price_cents
                      : p.monthly_price_cents;
                  const savings = annualSavingsPct(p);
                  return (
                    <button
                      key={p.tier_code}
                      type="button"
                      onClick={() => setTier(p.tier_code)}
                      className={`text-left p-5 rounded-xl border transition-all flex flex-col ${
                        selected
                          ? "border-equine-saddle bg-equine-saddle/10"
                          : "border-white/10 bg-white/5 hover:border-white/30"
                      }`}
                      data-testid={`signup-tier-${p.tier_code}`}
                    >
                      <div className="flex items-baseline justify-between gap-2">
                        <div className="font-display text-xl text-white capitalize">{p.name || p.tier_code}</div>
                      </div>
                      <div className="mt-2 text-white font-display text-2xl">
                        {isEnterprise ? (
                          "Let's talk"
                        ) : isFree ? (
                          <>$0<span className="text-[12px] text-white/40 font-sans"> /mo</span></>
                        ) : (
                          <>
                            {formatCents(priceCents)}
                            <span className="text-[12px] text-white/40 font-sans">
                              {signupCycle === "annual" ? " /yr" : " /mo"}
                            </span>
                          </>
                        )}
                      </div>
                      {signupCycle === "annual" && savings != null && !isEnterprise && !isFree && (
                        <div className="mt-1 text-[10.5px] tracking-[0.2em] uppercase text-equine-saddle" data-testid={`signup-savings-${p.tier_code}`}>
                          Save {savings}%
                        </div>
                      )}
                      <div className="text-[12.5px] text-white/55 mt-2 leading-relaxed flex-1">{p.description}</div>
                      {p.feature_limits && (
                        <div className="mt-3 text-[11.5px] text-white/55 space-y-1">
                          {p.feature_limits.horses != null && (
                            <div className="flex items-center gap-1.5"><Check className="w-3 h-3 text-equine-saddle" /> Up to {p.feature_limits.horses} horses</div>
                          )}
                          {p.feature_limits.users != null && (
                            <div className="flex items-center gap-1.5"><Check className="w-3 h-3 text-equine-saddle" /> Up to {p.feature_limits.users} users</div>
                          )}
                        </div>
                      )}
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
                ) : tier === "enterprise" ? (
                  <a
                    href="mailto:sales@equinesync.com?subject=Enterprise%20plan%20enquiry"
                    className="bg-equine-saddle text-equine-navyDeep hover:bg-white transition-all px-7 py-3 text-[13px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                    data-testid="signup-contact-sales"
                  >
                    Contact sales <ArrowRight className="w-4 h-4" />
                  </a>
                ) : (() => {
                  // Phase 15.C — gate the paid CTA on Stripe price-ID readiness
                  // (has_monthly / has_annual from /api/billing/plans). When
                  // neither cycle has a price ID, the backend would 500 on
                  // /api/subscriptions/checkout; surface a "Billing setup
                  // pending" message instead. When only one cycle is available
                  // we silently force that cycle.
                  const selectedPlan = plans.find((p) => p.tier_code === tier);
                  const cycleOk = isPlanCheckoutable(selectedPlan, signupCycle);
                  const noCycles = selectedPlan && !selectedPlan.contact_sales && !selectedPlan.has_monthly && !selectedPlan.has_annual;
                  const otherCycle = signupCycle === "monthly" ? "annual" : "monthly";
                  const otherOk = isPlanCheckoutable(selectedPlan, otherCycle);
                  return (
                    <div className="flex flex-col items-end gap-2">
                      <button
                        onClick={launchCheckout}
                        disabled={submitting || !tier || noCycles || (!cycleOk && !otherOk)}
                        className="bg-equine-saddle text-equine-navyDeep hover:bg-white disabled:opacity-40 disabled:cursor-not-allowed transition-all px-7 py-3 text-[13px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                        data-testid="signup-start-trial"
                      >
                        {submitting ? "Starting…" : noCycles ? "Billing setup pending" : "Start 14-day free trial"}
                        {!noCycles && <ArrowRight className="w-4 h-4" />}
                      </button>
                      {noCycles && (
                        <div
                          data-testid="signup-billing-setup-pending"
                          className="text-equine-clay text-[12px] text-right max-w-[280px]"
                        >
                          Stripe pricing for {selectedPlan?.name || tier} is being configured.
                          Pick a different plan or contact support to subscribe.
                        </div>
                      )}
                      {!noCycles && !cycleOk && otherOk && (
                        <div
                          data-testid="signup-cycle-fallback-hint"
                          className="text-white/60 text-[12px] text-right max-w-[280px]"
                        >
                          {signupCycle === "monthly" ? "Monthly" : "Annual"} pricing for {selectedPlan?.name || tier} isn&apos;t available yet —
                          we&apos;ll start you on {otherCycle} instead.
                        </div>
                      )}
                    </div>
                  );
                })()}
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
