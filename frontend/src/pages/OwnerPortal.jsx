import React, { useCallback, useEffect, useMemo, useState } from "react";
import { api, fmtDate, money } from "../lib/api";
import { Card, PageHeader, StatusPill } from "../components/Primitives";
import CuratedTimeline from "../components/CuratedTimeline";
import OwnerDigestCard from "../components/OwnerDigestCard";
import { useAuth } from "../context/AuthContext";
import { Heart, X, Check, Image, RefreshCw, FileSignature, PenLine, FileText, ExternalLink, Phone, ShieldAlert, Target, Trophy, Route, CreditCard, Receipt, Megaphone, HeartPulse } from "lucide-react";
import { toast } from "sonner";

const trainingTone = (status) => {
  if (["achieved", "accepted", "complete"].includes(status)) return "success";
  if (["active", "submitted", "planned"].includes(status)) return "warning";
  if (["paused", "scratched"].includes(status)) return "neutral";
  return "info";
};

const healthReminderTone = (record) => {
  const data = record.data || {};
  if (["complete", "completed"].includes(data.status)) return "success";
  if (["expired", "overdue"].includes(data.status)) return "critical";
  if (!data.due_date) return "neutral";
  const dueAt = new Date(data.due_date);
  if (Number.isNaN(dueAt.getTime())) return "neutral";
  const days = Math.ceil((dueAt.getTime() - Date.now()) / 86400000);
  if (days < 0) return "critical";
  if (days <= 30) return "warning";
  return "info";
};

const fmtDateTime = (value) => {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
};

export default function OwnerPortal() {
  const { user } = useAuth();
  const isOwner = user?.role === "horse_owner";
  const canSignPortalForms = ["horse_owner", "parent"].includes(user?.role);
  const canDecide = ["admin", "barn_manager", "trainer"].includes(user?.role);

  const [horses, setHorses] = useState([]);
  const [requests, setRequests] = useState([]);
  const [ownerUpdates, setOwnerUpdates] = useState([]);
  const [updatesError, setUpdatesError] = useState(null);
  const [ownerAnnouncements, setOwnerAnnouncements] = useState([]);
  const [announcementsError, setAnnouncementsError] = useState(null);
  const [announcementsLoading, setAnnouncementsLoading] = useState(true);
  const [ownerForms, setOwnerForms] = useState([]);
  const [formsError, setFormsError] = useState(null);
  const [formsLoading, setFormsLoading] = useState(true);
  const [signingFormId, setSigningFormId] = useState(null);
  const [ownerHealthDocuments, setOwnerHealthDocuments] = useState([]);
  const [documentsError, setDocumentsError] = useState(null);
  const [documentsLoading, setDocumentsLoading] = useState(true);
  const [ownerHealthSummary, setOwnerHealthSummary] = useState({ reminders: [], weight_entries: [] });
  const [healthSummaryError, setHealthSummaryError] = useState(null);
  const [healthSummaryLoading, setHealthSummaryLoading] = useState(true);
  const [ownerEmergency, setOwnerEmergency] = useState({ contacts: [], workflows: [] });
  const [emergencyError, setEmergencyError] = useState(null);
  const [emergencyLoading, setEmergencyLoading] = useState(true);
  const [ownerTraining, setOwnerTraining] = useState({ plans: [], shows: [], rides: [], ride_logs: [] });
  const [trainingError, setTrainingError] = useState(null);
  const [trainingLoading, setTrainingLoading] = useState(true);
  const [ownerBilling, setOwnerBilling] = useState({ invoices: [], payment_profiles: [], recurring_rules: [], payment_provider: "stripe_placeholder" });
  const [billingError, setBillingError] = useState(null);
  const [billingLoading, setBillingLoading] = useState(true);
  const [preparingPaymentId, setPreparingPaymentId] = useState(null);
  const [form, setForm] = useState({ horse_id: "", type: "extra_ride", details: "" });
  const [activeHorseId, setActiveHorseId] = useState("");
  const [declineFor, setDeclineFor] = useState(null);
  const [declineReason, setDeclineReason] = useState("");
  const [submittingDecline, setSubmittingDecline] = useState(false);

  const load = useCallback(async () => {
    const [horseRes, requestRes] = await Promise.all([
      api.get("/horses"),
      api.get("/service-requests"),
    ]);
    setHorses(horseRes.data);
    setActiveHorseId((current) => current || horseRes.data?.[0]?.id || "");
    setRequests(requestRes.data);
    try {
      const updatesRes = await api.get("/owner-portal/media-updates");
      setOwnerUpdates(updatesRes.data || []);
      setUpdatesError(null);
    } catch (err) {
      setUpdatesError(err?.response?.data?.detail || "Owner updates are unavailable.");
    }
    try {
      const announcementsRes = await api.get("/owner-portal/announcements");
      setOwnerAnnouncements(announcementsRes.data || []);
      setAnnouncementsError(null);
    } catch (err) {
      setAnnouncementsError(err?.response?.data?.detail || "Announcements are unavailable.");
    } finally {
      setAnnouncementsLoading(false);
    }
    try {
      const formsRes = await api.get("/owner-portal/forms");
      setOwnerForms(formsRes.data || []);
      setFormsError(null);
    } catch (err) {
      setFormsError(err?.response?.data?.detail || "Forms are unavailable.");
    } finally {
      setFormsLoading(false);
    }
    try {
      const documentsRes = await api.get("/owner-portal/health-documents");
      setOwnerHealthDocuments(documentsRes.data || []);
      setDocumentsError(null);
    } catch (err) {
      setDocumentsError(err?.response?.data?.detail || "Health documents are unavailable.");
    } finally {
      setDocumentsLoading(false);
    }
    try {
      const healthSummaryRes = await api.get("/owner-portal/health-summary");
      setOwnerHealthSummary({
        reminders: healthSummaryRes.data?.reminders || [],
        weight_entries: healthSummaryRes.data?.weight_entries || [],
      });
      setHealthSummaryError(null);
    } catch (err) {
      setHealthSummaryError(err?.response?.data?.detail || "Health summary is unavailable.");
    } finally {
      setHealthSummaryLoading(false);
    }
    try {
      const emergencyRes = await api.get("/owner-portal/emergency");
      setOwnerEmergency({
        contacts: emergencyRes.data?.contacts || [],
        workflows: emergencyRes.data?.workflows || [],
      });
      setEmergencyError(null);
    } catch (err) {
      setEmergencyError(err?.response?.data?.detail || "Emergency details are unavailable.");
    } finally {
      setEmergencyLoading(false);
    }
    try {
      const trainingRes = await api.get("/owner-portal/training-performance");
      setOwnerTraining({
        plans: trainingRes.data?.plans || [],
        shows: trainingRes.data?.shows || [],
        rides: trainingRes.data?.rides || [],
        ride_logs: trainingRes.data?.ride_logs || [],
      });
      setTrainingError(null);
    } catch (err) {
      setTrainingError(err?.response?.data?.detail || "Training details are unavailable.");
    } finally {
      setTrainingLoading(false);
    }
    try {
      const billingRes = await api.get("/owner-portal/billing");
      setOwnerBilling({
        invoices: billingRes.data?.invoices || [],
        payment_profiles: billingRes.data?.payment_profiles || [],
        recurring_rules: billingRes.data?.recurring_rules || [],
        payment_provider: billingRes.data?.payment_provider || "stripe_placeholder",
      });
      setBillingError(null);
    } catch (err) {
      setBillingError(err?.response?.data?.detail || "Billing details are unavailable.");
    } finally {
      setBillingLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
    const interval = setInterval(load, 45000);
    return () => clearInterval(interval);
  }, [load]);

  const submit = async (e) => {
    e.preventDefault();
    if (!form.horse_id) return;
    await api.post("/service-requests", form);
    setForm({ horse_id: "", type: "extra_ride", details: "" });
    load();
  };

  const approve = async (id) => {
    await api.post(`/service-requests/${id}/approve`);
    load();
  };

  const openDecline = (sr) => {
    setDeclineFor(sr);
    setDeclineReason("");
  };

  const submitDecline = async () => {
    if (!declineFor) return;
    setSubmittingDecline(true);
    try {
      await api.post(`/service-requests/${declineFor.id}/decline`, {
        reason: declineReason.trim() || null,
      });
      toast.success("Request declined with a thoughtful note.");
      setDeclineFor(null);
      load();
    } catch {
      toast.error("Could not decline this request.");
    } finally {
      setSubmittingDecline(false);
    }
  };

  const signForm = async (record) => {
    setSigningFormId(record.id);
    try {
      await api.post(`/owner-portal/forms/${record.id}/sign`);
      toast.success("Form signed.");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not sign this form.");
    } finally {
      setSigningFormId(null);
    }
  };

  const preparePayment = async (invoice) => {
    setPreparingPaymentId(invoice.id);
    try {
      const res = await api.post(`/owner-portal/billing/${invoice.id}/prepare-payment`);
      toast.success(res.data?.message || "Payment placeholder prepared.");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not prepare payment.");
    } finally {
      setPreparingPaymentId(null);
    }
  };

  const activeHorse = useMemo(
    () => horses.find((h) => h.id === activeHorseId),
    [horses, activeHorseId],
  );

  const visibleOwnerUpdates = useMemo(() => {
    if (!activeHorse?.name) return ownerUpdates;
    return ownerUpdates.filter((record) => {
      const data = record.data || {};
      return !data.horse_name || data.horse_name === activeHorse.name;
    });
  }, [ownerUpdates, activeHorse]);

  const visibleTraining = useMemo(() => {
    if (!activeHorse?.name) return ownerTraining;
    const matchesHorse = (item) => {
      const data = item.data || item;
      return !data.horse_name || data.horse_name === activeHorse.name;
    };
    return {
      plans: ownerTraining.plans.filter(matchesHorse),
      shows: ownerTraining.shows.filter(matchesHorse),
      rides: ownerTraining.rides.filter(matchesHorse),
      ride_logs: ownerTraining.ride_logs.filter(matchesHorse),
    };
  }, [ownerTraining, activeHorse]);

  const visibleHealthSummary = useMemo(() => {
    if (!activeHorse?.name) return ownerHealthSummary;
    const matchesHorse = (record) => {
      const data = record.data || {};
      return !data.horse_name || data.horse_name === activeHorse.name;
    };
    return {
      reminders: ownerHealthSummary.reminders.filter(matchesHorse),
      weight_entries: ownerHealthSummary.weight_entries.filter(matchesHorse),
    };
  }, [ownerHealthSummary, activeHorse]);

  const billingTotals = useMemo(() => {
    const invoices = ownerBilling.invoices || [];
    return {
      open: invoices.filter((invoice) => invoice.status === "open").reduce((sum, invoice) => sum + Number(invoice.total || 0), 0),
      overdue: invoices.filter((invoice) => invoice.status === "overdue").reduce((sum, invoice) => sum + Number(invoice.total || 0), 0),
      paid: invoices.filter((invoice) => invoice.status === "paid").reduce((sum, invoice) => sum + Number(invoice.total || 0), 0),
    };
  }, [ownerBilling.invoices]);

  return (
    <div data-testid="owner-portal-page">
      <PageHeader
        eyebrow="Concierge"
        title="Owner Portal"
        subtitle="Curated updates from the barn — medications, vet visits, farrier work, rehab and feeding — all in one calm stream."
      />

      {/* ───── Daily Digest (owner only) ───────────────────────────────── */}
      {isOwner && <OwnerDigestCard />}

      {/* ───── Curated Timeline ──────────────────────────────────────────── */}
      <Card className="mb-8" data-testid="owner-timeline-card">
        <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
              <Heart strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
            </div>
            <div>
              <h2 className="font-display text-2xl text-equine-ink">Care Timeline</h2>
              <div className="text-[12.5px] text-equine-inkMuted">
                Wellness-focused milestones only. Internal barn workflows stay behind the scenes.
              </div>
            </div>
          </div>
          {horses.length > 1 && (
            <div className="flex items-center gap-1.5 overflow-x-auto scrollbar-luxe">
              {horses.map((h) => (
                <button
                  key={h.id}
                  data-testid={`timeline-horse-${h.id}`}
                  onClick={() => setActiveHorseId(h.id)}
                  className={`shrink-0 px-3 py-1.5 rounded-full text-[12px] tracking-wide border transition-colors ${
                    activeHorseId === h.id
                      ? "bg-equine-navy text-white border-equine-navy"
                      : "bg-equine-card text-equine-inkMuted border-equine-hairline hover:border-equine-graphite"
                  }`}
                >
                  {h.name}
                </button>
              ))}
            </div>
          )}
        </div>
        {activeHorseId ? (
          <CuratedTimeline horseId={activeHorseId} />
        ) : (
          <div className="text-equine-inkSoft text-[13px] py-8 text-center">
            No horses linked yet.
          </div>
        )}
        {activeHorse && (
          <div className="mt-6 pt-5 border-t border-equine-hairline text-[12px] text-equine-inkSoft text-center">
            Viewing care for <span className="text-equine-ink font-medium">{activeHorse.name}</span>
          </div>
        )}
      </Card>

      {/* ───── Owner-visible photo/video updates ─────────────────────── */}
      <Card className="mb-8" data-testid="owner-media-updates-card">
        <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
              <Image strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
            </div>
            <div>
              <h2 className="font-display text-2xl text-equine-ink">Photo & Video Updates</h2>
              <div className="text-[12.5px] text-equine-inkMuted">
                Owner-visible media from the barn, refreshed while the portal is open.
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={load}
            className="btn-secondary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1"
            data-testid="owner-media-refresh"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>

        {updatesError ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            {updatesError}
          </div>
        ) : visibleOwnerUpdates.length === 0 ? (
          <div className="rounded-xl border border-dashed border-equine-hairline bg-equine-soft/45 py-8 text-center text-[13px] text-equine-inkMuted">
            No shared media updates yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {visibleOwnerUpdates.slice(0, 6).map((record) => {
              const data = record.data || {};
              return (
                <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 overflow-hidden" data-testid={`owner-media-update-${record.id}`}>
                  <div className="aspect-[4/3] bg-equine-soft border-b border-equine-hairline">
                    {data.media_url ? (
                      <img src={data.media_url} alt="" className="w-full h-full object-cover" />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-equine-inkSoft">
                        <Image className="w-8 h-8" />
                      </div>
                    )}
                  </div>
                  <div className="p-4">
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="font-display text-xl text-equine-ink truncate">{data.horse_name || "Barn update"}</div>
                      <StatusPill tone="success">shared</StatusPill>
                    </div>
                    {data.caption && <div className="text-[13px] text-equine-inkMuted leading-relaxed">{data.caption}</div>}
                    <div className="text-[11.5px] text-equine-inkSoft mt-3">{fmtDate(record.created_at)}</div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </Card>

      {/* ───── Barn announcements ────────────────────────────────────── */}
      <Card className="mb-8" data-testid="owner-announcements-card">
        <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
              <Megaphone strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
            </div>
            <div>
              <h2 className="font-display text-2xl text-equine-ink">Barn Announcements</h2>
              <div className="text-[12.5px] text-equine-inkMuted">
                Owner-facing notices from the barn, ready for push notification delivery later.
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={load}
            className="btn-secondary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1"
            data-testid="owner-announcements-refresh"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>

        {announcementsLoading ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            Loading announcements…
          </div>
        ) : announcementsError ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            {announcementsError}
          </div>
        ) : ownerAnnouncements.length === 0 ? (
          <div className="rounded-xl border border-dashed border-equine-hairline bg-equine-soft/45 py-8 text-center text-[13px] text-equine-inkMuted">
            No owner announcements right now.
          </div>
        ) : (
          <div className="space-y-3">
            {ownerAnnouncements.slice(0, 5).map((record) => {
              const data = record.data || {};
              return (
                <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-announcement-${record.id}`}>
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div>
                      <div className="font-display text-xl text-equine-ink">{data.subject || "Barn announcement"}</div>
                      <div className="text-[12.5px] text-equine-inkMuted">
                        {(data.channel || "in_app").replace(/_/g, " ")} · {fmtDate(record.updated_at || record.created_at)}
                      </div>
                    </div>
                    <StatusPill tone="success">sent</StatusPill>
                  </div>
                  {data.body && <div className="text-[13px] text-equine-inkMuted leading-relaxed whitespace-pre-wrap">{data.body}</div>}
                </div>
              );
            })}
          </div>
        )}
      </Card>

      {/* ───── Owner-visible forms and signatures ────────────────────── */}
      <Card className="mb-8" data-testid="owner-forms-card">
        <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
              <FileSignature strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
            </div>
            <div>
              <h2 className="font-display text-2xl text-equine-ink">Forms & Signatures</h2>
              <div className="text-[12.5px] text-equine-inkMuted">
                Sent releases, waivers, and acknowledgements ready for owner review.
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={load}
            className="btn-secondary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1"
            data-testid="owner-forms-refresh"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>

        {formsLoading ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            Loading forms…
          </div>
        ) : formsError ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            {formsError}
          </div>
        ) : ownerForms.length === 0 ? (
          <div className="rounded-xl border border-dashed border-equine-hairline bg-equine-soft/45 py-8 text-center text-[13px] text-equine-inkMuted">
            No forms waiting right now.
          </div>
        ) : (
          <div className="space-y-3">
            {ownerForms.map((record) => {
              const data = record.data || {};
              const canSignForm = canSignPortalForms && data.status === "sent";
              return (
                <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 flex items-start justify-between gap-4 flex-wrap" data-testid={`owner-form-${record.id}`}>
                  <div className="min-w-[220px] flex-1">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <div className="font-display text-xl text-equine-ink">{data.form_name || "Untitled form"}</div>
                      <StatusPill tone={data.status === "signed" ? "success" : data.status === "expired" ? "neutral" : "warning"}>
                        {data.status || "sent"}
                      </StatusPill>
                    </div>
                    <div className="text-[12.5px] text-equine-inkMuted">
                      Recipient: {data.recipient_name || "Owner"} · Provider: {(data.signature_provider || "internal_placeholder").replace("_", " ")}
                    </div>
                    <div className="text-[11.5px] text-equine-inkSoft mt-2">
                      {data.signed_at ? `Signed ${fmtDate(data.signed_at)}` : `Updated ${fmtDate(record.updated_at)}`}
                    </div>
                  </div>
                  {canSignForm && (
                    <button
                      type="button"
                      onClick={() => signForm(record)}
                      disabled={signingFormId === record.id}
                      className="btn-primary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1 disabled:opacity-60"
                      data-testid={`owner-form-sign-${record.id}`}
                    >
                      <PenLine className="w-3.5 h-3.5" />
                      {signingFormId === record.id ? "Signing…" : "Sign"}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </Card>

      {/* ───── Shared health documents ───────────────────────────────── */}
      <Card className="mb-8" data-testid="owner-health-documents-card">
        <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
              <FileText strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
            </div>
            <div>
              <h2 className="font-display text-2xl text-equine-ink">Shared Health Documents</h2>
              <div className="text-[12.5px] text-equine-inkMuted">
                Owner-visible Coggins, vaccine, insurance, and vet paperwork references.
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={load}
            className="btn-secondary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1"
            data-testid="owner-health-documents-refresh"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>

        {documentsLoading ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            Loading documents…
          </div>
        ) : documentsError ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            {documentsError}
          </div>
        ) : ownerHealthDocuments.length === 0 ? (
          <div className="rounded-xl border border-dashed border-equine-hairline bg-equine-soft/45 py-8 text-center text-[13px] text-equine-inkMuted">
            No shared health documents yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {ownerHealthDocuments.slice(0, 6).map((record) => {
              const data = record.data || {};
              const days = data.expires_at ? Math.ceil((new Date(data.expires_at).getTime() - Date.now()) / 86400000) : null;
              const statusTone = days === null ? "neutral" : days < 0 ? "critical" : days <= 30 ? "warning" : "success";
              const statusLabel = days === null ? "no expiration" : days < 0 ? "expired" : days === 0 ? "expires today" : `${days}d left`;
              return (
                <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-health-document-${record.id}`}>
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="min-w-0">
                      <div className="font-display text-xl text-equine-ink truncate">{data.horse_name || "Horse document"}</div>
                      <div className="text-[12.5px] text-equine-inkMuted capitalize">{(data.document_type || "document").replace(/_/g, " ")}</div>
                    </div>
                    <StatusPill tone={statusTone}>{statusLabel}</StatusPill>
                  </div>
                  {data.notes && <div className="text-[13px] text-equine-inkMuted leading-relaxed">{data.notes}</div>}
                  <div className="hairline mt-4 pt-3 flex items-center justify-between gap-3">
                    <div className="text-[11.5px] text-equine-inkSoft">
                      {data.expires_at ? `Expires ${fmtDate(data.expires_at)}` : `Shared ${fmtDate(record.updated_at || record.created_at)}`}
                    </div>
                    {data.document_url ? (
                      <a href={data.document_url} target="_blank" rel="noreferrer" className="text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1">
                        Open <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : (
                      <span className="text-[12px] text-equine-inkSoft">No file URL</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </Card>

      {/* ───── Health reminders and body condition ──────────────────── */}
      <Card className="mb-8" data-testid="owner-health-summary-card">
        <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
              <HeartPulse strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
            </div>
            <div>
              <h2 className="font-display text-2xl text-equine-ink">Health Snapshot</h2>
              <div className="text-[12.5px] text-equine-inkMuted">
                Upcoming vaccines, Coggins checks, and weight/body-condition trends for selected horses.
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={load}
            className="btn-secondary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1"
            data-testid="owner-health-summary-refresh"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>

        {healthSummaryLoading ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            Loading health snapshot…
          </div>
        ) : healthSummaryError ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            {healthSummaryError}
          </div>
        ) : (visibleHealthSummary.reminders.length + visibleHealthSummary.weight_entries.length) === 0 ? (
          <div className="rounded-xl border border-dashed border-equine-hairline bg-equine-soft/45 py-8 text-center text-[13px] text-equine-inkMuted">
            No shared health reminders or body-condition entries yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="space-y-3">
              <div className="label-eyebrow text-equine-inkSoft">Reminders</div>
              {visibleHealthSummary.reminders.length === 0 ? (
                <div className="rounded-xl border border-equine-hairline bg-equine-soft/45 p-4 text-[13px] text-equine-inkMuted">
                  No reminders shared.
                </div>
              ) : visibleHealthSummary.reminders.slice(0, 5).map((record) => {
                const data = record.data || {};
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-health-reminder-${record.id}`}>
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="min-w-0">
                        <div className="font-display text-xl text-equine-ink truncate">{data.horse_name || "Horse"}</div>
                        <div className="text-[12.5px] text-equine-inkMuted capitalize">{(data.reminder_type || "health reminder").replace(/_/g, " ")}</div>
                      </div>
                      <StatusPill tone={healthReminderTone(record)}>{(data.status || "scheduled").replace(/_/g, " ")}</StatusPill>
                    </div>
                    <div className="text-[12.5px] text-equine-inkMuted">
                      Due {fmtDate(data.due_date)}{data.provider ? ` · ${data.provider}` : ""}
                    </div>
                    {data.notes && <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{data.notes}</div>}
                  </div>
                );
              })}
            </div>

            <div className="space-y-3">
              <div className="label-eyebrow text-equine-inkSoft">Weight & Condition</div>
              {visibleHealthSummary.weight_entries.length === 0 ? (
                <div className="rounded-xl border border-equine-hairline bg-equine-soft/45 p-4 text-[13px] text-equine-inkMuted">
                  No weight or body-condition entries shared.
                </div>
              ) : visibleHealthSummary.weight_entries.slice(0, 5).map((record) => {
                const data = record.data || {};
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-weight-entry-${record.id}`}>
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="min-w-0">
                        <div className="font-display text-xl text-equine-ink truncate">{data.horse_name || "Horse"}</div>
                        <div className="text-[12.5px] text-equine-inkMuted">{fmtDate(data.recorded_at)}</div>
                      </div>
                      <StatusPill tone="info">BCS {data.body_condition || "—"}</StatusPill>
                    </div>
                    <div className="text-[13px] text-equine-ink">
                      {data.weight_lbs ? `${Number(data.weight_lbs).toLocaleString()} lb` : "Weight not recorded"}
                    </div>
                    {data.notes && <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{data.notes}</div>}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </Card>

      {/* ───── Emergency readiness ───────────────────────────────────── */}
      <Card className="mb-8" data-testid="owner-emergency-card">
        <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
              <ShieldAlert strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
            </div>
            <div>
              <h2 className="font-display text-2xl text-equine-ink">Emergency Readiness</h2>
              <div className="text-[12.5px] text-equine-inkMuted">
                Contacts and active emergency workflows visible for your horses.
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={load}
            className="btn-secondary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1"
            data-testid="owner-emergency-refresh"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>

        {emergencyLoading ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            Loading emergency details…
          </div>
        ) : emergencyError ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            {emergencyError}
          </div>
        ) : (ownerEmergency.contacts.length + ownerEmergency.workflows.length) === 0 ? (
          <div className="rounded-xl border border-dashed border-equine-hairline bg-equine-soft/45 py-8 text-center text-[13px] text-equine-inkMuted">
            No emergency contacts or workflows are shared yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="space-y-3">
              <div className="label-eyebrow text-equine-inkSoft">Contacts</div>
              {ownerEmergency.contacts.length === 0 ? (
                <div className="rounded-xl border border-equine-hairline bg-equine-soft/45 p-4 text-[13px] text-equine-inkMuted">
                  No contacts on file.
                </div>
              ) : ownerEmergency.contacts.slice(0, 4).map((record) => {
                const data = record.data || {};
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-emergency-contact-${record.id}`}>
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <div className="font-display text-xl text-equine-ink">{data.person_name || "Emergency contact"}</div>
                        <div className="text-[12.5px] text-equine-inkMuted">{data.relationship || "Contact"} · {data.horse_name || "Horse TBD"}</div>
                      </div>
                      <StatusPill tone={Number(data.priority) === 1 ? "critical" : "warning"}>priority {data.priority || "—"}</StatusPill>
                    </div>
                    {data.phone && (
                      <a href={`tel:${data.phone}`} className="mt-3 inline-flex items-center gap-2 text-[13px] text-equine-navy hover:text-equine-saddle">
                        <Phone className="w-3.5 h-3.5" /> {data.phone}
                      </a>
                    )}
                    {data.notes && <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{data.notes}</div>}
                  </div>
                );
              })}
            </div>

            <div className="space-y-3">
              <div className="label-eyebrow text-equine-inkSoft">Workflows</div>
              {ownerEmergency.workflows.length === 0 ? (
                <div className="rounded-xl border border-equine-hairline bg-equine-soft/45 p-4 text-[13px] text-equine-inkMuted">
                  No active workflows.
                </div>
              ) : ownerEmergency.workflows.slice(0, 4).map((record) => {
                const data = record.data || {};
                const status = data.workflow_status || "open";
                const tone = status === "resolved" || status === "closed" ? "success" : status === "stabilizing" ? "warning" : "critical";
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-emergency-workflow-${record.id}`}>
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div>
                        <div className="font-display text-xl text-equine-ink">{data.horse_name || "Horse"}</div>
                        <div className="text-[12.5px] text-equine-inkMuted capitalize">{(data.emergency_type || "emergency").replace(/_/g, " ")}</div>
                      </div>
                      <StatusPill tone={tone}>{status.replace(/_/g, " ")}</StatusPill>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-[12px]">
                      <div className="rounded-lg border border-equine-hairline bg-white/50 p-2">
                        <div className="text-equine-inkSoft">Owner</div>
                        <div className="text-equine-ink capitalize">{(data.owner_status || "not contacted").replace(/_/g, " ")}</div>
                      </div>
                      <div className="rounded-lg border border-equine-hairline bg-white/50 p-2">
                        <div className="text-equine-inkSoft">Vet</div>
                        <div className="text-equine-ink capitalize">{(data.vet_status || "not called").replace(/_/g, " ")}</div>
                      </div>
                    </div>
                    {data.notes && <div className="text-[12.5px] text-equine-inkMuted mt-3 leading-relaxed">{data.notes}</div>}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </Card>

      {/* ───── Training and performance ──────────────────────────────── */}
      <Card className="mb-8" data-testid="owner-training-card">
        <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
              <Target strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
            </div>
            <div>
              <h2 className="font-display text-2xl text-equine-ink">Training & Performance</h2>
              <div className="text-[12.5px] text-equine-inkMuted">
                Goals, show entries, ride logs, and GPS summaries shared for selected horses.
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={load}
            className="btn-secondary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1"
            data-testid="owner-training-refresh"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>

        {trainingLoading ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            Loading training details…
          </div>
        ) : trainingError ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            {trainingError}
          </div>
        ) : (visibleTraining.plans.length + visibleTraining.shows.length + visibleTraining.rides.length + visibleTraining.ride_logs.length) === 0 ? (
          <div className="rounded-xl border border-dashed border-equine-hairline bg-equine-soft/45 py-8 text-center text-[13px] text-equine-inkMuted">
            No shared training or performance updates yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
            <div className="space-y-3">
              <div className="label-eyebrow text-equine-inkSoft">Goals</div>
              {visibleTraining.plans.length === 0 ? (
                <div className="rounded-xl border border-equine-hairline bg-equine-soft/45 p-4 text-[13px] text-equine-inkMuted">No goals shared.</div>
              ) : visibleTraining.plans.slice(0, 3).map((record) => {
                const data = record.data || {};
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-training-plan-${record.id}`}>
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div>
                        <div className="font-display text-xl text-equine-ink">{data.goal || "Training goal"}</div>
                        <div className="text-[12.5px] text-equine-inkMuted">{data.horse_name || "Horse"} · {data.trainer_name || "Trainer TBD"}</div>
                      </div>
                      <StatusPill tone={trainingTone(data.status)}>{data.status || "planned"}</StatusPill>
                    </div>
                    {data.plan_notes && <div className="text-[12.5px] text-equine-inkMuted leading-relaxed">{data.plan_notes}</div>}
                    <div className="text-[11.5px] text-equine-inkSoft mt-3">Target {fmtDate(data.target_date)}</div>
                  </div>
                );
              })}
            </div>

            <div className="space-y-3">
              <div className="label-eyebrow text-equine-inkSoft">Shows</div>
              {visibleTraining.shows.length === 0 ? (
                <div className="rounded-xl border border-equine-hairline bg-equine-soft/45 p-4 text-[13px] text-equine-inkMuted">No show entries shared.</div>
              ) : visibleTraining.shows.slice(0, 3).map((record) => {
                const data = record.data || {};
                return (
                  <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-show-entry-${record.id}`}>
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div>
                        <div className="font-display text-xl text-equine-ink">{data.show_name || "Show entry"}</div>
                        <div className="text-[12.5px] text-equine-inkMuted">{data.horse_name || "Horse"}{data.rider_name ? ` · ${data.rider_name}` : ""}</div>
                      </div>
                      <StatusPill tone={trainingTone(data.entry_status)}>{data.entry_status || "planning"}</StatusPill>
                    </div>
                    {data.results && <div className="text-[12.5px] text-equine-inkMuted leading-relaxed">{data.results}</div>}
                    <div className="text-[11.5px] text-equine-inkSoft mt-3"><Trophy className="w-3 h-3 inline mr-1" /> {fmtDate(data.start_date)}</div>
                  </div>
                );
              })}
            </div>

            <div className="space-y-3">
              <div className="label-eyebrow text-equine-inkSoft">Rides</div>
              {visibleTraining.rides.length === 0 && visibleTraining.ride_logs.length === 0 ? (
                <div className="rounded-xl border border-equine-hairline bg-equine-soft/45 p-4 text-[13px] text-equine-inkMuted">No ride summaries shared.</div>
              ) : (
                <>
                  {visibleTraining.rides.slice(0, 2).map((record) => {
                    const data = record.data || {};
                    return (
                      <div key={record.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-gps-ride-${record.id}`}>
                        <div className="flex items-start justify-between gap-3 mb-2">
                          <div>
                            <div className="font-display text-xl text-equine-ink">{data.horse_name || "Ride"}</div>
                            <div className="text-[12.5px] text-equine-inkMuted">{data.rider_name || "Rider TBD"} · {fmtDateTime(data.started_at)}</div>
                          </div>
                          <StatusPill tone="info">{Number(data.distance_miles || 0).toFixed(1)} mi</StatusPill>
                        </div>
                        <div className="text-[12.5px] text-equine-inkMuted">{data.duration_minutes || "—"} minutes</div>
                        {data.track_url && (
                          <a href={data.track_url} target="_blank" rel="noreferrer" className="mt-3 text-[12px] text-equine-navy hover:text-equine-saddle inline-flex items-center gap-1">
                            <Route className="w-3 h-3" /> Open track
                          </a>
                        )}
                      </div>
                    );
                  })}
                  {visibleTraining.ride_logs.slice(0, 2).map((log) => (
                    <div key={log.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4" data-testid={`owner-ride-log-${log.id}`}>
                      <div className="font-display text-xl text-equine-ink">{log.horse_name || "Ride log"}</div>
                      <div className="text-[12.5px] text-equine-inkMuted">{log.trainer_name || "Trainer"} · {fmtDate(log.date)}</div>
                      {log.exercises && <div className="text-[12.5px] text-equine-inkMuted mt-2 leading-relaxed">{log.exercises}</div>}
                      {log.rating && <StatusPill tone="success">rating {log.rating}/10</StatusPill>}
                    </div>
                  ))}
                </>
              )}
            </div>
          </div>
        )}
      </Card>

      {/* ───── Billing readiness ─────────────────────────────────────── */}
      <Card className="mb-8" data-testid="owner-billing-card">
        <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-equine-soft border border-equine-hairline flex items-center justify-center">
              <CreditCard strokeWidth={1.5} className="w-4 h-4 text-equine-navy" />
            </div>
            <div>
              <h2 className="font-display text-2xl text-equine-ink">Billing</h2>
              <div className="text-[12.5px] text-equine-inkMuted">
                Invoices, auto-pay readiness, and recurring charges scoped to your owner account.
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={load}
            className="btn-secondary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1"
            data-testid="owner-billing-refresh"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>

        {billingLoading ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            Loading billing details…
          </div>
        ) : billingError ? (
          <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 py-8 text-center text-[13px] text-equine-inkMuted">
            {billingError}
          </div>
        ) : ownerBilling.invoices.length === 0 && ownerBilling.payment_profiles.length === 0 && ownerBilling.recurring_rules.length === 0 ? (
          <div className="rounded-xl border border-dashed border-equine-hairline bg-equine-soft/45 py-8 text-center text-[13px] text-equine-inkMuted">
            No billing records are shared yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
            <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
              <div className="label-eyebrow text-equine-inkSoft mb-3">Summary</div>
              <div className="grid grid-cols-3 gap-2">
                <BillingMetric label="Open" value={money(billingTotals.open)} />
                <BillingMetric label="Overdue" value={money(billingTotals.overdue)} critical />
                <BillingMetric label="Paid" value={money(billingTotals.paid)} />
              </div>
              <div className="hairline mt-4 pt-3 text-[12px] text-equine-inkMuted">
                Provider: {ownerBilling.payment_provider.replace("_", " ")}
              </div>
              {ownerBilling.payment_profiles.slice(0, 2).map((record) => {
                const data = record.data || {};
                return (
                  <div key={record.id} className="mt-3 rounded-lg border border-equine-hairline bg-white/50 p-3" data-testid={`owner-payment-profile-${record.id}`}>
                    <div className="flex items-center justify-between gap-2">
                      <div className="text-[13px] text-equine-ink">{data.provider || "Payment profile"}</div>
                      <StatusPill tone={data.autopay_status === "enrolled" ? "success" : "warning"}>{(data.autopay_status || "not_enrolled").replace(/_/g, " ")}</StatusPill>
                    </div>
                    {data.customer_ref && <div className="text-[11.5px] text-equine-inkSoft mt-1">{data.customer_ref}</div>}
                  </div>
                );
              })}
            </div>

            <div className="xl:col-span-2 space-y-3">
              <div className="label-eyebrow text-equine-inkSoft">Invoices</div>
              {ownerBilling.invoices.length === 0 ? (
                <div className="rounded-xl border border-equine-hairline bg-equine-soft/45 p-4 text-[13px] text-equine-inkMuted">No invoices shared.</div>
              ) : ownerBilling.invoices.slice(0, 5).map((invoice) => {
                const tone = invoice.status === "paid" ? "success" : invoice.status === "overdue" ? "critical" : "warning";
                return (
                  <div key={invoice.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4 flex items-start justify-between gap-4 flex-wrap" data-testid={`owner-invoice-${invoice.id}`}>
                    <div className="min-w-[220px] flex-1">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <Receipt className="w-4 h-4 text-equine-inkSoft" />
                        <div className="font-display text-xl text-equine-ink">{invoice.horse_name || "Invoice"}</div>
                        <StatusPill tone={tone}>{invoice.status || "open"}</StatusPill>
                      </div>
                      <div className="text-[12.5px] text-equine-inkMuted">Due {fmtDate(invoice.due_date)} · {invoice.owner_name || "Owner"}</div>
                      <div className="font-display text-2xl text-equine-ink mt-2">{money(invoice.total)}</div>
                    </div>
                    {invoice.status !== "paid" && (
                      <button
                        type="button"
                        onClick={() => preparePayment(invoice)}
                        disabled={preparingPaymentId === invoice.id}
                        className="btn-primary !py-2 !px-3 text-[12.5px] inline-flex items-center gap-1 disabled:opacity-60"
                        data-testid={`owner-invoice-prepare-${invoice.id}`}
                      >
                        <CreditCard className="w-3.5 h-3.5" />
                        {preparingPaymentId === invoice.id ? "Preparing…" : "Prepare payment"}
                      </button>
                    )}
                  </div>
                );
              })}

              {ownerBilling.recurring_rules.length > 0 && (
                <div className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
                  <div className="label-eyebrow text-equine-inkSoft mb-3">Recurring</div>
                  <div className="space-y-2">
                    {ownerBilling.recurring_rules.slice(0, 3).map((record) => {
                      const data = record.data || {};
                      return (
                        <div key={record.id} className="flex items-center justify-between gap-3 text-[13px]" data-testid={`owner-recurring-rule-${record.id}`}>
                          <div className="text-equine-ink">{data.name || "Recurring charge"} · {data.horse_name || "Horse"}</div>
                          <div className="text-equine-inkMuted">{money(data.amount)} {data.frequency || "monthly"}</div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </Card>

      {/* ───── Concierge form + request log ───────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <h2 className="font-display text-2xl mb-4 text-equine-ink">Request a service</h2>
          <form onSubmit={submit} className="space-y-3" data-testid="sr-form">
            <select
              required
              value={form.horse_id}
              onChange={(e) => setForm({ ...form, horse_id: e.target.value })}
              className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2"
            >
              <option value="">Choose horse…</option>
              {horses.map((h) => <option key={h.id} value={h.id}>{h.name}</option>)}
            </select>
            <select
              value={form.type}
              onChange={(e) => setForm({ ...form, type: e.target.value })}
              className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2"
            >
              <option value="extra_ride">Extra Ride</option>
              <option value="grooming">Grooming</option>
              <option value="body_clip">Body Clip</option>
              <option value="hand_walk">Hand Walking</option>
              <option value="lesson">Private Lesson</option>
              <option value="hauling">Hauling</option>
              <option value="show_prep">Show Prep</option>
            </select>
            <textarea
              value={form.details}
              onChange={(e) => setForm({ ...form, details: e.target.value })}
              placeholder="Details / preferences"
              rows={4}
              className="w-full bg-equine-soft border border-equine-graphite/60 rounded-lg px-3 py-2"
            />
            <button className="btn-primary w-full" data-testid="sr-submit">Submit Request</button>
          </form>
        </Card>

        <Card className="lg:col-span-2">
          <h2 className="font-display text-2xl mb-4 text-equine-ink">Recent updates & requests</h2>
          {requests.length === 0 && (
            <div className="text-[13px] text-equine-inkSoft py-6 text-center">
              No requests yet.
            </div>
          )}
          {requests.map((s) => (
            <div key={s.id} className="py-3 hairline flex items-start gap-4 flex-wrap">
              <div className="flex-1 min-w-[200px]">
                <div className="text-equine-ink">
                  {s.horse_name} — <span className="capitalize">{s.type.replace('_', ' ')}</span>
                </div>
                <div className="text-[12.5px] text-equine-inkMuted">
                  {s.details || "No additional notes"} · {fmtDate(s.created_at)}
                </div>
                {s.status === "declined" && s.decline_reason && (
                  <div className="text-[12.5px] text-equine-inkSoft mt-1 italic">
                    Note from the barn: {s.decline_reason}
                  </div>
                )}
              </div>
              <StatusPill tone={
                s.status === "approved" ? "success" :
                s.status === "declined" ? "neutral" : "warning"
              }>{s.status}</StatusPill>
              {s.status === "pending" && canDecide && (
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => approve(s.id)}
                    data-testid={`approve-${s.id}`}
                    className="btn-secondary !py-1.5 !px-3 text-[12.5px] inline-flex items-center gap-1"
                  >
                    <Check className="w-3.5 h-3.5" /> Approve
                  </button>
                  <button
                    onClick={() => openDecline(s)}
                    data-testid={`decline-${s.id}`}
                    className="!py-1.5 !px-3 text-[12.5px] inline-flex items-center gap-1 rounded-lg border border-equine-hairline text-equine-inkMuted hover:text-equine-ink hover:border-equine-graphite transition-colors"
                  >
                    <X className="w-3.5 h-3.5" /> Decline
                  </button>
                </div>
              )}
            </div>
          ))}
        </Card>
      </div>

      {/* ───── Decline modal ──────────────────────────────────────────── */}
      {declineFor && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-equine-navyDeep/40 backdrop-blur-sm px-4"
          data-testid="decline-modal"
          onClick={(e) => { if (e.target === e.currentTarget) setDeclineFor(null); }}
        >
          <div className="bg-equine-card border border-equine-hairline rounded-2xl shadow-xl max-w-md w-full p-6">
            <div className="uppercase tracking-[0.22em] text-[10.5px] text-equine-inkSoft mb-1">Decline request</div>
            <h3 className="font-display text-xl text-equine-ink mb-1">
              {declineFor.horse_name} · <span className="capitalize">{declineFor.type.replace('_', ' ')}</span>
            </h3>
            <p className="text-[13px] text-equine-inkMuted mb-4">
              Add a brief, owner-facing note (optional). Keep it warm and professional — the owner will see this in their portal.
            </p>
            <textarea
              data-testid="decline-reason-input"
              value={declineReason}
              onChange={(e) => setDeclineReason(e.target.value)}
              rows={3}
              maxLength={500}
              placeholder="e.g. Farrier visit scheduled the same morning — we'll book this for next week."
              className="w-full bg-equine-soft border border-equine-hairline rounded-lg px-3 py-2 text-[13.5px] text-equine-ink placeholder:text-equine-inkSoft focus:outline-none focus:border-equine-navy"
            />
            <div className="flex justify-end gap-2 mt-4">
              <button
                onClick={() => setDeclineFor(null)}
                className="px-4 py-2 text-[13px] text-equine-inkMuted hover:text-equine-ink"
              >
                Cancel
              </button>
              <button
                data-testid="decline-confirm-btn"
                onClick={submitDecline}
                disabled={submittingDecline}
                className="btn-primary !py-2 !px-4 text-[13px] disabled:opacity-60"
              >
                {submittingDecline ? "Declining…" : "Decline request"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const BillingMetric = ({ label, value, critical = false }) => (
  <div className="rounded-lg border border-equine-hairline bg-white/50 p-3">
    <div className="label-eyebrow-muted mb-1">{label}</div>
    <div className={`font-display text-xl leading-none ${critical ? "text-equine-clay" : "text-equine-ink"}`}>{value}</div>
  </div>
);
