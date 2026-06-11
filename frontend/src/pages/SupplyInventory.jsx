import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, Package, Plus, RefreshCw, Search } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const CATEGORIES = ["all", "feed", "hay", "bedding", "supplement", "medical", "other"];
const STATUSES = ["in_stock", "low", "ordered", "out"];
const STATUS_TONE = { in_stock: "success", low: "warning", ordered: "info", out: "critical" };

const ADD_FIELDS = [
  { key: "name", label: "Item", required: true, placeholder: "Orchard grass hay", full: true },
  { key: "category", label: "Category", kind: "select", opts: CATEGORIES.filter((c) => c !== "all") },
  { key: "quantity", label: "Quantity", type: "number", placeholder: "42" },
  { key: "unit", label: "Unit", placeholder: "bales" },
  { key: "reorder_at", label: "Reorder at", type: "number", placeholder: "25" },
  { key: "vendor", label: "Vendor", placeholder: "Bluegrass Feed" },
  { key: "location", label: "Location", placeholder: "Hay loft" },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const labelFor = (value) => String(value || "").replace(/_/g, " ");

const computedStatus = (data) => {
  const quantity = Number(data.quantity);
  const reorderAt = Number(data.reorder_at);
  if (Number.isFinite(quantity) && quantity <= 0) return "out";
  if (Number.isFinite(quantity) && Number.isFinite(reorderAt) && reorderAt > 0 && quantity <= reorderAt) return "low";
  return data.status || "in_stock";
};

export default function SupplyInventory() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [category, setCategory] = useState("all");
  const [query, setQuery] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/supply-inventory");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load supply inventory.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = useMemo(() => records.filter((record) => {
    const data = record.data || {};
    const haystack = [data.name, data.vendor, data.location, data.notes].join(" ").toLowerCase();
    return (category === "all" || data.category === category) && haystack.includes(query.toLowerCase());
  }), [records, category, query]);

  const stats = useMemo(() => {
    const out = { low: 0, out: 0, ordered: 0 };
    records.forEach((record) => {
      const status = computedStatus(record.data || {});
      if (out[status] !== undefined) out[status] += 1;
    });
    return out;
  }, [records]);

  const setStatus = async (record, status) => {
    try {
      await api.patch(`/feature-modules/supply-inventory/records/${record.id}`, { data: { status } });
      toast.success("Supply status updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update supply");
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/supply-inventory/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive supply");
    }
  };

  return (
    <div data-testid="supply-inventory-page">
      <PageHeader
        eyebrow="Operations"
        title="Supply Inventory"
        subtitle="Track feed, hay, bedding, supplements, reorder thresholds, vendors, storage locations, and order status."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="supply-inventory-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="supply-inventory-add">
              <Plus className="w-4 h-4" /> Add supply
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-3 gap-4 mb-6">
        <Metric label="Low stock" value={stats.low} tone="warning" />
        <Metric label="Out" value={stats.out} tone="critical" />
        <Metric label="Ordered" value={stats.ordered} tone="info" />
      </div>

      <Card hover={false} className="mb-6">
        <div className="flex flex-col lg:flex-row lg:items-center gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-equine-inkSoft" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search item, vendor, location..."
              className="w-full bg-white border border-equine-cloud rounded-lg pl-9 pr-3 py-2.5 text-equine-ink outline-none focus:border-equine-brass"
              data-testid="supply-inventory-search"
            />
          </div>
          <div className="flex flex-wrap gap-2">
            {CATEGORIES.map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => setCategory(item)}
                className={`px-3 py-2 rounded-lg text-[12px] border capitalize ${category === item ? "bg-equine-navy text-white border-equine-navy" : "bg-white text-equine-inkMuted border-equine-cloud"}`}
                data-testid={`supply-category-${item}`}
              >
                {labelFor(item)}
              </button>
            ))}
          </div>
        </div>
      </Card>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading supplies...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Supply inventory unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Package strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No supply records</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add hay, feed, bedding, or supplement stock.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="supply-inventory-empty-add">
            <Plus className="w-4 h-4" /> Add first supply
          </button>
        </Empty>
      ) : filtered.length === 0 ? (
        <Empty>
          <Package strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No matching supplies</div>
          <div className="text-[13px] text-equine-platinum/60">Try another category or search term.</div>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
          {filtered.map((record) => {
            const data = record.data || {};
            const status = computedStatus(data);
            return (
              <Card key={record.id} hover={false} data-testid={`supply-inventory-card-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.name}</div>
                    <div className="text-[12.5px] text-equine-inkMuted capitalize">{labelFor(data.category || "other")} - {data.location || "No location"}</div>
                  </div>
                  <StatusPill tone={STATUS_TONE[status] || "info"}>{labelFor(status)}</StatusPill>
                </div>
                <div className="grid grid-cols-3 gap-3 mb-4">
                  <div>
                    <div className="label-eyebrow-muted mb-1">On hand</div>
                    <div className="text-[14px] text-equine-ink">{data.quantity ?? 0} {data.unit || ""}</div>
                  </div>
                  <div>
                    <div className="label-eyebrow-muted mb-1">Reorder</div>
                    <div className="text-[14px] text-equine-ink">{data.reorder_at || "None"}</div>
                  </div>
                  <div>
                    <div className="label-eyebrow-muted mb-1">Vendor</div>
                    <div className="text-[14px] text-equine-ink truncate">{data.vendor || "TBD"}</div>
                  </div>
                </div>
                {data.notes && <div className="text-[13px] text-equine-inkMuted mb-4">{data.notes}</div>}
                <div className="hairline mt-3 pt-3 flex flex-wrap items-center gap-2">
                  {status !== "ordered" && <button type="button" onClick={() => setStatus(record, "ordered")} className="btn-secondary text-[12px] py-2 px-4">Ordered</button>}
                  {status !== "in_stock" && <button type="button" onClick={() => setStatus(record, "in_stock")} className="btn-primary text-[12px] py-2 px-4">Restocked</button>}
                  <button type="button" onClick={() => archiveRecord(record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">Archive</button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add supply"
        eyebrow="Operations"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/supply-inventory/records"
        initialValues={{ category: "hay", status: "in_stock" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save supply"
        testidPrefix="supply-inventory-add"
        onCreated={load}
      />
    </div>
  );
}

const Metric = ({ label, value, tone }) => (
  <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
    <div className="label-eyebrow-muted mb-2">{label}</div>
    <div className="flex items-end justify-between gap-3">
      <div className="font-display text-4xl text-equine-ink leading-none">{value}</div>
      <StatusPill tone={tone}>{label}</StatusPill>
    </div>
  </div>
);
