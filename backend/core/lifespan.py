"""Application lifecycle: startup bootstrap + background loops (Phase 3G).

Relocated verbatim from ``server.py`` during the app-assembly refactor. All
behavior — auto-seed policy (Security Patch 2E), Task Engine bootstrap, index
ensures, the email_verified backfill, starter-template hook, the rolling
materializer, the notification dispatcher, the owner daily-digest + weekly-recap
schedulers, and the auto-nudge loop — is preserved exactly, including every
``DISABLE_*`` flag, env-driven timing, and warm-up delay.

The only non-local dependency is ``send_nudges`` (derived from the reports
router that is assembled in ``server.py``); it is injected via
``register_lifecycle`` rather than imported, so this module never imports from
``server.py``.
"""
import asyncio
import logging
import os
from datetime import datetime, timezone

from core.config import auto_seed_enabled
from core.db import client, db
from core.analytics import _track
from core import runtime_state
from seed_data import run_seed
from task_engine import TaskEngine, seed_starter_templates
from auth_security import ensure_refresh_indexes
from notifications import (
    start_dispatcher as start_notification_dispatcher,
    ensure_indexes as ensure_notification_indexes,
)
from core.auth_tokens import ensure_auth_token_indexes
from core.audit import ensure_audit_indexes
from routes.billing import ensure_billing_indexes
from routes.backlog import BACKLOG_RESET_COLLECTIONS, ensure_backlog_indexes
from mailer import send as send_email, render as render_email
from owner_digest import (
    run_daily_digest_pass,
    ensure_digest_indexes,
    run_weekly_recap_pass,
)

logger = logging.getLogger(__name__)

PRIMARY_BARN_ID = "primary"

# Phase 4A: domain collections that gain a canonical `barn_id`.
# Phase 4B-7 extends this to the task-engine + `media` collections (previously
# excluded): they keep `tenant_id="default"` as the engine partition, and now
# additionally carry a canonical `barn_id` (the additive backfill below stamps
# legacy docs; the engine/storage write-paths stamp new docs). The user-keyed
# notification collections, the `barn` singleton (keyed by its own `id`), and
# all auth/session/attempt infra remain excluded.
BARN_BACKFILL_COLLECTIONS = [
    "users", "horses", "owners", "riders", "medications", "medication_logs",
    "feed_tasks", "vet_records", "farrier_history", "injuries", "wellness",
    "lessons", "training", "invoices", "messages", "service_requests",
    "incidents", "locations", "feed_templates", "inventory",
    "recurring_schedules", "staff_invites", "invites", "onboarding_progress",
    "events",
    # Phase 4B-7 — task engine + media (tenant_id="default" ≡ barn_id="primary"):
    "tasks", "task_templates", "task_completions", "task_events", "media",
    # Codex feature-backlog foundations — additive, non-destructive barn stamp.
    *BACKLOG_RESET_COLLECTIONS,
]


async def _backfill_barn_id(db) -> int:
    """Idempotent, additive backfill of barn_id=primary on legacy documents.

    Only touches documents missing the field, so it is safe to re-run on every
    boot (no destructive updates). Returns the total number of docs modified.
    """
    total = 0
    for coll in BARN_BACKFILL_COLLECTIONS:
        res = await db[coll].update_many(
            {"barn_id": {"$exists": False}},
            {"$set": {"barn_id": PRIMARY_BARN_ID}},
        )
        total += res.modified_count
    return total


def register_lifecycle(app, *, send_nudges):
    """Attach startup/shutdown handlers (with background loops) to ``app``.

    ``send_nudges`` is the reports router's nudge sender, injected from the
    app-assembly layer so this module avoids importing ``server.py``.
    """

    @app.on_event("startup")
    async def on_startup():
        # Phase 10B: mark process start for the readiness probe (no DB, no secrets).
        runtime_state.mark_started()
        # Optional local reset if empty, disabled by default and never allowed in
        # production so launch databases never receive starter content implicitly.
        if auto_seed_enabled() and await db.users.count_documents({}) == 0:
            try:
                await run_seed(db)
                logger.info("Initialized launch-safe starter workspace.")
            except Exception as e:
                logger.exception("Seed failed: %s", e)

        # ---------- Task Engine bootstrap ----------
        try:
            engine = TaskEngine(db, _track)
            await engine.ensure_indexes()
            await ensure_refresh_indexes(db)
            await ensure_notification_indexes(db)
            await ensure_auth_token_indexes(db)
            # Phase 5A: additive indexes for the immutable audit_log collection.
            await ensure_audit_indexes(db)
            # Phase 9B-2: partial unique index for recurring-invoice dedup.
            await ensure_billing_indexes(db)
            # Codex backlog foundations: module records, location sharing, upload
            # intents, export manifests, and integration readiness collections.
            await ensure_backlog_indexes(db)
            # Phase 10B: indexes ensured — surfaced on /api/health/ready.
            runtime_state.mark_indexes_ensured()
            # Safe migration (Phase 2C): backfill email_verified=True for any pre-existing
            # users missing the field so verification rollout never locks them out.
            backfill = await db.users.update_many(
                {"email_verified": {"$exists": False}},
                {"$set": {"email_verified": True}},
            )
            if backfill.modified_count:
                logger.info("Backfilled email_verified=True for %d existing users.", backfill.modified_count)
            # Retained compatibility hook; production no longer creates templates automatically.
            admin_user = await db.users.find_one({"role": "admin"}, {"_id": 0, "id": 1})
            admin_id = admin_user.get("id") if admin_user else None
            seed_res = await seed_starter_templates(db, admin_id)
            if not seed_res.get("skipped"):
                logger.info("Task engine: initialized %d starter templates.", seed_res.get("templates_created", 0))
            # Phase 4B-7: backfill barn_id BEFORE any materialization so the new
            # barn-scoped occurrence-dedup check sees legacy (barn_id-less) tasks
            # and never creates duplicate occurrences for the same template slot.
            try:
                barn_filled = await _backfill_barn_id(db)
                if barn_filled:
                    logger.info("Phase 4A/4B-7: backfilled barn_id=primary on %d documents.", barn_filled)
            except Exception:
                logger.exception("barn_id backfill failed")
            # Initial materialization for the 14-day horizon (post-backfill)
            created = await engine.materialize_all()
            if created:
                logger.info("Task engine: materialized %d initial occurrences.", created)
        except Exception:
            logger.exception("Task engine startup failed")

        # Phase 15.A — Stripe subscription catalog provisioning.
        # Idempotent. In PRODUCTION this validates env-provided Price IDs and
        # MUST abort startup on a miss (Codex fail-fast lock). In dev it
        # auto-creates Stripe Products and Prices tagged with
        # metadata.equinesync_managed=true, and is fail-open. Local `plans`
        # collection is always upserted (Free + Enterprise too).
        try:
            from core.billing_provisioning import ensure_stripe_catalog
            await ensure_stripe_catalog(db)
        except Exception:
            logger.exception("Stripe catalog provisioning failed (15.A)")
            # 15.A lock: PRODUCTION must fail-fast. Dev tolerates the error.
            if (os.environ.get("APP_ENV") or "development").lower() == "production":
                raise

        # Phase 15.B — unique indexes on Stripe-ID-keyed collections. Required
        # for the status-gated idempotency model in routes/subscriptions_webhook_handlers.
        try:
            await db.billing_events.create_index("stripe_event_id", unique=True)
            await db.subscription_invoices.create_index("stripe_invoice_id", unique=True)
            await db.payments.create_index("stripe_payment_intent_id", unique=True)
            await db.subscriptions.create_index("stripe_subscription_id", unique=True, sparse=True)
        except Exception:
            logger.exception("Phase 15.B index creation failed (non-fatal in dev)")
            if (os.environ.get("APP_ENV") or "development").lower() == "production":
                raise

        # Phase HorseOps-1A — indexes for the 8 new Ledger collections.
        # Index creation MAY create empty collections in Mongo as a
        # side-effect; 1-A writes ZERO documents to any of these. First
        # writes land in 1-B (profiles, equipment, providers, policy,
        # audit), 1-C (daily checks), 1-D (alerts).
        try:
            await db.horse_care_profiles.create_index("horse_id", unique=True)
            await db.horse_care_profiles.create_index("barn_id")

            await db.horse_equipment.create_index("horse_id")
            await db.horse_equipment.create_index([("barn_id", 1), ("category", 1)])

            await db.service_providers.create_index([("barn_id", 1), ("category", 1)])

            await db.horse_provider_assignments.create_index("horse_id")
            await db.horse_provider_assignments.create_index(
                [("barn_id", 1), ("next_due_date", 1)]
            )

            # Phase HorseOps-1C: 1-A used a planned `check_time` field
            # name; 1-C ships with `checked_at`. Indexes are aligned
            # here so the 1-C query shape (recent logs by horse, by
            # barn+type, by task_id) is index-backed from the first
            # write.
            #
            # Idempotent migration: existing deployments still carry
            # the legacy `check_time` indexes from the 1-A plan. Drop
            # them by name before creating the new set so we don't end
            # up with stale duplicates pointing at a non-existent
            # field. `drop_index` raises OperationFailure if the
            # index doesn't exist — we swallow that path so the
            # startup remains idempotent across cold and warm boots.
            _stale_hdcl_indexes = (
                "horse_id_1_check_time_-1",
                "barn_id_1_check_type_1_check_time_-1",
            )
            for _stale in _stale_hdcl_indexes:
                try:
                    await db.horse_daily_check_logs.drop_index(_stale)
                except Exception:
                    # Already absent (cold deploy / already migrated).
                    pass
            await db.horse_daily_check_logs.create_index(
                [("horse_id", 1), ("checked_at", -1)],
                name="hdcl_horse_checked_at",
            )
            await db.horse_daily_check_logs.create_index(
                [("barn_id", 1), ("horse_id", 1), ("checked_at", -1)],
                name="hdcl_barn_horse_checked_at",
            )
            await db.horse_daily_check_logs.create_index(
                [("barn_id", 1), ("check_type", 1), ("checked_at", -1)],
                name="hdcl_barn_check_type_checked_at",
            )
            await db.horse_daily_check_logs.create_index(
                [("task_id", 1)],
                name="hdcl_task_id",
                sparse=True,
            )

            await db.horse_ledger_alerts.create_index(
                [("horse_id", 1), ("opened_at", -1)]
            )
            await db.horse_ledger_alerts.create_index(
                [("barn_id", 1), ("severity", 1), ("closed_at", 1)]
            )
            # Phase 1-D: 1-A planned `opened_at` but 1-D ships with
            # `first_seen_at` / `last_seen_at`. Add the live shape
            # without dropping the legacy index (no existing deployment
            # has alert rows yet — 1-D is the first write).
            await db.horse_ledger_alerts.create_index(
                [("horse_id", 1), ("alert_type", 1), ("status", 1)],
                name="hla_horse_type_status",
            )
            await db.horse_ledger_alerts.create_index(
                [("barn_id", 1), ("status", 1), ("last_seen_at", -1)],
                name="hla_barn_status_last_seen",
            )
            # Phase 1-D Round-1: sort by explicit severity_rank, not
            # the lexical `severity` string.
            await db.horse_ledger_alerts.create_index(
                [("horse_id", 1), ("status", 1), ("severity_rank", -1),
                 ("last_seen_at", -1)],
                name="hla_horse_status_rank_last_seen",
            )
            await db.horse_ledger_alert_events.create_index(
                [("alert_id", 1), ("ts", 1)],
                name="hlae_alert_ts",
            )
            await db.horse_ledger_alert_events.create_index(
                [("horse_id", 1), ("ts", -1)],
                name="hlae_horse_ts",
            )
            await db.horse_ledger_alert_events.create_index(
                [("barn_id", 1), ("ts", -1)],
                name="hlae_barn_ts",
            )
            # Phase HorseOps-1E — owner service requests live alongside
            # operational rows in `service_requests`, discriminated by
            # `source="owner_care_ledger"`. This index backs the owner-
            # scoped query path AND the rate-limit count query.
            await db.service_requests.create_index(
                [("source", 1), ("barn_id", 1), ("horse_id", 1),
                 ("created_at", -1)],
                name="sr_source_barn_horse_created",
            )
            await db.service_requests.create_index(
                [("source", 1), ("owner_user_id", 1), ("horse_id", 1),
                 ("created_at", -1)],
                name="sr_owner_horse_created",
            )

            await db.horse_owner_visibility_policy.create_index(
                "horse_id", unique=True,
            )

            await db.horse_ledger_audit.create_index(
                [("horse_id", 1), ("ts", -1)]
            )
            await db.horse_ledger_audit.create_index(
                [("barn_id", 1), ("ts", -1)]
            )
            await db.horse_ledger_audit.create_index(
                [("actor_user_id", 1), ("ts", -1)]
            )
        except Exception:
            logger.exception("HorseOps-1A index creation failed (non-fatal in dev)")
            if (os.environ.get("APP_ENV") or "development").lower() == "production":
                raise

        async def _materialize_loop():
            await asyncio.sleep(60)
            engine_loop = TaskEngine(db, _track)
            while True:
                try:
                    n = await engine_loop.materialize_all()
                    if n:
                        logger.info("Task engine: rolling materialization created %d tasks.", n)
                except Exception:
                    logger.exception("Materialization loop failed")
                await asyncio.sleep(15 * 60)

        if os.environ.get("DISABLE_TASK_MATERIALIZER", "").lower() not in ("1", "true", "yes"):
            asyncio.create_task(_materialize_loop())

        # ---------- Notification dispatcher ----------
        if os.environ.get("DISABLE_NOTIFICATIONS", "").lower() not in ("1", "true", "yes"):
            mailer_handle = {"send": send_email, "render": render_email}
            asyncio.create_task(start_notification_dispatcher(db, mailer_handle))

        # ---------- Owner daily digest scheduler (Phase-C) ----------
        if os.environ.get("DISABLE_OWNER_DIGEST", "").lower() not in ("1", "true", "yes"):
            try:
                await ensure_digest_indexes(db)
            except Exception:
                logger.exception("Could not create digest indexes")

            async def _digest_loop():
                # Default delivery hour is 07:00 barn-local; we use UTC offset for simplicity.
                target_hour = int(os.environ.get("OWNER_DIGEST_HOUR_UTC", "7"))
                mailer = {"send": send_email, "render": render_email}
                await asyncio.sleep(30)  # let startup settle
                while True:
                    try:
                        now = datetime.now(timezone.utc)
                        if now.hour == target_hour:
                            res = await run_daily_digest_pass(db, mailer)
                            if res.get("sent"):
                                logger.info("Owner digest pass: sent=%d skipped=%d",
                                            res["sent"], res["skipped"])
                    except Exception:
                        logger.exception("Owner digest loop iteration failed")
                    # Sleep until top of next hour
                    now = datetime.now(timezone.utc)
                    seconds_to_next_hour = 3600 - (now.minute * 60 + now.second)
                    await asyncio.sleep(max(60, seconds_to_next_hour))

            asyncio.create_task(_digest_loop())

        # ---------- Owner weekly recap scheduler (lightweight, Sunday-evening) ----------
        if os.environ.get("DISABLE_OWNER_WEEKLY_RECAP", "").lower() not in ("1", "true", "yes"):
            async def _weekly_recap_loop():
                # Default: Sunday 18:00 UTC. Override via env if needed.
                target_dow = int(os.environ.get("OWNER_WEEKLY_RECAP_DOW", "6"))  # Mon=0 .. Sun=6
                target_hour = int(os.environ.get("OWNER_WEEKLY_RECAP_HOUR_UTC", "18"))
                mailer = {"send": send_email, "render": render_email}
                await asyncio.sleep(45)  # let startup settle (slight offset from daily digest)
                while True:
                    try:
                        now = datetime.now(timezone.utc)
                        if now.weekday() == target_dow and now.hour == target_hour:
                            res = await run_weekly_recap_pass(db, mailer, now=now)
                            if res.get("sent"):
                                logger.info("Owner weekly recap: sent=%d skipped=%d week=%s",
                                            res["sent"], res["skipped"], res["for_week"])
                    except Exception:
                        logger.exception("Owner weekly recap loop iteration failed")
                    # Sleep until top of next hour
                    now = datetime.now(timezone.utc)
                    seconds_to_next_hour = 3600 - (now.minute * 60 + now.second)
                    await asyncio.sleep(max(60, seconds_to_next_hour))

            asyncio.create_task(_weekly_recap_loop())

        # Kick off the daily nudge scheduler (24h interval, 6h warm-up after boot).
        async def _nudge_loop():
            await asyncio.sleep(6 * 3600)  # initial delay so server is warm + first nudges aren't spam
            while True:
                try:
                    result = await send_nudges(None, "EquineSync Concierge", min_days=3, cooldown_hours=24)
                    logger.info("Daily nudge run: %s", {k: v for k, v in result.items() if k != "detail"})
                    await _track("admin.nudges_run", {"trigger": "auto_daily", "sent": result.get("sent"), "candidates": result.get("candidates")}, None)
                except Exception:
                    logger.exception("Auto nudge loop failed")
                await asyncio.sleep(24 * 3600)

        if os.environ.get("DISABLE_AUTO_NUDGES", "").lower() not in ("1", "true", "yes"):
            asyncio.create_task(_nudge_loop())

        # ---------- Phase 15.D — Subscription email dispatcher ----------
        # Consumes `subscriptions.pending_emails` (populated by 15.B webhook
        # handlers via $addToSet). Runs every 15 minutes; per-row try/except
        # inside the pass keeps a single bad row from halting the loop.
        if os.environ.get("DISABLE_SUBSCRIPTION_EMAIL_DISPATCHER", "").lower() not in ("1", "true", "yes"):
            from services.subscription_email_dispatcher import run_subscription_email_pass

            async def _subscription_email_loop():
                # Slight stagger so it doesn't share boot-time with other loops.
                await asyncio.sleep(120)
                mailer = {"send": send_email, "render": render_email}
                interval_seconds = int(os.environ.get(
                    "SUBSCRIPTION_EMAIL_INTERVAL_SECONDS", "900"))  # 15 minutes
                while True:
                    try:
                        stats = await run_subscription_email_pass(db, mailer)
                        if any(stats.get(k) for k in ("sent", "failed", "permanent_failures", "unknown_pulled")):
                            logger.info("Subscription email pass: %s", stats)
                    except Exception:
                        logger.exception("Subscription email loop iteration failed")
                    await asyncio.sleep(max(60, interval_seconds))

            asyncio.create_task(_subscription_email_loop())

        # Phase 10B: structured startup-complete log — booleans/strings only,
        # no secrets/URLs/keys. Mirrors the /api/health/ready posture.
        def _enabled(flag: str) -> bool:
            return os.environ.get(flag, "").lower() not in ("1", "true", "yes")

        db_ok = True
        try:
            await db.command("ping")
        except Exception:
            db_ok = False
        snap = runtime_state.snapshot()
        logger.info(
            "startup complete: env=%s db_ok=%s indexes_ensured=%s "
            "task_materializer=%s notifications=%s owner_digest=%s "
            "weekly_recap=%s auto_nudges=%s subscription_emails=%s",
            "production" if os.environ.get("APP_ENV", "").lower() == "production" else "development",
            db_ok,
            snap["indexes_ensured"],
            _enabled("DISABLE_TASK_MATERIALIZER"),
            _enabled("DISABLE_NOTIFICATIONS"),
            _enabled("DISABLE_OWNER_DIGEST"),
            _enabled("DISABLE_OWNER_WEEKLY_RECAP"),
            _enabled("DISABLE_AUTO_NUDGES"),
            _enabled("DISABLE_SUBSCRIPTION_EMAIL_DISPATCHER"),
        )

    @app.on_event("shutdown")
    async def shutdown_db_client():
        logger.info("shutting down: closing database client")
        client.close()
