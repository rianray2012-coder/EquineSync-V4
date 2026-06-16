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


DEMO_KEY = "admin8_client_demo"
DEMO_PHASE = "phase_admin_8"

DEMO_EMAIL = "demo.client@equine-sync.com"
DEMO_NAME = "Demo Client"
DEMO_BARN_NAME = "Equine Sync Demo Barn"
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
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--allow-prod", action="store_true",
                   help="Required to run when APP_ENV is production.")
    p.add_argument("--teardown", action="store_true",
                   help=f"Remove every record tagged demo_seed_key='{DEMO_KEY}'.")
    return p.parse_args()


# ----------------------------------------------------------------------
# SEED
# ----------------------------------------------------------------------
async def _seed(db, *, dry_run: bool) -> Dict[str, object]:
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # 1. Barn / facility.
    existing_barn = await db.barns.find_one({"demo_seed_key": DEMO_KEY})
    if existing_barn:
        barn_id = existing_barn["id"]
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
    for col in ("users", "barns", "horses", "tasks", "subscriptions"):
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

    r = await _seed(db, dry_run=args.dry_run)
    print(f"  barn   {r['barn_action']:18} id={r['barn_id']}")
    print(f"  user   {r['user_action']:18} id={r['user_id']}  email={DEMO_EMAIL}")
    print(f"  horses added={r['horses_added']}")
    print(f"  tasks  added={r['tasks_added']}")
    print(f"  subscription {r['sub_action']}")
    print(f"  audit_rows added={r['audit_rows_added']}")
    print(f"  password_source={r['password_source']}")
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
        print("Demo logs in at /login (the normal client flow). The demo has")
        print("no platform_role; /admin/portal/* returns 403 unless separately")
        print("granted.")


if __name__ == "__main__":
    asyncio.run(_main())
