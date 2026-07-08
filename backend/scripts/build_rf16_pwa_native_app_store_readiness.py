#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf16_pwa_native_app_store_readiness import (  # noqa: E402
    ROOT,
    build_rf16_pwa_native_app_store_readiness,
    render_rf16_report,
)


STATIC_PACKAGE_FILES = [
    "BUILD_NEXT_RF16_PWA_NATIVE_APP_STORE_READINESS_README.md",
    "docs/RF16_PWA_NATIVE_APP_STORE_READINESS.md",
    "docs/RF16_PWA_NATIVE_APP_STORE_READINESS_PLAN.md",
    "backend/core/rf16_pwa_native_app_store_readiness.py",
    "backend/scripts/build_rf16_pwa_native_app_store_readiness.py",
    "backend/tests/test_rf16_pwa_native_app_store_readiness.py",
    "outputs/rf16_pwa_native_app_store_readiness_report.md",
    "frontend/package.json",
    "frontend/package-lock.json",
    "frontend/capacitor.config.json",
    "docs/REFINEMENT_ROADMAP.md",
    "docs/REFINEMENT_MASTER_FIX_LIST.md",
    "memory/PRD.md",
    "docs/BN22A_CAPACITOR_NATIVE_READINESS_PLAN.md",
    "docs/APP_STORE_PRODUCTION_READINESS.md",
]

NATIVE_PACKAGE_ROOTS = [
    "frontend/android",
    "frontend/ios",
]

EXCLUDED_PACKAGE_PARTS = {
    ".gradle",
    "node_modules",
    "build",
    "public",
    "__pycache__",
}

EXCLUDED_PACKAGE_FILES = {
    "frontend/android/local.properties",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the RF16 PWA/native app-store readiness report.")
    parser.add_argument(
        "--output",
        default="outputs/rf16_pwa_native_app_store_readiness_report.md",
        help="Report output path.",
    )
    parser.add_argument(
        "--zip-output",
        default=None,
        help="Optional RF16 review package output path. Rebuilt after the report is written.",
    )
    parser.add_argument("--fail-on-source-blockers", action="store_true")
    args = parser.parse_args()

    report = build_rf16_pwa_native_app_store_readiness(ROOT)
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_rf16_report(report), encoding="utf-8")

    if args.zip_output:
        zip_path = Path(args.zip_output)
        if not zip_path.is_absolute():
            zip_path = ROOT / zip_path
        _write_package(zip_path)
        print(f"RF16 package written: {zip_path}")

    source_blockers = [
        issue for issue in report["issues"]
        if issue["category"] in {"source_evidence", "overclaim_guard"}
    ]
    print(f"RF16 report written: {output_path}")
    print(f"status={report['overall_status']} source_blockers={len(source_blockers)} total_blockers={report['issue_counts'].get('blocker', 0)}")
    if args.fail_on_source_blockers and source_blockers:
        return 1
    return 0


def _package_manifest() -> list[str]:
    files = list(STATIC_PACKAGE_FILES)
    for package_root in NATIVE_PACKAGE_ROOTS:
        root_path = ROOT / package_root
        if not root_path.exists():
            continue
        for path in sorted(item for item in root_path.rglob("*") if item.is_file()):
            relative = path.relative_to(ROOT).as_posix()
            if _excluded_from_package(relative):
                continue
            files.append(relative)
    return sorted(dict.fromkeys(files))


def _excluded_from_package(relative: str) -> bool:
    if relative in EXCLUDED_PACKAGE_FILES:
        return True
    parts = set(Path(relative).parts)
    return bool(parts & EXCLUDED_PACKAGE_PARTS)


def _write_package(zip_path: Path) -> None:
    manifest = _package_manifest()
    missing = [item for item in manifest if not (ROOT / item).is_file()]
    if missing:
        raise FileNotFoundError(f"RF16 package manifest has missing files: {missing}")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
        for item in manifest:
            zf.write(ROOT / item, item)


if __name__ == "__main__":
    raise SystemExit(main())
