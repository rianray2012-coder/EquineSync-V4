import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Plus, RefreshCw, Layers, AlertTriangle, Plug } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const fieldToQuickAdd = (field) => {
  const out = {
    key: field.key,
    label: field.label,
    required: field.required,
    placeholder: field.placeholder,
    full: field.type === "textarea",
  };
  if (field.type === "select") {
    out.kind = "select";
    out.opts = field.options || [];
  } else if (field.type === "textarea") {
    out.kind = "textarea";
    out.rows = 4;
  } else {
    out.type = field.type === "number" ? "number" : field.type;
  }
  return out;
};

const valueLabel = (value) => {
  if (value === undefined || value === null || value === "") return "—";
  if (Array.isArray(value)) return value.join(", ");
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
};

const moduleSubtitle = (module) => {
  const features = module?.features || [];
  if (features.length === 0) return "Add records now; deeper automation can be layered in safely later.";
  return features.join(" · ");
};

export default function FeatureWorkspace({ moduleKey, fallbackTitle, icon: Icon = Layers }) {
  const [module, setModule] = useState(null);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [integrations, setIntegrations] = useState([]);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get(`/feature-modules/${moduleKey}`);
      setModule(r.data.module);
      setRecords(r.data.records || []);
      if (moduleKey === "integrations") {
        const p = await api.get("/integrations/placeholders");
        setIntegrations(p.data || []);
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load this workspace.");
    } finally {
      setLoading(false);
    }
  }, [moduleKey]);

  useEffect(() => { load(); }, [load]);

  const fields = useMemo(() => (module?.fields || []).map(fieldToQuickAdd), [module]);
  const primaryFields = (module?.fields || []).slice(0, 4);
  const title = module?.label || fallbackTitle || "Feature Workspace";

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/${moduleKey}/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive record");
    }
  };

  const prepareIntegration = async (provider) => {
    try {
      const r = await api.post(`/integrations/${provider}/prepare`);
      toast.success(r.data.message || "Configuration ready");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare integration");
    }
  };

  return (
    <div data-testid={`feature-${moduleKey}`}>
      <PageHeader
        eyebrow={module?.group || "Feature Backlog"}
        title={title}
        subtitle={moduleSubtitle(module)}
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="feature-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button
              onClick={() => setAddOpen(true)}
              disabled={!module || loading}
              data-testid="feature-add"
              className="btn-primary inline-flex items-center gap-2 disabled:opacity-50"
            >
              <Plus className="w-4 h-4" /> Add
            </button>
          </div>
        }
      />

      {module?.placeholder && (
        <Card hover={false} className="mb-6 border-equine-brass/30 bg-equine-brass/5" data-testid="feature-placeholder-note">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-4 h-4 text-equine-champagne mt-0.5 flex-shrink-0" />
            <div className="text-[13px] text-equine-inkMuted leading-relaxed">{module.placeholder}</div>
          </div>
        </Card>
      )}

      {loading ? (
        <Card hover={false}>
          <div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading {title.toLowerCase()}…</div>
        </Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">This workspace is not available.</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <Icon strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No records yet</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Create the first record to activate this workflow shell.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="feature-empty-add">
            <Plus className="w-4 h-4" /> Add first record
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
          {records.map((record) => {
            const data = record.data || {};
            const headingField = primaryFields[0]?.key;
            const heading = valueLabel(data[headingField]) || "Record";
            return (
              <Card key={record.id} hover={false} data-testid={`feature-record-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{heading}</div>
                    <div className="text-[11.5px] text-equine-inkSoft mt-0.5">
                      Updated {fmtDate(record.updated_at)} · Created by {record.created_by || "—"}
                    </div>
                  </div>
                  <StatusPill tone="neutral">{module.group}</StatusPill>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {primaryFields.map((field) => (
                    <div key={field.key} className={field.type === "textarea" ? "sm:col-span-2" : ""}>
                      <div className="label-eyebrow-muted mb-1">{field.label}</div>
                      <div className="text-[13.5px] text-equine-ink leading-relaxed break-words">{valueLabel(data[field.key])}</div>
                    </div>
                  ))}
                </div>
                <div className="hairline mt-4 pt-3 flex items-center justify-between gap-3">
                  <div className="text-[11px] text-equine-inkSoft truncate">{record.id}</div>
                  <button
                    type="button"
                    onClick={() => archiveRecord(record)}
                    className="text-[12px] text-equine-clay hover:text-equine-ink transition-colors"
                    data-testid={`feature-archive-${record.id}`}
                  >
                    Archive
                  </button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {moduleKey === "integrations" && integrations.length > 0 && (
        <Card hover={false} className="mt-6" data-testid="integration-readiness">
          <div className="flex items-center gap-2 mb-4">
            <Plug className="w-4 h-4 text-equine-navy" />
            <h2 className="font-display text-2xl text-equine-ink">Integration readiness</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {integrations.map((item) => (
              <div key={item.provider} className="rounded-xl border border-equine-hairline bg-equine-soft/60 p-4">
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="text-equine-ink capitalize">{item.provider.replace(/_/g, " ")}</div>
                  <StatusPill tone="info">{item.status.replace(/_/g, " ")}</StatusPill>
                </div>
                <div className="text-[12px] text-equine-inkMuted mb-3">{item.ready_for.join(" · ")}</div>
                <button
                  type="button"
                  onClick={() => prepareIntegration(item.provider)}
                  className="btn-secondary text-[12px] py-2 px-4"
                  data-testid={`prepare-${item.provider}`}
                >
                  Prepare
                </button>
              </div>
            ))}
          </div>
        </Card>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title={`Add ${title}`}
        eyebrow={module?.group || "Feature Backlog"}
        fields={fields}
        endpoint={`/feature-modules/${moduleKey}/records`}
        submitLabel="Save record"
        testidPrefix={`feature-${moduleKey}-add`}
        transform={(form) => ({ data: form })}
        onCreated={load}
      />
    </div>
  );
}
