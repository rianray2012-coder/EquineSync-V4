"""routes/admin_portal/portal.py — Phase Admin-7A.2b thin orchestrator.

Admin-7A.2b (Feb 2026): all 11 Admin Portal surfaces (8 legacy
Admin-1..6 + 3 Admin-7B) now live in their own per-surface modules.
This file is the orchestrator only — it owns:

  1. `build_router(*, db, get_current_user)` — the public factory
     server.py uses.
  2. The `ctx` namespace (`db`, `get_current_user`, `logger`, and the
     one true cross-surface helper `_facility_label_map`).
  3. A single `register` call into every surface module, in a stable
     order.

The 34 Admin Portal endpoints (26 GET + 8 POST) register under their
canonical paths — route-map preservation is locked by
`test_admin_portal_admin7a.py::LOCKED_GET_ROUTES` +
`LOCKED_POST_ROUTES`. No new endpoints, no role changes, no UI changes,
no audit changes vs Admin-7A.2a.

Behaviour for every endpoint is byte-identical; the bodies were lifted
verbatim into their surface module's `register(router, ctx)`.

DO NOT add route handlers to this file. New surfaces go in their own
file. New endpoints on existing surfaces go in the surface module.
"""
from __future__ import annotations

import logging
from types import SimpleNamespace
from typing import Dict, List, Optional

from fastapi import APIRouter

# Per-surface modules.
from . import alerts as _alerts_surface
from . import audit_logs as _audit_logs_surface
from . import billing as _billing_surface
from . import dashboard as _dashboard_surface
from . import facilities as _facilities_surface
from . import integrations as _integrations_surface
from . import reports as _reports_surface
from . import settings as _settings_surface
from . import subscriptions as _subscriptions_surface
from . import support as _support_surface
from . import users as _users_surface

# Re-export the locked helper surface for any legacy importer that
# still reaches into routes.admin_portal.portal. Admin-7A.2a moved the
# implementations into `_helpers.py`; this preserves the existing
# import path identity invariant (locked by
# test_admin_portal_admin7a2::test_helpers_module_owns_implementations).
from ._helpers import (
    SECTION_CAPABILITIES,
    _sections_for,
    _ACTIVITY_PREFIXES,
    _ACTIVITY_EXCLUDE_PREFIXES,
    _METADATA_SCRUB_KEYS,
    _STRIPE_VALUE_PATTERNS,
    _STRIPE_EMBEDDED_RE,
    _STRIPE_VALUE_RE,
    _METADATA_VALUE_MAX_LEN,
    _redact_stripe_in_string,
    _scrub_metadata,
    _scrub_metadata_value,
    _scrub_text,
    _admin_ref,
    _resolve_admin_ref,
    _attach_admin_ref,
    _strip_keys,
)

logger = logging.getLogger(__name__)


def build_router(*, db, get_current_user) -> APIRouter:
    """Compose the Admin Portal router by registering every surface
    module against a shared `ctx`. server.py calls this once at
    startup."""
    router = APIRouter(tags=["admin-portal"])

    # The one true cross-surface helper. Lives here (not in a surface
    # module) because it is consumed by subscriptions, billing, and
    # alerts — and moving it into any one of them would create an
    # import cycle. It's a thin Mongo wrapper; nothing else.
    async def _facility_label_map(barn_ids: List[str]) -> Dict[str, Optional[str]]:
        """Bulk-fetch facility names for a list of barn_ids. Returns a
        dict {barn_id: name or None}."""
        if not barn_ids:
            return {}
        rows = await db.barns.find(
            {"id": {"$in": list({b for b in barn_ids if b})}},
            {"_id": 0, "id": 1, "name": 1},
        ).to_list(length=len(barn_ids))
        return {r["id"]: r.get("name") for r in rows}

    ctx = SimpleNamespace(
        db=db,
        get_current_user=get_current_user,
        logger=logger,
        facility_label_map=_facility_label_map,
    )

    # Register every surface, in a stable order. Order is purely for
    # human readability — FastAPI sorts routes internally; the route
    # map is identical regardless of register order.
    _dashboard_surface.register(router, ctx)
    _users_surface.register(router, ctx)
    _facilities_surface.register(router, ctx)
    _subscriptions_surface.register(router, ctx)
    _billing_surface.register(router, ctx)
    _audit_logs_surface.register(router, ctx)
    _support_surface.register(router, ctx)
    _alerts_surface.register(router, ctx)
    # Admin-7B surfaces (already extracted in Admin-7A.2a).
    _reports_surface.register(router, ctx)
    _integrations_surface.register(router, ctx)
    _settings_surface.register(router, ctx)

    return router
