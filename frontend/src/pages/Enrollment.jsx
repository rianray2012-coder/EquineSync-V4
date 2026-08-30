import React from "react";
import { Link, useSearchParams } from "react-router-dom";
import { ArrowRight, Building2, HeartHandshake, ShieldCheck, Stethoscope, UserRound } from "lucide-react";
import { Logo } from "../components/Logo";
import { ENROLLMENT_PATHS, LEASEE_INVITE_RULE, LIMITED_INDIVIDUAL_OWNER_TRIAL } from "../lib/enrollmentPaths";

const ICONS = {
  individual_horse_owner: UserRound,
  barn_facility_owner: Building2,
  trainer: HeartHandshake,
  service_provider: Stethoscope,
};

export default function Enrollment() {
  const [params] = useSearchParams();
  const highlighted = params.get("path") || params.get("role");

  return (
    <div className="min-h-screen w-full bg-equine-navyDeep text-white font-sans" data-testid="enrollment-page">
      <header className="px-6 md:px-12 py-6 max-w-6xl mx-auto flex items-center justify-between">
        <Logo onNavy />
        <Link to="/login" className="text-[12px] tracking-wide text-white/60 hover:text-white" data-testid="enrollment-signin">
          Sign in
        </Link>
      </header>

      <main className="max-w-6xl mx-auto px-6 md:px-12 pb-20">
        <section className="pt-8 md:pt-14 pb-8">
          <div className="text-[11px] tracking-[0.28em] uppercase text-brand-lilac font-medium mb-4">
            Join EquineSync
          </div>
          <h1 className="font-display text-4xl md:text-6xl font-light leading-[1.05] text-white max-w-3xl">
            Choose the enrollment path that matches how you care for horses.
          </h1>
          <p className="mt-5 text-white/65 text-[15px] leading-relaxed max-w-2xl">
            Start with the path that fits your role. EquineSync will guide the right account setup,
            review steps, and workspace access from there.
          </p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 gap-4" aria-label="Enrollment paths">
          {ENROLLMENT_PATHS.map((path) => {
            const Icon = ICONS[path.id] || UserRound;
            const selected = highlighted === path.id || highlighted === path.role;
            return (
              <Link
                key={path.id}
                to={path.signupPath}
                className={`group rounded-2xl border p-5 md:p-6 bg-equine-navy/55 hover:bg-equine-navy transition-all ${
                  selected ? "border-brand-lilac/70" : "border-white/10 hover:border-brand-lilac/45"
                }`}
                data-testid={`enrollment-path-${path.id}`}
              >
                <div className="flex items-start gap-4">
                  <div className="w-11 h-11 rounded-xl border border-brand-lilac/30 bg-brand-lilac/10 flex items-center justify-center flex-shrink-0">
                    <Icon className="w-5 h-5 text-brand-lilac" strokeWidth={1.7} />
                  </div>
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-white group-hover:text-brand-lilac transition-colors">
                      {path.label}
                    </div>
                    <div className="mt-1 text-[12px] tracking-wide text-white/45">
                      {path.audience}
                    </div>
                  </div>
                </div>
                <p className="mt-5 text-[13.5px] text-white/65 leading-relaxed">{path.summary}</p>
                <div className="mt-5">
                  <div className="text-[10.5px] tracking-[0.24em] uppercase text-brand-lilac/85 mb-2">
                    Information needed
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {path.criticalData.map((item) => (
                      <span
                        key={item}
                        className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[11.5px] text-white/65"
                      >
                        {item}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="mt-6 flex items-center justify-between gap-3">
                  <span className="text-[12px] leading-relaxed text-white/45 max-w-md">
                    {path.availabilityNote}
                  </span>
                  <span className="inline-flex items-center gap-2 text-[13px] text-brand-lilac">
                    Continue <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                  </span>
                </div>
              </Link>
            );
          })}
        </section>

        <section
          className="mt-6 rounded-2xl border border-white/10 bg-equine-navy/40 p-5 md:p-6"
          data-testid="assisted-trial-guidance"
        >
          <div className="flex items-start gap-4">
            <div className="w-11 h-11 rounded-xl border border-brand-lilac/30 bg-brand-lilac/10 flex items-center justify-center flex-shrink-0">
              <ShieldCheck className="w-5 h-5 text-brand-lilac" strokeWidth={1.7} />
            </div>
            <div className="min-w-0 flex-1">
              <div className="font-display text-2xl text-white">
                Rider, Guardian, Or Staff?
              </div>
              <p className="mt-2 text-[13.5px] text-white/65 leading-relaxed max-w-3xl">
                Rider, guardian, and staff accounts remain invitation-based. These accounts normally come from a trainer, barn manager, barn owner, or boss invitation.
                Without an invite, you can start a limited seven-day individual-owner trial by providing
                contact information for your boarding facility, trainer, or equine provider.
              </p>
              <div className="mt-4 flex flex-wrap items-center gap-3">
                <Link
                  to={LIMITED_INDIVIDUAL_OWNER_TRIAL.signupPath}
                className="inline-flex items-center gap-2 rounded-full bg-white text-brand-graphite hover:bg-brand-lilac transition-colors px-5 py-2.5 text-[13px] tracking-wide font-medium"
                  data-testid="limited-owner-trial-link"
                >
                  Start limited trial <ArrowRight className="w-4 h-4" />
                </Link>
                <span className="text-[12px] text-white/45">
                  Limited access only; invite-based role access remains separate.
                </span>
              </div>
            </div>
          </div>
        </section>

        <section
          className="mt-4 rounded-2xl border border-white/10 bg-equine-navy/35 p-5 md:p-6"
          data-testid="leasee-invite-guidance"
        >
          <div className="text-[10.5px] tracking-[0.24em] uppercase text-brand-lilac/85 mb-2">
            Leasee access
          </div>
          <p className="text-[13.5px] text-white/65 leading-relaxed">
            {LEASEE_INVITE_RULE.summary} {LEASEE_INVITE_RULE.availabilityNote} Leasee access is not opened as a public enrollment path.
          </p>
        </section>
      </main>
    </div>
  );
}
