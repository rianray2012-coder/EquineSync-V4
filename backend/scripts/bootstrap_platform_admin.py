"""scripts/bootstrap_platform_admin.py — promote a user to a platform role.

Per the Admin-1 founder direction, existing `role="admin"` users are NOT
auto-elevated to the platform-admin trust boundary. Use this CLI to
explicitly promote the first super_admin (and any subsequent platform
admins until a UI promotion flow ships in a later phase).

Usage:
    cd /app/backend
    python -m scripts.bootstrap_platform_admin \\
        --email founder@equinesync.com \\
        --platform-role super_admin

    # Demote (clear platform role):
    python -m scripts.bootstrap_platform_admin \\
        --email someone@example.com --platform-role none

Safety:
  - Refuses to set a value that isn't one of PLATFORM_ROLES (or "none").
  - Always confirms by printing the BEFORE / AFTER user document
    (excluding password_hash).
  - Writes an audit_log entry tagged action="admin.platform_role.bootstrap"
    so the change is forever recoverable from the trail.
  - Asynchronous Mongo via motor (matches the running server).
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from core.permissions import PLATFORM_ROLES  # noqa: E402


def _parse_args():
    p = argparse.ArgumentParser(description="Bootstrap or revoke a platform admin role.")
    p.add_argument("--email", required=True, help="Target user's email address (case-insensitive).")
    p.add_argument(
        "--platform-role",
        required=True,
        help=f"One of {sorted(PLATFORM_ROLES) + ['none']} ('none' clears the field).",
    )
    return p.parse_args()


async def _main():
    args = _parse_args()
    target_role = (args.platform_role or "").strip().lower()
    if target_role != "none" and target_role not in PLATFORM_ROLES:
        print(f"ERROR: unknown platform role '{target_role}'. "
              f"Expected one of {sorted(PLATFORM_ROLES) + ['none']}.", file=sys.stderr)
        sys.exit(2)

    mongo_url = os.environ["MONGO_URL"]
    db_name = os.environ.get("DB_NAME") or "equinesync"
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    email = args.email.strip().lower()
    user = await db.users.find_one({"email": email}, {"password_hash": 0})
    if not user:
        print(f"ERROR: no user found with email={email}", file=sys.stderr)
        await client.close() if hasattr(client.close(), "__await__") else None
        sys.exit(3)

    before_role = (user.get("platform_role") or "").strip().lower() or "(none)"
    print(f"BEFORE: user={user.get('id')} email={email} platform_role={before_role}")

    update_doc = {"platform_role_updated_at": datetime.now(timezone.utc).isoformat()}
    if target_role == "none":
        await db.users.update_one(
            {"id": user["id"]},
            {"$set": update_doc, "$unset": {"platform_role": ""}},
        )
        new_role = "(none)"
    else:
        update_doc["platform_role"] = target_role
        await db.users.update_one({"id": user["id"]}, {"$set": update_doc})
        new_role = target_role
    print(f"AFTER:  user={user.get('id')} email={email} platform_role={new_role}")

    # Persistent audit entry — append-only.
    await db.audit_log.insert_one({
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": "admin.platform_role.bootstrap",
        "actor_email": "(cli)",
        "actor_role": "(cli)",
        "resource_type": "user",
        "resource_id": user["id"],
        "outcome": "success",
        "metadata": {
            "target_email": email,
            "previous_platform_role": before_role,
            "new_platform_role": new_role,
        },
    })

    print("OK — audit_log entry written: admin.platform_role.bootstrap")


if __name__ == "__main__":
    asyncio.run(_main())
