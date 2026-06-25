"""Phase 15R-B migration dry-run report.

Reads current `plans` and `subscriptions`, projects them into the future
provider-neutral entitlement shapes, and writes a markdown gap report. This
script is intentionally read-only with respect to MongoDB.

Usage:
    cd <repo-root>
    ./.venv/bin/python -m backend.scripts.phase15r_migration_dry_run
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(ROOT / ".env")
load_dotenv(BACKEND / ".env")

from core.entitlements_migration import build_migration_dry_run, render_migration_markdown  # noqa: E402


DEFAULT_OUTPUT = ROOT / "outputs" / "phase15r_b_migration_dry_run_report.md"


def _parse_args():
    p = argparse.ArgumentParser(description="Generate Phase 15R-B migration dry-run report.")
    p.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Markdown report path. Default: outputs/phase15r_b_migration_dry_run_report.md",
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
        plans = await db.plans.find({}, {"_id": 0}).to_list(length=500)
        subscriptions = await db.subscriptions.find({}, {"_id": 0}).to_list(length=5000)
        report = build_migration_dry_run(plans=plans, subscriptions=subscriptions)
        markdown = render_migration_markdown(report)

        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")

        severity = report.get("severity_counts") or {}
        print(f"Phase 15R-B dry-run report written: {out}")
        print(
            "Summary: "
            f"{report['source_counts']['plans']} plan rows, "
            f"{report['source_counts']['subscriptions']} subscription rows, "
            f"{severity.get('blocker', 0)} blocker(s), "
            f"{severity.get('warning', 0)} warning(s)."
        )
        return 0 if not severity.get("blocker") else 2
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main()))
