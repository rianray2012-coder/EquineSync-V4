from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf9_trainer_operating_center import (  # noqa: E402
    ROOT,
    build_rf9_trainer_operating_center,
    render_rf9_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the RF9 trainer operating-center report.")
    parser.add_argument(
        "--output",
        default="outputs/rf9_trainer_operating_center_report.md",
        help="Report path, relative to repo root unless absolute.",
    )
    parser.add_argument("--fail-on-blockers", action="store_true")
    args = parser.parse_args(argv)

    report = build_rf9_trainer_operating_center(ROOT)
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_rf9_report(report), encoding="utf-8")

    blocked = report["status_counts"].get("blocked", 0) + report["status_counts"].get("missing", 0)
    print(f"RF9 report written: {output_path}")
    print(f"status={report['overall_status']} blocked_or_missing={blocked}")
    if args.fail_on_blockers and blocked:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
