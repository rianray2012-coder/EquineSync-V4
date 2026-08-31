import React, { useCallback, useEffect, useState } from "react";
import { AlertTriangle, CalendarDays, FileText, HeartPulse, RefreshCw, Stethoscope } from "lucide-react";
import { api, fmtDate } from "../../lib/api";
import { Card, PageHeader, SectionEyebrow, Stat, StatusPill } from "../../components/Primitives";
import LastSyncedBadge from "../../components/today/LastSyncedBadge";
import TrustWorkflowPanel from "../../components/TrustWorkflowPanel";
import ProviderAccessPanel from "../../components/ProviderAccessPanel";

const labelFor = (value) => String(value || "").replace(/_/g, " ");

export default function ServiceProviderDashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [lastSyncedAt, setLastSyncedAt] = useState(null);

  const load = useCallback(async () => {
    setRefreshing(true);
    setError(null);
    try {
      const response = await api.get("/service-provider/operating-center");
      setData(response.data);
      setLastSyncedAt(new Date());
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load service provider center.");
    } finally {
      setRefreshing(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  if (error) {
    return (
      <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="dashboard-service-provider">
        <PageHeader
          eyebrow="Provider Home"
          title="Service Provider Center"
          subtitle="Shared horses and visit context appear only after explicit facility grants."
          action={<RefreshButton onClick={load} refreshing={refreshing} />}
        />
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Service provider center unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      </div>
    );
  }

  const counts = data?.counts || {};
  const providerName = data?.provider?.name || "Provider";

  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="dashboard-service-provider">
      <PageHeader
        eyebrow={`Provider, ${providerName}`}
        title="Service Provider Center"
        subtitle="Grant-scoped horses, care records, and visit-note context for this provider account."
        action={
          <div className="flex items-center gap-2 flex-wrap justify-end">
            <LastSyncedBadge at={lastSyncedAt} onRefresh={load} refreshing={refreshing} verb="Updated" tone="secondary" />
            <RefreshButton onClick={load} refreshing={refreshing} />
          </div>
        }
      />

      {!data ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading provider work...</div></Card>
      ) : (
        <>
          <TrustWorkflowPanel roleKey="serviceProvider" testid="provider-north-star" />

          <ProviderAccessPanel />

          <div className="grid grid-cols-2 lg:grid-cols-5 gap-5 mb-10">
            <Stat label="Active Grants" value={counts.active_grants || 0} caption="Explicit horse access" icon={Stethoscope} testid="provider-stat-grants" />
            <Stat label="Shared Horses" value={counts.shared_horses || 0} caption="Grant-scoped only" accent="steel" icon={HeartPulse} testid="provider-stat-horses" />
            <Stat label="Vet Records" value={counts.recent_vet_records || 0} caption="Provider-safe context" accent="sage" icon={Stethoscope} testid="provider-stat-vet" />
            <Stat label="Farrier Records" value={counts.recent_farrier_records || 0} caption="Provider-safe context" accent="brass" icon={CalendarDays} testid="provider-stat-farrier" />
            <Stat label="Visit Notes" value={counts.visit_notes || 0} caption="Provider-authored" accent="amber" icon={FileText} testid="provider-stat-notes" />
          </div>

          <SectionEyebrow>Shared Context</SectionEyebrow>
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-10">
            <Panel
              title="Shared Horses"
              icon={HeartPulse}
              empty="No horses are shared with this provider account."
              rows={data.shared_horses || []}
              render={(horse) => (
                <div>
                  <div className="text-equine-ink font-display text-xl leading-tight">{horse.name}</div>
                  <div className="text-[12.5px] text-equine-inkMuted mt-1">
                    {[horse.status, horse.discipline, horse.breed].filter(Boolean).map(labelFor).join(" - ") || "Horse context"}
                  </div>
                  {horse.allergies?.length > 0 && <div className="text-[12.5px] text-equine-saddle mt-2">Allergies: {horse.allergies.join(", ")}</div>}
                </div>
              )}
            />
            <Panel
              title="Vet Records"
              icon={Stethoscope}
              empty="No grant-scoped vet records yet."
              rows={data.recent_vet_records || []}
              render={(row) => (
                <div>
                  <div className="text-equine-ink font-display text-xl leading-tight">{row.title || "Vet record"}</div>
                  <div className="text-[12.5px] text-equine-inkMuted mt-1">{fmtDate(row.date)}{row.vet_name ? ` - ${row.vet_name}` : ""}</div>
                  {row.type && <div className="mt-2"><StatusPill tone="neutral">{labelFor(row.type)}</StatusPill></div>}
                </div>
              )}
            />
            <Panel
              title="Farrier Records"
              icon={CalendarDays}
              empty="No grant-scoped farrier records yet."
              rows={data.recent_farrier_records || []}
              render={(row) => (
                <div>
                  <div className="text-equine-ink font-display text-xl leading-tight">{row.farrier_name || "Farrier visit"}</div>
                  <div className="text-[12.5px] text-equine-inkMuted mt-1">{fmtDate(row.date)}{row.next_visit_due ? ` - next ${fmtDate(row.next_visit_due)}` : ""}</div>
                  {row.shoes_on?.length > 0 && <div className="text-[12.5px] text-equine-inkMuted mt-2">{row.shoes_on.join(", ")}</div>}
                </div>
              )}
            />
          </div>

          <SectionEyebrow>Provider Notes</SectionEyebrow>
          <Panel
            title="Recent Visit Notes"
            icon={FileText}
            empty="No provider-authored visit notes yet."
            rows={data.visit_notes || []}
            wide
            render={(row) => (
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="text-equine-ink font-display text-xl leading-tight">{row.title}</div>
                  <div className="text-[12.5px] text-equine-inkMuted mt-1">{labelFor(row.category)} - {fmtDate(row.visit_date || row.created_at)}</div>
                </div>
                {row.follow_up_due && <StatusPill tone="warning">Follow-up {fmtDate(row.follow_up_due)}</StatusPill>}
              </div>
            )}
          />
        </>
      )}
    </div>
  );
}

const RefreshButton = ({ onClick, refreshing }) => (
  <button onClick={onClick} disabled={refreshing} className="btn-secondary inline-flex items-center gap-2 disabled:opacity-50" data-testid="provider-dashboard-refresh">
    <RefreshCw className="w-4 h-4" /> Refresh
  </button>
);

const Panel = ({ title, icon: Icon, rows, empty, render, wide = false }) => (
  <Card hover={false} data-testid={`provider-${title.toLowerCase().replace(/[^a-z]+/g, "-")}`} className={wide ? "mb-10" : ""}>
    <div className="flex items-center gap-2 mb-4">
      <Icon className="w-4 h-4 text-equine-brass" />
      <h2 className="font-display text-2xl text-equine-ink">{title}</h2>
    </div>
    {rows.length === 0 ? (
      <div className="rounded-lg border border-dashed border-equine-cloud bg-white/45 py-8 px-4 text-center text-[13px] text-equine-inkMuted">{empty}</div>
    ) : (
      <div className={wide ? "grid grid-cols-1 lg:grid-cols-2 gap-3" : "space-y-3"}>
        {rows.map((row) => (
          <div key={row.id} className="rounded-lg border border-equine-hairline bg-equine-soft/55 p-4">{render(row)}</div>
        ))}
      </div>
    )}
  </Card>
);
