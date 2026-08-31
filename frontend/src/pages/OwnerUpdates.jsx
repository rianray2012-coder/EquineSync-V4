import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, Image, Plus, RefreshCw, Search, Upload } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const VISIBILITY = ["owner_only", "staff", "barn"];
const VISIBILITY_TONE = { owner_only: "success", staff: "info", barn: "neutral" };
const ADD_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Horse name" },
  { key: "owner_name", label: "Owner", placeholder: "Owner name" },
  { key: "visibility", label: "Visibility", kind: "select", opts: VISIBILITY },
  { key: "media_url", label: "Media URL", placeholder: "https://…" },
  { key: "caption", label: "Caption", kind: "textarea", rows: 4, full: true },
];

export default function OwnerUpdates() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [query, setQuery] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/owner-updates");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load owner updates.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return records.filter((record) => {
      const data = record.data || {};
      const haystack = [data.horse_name, data.owner_name, data.caption, data.visibility].filter(Boolean).join(" ").toLowerCase();
      return !q || haystack.includes(q);
    }).sort((a, b) => String(b.created_at || "").localeCompare(String(a.created_at || "")));
  }, [records, query]);

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/owner-updates/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive update");
    }
  };

  return (
    <div data-testid="owner-updates-page">
      <PageHeader
        eyebrow="Communication"
        title="Photo & Video Updates"
        subtitle="Prepare owner-visible media updates with captions, visibility controls, and storage-ready URL references."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="owner-updates-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="owner-updates-add">
              <Plus className="w-4 h-4" /> Add update
            </button>
          </div>
        }
      />

      <Card hover={false} className="mb-6 border-equine-icy/30 bg-equine-icy/5">
        <div className="flex items-start gap-3">
          <Upload className="w-4 h-4 text-equine-lilac mt-0.5 flex-shrink-0" />
          <div className="text-[13px] text-equine-inkMuted leading-relaxed">
            Uploads are storage-provider ready. This page tracks media URLs and owner-visibility metadata until live object storage credentials are configured.
          </div>
        </div>
      </Card>

      <Card hover={false} className="mb-6 p-4">
        <div className="relative">
          <Search className="w-4 h-4 text-equine-inkSoft absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search horse, owner, caption, visibility…"
            className="w-full bg-equine-soft border border-equine-hairline rounded-xl pl-9 pr-3 py-2.5 text-equine-ink outline-none focus:border-equine-icy"
            data-testid="owner-updates-search"
          />
        </div>
      </Card>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading owner updates…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Owner updates unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Image strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No media updates</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add the first photo/video update for an owner.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="owner-updates-empty-add">
            <Plus className="w-4 h-4" /> Add first update
          </button>
        </Empty>
      ) : filtered.length === 0 ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">No updates match this search.</div></Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-5">
          {filtered.map((record) => {
            const data = record.data || {};
            const visibility = data.visibility || "owner_only";
            return (
              <Card key={record.id} hover={false} className="overflow-hidden p-0" data-testid={`owner-update-card-${record.id}`}>
                <div className="aspect-[4/3] bg-equine-soft border-b border-equine-hairline overflow-hidden">
                  {data.media_url ? (
                    <img src={data.media_url} alt="" className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-equine-inkSoft">
                      <Image className="w-8 h-8" />
                    </div>
                  )}
                </div>
                <div className="p-5">
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="min-w-0">
                      <div className="font-display text-2xl text-equine-ink truncate">{data.horse_name}</div>
                      <div className="text-[12.5px] text-equine-inkMuted">{data.owner_name || "Owner TBD"} · {fmtDate(record.created_at)}</div>
                    </div>
                    <StatusPill tone={VISIBILITY_TONE[visibility]}>{visibility.replace(/_/g, " ")}</StatusPill>
                  </div>
                  {data.caption && <div className="text-[13.5px] text-equine-ink leading-relaxed">{data.caption}</div>}
                  <div className="hairline mt-4 pt-3 flex items-center justify-between gap-3">
                    <span className="text-[11px] text-equine-inkSoft truncate">{data.media_url || "No media URL"}</span>
                    <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink">
                      Archive
                    </button>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add owner update"
        eyebrow="Communication"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/owner-updates/records"
        initialValues={{ visibility: "owner_only" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save update"
        testidPrefix="owner-updates-add"
        onCreated={load}
      />
    </div>
  );
}
