from __future__ import annotations

import argparse
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import bcrypt
from dotenv import load_dotenv
from pymongo import MongoClient


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from core.account_context import standalone_owner_membership_from_user  # noqa: E402
from core.account_memberships import (  # noqa: E402
    MEMBERSHIP_COLLECTION,
    compatibility_membership_from_user,
)

DEMO_PASSWORD = "demo1234"
DEMO_USERS = [
    ("platform-admin@equinesync.com", "Demo Platform Admin", "admin", "platform_admin", "primary"),
    ("admin@equinesync.com", "Demo Facility Admin", "admin", None, "primary"),
    ("barn-owner@equinesync.com", "Demo Barn Owner", "barn_owner", None, "primary"),
    ("manager@equinesync.com", "Demo Barn Manager", "barn_manager", None, "primary"),
    ("owner@equinesync.com", "Demo Owner", "horse_owner", None, "primary"),
    ("individual-owner@equinesync.com", "Demo Individual Owner", "horse_owner", None, None),
    ("trainer@equinesync.com", "Demo Trainer", "trainer", None, "primary"),
    ("groom@equinesync.com", "Demo Groom", "groom", None, "primary"),
    ("working-student@equinesync.com", "Demo Working Student", "working_student", None, "primary"),
    ("guardian@equinesync.com", "Demo Guardian", "parent", None, "primary"),
    ("rider@equinesync.com", "Demo Rider", "rider", None, "primary"),
    ("service-provider@equinesync.com", "Demo Service Provider", "service_provider", None, "primary"),
    ("vet@equinesync.com", "Demo Veterinarian", "veterinarian", None, "primary"),
    ("farrier@equinesync.com", "Demo Farrier", "farrier", None, "primary"),
]


def _hash_pwd(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_production() -> bool:
    return (os.environ.get("APP_ENV") or "development").strip().lower() in {"production", "prod"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed local demo test users for backend integration tests.")
    parser.add_argument("--allow-non-test-db", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(ROOT / "backend" / ".env")
    if _is_production():
        raise SystemExit("Refusing to seed local demo test accounts in production.")

    db_name = os.environ.get("DB_NAME") or ""
    if not args.allow_non_test_db and db_name not in {"test_database", "equinesync_test", "local_test"}:
        raise SystemExit(f"Refusing DB_NAME={db_name!r}; pass --allow-non-test-db for intentional local use.")

    mongo_url = os.environ["MONGO_URL"]
    client = MongoClient(mongo_url)
    db = client[db_name]
    now = _now()

    if args.dry_run:
        for email, _name, role, platform_role, barn_id in DEMO_USERS:
            exists = db.users.find_one({"email": email}, {"_id": 0, "id": 1, "role": 1})
            action = "update" if exists else "insert"
            suffix = f" platform_role={platform_role}" if platform_role else ""
            barn_suffix = f" barn_id={barn_id}" if barn_id else " standalone"
            print(f"{action}: {email} role={role}{suffix}{barn_suffix}")
        return 0

    db.barn.update_one(
        {"id": "primary"},
        {"$set": {"id": "primary", "name": "Local Demo Barn", "updated_at": now}, "$setOnInsert": {"created_at": now}},
        upsert=True,
    )
    db.barns.update_one(
        {"id": "primary"},
        {"$set": {"id": "primary", "name": "Local Demo Barn", "status": "active", "updated_at": now}, "$setOnInsert": {"created_at": now}},
        upsert=True,
    )

    seeded_users = []
    for email, full_name, role, platform_role, barn_id in DEMO_USERS:
        existing = db.users.find_one({"email": email}, {"_id": 0, "id": 1})
        user_id = (existing or {}).get("id") or f"local_demo_{uuid.uuid4().hex[:12]}"
        doc = {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "role": role,
            "barn_id": barn_id,
            "password_hash": _hash_pwd(DEMO_PASSWORD),
            "email_verified": True,
            "account_status": "active",
            "role_status": "active",
            "role_intake_completed": True,
            "intake_completed": True,
            "profile_completed": True,
            "facility_setup_complete": True,
            "onboarding_completed": True,
            "platform_role": platform_role,
            "local_demo_seed": True,
            "updated_at": now,
        }
        if platform_role:
            doc["platform_role_updated_at"] = now
        db.users.update_one(
            {"email": email},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True,
        )
        if role == "horse_owner" and not barn_id:
            membership = standalone_owner_membership_from_user(doc)
            membership["updated_at"] = now
        else:
            membership = compatibility_membership_from_user(doc, generated_at=now)
        membership["local_demo_seed"] = True
        db[MEMBERSHIP_COLLECTION].update_one(
            {"id": membership["id"]},
            {
                "$set": membership,
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )
        seeded_users.append({"id": user_id, "email": email, "role": role, "barn_id": barn_id})
        print(f"seeded: {email} role={role}")

    _seed_facility_readiness(db, now, seeded_users)
    _seed_service_provider_demo_context(db, now)
    return 0


def _seed_facility_readiness(db, now: str, seeded_users) -> None:
    db.locations.update_one(
        {"id": "local_demo_main_barn"},
        {
            "$set": {
                "id": "local_demo_main_barn",
                "barn_id": "primary",
                "name": "Main Barn",
                "type": "barn",
                "status": "active",
                "updated_at": now,
                "local_demo_seed": True,
            },
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )
    db.owners.update_one(
        {"id": "local_demo_owner_record"},
        {
            "$set": {
                "id": "local_demo_owner_record",
                "barn_id": "primary",
                "full_name": "Demo Owner",
                "email": "owner@equinesync.com",
                "status": "active",
                "updated_at": now,
                "local_demo_seed": True,
            },
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )
    db.feed_templates.update_one(
        {"id": "local_demo_feed_template"},
        {
            "$set": {
                "id": "local_demo_feed_template",
                "barn_id": "primary",
                "meal": "AM",
                "name": "Morning Performance Feed",
                "description": "Local pilot feed template for setup-readiness preflight.",
                "updated_at": now,
                "local_demo_seed": True,
            },
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )

    complete_steps = {
        "barn": "complete",
        "locations": "complete",
        "owners": "complete",
        "horses": "complete",
        "feed_templates": "complete",
        "review": "complete",
    }
    for user in seeded_users:
        if user["role"] not in {"admin", "barn_owner"} or user.get("barn_id") != "primary":
            continue
        db.onboarding_progress.update_one(
            {"user_id": user["id"]},
            {
                "$set": {
                    "user_id": user["id"],
                    "barn_id": "primary",
                    "completed": True,
                    "steps": complete_steps,
                    "updated_at": now,
                    "local_demo_seed": True,
                },
                "$setOnInsert": {"id": f"onboarding_{uuid.uuid4().hex[:12]}", "created_at": now},
            },
            upsert=True,
        )


def _seed_service_provider_demo_context(db, now: str) -> None:
    horse_id = "local_demo_provider_horse"
    db.horses.update_one(
        {"id": horse_id},
        {
            "$set": {
                "id": horse_id,
                "barn_id": "primary",
                "name": "Valencia",
                "breed": "Warmblood",
                "discipline": "Hunter",
                "status": "active",
                "allergies": ["penicillin"],
                "updated_at": now,
                "local_demo_seed": True,
            },
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )

    provider_specs = [
        ("service-provider@equinesync.com", "body_worker", "Care Partner"),
        ("vet@equinesync.com", "vet", "Veterinarian"),
        ("farrier@equinesync.com", "farrier", "Farrier"),
    ]
    for email, category, name in provider_specs:
        user = db.users.find_one({"email": email}, {"_id": 0, "id": 1, "role": 1})
        if not user:
            continue
        provider_id = f"local_demo_provider_{category}"
        db.service_providers.update_one(
            {"id": provider_id},
            {
                "$set": {
                    "id": provider_id,
                    "barn_id": "primary",
                    "category": category,
                    "name": name,
                    "email": email,
                    "provider_user_id": user["id"],
                    "status": "active",
                    "updated_at": now,
                    "local_demo_seed": True,
                },
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )
        db.horse_provider_assignments.update_one(
            {"id": f"local_demo_grant_{category}"},
            {
                "$set": {
                    "id": f"local_demo_grant_{category}",
                    "barn_id": "primary",
                    "horse_id": horse_id,
                    "provider_id": provider_id,
                    "provider_user_id": user["id"],
                    "category": category,
                    "status": "active",
                    "last_service_date": "2026-07-01",
                    "next_due_date": "2026-08-01",
                    "interval_days": 30,
                    "is_primary_for_horse": category in {"vet", "farrier"},
                    "updated_at": now,
                    "local_demo_seed": True,
                },
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )

    db.vet_records.update_one(
        {"id": "local_demo_vet_record"},
        {
            "$set": {
                "id": "local_demo_vet_record",
                "barn_id": "primary",
                "horse_id": horse_id,
                "type": "wellness",
                "title": "Wellness check",
                "date": "2026-07-01",
                "vet_name": "Veterinarian",
                "follow_up_due": "2026-08-01",
                "updated_at": now,
                "local_demo_seed": True,
            },
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )
    db.farrier_history.update_one(
        {"id": "local_demo_farrier_record"},
        {
            "$set": {
                "id": "local_demo_farrier_record",
                "barn_id": "primary",
                "horse_id": horse_id,
                "date": "2026-07-01",
                "farrier_name": "Farrier",
                "next_visit_due": "2026-08-12",
                "shoes_on": ["front"],
                "updated_at": now,
                "local_demo_seed": True,
            },
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )
    db.provider_visit_notes.update_one(
        {"id": "local_demo_provider_note"},
        {
            "$set": {
                "id": "local_demo_provider_note",
                "barn_id": "primary",
                "horse_id": horse_id,
                "provider_name": "Care Partner",
                "category": "body_worker",
                "title": "Bodywork visit",
                "visit_date": "2026-07-01",
                "follow_up_due": "2026-08-01",
                "updated_at": now,
                "local_demo_seed": True,
            },
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )


if __name__ == "__main__":
    raise SystemExit(main())
