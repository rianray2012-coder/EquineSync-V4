import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Logo } from "../components/Logo";
import { Check, ArrowRight, ShieldCheck, Sparkles, Users, Calendar } from "lucide-react";
import { annualSavingsPct, formatCents } from "../lib/subscriptionBilling";

const ROLE_CARDS = [
  {
    id: "horse_owner",
    label: "Horse Owner",
    blurb: "Track your horse's care, billing and progress in one calm place.",
    image:
      "https://images.unsplash.com/photo-1600715151005-e6d44b9ef840?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTN8MHwxfHNlYXJjaHwzfHxsdXh1cnklMjBlcXVlc3RyaWFuJTIwaG9yc2UlMjByaWRlcnxlbnwwfHx8fDE3ODEzNDE1NDl8MA&ixlib=rb-4.1.0&q=85",
    span: "md:col-span-3",
  },
  {
    id: "rider",
    label: "Rider",
    blurb: "Log sessions, follow your training plan, and stay in sync with your trainer.",
    image:
      "https://images.unsplash.com/photo-1550785330-003a9afa3bd9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTN8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBlcXVlc3RyaWFuJTIwaG9yc2UlMjByaWRlcnxlbnwwfHx8fDE3ODEzNDE1NDl8MA&ixlib=rb-4.1.0&q=85",
    span: "md:col-span-3",
  },
  {
    id: "trainer",
    label: "Trainer",
    blurb: "Manage clients, sessions, and progress notes — verified by the Equine Sync team.",
    image:
      "https://images.unsplash.com/photo-1594768816441-1dd241ffaa67?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxOTB8MHwxfHNlYXJjaHwxfHxlcXVlc3RyaWFuJTIwdHJhaW5lcnxlbnwwfHx8fDE3ODEzNDE1NDl8MA&ixlib=rb-4.1.0&q=85",
    span: "md:col-span-2",
    pending: true,
  },
  {
    id: "barn_owner",
    label: "Barn / Facility",
    blurb: "Run a full operation — stalls, staff, owners, billing — under one roof.",
    image:
      "https://images.unsplash.com/photo-1576692192914-9abed71b3ef9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODF8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBob3JzZSUyMGJhcm58ZW58MHx8fHwxNzgxMzQxNTQ5fDA&ixlib=rb-4.1.0&q=85",
    span: "md:col-span-2",
    pending: true,
  },
  {
    id: "service_provider",
    label: "Service Provider",
    blurb: "Vets, farriers, body workers — connect with barns that need your expertise.",
    image:
      "https://images.unsplash.com/photo-1649127616601-6f0a3ea26eae?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwxfHxlcXVlc3RyaWFuJTIwZmFycmllcnxlbnwwfHx8fDE3ODEzNDE1NjF8MA&ixlib=rb-4.1.0&q=85",
    span: "md:col-span-2",
    pending: true,
  },
];

const TRUST = [
  { Icon: ShieldCheck, label: "Verified equestrian network" },
  { Icon: Calendar, label: "Skip & complete your profile later" },
  { Icon: Users, label: "5 role types, one connected platform" },
  { Icon: Sparkles, label: "Cancel anytime" },
];

// Phase 15.C — landing-page pricing band. The authoritative source is the
// seeded `plans` collection (see backend/scripts/seed_plans.py and the public
// catalog at GET /api/billing/plans). That endpoint requires auth, so this
// static mirror is what unauthenticated visitors see. Keep these values in
// lockstep with the seed; tweak both together. Numbers use the same shape
// (`monthly_price_cents`, `annual_price_cents`, `feature_limits`) so the
// rendering helpers (formatCents, annualSavingsPct) just work.
const LANDING_PLANS = [
  {
    tier_code: "free",
    name: "Free",
    description: "Solo riders, owners and small-stable getting started.",
    monthly_price_cents: 0,
    annual_price_cents: null,
    feature_limits: { horses: 3, users: 1 },
    bullets: [
      "Personal horse profile + journal",
      "Network directory presence",
      "Messaging with verified pros",
    ],
  },
  {
    tier_code: "starter",
    name: "Starter",
    description: "Small barns running day-to-day operations.",
    monthly_price_cents: 4900,
    annual_price_cents: 49980,
    feature_limits: { horses: 25, users: 5 },
    bullets: [
      "Up to 25 horses · 5 staff users",
      "Daily care, feed & medication tracking",
      "Boarder invoices & owner portal",
    ],
  },
  {
    tier_code: "professional",
    name: "Professional",
    description: "Growing facilities with training and lesson programs.",
    monthly_price_cents: 14900,
    annual_price_cents: 151980,
    feature_limits: { horses: 100, users: 25 },
    popular: true,
    bullets: [
      "Up to 100 horses · 25 staff users",
      "Training plans, GPS, advanced reporting",
      "Recurring billing + boarder messaging",
    ],
  },
  {
    tier_code: "enterprise",
    name: "Enterprise",
    description: "Multi-location facilities with custom needs.",
    contact_sales: true,
    feature_limits: { horses: null, users: null },
    bullets: [
      "Unlimited horses & staff users",
      "Dedicated support · SSO · custom integrations",
      "Volume pricing & on-prem options",
    ],
  },
];

const CONTACT_SALES_MAILTO = "mailto:sales@equinesync.com?subject=Enterprise%20plan%20enquiry";

export default function Landing() {
  const navigate = useNavigate();
  const { user, loading } = useAuth();
  const [billingCycle, setBillingCycle] = useState("monthly");

  useEffect(() => {
    if (user && !loading) navigate("/dashboard", { replace: true });
  }, [user, loading, navigate]);

  const plansForCycle = useMemo(
    () => LANDING_PLANS.map((p) => ({ ...p, _savings: annualSavingsPct(p) })),
    [],
  );

  const goToSignup = (roleId) => {
    const query = roleId ? `?role=${roleId}` : "";
    navigate(`/signup${query}`);
  };

  return (
    <div className="min-h-screen w-full bg-equine-navyDeep text-white font-sans" data-testid="landing-page">
      {/* Top nav */}
      <header className="px-6 md:px-12 py-6 flex items-center justify-between max-w-7xl mx-auto">
        <Logo onNavy />
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
            onClick={() => goToSignup()}
            className="bg-equine-saddle text-equine-navyDeep hover:bg-white transition-colors px-5 py-2 text-[13px] tracking-wide font-medium rounded-full"
            data-testid="nav-join-cta"
          >
            Join Equine Sync
          </button>
        </nav>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden min-h-[75vh] flex flex-col justify-center">
        <img
          src="https://images.unsplash.com/photo-1550785330-003a9afa3bd9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTN8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBlcXVlc3RyaWFuJTIwaG9yc2UlMjByaWRlcnxlbnwwfHx8fDE3ODEzNDE1NDl8MA&ixlib=rb-4.1.0&q=85"
          alt="Equestrian"
          className="absolute inset-0 w-full h-full object-cover opacity-25"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-equine-navyDeep via-equine-navy/85 to-equine-navyDeep" />
        <div className="relative max-w-7xl mx-auto px-6 md:px-12 py-20 md:py-28">
          <div className="max-w-3xl">
            <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle font-medium mb-6">
              The equestrian operating network
            </div>
            <h1 className="font-display text-5xl md:text-7xl font-light leading-[1.04] text-white">
              Every horse.<br />Every task.<br />
              <span className="text-equine-saddle">In sync.</span>
            </h1>
            <p className="mt-8 text-lg md:text-xl text-white/75 leading-relaxed max-w-2xl">
              Equine Sync connects riders, owners, trainers, barns and service providers in one
              quietly powerful platform. Build your profile, find the right people, and choose
              the tier that fits.
            </p>
            <div className="mt-10 flex flex-wrap items-center gap-4">
              <button
                onClick={() => goToSignup()}
                className="group bg-white text-equine-navyDeep hover:bg-equine-saddle transition-all px-8 py-4 text-[14px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                data-testid="hero-join-cta"
              >
                Join Equine Sync
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
              <t.Icon className="w-4 h-4 text-equine-saddle" strokeWidth={1.5} />
              <span>{t.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Role bento grid */}
      <section className="max-w-7xl mx-auto px-6 md:px-12 py-24">
        <div className="mb-14 max-w-2xl">
          <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle font-medium mb-4">
            Join as
          </div>
          <h2 className="font-display text-4xl md:text-5xl font-light text-white">
            Five roles. One quietly connected network.
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-6 gap-5 md:gap-6">
          {ROLE_CARDS.map((card) => (
            <button
              key={card.id}
              onClick={() => goToSignup(card.id)}
              className={`group relative overflow-hidden text-left ${card.span} col-span-1 bg-equine-navy/60 hover:bg-equine-navy border border-white/5 hover:border-equine-saddle/40 transition-all duration-500 rounded-2xl min-h-[280px] flex flex-col justify-end p-6 md:p-7`}
              data-testid={`role-card-${card.id}`}
            >
              <img
                src={card.image}
                alt={card.label}
                className="absolute inset-0 w-full h-full object-cover opacity-30 group-hover:opacity-45 group-hover:scale-105 transition-all duration-700"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-equine-navyDeep via-equine-navyDeep/40 to-transparent" />
              <div className="relative">
                {card.pending && (
                  <span className="inline-block text-[10px] tracking-[0.2em] uppercase text-equine-saddle bg-equine-saddle/10 border border-equine-saddle/30 px-2.5 py-1 rounded-full mb-3">
                    Verification required
                  </span>
                )}
                <div className="font-display text-2xl md:text-3xl text-white group-hover:text-equine-saddle transition-colors">
                  {card.label}
                </div>
                <div className="mt-2 text-[13.5px] text-white/65 leading-relaxed max-w-xs">{card.blurb}</div>
                <div className="mt-5 inline-flex items-center gap-1.5 text-[12px] tracking-wide text-white/80 group-hover:text-equine-saddle transition-colors">
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
              <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle font-medium mb-4">
                Membership
              </div>
              <h2 className="font-display text-4xl md:text-5xl font-light text-white">
                Pricing that respects your time.
              </h2>
              <p className="mt-4 text-white/65 text-[15px] leading-relaxed">
                Start free. Upgrade to a facility plan when you need it. Paid plans include a
                <span className="text-equine-saddle font-medium"> 14-day free trial</span>. Cancel anytime.
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
                      ? "bg-equine-saddle text-equine-navyDeep"
                      : "text-white/65 hover:text-white"
                  }`}
                >
                  {c}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {plansForCycle.map((tier) => {
              const popular = !!tier.popular;
              const contactSales = !!tier.contact_sales;
              const isFree = tier.tier_code === "free";
              const priceCents =
                billingCycle === "annual" && tier.annual_price_cents != null
                  ? tier.annual_price_cents
                  : tier.monthly_price_cents;
              const cycleLabel = billingCycle === "annual" ? "/ yr" : "/ mo";

              return (
                <div
                  key={tier.tier_code}
                  className={`relative bg-equine-navy/60 border ${
                    popular ? "border-equine-saddle/50 shadow-[0_0_60px_-20px_rgba(199,182,217,0.4)]" : "border-white/5"
                  } rounded-2xl p-8 flex flex-col`}
                  data-testid={`pricing-card-${tier.tier_code}`}
                >
                  {popular && (
                    <span className="absolute top-5 right-5 text-[10px] tracking-[0.2em] uppercase text-equine-saddle bg-equine-saddle/10 border border-equine-saddle/30 px-2.5 py-1 rounded-full">
                      Most popular
                    </span>
                  )}
                  <div className="text-[11px] tracking-[0.28em] uppercase text-equine-saddle/80 font-medium mb-3">
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
                      className="mt-2 text-[11px] tracking-[0.2em] uppercase text-equine-saddle"
                      data-testid={`pricing-savings-${tier.tier_code}`}
                    >
                      Save {tier._savings}% vs. monthly
                    </div>
                  )}

                  <p className="mt-4 text-[13.5px] text-white/65 leading-relaxed">{tier.description}</p>

                  <ul className="mt-6 space-y-2.5 text-[13px] text-white/70 flex-1">
                    {(tier.bullets || []).map((b) => (
                      <li key={b} className="flex items-start gap-2">
                        <Check className="w-3.5 h-3.5 mt-0.5 text-equine-saddle flex-shrink-0" />
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
                      onClick={() => goToSignup()}
                      className={`mt-8 w-full ${
                        popular
                          ? "bg-equine-saddle text-equine-navyDeep hover:bg-white"
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
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-10 px-6 md:px-12">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-[12px] tracking-wide text-white/40">
          <div>© Equine Sync · Crafted for the equestrian world</div>
          <div className="flex gap-6">
            <Link to="/login" className="hover:text-white transition-colors" data-testid="footer-signin">Sign in</Link>
            <button onClick={() => goToSignup()} className="hover:text-white transition-colors" data-testid="footer-join">Join</button>
          </div>
        </div>
      </footer>
    </div>
  );
}
