import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Logo } from "../components/Logo";
import { Check, ArrowRight, ShieldCheck, Sparkles, Users, Calendar } from "lucide-react";
import { annualSavingsPct, formatCents, sortPlans } from "../lib/subscriptionBilling";
import { api } from "../lib/api";

const ROLE_CARDS = [
  {
    id: "horse_owner",
    label: "Individual Horse Owner",
    blurb: "Track your horse's care, billing and progress outside an EquineSync barn workspace.",
    image:
      "https://images.unsplash.com/photo-1600715151005-e6d44b9ef840?auto=format&fit=crop&w=1400&q=85",
    span: "md:col-span-3",
  },
  {
    id: "barn_owner",
    label: "Barn Owner / Manager",
    blurb: "Start a barn workspace for stalls, staff, owners, billing, and facility operations.",
    image:
      "https://images.unsplash.com/photo-1576692192914-9abed71b3ef9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODF8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBob3JzZSUyMGJhcm58ZW58MHx8fHwxNzgxMzQxNTQ5fDA&ixlib=rb-4.1.0&q=85",
    span: "md:col-span-3",
  },
  {
    id: "service_provider",
    label: "Service Provider",
    blurb: "Vets, farriers, body workers — connect with barns that need your expertise.",
    image:
      "https://images.unsplash.com/photo-1649127616601-6f0a3ea26eae?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwxfHxlcXVlc3RyaWFuJTIwZmFycmllcnxlbnwwfHx8fDE3ODEzNDE1NjF8MA&ixlib=rb-4.1.0&q=85",
    span: "md:col-span-2",
  },
  {
    id: "trainer",
    label: "Trainer",
    blurb: "Manage clients, sessions, and progress notes with EquineSync verification.",
    image:
      "https://images.unsplash.com/photo-1594768816441-1dd241ffaa67?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxOTB8MHwxfHNlYXJjaHwxfHxlcXVlc3RyaWFuJTIwdHJhaW5lcnxlbnwwfHx8fDE3ODEzNDE1NDl8MA&ixlib=rb-4.1.0&q=85",
    span: "md:col-span-2",
  },
];

const TRUST = [
  { Icon: ShieldCheck, label: "Verified equestrian network" },
  { Icon: Calendar, label: "Skip & complete your profile later" },
  { Icon: Users, label: "4 public paths, invite-only barn roles" },
  { Icon: Sparkles, label: "Cancel anytime" },
];

// Phase 15.G round-2 (Codex blocker #3): Landing's pricing band is now
// SOURCED EXCLUSIVELY from `/api/billing/plans-public`. We no longer carry
// any prices, plan names, or descriptions in static frontend code — if
// that catalog changes server-side, this page reflects it immediately.
// The only thing kept locally is *marketing bullet copy*, keyed by
// tier_code, since the public API intentionally does not carry it. If the
// API call fails the page shows a graceful "pricing temporarily
// unavailable" state with a Contact-Sales CTA — it does NOT show stale
// hard-coded prices.
const LANDING_BULLETS_BY_TIER = {
  free: [
    "Included with subscribed barns",
    "Approved updates, invoices, photos & documents",
    "Owner requests and barn messaging",
  ],
  individual_owner: [
    null,
    "Feed, supplement, vet & farrier records",
    "Training notes, calendar, emergency profile",
  ],
  service_provider_free: [
    "Basic horse info, calendar and appointment scheduling",
    "Free profile for vets, farriers and care partners",
    "Scoped access through client and barn connections",
  ],
  service_provider_premium: [
    "Everything in Service Provider Free",
    "Premium scheduling, client notes and documents",
    "Enhanced provider visibility and messaging",
  ],
  private_owner_plus: [
    null,
    "Helper profile, document vault, QR stall cards",
    "Basic inventory and emergency mode",
  ],
  starter_barn: [
    null,
    "Feed, turnout, owner updates and billing",
    "Client owner portal accounts included",
  ],
  advanced_barn: [
    null,
    "Staff tasks, inventory, rehab and alerts",
    "Internal messaging and basic reports",
  ],
  elite_barn: [
    null,
    "Advanced reporting and permissions",
    "Contracts, signatures and branded portal",
  ],
  trainer_no_lesson: [
    null,
    "Training logs, plans and owner updates",
    "Ride calendar, documents and basic billing",
  ],
  trainer_lesson_15: [
    null,
    "Lesson scheduling, notes and packages",
    "Parent portal and lesson horse workload",
  ],
  trainer_lesson_50: [
    null,
    "Attendance, waivers and progress reports",
    "Lesson billing and revenue reports",
  ],
  enterprise: [
    "100+ horses and multi-location support",
    "Dedicated account manager and SSO options",
    "Custom onboarding, API access and migration",
  ],
  community_program: [
    "Nonprofit, education and rescue programs",
    "30-50% discount or custom quote",
    "Polished Community Program support",
  ],
};
const LANDING_POPULAR_BY_TIER = { advanced_barn: true };
const HIDDEN_LANDING_PRICING_TIERS = new Set([
  "starter",
  "professional",
]);

const CONTACT_SALES_MAILTO = "mailto:sales@equinesync.com?subject=EquineSync%20custom%20plan%20enquiry";
const LANDING_ROLE_SIGNUP_PATHS = {
  horse_owner: "/signup?enrollment=individual_horse_owner&role=horse_owner",
  barn_owner: "/signup?enrollment=barn_facility_owner&role=barn_owner",
  service_provider: "/signup?enrollment=service_provider&role=service_provider",
  trainer: "/signup?enrollment=trainer&role=trainer",
};

const buildLandingLimitBullet = (plan) => {
  const limits = plan.feature_limits || {};
  const parts = [];
  if (plan.tier_code === "service_provider_free") {
    return "Free service-provider signup";
  }
  if (plan.tier_code === "service_provider_premium") {
    return "$15/month premium provider subscription";
  }
  if (limits.horses != null) {
    parts.push(`Up to ${limits.horses} horse${limits.horses === 1 ? "" : "s"}`);
  }
  if (plan.tier_code === "free") {
    parts.push("1 invited owner profile");
  } else if (plan.tier_code === "individual_owner") {
    parts.push("1 owner profile");
  } else if (plan.tier_code === "private_owner_plus") {
    parts.push("1 additional profile");
  } else if (limits.users != null) {
    parts.push(`${limits.users} user${limits.users === 1 ? "" : "s"}`);
  }
  return parts.length ? parts.join(" · ") : null;
};

const signupPathForTier = (tierCode) => {
  const encodedTier = encodeURIComponent(tierCode || "");
  if ((tierCode || "").startsWith("service_provider")) {
    return `${LANDING_ROLE_SIGNUP_PATHS.service_provider}&tier=${encodedTier}`;
  }
  if ((tierCode || "").startsWith("trainer")) {
    return `${LANDING_ROLE_SIGNUP_PATHS.trainer}&tier=${encodedTier}`;
  }
  if ((tierCode || "").includes("barn")) {
    return `${LANDING_ROLE_SIGNUP_PATHS.barn_owner}&tier=${encodedTier}`;
  }
  if (tierCode === "individual_owner" || tierCode === "private_owner_plus") {
    return `${LANDING_ROLE_SIGNUP_PATHS.horse_owner}&tier=${encodedTier}`;
  }
  return "/enroll";
};

export default function Landing() {
  const navigate = useNavigate();
  const { user, loading } = useAuth();
  const [billingCycle, setBillingCycle] = useState("monthly");
  // Phase 15.G round-2: track loading + error states. Static prices are
  // no longer used as a fallback — if the public catalog is unreachable
  // we show a graceful unavailable state with a Contact-Sales CTA.
  const [livePlans, setLivePlans] = useState(null);
  const [plansError, setPlansError] = useState(false);

  useEffect(() => {
    if (user && !loading) navigate("/dashboard", { replace: true });
  }, [user, loading, navigate]);

  // Fetch the unauthenticated public plan catalog.
  useEffect(() => {
    let cancelled = false;
    api.get("/billing/plans-public")
      .then((r) => {
        if (cancelled) return;
        const sorted = sortPlans(Array.isArray(r.data) ? r.data : []).filter(
          (plan) => !HIDDEN_LANDING_PRICING_TIERS.has(plan.tier_code)
        );
        if (sorted.length === 0) {
          setPlansError(true);
          setLivePlans([]);
          return;
        }
        setLivePlans(sorted);
        setPlansError(false);
      })
      .catch(() => {
        if (cancelled) return;
        setLivePlans([]);
        setPlansError(true);
      });
    return () => { cancelled = true; };
  }, []);

  const plansForCycle = useMemo(() => {
    // Source of truth: the public catalog. We do NOT fall back to static
    // prices — see plansError empty state below. The static map only
    // contributes marketing bullets keyed by tier_code; bullet 1 is
    // derived live from `feature_limits` when present.
    if (!livePlans) return [];
    return livePlans.map((p) => {
      const fallbackBullets = (LANDING_BULLETS_BY_TIER[p.tier_code] || []).slice();
      const baseBullets = fallbackBullets.slice();
      const limitsBullet = buildLandingLimitBullet(p);
      if (limitsBullet) baseBullets[0] = limitsBullet;
      // Drop any placeholder slots that didn't get filled.
      const bullets = baseBullets.filter(Boolean);
      return {
        ...p,
        description:
          p.tier_code === "private_owner_plus"
            ? "Includes everything in Individual Horse Owner, plus one additional profile and private-owner tools for multi-horse setups."
            : p.description,
        bullets,
        popular: !!LANDING_POPULAR_BY_TIER[p.tier_code],
        _savings: annualSavingsPct(p),
      };
    });
  }, [livePlans]);

  const goToEnrollment = (roleId) => {
    navigate(roleId ? LANDING_ROLE_SIGNUP_PATHS[roleId] || "/enroll" : "/enroll");
  };

  return (
    <div className="min-h-screen w-full bg-equine-navyDeep text-white font-sans" data-testid="landing-page">
      {/* Top nav */}
      <header className="px-6 md:px-12 py-6 flex items-center justify-between max-w-7xl mx-auto">
        <Logo onNavy size={60} wordmarkSize={28} taglineSize={9.5} />
        <nav className="flex items-center gap-6">
          <a
            href="#pricing"
            className="hidden sm:inline text-[13px] tracking-wide text-white/70 hover:text-white transition-colors"
            data-testid="nav-pricing"
          >
            Pricing
          </a>
          <Link
            to="/login"
            className="text-[13px] tracking-wide text-white/70 hover:text-white transition-colors"
            data-testid="nav-signin"
          >
            Sign in
          </Link>
          <button
            onClick={() => goToEnrollment()}
            className="bg-equine-lavenderSoft text-equine-navyDeep hover:bg-white transition-colors px-5 py-2 text-[13px] tracking-wide font-medium rounded-full"
            data-testid="nav-join-cta"
          >
            Join EquineSync
          </button>
        </nav>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden min-h-[75vh] flex flex-col justify-center">
        <img
          src="https://images.unsplash.com/photo-1550785330-003a9afa3bd9?auto=format&fit=crop&w=2400&q=85"
          alt="Equestrian"
          className="absolute inset-0 w-full h-full object-cover opacity-45"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-equine-navyDeep/90 via-equine-navy/68 to-equine-navyDeep/92" />
        <div className="relative max-w-7xl mx-auto px-6 md:px-12 py-20 md:py-28">
          <div className="max-w-3xl">
            <div className="text-[11px] tracking-[0.28em] uppercase text-equine-lavenderSoft font-medium mb-6">
              The equestrian operating network
            </div>
            <h1 className="font-display text-5xl md:text-7xl font-light leading-[1.04] text-white">
              Every horse.<br />Every task.<br />
              <span className="text-equine-lavenderSoft">In sync.</span>
            </h1>
            <p className="mt-8 text-lg md:text-xl text-white/75 leading-relaxed max-w-2xl">
              EquineSync connects owners, barns, trainers, and service providers in one quietly
              powerful platform. Rider, guardian, and staff accounts remain invitation-based.
            </p>
            <div className="mt-10 flex flex-wrap items-center gap-4">
              <button
                onClick={() => goToEnrollment()}
                className="group bg-white text-equine-navyDeep hover:bg-equine-lavenderSoft transition-all px-8 py-4 text-[14px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                data-testid="hero-join-cta"
              >
                Join EquineSync
                <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </button>
              <Link
                to="/login"
                className="text-[14px] tracking-wide text-white/80 hover:text-white transition-colors px-6 py-4"
                data-testid="hero-signin-link"
              >
                Already a member? Sign in →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Trust strip */}
      <section className="border-y border-white/10 bg-equine-navy/40">
        <div className="max-w-7xl mx-auto px-6 md:px-12 py-8 flex flex-wrap justify-around md:justify-between gap-6">
          {TRUST.map((t, idx) => (
            <div key={idx} className="flex items-center gap-3 text-[13px] tracking-wide text-white/70">
              <t.Icon className="w-4 h-4 text-equine-lavenderSoft" strokeWidth={1.5} />
              <span>{t.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Role bento grid */}
      <section className="max-w-7xl mx-auto px-6 md:px-12 py-24">
        <div className="mb-14 max-w-2xl">
          <div className="text-[11px] tracking-[0.28em] uppercase text-equine-lavenderSoft font-medium mb-4">
            Join as
          </div>
          <h2 className="font-display text-4xl md:text-5xl font-light text-white">
            Four public paths. Invitation-only barn roles.
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-6 gap-5 md:gap-6">
          {ROLE_CARDS.map((card) => (
            <button
              key={card.id}
              onClick={() => goToEnrollment(card.id)}
              className={`group relative overflow-hidden text-left ${card.span} col-span-1 bg-equine-navy/60 hover:bg-equine-navy border border-white/5 hover:border-equine-lavenderSoft/40 transition-all duration-500 rounded-2xl min-h-[280px] flex flex-col justify-end p-6 md:p-7`}
              data-testid={`role-card-${card.id}`}
            >
              <img
                src={card.image}
                alt={card.label}
                className="absolute inset-0 w-full h-full object-cover opacity-30 group-hover:opacity-45 group-hover:scale-105 transition-all duration-700"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-equine-navyDeep via-equine-navyDeep/40 to-transparent" />
              <div className="relative">
                <div className="font-display text-2xl md:text-3xl text-white group-hover:text-equine-lavenderSoft transition-colors">
                  {card.label}
                </div>
                <div className="mt-2 text-[13.5px] text-white/65 leading-relaxed max-w-xs">{card.blurb}</div>
                <div className="mt-5 inline-flex items-center gap-1.5 text-[12px] tracking-wide text-white/80 group-hover:text-equine-lavenderSoft transition-colors">
                  Join as {card.label} <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* Pricing band */}
      <section id="pricing" className="border-t border-white/10 bg-equine-navy/30">
        <div className="max-w-7xl mx-auto px-6 md:px-12 py-24">
          <div className="mb-10 flex flex-wrap items-end justify-between gap-6">
            <div className="max-w-2xl">
              <div className="text-[11px] tracking-[0.28em] uppercase text-equine-lavenderSoft font-medium mb-4">
                Membership
              </div>
              <h2 className="font-display text-4xl md:text-5xl font-light text-white">
                Pricing that respects your time.
              </h2>
              <p className="mt-4 text-white/65 text-[15px] leading-relaxed">
                Start free as an invited owner or service provider. Upgrade when you need more. Paid plans include a
                <span className="text-equine-lavenderSoft font-medium"> 14-day free trial</span>. Cancel anytime.
              </p>
            </div>
            {/* Monthly / Annual toggle */}
            <div
              className="inline-flex bg-white/5 border border-white/10 rounded-full p-0.5"
              data-testid="landing-cycle-toggle"
              role="tablist"
              aria-label="Billing cycle"
            >
              {["monthly", "annual"].map((c) => (
                <button
                  key={c}
                  type="button"
                  onClick={() => setBillingCycle(c)}
                  data-testid={`landing-cycle-${c}`}
                  className={`px-4 py-2 text-[12px] tracking-wide uppercase rounded-full transition-colors ${
                    billingCycle === c
                      ? "bg-equine-lavenderSoft text-equine-navyDeep"
                      : "text-white/65 hover:text-white"
                  }`}
                >
                  {c}
                </button>
              ))}
            </div>
          </div>

          {/* Loading state (livePlans === null) → Skeleton */}
          {livePlans === null && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" data-testid="pricing-loading">
              {[0, 1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="bg-equine-navy/40 border border-white/5 rounded-2xl p-8 min-h-[420px] animate-pulse"
                />
              ))}
            </div>
          )}

          {/* Error / empty catalog state — graceful unavailable; no static prices */}
          {plansError && livePlans !== null && plansForCycle.length === 0 && (
            <div
              className="bg-equine-navy/40 border border-equine-lavenderSoft/30 rounded-2xl p-10 text-center"
              data-testid="pricing-unavailable"
            >
              <div className="text-[11px] tracking-[0.28em] uppercase text-equine-lavenderSoft/80 font-medium mb-3">
                Membership
              </div>
              <h3 className="font-display text-3xl text-white font-light">
                Pricing is temporarily unavailable.
              </h3>
              <p className="mt-3 text-white/65 text-[14px] max-w-md mx-auto">
                We&apos;re refreshing the public catalog. Reach out and our team will walk
                you through the right plan in minutes.
              </p>
              <a
                href={CONTACT_SALES_MAILTO}
                className="mt-6 inline-flex items-center gap-2 bg-equine-lavenderSoft text-equine-navyDeep hover:bg-white transition-colors px-6 py-3 text-[13px] tracking-wide font-medium rounded-full"
                data-testid="pricing-contact-sales-cta"
              >
                Contact sales <ArrowRight className="w-3.5 h-3.5" />
              </a>
            </div>
          )}

          {/* Loaded catalog — render cards from the public endpoint only */}
          {plansForCycle.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" data-testid="pricing-grid">
            {plansForCycle.map((tier) => {
              const popular = !!tier.popular;
              const contactSales = !!tier.contact_sales;
              const priceCents =
                billingCycle === "annual" && tier.annual_price_cents != null
                  ? tier.annual_price_cents
                  : tier.monthly_price_cents;
              const isFree = priceCents === 0;
              const cycleLabel = billingCycle === "annual" ? "/ yr" : "/ mo";

              return (
                <div
                  key={tier.tier_code}
                  className={`relative bg-equine-navy/60 border ${
                    popular ? "border-equine-lavenderSoft/50 shadow-[0_0_60px_-20px_rgba(199,182,217,0.4)]" : "border-white/5"
                  } rounded-2xl p-8 flex flex-col`}
                  data-testid={`pricing-card-${tier.tier_code}`}
                >
                  {popular && (
                    <span className="absolute top-5 right-5 text-[10px] tracking-[0.2em] uppercase text-equine-lavenderSoft bg-equine-lavenderSoft/10 border border-equine-lavenderSoft/30 px-2.5 py-1 rounded-full">
                      Most popular
                    </span>
                  )}
                  <div className="text-[11px] tracking-[0.28em] uppercase text-equine-lavenderSoft/80 font-medium mb-3">
                    {tier.name}
                  </div>

                  {contactSales ? (
                    <div className="font-display text-4xl text-white font-light">
                      Let&apos;s talk
                    </div>
                  ) : (
                    <div className="font-display text-5xl text-white font-light">
                      {formatCents(priceCents)}
                      <span className="text-[14px] text-white/50 font-sans tracking-wide ml-2">{cycleLabel}</span>
                    </div>
                  )}

                  {billingCycle === "annual" && tier._savings != null && (
                    <div
                      className="mt-2 text-[11px] tracking-[0.2em] uppercase text-equine-lavenderSoft"
                      data-testid={`pricing-savings-${tier.tier_code}`}
                    >
                      Save {tier._savings}% vs. monthly
                    </div>
                  )}

                  <p className="mt-4 text-[13.5px] text-white/65 leading-relaxed">{tier.description}</p>

                  <ul className="mt-6 space-y-2.5 text-[13px] text-white/70 flex-1">
                    {(tier.bullets || []).map((b) => (
                      <li key={b} className="flex items-start gap-2">
                        <Check className="w-3.5 h-3.5 mt-0.5 text-equine-lavenderSoft flex-shrink-0" />
                        <span>{b}</span>
                      </li>
                    ))}
                  </ul>

                  {contactSales ? (
                    <a
                      href={CONTACT_SALES_MAILTO}
                      className="mt-8 w-full text-center bg-white/5 text-white hover:bg-white/10 border border-white/10 transition-colors py-3 text-[13px] tracking-wide font-medium rounded-full inline-flex items-center justify-center gap-1.5"
                      data-testid={`pricing-cta-${tier.tier_code}`}
                    >
                      Contact sales <ArrowRight className="w-3.5 h-3.5" />
                    </a>
                  ) : (
                    <button
                      onClick={() => navigate(signupPathForTier(tier.tier_code))}
                      className={`mt-8 w-full ${
                        popular
                          ? "bg-equine-lavenderSoft text-equine-navyDeep hover:bg-white"
                          : "bg-white/5 text-white hover:bg-white/10 border border-white/10"
                      } transition-colors py-3 text-[13px] tracking-wide font-medium rounded-full`}
                      data-testid={`pricing-cta-${tier.tier_code}`}
                    >
                      {isFree ? "Start free" : `Start ${tier.name}`}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-10 px-6 md:px-12">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-[12px] tracking-wide text-white/40">
          <div>© EquineSync · Built by horse owners and equestrians for the people and facilities who care for horses</div>
          <div className="flex gap-6">
            <Link to="/login" className="hover:text-white transition-colors" data-testid="footer-signin">Sign in</Link>
            <button onClick={() => goToEnrollment()} className="hover:text-white transition-colors" data-testid="footer-join">Join</button>
          </div>
        </div>
      </footer>
    </div>
  );
}
