"""Generate the Stripe live-payment Wave E webhook/projection readiness report."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from core.stripe_webhook_projection_readiness import (  # noqa: E402
    build_stripe_webhook_projection_readiness_report,
    render_stripe_webhook_projection_readiness_markdown,
)


DEFAULT_OUTPUT = ROOT / "outputs" / "stripe_webhook_projection_readiness_report.md"


def _parse_args():
    parser = argparse.ArgumentParser(description="Generate Stripe webhook/projection readiness report.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Markdown report path. Default: outputs/stripe_webhook_projection_readiness_report.md",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    report = build_stripe_webhook_projection_readiness_report()
    markdown = render_stripe_webhook_projection_readiness_markdown(report)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    issue_counts = report.get("issue_counts") or {}
    print(f"Stripe webhook/projection readiness report written: {out}")
    print(
        "Summary: "
        f"{issue_counts.get('blocker', 0)} blocker(s), "
        f"{issue_counts.get('warning', 0)} warning(s), "
        f"overall={report['overall_status']}."
    )
    return 0 if not issue_counts.get("blocker") else 2


if __name__ == "__main__":
    raise SystemExit(main())
