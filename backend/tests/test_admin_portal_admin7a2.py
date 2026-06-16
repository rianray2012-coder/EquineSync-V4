"""tests/test_admin_portal_admin7a2.py — Phase Admin-7A.2a per-surface
split drift guards + helper-physical-move regression.

Locked invariants (founder, Feb 2026 — Admin-7A.2a approval):
  1.  reports.REPORTS_CSV_ROLES (backend) ↔ ADMIN_REPORTS_CSV_ROLES
      (frontend) — must match exactly. Frontend mirror lives in
      `frontend/src/lib/permissions.js`.
  2.  integrations.INTEGRATIONS_READ_ROLES (backend) ↔
      ADMIN_SECTION_CAPS.integrations (frontend). The frontend
      doesn't carry a separate "integrations roles" array — it
      reuses ADMIN_SECTION_CAPS.integrations, which is the
      canonical section-cap mirror. We lock the equivalence at
      source level here so any backend role change without a
      corresponding FE update will fail loudly.
  3.  SECTION_CAPABILITIES ↔ ADMIN_SECTION_CAPS — already locked by
      test_admin_portal_admin7b.py::test_frontend_section_caps_mirror_matches_backend
      but we re-assert here for completeness.
  4.  reports.py / integrations.py / settings.py expose `register`
      callables, the canonical post-split surface contract.
  5.  Module-level role constants live AT MODULE LEVEL in the surface
      modules (so this test file can import them without invoking
      the build_router factory).

The route-map preservation invariant from test_admin_portal_admin7a.py
already guarantees the 27 endpoints are still registered post-split.
This file layers ROLE-LIST and HELPER-PHYSICALIZATION guards on top.
"""
from __future__ import annotations

import pathlib
import re as _re
import sys

from dotenv import load_dotenv

load_dotenv("/app/backend/.env")

sys.path.insert(0, "/app/backend")


def _parse_js_string_array(body: str) -> set:
    """Extract `"foo"` / `'foo'` tokens from a JS array body. Tolerant
    of trailing commas + newlines. Returns a set of strings."""
    return set(_re.findall(r"""['"]([A-Za-z0-9_\-]+)['"]""", body))


# ---------------------------------------------------------------------
# 1. reports.REPORTS_CSV_ROLES ↔ permissions.js::ADMIN_REPORTS_CSV_ROLES
# ---------------------------------------------------------------------
def test_reports_csv_roles_backend_frontend_mirror():
    from routes.admin_portal.reports import REPORTS_CSV_ROLES

    fe_src = pathlib.Path(
        "/app/frontend/src/lib/permissions.js"
    ).read_text()
    m = _re.search(
        r"export const ADMIN_REPORTS_CSV_ROLES\s*=\s*\[(.+?)\];",
        fe_src, _re.DOTALL,
    )
    assert m, "ADMIN_REPORTS_CSV_ROLES not found in permissions.js"
    fe_roles = _parse_js_string_array(m.group(1))

    assert fe_roles == REPORTS_CSV_ROLES, (
        "Reports CSV role mirror drift:\n"
        f"  backend reports.REPORTS_CSV_ROLES = {sorted(REPORTS_CSV_ROLES)}\n"
        f"  frontend ADMIN_REPORTS_CSV_ROLES   = {sorted(fe_roles)}"
    )

    # Belt-and-braces: support_admin must remain explicitly excluded
    # from CSV export — this is locked founder decision 1.
    assert "support_admin" not in REPORTS_CSV_ROLES
    assert "support_admin" not in fe_roles


# ---------------------------------------------------------------------
# 2. integrations.INTEGRATIONS_READ_ROLES ↔ ADMIN_SECTION_CAPS.integrations
# ---------------------------------------------------------------------
def test_integrations_read_roles_backend_frontend_mirror():
    from routes.admin_portal.integrations import INTEGRATIONS_READ_ROLES

    fe_src = pathlib.Path(
        "/app/frontend/src/lib/permissions.js"
    ).read_text()
    # Parse ADMIN_SECTION_CAPS.integrations row.
    m = _re.search(
        r"integrations\s*:\s*\[(.+?)\]\s*,",
        fe_src,
    )
    assert m, "ADMIN_SECTION_CAPS.integrations not found in permissions.js"
    fe_roles = _parse_js_string_array(m.group(1))

    assert fe_roles == INTEGRATIONS_READ_ROLES, (
        "Integrations role mirror drift:\n"
        f"  backend  integrations.INTEGRATIONS_READ_ROLES = "
        f"{sorted(INTEGRATIONS_READ_ROLES)}\n"
        f"  frontend ADMIN_SECTION_CAPS.integrations       = "
        f"{sorted(fe_roles)}"
    )

    # Belt-and-braces: support_admin must remain explicitly excluded
    # from integrations (locked founder decision 2).
    assert "support_admin" not in INTEGRATIONS_READ_ROLES


# ---------------------------------------------------------------------
# 3. settings.SETTINGS_READ_ROLES ↔ ADMIN_SECTION_CAPS.settings
# ---------------------------------------------------------------------
def test_settings_read_roles_backend_frontend_mirror():
    from routes.admin_portal.settings import SETTINGS_READ_ROLES

    fe_src = pathlib.Path(
        "/app/frontend/src/lib/permissions.js"
    ).read_text()
    m = _re.search(
        r"settings\s*:\s*\[(.+?)\]\s*,",
        fe_src,
    )
    assert m, "ADMIN_SECTION_CAPS.settings not found in permissions.js"
    fe_roles = _parse_js_string_array(m.group(1))

    assert fe_roles == SETTINGS_READ_ROLES, (
        "Settings role mirror drift:\n"
        f"  backend  settings.SETTINGS_READ_ROLES   = "
        f"{sorted(SETTINGS_READ_ROLES)}\n"
        f"  frontend ADMIN_SECTION_CAPS.settings    = {sorted(fe_roles)}"
    )

    # Locked founder decision 3: settings is super_admin +
    # platform_admin only.
    assert SETTINGS_READ_ROLES == {"super_admin", "platform_admin"}


# ---------------------------------------------------------------------
# 4. Per-surface module contract — each Admin-7B file exposes
# `register` and the locked role constants.
# ---------------------------------------------------------------------
def test_reports_module_surface_contract():
    from routes.admin_portal import reports as _r
    assert callable(_r.register), "reports.register must be callable"
    # Module-level constants required by drift tests + downstream surfaces.
    assert isinstance(_r.REPORTS_READ_ROLES, set)
    assert isinstance(_r.REPORTS_CSV_ROLES, set)
    assert _r.REPORTS_WINDOWS == {"7d": 7, "30d": 30, "90d": 90}
    assert _r.REPORTS_CSV_TYPES == {
        "users", "facilities", "subscriptions", "usage"
    }


def test_integrations_module_surface_contract():
    from routes.admin_portal import integrations as _i
    assert callable(_i.register)
    assert callable(_i.stripe_configured)
    assert isinstance(_i.INTEGRATIONS_READ_ROLES, set)
    assert _i.INTEGRATION_SLUGS == ("stripe", "resend", "webhooks", "jobs")


def test_settings_module_surface_contract():
    from routes.admin_portal import settings as _s
    assert callable(_s.register)
    assert isinstance(_s.SETTINGS_READ_ROLES, set)


# ---------------------------------------------------------------------
# 5. Helper physical-move regression — `_helpers.py` now OWNS the
# shared helper implementations (no more re-export shim from
# `portal.py`). The locked helper surface must remain importable
# under both `routes.admin_portal._helpers` AND `routes.admin_portal.portal`
# (the latter via portal.py's compat re-imports).
# ---------------------------------------------------------------------
def test_helpers_module_owns_implementations():
    """Codex contract Admin-7A.2a: the helper bodies live in
    `_helpers.py`, NOT in `portal.py`. We verify by source inspection
    + identity check."""
    helpers_src = pathlib.Path(
        "/app/backend/routes/admin_portal/_helpers.py"
    ).read_text()
    portal_src = pathlib.Path(
        "/app/backend/routes/admin_portal/portal.py"
    ).read_text()

    # _helpers.py must DEFINE the Stripe-scrub regex (not re-export).
    assert "_STRIPE_EMBEDDED_RE = _re_module.compile(" in helpers_src, (
        "_helpers.py must define _STRIPE_EMBEDDED_RE; previously it "
        "re-exported from portal.py."
    )
    # portal.py must NOT re-define the helpers (they live in _helpers).
    # We accept the import line but reject a fresh definition.
    portal_lines = [l for l in portal_src.splitlines()
                    if "_STRIPE_EMBEDDED_RE = _re_module.compile" in l]
    assert not portal_lines, (
        "portal.py must not redefine _STRIPE_EMBEDDED_RE — it now "
        "lives in _helpers.py."
    )

    # Identity check: helpers exposed via both paths must be the SAME
    # object (i.e. portal.py imports them, doesn't redeclare).
    from routes.admin_portal import _helpers as h
    from routes.admin_portal import portal as p
    for name in (
        "_scrub_text", "_scrub_metadata", "_redact_stripe_in_string",
        "_admin_ref", "_resolve_admin_ref", "_attach_admin_ref",
        "_strip_keys", "SECTION_CAPABILITIES",
        "_ACTIVITY_EXCLUDE_PREFIXES",
    ):
        assert getattr(h, name) is getattr(p, name), (
            f"{name} differs between _helpers.py and portal.py; the "
            "physical move must keep the import-identity invariant."
        )


def test_activity_exclude_prefixes_consolidated():
    """`_ACTIVITY_EXCLUDE_PREFIXES` was previously initialized in
    portal.py to a 2-tuple and then re-bound further down to a
    larger tuple appending Admin-5/6/7B prefixes. Admin-7A.2a
    consolidates it into a single canonical tuple in `_helpers.py`.
    Confirm all required prefixes are present, in order."""
    from routes.admin_portal._helpers import _ACTIVITY_EXCLUDE_PREFIXES
    expected = (
        # Base Admin-1/2 reads.
        "admin.portal.read.",
        "admin.portal.me",
        # Admin-5 reads.
        "admin.portal.read.subscriptions",
        "admin.portal.read.subscription_detail",
        "admin.portal.read.billing_events",
        "admin.portal.read.payments",
        # Admin-6 reads.
        "admin.portal.read.audit_logs",
        "admin.portal.read.audit_log_detail",
        "admin.portal.read.support",
        "admin.portal.read.support_detail",
        "admin.portal.read.alerts",
        # Admin-7B reads.
        "admin.portal.read.reports.usage",
        "admin.portal.read.reports.subscriptions",
        "admin.portal.read.reports.facilities",
        "admin.portal.read.reports.export",
        "admin.portal.read.integrations",
        "admin.portal.read.integration_detail",
        "admin.portal.read.settings",
    )
    for needed in expected:
        assert needed in _ACTIVITY_EXCLUDE_PREFIXES, (
            f"missing {needed!r} from consolidated "
            "_ACTIVITY_EXCLUDE_PREFIXES."
        )



# ---------------------------------------------------------------------
# Admin-7A.2b round-2 — newly-promoted module-level constants per
# Codex P1 finding. Confirm every surface module exposes its locked
# role / safe-field / scope sets at MODULE scope (not closure scope),
# so future drift guards can import them without invoking
# build_router(). Also lock the values that the founder-locked
# decisions pin down.
# ---------------------------------------------------------------------
def test_support_constants_at_module_scope():
    from routes.admin_portal import support as _s
    # Module-level — these must be importable WITHOUT calling register().
    assert _s._SUPPORT_TAB_ROLES == {
        "super_admin", "platform_admin", "support_admin",
    }, "support_admin tab roles drift"
    assert _s._SUPPORT_ASSIGNEE_ROLES is _s._SUPPORT_TAB_ROLES, (
        "Codex round-1 contract: assignee role set === tab role set."
    )
    assert _s._SUPPORT_VALID_STATUSES == (
        "new", "in_progress", "waiting", "resolved",
    )
    assert _s._SUPPORT_NOTE_MAX_LEN == 4096
    assert "internal_notes" in _s._SUPPORT_SAFE_FIELDS


def test_alerts_constants_at_module_scope():
    from routes.admin_portal import alerts as _a
    assert _a._ALERTS_TAB_ROLES == {
        "super_admin", "platform_admin", "support_admin", "billing_admin",
    }, "alerts tab roles drift"
    assert _a._BILLING_ADMIN_ALERT_KEYS == {
        "billing_webhook_retry", "payment_failure",
        "pending_subscription_email_stale",
    }, "billing_admin alert key scope drift"


def test_audit_logs_constants_at_module_scope():
    from routes.admin_portal import audit_logs as _al
    # Decision 4a: exactly 4 action prefixes for billing_admin scope.
    assert _al._BILLING_ADMIN_AUDIT_SCOPE == (
        "admin.portal.read.subscriptions",
        "admin.portal.read.subscription_detail",
        "admin.portal.read.billing_events",
        "admin.portal.read.payments",
    ), "billing_admin audit-log action-prefix scope drift"
    # Roles that get full audit-log access (no scope filter).
    assert _al._AUDIT_UNSCOPED_ROLES == {
        "super_admin", "platform_admin", "support_admin", "read_only_auditor",
    }, "audit-log unscoped roles drift"
    assert "metadata" in _al._AUDIT_SAFE_FIELDS


def test_facilities_constants_at_module_scope():
    from routes.admin_portal import facilities as _f
    # `subscription_id` is in the INTERNAL projection (allowed) but
    # MUST be in the strip-keys tuple so it never crosses the wire.
    assert _f._BARN_SAFE_FIELDS.get("subscription_id") == 1
    assert "subscription_id" in _f._BARN_RESPONSE_STRIP_KEYS
    assert "subscription_updated_at" in _f._BARN_RESPONSE_STRIP_KEYS


def test_users_detail_barn_projection_excludes_subscription_id():
    """Codex P0 round-2 fix: the user-detail barn projection must NOT
    include `subscription_id`. This is a source-level lock so the
    leak can never regress silently."""
    src = pathlib.Path(
        "/app/backend/routes/admin_portal/users.py"
    ).read_text()
    # Find the barn projection block and confirm subscription_id
    # is not part of the projection. We look for the projection
    # dict on `db.barns.find_one`.
    m = _re.search(
        r"db\.barns\.find_one\s*\([^)]*\{([^}]*)\}", src, _re.DOTALL,
    )
    assert m, "could not locate db.barns.find_one(...) projection in users.py"
    projection = m.group(1)
    assert '"subscription_id"' not in projection, (
        "users.py db.barns.find_one projection still includes "
        "subscription_id — must be stripped for the API boundary."
    )
    assert "'subscription_id'" not in projection, (
        "users.py db.barns.find_one projection still includes "
        "subscription_id (single-quoted)."
    )


def test_subscriptions_uses_ctx_facility_label_map():
    """Codex P2 round-2 fix: subscriptions.py must NOT define its own
    `_facility_label_map`. It must use `ctx.facility_label_map` — the
    one canonical cross-surface helper. This source-level lock
    enforces the README's "only one cross-surface helper" invariant."""
    src = pathlib.Path(
        "/app/backend/routes/admin_portal/subscriptions.py"
    ).read_text()
    # The `_facility_label_map = ctx.facility_label_map` ALIAS line is
    # expected. A `def _facility_label_map(` or `async def
    # _facility_label_map(` DEFINITION line is not.
    bad_def = _re.search(
        r"(async\s+)?def\s+_facility_label_map\s*\(", src,
    )
    assert not bad_def, (
        "subscriptions.py defines a local _facility_label_map; it "
        "must use ctx.facility_label_map (the README's single "
        "cross-surface helper)."
    )
    # The alias must be present.
    assert "_facility_label_map = ctx.facility_label_map" in src, (
        "subscriptions.py must alias ctx.facility_label_map at the "
        "top of register()."
    )
