import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, Download, FileScan, Plus, QrCode, RefreshCw, Smartphone, UploadCloud } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const DRAFT_QUEUE_KEY = "equinesync_offline_action_queue";

const OFFLINE_FIELDS = [
  { key: "action_type", label: "Action", kind: "select", opts: ["create", "update", "complete_task", "upload_document"] },
  { key: "target_module", label: "Target module", required: true, placeholder: "staff-tasks" },
  { key: "payload_summary", label: "Payload summary", required: true, kind: "textarea", rows: 4, full: true },
  { key: "captured_at", label: "Captured", placeholder: "YYYY-MM-DDTHH:MM:SS" },
  { key: "sync_status", label: "Status", kind: "select", opts: ["queued", "ready", "synced", "failed"] },
];

const SCAN_FIELDS = [
  { key: "document_type", label: "Type", kind: "select", opts: ["receipt", "coggins", "waiver", "insurance", "other"] },
  { key: "horse_name", label: "Horse", placeholder: "Horse name" },
  { key: "file_url", label: "File URL", required: true, placeholder: "https://..." },
  { key: "linked_module", label: "Linked module", placeholder: "health-documents" },
  { key: "scan_status", label: "Status", kind: "select", opts: ["captured", "reviewed", "attached", "rejected"] },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

const QR_FIELDS = [
  { key: "horse_name", label: "Horse", required: true, placeholder: "Horse name" },
  { key: "qr_code", label: "QR code", required: true, placeholder: "EQSYNC-HORSE-001" },
  { key: "profile_url", label: "Profile URL", placeholder: "/horses/{horse-id}" },
  { key: "stall_location", label: "Stall/location", placeholder: "Stall ID" },
  { key: "status", label: "Status", kind: "select", opts: ["draft", "printed", "active", "retired"] },
];

const STATUS_TONE = {
  queued: "warning",
  ready: "info",
  synced: "success",
  failed: "critical",
  captured: "info",
  reviewed: "warning",
  attached: "success",
  rejected: "critical",
  draft: "info",
  printed: "warning",
  active: "success",
  retired: "neutral",
};

const labelFor = (value) => String(value || "").replace(/_/g, " ");

const loadDraftQueue = () => {
  try {
    return JSON.parse(localStorage.getItem(DRAFT_QUEUE_KEY) || "[]");
  } catch {
    return [];
  }
};

const saveDraftQueue = (rows) => {
  try {
    localStorage.setItem(DRAFT_QUEUE_KEY, JSON.stringify(rows));
  } catch {
    /* local storage can be disabled */
  }
};

export default function MobileReadiness() {
  const [offlineRecords, setOfflineRecords] = useState([]);
  const [scanRecords, setScanRecords] = useState([]);
  const [qrRecords, setQrRecords] = useState([]);
  const [readinessItems, setReadinessItems] = useState([]);
  const [localQueue, setLocalQueue] = useState(() => loadDraftQueue());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sheet, setSheet] = useState(null);
  const [stallCardId, setStallCardId] = useState(null);
  const [stallCardManifest, setStallCardManifest] = useState(null);
  const [scanFile, setScanFile] = useState(null);
  const [scanUploadForm, setScanUploadForm] = useState({ document_type: "receipt", horse_name: "", linked_module: "document-scans", notes: "" });
  const [scanUploadSaving, setScanUploadSaving] = useState(false);
  const [scanUploadIntent, setScanUploadIntent] = useState(null);
  const [scanFileKey, setScanFileKey] = useState(0);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [offlineRes, scanRes, qrRes, readinessRes] = await Promise.all([
        api.get("/feature-modules/offline-sync"),
        api.get("/feature-modules/document-scans"),
        api.get("/feature-modules/qr-horse-id"),
        api.get("/integrations/placeholders"),
      ]);
      setOfflineRecords(offlineRes.data.records || []);
      setScanRecords(scanRes.data.records || []);
      setQrRecords(qrRes.data.records || []);
      setReadinessItems(readinessRes.data || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load mobile readiness.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const readiness = useMemo(() => {
    const lookup = Object.fromEntries(readinessItems.map((item) => [item.provider, item]));
    return ["push_notifications", "wearables", "document_scanning", "qr_horse_id"].map((key) => lookup[key]).filter(Boolean);
  }, [readinessItems]);

  const addLocalOfflineAction = () => {
    const row = {
      id: `local-${Date.now()}`,
      action_type: "complete_task",
      target_module: "staff-tasks",
      payload_summary: "Local action waiting for network sync.",
      captured_at: new Date().toISOString(),
      sync_status: "queued",
    };
    const next = [row, ...localQueue];
    setLocalQueue(next);
    saveDraftQueue(next);
    toast.success("Offline action staged locally");
  };

  const clearLocalQueue = () => {
    setLocalQueue([]);
    saveDraftQueue([]);
    toast.success("Local queue cleared");
  };

  const archiveRecord = async (moduleKey, record) => {
    try {
      await api.delete(`/feature-modules/${moduleKey}/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive record");
    }
  };

  const updateStatus = async (moduleKey, record, key, status) => {
    try {
      await api.patch(`/feature-modules/${moduleKey}/records/${record.id}`, { data: { [key]: status } });
      toast.success("Status updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update status");
    }
  };

  const downloadStallCard = async (record) => {
    setStallCardId(record.id);
    try {
      const r = await api.get(`/integrations/qr-horse-id/${record.id}/stall-card`);
      const manifest = r.data;
      setStallCardManifest(manifest);
      const blob = new Blob([manifest.svg || ""], { type: manifest.content_type || "image/svg+xml" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = manifest.filename || "equinesync-stall-card.svg";
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Stall card prepared");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare stall card");
    } finally {
      setStallCardId(null);
    }
  };

  const prepareScanUpload = async () => {
    if (!scanFile) {
      toast.error("Choose a file first");
      return;
    }
    setScanUploadSaving(true);
    try {
      const intentRes = await api.post("/integrations/document-scans/prepare-upload", {
        filename: scanFile.name,
        mime_type: scanFile.type || "application/pdf",
        byte_size: scanFile.size,
        document_type: scanUploadForm.document_type,
        horse_name: scanUploadForm.horse_name,
        linked_module: scanUploadForm.linked_module,
        notes: scanUploadForm.notes,
      });
      const manifest = intentRes.data;
      if (manifest.upload?.upload_method === "PUT" && manifest.upload?.upload_url) {
        const uploaded = await fetch(manifest.upload.upload_url, {
          method: "PUT",
          headers: { "Content-Type": scanFile.type || "application/octet-stream" },
          body: scanFile,
        });
        if (!uploaded.ok) throw new Error("Storage upload failed");
      }
      await api.post("/feature-modules/document-scans/records", { data: manifest.draft_record });
      setScanUploadIntent(manifest);
      setScanFile(null);
      setScanFileKey((current) => current + 1);
      setScanUploadForm({ document_type: "receipt", horse_name: "", linked_module: "document-scans", notes: "" });
      toast.success("Document scan saved");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || err?.message || "Could not prepare document upload");
    } finally {
      setScanUploadSaving(false);
    }
  };

  const sheetConfig = {
    offline: {
      title: "Add offline action",
      eyebrow: "Mobile & Integrations",
      fields: OFFLINE_FIELDS,
      endpoint: "/feature-modules/offline-sync/records",
      initialValues: { action_type: "complete_task", sync_status: "queued", captured_at: new Date().toISOString().slice(0, 16) },
      submitLabel: "Save action",
      testidPrefix: "offline-sync-add",
    },
    scan: {
      title: "Add document scan",
      eyebrow: "Mobile & Integrations",
      fields: SCAN_FIELDS,
      endpoint: "/feature-modules/document-scans/records",
      initialValues: { document_type: "receipt", scan_status: "captured" },
      submitLabel: "Save scan",
      testidPrefix: "document-scan-add",
    },
    qr: {
      title: "Add QR horse ID",
      eyebrow: "Mobile & Integrations",
      fields: QR_FIELDS,
      endpoint: "/feature-modules/qr-horse-id/records",
      initialValues: { status: "draft" },
      submitLabel: "Save QR ID",
      testidPrefix: "qr-horse-id-add",
    },
  }[sheet];

  return (
    <div data-testid="mobile-readiness-page">
      <PageHeader
        eyebrow="Mobile & Integrations"
        title="Mobile Readiness"
        subtitle="Limited field-recovery queue shape, document scan intake, and stall-card identification workflows for native app handoff."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="mobile-readiness-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={addLocalOfflineAction} className="btn-primary inline-flex items-center gap-2" data-testid="mobile-readiness-stage-local">
              <Plus className="w-4 h-4" /> Stage offline
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-6">
        <Metric label="Offline actions" value={offlineRecords.length + localQueue.length} caption={`${localQueue.length} local`} icon={Smartphone} />
        <Metric label="Document scans" value={scanRecords.length} caption="Intake jobs" icon={FileScan} />
        <Metric label="QR IDs" value={qrRecords.length} caption="Horse identifiers" icon={QrCode} />
        <Metric label="Readiness hooks" value={readiness.length} caption="Provider setup" icon={UploadCloud} />
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading mobile readiness...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Mobile readiness unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : (
        <div className="space-y-6">
          <Card hover={false}>
            <div className="flex items-start justify-between gap-4 mb-5">
              <div>
                <div className="label-eyebrow mb-2">Limited field recovery</div>
                <h2 className="font-display text-3xl text-equine-ink">Sync queue</h2>
              </div>
              <div className="flex items-center gap-2">
                {localQueue.length > 0 && <button type="button" onClick={clearLocalQueue} className="btn-secondary text-[12px] py-2 px-4">Clear local</button>}
                <button type="button" onClick={() => setSheet("offline")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                  <Plus className="w-3.5 h-3.5" /> Add
                </button>
              </div>
            </div>
            <div className="space-y-3">
              {localQueue.map((row) => (
                <QueueRow key={row.id} row={row} local />
              ))}
              {offlineRecords.map((record) => (
                <QueueRow
                  key={record.id}
                  row={record.data || {}}
                  onSync={() => updateStatus("offline-sync", record, "sync_status", "synced")}
                  onArchive={() => archiveRecord("offline-sync", record)}
                />
              ))}
              {localQueue.length === 0 && offlineRecords.length === 0 && <SoftEmpty icon={Smartphone} text="No offline actions queued." />}
            </div>
          </Card>

          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
            <Card hover={false}>
              <div className="flex items-start justify-between gap-4 mb-5">
                <div>
                  <div className="label-eyebrow mb-2">Document scanning</div>
                  <h2 className="font-display text-3xl text-equine-ink">Scan intake</h2>
                  {scanUploadIntent && (
                    <div className="text-[12.5px] text-equine-inkMuted mt-1" data-testid="document-upload-intent">
                      Latest upload: {scanUploadIntent.filename} via {labelFor(scanUploadIntent.provider)}
                    </div>
                  )}
                </div>
                <button type="button" onClick={() => setSheet("scan")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                  <Plus className="w-3.5 h-3.5" /> Add
                </button>
              </div>

              <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 mb-4" data-testid="document-upload-panel">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <label className="block">
                    <div className="label-eyebrow-muted mb-1.5">File</div>
                    <input
                      key={scanFileKey}
                      type="file"
                      accept="application/pdf,image/jpeg,image/png"
                      onChange={(event) => setScanFile(event.target.files?.[0] || null)}
                      className="w-full bg-white border border-equine-cloud rounded-lg px-3 py-2.5 text-[13px] text-equine-ink"
                      data-testid="document-upload-file"
                    />
                  </label>
                  <label className="block">
                    <div className="label-eyebrow-muted mb-1.5">Type</div>
                    <select
                      value={scanUploadForm.document_type}
                      onChange={(event) => setScanUploadForm((current) => ({ ...current, document_type: event.target.value }))}
                      className="w-full bg-white border border-equine-cloud rounded-lg px-3 py-2.5 text-[13px] text-equine-ink"
                      data-testid="document-upload-type"
                    >
                      {["receipt", "coggins", "waiver", "insurance", "other"].map((type) => <option key={type} value={type}>{labelFor(type)}</option>)}
                    </select>
                  </label>
                  <label className="block">
                    <div className="label-eyebrow-muted mb-1.5">Horse</div>
                    <input
                      value={scanUploadForm.horse_name}
                      onChange={(event) => setScanUploadForm((current) => ({ ...current, horse_name: event.target.value }))}
                      placeholder="Horse name"
                      className="w-full bg-white border border-equine-cloud rounded-lg px-3 py-2.5 text-[13px] text-equine-ink"
                      data-testid="document-upload-horse"
                    />
                  </label>
                  <label className="block">
                    <div className="label-eyebrow-muted mb-1.5">Linked module</div>
                    <input
                      value={scanUploadForm.linked_module}
                      onChange={(event) => setScanUploadForm((current) => ({ ...current, linked_module: event.target.value }))}
                      className="w-full bg-white border border-equine-cloud rounded-lg px-3 py-2.5 text-[13px] text-equine-ink"
                      data-testid="document-upload-linked-module"
                    />
                  </label>
                  <label className="block md:col-span-2">
                    <div className="label-eyebrow-muted mb-1.5">Notes</div>
                    <textarea
                      value={scanUploadForm.notes}
                      onChange={(event) => setScanUploadForm((current) => ({ ...current, notes: event.target.value }))}
                      rows={2}
                      className="w-full bg-white border border-equine-cloud rounded-lg px-3 py-2.5 text-[13px] text-equine-ink"
                      data-testid="document-upload-notes"
                    />
                  </label>
                </div>
                <div className="mt-3 flex items-center justify-between gap-3 flex-wrap">
                  <div className="text-[12px] text-equine-inkMuted">{scanFile ? `${scanFile.name} · ${Math.round(scanFile.size / 1024)} KB` : "PDF, JPEG, or PNG up to 20 MB."}</div>
                  <button
                    type="button"
                    onClick={prepareScanUpload}
                    disabled={scanUploadSaving}
                    className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1 disabled:opacity-60"
                    data-testid="document-upload-save"
                  >
                    <UploadCloud className="w-3.5 h-3.5" /> {scanUploadSaving ? "Preparing" : "Prepare upload"}
                  </button>
                </div>
              </div>

              <div className="space-y-3">
                {scanRecords.map((record) => {
                  const data = record.data || {};
                  const status = data.scan_status || "captured";
                  return (
                    <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`document-scan-${record.id}`}>
                      <div className="flex items-start justify-between gap-3 mb-2">
                        <div>
                          <div className="font-display text-2xl text-equine-ink capitalize">{labelFor(data.document_type || "document")}</div>
                          <div className="text-[12.5px] text-equine-inkMuted">{data.horse_name || "No horse"} - {data.linked_module || "Unlinked"}</div>
                        </div>
                        <StatusPill tone={STATUS_TONE[status] || "info"}>{labelFor(status)}</StatusPill>
                      </div>
                      <a href={data.file_url} target="_blank" rel="noreferrer" className="text-[12px] text-equine-navy hover:text-equine-lilac break-all">{data.file_url}</a>
                      {data.notes && <div className="text-[13px] text-equine-inkMuted mt-2">{data.notes}</div>}
                      <div className="hairline mt-3 pt-3 flex flex-wrap items-center gap-2">
                        {status !== "reviewed" && <button type="button" onClick={() => updateStatus("document-scans", record, "scan_status", "reviewed")} className="btn-secondary text-[12px] py-2 px-4">Reviewed</button>}
                        {status !== "attached" && <button type="button" onClick={() => updateStatus("document-scans", record, "scan_status", "attached")} className="btn-primary text-[12px] py-2 px-4">Attached</button>}
                        <button type="button" onClick={() => archiveRecord("document-scans", record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">Archive</button>
                      </div>
                    </div>
                  );
                })}
                {scanRecords.length === 0 && <SoftEmpty icon={FileScan} text="No document scans captured." />}
              </div>
            </Card>

            <Card hover={false}>
              <div className="flex items-start justify-between gap-4 mb-5">
              <div>
                  <div className="label-eyebrow mb-2">Stall-card identification</div>
                  <h2 className="font-display text-3xl text-equine-ink">Horse IDs</h2>
                  {stallCardManifest && (
                    <div className="text-[12.5px] text-equine-inkMuted mt-1" data-testid="stall-card-manifest">
                      Latest card: {stallCardManifest.filename}
                    </div>
                  )}
                </div>
                <button type="button" onClick={() => setSheet("qr")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                  <Plus className="w-3.5 h-3.5" /> Add
                </button>
              </div>
              <div className="space-y-3">
                {qrRecords.map((record) => {
                  const data = record.data || {};
                  const status = data.status || "draft";
                  return (
                    <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`qr-horse-id-${record.id}`}>
                      <div className="flex gap-4">
                        <QrPreview code={data.qr_code || record.id} />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-2">
                            <div>
                              <div className="font-display text-2xl text-equine-ink truncate">{data.horse_name}</div>
                              <div className="text-[12.5px] text-equine-inkMuted">{data.stall_location || "No stall"} - {data.profile_url || "No profile URL"}</div>
                            </div>
                            <StatusPill tone={STATUS_TONE[status] || "info"}>{labelFor(status)}</StatusPill>
                          </div>
                          <div className="text-[12px] text-equine-inkSoft mt-2 break-all">{data.qr_code}</div>
                          <div className="hairline mt-3 pt-3 flex flex-wrap items-center gap-2">
                            <button
                              type="button"
                              onClick={() => downloadStallCard(record)}
                              disabled={stallCardId === record.id}
                              className="btn-secondary text-[12px] py-2 px-4 inline-flex items-center gap-1 disabled:opacity-60"
                              data-testid={`qr-stall-card-${record.id}`}
                            >
                              <Download className="w-3.5 h-3.5" /> {stallCardId === record.id ? "Preparing" : "Stall card"}
                            </button>
                            {status !== "printed" && <button type="button" onClick={() => updateStatus("qr-horse-id", record, "status", "printed")} className="btn-secondary text-[12px] py-2 px-4">Printed</button>}
                            {status !== "active" && (
                              <button type="button" onClick={() => updateStatus("qr-horse-id", record, "status", "active")} className="btn-primary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                                <CheckCircle2 className="w-3.5 h-3.5" /> Active
                              </button>
                            )}
                            <button type="button" onClick={() => archiveRecord("qr-horse-id", record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">Archive</button>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
                {qrRecords.length === 0 && <SoftEmpty icon={QrCode} text="No QR horse IDs created." />}
              </div>
            </Card>
          </div>
        </div>
      )}

      {sheetConfig && (
        <QuickAddSheet
          open={Boolean(sheet)}
          onClose={() => setSheet(null)}
          title={sheetConfig.title}
          eyebrow={sheetConfig.eyebrow}
          fields={sheetConfig.fields}
          endpoint={sheetConfig.endpoint}
          initialValues={sheetConfig.initialValues}
          transform={(form) => ({ data: form })}
          submitLabel={sheetConfig.submitLabel}
          testidPrefix={sheetConfig.testidPrefix}
          onCreated={load}
        />
      )}
    </div>
  );
}

const Metric = ({ label, value, caption, icon: Icon }) => (
  <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
    <div className="flex items-start justify-between gap-3">
      <div>
        <div className="label-eyebrow-muted mb-2">{label}</div>
        <div className="font-display text-4xl text-equine-ink leading-none">{value}</div>
        {caption && <div className="text-[12px] text-equine-inkMuted mt-2">{caption}</div>}
      </div>
      <Icon className="w-4 h-4 text-equine-lilac" />
    </div>
  </div>
);

const QueueRow = ({ row, local, onSync, onArchive }) => {
  const status = row.sync_status || "queued";
  return (
    <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
      <div className="flex flex-col lg:flex-row lg:items-center gap-3">
        <div className="flex-1 min-w-0">
          <div className="font-display text-2xl text-equine-ink capitalize">{labelFor(row.action_type || "action")}</div>
          <div className="text-[12.5px] text-equine-inkMuted">{row.target_module} - {row.captured_at || "No capture time"}</div>
          <div className="text-[13px] text-equine-inkMuted mt-2">{row.payload_summary}</div>
        </div>
        <StatusPill tone={local ? "warning" : STATUS_TONE[status] || "info"}>{local ? "local" : labelFor(status)}</StatusPill>
        {onSync && status !== "synced" && <button type="button" onClick={onSync} className="btn-primary text-[12px] py-2 px-4">Mark synced</button>}
        {onArchive && <button type="button" onClick={onArchive} className="text-[12px] text-equine-clay hover:text-equine-ink px-2">Archive</button>}
      </div>
    </div>
  );
};

const SoftEmpty = ({ icon: Icon, text }) => (
  <div className="rounded-xl border border-dashed border-equine-cloud bg-white/45 py-8 text-center text-[13px] text-equine-inkMuted">
    <Icon className="w-6 h-6 mx-auto mb-2 text-equine-lilac" />
    {text}
  </div>
);

const QrPreview = ({ code }) => {
  const bits = Array.from({ length: 49 }, (_, i) => {
    const c = code.charCodeAt(i % Math.max(1, code.length)) || 0;
    return (c + i * 17) % 3 !== 0;
  });
  return (
    <div className="grid grid-cols-7 gap-0.5 p-2 rounded-lg bg-white border border-equine-cloud w-24 h-24 flex-shrink-0" aria-label={`QR preview for ${code}`}>
      {bits.map((on, i) => (
        <span key={i} className={`rounded-[1px] ${on ? "bg-equine-ink" : "bg-white"}`} />
      ))}
    </div>
  );
};
