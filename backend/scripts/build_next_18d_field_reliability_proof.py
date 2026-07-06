from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.field_reliability_proof import (  # noqa: E402
    build_field_reliability_proof,
    render_field_reliability_report,
)


DEFAULT_OUTPUT = ROOT / "outputs" / "bn18d_field_reliability_report.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build-Next-18D read-only field reliability/offline proof report."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown report output path.")
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Exit non-zero if required source evidence is missing.",
    )
    args = parser.parse_args()

    report = build_field_reliability_proof(ROOT)
    rendered = render_field_reliability_report(report)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")

    blockers = report["issue_counts"].get("blocker", 0)
    decisions = report["issue_counts"].get("decision_required", 0)
    warnings = report["issue_counts"].get("warning", 0)
    print(f"Build-Next-18D field reliability proof written: {output}")
    print(
        "Summary: "
        f"status={report['overall_status']} "
        f"blocker(s)={blockers} "
        f"warning(s)={warnings} "
        f"decision_required={decisions}"
    )
    if args.fail_on_blockers and blockers:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
