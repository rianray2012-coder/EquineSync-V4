from __future__ import annotations

import argparse
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

import bcrypt
from dotenv import load_dotenv
from pymongo import MongoClient


ROOT = Path(__file__).resolve().parents[2]

DEMO_PASSWORD = "demo1234"
DEMO_USERS = [
    ("admin@equinesync.com", "Demo Admin", "admin"),
    ("owner@equinesync.com", "Demo Owner", "horse_owner"),
    ("trainer@equinesync.com", "Demo Trainer", "trainer"),
    ("groom@equinesync.com", "Demo Groom", "groom"),
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
        for email, _name, role in DEMO_USERS:
            exists = db.users.find_one({"email": email}, {"_id": 0, "id": 1, "role": 1})
            action = "update" if exists else "insert"
            print(f"{action}: {email} role={role}")
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

    for email, full_name, role in DEMO_USERS:
        existing = db.users.find_one({"email": email}, {"_id": 0, "id": 1})
        user_id = (existing or {}).get("id") or f"local_demo_{uuid.uuid4().hex[:12]}"
        doc = {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "role": role,
            "barn_id": "primary",
            "password_hash": _hash_pwd(DEMO_PASSWORD),
            "email_verified": True,
            "account_status": "active",
            "local_demo_seed": True,
            "updated_at": now,
        }
        db.users.update_one(
            {"email": email},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True,
        )
        db.account_memberships.update_one(
            {"user_id": user_id, "barn_id": "primary"},
            {
                "$set": {
                    "user_id": user_id,
                    "barn_id": "primary",
                    "role": role,
                    "status": "active",
                    "updated_at": now,
                },
                "$setOnInsert": {"id": f"membership_{uuid.uuid4().hex[:12]}", "created_at": now},
            },
            upsert=True,
        )
        print(f"seeded: {email} role={role}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
