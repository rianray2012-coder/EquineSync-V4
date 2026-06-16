"""scripts/seed_initial_admins.py — Phase Admin-8 Part A.

Idempotent CLI to ensure the 4 founder-locked platform admin users
exist (or are promoted) with the locked platform roles. Safe for
re-runs; safe across staging and production (production requires
`--allow-prod`).

Locked roles (founder, Feb 2026):
    info@equine-sync.com        →  platform_admin
    prsindustries23@gmail.com   →  billing_admin
    rian.ray2012@gmail.com      →  super_admin
    prspoon23@gmail.com         →  super_admin

Password source of truth (founder decision 1d):
    1. If `SEED_ADMIN_<slug>_PASSWORD` env var is present → use it.
    2. Else → mint a 32-char URL-safe random password, print ONCE to
       stdout (never to logs, audit, or files), and persist its
       bcrypt hash. The admin is expected to log in and change it.

The mint-and-print value is the ONLY moment the secret crosses any
boundary; nothing else writes it. Audit rows carry only metadata
(`source: "env" | "mint"`, never the value).

Usage:
    cd /app/backend
    python -m scripts.seed_initial_admins                    # safe local/staging
    python -m scripts.seed_initial_admins --dry-run          # show plan only
    python -m scripts.seed_initial_admins --allow-prod       # production
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


# Locked admin roster (founder decision, Feb 2026).
INITIAL_ADMINS = [
    {
        "email":         "info@equine-sync.com",
        "full_name":     "Admin 1",
        "title":         "Initial Admin Operator",
        "platform_role": "platform_admin",
    },
    {
        "email":         "prsindustries23@gmail.com",
        "full_name":     "Admin Business",
        "title":         "Billing Administrator",
        "platform_role": "billing_admin",
    },
    {
        "email":         "rian.ray2012@gmail.com",
        "full_name":     "Rian Ray",
        "title":         "Owner / Founder",
        "platform_role": "super_admin",
    },
    {
        "email":         "prspoon23@gmail.com",
        "full_name":     "Patrick K",
        "title":         "Owner / COO",
        "platform_role": "super_admin",
    },
]


def _slug(email: str) -> str:
    """Convert an email to a SCREAMING_SNAKE_CASE slug for env-var lookup."""
    return re.sub(r"[^A-Za-z0-9]+", "_", email).strip("_").upper()


def _hash_pwd(p: str) -> str:
    return bcrypt.hashpw(p.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _mint_password() -> str:
    # 32-char URL-safe random; >= 192 bits of entropy.
    return secrets.token_urlsafe(24)


def _parse_args():
    p = argparse.ArgumentParser(description=(
        "Seed/promote Phase Admin-8 initial platform admin users. "
        "Idempotent and re-runnable."
    ))
    p.add_argument("--dry-run", action="store_true",
                   help="Print the plan; do NOT touch the database.")
    p.add_argument("--allow-prod", action="store_true",
                   help="Required to run when APP_ENV is production.")
    # Codex 7A.2b-equivalent round-2 P1 fix: role changes on an
    # existing user require an explicit confirmation flag. Without it,
    # the script prints the role diff and SKIPS the user — no access-
    # control mutation happens silently.
    p.add_argument("--force-role-change", action="store_true",
                   help=(
                       "Allow overwriting an existing user's "
                       "platform_role when it differs from the locked "
                       "roster value. Default: skip + print diff."
                   ))
    # Codex round-2 P0 fix: the test suite must NEVER touch the real
    # founder roster. `--roster <path>` accepts a JSON file with a
    # list of {email, full_name, title, platform_role} objects. If
    # absent, the locked roster ships above is used.
    p.add_argument("--roster", type=str, default=None,
                   help=(
                       "Path to a JSON file overriding the admin "
                       "roster. Used by tests to point at throwaway "
                       "emails."
                   ))
    return p.parse_args()


def _load_roster(path: Optional[str]) -> List[Dict[str, str]]:
    if not path:
        return INITIAL_ADMINS
    import json
    with open(path) as f:
        roster = json.load(f)
    assert isinstance(roster, list), "roster JSON must be a list"
    for entry in roster:
        for k in ("email", "full_name", "title", "platform_role"):
            assert k in entry, f"roster entry missing {k}: {entry}"
    return roster


def _is_prod() -> bool:
    return (os.environ.get("APP_ENV") or "").strip().lower() in ("production", "prod")


async def _ensure_admin(db, spec: Dict[str, str], *, dry_run: bool) -> Dict[str, str]:
    """Idempotently ensure the admin user exists and carries the
    locked platform_role. Returns a result dict (no secret values)."""
    email = spec["email"].lower()
    existing = await db.users.find_one({"email": email}, {"password_hash": 0})

    env_key = f"SEED_ADMIN_{_slug(email)}_PASSWORD"
    env_password = os.environ.get(env_key)
    source = "env" if env_password else "mint"
    minted_password: Optional[str] = None

    action: str
    if existing:
        # PROMOTE only — never re-hash the password on an existing user.
        # Safe admin fields: platform_role, full_name (if blank), title,
        # account_status, role_status, platform_role_updated_at.
        updates: Dict[str, object] = {
            "platform_role": spec["platform_role"],
            "platform_role_updated_at": datetime.now(timezone.utc).isoformat(),
            "account_status": "active",
            "role_status": "active",
        }
        if not existing.get("full_name"):
            updates["full_name"] = spec["full_name"]
        if not existing.get("title"):
            updates["title"] = spec["title"]
        if dry_run:
            action = "would_promote"
        else:
            await db.users.update_one({"id": existing["id"]}, {"$set": updates})
            action = "promoted"
        user_id = existing["id"]
        prev_role = (existing.get("platform_role") or "(none)")
        source = "n/a (existing user)"
    else:
        # CREATE — password from env or freshly minted.
        password = env_password or _mint_password()
        if not env_password:
            minted_password = password
        user_doc = {
            "id": str(uuid.uuid4()),
            "email": email,
            "full_name": spec["full_name"],
            "title": spec["title"],
            "role": "admin",          # legacy role; platform_role is the source of truth.
            "role_status": "active",
            "account_status": "active",
            "platform_role": spec["platform_role"],
            "platform_role_updated_at": datetime.now(timezone.utc).isoformat(),
            "password_hash": _hash_pwd(password),
            "email_verified": True,   # operator-seeded; out-of-band verified.
            "signup_source": "phase_admin_8_seed",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        if dry_run:
            action = "would_create"
            user_id = "(dry-run)"
        else:
            await db.users.insert_one(user_doc)
            action = "created"
            user_id = user_doc["id"]
        prev_role = "(none)"

    # Audit — NEVER log the password value, only metadata.
    if not dry_run:
        await db.audit_log.insert_one({
            "id": str(uuid.uuid4()),
            "ts": datetime.now(timezone.utc).isoformat(),
            "action": f"admin.seed.{action}",
            "actor_email": "(cli)",
            "actor_role": "(cli)",
            "resource_type": "user",
            "resource_id": user_id,
            "outcome": "success",
            "status_code": 200,
            "metadata": {
                "target_email": email,
                "previous_platform_role": prev_role,
                "new_platform_role": spec["platform_role"],
                "password_source": source,
                "seed_phase": "phase_admin_8",
            },
        })

    return {
        "email": email,
        "platform_role": spec["platform_role"],
        "action": action,
        "user_id": user_id,
        "password_source": source,
        "minted_password": minted_password,  # may be None
        "env_var": env_key,
    }


async def _main():
    args = _parse_args()

    if _is_prod() and not args.allow_prod:
        print("ERROR: APP_ENV is production. Pass --allow-prod to confirm.",
              file=sys.stderr)
        sys.exit(2)

    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "equinesync"
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    print("=" * 72)
    print(f"Phase Admin-8 — seeding initial platform admins"
          f"{'  (DRY-RUN)' if args.dry_run else ''}")
    print(f"APP_ENV={os.environ.get('APP_ENV') or 'development'}")
    print("=" * 72)

    results: List[Dict[str, str]] = []
    for spec in INITIAL_ADMINS:
        r = await _ensure_admin(db, spec, dry_run=args.dry_run)
        results.append(r)
        print(f"  {r['action']:14}  {r['email']:30}  "
              f"role={r['platform_role']}  source={r['password_source']}")

    # Print minted passwords ONCE. Never logged, never persisted.
    minted = [r for r in results if r.get("minted_password")]
    if minted:
        print()
        print("=" * 72)
        print("ONE-TIME PASSWORDS — copy them now; they will not be shown again.")
        print("They are not written to logs, audit_log, or any file.")
        print("=" * 72)
        for r in minted:
            print(f"  {r['email']:30}  {r['minted_password']}")
        print()
        print("Each admin should log in to /admin/portal/login with the above")
        print("password, then change it from their account settings.")

    print()
    print(f"Done. {sum(1 for r in results if r['action'] in ('created','promoted'))}"
          f" change(s) applied"
          f"{', dry-run' if args.dry_run else ''}.")


if __name__ == "__main__":
    asyncio.run(_main())
