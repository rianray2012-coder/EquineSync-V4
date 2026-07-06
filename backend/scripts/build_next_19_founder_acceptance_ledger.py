from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.founder_acceptance_ledger import (  # noqa: E402
    build_founder_acceptance_ledger,
    render_founder_acceptance_ledger,
)


DEFAULT_OUTPUT = ROOT / "outputs" / "bn19_founder_acceptance_ledger.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build-Next-19 read-only founder acceptance ledger."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown report output path.")
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Exit non-zero if required locked evidence inputs are missing.",
    )
    args = parser.parse_args()

    report = build_founder_acceptance_ledger(ROOT)
    rendered = render_founder_acceptance_ledger(report)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")

    blockers = report["issue_counts"].get("blocker", 0)
    decisions = report["issue_counts"].get("decision_required", 0)
    warnings = report["issue_counts"].get("warning", 0)
    print(f"Build-Next-19 founder acceptance ledger written: {output}")
    print(
        "Summary: "
        f"status={report['overall_status']} "
        f"recommendation={report['pilot_recommendation']} "
        f"blocker(s)={blockers} "
        f"warning(s)={warnings} "
        f"decision_required={decisions}"
    )
    if args.fail_on_blockers and blockers:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
