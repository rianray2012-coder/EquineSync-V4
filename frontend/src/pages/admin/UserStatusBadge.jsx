/**
 * UserStatusBadge — small pill that renders a user's role_status,
 * account_status, or platform_role using ONLY the approved Admin
 * Portal palette (Midnight Graphite / Slate Navy / Frost White /
 * Smoky Lilac). No red/amber/green/blue tokens allowed.
 */
import React from "react";

const TONE = {
  // Approved palette only — see /admin/portal color guardrail.
  active:        "bg-equinesync-lilac/20 text-equinesync-graphite border-equinesync-lilac/40",
  pending:       "bg-equinesync-graphite/5 text-equinesync-graphite/80 border-equinesync-graphite/15",
  rejected:      "bg-equinesync-slate text-equinesync-frost border-equinesync-slate",
  suspended:     "bg-equinesync-slate text-equinesync-frost border-equinesync-slate",
  platform:      "bg-equinesync-lilac/40 text-equinesync-graphite border-equinesync-slate/30",
  muted:         "bg-equinesync-graphite/5 text-equinesync-graphite/55 border-equinesync-graphite/10",
};

const LABEL_TO_TONE = {
  active: "active", approved: "active", paid: "active", ok: "active",
  trialing: "pending", processing: "pending",
  past_due: "pending", retry_502: "pending",
  metadata_missing_retryable: "pending", incomplete: "pending",
  pending_review: "pending", pending: "pending", draft: "pending", open: "pending",
  rejected: "rejected",
  suspended: "suspended",
  canceled: "muted", void: "muted", uncollectible: "muted",
  unpaid: "muted", incomplete_expired: "muted",
  metadata_missing_permanent: "rejected", unknown_event: "muted",
};

export default function UserStatusBadge({ value, kind = "status" }) {
  if (!value) return null;
  const slug = String(value).toLowerCase();
  const tone = kind === "platform" ? "platform" : (LABEL_TO_TONE[slug] || "muted");
  const display =
    kind === "platform" ? value.replace(/_/g, " ") : slug.replace(/_/g, " ");
  return (
    <span
      data-testid={`user-status-${kind}-${slug}`}
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10.5px] tracking-[0.16em] uppercase border ${TONE[tone]}`}
    >
      {display}
    </span>
  );
}
