#!/usr/bin/env python3
"""Create the checksum-backed reconciliation evidence archive."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
REVIEW = REPO / "docs/canon/reviews/eight_canon_founder_approval_reconciliation_v1_0"
OUTPUT = REPO / "outputs/Eight_Canon_Founder_Approval_Status_Reconciliation_Package"
ARTIFACTS = OUTPUT / "artifacts"
ZIP_PATH = REPO / "outputs/eight_canon_founder_approval_status_reconciliation_package.zip"
SHA_PATH = ZIP_PATH.with_suffix(ZIP_PATH.suffix + ".sha256")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def files_to_package() -> list[Path]:
    paths = [
        REPO / "docs/canon/CANON_INDEX.md",
        REPO / "docs/canon/companions/CONSTITUTIONAL_DOMAIN_OWNERSHIP_AND_BOUNDARY_REGISTER_V1_1.md",
        REPO / "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_AUTHORITY_MATRIX_V1_2.md",
        REPO / "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_CROSS_REFERENCE_INDEX_V1_2.md",
        REPO / "docs/canon/companions/EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md",
        REPO / "docs/canon/companions/MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.md",
        REPO / "docs/canon/companions/MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.md",
        REPO / "docs/canon/companions/MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.md",
        REPO / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json",
        REPO / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.md",
        REPO / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json",
        REPO / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md",
        REPO / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md",
    ]
    paths.extend(sorted((REPO / "docs/canon/founder_approved_sources").glob("*_FOUNDER_APPROVED.*")))
    paths.extend(sorted(p for p in REVIEW.rglob("*") if p.is_file() and p.name != "EIGHT_CANON_PACKAGE_MANIFEST.json"))
    return sorted(set(paths), key=lambda p: str(p.relative_to(REPO)))


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    files = files_to_package()
    for source in files:
        relative = source.relative_to(REPO)
        target = ARTIFACTS / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    records = []
    for path in sorted(p for p in ARTIFACTS.rglob("*") if p.is_file()):
        records.append({
            "path": str(path.relative_to(OUTPUT)),
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
        })
    manifest = {
        "package": "EIGHT_CANON_FOUNDER_APPROVAL_STATUS_RECONCILIATION_PACKAGE_V1_0",
        "disposition": "EIGHT_CANON_FOUNDER_APPROVAL_STATUS_RECONCILIATION_PARTIALLY_COMPLETE_WITH_EXACT_SOURCE_BLOCKERS",
        "artifact_count": len(records),
        "reconciled_rows": 6,
        "blocked_rows": ["C0-035", "C0-023"],
        "rendered_docx": 6,
        "rendered_pages": 251,
        "authority": {
            "implementation": False,
            "schema_or_migration": False,
            "runtime_activation": False,
            "production": False,
            "external_provider_activation": False,
            "public_claims": False,
            "public_launch": False,
            "canon_lock": False,
        },
        "artifacts": records,
    }
    manifest_path = OUTPUT / "EIGHT_CANON_PACKAGE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    review_manifest = REVIEW / "EIGHT_CANON_PACKAGE_MANIFEST.json"
    review_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(p for p in OUTPUT.rglob("*") if p.is_file()):
            archive.write(path, Path(OUTPUT.name) / path.relative_to(OUTPUT))
    digest = sha256(ZIP_PATH)
    SHA_PATH.write_text(f"{digest}  {ZIP_PATH.name}\n", encoding="utf-8")
    record = {
        "package_path": str(ZIP_PATH.relative_to(REPO)),
        "package_sha256": digest,
        "package_size_bytes": ZIP_PATH.stat().st_size,
        "manifest_path": str(manifest_path.relative_to(REPO)),
        "manifest_sha256": sha256(manifest_path),
    }
    (REVIEW / "EIGHT_CANON_EVIDENCE_PACKAGE_RECORD.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
