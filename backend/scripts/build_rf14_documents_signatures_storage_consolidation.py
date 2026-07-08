#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf14_documents_signatures_storage_consolidation import (  # noqa: E402
    ROOT,
    build_rf14_documents_signatures_storage_consolidation,
    render_rf14_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the RF14 documents/signatures/storage consolidation report.")
    parser.add_argument(
        "--output",
        default="outputs/rf14_documents_signatures_storage_consolidation_report.md",
        help="Report output path.",
    )
    parser.add_argument("--fail-on-blockers", action="store_true")
    args = parser.parse_args()

    report = build_rf14_documents_signatures_storage_consolidation(ROOT)
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_rf14_report(report), encoding="utf-8")

    counts = report["status_counts"]
    blocked_or_missing = counts.get("blocked", 0) + counts.get("missing", 0)
    print(f"RF14 report written: {output_path}")
    print(f"status={report['overall_status']} blocked_or_missing={blocked_or_missing}")
    if args.fail_on_blockers and blocked_or_missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
