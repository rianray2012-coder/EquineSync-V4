"""Phase 15R-E billing-seat dry-run report.

Reads current `users` rows, projects them into future billing-seat fields, and
writes a markdown report. This script is intentionally read-only with respect
to MongoDB.

Usage:
    cd <repo-root>
    ./.venv/bin/python -m backend.scripts.phase15r_billing_seat_dry_run
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(ROOT / ".env")
load_dotenv(BACKEND / ".env")

from core.billing_seats import build_billing_seat_dry_run, render_billing_seat_markdown  # noqa: E402


DEFAULT_OUTPUT = ROOT / "outputs" / "phase15r_e_billing_seat_dry_run_report.md"


def _parse_args():
    p = argparse.ArgumentParser(description="Generate Phase 15R-E billing-seat dry-run report.")
    p.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Markdown report path. Default: outputs/phase15r_e_billing_seat_dry_run_report.md",
    )
    return p.parse_args()


async def _main() -> int:
    args = _parse_args()
    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        print(
            "ERROR: MONGO_URL is not configured. Export MONGO_URL and DB_NAME, "
            "or add them to backend/.env, then rerun the dry-run report.",
            file=sys.stderr,
        )
        return 2
    db_name = os.environ.get("DB_NAME") or "equinesync"
    client = AsyncIOMotorClient(mongo_url)
    try:
        db = client[db_name]
        try:
            users = await db.users.find({}, {"_id": 0}).to_list(length=10000)
        except PyMongoError as exc:
            print(
                "ERROR: Could not read Mongo users collection for the dry-run. "
                f"Check MONGO_URL/DB_NAME and local Mongo access. Details: {exc}",
                file=sys.stderr,
            )
            return 2
        report = build_billing_seat_dry_run(users)
        markdown = render_billing_seat_markdown(report)

        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")

        issues = report.get("issue_counts") or {}
        print(f"Phase 15R-E billing-seat dry-run report written: {out}")
        print(
            "Summary: "
            f"{report['source_counts']['users']} user rows, "
            f"{issues.get('blocker', 0)} blocker(s), "
            f"{issues.get('warning', 0)} warning(s)."
        )
        return 0
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main()))
