import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, ExternalLink, MapPin, Plus, RefreshCw, Route } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const ADD_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Horse name" },
  { key: "rider_name", label: "Rider", placeholder: "Staff name" },
  { key: "started_at", label: "Started", placeholder: "YYYY-MM-DDTHH:MM:SS" },
  { key: "distance_miles", label: "Distance", type: "number", placeholder: "Miles" },
  { key: "duration_minutes", label: "Minutes", type: "number", placeholder: "Minutes" },
  { key: "track_url", label: "Track URL", placeholder: "https://…" },
];

const fmtDateTime = (s) => {
  if (!s) return "—";
  const d = new Date(s);
  if (Number.isNaN(d.getTime())) return s;
  return d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
};

export default function RideGps() {
  const [records, setRecords] = useState([]);
  const [placeholders, setPlaceholders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [moduleRes, placeholderRes] = await Promise.all([
        api.get("/feature-modules/ride-gps"),
        api.get("/integrations/placeholders"),
      ]);
      setRecords(moduleRes.data.records || []);
      setPlaceholders((placeholderRes.data || []).filter((p) => p.provider === "wearables"));
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load GPS rides.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const totals = useMemo(() => ({
    rides: records.length,
    miles: records.reduce((sum, record) => sum + (Number((record.data || {}).distance_miles) || 0), 0),
    minutes: records.reduce((sum, record) => sum + (Number((record.data || {}).duration_minutes) || 0), 0),
  }), [records]);

  const sorted = useMemo(() => [...records].sort((a, b) => String((b.data || {}).started_at || "").localeCompare(String((a.data || {}).started_at || ""))), [records]);

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/ride-gps/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive GPS ride");
    }
  };

  return (
    <div data-testid="ride-gps-page">
      <PageHeader
        eyebrow="Mobile & Integrations"
        title="GPS Ride Tracking"
        subtitle="Record distance, duration, rider, horse, and track URL data now; native GPS capture can plug into this structure later."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="ride-gps-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="ride-gps-add">
              <Plus className="w-4 h-4" /> Add ride
            </button>
          </div>
        }
      />

      <Card hover={false} className="mb-6 border-equine-lilac/30 bg-equine-lilac/5">
        <div className="flex items-start gap-3">
          <MapPin className="w-4 h-4 text-equine-lilac mt-0.5 flex-shrink-0" />
          <div className="text-[13px] text-equine-inkMuted leading-relaxed">
            Native GPS capture and wearable integrations are deferred to mobile app wiring. This page stores ride track structure and external track references.
            {placeholders[0] && <span className="block mt-1 text-equine-inkSoft">{placeholders[0].ready_for.join(" · ")}</span>}
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <Metric label="Rides" value={totals.rides} />
        <Metric label="Miles" value={totals.miles.toFixed(1)} />
        <Metric label="Hours" value={(totals.minutes / 60).toFixed(1)} />
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading GPS rides…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">GPS rides unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Route strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No GPS rides tracked</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a ride distance, duration, and track link.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="ride-gps-empty-add">
            <Plus className="w-4 h-4" /> Add first ride
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          {sorted.map((record) => {
            const data = record.data || {};
            return (
              <Card key={record.id} hover={false} data-testid={`ride-gps-card-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.horse_name}</div>
                    <div className="text-[12.5px] text-equine-inkMuted">{data.rider_name || "Rider TBD"} · {fmtDateTime(data.started_at)}</div>
                  </div>
                  <StatusPill tone="info">{Number(data.distance_miles || 0).toFixed(1)} mi</StatusPill>
                </div>
                <div className="grid grid-cols-2 gap-3 mb-4">
                  <Metric label="Minutes" value={data.duration_minutes || "—"} compact />
                  <Metric label="Pace" value={paceLabel(data)} compact />
                </div>
                <div className="hairline mt-4 pt-3 flex items-center justify-between gap-3">
                  {data.track_url ? (
                    <a href={data.track_url} target="_blank" rel="noreferrer" className="text-[12px] text-equine-navy hover:text-equine-lilac inline-flex items-center gap-1">
                      Open track <ExternalLink className="w-3 h-3" />
                    </a>
                  ) : <span className="text-[12px] text-equine-inkSoft">No track URL</span>}
                  <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink">
                    Archive
                  </button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add GPS ride"
        eyebrow="Mobile & Integrations"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/ride-gps/records"
        initialValues={{ started_at: new Date().toISOString().slice(0, 16) }}
        transform={(form) => ({ data: form })}
        submitLabel="Save ride"
        testidPrefix="ride-gps-add"
        onCreated={load}
      />
    </div>
  );
}

const Metric = ({ label, value, compact }) => (
  <div className={`${compact ? "p-3" : "p-4"} rounded-lg border border-equine-cloud bg-white/70`}>
    <div className="label-eyebrow-muted mb-1">{label}</div>
    <div className={`${compact ? "text-2xl" : "text-4xl"} font-display text-equine-ink leading-none`}>{value}</div>
  </div>
);

const paceLabel = (data) => {
  const minutes = Number(data.duration_minutes) || 0;
  const miles = Number(data.distance_miles) || 0;
  if (!minutes || !miles) return "—";
  return `${Math.round(minutes / miles)} min/mi`;
};
