"""Build-Next-18A provider-live proof.

Generates a scrubbed provider-readiness report from environment variables and
locked source constants only. It does not call Stripe, Resend, DocuSign, or
MongoDB.

Usage:
    cd <repo-root>
    ./.venv/bin/python -m backend.scripts.build_next_18a_provider_live_proof
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(ROOT / ".env")
load_dotenv(BACKEND / ".env")

from core.provider_live_proof import (  # noqa: E402
    build_provider_live_proof,
    render_provider_live_proof_markdown,
)


DEFAULT_OUTPUT = ROOT / "outputs" / "bn18a_provider_live_proof_report.md"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the Build-Next-18A provider-live proof report."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Markdown output path. Default: outputs/bn18a_provider_live_proof_report.md",
    )
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Exit 2 when provider-live blockers are present. Default writes evidence and exits 0.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    report = build_provider_live_proof(os.environ)
    markdown = render_provider_live_proof_markdown(report)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")

    issue_counts = report.get("issue_counts") or {}
    print(f"Build-Next-18A provider-live proof written: {out}")
    print(
        "Summary: "
        f"status={report.get('overall_status')} "
        f"blocker(s)={issue_counts.get('blocker', 0)} "
        f"warning(s)={issue_counts.get('warning', 0)}"
    )
    if args.fail_on_blockers and issue_counts.get("blocker", 0):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
