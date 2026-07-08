#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf13_messaging_notifications_delivery_truth import (  # noqa: E402
    ROOT,
    build_rf13_messaging_notifications_delivery_truth,
    render_rf13_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the RF13 messaging/notifications delivery-truth report.")
    parser.add_argument(
        "--output",
        default="outputs/rf13_messaging_notifications_delivery_truth_report.md",
        help="Report output path.",
    )
    parser.add_argument("--fail-on-blockers", action="store_true")
    args = parser.parse_args()

    report = build_rf13_messaging_notifications_delivery_truth(ROOT)
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_rf13_report(report), encoding="utf-8")

    counts = report["status_counts"]
    blocked_or_missing = counts.get("blocked", 0) + counts.get("missing", 0)
    print(f"RF13 report written: {output_path}")
    print(f"status={report['overall_status']} blocked_or_missing={blocked_or_missing}")
    if args.fail_on_blockers and blocked_or_missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
