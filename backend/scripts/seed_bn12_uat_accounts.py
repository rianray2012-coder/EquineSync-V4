"""Seed BN12 UAT role accounts.

Creates a production-safe, idempotent set of role accounts for final UAT.
Passwords are minted and printed once for newly-created users unless an
environment variable supplies the password. Existing users are not re-hashed
unless --reset-passwords is explicitly passed.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import re
import secrets
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import bcrypt
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from core.account_memberships import (  # noqa: E402
    MEMBERSHIP_COLLECTION,
    compatibility_membership_from_user,
)
from core.account_context import standalone_owner_membership_from_user  # noqa: E402


SEED_KEY = "bn12_uat_accounts"
SEED_PHASE = "build_next_12a"
UAT_BARN_ID = "bn12_uat_facility"
UAT_BARN_NAME = "BN12 UAT Facility"

UAT_ROSTER: List[Dict[str, Optional[str]]] = [
    {
        "uat_id": "UAT-R1",
        "email": "uat.platform@equine-sync.com",
        "full_name": "UAT Platform Admin",
        "role": "admin",
        "platform_role": "platform_admin",
        "barn_id": UAT_BARN_ID,
        "description": "Platform admin",
    },
    {
        "uat_id": "UAT-R2",
        "email": "uat.facility-admin@equine-sync.com",
        "full_name": "UAT Facility Admin",
        "role": "admin",
        "platform_role": None,
        "barn_id": UAT_BARN_ID,
        "description": "Facility admin / barn owner",
    },
    {
        "uat_id": "UAT-R3",
        "email": "uat.manager@equine-sync.com",
        "full_name": "UAT Barn Manager",
        "role": "barn_manager",
        "platform_role": None,
        "barn_id": UAT_BARN_ID,
        "description": "Barn manager",
    },
    {
        "uat_id": "UAT-R4",
        "email": "uat.staff@equine-sync.com",
        "full_name": "UAT Staff",
        "role": "groom",
        "platform_role": None,
        "barn_id": UAT_BARN_ID,
        "description": "Staff",
    },
    {
        "uat_id": "UAT-R5",
        "email": "uat.owner@equine-sync.com",
        "full_name": "UAT Horse Owner",
        "role": "horse_owner",
        "platform_role": None,
        "barn_id": UAT_BARN_ID,
        "description": "Horse owner",
    },
    {
        "uat_id": "UAT-R6",
        "email": "uat.guardian@equine-sync.com",
        "full_name": "UAT Guardian Parent",
        "role": "parent",
        "platform_role": None,
        "barn_id": UAT_BARN_ID,
        "description": "Guardian / parent",
    },
    {
        "uat_id": "UAT-R7",
        "email": "uat.participant@equine-sync.com",
        "full_name": "UAT Lesson Participant",
        "role": "rider",
        "platform_role": None,
        "barn_id": UAT_BARN_ID,
        "description": "Lesson participant",
    },
    {
        "uat_id": "UAT-R8",
        "email": "uat.individual-owner@equine-sync.com",
        "full_name": "UAT Individual Owner",
        "role": "horse_owner",
        "platform_role": None,
        "barn_id": None,
        "description": "Standalone individual owner",
    },
]


def _slug(email: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", email).strip("_").upper()


def _is_prod() -> bool:
    return (os.environ.get("APP_ENV") or "").strip().lower() in ("production", "prod")


def _hash_pwd(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _mint_password() -> str:
    return secrets.token_urlsafe(24)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _tag() -> Dict[str, object]:
    return {
        "uat_seed": True,
        "uat_seed_key": SEED_KEY,
        "created_by_seed": SEED_PHASE,
    }


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Seed BN12 role accounts for final UAT."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Preview only. Reads the database, writes nothing, and mints/prints "
            "no passwords."
        ),
    )
    parser.add_argument(
        "--allow-prod",
        action="store_true",
        help="Required for writes when APP_ENV is production.",
    )
    parser.add_argument(
        "--reset-passwords",
        action="store_true",
        help=(
            "Explicitly rotate passwords for existing BN12 UAT users. New "
            "one-time passwords are printed once."
        ),
    )
    return parser.parse_args()


async def _ensure_barn(db, *, dry_run: bool) -> str:
    existing = await db.barns.find_one({"id": UAT_BARN_ID}, {"_id": 0})
    if existing:
        return "already_present"
    doc = {
        "id": UAT_BARN_ID,
        "name": UAT_BARN_NAME,
        "status": "active",
        "subscription_tier_code": "advanced_barn",
        "contact_email": "uat.facility-admin@equine-sync.com",
        "timezone": "America/Chicago",
        "created_at": _now(),
        **_tag(),
    }
    if not dry_run:
        await db.barns.insert_one(doc)
    return "would_create" if dry_run else "created"


async def _upsert_membership(db, user_doc: Dict[str, object], *, dry_run: bool) -> str:
    if user_doc.get("role") == "horse_owner" and not user_doc.get("barn_id"):
        membership = standalone_owner_membership_from_user(user_doc)
    else:
        membership = compatibility_membership_from_user(user_doc)
    membership.update(_tag())
    membership["updated_at"] = _now()
    if dry_run:
        return "would_upsert"
    await db[MEMBERSHIP_COLLECTION].update_one(
        {"id": membership["id"]},
        {"$set": membership, "$setOnInsert": {"created_at": _now()}},
        upsert=True,
    )
    return "upserted"


async def _ensure_user(
    db,
    spec: Dict[str, Optional[str]],
    *,
    dry_run: bool,
    reset_passwords: bool,
) -> Dict[str, object]:
    email = str(spec["email"]).lower()
    env_key = f"SEED_BN12_{_slug(email)}_PASSWORD"
    env_password = os.environ.get(env_key)
    existing = await db.users.find_one({"email": email}, {"password_hash": 0})
    minted_password: Optional[str] = None
    password_source = "n/a (existing user)"
    password_action = "not_changed"

    if existing:
        user_id = existing["id"]
        action = "already_present"
        updates = {
            "full_name": spec["full_name"],
            "role": spec["role"],
            "role_status": "active",
            "account_status": "active",
            "email_verified": True,
            "uat_id": spec["uat_id"],
            **_tag(),
        }
        if spec.get("barn_id"):
            updates["barn_id"] = spec["barn_id"]
        else:
            updates["barn_id"] = None
        if spec.get("platform_role"):
            updates["platform_role"] = spec["platform_role"]
            updates["platform_role_updated_at"] = _now()
        else:
            updates["platform_role"] = None

        if reset_passwords:
            password = env_password or _mint_password()
            if env_password:
                password_source = "env"
            else:
                password_source = "mint"
                minted_password = password
            updates["password_hash"] = _hash_pwd(password)
            password_action = "would_reset" if dry_run else "reset"
        if not dry_run:
            await db.users.update_one({"id": user_id}, {"$set": updates})
        user_doc = {**existing, **updates, "id": user_id, "email": email}
    else:
        if dry_run:
            password_hash = "(dry-run)"
            password_source = "env" if env_password else "would_mint_on_apply"
            password_action = "would_set"
        else:
            password = env_password or _mint_password()
            if env_password:
                password_source = "env"
            else:
                password_source = "mint"
                minted_password = password
            password_hash = _hash_pwd(password)
            password_action = "set"
        user_id = str(uuid.uuid4())
        action = "would_create" if dry_run else "created"
        user_doc = {
            "id": user_id,
            "email": email,
            "full_name": spec["full_name"],
            "role": spec["role"],
            "role_status": "active",
            "account_status": "active",
            "barn_id": spec.get("barn_id"),
            "platform_role": spec.get("platform_role"),
            "password_hash": password_hash,
            "email_verified": True,
            "signup_source": SEED_PHASE,
            "uat_id": spec["uat_id"],
            "created_at": _now(),
            **_tag(),
        }
        if spec.get("platform_role"):
            user_doc["platform_role_updated_at"] = _now()
        if not dry_run:
            await db.users.insert_one(user_doc)

    membership_action = await _upsert_membership(db, user_doc, dry_run=dry_run)

    if not dry_run:
        await db.audit_log.insert_one({
            "id": str(uuid.uuid4()),
            "ts": _now(),
            "action": "bn12.uat_account.seeded",
            "actor_email": "(cli)",
            "actor_role": "(cli)",
            "resource_type": "user",
            "resource_id": user_id,
            "outcome": "success",
            "status_code": 200,
            "metadata": {
                "uat_id": spec["uat_id"],
                "target_email": email,
                "role": spec["role"],
                "platform_role": spec.get("platform_role"),
                "barn_id_present": bool(spec.get("barn_id")),
                "password_source": password_source,
                "password_action": password_action,
                "seed_phase": SEED_PHASE,
            },
        })

    return {
        "uat_id": spec["uat_id"],
        "email": email,
        "description": spec["description"],
        "role": spec["role"],
        "platform_role": spec.get("platform_role"),
        "barn_id": spec.get("barn_id"),
        "action": action,
        "membership_action": membership_action,
        "password_source": password_source,
        "password_action": password_action,
        "minted_password": minted_password,
        "env_var": env_key,
    }


async def _main():
    args = _parse_args()
    if _is_prod() and not args.allow_prod and not args.dry_run:
        print(
            "ERROR: APP_ENV is production. Pass --allow-prod to write, or "
            "--dry-run to preview.",
            file=sys.stderr,
        )
        sys.exit(2)

    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    print("=" * 72)
    print(f"BN12A — seeding UAT role accounts{' (DRY-RUN)' if args.dry_run else ''}")
    print(f"APP_ENV={os.environ.get('APP_ENV') or 'development'}")
    if args.reset_passwords:
        print("reset_passwords=ON")
    print("=" * 72)

    barn_action = await _ensure_barn(db, dry_run=args.dry_run)
    print(f"  barn {barn_action:18} id={UAT_BARN_ID}")

    results = [
        await _ensure_user(
            db, spec, dry_run=args.dry_run, reset_passwords=args.reset_passwords
        )
        for spec in UAT_ROSTER
    ]
    for item in results:
        print(
            f"  {item['uat_id']:6} {item['action']:18} "
            f"{item['email']:38} role={item['role']} "
            f"membership={item['membership_action']}"
        )

    if args.dry_run:
        would_mint = [
            r for r in results
            if r["password_source"] == "would_mint_on_apply"
        ]
        if would_mint:
            print()
            print("DRY-RUN: no passwords minted, none printed.")
            for item in would_mint:
                print(f"  {item['uat_id']} {item['email']} (would mint on apply)")
    else:
        minted = [r for r in results if r.get("minted_password")]
        if minted:
            print()
            print("=" * 72)
            print("BN12A ONE-TIME PASSWORDS — copy now; they will not be shown again.")
            print("They are not written to logs, audit_log, or any file.")
            print("=" * 72)
            for item in minted:
                print(f"  {item['uat_id']:6} {item['email']:38} {item['minted_password']}")

    print()
    print("Done. BN12 UAT account readiness seed complete.")


if __name__ == "__main__":
    asyncio.run(_main())
