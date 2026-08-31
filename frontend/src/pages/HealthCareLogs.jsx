import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CalendarClock, HeartPulse, Pill, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const FARrier_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Horse name" },
  { key: "farrier_name", label: "Farrier", placeholder: "Provider name" },
  { key: "scheduled_at", label: "Scheduled", placeholder: "YYYY-MM-DDTHH:MM:SS" },
  { key: "completed_at", label: "Completed", placeholder: "YYYY-MM-DDTHH:MM:SS" },
  { key: "service_type", label: "Service", kind: "select", opts: ["trim", "front_shoes", "full_set", "reset", "therapeutic"] },
  { key: "status", label: "Status", kind: "select", opts: ["scheduled", "complete", "missed", "follow_up"] },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const MED_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Horse name" },
  { key: "medication_name", label: "Medication", required: true, placeholder: "Medication name" },
  { key: "dosage", label: "Dosage", placeholder: "Dosage" },
  { key: "administered_at", label: "Administered", placeholder: "YYYY-MM-DDTHH:MM:SS" },
  { key: "administered_by", label: "Administered by", placeholder: "Staff name" },
  { key: "status", label: "Status", kind: "select", opts: ["scheduled", "administered", "missed", "held"] },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const INJURY_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Horse name" },
  { key: "case_title", label: "Case", required: true, placeholder: "Observation summary", full: true },
  { key: "severity", label: "Severity", kind: "select", opts: ["watch", "mild", "moderate", "urgent"] },
  { key: "observed_at", label: "Observed", placeholder: "YYYY-MM-DDTHH:MM:SS" },
  { key: "status", label: "Status", kind: "select", opts: ["open", "monitoring", "vet_called", "resolved"] },
  { key: "care_plan", label: "Care plan", kind: "textarea", rows: 3, full: true },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const STATUS_TONE = {
  scheduled: "info",
  complete: "success",
  administered: "success",
  missed: "critical",
  held: "warning",
  follow_up: "warning",
  open: "info",
  monitoring: "warning",
  vet_called: "critical",
  resolved: "success",
  watch: "info",
  mild: "warning",
  moderate: "warning",
  urgent: "critical",
};

const labelFor = (value) => String(value || "").replace(/_/g, " ");
const fmt = (value) => {
  if (!value) return "TBD";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
};

export default function HealthCareLogs() {
  const [farrier, setFarrier] = useState([]);
  const [meds, setMeds] = useState([]);
  const [injuries, setInjuries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sheet, setSheet] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [farrierRes, medsRes, injuryRes] = await Promise.all([
        api.get("/feature-modules/farrier-history"),
        api.get("/feature-modules/medication-logs"),
        api.get("/feature-modules/injury-tracking"),
      ]);
      setFarrier(farrierRes.data.records || []);
      setMeds(medsRes.data.records || []);
      setInjuries(injuryRes.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load health care logs.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const stats = useMemo(() => ({
    farrierDue: farrier.filter((record) => ((record.data || {}).status || "scheduled") === "scheduled").length,
    medsOpen: meds.filter((record) => !["administered", "held"].includes((record.data || {}).status || "scheduled")).length,
    injuryOpen: injuries.filter((record) => !["resolved"].includes((record.data || {}).status || "open")).length,
  }), [farrier, meds, injuries]);

  const updateStatus = async (moduleKey, record, status) => {
    try {
      await api.patch(`/feature-modules/${moduleKey}/records/${record.id}`, { data: { status } });
      toast.success("Health log updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update health log");
    }
  };

  const archiveRecord = async (moduleKey, record) => {
    try {
      await api.delete(`/feature-modules/${moduleKey}/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive health log");
    }
  };

  const sheetConfig = {
    farrier: {
      title: "Add farrier record",
      fields: FARrier_FIELDS,
      endpoint: "/feature-modules/farrier-history/records",
      initialValues: { service_type: "trim", status: "scheduled" },
      testidPrefix: "farrier-history-add",
    },
    meds: {
      title: "Add medication log",
      fields: MED_FIELDS,
      endpoint: "/feature-modules/medication-logs/records",
      initialValues: { status: "administered", administered_at: new Date().toISOString().slice(0, 16) },
      testidPrefix: "medication-log-add",
    },
    injury: {
      title: "Add injury case",
      fields: INJURY_FIELDS,
      endpoint: "/feature-modules/injury-tracking/records",
      initialValues: { severity: "watch", status: "open", observed_at: new Date().toISOString().slice(0, 16) },
      testidPrefix: "injury-tracking-add",
    },
  }[sheet];

  return (
    <div data-testid="health-care-logs-page">
      <PageHeader
        eyebrow="Health"
        title="Health Care Logs"
        subtitle="Farrier history, medication administration, and injury or lameness tracking with audit-friendly records."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="health-care-logs-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setSheet("injury")} className="btn-primary inline-flex items-center gap-2" data-testid="health-care-logs-add-injury">
              <Plus className="w-4 h-4" /> Add case
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-3 gap-4 mb-6">
        <Metric label="Farrier scheduled" value={stats.farrierDue} />
        <Metric label="Med actions open" value={stats.medsOpen} />
        <Metric label="Active cases" value={stats.injuryOpen} />
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading health care logs...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Health care logs unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
          <LogColumn
            title="Farrier"
            icon={CalendarClock}
            records={farrier}
            emptyText="No farrier records."
            onAdd={() => setSheet("farrier")}
            render={(record) => {
              const data = record.data || {};
              const status = data.status || "scheduled";
              return (
                <LogCard
                  key={record.id}
                  title={data.horse_name}
                  subtitle={`${data.farrier_name || "Farrier TBD"} - ${labelFor(data.service_type || "trim")}`}
                  meta={`Scheduled ${fmt(data.scheduled_at)}`}
                  status={status}
                  notes={data.notes}
                  onPrimary={() => updateStatus("farrier-history", record, "complete")}
                  primaryLabel="Complete"
                  onArchive={() => archiveRecord("farrier-history", record)}
                />
              );
            }}
          />
          <LogColumn
            title="Medication Logs"
            icon={Pill}
            records={meds}
            emptyText="No medication administration logs."
            onAdd={() => setSheet("meds")}
            render={(record) => {
              const data = record.data || {};
              const status = data.status || "scheduled";
              return (
                <LogCard
                  key={record.id}
                  title={data.medication_name}
                  subtitle={`${data.horse_name} - ${data.dosage || "Dose TBD"}`}
                  meta={`${data.administered_by || "Staff TBD"} - ${fmt(data.administered_at)}`}
                  status={status}
                  notes={data.notes}
                  onPrimary={() => updateStatus("medication-logs", record, "administered")}
                  primaryLabel="Administered"
                  onArchive={() => archiveRecord("medication-logs", record)}
                />
              );
            }}
          />
          <LogColumn
            title="Injury & Lameness"
            icon={HeartPulse}
            records={injuries}
            emptyText="No injury or lameness cases."
            onAdd={() => setSheet("injury")}
            render={(record) => {
              const data = record.data || {};
              const status = data.status || "open";
              return (
                <LogCard
                  key={record.id}
                  title={data.case_title}
                  subtitle={`${data.horse_name} - ${labelFor(data.severity || "watch")}`}
                  meta={`Observed ${fmt(data.observed_at)}`}
                  status={status}
                  notes={data.care_plan || data.notes}
                  onPrimary={() => updateStatus("injury-tracking", record, "resolved")}
                  primaryLabel="Resolve"
                  onArchive={() => archiveRecord("injury-tracking", record)}
                />
              );
            }}
          />
        </div>
      )}

      {sheetConfig && (
        <QuickAddSheet
          open={Boolean(sheet)}
          onClose={() => setSheet(null)}
          title={sheetConfig.title}
          eyebrow="Health"
          fields={sheetConfig.fields}
          endpoint={sheetConfig.endpoint}
          initialValues={sheetConfig.initialValues}
          transform={(form) => ({ data: form })}
          submitLabel="Save log"
          testidPrefix={sheetConfig.testidPrefix}
          onCreated={load}
        />
      )}
    </div>
  );
}

const Metric = ({ label, value }) => (
  <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
    <div className="label-eyebrow-muted mb-2">{label}</div>
    <div className="font-display text-4xl text-equine-ink leading-none">{value}</div>
  </div>
);

const LogColumn = ({ title, icon: Icon, records, emptyText, onAdd, render }) => (
  <Card hover={false}>
    <div className="flex items-center justify-between mb-4">
      <div className="flex items-center gap-2">
        <Icon className="w-4 h-4 text-equine-icy" />
        <h2 className="font-display text-2xl text-equine-ink">{title}</h2>
      </div>
      <button type="button" onClick={onAdd} className="btn-secondary text-[12px] py-2 px-4">
        Add
      </button>
    </div>
    <div className="space-y-3">
      {records.length === 0 ? (
        <div className="rounded-xl border border-dashed border-equine-cloud bg-white/45 py-8 text-center text-[13px] text-equine-inkMuted">
          {emptyText}
        </div>
      ) : records.map(render)}
    </div>
  </Card>
);

const LogCard = ({ title, subtitle, meta, status, notes, onPrimary, primaryLabel, onArchive }) => (
  <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
    <div className="flex items-start justify-between gap-3 mb-2">
      <div className="min-w-0">
        <div className="font-display text-xl text-equine-ink truncate">{title}</div>
        <div className="text-[12.5px] text-equine-inkMuted">{subtitle}</div>
      </div>
      <StatusPill tone={STATUS_TONE[status] || "info"}>{labelFor(status)}</StatusPill>
    </div>
    <div className="text-[12px] text-equine-inkSoft">{meta}</div>
    {notes && <div className="text-[13px] text-equine-inkMuted mt-2">{notes}</div>}
    <div className="hairline mt-3 pt-3 flex items-center gap-2">
      <button type="button" onClick={onPrimary} className="btn-primary text-[12px] py-2 px-4">{primaryLabel}</button>
      <button type="button" onClick={onArchive} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">Archive</button>
    </div>
  </div>
);
