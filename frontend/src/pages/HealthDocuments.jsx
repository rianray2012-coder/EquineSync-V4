import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, ExternalLink, FileText, Plus, RefreshCw, Search, Share2 } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const TYPES = ["all", "coggins", "vaccine", "vet_report", "insurance", "other"];
const ADD_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Horse name" },
  { key: "document_type", label: "Type", kind: "select", opts: TYPES.filter((t) => t !== "all") },
  { key: "document_url", label: "File URL", placeholder: "https://…" },
  { key: "shared_with", label: "Shared with", placeholder: "owner, show secretary" },
  { key: "expires_at", label: "Expires", type: "date" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const expiryTone = (expiresAt) => {
  if (!expiresAt) return "neutral";
  const days = Math.ceil((new Date(expiresAt).getTime() - Date.now()) / 86400000);
  if (days < 0) return "critical";
  if (days <= 30) return "warning";
  return "success";
};

const expiryLabel = (expiresAt) => {
  if (!expiresAt) return "No expiration";
  const days = Math.ceil((new Date(expiresAt).getTime() - Date.now()) / 86400000);
  if (days < 0) return "expired";
  if (days === 0) return "expires today";
  return `${days}d left`;
};

export default function HealthDocuments() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [type, setType] = useState("all");
  const [query, setQuery] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/health-documents");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load health documents.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return records.filter((record) => {
      const data = record.data || {};
      const matchesType = type === "all" || data.document_type === type;
      const haystack = [data.horse_name, data.document_type, data.shared_with, data.notes]
        .filter(Boolean).join(" ").toLowerCase();
      return matchesType && (!q || haystack.includes(q));
    }).sort((a, b) => String((a.data || {}).expires_at || "9999").localeCompare(String((b.data || {}).expires_at || "9999")));
  }, [records, type, query]);

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/health-documents/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive document");
    }
  };

  return (
    <div data-testid="health-documents-page">
      <PageHeader
        eyebrow="Health"
        title="Health Documents"
        subtitle="Store document references, expiration dates, and sharing notes for Coggins, vaccines, insurance, and vet paperwork."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="health-documents-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="health-documents-add">
              <Plus className="w-4 h-4" /> Add document
            </button>
          </div>
        }
      />

      <Card hover={false} className="mb-6 border-equine-icy/30 bg-equine-icy/5">
        <div className="flex items-start gap-3">
          <FileText className="w-4 h-4 text-equine-lilac mt-0.5 flex-shrink-0" />
          <div className="text-[13px] text-equine-inkMuted leading-relaxed">
            Upload and scanning workflows are storage-provider ready. This page tracks document URLs and sharing/expiration metadata until live storage credentials are configured.
          </div>
        </div>
      </Card>

      <Card hover={false} className="mb-6 p-4">
        <div className="flex flex-col lg:flex-row gap-3 lg:items-center">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-equine-inkSoft absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search horse, type, sharing notes…"
              className="w-full bg-equine-soft border border-equine-hairline rounded-xl pl-9 pr-3 py-2.5 text-equine-ink outline-none focus:border-equine-icy"
              data-testid="health-documents-search"
            />
          </div>
          <div className="flex gap-2 overflow-x-auto scrollbar-luxe pb-1 lg:pb-0">
            {TYPES.map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => setType(t)}
                className={`px-3 py-2 rounded-full text-[12px] border whitespace-nowrap ${
                  type === t ? "bg-equine-navy text-white border-equine-navy" : "bg-equine-soft text-equine-inkMuted border-equine-hairline hover:text-equine-ink"
                }`}
                data-testid={`health-documents-filter-${t}`}
              >
                {t.replace(/_/g, " ")}
              </button>
            ))}
          </div>
        </div>
      </Card>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading documents…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Health documents unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <FileText strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No documents tracked</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add the first Coggins, vaccine, insurance, or vet document reference.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="health-documents-empty-add">
            <Plus className="w-4 h-4" /> Add first document
          </button>
        </Empty>
      ) : filtered.length === 0 ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">No documents match this search.</div></Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-5">
          {filtered.map((record) => {
            const data = record.data || {};
            return (
              <Card key={record.id} hover={false} data-testid={`health-document-card-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.horse_name}</div>
                    <div className="text-[12.5px] text-equine-inkMuted capitalize">{(data.document_type || "document").replace(/_/g, " ")}</div>
                  </div>
                  <StatusPill tone={expiryTone(data.expires_at)}>{expiryLabel(data.expires_at)}</StatusPill>
                </div>
                <div className="space-y-2 text-[13px] text-equine-inkMuted">
                  <div>Expires {fmtDate(data.expires_at)}</div>
                  {data.shared_with && (
                    <div className="flex items-start gap-2">
                      <Share2 className="w-3.5 h-3.5 mt-0.5 flex-shrink-0" />
                      <span>{data.shared_with}</span>
                    </div>
                  )}
                  {data.notes && <div className="text-equine-ink">{data.notes}</div>}
                </div>
                <div className="hairline mt-4 pt-3 flex items-center justify-between gap-3">
                  {data.document_url ? (
                    <a href={data.document_url} target="_blank" rel="noreferrer" className="text-[12px] text-equine-navy hover:text-equine-lavenderSoft inline-flex items-center gap-1">
                      Open document <ExternalLink className="w-3 h-3" />
                    </a>
                  ) : <span className="text-[12px] text-equine-inkSoft">No file URL</span>}
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
        title="Add health document"
        eyebrow="Health"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/health-documents/records"
        initialValues={{ document_type: "coggins" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save document"
        testidPrefix="health-documents-add"
        onCreated={load}
      />
    </div>
  );
}
