import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, PhoneCall, Plus, RefreshCw, ShieldAlert } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const WORKFLOW_STATUSES = ["open", "stabilizing", "resolved", "closed"];
const STATUS_TONE = { open: "critical", stabilizing: "warning", resolved: "success", closed: "neutral" };

const ADD_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Valentino" },
  { key: "emergency_type", label: "Type", kind: "select", opts: ["colic", "injury", "cast", "transport", "weather", "other"] },
  { key: "primary_contact", label: "Primary contact", placeholder: "Charlotte Vance" },
  { key: "vet_status", label: "Vet", kind: "select", opts: ["not_called", "called", "en_route", "on_site", "complete"] },
  { key: "owner_status", label: "Owner", kind: "select", opts: ["not_contacted", "left_message", "confirmed", "authorized"] },
  { key: "workflow_status", label: "Status", kind: "select", opts: WORKFLOW_STATUSES },
  { key: "started_at", label: "Started", placeholder: "2026-06-10T16:20:00" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 4, full: true },
];

const labelFor = (value) => String(value || "").replace(/_/g, " ");
const fmtDateTime = (value) => {
  if (!value) return "No time";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
};

export default function EmergencyWorkflows() {
  const [records, setRecords] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [workflowRes, contactRes] = await Promise.all([
        api.get("/feature-modules/emergency-workflows"),
        api.get("/feature-modules/emergency-contacts"),
      ]);
      setRecords(workflowRes.data.records || []);
      setContacts(contactRes.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load emergency workflows.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const grouped = useMemo(() => {
    const out = Object.fromEntries(WORKFLOW_STATUSES.map((status) => [status, []]));
    records.forEach((record) => {
      const status = (record.data || {}).workflow_status || "open";
      (out[status] || out.open).push(record);
    });
    Object.values(out).forEach((rows) => rows.sort((a, b) => String(b.created_at || "").localeCompare(String(a.created_at || ""))));
    return out;
  }, [records]);

  const contactLookup = useMemo(() => {
    const map = {};
    contacts.forEach((record) => {
      const data = record.data || {};
      if (data.person_name) map[data.person_name] = data;
      if (data.horse_name && !map[data.horse_name]) map[data.horse_name] = data;
    });
    return map;
  }, [contacts]);

  const updateRecord = async (record, data) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/emergency-workflows/records/${record.id}`, { data });
      toast.success("Emergency workflow updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update workflow");
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/emergency-workflows/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive workflow");
    }
  };

  return (
    <div data-testid="emergency-workflows-page">
      <PageHeader
        eyebrow="Communication"
        title="Emergency Workflows"
        subtitle="Track emergency type, owner authorization, vet status, primary contact, and resolution notes during urgent incidents."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="emergency-workflows-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="emergency-workflows-add">
              <Plus className="w-4 h-4" /> Start workflow
            </button>
          </div>
        }
      />

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading emergency workflows...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Emergency workflows unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <ShieldAlert strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No emergency workflows</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Start a workflow when an urgent contact chain or vet call needs tracking.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="emergency-workflows-empty-add">
            <Plus className="w-4 h-4" /> Start first workflow
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-4">
          {WORKFLOW_STATUSES.map((status) => (
            <Card key={status} hover={false} className="p-4" data-testid={`emergency-workflows-${status}`}>
              <div className="flex items-center justify-between mb-3">
                <div className="label-eyebrow capitalize">{labelFor(status)}</div>
                <StatusPill tone={STATUS_TONE[status]}>{grouped[status].length}</StatusPill>
              </div>
              <div className="space-y-3">
                {grouped[status].map((record) => {
                  const data = record.data || {};
                  const contact = contactLookup[data.primary_contact] || contactLookup[data.horse_name] || {};
                  return (
                    <div key={record.id} className={`rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 ${savingId === record.id ? "opacity-60" : ""}`} data-testid={`emergency-workflow-card-${record.id}`}>
                      <div className="font-display text-xl leading-none text-equine-ink">{data.horse_name}</div>
                      <div className="text-[12px] text-equine-inkMuted mt-2 capitalize">
                        {labelFor(data.emergency_type || "other")} - {fmtDateTime(data.started_at)}
                      </div>
                      <div className="grid grid-cols-2 gap-2 mt-3">
                        <MiniStatus label="Owner" value={data.owner_status || "not_contacted"} />
                        <MiniStatus label="Vet" value={data.vet_status || "not_called"} />
                      </div>
                      {contact.phone && (
                        <a href={`tel:${contact.phone}`} className="mt-3 inline-flex items-center gap-1 text-[12px] text-equine-navy hover:text-equine-saddle">
                          <PhoneCall className="w-3.5 h-3.5" /> {contact.phone}
                        </a>
                      )}
                      {data.notes && <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{data.notes}</div>}
                      <div className="hairline mt-3 pt-3 flex flex-wrap items-center gap-2">
                        {data.owner_status !== "authorized" && (
                          <button type="button" onClick={() => updateRecord(record, { owner_status: "authorized" })} className="text-[12px] text-equine-navy hover:text-equine-saddle">
                            Owner authorized
                          </button>
                        )}
                        {data.vet_status !== "on_site" && data.vet_status !== "complete" && (
                          <button type="button" onClick={() => updateRecord(record, { vet_status: "on_site" })} className="text-[12px] text-equine-navy hover:text-equine-saddle">
                            Vet on site
                          </button>
                        )}
                        {status !== "resolved" && (
                          <button type="button" onClick={() => updateRecord(record, { workflow_status: "resolved", vet_status: "complete" })} className="text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1">
                            <CheckCircle2 className="w-3.5 h-3.5" /> Resolve
                          </button>
                        )}
                        <button type="button" onClick={() => archiveRecord(record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">
                          Archive
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          ))}
        </div>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Start emergency workflow"
        eyebrow="Communication"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/emergency-workflows/records"
        initialValues={{
          emergency_type: "injury",
          vet_status: "not_called",
          owner_status: "not_contacted",
          workflow_status: "open",
          started_at: new Date().toISOString().slice(0, 16),
        }}
        transform={(form) => ({ data: form })}
        submitLabel="Start workflow"
        testidPrefix="emergency-workflows-add"
        onCreated={load}
      />
    </div>
  );
}

const MiniStatus = ({ label, value }) => (
  <div className="rounded-lg border border-equine-cloud bg-white/60 p-2">
    <div className="label-eyebrow-muted mb-1">{label}</div>
    <div className="text-[12px] text-equine-ink capitalize">{labelFor(value)}</div>
  </div>
);
