#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf15_offline_lock_screen_field_reliability import (  # noqa: E402
    ROOT,
    build_rf15_offline_lock_screen_field_reliability,
    render_rf15_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the RF15 offline/field-reliability report.")
    parser.add_argument(
        "--output",
        default="outputs/rf15_offline_lock_screen_field_reliability_report.md",
        help="Report output path.",
    )
    parser.add_argument("--fail-on-blockers", action="store_true")
    args = parser.parse_args()

    report = build_rf15_offline_lock_screen_field_reliability(ROOT)
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_rf15_report(report), encoding="utf-8")

    blockers = report["issue_counts"].get("blocker", 0)
    print(f"RF15 report written: {output_path}")
    print(f"status={report['overall_status']} blockers={blockers}")
    if args.fail_on_blockers and blockers:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
