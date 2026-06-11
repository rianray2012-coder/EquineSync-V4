import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, Plus, RefreshCw, Search, Wrench } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const CATEGORIES = ["all", "tack", "equipment", "blanket", "vehicle", "tool"];
const CONDITIONS = ["excellent", "good", "repair", "retired"];
const CONDITION_TONE = {
  excellent: "success",
  good: "info",
  repair: "warning",
  retired: "critical",
};

const ADD_FIELDS = [
  { key: "name", label: "Item", required: true, placeholder: "Devoucoux jump saddle", full: true },
  { key: "category", label: "Category", kind: "select", opts: CATEGORIES.filter((c) => c !== "all") },
  { key: "assigned_to", label: "Assigned to", placeholder: "Valentino" },
  { key: "condition", label: "Condition", kind: "select", opts: CONDITIONS },
  { key: "location", label: "Location", placeholder: "Tack Room A" },
  { key: "serial_number", label: "Serial / tag", placeholder: "DX-1842" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

export default function Equipment() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [category, setCategory] = useState("all");
  const [query, setQuery] = useState("");
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/equipment");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load equipment.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return records.filter((record) => {
      const data = record.data || {};
      const matchesCategory = category === "all" || data.category === category;
      const haystack = [data.name, data.assigned_to, data.location, data.serial_number, data.notes]
        .filter(Boolean).join(" ").toLowerCase();
      return matchesCategory && (!q || haystack.includes(q));
    }).sort((a, b) => String((a.data || {}).name || "").localeCompare(String((b.data || {}).name || "")));
  }, [records, category, query]);

  const stats = useMemo(() => Object.fromEntries(CONDITIONS.map((condition) => [
    condition,
    records.filter((record) => ((record.data || {}).condition || "good") === condition).length,
  ])), [records]);

  const setCondition = async (record, condition) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/equipment/records/${record.id}`, { data: { condition } });
      toast.success("Condition updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update condition");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/equipment/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive item");
    }
  };

  return (
    <div data-testid="equipment-page">
      <PageHeader
        eyebrow="Operations"
        title="Equipment & Tack"
        subtitle="Track tack, blankets, tools, vehicles, assignments, locations, condition, and repair needs."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="equipment-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="equipment-add">
              <Plus className="w-4 h-4" /> Add item
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {CONDITIONS.map((condition) => (
          <Card key={condition} hover={false} className="p-4">
            <div className="label-eyebrow-muted mb-2 capitalize">{condition}</div>
            <div className="flex items-end justify-between gap-3">
              <div className="font-display text-4xl text-equine-ink leading-none">{stats[condition]}</div>
              <StatusPill tone={CONDITION_TONE[condition]}>{condition}</StatusPill>
            </div>
          </Card>
        ))}
      </div>

      <Card hover={false} className="mb-6 p-4">
        <div className="flex flex-col lg:flex-row gap-3 lg:items-center">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-equine-inkSoft absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search item, assignment, location, tag…"
              className="w-full bg-equine-soft border border-equine-hairline rounded-xl pl-9 pr-3 py-2.5 text-equine-ink outline-none focus:border-equine-brass"
              data-testid="equipment-search"
            />
          </div>
          <div className="flex gap-2 overflow-x-auto scrollbar-luxe pb-1 lg:pb-0">
            {CATEGORIES.map((c) => (
              <button
                key={c}
                type="button"
                onClick={() => setCategory(c)}
                className={`px-3 py-2 rounded-full text-[12px] border whitespace-nowrap ${
                  category === c
                    ? "bg-equine-navy text-white border-equine-navy"
                    : "bg-equine-soft text-equine-inkMuted border-equine-hairline hover:text-equine-ink"
                }`}
                data-testid={`equipment-filter-${c}`}
              >
                {c}
              </button>
            ))}
          </div>
        </div>
      </Card>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading equipment…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Equipment unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Wrench strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No tack or equipment tracked</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add saddles, blankets, vehicles, tools, or repair items.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="equipment-empty-add">
            <Plus className="w-4 h-4" /> Add first item
          </button>
        </Empty>
      ) : filtered.length === 0 ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">No items match this search.</div></Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-5">
          {filtered.map((record) => {
            const data = record.data || {};
            const condition = data.condition || "good";
            return (
              <Card key={record.id} hover={false} className={savingId === record.id ? "opacity-60" : ""} data-testid={`equipment-card-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.name}</div>
                    <div className="text-[12.5px] text-equine-inkMuted capitalize">{data.category || "equipment"}</div>
                  </div>
                  <StatusPill tone={CONDITION_TONE[condition]}>{condition}</StatusPill>
                </div>
                <div className="grid grid-cols-2 gap-3 text-[13px]">
                  <Field label="Assigned" value={data.assigned_to || "Unassigned"} />
                  <Field label="Location" value={data.location || "—"} />
                  <Field label="Serial / tag" value={data.serial_number || "—"} />
                  <Field label="Updated" value={record.updated_at ? new Date(record.updated_at).toLocaleDateString() : "—"} />
                </div>
                {data.notes && <div className="mt-4 text-[13px] text-equine-inkMuted leading-relaxed">{data.notes}</div>}
                <div className="hairline mt-4 pt-3 flex flex-wrap items-center gap-2">
                  {CONDITIONS.map((next) => (
                    <button
                      key={next}
                      type="button"
                      disabled={next === condition}
                      onClick={() => setCondition(record, next)}
                      className="text-[11.5px] px-2.5 py-1.5 rounded-full border border-equine-hairline bg-equine-soft text-equine-inkMuted hover:text-equine-ink disabled:opacity-35 disabled:pointer-events-none"
                    >
                      {next}
                    </button>
                  ))}
                  <button type="button" onClick={() => archiveRecord(record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">
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
        title="Add equipment or tack"
        eyebrow="Operations"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/equipment/records"
        initialValues={{ category: "tack", condition: "good" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save item"
        testidPrefix="equipment-add"
        onCreated={load}
      />
    </div>
  );
}

const Field = ({ label, value }) => (
  <div>
    <div className="label-eyebrow-muted mb-1">{label}</div>
    <div className="text-equine-ink break-words">{value}</div>
  </div>
);
