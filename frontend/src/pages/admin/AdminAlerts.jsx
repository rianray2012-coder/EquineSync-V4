/**
 * AdminAlerts — read-only operational alerts derived from local
 * collections (Admin-6).
 *
 * No alerts collection — alerts are computed on-read. No dismissal.
 * Severities use approved Equine-Sync palette tones via UserStatusBadge.
 */
import React, { useEffect, useState } from "react";
import { AlertTriangle, RefreshCcw } from "lucide-react";
import { api } from "../../lib/api";
import UserStatusBadge from "./UserStatusBadge";

const ALERT_LABEL = {
  billing_webhook_retry: "Webhook retry",
  pending_subscription_email_stale: "Pending subscription email > 72h",
  payment_failure: "Failed payment",
  pending_user_approval_stale: "Pending user approval > 48h",
  denied_admin_access_pattern: "Denied admin access spike",
};

const formatTs = (iso) => {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return iso; }
};

export default function AdminAlerts() {
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    api.get(`/admin/portal/alerts`)
      .then((r) => {
        if (cancelled) return;
        setItems(r.data.items);
        setErr(null);
        setLoading(false);
      })
      .catch((e) => {
        if (cancelled) return;
        setErr(e?.response?.data?.detail || "Failed to load alerts.");
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [reloadKey]);

  // Group by alert key for the operator's eye.
  const grouped = (items || []).reduce((acc, a) => {
    (acc[a.key] = acc[a.key] || []).push(a);
    return acc;
  }, {});

  return (
    <div className="max-w-6xl mx-auto" data-testid="admin-alerts-page">
      <div className="mb-6 flex items-end justify-between">
        <div>
          <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
            Admin Portal · Alerts
          </div>
          <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">Alerts</h1>
          <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
            Live signals derived from billing, webhook, user approval, and
            denied-access data. Read-only; no dismissal in this phase.
          </p>
        </div>
        <button type="button" onClick={() => setReloadKey((k) => k + 1)}
                data-testid="admin-alerts-refresh"
                className="inline-flex items-center gap-2 px-3 py-2 rounded-lg border border-equinesync-graphite/15 text-[12.5px] text-equinesync-graphite hover:bg-equinesync-frost">
          <RefreshCcw className="w-3.5 h-3.5" /> Refresh
        </button>
      </div>

      {err && (
        <div className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
             data-testid="admin-alerts-error">{err}</div>
      )}

      {loading && !items && (
        <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-6 space-y-3"
             data-testid="admin-alerts-loading">
          {[0,1,2].map((i) => <div key={i} className="h-12 bg-equinesync-graphite/5 rounded animate-pulse" />)}
        </div>
      )}

      {!loading && items && items.length === 0 && (
        <div className="bg-white rounded-xl border border-equinesync-graphite/10 p-10 text-center text-[13px] text-equinesync-graphite/50"
             data-testid="admin-alerts-empty">
          No alerts right now. Everything looks healthy.
        </div>
      )}

      {items && items.length > 0 && (
        <div className="space-y-5" data-testid="admin-alerts-list">
          {Object.entries(grouped).map(([key, rows]) => (
            <section key={key} data-testid={`admin-alerts-group-${key}`}
                     className="bg-white rounded-xl border border-equinesync-graphite/10 overflow-hidden">
              <header className="px-4 py-3 bg-equinesync-frost border-b border-equinesync-graphite/10 flex items-center justify-between">
                <div className="flex items-center gap-2 text-[13px] text-equinesync-graphite">
                  <AlertTriangle className="w-4 h-4 text-equinesync-graphite/60" />
                  <span className="font-medium">{ALERT_LABEL[key] || key}</span>
                  <span className="text-equinesync-graphite/55 text-[11.5px]">· {rows.length}</span>
                </div>
                <UserStatusBadge value={rows[0]?.severity || "info"} />
              </header>
              <ul>
                {rows.map((a) => (
                  <li key={a.alert_ref}
                      data-testid={`admin-alerts-row-${a.alert_ref}`}
                      className="px-4 py-3 border-b border-equinesync-graphite/5 last:border-b-0 text-[13px]">
                    <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                      <span className="text-equinesync-graphite">
                        {a.facility_name || a.facility_id || a.actor_email || "—"}
                      </span>
                      <span className="text-equinesync-graphite/55 text-[11.5px]">
                        {a.count} item{a.count === 1 ? "" : "s"} · oldest {formatTs(a.oldest_at)}
                      </span>
                      {a.drill_in?.admin_ref && (
                        <span className="text-equinesync-graphite/55 font-mono text-[11px]">
                          → {a.drill_in.kind} · {a.drill_in.admin_ref}
                        </span>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      )}
    </div>
  );
}
