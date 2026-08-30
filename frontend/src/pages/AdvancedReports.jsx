import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, BarChart3, Download, FileSpreadsheet, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";

const fmtMoney = (value) => {
  const n = Number(value || 0);
  return n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
};

const csvCell = (value) => `"${String(value ?? "").replace(/"/g, '""')}"`;

const downloadBlob = (content, filename, type) => {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
};

const manifestToCsv = (manifest) => {
  const columns = manifest.columns || [];
  const rows = manifest.rows || [];
  return [
    columns.join(","),
    ...rows.map((row) => (
      columns.map((column) => (
        column === "data" ? JSON.stringify(row.data || {}) : row[column]
      )).map(csvCell).join(",")
    )),
  ].join("\n");
};

export default function AdvancedReports() {
  const [dashboard, setDashboard] = useState(null);
  const [modules, setModules] = useState([]);
  const [selected, setSelected] = useState(["stall-map", "payments", "health-reminders"]);
  const [reportName, setReportName] = useState("Monthly barn performance");
  const [filters, setFilters] = useState("{}");
  const [definition, setDefinition] = useState(null);
  const [exportManifest, setExportManifest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [building, setBuilding] = useState(false);
  const [exportingFormat, setExportingFormat] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [dashboardRes, modulesRes] = await Promise.all([
        api.get("/reports/backlog-dashboard"),
        api.get("/feature-modules"),
      ]);
      setDashboard(dashboardRes.data);
      setModules(Array.isArray(modulesRes.data) ? modulesRes.data : modulesRes.data.modules || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load advanced reports.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const occupancyPct = useMemo(() => {
    const occupied = dashboard?.occupancy?.occupied || 0;
    const total = dashboard?.occupancy?.total_stalls || 0;
    return total ? Math.round((occupied / total) * 100) : 0;
  }, [dashboard]);

  const toggleModule = (key) => {
    setSelected((current) => (
      current.includes(key)
        ? current.filter((item) => item !== key)
        : [...current, key]
    ));
  };

  const reportPayload = () => {
    if (!reportName.trim()) {
      toast.error("Report name is required");
      return null;
    }
    if (!selected.length) {
      toast.error("Choose at least one data source");
      return null;
    }
    let parsedFilters = {};
    try {
      parsedFilters = filters.trim() ? JSON.parse(filters) : {};
    } catch {
      toast.error("Filters must be valid JSON");
      return null;
    }
    return {
      name: reportName,
      module_keys: selected,
      filters: parsedFilters,
    };
  };

  const buildReport = async (event) => {
    event?.preventDefault();
    const payload = reportPayload();
    if (!payload) {
      return;
    }
    setBuilding(true);
    try {
      const r = await api.post("/reports/custom-builder", payload);
      setDefinition(r.data);
      toast.success("Report definition validated");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not build report");
    } finally {
      setBuilding(false);
    }
  };

  const exportReport = async (format) => {
    const payload = reportPayload();
    if (!payload) {
      return;
    }
    setExportingFormat(format);
    try {
      const r = await api.post("/reports/export", { ...payload, format });
      const manifest = r.data;
      setExportManifest(manifest);
      if (manifest.download_format === "csv") {
        downloadBlob(manifestToCsv(manifest), manifest.filename, "text/csv;charset=utf-8");
      } else {
        downloadBlob(JSON.stringify(manifest, null, 2), manifest.filename, "application/json;charset=utf-8");
      }
      toast.success(`${format.toUpperCase()} export manifest prepared`);
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare export");
    } finally {
      setExportingFormat(null);
    }
  };

  return (
    <div data-testid="advanced-reports-page">
      <PageHeader
        eyebrow="Reporting"
        title="Barn Performance Reports"
        subtitle="Occupancy, revenue, health trends, trainer performance inputs, custom report definitions, and export manifests."
        action={
          <div className="flex items-center gap-3">
            <button onClick={() => exportReport("xlsx")} disabled={exportingFormat === "xlsx"} className="btn-secondary inline-flex items-center gap-2 disabled:opacity-50" data-testid="advanced-reports-export-xlsx">
              <FileSpreadsheet className="w-4 h-4" /> {exportingFormat === "xlsx" ? "Preparing" : "Excel manifest"}
            </button>
            <button onClick={() => exportReport("pdf")} disabled={exportingFormat === "pdf"} className="btn-secondary inline-flex items-center gap-2 disabled:opacity-50" data-testid="advanced-reports-export-pdf">
              <Download className="w-4 h-4" /> {exportingFormat === "pdf" ? "Preparing" : "PDF manifest"}
            </button>
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="advanced-reports-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
          </div>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading reports...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Advanced reports unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : !dashboard ? (
        <Empty>
          <BarChart3 strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No report data yet</div>
          <div className="text-[13px] text-equine-platinum/60">Seed or create records to populate reporting dashboards.</div>
        </Empty>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5 mb-6">
            <Metric label="Occupancy" value={`${occupancyPct}%`} caption={`${dashboard.occupancy.occupied}/${dashboard.occupancy.total_stalls} stalls`} />
            <Metric label="Revenue" value={fmtMoney(dashboard.financial.revenue)} caption="Non-void invoices" />
            <Metric label="Profit / loss" value={fmtMoney(dashboard.financial.profit_loss)} caption={`${fmtMoney(dashboard.financial.expenses)} expenses`} />
            <Metric label="Health due" value={dashboard.health.due_or_expired} caption="Due or expired reminders" />
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
            <Card hover={false} className="xl:col-span-2">
              <div className="label-eyebrow mb-2">Executive snapshot</div>
              <h2 className="font-display text-3xl text-equine-ink mb-5">Current barn signals</h2>
              <Bar label="Occupancy" value={occupancyPct} />
              <Bar label="Revenue vs expenses" value={dashboard.financial.revenue ? Math.max(0, Math.min(100, Math.round((dashboard.financial.profit_loss / dashboard.financial.revenue) * 100))) : 0} />
              <Bar label="Health readiness" value={dashboard.health.due_or_expired ? 35 : 100} invert={dashboard.health.due_or_expired > 0} />
              <div className="hairline mt-5 pt-4 flex flex-wrap gap-2">
                <StatusPill tone="info">Excel manifest {dashboard.exports.excel.replace(/_/g, " ")}</StatusPill>
                <StatusPill tone="info">PDF manifest {dashboard.exports.pdf.replace(/_/g, " ")}</StatusPill>
              </div>
            </Card>

            <Card hover={false} className="xl:col-span-3">
              <form onSubmit={buildReport} data-testid="custom-report-builder">
                <div className="flex items-start justify-between gap-4 mb-5">
                  <div>
                    <div className="label-eyebrow mb-2">Custom builder</div>
                    <h2 className="font-display text-3xl text-equine-ink">Report definition</h2>
                  </div>
                  <button type="submit" disabled={building} className="btn-primary inline-flex items-center gap-2 disabled:opacity-50" data-testid="custom-report-submit">
                    <Plus className="w-4 h-4" /> {building ? "Building..." : "Build"}
                  </button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-5">
                  <label className="block">
                    <div className="label-eyebrow-muted mb-1.5">Name</div>
                    <input value={reportName} onChange={(e) => setReportName(e.target.value)} className="w-full bg-white border border-equine-cloud rounded-lg px-3 py-2.5 text-equine-ink outline-none focus:border-equine-lilac" data-testid="custom-report-name" />
                  </label>
                  <label className="block">
                    <div className="label-eyebrow-muted mb-1.5">Filters JSON</div>
                    <input value={filters} onChange={(e) => setFilters(e.target.value)} className="w-full bg-white border border-equine-cloud rounded-lg px-3 py-2.5 text-equine-ink outline-none focus:border-equine-lilac" data-testid="custom-report-filters" />
                  </label>
                </div>

                <div className="label-eyebrow-muted mb-2">Data sources</div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-72 overflow-y-auto pr-1">
                  {modules.map((module) => (
                    <label key={module.key} className="flex items-center gap-3 rounded-lg border border-equine-cloud bg-white/70 px-3 py-2.5 text-[13px] text-equine-ink">
                      <input
                        type="checkbox"
                        checked={selected.includes(module.key)}
                        onChange={() => toggleModule(module.key)}
                        className="accent-equine-lilac"
                        data-testid={`custom-report-source-${module.key}`}
                      />
                      <span className="flex-1">{module.label}</span>
                      <span className="text-[11px] text-equine-inkSoft">{module.group}</span>
                    </label>
                  ))}
                </div>
              </form>

              {definition && (
                <div className="hairline mt-5 pt-4" data-testid="custom-report-definition">
                  <div className="flex items-center justify-between gap-3 mb-2">
                    <div className="font-display text-2xl text-equine-ink">{definition.name}</div>
                    <StatusPill tone="success">{definition.status.replace(/_/g, " ")}</StatusPill>
                  </div>
                  <div className="text-[12.5px] text-equine-inkMuted mb-2">{definition.collections.join(" - ")}</div>
                  <div className="text-[12px] text-equine-inkSoft">Export manifests: {definition.export_formats.join(", ")}</div>
                </div>
              )}

              {exportManifest && (
                <div className="hairline mt-5 pt-4" data-testid="custom-report-export-manifest">
                  <div className="flex items-center justify-between gap-3 mb-2">
                    <div className="font-display text-2xl text-equine-ink">{exportManifest.filename}</div>
                    <StatusPill tone="info">{exportManifest.row_count} rows</StatusPill>
                  </div>
                  <div className="text-[12.5px] text-equine-inkMuted">
                    {exportManifest.format.toUpperCase()} manifest generated from {exportManifest.module_keys.length} data source(s).
                  </div>
                </div>
              )}
            </Card>
          </div>
        </>
      )}
    </div>
  );
}

const Metric = ({ label, value, caption }) => (
  <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
    <div className="label-eyebrow-muted mb-2">{label}</div>
    <div className="font-display text-4xl text-equine-ink leading-none">{value}</div>
    {caption && <div className="text-[12px] text-equine-inkMuted mt-2">{caption}</div>}
  </div>
);

const Bar = ({ label, value, invert }) => (
  <div className="mb-4">
    <div className="flex items-center justify-between mb-1">
      <div className="text-[12.5px] text-equine-inkMuted">{label}</div>
      <div className="text-[12.5px] text-equine-ink">{value}%</div>
    </div>
    <div className="h-3 rounded-full bg-equine-cloud overflow-hidden">
      <div
        className={`h-full rounded-full ${invert ? "bg-equine-amber" : "bg-equine-lilac"}`}
        style={{ width: `${Math.max(0, Math.min(100, value))}%` }}
      />
    </div>
  </div>
);
