import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Activity, AlertTriangle, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const ADD_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Valentino" },
  { key: "recorded_at", label: "Date", type: "date", required: true },
  { key: "weight_lbs", label: "Weight lbs", type: "number", placeholder: "1180" },
  { key: "body_condition", label: "Body condition", type: "number", placeholder: "5.5" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const numberOrNull = (v) => {
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
};

const latestByDate = (rows) => [...rows].sort((a, b) => String((b.data || {}).recorded_at || "").localeCompare(String((a.data || {}).recorded_at || "")));

export default function WeightTrends() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [selectedHorse, setSelectedHorse] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/weight-trends");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load weight trends.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const horses = useMemo(() => {
    const names = [...new Set(records.map((record) => (record.data || {}).horse_name).filter(Boolean))].sort();
    return ["all", ...names];
  }, [records]);

  const visible = useMemo(() => {
    const rows = selectedHorse === "all"
      ? records
      : records.filter((record) => (record.data || {}).horse_name === selectedHorse);
    return latestByDate(rows);
  }, [records, selectedHorse]);

  const byHorse = useMemo(() => {
    const out = {};
    records.forEach((record) => {
      const horse = (record.data || {}).horse_name || "Unknown";
      (out[horse] = out[horse] || []).push(record);
    });
    return out;
  }, [records]);

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/weight-trends/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive entry");
    }
  };

  return (
    <div data-testid="weight-trends-page">
      <PageHeader
        eyebrow="Health"
        title="Weight & Body Condition"
        subtitle="Track each horse's weight and body-condition score over time for feed, health, and performance decisions."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="weight-trends-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="weight-trends-add">
              <Plus className="w-4 h-4" /> Add entry
            </button>
          </div>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading trends…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Weight trends unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Activity strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No measurements yet</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a weight or body-condition entry to start the trend line.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="weight-trends-empty-add">
            <Plus className="w-4 h-4" /> Add first entry
          </button>
        </Empty>
      ) : (
        <>
          <div className="flex gap-2 overflow-x-auto scrollbar-luxe pb-3 mb-3">
            {horses.map((horse) => (
              <button
                key={horse}
                type="button"
                onClick={() => setSelectedHorse(horse)}
                className={`px-3 py-2 rounded-full text-[12px] border whitespace-nowrap ${
                  selectedHorse === horse ? "bg-equine-navy text-white border-equine-navy" : "bg-equine-soft text-equine-inkMuted border-equine-hairline hover:text-equine-ink"
                }`}
                data-testid={`weight-filter-${horse.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
              >
                {horse === "all" ? "All horses" : horse}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-6">
            {Object.entries(byHorse).map(([horse, rows]) => (
              <Card key={horse} hover={false} className="p-5">
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div>
                    <div className="font-display text-2xl text-equine-ink leading-none">{horse}</div>
                    <div className="text-[12px] text-equine-inkMuted mt-1">{rows.length} measurement{rows.length === 1 ? "" : "s"}</div>
                  </div>
                  <StatusPill tone="info">{latestByDate(rows)[0]?.data?.body_condition || "—"} BCS</StatusPill>
                </div>
                <TrendChart rows={rows} />
              </Card>
            ))}
          </div>

          <Card hover={false} data-testid="weight-entries">
            <div className="space-y-3">
              {visible.map((record) => {
                const data = record.data || {};
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`weight-entry-${record.id}`}>
                    <div className="flex flex-col lg:flex-row lg:items-center gap-3">
                      <div className="flex-1 min-w-0">
                        <div className="font-display text-2xl text-equine-ink leading-none">{data.horse_name}</div>
                        <div className="text-[12.5px] text-equine-inkMuted mt-1">{fmtDate(data.recorded_at)}</div>
                        {data.notes && <div className="mt-2 text-[13px] text-equine-inkMuted">{data.notes}</div>}
                      </div>
                      <div className="grid grid-cols-2 gap-3 min-w-[220px]">
                        <Metric label="Weight" value={data.weight_lbs ? `${data.weight_lbs} lb` : "—"} />
                        <Metric label="Body condition" value={data.body_condition ?? "—"} />
                      </div>
                      <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink lg:ml-2">
                        Archive
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>
        </>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add measurement"
        eyebrow="Health"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/weight-trends/records"
        initialValues={{ recorded_at: new Date().toISOString().slice(0, 10) }}
        transform={(form) => ({ data: form })}
        submitLabel="Save entry"
        testidPrefix="weight-trends-add"
        onCreated={load}
      />
    </div>
  );
}

const Metric = ({ label, value }) => (
  <div className="rounded-lg border border-equine-hairline bg-equine-card p-3">
    <div className="label-eyebrow-muted mb-1">{label}</div>
    <div className="font-display text-2xl text-equine-ink leading-none">{value}</div>
  </div>
);

const TrendChart = ({ rows }) => {
  const points = [...rows]
    .map((record) => ({ date: (record.data || {}).recorded_at, weight: numberOrNull((record.data || {}).weight_lbs) }))
    .filter((p) => p.date && p.weight !== null)
    .sort((a, b) => String(a.date).localeCompare(String(b.date)));

  if (points.length < 2) {
    return <div className="h-28 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center text-[12px] text-equine-inkSoft">Add another weight entry for a trend line.</div>;
  }

  const weights = points.map((p) => p.weight);
  const min = Math.min(...weights);
  const max = Math.max(...weights);
  const spread = Math.max(1, max - min);
  const coords = points.map((p, i) => {
    const x = 12 + (i / Math.max(1, points.length - 1)) * 276;
    const y = 96 - ((p.weight - min) / spread) * 72;
    return `${x},${y}`;
  }).join(" ");

  return (
    <svg viewBox="0 0 300 112" className="w-full h-28 rounded-xl bg-equine-soft border border-equine-hairline" role="img" aria-label="Weight trend">
      <line x1="12" y1="96" x2="288" y2="96" stroke="#E0DCEC" strokeWidth="1" />
      <line x1="12" y1="24" x2="288" y2="24" stroke="#E0DCEC" strokeWidth="1" />
      <polyline points={coords} fill="none" stroke="#2E3448" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
      {coords.split(" ").map((pair, i) => {
        const [x, y] = pair.split(",");
        return <circle key={pair} cx={x} cy={y} r={4} fill={i === coords.split(" ").length - 1 ? "#B89B7A" : "#A7B7E7"} />;
      })}
      <text x="12" y="14" fontSize="10" fill="#666674">{max} lb</text>
      <text x="12" y="108" fontSize="10" fill="#666674">{min} lb</text>
    </svg>
  );
};
