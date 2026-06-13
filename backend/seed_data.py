"""Launch-safe starter reset.

This module intentionally does not create starter users, horses, invoices, medical
records, schedules, or other customer-visible records. The guarded `/api/seed`
route uses this only when explicitly enabled outside production, and the result
is an empty workspace that sends users through onboarding.
"""
from __future__ import annotations

from datetime import datetime, timezone

from routes.backlog import BACKLOG_RESET_COLLECTIONS


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def run_seed(db):
    """Clear launch-workspace collections and create only a blank starter barn."""
    reset_collections = [
        "horses", "owners", "riders", "medications", "medication_logs",
        "feed_tasks", "vet_records", "farrier_history", "injuries", "wellness",
        "lessons", "training", "invoices", "messages", "service_requests",
        "incidents", "locations", "feed_templates", "inventory",
        "recurring_schedules", "staff_invites", "invites", "onboarding_progress",
        "events", "tasks", "task_templates", "task_completions", "task_events",
        "media", "owner_updates", "audit_log", *BACKLOG_RESET_COLLECTIONS,
    ]
    for collection in reset_collections:
        await db[collection].delete_many({})

    await db.barn.update_one(
        {"id": "primary"},
        {"$set": {
            "id": "primary",
            "name": "",
            "facility_type": "boarding",
            "disciplines": [],
            "address": "",
            "timezone": "America/New_York",
            "contact_email": "",
            "contact_phone": "",
            "logo_url": "",
            "banner_url": "",
            "created_at": _iso_now(),
            "updated_at": _iso_now(),
        }},
        upsert=True,
    )
    return {"ok": True, "starter_workspace": True, "records_created": 0}
