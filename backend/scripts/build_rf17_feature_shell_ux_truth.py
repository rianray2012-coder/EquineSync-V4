#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf17_feature_shell_ux_truth import (  # noqa: E402
    ROOT,
    build_rf17_feature_shell_ux_truth,
    render_rf17_report,
)


PACKAGE_FILES = [
    "BUILD_NEXT_RF17_FEATURE_SHELL_UX_TRUTH_README.md",
    "docs/RF17_FEATURE_SHELL_UX_TRUTH.md",
    "docs/RF17_FEATURE_SHELL_UX_TRUTH_PLAN.md",
    "backend/core/rf17_feature_shell_ux_truth.py",
    "backend/scripts/build_rf17_feature_shell_ux_truth.py",
    "backend/tests/test_rf17_feature_shell_ux_truth.py",
    "outputs/rf17_feature_shell_ux_truth_report.md",
    "frontend/src/App.js",
    "frontend/src/lib/roleNavigation.js",
    "frontend/src/pages/AdvancedReports.jsx",
    "frontend/src/pages/GroupMessaging.jsx",
    "frontend/src/pages/Integrations.jsx",
    "frontend/src/pages/MobileReadiness.jsx",
    "frontend/src/pages/FormsSignatures.jsx",
    "docs/REFINEMENT_ROADMAP.md",
    "docs/REFINEMENT_MASTER_FIX_LIST.md",
    "memory/PRD.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the RF17 feature-shell UX truth report.")
    parser.add_argument(
        "--output",
        default="outputs/rf17_feature_shell_ux_truth_report.md",
        help="Report output path.",
    )
    parser.add_argument(
        "--zip-output",
        default=None,
        help="Optional RF17 review package output path. Rebuilt after the report is written.",
    )
    parser.add_argument("--fail-on-blockers", action="store_true")
    args = parser.parse_args()

    report = build_rf17_feature_shell_ux_truth(ROOT)
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_rf17_report(report), encoding="utf-8")

    if args.zip_output:
        zip_path = Path(args.zip_output)
        if not zip_path.is_absolute():
            zip_path = ROOT / zip_path
        _write_package(zip_path)
        print(f"RF17 package written: {zip_path}")

    blockers = report["issue_counts"].get("blocker", 0)
    print(f"RF17 report written: {output_path}")
    print(f"status={report['overall_status']} blockers={blockers}")
    if args.fail_on_blockers and blockers:
        return 1
    return 0


def _package_manifest() -> list[str]:
    return sorted(dict.fromkeys(PACKAGE_FILES))


def _write_package(zip_path: Path) -> None:
    manifest = _package_manifest()
    missing = [item for item in manifest if not (ROOT / item).is_file()]
    if missing:
        raise FileNotFoundError(f"RF17 package manifest has missing files: {missing}")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
        for item in manifest:
            zf.write(ROOT / item, item)


if __name__ == "__main__":
    raise SystemExit(main())
