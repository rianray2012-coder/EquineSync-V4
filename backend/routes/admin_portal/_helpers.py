"""routes/admin_portal/_helpers.py — shared Admin Portal helpers.

Admin-7A.2a (physical move, Feb 2026):
  This file now OWNS the implementations of the shared helpers used by
  every Admin Portal surface module. Admin-7A.1 created the boundary
  via a re-export shim; Admin-7A.2a completes the move by physically
  relocating the helper bodies here so the per-surface modules in
  `routes/admin_portal/` (`reports.py`, `integrations.py`,
  `settings.py`, and — in Admin-7A.2b — `dashboard.py`, `users.py`,
  `facilities.py`, `subscriptions.py`, `billing.py`, `audit_logs.py`,
  `support.py`, `alerts.py`) can `from . import _helpers` directly.

  The portal.py monolith now imports these names FROM `_helpers.py`,
  inverting the dependency. The locked helper surface
  (`SECTION_CAPABILITIES`, `_scrub_text`, `_admin_ref` etc.) is
  unchanged byte-for-byte; Admin-7A.1's behaviour-preservation
  invariants therefore continue to hold.

  NOTE: the package path is `routes/admin_portal/`, NOT
  `routes/admin/` — the legacy `routes/admin.py` (seed + tenant-reset)
  owns the `routes.admin` import path.

Locked invariants (continuing from Admin-6 round-2):
  - `_scrub_text()` is **Stripe-ID redaction ONLY**. Do NOT describe
    it as general secret/token/password scrubbing — that policy lives
    in `_scrub_metadata`'s sensitive-key drop list, which is a
    separate code path.
"""
from __future__ import annotations

import re as _re_module
from typing import Any, Dict, List, Optional

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException


# ----------------------------------------------------------------------
# Sidebar capability map (consumed by /admin/portal/me + frontend mirror)
# ----------------------------------------------------------------------
SECTION_CAPABILITIES: Dict[str, List[str]] = {
    "dashboard":     ["super_admin", "platform_admin", "support_admin", "billing_admin", "read_only_auditor"],
    "users":         ["super_admin", "platform_admin", "support_admin"],
    "facilities":    ["super_admin", "platform_admin", "support_admin"],
    "horses":        ["super_admin", "platform_admin", "support_admin"],
    "approvals":     ["super_admin", "platform_admin"],
    "subscriptions": ["super_admin", "platform_admin", "support_admin", "billing_admin", "read_only_auditor"],
    "billing":       ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
    "permissions":   ["super_admin", "platform_admin"],
    "support":       ["super_admin", "platform_admin", "support_admin"],
    "alerts":        ["super_admin", "platform_admin", "support_admin", "billing_admin"],
    # Admin-7B (locked Feb 2026): Reports readable by all 5 platform
    # roles; CSV export gated tighter (see reports.REPORTS_CSV_ROLES).
    "reports":       ["super_admin", "platform_admin", "support_admin", "billing_admin", "read_only_auditor"],
    # Admin-7B: integrations is read-only operational visibility — NOT
    # a support surface, so support_admin is excluded.
    "integrations":  ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
    "settings":      ["super_admin", "platform_admin"],
    "audit_logs":    ["super_admin", "platform_admin", "support_admin", "billing_admin", "read_only_auditor"],
}


def _sections_for(role: str) -> List[str]:
    """Return the list of sidebar section keys the given platform_role can see."""
    return [s for s, allowed in SECTION_CAPABILITIES.items() if role in allowed]


# ----------------------------------------------------------------------
# Activity feed allowlist/exclude — used by dashboard surface.
# ----------------------------------------------------------------------
# Curated activity allowlist (prefixes). Anything that doesn't match one
# of these falls out of the admin feed. Keeps the surface calm; full
# trail is still queryable via the dedicated audit-log surface (Admin-6).
_ACTIVITY_PREFIXES = (
    "admin.",
    "subscription.",
    "user.",
    "auth.login.",
    "billing.event.",
    "permission.denied",      # security signal
)

# Codex round-1 (Admin-2) blocker fix: the activity feed must NOT show
# its own dashboard reads back to itself. Read prefixes for every
# Admin-N surface that adds operator-only reads land here so the
# curated Admin-2 dashboard feed does not self-flood.
_ACTIVITY_EXCLUDE_PREFIXES = (
    # Base Admin-1/2 reads.
    "admin.portal.read.",
    "admin.portal.me",
    # Admin-5 reads (decision 8a — Subscription + Billing Control Center).
    "admin.portal.read.subscriptions",
    "admin.portal.read.subscription_detail",
    "admin.portal.read.billing_events",
    "admin.portal.read.payments",
    # Admin-6 reads (decision 8a continuation — Audit Logs + Support + Alerts).
    "admin.portal.read.audit_logs",
    "admin.portal.read.audit_log_detail",
    "admin.portal.read.support",
    "admin.portal.read.support_detail",
    "admin.portal.read.alerts",
    # Admin-7B reads (locked Feb 2026 — Reports / Integrations / Settings).
    "admin.portal.read.reports.usage",
    "admin.portal.read.reports.subscriptions",
    "admin.portal.read.reports.facilities",
    "admin.portal.read.reports.export",
    "admin.portal.read.integrations",
    "admin.portal.read.integration_detail",
    "admin.portal.read.settings",
)


# ----------------------------------------------------------------------
# Defensive scrub list — these keys must NEVER appear in an activity
# response, even if they leaked into audit_log metadata.
# ----------------------------------------------------------------------
_METADATA_SCRUB_KEYS = {
    "password", "password_hash", "token", "access_token", "refresh_token",
    "jwt", "stripe_secret_key", "stripe_webhook_secret", "client_secret",
    "api_key",
}


# ----------------------------------------------------------------------
# Stripe-shaped ID redaction.
# ----------------------------------------------------------------------
# Codex round-1 fix:
#   * adds `pi_` (payment_intent) and `ch_` (charge) prefixes
#   * scrubs EMBEDDED Stripe IDs inside longer strings, not just
#     whole-string matches
# Real Stripe IDs are `<prefix>_<14-32 base62 chars>` (no underscores
# inside the body). The 14-char minimum keeps the regex from matching
# legitimate snake_case words like `in_progress`, `branch_alpha`, etc.
_STRIPE_VALUE_PATTERNS = ("sub", "evt", "in", "cus", "price", "pi", "ch")
_STRIPE_EMBEDDED_RE = _re_module.compile(
    r"\b(?:" + "|".join(_STRIPE_VALUE_PATTERNS) + r")_[A-Za-z0-9]{14,}\b"
)
# Whole-string variant — for the readable "[stripe_id_redacted]"
# marker on a value that is EXACTLY a Stripe id. Allows the historical
# inner-`_` shape some test fixtures used.
_STRIPE_VALUE_RE = _re_module.compile(
    r"^(?:" + "|".join(_STRIPE_VALUE_PATTERNS) + r")_[A-Za-z0-9_]{4,}$"
)
_METADATA_VALUE_MAX_LEN = 256


def _redact_stripe_in_string(s: str) -> str:
    """Replace every Stripe-shaped substring inside `s` with
    `[stripe_id_redacted]`. Used so longer strings carrying an
    embedded Stripe ID (e.g. error messages like "missing sub_xxx")
    don't leak."""
    return _STRIPE_EMBEDDED_RE.sub("[stripe_id_redacted]", s)


def _scrub_metadata(meta: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Strip any sensitive-looking keys from audit metadata before
    surfacing it. Defense-in-depth — these keys should never have been
    logged in the first place. Also redacts Stripe-shaped values
    (exact AND embedded) and truncates long strings."""
    if not isinstance(meta, dict):
        return {}
    out: Dict[str, Any] = {}
    for k, v in meta.items():
        k_low = str(k).lower()
        if k_low in _METADATA_SCRUB_KEYS:
            continue
        if any(s in k_low for s in ("password", "secret", "token",
                                    "signature", "authorization", "cookie",
                                    "api_key")):
            continue
        out[k] = _scrub_metadata_value(v)
    return out


def _scrub_metadata_value(v: Any) -> Any:
    """Recursively scrub a metadata value: redact Stripe-shaped strings
    (both whole-string and embedded), truncate long strings, preserve
    numerics/bools/None, recurse into nested dicts/lists."""
    if isinstance(v, str):
        # Whole-string redaction (kept for backwards readability —
        # operator sees a clean marker rather than a partial match).
        if _STRIPE_VALUE_RE.match(v):
            return "[stripe_id_redacted]"
        # Embedded redaction — catches Stripe IDs nested inside longer
        # strings like "Error: subscription sub_xyz failed".
        v = _redact_stripe_in_string(v)
        if len(v) > _METADATA_VALUE_MAX_LEN:
            return v[:_METADATA_VALUE_MAX_LEN] + "…(truncated)"
        return v
    if isinstance(v, dict):
        return _scrub_metadata(v)
    if isinstance(v, list):
        return [_scrub_metadata_value(x) for x in v]
    return v


def _scrub_text(s: Optional[str]) -> Optional[str]:
    """Boundary scrub for free-text fields destined for the API
    surface. **Stripe-ID redaction ONLY** — replaces embedded
    Stripe-shaped substrings with `[stripe_id_redacted]`. Does NOT
    drop general secrets, tokens, or passwords (that policy lives in
    `_scrub_metadata`'s sensitive-key drop list). Callers handle
    length policy."""
    if not isinstance(s, str):
        return s
    return _redact_stripe_in_string(s)


# ----------------------------------------------------------------------
# Opaque admin_ref system (Admin-5 onward).
#
# Per locked decision 4a, Admin-5+ surfaces only opaque local refs —
# raw Stripe-shaped IDs (`sub_…`, `evt_…`, `in_…`, `cus_…`, `price_…`)
# NEVER cross the API boundary, even when they happen to BE the local
# entity id.
# ----------------------------------------------------------------------
def _admin_ref(prefix: str, mongo_id) -> str:
    """Return an opaque, API-safe identifier derived from Mongo `_id`.
    Never Stripe-shaped. Example: `as_507f1f77bcf86cd799439011`."""
    return f"{prefix}_{str(mongo_id)}"


def _resolve_admin_ref(prefix: str, ref: str) -> ObjectId:
    """Parse a `<prefix>_<hex24>` admin_ref back to its Mongo ObjectId.
    Any malformed input → 404 (we never reveal which prefix was used)."""
    expected = f"{prefix}_"
    if not ref or not ref.startswith(expected):
        raise HTTPException(404, "Not found.")
    try:
        return ObjectId(ref[len(expected):])
    except (InvalidId, TypeError, ValueError):
        raise HTTPException(404, "Not found.")


def _attach_admin_ref(prefix: str, row: Dict[str, Any]) -> Dict[str, Any]:
    """Mint `admin_ref` from `_id`; drop both `_id` and raw `id` from
    the outbound payload. Mutates and returns the row."""
    if not isinstance(row, dict):
        return row
    mid = row.pop("_id", None)
    row.pop("id", None)
    if mid is not None:
        row["admin_ref"] = _admin_ref(prefix, mid)
    return row


def _strip_keys(doc: Optional[Dict[str, Any]], keys) -> Optional[Dict[str, Any]]:
    if not isinstance(doc, dict):
        return doc
    return {k: v for k, v in doc.items() if k not in keys}


__all__ = [
    "SECTION_CAPABILITIES", "_sections_for",
    "_ACTIVITY_PREFIXES", "_ACTIVITY_EXCLUDE_PREFIXES",
    "_METADATA_SCRUB_KEYS", "_STRIPE_VALUE_PATTERNS",
    "_STRIPE_EMBEDDED_RE", "_STRIPE_VALUE_RE", "_METADATA_VALUE_MAX_LEN",
    "_redact_stripe_in_string", "_scrub_metadata", "_scrub_metadata_value",
    "_scrub_text",
    "_admin_ref", "_resolve_admin_ref", "_attach_admin_ref",
    "_strip_keys",
]
