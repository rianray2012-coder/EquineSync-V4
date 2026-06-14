/**
 * AdminActivityFeed — last N curated audit-log entries.
 *
 * The backend already enforces the allowlist + scrubbing. Frontend just
 * formats the timeline and offers an expandable per-row metadata view.
 * No mutation affordances; read-only timeline.
 */
import React, { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

const formatTs = (iso) => {
  if (!iso) return "—";
  try {
    const d = new Date(iso);
    return d.toLocaleString("en-US", {
      month: "short", day: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit",
    });
  } catch {
    return iso;
  }
};

const ActionPill = ({ action }) => (
  <span
    className="px-2 py-0.5 rounded-full text-[10.5px] tracking-wide uppercase bg-equinesync-lilac/20 text-equinesync-graphite/75 font-medium"
    data-testid={`admin-activity-action-${action}`}
  >
    {action}
  </span>
);

const OutcomePill = ({ outcome, status }) => {
  // Approved palette only (Admin Portal guardrail): no red/amber tokens.
  // Denied → solid Slate Navy for highest emphasis (security signal).
  // Failure → Smoky Lilac w/ Graphite text + Slate Navy border (visible,
  // calm). Success/neutral renders nothing — keeps the timeline quiet.
  if (outcome === "denied" || status === 403) {
    return (
      <span
        className="px-2 py-0.5 rounded-full text-[10px] tracking-wide uppercase bg-equinesync-slate text-equinesync-frost border border-equinesync-slate"
        data-tone="denied"
      >
        Denied
      </span>
    );
  }
  if (outcome === "failure") {
    return (
      <span
        className="px-2 py-0.5 rounded-full text-[10px] tracking-wide uppercase bg-equinesync-lilac/40 text-equinesync-graphite border border-equinesync-slate/30"
        data-tone="failure"
      >
        Failure
      </span>
    );
  }
  return null;
};

const Row = ({ item }) => {
  const [open, setOpen] = useState(false);
  const meta = item.metadata || {};
  const hasMeta = Object.keys(meta).length > 0;
  return (
    <div
      data-testid={`admin-activity-row-${item.id || item.action}`}
      className="py-3 border-b border-equinesync-graphite/5 last:border-b-0"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center flex-wrap gap-2">
            <ActionPill action={item.action} />
            <OutcomePill outcome={item.outcome} status={item.status_code} />
            <span className="text-[11.5px] text-equinesync-graphite/50">
              {formatTs(item.ts)}
            </span>
          </div>
          <div className="mt-1.5 text-[13px] text-equinesync-graphite truncate">
            <span className="text-equinesync-graphite/65">{item.actor_email || "(system)"}</span>
            {item.resource_type && (
              <>
                <span className="text-equinesync-graphite/30 mx-2">·</span>
                <span className="text-equinesync-graphite/65">
                  {item.resource_type}
                  {item.resource_id ? ` ${String(item.resource_id).slice(0, 8)}…` : ""}
                </span>
              </>
            )}
          </div>
        </div>
        {hasMeta && (
          <button
            type="button"
            onClick={() => setOpen((o) => !o)}
            data-testid={`admin-activity-toggle-${item.id || item.action}`}
            className="text-equinesync-graphite/55 hover:text-equinesync-graphite transition-colors flex items-center gap-1 text-[11px] tracking-wide"
          >
            {open ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            Details
          </button>
        )}
      </div>
      {open && hasMeta && (
        <pre
          className="mt-3 p-3 rounded-lg bg-equinesync-frost text-[11.5px] text-equinesync-graphite/80 overflow-x-auto leading-relaxed"
          data-testid={`admin-activity-meta-${item.id || item.action}`}
        >
{JSON.stringify(meta, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default function AdminActivityFeed({ items, loading, error }) {
  return (
    <section
      className="rounded-xl border border-equinesync-graphite/10 bg-white p-5"
      data-testid="admin-activity-feed"
    >
      <div className="flex items-start justify-between gap-4 mb-2">
        <div>
          <div className="text-[10.5px] tracking-[0.22em] uppercase text-equinesync-graphite/50">
            Recent activity
          </div>
          <div className="mt-1 text-[13px] text-equinesync-graphite/65">
            Curated to admin / subscription / user / login / billing-event entries.
          </div>
        </div>
      </div>

      {loading && !items && (
        <div className="space-y-2 mt-3" data-testid="admin-activity-loading">
          {[0, 1, 2, 3, 4].map((i) => (
            <div key={i} className="h-12 bg-equinesync-graphite/5 rounded animate-pulse" />
          ))}
        </div>
      )}
      {error && (
        <div className="text-[13px] text-equinesync-graphite/70" data-testid="admin-activity-error">
          Could not load activity feed.
        </div>
      )}
      {!loading && items && items.length === 0 && (
        <div className="text-[13px] text-equinesync-graphite/50 py-6 text-center" data-testid="admin-activity-empty">
          No matching activity yet.
        </div>
      )}
      {items && items.length > 0 && (
        <div className="mt-2">
          {items.map((item, i) => (
            <Row key={item.id || `${item.action}-${i}`} item={item} />
          ))}
        </div>
      )}
    </section>
  );
}
