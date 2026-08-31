import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CalendarDays, CheckCircle2, Download, Plus, Plug, RefreshCw, Wrench } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const PROVIDERS = ["quickbooks", "stripe", "google_calendar", "push_notifications", "wearables", "document_scanning", "qr_horse_id"];
const STATUSES = ["not_configured", "ready", "connected", "paused"];
const STATUS_TONE = { not_configured: "neutral", ready: "info", connected: "success", paused: "warning" };

const ADD_FIELDS = [
  { key: "provider", label: "Provider", kind: "select", opts: PROVIDERS },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "external_ref", label: "External ref", placeholder: "Account or connection id" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 4, full: true },
];

const labelFor = (value) => String(value || "").replace(/_/g, " ");

export default function Integrations() {
  const [records, setRecords] = useState([]);
  const [readinessItems, setReadinessItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingProvider, setSavingProvider] = useState(null);
  const [calendarExporting, setCalendarExporting] = useState(false);
  const [calendarManifest, setCalendarManifest] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [moduleRes, readinessRes] = await Promise.all([
        api.get("/feature-modules/integrations"),
        api.get("/integrations/placeholders"),
      ]);
      setRecords(moduleRes.data.records || []);
      setReadinessItems(readinessRes.data || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load integrations.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const connectedByProvider = useMemo(() => Object.fromEntries(records.map((record) => [(record.data || {}).provider, record])), [records]);

  const prepareIntegration = async (provider) => {
    setSavingProvider(provider);
    try {
      const r = await api.post(`/integrations/${provider}/prepare`);
      toast.success(r.data.message || "Configuration ready");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare integration");
    } finally {
      setSavingProvider(null);
    }
  };

  const exportCalendar = async () => {
    setCalendarExporting(true);
    try {
      const r = await api.post("/integrations/google-calendar/export", {
        sources: ["competitions", "staff-scheduling", "health-reminders"],
      });
      const manifest = r.data;
      setCalendarManifest(manifest);
      const blob = new Blob([manifest.ics || ""], { type: manifest.content_type || "text/calendar" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = manifest.filename || "equinesync-google-calendar.ics";
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Calendar export prepared");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare calendar export");
    } finally {
      setCalendarExporting(false);
    }
  };

  const setStatus = async (record, status) => {
    try {
      await api.patch(`/feature-modules/integrations/records/${record.id}`, { data: { status } });
      toast.success("Integration status updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update integration");
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/integrations/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive integration");
    }
  };

  return (
    <div data-testid="integrations-page">
      <PageHeader
        eyebrow="Mobile & Integrations"
        title="Integration Readiness"
        subtitle="Track provider readiness for payments, accounting, calendars, push notifications, wearables, scanning, and QR horse identification."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="integrations-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="integrations-add">
              <Plus className="w-4 h-4" /> Add connection
            </button>
          </div>
        }
      />

      <Card hover={false} className="mb-6 border-equine-icy/30 bg-equine-icy/5">
        <div className="flex items-start gap-3">
          <Plug className="w-4 h-4 text-equine-lilac mt-0.5 flex-shrink-0" />
          <div className="text-[13px] text-equine-inkMuted leading-relaxed">
            Credentials and native app tokens are intentionally not stored here. These records define the abstraction layer and readiness state for future provider wiring.
          </div>
        </div>
      </Card>

      {calendarManifest && (
        <Card hover={false} className="mb-6" data-testid="google-calendar-export-manifest">
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <div>
              <div className="label-eyebrow-muted mb-1">Latest calendar export</div>
              <div className="font-display text-2xl text-equine-ink">{calendarManifest.filename}</div>
              <div className="text-[12.5px] text-equine-inkMuted">
                {calendarManifest.event_count} event(s) · {calendarManifest.sources.map(labelFor).join(", ")}
              </div>
            </div>
            <StatusPill tone="success">{labelFor(calendarManifest.status)}</StatusPill>
          </div>
        </Card>
      )}

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading integrations...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Integrations unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
            {readinessItems.map((item) => {
              const record = connectedByProvider[item.provider];
              const status = (record?.data || {}).status || "not_configured";
              return (
                <div key={item.provider} className="rounded-xl border border-equine-cloud bg-white/75 p-5" data-testid={`integration-provider-${item.provider}`}>
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div>
                      <div className="font-display text-2xl text-equine-ink capitalize">{labelFor(item.provider)}</div>
                      <div className="text-[12.5px] text-equine-inkMuted">{item.ready_for.join(" - ")}</div>
                    </div>
                    <StatusPill tone={STATUS_TONE[status] || "info"}>{labelFor(status)}</StatusPill>
                  </div>
                  <div className="text-[12px] text-equine-inkSoft mb-4 capitalize">Provider state: {labelFor(item.status)}</div>
                  <div className="flex flex-wrap items-center gap-2">
                    <button
                      type="button"
                      onClick={() => prepareIntegration(item.provider)}
                      disabled={savingProvider === item.provider}
                      className="btn-secondary text-[12px] py-2 px-4 inline-flex items-center gap-1"
                      data-testid={`integrations-prepare-${item.provider}`}
                    >
                      <Wrench className="w-3.5 h-3.5" /> Prepare
                    </button>
                    {item.provider === "google_calendar" && (
                      <button
                        type="button"
                        onClick={exportCalendar}
                        disabled={calendarExporting}
                        className="btn-secondary text-[12px] py-2 px-4 inline-flex items-center gap-1 disabled:opacity-60"
                        data-testid="integrations-google-calendar-export"
                      >
                        {calendarExporting ? <CalendarDays className="w-3.5 h-3.5" /> : <Download className="w-3.5 h-3.5" />}
                        {calendarExporting ? "Preparing" : "Export ICS"}
                      </button>
                    )}
                    {record && status !== "ready" && (
                      <button type="button" onClick={() => setStatus(record, "ready")} className="btn-secondary text-[12px] py-2 px-4">Ready</button>
                    )}
            {record && status !== "connected" && (
                      <button type="button" onClick={() => setStatus(record, "connected")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5" /> Record connected
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {records.length === 0 ? (
            <Empty>
              <Plug strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
              <div className="font-display text-2xl text-equine-ivory mb-1">No connection records</div>
              <div className="text-[13px] text-equine-platinum/60 mb-4">Add a provider record when a barn is ready to configure credentials with its provider.</div>
              <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="integrations-empty-add">
                <Plus className="w-4 h-4" /> Add first connection
              </button>
            </Empty>
          ) : (
            <Card hover={false} data-testid="integrations-records">
              <div className="space-y-3">
                {records.map((record) => {
                  const data = record.data || {};
                  const status = data.status || "not_configured";
                  return (
                    <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
                      <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                        <div className="flex-1 min-w-0">
                          <div className="font-display text-2xl text-equine-ink capitalize">{labelFor(data.provider)}</div>
                          <div className="text-[12.5px] text-equine-inkMuted">{data.external_ref || "No external reference"}</div>
                          {data.notes && <div className="mt-2 text-[13px] text-equine-inkMuted">{data.notes}</div>}
                        </div>
                        <StatusPill tone={STATUS_TONE[status] || "info"}>{labelFor(status)}</StatusPill>
                        {status !== "paused" && <button type="button" onClick={() => setStatus(record, "paused")} className="btn-secondary text-[12px] py-2 px-4">Pause</button>}
                        <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink px-2">Archive</button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          )}
        </>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add integration connection"
        eyebrow="Mobile & Integrations"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/integrations/records"
        initialValues={{ provider: "stripe", status: "not_configured" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save connection"
        testidPrefix="integrations-add"
        onCreated={load}
      />
    </div>
  );
}
