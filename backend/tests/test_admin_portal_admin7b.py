"""tests/test_admin_portal_admin7b.py — Reports + Integrations +
Settings + Admin Login (Phase Admin-7B).

Locked founder decisions (Feb 2026):
  1.  Reports readable by all 5 platform roles; CSV export gated tighter
      (no support_admin). support_admin may read reports but may NOT
      export CSV.
  2.  Integrations readable by super_admin, platform_admin, billing_admin,
      read_only_auditor (NOT support_admin).
  3.  Settings is super_admin + platform_admin only.
  5.  Static integration slugs (stripe / resend / webhooks / jobs) — no
      opaque Mongo refs.
  6.  Reports windows: 7d / 30d / 90d only.
  7.  CSV: single endpoint, `text/csv`, Stripe-shaped values scrubbed.
  8.  Admin login: existing /api/auth/login; redirect to dashboard if
      platform_role valid, else AdminForbidden.

CRITICAL guardrails enforced by this suite:
  - No raw Stripe IDs / secrets in any Admin-7B response.
  - No mutation methods on reports / integrations / settings.
  - Read audit events emitted for all 7 endpoints.
  - Admin-2 activity feed excludes the 7 new read prefixes.
  - Legacy /admin/billing and /admin/review-queue routes unaffected.
"""
from __future__ import annotations

import os
import pathlib
import re
import sys
import uuid
from datetime import datetime, timezone

import pytest
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

sys.path.insert(0, "/app/backend")
load_dotenv("/app/backend/.env")


def _base_url() -> str:
    v = os.environ.get("REACT_APP_BACKEND_URL")
    if v:
        return v.rstrip("/")
    env = pathlib.Path(__file__).resolve().parents[2] / "frontend" / ".env"
    for line in env.read_text().splitlines():
        if line.startswith("REACT_APP_BACKEND_URL="):
            return line.split("=", 1)[1].strip().rstrip("/")
    raise RuntimeError("REACT_APP_BACKEND_URL not configured")


BASE = _base_url()
API = f"{BASE}/api"

# Stripe-shaped values that MUST NEVER appear in Admin-7B responses.
STRIPE_VALUE_RE = re.compile(
    r'\b(sub|sk_live|sk_test|cus|evt|in|ch|pi|price|seti|whsec|rk)_[A-Za-z0-9_]{4,}\b'
)


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "test_database"]
    c.close()


def _signup(role: str = "horse_owner") -> dict:
    email = f"adm7b_{uuid.uuid4().hex[:10]}@example.com"
    r = requests.post(
        f"{API}/auth/signup",
        json={"email": email, "password": "securepass1",
              "full_name": "Adm7B Test", "role": role},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def _promote(db, user_id: str, platform_role: str):
    db.users.update_one({"id": user_id}, {"$set": {"platform_role": platform_role}})


def _admin_session(db, plat_role: str = "platform_admin") -> dict:
    s = _signup()
    _promote(db, s["user"]["id"], plat_role)
    return s


def _bearer(s: dict) -> dict:
    return {"Authorization": f"Bearer {s['token']}"}


# ---------------------------------------------------------------------
# /me — sections list must reflect Admin-7B SECTION_CAPABILITIES update.
# ---------------------------------------------------------------------
@pytest.mark.parametrize("role,expected_sections", [
    ("super_admin",       {"reports", "integrations", "settings"}),
    ("platform_admin",    {"reports", "integrations", "settings"}),
    ("billing_admin",     {"reports", "integrations"}),       # no settings
    ("read_only_auditor", {"reports", "integrations"}),       # no settings
    ("support_admin",     {"reports"}),                       # no integrations, no settings
])
def test_me_sections_reflect_admin7b_caps(db, role, expected_sections):
    s = _admin_session(db, role)
    r = requests.get(f"{API}/admin/portal/me", headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    sections = set(body["sections"])
    assert expected_sections.issubset(sections), (
        f"{role}: expected {expected_sections} ⊆ {sections}"
    )


def test_me_section_caps_payload_includes_admin7b(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/me", headers=_bearer(s), timeout=10)
    body = r.json()
    caps = body["section_capabilities"]
    # support_admin must be in reports but not in integrations/settings.
    assert "support_admin" in caps["reports"]
    assert "support_admin" not in caps["integrations"]
    assert "support_admin" not in caps["settings"]
    # billing_admin + read_only_auditor in integrations.
    assert "billing_admin" in caps["integrations"]
    assert "read_only_auditor" in caps["integrations"]
    # settings is exactly {super_admin, platform_admin}.
    assert set(caps["settings"]) == {"super_admin", "platform_admin"}


# ---------------------------------------------------------------------
# Reports — read role gates.
# ---------------------------------------------------------------------
REPORT_ENDPOINTS = [
    "/admin/portal/reports/usage",
    "/admin/portal/reports/subscriptions",
    "/admin/portal/reports/facilities",
]


@pytest.mark.parametrize("role", [
    "super_admin", "platform_admin", "support_admin",
    "billing_admin", "read_only_auditor",
])
@pytest.mark.parametrize("path", REPORT_ENDPOINTS)
def test_reports_readable_by_all_5_platform_roles(db, role, path):
    s = _admin_session(db, role)
    r = requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
    assert r.status_code == 200, f"{role} {path} got {r.status_code}: {r.text}"
    body = r.json()
    assert "window" in body
    assert "window_days" in body


@pytest.mark.parametrize("path", REPORT_ENDPOINTS)
def test_reports_denied_to_non_platform_user(db, path):
    s = _signup()  # no platform_role
    r = requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
    assert r.status_code in (401, 403)


@pytest.mark.parametrize("path", REPORT_ENDPOINTS)
def test_reports_window_validation(db, path):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}{path}?window=1d", headers=_bearer(s), timeout=10)
    assert r.status_code == 400
    r2 = requests.get(f"{API}{path}?window=junk", headers=_bearer(s), timeout=10)
    assert r2.status_code == 400


@pytest.mark.parametrize("window", ["7d", "30d", "90d"])
def test_reports_usage_accepts_valid_windows(db, window):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/reports/usage?window={window}",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    assert r.json()["window"] == window


def test_reports_no_raw_stripe_ids_in_responses(db):
    s = _admin_session(db, "platform_admin")
    for path in REPORT_ENDPOINTS:
        r = requests.get(f"{API}{path}?window=30d", headers=_bearer(s), timeout=10)
        assert r.status_code == 200
        assert not STRIPE_VALUE_RE.search(r.text), (
            f"Stripe-shaped value leaked in {path}: {r.text[:300]}"
        )


# ---------------------------------------------------------------------
# Reports — CSV export.
# ---------------------------------------------------------------------
@pytest.mark.parametrize("role", [
    "super_admin", "platform_admin", "billing_admin", "read_only_auditor",
])
def test_csv_export_allowed_for_admin_billing_auditor(db, role):
    s = _admin_session(db, role)
    r = requests.get(
        f"{API}/admin/portal/reports/export.csv?type=usage&window=30d",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 200, f"{role} got {r.status_code}: {r.text}"
    assert "text/csv" in r.headers.get("content-type", "")
    assert "attachment" in r.headers.get("content-disposition", "").lower()
    assert "metric,value" in r.text


def test_csv_export_denied_for_support_admin(db):
    """Decision 1: support_admin may read reports but may NOT export CSV."""
    s = _admin_session(db, "support_admin")
    r = requests.get(
        f"{API}/admin/portal/reports/export.csv?type=usage&window=30d",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 403, f"support_admin CSV got {r.status_code}: {r.text}"


@pytest.mark.parametrize("t", ["users", "facilities", "subscriptions", "usage"])
def test_csv_export_all_4_types(db, t):
    s = _admin_session(db, "platform_admin")
    r = requests.get(
        f"{API}/admin/portal/reports/export.csv?type={t}&window=30d",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 200
    assert "text/csv" in r.headers.get("content-type", "")
    # Filename mentions the type.
    assert t in r.headers.get("content-disposition", "")


def test_csv_export_invalid_type_rejected(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(
        f"{API}/admin/portal/reports/export.csv?type=stripeids&window=30d",
        headers=_bearer(s), timeout=10,
    )
    assert r.status_code == 400


def test_csv_export_scrubs_stripe_shaped_values(db):
    """Plant a Stripe-shaped tier/status string on a subscription and
    confirm it never reaches the CSV body."""
    s = _admin_session(db, "platform_admin")
    plant = f"sub_PLANT{uuid.uuid4().hex[:20]}"
    db.subscriptions.insert_one({
        "id": f"adm7b_plant_{uuid.uuid4().hex[:10]}",
        "barn_id": f"adm7b_barn_{uuid.uuid4().hex[:6]}",
        "status": plant,
        "tier": plant,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "_adm7b_plant": True,
    })
    try:
        r = requests.get(
            f"{API}/admin/portal/reports/export.csv?type=subscriptions&window=30d",
            headers=_bearer(s), timeout=10,
        )
        assert r.status_code == 200
        assert plant not in r.text, (
            f"Stripe-shaped value leaked into CSV: {r.text[:500]}"
        )
        assert not STRIPE_VALUE_RE.search(r.text), (
            f"Stripe-shaped value leaked into CSV: {r.text[:500]}"
        )
    finally:
        db.subscriptions.delete_many({"_adm7b_plant": True})


# ---------------------------------------------------------------------
# Integrations — read role gates.
# ---------------------------------------------------------------------
@pytest.mark.parametrize("role", [
    "super_admin", "platform_admin", "billing_admin", "read_only_auditor",
])
def test_integrations_list_allowed(db, role):
    s = _admin_session(db, role)
    r = requests.get(f"{API}/admin/portal/integrations",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200, f"{role} got {r.status_code}"
    body = r.json()
    assert "items" in body
    assert "total" in body
    slugs = {it["slug"] for it in body["items"]}
    assert slugs == {"stripe", "resend", "webhooks", "jobs"}


def test_integrations_list_denied_for_support_admin(db):
    """Decision 2: integrations excludes support_admin."""
    s = _admin_session(db, "support_admin")
    r = requests.get(f"{API}/admin/portal/integrations",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 403, f"support_admin integrations got {r.status_code}"


@pytest.mark.parametrize("slug", ["stripe", "resend", "webhooks", "jobs"])
def test_integration_detail_allowed_for_platform_admin(db, slug):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/integrations/{slug}",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert body["slug"] == slug
    assert "label" in body
    assert "configured" in body
    assert "status_label" in body


def test_integration_detail_denied_for_support_admin(db):
    s = _admin_session(db, "support_admin")
    r = requests.get(f"{API}/admin/portal/integrations/stripe",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 403


def test_integration_detail_unknown_slug_404(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/integrations/wibble",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 404


def test_integrations_response_no_raw_stripe_ids(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/integrations",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    assert not STRIPE_VALUE_RE.search(r.text), (
        f"Stripe-shaped value leaked in /integrations: {r.text[:500]}"
    )
    for slug in ("stripe", "resend", "webhooks", "jobs"):
        r2 = requests.get(f"{API}/admin/portal/integrations/{slug}",
                          headers=_bearer(s), timeout=10)
        assert r2.status_code == 200
        assert not STRIPE_VALUE_RE.search(r2.text), (
            f"Stripe-shaped value leaked in /integrations/{slug}: {r2.text[:500]}"
        )


# ---------------------------------------------------------------------
# Settings — read role gates.
# ---------------------------------------------------------------------
def test_settings_allowed_for_super_admin(db):
    s = _admin_session(db, "super_admin")
    r = requests.get(f"{API}/admin/portal/settings",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    for k in ("environment", "is_production", "feature_flags",
              "billing", "email", "scheduler", "cors", "auth_policy"):
        assert k in body, f"settings payload missing {k}"


def test_settings_allowed_for_platform_admin(db):
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/settings",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200


@pytest.mark.parametrize("role", ["support_admin", "billing_admin", "read_only_auditor"])
def test_settings_denied_for_lower_platform_roles(db, role):
    """Decision 3: settings is super_admin + platform_admin only."""
    s = _admin_session(db, role)
    r = requests.get(f"{API}/admin/portal/settings",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 403, f"{role} settings got {r.status_code}: {r.text}"


def test_settings_denied_for_non_platform_user(db):
    s = _signup()
    r = requests.get(f"{API}/admin/portal/settings",
                     headers=_bearer(s), timeout=10)
    assert r.status_code in (401, 403)


def test_settings_no_raw_secrets_or_stripe_ids(db):
    """Critical: settings exposes booleans + safe labels only — never
    raw env values, secrets, JWT secrets, webhook secrets, or Stripe
    IDs. We assert by absence of the actual env value of any sensitive
    var and by absence of Stripe-shaped value patterns."""
    s = _admin_session(db, "super_admin")
    r = requests.get(f"{API}/admin/portal/settings",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    txt = r.text
    # Stripe-shaped values must not appear.
    assert not STRIPE_VALUE_RE.search(txt), (
        f"Stripe-shaped value in /settings: {txt[:500]}"
    )
    # Specific env values must not leak.
    for env_key in ("JWT_SECRET", "STRIPE_API_KEY", "STRIPE_SECRET_KEY",
                    "STRIPE_WEBHOOK_SECRET", "RESEND_API_KEY",
                    "MONGO_URL"):
        raw = os.environ.get(env_key) or ""
        if raw and len(raw) >= 6:
            assert raw not in txt, (
                f"Env value of {env_key} leaked in /settings"
            )


# ---------------------------------------------------------------------
# Mutation methods on Admin-7B endpoints must be rejected (no writes).
# ---------------------------------------------------------------------
@pytest.mark.parametrize("path", [
    "/admin/portal/reports/usage",
    "/admin/portal/reports/subscriptions",
    "/admin/portal/reports/facilities",
    "/admin/portal/reports/export.csv",
    "/admin/portal/integrations",
    "/admin/portal/integrations/stripe",
    "/admin/portal/settings",
])
@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_admin7b_endpoints_reject_mutations(db, path, method):
    s = _admin_session(db, "super_admin")
    r = requests.request(
        method.upper(), f"{API}{path}", headers=_bearer(s),
        json={}, timeout=10,
    )
    assert r.status_code in (404, 405), (
        f"{method.upper()} {path} accepted (got {r.status_code})"
    )


# ---------------------------------------------------------------------
# Audit emission — confirm each read action shows up in audit_log.
# ---------------------------------------------------------------------
def test_audit_emission_for_all_7_admin7b_actions(db):
    s = _admin_session(db, "super_admin")
    actor_email = s["user"]["email"]

    # Fire every Admin-7B read endpoint.
    calls = [
        ("/admin/portal/reports/usage?window=30d",          "admin.portal.read.reports.usage"),
        ("/admin/portal/reports/subscriptions?window=30d",  "admin.portal.read.reports.subscriptions"),
        ("/admin/portal/reports/facilities?window=30d",     "admin.portal.read.reports.facilities"),
        ("/admin/portal/reports/export.csv?type=usage&window=30d", "admin.portal.read.reports.export"),
        ("/admin/portal/integrations",                      "admin.portal.read.integrations"),
        ("/admin/portal/integrations/stripe",               "admin.portal.read.integration_detail"),
        ("/admin/portal/settings",                          "admin.portal.read.settings"),
    ]
    for path, _action in calls:
        r = requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
        assert r.status_code == 200, f"{path} got {r.status_code}: {r.text}"

    # Confirm each action landed in audit_log for this actor.
    for _path, action in calls:
        n = db.audit_log.count_documents({
            "action": action, "actor_email": actor_email,
        })
        assert n >= 1, f"no audit_log row for {action}"


# ---------------------------------------------------------------------
# Dashboard activity feed must exclude all 7 Admin-7B read prefixes.
# ---------------------------------------------------------------------
def test_dashboard_activity_excludes_admin7b_reads(db):
    s = _admin_session(db, "super_admin")
    # Generate Admin-7B reads.
    for path in (
        "/admin/portal/reports/usage?window=30d",
        "/admin/portal/integrations",
        "/admin/portal/settings",
    ):
        requests.get(f"{API}{path}", headers=_bearer(s), timeout=10)
    # Now hit the curated activity feed.
    r = requests.get(f"{API}/admin/portal/activity?limit=100",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    bad_prefixes = (
        "admin.portal.read.reports.",
        "admin.portal.read.integrations",
        "admin.portal.read.integration_detail",
        "admin.portal.read.settings",
    )
    for item in body.get("items", []):
        action = item.get("action") or ""
        for p in bad_prefixes:
            assert not action.startswith(p), (
                f"Admin-7B read action {action!r} leaked into activity feed"
            )
    # Exclude-list reported by the endpoint must contain the 7 new
    # prefixes (decision 8a continuation).
    excl = set(body.get("exclude_prefixes") or [])
    for required in (
        "admin.portal.read.reports.usage",
        "admin.portal.read.reports.subscriptions",
        "admin.portal.read.reports.facilities",
        "admin.portal.read.reports.export",
        "admin.portal.read.integrations",
        "admin.portal.read.integration_detail",
        "admin.portal.read.settings",
    ):
        assert required in excl, f"activity feed exclude list missing {required}"


# ---------------------------------------------------------------------
# Admin Login — uses existing /api/auth/login.
# ---------------------------------------------------------------------
def test_admin_login_route_via_existing_auth_login(db):
    """Decision 8: dedicated frontend route uses existing /api/auth/login.
    Confirm the existing endpoint accepts an Admin-7B platform user and
    returns a session bearer + user object."""
    s = _signup()
    _promote(db, s["user"]["id"], "platform_admin")
    email = s["user"]["email"]
    r = requests.post(f"{API}/auth/login",
                      json={"email": email, "password": "securepass1"},
                      timeout=15)
    assert r.status_code == 200
    body = r.json()
    assert "token" in body
    user = body["user"]
    # The current user response should carry platform_role so the
    # frontend can decide to land in dashboard vs AdminForbidden.
    assert user.get("platform_role") == "platform_admin"


def test_admin_portal_me_after_existing_auth_login(db):
    """Confirm post-login the standard /admin/portal/me works and
    indicates Admin-7B sections are reachable."""
    s = _admin_session(db, "platform_admin")
    r = requests.get(f"{API}/admin/portal/me", headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert body["platform_role"] == "platform_admin"
    assert "reports" in body["sections"]
    assert "integrations" in body["sections"]
    assert "settings" in body["sections"]


# ---------------------------------------------------------------------
# Legacy /admin/billing and /admin/review-queue must still register
# (route-map preservation invariant from Admin-1).
# ---------------------------------------------------------------------
def test_legacy_admin_routes_still_registered():
    sys.path.insert(0, "/app/backend")
    from server import app
    paths = {getattr(r, "path", None) for r in app.routes}
    # The platform portal lives under /api/admin/portal/*; the legacy
    # barn-admin routes live under /api/admin/* (no /portal/).
    # We can't check the React-side `/admin/billing` / `/admin/review-queue`
    # routes from here, but their backend support must still exist.
    legacy_present = any(p and p.startswith("/api/admin/")
                         and not p.startswith("/api/admin/portal/") for p in paths)
    assert legacy_present, (
        "Legacy /api/admin/* routes (review queue, etc.) appear to have "
        "regressed — Admin-7B must not touch them."
    )



# ---------------------------------------------------------------------
# Codex round-2 fixes — Stripe env contract & FE/BE caps mirror.
# ---------------------------------------------------------------------
def test_stripe_configured_uses_phase15_env_contract(db, monkeypatch):
    """Codex round-2 blocker #1: Phase 15 uses STRIPE_API_KEY (see
    `routes/subscriptions.py`, `core/billing_provisioning.py`,
    `routes/membership.py`). The Admin Portal "Stripe configured"
    badge MUST therefore read STRIPE_API_KEY (with STRIPE_SECRET_KEY
    as a non-authoritative fallback) — otherwise the badge can read
    "not configured" on a working production env.

    Admin-7A.2a (Feb 2026): the Stripe-configured helper moved out of
    portal.py into the per-surface integrations module. We now assert
    the contract on `integrations.stripe_configured` directly AND on
    its source — both the import and the env precedence (API_KEY
    first, SECRET_KEY fallback) must hold.
    """
    sys.path.insert(0, "/app/backend")
    src = pathlib.Path(
        "/app/backend/routes/admin_portal/integrations.py"
    ).read_text()
    assert "STRIPE_API_KEY" in src, (
        "integrations.py must read STRIPE_API_KEY (Phase 15 contract)."
    )
    # Backwards tolerance: STRIPE_SECRET_KEY may still appear as a
    # documented fallback, but STRIPE_API_KEY must be the first check.
    api_idx = src.find("STRIPE_API_KEY")
    sec_idx = src.find("STRIPE_SECRET_KEY")
    if sec_idx != -1:
        assert api_idx < sec_idx, (
            "STRIPE_API_KEY must be checked before STRIPE_SECRET_KEY "
            "fallback in integrations.py."
        )

    # Behavioural assertion: with STRIPE_API_KEY set and SECRET_KEY
    # explicitly unset, the helper must return True.
    from routes.admin_portal.integrations import stripe_configured
    monkeypatch.setenv("STRIPE_API_KEY", "sk_test_admin7a2a_assert")
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
    assert stripe_configured() is True

    # And with neither set, must return False.
    monkeypatch.delenv("STRIPE_API_KEY", raising=False)
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
    assert stripe_configured() is False

    # SECRET_KEY-only fallback continues to work.
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_fallback")
    assert stripe_configured() is True


def test_integrations_stripe_reports_configured_when_api_key_set(db):
    """End-to-end positive case: with the live `STRIPE_API_KEY` env
    populated (the dev pod ships sk_test_emergent), the integrations
    detail page must report `configured=True`. This is the regression
    Codex flagged — previously the badge would say "not configured"
    despite a working Phase 15 install."""
    s = _admin_session(db, "platform_admin")
    has_api_key = bool((os.environ.get("STRIPE_API_KEY") or "").strip())
    if not has_api_key:
        pytest.skip("STRIPE_API_KEY not configured in this env")
    r = requests.get(f"{API}/admin/portal/integrations/stripe",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    assert r.json()["configured"] is True, (
        "Stripe must report configured=True when STRIPE_API_KEY is set "
        "(Phase 15 env contract)."
    )


def test_settings_stripe_configured_when_api_key_set(db):
    """Same regression on the /settings surface — `billing.stripe_configured`
    must reflect STRIPE_API_KEY, not STRIPE_SECRET_KEY."""
    s = _admin_session(db, "platform_admin")
    has_api_key = bool((os.environ.get("STRIPE_API_KEY") or "").strip())
    if not has_api_key:
        pytest.skip("STRIPE_API_KEY not configured in this env")
    r = requests.get(f"{API}/admin/portal/settings",
                     headers=_bearer(s), timeout=10)
    assert r.status_code == 200
    assert r.json()["billing"]["stripe_configured"] is True


def test_frontend_section_caps_mirror_matches_backend():
    """Codex round-2 blocker #2: `frontend/src/lib/permissions.js`
    `ADMIN_SECTION_CAPS` MUST mirror backend
    `SECTION_CAPABILITIES` exactly. Previously the mirror omitted
    support_admin from subscriptions and dropped support_admin +
    billing_admin from audit_logs, which silently hid locked
    Admin-5/Admin-6 surfaces from roles the backend explicitly
    allows.

    This regression test is source-level so it runs without a
    browser / build step and guards future edits to either map.
    """
    import json as _json
    import re as _re

    sys.path.insert(0, "/app/backend")
    from routes.admin_portal.portal import SECTION_CAPABILITIES as BE_CAPS

    fe_src = pathlib.Path("/app/frontend/src/lib/permissions.js").read_text()
    m = _re.search(
        r"export const ADMIN_SECTION_CAPS\s*=\s*\{(.+?)\};",
        fe_src, _re.DOTALL,
    )
    assert m, "Could not locate ADMIN_SECTION_CAPS in permissions.js"
    body = m.group(1)

    # Parse `key: [ "...", "..." ],` lines into a dict.
    fe_caps: dict = {}
    for line in body.splitlines():
        kv = _re.match(r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*\[(.+?)\]\s*,?\s*$",
                       line.strip())
        if not kv:
            continue
        key = kv.group(1)
        arr = "[" + kv.group(2) + "]"
        # Convert single quotes to double quotes for JSON parsing.
        arr_json = arr.replace("'", '"')
        try:
            fe_caps[key] = _json.loads(arr_json)
        except Exception as e:  # pragma: no cover - parser drift
            raise AssertionError(f"Failed to parse FE caps for {key}: {e}")

    be_caps = {k: list(v) for k, v in BE_CAPS.items()}

    # Same key set on both sides.
    assert set(fe_caps.keys()) == set(be_caps.keys()), (
        "Section keys differ between FE and BE caps maps.\n"
        f"  FE-only: {set(fe_caps) - set(be_caps)}\n"
        f"  BE-only: {set(be_caps) - set(fe_caps)}"
    )

    # Same role list per key (order-independent).
    diffs = []
    for k in be_caps:
        if sorted(fe_caps[k]) != sorted(be_caps[k]):
            diffs.append(f"  {k}: FE={fe_caps[k]} vs BE={be_caps[k]}")
    assert not diffs, (
        "FE permissions.js ADMIN_SECTION_CAPS is out of sync with "
        "backend SECTION_CAPABILITIES:\n" + "\n".join(diffs)
    )

    # And specifically lock the three roles Codex flagged in round-2.
    assert "support_admin" in fe_caps["subscriptions"], (
        "FE mirror must include support_admin in 'subscriptions'."
    )
    assert "support_admin" in fe_caps["audit_logs"], (
        "FE mirror must include support_admin in 'audit_logs'."
    )
    assert "billing_admin" in fe_caps["audit_logs"], (
        "FE mirror must include billing_admin in 'audit_logs'."
    )
