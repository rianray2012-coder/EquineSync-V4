#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf18_qa_uat_public_launch_readiness import (  # noqa: E402
    ROOT,
    build_rf18_qa_uat_public_launch_readiness,
    render_rf18_report,
)


PACKAGE_FILES = [
    "BUILD_NEXT_RF18_QA_UAT_PUBLIC_LAUNCH_READINESS_README.md",
    "docs/RF18_QA_UAT_PUBLIC_LAUNCH_READINESS.md",
    "docs/RF18_QA_UAT_PUBLIC_LAUNCH_READINESS_PLAN.md",
    "backend/core/rf18_qa_uat_public_launch_readiness.py",
    "backend/scripts/build_rf18_qa_uat_public_launch_readiness.py",
    "backend/tests/test_rf18_qa_uat_public_launch_readiness.py",
    "outputs/rf18_qa_uat_public_launch_readiness_report.md",
    "docs/REFINEMENT_ROADMAP.md",
    "docs/REFINEMENT_MASTER_FIX_LIST.md",
    "memory/PRD.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the RF18 QA/UAT public-launch readiness report.")
    parser.add_argument(
        "--output",
        default="outputs/rf18_qa_uat_public_launch_readiness_report.md",
        help="Report output path.",
    )
    parser.add_argument(
        "--zip-output",
        default=None,
        help="Optional RF18 review package output path. Rebuilt after the report is written.",
    )
    parser.add_argument("--fail-on-blockers", action="store_true")
    args = parser.parse_args()

    report = build_rf18_qa_uat_public_launch_readiness(ROOT)
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_rf18_report(report), encoding="utf-8")

    if args.zip_output:
        zip_path = Path(args.zip_output)
        if not zip_path.is_absolute():
            zip_path = ROOT / zip_path
        _write_package(zip_path)
        print(f"RF18 package written: {zip_path}")

    blockers = report["issue_counts"].get("blocker", 0)
    print(f"RF18 report written: {output_path}")
    print(
        f"status={report['overall_status']} public_launch={report['public_launch_status']} "
        f"blockers={blockers} open_uat={report['uat_open_count']}"
    )
    if args.fail_on_blockers and blockers:
        return 1
    return 0


def _package_manifest() -> list[str]:
    return sorted(dict.fromkeys(PACKAGE_FILES))


def _write_package(zip_path: Path) -> None:
    manifest = _package_manifest()
    missing = [item for item in manifest if not (ROOT / item).is_file()]
    if missing:
        raise FileNotFoundError(f"RF18 package manifest has missing files: {missing}")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
        for item in manifest:
            zf.write(ROOT / item, item)


if __name__ == "__main__":
    raise SystemExit(main())
