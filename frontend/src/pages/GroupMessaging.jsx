import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, Bell, Download, MessageSquare, Plus, RefreshCw, Send } from "lucide-react";
import { toast } from "sonner";
import { api, fmtDate } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const STATUSES = ["draft", "queued", "sent"];
const STATUS_TONE = { draft: "neutral", queued: "warning", sent: "success" };
const DISPLAY_LABELS = { draft: "draft", queued: "queued", sent: "logged locally" };
const ADD_FIELDS = [
  { key: "subject", label: "Subject", required: true, placeholder: "Message subject", full: true },
  { key: "audience", label: "Audience", kind: "select", opts: ["all_staff", "owners", "trainers", "custom"] },
  { key: "channel", label: "Channel", kind: "select", opts: ["in_app", "email", "push_ready"] },
  { key: "status", label: "Status", kind: "select", opts: STATUSES },
  { key: "body", label: "Message", kind: "textarea", rows: 5, required: true, full: true },
];

export default function GroupMessaging() {
  const [records, setRecords] = useState([]);
  const [placeholders, setPlaceholders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [savingId, setSavingId] = useState(null);
  const [previewingPush, setPreviewingPush] = useState(false);
  const [pushManifest, setPushManifest] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [moduleRes, placeholderRes] = await Promise.all([
        api.get("/feature-modules/group-messaging"),
        api.get("/integrations/placeholders"),
      ]);
      setRecords(moduleRes.data.records || []);
      setPlaceholders((placeholderRes.data || []).filter((p) => p.provider === "push_notifications"));
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load group messaging.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const stats = useMemo(() => Object.fromEntries(STATUSES.map((status) => [
    status,
    records.filter((record) => ((record.data || {}).status || "draft") === status).length,
  ])), [records]);

  const setStatus = async (record, status) => {
    setSavingId(record.id);
    try {
      await api.patch(`/feature-modules/group-messaging/records/${record.id}`, { data: { status } });
      toast.success("Message updated");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update message");
    } finally {
      setSavingId(null);
    }
  };

  const previewPush = async () => {
    setPreviewingPush(true);
    try {
      const r = await api.post("/integrations/push-notifications/preview", {
        include_group_messages: true,
        include_owner_updates: true,
      });
      const manifest = r.data;
      setPushManifest(manifest);
      const blob = new Blob([JSON.stringify(manifest, null, 2)], { type: manifest.content_type || "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = manifest.filename || "equinesync-push-preview.json";
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Push preview prepared");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare push preview");
    } finally {
      setPreviewingPush(false);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/group-messaging/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive message");
    }
  };

  return (
    <div data-testid="group-messaging-page">
      <PageHeader
        eyebrow="Communication"
        title="Group Messaging"
        subtitle="Draft and track owner, trainer, staff, and custom audience announcements with push-preview metadata."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="group-messaging-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="group-messaging-add">
              <Plus className="w-4 h-4" /> New message
            </button>
          </div>
        }
      />

      <Card hover={false} className="mb-6 border-equine-lilac/30 bg-equine-lilac/5">
        <div className="flex items-start gap-3">
          <Bell className="w-4 h-4 text-equine-lilac mt-0.5 flex-shrink-0" />
          <div className="flex-1 text-[13px] text-equine-inkMuted leading-relaxed">
            <div>
              Push notification payload previews are app-token shaped. Current records track channel intent and local status without sending external push notifications.
              {placeholders[0] && <span className="block mt-1 text-equine-inkSoft">{placeholders[0].ready_for.join(" · ")}</span>}
            </div>
          </div>
          <button
            type="button"
            onClick={previewPush}
            disabled={previewingPush}
            className="btn-secondary text-[12px] py-2 px-4 inline-flex items-center gap-1 disabled:opacity-60"
            data-testid="push-preview-export"
          >
            <Download className="w-3.5 h-3.5" /> {previewingPush ? "Preparing" : "Preview push"}
          </button>
        </div>
      </Card>

      {pushManifest && (
        <Card hover={false} className="mb-6" data-testid="push-preview-manifest">
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <div>
              <div className="label-eyebrow-muted mb-1">Latest push preview</div>
              <div className="font-display text-2xl text-equine-ink">{pushManifest.filename}</div>
              <div className="text-[12.5px] text-equine-inkMuted">
                {pushManifest.payload_count} payload(s) prepared for review
              </div>
            </div>
            <StatusPill tone="success">{pushManifest.status.replace(/_/g, " ")}</StatusPill>
          </div>
        </Card>
      )}

      <div className="grid grid-cols-3 gap-4 mb-6">
        {STATUSES.map((status) => (
          <Card key={status} hover={false} className="p-4">
            <div className="label-eyebrow-muted mb-2 capitalize">{DISPLAY_LABELS[status]}</div>
            <div className="flex items-end justify-between gap-3">
              <div className="font-display text-4xl text-equine-ink leading-none">{stats[status]}</div>
              <StatusPill tone={STATUS_TONE[status]}>{DISPLAY_LABELS[status]}</StatusPill>
            </div>
          </Card>
        ))}
      </div>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading group messages…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Group messaging unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <MessageSquare strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-lilac" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No group messages</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Draft the first announcement for staff, owners, or trainers.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="group-messaging-empty-add">
            <Plus className="w-4 h-4" /> Create first message
          </button>
        </Empty>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          {records.map((record) => {
            const data = record.data || {};
            const status = data.status || "draft";
            return (
              <Card key={record.id} hover={false} className={savingId === record.id ? "opacity-60" : ""} data-testid={`group-message-card-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.subject}</div>
                    <div className="text-[12.5px] text-equine-inkMuted">
                      {(data.audience || "custom").replace(/_/g, " ")} · {(data.channel || "in_app").replace(/_/g, " ")} · {fmtDate(record.created_at)}
                    </div>
                  </div>
                  <StatusPill tone={STATUS_TONE[status]}>{DISPLAY_LABELS[status]}</StatusPill>
                </div>
                <div className="text-[13.5px] text-equine-ink leading-relaxed whitespace-pre-wrap">{data.body}</div>
                <div className="hairline mt-4 pt-3 flex flex-wrap items-center gap-2">
                  {status !== "sent" ? (
                    <button type="button" onClick={() => setStatus(record, status === "draft" ? "queued" : "sent")} className="btn-secondary text-[12px] py-2 px-4 inline-flex items-center gap-1">
                      <Send className="w-3.5 h-3.5" /> {status === "draft" ? "Queue" : "Log locally"}
                    </button>
                  ) : <span className="text-[12px] text-equine-inkSoft">Local communication log</span>}
                  <button type="button" onClick={() => archiveRecord(record)} className="ml-auto text-[12px] text-equine-clay hover:text-equine-ink">
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
        title="New group message"
        eyebrow="Communication"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/group-messaging/records"
        initialValues={{ audience: "all_staff", channel: "in_app", status: "draft" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save message"
        testidPrefix="group-messaging-add"
        onCreated={load}
      />
    </div>
  );
}
