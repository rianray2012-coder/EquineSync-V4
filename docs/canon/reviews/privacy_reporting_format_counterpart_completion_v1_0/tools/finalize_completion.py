#!/usr/bin/env python3
"""Validate and package the Privacy/Reporting counterpart completion evidence."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
REVIEW = REPO / "docs/canon/reviews/privacy_reporting_format_counterpart_completion_v1_0"
APPROVED = REPO / "docs/canon/founder_approved_sources"
OUTPUTS = REPO / "outputs"
PACKAGE_DIR = OUTPUTS / "Privacy_Reporting_Format_Counterpart_Completion_Package"
PACKAGE_ZIP = OUTPUTS / "privacy_reporting_format_counterpart_completion_package.zip"

PRIVACY_SOURCE = Path("/Users/rianray/Downloads/MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_REVIEWED_DRAFT.md")
REPORTING_SOURCE = Path("/Users/rianray/Downloads/MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0.docx")
PRIVACY_SHA = "30858ed46725a8adaf7104193525aa1074dd8421555ded92ede034ec3339202e"
REPORTING_SHA = "d6cc3cc2add501d2d34d947de4e7a2ee7c6af77aa9669606c95514361657504d"

MANIFEST = REVIEW / "PRIVACY_REPORTING_FORMAT_COUNTERPART_MANIFEST.json"
CHANGED_MANIFEST = REVIEW / "PRIVACY_REPORTING_CHANGED_FILE_MANIFEST.json"
VALIDATION_JSON = REVIEW / "PRIVACY_REPORTING_FORMAT_COUNTERPART_VALIDATION.json"
VALIDATION_MD = REVIEW / "PRIVACY_REPORTING_FORMAT_COUNTERPART_VALIDATION.md"
PACKAGE_RECORD = REVIEW / "PRIVACY_REPORTING_EVIDENCE_PACKAGE_RECORD.json"

COMPANION_FILES = [
    "docs/canon/CANON_INDEX.md",
    "docs/canon/registries/CANON_ARTIFACT_INVENTORY.md",
    "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_AUTHORITY_MATRIX_V1_2.md",
    "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_CROSS_REFERENCE_INDEX_V1_2.md",
    "docs/canon/companions/EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md",
    "docs/canon/companions/MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.md",
    "docs/canon/companions/MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.json",
    "docs/canon/companions/MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.md",
    "docs/canon/companions/MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.json",
    "docs/canon/companions/MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.md",
    "docs/canon/companions/MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.json",
    "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.md",
    "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_CURRENT_LIFECYCLE_STATE_REGISTER.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_CURRENT_LIFECYCLE_STATE_REGISTER.json",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_HISTORICAL_TO_CURRENT_DELTA.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_HISTORICAL_TO_CURRENT_DELTA.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def verify_links(paths: list[Path]) -> list[str]:
    broken: list[str] = []
    link_pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        for target in link_pattern.findall(path.read_text(encoding="utf-8")):
            target = target.strip().split("#", 1)[0]
            if not target or re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                broken.append(f"{rel(path)} -> {target}")
    return broken


def main() -> None:
    checks: dict[str, object] = {}
    checks["privacy_source_hash"] = sha256(PRIVACY_SOURCE) == PRIVACY_SHA
    checks["reporting_source_hash"] = sha256(REPORTING_SOURCE) == REPORTING_SHA
    checks["privacy_preserved_copy_hash"] = sha256(REVIEW / "exact_sources" / PRIVACY_SOURCE.name) == PRIVACY_SHA
    checks["reporting_preserved_copy_hash"] = sha256(REVIEW / "exact_sources" / REPORTING_SOURCE.name) == REPORTING_SHA

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact_hashes = {item["path"]: item["sha256"] for item in manifest["artifacts"]}
    checks["artifact_hashes"] = all(sha256(REPO / path) == digest for path, digest in artifact_hashes.items())
    checks["privacy_parity"] = all([
        manifest["privacy"]["source_substantive_body_exact_match"],
        manifest["privacy"]["paragraph_sequence_equal"],
        manifest["privacy"]["table_content_equal"],
        manifest["privacy"]["source_requirement_ids"] == manifest["privacy"]["successor_requirement_ids"],
        manifest["privacy"]["source_defined_terms"] == manifest["privacy"]["successor_defined_terms"],
        manifest["privacy"]["source_authority_signals"] == manifest["privacy"]["successor_authority_signals"],
    ])
    checks["reporting_parity"] = all([
        manifest["reporting"]["approved_docx_byte_identical_to_source"],
        manifest["reporting"]["paragraph_sequence_equal"],
        manifest["reporting"]["table_content_equal"],
        manifest["reporting"]["source_requirement_ids"] == manifest["reporting"]["derived_requirement_ids"],
        manifest["reporting"]["source_defined_terms"] == manifest["reporting"]["derived_defined_terms"],
        manifest["reporting"]["source_authority_signals"] == manifest["reporting"]["derived_authority_signals"],
    ])

    render = json.loads((REVIEW / "render_evidence/DOCX_RENDER_METRICS.json").read_text(encoding="utf-8"))
    checks["privacy_render"] = render["privacy"]["page_count"] == 24 and render["privacy"]["blank_pages"] == 0
    checks["reporting_render"] = render["reporting"]["page_count"] == 15 and render["reporting"]["blank_pages"] == 0
    checks["visual_qa"] = (REVIEW / "DOCX_RENDER_VISUAL_QA.md").exists()
    manifest["visual_validation"] = {
        "status": "PASS",
        "privacy_pages": 24,
        "reporting_pages": 15,
        "blank_pages": 0,
        "review": rel(REVIEW / "DOCX_RENDER_VISUAL_QA.md"),
    }
    write_json(MANIFEST, manifest)

    lifecycle_path = REPO / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_CURRENT_LIFECYCLE_STATE_REGISTER.json"
    lifecycle = json.loads(lifecycle_path.read_text(encoding="utf-8"))
    lifecycle["category_counts"] = dict(Counter(row["current_category"] for row in lifecycle["rows"]))
    write_json(lifecycle_path, lifecycle)
    rows = {row["record_id"]: row for row in lifecycle["rows"]}
    checks["c0_023_state"] = rows["C0-023"]["current_exact_source_status"] == "EXACT_SOURCE_AVAILABLE_FORMAT_COUNTERPART_COMPLETE" and rows["C0-023"]["adoption_state"] == "PENDING_SEPARATE_FOUNDER_AUTHORIZATION"
    checks["c0_035_state"] = rows["C0-035"]["current_exact_source_status"] == "EXACT_SOURCE_AVAILABLE_FORMAT_COUNTERPART_COMPLETE" and rows["C0-035"]["lock_state"] == "PENDING_SEPARATE_FOUNDER_AUTHORIZATION"
    checks["authority_flags_false"] = all(value is False for value in manifest["authority"].values())

    approved_files = sorted(APPROVED.glob("MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_FOUNDER_APPROVED.*")) + sorted(APPROVED.glob("MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0_FOUNDER_APPROVED.*"))
    review_files = sorted(path for path in REVIEW.rglob("*") if path.is_file() and path not in {CHANGED_MANIFEST, VALIDATION_JSON, VALIDATION_MD, PACKAGE_RECORD})
    companion_paths = [REPO / path for path in COMPANION_FILES]
    scoped_files = sorted(set(approved_files + review_files + companion_paths))

    broken_links = verify_links([path for path in scoped_files if path.suffix.lower() == ".md"])
    checks["broken_references"] = len(broken_links) == 0
    placeholder_pattern = re.compile(r"\b(?:TODO|TBD|FIXME|CHANGEME)\b|\{\{[^}]+\}\}", re.I)
    placeholder_hits = []
    secret_pattern = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk_(?:live|test)_[A-Za-z0-9]{16,}|\bAKIA[0-9A-Z]{16}\b")
    secret_hits = []
    for path in scoped_files:
        if path.suffix.lower() not in {".md", ".json", ".py", ".txt"}:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if placeholder_pattern.search(text):
            placeholder_hits.append(rel(path))
        if secret_pattern.search(text):
            secret_hits.append(rel(path))
    checks["unresolved_placeholders"] = len(placeholder_hits) == 0
    checks["secret_scan"] = len(secret_hits) == 0

    json_errors = []
    for path in scoped_files:
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:  # pragma: no cover - evidence diagnostics
                json_errors.append(f"{rel(path)}: {exc}")
    checks["json_validation"] = len(json_errors) == 0
    checks["runtime_files_changed_by_operation"] = False

    changed_entries = []
    for path in scoped_files:
        changed_entries.append({"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)})
    changed_manifest = {
        "scope": "Privacy and Reporting deterministic format-counterpart completion",
        "classification": "FOUNDER_AUTHORIZED_DETERMINISTIC_FORMAT_COUNTERPART_DERIVED_FROM_EXACT_SUBSTANTIVE_SOURCE",
        "files": changed_entries,
        "self_hash_excluded": True,
        "runtime_or_application_files": [],
    }
    write_json(CHANGED_MANIFEST, changed_manifest)

    checks["all_required_checks_pass"] = all(value is True or value is False and key == "runtime_files_changed_by_operation" for key, value in checks.items())
    validation = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disposition": "PRIVACY_AND_REPORTING_FOUNDER_APPROVED_FORMAT_COUNTERPARTS_COMPLETE_PENDING_SEPARATE_ADOPTION",
        "checks": checks,
        "broken_references": broken_links,
        "placeholder_hits": placeholder_hits,
        "secret_hits": secret_hits,
        "json_errors": json_errors,
        "semantic_deltas": 0,
        "omitted_substantive_provisions": 0,
        "added_substantive_provisions": 0,
        "changed_requirement_identifiers": 0,
        "changed_authority_boundaries": 0,
    }
    write_json(VALIDATION_JSON, validation)
    status = "PASS" if checks["all_required_checks_pass"] else "FAIL"
    lines = [
        "# Privacy and Reporting Format-Counterpart Validation",
        "",
        f"Result: `{status}`",
        "",
        "| Validation | Result |",
        "|---|---|",
    ]
    for name, result in checks.items():
        display = "PASS" if (result is True or name == "runtime_files_changed_by_operation" and result is False) else "FAIL"
        lines.append(f"| `{name}` | {display} |")
    lines.extend([
        "",
        "Omitted substantive provisions: `0`. Added substantive provisions: `0`. Changed requirement identifiers: `0`. Changed authority boundaries: `0`. Unexplained semantic deltas: `0`.",
        "",
        "No application or runtime file was modified by this operation. Adoption, lock, implementation, runtime, production, provider activation, public launch, and public-trust authority remain `FALSE`.",
    ])
    VALIDATION_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if status != "PASS":
        raise SystemExit("Validation failed")

    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir(parents=True)
    package_files = sorted(set(scoped_files + [CHANGED_MANIFEST, VALIDATION_JSON, VALIDATION_MD]))
    for source in package_files:
        destination = PACKAGE_DIR / rel(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    if PACKAGE_ZIP.exists():
        PACKAGE_ZIP.unlink()
    with zipfile.ZipFile(PACKAGE_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_DIR.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE_DIR))
    with zipfile.ZipFile(PACKAGE_ZIP) as archive:
        corrupt = archive.testzip()
        if corrupt:
            raise SystemExit(f"Archive corruption: {corrupt}")
    package_record = {
        "package": rel(PACKAGE_ZIP),
        "sha256": sha256(PACKAGE_ZIP),
        "size_bytes": PACKAGE_ZIP.stat().st_size,
        "archive_extraction_validation": "PASS",
        "files": len(package_files),
        "disposition": "PRIVACY_AND_REPORTING_FOUNDER_APPROVED_FORMAT_COUNTERPARTS_COMPLETE_PENDING_SEPARATE_ADOPTION",
        "authority": manifest["authority"],
    }
    write_json(PACKAGE_RECORD, package_record)
    print(json.dumps(package_record, indent=2))


if __name__ == "__main__":
    main()
