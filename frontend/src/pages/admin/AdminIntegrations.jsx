/**
 * AdminIntegrations — Admin-7B read-only integration health page.
 *
 * Lists the 4 static integration slugs (stripe, resend, webhooks,
 * jobs) with safe derived status. Clicking a card opens the detail
 * drawer (also read-only). No retry/disable mutations in this phase.
 *
 * support_admin is server-side blocked from this page (decision 2).
 * Palette: approved Equine-Sync tones only.
 */
import React, { useEffect, useState } from "react";
import {
  Plug, RefreshCcw, AlertOctagon, CheckCircle2, Pause, AlertTriangle,
} from "lucide-react";
import { api } from "../../lib/api";
import AdminIntegrationDrawer from "./AdminIntegrationDrawer";

const STATUS_TONE = {
  healthy: {
    Icon: CheckCircle2,
    cls: "bg-equinesync-lilac/15 text-equinesync-slate",
    label: "Healthy",
  },
  attention: {
    Icon: AlertTriangle,
    cls: "bg-equinesync-graphite/8 text-equinesync-graphite",
    label: "Attention",
  },
  not_configured: {
    Icon: Pause,
    cls: "bg-equinesync-frost text-equinesync-graphite/60",
    label: "Not configured",
  },
  disabled: {
    Icon: Pause,
    cls: "bg-equinesync-frost text-equinesync-graphite/60",
    label: "Disabled",
  },
};

const StatusPill = ({ status }) => {
  const tone = STATUS_TONE[status] || STATUS_TONE.attention;
  const { Icon } = tone;
  return (
    <span
      data-testid={`integration-status-${status}`}
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] tracking-[0.18em] uppercase ${tone.cls}`}
    >
      <Icon className="w-3 h-3" />
      {tone.label}
    </span>
  );
};

const formatTs = (iso) => {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleString("en-US", {
      dateStyle: "medium", timeStyle: "short",
    });
  } catch { return iso; }
};

const Card = ({ row, onOpen }) => (
  <button
    type="button"
    onClick={() => onOpen(row)}
    data-testid={`admin-integration-card-${row.slug}`}
    className="text-left rounded-2xl border border-equinesync-graphite/10 bg-white p-6 hover:border-equinesync-graphite/25 transition-colors w-full"
  >
    <div className="flex items-start justify-between">
      <div>
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          {row.slug}
        </div>
        <h2 className="mt-2 font-display text-xl text-equinesync-graphite font-light">
          {row.label}
        </h2>
      </div>
      <StatusPill status={row.status_label} />
    </div>
    <dl className="mt-4 grid grid-cols-2 gap-x-4 gap-y-2 text-[12.5px]">
      <dt className="text-equinesync-graphite/55">Configured</dt>
      <dd
        data-testid={`integration-${row.slug}-configured`}
        className="text-equinesync-graphite"
      >
        {row.configured ? "Yes" : "No"}
      </dd>
      {row.last_successful_event_at !== undefined && (
        <>
          <dt className="text-equinesync-graphite/55">Last event</dt>
          <dd className="text-equinesync-graphite tabular-nums">
            {formatTs(row.last_successful_event_at)}
          </dd>
        </>
      )}
      {row.stale_count !== undefined && (
        <>
          <dt className="text-equinesync-graphite/55">Stale / retries</dt>
          <dd className="text-equinesync-graphite tabular-nums">{row.stale_count}</dd>
        </>
      )}
      {row.pending_email_count !== undefined && (
        <>
          <dt className="text-equinesync-graphite/55">Pending emails</dt>
          <dd className="text-equinesync-graphite tabular-nums">
            {row.pending_email_count}
          </dd>
        </>
      )}
      {row.scheduler_enabled !== undefined && (
        <>
          <dt className="text-equinesync-graphite/55">Scheduler</dt>
          <dd className="text-equinesync-graphite">
            {row.scheduler_enabled ? "Enabled" : "Disabled"}
          </dd>
        </>
      )}
    </dl>
  </button>
);

export default function AdminIntegrations() {
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [reloadKey, setReloadKey] = useState(0);
  const [openSlug, setOpenSlug] = useState(null);

  useEffect(() => {
    let cancelled = false;
    api.get(`/admin/portal/integrations`)
      .then((r) => {
        if (cancelled) return;
        setItems(r.data.items);
        setErr(null);
        setLoading(false);
      })
      .catch((e) => {
        if (cancelled) return;
        setErr(e?.response?.data?.detail || "Failed to load integrations.");
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [reloadKey]);

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-integrations-page">
      <div className="mb-6 flex items-end justify-between flex-wrap gap-3">
        <div>
          <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
            Admin Portal · Integrations
          </div>
          <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">
            Integrations
          </h1>
          <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
            Read-only operational visibility into connected services. No
            retry, disable, or mutation controls in this phase.
          </p>
        </div>
        <button
          type="button"
          onClick={() => setReloadKey((k) => k + 1)}
          data-testid="admin-integrations-refresh"
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 text-[12.5px] text-equinesync-graphite hover:bg-equinesync-frost"
        >
          <RefreshCcw className="w-3.5 h-3.5" /> Refresh
        </button>
      </div>

      {err && (
        <div
          data-testid="admin-integrations-error"
          className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
        >
          <span className="inline-flex items-center gap-2">
            <AlertOctagon className="w-3.5 h-3.5" /> {err}
          </span>
        </div>
      )}

      {loading ? (
        <div
          className="rounded-2xl border border-equinesync-graphite/10 bg-white p-10 text-center text-[13px] text-equinesync-graphite/55"
          data-testid="admin-integrations-loading"
        >
          Loading integrations…
        </div>
      ) : (items && items.length === 0) ? (
        <div
          className="rounded-2xl border border-equinesync-graphite/10 bg-white p-10 text-center text-[13px] text-equinesync-graphite/55"
          data-testid="admin-integrations-empty"
        >
          <Plug className="w-5 h-5 mx-auto mb-3 text-equinesync-slate" />
          No integrations available.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {(items || []).map((row) => (
            <Card key={row.slug} row={row} onOpen={(r) => setOpenSlug(r.slug)} />
          ))}
        </div>
      )}

      {openSlug && (
        <AdminIntegrationDrawer
          slug={openSlug}
          onClose={() => setOpenSlug(null)}
        />
      )}
    </div>
  );
}
