from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.bn20_bn12_closure import (  # noqa: E402
    build_bn20_bn12_closure,
    render_bn20_bn12_closure,
)


DEFAULT_OUTPUT = ROOT / "outputs" / "bn20_bn12_closure_report.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build-Next-20 / BN12 read-only closure report."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown report output path.")
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Exit non-zero if BN20 / BN12 closure blockers are present.",
    )
    args = parser.parse_args()

    report = build_bn20_bn12_closure(ROOT)
    rendered = render_bn20_bn12_closure(report)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")

    blockers = report["issue_counts"].get("blocker", 0)
    decisions = report["issue_counts"].get("decision_required", 0)
    warnings = report["issue_counts"].get("warning", 0)
    print(f"Build-Next-20 / BN12 closure report written: {output}")
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
