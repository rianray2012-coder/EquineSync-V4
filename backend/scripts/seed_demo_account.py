"""scripts/seed_demo_account.py — Phase Admin-8 Part C.

Idempotent CLI to seed (or tear down) the Equine Sync demo client
account. The demo logs in through the SAME `/login` flow as a real
client, uses normal app routes, and is bound by normal permissions
(no `platform_role`, no admin portal access).

Every record carries:
    demo_seed:     True
    demo_seed_key: "admin8_client_demo"
    created_by_seed: "phase_admin_8"

…so teardown is surgical and metrics/exclusion logic can find them.

Password (founder decision 2b):
    Always mint-and-print a one-time password unless
    `SEED_DEMO_CLIENT_PASSWORD` is set. Never logged.

Usage:
    cd /app/backend
    python -m scripts.seed_demo_account              # seed
    python -m scripts.seed_demo_account --dry-run    # show plan
    python -m scripts.seed_demo_account --teardown   # remove demo records
    python -m scripts.seed_demo_account --allow-prod # required in prod
"""
from __future__ import annotations

import argparse
import asyncio
import os
import secrets
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

import bcrypt
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from core.account_memberships import compatibility_membership_from_user


DEMO_KEY = "admin8_client_demo"
DEMO_PHASE = "phase_admin_8"

DEMO_EMAIL = "demo.client@equine-sync.com"
DEMO_NAME = "Pilot Client"
EXTRA_OWNER_EMAIL = "demo.owner2@equine-sync.com"
EXTRA_OWNER_NAME = "Secondary Owner"
DEMO_BARN_NAME = "EquineSync Pilot Stable"
DEMO_HORSES = [
    {"name": "Aurelia",  "breed": "Andalusian", "age": 9,  "discipline": "Dressage"},
    {"name": "Beacon",   "breed": "Thoroughbred", "age": 6, "discipline": "Eventing"},
    {"name": "Cinder",   "breed": "Quarter Horse", "age": 14, "discipline": "Western"},
]


def _hash_pwd(p: str) -> str:
    return bcrypt.hashpw(p.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _mint_password() -> str:
    return secrets.token_urlsafe(24)


def _is_prod() -> bool:
    return (os.environ.get("APP_ENV") or "").strip().lower() in ("production", "prod")


def _tag() -> Dict[str, object]:
    """Standard demo-tag dict applied to every record we create."""
    return {
        "demo_seed": True,
        "demo_seed_key": DEMO_KEY,
        "created_by_seed": DEMO_PHASE,
    }


def _parse_args():
    p = argparse.ArgumentParser(description=(
        "Seed (or tear down) the Phase Admin-8 client-like demo account."
    ))
    p.add_argument("--dry-run", action="store_true",
                   help="Print the plan; does NOT write to the database "
                        "(reads are still performed to build the preview). "
                        "No password is minted or printed in dry-run.")
    p.add_argument("--allow-prod", action="store_true",
                   help="Required to run when APP_ENV is production.")
    p.add_argument("--teardown", action="store_true",
                   help=f"Remove every record tagged demo_seed_key='{DEMO_KEY}'.")
    p.add_argument("--extra-owner", action="store_true",
                   help="Also seed a second demo horse-owner user "
                        f"({EXTRA_OWNER_EMAIL}) linked to one demo horse.")
    p.add_argument("--reset-extra-owner-password", action="store_true",
                   help="When used with --extra-owner and "
                        "SEED_DEMO_EXTRA_OWNER_PASSWORD, update the second "
                        "demo owner's password hash. Does not affect the "
                        "original demo client account.")
    return p.parse_args()


# ----------------------------------------------------------------------
# SEED
# ----------------------------------------------------------------------
async def _upsert_demo_membership(db, user_doc: Dict[str, object],
                                  *, generated_at: str, dry_run: bool) -> str:
    """Mirror a demo user into account_memberships immediately.

    Startup also backfills this collection, but the seed script should leave
    production/staging ready for a login right away without waiting for a
    service restart. The row is demo-tagged so teardown remains surgical.
    """
    membership = compatibility_membership_from_user(
        user_doc, generated_at=generated_at,
    )
    membership.update(_tag())
    if not dry_run:
        await db.account_memberships.update_one(
            {"compatibility_key": membership["compatibility_key"]},
            {
                "$set": membership,
                "$setOnInsert": {"created_at": generated_at},
            },
            upsert=True,
        )
    return membership["id"]


async def _ensure_extra_owner(db, *, barn_id: str, now_iso: str,
                              dry_run: bool, reset_password: bool) -> Dict[str, object]:
    env_password = os.environ.get("SEED_DEMO_EXTRA_OWNER_PASSWORD")
    if not env_password and not dry_run:
        raise RuntimeError(
            "SEED_DEMO_EXTRA_OWNER_PASSWORD is required when --extra-owner "
            "creates or resets the second demo owner."
        )

    existing = await db.users.find_one(
        {"email": EXTRA_OWNER_EMAIL}, {"password_hash": 0},
    )
    password_source = "env" if env_password else "env_required_on_apply"
    password_action = "not_applicable"

    if existing:
        user_id = existing["id"]
        user_action = "already_present"
        existing_updates = {
            "full_name": EXTRA_OWNER_NAME,
            "barn_id": existing.get("barn_id") or barn_id,
            "role": existing.get("role") or "horse_owner",
            "role_status": existing.get("role_status") or "active",
            "account_status": existing.get("account_status") or "active",
            "updated_at": now_iso,
            **_tag(),
        }
        user_doc = {
            **existing,
            **existing_updates,
        }
        if not dry_run:
            await db.users.update_one({"id": user_id}, {"$set": existing_updates})
        if reset_password:
            password_action = "would_reset" if dry_run else "reset"
            if not dry_run:
                await db.users.update_one(
                    {"id": user_id},
                    {"$set": {
                        "password_hash": _hash_pwd(env_password),
                        "updated_at": now_iso,
                        "barn_id": barn_id,
                        "role": "horse_owner",
                        "role_status": "active",
                        "account_status": "active",
                        "email_verified": True,
                        "full_name": EXTRA_OWNER_NAME,
                        **_tag(),
                    }},
                )
                user_doc.update({
                    "barn_id": barn_id,
                    "role": "horse_owner",
                    "role_status": "active",
                    "account_status": "active",
                    "email_verified": True,
                    "full_name": EXTRA_OWNER_NAME,
                    **_tag(),
                })
        else:
            password_source = "n/a (existing user)"
    else:
        user_id = str(uuid.uuid4())
        user_action = "created"
        password_action = "would_set" if dry_run else "set"
        user_doc = {
            "id": user_id,
            "email": EXTRA_OWNER_EMAIL,
            "full_name": EXTRA_OWNER_NAME,
            "role": "horse_owner",
            "role_status": "active",
            "account_status": "active",
            "barn_id": barn_id,
            "password_hash": "(dry-run)" if dry_run else _hash_pwd(env_password),
            "email_verified": True,
            "signup_source": "phase_admin_8_extra_owner",
            "membership_tier": "demo",
            "subscription_status": "active",
            "created_at": now_iso,
            **_tag(),
        }
        if not dry_run:
            await db.users.insert_one(user_doc)

    membership_id = await _upsert_demo_membership(
        db, user_doc, generated_at=now_iso, dry_run=dry_run,
    )

    horse_name = "Beacon"
    horse = await db.horses.find_one({
        "barn_id": barn_id,
        "name": horse_name,
        "demo_seed_key": DEMO_KEY,
    }, {"_id": 0, "id": 1})
    horse_link_action = "missing_demo_horse"
    if horse:
        horse_link_action = "would_link" if dry_run else "linked"
        if not dry_run:
            await db.horses.update_one(
                {"id": horse["id"]},
                {
                    "$addToSet": {"secondary_owner_ids": user_id},
                    "$set": {"updated_at": now_iso},
                },
            )

    if not dry_run:
        await db.audit_log.insert_one({
            "id": str(uuid.uuid4()),
            "ts": now_iso,
            "action": "admin.seed.demo_extra_owner_created",
            "actor_email": "(cli)",
            "actor_role": "(cli)",
            "resource_type": "user",
            "resource_id": user_id,
            "outcome": "success",
            "status_code": 200,
            "metadata": {
                "demo_seed_key": DEMO_KEY,
                "seed_phase": "phase_admin_8_extra_owner",
                "target_email": EXTRA_OWNER_EMAIL,
                "user_action": user_action,
                "password_source": password_source,
                "password_action": password_action,
                "membership_id": membership_id,
                "horse_link_action": horse_link_action,
                "linked_horse_name": horse_name if horse else None,
            },
        })

    return {
        "email": EXTRA_OWNER_EMAIL,
        "user_id": user_id,
        "user_action": user_action,
        "password_source": password_source,
        "password_action": password_action,
        "membership_id": membership_id,
        "horse_link_action": horse_link_action,
    }


async def _seed(db, *, dry_run: bool, extra_owner: bool = False,
                reset_extra_owner_password: bool = False) -> Dict[str, object]:
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # 1. Barn / facility.
    existing_barn = await db.barns.find_one({"demo_seed_key": DEMO_KEY})
    if existing_barn:
        barn_id = existing_barn["id"]
        if existing_barn.get("name") != DEMO_BARN_NAME:
            barn_action = "would_update_name" if dry_run else "updated_name"
            if not dry_run:
                await db.barns.update_one(
                    {"id": barn_id},
                    {"$set": {"name": DEMO_BARN_NAME, "updated_at": now_iso}},
                )
        else:
            barn_action = "already_present"
    else:
        barn_id = f"barn_demo_{uuid.uuid4().hex[:10]}"
        barn_doc = {
            "id": barn_id,
            "name": DEMO_BARN_NAME,
            "status": "active",
            "subscription_tier_code": "demo",
            "subscription_id": None,    # NEVER a Stripe ID
            "address": "1 Demo Lane, Lexington, KY",
            "phone": "+1-555-0100",
            "contact_email": DEMO_EMAIL,
            "timezone": "America/New_York",
            "created_at": now_iso,
            **_tag(),
        }
        if not dry_run:
            await db.barns.insert_one(barn_doc)
        barn_action = "created"

    # 2. Demo user (horse_owner). Mint password unless env override.
    env_password = os.environ.get("SEED_DEMO_CLIENT_PASSWORD")
    minted_password: Optional[str] = None
    existing_user = await db.users.find_one(
        {"email": DEMO_EMAIL}, {"password_hash": 0},
    )
    if existing_user:
        user_id = existing_user["id"]
        user_action = "already_present"
        password_source = "n/a (existing user)"
        existing_user_updates = {
            "full_name": DEMO_NAME,
            "barn_id": existing_user.get("barn_id") or barn_id,
            "role": existing_user.get("role") or "horse_owner",
            "role_status": existing_user.get("role_status") or "active",
            "account_status": existing_user.get("account_status") or "active",
            "updated_at": now_iso,
            **_tag(),
        }
        primary_user_doc = {
            **existing_user,
            **existing_user_updates,
        }
        if not dry_run:
            await db.users.update_one({"id": user_id}, {"$set": existing_user_updates})
    else:
        # Codex round-2 P1 fix: do NOT mint a password in dry-run.
        # The hash would never persist, so any printed value would
        # mislead an operator into thinking they have a usable
        # credential.
        if dry_run:
            password = "(dry-run: would mint on apply)"
            password_hash_for_doc = "(dry-run)"
            password_source = "env" if env_password else "would_mint_on_apply"
        else:
            password = env_password or _mint_password()
            if not env_password:
                minted_password = password
            password_source = "env" if env_password else "mint"
            password_hash_for_doc = _hash_pwd(password)
        user_id = str(uuid.uuid4())
        user_doc = {
            "id": user_id,
            "email": DEMO_EMAIL,
            "full_name": DEMO_NAME,
            "role": "horse_owner",
            "role_status": "active",
            "account_status": "active",
            # IMPORTANT: NO platform_role — demo cannot enter Admin Portal.
            "barn_id": barn_id,
            "password_hash": password_hash_for_doc,
            "email_verified": True,
            "signup_source": DEMO_PHASE,
            "membership_tier": "demo",
            "subscription_status": "active",
            "created_at": now_iso,
            **_tag(),
        }
        if not dry_run:
            await db.users.insert_one(user_doc)
        user_action = "created"
        primary_user_doc = user_doc

    await _upsert_demo_membership(
        db, primary_user_doc, generated_at=now_iso, dry_run=dry_run,
    )

    # 3. Horses.
    horses_added = 0
    for h in DEMO_HORSES:
        exists = await db.horses.find_one(
            {"barn_id": barn_id, "name": h["name"], "demo_seed_key": DEMO_KEY},
        )
        if exists:
            continue
        horse_doc = {
            "id": str(uuid.uuid4()),
            "barn_id": barn_id,
            "owner_user_id": user_id,
            "created_at": now_iso,
            **h,
            **_tag(),
        }
        if not dry_run:
            await db.horses.insert_one(horse_doc)
        horses_added += 1

    # 4. Tasks/appointments — 5 upcoming, 3 past (only if a `tasks`
    # collection is in use; otherwise log and skip cleanly).
    tasks_added = 0
    if "tasks" in await db.list_collection_names():
        # Don't double-add if previous run already populated.
        existing_count = await db.tasks.count_documents(
            {"barn_id": barn_id, "demo_seed_key": DEMO_KEY},
        )
        if existing_count == 0:
            templates = [
                ("Farrier visit",       +3,  "scheduled"),
                ("Veterinary checkup",  +7,  "scheduled"),
                ("Worming",             +14, "scheduled"),
                ("Lesson — Aurelia",    +1,  "scheduled"),
                ("Trim — Cinder",       +21, "scheduled"),
                ("Vaccination",         -7,  "completed"),
                ("Dental floating",     -21, "completed"),
                ("Hoof trim",           -35, "completed"),
            ]
            for title, day_offset, status in templates:
                due = (now + timedelta(days=day_offset)).isoformat()
                task = {
                    "id": str(uuid.uuid4()),
                    "barn_id": barn_id,
                    "owner_user_id": user_id,
                    "title": title,
                    "status": status,
                    "due_at": due,
                    "created_at": now_iso,
                    **_tag(),
                }
                if not dry_run:
                    await db.tasks.insert_one(task)
                tasks_added += 1

    # 5. Subscription record — purely local, NEVER a Stripe ID.
    sub_present = await db.subscriptions.find_one(
        {"barn_id": barn_id, "demo_seed_key": DEMO_KEY},
    )
    if not sub_present:
        sub_doc = {
            "id": f"demo_subscription_{uuid.uuid4().hex[:12]}",  # local, not Stripe-shaped
            "barn_id": barn_id,
            "status": "active",
            "tier": "demo",
            "billing_mode": "demo",
            "created_at": now_iso,
            "current_period_start": now_iso,
            "current_period_end": (now + timedelta(days=30)).isoformat(),
            **_tag(),
        }
        if not dry_run:
            await db.subscriptions.insert_one(sub_doc)
        sub_action = "created"
    else:
        sub_action = "already_present"

    # 6. Audit rows — 2 representative demo-tagged events so admin
    # dashboards have something to render when viewing this barn.
    audit_added = 0
    existing_audit = await db.audit_log.count_documents(
        {"resource_id": user_id, "metadata.demo_seed_key": DEMO_KEY},
    )
    if existing_audit == 0:
        rows = [
            {"action": "auth.login.success", "outcome": "success"},
            {"action": "horse.created", "outcome": "success"},
            {"action": "subscription.entitlement.applied", "outcome": "success"},
        ]
        for r in rows:
            entry = {
                "id": str(uuid.uuid4()),
                "ts": now_iso,
                "action": r["action"],
                "actor_email": DEMO_EMAIL,
                "actor_user_id": user_id,
                "resource_type": "user",
                "resource_id": user_id,
                "outcome": r["outcome"],
                "status_code": 200,
                "metadata": {
                    "demo_seed_key": DEMO_KEY,
                    "seed_phase": DEMO_PHASE,
                },
            }
            if not dry_run:
                await db.audit_log.insert_one(entry)
            audit_added += 1

    # 7. Top-level seed audit row — never carries the password value.
    if not dry_run:
        await db.audit_log.insert_one({
            "id": str(uuid.uuid4()),
            "ts": now_iso,
            "action": "admin.seed.demo_account_created",
            "actor_email": "(cli)",
            "actor_role": "(cli)",
            "resource_type": "user",
            "resource_id": user_id,
            "outcome": "success",
            "status_code": 200,
            "metadata": {
                "demo_seed_key": DEMO_KEY,
                "seed_phase": DEMO_PHASE,
                "barn_id": barn_id,
                "barn_action": barn_action,
                "user_action": user_action,
                "horses_added": horses_added,
                "tasks_added": tasks_added,
                "sub_action": sub_action,
                "audit_rows_added": audit_added,
                "password_source": password_source,
            },
        })

    extra_owner_result = None
    if extra_owner:
        extra_owner_result = await _ensure_extra_owner(
            db, barn_id=barn_id, now_iso=now_iso, dry_run=dry_run,
            reset_password=reset_extra_owner_password,
        )

    return {
        "barn_id": barn_id,
        "user_id": user_id,
        "barn_action": barn_action,
        "user_action": user_action,
        "horses_added": horses_added,
        "tasks_added": tasks_added,
        "sub_action": sub_action,
        "audit_rows_added": audit_added,
        "password_source": password_source,
        "minted_password": minted_password,
        "extra_owner": extra_owner_result,
    }


# ----------------------------------------------------------------------
# TEARDOWN
# ----------------------------------------------------------------------
async def _teardown(db, *, dry_run: bool) -> Dict[str, int]:
    """Remove every record tagged `demo_seed_key == DEMO_KEY`. We
    DO NOT touch records that lack the tag, even if they look similar."""
    sel = {"demo_seed_key": DEMO_KEY}
    audit_sel = {"metadata.demo_seed_key": DEMO_KEY}

    counts: Dict[str, int] = {}
    for col in ("users", "barns", "horses", "tasks", "subscriptions",
                "account_memberships"):
        if col not in await db.list_collection_names():
            counts[col] = 0
            continue
        if dry_run:
            counts[col] = await db[col].count_documents(sel)
        else:
            res = await db[col].delete_many(sel)
            counts[col] = res.deleted_count

    # Demo-tagged audit rows ARE removed (founder direction: "Keep
    # audit rows unless they are explicitly demo-tagged and safe to
    # remove" — our seed audit rows are explicitly tagged).
    if dry_run:
        counts["audit_log"] = await db.audit_log.count_documents(audit_sel)
    else:
        res = await db.audit_log.delete_many(audit_sel)
        counts["audit_log"] = res.deleted_count

    if not dry_run:
        await db.audit_log.insert_one({
            "id": str(uuid.uuid4()),
            "ts": datetime.now(timezone.utc).isoformat(),
            "action": "admin.seed.demo_account_torn_down",
            "actor_email": "(cli)",
            "actor_role": "(cli)",
            "resource_type": "demo_seed",
            "resource_id": DEMO_KEY,
            "outcome": "success",
            "status_code": 200,
            "metadata": {
                "demo_seed_key": DEMO_KEY,
                "seed_phase": DEMO_PHASE,
                "removed": counts,
            },
        })
    return counts


async def _main():
    args = _parse_args()

    if _is_prod() and not args.allow_prod and not args.dry_run:
        print("ERROR: APP_ENV is production. Pass --allow-prod to confirm "
              "(or use --dry-run to preview without writes).",
              file=sys.stderr)
        sys.exit(2)

    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "equinesync"
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    print("=" * 72)
    mode = "TEARDOWN" if args.teardown else "SEED"
    print(f"Phase Admin-8 — demo account {mode}"
          f"{'  (DRY-RUN)' if args.dry_run else ''}")
    print(f"APP_ENV={os.environ.get('APP_ENV') or 'development'}")
    print("=" * 72)

    if args.teardown:
        counts = await _teardown(db, dry_run=args.dry_run)
        print(f"  removed counts: {counts}")
        return

    r = await _seed(
        db, dry_run=args.dry_run, extra_owner=args.extra_owner,
        reset_extra_owner_password=args.reset_extra_owner_password,
    )
    print(f"  barn   {r['barn_action']:18} id={r['barn_id']}")
    print(f"  user   {r['user_action']:18} id={r['user_id']}  email={DEMO_EMAIL}")
    print(f"  horses added={r['horses_added']}")
    print(f"  tasks  added={r['tasks_added']}")
    print(f"  subscription {r['sub_action']}")
    print(f"  audit_rows added={r['audit_rows_added']}")
    print(f"  password_source={r['password_source']}")
    if r.get("extra_owner"):
        extra = r["extra_owner"]
        print("  extra_owner "
              f"{extra['user_action']:18} id={extra['user_id']}  "
              f"email={extra['email']}")
        print(f"  extra_owner_password {extra['password_action']}  "
              f"source={extra['password_source']}")
        print(f"  extra_owner_horse_link {extra['horse_link_action']}")
    if args.dry_run and r["password_source"] == "would_mint_on_apply":
        print()
        print("=" * 72)
        print("DRY-RUN: no password minted, none printed.")
        print("On apply, a 32-char one-time password would be minted for:")
        print("=" * 72)
        print(f"  {DEMO_EMAIL}  (would mint password on apply)")
    elif r["minted_password"]:
        print()
        print("=" * 72)
        print("ONE-TIME DEMO PASSWORD — copy now; not logged, not stored.")
        print("=" * 72)
        print(f"  {DEMO_EMAIL}  {r['minted_password']}")
        print()
        print("Pilot account logs in at /login (the normal client flow). It has")
        print("no platform_role; /admin/portal/* returns 403 unless separately")
        print("granted.")


if __name__ == "__main__":
    asyncio.run(_main())
