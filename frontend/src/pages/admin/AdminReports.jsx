/**
 * AdminReports — Admin-7B read-only Reports page.
 *
 * Pulls three aggregates from the backend (usage / subscriptions /
 * facilities), all gated server-side by platform_role. The CSV
 * download button is only rendered for platform roles that the
 * backend will accept (support_admin is read-only).
 *
 * No mutations. No raw Stripe IDs. No PHI.
 * Palette: Midnight Graphite / Slate Navy / Frost White / Smoky Lilac.
 */
import React, { useEffect, useMemo, useState } from "react";
import {
  BarChart3, Download, RefreshCcw, Users, Building2, CreditCard,
  AlertOctagon,
} from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import { canExportAdminReports } from "../../lib/permissions";
import { api, API, tokens } from "../../lib/api";

const WINDOWS = [
  { id: "7d", label: "Last 7 days" },
  { id: "30d", label: "Last 30 days" },
  { id: "90d", label: "Last 90 days" },
];

const CSV_TYPES = [
  { id: "users", label: "Users" },
  { id: "facilities", label: "Facilities" },
  { id: "subscriptions", label: "Subscriptions" },
  { id: "usage", label: "Usage" },
];

const Card = ({ title, children, testid }) => (
  <div
    data-testid={testid}
    className="rounded-2xl border border-equinesync-graphite/10 bg-white p-6"
  >
    <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
      {title}
    </div>
    <div className="mt-4">{children}</div>
  </div>
);

const Stat = ({ label, value, testid }) => (
  <div className="flex items-baseline justify-between py-2 border-b border-equinesync-graphite/5 last:border-0">
    <span className="text-[13px] text-equinesync-graphite/70">{label}</span>
    <span
      data-testid={testid}
      className="font-display text-xl text-equinesync-graphite tabular-nums"
    >
      {value ?? "—"}
    </span>
  </div>
);

const DistBar = ({ map }) => {
  const entries = Object.entries(map || {}).sort((a, b) => b[1] - a[1]);
  const total = entries.reduce((s, [, n]) => s + n, 0) || 1;
  return (
    <div className="space-y-2">
      {entries.length === 0 && (
        <div className="text-[12.5px] text-equinesync-graphite/50">No data.</div>
      )}
      {entries.map(([k, n]) => (
        <div key={k}>
          <div className="flex items-center justify-between text-[12px] text-equinesync-graphite/70">
            <span className="truncate">{k}</span>
            <span className="tabular-nums">{n}</span>
          </div>
          <div className="h-1.5 rounded-full bg-equinesync-frost overflow-hidden">
            <div
              className="h-full bg-equinesync-slate"
              style={{ width: `${Math.max(2, (n / total) * 100)}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
};

export default function AdminReports() {
  const { user } = useAuth();
  const [window, setWindow] = useState("30d");
  const [csvType, setCsvType] = useState("usage");
  const [usage, setUsage] = useState(null);
  const [subs, setSubs] = useState(null);
  const [facs, setFacs] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [reloadKey, setReloadKey] = useState(0);
  const [exporting, setExporting] = useState(false);
  const [exportErr, setExportErr] = useState(null);

  const canExport = useMemo(() => canExportAdminReports(user), [user]);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      api.get(`/admin/portal/reports/usage`, { params: { window } }),
      api.get(`/admin/portal/reports/subscriptions`, { params: { window } }),
      api.get(`/admin/portal/reports/facilities`, { params: { window } }),
    ])
      .then(([u, s, f]) => {
        if (cancelled) return;
        setUsage(u.data); setSubs(s.data); setFacs(f.data);
        setErr(null);
        setLoading(false);
      })
      .catch((e) => {
        if (cancelled) return;
        setErr(e?.response?.data?.detail || "Failed to load reports.");
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [window, reloadKey]);

  const downloadCsv = async () => {
    setExporting(true);
    setExportErr(null);
    try {
      const token = tokens.getAccess();
      const url = `${API}/admin/portal/reports/export.csv?type=${encodeURIComponent(csvType)}&window=${encodeURIComponent(window)}`;
      const resp = await fetch(url, {
        method: "GET",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!resp.ok) {
        let detail = `Export failed (${resp.status})`;
        try {
          const j = await resp.json();
          if (j?.detail) detail = j.detail;
        } catch { /* not JSON */ }
        throw new Error(detail);
      }
      const blob = await resp.blob();
      const dl = document.createElement("a");
      dl.href = URL.createObjectURL(blob);
      dl.download = `equinesync-${csvType}-${window}.csv`;
      document.body.appendChild(dl);
      dl.click();
      dl.remove();
    } catch (e) {
      setExportErr(e?.message || "Export failed.");
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-reports-page">
      <div className="mb-6 flex items-end justify-between flex-wrap gap-3">
        <div>
          <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
            Admin Portal · Reports
          </div>
          <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">
            Reports
          </h1>
          <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
            Usage, subscription, and facility aggregates over the selected
            window. Read-only; CSV export available to admin & auditor roles.
          </p>
        </div>
        <div className="flex items-center gap-2" data-testid="admin-reports-controls">
          <div role="tablist" className="inline-flex rounded-lg border border-equinesync-graphite/15 overflow-hidden">
            {WINDOWS.map((w) => (
              <button
                key={w.id}
                type="button"
                onClick={() => setWindow(w.id)}
                data-testid={`admin-reports-window-${w.id}`}
                className={`px-3 py-1.5 text-[12.5px] tracking-wide transition-colors ${
                  window === w.id
                    ? "bg-equinesync-slate text-equinesync-frost"
                    : "text-equinesync-graphite hover:bg-equinesync-frost"
                }`}
              >
                {w.label}
              </button>
            ))}
          </div>
          <button
            type="button"
            onClick={() => setReloadKey((k) => k + 1)}
            data-testid="admin-reports-refresh"
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 text-[12.5px] text-equinesync-graphite hover:bg-equinesync-frost"
          >
            <RefreshCcw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>
      </div>

      {err && (
        <div
          className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
          data-testid="admin-reports-error"
        >
          <span className="inline-flex items-center gap-2">
            <AlertOctagon className="w-3.5 h-3.5 text-equinesync-slate" /> {err}
          </span>
        </div>
      )}

      {loading ? (
        <div
          className="rounded-2xl border border-equinesync-graphite/10 bg-white p-10 text-center text-[13px] text-equinesync-graphite/55"
          data-testid="admin-reports-loading"
        >
          Loading aggregates…
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <Card title="Usage" testid="admin-reports-usage-card">
            <div className="flex items-center gap-2 mb-3">
              <BarChart3 className="w-4 h-4 text-equinesync-slate" />
              <span className="text-[12.5px] text-equinesync-graphite/70">
                Activity in window
              </span>
            </div>
            <Stat label="New users" value={usage?.new_users} testid="report-new-users" />
            <Stat label="New facilities" value={usage?.new_facilities} testid="report-new-facilities" />
            <Stat label="New horses" value={usage?.new_horses} testid="report-new-horses" />
            <Stat label="Audit events" value={usage?.audit_events} testid="report-audit-events" />
            <Stat label="Denied events" value={usage?.denied_events} testid="report-denied-events" />
            <Stat label="New support tickets" value={usage?.new_support_tickets} testid="report-new-tickets" />
          </Card>

          <Card title="Subscriptions" testid="admin-reports-subs-card">
            <div className="flex items-center gap-2 mb-3">
              <CreditCard className="w-4 h-4 text-equinesync-slate" />
              <span className="text-[12.5px] text-equinesync-graphite/70">
                Distribution snapshot
              </span>
            </div>
            <Stat label="Total" value={subs?.total} testid="report-subs-total" />
            <Stat label={`New in ${window}`} value={subs?.new_in_window} testid="report-subs-new" />
            <div className="mt-4 text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              By status
            </div>
            <div className="mt-2"><DistBar map={subs?.by_status} /></div>
            <div className="mt-4 text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              By tier
            </div>
            <div className="mt-2"><DistBar map={subs?.by_tier} /></div>
          </Card>

          <Card title="Facilities" testid="admin-reports-facilities-card">
            <div className="flex items-center gap-2 mb-3">
              <Building2 className="w-4 h-4 text-equinesync-slate" />
              <span className="text-[12.5px] text-equinesync-graphite/70">
                Roster + horse summary
              </span>
            </div>
            <Stat label="Total facilities" value={facs?.total_facilities} testid="report-facilities-total" />
            <Stat label={`New in ${window}`} value={facs?.new_facilities_in_window} testid="report-facilities-new" />
            <Stat label="Total horses" value={facs?.total_horses} testid="report-horses-total" />
            <Stat label="Facilities w/ horses" value={facs?.horses_summary?.facilities_with_horses} testid="report-facilities-with-horses" />
            <Stat label="Max horses / facility" value={facs?.horses_summary?.max_horses_at_facility} testid="report-max-horses" />
            <div className="mt-4 text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              By status
            </div>
            <div className="mt-2"><DistBar map={facs?.facilities_by_status} /></div>
          </Card>
        </div>
      )}

      <div className="mt-8 rounded-2xl border border-equinesync-graphite/10 bg-white p-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          <Users className="w-3.5 h-3.5 inline mr-1.5 -mt-0.5" />
          CSV Export
        </div>
        <p className="mt-2 text-[13px] text-equinesync-graphite/65 max-w-2xl">
          Download safe aggregates as CSV. Stripe-shaped values are scrubbed
          before serialization. {!canExport && (
            <span
              data-testid="admin-reports-csv-locked-note"
              className="text-equinesync-graphite/55"
            >
              Your platform role can read reports but is not authorised to
              export.
            </span>
          )}
        </p>
        <div className="mt-4 flex flex-wrap items-center gap-2" data-testid="admin-reports-csv-controls">
          <div className="inline-flex rounded-lg border border-equinesync-graphite/15 overflow-hidden">
            {CSV_TYPES.map((t) => (
              <button
                key={t.id}
                type="button"
                onClick={() => setCsvType(t.id)}
                data-testid={`admin-reports-csv-type-${t.id}`}
                className={`px-3 py-1.5 text-[12.5px] tracking-wide transition-colors ${
                  csvType === t.id
                    ? "bg-equinesync-slate text-equinesync-frost"
                    : "text-equinesync-graphite hover:bg-equinesync-frost"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
          {canExport && (
            <button
              type="button"
              onClick={downloadCsv}
              disabled={exporting}
              data-testid="admin-reports-csv-download"
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-equinesync-graphite text-equinesync-frost text-[12.5px] tracking-wide hover:bg-equinesync-slate disabled:opacity-60"
            >
              <Download className="w-3.5 h-3.5" />
              {exporting ? "Exporting…" : "Download CSV"}
            </button>
          )}
          {exportErr && (
            <span
              data-testid="admin-reports-csv-error"
              className="text-[12px] text-equinesync-graphite/80"
            >
              {exportErr}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
