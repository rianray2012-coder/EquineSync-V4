"""EquineSync API — application assembly (Phase 3G).

This module is intentionally thin: it loads the environment, validates the
security-critical configuration, constructs the FastAPI app, wires every
domain router under ``/api``, attaches middleware, and registers the
application lifecycle (startup bootstrap + background loops).

All shared infrastructure now lives in ``core/*``:
  - ``core.db``        Mongo client + ``db`` handle
  - ``core.auth``      JWT helpers, ``get_current_user`` (Security Patch 2E gate)
  - ``core.helpers``   generic time/id + Mongo listing utilities
  - ``core.analytics`` ``_track`` event recorder
  - ``core.urls``      ``_base_url`` link resolution
  - ``core.constants`` ``ROLES`` / ``ROLE_LABELS``
  - ``core.lifespan``  startup/shutdown + materializer/dispatcher/digest/nudge loops

No module imports from ``server.py``; the ASGI entrypoint remains ``server:app``.
"""
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

# Load .env BEFORE importing any submodule that reads env vars at import time
# (core.config reads JWT_SECRET; core.db reads MONGO_URL/DB_NAME; auth_security
# reads JWT_EXP_HOURS).
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Centralized config validation — fail fast on missing/insecure security vars
# (Phase 2A). Must run after load_dotenv and before importing modules below
# that read env at import time.
from core.config import validate_config, get_cors_origins
validate_config()

# Shared infrastructure (imported only after .env load + config validation).
from core.db import db
import core.auth as _core_auth
from core.auth import get_current_user, create_token, hash_pwd, require_setup_role
from core.helpers import (
    new_id, clean, list_collection, _user_safe, _client_meta,
)
from core.analytics import _track
from core.urls import _base_url
from core.constants import ROLES, ROLE_LABELS
from core.lifespan import register_lifecycle
from core.logging_config import configure_logging
from core.middleware import RequestContextMiddleware

from auth_security import (
    JWT_EXP_HOURS,
    SecurityHeadersMiddleware,
    issue_refresh_token,
)
from mailer import send as send_email
from task_engine import (
    build_router as build_task_engine_router,
    DEFAULT_TENANT_ID as TASK_TENANT_ID,
)
from notifications import build_router as build_notifications_router
from routes.auth import build_router as build_auth_router
from routes.dashboard import build_router as build_dashboard_router
from routes.pulse import build_router as build_pulse_router
from routes.reports import build_router as build_reports_router
from routes.invites import build_router as build_invites_router
from routes.onboarding import build_router as build_onboarding_router, ONBOARDING_STEPS
from routes.care import build_router as build_care_router
from routes.horses import build_router as build_horses_router
from routes.operations import build_router as build_operations_router
from routes.billing import build_router as build_billing_router
from routes.membership import build_router as build_membership_router
from routes.admin_review import build_router as build_admin_review_router
from routes.subscriptions import build_router as build_subscriptions_router
from routes.subscription_emails import build_router as build_subscription_emails_router
from routes.admin_billing import build_router as build_admin_billing_router
from routes.recurring_charges import build_router as build_recurring_charges_router
from routes.system import build_router as build_system_router
from routes.admin import build_router as build_admin_router
from routes.analytics import build_router as build_analytics_router
from routes.digests import build_router as build_digests_router
from routes.barns import build_router as build_barns_router
from routes.audit import build_router as build_audit_router
from routes.owner_updates import build_router as build_owner_updates_router
from routes.owner import build_router as build_owner_router
from routes.backlog import build_router as build_backlog_router
from routes.horse_ledger import build_router as build_horse_ledger_router
from routes.account_context import build_router as build_account_context_router
from routes.student_guardians import build_router as build_student_guardians_router
from routes.document_signatures import build_router as build_document_signatures_router
from routes.rider_profile import build_router as build_rider_profile_router
from routes.guardian_intake import build_router as build_guardian_intake_router
from routes.owner_intake import build_router as build_owner_intake_router
from routes.barn_owner_intake import build_router as build_barn_owner_intake_router
from routes.trainer_intake import build_router as build_trainer_intake_router
from routes.trainer_operating_center import build_router as build_trainer_operating_center_router
from routes.service_provider_center import build_router as build_service_provider_center_router
from routes.manager_intake import build_router as build_manager_intake_router
from routes.staff_intake import build_router as build_staff_intake_router
from seed_data import run_seed

# Phase Admin-4b: tenancy enforcement for soft-disabled facilities.
# Builds the FastAPI dependency that blocks barn-scoped users whose
# facility has been disabled via the Admin Portal. Attached at
# `include_router(..., dependencies=[Depends(...)])` scope on every
# product/tenant-data router below. See PHASE_ADMIN_4B_README.md for
# the full applied/excluded inventory.
from fastapi import Depends as _Depends
from core.auth import security as _security
from core.tenancy import (
    make_require_active_facility,
    make_require_active_facility_optional_auth,
)
require_active_facility = make_require_active_facility(db, get_current_user)
PRODUCT_FACILITY_DEPS = [_Depends(require_active_facility)]

# Codex round-1 fix (Admin-4b): the Phase 15 subscriptions router (and
# the membership router) mix authenticated tenant routes with anonymous
# Stripe webhooks and public marketing endpoints. Attaching the strict
# dependency would 401 the webhook. The optional-auth variant passes
# anonymous requests through and only enforces the facility gate when
# a valid token is presented AND its user is barn-scoped.
require_active_facility_optional_auth = make_require_active_facility_optional_auth(
    db, _security,
)
PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH = [_Depends(require_active_facility_optional_auth)]

# Phase 10A: centralized structured logging + request-correlation filters
# (JSON in prod, plain in dev; configures the root logger).
configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="EquineSync API")
api_router = APIRouter(prefix="/api")

# ---------------- Router assembly ----------------
# Unified Task Engine
api_router.include_router(
    build_task_engine_router(
        db,
        get_current_user,
        _track,
        require_active_facility=require_active_facility,
    ),
)

# Auth (routes/auth.py)
api_router.include_router(build_auth_router(db))

# Build-Next-3B — read-only account context contract.
# Intentionally not attached to the product facility dependency list: this endpoint is a
# planning/selection surface that must remain readable before later phases move
# product route guards to membership-aware context selection.
api_router.include_router(build_account_context_router(
    db=db,
    get_current_user=get_current_user,
))

# Build-Next-13C — rider first-login profile/intake shell.
# Authenticated and rider-role scoped, but intentionally not attached to the
# facility product dependency: marketplace rider accounts may exist before
# joining an active facility.
api_router.include_router(build_rider_profile_router(
    db=db,
    get_current_user=get_current_user,
))

# Build-Next-13D — guardian + minor rider intake shell.
# Authenticated and parent-role scoped, but intentionally not attached to the
# facility product dependency: guardian accounts may complete first-login
# intake before the minor rider is connected to an active facility.
api_router.include_router(build_guardian_intake_router(
    db=db,
    get_current_user=get_current_user,
))

# Build-Next-13E — owner first-login intake shell.
# Authenticated and horse_owner-role scoped, but intentionally not attached to
# the facility product dependency: individual owner accounts may exist before
# joining an active facility or creating their first horse setup.
api_router.include_router(build_owner_intake_router(
    db=db,
    get_current_user=get_current_user,
))

# Build-Next-13F — barn owner first-login intake shell.
# Authenticated and barn_owner-role scoped, but intentionally not attached to
# the facility product dependency: facility founders may capture setup intent
# before creating or joining an active facility.
api_router.include_router(build_barn_owner_intake_router(
    db=db,
    get_current_user=get_current_user,
))

# Build-Next-13G — trainer first-login intake shell.
# Authenticated and trainer-role scoped, but intentionally not attached to the
# facility product dependency: marketplace trainer accounts may capture setup
# intent before assignments, lessons, or active facility membership are ready.
api_router.include_router(build_trainer_intake_router(
    db=db,
    get_current_user=get_current_user,
))

# RF9 — trainer operating-center read model. Facility-gated product data; unlike
# trainer intake, this reads active lesson/training/horse/rider context.
api_router.include_router(build_trainer_operating_center_router(
    db=db,
    get_current_user=get_current_user,
), dependencies=PRODUCT_FACILITY_DEPS)

# RF10 — explicit-grant service-provider operating center.
api_router.include_router(build_service_provider_center_router(
    db=db,
    get_current_user=get_current_user,
    new_id=new_id,
), dependencies=PRODUCT_FACILITY_DEPS)

# Build-Next-13H — barn manager first-login intake shell.
# Authenticated and barn_manager-role scoped, but intentionally not attached to
# the facility product dependency: manager accounts may capture setup intent
# before task ownership, staff coordination, or active facility context is ready.
api_router.include_router(build_manager_intake_router(
    db=db,
    get_current_user=get_current_user,
))

# Build-Next-13I — staff first-login intake shell.
# Authenticated and groom/working_student-role scoped, but intentionally not
# attached to the facility product dependency: staff accounts may capture setup
# intent before task assignment, HorseOps writes, or active facility context.
api_router.include_router(build_staff_intake_router(
    db=db,
    get_current_user=get_current_user,
))

# Notifications
api_router.include_router(
    build_notifications_router(db, get_current_user),
    dependencies=PRODUCT_FACILITY_DEPS,
)

# Dashboard (routes/dashboard.py)
api_router.include_router(
    build_dashboard_router(db, get_current_user, TASK_TENANT_ID),
)

# Build-Next-15A - read-only Today Pulse data contract for role-home pages.
# Not attached to product facility dependencies because it must serve platform
# admins and standalone individual-owner contexts as well as facility contexts.
api_router.include_router(
    build_pulse_router(db, get_current_user, TASK_TENANT_ID),
)

# Reports (routes/reports.py) — exposes send_nudges for the startup auto-nudge loop
_reports_router = build_reports_router(
    db=db,
    get_current_user=get_current_user,
    onboarding_steps=ONBOARDING_STEPS,
    mailer_send=send_email,
    track=lambda *a, **kw: _track(*a, **kw),
    base_url_from_request=lambda req: _base_url(req),
    require_setup_role=require_setup_role,
)
_send_nudges = _reports_router._reports_helpers["send_nudges"]
api_router.include_router(_reports_router, dependencies=PRODUCT_FACILITY_DEPS)

# Invites (routes/invites.py)
api_router.include_router(build_invites_router(
    db=db,
    get_current_user=get_current_user,
    require_setup_role=require_setup_role,
    roles=ROLES,
    role_labels=ROLE_LABELS,
    onboarding_steps=ONBOARDING_STEPS,
    mailer_send=send_email,
    track=_track,
    base_url_from_request=_base_url,
    create_token=create_token,
    hash_pwd=hash_pwd,
    verify_pwd=_core_auth.verify_pwd,
    user_safe=_user_safe,
    client_meta=_client_meta,
    issue_refresh_token=issue_refresh_token,
    jwt_exp_hours=JWT_EXP_HOURS,
    new_id=new_id,
    include_public=False,
), dependencies=PRODUCT_FACILITY_DEPS)
api_router.include_router(build_invites_router(
    db=db,
    get_current_user=get_current_user,
    require_setup_role=require_setup_role,
    roles=ROLES,
    role_labels=ROLE_LABELS,
    onboarding_steps=ONBOARDING_STEPS,
    mailer_send=send_email,
    track=_track,
    base_url_from_request=_base_url,
    create_token=create_token,
    hash_pwd=hash_pwd,
    verify_pwd=_core_auth.verify_pwd,
    user_safe=_user_safe,
    client_meta=_client_meta,
    issue_refresh_token=issue_refresh_token,
    jwt_exp_hours=JWT_EXP_HOURS,
    new_id=new_id,
    include_protected=False,
))

# Onboarding (routes/onboarding.py)
api_router.include_router(build_onboarding_router(
    db=db,
    get_current_user=get_current_user,
    require_setup_role=require_setup_role,
    roles=ROLES,
    list_collection=list_collection,
    clean=clean,
    new_id=new_id,
), dependencies=PRODUCT_FACILITY_DEPS)

# Build-Next-5B — guardian-first lesson-student onboarding foundation.
# Barn-scoped product surface; no messaging, waiver, payment, billing, or
# document workflows are introduced here.
api_router.include_router(build_student_guardians_router(
    db=db,
    get_current_user=get_current_user,
    mailer_send=send_email,
    base_url_from_request=_base_url,
    new_id=new_id,
), dependencies=PRODUCT_FACILITY_DEPS)

# Horses — horse-profile CRUD (routes/horses.py).
# NOTE: GET /horses/{id}/timeline intentionally remains in task_engine.py
# (it is a task-event projection, not horse-profile CRUD).
api_router.include_router(build_horses_router(
    db=db,
    get_current_user=get_current_user,
    list_collection=list_collection,
    clean=clean,
    new_id=new_id,
    require_active_facility=require_active_facility,
))

# Care records (routes/care.py)
api_router.include_router(build_care_router(
    db=db,
    get_current_user=get_current_user,
    list_collection=list_collection,
    clean=clean,
    new_id=new_id,
), dependencies=PRODUCT_FACILITY_DEPS)

# Operations (routes/operations.py)
api_router.include_router(build_operations_router(
    db=db,
    get_current_user=get_current_user,
    list_collection=list_collection,
    clean=clean,
    new_id=new_id,
), dependencies=PRODUCT_FACILITY_DEPS)

# Billing — invoices (routes/billing.py) — Phase 9 read path.
# Disabled-facility members cannot read tenant invoices; the underlying
# invoice/recurring_charge docs are NOT mutated by enforcement.
api_router.include_router(build_billing_router(
    db=db,
    get_current_user=get_current_user,
    list_collection=list_collection,
    clean=clean,
    new_id=new_id,
), dependencies=PRODUCT_FACILITY_DEPS)

# Marketplace membership — Stripe Checkout (routes/membership.py)
# Mixed-auth router (anonymous Stripe webhook + public `/membership/tiers`
# + authenticated tenant checkout). Use the optional-auth variant so
# anonymous routes pass through; authenticated calls from a disabled
# facility are still gated.
api_router.include_router(build_membership_router(
    db=db,
    get_current_user=get_current_user,
), dependencies=PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH)

# Admin marketplace review queue (routes/admin_review.py)
api_router.include_router(build_admin_review_router(
    db=db,
    get_current_user=get_current_user,
))

# Phase 15.A — facility-level Stripe Subscriptions (routes/subscriptions.py)
# Mixed-auth router (anonymous `/webhook/stripe-subscriptions` + public
# `/billing/plans-public` + authenticated tenant routes). Optional-auth
# variant: anonymous pass-through; authenticated tenant call from a
# disabled facility → 403 "Facility unavailable" (Codex round-1 fix).
api_router.include_router(build_subscriptions_router(
    db=db,
    get_current_user=get_current_user,
), dependencies=PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH)

# Phase 15.D — manual trigger for the subscription-email dispatcher.
api_router.include_router(build_subscription_emails_router(
    db=db,
    get_current_user=get_current_user,
))

# Phase 15.E — Platform-admin billing dashboard endpoints.
api_router.include_router(build_admin_billing_router(
    db=db,
    get_current_user=get_current_user,
))

# Recurring charges — Phase 9B-1 billing templates (routes/recurring_charges.py)
api_router.include_router(build_recurring_charges_router(
    db=db,
    get_current_user=get_current_user,
    clean=clean,
    new_id=new_id,
), dependencies=PRODUCT_FACILITY_DEPS)

# System — root + health (routes/system.py)
api_router.include_router(build_system_router(db))

# Admin — seed + tenant-reset (routes/admin.py)
api_router.include_router(build_admin_router(
    db=db,
    get_current_user=get_current_user,
    track=_track,
    run_seed=run_seed,
))

# Admin Portal — platform-level role foundation (Admin-1).
from routes.admin_portal import build_router as build_admin_portal_router  # noqa: E402
api_router.include_router(build_admin_portal_router(
    db=db,
    get_current_user=get_current_user,
))

# Analytics (routes/analytics.py)
api_router.include_router(build_analytics_router(db, get_current_user, require_setup_role),
                          dependencies=PRODUCT_FACILITY_DEPS)

# Owner digest + weekly recap HTTP routes (routes/digests.py)
api_router.include_router(build_digests_router(db=db, get_current_user=get_current_user),
                          dependencies=PRODUCT_FACILITY_DEPS)

# Barn provisioning — Phase 4D multi-barn (routes/barns.py)
api_router.include_router(build_barns_router(
    db=db,
    get_current_user=get_current_user,
    hash_pwd=hash_pwd,
    user_safe=_user_safe,
    new_id=new_id,
    onboarding_steps=ONBOARDING_STEPS,
), dependencies=PRODUCT_FACILITY_DEPS)

# Audit log read API — Phase 5D (routes/audit.py)
api_router.include_router(build_audit_router(db=db, get_current_user=get_current_user),
                          dependencies=PRODUCT_FACILITY_DEPS)

# Owner Updates — Phase 7A Owner Trust Layer (routes/owner_updates.py)
api_router.include_router(build_owner_updates_router(
    db=db,
    get_current_user=get_current_user,
    list_collection=list_collection,
    clean=clean,
    new_id=new_id,
), dependencies=PRODUCT_FACILITY_DEPS)

# Owner self-service reads — Phase 7D-2 (routes/owner.py)
api_router.include_router(build_owner_router(db=db, get_current_user=get_current_user),
                          dependencies=PRODUCT_FACILITY_DEPS)

# Codex feature backlog foundations — additive modules and integration-ready
# shells alongside the Emergent founder-beta routes.
api_router.include_router(build_backlog_router(
    db=db,
    get_current_user=get_current_user,
    new_id=new_id,
), dependencies=PRODUCT_FACILITY_DEPS)

# Build-Next-6A — document-signature provider readiness.
# Connector status only: no provider API calls, no envelopes, no signed document
# storage, and no participation gates.
api_router.include_router(
    build_document_signatures_router(get_current_user=get_current_user),
    dependencies=PRODUCT_FACILITY_DEPS,
)

# Phase HorseOps-1A — composed read-only Care Ledger endpoint.
# The line below is the Admin-4b enforcement gate for this surface.
# A disabled-facility member calling /api/horse-ledger/{horse_id} hits
# 403 "Facility unavailable" before any controller code runs. Removing
# `dependencies=PRODUCT_FACILITY_DEPS` would silently disable the gate —
# `test_get_ledger_disabled_facility_gate_applies` guards against that.
api_router.include_router(
    build_horse_ledger_router(db=db, get_current_user=get_current_user),
    dependencies=PRODUCT_FACILITY_DEPS,
)

app.include_router(api_router)

# ---------------- Middleware ----------------
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=get_cors_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)
# Phase 10A: outermost — assigns request_id + emits the request-completion log.
# Pure ASGI (contextvar-safe); additive X-Request-ID header only.
app.add_middleware(RequestContextMiddleware)

# ---------------- Lifecycle (startup/shutdown + background loops) ----------------
register_lifecycle(app, send_nudges=_send_nudges)
