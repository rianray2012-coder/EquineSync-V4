/**
 * AdminIntegrationDrawer — Admin-7B read-only integration detail.
 *
 * Pulls /admin/portal/integrations/{slug} for a richer view (recent
 * processing-status summaries, etc.). NO mutation controls.
 */
import React, { useEffect, useState } from "react";
import { X } from "lucide-react";
import { api } from "../../lib/api";

const formatTs = (iso) => {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleString("en-US", {
      dateStyle: "medium", timeStyle: "short",
    });
  } catch { return iso; }
};

export default function AdminIntegrationDrawer({ slug, onClose }) {
  const [detail, setDetail] = useState(null);
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    api.get(`/admin/portal/integrations/${encodeURIComponent(slug)}`)
      .then((r) => {
        if (cancelled) return;
        setDetail(r.data);
        setErr(null);
        setLoading(false);
      })
      .catch((e) => {
        if (cancelled) return;
        setErr(e?.response?.data?.detail || "Failed to load integration detail.");
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [slug]);

  return (
    <div
      className="fixed inset-0 z-50 flex justify-end"
      data-testid="admin-integration-drawer"
    >
      <div className="absolute inset-0 bg-equinesync-graphite/40" onClick={onClose} />
      <div className="relative w-full max-w-md bg-white h-full overflow-y-auto shadow-xl">
        <div className="flex items-start justify-between px-6 pt-6 pb-3 border-b border-equinesync-graphite/10">
          <div>
            <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55">
              Integration · {slug}
            </div>
            <h2 className="font-display text-xl text-equinesync-graphite font-light mt-1">
              {detail?.label || slug}
            </h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            data-testid="admin-integration-drawer-close"
            className="p-1.5 rounded-lg text-equinesync-graphite/60 hover:bg-equinesync-frost"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-6 space-y-5">
          {loading && (
            <div className="text-[13px] text-equinesync-graphite/55">Loading…</div>
          )}
          {err && (
            <div
              data-testid="admin-integration-drawer-error"
              className="rounded-lg border border-equinesync-graphite/15 p-4 text-[13px] text-equinesync-graphite/80"
            >
              {err}
            </div>
          )}
          {detail && (
            <>
              <section>
                <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
                  Status
                </div>
                <dl className="mt-3 grid grid-cols-2 gap-y-2 text-[12.5px]">
                  <dt className="text-equinesync-graphite/55">Configured</dt>
                  <dd className="text-equinesync-graphite">{detail.configured ? "Yes" : "No"}</dd>
                  <dt className="text-equinesync-graphite/55">Health</dt>
                  <dd className="text-equinesync-graphite">{detail.status_label}</dd>
                  {detail.last_successful_event_at !== undefined && (
                    <>
                      <dt className="text-equinesync-graphite/55">Last event</dt>
                      <dd className="text-equinesync-graphite tabular-nums">
                        {formatTs(detail.last_successful_event_at)}
                      </dd>
                    </>
                  )}
                  {detail.stale_count !== undefined && (
                    <>
                      <dt className="text-equinesync-graphite/55">Stale / retries</dt>
                      <dd className="text-equinesync-graphite tabular-nums">{detail.stale_count}</dd>
                    </>
                  )}
                  {detail.retry_count !== undefined && (
                    <>
                      <dt className="text-equinesync-graphite/55">Retry count</dt>
                      <dd className="text-equinesync-graphite tabular-nums">{detail.retry_count}</dd>
                    </>
                  )}
                  {detail.pending_email_count !== undefined && (
                    <>
                      <dt className="text-equinesync-graphite/55">Pending emails</dt>
                      <dd className="text-equinesync-graphite tabular-nums">
                        {detail.pending_email_count}
                      </dd>
                    </>
                  )}
                  {detail.scheduler_enabled !== undefined && (
                    <>
                      <dt className="text-equinesync-graphite/55">Scheduler</dt>
                      <dd className="text-equinesync-graphite">
                        {detail.scheduler_enabled ? "Enabled" : "Disabled"}
                      </dd>
                    </>
                  )}
                </dl>
              </section>

              {Array.isArray(detail.recent_summaries) && detail.recent_summaries.length > 0 && (
                <section data-testid="admin-integration-drawer-recent">
                  <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
                    Recent processing
                  </div>
                  <div className="mt-3 space-y-1.5">
                    {detail.recent_summaries.map((s, i) => (
                      <div key={i} className="flex items-center justify-between text-[12.5px] text-equinesync-graphite">
                        <span>{s.processing_status}</span>
                        <span className="tabular-nums">{s.count}</span>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              <div className="text-[11.5px] text-equinesync-graphite/55 pt-2 border-t border-equinesync-graphite/10">
                Read-only view. Operational controls (retry, disable) are
                not exposed in this phase.
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
