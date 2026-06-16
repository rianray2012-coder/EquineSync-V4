"""routes/admin_portal/_helpers.py — shared Admin Portal helpers.

Admin-7A.1 (layered split, Feb 2026):
  The helper SURFACE lives here so per-surface files in the upcoming
  Admin-7A.2 split (`dashboard.py`, `users.py`, `facilities.py`, …)
  have a single canonical import path:

      from routes.admin_portal._helpers import (
          SECTION_CAPABILITIES, _sections_for,
          _admin_ref, _resolve_admin_ref, _attach_admin_ref,
          _scrub_metadata, _scrub_text, _strip_keys,
          ...
      )

  NOTE: the package path is `routes/admin_portal/`, NOT
  `routes/admin/` — the legacy `routes/admin.py` (seed + tenant-reset)
  already owns the `routes.admin` import path. Admin-7A.1 deliberately
  avoided that collision.

  In this transitional phase, the implementations remain in
  `portal.py` (the file that previously was `admin_portal.py`) and
  `_helpers.py` re-exports them verbatim. This is intentional: the
  byte-identical re-export guarantees Admin-1 through Admin-6
  behavior is unchanged — the helper bodies are not touched in any
  way during the boundary creation.

  Admin-7A.2 will physically move the helper definitions into this
  file once the boundary is locked. At that point this docstring
  becomes "Helpers physically live here; see git history for the
  re-export shim that bridged 7A.1 → 7A.2."

Locked invariants (continuing from Admin-6 round-2):
  - `_scrub_text()` is **Stripe-ID redaction ONLY**. Do NOT describe
    it as general secret/token/password scrubbing — that policy lives
    in `_scrub_metadata`'s sensitive-key drop list, which is a
    separate code path.
"""
from __future__ import annotations

# Re-export from `portal.py`. The names here are the locked public
# surface of the helper boundary; per-surface modules import from
# this file going forward.
from .portal import (  # noqa: F401  — re-export
    SECTION_CAPABILITIES,
    _sections_for,
    _METADATA_SCRUB_KEYS,
    _STRIPE_VALUE_PATTERNS,
    _STRIPE_EMBEDDED_RE,
    _STRIPE_VALUE_RE,
    _METADATA_VALUE_MAX_LEN,
    _ACTIVITY_EXCLUDE_PREFIXES,
    _redact_stripe_in_string,
    _scrub_metadata,
    _scrub_metadata_value,
    _scrub_text,
    _admin_ref,
    _resolve_admin_ref,
    _attach_admin_ref,
    _strip_keys,
)

__all__ = [
    "SECTION_CAPABILITIES", "_sections_for",
    "_METADATA_SCRUB_KEYS", "_STRIPE_VALUE_PATTERNS",
    "_STRIPE_EMBEDDED_RE", "_STRIPE_VALUE_RE", "_METADATA_VALUE_MAX_LEN",
    "_ACTIVITY_EXCLUDE_PREFIXES",
    "_redact_stripe_in_string", "_scrub_metadata", "_scrub_metadata_value",
    "_scrub_text",
    "_admin_ref", "_resolve_admin_ref", "_attach_admin_ref",
    "_strip_keys",
]
