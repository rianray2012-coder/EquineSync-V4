import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, ClipboardList, RefreshCw, ShieldCheck } from "lucide-react";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";

const actionTone = (action) => {
  if (String(action).includes("archived")) return "critical";
  if (String(action).includes("created") || String(action).includes("clocked_in")) return "success";
  if (String(action).includes("prepare")) return "info";
  return "warning";
};

const label = (value) => String(value || "").replace(/_/g, " ");

export default function AuditLog() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [moduleFilter, setModuleFilter] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/audit/backlog");
      setRows(r.data || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load audit log.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const modules = useMemo(() => {
    const keys = rows.map((row) => row.module_key || row.collection).filter(Boolean);
    return ["all", ...Array.from(new Set(keys)).sort()];
  }, [rows]);

  const filtered = useMemo(() => (
    moduleFilter === "all" ? rows : rows.filter((row) => (row.module_key || row.collection) === moduleFilter)
  ), [rows, moduleFilter]);

  return (
    <div data-testid="audit-log-page">
      <PageHeader
        eyebrow="Insights"
        title="Backlog Audit Log"
        subtitle="Recent create, update, archive, portal, and integration-readiness actions across the additive backlog modules."
        action={
          <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="audit-log-refresh">
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        }
      />

      <Card hover={false} className="mb-6 p-4">
        <div className="flex items-center gap-3 overflow-x-auto scrollbar-luxe">
          <ShieldCheck className="w-4 h-4 text-equine-inkSoft flex-shrink-0" />
          {modules.map((key) => (
            <button
              key={key}
              type="button"
              onClick={() => setModuleFilter(key)}
              className={`px-3 py-2 rounded-full text-[12px] border whitespace-nowrap ${
                moduleFilter === key ? "bg-equine-navy text-white border-equine-navy" : "bg-equine-soft text-equine-inkMuted border-equine-hairline hover:text-equine-ink"
              }`}
              data-testid={`audit-filter-${key}`}
            >
              {label(key)}
            </button>
          ))}
        </div>
      </Card>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading audit log…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Audit log unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : filtered.length === 0 ? (
        <Empty>
          <ClipboardList strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No audit events yet</div>
          <div className="text-[13px] text-equine-platinum/60">Backlog changes will appear here after staff create, update, archive, sign, clock, or prepare records.</div>
        </Empty>
      ) : (
        <Card hover={false} data-testid="audit-log-list">
          <div className="space-y-3">
            {filtered.map((row) => (
              <div key={row.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`audit-log-row-${row.id}`}>
                <div className="flex items-start justify-between gap-3 flex-wrap">
                  <div>
                    <div className="font-display text-xl text-equine-ink capitalize">{label(row.action)}</div>
                    <div className="text-[12.5px] text-equine-inkMuted">
                      {row.actor_name || "Unknown actor"} · {label(row.actor_role)} · {fmtDate(row.created_at)}
                    </div>
                  </div>
                  <StatusPill tone={actionTone(row.action)}>{label(row.module_key || row.collection)}</StatusPill>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-3 mt-3 text-[12px]">
                  <AuditMeta label="Record" value={row.record_id || "none"} />
                  <AuditMeta label="Collection" value={row.collection || "none"} />
                  <AuditMeta label="Action ID" value={row.id} />
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

const AuditMeta = ({ label, value }) => (
  <div className="rounded-lg border border-equine-hairline bg-white/50 p-3 min-w-0">
    <div className="label-eyebrow-muted mb-1">{label}</div>
    <div className="text-[12px] text-equine-ink truncate">{value}</div>
  </div>
);
