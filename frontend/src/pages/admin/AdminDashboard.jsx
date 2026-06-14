import React, { useEffect, useState } from "react";
import { api } from "../../lib/api";
import { getPlatformRole } from "../../lib/permissions";
import { useAuth } from "../../context/AuthContext";
import AdminKpiCards from "./AdminKpiCards";
import AdminSubscriptionHealth from "./AdminSubscriptionHealth";
import AdminActivityFeed from "./AdminActivityFeed";

/**
 * Admin-2 — read-only platform dashboard.
 *
 * Three parallel reads on mount: /portal/kpis, /portal/subscription-health,
 * /portal/activity?limit=25. Each surface owns its own loading + error
 * state so a stale activity feed doesn't blank the KPI row.
 *
 * Per the founder gate: ZERO mutation buttons on this page. The
 * Stripe-customer link and other safe affordances land in Admin-5 (and
 * only after a separate gated plan).
 */
export default function AdminDashboard() {
  const { user } = useAuth();
  const [me, setMe] = useState(null);
  const [meErr, setMeErr] = useState(null);

  const [kpis, setKpis] = useState(null);
  const [kpiLoading, setKpiLoading] = useState(true);
  const [kpiErr, setKpiErr] = useState(null);

  const [subHealth, setSubHealth] = useState(null);
  const [subLoading, setSubLoading] = useState(true);
  const [subErr, setSubErr] = useState(null);

  const [activity, setActivity] = useState(null);
  const [actLoading, setActLoading] = useState(true);
  const [actErr, setActErr] = useState(null);

  useEffect(() => {
    let cancelled = false;
    api.get("/admin/portal/me")
      .then((r) => { if (!cancelled) setMe(r.data); })
      .catch((e) => { if (!cancelled) setMeErr(e?.response?.data?.detail || "Failed to load admin context."); });
    api.get("/admin/portal/kpis")
      .then((r) => { if (!cancelled) setKpis(r.data); })
      .catch(() => { if (!cancelled) setKpiErr(true); })
      .finally(() => { if (!cancelled) setKpiLoading(false); });
    api.get("/admin/portal/subscription-health")
      .then((r) => { if (!cancelled) setSubHealth(r.data); })
      .catch(() => { if (!cancelled) setSubErr(true); })
      .finally(() => { if (!cancelled) setSubLoading(false); });
    api.get("/admin/portal/activity?limit=25")
      .then((r) => { if (!cancelled) setActivity(r.data); })
      .catch(() => { if (!cancelled) setActErr(true); })
      .finally(() => { if (!cancelled) setActLoading(false); });
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
          Numbers update every 30 seconds; the dashboard is intentionally read-only.
        </p>
      </div>

      {meErr && (
        <div
          className="mb-6 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
          data-testid="admin-dashboard-error"
        >
          {meErr}
        </div>
      )}

      <AdminKpiCards kpis={kpis} loading={kpiLoading} error={kpiErr} />

      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AdminSubscriptionHealth data={subHealth} loading={subLoading} error={subErr} />
        <AdminActivityFeed items={activity?.items} loading={actLoading} error={actErr} />
      </div>

      {/* Access summary — useful for QA + reviewers, harmless */}
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
