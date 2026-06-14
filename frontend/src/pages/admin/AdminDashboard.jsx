import React, { useEffect, useState } from "react";
import { api } from "../../lib/api";
import { getPlatformRole } from "../../lib/permissions";
import { useAuth } from "../../context/AuthContext";

const KPI_PLACEHOLDERS = [
  { key: "users",         label: "Total users",            phase: "Admin-2" },
  { key: "facilities",    label: "Facilities",             phase: "Admin-2" },
  { key: "horses",        label: "Horses on record",       phase: "Admin-2" },
  { key: "active_subs",   label: "Active subscriptions",   phase: "Admin-2" },
  { key: "trialing",      label: "Trialing subscriptions", phase: "Admin-2" },
  { key: "past_due",      label: "Past-due subscriptions", phase: "Admin-2" },
  { key: "approvals",     label: "Pending approvals",      phase: "Admin-2" },
  { key: "mrr",           label: "Monthly recurring revenue", phase: "Admin-2" },
];

/**
 * Admin-1 — Dashboard placeholder.
 *
 * Per founder direction this surface is intentionally read-only and
 * dataless in Admin-1. The KPI cards render with em-dash placeholders +
 * a "Wires up in Admin-2" hint so reviewers can confirm the layout
 * without us inventing fake production metrics.
 *
 * The /api/admin/portal/me call here is the live access check (the
 * Layout guard is the structural one; this is the data-layer one). It
 * also surfaces the section list the current platform_role can see —
 * useful telemetry for the testing agent.
 */
export default function AdminDashboard() {
  const { user } = useAuth();
  const [me, setMe] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    let cancelled = false;
    api.get("/admin/portal/me")
      .then((r) => { if (!cancelled) setMe(r.data); })
      .catch((e) => {
        if (cancelled) return;
        setErr(e?.response?.data?.detail || "Failed to load admin context.");
      });
    return () => { cancelled = true; };
  }, []);

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-dashboard">
      <div className="mb-8">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal · Dashboard
        </div>
        <h1 className="font-display text-3xl md:text-4xl font-light text-equinesync-graphite mt-2">
          Welcome back{user?.full_name ? `, ${user.full_name.split(" ")[0]}` : ""}.
        </h1>
        <p className="mt-2 text-[14px] text-equinesync-graphite/65 max-w-2xl">
          You&apos;re signed into the Equine·Sync platform control center as
          <span className="text-equinesync-slate font-medium"> {getPlatformRole(user) || "—"}</span>.
          Live operational data lands in Admin-2; this Admin-1 build wires the
          access boundary and the shell only.
        </p>
      </div>

      {err && (
        <div
          className="mb-6 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
          data-testid="admin-dashboard-error"
        >
          {err}
        </div>
      )}

      {/* KPI grid — placeholders only */}
      <div
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
        data-testid="admin-kpi-grid"
      >
        {KPI_PLACEHOLDERS.map(({ key, label, phase }) => (
          <div
            key={key}
            data-testid={`admin-kpi-${key}`}
            className="rounded-xl border border-equinesync-graphite/10 bg-white p-5"
          >
            <div className="text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/50">
              {label}
            </div>
            <div className="mt-3 font-display text-3xl font-light text-equinesync-graphite/30">
              —
            </div>
            <div className="mt-2 text-[10.5px] tracking-wide uppercase text-equinesync-lilac/80">
              Wires up in {phase}
            </div>
          </div>
        ))}
      </div>

      {/* Access summary — useful for QA + reviewers, harmless to surface */}
      <div
        className="mt-8 rounded-xl border border-equinesync-graphite/10 bg-white p-5"
        data-testid="admin-access-summary"
      >
        <div className="text-[11px] tracking-[0.22em] uppercase text-equinesync-graphite/55 font-medium">
          Access summary
        </div>
        <div className="mt-3 text-[13px] text-equinesync-graphite/75">
          {me ? (
            <>
              <span className="text-equinesync-graphite">Platform role:</span>{" "}
              <span className="text-equinesync-slate font-medium">{me.platform_role}</span>
              <div className="mt-2 flex flex-wrap gap-1.5" data-testid="admin-section-chips">
                {(me.sections || []).map((s) => (
                  <span
                    key={s}
                    className="px-2 py-0.5 rounded-full text-[10.5px] tracking-wide uppercase bg-equinesync-lilac/15 text-equinesync-graphite/70"
                  >
                    {s.replace(/_/g, " ")}
                  </span>
                ))}
              </div>
            </>
          ) : (
            <span className="text-equinesync-graphite/40">Loading…</span>
          )}
        </div>
      </div>
    </div>
  );
}
