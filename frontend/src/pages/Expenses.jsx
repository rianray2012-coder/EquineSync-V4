import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, Download, ExternalLink, Plus, Receipt, RefreshCw, Search } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate, money } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const CATEGORIES = ["all", "feed", "bedding", "labor", "vet", "farrier", "maintenance", "show", "other"];
const ADD_FIELDS = [
  { key: "vendor", label: "Vendor", required: true, placeholder: "Vendor name", full: true },
  { key: "category", label: "Category", kind: "select", opts: CATEGORIES.filter((c) => c !== "all") },
  { key: "amount", label: "Amount", type: "number", required: true },
  { key: "spent_at", label: "Date", type: "date" },
  { key: "receipt_url", label: "Receipt URL", placeholder: "https://…" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const csvCell = (value) => `"${String(value ?? "").replace(/"/g, '""')}"`;

export default function Expenses() {
  const [records, setRecords] = useState([]);
  const [readinessItems, setReadinessItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [category, setCategory] = useState("all");
  const [query, setQuery] = useState("");
  const [exportingQuickBooks, setExportingQuickBooks] = useState(false);
  const [quickBooksManifest, setQuickBooksManifest] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [moduleRes, readinessRes] = await Promise.all([
        api.get("/feature-modules/expenses"),
        api.get("/integrations/placeholders"),
      ]);
      setRecords(moduleRes.data.records || []);
      setReadinessItems((readinessRes.data || []).filter((p) => p.provider === "quickbooks"));
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load expenses.");
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
      const haystack = [data.vendor, data.category, data.notes].filter(Boolean).join(" ").toLowerCase();
      return matchesCategory && (!q || haystack.includes(q));
    }).sort((a, b) => String((b.data || {}).spent_at || "").localeCompare(String((a.data || {}).spent_at || "")));
  }, [records, category, query]);

  const totals = useMemo(() => {
    const byCategory = {};
    records.forEach((record) => {
      const data = record.data || {};
      const key = data.category || "other";
      byCategory[key] = (byCategory[key] || 0) + (Number(data.amount) || 0);
    });
    return {
      all: records.reduce((sum, record) => sum + (Number((record.data || {}).amount) || 0), 0),
      byCategory,
    };
  }, [records]);

  const prepareQuickBooks = async () => {
    try {
      const r = await api.post("/integrations/quickbooks/prepare");
      toast.success(r.data.message || "QuickBooks configuration ready");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare QuickBooks");
    }
  };

  const exportQuickBooks = async () => {
    setExportingQuickBooks(true);
    try {
      const r = await api.post("/integrations/quickbooks/export", {
        include_expenses: true,
        include_invoices: true,
      });
      const manifest = r.data;
      setQuickBooksManifest(manifest);
      const columns = manifest.columns || [];
      const rows = (manifest.rows || []).map((row) => columns.map((column) => csvCell(row[column])).join(","));
      const csv = [columns.join(","), ...rows].join("\n");
      const blob = new Blob([csv], { type: manifest.content_type || "text/csv;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = manifest.filename || `equinesync-quickbooks-export-${new Date().toISOString().slice(0, 10)}.csv`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success("QuickBooks export prepared");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare QuickBooks export");
    } finally {
      setExportingQuickBooks(false);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/expenses/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive expense");
    }
  };

  return (
    <div data-testid="expenses-page">
      <PageHeader
        eyebrow="Financial"
        title="Expenses"
        subtitle="Track feed, bedding, labor, vet, farrier, maintenance, and show expenses for profit/loss reporting."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="expenses-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="expenses-add">
              <Plus className="w-4 h-4" /> Add expense
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-6">
        <Card hover={false}>
          <div className="label-eyebrow">Total expenses</div>
          <div className="font-display text-4xl mt-2 text-equine-ink">{money(totals.all)}</div>
        </Card>
        <Card hover={false} className="lg:col-span-2 border-equine-brass/30 bg-equine-brass/5">
          <div className="flex flex-col lg:flex-row lg:items-center gap-4">
            <div className="flex items-start gap-3 flex-1">
              <Receipt className="w-4 h-4 text-equine-champagne mt-0.5 flex-shrink-0" />
              <div>
                <div className="text-equine-ink text-[14px]">QuickBooks-ready export</div>
                <div className="text-[12.5px] text-equine-inkMuted mt-1">
                  Expense export and invoice sync are scaffolded behind the integration abstraction until credentials are available.
                </div>
                {readinessItems[0] && <div className="text-[11.5px] text-equine-inkSoft mt-2">{readinessItems[0].ready_for.join(" · ")}</div>}
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              <button type="button" onClick={prepareQuickBooks} className="btn-secondary text-[12px] py-2 px-4" data-testid="prepare-quickbooks">
                Prepare QuickBooks
              </button>
              <button
                type="button"
                onClick={exportQuickBooks}
                disabled={exportingQuickBooks}
                className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1 disabled:opacity-60"
                data-testid="export-quickbooks"
              >
                <Download className="w-3.5 h-3.5" /> {exportingQuickBooks ? "Preparing" : "Export CSV"}
              </button>
            </div>
          </div>
        </Card>
      </div>

      {quickBooksManifest && (
        <Card hover={false} className="mb-6" data-testid="quickbooks-export-manifest">
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <div>
              <div className="label-eyebrow-muted mb-1">Latest QuickBooks export</div>
              <div className="font-display text-2xl text-equine-ink">{quickBooksManifest.filename}</div>
              <div className="text-[12.5px] text-equine-inkMuted">
                {quickBooksManifest.row_count} row(s) · {money(quickBooksManifest.total_amount)} total
              </div>
            </div>
            <StatusPill tone="success">{quickBooksManifest.status.replace(/_/g, " ")}</StatusPill>
          </div>
        </Card>
      )}

      <Card hover={false} className="mb-6 p-4">
        <div className="flex flex-col lg:flex-row gap-3 lg:items-center">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-equine-inkSoft absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search vendor, category, notes…"
              className="w-full bg-equine-soft border border-equine-hairline rounded-xl pl-9 pr-3 py-2.5 text-equine-ink outline-none focus:border-equine-brass"
              data-testid="expenses-search"
            />
          </div>
          <div className="flex gap-2 overflow-x-auto scrollbar-luxe pb-1 lg:pb-0">
            {CATEGORIES.map((c) => (
              <button
                key={c}
                type="button"
                onClick={() => setCategory(c)}
                className={`px-3 py-2 rounded-full text-[12px] border whitespace-nowrap ${
                  category === c ? "bg-equine-navy text-white border-equine-navy" : "bg-equine-soft text-equine-inkMuted border-equine-hairline hover:text-equine-ink"
                }`}
                data-testid={`expenses-filter-${c}`}
              >
                {c} {c !== "all" && totals.byCategory[c] ? `· ${money(totals.byCategory[c])}` : ""}
              </button>
            ))}
          </div>
        </div>
      </Card>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading expenses…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Expenses unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Receipt strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No expenses tracked</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add your first feed, bedding, labor, vet, farrier, maintenance, or show expense.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="expenses-empty-add">
            <Plus className="w-4 h-4" /> Add first expense
          </button>
        </Empty>
      ) : filtered.length === 0 ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">No expenses match this search.</div></Card>
      ) : (
        <Card hover={false} data-testid="expenses-list">
          <div className="space-y-3">
            {filtered.map((record) => {
              const data = record.data || {};
              return (
                <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`expense-row-${record.id}`}>
                  <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="font-display text-2xl text-equine-ink truncate">{data.vendor}</div>
                      <div className="text-[12.5px] text-equine-inkMuted">
                        {fmtDate(data.spent_at)} · {(data.category || "other").replace(/_/g, " ")}
                      </div>
                      {data.notes && <div className="mt-2 text-[13px] text-equine-inkMuted">{data.notes}</div>}
                    </div>
                    <div className="font-display text-3xl text-equine-ink lg:w-32 lg:text-right">{money(data.amount)}</div>
                    <StatusPill tone="neutral">{data.category || "other"}</StatusPill>
                    {data.receipt_url ? (
                      <a href={data.receipt_url} target="_blank" rel="noreferrer" className="text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1">
                        Receipt <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : <span className="text-[12px] text-equine-inkSoft">No receipt</span>}
                    <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink">
                      Archive
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add expense"
        eyebrow="Financial"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/expenses/records"
        initialValues={{ category: "feed", spent_at: new Date().toISOString().slice(0, 10) }}
        transform={(form) => ({ data: form })}
        submitLabel="Save expense"
        testidPrefix="expenses-add"
        onCreated={load}
      />
    </div>
  );
}
