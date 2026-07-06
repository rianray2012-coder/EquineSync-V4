from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.bn21_pilot_go_no_go import (  # noqa: E402
    build_bn21_pilot_go_no_go,
    render_bn21_pilot_go_no_go,
)


DEFAULT_OUTPUT = ROOT / "outputs" / "bn21_first_client_pilot_go_no_go_report.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build-Next-21 read-only first-client pilot go/no-go report."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown report output path.")
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Exit non-zero if BN21 go/no-go blockers are present.",
    )
    args = parser.parse_args()

    report = build_bn21_pilot_go_no_go(ROOT)
    rendered = render_bn21_pilot_go_no_go(report)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")

    blockers = report["issue_counts"].get("blocker", 0)
    decisions = report["issue_counts"].get("decision_required", 0)
    warnings = report["issue_counts"].get("warning", 0)
    print(f"Build-Next-21 first-client pilot go/no-go report written: {output}")
    print(
        "Summary: "
        f"status={report['overall_status']} "
        f"recommendation={report['recommendation']} "
        f"blocker(s)={blockers} "
        f"warning(s)={warnings} "
        f"decision_required={decisions}"
    )
    if args.fail_on_blockers and blockers:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
