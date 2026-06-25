"""Build-Next-1 billing launch readiness report.

Reads current catalog collections, compares them with the locked live Stripe
catalog constants and future Apple product-id contract placeholders, and writes
a markdown report. This script is read-only with respect to MongoDB.

Usage:
    cd <repo-root>
    ./.venv/bin/python -m backend.scripts.build_next_1_billing_launch_readiness
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(ROOT / ".env")
load_dotenv(BACKEND / ".env")

from core.billing_launch_readiness import (  # noqa: E402
    build_billing_launch_readiness_report,
    render_billing_launch_readiness_markdown,
)


DEFAULT_OUTPUT = ROOT / "outputs" / "build_next_1_billing_launch_readiness_report.md"


def _parse_args():
    parser = argparse.ArgumentParser(description="Generate Build-Next-1 billing launch readiness report.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Markdown report path. Default: outputs/build_next_1_billing_launch_readiness_report.md",
    )
    parser.add_argument(
        "--constants-only",
        action="store_true",
        help="Generate from locked source constants only; do not require or read MongoDB.",
    )
    return parser.parse_args()


async def _main() -> int:
    args = _parse_args()
    if args.constants_only:
        report = build_billing_launch_readiness_report()
        markdown = render_billing_launch_readiness_markdown(report)
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
        issue_counts = report.get("issue_counts") or {}
        print(f"Build-Next-1 billing launch readiness report written: {out}")
        print(
            "Summary: "
            f"{report['source_counts']['catalog_plans']} catalog plan(s), "
            f"{report['source_counts']['addons']} add-on(s), "
            f"{issue_counts.get('blocker', 0)} blocker(s), "
            f"{issue_counts.get('warning', 0)} warning(s)."
        )
        return 0 if not issue_counts.get("blocker") else 2

    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        print(
            "ERROR: MONGO_URL is not configured. Export MONGO_URL and DB_NAME, "
            "or add them to backend/.env, then rerun the readiness report.",
            file=sys.stderr,
        )
        return 2
    from motor.motor_asyncio import AsyncIOMotorClient

    db_name = os.environ.get("DB_NAME") or "equinesync"
    client = AsyncIOMotorClient(mongo_url)
    try:
        db = client[db_name]
        plans = await db.plans.find({}, {"_id": 0}).to_list(length=500)
        subscription_plans = await db.subscription_plans.find({}, {"_id": 0}).to_list(length=500)
        addons = await db.subscription_addons.find({}, {"_id": 0}).to_list(length=500)
        report = build_billing_launch_readiness_report(
            plans=plans,
            subscription_plans=subscription_plans,
            addons=addons,
        )
        markdown = render_billing_launch_readiness_markdown(report)

        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")

        issue_counts = report.get("issue_counts") or {}
        print(f"Build-Next-1 billing launch readiness report written: {out}")
        print(
            "Summary: "
            f"{report['source_counts']['catalog_plans']} catalog plan(s), "
            f"{report['source_counts']['addons']} add-on(s), "
            f"{issue_counts.get('blocker', 0)} blocker(s), "
            f"{issue_counts.get('warning', 0)} warning(s)."
        )
        return 0 if not issue_counts.get("blocker") else 2
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main()))
